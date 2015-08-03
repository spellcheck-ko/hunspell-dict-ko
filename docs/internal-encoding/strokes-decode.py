#!/usr/bin/python3

import sys
import unicodedata

RESET_CODE = ':'

def stroke_is_c(ch):
    return (ord(ch) >= 0x3131) and (ord(ch) <= 0x314E)

def stroke_is_v(ch):
    return (ord(ch) >= 0x314F) and (ord(ch) <= 0x3163)

LSTROKES2JAMO = {
    'ㄱ': '\u1100',
    'ㄲ': '\u1101',
    'ㄴ': '\u1102',
    'ㄷ': '\u1103',
    'ㄸ': '\u1104',
    'ㄹ': '\u1105',
    'ㅁ': '\u1106',
    'ㅂ': '\u1107',
    'ㅃ': '\u1108',
    'ㅅ': '\u1109',
    'ㅆ': '\u110A',
    'ㅇ': '\u110B',
    'ㅈ': '\u110C',
    'ㅉ': '\u110D',
    'ㅊ': '\u110E',
    'ㅋ': '\u110F',
    'ㅌ': '\u1110',
    'ㅍ': '\u1111',
    'ㅎ': '\u1112',
    }

VSTROKES2JAMO = {
    'ㅏ': '\u1161',
    'ㅐ': '\u1162',
    'ㅑ': '\u1163',
    'ㅒ': '\u1164',
    'ㅓ': '\u1165',
    'ㅔ': '\u1166',
    'ㅕ': '\u1167',
    'ㅖ': '\u1168',
    'ㅗ': '\u1169',
    'ㅗㅏ': '\u116A',
    'ㅗㅐ': '\u116B',
    'ㅗㅣ': '\u116C',
    'ㅛ': '\u116D',
    'ㅜ': '\u116E',
    'ㅜㅓ': '\u116F',
    'ㅜㅔ': '\u1170',
    'ㅜㅣ': '\u1171',
    'ㅠ': '\u1172',
    'ㅡ': '\u1173',
    'ㅡㅣ': '\u1174',
    'ㅣ': '\u1175',
    }

TSTROKES2JAMO = {
    'ㄱ': '\u11A8',
    'ㄲ': '\u11A9',
    'ㄱㅅ': '\u11AA',
    'ㄴ': '\u11AB',
    'ㄴㅈ': '\u11AC',
    'ㄴㅎ': '\u11AD',
    'ㄷ': '\u11AE',
    'ㄹ': '\u11AF',
    'ㄹㄱ': '\u11B0',
    'ㄹㅁ': '\u11B1',
    'ㄹㅂ': '\u11B2',
    'ㄹㅅ': '\u11B3',
    'ㄹㅌ': '\u11B4',
    'ㄹㅍ': '\u11B5',
    'ㄹㅎ': '\u11B6',
    'ㅁ': '\u11B7',
    'ㅂ': '\u11B8',
    'ㅂㅅ': '\u11B9',
    'ㅅ': '\u11BA',
    'ㅆ': '\u11BB',
    'ㅇ': '\u11BC',
    'ㅈ': '\u11BD',
    'ㅊ': '\u11BE',
    'ㅋ': '\u11BF',
    'ㅌ': '\u11C0',
    'ㅍ': '\u11C1',
    'ㅎ': '\u11C2',
}

def compose_syllable(strokes):
    if len(strokes) < 2:
        return ''
    if not stroke_is_c(strokes[0]):
        return ''
    if not stroke_is_v(strokes[1]):
        return ''

    jamo_l = LSTROKES2JAMO[strokes[0]]

    index = 1
    if (len(strokes) >= 3) and (stroke_is_v(strokes[2])):
        if strokes[1:3] in VSTROKES2JAMO:
            jamo_v = VSTROKES2JAMO[strokes[1:3]]
            index = 3
        else:
            return ''
    else:
        jamo_v = VSTROKES2JAMO[strokes[1]]
        index = 2
    if len(strokes) == index:
        return unicodedata.normalize('NFC', jamo_l + jamo_v)
    elif len(strokes) > index and stroke_is_c(strokes[index]):
        if len(strokes) == (index + 1):
            jamo_t = TSTROKES2JAMO[strokes[index]]
            return unicodedata.normalize('NFC', jamo_l + jamo_v + jamo_t)
        elif (len(strokes) == (index + 2)) and (stroke_is_c(strokes[index + 1])):
            if strokes[index:] in TSTROKES2JAMO:
                jamo_t = TSTROKES2JAMO[strokes[index:]]
                return unicodedata.normalize('NFC', jamo_l + jamo_v + jamo_t)
            else:
                return ''
        else:
            return ''
    else:
        return ''
    
def compose_t(strokes):
    if len(strokes) != 2:
        return ''
    table = { 'ㄱㅅ': 'ㄳ', 'ㄴㅈ': 'ㄵ', 'ㄴㅎ': 'ㄶ', 'ㄹㄱ': 'ㄺ',
              'ㄹㅁ': 'ㄻ', 'ㄹㅂ': 'ㄼ', 'ㄹㅅ': 'ㄽ', 'ㄹㅌ': 'ㄾ',
              'ㄹㅍ': 'ㄿ', 'ㄹㅎ': 'ㅀ', 'ㅂㅅ': 'ㅄ' }
    if strokes in table:
        return table[strokes]
    else:
        return ''

def compose_v(strokes):
    if len(strokes) != 2:
        return ''
    table = { 'ㅗㅏ': 'ㅘ', 'ㅗㅐ': 'ㅙ', 'ㅗㅣ': 'ㅚ', 'ㅜㅓ':
              'ㅝ', 'ㅜㅔ': 'ㅞ', 'ㅜㅣ': 'ㅟ', 'ㅢ': 'ㅡㅣ', }
    if strokes in table:
        return table[strokes]
    else:
        return ''

class Decoder:
    def __init__(self):
        self.precompose = ''
        self.prestrokes = ''

    def decode_stroke(self, ch):
        if ch == RESET_CODE:
            out = self.precompose
            self.precompose = ''
            self.prestrokes = ''
            return out
        elif stroke_is_c(ch):
            # 자음
            if self.precompose == '':
                self.precompose = ch
                self.prestrokes = ch
                print('자음 pc: %s' % self.precompose)
                return ''
            elif stroke_is_c(self.prestrokes[-1]):
                if len(self.prestrokes) == 1:
                    out = compose_t(self.prestrokes[-1] + ch)
                    if out:
                        self.prestrokes = ''
                        self.precompose = ''
                        return out
                    else:
                        out = self.precompose
                        self.prestrokes = ch
                        self.precompose = ch
                        return out
                else:
                    syl = compose_syllable(self.prestrokes + ch)
                    if syl:
                        self.prestrokes += ch
                        self.precompose = syl
                        return ''
                    else:
                        out = self.precompose
                        self.prestrokes = ch
                        self.precompose = ch
                        return out
            elif stroke_is_v(self.prestrokes[-1]):
                out = compose_syllable(self.prestrokes + ch)
                if (ch == 'ㄱ') or (ch == 'ㄴ') or (ch == 'ㄹ') or (ch == 'ㅂ'):
                    self.prestrokes += ch
                    self.precompose = out
                    return ''
                else:
                    self.prestrokes = ''
                    self.precompose = ''
                    return out
            else:
                out = self.precompose + ch
                self.precompose = ''
                self.prestrokes = ''
                return out
        elif stroke_is_v(ch):
            if self.precompose == '':
                self.prestrokes = ch
                self.precompose = ch
                return ''
            elif stroke_is_c(self.prestrokes[-1]):
                self.prestrokes += ch
                self.precompose = compose_syllable(self.prestrokes)
                return ''
            elif stroke_is_v(self.prestrokes[-1]):
                out = compose_syllable(self.prestrokes + ch)
                if out:
                    self.prestrokes += ch
                    self.precompose = out
                    return ''
                elif len(self.prestrokes) == 1:
                    out = compose_v(self.prestrokes[-1] + ch)
                    if out:
                        self.prestrokes = ''
                        self.precompose = ''
                        return out
                    else:
                        out = self.precompose
                        self.prestrokes = ch
                        self.precompose = ch
                        return out
                else:
                    out = self.precompose
                    self.prestrokes = ch
                    self.precompose = ch
                    return out
            else:
                out = self.precompose + ch
                self.precompose = ''
                self.prestrokes = ''
                return out
        else:
            out = self.precompose + ch
            self.precompose = ''
            self.prestrokes = ''
            return out

    def decode(self, s):
        result = []
        precompose = ''
        for ch in s:
            o = self.decode_stroke(ch)
            result.append(o)
        print('pc: %s' % self.precompose)
        result.append(self.precompose)
        self.prestrokes = ''
        self.precompose = ''
        return ''.join(result)


decoder = Decoder()
while True:
    line = sys.stdin.readline()
    if not line:
        break
    sys.stdout.write(decoder.decode(line))
        
