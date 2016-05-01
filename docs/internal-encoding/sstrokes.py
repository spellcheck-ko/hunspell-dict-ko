#!/usr/bin/python3

import unicodedata

START_CODE = '\uF8FF'           # Unicode PUA code
JAMO2STROKES = {
    '\u1100': 'ㄱ',
    '\u1101': 'ㄲ',
    '\u1102': 'ㄴ',
    '\u1103': 'ㄷ',
    '\u1104': 'ㄸ',
    '\u1105': 'ㄹ',
    '\u1106': 'ㅁ',
    '\u1107': 'ㅂ',
    '\u1108': 'ㅃ',
    '\u1109': 'ㅅ',
    '\u110A': 'ㅆ',
    '\u110B': 'ㅇ',
    '\u110C': 'ㅈ',
    '\u110D': 'ㅉ',
    '\u110E': 'ㅊ',
    '\u110F': 'ㅋ',
    '\u1110': 'ㅌ',
    '\u1111': 'ㅍ',
    '\u1112': 'ㅎ',
    '\u1161': 'ㅏ',
    '\u1162': 'ㅐ',
    '\u1163': 'ㅑ',
    '\u1164': 'ㅒ',
    '\u1165': 'ㅓ',
    '\u1166': 'ㅔ',
    '\u1167': 'ㅕ',
    '\u1168': 'ㅖ',
    '\u1169': 'ㅗ',
    '\u116A': 'ㅗㅏ',
    '\u116B': 'ㅗㅐ',
    '\u116C': 'ㅗㅣ',
    '\u116D': 'ㅛ',
    '\u116E': 'ㅜ',
    '\u116F': 'ㅜㅓ',
    '\u1170': 'ㅜㅔ',
    '\u1171': 'ㅜㅣ',
    '\u1172': 'ㅠ',
    '\u1173': 'ㅡ',
    '\u1174': 'ㅡㅣ',
    '\u1175': 'ㅣ',
    '\u11A8': 'ㄱ',
    '\u11A9': 'ㄲ',
    '\u11AA': 'ㄱㅅ',
    '\u11AB': 'ㄴ',
    '\u11AC': 'ㄴㅈ',
    '\u11AD': 'ㄴㅎ',
    '\u11AE': 'ㄷ',
    '\u11AF': 'ㄹ',
    '\u11B0': 'ㄹㄱ',
    '\u11B1': 'ㄹㅁ',
    '\u11B2': 'ㄹㅂ',
    '\u11B3': 'ㄹㅅ',
    '\u11B4': 'ㄹㅌ',
    '\u11B5': 'ㄹㅍ',
    '\u11B6': 'ㄹㅎ',
    '\u11B7': 'ㅁ',
    '\u11B8': 'ㅂ',
    '\u11B9': 'ㅂㅅ',
    '\u11BA': 'ㅅ',
    '\u11BB': 'ㅆ',
    '\u11BC': 'ㅇ',
    '\u11BD': 'ㅈ',
    '\u11BE': 'ㅊ',
    '\u11BF': 'ㅋ',
    '\u11C0': 'ㅌ',
    '\u11C1': 'ㅍ',
    '\u11C2': 'ㅎ',
}

COMP2STROKES = {
    'ㄳ': 'ㄱㅅ',
    'ㄵ': 'ㄴㅈ',
    'ㄶ': 'ㄴㅎ',
    'ㄺ': 'ㄹㄱ',
    'ㄻ': 'ㄹㅁ',
    'ㄼ': 'ㄹㅂ',
    'ㄽ': 'ㄹㅅ',
    'ㄾ': 'ㄹㅌ',
    'ㄿ': 'ㄹㅍ',
    'ㅀ': 'ㄹㅎ',
    'ㅄ': 'ㅂㅅ',
    'ㅘ': 'ㅗㅏ',
    'ㅙ': 'ㅗㅐ',
    'ㅚ': 'ㅗㅣ',
    'ㅝ': 'ㅜㅓ',
    'ㅞ': 'ㅜㅔ',
    'ㅟ': 'ㅜㅣ',
    'ㅢ': 'ㅡㅣ',
}

rev = []

print('VERSION sstrokes-test 0.1')
print('SET UTF-8')

inlist = []
outlist = []

for c in range(0xAC00, 0xD7A3 + 1):
    jamos = unicodedata.normalize('NFD', chr(c))
    strokes = ''.join([JAMO2STROKES[j] for j in jamos])
    inlist.append((chr(c), strokes))
    outlist.append((strokes, chr(c)))
for c in range(0x3131, 0x3163 + 1):
    if chr(c) in COMP2STROKES:
        strokes = COMP2STROKES[chr(c)]
    else:
        strokes = chr(c)
    inlist.append((chr(c), strokes))
    outlist.append((strokes, chr(c)))

print('ICONV %d' % len(inlist))
for ch, strokes in inlist:
    print('ICONV %s %s%s' % (ch, START_CODE, strokes))

def compare_func(x, y):
    k1 = x[0]
    k2 = y[0]
    if k1 == k2:
        return 0
    elif k1.startswith(k2):
        return -1
    elif k2.startswith(k1):
        return 1
    elif k1.__lt__(k2):
        return -1
    else:
        return 1

def compare_key(mycomp):
    class K(object):
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycomp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycomp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycomp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycomp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycomp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycomp(self.obj, other.obj) != 0
    return K

outlist = sorted(outlist, key=compare_key(compare_func))

print('OCONV %d' % len(outlist))
for strokes, ch in outlist:
    print('OCONV %s%s %s' % (START_CODE, strokes, ch))
print('OCONV %s%s %s' % (START_CODE, START_CODE, START_CODE))
