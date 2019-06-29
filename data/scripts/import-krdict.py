#!/usr/bin/python3

import datetime
import glob
import os
import sys
import tzlocal
import xml.etree.ElementTree as ElementTree
import yaml
import zipfile

def do_merge_from_zip(filename, outdir):
    zf = zipfile.ZipFile(filename)
    tz_kst = pytz.timezone('Asia/Seoul')
    for member in zf.namelist():
        s = zf.open(member).read().decode('UTF-8')
        s = xml_workaround(s)
        root = ElementTree.fromstring(s)
        createdString = root.find('GlobalInformation/feat[@att="creationDate"]').get('val')
        created = datetime.datetime.strptime(createdString, '%Y/%m/%d %H:%M:%S')
        datetimestr = tz_kst.localize(created).isoformat()
        entries = root.findall('Lexicon/LexicalEntry')
        for entry in entries:
            do_merge_entry(entry, outdir, datetimestr)

def do_merge_entry(entry, outdir, datetimestr):
    id = int(entry.get('val'))
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
    entry = make_rec(entry, datetimestr)
    filename = find_entry_file(outdir, id, word, pos)
    insert_or_replace_entry(filename, entry)

def insert_or_replace_entry(filename, entry):
  if os.access(filename, os.F_OK):
      k = yaml.load(open(filename).read())
  else:
      k = {}
  if 'imported' not in k:
      k['imported'] = {}
  k['imported']['한국어기초사전'] = entry
  with open(filename, 'w') as fp:
      fp.write(yaml.dump(k, allow_unicode=True, default_flow_style=False, indent=2))

def make_rec(entry, datetimestr):
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

def find_entry_file(outdir, id, word, pos):
    subdir = get_subdir(word)
    dirname = os.path.join(outdir, subdir)
    if not os.access(dirname, os.F_OK):
        os.makedirs(dirname)
    filename_prefix = (word + '__' + pos).replace(' ', '_')
    pattern = os.path.join(outdir, subdir, filename_prefix + '__*.yaml')
    filenames = glob.glob(pattern)
    serial = 1
    while True:
        filename = os.path.join(outdir, subdir, filename_prefix + ('__%03d.yaml' % serial))
        if os.access(filename, os.F_OK):
            print('file: ' + filename)
            k = yaml.load(open(filename).read())
            if 'imported' in k and k['imported'] and '한국어기초사전' in k['imported']:
                if k['imported']['한국어기초사전']['항목ID'] == id:
                    return filename
        else:
            return filename
        serial += 1

def get_subdir(word):
    first = word[0]
    if first == '-':
        first = word[1]
    if ord(first) >= ord('가') and ord(first) <= ord('힣'):
        return chr(ord('가') + ((ord(first) - ord('가')) // 28 * 28))
    else:
        return first

def xml_workaround(s):
    if '<système de chauffage par le sol>' in s:
        s = s.replace('<système de chauffage par le sol>', '&lt;système de chauffage par le sol&gt;')
    return s

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stderr.write('Usage: %s FILENAME.zip\n' % sys.argv[0])
        sys.stderr.write('       %s DIRNAME\n' % sys.argv[0])
        sys.exit(1)
    filename = sys.argv[1]
    outdir = './entries'
    do_merge_from_zip(filename, outdir)
