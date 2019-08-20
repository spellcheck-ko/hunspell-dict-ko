#!/usr/bin/python3

import datetime
import glob
import os
import sys
import pytz
import xml.etree.ElementTree as ElementTree
import yaml
import zipfile

class ImportKrdict:
    def __init__(self, input_filename, outdir):
        self.input_filename = input_filename
        self.outdir = outdir
        self.yaml_output_recently_used = []
        self.yaml_output_cache = {}
        self.yaml_output_cache_max = 5

    def run(self):
        zf = zipfile.ZipFile(self.input_filename)

        members = zf.namelist()
        # 한국어기초사전 zip 파일 내부 XML 파일은 NNNNN_5000.xml,
        # NNNNN_10000.xml, NNNNN_15000.xml, ..., NNNNN_51947 이런 식으로 되어
        # 있는데 번호 순서대로 정렬한다.
        members.sort(key=lambda x : int(x.split('.')[0].split('_')[1]))

        for member in members:
            sys.stdout.write('Processing %s...' % member)
            sys.stdout.flush()
            s = zf.open(member).read().decode('UTF-8')
            self.do_merge_xml_string(s)
            sys.stdout.write('\n')

        sys.stdout.write('Flushing the cache...')
        sys.stdout.flush()
        self.yaml_cache_flush_all()
        sys.stdout.write('\n')

    def do_merge_xml_string(self, xml_str):
        xml_str = self.xml_workaround(xml_str)
        root = ElementTree.fromstring(xml_str)
        createdString = root.find('GlobalInformation/feat[@att="creationDate"]').get('val')
        created = datetime.datetime.strptime(createdString, '%Y/%m/%d %H:%M:%S')
        # 타임스탬프를 한국 시간으로 해석
        datetimestr = pytz.timezone('Asia/Seoul').localize(created).isoformat()
        entries = root.findall('Lexicon/LexicalEntry')
        for entry in entries:
            self.do_merge_entry(entry, datetimestr)

    def do_merge_entry(self, entry, datetimestr):
        krdict_id = int(entry.get('val'))
        tag = entry.find('feat[@att="lexicalUnit"]')
        if tag is None:
            # 사용예 정도로 보이는데 lexicalUnit tag가 없는 경우가 종종 있음
            return
        unit = tag.get('val')
        if unit != "단어":
            # 속담, 관용구 등은 제외
            return
        pos = entry.find('feat[@att="partOfSpeech"]').get('val')
        if pos == '품사 없음':
            # 활용 형태 등 제외
            return
        word = entry.find('Lemma/feat[@att="writtenForm"]').get('val')
        entry = self.make_rec_from_xml_entry(entry, datetimestr)
        yaml_doc = self.yaml_cache_find_yaml_doc(krdict_id, word, pos)
        self.insert_or_replace_entry(yaml_doc, entry)

    def xml_workaround(self, s):
        # 2019/08/13 다운로드 기준
        if '<système de chauffage par le sol>' in s:
            s = s.replace('<système de chauffage par le sol>', '&lt;système de chauffage par le sol&gt;')
        return s

    def yaml_cache_find_yaml_doc(self, krdict_id, word, pos):
        # 첫 음절에서 받침 제외
        if word[0] == '-':
            initial = word[1]
        else:
            initial = word[0]
        n = ord(initial)
        if n >= ord('가') and n <= ord('힣'):
            initial = chr(ord('가') + ((n - ord('가')) // 28 * 28))
        filename = initial + '.yaml'
        docs = self.yaml_cache_open_docs(filename)
        kw_prefix = word + '__' + pos
        last_serial = 0

        for i in range(0,len(docs)):
            doc = docs[i]
            if 'import' in doc and doc['import'] and '한국어기초사전' in doc['import']:
                if doc['import']['한국어기초사전']['항목ID'] == krdict_id:
                    return doc

        for i in range(0,len(docs)):
            doc = docs[i]
            if 'import' in doc and doc['import']:
                kw = doc['000_KEYWORD']
                if kw_prefix == kw[:-5]:
                    last_serial = int(kw[-3:])
                    continue
                elif kw_prefix < kw[:-5]:
                    new_entry = {}
                    new_entry['000_KEYWORD'] = kw_prefix + ('__%03d' % (last_serial + 1))
                    docs.insert(i, new_entry)
                    return new_entry

        new_entry = {}
        new_entry['000_KEYWORD'] = kw_prefix + ('__%03d' % (last_serial + 1))
        docs.append(new_entry)
        return new_entry

    def yaml_cache_clear(self):
        self.yaml_output_recently_used = []
        self.yaml_output_cache = {}

    def yaml_cache_open_docs(self, filename):
        if filename in self.yaml_output_cache:
            self.yaml_output_recently_used.remove(filename)
            self.yaml_output_recently_used.append(filename)
            return self.yaml_output_cache[filename]
        else:
            with open(os.path.join(self.outdir, filename)) as infile:
                sys.stdout.write('r..')
                sys.stdout.flush()
                yaml_docs = list(yaml.load_all(infile, Loader=yaml.FullLoader))
                yaml_docs.sort(key=lambda x : x['000_KEYWORD'])
                self.yaml_output_recently_used.append(filename)
                self.yaml_output_cache[filename] = yaml_docs
            if len(self.yaml_output_cache) > self.yaml_output_cache_max:
                remove_filename = self.yaml_output_recently_used[0]
                self.yaml_cache_flush(remove_filename)
                self.yaml_output_recently_used.remove(remove_filename)
                del self.yaml_output_cache[remove_filename]
            return yaml_docs

    def yaml_cache_flush(self, filename):
        docs = self.yaml_output_cache[filename]
        with open(os.path.join(self.outdir, filename), 'w') as outfile:
            sys.stdout.write('w..')
            sys.stdout.flush()
            yaml.dump_all(docs, outfile, allow_unicode=True, default_flow_style=False, indent=2)

    def yaml_cache_flush_all(self):
        for filename in self.yaml_output_cache:
            self.yaml_cache_flush(filename)

    def insert_or_replace_entry(self, yaml_doc, entry):
        if 'import' not in yaml_doc:
            yaml_doc['import'] = {}
        yaml_doc['import']['한국어기초사전'] = entry

    def make_rec_from_xml_entry(self, entry, datetimestr):
        rec = {}
        rec['항목ID'] = int(entry.get('val'))
        rec['가져온 시각'] = datetimestr
        rec['URL'] = 'https://krdict.korean.go.kr/dicSearch/SearchView?ParaWordNo=%s' % rec['항목ID']
        for item in entry:
            if item.tag == 'feat':
                if item.get('att') == 'homonym_number':
                    rec['동형어 번호'] = int(item.get('val'))
                elif item.get('att') == 'lexicalUnit':
                    rec['구분'] = item.get('val').strip()
                elif item.get('att') == 'partOfSpeech':
                    rec['품사'] = item.get('val').strip()
                elif item.get('att') == 'vocabularyLevel':
                    rec['어휘 등급'] = item.get('val').strip()
                elif item.get('att') == 'subjectCategiory':
                    rec['의미 범주'] = item.get('val').strip()
                elif item.get('att') == 'semanticCategory':
                    rec['주제 및 상황 범주'] = item.get('val').strip()
                elif item.get('att') == 'origin':
                    rec['원어'] = item.get('val').strip()
                elif item.get('att') == 'annotation':
                    rec['전체 참고'] = item.get('val').strip()
                else:
                    raise Exception('Unknown att ' + item.get('att'))
            elif item.tag == 'Lemma':
                for subitem in item:
                    if subitem.get('att') == 'writtenForm':
                        rec['표제어'] = subitem.get('val').strip()
                    elif subitem.get('att') == 'variant':
                        rec['검색용 이형태'] = subitem.get('val').strip()
                    else:
                        raise Exception('Unknown att ' + subitem.get('att'))
            elif item.tag == 'WordForm':
                type = [x.get('val') for x in item if x.get('att') == 'type'][0]
                if type == '발음':
                    if '발음' not in rec:
                        rec['발음'] = []
                    subrec = {}
                    for subitem in item:
                        if subitem.get('att') == 'type':
                            pass
                        elif subitem.get('att') == 'pronunciation':
                            if subitem.get('val'):
                                subrec['발음'] = subitem.get('val').strip()
                            else:
                                subrec['발음'] = ''
                        elif subitem.get('att') == 'sound':
                            subrec['URL'] = subitem.get('val')
                        else:
                            raise Exception('Unknown att ' + subitem.get('att'))
                    rec['발음'].append(subrec)
                elif type == '활용':
                    # '형태;발음;URL', 별개의 발음은 별개 활용에 하나 추가
                    if '활용' not in rec:
                        rec['활용'] = []

                    subrec = {}
                    for subitem in item:
                        if subitem.tag == 'feat':
                            if subitem.get('att') == 'type':
                                pass
                            elif subitem.get('att') == 'writtenForm':
                                if subitem.get('val'):
                                    subrec['형태'] = subitem.get('val').strip()
                                else:
                                    subrec['형태'] = ''
                            elif subitem.get('att') == 'pronunciation':
                                if '발음' in subrec:
                                    rec['활용'].append(subrec)
                                    word = subrec['형태']
                                    subrec = { '형태': word }
                                subrec['발음'] = subitem.get('val').strip()
                            elif subitem.get('att') == 'sound':
                                subrec['발음 URL'] = subitem.get('val').strip()
                            else:
                                raise Exception('Unknown att ' + subitem.get('att'))
                        elif subitem.tag == 'FormRepresentation':
                            rec['활용'].append(subrec)
                            word = subrec['형태']
                            subrec = {}
                            for subsubitem in subitem:
                                if subsubitem.get('att') == 'type':
                                    frtype = subsubitem.get('val')
                                elif subsubitem.get('att') == 'writtenForm':
                                    if subsubitem.get('val'):
                                        subrec['형태'] = subsubitem.get('val').strip()
                                    else:
                                        subrec['형태'] = ''
                                elif subsubitem.get('att') == 'pronunciation':
                                    subrec['발음'] = subsubitem.get('val').strip()
                                elif subsubitem.get('att') == 'sound':
                                    subrec['발음 URL'] = subsubitem.get('val').strip()
                                else:
                                    raise Exception('Unknown att ' + subitem.get('att'))
                            # subrec[frtype] = subsubrec
                            rec['활용'].append(subrec)
                            subrec = {}
                        else:
                            raise Exception('Unknown tag ' + subitem.tag)
                    if subrec:
                        rec['활용'].append(subrec)
                else:
                    raise Exception('Unknown WordForm type ' + type)
            elif item.tag == 'Sense':
                sense = {}
                sense['의미ID'] = int(item.get('val'))
                for subitem in item:
                    if subitem.tag == 'feat':
                        if subitem.get('att') == 'annotation':
                            sense['의미 참고'] = subitem.get('val').strip()
                        elif subitem.get('att') == 'definition':
                            sense['뜻풀이'] = subitem.get('val').strip()
                        elif subitem.get('att') == 'syntacticAnnotation':
                            sense['문형 참고'] = subitem.get('val').strip()
                        elif subitem.get('att') == 'syntacticPattern':
                            sense['문형'] = subitem.get('val').strip()
                        else:
                            raise Exception('Unknown att ' + subitem.get('att'))
                    elif subitem.tag == 'SenseRelation':
                        subsense = {}
                        subsensetype = ''
                        for subsubitem in subitem:
                            if subsubitem.get('att') == 'type':
                                subsensetype = subsubitem.get('val')
                            elif subsubitem.get('att') == 'id':
                                if subsubitem.get('val'):
                                    subsense['항목ID'] = int(subsubitem.get('val'))
                            elif subsubitem.get('att') == 'lemma':
                                if subsubitem.get('val'):
                                    subsense['표제어'] = subsubitem.get('val').strip()
                            elif subsubitem.get('att') == 'homonymNumber':
                                if subsubitem.get('val'):
                                    subsense['동형어 번호'] = int(subsubitem.get('val'))
                            else:
                                raise Exception('Unknown att ' + subsubitem.get('att'))
                        # 내용이 없는 SenseRelation tag가 있으니 내용 여부 확인
                        if subsense:
                            if '관련어:' + subsensetype not in sense:
                                sense['관련어:' + subsensetype] = []
                            sense['관련어:' + subsensetype].append(subsense)
                    elif subitem.tag == 'SenseExample':
                        subtype, example = '', ''
                        for subsubitem in subitem:
                            if subsubitem.get('att') == 'type':
                                subtype = subsubitem.get('val').strip()
                            elif subsubitem.get('att') == 'example':
                                example = subsubitem.get('val').strip()
                            else:
                                raise Exception('Unknown att ' + subitem.get('att'))
                        if subtype == '1':
                            tt = '용례'
                        else:
                            tt = '용례.' + subtype
                        if tt not in sense:
                            sense[tt] = []
                        sense[tt].append(example)
                    elif subitem.tag == 'Multimedia':
                        subtype = ''
                        subsense = {}
                        for subsubitem in subitem:
                            if subsubitem.get('att') == 'type':
                                subtype = subsubitem.get('val').strip()
                            elif subsubitem.get('att') == 'label':
                                subsense['레이블'] = subsubitem.get('val').strip()
                            elif subsubitem.get('att') == 'url':
                                subsense['URL'] = subsubitem.get('val').strip()
                            else:
                                raise Exception('Unknown att ' + subitem.get('att'))
                        if '다중 매체 정보:' + subtype not in sense:
                            sense['다중 매체 정보:' + subtype] = []
                        sense['다중 매체 정보:' + subtype].append(subsense)
                    elif subitem.tag == 'Equivalent':
                        pass
                    else:
                        raise Exception('Unknown subitem tag ' + subitem.tag)
                if '의미' not in rec:
                    rec['의미'] = []
                rec['의미'].append(sense)
        return rec


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stderr.write('Usage: %s FILENAME.zip\n' % sys.argv[0])
        sys.exit(1)
    filename = sys.argv[1]
    outdir = './entries'
    importer = ImportKrdict(filename, outdir)
    importer.run()
