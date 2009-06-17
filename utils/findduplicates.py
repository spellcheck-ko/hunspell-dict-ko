#!/usr/bin/python
# -*- coding: utf-8 -*-

from lxml import etree
import sys

class Word:
    def __init__(self):
        self.word = ''
        self.pos = ''
        self.props = []
    def __hash__(self):
        return (self.word + self.pos).__hash__()
    def __cmp__(self, other):
        n = cmp(self.word, other.word)
        if n != 0:
            return n
        n = cmp(self.pos, other.pos)
        if n != 0:
            return n
        # FIXME: 이렇게 하면 순서가 다를텐데. set에서 뭐가 먼저 나올지 알고...
        if self.pos == '명사':
            return 0
        for prop in other.props:
            if not prop in self.props:
                return -1
        for prop in self.props:
            if not prop in other.props:
                return 1
        return 0

######################################################################

if len(sys.argv) < 1:
    sys.exit(1)

filename = sys.argv[1]
doc = etree.parse(open(filename))
root = doc.getroot()
wordset = set()
for item in root:
    w = Word()
    for field in item:
        if field.tag == 'word':
            w.word = field.text.encode('UTF-8')
        elif field.tag == 'pos':
            w.pos = field.text.encode('UTF-8')
        elif field.tag == 'props' and field.text:
            w.props = field.text.encode('UTF-8').split(',')
            w.props.sort()
    if w in wordset:
        sys.stderr.write('%s (%s)\n' % (w.word, w.pos))
    else:
        wordset.add(w)
