# 한국어기초사전 불규칙용언 찾기

import sys
import datetime
import tzlocal
import unicodedata
import yaml

L_RIEUL = '\u1105'
V_A = '\u1161'
V_AE = '\u1162'
V_EO = '\u1165'
V_E = '\u1166'
V_EU = '\u1173'
T_KIYEOK = '\u11A8'
T_NIEUN = '\u11AB'
T_TIKEUT = '\u11AE'
T_RIEUL = '\u11AF'
T_PIEUP = '\u11B8'
T_SIOS = '\u11BA'
T_HIEUH = '\u11C2'

def is_jongseong(j):
    return ord(j) >= ord(T_KIYEOK) and ord(j) <= ord(T_HIEUH)

def detect_irregular(word, inflections):
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
            result = '규칙'
        elif unicodedata.normalize('NFC', nfd[:-1] + V_A) in inflections:
            result = '규칙'
        elif is_jongseong(nfd[-3]):
            # '-ㄹ르다'처럼 '르' 앞에 종성이 있으면 르불규칙이 될 수 없고
            # '-ㄹ르러' 처럼 되기도 어려워 보이므로 규칙활용 '-ㄹ러'일 것이다
            result = '규칙'
        else:
            result = '르/러불규칙 미확정'
    elif nfd[-1] == T_TIKEUT:
        if unicodedata.normalize('NFC', nfd[:-1] + T_RIEUL) + '어' in inflections:
            result = 'ㄷ불규칙'
        elif unicodedata.normalize('NFC', nfd[:-1] + T_RIEUL) + '아' in inflections:
            result = 'ㄷ불규칙'
        elif word[:-1] + '어' in inflections:
            result = '규칙'
        elif word[:-1] + '아' in inflections:
            result = '규칙'
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
            result = '규칙'
        elif word[:-1] + '아' in inflections:
            result = '규칙'
        else:
            result = 'ㅂ불규칙 미확정'
        pass
    elif nfd[-1] == T_SIOS:
        if unicodedata.normalize('NFC', nfd[:-1]) + '어' in inflections:
            result = 'ㅅ불규칙'
        elif unicodedata.normalize('NFC', nfd[:-1]) + '아' in inflections:
            result = 'ㅅ불규칙'
        elif word[:-1] + '어' in inflections:
            result = '규칙'
        elif word[:-1] + '아' in inflections:
            result = '규칙'
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
            result = '규칙'
        elif word[:-1] + '아' in inflections:
            result = '규칙'
        elif word[:-1] + '어' in inflections:
            result = '규칙'
        elif word[-1] == '렇' or word[-1] == '랗':
            # '-렇다', '-랗다'는 불규칙
            result = 'ㅎ불규칙'
        else:
            result = 'ㅎ불규칙 미확정'
    else:
        result = None

    return result

def process_file(filename):
    k = yaml.load(open(filename).read())
    if '한국어기초사전' not in k['imported']:
        return
    imported = k['imported']['한국어기초사전']
    if imported['품사'] not in ['형용사','동사','보조 형용사','보조 동사']:
        return

    # 이미 설정되어 있는지 확인
    # if '불규칙 활용' in k['processed']['맞춤법 검사']:
    #     return

    word = k['processed']['맞춤법 검사']['표제어']
    if '활용' in imported:
        inflections = [dd['형태'] for dd in imported['활용']]
    else:
        inflections = []

    result = detect_irregular(word, inflections)
    if not result:
        return

    if result.endswith('미확정'):
        print('단어: %s (%s), 활용: %s' % (word, result, ', '.join(inflections)))

    print(filename)
    k['processed']['맞춤법 검사']['불규칙 활용'] = result
    print('불규칙:' + result)
    with open(filename, 'w') as fp:
        fp.write(yaml.dump(k, allow_unicode=True, default_flow_style=False, indent=2))


if __name__ == '__main__':
    filenames = sys.argv[1:]
    for filename in filenames:
        process_file(filename)
