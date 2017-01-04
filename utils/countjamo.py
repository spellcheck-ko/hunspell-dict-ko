#!/usr/bin/python3
# 표준 입력의 모든 자모 수 세는 유틸리티 (TRY 키워드를 위해)

import sys
import unicodedata

count = [0] * 256

line = sys.stdin.readline()
while line:
    text = unicodedata.normalize("NFD", line)
    for ch in text:
        if ord(ch) >= 0x1100 and ord(ch) <= 0x11FF:
            count[ord(ch) - 0x1100] += 1
    line = sys.stdin.readline()

result = sorted(zip(range(0x1100, 0x1200), count), key=lambda x: -x[1])


def not_old(jamo):
    k = ord(jamo)
    return (((0x1100 <= k) and (k <= 0x1112)) or
            ((0x1161 <= k) and (k <= 0x1175)) or
            ((0x11a8 <= k) and (k <= 0x11c2)))

sys.stdout.write('TRY ')
for (i, c) in result:
    if not_old(chr(i)):
        sys.stdout.write('\\u%04x' % i)
sys.stdout.write('\n')

for (i, c) in result:
    if not_old(chr(i)):
        name = unicodedata.name(chr(i))
        sys.stderr.write('U+%04x: %d (%s)\n' % (i, c, name))
