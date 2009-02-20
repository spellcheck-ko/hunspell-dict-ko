# -*- coding: utf-8 -*-
version = '0.1.7'
header = '''\
# This is the affix file of the Korean hunspell dictionary
#
# Automatically generated; do not edit it manually.

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
# Contributor(s):
# Changwoo Ryu
# Namhyung Kim
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

'''

## FLAG management
josa_flag = 1                   # 조사

digit_flag = 2                  # 아라비아숫자
counter_flag = 3                # 숫자와 붙여 쓸 수 있는 의존명사

plural_suffix_flag = 4          # -들
countable_noun_flag = 5         # "-들" 붙일 수 있는 가산명사

forbidden_flag = 6		# 규칙의 예외로 금지할 단어

alpha_flag = 7                  # 영문자 섞어쓰기


eo_flag = 8                     # "-어" 활용형
auxiliary_eo_flag = 9           # "-어" 뒤에 붙여 쓸 수 있는 보조용언

endings_flag_start = 100        # 용언의 어미
