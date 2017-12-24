# Hunspell FLAG management

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


_flags = [
    'onlyincompound',
    # 체언
    'substantive',
    'substantive_t',                       # 받침으로 끝나는 체언
    'substantive_v',                       # 모음으로 끝나는 체언
    'substantive_v_not_pronoun_exception', # 모음으로 끝나는 체언 대명사 나/너/저 제외
    # 대명사
    'pronoun',
    'pronoun_plural',                      # '-들'붙을 수 있는 대명사
    'pronoun_exception',                   # 대명사 나/너/저
    # 명사
    'noun',
    'noun_t',              # 받침 있는 명사
    'noun_v',              # 받침 없는 명사
    # 아라비아숫자
    'digit',
    # 단위 명사, 숫자와 붙여 쓸 수 있음
    'counter',
    # '-들'
    'plural_suffix',
    # 규칙의 예외로 금지할 단어
    'forbidden',
    # 영문자 섞어쓰기
    'alpha',
    # "-어" 활용형
    'conjugation_eo',
    # "-어" 뒤에 붙여 쓸 수 있는 보조용언
    'auxiliary_eo',
    # "-은" 활용형
    'conjugation_eun',
    # "-은" 뒤에 붙여 쓸 수 있는 보조용언
    'auxiliary_eun',
    # "-을" 활용형
    'conjugation_eul',
    # "-을" 뒤에 붙여 쓸 수 있는 보조용언
    'auxiliary_eul',
    # 한자어 숫자, 자리수별
    'number_1', 'number_10', 'number_100', 'number_1000', 'number_10000',
    # 우리말 숫자, 자리수별
    'knumber_1', 'knumber_10',
    # 용언 활용
    ('endings', 500),
    # 조사 모음
    ('josas', 100),
    # 서술 조사
    'josa_ida',
    'josa_ida_t',               # 받침으로 시작
    'josa_ida_noun',            # 서술격조사명사형 (이었음)
    'josa_ida_noun_v',          # 서술격조사명사형, 모음 뒤 (였음)
    'ida_eo',
    'ida_eun',
    'ida_eul',
]


def _define_flags():
    count = 1
    for flag in _flags:
        if isinstance(flag, tuple):
            (name, num) = flag
            globals()[name + '_flag_start'] = count
            globals()[name + '_flag_end'] = count + num - 1
            count += num
        else:
            globals()[flag + '_flag'] = count
            count += 1

_define_flags()
