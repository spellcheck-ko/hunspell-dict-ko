#!/usr/bin/python3

import datetime
import glob
import os
import pytz
import re
import sys
import xml.etree.ElementTree as ElementTree
import yaml
import zipfile

class ImportOpendict:
    def __init__(self, input_filename, outdir):
        self.input_filename = input_filename
        self.outdir = outdir
        self.yaml_output_recently_used = []
        self.yaml_output_cache = {}
        self.yaml_output_cache_max = 5

    def load_white_list(self, infile):
        lines = infile.read().split('\n')
        result = {}
        for line in lines:
            if len(line) == 0 or line[0] == '#':
                continue
            fields = line.split(',')
            if len(fields) == 3:
                result[int(fields[2])] = fields
        self.white_list = result

    def get_white_list(self, id):
        if id in self.white_list:
            result = self.white_list[id]
            del self.white_list[id]
            return result
        else:
            return None

    def print_white_list(self):
        for entry in self.white_list.values():
            print('%s' % str(entry))

    def run(self):
        zf = zipfile.ZipFile(self.input_filename)

        members = zf.namelist()

        # zip 파일 내부 XML 파일은 NNNNN_5000.xml, NNNNN_10000.xml,
        # NNNNN_15000.xml, ..., NNNNN_51947 이런 식으로 되어 있는데 번호
        # 순서대로 정렬한다.
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
        createdString = root.find('lastBuildDate').text
        created = datetime.datetime.strptime(createdString, '%Y%m%d%H%M%S')
        # 타임스탬프를 한국 시간으로 해석
        datetimestr = pytz.timezone('Asia/Seoul').localize(created).isoformat()
        entries = root.findall('item')
        for entry in entries:
            self.do_merge_entry(entry, datetimestr)

    def do_merge_entry(self, entry, datetimestr):
        opendict_id = int(entry.find('target_code').text)
        white_item = self.get_white_list(opendict_id)
        if white_item is None:
            return
        white_pos = white_item[1]
        # FIXMEFIXMEFIXME

        word = self.sanitize_word(entry.find('wordInfo/word').text)
        pos_tag = entry.find('senseInfo/pos')
        if pos_tag is None:
            pos = white_pos
        else:
            pos = pos_tag.text
            if pos == '관·명':
                pos = '명사'
        entry = self.make_rec_from_xml_entry(entry, datetimestr)
        yaml_doc = self.yaml_cache_find_yaml_doc(opendict_id, word, pos)
        self.insert_or_replace_entry(yaml_doc, entry)

    def xml_workaround(self, s):
        return s

    def sanitize_word(self, word):
        word = word[:1] + word[1:].replace('-','').replace('^','')
        m = re.match('^([^0-9]+)[0-9]*', word)
        return m.group(1)

    def yaml_cache_find_yaml_doc(self, opendict_id, word, pos):
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
            if 'import' in doc and doc['import'] and '우리말샘' in doc['import']:
                if doc['import']['우리말샘']['항목ID'] == opendict_id:
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
        yaml_doc['import']['우리말샘'] = entry

    def make_rec_from_xml_entry(self, entry, datetimestr):
        rec = {}
        rec['항목ID'] = int(entry.find('target_code').text)
        rec['가져온 시각'] = datetimestr
        rec['URL'] = entry.find('link').text
        word_info = entry.find('wordInfo')
        sense_info = entry.find('senseInfo')

        for item in word_info:
            if item.tag == 'word':
                rec['표제어'] = item.text
            elif item.tag == 'word_unit':
                rec['구분'] = item.text
            elif item.tag == 'word_type':
                rec['종류'] = item.text
            elif item.tag == 'original_language_info':
                rec['원어'] = {}
                for subitem in item:
                    if subitem.tag == 'original_language':
                        rec['원어']['원어'] = subitem.text
                    elif subitem.tag == 'language_type':
                        rec['원어']['언어'] = subitem.text
                    else:
                        raise Exception('Unknown original_language_info subitem tag ' + subitem.tag)
            elif item.tag == 'pronunciation_info':
                if '발음' not in rec:
                    rec['발음'] = []
                for subitem in item:
                    if subitem.tag == 'pronunciation':
                        rec['발음'].append(subitem.text)
                    else:
                        raise Exception('Unknown pronunciation_info subitem tag ' + subitem.tag)
            elif item.tag == 'conju_info':
                if '활용' not in rec:
                    rec['활용'] = []
                subrecord = {}
                for subitem in item:
                    if subitem.tag == 'conjugation_info':
                        for subsubitem in subitem:
                            if subsubitem.tag == 'conjugation':
                                subrecord['활용'] = subsubitem.text
                            elif subsubitem.tag == 'pronunciation_info':
                                for subsubsubitem in subsubitem:
                                    if subsubsubitem.tag == 'pronunciation':
                                        if '발음' not in subrecord:
                                            subrecord['발음'] = []
                                        subrecord['발음'].append(subsubsubitem.text)
                                    else:
                                        raise Exception('Unknown conju_info/pronunciation_info subitem tag ' + subitem.tag)
                            else:
                                raise Exception('Unknown conjugation_info_info subitem tag ' + subitem.tag)
                    elif subitem.tag == 'abbreviation_info':
                        for subsubitem in subitem:
                            if subsubitem.tag == 'abbreviation':
                                subrecord['약어'] = subsubitem.text
                            elif subsubitem.tag == 'pronunciation_info':
                                for subsubsubitem in subsubitem:
                                    if subsubsubitem.tag == 'pronunciation':
                                        if '약어 발음' not in subrecord:
                                            subrecord['약어 발음'] = []
                                        subrecord['약어 발음'].append(subsubsubitem.text)
                                    else:
                                        raise Exception('Unknown conju_info/abbreviation_info subitem tag ' + subitem.tag)
                            else:
                                raise Exception('Unknown conjugation_info_info subitem tag ' + subitem.tag)
                    else:
                        raise Exception('Unknown conju_info subitem tag ' + subitem.tag)
                rec['활용'].append(subrecord)
            elif item.tag == 'origin':
                rec['어원'] = item.text
            else:
                raise Exception('Unknown wordInfo subitem tag ' + item.tag)

        for item in sense_info:
            if item.tag == 'sense_no':
                rec['의미 번호'] = int(item.text)
            elif item.tag == 'pos':
                if item.tag == '관·명':
                    rec['품사'] = '명사'
                else:
                    rec['품사'] = item.text
            elif item.tag == 'type':
                rec['종류'] = item.text
            elif item.tag == 'definition':
                rec['뜻풀이'] = item.text
            elif item.tag == 'cat_info':
                for subitem in item:
                    if subitem.tag == 'cat':
                        rec['분류'] = subitem.text
                    else:
                        raise Exception('Unknown cat_info subitem tag ' + subitem.tag)
            elif item.tag == 'translation_info':
                if '번역' not in rec:
                    rec['번역'] = []
                subrecord = {}
                for subitem in item:
                    if subitem.tag == 'translation':
                        subrecord['번역'] = subitem.text
                    elif subitem.tag == 'language_type':
                        subrecord['언어'] = subitem.text
                    else:
                        raise Exception('Unknown translation_info subitem tag ' + subitem.tag)
                rec['번역'].append(subrecord)
            elif item.tag == 'example_info':
                # 출처가 명시된 예문은 수정 재배포 불가능하므로 제외
                source_tag = item.find('source')
                if source_tag is not None:
                    continue

                if '용례' not in rec:
                    rec['용례'] = []
                subrec = {}
                for subitem in item:
                    if subitem.tag == 'example':
                        subrec['용례'] = subitem.text
                    else:
                        raise Exception('Unknown example_info subitem tag ' + subitem.tag)
                rec['용례'].append(subrec)
            elif item.tag == 'relation_info':
                if '관련어' not in rec:
                    rec['관련어'] = []
                subrecord = {}
                for subitem in item:
                    if subitem.tag == 'word':
                        subrecord['표제어'] = subitem.text
                    elif subitem.tag == 'type':
                        subrecord['종류'] = subitem.text
                    elif subitem.tag == 'link_target_code':
                        subrecord['항목ID'] = int(subitem.text)
                    elif subitem.tag == 'link':
                        subrecord['URL'] = subitem.text
                    else:
                        raise Exception('Unknown relation_info subitem tag ' + subitem.tag)
                rec['관련어'].append(subrecord)
            elif item.tag == 'multimedia_info':
                # 멀티미디어 자료는 십중팔구 non-free이지만, 링크만 포함하므로 포함
                if '멀티미디어' not in rec:
                    rec['멀티미디어'] = []
                subrecord = {}
                for subsubitem in subitem:
                    if subsubitem.tag == 'label':
                        subrecord['레이블'] = subsubitem.text
                    elif subsubitem.tag == 'type':
                        subrecord['종류'] = subsubitem.text
                    elif subsubitem.tag == 'link':
                        subrecord['URL'] = subsubitem.text
                    else:
                        raise Exception('Unknown multimedia_info subitem tag ' + subsubitem.tag)
                rec['멀티미디어'].append(subrecord)
            elif item.tag == 'pattern_info':
                if '용례' not in rec:
                    rec['용례'] = []
                subrecord = {}
                for subitem in subitem:
                    if subitem.tag == 'pattern':
                        subrecord['용례'] = subitem.text
                    elif subitem.tag == 'conjugation':
                        subrecord['활용'] = subitem.text
                    elif subitem.tag == 'pronunciation':
                        subrecord['발음'] = subitem.text
                    elif subitem.tag == 'pronunciation_info':
                        for subsubitem in subitem:
                            if subsubitem.tag == 'pronunciation':
                                subrecord['발음'] = subsubitem.text
                            else:
                                raise Exception('Unknown pattern_info/pronunciation_info subitem tag ' + subsubitem.tag)                            
                    else:
                        raise Exception('Unknown pattern_info subitem tag ' + subitem.tag)
                rec['용례'].append(subrecord)
            elif item.tag == 'grammar_info':
                for subitem in subitem:
                    if subitem.tag == 'grammar':
                        rec['문법'] = subitem.text
                    else:
                        raise Exception('Unknown grammar_info subitem tag ' + subitem.tag)
            elif item.tag == 'proverb_info':
                if '속담' not in rec:
                    rec['속담'] = []
                subrecord = {}
                for subitem in item:
                    if subitem.tag == 'word':
                        subrecord['표제어'] = subitem.text
                    elif subitem.tag == 'definition':
                        subrecord['뜻풀이'] = subitem.text
                    elif subitem.tag == 'type':
                        subrecord['종류'] = subitem.text
                    elif subitem.tag == 'link_target_code':
                        subrecord['항목ID'] = int(subitem.text)
                    elif subitem.tag == 'link':
                        subrecord['URL'] = subitem.text
                    else:
                        raise Exception('Unknown proverb_info tag ' + subitem.tag)
                rec['속담'].append(subrecord)
            elif item.tag == 'region_info':
                for subitem in item:
                    if subitem.tag == 'region':
                        rec['지역'] = subitem.text
                    else:
                        raise Exception('Unknown region_info tag ' + subitem.tag)
            elif item.tag == 'history_info':
                if '변화' not in rec:
                    rec['변화'] = []
                subrecord = {}
                for subitem in item:
                    if subitem.tag == 'word_form':
                        subrecord['단어 형태'] = subitem.text
                    elif subitem.tag == 'desc':
                        subrecord['설명'] = subitem.text
                    elif subitem.tag == 'allomorph':
                        subrecord['이형'] = subitem.text
                    elif subitem.tag == 'history_sense_info':
                        if '문헌' not in subrecord:
                            subrecord['문헌'] = []
                        subsubrecord = {}
                        for subsubitem in subitem:
                            if subsubitem.tag == 'history_century_info':
                                for subsubsubitem in subsubitem:
                                    if subsubsubitem.tag == 'century':
                                        subsubrecord['세기'] = subsubsubitem.text
                                    elif subsubsubitem.tag == 'mark':
                                        subsubrecord['강조'] = subsubsubitem.text
                                    elif subsubsubitem.tag == 'history_example_info':
                                        if '용례' not in subsubrecord:
                                            subsubrecord['용례'] = []
                                        subsubsubrecord = {}
                                        for subsubsubsubitem in subsubsubitem:
                                            if subsubsubsubitem.tag == 'example':
                                                subsubsubrecord['용례'] = subsubsubsubitem.text
                                            elif subsubsubsubitem.tag == 'source':
                                                subsubsubrecord['문헌'] = subsubsubsubitem.text
                                            else:
                                                raise Exception('Unknown history_example_info tag ' + subsubsubsubitem.tag)
                                        subsubrecord['용례'].append(subsubsubrecord)
                                    else:
                                        raise Exception('Unknown history_century_info tag ' + subsubsubitem.tag)
                            else:
                                raise Exception('Unknown history_sense_info tag ' + subsubitem.tag)
                        subrecord['문헌'].append(subsubrecord)
                    else:
                        raise Exception('Unknown region_info tag ' + subitem.tag)
                rec['변화'].append(subrecord)
            elif item.tag == 'sl_info_link':
                rec['수어 URL'] = item.text
            elif item.tag == 'norm_info':
                subrecord = {}
                for subitem in item:
                    if subitem.tag == 'type':
                        subrecord['종류'] = subitem.text
                    elif subitem.tag == 'role':
                        subrecord['근거'] = subitem.text
                    elif subitem.tag == 'desc':
                        subrecord['설명'] = subitem.text
                    else:
                        raise Exception('Unknown norm_info tag ' + item.tag)
                rec['순화 정보'] = subrecord
            elif item.tag == 'scientific_name':
                rec['학명'] = item.text
            else:
                raise Exception('Unknown senseInfo tag ' + item.tag)

        return rec


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.stderr.write('Usage: %s FILENAME.zip whitelist.txt\n' % sys.argv[0])
        sys.exit(1)
    zip_filename = sys.argv[1]
    list_filename = sys.argv[2]
    outdir = './entries'
    importer = ImportOpendict(zip_filename, outdir)
    importer.load_white_list(open(list_filename))
    importer.run()
    importer.print_white_list()
