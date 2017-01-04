# Hunspell FLAG management

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


_flags = [
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
    'josa_ida_t',  # 받침으로 시작
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
