#!/usr/bin/python3

import sys
import unicodedata

LAST_RESET = 0
LAST_L = 1
LAST_V = 2
LAST_T = 3

RESET_CODE = ':'

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

class Encoder:

    def __init__(self):
        self.state = LAST_RESET
        self.last = ''
        self.result = []

    def encode_compjamo(self, ch):
        result = []
        if (ord(ch) >= 0x3131) and (ord(ch) <= 0x314E):
            # 초성
            if self.state == LAST_V:
                result.append(RESET_CODE)
            self.state = LAST_L
        elif (ord(ch) >= 0x314F) and (ord(ch) <= 0x3163):
            # 중성
            if self.state == LAST_L:
                result.append(RESET_CODE)
            self.state = LAST_V
        else:
            self.state = LAST_RESET
        if ch in COMP2STROKES:
            result.append(COMP2STROKES[ch])
        else:
            result.append(ch)
        return ''.join(result)

    def encode_syllable(self, ch):
        result = []
        jamos = unicodedata.normalize('NFD', ch)
        c = JAMO2STROKES[jamos[0]]
        result.append(c)
        c = JAMO2STROKES[jamos[1]]
        result.append(c)
        if len(jamos) == 2:
            self.state = LAST_V
        else:
            c = JAMO2STROKES[jamos[2]]
            result.append(c)
            self.state = LAST_T
        return ''.join(result)

    def encode(self, s):
        s = unicodedata.normalize('NFC', s)
        outlist = []
        for ch in s:
            if (ord(ch) >= 0xAC00) and (ord(ch) <= 0xD7A3):
                outlist.append(self.encode_syllable(ch))
            elif (ord(ch) >= 0x3131) and (ord(ch) <= 0x3163):
                outlist.append(self.encode_compjamo(ch))
            else:
                self.state = LAST_RESET
                outlist.append(ch)
        return ''.join(outlist)


encoder = Encoder()
while True:
    line = sys.stdin.readline()
    if not line:
        break
    sys.stdout.write(encoder.encode(line))
