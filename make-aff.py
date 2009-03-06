# -*- coding: utf-8 -*-
# 파생 규칙 파일 생성
#
# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is Hunspell Korean spellchecking dictionary.
#
# The Initial Developer of the Original Code is
# Changwoo Ryu.
# Portions created by the Initial Developer are Copyright (C) 2008, 2009
# the Initial Developer. All Rights Reserved.
#
# Contributor(s):
# Changwoo Ryu
# Namhyung Kim
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# ***** END LICENSE BLOCK *****

import sys
import unicodedata

reload(sys)
sys.setdefaultencoding('UTF-8')

def nfd(u8str):
    return unicodedata.normalize('NFD', u8str.decode('UTF-8')).encode('UTF-8')
def nfc(u8str):
    return unicodedata.normalize('NFC', u8str.decode('UTF-8')).encode('UTF-8')

def NFD(unistr):
    return unicodedata.normalize('NFD', unistr)
def NFC(unistr):
    return unicodedata.normalize('NFC', unistr)

def out(u8str):
    return sys.stdout.write(u8str)

def outnfd(u8str):
    return sys.stdout.write(nfd(u8str))

def err(u8str):
    return sys.stderr.write(u8str)

from config import *

## 헤더 정보
out(header)
out('VERSION hunspell-dict-ko %s\n' % version)
out('SET UTF-8\n')
out('LANG ko\n')
out('FLAG num\n')

## WORDCHARS
out('WORDCHARS 0123456789\n')

## TRY - 빈도가 높은 글자를 앞에 쓸 수록 처리 속도 향상
# 2008년 12월 현재 한국어 위키백과의 빈도:
#
# U+110b: 12945437 (HANGUL CHOSEONG IEUNG)
# U+1161: 11184877 (HANGUL JUNGSEONG A)
# U+11ab: 9201655 (HANGUL JONGSEONG NIEUN)
# U+1175: 8976003 (HANGUL JUNGSEONG I)
# U+1100: 6748571 (HANGUL CHOSEONG KIYEOK)
# U+1173: 6501009 (HANGUL JUNGSEONG EU)
# U+1169: 6130514 (HANGUL JUNGSEONG O)
# U+1109: 5708785 (HANGUL CHOSEONG SIOS)
# U+1165: 5264197 (HANGUL JUNGSEONG EO)
# U+11bc: 5092793 (HANGUL JONGSEONG IEUNG)
# U+110c: 4962840 (HANGUL CHOSEONG CIEUC)
# U+116e: 4835854 (HANGUL JUNGSEONG U)
# U+1105: 4667272 (HANGUL CHOSEONG RIEUL)
# U+1103: 4663742 (HANGUL CHOSEONG TIKEUT)
# U+11af: 4478045 (HANGUL JONGSEONG RIEUL)
# U+1112: 3953535 (HANGUL CHOSEONG HIEUH)
# U+1167: 3444653 (HANGUL JUNGSEONG YEO)
# U+11a8: 3353338 (HANGUL JONGSEONG KIYEOK)
# U+1102: 3270768 (HANGUL CHOSEONG NIEUN)
# U+1107: 3037763 (HANGUL CHOSEONG PIEUP)
# U+1166: 2881967 (HANGUL JUNGSEONG E)
# U+1106: 2635707 (HANGUL CHOSEONG MIEUM)
# U+1162: 2533498 (HANGUL JUNGSEONG AE)
# U+11b7: 1718630 (HANGUL JONGSEONG MIEUM)
# U+110e: 1507312 (HANGUL CHOSEONG CHIEUCH)
# U+1110: 1505921 (HANGUL CHOSEONG THIEUTH)
# U+1174: 1230310 (HANGUL JUNGSEONG YI)
# U+116a: 1195625 (HANGUL JUNGSEONG WA)
# U+1111: 1174547 (HANGUL CHOSEONG PHIEUPH)
# U+110f: 912332 (HANGUL CHOSEONG KHIEUKH)
# U+11bb: 875292 (HANGUL JONGSEONG SSANGSIOS)
# U+116d: 848305 (HANGUL JUNGSEONG YO)
# U+11b8: 806419 (HANGUL JONGSEONG PIEUP)
# U+1172: 798379 (HANGUL JUNGSEONG YU)
# U+116f: 717457 (HANGUL JUNGSEONG WEO)
# U+116c: 711301 (HANGUL JUNGSEONG OE)
# U+11ba: 389100 (HANGUL JONGSEONG SIOS)
# U+1171: 375026 (HANGUL JUNGSEONG WI)
# U+1163: 359881 (HANGUL JUNGSEONG YA)
# U+1168: 288224 (HANGUL JUNGSEONG YE)
# U+1104: 233944 (HANGUL CHOSEONG SSANGTIKEUT)
# U+1101: 189755 (HANGUL CHOSEONG SSANGKIYEOK)
# U+11c0: 119337 (HANGUL JONGSEONG THIEUTH)
# U+110a: 113001 (HANGUL CHOSEONG SSANGSIOS)
# U+11ad: 97304 (HANGUL JONGSEONG NIEUN-HIEUH)
# U+110d: 84806 (HANGUL CHOSEONG SSANGCIEUC)
# U+11ae: 70808 (HANGUL JONGSEONG TIKEUT)
# U+11b9: 61476 (HANGUL JONGSEONG PIEUP-SIOS)
# U+1170: 52914 (HANGUL JUNGSEONG WE)
# U+11be: 48191 (HANGUL JONGSEONG CHIEUCH)
# U+11c1: 44326 (HANGUL JONGSEONG PHIEUPH)
# U+11bd: 42718 (HANGUL JONGSEONG CIEUC)
# U+11c2: 40882 (HANGUL JONGSEONG HIEUH)
# U+1108: 36758 (HANGUL CHOSEONG SSANGPIEUP)
# U+11b0: 22199 (HANGUL JONGSEONG RIEUL-KIYEOK)
# U+11b1: 21644 (HANGUL JONGSEONG RIEUL-MIEUM)
# U+116b: 20701 (HANGUL JUNGSEONG WAE)
# U+11a9: 16775 (HANGUL JONGSEONG SSANGKIYEOK)
# U+11b2: 7965 (HANGUL JONGSEONG RIEUL-PIEUP)
# U+11b6: 6840 (HANGUL JONGSEONG RIEUL-HIEUH)
# U+1164: 1946 (HANGUL JUNGSEONG YAE)
# U+11ac: 1710 (HANGUL JONGSEONG NIEUN-CIEUC)
# U+11aa: 1600 (HANGUL JONGSEONG KIYEOK-SIOS)
# U+11bf: 794 (HANGUL JONGSEONG KHIEUKH)
# U+11b4: 544 (HANGUL JONGSEONG RIEUL-THIEUTH)
# U+11b3: 523 (HANGUL JONGSEONG RIEUL-SIOS)
# U+11b5: 495 (HANGUL JONGSEONG RIEUL-PHIEUPH)
trychars = u'\u110b\u1161\u11ab\u1175\u1100\u1173\u1169\u1109\u1165\u11bc\u110c\u116e\u1105\u1103\u11af\u1112\u1167\u11a8\u1102\u1107\u1166\u1106\u1162\u11b7\u110e\u1110\u1174\u116a\u1111\u110f\u11bb\u116d\u11b8\u1172\u116f\u116c\u11ba\u1171\u1163\u1168\u1104\u1101\u11c0\u110a\u11ad\u110d\u11ae\u11b9\u1170\u11be\u11c1\u11bd\u11c2\u1108\u11b0\u11b1\u116b\u11a9\u11b2\u11b6\u1164\u11ac\u11aa\u11bf\u11b4\u11b3\u11b5'
out('TRY %s\n' % trychars)


def write_conv_table():
    out('ICONV 11172\n')
    for uch in map(unichr, range(0xac00, 0xd7a3 + 1)):
        out('ICONV %s %s\n' % (uch, unicodedata.normalize("NFD", uch)))
    out('OCONV 11172\n')
    for uch in map(unichr, range(0xac00, 0xd7a3 + 1)):
        out('OCONV %s %s\n' % (unicodedata.normalize("NFD", uch), uch))

write_conv_table()

## 자모 목록 (L_*, V_*, T_*)
from jamo import *

## FLAG
from flags import *

## TODO: KEY - 두벌식 키보드 배치

######################################################################
## MAP: 비슷한 자모
# 된소리/거센소리, 비슷한 발음의 중성, 같은 발음의 종성

map_list = [
    L_KIYEOK + L_SSANGKIYEOK + L_KHIEUKH,
    L_TIKEUT + L_SSANGTIKEUT + L_THIEUTH,
    L_PIEUP + L_SSANGPIEUP + L_PHIEUPH,
    L_SIOS + L_SSANGSIOS,
    L_CIEUC + L_SSANGCIEUC + L_CHIEUCH,
    V_AE + V_E,
    V_YAE + V_YE,
    V_WAE + V_OE + V_WE,
    T_KIYEOK + T_SSANGKIYEOK + T_KIYEOK_SIOS + T_KHIEUKH,
    T_NIEUN + T_NIEUN_CIEUC + T_NIEUN_HIEUH,
    T_TIKEUT + T_SIOS + T_SSANGSIOS + T_CIEUC + T_CHIEUCH + T_THIEUTH + T_HIEUH,
    T_RIEUL + T_RIEUL_KIYEOK + T_RIEUL_MIEUM + T_RIEUL_PIEUP +
    T_RIEUL_SIOS + T_RIEUL_THIEUTH + T_RIEUL_PHIEUPH + T_RIEUL_HIEUH,
    T_PIEUP + T_PIEUP_SIOS + T_PHIEUPH,
]
out('MAP %d\n' % len(map_list))
for m in map_list:
    outnfd('MAP %s\n' % m)


######################################################################
## REP: 흔히 틀리는 목록

rep_list = [
    # ㅕ/ㅓ
    (u'\u1167', u'\u1165'),
    # 의존명사 앞에 띄어 쓰기
    (u'\u11af것', u'\u11af_것'),
    ]
out('REP %d\n' % len(rep_list))
for rep in rep_list:
    outnfd('REP %s %s\n' % (rep[0], rep[1]))


######################################################################    

out('COMPOUNDMIN 1\n')
#out('ONLYINCOMPOUND %d\n' % plural_suffix_flag)

compound_rules = [
    # 숫자+단위
    '(%d)*(%d)(%d)' % (digit_flag, digit_flag, counter_flag),
    # 가산명사+'들'
    '(%d)(%d)' % (countable_noun_flag, plural_suffix_flag),
    # tokenizer에서 로마자를 분리해 주지 않는 경우를 위해 로마자로 된 모든
    # 단어를 허용하고 명사로 취급한다.
    '(%d)*(%d)?' % (alpha_flag, plural_suffix_flag),
    # '-어' 형태 뒤에 붙여 쓸 수 있는 보조 용언
    '(%d)(%d)' % (conjugation_eo_flag, auxiliary_eo_flag),
    # '-은' 형태 뒤에 붙여 쓸 수 있는 보조 용언
    '(%d)(%d)' % (conjugation_eun_flag, auxiliary_eun_flag),
    # '-을' 형태 뒤에 붙여 쓸 수 있는 보조 용언
    '(%d)(%d)' % (conjugation_eul_flag, auxiliary_eul_flag),
    # 숫자 만 단위로 띄어 쓰기
    # FIXME: hunspell 1.2.8에서는 백자리 이상 쓰면 SEGV
    #'(%d)?(%d)?(%d)?(%d)?(%d)?' % (number_1000_flag,
    #                               number_100_flag,
    #                               number_10_flag,
    #                               number_1_flag,
    #                               number_10000_flag),
    '(%d)?(%d)?(%d)?' % (number_10_flag,
                         number_1_flag,
                         number_10000_flag),
]

out('COMPOUNDRULE %d\n' % len(compound_rules))
for rule in compound_rules:
    out('COMPOUNDRULE %s\n' % rule)

######################################################################

out('FORBIDDENWORD %d\n' % forbidden_flag)

######################################################################
## FLAG

## 어미

import suffix

suffix.write_suffixes(sys.stdout)

######################################################################

## 조사

ALPHA_ALL = ''.join(map(unichr, range(ord('a'),ord('z')+1)))

## 임의로 허용하는 로마자로 된 단어는 음운 구별을 하지 않는다. 할 방법이 없음.
COND_ALL = '.'
COND_V_ALL = '[%s]' % (V_ALL + ALPHA_ALL)
COND_T_ALL = '[%s]' % (T_ALL + ALPHA_ALL)
COND_V_OR_RIEUL = '[%s]' % (V_ALL + u'\u11af' + ALPHA_ALL)
COND_T_NOT_RIEUL = '[%s]' % (T_ALL.replace(u'\u11af', '') + ALPHA_ALL)

josas = [('이', COND_T_ALL), ('가', COND_V_ALL),
         ('을', COND_T_ALL), ('를', COND_V_ALL),
         ('과', COND_T_ALL), ('와', COND_V_ALL),
         ('은', COND_T_ALL), ('는', COND_V_ALL),
         ('라', COND_V_ALL), ('이라', COND_T_ALL),
         ('라고', COND_V_ALL), ('이라고', COND_T_ALL),
         ('라는', COND_V_ALL), ('이라는', COND_T_ALL),
         ('라도', COND_V_ALL), ('이라도', COND_T_ALL),
         ('라면', COND_V_ALL), ('이라면', COND_T_ALL),
         ('라서', COND_V_ALL), ('이라서', COND_T_ALL),
         ('란', COND_V_ALL), ('이란', COND_T_ALL),
         ('랑', COND_V_ALL), ('이랑', COND_T_ALL),
         ('로', COND_V_OR_RIEUL), ('으로', COND_T_NOT_RIEUL),
         ('로는', COND_V_OR_RIEUL), ('으로는', COND_T_NOT_RIEUL),
         ('로도', COND_V_OR_RIEUL), ('으로도', COND_T_NOT_RIEUL),
         ('로서', COND_V_OR_RIEUL), ('으로서', COND_T_NOT_RIEUL),
         ('로써', COND_V_OR_RIEUL), ('으로써', COND_T_NOT_RIEUL),
         ('로부터', COND_V_OR_RIEUL), ('으로부터', COND_T_NOT_RIEUL),
         # sorted list
         ('같이', COND_ALL),
         ('까지', COND_ALL),
         ('까지는', COND_ALL),
         ('까지도', COND_ALL),
         ('까지라도', COND_ALL),
         ('께', COND_ALL),
         ('께는', COND_ALL),
         ('께도', COND_ALL),
         ('께서', COND_ALL),
         ('께서는', COND_ALL),
         ('께서도', COND_ALL),
# FIXME: -ㄴ 조사를 허용하면 모든 명사에 ㄴ을 허용하게 되어 범위가 너무 넓어진다.
#         (u'\u11ab', COND_V_ALL), # -ㄴ: '-는' 구어체
         ('나', COND_V_ALL),
         ('대로', COND_ALL),
         ('대로는', COND_ALL),
         ('도', COND_ALL),
         ('마다', COND_ALL),         # 보조사, '모두'
         ('마저', COND_ALL),
         ('마저도', COND_ALL),
         ('만', COND_ALL),
         ('만이', COND_ALL),
         ('밖에', COND_ALL),
         ('밖에는', COND_ALL),
         ('보다', COND_ALL),
         ('보다는', COND_ALL),
         ('보다도', COND_ALL),
         ('부터', COND_ALL),
         ('부터라도', COND_ALL),
         ('서', COND_ALL),           # '~에서' 준말
         ('에', COND_ALL),
         ('에게', COND_ALL),
         ('에게서', COND_ALL),
         ('에게서는', COND_ALL),
         ('에게서도', COND_ALL),
         ('에는', COND_ALL),         # 에+'는' 보조사
         ('에도', COND_ALL),         # 에+'도' 보조사
         ('에서', COND_ALL),
         ('엔', COND_ALL),           # '에는' 준말
         ('야', COND_V_ALL),
         ('의', COND_ALL),
         ('이나', COND_T_ALL),
         ('이든', COND_ALL),
         ('이든지', COND_ALL),
         ('이야', COND_T_ALL), # '-(이)야' 강조
         ('조차', COND_ALL),
         ('조차도', COND_ALL),
         ('처럼', COND_ALL),
         ('처럼은', COND_ALL),
         # TODO: -한테 조사는 사람이나 동물 등에만 붙음
         ('하고', COND_ALL),         # 구어체
         ('한테', COND_ALL),
         ('한테서', COND_ALL),
         ]

# 주격조사 ('이다') 활용을 조사 목록에 덧붙이기
# twofold suffix를 여기에 써먹기에는 아깝다
ida_conjugations = suffix.make_all_conjugations('이다', '이다', [])
for c in ida_conjugations:
    if NFD(c)[:2] == NFD(u'여'):
        # '-이어' -> '여' 줄임형은 받침이 있을 경우에만
        josas.append((c, COND_V_ALL))
    else:
        josas.append((c, COND_ALL))
    # '이' 생략
    # TODO: 받침이 앞의 명사에 붙는 경우 허용 여부 (예: "마찬가집니다")
    if NFC(c)[0] == u'이':
        josas.append((NFC(c)[1:], COND_V_ALL))

out('SFX %d Y %d\n' % (josa_flag, len(josas)))
for (suffix,cond) in josas:
    outnfd('SFX %d 0 %s %s\n' % (josa_flag, suffix, cond))

