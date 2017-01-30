# Unicode Hangul Jamo utility

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

L_START = 0x1100
L_END = 0x1112
V_START = 0x1161
V_END = 0x1175
T_START = 0x11a8
T_END = 0x11c2

L_ALL = ''.join([chr(c) for c in range(L_START, L_END + 1)])
V_ALL = ''.join([chr(c) for c in range(V_START, V_END + 1)])
T_ALL = ''.join([chr(c) for c in range(T_START, T_END + 1)])

__all__ = ['L_START', 'L_END', 'V_START', 'V_END', 'T_START', 'T_END',
           'L_ALL', 'V_ALL', 'T_ALL']


def define_jamos(jamos, unicodeprefix, prefix):
    import unicodedata
    for jamo in jamos:
        unicodename = unicodedata.name(jamo)
        if not unicodename.startswith(unicodeprefix):
            raise "BUG"
        name = prefix + unicodename[len(unicodeprefix):].replace('-', '_')
        __all__.append(name)
        globals()[name] = jamo

define_jamos(L_ALL, 'HANGUL CHOSEONG ', 'L_')
define_jamos(V_ALL, 'HANGUL JUNGSEONG ', 'V_')
define_jamos(T_ALL, 'HANGUL JONGSEONG ', 'T_')
