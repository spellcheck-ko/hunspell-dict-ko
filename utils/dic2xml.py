#!/usr/bin/python
# -*- coding: utf-8 -*-
# XML 변환
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

from datetime import datetime, tzinfo, timedelta

def nfd(u8str):
    return unicodedata.normalize('NFD', u8str.decode('UTF-8')).encode('UTF-8')
def out(u8str):
    return sys.stdout.write(u8str)
def outnfd(u8str):
    return sys.stdout.write(nfd(u8str))
def warn(u8str):
    return sys.stderr.write(u8str + '\n')

class ParseError(Exception):
    pass

class Dictionary:
    def __init__(self):
        self.words = set([])

    def load_file(self, filename):
        errstr_duplicated = '경고: 중복 무시 (바꾸려면 meta:remove로 지우고, 동음이의어는 idno: 값 사용).'
        errstr_notfound = '경고: 해당 단어 없음'
        # read it
        lines = open(filename).readlines()
        for lineno in range(len(lines)):
            line = lines[lineno]
            # comments out
            #line = line.split('#', 1)[0]
            if line[0] == '#':
                continue
            # remove whitespaces
            line = line.strip()
            if line == '':
                continue
            try:
                word = Word(line)
            except ParseError, errstr:
                warn('%s:%d: %s' % (filename, lineno+1, errstr))
                sys.exit(1)
            if word.meta == 'remove':
                if word in self.words:
                    self.remove(word)
                else:
                    warn('%s:%d: %s' % (filename, lineno+1, errstr_notfound))
            elif word in self.words:
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
        file.write('<entries>\n')
        for word in sorted(list(self.words)):
            word.output(file)
        file.write('</entries>\n')

class Word:
    def __init__(self, line):
        self.word = ''
        self.meta = ''
        self.po = ''
        self.pos = ''
        self.idno = 0
        self.st = ''
        self.props = set()
        self.etym = ''
        self.orig = ''
        self.comment = ''

        # parse a dictionary line

        def load_po(self, val):
            self.po = val
            pos_values = {
            'noun': '명사',
            'pronoun': '대명사',
            'verb': '동사',
            'adjective': '형용사',
            'interjection': '감탄사',
            'determiner': '관형사',
            'adverb': '부사',
            'counter': '특수:단위',
            'plural_suffix': '특수:복수접미사',
            'pseudo_alpha': '특수:알파벳',
            'pseudo_digit': '특수:숫자',
            }
            try:
                self.pos = pos_values[val]
            except KeyError:
                raise ParseError, 'Unknown PO "%s"' % val

        def load_idno(self, val):
            self.idno = int(val)
        def load_st(self, val):
            self.st = val
        def load_meta(self, val):
            self.meta = val
            if val == 'forbidden':
                self.pos = '특수:금지어'
        def load_prop(self, val):
            for p in val.split(','):
                self.props.add(p)
        def load_from(self, val):
            self.etym = val
        def load_orig(self, val):
            self.orig = val

        info_load_funcs = { 'po': load_po,
                            'st': load_st,
                            'idno': load_idno,
                            'meta': load_meta,
                            'prop': load_prop,
                            'from': load_from,
                            'orig': load_orig,
                          }

        s = line.split('#', 1)
        if len(s) > 1:
            self.comment = s[1].strip()
        line = s[0]

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

        if self.po == 'verb' and self.word.endswith('가다'):
            self.props.add('거라불규칙')
        if self.po == 'verb' and self.word.endswith('오다'):
            self.props.add('너라불규칙')

        self.verify_props()
                
    def is_forbidden(self):
        return self.meta == 'forbidden'
    def __repr__(self):
        return '%(word)s po:%(po)s prop:%(props)s' % {
            'word': self.word, 'po': self.po, 'props': ','.join(self.props), }
    def __cmp__(self, other):
        n = cmp(self.word, other.word)
        if n != 0:
            return n
        n = cmp(self.po, other.po)
        if n != 0:
            return n
        n = cmp(self.idno, other.idno)
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
             (self.word.endswith('업다') and self.word != '업다') or
             self.word.endswith('스럽다')) and
            (not 'ㅂ불규칙' in self.props)):
            raise ParseError, 'ㅂ불규칙 용언으로 보이지만 속성 없음'

    def output(self, file):
        file.write('<Entry>\n')
        file.write('  <word>%s</word>\n' % self.word)
        if self.pos:
            file.write('  <pos>%s</pos>\n' % self.pos)
        else:
            file.write('  <pos>특수:없음</pos>\n')
        if self.st:
            file.write('  <stem>%s</stem>\n' % self.st)
        if len(self.props) > 0:
            file.write('  <props>')
            for prop in self.props:
                file.write('<prop>%s</prop>' % prop)
            file.write('</props>\n')
        if self.etym:
            file.write('  <from>%s</from>\n' % self.etym)
        if self.orig:
            file.write('  <orig>%s</orig>\n' % self.orig)
        if self.comment:
            file.write('  <comment>%s</comment>\n' % self.comment)
        file.write('</Entry>\n')

if __name__ == '__main__':
    filenames = sys.argv[1:]

    if len(filenames) < 1:
        sys.stderr.write('Usage: %s filenames...' % sys.argv[0])
        sys.exit(1)

    dict = Dictionary()
    for filename in filenames:
        dict.load_file(filename)

    dict.output(sys.stdout)
