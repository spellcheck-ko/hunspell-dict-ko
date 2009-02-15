# -*- coding: utf-8 -*-
# 사전 파일 생성
#
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
# Portions created by the Initial Developer are Copyright (C) 2008
# the Initial Developer. All Rights Reserved.
#
# Contributor(s): Changwoo Ryu <cwryu@debian.org>
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

import sys
import unicodedata

reload(sys)
sys.setdefaultencoding('UTF-8')

def nfd(u8str):
    return unicodedata.normalize('NFD', u8str.decode('UTF-8')).encode('UTF-8')
def out(u8str):
    return sys.stdout.write(u8str)
def outnfd(u8str):
    return sys.stdout.write(nfd(u8str))
def warn(u8str):
    return sys.stderr.write(u8str + '\n')

import config
import suffix

import xml.dom.minidom

class ParseError(Exception):
    pass

class Dictionary:
    def __init__(self):
        self.words = set([])

    def load_file(self, filename):
        doc = xml.dom.minidom.parse(open(filename))
        for node in doc.childNodes[0].childNodes:
            if node.nodeType != node.ELEMENT_NODE:
                continue
            if node.nodeName != 'Entry':
                continue
            tags = node.getElementsByTagName('valid')
            if tags and tags[0].childNodes[0].data == 'True':
                word = Word(node)
                self.add(word)

    def add(self, word):
        self.words.add(word)
    def remove(self, word):
        self.words.remove(word)
    
    def __len__(self):
        return len(self.words)

    def expand(self):
        expanded = []
        # '-어' 활용형 별도 단어로 분리
        for word in self.words:
            if word.pos != '동사' and word.pos != '형용사':
                continue
            expanded += suffix.make_conjugations(unicode(word.word, 'utf-8'),
                                                 word.pos, word.props, u'-어')
        for word in expanded:
            w = Word()
            w.word = word
            w.pos = '내부:활용:-어'
            w.ident = -1
            w.compute_flags()
            self.add(w)

    def output(self, file):
        file.write('%d\n' % len(self))
        for word in sorted(list(self.words)):
            word.output(file)

class Word:
    def __init__(self, node=None):
        self.word = ''
        self.meta = ''
        self.pos = ''
        self.stem = ''
        self.props = set()
        self.flags = []
        self.ident = 0

        if not node:
            return

        # parse a dictionary line

        def load_word(self, val):
            self.word = val.encode('UTF-8')
        def load_pos(self, val):
            self.pos = val.encode('UTF-8')
            # default properties
            if val == '동사':
                self.props.add('용언')
                self.props.add('동사')
            elif val == '형용사':
                self.props.add('용언')
                self.props.add('형용사')
        def load_stem(self, val):
            self.stem = val.encode('UTF-8')
        def load_ident(self, val):
            self.ident = val
        def load_props(self, val):
            for p in val.split(','):
                self.props.add(p.encode('UTF-8'))

        info_load_funcs = { 'word': load_word,
                            'pos': load_pos,
                            'stem': load_stem,
                            'props': load_props,
                            'ident': load_ident,
                          }

        for field in node.childNodes:
            if field.nodeType != field.ELEMENT_NODE:
                continue
            if len(field.childNodes) <= 0:
                continue
            try:
                fun = info_load_funcs[field.nodeName]
                fun(self, field.childNodes[0].data)
            except KeyError:
                pass

        self.verify_props()
        self.compute_flags()

    def verify_props(self):
        # -답다, -롭다, -업다로 끝나는 용언은 ㅂ불규칙
        if (self.pos == '동사' and self.word.endswith('가다') and
            (not '거라불규칙' in self.props)):
            raise ParseError, '거라불규칙 용언으로 보이지만 속성 없음'
        if (self.pos == '동사' and self.word.endswith('오다') and
            (not '너라불규칙' in self.props)):
            raise ParseError, '너라불규칙 용언으로 보이지만 속성 없음'
        if ((self.pos == '동사' or self.pos == '형용사') and
            (self.word.endswith('답다') or
             self.word.endswith('롭다') or
             (self.word.endswith('업다') and self.word != '업다') or
             self.word.endswith('스럽다')) and
            (not 'ㅂ불규칙' in self.props)):
            raise ParseError, 'ㅂ불규칙 용언으로 보이지만 속성 없음'

    def compute_flags(self):
        default_flags = {
            '명사': [ config.josa_flag ],
            '대명사': [ config.josa_flag ],
            '특수:단위': [ config.josa_flag, config.counter_flag ],
            '특수:복수접미사': [ config.josa_flag, config.plural_suffix_flag ],
            '특수:알파벳': [ config.alpha_flag, config.josa_flag ],
            '특수:숫자': [ config.josa_flag, config.digit_flag ],
            '특수:금지어': [ config.forbidden_flag ],
            '내부:활용:-어': [ config.eo_flag ],
            }
        self.flags = []
                
        try:
            self.flags += default_flags[self.pos]
        except KeyError:
            pass

        if self.pos == '명사' or self.pos == '명사':
            if '가산명사' in self.props:
                self.flags += [ config.countable_noun_flag ]

        if self.pos == '동사' or self.pos == '형용사':
            self.flags += suffix.find_flags(self.word, self.pos, self.props)
            if '보조용언:-어' in self.props:
                self.flags += [ config.auxiliary_eo_flag ]

        self.flags.sort()

    def output(self, file):
        line = self.word
        if self.flags:
            line += '/' + ','.join([('%d' % f) for f in self.flags])
        #if self.pos:
        #    line += ' po:%s' % self.pos
        #if self.stem:
        #    line += ' st:%s' % self.stem
        file.write(nfd(line) + '\n')

    def __cmp__(self, other):
        n = cmp(self.word, other.word)
        if n != 0:
            return n
        n = cmp(self.pos, other.pos)
        if n != 0:
            return n
        n = cmp(self.ident, other.ident)
        if n != 0:
            return n
        return 0
    def __hash__(self):
        return (self.word + self.pos).__hash__()

    def __repr__(self):
        return '%(word)s po:%(po)s prop:%(props)s' % {
            'word': self.word, 'po': self.po, 'props': ','.join(self.props), }

if __name__ == '__main__':
    filenames = sys.argv[1:]

    if len(filenames) < 1:
        sys.stderr.write('Usage: %s filenames...' % sys.argv[0])
        sys.exit(1)

    dict = Dictionary()
    for filename in filenames:
        dict.load_file(filename)

    dict.expand()

    dict.output(sys.stdout)
