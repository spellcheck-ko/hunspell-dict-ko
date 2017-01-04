# Unicode Hangul Jamo utility

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

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
