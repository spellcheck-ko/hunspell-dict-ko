# -*- coding: utf-8 -*-
version = '0.1.4'
header = '''\
# This is the affix file of the Korean hunspell dictionary
#
# Copyright 2008 (C) Changwoo Ryu
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#
'''

## FLAG management
josa_flag = 1                   # 조사

digit_flag = 2                  # 아라비아숫자
counter_flag = 3                # 숫자와 붙여 쓸 수 있는 의존명사

plural_suffix_flag = 4          # -들
countable_noun_flag = 5         # "-들" 붙일 수 있는 가산명사

forbidden_flag = 6		# 규칙의 예외로 금지할 단어

endings_flag_start = 1000       # 어미
