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
#

import sys
import unicodedata

reload(sys)
sys.setdefaultencoding('UTF-8')

def nfd(u8str):
    return unicodedata.normalize('NFD', u8str.decode('UTF-8')).encode('UTF-8')

def out(u8str):
    return sys.stdout.write(u8str)

filenames = sys.argv[1:]

if len(filenames) < 1:
    print 'Usage: %s filenames...' % sys.argv[0]
    sys.exit(1)

## load

lines = []
for filename in filenames:
    lines += open(filename).readlines()

# comment out
lines = [line.split('#', 1)[0] for line in lines]

# remove whitespaces
lines = [line.strip() for line in lines]

# empty line out
lines = [line for line in lines if line != '']

## 

def make_entry(str):
    d = str.split()
    name = d[0]
    info = {}
    for i in d[1:]:
        try:
            key, val = i.split(':')
        except ValueError:
            sys.stderr.write('make-dic: wrong info "%s"\n' % i)
            raise ValueError
        info[key] = val
    return (name, info)

data = map(make_entry, lines)
def compare_entry(a,b):
    if a[0] != b[0]:
        return cmp(nfd(a[0]), nfd(b[0]))
    try:
        return cmp(a[1]['po'], b[1]['po'])
    except KeyError:
        if b[1].has_key('po'):
            return 1
        elif a[1].has_key('po'):
            return -1
        else:
            return 0
data.sort(compare_entry)

#for i in data:
#    sys.stderr.write('entry: %s, %s\n' % (i[0], str(i[1])))

def remove_duplicates(data):
    i = 0
    try:
        while True:
            if data[i][0] == data[i+1][0]:
                if data[i][1] == data[i+1][1]:
                    del data[i+1]
                # 같은 품사 지우기
                elif (data[i][1].has_key('po') and
                      data[i+1][1].has_key('po') and
                      data[i][1]['po'] == data[i+1][1]['po']):
                    sys.stderr.write('Warning: 삭제 "%s" (%s and %s)\n' % (data[i][0], str(data[i][1]), str(data[i+1][1])))
                    del data[i+1]
                else:
                    #sys.stderr.write('Warning: 유지 "%s" (%s and %s)\n' % (data[i][0], str(data[i][1]), str(data[i+1][1])))
                    i+=1
            else:
                i+=1
    except IndexError:
        pass

remove_duplicates(data)

##

import config
from flaginfo import flaginfo

out('%d\n' % len(data))

def print_entry((name,info)):
    flags = []
    if info.has_key('po'):
        po = info['po']
        if po == 'noun' or po == 'pronoun' or po == 'counter':
            flags.append(config.josa_flag)
            if info.has_key('prop') and '가산명사' in info['prop'].split(','):
                flags.append(config.countable_noun_flag)
        if po == 'digit':
            flags.append(config.digit_flag)
        if po == 'counter':
            flags.append(config.counter_flag)
        if po == 'verb' or po == 'adjective': # temporary
            for flag in flaginfo.keys():
                fi = flaginfo[flag]
                if name in fi:
                    flags.append(flag)
                elif '#용언' in fi:
                    flags.append(flag)
                elif '#동사' in fi and po == 'verb':
                    flags.append(flag)
                elif '#형용사' in fi and po == 'adjective':
                    flags.append(flag)
        if po == 'plural_suffix':
            flags.append(config.josa_flag)
            flags.append(config.plural_suffix_flag)
    else:
        sys.stderr.write('Warning: no info on "%s"\n' % name)

    if len(flags) > 0:
        out('%s/%s\n' % (nfd(name), ','.join(map(str, flags))))
    else:
        out('%s\n' % nfd(name))

map(print_entry, data)
