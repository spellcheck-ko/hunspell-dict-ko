import copy
import glob
import os
import re
import sys
import unicodedata
import yaml

from jamo import *

class ProcessYamlDocs:
    def __init__(self, yaml_dir):
        self.entries_dir = entries_dir

    def run(self):
        filenames = glob.glob(os.path.join(self.entries_dir, '*.yaml'))
        filenames.sort()
        for filename in filenames:
            self.process_file(filename)

    def process_file(self, filename):
        print('Processing %s...' % filename)
        docs = list(yaml.load_all(open(filename)))
        docs.sort(key=lambda x : x['000_KEYWORD'])
        for doc in docs:
            self.process_doc(doc)
        with open(filename, 'w') as outfile:
            yaml.dump_all(docs, outfile, allow_unicode=True,
                          default_flow_style=False, indent=2)

    def process_doc(self, doc):
        if 'import' in doc:
            self.process_doc_import(doc)
        self.process_doc_manual(doc)

    def process_doc_import(self, doc):
        supported = [ x in doc for x in [ '한국어기초사전', '표준국어대사전', '우리말샘', '갈퀴 Django'] ]
        if supported:
            if 'import_derived' not in doc:
                doc['import_derived'] = {}

            doc['import_derived']['맞춤법 검사'] = {}
            output = doc['import_derived']['맞춤법 검사']

            if '한국어기초사전' in doc['import']:
                input = doc['import']['한국어기초사전']
                self.process_doc_krdict(input, output)
            elif '표준국어대사전' in doc['import']:
                input = doc['import']['표준국어대사전']
                self.process_doc_stdict(input, output)
            elif '우리말샘' in doc['import']:
                input = doc['import']['우리말샘']
                # if '품사' not in input and 'manual' not in doc:
                #     doc['manual'] = { '맞춤법 검사': { '품사': '명사' } }
                self.process_doc_opendict(input, output)
            elif '갈퀴 Django' in doc['import']:
                input = doc['import']['갈퀴 Django']
                self.process_doc_galkwidjango(input, output)
        else:
            sys.stderr.write('Warning: unknown import: %s\n' % str(doc))

    def process_doc_krdict(self, input, output):
        if input['의미'][0]['뜻풀이'].startswith('→'):
            output['제외'] = '틀린 말'
        elif input['품사'] in ['어미', '접사']:
            output['제외'] = '해당 품사 아님'
        else:
            word = input['표제어']
            pos = input['품사']
            output['표제어'] = word
            output['품사'] = pos

            props = []

            # 불규칙 활용
            if pos in ['동사', '형용사', '보조 형용사', '보조 동사']:
                if '활용' in input:
                    inflections = [dd['형태'] for dd in input['활용'] if '형태' in dd]
                    inflection_type = self.detect_inflection_type(word, inflections)
                    if inflection_type is not None and inflection_type != '규칙':
                        props.append(inflection_type)

            # 보조용언 타입
            if pos.startswith('보조 '):
                clue = input['의미'][0]['참고']
                detected = self.detect_aux_verb_type(word, clue)
                props += detected

            # 합성용언
            if pos in ['동사', '형용사']:
                if self.detect_compound_verb(word):
                    props.append('용언합성')

            if pos in ['명사', '의존 명사']:
                if '주제 및 상황 범주' in input and input['주제 및 상황 범주'] == '개념 > 세는 말':
                    props.append('단위명사')

            # 조사 문법
            if pos == '조사':
                clues = []
                if '참고' in input:
                    for sentence in input['참고'].split('.'):
                        sentence = sentence.strip()
                        if len(sentence) > 0:
                            clues.append(sentence)
                for m in input['의미']:
                    if '참고' in m:
                        for sentence in m['참고'].split('.'):
                            sentence = sentence.strip()
                            if len(sentence) > 0:
                                clues.append(sentence)
                if len(clues) == 0:
                    # 문법이 없으면 일반적인 체언 뒤에 붙는 것으로 가정한다
                    output['조사 조합'] = ['체언']
                else:
                    josa_combinations = self.detect_josa_combination_krdict(clues)
                    if len(josa_combinations) > 0:
                        output['조사 조합'] = josa_combinations
                    else:
                        output['제외'] = '조사 문법 정보 부족'

            if len(props) > 0:
                props.sort()
                if '속성' not in output:
                    output['속성'] = []
                output['속성'] += props

    def process_doc_stdict(self, input, output):
        word = self.stdict_sanitize_word(input['표제어'])
        pos = input['의미'][0]['품사']

        if input['의미'][0]['뜻풀이'].startswith('→'):
            output['제외'] = '틀린 말'
        elif pos in ['어미', '접사', '조사']:
            output['제외'] = '해당 품사 아님'
        else:
            output['표제어'] = word
            output['품사'] = pos

            props = []

            # 불규칙 활용
            if pos in ['동사', '형용사', '보조 형용사', '보조 동사']:
                if '활용' in input:
                    inflections = [dd['활용'] for dd in input['활용']]
                    inflection_type = self.detect_inflection_type(word, inflections)
                    if inflection_type is not None and inflection_type != '규칙':
                        props.append(inflection_type)

            # 보조용언 타입
            if pos.startswith('보조 '):
                if '문법' in input['의미'][0]:
                    clue = input['의미'][0]['문법']
                    detected = self.detect_aux_verb_type(word, clue)
                    props += detected
                else:
                    raise Exception('word: %s, pos: %s, but no 문법' % (word, pos))

            # 합성용언
            if pos in ['동사', '형용사']:
                if self.detect_compound_verb(word):
                    props.append('용언합성')

            if pos in ['명사', '의존 명사']:
                if '주제 및 상황 범주' in input and input['주제 및 상황 범주'] == '개념 > 세는 말':
                    props.append('단위명사')

            if len(props) > 0:
                props.sort()
                if '속성' not in output:
                    output['속성'] = []
                output['속성'] += props

    def process_doc_opendict(self, input, output):
        word = self.stdict_sanitize_word(input['표제어'])
        if '품사' in input:
            pos = input['품사']
        else:
            pos = '품사 없음'

        if '⇒규범 표기는 \‘' in input['뜻풀이']:
            output['제외'] = '틀린 말'
        elif pos in ['어미', '접사', '조사']:
            output['제외'] = '해당 품사 아님'
        else:
            output['표제어'] = word
            output['품사'] = pos

            props = []

            # 불규칙 활용
            if pos in ['동사', '형용사', '보조 형용사', '보조 동사']:
                if '활용' in input:
                    inflections = [dd['활용'] for dd in input['활용']]
                    inflection_type = self.detect_inflection_type(word, inflections)
                    if inflection_type is not None and inflection_type != '규칙':
                        props.append(inflection_type)

            # 보조용언 타입
            if pos.startswith('보조 '):
                if '문법' in input:
                    clue = input['문법']
                    detected = self.detect_aux_verb_type(word, clue)
                    props += detected
                else:
                    raise Exception('word: %s, pos: %s, but no 문법' % (word, pos))

            # 합성용언
            if pos in ['동사', '형용사']:
                if self.detect_compound_verb(word):
                    props.append('용언합성')

            if pos in ['명사', '의존 명사']:
                if '뜻풀이' in input and '세는 단위' in input['뜻풀이']:
                    props.append('단위명사')

            if len(props) > 0:
                props.sort()
                if '속성' not in output:
                    output['속성'] = []
                output['속성'] += props

    def process_doc_galkwidjango(self, input, output):
        word = input['표제어']
        output['표제어'] = word

        pos = input['품사']
        pos_simplified = input['품사'].split(':')[0]
        if pos_simplified in ['특수']:
            output['품사'] = pos
        else:
            output['품사'] = pos_simplified

        if '속성' in input:
            props = copy.deepcopy(input['속성'])
        else:
            props = []

        if pos_simplified in ['동사', '형용사']:
            if '용언합성' not in props:
                if self.detect_compound_verb(word):
                    props.append('용언합성')
        if len(props) > 0:
            props.sort()
            output['속성'] = props

    def process_doc_manual(self, doc):
        if 'manual' not in doc:
            doc['result'] = doc['import_derived']
            del doc['import_derived']
        elif 'import_derived' in doc and '맞춤법 검사' in doc['import_derived']:
            doc['result'] = {}
            if '맞춤법 검사' in doc['manual'] and '제외' in doc['manual']['맞춤법 검사']:
                doc['result']['맞춤법 검사'] = copy.deepcopy(doc['manual']['맞춤법 검사'])
            else:
                entry = copy.deepcopy(doc['import_derived']['맞춤법 검사'])
                for key in doc['manual']['맞춤법 검사'].keys():
                    entry[key] = copy.deepcopy(doc['manual']['맞춤법 검사'][key])
                doc['result']['맞춤법 검사'] = entry

    def stdict_sanitize_word(self, word):
        word = word[:1] + word[1:].replace('-','').replace('^','')
        m = re.match('^([^0-9]+)[0-9]*', word)
        return m.group(1)

    def detect_inflection_type(self, word, inflections):
        if not word.endswith('다'):
            print('어라? %s' % word)
            return None

        nfd = unicodedata.normalize('NFD', word[:-1])

        # 불규칙 활용이 가능한 형태마다 가능한 불규칙형태와 규칙형태를
        # 만들어서 '활용'에 들어있는지 확인한다.

        # - '어/아'같은 어미 같은 경우 모음조화에 따라 붙여야 맞겠지만 활용
        # 정보에 어떻게든 하나만 들어 있으면 확인되니 자세한 구현은 넘어간다

        if nfd[-2:] == L_RIEUL + V_EU:
            #  '르' 앞 음절이 종성으로 끝나면 규칙?
            if unicodedata.normalize('NFC', nfd[:-2] + T_RIEUL) + '러' in inflections:
                result = '르불규칙'
            elif unicodedata.normalize('NFC', nfd[:-2] + T_RIEUL) + '라' in inflections:
                result = '르불규칙'
            elif word[:-1] + '러' in inflections:
                result = '러불규칙'
            elif word[:-1] + '라' in inflections:
                result = '러불규칙'
            elif unicodedata.normalize('NFC', nfd[:-1] + V_EO) in inflections:
                result = None
            elif unicodedata.normalize('NFC', nfd[:-1] + V_A) in inflections:
                result = None
            elif ord(nfd[-3]) >= ord(T_KIYEOK) and ord(nfd[-3]) <= ord(T_HIEUH):
                # 종성일 경우,
                # '-ㄹ르다'처럼 '르' 앞에 종성이 있으면 르불규칙이 될 수 없고
                # '-ㄹ르러' 처럼 되기도 어려워 보이므로 규칙활용 '-ㄹ러'일 것이다
                result = None
            else:
                result = '르/러불규칙 미확정'
        elif nfd[-1] == T_TIKEUT:
            if unicodedata.normalize('NFC', nfd[:-1] + T_RIEUL) + '어' in inflections:
                result = 'ㄷ불규칙'
            elif unicodedata.normalize('NFC', nfd[:-1] + T_RIEUL) + '아' in inflections:
                result = 'ㄷ불규칙'
            elif word[:-1] + '어' in inflections:
                result = None
            elif word[:-1] + '아' in inflections:
                result = None
            else:
                result = 'ㄷ불규칙 미확정'
        elif nfd[-1] == T_PIEUP:
            if unicodedata.normalize('NFC', nfd[:-1]) + '워' in inflections:
                result = 'ㅂ불규칙'
            elif unicodedata.normalize('NFC', nfd[:-1]) + '와' in inflections:
                result = 'ㅂ불규칙'
            elif unicodedata.normalize('NFC', nfd[:-1]) + '운' in inflections:
                result = 'ㅂ불규칙'
            elif word[:-1] + '어' in inflections:
                result = None
            elif word[:-1] + '아' in inflections:
                result = None
            else:
                result = 'ㅂ불규칙 미확정'
            pass
        elif nfd[-1] == T_SIOS:
            if unicodedata.normalize('NFC', nfd[:-1]) + '어' in inflections:
                result = 'ㅅ불규칙'
            elif unicodedata.normalize('NFC', nfd[:-1]) + '아' in inflections:
                result = 'ㅅ불규칙'
            elif word[:-1] + '어' in inflections:
                result = None
            elif word[:-1] + '아' in inflections:
                result = None
            else:
                result = 'ㅅ불규칙 미확정'
        elif nfd[-1] == T_HIEUH:
            if unicodedata.normalize('NFC', nfd[:-1] + T_NIEUN) in inflections:
                result = 'ㅎ불규칙'
            elif unicodedata.normalize('NFC', nfd[:-2] + V_AE) in inflections:
                result = 'ㅎ불규칙'
            elif unicodedata.normalize('NFC', nfd[:-2] + V_E) in inflections:
                result = 'ㅎ불규칙'
            elif word[:-1] + '은' in inflections:
                result = None
            elif word[:-1] + '아' in inflections:
                result = None
            elif word[:-1] + '어' in inflections:
                result = None
            elif word[-1] == '렇' or word[-1] == '랗':
                # '-렇다', '-랗다'는 불규칙
                result = 'ㅎ불규칙'
            else:
                result = 'ㅎ불규칙 미확정'
        else:
            result = None

        return result


    def detect_aux_verb_type(self, word, clue):
        props = []
        examples = None
        clue = clue.replace('‘','\'').replace('’','\'')
        if '뒤에서 ' in clue:
            examples = clue.split('뒤에서 ')[1].split('\'')[1::2]
        elif '뒤에 ' in clue:
            examples = clue.split('뒤에 ')[1].split('\'')[1::2]
        if examples is not None and len(examples) > 0:
            for example in examples:
                if example.endswith(word):
                    example = example[:-len(word)]
                prefixes = example.split(' ')[0].split('/')
                for prefix in prefixes:
                    if prefix[0] != '-':
                        prefix = '-' + prefix
                    if prefix in ['-ㄴ', '-는', '-ㅁ']:
                        continue
                    props.append('보조용언:' + prefix)
        else:
            if word == '드리다':
                props.append('보조용언:-어')
        return props


    def detect_compound_verb(self, word):
        if len(word) < 4:
            return False
        suspected = False
        if word.endswith('가다') or  word.endswith('보내다') or word.endswith('오다') or word.endswith('주다') or word.endswith('치다') or word.endswith('놓다') or word.endswith('내다'):
            suspected = True
        if word.endswith('지다') and not word.endswith('빠지다'):
            suspected = True

        if suspected:
            prefix_nfd = unicodedata.normalize('NFD', word[:-2])
            if prefix_nfd[-1] in [V_A, V_AE, V_E, V_EO]:
                return True
        return False

    def detect_josa_combination_krdict(self, clues):
        prefix_list = []
        if len(clues) == 0:
            # 아무 정보가 없으면 모든 체언 뒤에 붙는 걸로 취급
            prefix_list.append('체언')
            return prefix_list

        for clue in clues:
            used = False

            if clue.startswith('주로 '):
                continue

            if '나타내는 ' in clue:
                s = clue.split('나타내는 ')[1]
            elif '나타내는, ' in clue:
                s = clue.split('나타내는, ')[1]
            else:
                s = clue

            if s.startswith('‘ㄹ’을 제외한 받침 있는 '):
                prefix_list.append('ㄹ 제외한 받침 있음')
                s = s[len('‘ㄹ’을 제외한 받침 있는 '):]
            elif s.startswith('받침이 없거나 ‘ㄹ’ 받침으로 끝나는 '):
                prefix_list.append('받침 없거나 ㄹ 받침')
                s = s[len('받침이 없거나 ‘ㄹ’ 받침으로 끝나는 '):]
            elif s.startswith('받침이 없거나 ‘ㄹ’ 받침인 '):
                prefix_list.append('받침 없거나 ㄹ 받침')
                s = s[len('받침이 없거나 ‘ㄹ’ 받침인 '):]
            elif s.startswith('받침이 없거나 ‘ㄹ’, ‘ㅆ’, ‘ㅄ’ 받침인 '):
                prefix_list.append('받침 없거나 ㄹㅆㅄ 받침')
                s = s[len('받침이 없거나 ‘ㄹ’, ‘ㅆ’, ‘ㅄ’ 받침인 '):]
            elif s.startswith('받침 없는 '):
                prefix_list.append('받침 없음')
                s = s[len('받침 없는 '):]
            elif s.startswith('받침 있는 '):
                prefix_list.append('받침 있음')
                s = s[len('받침 있는 '):]

            prefix_found = False
            if '뒤에 붙여 ' in s:
                s = s.split(' 뒤에 붙여 ')[0]
                prefix_found = True
            elif '에 붙여 쓴다' in s:
                s = s.split('에 붙여 쓴다')[0]
                prefix_found = True

            if prefix_found:
                if s == '말':
                    prefix_list.append('체언')
                    used = True
                elif '명사' in s:
                    prefix_list.append('명사')
                    used = True
                elif '체언' in s:
                    prefix_list.append('체언')
                    used = True
                elif '부사어' in s:
                    prefix_list.append('부사어')
                    used = True
                elif '조사' in s:
                    prefix_list.append('조사')
                    used = True
            elif s.endswith(' 온다'):
                continue
            elif s.endswith(' 쓸 수 있다'):
                continue
            elif s.endswith('로 쓴다'):
                continue
            elif s.endswith('활용을 한다'):
                continue
            elif s.endswith('잘 쓰지 않는다'):
                continue
            elif s.endswith('함께 쓴다'):
                continue

            if not used:
                print('사용되지 않은 조사 참고: %s (%s)' % (clue,s))

        found = False
        for prefix in prefix_list:
            if prefix in ['명사', '대명사', '수사']:
                found = True

        if not found:
            prefix_list = []
        else:
            # remove duplicates
            new_prefix_list = []
            for prefix in prefix_list:
                # 형태가 다를 수는 있어도 명사만 받는 조사는 없다
                if prefix in ['명사']:
                    if '체언' not in new_prefix_list:
                        new_prefix_list.append('체언')
            prefix_list = new_prefix_list
            prefix_list.sort()

        return prefix_list

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: %s <entries_dir>')
        sys.exit(1)

    entries_dir = sys.argv[1]
    processor = ProcessYamlDocs(entries_dir)
    processor.run()
