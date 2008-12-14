# -*- coding: utf-8 -*-
# dictionary generating script
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
from flaginfo import flaginfo

class ParseError(Exception):
    pass

class Dictionary:
    def __init__(self):
        self.words = set([])

    def load_file(self, filename):
        errstr_duplicated = '경고: 중복 단어 무시 (덮어 쓰려면 meta:remove로 지우고 사용).'
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
                if word.meta == 'remove':
                    self.remove(word)
                else:
                    warn('%s:%d: %s' % (filename, lineno+1, errstr_duplicated))
            else:
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

        self.verify_props()
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
        #n = cmp(self.meta, other.meta)
        #if n != 0:
        #    return n
        n = cmp(self.po, other.po)
        if n != 0:
            return n
        return 0
    def __hash__(self):
        return (self.word + self.po).__hash__()

    def verify_props(self):
        # -답다, -롭다, -업다로 끝나는 용언은 ㅂ불규칙
        if ((self.po == 'verb' or self.po == 'adjective') and
            (self.word.endswith('답다') or
             self.word.endswith('롭다') or
             (self.word.endswith('업다') and self.word != '업다')) and
            (not 'ㅂ불규칙' in self.props)):
            raise ParseError, 'ㅂ불규칙 용언으로 보이지만 속성 없음'

    def compute_flags(self):
        meta_default_flags = {
            'forbidden': [ config.forbidden_flag ],
            }

        po_default_flags = {
            'noun': [ config.josa_flag ],
            'pronoun': [ config.josa_flag ],
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

        if self.po == 'noun' or self.po == 'pronoun':
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
