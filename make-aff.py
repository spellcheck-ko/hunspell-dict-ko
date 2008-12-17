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

import sys
import unicodedata

reload(sys)
sys.setdefaultencoding('UTF-8')

#if len(sys.argv) != 2:
#    err('Usage: %s flagfile.py\n')
#    sys.exit(1)

## 

def nfd(u8str):
    return unicodedata.normalize('NFD', u8str.decode('UTF-8')).encode('UTF-8')
def nfc(u8str):
    return unicodedata.normalize('NFC', u8str.decode('UTF-8')).encode('UTF-8')

def out(u8str):
    return sys.stdout.write(u8str)

def outnfd(u8str):
    return sys.stdout.write(nfd(u8str))

def err(u8str):
    return sys.stderr.write(u8str)

## 모든 자음, 모음
## 간략하게 하기 위해 중세국어는 제외
all_leading = ''.join(map(unichr, range(0x1100,0x1112+1)))
all_vowel = ''.join(map(unichr, range(0x1161,0x1175+1)))
all_trailing = ''.join(map(unichr, range(0x11a8,0x11c2+1)))

from config import header
from config import version

## 헤더 정보
out(header)
out('VERSION hunspell-dict-ko %s\n' % version)
out('SET UTF-8\n')
out('LANG ko\n')
out('FLAG num\n')

## WORDCHARS
out('WORDCHARS 0123456789\n')

## TRY - 빈도가 높은 글자를 앞에 쓸 수록 처리 속도 향상
trychars = u'\u110b\u1161\u1175\u11ab\u1100\u1109\u1173\u1169\u11bc\u110c\u1165\u116e\u1103\u11af\u1112\u1107\u11a8\u1162\u1105\u1102\u1106\u1166\u1167\u110e\u11b7\u1110\u116a\u1111\u11b8\u116d\u1172\u110f\u1174\u116f\u116c\u11bb\u11ba\u1163\u1101\u1171\u1168\u1104\u11c0\u110a\u11b9\u11bd\u11ae\u11ad\u11c1\u110d\u116b\u11c2\u11be\u1108\u11b0\u1170\u11b1\u11b2\u11a9\u11b6\u11ac\u1164\u11aa\u11b3\u11b4\u11b5\u11bf'
out('TRY %s\n' % trychars)


def write_conv_table():
    out('ICONV 11172\n')
    for uch in map(unichr, range(0xac00, 0xd7a3 + 1)):
        out('ICONV %s %s\n' % (uch, unicodedata.normalize("NFD", uch)))
    out('OCONV 11172\n')
    for uch in map(unichr, range(0xac00, 0xd7a3 + 1)):
        out('OCONV %s %s\n' % (unicodedata.normalize("NFD", uch), uch))

write_conv_table()



## TODO: KEY - 두벌식 키보드 배치

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

from config import digit_flag
from config import counter_flag
from config import countable_noun_flag
from config import plural_suffix_flag

out('COMPOUNDMIN 1\n')
#out('ONLYINCOMPOUND %d\n' % plural_suffix_flag)
out('COMPOUNDRULE 2\n')
# 숫자+단위
out('COMPOUNDRULE (%d)*(%d)(%d)\n' % (digit_flag, digit_flag, counter_flag))
# 가산명사+'들'
out('COMPOUNDRULE (%d)(%d)\n' % (countable_noun_flag, plural_suffix_flag))
# TODO: 가산명사+(들)끼리

######################################################################

from config import forbidden_flag
out('FORBIDDENWORD %d\n' % forbidden_flag)

######################################################################
## FLAG

## 어미

import suffix

suffix.write_suffixes(sys.stdout)

######################################################################

## 조사

cond_all = '.'
# 모음
cond_vowel = '[%s]' % all_vowel
# 받침
cond_trailing = '[%s]' % all_trailing
# 모음 + ㄹ받침
cond_vowel_r = '[%s]' % (all_vowel + u'\u11af')
# ㄹ 제외한 받침
cond_trailing_r = '[%s]' % all_trailing.replace(u'\u11af', '')

from config import josa_flag

josas = [('이', cond_trailing),
         ('가',	cond_vowel),
         ('을', cond_trailing),
         ('를', cond_vowel),
         ('과', cond_trailing),
         ('와', cond_vowel),
         ('은', cond_trailing),
         ('는', cond_vowel),
         ('으로', cond_trailing_r),
         ('로', cond_vowel_r),
         ('으로서', cond_trailing_r),
         ('로서', cond_vowel_r),
         ('으로써', cond_trailing_r),
         ('로써', cond_vowel_r),
         ('도', '.'),
         ('부터', '.'),
         ('에', '.'),
         ('에서', '.'),
         ('까지', '.'),
         ('의', '.'),
         ('에게', '.'),
         ('께', '.'),
         ('보다', '.'),
         ('이라', cond_trailing),
         ('라', cond_vowel),
         ('이란', cond_trailing),
         ('란', cond_vowel),
         ('만', '.'),
         ('만이', '.'),
         ('이나', cond_trailing),
         ('나', cond_vowel),
         ('처럼', '.'),
         ('서', '.'),           # '~에서' 준말
         ('마다', '.'),         # 보조사, '모두'
         ('에는', '.'),         # 에+'는' 보조사
         ('엔', '.'),           # '에는' 준말
         ('이라도', cond_trailing),
         ('라도', cond_vowel),
         ('밖에', '.'),
         ('하고', '.'),         # 구어체
         ('조차', '.'),
         ('대로', '.'),
# FIXME: -ㄴ 조사를 허용하면 모든 명사에 ㄴ을 허용하게 되어 범위가 너무 넓어진다.
#         (u'\u11ab', cond_vowel), # -ㄴ: '-는' 구어체
         # TODO: -한테 조사는 사람이나 동물 등에만 붙음
         ('한테', '.'),
         ('마저', '.'),
         ('로부터', cond_vowel_r),
         ('으로부터', cond_trailing_r),
         ('이야', cond_trailing), # '-(이)야' 강조
         ('야', cond_vowel),
         ]

# 주격조사 ('이다') 활용을 조사 목록에 덧붙이기
# twofold suffix를 여기에 써먹기에는 아깝다
ida_conjugations = suffix.make_conjugations(u'이다', '이다', [])
# TODO: '-이다' 줄임형  구하기 '-다', '-라는'
josas += [(c, '.') for c in ida_conjugations]

out('SFX %d Y %d\n' % (josa_flag, len(josas)))
for (suffix,cond) in josas:
    outnfd('SFX %d 0 %s %s\n' % (josa_flag, suffix, cond))

