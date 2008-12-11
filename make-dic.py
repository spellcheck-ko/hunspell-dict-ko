# -*- coding: utf-8 -*-
# dictionary generating script
#
# Copyright 2008 (C) Changwoo Ryu
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

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
from flaginfo import flaginfo

class ParseError(Exception):
    pass

class Dictionary:
    def __init__(self):
        self.words = set([])

    def load_file(self, filename):
        errstr_duplicated = 'Duplicated. The older one will be overwritten'
        errstr_overwritten = 'The older one'
        # read it
        lines = open(filename).readlines()
        for lineno in range(len(lines)):
            line = lines[lineno]
            # comments out
            line = line.split('#', 1)[0]
            # remove whitespaces
            line = line.strip()
            if line == '':
                continue
            try:
                word = Word(line)
            except ParseError, errstr:
                warn('%s:%d: %s' % (filename, lineno+1, errstr))
                sys.exit(1)
            if word in self.words:
                warn('%s:%d: %s' % (filename, lineno+1, errstr_duplicated))
                self.remove(word)
            self.add(word)

    def add(self, word):
        self.words.add(word)
    def remove(self, word):
        self.words.remove(word)
    
    def __len__(self):
        return len(self.words)

    def output(self, file):
        file.write('%d\n' % len(self))
        for word in sorted(list(self.words)):
            word.output(file)

class Word:
    def __init__(self, line):
        self.word = ''
        self.meta = ''
        self.po = ''
        self.st = ''
        self.props = set()
        self.flags = []

        # parse a dictionary line

        def load_po(self, val):
            self.po = val
            # default properties
            if val == 'verb':
                self.props.add('용언')
                self.props.add('동사')
            elif val == 'adjective':
                self.props.add('용언')
                self.props.add('형용사')
        def load_st(self, val):
            self.st = val
        def load_meta(self, val):
            self.meta = val
        def load_prop(self, val):
            for p in val.split(','):
                self.props.add(p)
        def load_none(self, val):
            pass

        info_load_funcs = { 'po': load_po,
                            'st': load_st,
                            'meta': load_meta,
                            'prop': load_prop,
                            'from': load_none,
                            'orig': load_none,
                          }

        data = line.split()
        self.word, infos = data[0], data[1:]

        for info in infos:
            try:
                key, val = info.split(':')
            except ValueError:
                raise ParseError, 'Wrong information format'
            try:
                info_load_funcs[key](self, val)
            except KeyError:
                raise ParseError, 'Unknown info key "%s"' % key

        self.compute_flags()
                
    def is_forbidden(self):
        return self.meta == 'forbidden'
    def __repr__(self):
        return '%(word)s po:%(po)s prop:%(props)s' % {
            'word': self.word, 'po': self.po, 'props': ','.join(self.props), }
    def __cmp__(self, other):
        n = cmp(self.word, other.word)
        if n != 0:
            return n
        n = cmp(self.meta, other.meta)
        if n != 0:
            return n
        n = cmp(self.po, other.po)
        if n != 0:
            return n
        return 0
    def __hash__(self):
        return (self.word + self.po).__hash__()

    def compute_flags(self):
        meta_default_flags = {
            'forbidden': [ config.forbidden_flag ],
            }

        po_default_flags = {
            'noun': [ config.josa_flag ],
            'digit': [ config.josa_flag, config.digit_flag ],
            'counter': [ config.josa_flag, config.counter_flag ],
            'plural_suffix': [ config.josa_flag, config.plural_suffix_flag ],
            }
        self.flags = []
        try:
            self.flags += meta_default_flags[self.meta]
        except KeyError:
            pass
        try:
            self.flags += po_default_flags[self.po]
        except KeyError:
            pass

        if self.po == 'noun':
            if '가산명사' in self.props:
                self.flags.append(config.countable_noun_flag)

        if self.po == 'verb' or self.po == 'adjective':
            for flag in flaginfo.keys():
                starts = flaginfo[flag][0]
                excepts = flaginfo[flag][1]
                if self.word in excepts:
                    continue
                if self.word in starts:
                    self.flags.append(flag)
                    continue

                # only when one prop is in 'starts' and not in 'excepts'
                for prop in self.props:
                    if ('#'+prop) in starts:
                        break
                else:
                    continue
                for prop in self.props:
                    if ('#'+prop) in excepts:
                        break
                else:
                    self.flags.append(flag)

                

        self.flags.sort()

    def output(self, file):
        line = self.word
        if self.flags:
            line += '/' + ','.join([('%d' % f) for f in self.flags])
        if self.po:
            line += ' po:%s' % self.po
        if self.st:
            line += ' st:%s' % self.st
        file.write(nfd(line) + '\n')

if __name__ == '__main__':
    filenames = sys.argv[1:]

    if len(filenames) < 1:
        sys.stderr.write('Usage: %s filenames...' % sys.argv[0])
        sys.exit(1)

    dict = Dictionary()
    for filename in filenames:
        dict.load_file(filename)

    dict.output(sys.stdout)
