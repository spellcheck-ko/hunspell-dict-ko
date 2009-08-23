#!/usr/bin/python

import sys
import os
import subprocess

def usage():
    sys.stderr.write('Usage: %s filename\n' % sys.argv[0])

def main():
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)
    filename = sys.argv[1]
    lines = open(filename).read().split('\n')

    if os.path.exists('./hunspell'):
        hunspell_cmd = './hunspell'
    else:
        hunspell_cmd = 'hunspell'
    hunspell = subprocess.Popen([hunspell_cmd, '-d', '../ko'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    hunspell.stdout.readline()  # the first line "Husnpell 1.2.8 ..."
    lineno = 0
    errmsg = sys.stderr.write
    for l in lines:
        lineno += 1
        if not l:               # empty line
            continue
        if l[0] == '#':         # comment
            continue
        tokens = l.split(' ')
        flag = tokens[0]
        word = tokens[1]
        args = tokens[2:]

        hunspell.stdin.write('%s\n' % word)
        result = hunspell.stdout.readline().strip()
        hunspell.stdout.readline() # empty line
        if flag == 'Y' or flag == 'N':
            if ((flag == 'Y' and 
                 result[0] != '*' and result[0] != '+' and result[0] != '-') or
                (flag == 'N' and
                 result[0] != '&' and result[0] != '#')):
                    errmsg('%s:%d: %s %s: %s\n' % (filename, lineno, flag,
                                                   word, result))
                    sys.exit(1)
        elif flag == 'S':
            if result[0] != '&':
                errmsg('%s:%d: %s %s: %s\n' % (filename, lineno, flag,
                                               word, result))
                sys.exit(1)
            else:
                suggests = result[result.find(':')+2:].split(', ')
                if suggests[0] != args[0]:
                    errmsg('%s:%d: %s %s %s: %s\n' % (filename, lineno, flag,
                                                      word, args[0],
                                                      result))
                    sys.exit(1)
        else:
            errmsg('%s:%d: invalid format\n')
    sys.exit(0)

main()
