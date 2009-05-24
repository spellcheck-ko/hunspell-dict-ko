# -*- coding: utf-8 -*-

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
# Portions created by the Initial Developer are Copyright (C) 2009
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
from flags import *
from jamo import *
import suffix

import unicodedata

def nfd(u8str):
    return unicodedata.normalize('NFD', u8str.decode('UTF-8')).encode('UTF-8')
def NFD(unistr):
    return unicodedata.normalize('NFD', unistr)
def NFC(unistr):
    return unicodedata.normalize('NFC', unistr)

ALPHA_ALL = ''.join(map(unichr, range(ord('0'),ord('9')+1) + range(ord('a'),ord('z')+1)))

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
         ('로만', COND_V_OR_RIEUL), ('으로만', COND_T_NOT_RIEUL),
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
         ('에게는', COND_ALL),
         ('에게도', COND_ALL),
         ('에게만', COND_ALL),
         ('에게서', COND_ALL),
         ('에게서는', COND_ALL),
         ('에게서도', COND_ALL),
         ('에게서만', COND_ALL),
         ('에는', COND_ALL),         # 에+'는' 보조사
         ('에도', COND_ALL),         # 에+'도' 보조사
         ('에만', COND_ALL),         # 에+'만' 보조사
         ('에서', COND_ALL),
         ('에서는', COND_ALL),       # 에서+'는' 보조사
         ('에서도', COND_ALL),       # 에서+'도' 보조사
         ('에서만', COND_ALL),       # 에서+'만' 보조사
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

def get_rules_string(flagaliases):
    ida_josas = []
    # 주격조사 ('이다') 활용을 조사 목록에 덧붙이기
    # twofold suffix를 여기에 써먹기에는 아깝다
    ida_conjugations = suffix.make_all_conjugations('이다', '이다', [])
    for c in ida_conjugations:
        if flagaliases and '/' in c:
            (word,flags_str) = c.split('/')
            cont_flags = [int(s) for s in flags_str.split(',')]
            if not cont_flags in flagaliases:
                flagaliases.append(cont_flags)
            c = word + '/%d' % (flagaliases.index(cont_flags) + 1)
        if (NFD(c.decode('utf-8'))[:2] == NFD(u'여') or
            NFD(c.decode('utf-8'))[:2] == NFD(u'예')):
            # '이어' -> '여', '이에' => '예' 줄임형은 받침이 있을 경우에만
            ida_josas.append((c, COND_V_ALL))
        else:
            ida_josas.append((c, COND_ALL))
        # '이' 생략
        # TODO: 받침이 앞의 명사에 붙는 경우 허용 여부 (예: "마찬가집니다")
        if NFC(c.decode('utf-8'))[0] == u'이':
            ida_josas.append((NFC(c.decode('utf-8'))[1:], COND_V_ALL))

    result = ['SFX %d Y %d' % (josa_flag, len(josas + ida_josas))]
    for (sfx,cond) in josas + ida_josas:
        result.append(nfd('SFX %d 0 %s %s' % (josa_flag, sfx, cond)))
    return '\n'.join(result)

def find_flags(word, po, props):
    result = []
    for klass in klasses:
        if class_match_word(klass, word, po, props):
            result.append(klass['flag'])
    return result
    
