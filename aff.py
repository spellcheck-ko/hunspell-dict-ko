# -*- coding: utf-8 -*-
# AFF file utility

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
# Contributor(s): See CREDITS file
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

import config
from flags import *
from jamo import *
import suffix
import josa

import unicodedata

def nfd(u8str):
    return unicodedata.normalize('NFD', u8str.decode('UTF-8')).encode('UTF-8')
def NFD(unistr):
    return unicodedata.normalize('NFD', unistr)
def NFC(unistr):
    return unicodedata.normalize('NFC', unistr)

# 빈도가 높은 글자를 앞에 쓸 수록 처리 속도 향상
# 
# NOTE: 단, 모음이 틀리는 경우가 보통 더 많으므로 더 나은 단어가 앞에
# 추천 단어의 앞에 나오도록 모음을 먼저 쓴다.
#
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
TRYCHARS = (u'\u1161\u1175\u1173\u1169\u1165\u116e\u1167\u1166\u1162\u1174' +
            u'\u116a\u116d\u1172\u116f\u116c\u1171\u1163\u1168\u1170\u116b' +
            u'\u1164' +
            u'\u110b\u11ab\u1100\u1109\u11bc\u110c\u1105\u1103\u11af\u1112' + 
            u'\u11a8\u1102\u1107\u1106\u11b7\u110e\u1110\u1111\u110f\u11bb' + 
            u'\u11b8\u11ba\u1104\u1101\u11c0\u110a\u11ad\u110d\u11ae\u11b9' + 
            u'\u11be\u11c1\u11bd\u11c2\u1108\u11b0\u11b1\u11a9\u11b2\u11b6' + 
            u'\u11ac\u11aa\u11bf\u11b4\u11b3\u11b5')

_conv_strings = []
_conv_strings.append('ICONV 11172')
for uch in map(unichr, range(0xac00, 0xd7a3 + 1)):
    _conv_strings.append('ICONV %s %s' % (uch, NFD(uch)))
_conv_strings.append('OCONV 11172')
for uch in map(unichr, range(0xac00, 0xd7a3 + 1)):
    _conv_strings.append('OCONV %s %s' % (NFD(uch), uch))
CONV_DEFINES = '\n'.join(_conv_strings)

# MAP: 비슷한 성격의 자모
# - 초성은 거센소리나 된소리처럼 같은 계열 초성 묶음
# - 중성은 비슷한 발음 묶음
# - 종성의 경우 받침 소리가 같은 발음 묶음

map_list = [
    L_KIYEOK + L_SSANGKIYEOK + L_KHIEUKH,
    L_TIKEUT + L_SSANGTIKEUT + L_THIEUTH,
    L_PIEUP + L_SSANGPIEUP + L_PHIEUPH,
    L_SIOS + L_SSANGSIOS,
    L_CIEUC + L_SSANGCIEUC + L_CHIEUCH,
    V_AE + V_E + V_YAE + V_YE,
    V_WAE + V_OE + V_WE,
    T_KIYEOK + T_SSANGKIYEOK + T_KIYEOK_SIOS + T_KHIEUKH,
    T_NIEUN + T_NIEUN_CIEUC + T_NIEUN_HIEUH,
    T_TIKEUT + T_SIOS + T_SSANGSIOS + T_CIEUC + T_CHIEUCH +
    T_THIEUTH + T_HIEUH,
    T_RIEUL + T_RIEUL_KIYEOK + T_RIEUL_MIEUM + T_RIEUL_PIEUP +
    T_RIEUL_SIOS + T_RIEUL_THIEUTH + T_RIEUL_PHIEUPH + T_RIEUL_HIEUH,
    T_PIEUP + T_PIEUP_SIOS + T_PHIEUPH,
]
MAP_DEFINES = 'MAP %d\n' % len(map_list)
for m in map_list:
    MAP_DEFINES += 'MAP %s\n' % m

######################################################################
## REP: 흔히 틀리는 목록

rep_list = [
    # 의존명사 앞에 띄어 쓰기
    (u'것', u'_것'),

    ## 두벌식 입력 순서 바뀜
    (u'빈', T_PIEUP + u'니'),      # 하빈다, 스빈다, ...
    (V_O + u'나', V_WA + T_NIEUN), # 오나전 => 완전
    (u'낟', T_NIEUN + u'다'),      # 하낟 => 한다
    (u'싿', T_SSANGSIOS + u'다'),  # 이싿 => 있다

    ## 불규칙 용언의 활용을 잘못 썼을 경우에 대한 대치어 만들기. 단순
    ## 탈락이나 자모 1개 변경처럼 hunspell의 suggestion 규칙에서
    ## 처리하지 못하는 경우만.
    # ㅂ불규칙
    (T_PIEUP + u'아', u'와'),
    (T_PIEUP + u'어', u'워'),
    (T_PIEUP + u'으', u'우'),
    # 르불규칙
    (u'르어', T_RIEUL + u'러'),
    (u'르어', T_RIEUL + u'라'),
    # 으불규칙
    (V_EU + u'어', V_EO),
    (V_EU + u'어', V_A),

    ## 활용
    # ㄹ런지 => ㄹ는지
    (T_RIEUL + u'런지', T_RIEUL + u'는지'),
    # 스런 => 스러운 (잘못된 준말 사용)
    (u'스런', u'스러운'),

    ## 연철/분철 발음을 혼동할 때 나타나는 오타 대치어
    # 받침+ㅇ초성 (일찍이/일찌기 등)
    (T_KIYEOK + L_IEUNG, L_KIYEOK),
    (L_KIYEOK, T_KIYEOK + L_IEUNG),
    (T_NIEUN + L_IEUNG, L_NIEUN),
    (L_NIEUN, T_NIEUN + L_IEUNG),
    (T_RIEUL + L_IEUNG, L_RIEUL),
    (L_RIEUL, T_RIEUL + L_IEUNG),
    (T_MIEUM + L_IEUNG, L_MIEUM),
    (L_MIEUM, T_MIEUM + L_IEUNG),
    (T_PHIEUPH + L_IEUNG, L_PHIEUPH),
    (L_PHIEUPH, T_PHIEUPH + L_IEUNG),
    (T_SIOS + L_IEUNG, L_SIOS),
    (L_SIOS, T_SIOS + L_IEUNG),
    (L_CIEUC, T_CIEUC + L_IEUNG),
    (T_CIEUC + L_IEUNG, L_CIEUC),
     # ㅅㅎ -> ㅌ (통신어..)
    (T_SIOS + L_HIEUH, L_THIEUTH),
]

REP_DEFINES = 'REP %d\n' % len(rep_list)
for rep in rep_list:
    REP_DEFINES += nfd('REP %s %s\n' % (rep[0], rep[1]))

compound_rules = [
    # 숫자
    '(%d)*(%d)' % (digit_flag, digit_flag),
    # 숫자+단위
    '(%d)*(%d)(%d)' % (digit_flag, digit_flag, counter_flag),
    # tokenizer에서 로마자를 분리해 주지 않는 경우를 위해 로마자로 된 모든
    # 단어를 허용하고 명사로 취급한다.
    '(%d)*(%d)?' % (alpha_flag, plural_suffix_flag),
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

# 보조용언 붙여 쓰기: 별도로 확장하지 않는 경우에만 필요
if not config.expand_auxiliary_attached:
    compound_rules += [
        '(%d)(%d)' % (conjugation_eo_flag, auxiliary_eo_flag),
        '(%d)(%d)' % (conjugation_eun_flag, auxiliary_eun_flag),
        '(%d)(%d)' % (conjugation_eul_flag, auxiliary_eul_flag),
    ]

COMPOUNDRULE_DEFINES = 'COMPOUNDRULE %d\n' % len(compound_rules)
for rule in compound_rules:
    COMPOUNDRULE_DEFINES += 'COMPOUNDRULE %s\n' % rule

## 용언 어미

def get_suffix_defines(flagaliases):
    return suffix.get_rules_string(flagaliases)

# 조사

def get_josa_defines(flagaliases):
    return josa.get_output(flagaliases)
