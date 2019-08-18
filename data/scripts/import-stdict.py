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

class ImportStdict:
    def __init__(self, input_filename, outdir):
        self.input_filename = input_filename
        self.outdir = outdir
        self.yaml_output_recently_used = []
        self.yaml_output_cache = {}
        self.yaml_output_cache_max = 5

    def load_white_list(self, infile):
        lines = infile.read().split('\n')
        result = []
        for line in lines:
            if len(line) == 0 or line[0] == '#':
                continue
            fields = line.split(',')
            if len(fields) == 3:
                result.append(int(fields[2]))
        self.white_list = result

    def is_in_white_list(self, id):
        if id in self.white_list:
            self.white_list.remove(id)
            return True
        else:
            return False

    def print_white_list(self):
        for id in self.white_list:
            print(id)

    def run(self):
        zf = zipfile.ZipFile(self.input_filename)

        members = zf.namelist()
        # 표준국어대사전 zip 파일 내부 XML 파일은 NNNNN_5000.xml,
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
        createdString = root.find('lastBuildDate').text
        created = datetime.datetime.strptime(createdString, '%Y%m%d %H:%M:%S')
        # 타임스탬프를 한국 시간으로 해석
        datetimestr = pytz.timezone('Asia/Seoul').localize(created).isoformat()
        entries = root.findall('item')
        for entry in entries:
            self.do_merge_entry(entry, datetimestr)

    def do_merge_entry(self, entry, datetimestr):
        stdict_id = int(entry.find('target_code').text)
        if not self.is_in_white_list(stdict_id):
            return
        tag = entry.find('word_info')
        if tag is None:
            return
        f = tag.find('pos_info/pos')
        if f is None:
            return

        pos = f.text
        # 표준국어대사전은 일부 명사가 '품사 없음'으로 들어 있다. 어차피 화이트리스트로 가져오므로
        # 나중에 manual로 추가할 걸 생각하고 명사로 취급
        if pos == '품사 없음':
            pos = '명사'

        word = self.sanitize_word(entry.find('word_info/word').text)

        entry = self.make_rec_from_xml_entry(entry, datetimestr)
        yaml_doc = self.yaml_cache_find_yaml_doc(stdict_id, word, pos)
        self.insert_or_replace_entry(yaml_doc, entry)

    def xml_workaround(self, s):
        return s

    def sanitize_word(self, word):
        word = word[:1] + word[1:].replace('-','').replace('^','')
        m = re.match('^([^0-9]+)[0-9]*', word)
        return m.group(1)

    def yaml_cache_find_yaml_doc(self, stdict_id, word, pos):
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
            if 'import' in doc and doc['import'] and '표준국어대사전' in doc['import']:
                if doc['import']['표준국어대사전']['항목ID'] == stdict_id:
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
        yaml_doc['import']['표준국어대사전'] = entry

    def make_rec_from_xml_entry(self, entry, datetimestr):
        rec = {}
        rec['항목ID'] = int(entry.find('target_code').text)
        rec['가져온 시각'] = datetimestr
        rec['URL'] = 'https://stdict.korean.go.kr/search/searchView.do?word_no=%d&searchKeywordTo=3' % rec['항목ID']
        word_info = entry.find('word_info')
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
            elif item.tag == 'origin':
                rec['어원'] = item.text
            elif item.tag == 'conju_info':
                if '활용' not in rec:
                    rec['활용'] = []
                subrecord = {}
                for subitem in item:
                    if subitem.tag == 'conjugation_info':
                        for subsubitem in subitem:
                            if subsubitem.tag == 'conjugation':
                                subrecord['활용'] = subsubitem.text
                            else:
                                raise Exception('Unknown conjugation_info subitem tag ' + subsubitem.tag)
                    elif subitem.tag == 'abbreviation_info':
                        for subsubitem in subitem:
                            if subsubitem.tag == 'abbreviation':
                                subrecord['약어'] = subsubitem.text
                            else:
                                raise Exception('Unknown abbreviation_info subitem tag ' + subsubitem.tag)
                    else:
                        raise Exception('Unknown conju_info subitem tag ' + subitem.tag)
                rec['활용'].append(subrecord)
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
            elif item.tag == 'pos_info':
                if '의미' not in rec:
                    rec['의미'] = []
                subrecord = {}
                subrecord['품사'] = item.find('pos').text
                for subitem in item.find('comm_pattern_info'):
                    if subitem.tag == 'sense_info':
                        for subsubitem in subitem:
                            if subsubitem.tag == 'type':
                                subrecord['종류'] = subsubitem.text
                            elif subsubitem.tag == 'definition':
                                subrecord['뜻풀이'] = subsubitem.text
                            elif subsubitem.tag == 'example_info':
                                for subsubsubitem in subsubitem:
                                    # 출처가 표시된 예제는 독점적 저작권이 있는 출처의 문헌, 제외한다
                                    if subsubsubitem.find('source') is not None:
                                        if subsubsubitem.tag == 'example':
                                            if '용례' not in subrecord:
                                                subrecord['용례'] = []
                                            subrecord['용례'].append(subsubsubitem.text)
                                        else:
                                            raise Exception('Unknown example_info subitem tag ' + subsubsubitem.tag)
                            elif subsubitem.tag == 'cat_info':
                                for subsubsubitem in subsubitem:
                                    if subsubsubitem.tag == 'cat':
                                        subrecord['분류'] = subsubsubitem.text
                                    else:
                                        raise Exception('Unknown cat_info subitem tag ' + subsubsubitem.tag)
                            elif subsubitem.tag == 'multimedia_info':
                                # 멀티미디어 자료는 십중팔구 non-free이지만, 링크만 포함하므로 포함
                                if '멀티미디어' not in subrecord:
                                    subrecord['멀티미디어'] = []
                                subsubrecord = {}
                                for subsubsubitem in subsubitem:
                                    if subsubsubitem.tag == 'label':
                                        subsubrecord['레이블'] = subsubsubitem.text
                                    elif subsubsubitem.tag == 'type':
                                        subsubrecord['종류'] = subsubsubitem.text
                                    elif subsubsubitem.tag == 'link':
                                        subsubrecord['URL'] = subsubsubitem.text
                                    else:
                                        raise Exception('Unknown multimedia_info subitem tag ' + subsubsubitem.tag)
                                subrecord['멀티미디어'].append(subsubrecord)
                            elif subsubitem.tag == 'scientific_name':
                                subrecord['학명'] = subsubitem.text
                            elif subsubitem.tag == 'sense_pattern_info':
                                for subsubsubitem in subsubitem:
                                    if subsubsubitem.tag == 'pattern':
                                        subrecord['형태'] = subsubsubitem.text
                                    else:
                                        raise Exception('Unknown cat_info subitem tag ' + subsubsubitem.tag)
                            elif subsubitem.tag == 'sense_grammar_info':
                                for subsubsubitem in subsubitem:
                                    if subsubsubitem.tag == 'grammar':
                                        subrecord['문법'] = subsubitem.text
                                    else:
                                        raise Exception('Unknown cat_info subitem tag ' + subsubsubitem.tag)
                            else:
                                raise Exception('Unknown sense_info subitem tag ' + subsubitem.tag)
                    elif subitem.tag == 'pattern_info':
                        for subsubitem in subitem:
                            if subsubitem.tag == 'pattern':
                                subrecord['형태'] = subsubitem.text
                            else:
                                raise Exception('Unknown pattern_info subitem tag ' + subsubitem.tag)
                    elif subitem.tag == 'grammar_info':
                        for subsubitem in subitem:
                            if subsubitem.tag == 'grammar':
                                subrecord['문법'] = subsubitem.text
                            else:
                                raise Exception('Unknown grammar_info subitem tag ' + subsubitem.tag)
                rec['의미'].append(subrecord)
            else:
                print(rec['항목ID'])
                raise Exception('Unknown tag ' + item.tag)
        return rec


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.stderr.write('Usage: %s FILENAME.zip whitelist.txt\n' % sys.argv[0])
        sys.exit(1)
    zip_filename = sys.argv[1]
    list_filename = sys.argv[2]
    outdir = './entries'
    importer = ImportStdict(zip_filename, outdir)
    importer.load_white_list(open(list_filename))
    importer.run()
    importer.print_white_list()
