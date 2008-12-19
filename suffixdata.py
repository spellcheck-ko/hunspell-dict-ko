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
# Portions created by the Initial Developer are Copyright (C) 2008
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

######################################################################
#### 유틸리티

# 자모

LSTART = 0x1100
LEND = 0x1112
VSTART = 0x1161
VEND = 0x1175
TSTART = 0x11a8
TEND = 0x11c2

L_ALL = ''.join([unichr(c) for c in range(LSTART, LEND + 1)])
V_ALL = ''.join([unichr(c) for c in range(VSTART, VEND + 1)])
T_ALL = ''.join([unichr(c) for c in range(TSTART, TEND + 1)])

L_HIEUH = u'\u1112'
V_A = u'\u1161'
V_AE = u'\u1162'
V_YA = u'\u1163'
V_YAE = u'\u1164'
V_EO = u'\u1165'
V_E = u'\u1166'
V_YEO = u'\u1167'
V_O = u'\u1169'
V_OE = u'\u116c'
V_U = u'\u116e'
V_EU = u'\u1173'
V_I = u'\u1175'
T_NIEUN = u'\u11ab'
T_TIKEUT = u'\u11ae'
T_RIEUL = u'\u11af'
T_RIEUL_MIEUM = u'\u11b1'
T_PIEUP = u'\u11b8'
T_SIOS = u'\u11ba'
T_SSANGSIOS = u'\u11bb'
T_HIEUH = u'\u11c2'

L_NOT_HIEUH = ''.join([c for c in L_ALL if not c in L_HIEUH])
V_A_O = V_A + V_O
V_NOT_A_O = ''.join([c for c in V_ALL if  not c in V_A_O])
V_NOT_A_EO_O = ''.join([c for c in V_NOT_A_O if not c in V_EO])

# 조건

COND_V_ALL = u'[%s]' % V_ALL
COND_T_ALL = u'[%s]' % T_ALL
COND_V_OR_RIEUL = u'[%s%s]' % (V_ALL, T_RIEUL)
COND_T_NOT_RIEUL = u'[%s]' % ''.join([t for t in T_ALL if t != T_RIEUL])

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

# 전성어미처럼 또 다른 접사 규칙이 적용될 수 있는 경우 플래그 지정 (예: ~음 + 을)
def attach_continuation_flags(group, flags):
    for klass in group:
        for r in klass['rules']:
            r.append(flags)

#### 어/아로 시작하는 어미를 위한 유틸리티

# ㅏ/ㅗ 모음의 음절로 끝나는 경우  (ㅏ로 끝나는 경우 제외)
COND_EOA_AO = [ V_O, '[%s][%s]' % (V_A_O, T_ALL) ]
# ㅏ/ㅗ 제외한 모음의 음절로 끝나는 경우  (ㅓ로 끝나는 경우 제외)
COND_EOA_NOT_AO = [ '[%s]' % V_NOT_A_EO_O, '[%s][%s]' % (V_NOT_A_O, T_ALL) ]
# ㅓ로 끝나는 경우
COND_EOA_EO = V_EO
# ㅏ로 끝나는 경우 ('하' 제외)
COND_EOA_A = '[%s]%s' % (L_NOT_HIEUH, V_A)
# 하로 끝나는 경우
COND_EOA_HA = u'하'

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

# 참고: '으' 음절 앞에 오는 음절이 있다면 그 음절의 모음이 양성모음이냐
# 음성모음이냐에 따라 어미의 '어/아'가 결정되는데, '크다', '쓰다',
# '끄다'같은 으불규칙용언의 경우 앞의 음절이 없으면서 '어'가 붙는다.
# 그래서 aff 파일의 같은 규칙 안에서 조건으로 정의할 수가 없다. (aff
# 파일에서 쓸 수 있는 condition으로는 으 앞에 없다는 걸 정의할 수가
# 없다.) 그러므로 '크다', '쓰다', '끄다'는 항상 별도 규칙으로 만든다.

# 앞에 ㅏ/ㅗ 모음의 음절
COND_EU_AO = [ u'[%s][%s]%s' % (V_A_O, L_ALL, V_EU),
               u'[%s][%s][%s]%s' % (V_A_O, T_ALL, L_ALL, V_EU) ]
# 앞에 ㅏ/ㅗ 모음이 아닌 음절
COND_EU_NOT_AO = [ u'[%s][%s]%s' % (V_NOT_A_O, L_ALL, V_EU),
                   u'[%s][%s][%s]%s' % (V_NOT_A_O, T_ALL, L_ALL, V_EU) ]



######################################################################
#### 어미 데이터

groups = {}

#### 높임 선어말

groups[u'-으시-'] = [
    { 'rules': [[u'-시-', COND_V_ALL, ''],
                [u'-시-', T_RIEUL, T_RIEUL],
                [u'-으시-', COND_T_NOT_RIEUL, '']],
      'after': ['#용언', '#이다'],
      'notafter': ['계시다', '모시다'],
      'notcond': ['#ㅂ불규칙', '#ㅅ불규칙'],
    },
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS(u'-우시', ['#용언']),
    # ㅅ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS(u'-으시', ['#용언']),
]

#### 과거 시제 선어말

groups[u'-었-'] = [
    { 'rules': [[u'-었-', COND_EOA_NOT_AO, ''],
                [u'-았-', COND_EOA_AO, ''],
                [u'-\u1165\u11bb-', COND_EOA_EO, V_EO],
                [u'-\u1161\u11bb-', COND_EOA_A, V_A],
                [u'-였-', u'하', ''],
                # 준말
                [u'-\u116a\u11bb-', V_O, V_O], # 오았 -> 왔
                [u'-\u116f\u11bb-', V_U, V_U], # 우었 -> 웠
                [u'-\u116b\u11bb-', V_OE, V_OE], # 외었 -> 왜ㅆ  # TODO: '외다', '뇌다' 예외
                [u'-\u1162\u11bb-', u'하', V_A], # 하였 -> 했
                [u'-\u1167\u11bb-', V_I, V_I], # 이었 -> 였
                [u'-\u11bb-', V_AE, ''], # 애었 -> 앴
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
               ],
      'after': ['#용언'],
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
      'cond': ['#으불규칙'],
    },
    # 으불규칙 예외 '끄다', '뜨다', '크다', '쓰다'
    { 'rules': [[u'-\u1165\u11bb-', V_EU, V_EU]],
      'after': ['끄다', '뜨다', '크다', '쓰다'],
      'cond': ['#으불규칙'],
    },
]
# 대과거 시제 덧붙이기
for klass in groups[u'-었-']:
    new_rules = []
    for r in klass['rules']:
        new_rules.append([r[0][:-1] + u'었-'] + r[1:])
    klass['rules'] += new_rules

#### 미래 시제 선어말

groups[u'-겠-'] = [
    { 'rules': [[u'-겠-', '', '']],
      'after': ['#용언', '#이다', '-으시-', '-었-'],
    },
]

#### 시제 선어말: -더-

groups[u'-더-'] = [
    { 'rules': [[u'-더-', '', '']],
      'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
    },
]


#### 연결: -어, -아
groups[u'-어'] = [
    { 'rules': [[u'-어', COND_EOA_NOT_AO, ''],
                [u'-아', COND_EOA_AO, ''],
                [u'-\u1165', COND_EOA_EO, V_EO],
                [u'-\u1161', COND_EOA_A, V_A],
                [u'-여', u'하', ''],
                [u'-\u116a', V_O, V_O], # 오아 -> 와
                [u'-\u116f', V_U, V_U], # 우어 -> 워
                [u'-\u116b', V_OE, V_OE], # 외어 -> 왜  # TODO: '외다', '뇌다' 예외
                [u'-\u1162', u'하', V_A], # 하여 -> 해
                [u'-\u1167', V_I, V_I], # 이어 -> 여
                [u'-\u1162', V_AE, V_AE], # 애어 -> 애
                ],
      'after': ['#용언', '-었-'],
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
               ],
      'after': ['#용언'],
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
      'cond': ['#으불규칙'],
    },
    # 으불규칙 예외 '끄다', '뜨다', '크다', '쓰다'
    { 'rules': [[u'-\u1165', V_EU, V_EU]],
      'after': ['끄다', '뜨다', '크다', '쓰다'],
      'cond': ['#으불규칙'],
    },
]

#### 연결: -어다, -아다 (동사)
# '-어' 재활용
groups[u'-어다'] = copy_group(groups[u'-어'])
for klass in groups[u'-어다']:
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
groups[u'-어라'] = copy_group(groups[u'-어'])
for klass in groups[u'-어라']:
    for r in klass['rules']:
        r[0] = r[0] + '라'
# 거라불규칙/너라불규칙 포함
groups[u'-어라'][0]['notcond'] += ['#거라불규칙', '#너라불규칙']
groups[u'-어라'] += [
    # 거라불규칙
    { 'rules': [[u'-거라', '', '']],
      'after': ['#동사'],
      'cond': ['#거라불규칙'],
    },
    # 너라불규칙
    { 'rules': [[u'-너라', '', '']],
      'after': ['#동사'],
      'cond': ['#너라불규칙'],
    },
]

#### 연결: -어도, -아도
# '-어' 재활용
groups[u'-어도'] = copy_group(groups[u'-어'])
for klass in groups[u'-어도']:
    for r in klass['rules']:
        r[0] = r[0] + '도'

#### 연결: -어서, -아서
# '-어' 재활용
groups[u'-어서'] = copy_group(groups[u'-어'])
for klass in groups[u'-어서']:
    for r in klass['rules']:
        r[0] = r[0] + '서'

#### 연결: -어야, -아야
# '-어' 재활용
groups[u'-어야'] = copy_group(groups[u'-어'])
for klass in groups[u'-어야']:
    for r in klass['rules']:
        r[0] = r[0] + '야'

#### 연결: -어야, -아야
# '-어' 재활용
groups[u'-어야지'] = copy_group(groups[u'-어'])
for klass in groups[u'-어야지']:
    for r in klass['rules']:
        r[0] = r[0] + '야지'

#### 종결: -어요, -아요
# '-어' 재활용
groups[u'-어요'] = copy_group(groups[u'-어'])
for klass in groups[u'-어요']:
    new_rule = []
    for r in klass['rules']:
        new_rule.append([r[0] + '요'] + r[1:])
    klass['rules'] = new_rule

#### 관형사형 전성: -ㄹ, -을
groups[u'-을'] = [
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
    # ㅎ불규칙 TODO: 확인 필요
    HIEUH_IRREGULAR_TYPICAL_CLASS(u'-\u11af', ['#용언']),
]

#### 종결: -ㄹ걸, -을걸
# '-을' 재활용
groups[u'-을걸'] = copy_group(groups[u'-을'])
for klass in groups[u'-을걸']:
    for r in klass['rules']:
        r[0] = r[0] + '걸'

#### 연결: -ㄹ까, -을까
# '-을' 재활용
groups[u'-을까'] = copy_group(groups[u'-을'])
for klass in groups[u'-을까']:
    for r in klass['rules']:
        r[0] = r[0] + '까'
# ~ㄹ까요, -을까요 보조사
attach_emphasis(groups[u'-을까'], ['요'])

#### 연결: -ㄹ망정, -을망정
# '-을' 재활용
groups[u'-을망정'] = copy_group(groups[u'-을'])
for klass in groups[u'-을망정']:
    for r in klass['rules']:
        r[0] = r[0] + '망정'

#### 연결: -ㄹ수록, -을수록
# '-을' 재활용
groups[u'-을수록'] = copy_group(groups[u'-을'])
for klass in groups[u'-을수록']:
    for r in klass['rules']:
        r[0] = r[0] + '수록'

#### 연결: -ㄹ지, -을지
# '-을' 재활용
groups[u'-을지'] = copy_group(groups[u'-을'])
for klass in groups[u'-을지']:
    for r in klass['rules']:
        r[0] = r[0] + '지'
attach_emphasis(groups[u'-을지'], ['는', '도'])

#### 연결: -ㄹ지라도, -을지라도
# '-을' 재활용
groups[u'-을지라도'] = copy_group(groups[u'-을'])
for klass in groups[u'-을지라도']:
    for r in klass['rules']:
        r[0] = r[0] + '지라도'

#### 연결: -ㄹ지언정, -을지언정
# '-을' 재활용
groups[u'-을지언정'] = copy_group(groups[u'-을'])
for klass in groups[u'-을지언정']:
    for r in klass['rules']:
        r[0] = r[0] + '지언정'

#### 종결: -다

groups[u'-다'] = [
    { 'rules': [[u'-다', '', '']],
      'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
    },
]

#### 관형사형 전성: -는
groups[u'-는'] = [
    { 'rules': [[u'-는', u'[^%s]' % T_RIEUL, ''],
                [u'-는', T_RIEUL, T_RIEUL]],
      'after': ['#동사', '있다', '없다', '계시다', '-으시-', '-겠-'],
    },
]

#### 연결: -게
groups[u'-게'] = [
    { 'rules': [[u'-게', '', ''],
                [u'-케', u'하', u'하'], # 하게 -> 케 준말
                ],
      'after': ['#용언', '-으시-'],
    },
]
attach_emphasis(groups[u'-게'], ['도'])

#### 연결: -다가
groups[u'-다가'] = [
    { 'rules': [[u'-다가', '', '']],
      'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
    },
]

#### 관형사형 전성: -ㄴ, -은
groups[u'-은'] = [
    { 'rules': [[u'-\u11ab', COND_V_ALL, ''],
                [u'-\u11ab', T_RIEUL, T_RIEUL],
                [u'-은', COND_T_NOT_RIEUL, '']],
      'after': ['#용언', '#이다', '-으시-'],
      'notafter': ['있다', '없다'],
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
groups[u'-지'] = [
    { 'rules': [[u'-지', '', ''],
                [u'-치', u'하', u'하'], # 하지 -> 치 준말
               ],
      'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
    },
]
attach_emphasis(groups[u'-지'], ['요', '도'])
# 지요 -> 죠 준말
groups[u'-지'][0]['rules'].append([u'-죠', '', ''])


#### 연결: -지마는
groups[u'-지마는'] = [
    { 'rules': [[u'-지마는', '', ''],
                [u'-지만', '', ''],
                [u'-치만', u'하', u'하'],   # 하지만 -> 치만 준말
                [u'-치마는', u'하', u'하'], # 하지마는 -> 치마는 준말
                ],
      'after': ['#용언', '#이다', '-었-', '-겠-'],
    },
]

#### 연결: -며, -으며
groups[u'-으며'] = [
    { 'rules': [[u'-며', COND_V_OR_RIEUL, ''],
                [u'-으며', COND_T_NOT_RIEUL, '']],
      'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
      'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙'],
    },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS(u'-으며', ['#용언']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS(u'-우며', ['#용언']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS(u'-으며', ['#용언']),
]

#### 종결: -ㅂ니다, -습니다
groups[u'-습니다'] = [
    { 'rules': [[u'-\u11b8니다', COND_V_ALL, ''],
                [u'-\u11b8니다', T_RIEUL, T_RIEUL],
                [u'-습니다', COND_T_NOT_RIEUL, '']],
      'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
    },
]

#### 종결: -ㅂ니까, -습니까
groups[u'-습니까'] = [
    { 'rules': [[u'-\u11b8니까', COND_V_ALL, ''],
                [u'-\u11b8니까', T_RIEUL, T_RIEUL],
                [u'-습니까', COND_T_NOT_RIEUL, '']],
      'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
    },
]

#### 연결: -고
#### 종결: -고
groups[u'-고'] = [
    { 'rules': [[u'-고', '', '']],
      'after': ['#용언', '#이다', '-'],
      'notafter': ['-으리-', '-더-'],
    },
]
attach_emphasis(groups[u'-고'], ['요'])

#### 연결: -고는
groups[u'-고는'] = [
    { 'rules': [[u'-고는', '', ''],
                [u'-곤', '', '']],
      'after': ['#동사', '-으시-'],
    },
]

#### 연결: -고도
groups[u'-고도'] = [
    { 'rules': [[u'-고도', '', '']],
      'after': ['#용언', '#이다', '-으시-'],
    },
]

#### 연결: -고자
groups[u'-고자'] = [
    { 'rules': [[u'-고자', '', '']],
      'after': ['#동사', '있다', '없다', '계시다', '-으시-'],
    },
]

#### 종결: -시어요, -으시어요
groups[u'-으시어요'] = [
    { 'rules': [[u'-시어요', COND_V_ALL, ''],
                [u'-시어요', T_RIEUL, T_RIEUL],
                [u'-으시어요', COND_T_NOT_RIEUL, ''],
                # 준말: -세요, -으세요
                [u'-세요', COND_V_ALL, ''],
                [u'-세요', T_RIEUL, T_RIEUL],
                [u'-으세요', COND_T_NOT_RIEUL, '']],
      'after': ['#동사', '#이다'],
    },
]

#### 연결: -거나
groups[u'-거나'] = [
    { 'rules': [[u'-거나', '', '']],
      'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-', '-으옵-'],
    },
]

#### 연결: -려, -으려
groups[u'-으려'] = [
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
]

#### 연결: -려고, -으려고
groups[u'-으려고'] = [
    { 'rules': [[u'-려고', COND_V_OR_RIEUL, ''],
                [u'-으려고', COND_T_NOT_RIEUL, '']],
      'after': ['#동사', '-으시-'],
      'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙'],
    },
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS(u'-우려고', ['#동사']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS(u'-으려고', ['#동사']),
]

#### 연결: -려는, -으려는 (려고 하는)
groups[u'-으려는'] = [
    { 'rules': [[u'-려는', COND_V_OR_RIEUL, ''],
                [u'-으려는', COND_T_NOT_RIEUL, '']],
      'after': ['#동사', '#이다', '-으시-'],
      'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙'],
    },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS(u'-으려는', ['#동사']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS(u'-우려는', ['#동사']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS(u'-으려는', ['#동사']),
]

#### 연결: -려면, -으려면
groups[u'-으려면'] = [
    { 'rules': [[u'-려면', COND_V_OR_RIEUL, ''],
                [u'-으려면', COND_T_NOT_RIEUL, '']],
      'after': ['#용언', '#이다', '-으시-', '-었-'],
      'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙'],
    },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS(u'-으려면', ['#용언']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS(u'-우려면', ['#용언']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS(u'-으려면', ['#용언']),
]

#### 연결: -도록
groups[u'-도록'] = [
    { 'rules': [[u'-도록', '', '']],
      'after': ['#동사', '-으시-',
                '#형용사', # FIXME: 일부 형용사만 포함하지만 열거하기에는 너무 많다.
               ],
    },
]

#### 연결: -는데
groups[u'-는데'] = [
    { 'rules': [[u'-는데', '', '']],
      'after': ['#동사', '있다', '없다', '계시다', '-으시-', '-었-', '-겠-'], 
    },
]
attach_emphasis(groups[u'-는데'], ['도', '요'])

#### 연결: -나, -으나
groups[u'-으나'] = [
    { 'rules': [[u'-나', COND_V_ALL, ''],
                [u'-나', T_RIEUL, T_RIEUL],
                [u'-으나', COND_T_NOT_RIEUL, '']],
      'after': ['#용언', '#이다', '-으시-', '-사오-', '-었-', '-겠-'],
      'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙'],
    },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS(u'-으나', ['#용언']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS(u'-우나', ['#용언']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS(u'-으나', ['#용언']),
]

#### 연결: -다시피
groups[u'-다시피'] = [
    { 'rules': [[u'-다시피', '', '']],
      'after': ['#동사', '-으시-', '-었-', '-겠-'],
    },
]

#### 종결: -ㅂ시다, -읍시다
groups[u'-읍시다'] = [
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
]

#### 연결: -자
groups[u'-자'] = [
    { 'rules': [[u'-자', '', '']],
      'after': ['#동사'], # TODO: 일부 형용사
    },
]

#### 연결: -기에
groups[u'-기에'] = [
    { 'rules': [[u'-기에', '', '']],
      'after': ['#용언', '#이다', '-으시-', '-었-'], # TODO: 일부 형용사
    },
]

#### 연결: -듯
groups[u'-듯'] = [
    { 'rules': [[u'-듯', '', ''],
                [u'-듯이', '', '']],
      'after': ['#용언', '#이다'],
    },
]

#### 연결: -다면
groups[u'-다면'] = [
    { 'rules': [[u'-다면', '', '']],
      'after': ['#형용사', '-으시-', '-었-', '-겠-'],
    },
]

#### 연결: -다면서
groups[u'-다면서'] = [
    { 'rules': [[u'-다면서', '', ''],
                [u'-다며', '', '']],
      'after': ['#형용사', '-으시-', '-었-', '-겠-'],
    },
]

#### 종결: -자고
groups[u'-자고'] = [
    { 'rules': [[u'-자고', '', '']],
      'after': ['#동사'],
    },
]

#### 연결: -기로
groups[u'-기로'] = [
    { 'rules': [[u'-기로', '', ''],
                [u'-키로', u'하', u'하'], # 하기로 -> 키로 준말
                ],
      'after': ['#용언', '#이다', '-'],
      'notafter': ['-더-', '-으리-'],
    },
]

#### 종결: -라, -으라
groups[u'-으라'] = [
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
]

#### 연결: -라고, -으라고
groups[u'-으라고'] = [
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
]

#### 연결: -라는, -으라는 (라고 하는)
groups[u'-으라는'] = [
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
]

#### 연결 -ㄴ데, -은데
groups[u'-은데'] = [
    { 'rules': [[u'-\u11ab데', COND_V_OR_RIEUL, ''],
                [u'-\u11ab데', T_RIEUL, T_RIEUL],
                [u'-은데', COND_T_NOT_RIEUL, '']],
      'after': ['#형용사', '#이다', '-으시-', '-사오-'],
      'notafter': ['있다', '없다'],
      'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙'],
    },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS(u'-은데', ['#형용사']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS(u'-운데', ['#형용사']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS(u'-은데', ['#형용사']),
]
attach_emphasis(groups[u'-은데'], ['도', '요'])

#### 명사형 전성: -기
groups[u'-기'] = [
    { 'rules': [[u'-기', '', '']],
      'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
    },
]
# FIXME: 조사 외에 다른 부분 고려
attach_continuation_flags(groups[u'-기'], [config.josa_flag])

#### 명사형 전성: -음
groups[u'-음'] = [
    { 'rules': [[u'-\u11b7', COND_V_ALL, ''],
                [u'-\u11b7', T_RIEUL, T_RIEUL_MIEUM],
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
    # ㅎ불규칙 TODO: 확인 필요
    HIEUH_IRREGULAR_TYPICAL_CLASS(u'-\u11b7', ['#용언']),
]
# FIXME: 조사 외에 다른 부분 고려
attach_continuation_flags(groups[u'-음'], [config.josa_flag])

#### 종결: -ㄴ다, -는다
groups[u'-는다'] = [
    { 'rules': [[u'-\u11ab다', COND_V_OR_RIEUL, ''],
                [u'-\u11ab다', T_RIEUL, T_RIEUL],
                [u'-는다', COND_T_NOT_RIEUL, '']],
      'after': ['#동사', '-으시-'],
    },
]

#### 연결: -ㄴ다고, -는다고
groups[u'-는다고'] = [
    { 'rules': [[u'-\u11ab다고', COND_V_ALL, ''],
                [u'-\u11ab다고', T_RIEUL, T_RIEUL],
                [u'-는다고', COND_T_NOT_RIEUL, '']],
      'after': ['#동사', '-으시-'],
    },
]

#### 연결: -ㄴ다는, -는다는 (는다고 하는)
groups[u'-는다는'] = [
    { 'rules': [[u'-\u11ab다는', COND_V_ALL, ''],
                [u'-\u11ab다는', T_RIEUL, T_RIEUL],
                [u'-는다는', COND_T_NOT_RIEUL, '']],
      'after': ['#동사', '-으시-'],
    },
]

#### 연결: -ㄴ다면, -는다면
groups[u'-는다면'] = [
    { 'rules': [[u'-\u11ab다면', COND_V_ALL, ''],
                [u'-\u11ab다면', T_RIEUL, T_RIEUL],
                [u'-는다면', COND_T_NOT_RIEUL, '']],
      'after': ['#동사', '-으시-'],
    },
]

#### 종결: -는군
groups[u'-는군'] = [
    { 'rules': [[u'-는군', '', '']],
      'after': ['#동사', '-으시-'],
    },
]
attach_emphasis(groups[u'-는군'], ['요'])

#### 종결: -는구나
groups[u'-는구나'] = [
    { 'rules': [[u'-는구나', '', '']],
      'after': ['#동사', '-으시-'],
    },
]

#### 연결, 종결: -는지
groups[u'-는지'] = [
    { 'rules': [[u'-는지', '', '']],
      'after': ['#동사', '있다', '없다', '계시다', '-으시-', '-었-', '-겠-'],
    },
]


#### 연결: -면, -으면
groups[u'-으면'] = [
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
    # ㅎ불규칙 TODO: 확인 필요
    HIEUH_IRREGULAR_TYPICAL_CLASS(u'-면', ['#용언']),
]

#### 연결: -면서, -으면서
# '-으면' 재활용
groups[u'-으면서'] = [k.copy() for k in groups[u'-으면']]
for klass in groups[u'-으면서']:
    new_rule = []
    for r in klass['rules']:
        new_rule.append([r[0] + '서'] + r[1:])
    klass['rules'] = new_rule

#### 연결: -자마자
groups[u'-자마자'] = [
    { 'rules': [[u'-자마자', '', '']],
      'after': ['#동사', '-으시-'],
    },
]

#### 관형사형 전성: -던
groups[u'-던'] = [
    { 'rules': [[u'-던', '', '']],
      'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
    },
]

#### 연결: -ㄴ가, -은가
#### 의문형 종결: -ㄴ가, -은가
groups[u'-은가'] = [
    { 'rules': [[u'-\u11ab가', COND_V_ALL, ''],
                [u'-\u11ab가', T_RIEUL, T_RIEUL],
                [u'-은가', COND_T_NOT_RIEUL, '']],
      'after': ['#형용사', '#이다', '-으시-'],
      'notafter': ['있다', '없다'],
      'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#ㅎ불규칙'],
    },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS(u'-은가', ['#형용사']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS(u'-운가', ['#형용사']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS(u'-은가', ['#형용사']),
    # ㅎ불규칙 TODO: 확인 필요
    HIEUH_IRREGULAR_TYPICAL_CLASS(u'-\u11ab가', ['#형용사']),
]

#### 연결: -니까, -으니까
groups[u'-으니까'] = [
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
    # ㅎ불규칙 TODO: 확인 필요
    HIEUH_IRREGULAR_TYPICAL_CLASS(u'-니까', ['#용언']),
]
attach_emphasis(groups[u'-으니까'], ['요'])

#### 연결: -라면
groups[u'-라면'] = [
    { 'rules': [[u'-라면', '', '']],
      'after': ['#이다', '아니다', '-으시-', '-더-', '-으리-'],
    },
]

#### 연결: -로구나
groups[u'-로구나'] = [
    { 'rules': [[u'-로구나', '', '']],
      'after': ['#이다', '아니다', '-으시-'],
    },
]

#### 연결: -ㄴ지, -은지
groups[u'-은지'] = [
    { 'rules': [[u'-\u11ab지', COND_V_ALL, ''],
                [u'-\u11ab지', T_RIEUL, T_RIEUL],
                [u'-은지', COND_T_NOT_RIEUL, '']],
      'after': ['#형용사', '-으시-'],
      'notafter': ['있다', '없다'],
      'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#ㅎ불규칙'],
    },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS(u'-은지', ['#형용사']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS(u'-운지', ['#형용사']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS(u'-은지', ['#형용사']),
    # ㅎ불규칙 TODO: 확인 필요
    HIEUH_IRREGULAR_TYPICAL_CLASS(u'-\u11ab지', ['#형용사']),
]

#### 종결: -십시오, -으십시오
groups[u'-으십시오'] = [
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
]

#### 연결: -므로, -으므로
groups[u'-으므로'] = [
    { 'rules': [[u'-므로', COND_V_ALL, ''],
                [u'-므로', T_RIEUL, T_RIEUL],
                [u'-으므로', COND_T_NOT_RIEUL, '']],
      'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
      'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙'],
    },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS(u'-으므로', ['#용언']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS(u'-우므로', ['#용언']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS(u'-으므로', ['#용언']),
]

#### 연결: -다고
groups[u'-다고'] = [
    { 'rules': [[u'-다고', '', '']],
      'after': ['#형용사', '-으시-', '-었-', '-겠-'],
    },
]

#### 연결: -다는 (다고 하는)
groups[u'-다는'] = [
    { 'rules': [[u'-다는', '', '']],
      'after': ['#용언', '-으시-', '-었-', '-겠-'],
    },
]

#### 연결: -더라도
groups[u'-더라도'] = [
    { 'rules': [[u'-더라도', '', '']],
      'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
    },
]

#### 연결: -러, -으러
groups[u'-으러'] = [
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
]

#### 종결: -네
groups[u'-네'] = [
    { 'rules': [[u'-네', '', '']],
      'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
    },
]
attach_emphasis(groups[u'-네'], ['요'])

#### 종결: -니, -으니
#### 연결: -니, -으니
groups[u'-으니'] = [
    { 'rules': [[u'-니', COND_V_ALL, ''],
                [u'-니', T_RIEUL, T_RIEUL],
                [u'-으니', COND_T_NOT_RIEUL, '']],
      'after': ['#용언', '#이다', '-으시-', '-오-', '-더-'],
      'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#ㅎ불규칙'],
    },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS(u'-으니', ['#용언']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS(u'-우니', ['#용언']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS(u'-으니', ['#용언']),
    # ㅎ불규칙 TODO: 확인 필요
    HIEUH_IRREGULAR_TYPICAL_CLASS(u'-니', ['#용언']),
]

#### 의문형 종결: -니 (위와 구별된다)
groups[u'-니?'] = [
    { 'rules': [[u'-니', '[^%s]' % T_RIEUL, ''],
                [u'-니', T_RIEUL, T_RIEUL]],
      'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
    },
]

# #### 의문형 종결: -으니 (구어체)
# groups[u'-으니?'] = [
#     { 'rules': [[u'-으니', COND_T_NOT_RIEUL, '']],
#       'after': ['#형용사'],
#     },
# ]

#### 종결: -군
groups[u'-군'] = [
    { 'rules': [[u'-군', '', '']],
      'after': ['#형용사', '#이다', '-으시-', '-었-', '-겠-', '-더-'],
    },
]
attach_emphasis(groups[u'-군'], ['요'])

#### 종결: -구나
groups[u'-구나'] = [
    { 'rules': [[u'-구나', '', '']],
      'after': ['#형용사', '#이다', '-으시-', '-었-', '-겠-'],
    },
]

#### 종결: -으냐 (형용사)
groups[u'-으냐'] = [
    { 'rules': [[u'-냐', COND_V_ALL, ''],
                [u'-냐', T_RIEUL, T_RIEUL],
                [u'-으냐', COND_T_NOT_RIEUL, '']],
      'after': ['#형용사', '#이다', '-으시-', '-었-', '-겠-'],
      'notafter': ['있다', '없다'],
      'notcond': ['#ㄷ불규칙', '#ㅂ불규칙', '#ㅅ불규칙', '#ㅎ불규칙'],
    },
    # ㄷ불규칙
    TIKEUT_IRREGULAR_TYPICAL_CLASS(u'-으냐', ['#형용사']),
    # ㅂ불규칙
    PIEUP_IRREGULAR_TYPICAL_CLASS(u'-우냐', ['#형용사']),
    # ㅅ불규칙
    SIOS_IRREGULAR_TYPICAL_CLASS(u'-으냐', ['#형용사']),
    # ㅎ불규칙 TODO: 확인 필요
    HIEUH_IRREGULAR_TYPICAL_CLASS(u'-냐', ['#형용사']),
]

#### 종결: -느냐 (동사)
groups[u'-느냐'] = [
    { 'rules': [[u'-느냐', '', '']],
      'after': ['#동사', '있다', '없다', '계시다', '-으시-', '-었-', '-겠-'],
    },
]

#### 연결: -느니
#### 종결: -느니
groups[u'-느니'] = [
    { 'rules': [[u'-느니', '', '']],
      'after': ['#동사', '있다', '없다', '계시다', '-으시-', '-었-', '-겠-'],
    },
]
attach_emphasis(groups[u'-느니'], ['만'])

#### 연결: -되
groups[u'-되'] = [
    { 'rules': [[u'-되', '', '']],
      'after': ['#용언', '#이다', '-으시-'],
    },
]

