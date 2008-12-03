#!/usr/bin/env python

import unicodedata
import sys

while True:
    line = sys.stdin.readline()
    if not line:
        break
    line = unicodedata.normalize('NFC', line.decode("UTF-8")).encode("UTF-8")
    sys.stdout.write(line)
