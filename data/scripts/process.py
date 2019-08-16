import copy
import glob
import os
import sys
import yaml
import unicodedata

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
        docs = list(yaml.load_all(open(filename), Loader=yaml.FullLoader))
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
        supported = [ x in doc for x in [ '한국어기초사전', '표준국어대사전', '갈퀴 Django'] ]
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
            elif '갈퀴 Django' in doc['import']:
                input = doc['import']['갈퀴 Django']
                self.process_doc_galkwidjango(input, output)
        else:
            sys.stderr.write('Warning: unknown import: %s\n' % str(doc))

    def process_doc_krdict(self, input, output):
        if input['의미'][0]['뜻풀이'].startswith('→'):
            output['제외'] = '틀린 말'
        elif input['품사'] in ['어미', '접사', '조사']:
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
                    inflections = [dd['형태'] for dd in input['활용']]
                    inflection_type = self.detect_inflection_type(word, inflections)
                    if inflection_type is not None and inflection_type != '규칙':
                        props.append(inflection_type)

            # 보조용언 타입
            if pos.startswith('보조 '):
                clue = input['의미'][0]['의미 참고']

                examples = []
                if '뒤에서 ' in clue:
                    examples = clue.split('뒤에서 ')[1].split('로 쓴다.')[0].split(', ')
                elif '뒤에 ' in clue:
                    examples = clue.split('뒤에 ')[1].split('로 쓴다.')[0].split(', ')
                if examples:
                    if len(examples) > 0:
                        examples = [k[1:-1] for k in examples]
                        for example in examples:
                            prefixes = example.split(' ')[0].split('/')
                            for prefix in prefixes:
                                if prefix[0] != '-':
                                    prefix = '-' + prefix
                                props.append('보조용언:' + prefix)
                else:
                    if word == '드리다':
                        props.append('보조용언:-어')

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

    def process_doc_stdict(self, input, output):
        pass

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
            entry = copy.deepcopy(doc['import_derived']['맞춤법 검사'])
            for key in doc['manual']['맞춤법 검사'].keys():
                entry[key] = copy.deepcopy(doc['manual']['맞춤법 검사'][key])
            doc['result']['맞춤법 검사'] = entry

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

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: %s <entries_dir>')
        sys.exit(1)

    entries_dir = sys.argv[1]
    processor = ProcessYamlDocs(entries_dir)
    processor.run()
