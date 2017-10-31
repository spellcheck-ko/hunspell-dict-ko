# 용언/서술격조사 활용 데이터

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
# Portions created by the Initial Developer are Copyright (C) 2008, 2009, 2010
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
import flags
import encoding
import unicodedata
from jamo import *


def ENC(unistr):
    if config.internal_encoding == '2+RST':
        return encoding.encode(unistr).replace(encoding.RESET_CODE, '')
    else:
        return unicodedata.normalize('NFD', unistr)


def DEC(s):
    if config.internal_encoding == '2+RST':
        return encoding.decode(s)
    else:
        return unicodedata.normalize('NFC', s)


######################################################################
# 유틸리티

# 자모

if config.internal_encoding == '2+RST':
    ALPHA_ALL = '01234567890abcdefghijklmnopqrstuvwxyz'
    L_ALL = 'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ'
    T_ALL = 'ㄱㄲㄴㄷㄹㅁㅂㅅㅆㅇㅈㅊㅋㅌㅍㅎ'
    V_ALL = 'ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅛㅜㅠㅡㅣ'
    L_HIEUH = 'ㅎ'
    L_IEUNG = 'ㅇ'
    L_NIEUN = 'ㄴ'
    T_HIEUH = 'ㅎ'
    T_IEUNG = 'ㅇ'
    T_MIEUM = 'ㅁ'
    T_NIEUN = 'ㄴ'
    T_PIEUP = 'ㅂ'
    T_RIEUL = 'ㄹ'
    T_RIEUL_MIEUM = 'ㄹㅁ'
    T_SIOS = 'ㅅ'
    T_SSANGSIOS = 'ㅆ'
    T_TIKEUT = 'ㄷ'
    V_A = 'ㅏ'
    V_AE = 'ㅐ'
    V_E = 'ㅔ'
    V_EO = 'ㅓ'
    V_EU = 'ㅡ'
    V_I = 'ㅣ'
    V_O = 'ㅗ'
    V_OE = 'ㅗㅣ'
    V_U = 'ㅜ'
    V_WA = 'ㅗㅏ'
    V_WAE = 'ㅗㅐ'
    V_WEO = 'ㅜㅓ'
    V_YA = 'ㅑ'
    V_YAE = 'ㅒ'
    V_YE = 'ㅖ'
    V_YEO = 'ㅕ'


def L_NOT(jamos):
    return ''.join([c for c in L_ALL if c not in jamos])


def V_NOT(jamos):
    return ''.join([c for c in V_ALL if c not in jamos])


def T_NOT(jamos):
    return ''.join([c for c in T_ALL if c not in jamos])


if config.internal_encoding == '2+RST':
    V_A_O = 'ㅏㅑㅗㅛ'
    V_NOT_A_O = V_NOT('ㅏㅑㅗㅛ')
    V_NOT_A_O_EU = V_NOT('ㅏㅑㅗㅛㅡ')
    L_NOT_HIEUH = L_NOT('ㅎ')
else:
    V_A_O = V_A + V_YA + V_O + V_YO
    V_NOT_A_O = V_NOT(V_A + V_YA + V_O + V_YO)
    V_NOT_A_O_EU = V_NOT(V_A + V_YA + V_O + V_YO + V_EU)
    L_NOT_HIEUH = L_NOT(L_HIEUH)

# 조건

if config.internal_encoding == '2+RST':
    COND_V_ALL = '[ㅏㅑㅐㅒㅗㅛㅓㅔㅕㅖㅜㅠㅡㅣ]'
    COND_T_ALL = '[ㄱㄲㄴㄷㄹㅁㅂㅅㅆㅇㅈㅊㅋㅌㅍㅎ]'
    COND_V_OR_RIEUL = '[ㅏㅑㅐㅒㅗㅛㅓㅔㅕㅖㅜㅠㅡㅣㄹ]'
    COND_T_NOT_RIEUL = '[ㄱㄲㄴㄷㅁㅂㅅㅆㅇㅈㅊㅋㅌㅍㅎ]'
    COND_NOT_RIEUL = '[^ㄹ]'
else:
    COND_V_ALL = '[%s]' % V_ALL
    COND_T_ALL = '[%s]' % T_ALL
    COND_V_OR_RIEUL = '[%s%s]' % (V_ALL, T_RIEUL)
    COND_T_NOT_RIEUL = '[%s]' % T_NOT(T_RIEUL)
    COND_NOT_RIEUL = '[^%s]' % T_RIEUL


# 보조사 확장
def attach_emphasis(group, particles):
    for klass in group:
        expanded = []
        for r in klass['rules']:
            expanded += [[r[0] + p] + r[1:] for p in particles]
        klass['rules'] += expanded


# 재활용
def copy_group(group):
    def copy_class(klass):
        new_class = {}
        for key in klass:
            if key == 'rules':
                new_class[key] = [l[:] for l in klass[key]]  # copy list-list
            else:
                new_class[key] = klass[key][:]  # copy list
        return new_class
    return [copy_class(klass) for klass in group]


# hunspell의 twofold suffix를 통해 확장할 추가 플래그 지정, 해당 파생
# 형태에 또 다른 접미어 규칙이 적용될 수 있는 경우 사용한다. (예:
# 명사형 전성어미 + 조사)
def attach_continuation_flags(group, flags):
    for klass in group:
        for r in klass['rules']:
            r.append(flags)

####
# 어/아로 시작하는 어미를 위한 유틸리티

# ㅏ/ㅗ 모음의 음절로 끝나는 경우 ('하'로 끝나는 경우 (여불규칙) 제외)
COND_EOA_AO = ['[%s][%s]' % (L_NOT_HIEUH, V_A_O), '[%s][%s]' % (V_A_O, T_ALL)]
if config.internal_encoding == '2+RST':
    # 복자음 받침
    COND_EOA_AO += ['[%s][ㄱㄴㄹㅂ][ㄱㅁㅂㅅㅈㅌㅎ]' % (V_A_O)]
# ㅏ/ㅗ 제외한 모음의 음절로 끝나는 경우 (ㅡ로 끝나는 경우 (으불규칙) 제외)
COND_EOA_NOT_AO = ['[%s]' % V_NOT_A_O_EU, '[%s][%s]' % (V_NOT_A_O, T_ALL)]
if config.internal_encoding == '2+RST':
    # 복자음 받침
    COND_EOA_NOT_AO += ['[%s][ㄱㄴㄹㅂ][ㄱㅁㅂㅅㅈㅌㅎ]' % (V_NOT_A_O)]

# ㅡ로 끝나는 경우 (으불규칙)
COND_EOA_EO = V_EO
# ㅓ로 끝나는 경우
COND_EOA_EO = V_EO
# ㅏ로 끝나는 경우 ('하' 제외)
COND_EOA_A = '[%s]%s' % (L_NOT(L_HIEUH), V_A)
# 하로 끝나는 경우
COND_EOA_HA = ENC('하')
# 외어 -> 왜 ('외다', '뇌다' 예외) - 한글 맞춤법 35항
COND_EOA_OE = '[%s]%s' % (L_NOT(L_NIEUN + L_IEUNG), V_OE)


####
# ㄷ불규칙활용 유틸리티

# 종성의 ㄷ이 ㄹ로 바뀜
def TIKEUT_IRREGULAR_TYPICAL_CLASS(suffix, after):
    return {'rules': [['-' + T_RIEUL + suffix[1:], T_TIKEUT, T_TIKEUT]],
            'after': after,
            'cond': ['#ㄷ불규칙'],
            }


####
# ㅂ불규칙활용 유틸리티

# 단순 탈락인 경우
def PIEUP_IRREGULAR_TYPICAL_CLASS(suffix, after):
    return {'rules': [[suffix, T_PIEUP, T_PIEUP]],
            'after': after,
            'cond': ['#ㅂ불규칙'],
            }


####
# ㅅ불규칙활용 유틸리티

# 단순 탈락인 경우
def SIOS_IRREGULAR_TYPICAL_CLASS(suffix, after):
    return {'rules': [[suffix, T_SIOS, T_SIOS]],
            'after': after,
            'cond': ['#ㅅ불규칙'],
            }


####
# ㅎ불규칙활용 유틸리티

# 단순 탈락인 경우
def HIEUH_IRREGULAR_TYPICAL_CLASS(suffix, after):
    return {'rules': [[suffix, T_HIEUH, T_HIEUH]],
            'after': after,
            'cond': ['#ㅎ불규칙'],
            }


####
# 르불규칙활용 유틸리티

# '르다' 앞에 ㅏ/ㅗ 모음의 음절
COND_REU_AO = ['[%s]' % V_A_O + ENC('르'),
               '[%s][%s]' % (V_A_O, T_ALL) + ENC('르')]
# '르다' 앞에 ㅏ/ㅗ 모음이 아닌 음절
COND_REU_NOT_AO = ['[%s]' % V_NOT_A_O + ENC('르'),
                   '[%s][%s]' % (V_NOT_A_O, T_ALL) + ENC('르')]

####
# 으불규칙활용 유틸리티

# 참고: 으불규칙 활용은 어/아 어미와 예외에 대해 3개의 규칙으로 만든다
#
# '으' 음절 앞에 오는 음절이 있는 경우 그 음절의 모음이 양성모음이냐
# 음성모음이냐에 따라 어미의 '어/아'가 결정되는데, '끄다', '뜨다', '쓰다',
# '트다', '크다'같은 으불규칙용언의 경우 앞의 음절이 없으면서 '어'가 붙어서
# 예외이다. 이 셋은 aff 파일의 같은 규칙 안에서 조건으로 정의할 수가 없다.
# (aff 파일에서 쓸 수 있는 제한된 정규식으로는 으 앞에 음절이 없다는 걸 정의할
# 수가 없다.) 그러므로 항상 별도 규칙으로 만든다.

# 앞에 ㅏ/ㅗ 모음의 음절
L_ALL_EU_EXCEPTIONS = ''.join([L_SSANGKIYEOK, L_SSANGTIKEUT, L_SSANGSIOS,
                               L_THIEUTH, L_KHIEUKH])
L_ALL_EU = ''.join([j for j in L_ALL if j not in L_ALL_EU_EXCEPTIONS])

COND_EU_AO = ['[%s][%s]%s' % (V_A_O, L_ALL_EU, V_EU),
              '[%s][%s][%s]%s' % (V_A_O, T_ALL, L_ALL_EU, V_EU)]
# 앞에 ㅏ/ㅗ 모음이 아닌 음절
COND_EU_NOT_AO = ['[%s][%s]%s' % (V_NOT_A_O, L_ALL_EU, V_EU),
                  '[%s][%s][%s]%s' % (V_NOT_A_O, T_ALL, L_ALL_EU, V_EU)]
# '끄다', '뜨다', '쓰다', '트다', '크다'
COND_EU_EXCEPTIONS = ['[%s]%s' % (L_ALL_EU_EXCEPTIONS, V_EU)]

####
# 유성음/무성음 자모 구분

T_VOICED = T_NIEUN + T_RIEUL + T_MIEUM + T_IEUNG
T_UNVOICED = ''.join([l for l in T_ALL if l not in T_VOICED])
COND_VOICED = '[%s]' % (V_ALL + T_VOICED)
COND_UNVOICED = '[%s]' % T_UNVOICED

######################################################################
####
# 어미 데이터

# 참고: 교착적 선어말어미
#
# 적은 숫자의 어말어미와 제한적으로만 결합하는 선어말어미는 (교착적
# 선어말어미) 여기에서 별도의 그룹으로 취급하지 않고, 높임/시제/공손
# 선어말 어미처럼 결합이 자유로운 선어말 어미만 (분리적 선어말어미)
# 취급한다. 예를 들어 '-느냐'에서 '-느-' 선어말어미를 별도로 취급하지
# 않는다. 이러한 교착적 선어말어미는 사전에도 어말어미와 붙인 형태로
# 기재되어 있고, 가능한 모든 어미의 가짓수가 몇 개 되지 않으므로 별도
# 그룹으로 취급할 필요가 없다.

groups = {}

####
# 높임 선어말

groups['-으시-'] = [
    {'rules': [['-시-', COND_V_ALL, ''],
               ['-시-', T_RIEUL, T_RIEUL],
               ['-으시-', COND_T_NOT_RIEUL, '']],
     'after': ['#용언', '#이다'],
     'notafter': ['계시다', '모시다'],
     'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#ㅎ불규칙',
                 '#준말용언'],
     },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS('-으시-', ['#용언']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS('-우시-', ['#용언']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS('-으시-', ['#용언']),
    # ㅎ불규칙
    HIEUH_IRREGULAR_TYPICAL_CLASS('-시-', ['#용언']),
]

####
# 과거 시제 선어말
# - '-었-'
# - '-어서였-'

groups['-었-'] = [
    {'rules': [['-었-', COND_EOA_NOT_AO, ''],
               ['-았-', COND_EOA_AO, ''],
               # 으불규칙 (하지만 규칙적)
               ['-' + V_A + T_SSANGSIOS + '-', COND_EU_AO, V_EU],
               ['-' + V_EO + T_SSANGSIOS + '-', COND_EU_NOT_AO, V_EU],
               ['-' + V_EO + T_SSANGSIOS + '-', COND_EU_EXCEPTIONS, V_EU],
               # 여불규칙 (하지만 규칙적)
               ['-였-', ENC('하'), ''],

               ## 줄임 형태
               ['-' + V_EO + T_SSANGSIOS + '-', COND_EOA_EO, V_EO],
               ['-' + V_A + T_SSANGSIOS + '-', COND_EOA_A, V_A],
               ['-' + V_A + T_SSANGSIOS + '-', COND_EU_AO, V_EU],
               ['-' + V_EO + T_SSANGSIOS + '-', COND_EU_NOT_AO, V_EU],
               ['-' + V_EO + T_SSANGSIOS + '-', COND_EU_EXCEPTIONS, V_EU],
               # 준말
               ['-' + V_WA + T_SSANGSIOS + '-', V_O, V_O],  # 오았 -> 왔
               ['-' + V_WEO + T_SSANGSIOS + '-', V_U, V_U],  # 우었 -> 웠
               ['-' + V_WAE + T_SSANGSIOS + '-', COND_EOA_OE,
                V_OE],  # 외었 -> 왜ㅆ
               ['-' + V_WA + T_SSANGSIOS + '-', ENC('놓'),
                V_O + T_HIEUH],  # 놓아 -> 놔
               ['-' + V_AE + T_SSANGSIOS + '-', ENC('하'), V_A],  # 하였 -> 했
               ['-' + V_YEO + T_SSANGSIOS + '-', V_I, V_I],  # 이었 -> 였
               ['-' + T_SSANGSIOS + '-', V_AE, ''],  # 애었 -> 앴
               ['-' + T_SSANGSIOS + '-', V_E, ''],  # 에었 -> 엤

               ['-어서였-', COND_EOA_NOT_AO, ''],
               ['-아서였-', COND_EOA_AO, ''],
               ['-' + V_EO + '서였-', V_EU, V_EU],
               # 으불규칙 (하지만 규칙적)
               ['-' + V_A + '서였-', COND_EU_AO, V_EU],
               ['-' + V_EO + '서였-', COND_EU_NOT_AO, V_EU],
               ['-' + V_EO + '서였-', COND_EU_EXCEPTIONS, V_EU],
               # 여불규칙 (하지만 규칙적)
               ['-여서였-', ENC('하'), ''],

               ['-' + V_EO + '서였-', COND_EOA_EO, V_EO],
               ['-' + V_A + '서였-', COND_EOA_A, V_A],
               ['-' + V_WA + '서였-', V_O, V_O],  # 오아 -> 와
               ['-' + V_WEO + '서였-', V_U, V_U],  # 우어 -> 워
               ['-' + V_WAE + '서였-', COND_EOA_OE, V_OE],  # 외어 -> 왜
               ['-' + V_WA + '서였-', ENC('놓'), V_O + T_HIEUH],  # 놓아 -> 놔
               ['-' + V_AE + '서였-', ENC('하'), V_A],  # 하여 -> 해
               ['-' + V_YEO + '서였-', V_I, V_I],  # 이어 -> 여
               ['-' + V_AE + '서였-', V_AE, V_AE],  # 애어 -> 애
               ['-' + V_E + '서였-', V_E, V_E],  # 에어 -> 에


               ],
     'after': ['#용언', '#이다', '-으시-'],
     'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#ㅎ불규칙',
                 '#러불규칙', '#르불규칙', '#우불규칙', '#준말용언'],
     },
    # ㄷ불규칙
    {'rules': [['-%s었-' % T_RIEUL, '[%s]%s' % (V_NOT_A_O, T_TIKEUT), T_TIKEUT],
               ['-%s았-' % T_RIEUL, '[%s]%s' % (V_A_O, T_TIKEUT), T_TIKEUT],

               ['-' + T_RIEUL + '어서였-', '[%s]%s' % (V_NOT_A_O, T_TIKEUT),
                T_TIKEUT],
               ['-' + T_RIEUL + '아서였-', '[%s]%s' % (V_A_O, T_TIKEUT),
                T_TIKEUT],
               ],
     'after': ['#용언'],
     'cond': ['#ㄷ불규칙'],
     },
    # ㅂ불규칙
    {'rules': [['-웠-', T_PIEUP, T_PIEUP],

               ['-워서였-', T_PIEUP, T_PIEUP],
               ],
     'after': ['#용언'],
     'notafter': ['곱다', '곱디곱다', '돕다'],
     'cond': ['#ㅂ불규칙'],
     },
    # ㅂ불규칙 중 예외적으로 '-와'가 붙는 경우
    {'rules': [['-왔-', T_PIEUP, T_PIEUP],

               ['-와서였-', T_PIEUP, T_PIEUP],
               ],
     'after': ['곱다', '곱디곱다', '돕다'],
     'cond': ['#ㅂ불규칙'],
     },
    # ㅅ불규칙
    {'rules': [['-었-', '[%s]%s' % (V_NOT_A_O, T_SIOS), T_SIOS],
               ['-았-', '[%s]%s' % (V_A_O, T_SIOS), T_SIOS],

               ['-어서였-', '[%s]%s' % (V_NOT_A_O, T_SIOS), T_SIOS],
               ['-아서였-', '[%s]%s' % (V_A_O, T_SIOS), T_SIOS],
               ],
     'after': ['#용언'],
     'cond': ['#ㅅ불규칙'],
     },
    # ㅎ불규칙
    {'rules': [['-' + V_AE + T_SSANGSIOS + '-', V_A + T_HIEUH,
                V_A + T_HIEUH],   # 파랗다
               ['-' + V_YAE + T_SSANGSIOS + '-', V_YA + T_HIEUH,
                V_YA + T_HIEUH],  # 하얗다
               ['-' + V_E + T_SSANGSIOS + '-', V_EO + T_HIEUH,
                V_EO + T_HIEUH],  # 누렇다
               ['-' + V_YE + T_SSANGSIOS + '-', V_YEO + T_HIEUH,
                V_YEO + T_HIEUH],  # 허옇다

               ['-' + V_AE + '서였-', V_A + T_HIEUH, V_A + T_HIEUH],   # 파랗다
               ['-' + V_YAE + '서였-', V_YA + T_HIEUH, V_YA + T_HIEUH],  # 하얗다
               ['-' + V_E + '서였-', V_EO + T_HIEUH, V_EO + T_HIEUH],  # 누렇다
               ['-' + V_YE + '서였-', V_YEO + T_HIEUH, V_YEO + T_HIEUH],  # 허옇다
               ],
     'after': ['#용언'],
     'notafter': ['그렇다', '고렇다', '이렇다', '요렇다', '저렇다', '조렇다',
                  '어떻다', '아무렇다'],
     'cond': ['#ㅎ불규칙'],
     },
    # ㅎ불규칙 지시형용사
    {'rules': [['-' + V_AE + T_SSANGSIOS + '-', V_EO + T_HIEUH,
                V_EO + T_HIEUH],

               ['-' + V_AE + '서였-', V_EO + T_HIEUH, V_EO + T_HIEUH],
               ],
     'after': ['그렇다', '고렇다', '이렇다', '요렇다', '저렇다', '조렇다',
               '어떻다', '아무렇다'],
     'cond': ['#ㅎ불규칙'],
     },
    # 러불규칙
    {'rules': [['-렀-', ENC('르'), ''],

               ['-러서였-', ENC('르'), ''],
               ],
     'after': ['#용언'],
     'cond': ['#러불규칙'],
     },
    # 르불규칙
    {'rules': [['-%s렀-' % T_RIEUL, COND_REU_NOT_AO, '르'],
               ['-%s랐-' % T_RIEUL, COND_REU_AO, '르'],

               ['-%s러서였-' % T_RIEUL, COND_REU_NOT_AO, '르'],
               ['-%s라서였-' % T_RIEUL, COND_REU_AO, '르'],
               ],
     'after': ['#용언'],
     'cond': ['#르불규칙'],
     },
    # 우불규칙
    {'rules': [['-' + V_EO + T_SSANGSIOS + '-', V_U, V_U],

               ['-' + V_EO + '서였-', V_U, V_U],
               ],
     'after': ['#용언'],
     'cond': ['#우불규칙'],
     },
]
# 대과거 시제 덧붙이기
for klass in groups['-었-']:
    new_rules = []
    for r in klass['rules']:
        new_rules.append([r[0][:-1] + '었-'] + r[1:])
    klass['rules'] += new_rules

####
# 미래 시제 선어말
# - '-겠-'
# - '-어서겠-'

groups['-겠-'] = [
    {'rules': [['-겠-', '', '']],
     # '-어야-'는 '-어야겠-' 형태를 위해서 허용
     'after': ['#용언', '#이다', '-으시-', '-었-', '-어야-'],
     },

    {'rules': [['-어서겠-', COND_EOA_NOT_AO, ''],
               ['-아서겠-', COND_EOA_AO, ''],
               # 으불규칙 (하지만 규칙적)
               ['-' + V_A + '서겠-', COND_EU_AO, V_EU],
               ['-' + V_EO + '서겠-', COND_EU_NOT_AO, V_EU],
               ['-' + V_EO + '서겠-', COND_EU_EXCEPTIONS, V_EU],
               # 여불규칙 (하지만 규칙적)
               ['-여서겠-', ENC('하'), ''],

               ['-' + V_EO + '서겠-', COND_EOA_EO, V_EO],
               ['-' + V_A + '서겠-', COND_EOA_A, V_A],
               ['-' + V_WA + '서겠-', V_O, V_O],  # 오아 -> 와
               ['-' + V_WEO + '서겠-', V_U, V_U],  # 우어 -> 워
               ['-' + V_WAE + '서겠-', COND_EOA_OE, V_OE],  # 외어 -> 왜
               ['-' + V_WA + '서겠-', ENC('놓'), V_O + T_HIEUH],  # 놓아 -> 놔
               ['-' + V_AE + '서겠-', ENC('하'), V_A],  # 하여 -> 해
               ['-' + V_YEO + '서겠-', V_I, V_I],  # 이어 -> 여
               ['-' + V_AE + '서겠-', V_AE, V_AE],  # 애어 -> 애
               ['-' + V_E + '서겠-', V_E, V_E],  # 에어 -> 에
               ],
     'after': ['#용언', '-으시-'],
     'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#ㅎ불규칙',
                 '#러불규칙', '#르불규칙', '#우불규칙', '#준말용언'],
     },
    # ㄷ불규칙
    {'rules': [['-%s어서겠-' % T_RIEUL, '[%s]%s' % (V_NOT_A_O, T_TIKEUT),
                T_TIKEUT],
               ['-%s아서겠-' % T_RIEUL, '[%s]%s' % (V_A_O, T_TIKEUT),
                T_TIKEUT],
               ],
     'after': ['#용언'],
     'cond': ['#ㄷ불규칙'],
     },
    # ㅂ불규칙
    {'rules': [['-워서겠-', T_PIEUP, T_PIEUP]],
     'after': ['#용언'],
     'notafter': ['곱다', '곱디곱다', '돕다'],
     'cond': ['#ㅂ불규칙'],
     },
    # ㅂ불규칙 중 예외적으로 '-와'가 붙는 경우
    {'rules': [['-와서겠-', T_PIEUP, T_PIEUP]],
     'after': ['곱다', '곱디곱다', '돕다'],
     'cond': ['#ㅂ불규칙'],
     },
    # ㅅ불규칙
    {'rules': [['-어서겠-', '[%s]%s' % (V_NOT_A_O, T_SIOS), T_SIOS],
               ['-아서겠-', '[%s]%s' % (V_A_O, T_SIOS), T_SIOS]],
     'after': ['#용언'],
     'cond': ['#ㅅ불규칙'],
     },
    # ㅎ불규칙
    {'rules': [['-' + V_AE + '서겠-', V_A + T_HIEUH, V_A + T_HIEUH],   # 파랗다
               ['-' + V_YAE + '서겠-', V_YA + T_HIEUH, V_YA + T_HIEUH],  # 하얗다
               ['-' + V_E + '서겠-', V_EO + T_HIEUH, V_EO + T_HIEUH],  # 누렇다
               ['-' + V_YE + '서겠-', V_YEO + T_HIEUH, V_YEO + T_HIEUH]],  # 허옇다
     'after': ['#용언'],
     'notafter': ['그렇다', '고렇다', '이렇다', '요렇다', '저렇다', '조렇다',
                  '어떻다', '아무렇다'],
     'cond': ['#ㅎ불규칙'],
     },
    # ㅎ불규칙 지시형용사
    {'rules': [['-' + V_AE + '서겠-', V_EO + T_HIEUH, V_EO + T_HIEUH]],
     'after': ['그렇다', '고렇다', '이렇다', '요렇다', '저렇다', '조렇다',
               '어떻다', '아무렇다'],
     'cond': ['#ㅎ불규칙'],
     },
    # 러불규칙
    {'rules': [['-러서겠-', ENC('르'), '']],
     'after': ['#용언'],
     'cond': ['#러불규칙'],
     },
    # 르불규칙
    {'rules': [['-%s러서겠-' % T_RIEUL, COND_REU_NOT_AO, '르'],
               ['-%s라서겠-' % T_RIEUL, COND_REU_AO, '르']],
     'after': ['#용언'],
     'cond': ['#르불규칙'],
     },
    # 우불규칙
    {'rules': [['-' + V_EO + '서겠-', V_U, V_U]],
     'after': ['#용언'],
     'cond': ['#우불규칙'],
     },
]

####
# 시제 선어말: -더-

groups['-더-'] = [
    {'rules': [['-더-', '', '']],
     'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
     },
]

####
# 연결: -어, -아
groups['-어'] = [
    {'rules': [['-어', COND_EOA_NOT_AO, ''],
               ['-아', COND_EOA_AO, ''],
               # 으불규칙 (하지만 규칙적)
               ['-' + V_A, COND_EU_AO, V_EU],
               ['-' + V_EO, COND_EU_NOT_AO, V_EU],
               ['-' + V_EO, COND_EU_EXCEPTIONS, V_EU],
               # 여불규칙 (하지만 규칙적)
               ['-여', ENC('하'), ''],

               ['-' + V_EO, COND_EOA_EO, V_EO],
               ['-' + V_A, COND_EOA_A, V_A],
               ['-' + V_WA, V_O, V_O],  # 오아 -> 와
               ['-' + V_WEO, V_U, V_U],  # 우어 -> 워
               ['-' + V_WAE, COND_EOA_OE, V_OE],  # 외어 -> 왜
               ['-' + V_WA, ENC('놓'), V_O + T_HIEUH],  # 놓아 -> 놔
               ['-' + V_AE, ENC('하'), V_A],  # 하여 -> 해
               ['-' + V_YEO, V_I, V_I],  # 이어 -> 여
               ['-' + V_AE, V_AE, V_AE],  # 애어 -> 애
               ['-' + V_E, V_E, V_E],  # 에어 -> 에
               ],
     'after': ['#용언', '-었-', '-겠-', '-으시-'],
     'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#ㅎ불규칙',
                 '#러불규칙', '#르불규칙', '#우불규칙', '#준말용언'],
     },
    # ㄷ불규칙
    {'rules': [['-%s어' % T_RIEUL, '[%s]%s' % (V_NOT_A_O, T_TIKEUT), T_TIKEUT],
               ['-%s아' % T_RIEUL, '[%s]%s' % (V_A_O, T_TIKEUT), T_TIKEUT]],
     'after': ['#용언'],
     'cond': ['#ㄷ불규칙'],
     },
    # ㅂ불규칙
    {'rules': [['-워', T_PIEUP, T_PIEUP]],
     'after': ['#용언'],
     'notafter': ['곱다', '곱디곱다', '돕다'],
     'cond': ['#ㅂ불규칙'],
     },
    # ㅂ불규칙 중 예외적으로 '-와'가 붙는 경우
    {'rules': [['-와', T_PIEUP, T_PIEUP]],
     'after': ['곱다', '곱디곱다', '돕다'],
     'cond': ['#ㅂ불규칙'],
     },
    # ㅅ불규칙
    {'rules': [['-어', '[%s]%s' % (V_NOT_A_O, T_SIOS), T_SIOS],
               ['-아', '[%s]%s' % (V_A_O, T_SIOS), T_SIOS]],
     'after': ['#용언'],
     'cond': ['#ㅅ불규칙'],
     },
    # ㅎ불규칙
    {'rules': [['-' + V_AE, V_A + T_HIEUH, V_A + T_HIEUH],   # 파랗다
               ['-' + V_YAE, V_YA + T_HIEUH, V_YA + T_HIEUH],  # 하얗다
               ['-' + V_E, V_EO + T_HIEUH, V_EO + T_HIEUH],  # 누렇다
               ['-' + V_YE, V_YEO + T_HIEUH, V_YEO + T_HIEUH]],  # 허옇다
     'after': ['#용언'],
     'notafter': ['그렇다', '고렇다', '이렇다', '요렇다', '저렇다', '조렇다',
                  '어떻다', '아무렇다'],
     'cond': ['#ㅎ불규칙'],
     },
    # ㅎ불규칙 지시형용사
    {'rules': [['-' + V_AE, V_EO + T_HIEUH, V_EO + T_HIEUH]],
     'after': ['그렇다', '고렇다', '이렇다', '요렇다', '저렇다', '조렇다',
               '어떻다', '아무렇다'],
     'cond': ['#ㅎ불규칙'],
     },
    # 러불규칙
    {'rules': [['-러', ENC('르'), '']],
     'after': ['#용언'],
     'cond': ['#러불규칙'],
     },
    # 르불규칙
    {'rules': [['-%s러' % T_RIEUL, COND_REU_NOT_AO, '르'],
               ['-%s라' % T_RIEUL, COND_REU_AO, '르']],
     'after': ['#용언'],
     'cond': ['#르불규칙'],
     },
    # 우불규칙
    {'rules': [['-' + V_EO, V_U, V_U]],
     'after': ['#용언'],
     'cond': ['#우불규칙'],
     },
]

####
# 연결: -어다, -아다 (동사)

# '-어' 재활용
groups['-어다'] = copy_group(groups['-어'])
for klass in groups['-어다']:
    if '#용언' in klass['after']:
        klass['after'].remove('#용언')
        klass['after'].append('#동사')
    elif klass['after'] == ['곱다', '곱디곱다', '돕다']:
        # 동사만
        klass['after'] = ['돕다']
    new_rule = []
    for r in klass['rules']:
        new_rule.append([r[0] + '다'] + r[1:])
        new_rule.append([r[0] + '다가'] + r[1:])
    klass['rules'] = new_rule

####
# 종결: -어라, -아라

groups['-어라'] = copy_group(groups['-어'])
for klass in groups['-어라']:
    for r in klass['rules']:
        r[0] = r[0] + '라'

####
# 종결: -거라, -너라

# 학교 문법 및 2008년 개정 표준국어대사전에 따르면 "-거라"를
# "-어라/아라"의 불규칙 형태가 아닌 별도의 어미로 본다.
#
# "-거라"를 허용하는 범위는 논란의 여지가 있다. 표준국어대사전에서는
# "-가다" 형태의 동사만 허용 학교 문법에서는 "-자다" 등 일부 동사에서도
# 허용, 실생활에서는 거의 모든 동사와 결합하곤 한다.
groups['-거라'] = [
    {'rules': [['-거라', '', '']],
     'after': ['#동사'],
     'cond': ['^.*가다$'],
     },
    {'rules': [['-너라', '', '']],
     'after': ['#동사'],
     'cond': ['^.*오다$'],
     },
]

####
# 연결: -어도, -아도

# '-어' 재활용
groups['-어도'] = copy_group(groups['-어'])
for klass in groups['-어도']:
    for r in klass['rules']:
        r[0] = r[0] + '도'
groups['-어도'][0]['after'].append('#이다')

####
# 연결: -어서, -아서

# '-어' 재활용
groups['-어서'] = copy_group(groups['-어'])
for klass in groups['-어서']:
    for r in klass['rules']:
        r[0] = r[0] + '서'
groups['-어서'][0]['after'].append('#이다')
attach_emphasis(groups['-어서'], ['는', T_NIEUN, '도', '요'])

####
# 연결: -어야, -아야

# '-어' 재활용
groups['-어야'] = copy_group(groups['-어'])
for klass in groups['-어야']:
    for r in klass['rules']:
        r[0] = r[0] + '야'
groups['-어야'][0]['after'].append('#이다')
attach_emphasis(groups['-어야'], ['만'])

####
# -어야-

# NOTE: 문법상 선어말 어미는 아니지만 '어야겠' ('어야하겠'의 준말)
# 형태를 만드는 용도.
# '-어야' 재활용
groups['-어야-'] = copy_group(groups['-어야'])
for klass in groups['-어야-']:
    for r in klass['rules']:
        r[0] = r[0] + '-'
# '셨어야겠다' 따위로 확장되지 않도록 앞에 시제 선어말 어미 금지
groups['-어야-'][0]['after'] = ['#용언', '#이다', '-으시-']

####
# 연결, 종결: -어야지, -아야지

# '-어' 재활용
groups['-어야지'] = copy_group(groups['-어'])
for klass in groups['-어야지']:
    for r in klass['rules']:
        r[0] = r[0] + '야지'
groups['-어야지'][0]['after'].append('#이다')
attach_emphasis(groups['-어야지'], ['요'])
# 지요 -> 죠 준말
for klass in groups['-어야지']:
    expanded = []
    for r in klass['rules']:
        if r[0].endswith('지요'):
            expanded.append([r[0][:-len('지요')] + '죠'] + r[1:])
    klass['rules'] += expanded

####
# 종결: -어요, -아요

# '-어' 재활용
groups['-어요'] = copy_group(groups['-어'])
for klass in groups['-어요']:
    for r in klass['rules']:
        r[0] = r[0] + '요'
groups['-어요'][0]['after'].append('#이다')
groups['-어요'] += [
    # 이다/아니다의 경우 -에요 가능, 줄임 이예요 => 예요
    {'rules': [['-에요', V_I, ''],
               ['-%s요' % V_YE, V_I, V_I]],
     'after': ['#이다', '아니다'],
     },
]

####
# 형사형 전성: -ㄹ, -을

groups['-을'] = [
    {'rules': [['-' + T_RIEUL, COND_V_ALL, ''],
               ['-' + T_RIEUL, T_RIEUL, T_RIEUL],
               ['-을', COND_T_NOT_RIEUL, '']],
     'after': ['#용언', '#이다', '-으시-', '-시오-', '-었-'],
     'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#ㅎ불규칙',
                 '#준말용언'],
     },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS('-을', ['#용언']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS('-울', ['#용언']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS('-을', ['#용언']),
    # ㅎ불규칙
    HIEUH_IRREGULAR_TYPICAL_CLASS('-' + T_RIEUL, ['#용언']),
]

####
# 종결: -ㄹ걸, -을걸

# '-을' 재활용
groups['-을걸'] = copy_group(groups['-을'])
for klass in groups['-을걸']:
    for r in klass['rules']:
        r[0] = r[0] + '걸'

####
# 종결: -ㄹ게, -을게

# 동사 전용
groups['-을게'] = [
    {'rules': [['-%s게' % T_RIEUL, COND_V_ALL, ''],
               ['-%s게' % T_RIEUL, T_RIEUL, T_RIEUL],
               ['-을게', COND_T_NOT_RIEUL, '']],
     'after': ['#동사'],
     'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#준말용언'],
     },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS('-을게', ['#동사']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS('-울게', ['#동사']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS('-을게', ['#동사']),
    # 동사이므로 ㅎ불규칙 해당 없음
]
attach_emphasis(groups['-을게'], ['요'])

####
# 연결: -ㄹ까, -을까

# '-을' 재활용
groups['-을까'] = copy_group(groups['-을'])
for klass in groups['-을까']:
    for r in klass['rules']:
        r[0] = r[0] + '까'
# ~ㄹ까요, -을까요 보조사
attach_emphasis(groups['-을까'], ['요'])

####
# 연결: -ㄹ망정, -을망정

# '-을' 재활용
groups['-을망정'] = copy_group(groups['-을'])
for klass in groups['-을망정']:
    for r in klass['rules']:
        r[0] = r[0] + '망정'

####
# 연결: -ㄹ수록, -을수록

# '-을' 재활용
groups['-을수록'] = copy_group(groups['-을'])
for klass in groups['-을수록']:
    for r in klass['rules']:
        r[0] = r[0] + '수록'

####
# 연결: -ㄹ지, -을지

# '-을' 재활용
groups['-을지'] = copy_group(groups['-을'])
for klass in groups['-을지']:
    for r in klass['rules']:
        r[0] = r[0] + '지'
attach_emphasis(groups['-을지'], ['는', T_NIEUN, '도'])

####
# 연결: -ㄹ지라도, -을지라도

# '-을' 재활용
groups['-을지라도'] = copy_group(groups['-을'])
for klass in groups['-을지라도']:
    for r in klass['rules']:
        r[0] = r[0] + '지라도'

####
# 연결: -ㄹ지언정, -을지언정

# '-을' 재활용
groups['-을지언정'] = copy_group(groups['-을'])
for klass in groups['-을지언정']:
    for r in klass['rules']:
        r[0] = r[0] + '지언정'

####
# 종결: -다


groups['-다'] = [
    {'rules': [['-다', '', '']],
     'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
     },
]

####
# 관형사형 전성: -는

groups['-는'] = [
    {'rules': [['-는', '[^%s]' % T_RIEUL, ''],
               ['-는', T_RIEUL, T_RIEUL]],
     'after': ['#동사', '^.*%s다$' % (V_I + T_SSANGSIOS), '^.*없다$',
               '^.*계시다$', '-으시-', '-겠-'],
     },
]

####
# 연결: -게

groups['-게'] = [
    {'rules': [['-게', '', ''],
               # ~하다 준말
               ['-케', COND_VOICED + ENC('하'), '하'],  # 하게 -> 케
               ['-게', COND_UNVOICED + ENC('하'), '하'],  # 하게 -> 게
               ],
     'after': ['#용언', '-으시-'],
     },
]
attach_emphasis(groups['-게'], ['도'])
attach_emphasis(groups['-게'], ['까지'])

####
# 종결: -게나
attach_emphasis(groups['-게'], ['나'])

####
# 연결: -다가

groups['-다가'] = [
    {'rules': [['-다가', '', '']],
     'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
     },
]

####
# 관형사형 전성: -ㄴ, -은

groups['-은'] = [
    {'rules': [['-' + T_NIEUN, COND_V_ALL, ''],
               ['-' + T_NIEUN, T_RIEUL, T_RIEUL],
               ['-은', COND_T_NOT_RIEUL, '']],
     'after': ['#용언', '#이다', '-으시-'],
     'notafter': ['^.*%s다$' % (V_I + T_SSANGSIOS), '^.*없다$'],
     'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#ㅎ불규칙',
                 '#준말용언'],
     },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS('-은', ['#용언']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS('-운', ['#용언']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS('-은', ['#용언']),
    # ㅎ불규칙
    HIEUH_IRREGULAR_TYPICAL_CLASS('-' + T_NIEUN, ['#용언']),
]

####
# 연결: -지

####
# 종결: -지

groups['-지'] = [
    {'rules': [['-지', '', ''],
               # ~하다 준말
               ['-치', COND_VOICED + ENC('하'), '하'],  # 하지 -> 치
               ['-지', COND_UNVOICED + ENC('하'), '하']],  # 하지 -> 지
     'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
     },
]
attach_emphasis(groups['-지'], ['는', T_NIEUN, '도', '요'])
# 지요 -> 죠 준말
groups['-지'][0]['rules'].append(['-죠', '', ''])


####
# 연결: -지마는

groups['-지마는'] = [
    {'rules': [['-지마는', '', ''],
               ['-지만', '', ''],
               # ~하다 준말
               ['-치만', COND_VOICED + ENC('하'), '하'],   # 하지만 -> 치만
               ['-지만', COND_UNVOICED + ENC('하'), '하'],  # 하지만 -> 지만
               ['-치마는', COND_VOICED + ENC('하'), '하'],  # 하지마는 -> 치마는
               ['-지마는', COND_UNVOICED + ENC('하'), '하'],  # 하지마는 -> 치마는
               ],
     'after': ['#용언', '#이다', '-었-', '-겠-'],
     },
]

####
# 연결: -며, -으며

groups['-으며'] = [
    {'rules': [['-며', COND_V_OR_RIEUL, ''],
               ['-으며', COND_T_NOT_RIEUL, '']],
     'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
     'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#ㅎ불규칙',
                 '#준말용언'],
     },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS('-으며', ['#용언']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS('-우며', ['#용언']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS('-으며', ['#용언']),
    # ㅎ불규칙
    HIEUH_IRREGULAR_TYPICAL_CLASS('-며', ['#용언']),
]

####
# 종결: -ㅂ니다, -습니다

groups['-습니다'] = [
    {'rules': [['-%s니다' % T_PIEUP, COND_V_ALL, ''],
               ['-%s니다' % T_PIEUP, T_RIEUL, T_RIEUL],
               ['-습니다', COND_T_NOT_RIEUL, '']],
     'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
     },
]

####
# 종결: -ㅂ니까, -습니까

groups['-습니까'] = [
    {'rules': [['-%s니까' % T_PIEUP, COND_V_ALL, ''],
               ['-%s니까' % T_PIEUP, T_RIEUL, T_RIEUL],
               ['-습니까', COND_T_NOT_RIEUL, '']],
     'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
     },
]

####
# 연결: -고

####
# 종결: -고

groups['-고'] = [
    {'rules': [['-고', '', '']],
     'after': ['#용언', '#이다', '-'],
     'notafter': ['-으리-', '-더-'],
     },
]
attach_emphasis(groups['-고'], ['요'])

####
# 연결: -고는

groups['-고는'] = [
    {'rules': [['-고는', '', ''],
               ['-곤', '', '']],
     'after': ['#동사', '-으시-'],
     },
]

####
# 연결: -고도

groups['-고도'] = [
    {'rules': [['-고도', '', '']],
     'after': ['#용언', '#이다', '-으시-'],
     },
]

####
# 연결: -고서

groups['-고서'] = [
    {'rules': [['-고서', '', '']],
     'after': ['#용언', '#이다', '-으시-'],
     },
]

####
# 연결: -고자

groups['-고자'] = [
    {'rules': [['-고자', '', '']],
     'after': ['#동사', '^.*있다$', '^.*없다$', '^.*계시다$', '-으시-'],
     },
]

####
# 종결: -세요, -으세요 (-시어요, -으시어요 축약)

groups['-으세요'] = [
    {'rules': [['-세요', COND_V_ALL, ''],
               ['-세요', T_RIEUL, T_RIEUL],
               ['-으세요', COND_T_NOT_RIEUL, '']],
     'after': ['#용언', '#이다'],
     'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#ㅎ불규칙',
                 '#준말용언'],
     },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS('-으세요', ['#용언']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS('-우세요', ['#용언']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS('-으세요', ['#용언']),
    # ㅎ불규칙
    HIEUH_IRREGULAR_TYPICAL_CLASS('-세요', ['#용언']),
]

####
# 연결: -거나

groups['-거나'] = [
    {'rules': [['-거나', '', ''],
               # 준말
               ['-건', '', '']],
     'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-', '-으옵-'],
     },
]

####
# 연결: -려, -으려

groups['-으려'] = [
    {'rules': [['-려', COND_V_OR_RIEUL, ''],
               ['-으려', COND_T_NOT_RIEUL, '']],
     'after': ['#동사', '-으시-'],
     'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#준말용언'],
     },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS('-으려', ['#동사']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS('-우려', ['#동사']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS('-으려', ['#동사']),
    # 동사이므로 ㅎ불규칙 해당 없음
]

####
# 연결: -려고, -으려고

# '-으려' 재활용
groups['-으려고'] = copy_group(groups['-으려'])
for klass in groups['-으려고']:
    for r in klass['rules']:
        r[0] = r[0] + '고'

####
# 연결: -려다, -으려다 (려고 하다)

# '-으려' 재활용
groups['-으려다'] = copy_group(groups['-으려'])
for klass in groups['-으려다']:
    for r in klass['rules']:
        r[0] = r[0] + '다'

####
# 연결: -려는, -으려는 (려고 하는)

# '-으려' 재활용
groups['-으려는'] = copy_group(groups['-으려'])
for klass in groups['-으려는']:
    for r in klass['rules']:
        r[0] = r[0] + '는'

####
# 연결: -려면, -으려면

# '-으려' 재활용
groups['-으려면'] = copy_group(groups['-으려'])
for klass in groups['-으려면']:
    for r in klass['rules']:
        r[0] = r[0] + '면'

####
# 연결: -도록

groups['-도록'] = [
    {'rules': [['-도록', '', ''],
               # ~하다 준말
               ['-토록', COND_VOICED + ENC('하'), '하'],  # 하도록 -> 토록
               ['-도록', COND_UNVOICED + ENC('하'), '하'],  # 하도록 -> 도록
               ],
     'after': ['#동사', '-으시-',
               '#형용사'],  # FIXME: 일부 형용사만 허용하지만 구분하기에는 너무 많다.
     },
]

####
# 연결: -는데

groups['-는데'] = [
    {'rules': [['-는데', COND_NOT_RIEUL, ''],
               ['-는데', T_RIEUL, T_RIEUL]],
     'after': ['#동사', '^.*있다$', '^.*없다$', '^.*계시다$', '-으시-', '-었-', '-겠-'],
     },
]
attach_emphasis(groups['-는데'], ['도', '요'])

####
# 연결: -나, -으나

groups['-으나'] = [
    {'rules': [['-나', COND_V_ALL, ''],
               ['-나', T_RIEUL, T_RIEUL],
               ['-으나', COND_T_NOT_RIEUL, '']],
     'after': ['#용언', '#이다', '-으시-', '-사오-', '-었-', '-겠-'],
     'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#ㅎ불규칙',
                 '#준말용언'],
     },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS('-으나', ['#용언']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS('-우나', ['#용언']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS('-으나', ['#용언']),
    # ㅎ불규칙
    HIEUH_IRREGULAR_TYPICAL_CLASS('-나', ['#용언']),
]

####
# 종결: -나 (동사, 물음)

groups['-나'] = [
    {'rules': [['-나', COND_NOT_RIEUL, ''],
               ['-나', T_RIEUL, T_RIEUL]],
     'after': ['#용언', '-으시-', '-었-', '-겠-'],
     },
]
attach_emphasis(groups['-나'], ['요'])

####
# 연결: -다시피

groups['-다시피'] = [
    {'rules': [['-다시피', '', '']],
     'after': ['#동사', '-으시-', '-었-', '-겠-'],
     },
]

####
# 종결: -ㅂ시다, -읍시다

groups['-읍시다'] = [
    {'rules': [['-%s시다' % T_PIEUP, COND_V_ALL, ''],
               ['-%s시다' % T_PIEUP, T_RIEUL, T_RIEUL],
               ['-읍시다', COND_T_NOT_RIEUL, '']],
     'after': ['#동사', '-으시-'],
     'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#준말용언'],
     },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS('-읍시다', ['#동사']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS('-웁시다', ['#동사']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS('-읍시다', ['#동사']),
    # 동사이므로 ㅎ불규칙 해당 없음
]

####
# 연결: -자

groups['-자'] = [
    {'rules': [['-자', '', '']],
     'after': ['#용언', '#이다', '-으시-', '-었-'],  # TODO: 일부 형용사
     },
]

####
# 연결: -기에,-길래

groups['-기에'] = [
    {'rules': [['-기에', '', ''],
               ['-길래', '', '']],
     'after': ['#용언', '#이다', '-으시-', '-었-'],  # TODO: 일부 형용사
     },
]

####
# 연결: -듯

groups['-듯'] = [
    {'rules': [['-듯', '', ''],
               ['-듯이', '', '']],
     'after': ['#용언', '#이다'],
     },
]

####
# 연결: -다면

groups['-다면'] = [
    {'rules': [['-다면', '', '']],
     'after': ['#형용사', '-으시-', '-었-', '-겠-'],
     },
]

####
# 연결: -다면서

groups['-다면서'] = [
    {'rules': [['-다면서', '', ''],
               ['-다며', '', '']],
     'after': ['#형용사', '-으시-', '-었-', '-겠-'],
     },
]
attach_emphasis(groups['-다면서'], ['요'])

####
# 종결: -자고

groups['-자고'] = [
    {'rules': [['-자고', '', '']],
     'after': ['#동사'],
     },
]
attach_emphasis(groups['-자고'], ['요'])

####
# 연결: -기로

groups['-기로'] = [
    {'rules': [['-기로', '', ''],
               # ~하다 준말
               ['-키로', COND_VOICED + ENC('하'), '하'],  # 하기로 -> 키로
               ['-기로', COND_UNVOICED + ENC('하'), '하'],  # 하기로 -> 기로
               ],
     'after': ['#용언', '#이다', '-'],
     'notafter': ['-더-', '-으리-'],
     },
]

####
# 종결: -라, -으라

groups['-으라'] = [
    {'rules': [['-라', COND_V_OR_RIEUL, ''],
               ['-으라', COND_T_NOT_RIEUL, '']],
     'after': ['#동사', '-으시-'],
     'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#준말용언'],
     },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS('-으라', ['#동사']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS('-우라', ['#동사']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS('-으라', ['#동사']),
    # 동사이므로 ㅎ불규칙 해당 없음
]

####
# 연결: -라고, -으라고

groups['-으라고'] = [
    {'rules': [['-라고', COND_V_OR_RIEUL, ''],
               ['-으라고', COND_T_NOT_RIEUL, '']],
     'after': ['#동사', '#이다', '아니다', '-으시-', '-더-', '-으리-'],
     'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#준말용언'],
     },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS('-으라고', ['#동사']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS('-우라고', ['#동사']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS('-으라고', ['#동사']),
    # 동사이므로 ㅎ불규칙 해당 없음
]
attach_emphasis(groups['-으라고'], ['요'])

####
# 연결: -라는, -으라는 (라고 하는)

groups['-으라는'] = [
    {'rules': [['-라는', COND_V_OR_RIEUL, ''],
               ['-으라는', COND_T_NOT_RIEUL, ''],
               ['-란', COND_V_OR_RIEUL, ''],
               ['-으란', COND_T_NOT_RIEUL, '']],
     'after': ['#동사', '#이다', '아니다', '-으시-', '-더-', '-으리-'],
     'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#준말용언'],
     },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS('-으라는', ['#동사']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS('-우라는', ['#동사']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS('-으라는', ['#동사']),
    # 동사이므로 ㅎ불규칙 해당 없음
]

####
# 연결: -라면, -으라면 (라고 하면)

groups['-으라면'] = [
    {'rules': [['-라면', COND_V_OR_RIEUL, ''],
               ['-으라면', COND_T_NOT_RIEUL, '']],
     'after': ['#동사', '#이다', '아니다', '-으시-', '-더-', '-으리-'],
     'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#준말용언'],
     },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS('-으라면', ['#동사']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS('-우라면', ['#동사']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS('-으라면', ['#동사']),
    # 동사이므로 ㅎ불규칙 해당 없음
]

####
# 연결: -으래도,-래도 (라고 해도)

groups['-으래도'] = [
    {'rules': [['-래도', COND_V_OR_RIEUL, ''],
               ['-으래도', COND_T_NOT_RIEUL, '']],
     'after': ['#동사', '#이다', '아니다', '-으시-', '-더-', '-으리-'],
     'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#준말용언'],
     },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS('-으래도', ['#동사']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS('-우래도', ['#동사']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS('-으래도', ['#동사']),
    # 동사이므로 ㅎ불규칙 해당 없음
]

####
# 연결 -ㄴ데, -은데

groups['-은데'] = [
    {'rules': [['-%s데' % T_NIEUN, COND_V_OR_RIEUL, ''],
               ['-%s데' % T_NIEUN, T_RIEUL, T_RIEUL],
               ['-은데', COND_T_NOT_RIEUL, '']],
     'after': ['#형용사', '#이다', '-으시-', '-사오-'],
     'notafter': ['^.*있다$', '^.*없다$'],
     'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#ㅎ불규칙',
                 '#준말용언'],
     },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS('-은데', ['#형용사']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS('-운데', ['#형용사']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS('-은데', ['#형용사']),
    # ㅎ불규칙
    HIEUH_IRREGULAR_TYPICAL_CLASS('-%s데' % T_NIEUN, ['#형용사']),
]
attach_emphasis(groups['-은데'], ['도', '요'])

####
# 명사형 전성: -기

groups['-기'] = [
    {'rules': [['-기', '', ''],
               # ~하다 준말
               ['-키', COND_VOICED + ENC('하'), '하'],  # 하기 -> 키
               ['-기', COND_UNVOICED + ENC('하'), '하'],  # 하기 -> 기
               ],
     'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
     },
]
# 조사
# FIXME: 일단 모든 조사 허용
attach_continuation_flags(groups['-기'], [flags.josa_ida_flag] +
                          list(range(flags.josas_flag_start,
                                     flags.josas_flag_end)))

####
# 명사형 전성: -음

groups['-음'] = [
    {'rules': [['-' + T_MIEUM, COND_V_ALL, ''],
               ['-' + T_RIEUL_MIEUM, T_RIEUL, T_RIEUL],
               ['-음', COND_T_NOT_RIEUL, '']],
     'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
     'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#ㅎ불규칙',
                 '#준말용언'],
     },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS('-음', ['#용언']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS('-움', ['#용언']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS('-음', ['#용언']),
    # ㅎ불규칙
    HIEUH_IRREGULAR_TYPICAL_CLASS('-' + T_MIEUM, ['#용언']),
]
# 조사
# FIXME: 일단 모든 조사 허용
attach_continuation_flags(groups['-음'], [flags.josa_ida_flag] +
                          list(range(flags.josas_flag_start,
                                     flags.josas_flag_end)))

####
# 종결: -ㄴ다, -는다

groups['-는다'] = [
    {'rules': [['-%s다' % T_NIEUN, COND_V_OR_RIEUL, ''],
               ['-%s다' % T_NIEUN, T_RIEUL, T_RIEUL],
               ['-는다', COND_T_NOT_RIEUL, '']],
     'after': ['#동사', '-으시-'],
     },
]

####
# 연결: -ㄴ다고, -는다고

groups['-는다고'] = [
    {'rules': [['-%s다고' % T_NIEUN, COND_V_ALL, ''],
               ['-%s다고' % T_NIEUN, T_RIEUL, T_RIEUL],
               ['-는다고', COND_T_NOT_RIEUL, '']],
     'after': ['#동사', '-으시-'],
     },
]

####
# 연결: -ㄴ다는, -는다는 (는다고 하는)

groups['-는다는'] = [
    {'rules': [['-%s다는' % T_NIEUN, COND_V_ALL, ''],
               ['-%s다는' % T_NIEUN, T_RIEUL, T_RIEUL],
               ['-는다는', COND_T_NOT_RIEUL, '']],
     'after': ['#동사', '-으시-'],
     },
]

####
# 연결: -ㄴ단, -는단 (는다고 하는, 는다고 한)

groups['-는단'] = [
    {'rules': [['-%s단' % T_NIEUN, COND_V_ALL, ''],
               ['-%s단' % T_NIEUN, T_RIEUL, T_RIEUL],
               ['-는단', COND_T_NOT_RIEUL, '']],
     'after': ['#동사', '-으시-'],
     },
]

####
# 연결: -ㄴ다면, -는다면

groups['-는다면'] = [
    {'rules': [['-%s다면' % T_NIEUN, COND_V_ALL, ''],
               ['-%s다면' % T_NIEUN, T_RIEUL, T_RIEUL],
               ['-는다면', COND_T_NOT_RIEUL, '']],
     'after': ['#동사', '-으시-'],
     },
]

####
# 종결: -ㄴ다면서, -는다면서

groups['-는다면서'] = [
    {'rules': [['-%s다면서' % T_NIEUN, COND_V_ALL, ''],
               ['-%s다면서' % T_NIEUN, T_RIEUL, T_RIEUL],
               ['-는다면서', COND_T_NOT_RIEUL, ''],
               ['-%s다며' % T_NIEUN, COND_V_ALL, ''],
               ['-%s다며' % T_NIEUN, T_RIEUL, T_RIEUL],
               ['-는다며', COND_T_NOT_RIEUL, ''],
               ],
     'after': ['#동사', '-으시-'],
     },
]
attach_emphasis(groups['-는다면서'], ['요'])

####
# 종결: -는군

groups['-는군'] = [
    {'rules': [['-는군', COND_NOT_RIEUL, ''],
               ['-는군', T_RIEUL, T_RIEUL]],
     'after': ['#동사', '-으시-'],
     },
]
attach_emphasis(groups['-는군'], ['요'])

####
# 종결: -는구나

groups['-는구나'] = [
    {'rules': [['-는구나', COND_NOT_RIEUL, ''],
               ['-는구나', T_RIEUL, T_RIEUL]],
     'after': ['#동사', '-으시-'],
     },
]

####
# 연결, 종결: -는지

groups['-는지'] = [
    {'rules': [['-는지', COND_NOT_RIEUL, ''],
               ['-는지', T_RIEUL, T_RIEUL]],
     'after': ['#동사', '^.*있다$', '^.*없다$', '^.*계시다$', '-으시-', '-었-', '-겠-'],
     },
]
attach_emphasis(groups['-는지'], ['요'])
# 보조사 안 붙은 경우만 조사 허용
for rule in groups['-는지'][0]['rules']:
    if rule[0] == '-는지':
        rule.append([flags.josa_ida_flag] + list(range(flags.josas_flag_start,
                                                       flags.josas_flag_end)))

####
# 연결: -면, -으면

groups['-으면'] = [
    {'rules': [['-면', COND_V_OR_RIEUL, ''],
               ['-으면', COND_T_NOT_RIEUL, '']],
     'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
     'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#ㅎ불규칙',
                 '#준말용언'],
     },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS('-으면', ['#용언']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS('-우면', ['#용언']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS('-으면', ['#용언']),
    # ㅎ불규칙
    HIEUH_IRREGULAR_TYPICAL_CLASS('-면', ['#용언']),
]

####
# 연결: -면서, -으면서

# '-으면' 재활용
groups['-으면서'] = [k.copy() for k in groups['-으면']]
for klass in groups['-으면서']:
    new_rule = []
    for r in klass['rules']:
        new_rule.append([r[0] + '서'] + r[1:])
    klass['rules'] = new_rule
attach_emphasis(groups['-으면서'], ['도'])

####
# 연결: -자마자

groups['-자마자'] = [
    {'rules': [['-자마자', '', '']],
     'after': ['#동사', '-으시-'],
     },
]

####
# 관형사형 전성: -던

groups['-던'] = [
    {'rules': [['-던', '', '']],
     'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
     },
]

####
# 연결: -ㄴ가, -은가

####
# 의문형 종결: -ㄴ가, -은가

groups['-은가'] = [
    {'rules': [['-%s가' % T_NIEUN, COND_V_ALL, ''],
               ['-%s가' % T_NIEUN, T_RIEUL, T_RIEUL],
               ['-은가', COND_T_NOT_RIEUL, '']],
     'after': ['#형용사', '#이다', '-으시-'],
     'notafter': ['^.*있다$', '^.*없다$'],
     'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#ㅎ불규칙',
                 '#준말용언'],
     },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS('-은가', ['#형용사']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS('-운가', ['#형용사']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS('-은가', ['#형용사']),
    # ㅎ불규칙
    HIEUH_IRREGULAR_TYPICAL_CLASS('-%s가' % T_NIEUN, ['#형용사']),
]
attach_emphasis(groups['-은가'], ['요'])

####
# 연결: -니까, -으니까

groups['-으니까'] = [
    {'rules': [['-니까', COND_V_ALL, ''],
               ['-니까', T_RIEUL, T_RIEUL],
               ['-으니까', COND_T_NOT_RIEUL, '']],
     'after': ['#용언', '#이다', '-으시-', '-오-', '-더-', '-었-', '-겠-'],
     'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#ㅎ불규칙',
                 '#준말용언'],
     },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS('-으니까', ['#용언']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS('-우니까', ['#용언']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS('-으니까', ['#용언']),
    # ㅎ불규칙
    HIEUH_IRREGULAR_TYPICAL_CLASS('-니까', ['#용언']),
]
attach_emphasis(groups['-으니까'], ['요'])

####
# 연결: -라면

groups['-라면'] = [
    {'rules': [['-라면', '', '']],
     'after': ['#이다', '아니다', '-으시-', '-더-', '-으리-'],
     },
]

####
# 연결: -로구나

groups['-로구나'] = [
    {'rules': [['-로구나', '', '']],
     'after': ['#이다', '아니다', '-으시-'],
     },
]

####
# 연결: -ㄴ지, -은지

groups['-은지'] = [
    {'rules': [['-%s지' % T_NIEUN, COND_V_ALL, ''],
               ['-%s지' % T_NIEUN, T_RIEUL, T_RIEUL],
               ['-은지', COND_T_NOT_RIEUL, '']],
     'after': ['#이다', '#형용사', '-으시-'],
     'notafter': ['^.*있다$', '^.*없다$'],
     'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#ㅎ불규칙',
                 '#준말용언'],
     },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS('-은지', ['#형용사']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS('-운지', ['#형용사']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS('-은지', ['#형용사']),
    # ㅎ불규칙
    HIEUH_IRREGULAR_TYPICAL_CLASS('-%s지' % T_NIEUN, ['#형용사']),
]
attach_emphasis(groups['-은지'], ['는', T_NIEUN, '도', '요'])

####
# 종결: -십시오, -으십시오

groups['-으십시오'] = [
    {'rules': [['-십시오', COND_V_ALL, ''],
               ['-십시오', T_RIEUL, T_RIEUL],
               ['-으십시오', COND_T_NOT_RIEUL, '']],
     'after': ['#동사'],
     'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#준말용언'],
     },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS('-으십시오', ['#동사']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS('-우십시오', ['#동사']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS('-으십시오', ['#동사']),
    # 동사이므로 ㅎ불규칙 해당 없음
]

####
# 연결: -므로, -으므로

groups['-으므로'] = [
    {'rules': [['-므로', COND_V_OR_RIEUL, ''],
               ['-으므로', COND_T_NOT_RIEUL, '']],
     'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
     'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#ㅎ불규칙',
                 '#준말용언'],
     },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS('-으므로', ['#용언']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS('-우므로', ['#용언']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS('-으므로', ['#용언']),
    # ㅎ불규칙
    HIEUH_IRREGULAR_TYPICAL_CLASS('-므로', ['#용언']),
]

####
# 연결: -다고

groups['-다고'] = [
    {'rules': [['-다고', '', '']],
     'after': ['#형용사', '-으시-', '-었-', '-겠-'],
     },
]
attach_emphasis(groups['-다고'], ['요'])

####
# 연결: -다는 (다고 하는)

groups['-다는'] = [
    {'rules': [['-다는', '', ''],
               ['-단', '', '']],
     'after': ['#용언', '-으시-', '-었-', '-겠-'],
     },
]

####
# 종결: -대 (다고 해)

groups['-대'] = [
    {'rules': [['-대', '', '']],
     'after': ['#용언', '-으시-', '-었-', '-겠-'],
     },
]

####
# 연결: -대도 (다고 하여도)

groups['-대도'] = [
    {'rules': [['-대도', '', '']],
     'after': ['#형용사', '-으시-', '-었-', '-겠-'],
     },
]

####
# 연결: -대서 (다고 하여서)

groups['-대서'] = [
    {'rules': [['-대서', '', '']],
     'after': ['#형용사', '-으시-', '-었-', '-겠-'],
     },
]

####
# 연결: -더라도

groups['-더라도'] = [
    {'rules': [['-더라도', '', '']],
     'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
     },
]

####
# 연결: -러, -으러

groups['-으러'] = [
    {'rules': [['-러', COND_V_OR_RIEUL, ''],
               ['-으러', COND_T_NOT_RIEUL, '']],
     'after': ['#동사', '-으시-'],
     'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#준말용언'],
     },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS('-으러', ['#동사']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS('-우러', ['#동사']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS('-으러', ['#동사']),
    # 동사이므로 ㅎ불규칙 해당 없음
]

####
# 종결: -네

groups['-네'] = [
    {'rules': [['-네', COND_NOT_RIEUL, ''],
               ['-네', T_RIEUL, T_RIEUL]],
     'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
     },
]
attach_emphasis(groups['-네'], ['요'])

####
# 종결: -니, -으니

####
# 연결: -니, -으니

groups['-으니'] = [
    {'rules': [['-니', COND_V_ALL, ''],
               ['-니', T_RIEUL, T_RIEUL],
               ['-으니', COND_T_NOT_RIEUL, '']],
     'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-', '-오-', '-더-'],
     'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#ㅎ불규칙',
                 '#준말용언'],
     },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS('-으니', ['#용언']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS('-우니', ['#용언']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS('-으니', ['#용언']),
    # ㅎ불규칙
    HIEUH_IRREGULAR_TYPICAL_CLASS('-니', ['#용언']),
]

####
# 의문형 종결: -니 (위와 구별된다)

groups['-니?'] = [
    {'rules': [['-니', COND_NOT_RIEUL, ''],
               ['-니', T_RIEUL, T_RIEUL]],
     'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
     },
]

# ####
# 의문형 종결: -으니 (구어체)

# groups['-으니?'] = [
#     {'rules': [['-으니', COND_T_NOT_RIEUL, '']],
#      'after': ['#형용사'],
#     },
# ]

####
# 종결: -군

groups['-군'] = [
    {'rules': [['-군', '', '']],
     'after': ['#형용사', '#이다', '-으시-', '-었-', '-겠-', '-더-'],
     },
]
attach_emphasis(groups['-군'], ['요'])

####
# 종결: -구나

groups['-구나'] = [
    {'rules': [['-구나', '', '']],
     'after': ['#형용사', '#이다', '-으시-', '-었-', '-겠-'],
     },
]

####
# 종결: -으냐 (형용사)

groups['-으냐'] = [
    {'rules': [['-냐', COND_V_ALL, ''],
               ['-냐', T_RIEUL, T_RIEUL],
               ['-으냐', COND_T_NOT_RIEUL, '']],
     'after': ['#형용사', '#이다'],
     'notafter': ['^.*있다$', '^.*없다$'],
     'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#ㅎ불규칙',
                 '#준말용언'],
     },
    # NOTE: 어간과 결합하지 않고 '-었-' 및 '-겠-' 선어말 어미와 결합할
    # 경우에는 받침이 있음에도 "-었으냐", "-겠느냐"가 아니라 "-었냐",
    # "-겠냐" 형태가 되므로, 선어말 어미 결합하는 부분은 별도로 구분해
    # 모든 음절과 결합을 허용한다.
    {'rules': [['-냐', '', '']],
     'after': ['-으시-', '-었-', '-겠-'],
     },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS('-으냐', ['#형용사']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS('-우냐', ['#형용사']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS('-으냐', ['#형용사']),
    # ㅎ불규칙
    HIEUH_IRREGULAR_TYPICAL_CLASS('-냐', ['#형용사']),
]

####
# 종결: -으냐고 (형용사)

groups['-으냐고'] = [k.copy() for k in groups['-으냐']]
for klass in groups['-으냐고']:
    new_rule = []
    for r in klass['rules']:
        new_rule.append([r[0] + '고'] + r[1:])
    klass['rules'] = new_rule
attach_emphasis(groups['-으냐고'], ['요'])

####
# 연결: -으냐네 (-으냐고 하네)

groups['-으냐네'] = [k.copy() for k in groups['-으냐']]
for klass in groups['-으냐네']:
    new_rule = []
    for r in klass['rules']:
        new_rule.append([r[0] + '네'] + r[1:])
    klass['rules'] = new_rule

####
# 연결: -으냐는 (-으냐고 하는)

groups['-으냐는'] = [k.copy() for k in groups['-으냐']]
for klass in groups['-으냐는']:
    new_rule = []
    for r in klass['rules']:
        new_rule.append([r[0] + '는'] + r[1:])
    klass['rules'] = new_rule

####
# 연결: -으냐니 (-으냐고 하니)

groups['-으냐니'] = [k.copy() for k in groups['-으냐']]
for klass in groups['-으냐니']:
    new_rule = []
    for r in klass['rules']:
        new_rule.append([r[0] + '니'] + r[1:])
    klass['rules'] = new_rule

####
# 연결: -으냐니까 (-으냐고 하니)

groups['-으냐니까'] = [k.copy() for k in groups['-으냐']]
for klass in groups['-으냐니까']:
    new_rule = []
    for r in klass['rules']:
        new_rule.append([r[0] + '니까'] + r[1:])
    klass['rules'] = new_rule

####
# 연결: -으냐며 (-으냐고 하며)

groups['-으냐며'] = [k.copy() for k in groups['-으냐']]
for klass in groups['-으냐며']:
    new_rule = []
    for r in klass['rules']:
        new_rule.append([r[0] + '며'] + r[1:])
    klass['rules'] = new_rule

####
# 연결: -으냐면 (-으냐고 하면)

groups['-으냐면'] = [k.copy() for k in groups['-으냐']]
for klass in groups['-으냐면']:
    new_rule = []
    for r in klass['rules']:
        new_rule.append([r[0] + '면'] + r[1:])
    klass['rules'] = new_rule

####
# 연결: -으냐면서 (-으냐고 하면서)

groups['-으냐면서'] = [k.copy() for k in groups['-으냐']]
for klass in groups['-으냐면서']:
    new_rule = []
    for r in klass['rules']:
        new_rule.append([r[0] + '면서'] + r[1:])
    klass['rules'] = new_rule

####
# 종결: -느냐 (동사)

groups['-느냐'] = [
    {'rules': [['-느냐', COND_NOT_RIEUL, ''],
               ['-느냐', T_RIEUL, T_RIEUL]],
     'after': ['#동사', '^.*있다$', '^.*없다$', '^.*계시다$', '-으시-', '-었-', '-겠-'],
     },
]

####
# 종결: -느냐고 (동사)

groups['-느냐고'] = [k.copy() for k in groups['-느냐']]
for klass in groups['-느냐고']:
    new_rule = []
    for r in klass['rules']:
        new_rule.append([r[0] + '고'] + r[1:])
    klass['rules'] = new_rule
attach_emphasis(groups['-느냐고'], ['요'])

####
# 연결: -느냐네 (-느냐고 하네)

groups['-느냐네'] = [k.copy() for k in groups['-느냐']]
for klass in groups['-느냐네']:
    new_rule = []
    for r in klass['rules']:
        new_rule.append([r[0] + '네'] + r[1:])
    klass['rules'] = new_rule

####
# 연결: -느냐는 (-느냐고 하는)

groups['-느냐는'] = [k.copy() for k in groups['-느냐']]
for klass in groups['-느냐는']:
    new_rule = []
    for r in klass['rules']:
        new_rule.append([r[0] + '는'] + r[1:])
    klass['rules'] = new_rule

####
# 연결: -느냐니 (-느냐고 하니)

groups['-느냐니'] = [k.copy() for k in groups['-느냐']]
for klass in groups['-느냐니']:
    new_rule = []
    for r in klass['rules']:
        new_rule.append([r[0] + '니'] + r[1:])
    klass['rules'] = new_rule

####
# 연결: -느냐니까 (-느냐고 하니)

groups['-느냐니까'] = [k.copy() for k in groups['-느냐']]
for klass in groups['-느냐니까']:
    new_rule = []
    for r in klass['rules']:
        new_rule.append([r[0] + '니까'] + r[1:])
    klass['rules'] = new_rule

####
# 연결: -느냐며 (-느냐고 하며)

groups['-느냐며'] = [k.copy() for k in groups['-느냐']]
for klass in groups['-느냐며']:
    new_rule = []
    for r in klass['rules']:
        new_rule.append([r[0] + '며'] + r[1:])
    klass['rules'] = new_rule

####
# 연결: -느냐면 (-느냐고 하면)

groups['-느냐면'] = [k.copy() for k in groups['-느냐']]
for klass in groups['-느냐면']:
    new_rule = []
    for r in klass['rules']:
        new_rule.append([r[0] + '면'] + r[1:])
    klass['rules'] = new_rule

####
# 연결: -느냐면서 (-느냐고 하면서)

groups['-느냐면서'] = [k.copy() for k in groups['-느냐']]
for klass in groups['-느냐면서']:
    new_rule = []
    for r in klass['rules']:
        new_rule.append([r[0] + '면서'] + r[1:])
    klass['rules'] = new_rule

####
# 연결: -느니

####
# 종결: -느니

groups['-느니'] = [
    {'rules': [['-느니', COND_NOT_RIEUL, ''],
               ['-느니', T_RIEUL, T_RIEUL]],
     'after': ['#동사', '^.*있다$', '^.*없다$', '^.*계시다$', '-으시-', '-었-', '-겠-'],
     },
]
attach_emphasis(groups['-느니'], ['만'])

####
# 연결: -되

groups['-되'] = [
    {'rules': [['-되', '', '']],
     'after': ['#용언', '#이다', '-으시-'],
     },
]

####
# 종결: -소

groups['-소'] = [
    {'rules': [['-소', COND_NOT_RIEUL, ''],
               ['-소', T_RIEUL, T_RIEUL]],
     'after': ['#용언', '-었-', '-겠-'],
     },
]

####
# 종결: -오

groups['-으오'] = [
    {'rules': [['-오', COND_V_ALL, ''],
               ['-오', T_RIEUL, T_RIEUL],
               ['-으오', COND_T_NOT_RIEUL, '']],
     'after': ['#용언', '#이다', '-으시-'],
     'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#ㅎ불규칙',
                 '#준말용언'],
     },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS('-으오', ['#용언']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS('-우오', ['#용언']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS('-으오', ['#용언']),
    # ㅎ불규칙
    HIEUH_IRREGULAR_TYPICAL_CLASS('-오', ['#용언']),
]

####
# 종결: -잖아 (~지 않아)

groups['-잖아'] = [
    {'rules': [['-잖아', '', '']],
     'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
     },
]
attach_emphasis(groups['-잖아'], ['요'])

####
# 종결: -든지 (혹은 줄임 형태 -든)

groups['-든지'] = [
    {'rules': [['-든지', '', ''],
               ['-든', '', '']],
     'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
     },
]

####
# 종결: -라

groups['-라'] = [
    {'rules': [['-라', '', '']],
     'after': ['#이다', '아니다', '-으시-', '-더-', '-으리-'],
     },
]

####
# 종결: -라니, -으라니

groups['-으라니'] = [
    {'rules': [['-라니', COND_V_OR_RIEUL, ''],
               ['-으라니', COND_T_NOT_RIEUL, '']],
     'after': ['#동사', '#이다', '아니다', '-으시-', '-더-', '-으리-'],
     'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#준말용언'],
     },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS('-으라니', ['#동사']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS('-우라니', ['#동사']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS('-으라니', ['#동사']),
    # 동사이므로 ㅎ불규칙 해당 없음
]
attach_emphasis(groups['-으라니'], ['요'])

####
# 연결: -거든

####
# 종결: -거든

groups['-거든'] = [
    {'rules': [['-거든', '', '']],
     'after': ['#용언', '#이다', '아니다', '-으시-', '-었-', '-겠-'],
     },
]
attach_emphasis(groups['-거든'], ['요'])

####
# 연결: -자면 (-자고 하면)

groups['-자면'] = [
    {'rules': [['-자면', '', '']],
     'after': ['#동사'],
     },
]

####
# 종결: -으리라, -리라

groups['-으리라'] = [
    {'rules': [['-리라', COND_V_OR_RIEUL, ''],
               ['-으리라', COND_T_NOT_RIEUL, '']],
     'after': ['#용언', '-으시', '-었-', '-겠-'],
     'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#ㅎ불규칙',
                 '#준말용언'],
     },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS('-으리라', ['#용언']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS('-우리라', ['#용언']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS('-으리라', ['#용언']),
    # ㅎ불규칙
    HIEUH_IRREGULAR_TYPICAL_CLASS('-리라', ['#용언']),
]

####
# 종결: -으려니, -려니

groups['-으려니'] = [
    {'rules': [['-려니', COND_V_OR_RIEUL, ''],
               ['-으려니', COND_T_NOT_RIEUL, '']],
     'after': ['#용언', '#이다', '-으시-', '-었-'],
     'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#ㅎ불규칙',
                 '#준말용언'],
     },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS('-으려니', ['#용언']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS('-우려니', ['#용언']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS('-으려니', ['#용언']),
    # ㅎ불규칙
    HIEUH_IRREGULAR_TYPICAL_CLASS('-려니', ['#용언']),
]

####
# 종결: -는가

groups['-는가'] = [
    {'rules': [['-는가', COND_NOT_RIEUL, ''],
               ['-는가', T_RIEUL, T_RIEUL]],
     'after': ['#동사', '^.*있다$', '^.*없다$', '^.*계시다$', '-으시-', '-었-', '-겠-'],
     },
]

####
# 종결: -(으)라네

groups['-으라네'] = [
    {'rules': [['-라네', COND_V_ALL, ''],
               ['-라네', T_RIEUL, T_RIEUL],
               ['-으라네', COND_T_NOT_RIEUL, '']],
     'after': ['#동사', '#이다', '아니다', '-으시-', '-더-', '-으리-'],
     'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#준말용언'],
     },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS('-으라네', ['#동사']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS('-우라네', ['#동사']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS('-으라네', ['#동사']),
    # 동사이므로 ㅎ불규칙 해당 없음
]
attach_emphasis(groups['-으라네'], ['요'])

####
# 종결: -(는)다네

groups['-다네'] = [
    {'rules': [['-%s다네' % T_NIEUN, COND_V_ALL, ''],
               ['-%s다네' % T_NIEUN, T_RIEUL, T_RIEUL],
               ['-는다네', COND_T_NOT_RIEUL, '']],
     'after': ['#동사'],
     },
]
attach_emphasis(groups['-다네'], ['요'])

groups['-다네(형용사)'] = [
    {'rules': [['-다네', '', '']],
     'after': ['#형용사'],
     },
]
attach_emphasis(groups['-다네(형용사)'], ['요'])

####
# 연결: -라서

groups['-라서'] = [
    {'rules': [['-라서', '', '']],
     'after': ['#이다', '아니다', '-으시-', '-더-', '-으리-'],
     },
]

####
# 연결: -ㄹ는지, -을는지

groups['-을는지'] = [
    {'rules': [['-%s는지' % T_RIEUL, COND_V_ALL, ''],
               ['-%s는지' % T_RIEUL, T_RIEUL, T_RIEUL],
               ['-을는지', COND_T_NOT_RIEUL, '']],
     'after': ['#용언', '#이다', '-으시-', '-었-'],
     'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#ㅎ불규칙',
                 '#준말용언'],
     },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS('-을는지', ['#용언']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS('-울는지', ['#용언']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS('-을는지', ['#용언']),
    # ㅎ불규칙
    HIEUH_IRREGULAR_TYPICAL_CLASS('-%s는지' % T_RIEUL, ['#용언']),
]
attach_emphasis(groups['-을는지'], ['는', T_NIEUN, '도'])

####
# 종결: -ㄴ다니, -는다니

groups['-는다니'] = [
    {'rules': [['-%s다니' % T_NIEUN, COND_V_ALL, ''],
               ['-%s다니' % T_NIEUN, T_RIEUL, T_RIEUL],
               ['-는다니', COND_T_NOT_RIEUL, '']],
     'after': ['#동사', '-으시-'],
     },
]

####
# 종결: -다니

groups['-다니'] = [
    {'rules': [['-다니', '', '']],
     'after': ['#용언', '-으시-', '-었-', '-겠-'],
     },
]

####
# 연결: -자는 (-자고 하는)

groups['-자는'] = [
    {'rules': [['-자는', '', '']],
     'after': ['#동사'],
     },
]

####
# 연결: -던데

groups['-던데'] = [
    {'rules': [['-던데', '', '']],
     'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
     },
]

####
# 연결: -느라고, -느라

groups['-느라고'] = [
    {'rules': [['-느라고', COND_NOT_RIEUL, ''],
               ['-느라고', T_RIEUL, T_RIEUL],
               ['-느라', COND_NOT_RIEUL, ''],
               ['-느라', T_RIEUL, T_RIEUL]],
     'after': ['#동사', '-으시-'],
     },
]

####
# 종결: -ㄹ래, -을래

groups['-을래'] = [
    {'rules': [['-%s래' % T_RIEUL, COND_V_ALL, ''],
               ['-%s래' % T_RIEUL, T_RIEUL, T_RIEUL],
               ['-을래', COND_T_NOT_RIEUL, '']],
     'after': ['#동사'],
     'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#준말용언'],
     },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS('-을래', ['#동사']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS('-울래', ['#동사']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS('-을래', ['#동사']),
    # 동사이므로 ㅎ불규칙 해당 없음
]
attach_emphasis(groups['-을래'], ['요'])

####
# 종결: -답니다

groups['-답니다'] = [
    {'rules': [['-답니다', '', '']],
     'after': ['#형용사', '-으시-', '-었-', '-겠-'],
     },
]

####
# 종결: -는답니다

groups['-는답니다'] = [
    {'rules': [['-%s답니다' % T_NIEUN, COND_V_ALL, ''],
               ['-%s답니다' % T_NIEUN, T_RIEUL, T_RIEUL],
               ['-는답니다', COND_T_NOT_RIEUL, '']],
     'after': ['#동사', '-으시-'],
     },
]

####
# 종결: -ㄹ세, -을세

groups['-을세'] = [
    {'rules': [['-%s세' % T_RIEUL, COND_V_ALL, ''],
               ['-%s세' % T_RIEUL, T_RIEUL, T_RIEUL],
               ['-을세', COND_T_NOT_RIEUL, '']],
     'after': ['#용언', '#이다', '-으시-', '-었-'],
     'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#ㅎ불규칙',
                 '#준말용언'],
     },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS('-을세', ['#용언']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS('-울세', ['#용언']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS('-을세', ['#용언']),
    # ㅎ불규칙
    HIEUH_IRREGULAR_TYPICAL_CLASS('-%s세' % T_RIEUL, ['#용언']),
]

####
# 연결: -요

groups['-요'] = [
    {'rules': [['-요', '', '']],
     'after': ['#이다', '아니다'],
     },
]

####
# 종결: -ㄹ라, -을라

groups['-을라'] = [
    {'rules': [['-%s라' % T_RIEUL, COND_V_ALL, ''],
               ['-%s라' % T_RIEUL, T_RIEUL, T_RIEUL],
               ['-을라', COND_T_NOT_RIEUL, '']],
     'after': ['#용언', '#이다', '-으시-', '-었-'],
     'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#ㅎ불규칙',
                 '#준말용언'],
     },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS('-을라', ['#용언']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS('-울라', ['#용언']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS('-을라', ['#용언']),
    # ㅎ불규칙
    HIEUH_IRREGULAR_TYPICAL_CLASS('-%s라' % T_RIEUL, ['#용언']),
]

####
# 연결: -건대

groups['-건대'] = [
    {'rules': [['-건대', '', ''],
               # ~하다 준말
               ['-컨대', COND_VOICED + ENC('하'), '하'],  # 하건대 -> 컨대
               ['-건대', COND_UNVOICED + ENC('하'), '하'],  # 하건대 -> 건대
               ],
     'after': ['#동사'],
     },
]

####
# 종결: -ㄴ대, -는대

groups['-는대'] = [
    {'rules': [['-%s대' % T_NIEUN, COND_V_ALL, ''],
               ['-%s대' % T_NIEUN, T_RIEUL, T_RIEUL],
               ['-는대', COND_T_NOT_RIEUL, '']],
     'after': ['#동사', '-으시-'],
     },
]

####
# 종결: -데

groups['-데'] = [
    {'rules': [['-데', COND_V_ALL, '']],
     'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
     },
]

####
# 종결: -마, -으마

groups['-으마'] = [
    {'rules': [['-마', COND_V_ALL, ''],
               ['-마', T_RIEUL, T_RIEUL],
               ['-으마', COND_T_NOT_RIEUL, '']],
     'after': ['#동사'],
     'notcond': ['#준말용언'],
     },
]

####
# 연결: -던지

groups['-던지'] = [
    {'rules': [['-던지', COND_V_ALL, '']],
     'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
     },
]

####
# 종결: -더구나


groups['-더구나'] = [
    {'rules': [['-더구나', '', '']],
     'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
     },
]

####
# 종결: -라면서,-으라면서


groups['-라면서'] = [
    {'rules': [['-라면서', COND_V_ALL, ''],
               ['-라면서', T_RIEUL, T_RIEUL],
               ['-으라면서', COND_T_NOT_RIEUL, ''],
               # 준말
               ['-라며', COND_V_ALL, ''],
               ['-라며', T_RIEUL, T_RIEUL],
               ['-으라며', COND_T_NOT_RIEUL, '']],
     'after': ['#이다', '아니다', '#동사', '-으시-', '-었-', '-더-', '-으리-'],
     'notcond': ['#준말용언'],
     },
]

####
# 종결: -던가


groups['-던가'] = [
    {'rules': [['-던가', '', '']],
     'after': ['#용언'],
     },
]

####
# 연결: -다느니


groups['-다느니'] = [
    {'rules': [['-다느니', '', '']],
     'after': ['#형용사', '-으시-', '-었-', '-겠-'],
     },
]

####
# 연결: -는다느니,-ㄴ다느니


groups['-는다느니'] = [
    {'rules': [['-%s다느니' % T_NIEUN, COND_V_ALL, ''],
               ['-%s다느니' % T_NIEUN, T_RIEUL, T_RIEUL],
               ['-는다느니', COND_T_NOT_RIEUL, '']],
     'after': ['#동사', '-으시-'],
     },
]

####
# 연결: -다가는


groups['-다가는'] = [
    {'rules': [['-다가는', '', '']],
     'after': ['#이다', '#용언', '-으시-', '-었-', '-겠-'],
     },
]

####
# 연결: -다기보다는 (-다고 하기보다는)


groups['-다기보다는'] = [
    {'rules': [['-다기보다는', '', '']],
     'after': ['#이다', '#용언', '-으시-', '-었-', '-겠-'],
     },
]

####
# 연결: -ㄴ들, -은들

groups['-은들'] = [
    {'rules': [['-%s들' % T_NIEUN, COND_V_ALL, ''],
               ['-%s들' % T_NIEUN, T_RIEUL, T_RIEUL],
               ['-은들', COND_T_NOT_RIEUL, '']],
     'after': ['#이다', '#용언', '-으시-'],
     'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#ㅎ불규칙',
                 '#준말용언'],
     },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS('-은들', ['#형용사']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS('-운들', ['#형용사']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS('-은들', ['#형용사']),
    # ㅎ불규칙
    HIEUH_IRREGULAR_TYPICAL_CLASS('-%s들' % T_NIEUN, ['#형용사']),
]

####
# 종결: -(으)리

groups['-으리'] = [
    {'rules': [['-리', COND_V_OR_RIEUL, ''],
               ['-으리', COND_T_NOT_RIEUL, '']],
     'after': ['#용언'],
     'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#ㅎ불규칙',
                 '#준말용언'],
     },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS('-으리', ['#용언']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS('-우리', ['#용언']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS('-으리', ['#용언']),
    # ㅎ불규칙
    HIEUH_IRREGULAR_TYPICAL_CLASS('-리', ['#용언']),
]

####
# 종결: -냐

groups['-냐'] = [
    {'rules': [['-냐', '', '']],
     'after': ['#이다', '#용언', '-으시-', '-었-', '-겠-'],
     },
]
