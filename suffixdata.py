# -*- coding: utf-8 -*-
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
# Portions created by the Initial Developer are Copyright (C) 2008, 2009
# the Initial Developer. All Rights Reserved.
#
# Contributor(s): Changwoo Ryu <cwryu@debian.org>
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

######################################################################
#### 유틸리티

# 자모

from jamo import *

def L_NOT(jamos):
    return ''.join([c for c in L_ALL if not c in jamos])
def V_NOT(jamos):
    return ''.join([c for c in V_ALL if not c in jamos])
def T_NOT(jamos):
    return ''.join([c for c in T_ALL if not c in jamos])

V_A_O = V_A + V_O
V_NOT_A_O = V_NOT(V_A + V_O)
V_NOT_A_EO_O = V_NOT(V_A + V_EO + V_O)

# 조건

COND_V_ALL = u'[%s]' % V_ALL
COND_T_ALL = u'[%s]' % T_ALL
COND_V_OR_RIEUL = u'[%s%s]' % (V_ALL, T_RIEUL)
COND_T_NOT_RIEUL = u'[%s]' % T_NOT(T_RIEUL)
COND_NOT_RIEUL = u'[^%s]' % T_RIEUL

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
                new_class[key] = [l[:] for l in klass[key]] # copy list-list
            else:
                new_class[key] = klass[key][:] # copy list
        return new_class
    return [copy_class(klass) for klass in group]

# hunspell의 twofold suffix를 통해 확장할 추가 플래그 지정, 해당 파생
# 형태에 또 다른 접미어 규칙이 적용될 수 있는 경우 사용한다. (예:
# 명사형 전성어미 + 조사)
def attach_continuation_flags(group, flags):
    for klass in group:
        for r in klass['rules']:
            r.append(flags)

#### 어/아로 시작하는 어미를 위한 유틸리티

# ㅏ/ㅗ 모음의 음절로 끝나는 경우  (ㅏ로 끝나는 경우, '오'로 끝나는 경우 제외)
COND_EOA_AO = [ '[%s]%s' % (L_NOT(L_IEUNG), V_O), '[%s][%s]' % (V_A_O, T_ALL) ]
# ㅏ/ㅗ 제외한 모음의 음절로 끝나는 경우  (ㅓ로 끝나는 경우 제외)
COND_EOA_NOT_AO = [ '[%s]' % V_NOT_A_EO_O, '[%s][%s]' % (V_NOT_A_O, T_ALL) ]
# ㅓ로 끝나는 경우
COND_EOA_EO = V_EO
# ㅏ로 끝나는 경우 ('하' 제외)
COND_EOA_A = '[%s]%s' % (L_NOT(L_HIEUH), V_A)
# 하로 끝나는 경우
COND_EOA_HA = u'하'
# 외어 -> 왜 ('외다', '뇌다' 예외) - 한글 맞춤법 35항
COND_EOA_OE = '[%s]%s' % (L_NOT(L_NIEUN + L_IEUNG), V_OE)

#### ㄷ불규칙활용 유틸리티

# 종성의 ㄷ이 ㄹ로 바뀜
def TIKEUT_IRREGULAR_TYPICAL_CLASS(suffix, after):
    return { 'rules': [[u'-' + T_RIEUL + suffix[1:], T_TIKEUT, T_TIKEUT]],
             'after': after,
             'cond': ['#ㄷ불규칙'] }

#### ㅂ불규칙활용 유틸리티

# 단순 탈락인 경우
def PIEUP_IRREGULAR_TYPICAL_CLASS(suffix, after):
    return { 'rules': [[suffix, T_PIEUP, T_PIEUP]],
             'after': after,
             'cond': ['#ㅂ불규칙'] }

#### ㅅ불규칙활용 유틸리티

# 단순 탈락인 경우
def SIOS_IRREGULAR_TYPICAL_CLASS(suffix, after):
    return { 'rules': [[suffix, T_SIOS, T_SIOS]],
             'after': after,
             'cond': ['#ㅅ불규칙'] }

#### ㅎ불규칙활용 유틸리티

# 단순 탈락인 경우
def HIEUH_IRREGULAR_TYPICAL_CLASS(suffix, after):
    return { 'rules': [[suffix, T_HIEUH, T_HIEUH]],
             'after': after,
             'cond': ['#ㅎ불규칙'] }



#### 르불규칙활용 유틸리티

# '르다' 앞에 ㅏ/ㅗ 모음의 음절
COND_REU_AO = [ u'[%s]르' % V_A_O, u'[%s][%s]르' % (V_A_O, T_ALL) ]
# '르다' 앞에 ㅏ/ㅗ 모음이 아닌 음절
COND_REU_NOT_AO = [ u'[%s]르' % V_NOT_A_O, u'[%s][%s]르' % (V_NOT_A_O, T_ALL) ]

#### 으불규칙활용 유틸리티

# 참고: 으불규칙 활용을 어/아 어미에 대해 2개의 규칙으로 만드는 이유
# 
# '으' 음절 앞에 오는 음절이 있는 경우 그 음절의 모음이 양성모음이냐
# 음성모음이냐에 따라 어미의 '어/아'가 결정되는데, '끄다', '뜨다',
# '쓰다', '크다'같은 으불규칙용언의 경우 앞의 음절이 없으면서 '어'가
# 붙는다. 그래서 aff 파일의 같은 규칙 안에서 조건으로 정의할 수가
# 없다. (aff 파일에서 쓸 수 있는 제한된 정규식으로는 으 앞에 음절이
# 없다는 걸 정의할 수가 없다.) 그러므로 '끄다', '뜨다', '쓰다',
# '크다'는 항상 별도 규칙으로 만든다.

# 앞에 ㅏ/ㅗ 모음의 음절
COND_EU_AO = [ u'[%s][%s]%s' % (V_A_O, L_ALL, V_EU),
               u'[%s][%s][%s]%s' % (V_A_O, T_ALL, L_ALL, V_EU) ]
# 앞에 ㅏ/ㅗ 모음이 아닌 음절
COND_EU_NOT_AO = [ u'[%s][%s]%s' % (V_NOT_A_O, L_ALL, V_EU),
                   u'[%s][%s][%s]%s' % (V_NOT_A_O, T_ALL, L_ALL, V_EU) ]



######################################################################
#### 어미 데이터

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

#### 높임 선어말

groups['-으시-'] = [
    { 'rules': [[u'-시-', COND_V_ALL, ''],
                [u'-시-', T_RIEUL, T_RIEUL],
                [u'-으시-', COND_T_NOT_RIEUL, '']],
      'after': ['#용언', '#이다'],
      'notafter': ['계시다', '모시다'],
      'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#ㅎ불규칙'],
    },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS(u'-으시-', ['#용언']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS(u'-우시-', ['#용언']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS(u'-으시-', ['#용언']),
    # ㅎ불규칙
    HIEUH_IRREGULAR_TYPICAL_CLASS(u'-시-', ['#용언']),
]

#### 과거 시제 선어말

groups['-었-'] = [
    { 'rules': [[u'-었-', COND_EOA_NOT_AO, ''],
                [u'-았-', COND_EOA_AO, ''],
                [u'-\u1165\u11bb-', COND_EOA_EO, V_EO],
                [u'-\u1161\u11bb-', COND_EOA_A, V_A],
                [u'-였-', u'하', ''],
                # 준말
                [u'-\u116a\u11bb-', V_O, V_O], # 오았 -> 왔
                [u'-\u116f\u11bb-', V_U, V_U], # 우었 -> 웠
                [u'-\u116b\u11bb-', COND_EOA_OE, V_OE], # 외었 -> 왜ㅆ
                [u'-\u116a\u11bb-', u'놓', V_O + T_HIEUH], # 놓아 -> 놔
                [u'-\u1162\u11bb-', u'하', V_A], # 하였 -> 했
                [u'-\u1167\u11bb-', V_I, V_I], # 이었 -> 였
                [u'-\u11bb-', V_AE, ''], # 애었 -> 앴
                [u'-\u11bb-', V_E, ''], # 에었 -> 엤
                ],
      'after': ['#용언', '#이다', '-으시-'],
      'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#ㅎ불규칙',
                  '#러불규칙', '#르불규칙', '#우불규칙', '#으불규칙'],
    },
    # ㄷ불규칙
    { 'rules': [[u'-\u11af었-', '[%s]%s' % (V_NOT_A_O, T_TIKEUT), T_TIKEUT],
                [u'-\u11af았-', '[%s]%s' % (V_A_O, T_TIKEUT), T_TIKEUT]],
      'after': ['#용언'],
      'cond': ['#ㄷ불규칙'],
    },
    # ㅂ불규칙
    { 'rules': [[u'-웠-', T_PIEUP, T_PIEUP]],
      'after': ['#용언'],
      'notafter': ['곱다', '곱디곱다', '돕다'],
      'cond': ['#ㅂ불규칙'],
    },
    # ㅂ불규칙 중 예외적으로 '-와'가 붙는 경우
    { 'rules': [[u'-왔-', T_PIEUP, T_PIEUP]],
      'after': ['곱다', '곱디곱다', '돕다'],
      'cond': ['#ㅂ불규칙'],
    },
    # ㅅ불규칙
    { 'rules': [[u'-었-', u'[%s]%s' % (V_NOT_A_O, T_SIOS), T_SIOS],
                [u'-았-', u'[%s]%s' % (V_A_O, T_SIOS), T_SIOS]],
      'after': ['#용언'],
      'cond': ['#ㅅ불규칙'],
    },
    # ㅎ불규칙
    { 'rules': [[u'-\u1162\u11bb-', V_A + T_HIEUH, V_A + T_HIEUH],   # 파랗다
                [u'-\u1164\u11bb-', V_YA + T_HIEUH, V_YA + T_HIEUH], # 하얗다
                [u'-\u1166\u11bb-', V_EO + T_HIEUH, V_EO + T_HIEUH], # 누렇다
                [u'-\u1168\u11bb-', V_YEO + T_HIEUH, V_YEO + T_HIEUH], # 허옇다
               ],
      'after': ['#용언'],
      'notafter': ['그렇다', '고렇다', '이렇다', '요렇다', '저렇다', '조렇다',
                   '어떻다', '아무렇다'],
      'cond': ['#ㅎ불규칙'],
    },
    # ㅎ불규칙 지시형용사
    { 'rules': [[u'-\u1162\u11bb-', V_EO + T_HIEUH, V_EO + T_HIEUH]],
      'after': ['그렇다', '고렇다', '이렇다', '요렇다', '저렇다', '조렇다',
                '어떻다', '아무렇다'],
      'cond': ['#ㅎ불규칙'],
    },
    # 러불규칙
    { 'rules': [[u'-렀-', '르', '']],
      'after': ['#용언'],
      'cond': ['#러불규칙'],
    },
    # 르불규칙
    { 'rules': [[u'-\u11af렀-', COND_REU_NOT_AO, u'르'],
                [u'-\u11af랐-', COND_REU_AO, u'르']],
      'after': ['#용언'],
      'cond': ['#르불규칙'],
    },
    # 우불규칙
    { 'rules': [[u'-\u1165\u11bb-', V_U, V_U]],
      'after': ['#용언'],
      'cond': ['#우불규칙'],
    },
    # 으불규칙
    { 'rules': [[u'-\u1161\u11bb-', COND_EU_AO, V_EU],
                [u'-\u1165\u11bb-', COND_EU_NOT_AO, V_EU]],
      'after': ['#용언'],
      'notafter': ['^.*끄다$', '^.*뜨다$', '^.*쓰다$', '^.*크다$'],
      'cond': ['#으불규칙'],
    },
    # 으불규칙 예외 '끄다', '뜨다', '쓰다', '크다'
    { 'rules': [[u'-\u1165\u11bb-', V_EU, V_EU]],
      'after': ['^.*끄다$', '^.*뜨다$', '^.*쓰다$', '^.*크다$'],
      'cond': ['#으불규칙'],
    },
]
# 대과거 시제 덧붙이기
for klass in groups['-었-']:
    new_rules = []
    for r in klass['rules']:
        new_rules.append([r[0][:-1] + u'었-'] + r[1:])
    klass['rules'] += new_rules

#### 미래 시제 선어말

groups['-겠-'] = [
    { 'rules': [[u'-겠-', '', '']],
      # '-어야-'는 '-어야겠-' 형태를 위해서 허용
      'after': ['#용언', '#이다', '-으시-', '-었-', '-어야-'],
    },
]

#### 시제 선어말: -더-

groups['-더-'] = [
    { 'rules': [[u'-더-', '', '']],
      'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
    },
]

#### 연결: -어, -아
groups['-어'] = [
    { 'rules': [[u'-어', COND_EOA_NOT_AO, ''],
                [u'-아', COND_EOA_AO, ''],
                [u'-\u1165', COND_EOA_EO, V_EO],
                [u'-\u1161', COND_EOA_A, V_A],
                [u'-여', u'하', ''],
                [u'-\u116a', V_O, V_O], # 오아 -> 와
                [u'-\u116f', V_U, V_U], # 우어 -> 워
                [u'-\u116b', COND_EOA_OE, V_OE], # 외어 -> 왜
                [u'-\u116a', u'놓', V_O + T_HIEUH], # 놓아 -> 놔
                [u'-\u1162', u'하', V_A], # 하여 -> 해
                [u'-\u1167', V_I, V_I], # 이어 -> 여
                [u'-\u1162', V_AE, V_AE], # 애어 -> 애
                [u'-\u1166', V_E, V_E], # 에어 -> 에
                ],
      'after': ['#용언', '-었-', '-겠-', '-으시-'],
      'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#ㅎ불규칙',
                  '#러불규칙', '#르불규칙', '#우불규칙', '#으불규칙'],
    },
    # ㄷ불규칙
    { 'rules': [[u'-\u11af어', '[%s]%s' % (V_NOT_A_O, T_TIKEUT), T_TIKEUT],
                [u'-\u11af아', '[%s]%s' % (V_A_O, T_TIKEUT), T_TIKEUT]],
      'after': ['#용언'],
      'cond': ['#ㄷ불규칙'],
    },
    # ㅂ불규칙
    { 'rules': [[u'-워', T_PIEUP, T_PIEUP]],
      'after': ['#용언'],
      'notafter': ['곱다', '곱디곱다', '돕다'],
      'cond': ['#ㅂ불규칙'],
    },
    # ㅂ불규칙 중 예외적으로 '-와'가 붙는 경우
    { 'rules': [[u'-와', T_PIEUP, T_PIEUP]],
      'after': ['곱다', '곱디곱다', '돕다'],
      'cond': ['#ㅂ불규칙'],
    },
    # ㅅ불규칙
    { 'rules': [[u'-어', '[%s]%s' % (V_NOT_A_O, T_SIOS), T_SIOS],
                [u'-아', '[%s]%s' % (V_A_O, T_SIOS), T_SIOS]],
      'after': ['#용언'],
      'cond': ['#ㅅ불규칙'],
    },
    # ㅎ불규칙
    { 'rules': [[u'-\u1162', V_A + T_HIEUH, V_A + T_HIEUH],   # 파랗다
                [u'-\u1164', V_YA + T_HIEUH, V_YA + T_HIEUH], # 하얗다
                [u'-\u1166', V_EO + T_HIEUH, V_EO + T_HIEUH], # 누렇다
                [u'-\u1168', V_YEO + T_HIEUH, V_YEO + T_HIEUH], # 허옇다
               ],
      'after': ['#용언'],
      'notafter': ['그렇다', '고렇다', '이렇다', '요렇다', '저렇다', '조렇다',
                   '어떻다', '아무렇다'],
      'cond': ['#ㅎ불규칙'],
    },
    # ㅎ불규칙 지시형용사
    { 'rules': [[u'-\u1162', V_EO + T_HIEUH, V_EO + T_HIEUH]],
      'after': ['그렇다', '고렇다', '이렇다', '요렇다', '저렇다', '조렇다',
                '어떻다', '아무렇다'],
      'cond': ['#ㅎ불규칙'],
    },
    # 러불규칙
    { 'rules': [[u'-러', '르', '']],
      'after': ['#용언'],
      'cond': ['#러불규칙'],
    },
    # 르불규칙
    { 'rules': [[u'-\u11af러', COND_REU_NOT_AO, u'르'],
                [u'-\u11af라', COND_REU_AO, u'르']],
      'after': ['#용언'],
      'cond': ['#르불규칙'],
    },
    # 우불규칙
    { 'rules': [[u'-\u1165', V_U, V_U]],
      'after': ['#용언'],
      'cond': ['#우불규칙'],
    },
    # 으불규칙
    { 'rules': [[u'-\u1161', COND_EU_AO, V_EU],
                [u'-\u1165', COND_EU_NOT_AO, V_EU]],
      'after': ['#용언'],
      'notafter': ['^.*끄다$', '^.*뜨다$', '^.*쓰다$', '^.*크다$'],
      'cond': ['#으불규칙'],
    },
    # 으불규칙 예외 '끄다', '뜨다', '크다', '쓰다'
    { 'rules': [[u'-\u1165', V_EU, V_EU]],
      'after': ['^.*끄다$', '^.*뜨다$', '^.*쓰다$', '^.*크다$'],
      'cond': ['#으불규칙'],
    },
]

#### 연결: -어다, -아다 (동사)
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

#### 종결: -어라, -아라
groups['-어라'] = copy_group(groups['-어'])
for klass in groups['-어라']:
    for r in klass['rules']:
        r[0] = r[0] + '라'

#### 종결: -거라, -너라
# 학교 문법 및 2008년 개정 표준국어대사전에 따르면 "-거라"를
# "-어라/아라"의 불규칙 형태가 아닌 별도의 어미로 본다. 
#
# "-거라"를 허용하는 범위는 논란의 여지가 있다. 표준국어대사전에서는
# "-가다" 형태의 동사만 허용 학교 문법에서는 "-자다" 등 일부 동사에서도
# 허용, 실생활에서는 거의 모든 동사와 결합하곤 한다.
groups['-거라'] = [
    { 'rules': [[u'-거라', '', '']],
      'after': ['#동사'],
      'cond': ['^.*가다$'],
    },
    { 'rules': [[u'-너라', '', '']],
      'after': ['#동사'],
      'cond': ['^.*오다$'],
    },
]

#### 연결: -어도, -아도
# '-어' 재활용
groups['-어도'] = copy_group(groups['-어'])
for klass in groups['-어도']:
    for r in klass['rules']:
        r[0] = r[0] + '도'
groups['-어도'][0]['after'].append('#이다')

#### 연결: -어서, -아서
# '-어' 재활용
groups['-어서'] = copy_group(groups['-어'])
for klass in groups['-어서']:
    for r in klass['rules']:
        r[0] = r[0] + '서'
groups['-어서'][0]['after'].append('#이다')
attach_emphasis(groups['-어서'], ['는', '도'])

#### 연결: -어야, -아야
# '-어' 재활용
groups['-어야'] = copy_group(groups['-어'])
for klass in groups['-어야']:
    for r in klass['rules']:
        r[0] = r[0] + '야'
groups['-어야'][0]['after'].append('#이다')

#### -어야-
# NOTE: 문법상 선어말 어미는 아니지만 '어야겠' ('어야하겠'의 준말)
# 형태를 만드는 용도.
# '-어야' 재활용
groups['-어야-'] = copy_group(groups['-어야'])
for klass in groups['-어야-']:
    for r in klass['rules']:
        r[0] = r[0] + '-'
# '셨어야겠다' 따위로 확장되지 않도록 앞에 시제 선어말 어미 금지
groups['-어야-'][0]['after'] = ['#용언', '#이다', '-으시-']

#### 연결, 종결: -어야지, -아야지
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
        if r[0].endswith(u'지요'):
            expanded.append([r[0][:-len(u'지요')] + u'죠'] + r[1:])
    klass['rules'] += expanded

#### 종결: -어요, -아요
# '-어' 재활용
groups['-어요'] = copy_group(groups['-어'])
for klass in groups['-어요']:
    for r in klass['rules']:
        r[0] = r[0] + '요'
groups['-어요'][0]['after'].append('#이다')
groups['-어요'] += [
    # 이다/아니다의 경우 -에요 가능, 줄임 이예요 => 예요
    { 'rules': [[u'-에요', V_I, ''],
                [u'-%s요' % V_YE, V_I, V_I]],
      'after': ['#이다', '^.*아니다$'],
    }
]

#### 관형사형 전성: -ㄹ, -을
groups['-을'] = [
    { 'rules': [[u'-\u11af', COND_V_ALL, ''],
                [u'-\u11af', T_RIEUL, T_RIEUL],
                [u'-을', COND_T_NOT_RIEUL, '']],
      'after': ['#용언', '#이다', '-으시-', '-시오-', '-었-'],
      'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#ㅎ불규칙'],
    },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS(u'-을', ['#용언']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS(u'-울', ['#용언']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS(u'-을', ['#용언']),
    # ㅎ불규칙
    HIEUH_IRREGULAR_TYPICAL_CLASS(u'-\u11af', ['#용언']),
]

#### 종결: -ㄹ걸, -을걸
# '-을' 재활용
groups['-을걸'] = copy_group(groups['-을'])
for klass in groups['-을걸']:
    for r in klass['rules']:
        r[0] = r[0] + '걸'

#### 종결: -ㄹ게, -을게
# 동사 전용
groups['-을게'] = [
    { 'rules': [[u'-\u11af게', COND_V_ALL, ''],
                [u'-\u11af게', T_RIEUL, T_RIEUL],
                [u'-을게', COND_T_NOT_RIEUL, '']],
      'after': ['#동사'],
      'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙'],
    },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS(u'-을게', ['#동사']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS(u'-울게', ['#동사']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS(u'-을게', ['#동사']),
    # 동사이므로 ㅎ불규칙 해당 없음
]
attach_emphasis(groups['-을게'], ['요'])

#### 연결: -ㄹ까, -을까
# '-을' 재활용
groups['-을까'] = copy_group(groups['-을'])
for klass in groups['-을까']:
    for r in klass['rules']:
        r[0] = r[0] + '까'
# ~ㄹ까요, -을까요 보조사
attach_emphasis(groups['-을까'], ['요'])

#### 연결: -ㄹ망정, -을망정
# '-을' 재활용
groups['-을망정'] = copy_group(groups['-을'])
for klass in groups['-을망정']:
    for r in klass['rules']:
        r[0] = r[0] + '망정'

#### 연결: -ㄹ수록, -을수록
# '-을' 재활용
groups['-을수록'] = copy_group(groups['-을'])
for klass in groups['-을수록']:
    for r in klass['rules']:
        r[0] = r[0] + '수록'

#### 연결: -ㄹ지, -을지
# '-을' 재활용
groups['-을지'] = copy_group(groups['-을'])
for klass in groups['-을지']:
    for r in klass['rules']:
        r[0] = r[0] + '지'
attach_emphasis(groups['-을지'], ['는', '도'])

#### 연결: -ㄹ지라도, -을지라도
# '-을' 재활용
groups['-을지라도'] = copy_group(groups['-을'])
for klass in groups['-을지라도']:
    for r in klass['rules']:
        r[0] = r[0] + '지라도'

#### 연결: -ㄹ지언정, -을지언정
# '-을' 재활용
groups['-을지언정'] = copy_group(groups['-을'])
for klass in groups['-을지언정']:
    for r in klass['rules']:
        r[0] = r[0] + '지언정'

#### 종결: -다

groups['-다'] = [
    { 'rules': [[u'-다', '', '']],
      'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
    },
]

#### 관형사형 전성: -는
groups['-는'] = [
    { 'rules': [[u'-는', u'[^%s]' % T_RIEUL, ''],
                [u'-는', T_RIEUL, T_RIEUL]],
      'after': ['#동사', '^.*있다$', '^.*없다$', '^.*계시다$', '-으시-', '-겠-'],
    },
]

#### 연결: -게
groups['-게'] = [
    { 'rules': [[u'-게', '', ''],
                [u'-케', u'하', u'하'], # 하게 -> 케 준말
                ],
      'after': ['#용언', '-으시-'],
    },
]
attach_emphasis(groups['-게'], ['도'])

#### 연결: -다가
groups['-다가'] = [
    { 'rules': [[u'-다가', '', '']],
      'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
    },
]

#### 관형사형 전성: -ㄴ, -은
groups['-은'] = [
    { 'rules': [[u'-\u11ab', COND_V_ALL, ''],
                [u'-\u11ab', T_RIEUL, T_RIEUL],
                [u'-은', COND_T_NOT_RIEUL, '']],
      'after': ['#용언', '#이다', '-으시-'],
      'notafter': ['^.*있다$', '^.*없다$'],
      'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#ㅎ불규칙'],
    },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS(u'-은', ['#용언']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS(u'-운', ['#용언']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS(u'-은', ['#용언']),
    # ㅎ불규칙
    HIEUH_IRREGULAR_TYPICAL_CLASS(u'-\u11ab', ['#용언']),
]

#### 연결: -지
#### 종결: -지
groups['-지'] = [
    { 'rules': [[u'-지', '', ''],
                [u'-치', u'하', u'하'], # 하지 -> 치 준말
               ],
      'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
    },
]
attach_emphasis(groups['-지'], ['요', '도', '는'])
# 지요 -> 죠 준말
groups['-지'][0]['rules'].append([u'-죠', '', ''])


#### 연결: -지마는
groups['-지마는'] = [
    { 'rules': [[u'-지마는', '', ''],
                [u'-지만', '', ''],
                [u'-치만', u'하', u'하'],   # 하지만 -> 치만 준말
                [u'-치마는', u'하', u'하'], # 하지마는 -> 치마는 준말
                ],
      'after': ['#용언', '#이다', '-었-', '-겠-'],
    },
]

#### 연결: -며, -으며
groups['-으며'] = [
    { 'rules': [[u'-며', COND_V_OR_RIEUL, ''],
                [u'-으며', COND_T_NOT_RIEUL, '']],
      'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
      'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#ㅎ불규칙'],
    },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS(u'-으며', ['#용언']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS(u'-우며', ['#용언']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS(u'-으며', ['#용언']),
    # ㅎ불규칙
    HIEUH_IRREGULAR_TYPICAL_CLASS(u'-며', ['#용언']),
]

#### 종결: -ㅂ니다, -습니다
groups['-습니다'] = [
    { 'rules': [[u'-\u11b8니다', COND_V_ALL, ''],
                [u'-\u11b8니다', T_RIEUL, T_RIEUL],
                [u'-습니다', COND_T_NOT_RIEUL, '']],
      'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
    },
]

#### 종결: -ㅂ니까, -습니까
groups['-습니까'] = [
    { 'rules': [[u'-\u11b8니까', COND_V_ALL, ''],
                [u'-\u11b8니까', T_RIEUL, T_RIEUL],
                [u'-습니까', COND_T_NOT_RIEUL, '']],
      'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
    },
]

#### 연결: -고
#### 종결: -고
groups['-고'] = [
    { 'rules': [[u'-고', '', '']],
      'after': ['#용언', '#이다', '-'],
      'notafter': ['-으리-', '-더-'],
    },
]
attach_emphasis(groups['-고'], ['요'])

#### 연결: -고는
groups['-고는'] = [
    { 'rules': [[u'-고는', '', ''],
                [u'-곤', '', '']],
      'after': ['#동사', '-으시-'],
    },
]

#### 연결: -고도
groups['-고도'] = [
    { 'rules': [[u'-고도', '', '']],
      'after': ['#용언', '#이다', '-으시-'],
    },
]

#### 연결: -고자
groups['-고자'] = [
    { 'rules': [[u'-고자', '', '']],
      'after': ['#동사', '^.*있다$', '^.*없다$', '^.*계시다$', '-으시-'],
    },
]

#### 종결: -세요, -으세요 (-시어요, -으시어요 축약)
groups['-으세요'] = [
    { 'rules': [[u'-세요', COND_V_ALL, ''],
                [u'-세요', T_RIEUL, T_RIEUL],
                [u'-으세요', COND_T_NOT_RIEUL, '']],
      'after': ['#용언', '#이다'],
      'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#ㅎ불규칙'],
    },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS(u'-으세요', ['#용언']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS(u'-우세요', ['#용언']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS(u'-으세요', ['#용언']),
    # ㅎ불규칙
    HIEUH_IRREGULAR_TYPICAL_CLASS(u'-세요', ['#용언']),
]

#### 연결: -거나
groups['-거나'] = [
    { 'rules': [[u'-거나', '', '']],
      'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-', '-으옵-'],
    },
]

#### 연결: -려, -으려
groups['-으려'] = [
    { 'rules': [[u'-려', COND_V_OR_RIEUL, ''],
                [u'-으려', COND_T_NOT_RIEUL, '']],
      'after': ['#동사', '-으시-'],
      'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙'],
    },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS(u'-으려', ['#동사']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS(u'-우려', ['#동사']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS(u'-으려', ['#동사']),
    # 동사이므로 ㅎ불규칙 해당 없음
]

#### 연결: -려고, -으려고
# '-으려' 재활용
groups['-으려고'] = copy_group(groups['-으려'])
for klass in groups['-으려고']:
    for r in klass['rules']:
        r[0] = r[0] + '고'

#### 연결: -려다, -으려다 (려고 하다)
# '-으려' 재활용
groups['-으려다'] = copy_group(groups['-으려'])
for klass in groups['-으려다']:
    for r in klass['rules']:
        r[0] = r[0] + '다'

#### 연결: -려는, -으려는 (려고 하는)
# '-으려' 재활용
groups['-으려는'] = copy_group(groups['-으려'])
for klass in groups['-으려는']:
    for r in klass['rules']:
        r[0] = r[0] + '는'

#### 연결: -려면, -으려면
# '-으려' 재활용
groups['-으려면'] = copy_group(groups['-으려'])
for klass in groups['-으려면']:
    for r in klass['rules']:
        r[0] = r[0] + '면'

#### 연결: -도록
groups['-도록'] = [
    { 'rules': [[u'-도록', '', ''],
                [u'-토록', u'하', u'하'], # 하도록 -> 토록 준말
                ],
      'after': ['#동사', '-으시-',
                '#형용사', # FIXME: 일부 형용사만 허용하지만 구분하기에는 너무 많다.
               ],
    },
]

#### 연결: -는데
groups['-는데'] = [
    { 'rules': [[u'-는데', COND_NOT_RIEUL, ''],
                [u'-는데', T_RIEUL, T_RIEUL]],
      'after': ['#동사', '^.*있다$', '^.*없다$', '^.*계시다$', '-으시-', '-었-', '-겠-'], 
    },
]
attach_emphasis(groups['-는데'], ['도', '요'])

#### 연결: -나, -으나
groups['-으나'] = [
    { 'rules': [[u'-나', COND_V_ALL, ''],
                [u'-나', T_RIEUL, T_RIEUL],
                [u'-으나', COND_T_NOT_RIEUL, '']],
      'after': ['#용언', '#이다', '-으시-', '-사오-', '-었-', '-겠-'],
      'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#ㅎ불규칙'],
    },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS(u'-으나', ['#용언']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS(u'-우나', ['#용언']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS(u'-으나', ['#용언']),
    # ㅎ불규칙
    HIEUH_IRREGULAR_TYPICAL_CLASS(u'-나', ['#용언']),
]

#### 종결: -나 (동사, 물음)
groups['-나'] = [
    { 'rules': [[u'-나', COND_NOT_RIEUL, ''],
                [u'-나', T_RIEUL, T_RIEUL]],
      'after': ['#용언', '-으시-', '-었-', '-겠-'],
    },
]
attach_emphasis(groups['-나'], ['요'])

#### 연결: -다시피
groups['-다시피'] = [
    { 'rules': [[u'-다시피', '', '']],
      'after': ['#동사', '-으시-', '-었-', '-겠-'],
    },
]

#### 종결: -ㅂ시다, -읍시다
groups['-읍시다'] = [
    { 'rules': [[u'-\u11b8시다', COND_V_ALL, ''],
                [u'-\u11b8시다', T_RIEUL, T_RIEUL],
                [u'-읍시다', COND_T_NOT_RIEUL, '']],
      'after': ['#동사', '-으시-'],
      'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙'],
    },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS(u'-읍시다', ['#동사']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS(u'-웁시다', ['#동사']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS(u'-읍시다', ['#동사']),
    # 동사이므로 ㅎ불규칙 해당 없음
]

#### 연결: -자
groups['-자'] = [
    { 'rules': [[u'-자', '', '']],
      'after': ['#동사'], # TODO: 일부 형용사
    },
]

#### 연결: -기에
groups['-기에'] = [
    { 'rules': [[u'-기에', '', '']],
      'after': ['#용언', '#이다', '-으시-', '-었-'], # TODO: 일부 형용사
    },
]

#### 연결: -듯
groups['-듯'] = [
    { 'rules': [[u'-듯', '', ''],
                [u'-듯이', '', '']],
      'after': ['#용언', '#이다'],
    },
]

#### 연결: -다면
groups['-다면'] = [
    { 'rules': [[u'-다면', '', '']],
      'after': ['#형용사', '-으시-', '-었-', '-겠-'],
    },
]

#### 연결: -다면서
groups['-다면서'] = [
    { 'rules': [[u'-다면서', '', ''],
                [u'-다며', '', '']],
      'after': ['#형용사', '-으시-', '-었-', '-겠-'],
    },
]
attach_emphasis(groups['-다면서'], ['요'])

#### 종결: -자고
groups['-자고'] = [
    { 'rules': [[u'-자고', '', '']],
      'after': ['#동사'],
    },
]
attach_emphasis(groups['-자고'], ['요'])

#### 연결: -기로
groups['-기로'] = [
    { 'rules': [[u'-기로', '', ''],
                [u'-키로', u'하', u'하'], # 하기로 -> 키로 준말
                ],
      'after': ['#용언', '#이다', '-'],
      'notafter': ['-더-', '-으리-'],
    },
]

#### 종결: -라, -으라
groups['-으라'] = [
    { 'rules': [[u'-라', COND_V_OR_RIEUL, ''],
                [u'-으라', COND_T_NOT_RIEUL, '']],
      'after': ['#동사', '-으시-'],
      'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙'],
    },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS(u'-으라', ['#동사']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS(u'-우라', ['#동사']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS(u'-으라', ['#동사']),
    # 동사이므로 ㅎ불규칙 해당 없음
]

#### 연결: -라고, -으라고
groups['-으라고'] = [
    { 'rules': [[u'-라고', COND_V_OR_RIEUL, ''],
                [u'-으라고', COND_T_NOT_RIEUL, '']],
      'after': ['#동사', '#이다', '아니다', '-으시-', '-더-', '-으리-'],
      'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙'],
    },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS(u'-으라고', ['#동사']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS(u'-우라고', ['#동사']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS(u'-으라고', ['#동사']),
    # 동사이므로 ㅎ불규칙 해당 없음
]
attach_emphasis(groups['-으라고'], ['요'])

#### 연결: -라는, -으라는 (라고 하는)
groups['-으라는'] = [
    { 'rules': [[u'-라는', COND_V_OR_RIEUL, ''],
                [u'-으라는', COND_T_NOT_RIEUL, '']],
      'after': ['#동사', '#이다', '아니다', '-으시-', '-더-', '-으리-'],
      'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙'],
    },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS(u'-으라는', ['#동사']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS(u'-우라는', ['#동사']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS(u'-으라는', ['#동사']),
    # 동사이므로 ㅎ불규칙 해당 없음
]

#### 연결 -ㄴ데, -은데
groups['-은데'] = [
    { 'rules': [[u'-\u11ab데', COND_V_OR_RIEUL, ''],
                [u'-\u11ab데', T_RIEUL, T_RIEUL],
                [u'-은데', COND_T_NOT_RIEUL, '']],
      'after': ['#형용사', '#이다', '-으시-', '-사오-'],
      'notafter': ['^.*있다$', '^.*없다$'],
      'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#ㅎ불규칙'],
    },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS(u'-은데', ['#형용사']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS(u'-운데', ['#형용사']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS(u'-은데', ['#형용사']),
    # ㅎ불규칙
    HIEUH_IRREGULAR_TYPICAL_CLASS(u'-%s데' % T_NIEUN, ['#형용사']),
]
attach_emphasis(groups['-은데'], ['도', '요'])

#### 명사형 전성: -기
groups['-기'] = [
    { 'rules': [[u'-기', '', ''],
                [u'-키', u'하', u'하'], # 하기 -> 키 준말
               ],
      'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
    },
]
# 조사
attach_continuation_flags(groups['-기'], [flags.josa_flag])

#### 명사형 전성: -음
groups['-음'] = [
    { 'rules': [[u'-\u11b7', COND_V_ALL, ''],
                [u'-\u11b1', T_RIEUL, T_RIEUL],
                [u'-음', COND_T_NOT_RIEUL, '']],
      'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
      'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#ㅎ불규칙'],
    },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS(u'-음', ['#용언']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS(u'-움', ['#용언']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS(u'-음', ['#용언']),
    # ㅎ불규칙
    HIEUH_IRREGULAR_TYPICAL_CLASS(u'-\u11b7', ['#용언']),
]
# 조사
attach_continuation_flags(groups['-음'], [flags.josa_flag])

#### 종결: -ㄴ다, -는다
groups['-는다'] = [
    { 'rules': [[u'-\u11ab다', COND_V_OR_RIEUL, ''],
                [u'-\u11ab다', T_RIEUL, T_RIEUL],
                [u'-는다', COND_T_NOT_RIEUL, '']],
      'after': ['#동사', '-으시-'],
    },
]

#### 연결: -ㄴ다고, -는다고
groups['-는다고'] = [
    { 'rules': [[u'-\u11ab다고', COND_V_ALL, ''],
                [u'-\u11ab다고', T_RIEUL, T_RIEUL],
                [u'-는다고', COND_T_NOT_RIEUL, '']],
      'after': ['#동사', '-으시-'],
    },
]

#### 연결: -ㄴ다는, -는다는 (는다고 하는)
groups['-는다는'] = [
    { 'rules': [[u'-\u11ab다는', COND_V_ALL, ''],
                [u'-\u11ab다는', T_RIEUL, T_RIEUL],
                [u'-는다는', COND_T_NOT_RIEUL, '']],
      'after': ['#동사', '-으시-'],
    },
]

#### 연결: -ㄴ다면, -는다면
groups['-는다면'] = [
    { 'rules': [[u'-\u11ab다면', COND_V_ALL, ''],
                [u'-\u11ab다면', T_RIEUL, T_RIEUL],
                [u'-는다면', COND_T_NOT_RIEUL, '']],
      'after': ['#동사', '-으시-'],
    },
]

#### 종결: -ㄴ다면서, -는다면서
groups['-는다면서'] = [
    { 'rules': [[u'-\u11ab다면서', COND_V_ALL, ''],
                [u'-\u11ab다면서', T_RIEUL, T_RIEUL],
                [u'-는다면서', COND_T_NOT_RIEUL, ''],
                [u'-\u11ab다며', COND_V_ALL, ''],
                [u'-\u11ab다며', T_RIEUL, T_RIEUL],
                [u'-는다며', COND_T_NOT_RIEUL, ''],
                ],
      'after': ['#동사', '-으시-'],
    },
]
attach_emphasis(groups['-는다면서'], ['요'])

#### 종결: -는군
groups['-는군'] = [
    { 'rules': [[u'-는군', COND_NOT_RIEUL, ''],
                [u'-는군', T_RIEUL, T_RIEUL]],
      'after': ['#동사', '-으시-'],
    },
]
attach_emphasis(groups['-는군'], ['요'])

#### 종결: -는구나
groups['-는구나'] = [
    { 'rules': [[u'-는구나', COND_NOT_RIEUL, ''],
                [u'-는구나', T_RIEUL, T_RIEUL]],
      'after': ['#동사', '-으시-'],
    },
]

#### 연결, 종결: -는지
groups['-는지'] = [
    { 'rules': [[u'-는지', COND_NOT_RIEUL, ''],
                [u'-는지', T_RIEUL, T_RIEUL]],
      'after': ['#동사', '^.*있다$', '^.*없다$', '^.*계시다$', '-으시-', '-었-', '-겠-'],
    },
]


#### 연결: -면, -으면
groups['-으면'] = [
    { 'rules': [[u'-면', COND_V_OR_RIEUL, ''],
                [u'-으면', COND_T_NOT_RIEUL, '']],
      'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
      'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#ㅎ불규칙'],
    },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS(u'-으면', ['#용언']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS(u'-우면', ['#용언']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS(u'-으면', ['#용언']),
    # ㅎ불규칙
    HIEUH_IRREGULAR_TYPICAL_CLASS(u'-면', ['#용언']),
]

#### 연결: -면서, -으면서
# '-으면' 재활용
groups['-으면서'] = [k.copy() for k in groups['-으면']]
for klass in groups['-으면서']:
    new_rule = []
    for r in klass['rules']:
        new_rule.append([r[0] + '서'] + r[1:])
    klass['rules'] = new_rule
attach_emphasis(groups['-으면서'], ['도'])

#### 연결: -자마자
groups['-자마자'] = [
    { 'rules': [[u'-자마자', '', '']],
      'after': ['#동사', '-으시-'],
    },
]

#### 관형사형 전성: -던
groups['-던'] = [
    { 'rules': [[u'-던', '', '']],
      'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
    },
]

#### 연결: -ㄴ가, -은가
#### 의문형 종결: -ㄴ가, -은가
groups['-은가'] = [
    { 'rules': [[u'-\u11ab가', COND_V_ALL, ''],
                [u'-\u11ab가', T_RIEUL, T_RIEUL],
                [u'-은가', COND_T_NOT_RIEUL, '']],
      'after': ['#형용사', '#이다', '-으시-'],
      'notafter': ['^.*있다$', '^.*없다$'],
      'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#ㅎ불규칙'],
    },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS(u'-은가', ['#형용사']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS(u'-운가', ['#형용사']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS(u'-은가', ['#형용사']),
    # ㅎ불규칙
    HIEUH_IRREGULAR_TYPICAL_CLASS(u'-\u11ab가', ['#형용사']),
]
attach_emphasis(groups['-은가'], ['요'])

#### 연결: -니까, -으니까
groups['-으니까'] = [
    { 'rules': [[u'-니까', COND_V_ALL, ''],
                [u'-니까', T_RIEUL, T_RIEUL],
                [u'-으니까', COND_T_NOT_RIEUL, '']],
      'after': ['#용언', '#이다', '-으시-', '-오-', '-더-', '-었-', '-겠-'],
      'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#ㅎ불규칙'],
    },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS(u'-으니까', ['#용언']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS(u'-우니까', ['#용언']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS(u'-으니까', ['#용언']),
    # ㅎ불규칙
    HIEUH_IRREGULAR_TYPICAL_CLASS(u'-니까', ['#용언']),
]
attach_emphasis(groups['-으니까'], ['요'])

#### 연결: -라면
groups['-라면'] = [
    { 'rules': [[u'-라면', '', '']],
      'after': ['#이다', '아니다', '-으시-', '-더-', '-으리-'],
    },
]

#### 연결: -로구나
groups['-로구나'] = [
    { 'rules': [[u'-로구나', '', '']],
      'after': ['#이다', '아니다', '-으시-'],
    },
]

#### 연결: -ㄴ지, -은지
groups['-은지'] = [
    { 'rules': [[u'-\u11ab지', COND_V_ALL, ''],
                [u'-\u11ab지', T_RIEUL, T_RIEUL],
                [u'-은지', COND_T_NOT_RIEUL, '']],
      'after': ['#이다', '#형용사', '-으시-'],
      'notafter': ['^.*있다$', '^.*없다$'],
      'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#ㅎ불규칙'],
    },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS(u'-은지', ['#형용사']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS(u'-운지', ['#형용사']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS(u'-은지', ['#형용사']),
    # ㅎ불규칙
    HIEUH_IRREGULAR_TYPICAL_CLASS(u'-\u11ab지', ['#형용사']),
]

#### 종결: -십시오, -으십시오
groups['-으십시오'] = [
    { 'rules': [[u'-십시오', COND_V_ALL, ''],
                [u'-십시오', T_RIEUL, T_RIEUL],
                [u'-으십시오', COND_T_NOT_RIEUL, '']],
      'after': ['#동사'],
      'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙'],
    },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS(u'-으십시오', ['#동사']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS(u'-우십시오', ['#동사']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS(u'-으십시오', ['#동사']),
    # 동사이므로 ㅎ불규칙 해당 없음
]

#### 연결: -므로, -으므로
groups['-으므로'] = [
    { 'rules': [[u'-므로', COND_V_OR_RIEUL, ''],
                [u'-으므로', COND_T_NOT_RIEUL, '']],
      'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
      'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#ㅎ불규칙'],
    },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS(u'-으므로', ['#용언']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS(u'-우므로', ['#용언']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS(u'-으므로', ['#용언']),
    # ㅎ불규칙
    HIEUH_IRREGULAR_TYPICAL_CLASS(u'-므로', ['#용언']),
]

#### 연결: -다고
groups['-다고'] = [
    { 'rules': [[u'-다고', '', '']],
      'after': ['#형용사', '-으시-', '-었-', '-겠-'],
    },
]
attach_emphasis(groups['-다고'], ['요'])

#### 연결: -다는 (다고 하는)
groups['-다는'] = [
    { 'rules': [[u'-다는', '', '']],
      'after': ['#용언', '-으시-', '-었-', '-겠-'],
    },
]

#### 연결: -더라도
groups['-더라도'] = [
    { 'rules': [[u'-더라도', '', '']],
      'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
    },
]

#### 연결: -러, -으러
groups['-으러'] = [
    { 'rules': [[u'-러', COND_V_OR_RIEUL, ''],
                [u'-으러', COND_T_NOT_RIEUL, '']],
      'after': ['#동사', '-으시-'],
      'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙'],
    },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS(u'-으러', ['#동사']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS(u'-우러', ['#동사']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS(u'-으러', ['#동사']),
    # 동사이므로 ㅎ불규칙 해당 없음
]

#### 종결: -네
groups['-네'] = [
    { 'rules': [[u'-네', COND_NOT_RIEUL, ''],
                [u'-네', T_RIEUL, T_RIEUL]],
      'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
    },
]
attach_emphasis(groups['-네'], ['요'])

#### 종결: -니, -으니
#### 연결: -니, -으니
groups['-으니'] = [
    { 'rules': [[u'-니', COND_V_ALL, ''],
                [u'-니', T_RIEUL, T_RIEUL],
                [u'-으니', COND_T_NOT_RIEUL, '']],
      'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-', '-오-', '-더-'],
      'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#ㅎ불규칙'],
    },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS(u'-으니', ['#용언']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS(u'-우니', ['#용언']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS(u'-으니', ['#용언']),
    # ㅎ불규칙
    HIEUH_IRREGULAR_TYPICAL_CLASS(u'-니', ['#용언']),
]

#### 의문형 종결: -니 (위와 구별된다)
groups['-니?'] = [
    { 'rules': [[u'-니', COND_NOT_RIEUL, ''],
                [u'-니', T_RIEUL, T_RIEUL]],
      'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
    },
]

# #### 의문형 종결: -으니 (구어체)
# groups['-으니?'] = [
#     { 'rules': [[u'-으니', COND_T_NOT_RIEUL, '']],
#       'after': ['#형용사'],
#     },
# ]

#### 종결: -군
groups['-군'] = [
    { 'rules': [[u'-군', '', '']],
      'after': ['#형용사', '#이다', '-으시-', '-었-', '-겠-', '-더-'],
    },
]
attach_emphasis(groups['-군'], ['요'])

#### 종결: -구나
groups['-구나'] = [
    { 'rules': [[u'-구나', '', '']],
      'after': ['#형용사', '#이다', '-으시-', '-었-', '-겠-'],
    },
]

#### 종결: -으냐 (형용사)
groups['-으냐'] = [
    { 'rules': [[u'-냐', COND_V_ALL, ''],
                [u'-냐', T_RIEUL, T_RIEUL],
                [u'-으냐', COND_T_NOT_RIEUL, '']],
      'after': ['#형용사', '#이다'],
      'notafter': ['^.*있다$', '^.*없다$'],
      'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#ㅎ불규칙'],
    },
    # NOTE: 어간과 결합하지 않고 '-었-' 및 '-겠-' 선어말 어미와 결합할
    # 경우에는 받침이 있음에도 "-었으냐", "-겠느냐"가 아니라 "-었냐",
    # "-겠냐" 형태가 되므로, 선어말 어미 결합하는 부분은 별도로 구분해
    # 모든 음절과 결합을 허용한다.
    { 'rules': [[u'-냐', '', '']],
      'after': ['-으시-', '-었-', '-겠-'],
    },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS(u'-으냐', ['#형용사']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS(u'-우냐', ['#형용사']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS(u'-으냐', ['#형용사']),
    # ㅎ불규칙
    HIEUH_IRREGULAR_TYPICAL_CLASS(u'-냐', ['#형용사']),
]

#### 종결: -으냐고 (형용사)
groups['-으냐고'] = [k.copy() for k in groups['-으냐']]
for klass in groups['-으냐고']:
    new_rule = []
    for r in klass['rules']:
        new_rule.append([r[0] + '고'] + r[1:])
    klass['rules'] = new_rule

#### 연결: -으냐네 (-으냐고 하네)
groups['-으냐네'] = [k.copy() for k in groups['-으냐']]
for klass in groups['-으냐네']:
    new_rule = []
    for r in klass['rules']:
        new_rule.append([r[0] + '네'] + r[1:])
    klass['rules'] = new_rule

#### 연결: -으냐는 (-으냐고 하는)
groups['-으냐는'] = [k.copy() for k in groups['-으냐']]
for klass in groups['-으냐는']:
    new_rule = []
    for r in klass['rules']:
        new_rule.append([r[0] + '는'] + r[1:])
    klass['rules'] = new_rule

#### 연결: -으냐니 (-으냐고 하니)
groups['-으냐니'] = [k.copy() for k in groups['-으냐']]
for klass in groups['-으냐니']:
    new_rule = []
    for r in klass['rules']:
        new_rule.append([r[0] + '니'] + r[1:])
    klass['rules'] = new_rule

#### 연결: -으냐니까 (-으냐고 하니)
groups['-으냐니까'] = [k.copy() for k in groups['-으냐']]
for klass in groups['-으냐니까']:
    new_rule = []
    for r in klass['rules']:
        new_rule.append([r[0] + '니까'] + r[1:])
    klass['rules'] = new_rule

#### 연결: -으냐며 (-으냐고 하며)
groups['-으냐며'] = [k.copy() for k in groups['-으냐']]
for klass in groups['-으냐며']:
    new_rule = []
    for r in klass['rules']:
        new_rule.append([r[0] + '며'] + r[1:])
    klass['rules'] = new_rule

#### 연결: -으냐면 (-으냐고 하면)
groups['-으냐면'] = [k.copy() for k in groups['-으냐']]
for klass in groups['-으냐면']:
    new_rule = []
    for r in klass['rules']:
        new_rule.append([r[0] + '면'] + r[1:])
    klass['rules'] = new_rule

#### 연결: -으냐면서 (-으냐고 하면서)
groups['-으냐면서'] = [k.copy() for k in groups['-으냐']]
for klass in groups['-으냐면서']:
    new_rule = []
    for r in klass['rules']:
        new_rule.append([r[0] + '면서'] + r[1:])
    klass['rules'] = new_rule

#### 종결: -느냐 (동사)
groups['-느냐'] = [
    { 'rules': [[u'-느냐', COND_NOT_RIEUL, ''],
                [u'-느냐', T_RIEUL, T_RIEUL]],
      'after': ['#동사', '^.*있다$', '^.*없다$', '^.*계시다$', '-으시-', '-었-', '-겠-'],
    },
]

#### 종결: -느냐고 (동사)
groups['-느냐고'] = [k.copy() for k in groups['-느냐']]
for klass in groups['-느냐고']:
    new_rule = []
    for r in klass['rules']:
        new_rule.append([r[0] + '고'] + r[1:])
    klass['rules'] = new_rule

#### 연결: -느냐네 (-느냐고 하네)
groups['-느냐네'] = [k.copy() for k in groups['-느냐']]
for klass in groups['-느냐네']:
    new_rule = []
    for r in klass['rules']:
        new_rule.append([r[0] + '네'] + r[1:])
    klass['rules'] = new_rule

#### 연결: -느냐는 (-느냐고 하는)
groups['-느냐는'] = [k.copy() for k in groups['-느냐']]
for klass in groups['-느냐는']:
    new_rule = []
    for r in klass['rules']:
        new_rule.append([r[0] + '는'] + r[1:])
    klass['rules'] = new_rule

#### 연결: -느냐니 (-느냐고 하니)
groups['-느냐니'] = [k.copy() for k in groups['-느냐']]
for klass in groups['-느냐니']:
    new_rule = []
    for r in klass['rules']:
        new_rule.append([r[0] + '니'] + r[1:])
    klass['rules'] = new_rule

#### 연결: -느냐니까 (-느냐고 하니)
groups['-느냐니까'] = [k.copy() for k in groups['-느냐']]
for klass in groups['-느냐니까']:
    new_rule = []
    for r in klass['rules']:
        new_rule.append([r[0] + '니까'] + r[1:])
    klass['rules'] = new_rule

#### 연결: -느냐며 (-느냐고 하며)
groups['-느냐며'] = [k.copy() for k in groups['-느냐']]
for klass in groups['-느냐며']:
    new_rule = []
    for r in klass['rules']:
        new_rule.append([r[0] + '며'] + r[1:])
    klass['rules'] = new_rule

#### 연결: -느냐면 (-느냐고 하면)
groups['-느냐면'] = [k.copy() for k in groups['-느냐']]
for klass in groups['-느냐면']:
    new_rule = []
    for r in klass['rules']:
        new_rule.append([r[0] + '면'] + r[1:])
    klass['rules'] = new_rule

#### 연결: -느냐면서 (-느냐고 하면서)
groups['-느냐면서'] = [k.copy() for k in groups['-느냐']]
for klass in groups['-느냐면서']:
    new_rule = []
    for r in klass['rules']:
        new_rule.append([r[0] + '면서'] + r[1:])
    klass['rules'] = new_rule

#### 연결: -느니
#### 종결: -느니
groups['-느니'] = [
    { 'rules': [[u'-느니', COND_NOT_RIEUL, ''],
                [u'-느니', T_RIEUL, T_RIEUL]],
      'after': ['#동사', '^.*있다$', '^.*없다$', '^.*계시다$', '-으시-', '-었-', '-겠-'],
    },
]
attach_emphasis(groups['-느니'], ['만'])

#### 연결: -되
groups['-되'] = [
    { 'rules': [[u'-되', '', '']],
      'after': ['#용언', '#이다', '-으시-'],
    },
]

#### 종결: -소
groups['-소'] = [
    { 'rules': [[u'-소', COND_NOT_RIEUL, ''],
                [u'-소', T_RIEUL, T_RIEUL]],
      'after': ['#용언', '-었-', '-겠-'],
    },
]

#### 종결: -오
groups['-으오'] = [
    { 'rules': [[u'-오', COND_V_ALL, ''],
                [u'-오', T_RIEUL, T_RIEUL],
                [u'-으오', COND_T_NOT_RIEUL, '']],
      'after': ['#용언', '#이다', '-으시-'],
      'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#ㅎ불규칙'],
    },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS(u'-으오', ['#용언']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS(u'-우오', ['#용언']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS(u'-으오', ['#용언']),
    # ㅎ불규칙
    HIEUH_IRREGULAR_TYPICAL_CLASS(u'-오', ['#용언']),
]

#### 연결: -대서 (다고 하여서)
groups['-대서'] = [
    { 'rules': [[u'-대서', '', '']],
      'after': ['#형용사', '-으시-', '-었-', '-겠-'],
    },
]

#### 종결: -잖아 (~지 않아)
groups['-잖아'] = [
    { 'rules': [[u'-잖아', '', '']],
      'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
    },
]
attach_emphasis(groups['-잖아'], ['요'])

#### 종결: -든지 (혹은 줄임 형태 -든)
groups['-든지'] = [
    { 'rules': [[u'-든지', '', ''],
                [u'-든', '', '']],
      'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
    },
]

#### 종결: -라
groups['-라'] = [
    { 'rules': [[u'-라', '', '']],
      'after': ['#이다', '아니다', '-으시-', '-더-', '-으리-'],
    },
]

#### 종결: -라니, -으라니
groups['-으라니'] = [
    { 'rules': [[u'-라니', COND_V_OR_RIEUL, ''],
                [u'-으라니', COND_T_NOT_RIEUL, '']],
      'after': ['#동사', '#이다', '아니다', '-으시-', '-더-', '-으리-'],
      'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙'],
    },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS(u'-으라니', ['#동사']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS(u'-우라니', ['#동사']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS(u'-으라니', ['#동사']),
    # 동사이므로 ㅎ불규칙 해당 없음
]
attach_emphasis(groups['-으라니'], ['요'])

#### 연결: -거든
#### 종결: -거든
groups['-거든'] = [
    { 'rules': [[u'-거든', '', '']],
      'after': ['#용언', '#이다', '아니다', '-으시-', '-었-', '-겠-'],
    },
]
attach_emphasis(groups['-거든'], ['요'])

#### 연결: -자면 (-자고 하면)
groups['-자면'] = [
    { 'rules': [[u'-자면', '', '']],
      'after': ['#동사'],
    },
]

#### 종결: -으리라, -리라
groups['-으리라'] = [
    { 'rules': [[u'-리라', COND_V_OR_RIEUL, ''],
                [u'-으리라', COND_T_NOT_RIEUL, '']],
      'after': ['#용언', '-으시', '-었-', '-겠-'],
      'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#ㅎ불규칙'],
    },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS(u'-으리라', ['#용언']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS(u'-우리라', ['#용언']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS(u'-으리라', ['#용언']),
    # ㅎ불규칙
    HIEUH_IRREGULAR_TYPICAL_CLASS(u'-리라', ['#용언']),
]

#### 종결: -으려니, -려니
groups['-으려니'] = [
    { 'rules': [[u'-려니', COND_V_OR_RIEUL, ''],
                [u'-으려니', COND_T_NOT_RIEUL, '']],
      'after': ['#용언', '#이다', '-으시-', '-었-'],
      'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#ㅎ불규칙'],
    },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS(u'-으려니', ['#용언']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS(u'-우려니', ['#용언']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS(u'-으려니', ['#용언']),
    # ㅎ불규칙
    HIEUH_IRREGULAR_TYPICAL_CLASS(u'-려니', ['#용언']),
]

#### 종결: -는가
groups['-는가'] = [
    { 'rules': [[u'-는가', COND_NOT_RIEUL, ''],
                [u'-는가', T_RIEUL, T_RIEUL]],
      'after': ['#동사', '^.*있다$', '^.*없다$', '^.*계시다$', '-으시-', '-었-', '-겠-'],
    },
]

#### 종결: -(으)라네
groups['-으라네'] = [
    { 'rules': [[u'-라네', COND_V_ALL, ''],
                [u'-라네', T_RIEUL, T_RIEUL],
                [u'-으라네', COND_T_NOT_RIEUL, '']],
      'after': ['#동사', '#이다', '^.*아니다$', '-으시-', '-더-', '-으리-'],
      'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙'],
    },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS(u'-으라네', ['#동사']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS(u'-우라네', ['#동사']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS(u'-으라네', ['#동사']),
    # 동사이므로 ㅎ불규칙 해당 없음
]
attach_emphasis(groups['-으라네'], ['요'])

#### 종결: -(는)다네
groups['-다네'] = [
    { 'rules': [[u'-%s다네' % T_NIEUN, COND_V_ALL, ''],
                [u'-%s다네' % T_NIEUN, T_RIEUL, T_RIEUL],
                [u'-는다네', COND_T_NOT_RIEUL, '']],
      'after': ['#동사'],
    },
]
attach_emphasis(groups['-다네'], ['요'])

#### 연결: -라서
groups['-라서'] = [
    { 'rules': [[u'-라서', '', '']],
      'after': ['#이다', '아니다', '-으시-', '-더-', '-으리-'],
    },
]

#### 연결: -ㄹ는지, -을는지
groups['-을는지'] = [
    { 'rules': [[u'-%s는지' % T_RIEUL, COND_V_ALL, ''],
                [u'-%s는지' % T_RIEUL, T_RIEUL, T_RIEUL],
                [u'-을는지', COND_T_NOT_RIEUL, '']],
      'after': ['#용언', '#이다', '-으시-', '-었-'],
      'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#ㅎ불규칙'],
    },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS(u'-을는지', ['#용언']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS(u'-울는지', ['#용언']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS(u'-을는지', ['#용언']),
    # ㅎ불규칙
    HIEUH_IRREGULAR_TYPICAL_CLASS(u'-%s는지' % T_RIEUL, ['#용언']),
]
attach_emphasis(groups['-을는지'], ['는', '도'])

#### 종결: -ㄴ다니, -는다니
groups['-는다니'] = [
    { 'rules': [[u'-%s다니' % T_NIEUN, COND_V_ALL, ''],
                [u'-%s다니' % T_NIEUN, T_RIEUL, T_RIEUL],
                [u'-는다니', COND_T_NOT_RIEUL, '']],
      'after': ['#동사', '-으시-'],
    },
]

#### 종결: -다니
groups['-다니'] = [
    { 'rules': [[u'-다니', '', '']],
      'after': ['#용언', '-으시-', '-었-', '-겠-'],
    },
]

#### 연결: -자는 (-자고 하는)
groups['-자는'] = [
    { 'rules': [[u'-자는', '', '']],
      'after': ['#동사'],
    },
]

#### 연결: -던데
groups['-던데'] = [
    { 'rules': [[u'-던데', '', '']],
      'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
    },
]

#### 연결: -느라고, -느라
groups['-느라고'] = [
    { 'rules': [[u'-느라고', COND_NOT_RIEUL, ''],
                [u'-느라고', T_RIEUL, T_RIEUL],
                [u'-느라', COND_NOT_RIEUL, ''],
                [u'-느라', T_RIEUL, T_RIEUL]],
      'after': ['#동사', '-으시-'],
    },
]

#### 종결: -ㄹ래, -을래
groups['-을래'] = [
    { 'rules': [[u'-%s래' % T_RIEUL, COND_V_ALL, ''],
                [u'-%s래' % T_RIEUL, T_RIEUL, T_RIEUL],
                [u'-을래', COND_NOT_RIEUL, '']],
      'after': ['#동사'],
      'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙'],
    },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS(u'-을래', ['#동사']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS(u'-울래', ['#동사']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS(u'-을래', ['#동사']),
    # 동사이므로 ㅎ불규칙 해당 없음
]
attach_emphasis(groups['-을래'], ['요'])

