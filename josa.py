# josa

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
import encoding
from flags import *
from jamo import *
import suffix

import unicodedata

if config.internal_encoding == '2+RST':
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


def ENC(unistr):
    if config.internal_encoding == '2+RST':
        return encoding.encode(unistr)
    else:
        return unicodedata.normalize('NFD', unistr)


def NFD(unistr):
    return unicodedata.normalize('NFD', unistr)


def NFC(unistr):
    return unicodedata.normalize('NFC', unistr)


ALPHA_ALL = '01234567890abcdefghijklmnopqrstuvwxyz'

#
# 임의로 허용하는 로마자로 된 단어는 음운 구별을 하지 않는다. 할 방법이 없음.
COND_ALL = '.'
if config.internal_encoding == '2+RST':
    COND_V_ALL = '[ㅏㅑㅐㅒㅗㅛㅓㅔㅕㅖㅜㅠㅡㅣ%s]' % (ALPHA_ALL)
    COND_T_ALL = '[ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ%s]' % (ALPHA_ALL)
    COND_V_OR_RIEUL = '[ㅏㅣㅗㅡㅓㅜㅕㅔㅐㅛㅠㅑㅖㅒㄹ%s]' % (ALPHA_ALL)
    COND_T_NOT_RIEUL = '[ㄱㄲㄴㄷㄸㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ%s]' % (ALPHA_ALL)
else:
    COMP_V = 'ㅏㅑㅐㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ'
    COMP_C = 'ㄱㄳㄲㄴㄵㄶㄷㄸㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ'
    COND_V_ALL = '[%s%s%s]' % (V_ALL, COMP_V, ALPHA_ALL)
    COND_T_ALL = '[%s%s%s]' % (T_ALL, COMP_C, ALPHA_ALL)
    COND_V_OR_RIEUL = '[%s%s%s]' % (V_ALL + T_RIEUL, COMP_V + 'ㄹ', ALPHA_ALL)
    COND_T_NOT_RIEUL = '[%s%s%s]' % (T_ALL.replace(T_RIEUL, ''),
                                     COMP_C.replace('ㄹ', ''), ALPHA_ALL)


TRYCHARS = ''


class JosaClass:
    next_flag = josas_flag_start

    def __init__(self, rules=[], after=[], notafter=[]):
        self.rules = rules
        self.after = after
        self.notafter = notafter
        self.flag = JosaClass.next_flag
        JosaClass.next_flag += 1

    def match(self, word, pos, props):
        if self.notafter:
            if (word, '#' + pos) in self.notafter:
                return False
        if self.after:
            if pos == '부사':
                # FIXME - # 부사는 상태부사, 성상부사, 정도부사, 양태부사만 보조사 허용해야 하는데..
                # if pos_detail in ['부사:상태', '부사:성상', '부사:정도', '부사:양태']:
                #     pass
                # else:
                #     return False
                pass

            if pos in ('명사', '대명사', '수사', '특수:숫자',
                       '특수:알파벳', '특수:복수접미사'):
                if '#체언' in self.after:
                    return True

            if ('#' + pos) in self.after:
                return True
            elif (word, '#' + pos) in self.after:
                return True
            else:
                return False
        else:
            return True

    def output(self):
        if len(self.rules) == 0:
            return ''
        result = []
        line = 'SFX %d Y %d' % (self.flag, len(self.rules))
        result.append(line)
        for (sfx, cond, strip) in self.rules:
            if not strip:
                strip = '0'
            if not cond:
                cond = '.'
            line = 'SFX %d %s %s %s' % (self.flag, ENC(strip), ENC(sfx), cond)
            result.append(line)
        return '\n'.join(result)


##
##

groups = {}

#
# '이' 주격/보격 조사
groups['이'] = [
    JosaClass(rules=[('이', COND_T_ALL, '')],
              after=['#체언'],
    ),
    # 대명사 '-것'+'이' -> '게'
    JosaClass(
        rules=[(V_E, ENC('것'), V_EO + T_SIOS)],
        after=['#대명사'],
    ),
]

# '가' 주격/보격 조사
groups['가'] = [
    JosaClass(
        rules=[('가', COND_V_ALL, '')],
        after=['#체언'],
        notafter=[('나', '#대명사'),
                  ('너', '#대명사'),
                  ('저', '#대명사'),
                  ],
    ),
    # 대명사 '나'+'가' -> '내가', '너'+'가' -> '네가', '저'+'가' -> '제가'
    JosaClass(
        rules=[(V_AE + '가', V_A, V_A),
               (V_E + '가', V_EO, V_EO),
               ],
        after=[('나', '#대명사'),
               ('너', '#대명사'),
               ('저', '#대명사'),
               ],
    ),
    # 대명사 '누구'+'가' -> '누가'
    JosaClass(
        rules=[('가', ENC('누구'), '구')],
        after=[('누구', '#대명사')],
    ),
]

groups['!대명사+의'] = [
    # 대명사 '나'+'의' -> '내', '너'+'의' -> '네', '저'+'의' -> '제'
    JosaClass(
        rules=[(V_AE, V_A, V_A),
               (V_E, V_EO, V_EO),
               ],
        after=[('나', '#대명사'),
               ('너', '#대명사'),
               ('저', '#대명사'),
               ],
    ),
]

# 대명사 '나'+'에게' -> '내게', '너'+'에게' -> '네게', '저'+'에게' -> '제게'

_rules=[(V_AE+'게', V_A, V_A),
        (V_E+'게', V_EO, V_EO)]
_suffix_list = ['까지', '는', T_NIEUN,  '나',  '도',  '만',  '서',  '서는',  '서도',  '서만']
_rules_suffix = []
for _suffix in _suffix_list:
    _rules_suffix += [(r[0]+_suffix,r[1],r[2]) for r in _rules]
_rules += _rules_suffix

groups['!대명사+에게'] = [
    # 대명사 '나'+'에게' -> '내게', '너'+'에게' -> '네게', '저'+'에게' -> '제게'
    JosaClass(
        rules=_rules,
        after=[('나', '#대명사'),
               ('너', '#대명사'),
               ('저', '#대명사'),
               ],
    ),
]

# 보조사 붙임


# '-ㄴ', '-ㄹ' 형태로 줄여진 구어체
groups['!종성줄임'] = [
    JosaClass(
        rules=[(T_RIEUL, COND_V_ALL, ''),
               (T_NIEUN, COND_V_ALL, '')],
        after=['#명사', '#대명사'],
    ),
]

# '거'+'로' => '걸로'
groups['!거+로'] = [
    JosaClass(
        rules=[(T_RIEUL + '로' + emph, ENC('거'), '')
               for emph in ['', '는', T_RIEUL, '도',
                            '만',
                            '서', '서는', '선', '서도',
                            '써', '써는', '썬', '써도',
                            '부터', '부터는', '부턴', '부터도']],
        after=[('거', '#대명사'),
               ('그거', '#대명사'),
               ('요거', '#대명사'),
               ('이거', '#대명사'),
               ('저거', '#대명사'),
               ],
    ),
]

# '이서' => '-서'가 숫자 뒤라면 받침이 있을 경우에도 '이서' 형태로 붙을 수 있음
groups['이서'] = [
    JosaClass(
        rules=[('이서', COND_T_ALL, '')],
        after=['#특수:고유수:1']
    ),
]

# 보조사
groups['!보조사'] = [
    JosaClass(
        rules=[('도', COND_ALL, ''),
               ('만', COND_ALL, ''),
               ('은', COND_T_ALL, ''), ('는', COND_V_ALL, ''),
               ('은커녕', COND_T_ALL, ''), ('는커녕', COND_V_ALL, ''),
               ],
        after=['#부사', '#체언'],
    ),
]

groups['*'] = [
    JosaClass(
        rules=[
         ('을', COND_T_ALL, ''), ('를', COND_V_ALL, ''),
         ('과', COND_T_ALL, ''), ('와', COND_V_ALL, ''),
         ('과는', COND_T_ALL, ''), ('와는', COND_V_ALL, ''),
         ('관', COND_T_ALL, ''), ('완', COND_V_ALL, ''),
         ('과도', COND_T_ALL, ''), ('와도', COND_V_ALL, ''),
         ('과의', COND_T_ALL, ''), ('와의', COND_V_ALL, ''),
         ('라', COND_V_ALL, ''), ('이라', COND_T_ALL, ''),
         ('라고', COND_V_ALL, ''), ('이라고', COND_T_ALL, ''),
         ('라는', COND_V_ALL, ''), ('이라는', COND_T_ALL, ''),
         ('라도', COND_V_ALL, ''), ('이라도', COND_T_ALL, ''),
         ('라면', COND_V_ALL, ''), ('이라면', COND_T_ALL, ''),
         ('라서', COND_V_ALL, ''), ('이라서', COND_T_ALL, ''),
         ('란', COND_V_ALL, ''), ('이란', COND_T_ALL, ''),
         ('랑', COND_V_ALL, ''), ('이랑', COND_T_ALL, ''),
         ('로', COND_V_OR_RIEUL, ''), ('으로', COND_T_NOT_RIEUL, ''),
         ('로는', COND_V_OR_RIEUL, ''), ('으로는', COND_T_NOT_RIEUL, ''),
         ('론', COND_V_OR_RIEUL, ''), ('으론', COND_T_NOT_RIEUL, ''),
         ('로의', COND_V_OR_RIEUL, ''), ('으로의', COND_T_NOT_RIEUL, ''),
         ('로도', COND_V_OR_RIEUL, ''), ('으로도', COND_T_NOT_RIEUL, ''),
         ('로만', COND_V_OR_RIEUL, ''), ('으로만', COND_T_NOT_RIEUL, ''),
         ('로밖에', COND_V_OR_RIEUL, ''), ('으로밖에', COND_T_NOT_RIEUL, ''),
         ('로부터', COND_V_OR_RIEUL, ''), ('으로부터', COND_T_NOT_RIEUL, ''),
         ('로부터는', COND_V_OR_RIEUL, ''), ('으로부터는', COND_T_NOT_RIEUL, ''),
         ('로부턴', COND_V_OR_RIEUL, ''), ('으로부턴', COND_T_NOT_RIEUL, ''),
         ('로부터도', COND_V_OR_RIEUL, ''), ('으로부터도', COND_T_NOT_RIEUL, ''),
         ('로부터의', COND_V_OR_RIEUL, ''), ('으로부터의', COND_T_NOT_RIEUL, ''),
         ('로서', COND_V_OR_RIEUL, ''), ('으로서', COND_T_NOT_RIEUL, ''),
         ('로서는', COND_V_OR_RIEUL, ''), ('으로서는', COND_T_NOT_RIEUL, ''),
         ('로선', COND_V_OR_RIEUL, ''), ('으로선', COND_T_NOT_RIEUL, ''),
         ('로서도', COND_V_OR_RIEUL, ''), ('으로서도', COND_T_NOT_RIEUL, ''),
         ('로서의', COND_V_OR_RIEUL, ''), ('으로서의', COND_T_NOT_RIEUL, ''),
         ('로써', COND_V_OR_RIEUL, ''), ('으로써', COND_T_NOT_RIEUL, ''),
         ('로써는', COND_V_OR_RIEUL, ''), ('으로써는', COND_T_NOT_RIEUL, ''),
         ('로썬', COND_V_OR_RIEUL, ''), ('으로썬', COND_T_NOT_RIEUL, ''),
         ('로써도', COND_V_OR_RIEUL, ''), ('으로써도', COND_T_NOT_RIEUL, ''),
         ('야말로', COND_V_ALL, ''), ('이야말로', COND_T_ALL, ''),

         # sorted list
         ('같이', COND_ALL, ''),
         ('까지', COND_ALL, ''),
         ('까지는', COND_ALL, ''),
         ('까진', COND_ALL, ''),
         ('까지도', COND_ALL, ''),
         ('까지만', COND_ALL, ''),
         ('까지라도', COND_ALL, ''),
         ('께', COND_ALL, ''),
         ('께는', COND_ALL, ''),
         ('껜', COND_ALL, ''),
         ('께도', COND_ALL, ''),
         ('께서', COND_ALL, ''),
         ('께서는', COND_ALL, ''),
         ('께선', COND_ALL, ''),
         ('께서도', COND_ALL, ''),
         ('끼리', COND_ALL, ''),         # TODO: -끼리: 가산명사에만 붙음
         ('나', COND_V_ALL, ''),
         ('대로', COND_ALL, ''),
         ('대로는', COND_ALL, ''),
         ('대론', COND_ALL, ''),
         ('대로만', COND_ALL, ''),
         ('대로의', COND_ALL, ''),
         # TODO: -더러 조사는 사람이나 동물 등에만 붙음
         ('더러', COND_ALL, ''),
         ('더러는', COND_ALL, ''),
         ('더러만', COND_ALL, ''),
         ('더런', COND_ALL, ''),
         ('마다', COND_ALL, ''),         # 보조사, '모두'
         ('마저', COND_ALL, ''),
         ('마저도', COND_ALL, ''),
         ('만의', COND_ALL, ''),
         ('만이', COND_ALL, ''),
         ('만큼', COND_ALL, ''),
         ('밖에', COND_ALL, ''),
         ('밖에는', COND_ALL, ''),
         ('밖엔', COND_ALL, ''),
         ('보다', COND_ALL, ''),
         ('보다는', COND_ALL, ''),
         ('보단', COND_ALL, ''),
         ('보다도', COND_ALL, ''),
         ('부터', COND_ALL, ''),
         ('부터는', COND_ALL, ''),
         ('부턴', COND_ALL, ''),
         ('부터라도', COND_ALL, ''),
         ('서', COND_ALL, ''),           # '~에서' 준말
         ('에', COND_ALL, ''),
         ('에게', COND_ALL, ''),
         ('에게까지', COND_ALL, ''),      # + 보조사 추가
         ('에게는', COND_ALL, ''),
         ('에겐', COND_ALL, ''),
         ('에게나', COND_ALL, ''),
         ('에게도', COND_ALL, ''),
         ('에게만', COND_ALL, ''),
         ('에게서', COND_ALL, ''),
         ('에게서는', COND_ALL, ''),
         ('에게서도', COND_ALL, ''),
         ('에게서만', COND_ALL, ''),
         ('에까지', COND_ALL, ''),
         ('에나', COND_ALL, ''),         # 에+'나' 보조사
         ('에는', COND_ALL, ''),         # 에+'는' 보조사
         ('에라도', COND_ALL, ''),       # 에+'라도' 보조사
         ('에야', COND_ALL, ''),         # 에+'야' 보조사
         ('에의', COND_ALL, ''),
         ('엔', COND_ALL, ''),           # '에는' 준말
         ('에나', COND_ALL, ''),         # 에+'나' 보조사
         ('에도', COND_ALL, ''),         # 에+'도' 보조사
         ('에만', COND_ALL, ''),         # 에+'만' 보조사
         ('에서', COND_ALL, ''),
         ('에서는', COND_ALL, ''),       # 에서+'는' 보조사
         ('에선', COND_ALL, ''),
         ('에서도', COND_ALL, ''),       # 에서+'도' 보조사
         ('에서만', COND_ALL, ''),       # 에서+'만' 보조사
         ('야', COND_V_ALL, ''),
         ('의', COND_ALL, ''),
         ('이나', COND_T_ALL, ''),
         ('이든', COND_ALL, ''),
         ('이든지', COND_ALL, ''),
         ('이야', COND_T_ALL, ''),       # '-(이, '')야' 강조
         ('조차', COND_ALL, ''),
         ('조차도', COND_ALL, ''),
         ('처럼', COND_ALL, ''),
         ('처럼은', COND_ALL, ''),
         ('커녕', COND_ALL, ''),
         # TODO: -한테 조사는 사람이나 동물 등에만 붙음
         ('하고', COND_ALL, ''),         # 구어체
         ('한테', COND_ALL, ''),
         ('한테는', COND_ALL, ''),
         ('한텐', COND_ALL, ''),
         ('한테도', COND_ALL, ''),
         ('한테서', COND_ALL, ''),
         ],
        after=['#체언'],
    ),
]

klasses = []

# FIXME: 임시
for _key in groups.keys():
    klasses += groups[_key]


def find_flags(word, pos, props):
    result = []
    for klass in klasses:
        if klass.match(word, pos, props):
            result.append(klass.flag)

    if pos in ('명사', '대명사', '수사', '특수:숫자',
               '특수:알파벳', '특수:복수접미사'):
        result.append(josa_ida_flag)
    if pos == '대명사':
        result.append(josa_ida_t_flag)
    return result


def get_ida_rules(flagaliases):
    ida_josas = []
    ida_josas_t = []
    # 주격조사 ('이다') 활용을 조사 목록에 덧붙이기
    # twofold suffix를 여기에 써먹기에는 아깝다
    ida_conjugations = suffix.make_all_conjugations('이다', '이다', [])
    for c in ida_conjugations:
        if flagaliases and '/' in c:
            (word, flags_str) = c.split('/')
            cont_flags = [int(s) for s in flags_str.split(',')]
            if cont_flags not in flagaliases:
                flagaliases.append(cont_flags)
            c = word + '/%d' % (flagaliases.index(cont_flags) + 1)
        if ENC(c)[:2] in [ENC('여'), ENC('예')]:
            # '이어' -> '여', '이에' => '예' 줄임형은 받침이 있을 경우에만
            ida_josas.append((c, COND_V_ALL))
        else:
            ida_josas.append((c, COND_ALL))
        # '이' 생략
        # TODO: 받침이 앞의 명사에 붙는 경우 허용 여부 (예: "마찬가집니다")
        if config.internal_encoding == '2+RST':
            if c.startswith('이'):
                ida_josas.append((c[1:], COND_V_ALL))
            elif c.startswith(NFD('이')):
                ida_josas_t.append((c[2:], COND_V_ALL))
        else:
            if NFC(c)[0] == '이':
                ida_josas.append((NFC(c)[1:], COND_V_ALL))
            elif NFD(c)[:2] == NFD('이'):
                ida_josas_t.append((NFD(c)[2:], COND_V_ALL))

    result = []
    if len(ida_josas) > 0:
        result.append('# 서술격 조사')
        result.append('SFX %d Y %d' % (josa_ida_flag, len(ida_josas)))
        for (sfx, cond) in ida_josas:
            result.append('SFX %d 0 %s %s' % (josa_ida_flag, ENC(sfx), cond))

    if len(ida_josas_t) > 0:
        result.append('# 서술격 조사 받침 뒤')
        result.append('SFX %d Y %d' % (josa_ida_t_flag, len(ida_josas_t)))
        for (sfx, cond) in ida_josas_t:
            result.append('SFX %d 0 %s %s' % (josa_ida_t_flag, ENC(sfx), cond))
    return result


def get_output(flagaliases):
    result = []
    for klass in klasses:
        result.append(klass.output())
    result += get_ida_rules(flagaliases)
    return '\n'.join(result)
