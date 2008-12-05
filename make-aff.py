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

if len(sys.argv) != 2:
    sys.stderr.write('Usage: %s flagfile.py\n')
    sys.exit(1)
flaginfo_filename = sys.argv[1]

## 

def nfd(u8str):
    return unicodedata.normalize('NFD', u8str.decode('UTF-8')).encode('UTF-8')
def nfc(u8str):
    return unicodedata.normalize('NFC', u8str.decode('UTF-8')).encode('UTF-8')

def out(u8str):
    return sys.stdout.write(u8str)

def outnfd(u8str):
    return sys.stdout.write(nfd(u8str))

## 모든 자음, 모음
## 간략하게 하기 위해 중세국어는 제외
all_leading = ''.join(map(unichr, range(0x1100,0x1112+1)))
all_vowel = ''.join(map(unichr, range(0x1161,0x1175+1)))
all_trailing = ''.join(map(unichr, range(0x11a8,0x11c2+1)))

from config import header
from config import version

## 헤더 정보
out(header)
out('VERSION hunspell-ko-dict %s\n' % version)
out('SET UTF-8\n')
out('LANG ko\n')
out('FLAG num\n')

## WORDCHARS
out('WORDCHARS 0123456789\n')

## TRY - 빈도가 높은 글자를 앞에 쓸 수록 처리 속도 향상
trychars = u'\u110b\u1161\u1175\u11ab\u1100\u1109\u1173\u1169\u11bc\u110c\u1165\u116e\u1103\u11af\u1112\u1107\u11a8\u1162\u1105\u1102\u1106\u1166\u1167\u110e\u11b7\u1110\u116a\u1111\u11b8\u116d\u1172\u110f\u1174\u116f\u116c\u11bb\u11ba\u1163\u1101\u1171\u1168\u1104\u11c0\u110a\u11b9\u11bd\u11ae\u11ad\u11c1\u110d\u116b\u11c2\u11be\u1108\u11b0\u1170\u11b1\u11b2\u11a9\u11b6\u11ac\u1164\u11aa\u11b3\u11b4\u11b5\u11bf'
out('TRY %s\n' % trychars)

print "ICONV 11172"
for k in range(0xac00, 0xd7a3 + 1):
    print "ICONV %s %s" % (unichr(k), unicodedata.normalize("NFD", unichr(k)))

print "OCONV 11172"
for k in range(0xac00, 0xd7a3 + 1):
    print "OCONV %s %s" % (unicodedata.normalize("NFD", unichr(k)), unichr(k))

## KEY - 두벌식 키보드 배치


cond_all = '.'
# 모음
cond_vowel = '[%s]' % all_vowel
# 받침
cond_trailing = '[%s]' % all_trailing
# 모음 + ㄹ받침
cond_vowel_r = '[%s]' % (all_vowel + u'\u11af')
# ㄹ 제외한 받침
cond_trailing_r = '[%s]' % all_trailing.replace(u'\u11af', '')

## 숫자+단위

from config import digit_flag
from config import counter_flag

out('COMPOUNDMIN 1\n')
out('ONLYINCOMPOUND %d\n' % counter_flag)
out('COMPOUNDRULE 1\n')
out('COMPOUNDRULE (%d)*(%d)(%d)\n' % (digit_flag, digit_flag, counter_flag))


## 어미

from config import endings_flag_start

all_vowel_ao = all_vowel.replace(u'\u1161', '').replace(u'\u1169', '')
cond_not_ao = ['[%s]' % all_vowel_ao,
               '[%s][%s]' % (all_vowel_ao, all_trailing)]
cond_ao = ['[%s]' % u'\u1161\u1169',
           '[%s][%s]' % (u'\u1161\u1169', all_trailing)]
endings = [
    ## '-다'
    { 'id': 0,
      'name': '-다', 'cond': '.',
      'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
    },
    ## '-는'
    { 'id': 1,
      'name': '-는', 'cond': '.',
      'after': ['#동사', '있다', '없다', '계시다', '-으시-', '-겠-'],
    },
    ## '-(으)시-'
    # TODO: 계시다,모시다 + -시- 금지
    # TODO: 불규칙
    { 'id': 2,
      'name': '-시-', 'cond': cond_vowel,
      'after': ['#용언', '#이다'],
    },
    { 'id': 2,
      'name': '-으시-', 'cond': cond_trailing_r,
      'after': ['#용언'],
    },
    ## '-겠-'
    { 'id': 3,
      'name': '-겠-', 'cond': '.',
      'after': ['#용언', '#이다', '-으시-', '-었-'],
    },
    ## '-게'
    { 'id': 4,
      'name': '-게', 'cond': '.',
      'after': ['#용언', '-으시-'],
    },
    { 'id': 4,
      'name': '-게도', 'cond': '.',
      'after': ['#용언', '-으시-'],
    },
    { 'id': 4,
      'name': '-게는', 'cond': '.',
      'after': ['#용언', '-으시-'],
    },
    ## '-었-'
    { 'id': 5,
      'name': '-었-', 'cond': cond_not_ao,
      'after': ['#용언', '#이다'],
    },
    { 'id': 5,
      'name': '-았-', 'cond': [u'\u1169',
                               '[%s][%s]' % (u'\u1161\u1169', all_trailing)],
      'after': ['#용언'],
    },
    { 'id': 5,
      # 'ㅏ'+'았': ㅏ 생략
      'name': u'-\u1161\u11bb-', 'cond': u'\u1161', 'strip': u'\u1161',
      'after': ['#용언'],
    },
# TODO ㅗ 았 -> 왔
#    { 'id': 5,
#      'name': u'-\u116a\u11bb-', 'cond': u'\u1169', 'strip': u'\u1169',
#      'after': ['#용언'],
#    },
    ## '-(ㄹ)지라도', '-을지라도'
    { 'id': 6,
      'name': u'-\u11af지라도', 'cond': cond_vowel,
      'after': ['#용언', '#이다', '-으시-'],
    },
    { 'id': 6,
      'name': u'-지라도', 'cond': u'\u11af',
      'after': ['#용언', '-으시-'],
    },
    { 'id': 6,
      'name': u'-을지라도', 'cond': cond_trailing_r,
      'after': ['#용언', '-었-'],
    },
    ## '-ㄹ', '-을'
    { 'id': 7,
      'name': u'-\u11af', 'cond': cond_vowel,
      'after': ['#용언', '#이다', '-으시-', '-시오-'],
    },
    { 'id': 7,
      'name': u'-\u11af', 'cond': u'\u11af', 'strip': u'\u11af',
      'after': ['#용언'],
    },
    { 'id': 7,
      'name': u'-을', 'cond': cond_trailing_r,
      'after': ['#용언', '-었-'],
    },
    ##
    { 'id': 8,
      'name': u'-다가', 'cond': '.',
      'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
    },
    ## '-ㄴ'
    # TODO: 불규칙
    { 'id': 9,
      'name': u'-\u11ab', 'cond': cond_vowel,
      'after': ['#동사', '#이다', '#형용사', '-으시-'],
    },
    { 'id': 9,
      'name': u'-\u11ab', 'cond': u'\u11af', 'strip': u'\u11af',
      'after': ['#동사', '#형용사'],
    },
    { 'id': 9,
      'name': u'-은', 'cond': cond_trailing_r,
      'after': ['#동사', '#형용사'],
    },
    ##
    { 'id': 10,
      'name': u'-지', 'cond': '.',
      'after': ['#용언', '-으시-'],
    },
    ##
    { 'id': 11,
      'name': u'-며', 'cond': cond_vowel_r,
      'after': ['#용언', '#이다', '-으시-'],
    },
    { 'id': 11,
      'name': u'-으며', 'cond': cond_trailing_r,
      'after': ['#용언', '-었-', '-겠-'],
    },
    ## '-ㅂ니다', '-습니다'
    { 'id': 12,
      'name': u'-\u11b8니다', 'cond': cond_vowel,
      'after': ['#용언', '#이다', '-으시-'],
    },
    { 'id': 12,
      'name': u'-\u11b8니다', 'cond': u'\u11af', 'strip': u'\u11af',
      'after': ['#용언'],
    },
    { 'id': 12,
      'name': u'-습니다', 'cond': cond_trailing_r,
      'after': ['#용언', '-었-', '-겠-'],
    },
    ## '-고'
    ## TODO: -으리-, -더- 제외
    { 'id': 13,
      'name': u'-고', 'cond': '.',
      'after': ['#용언', '#이다', '-'],
    },
    ## '-세요', '-으세요'
    { 'id': 14,
      'name': u'-세요', 'cond': cond_vowel,
      'after': ['#용언', '#이다'],
    },
    { 'id': 14,
      'name': u'-세요', 'cond': u'\u11af', 'strip': u'\u11af',
      'after': ['#용언'],
    },
    { 'id': 14,
      'name': u'-으세요', 'cond': cond_trailing_r,
      'after': ['#용언'],
    },
    ## '-면', '-으면'
    { 'id': 15,
      'name': u'-면', 'cond': cond_vowel_r,
      'after': ['#용언', '#이다', '-으시-'],
    },
    { 'id': 15,
      'name': u'-으면', 'cond': cond_trailing_r,
      'after': ['#용언', '-었-', '-겠-'],
    },
    ## '-어서', '-아서',
    { 'id': 16,
      'name': u'-어서', 'cond': cond_not_ao,
      'after': ['#용언'],
    },
    { 'id': 16,
      'name': u'-아서', 'cond': cond_ao,
      'after': ['#용언'],
    },
    ## '-네', '-네요'
    { 'id': 17,
      'name': u'-네', 'cond': '.',
      'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
    },
    { 'id': 17,
      'name': u'-네요', 'cond': '.',
      'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
    },
    ## '-더라도'
    { 'id': 18,
      'name': u'-더라도', 'cond': '.',
      'after': ['#이다', '#용언', '-으시-', '-었-', '-겠-'],
    },
    ## '-ㄴ다는'
    { 'id': 19,
      'name': u'-\u11ab다는', 'cond': cond_vowel,
      'after': ['#동사', '-으시-'],
    },
    { 'id': 19,
      'name': u'-\u11ab다는', 'cond': u'\u11af', 'strip': u'\u11af',
      'after': ['#동사', '-으시-'],
    },
    ## '-다는'
    { 'id': 20,
      'name': u'-다는', 'cond': '.',
      'after': ['#용언', '-으시-', '-었-', '-겠-'],
    },
    ## '-러', '-으러'
    { 'id': 21,
      'name': u'-러', 'cond': cond_vowel_r,
      'after': ['#동사', '-으시-'],
    },
    { 'id': 21,
      'name': u'-으러', 'cond': cond_trailing_r,
      'after': ['#동사', '-으시-'],
    },
    ## '-다고'
    { 'id': 22,
      'name': u'-다고', 'cond': '.',
      'after': ['#형용사', '-으시-', '-었-', '-겠-'],
    },
    ## '-ㄴ다고', '-는다고'
    { 'id': 23,
      'name': u'-\u11ab다고', 'cond': cond_vowel,
      'after': ['#동사', '-으시-'],
    },
    { 'id': 23,
      'name': u'-\u11ab다고', 'cond': u'\u11af', 'strip': u'\u11af',
      'after': ['#동사'],
    },
    { 'id': 23,
      'name': u'-는다고', 'cond': cond_trailing_r,
      'after': ['#동사'],
    },
    ## '-어', '-아'
    # TODO: 불규칙
    { 'id': 24,
      'name': u'-어', 'cond': ['[%s]' % all_vowel_ao.replace(u'\u1165',''),
                               '[%s][%s]' % (all_vowel_ao, all_trailing)],
      'after': ['#용언'],
    },
    { 'id': 24,
      'name': u'-어', 'cond': u'\u1165', 'strip': u'\u1165',
      'after': ['#용언'],
    },
    { 'id': 24,
      'name': u'-아', 'cond': ['[%s]' % u'\u1169',
                               '[%s][%s]' % (u'\u1161\u1169', all_trailing)],
      'after': ['#용언'], 
    },
    # ㅏ 뒤에 -아
    { 'id': 24,
      'name': u'-\u1161', 'cond': '\u1161', 'strip': '\u1161', 
      'after': ['#용언'], 
    },

    ## '-거나'
    { 'id': 25,
      'name': u'-거나', 'cond': '.',
      'after': ['#용언', '-으시-', '-었-', '-겠-', '-옵-', '-으옵-'], 
    },
    ## '-지만', '-지마는'
    { 'id': 26,
      'name': u'-지만', 'cond': '.',
      'after': ['#용언', '-었-', '-겠-'],
    },
    { 'id': 26,
      'name': u'-지마는', 'cond': '.',
      'after': ['#용언', '-었-', '-겠-'],
    },
    ## '-려고', '-으려고'
    # TODO: 불규칙
    { 'id': 27,
      'name': u'-려고', 'cond': cond_vowel_r,
      'after': ['#동사', '-으시-'],
    },
    { 'id': 27,
      'name': u'-으려고', 'cond': cond_trailing_r,
      'after': ['#동사'],
    },
    ## '-도록'
    ## TODO: 일부 형용사
    { 'id': 28,
      'name': u'-도록', 'cond': '.',
      'after': ['#동사', '-으시-'],
    },
    ## '-는데'
    # TODO: 불규칙
    { 'id': 29,
      'name': u'-는데', 'cond': '.',
      'after': ['#동사', '있다', '없다', '계시다',
                '-으시-', '-었-', '-겠-'],
    },
    ## '-ㄹ까', '-을까'
    # TODO: 불규칙
    { 'id': 30,
      'name': u'-\u11af까', 'cond': cond_vowel,
      'after': ['#동사', '-으시-'],
    },
    { 'id': 30,
      'name': u'-\u11af까', 'cond': u'\u11af', 'strip': u'\u11af',
      'after': ['#동사'],
    },
    { 'id': 30,
      'name': u'-을까', 'cond': cond_trailing_r,
      'after': ['#동사', '-었-'],
    },
    { 'id': 30,
      'name': u'-\u11af까요', 'cond': cond_vowel,
      'after': ['#동사', '-으시-'],
    },
    { 'id': 30,
      'name': u'-\u11af까요', 'cond': u'\u11af', 'strip': u'\u11af',
      'after': ['#동사'],
    },
    { 'id': 30,
      'name': u'-을까요', 'cond': cond_trailing_r,
      'after': ['#동사', '-었-'],
    },
    ## '-어요', '-아요'
    ## TODO: ㅏ 뒤에 -아요
    { 'id': 31,
      'name': u'-어요', 'cond': cond_not_ao,
      'after': ['#용언'],
    },
    { 'id': 31,
      'name': u'-아요', 'cond': ['[%s]' % u'\u1169',
                               '[%s][%s]' % (u'\u1161\u1169', all_trailing)],
      'after': ['#용언'], 
    },
    ## '-ㅂ니까', '-습니다'
    { 'id': 32,
      'name': u'-\u11b8니까', 'cond': cond_vowel,
      'after': ['#용언', '#이다', '-으시-'],
    },
    { 'id': 32,
      'name': u'-\u11b8니까', 'cond': u'\u11af', 'strip': u'\u11af',
      'after': ['#용언'],
    },
    { 'id': 32,
      'name': u'-습니까', 'cond': cond_trailing_r,
      'after': ['#용언', '-었-', '-겠-'],
    },
    ## '-히'
    { 'id': 33,
      'name': u'-히', 'cond': '하', 'strip': '하',
      'after': ['#형용사'],
    },
    ## '-어야', '-아야'
    { 'id': 34,
      'name': u'-어야', 'cond': cond_not_ao,
      'after': ['#용언'],
    },
    { 'id': 34,
      'name': u'-아야', 'cond': cond_ao,
      'after': ['#용언'],
    },
    ## '-ㄴ다'
    { 'id': 35,
      'name': u'-\u11ab다', 'cond': cond_vowel,
      'after': ['#동사', '-으시-'],
    },
    { 'id': 35,
      'name': u'-\u11ab다', 'cond': u'\u11af', 'stripo': u'\u11af',
      'after': ['#동사', '-으시-'],
    },
    { 'id': 35,
      'name': u'-는다', 'cond': cond_trailing_r,
      'after': ['#동사'],
    },
    ## '-ㄴ데', '-은데'
    { 'id': 36,
      'name': u'-\u11ab데', 'cond': cond_vowel,
      'after': ['#형용사', '#이다', '-으시-', '-사오-'],
    },
    { 'id': 36,
      'name': u'-\u11ab데', 'cond': u'\u11af', 'strip': u'\u11af',
      'after': ['#형용사'],
    },
    { 'id': 36,
      'name': u'-은데', 'cond': cond_trailing_r,
      'after': ['#형용사'],
    },
    ## '-기' 명사형어미
    { 'id': 37,
      'name': u'-기', 'cond': '.',
      'after': ['#용언', '#이다', '-으시-', '-었-', '-겠-'],
    },
    ## '-(으)면서' 연결어미
    { 'id': 38,
      'name': u'-면서', 'cond': cond_vowel,
      'after': ['#용언', '#이다', '-으시-'],
    },
    { 'id': 38,
      'name': u'-면서', 'cond': '\u11af', 'strip': '\u11af',
      'after': ['#용언', '-으시-'],
    },
    { 'id': 38,
      'name': u'-으면서', 'cond': cond_trailing_r,
      'after': ['#용언', '-었-', '-겠-'],
    },
    ## '-자마자' 연결어미
    { 'id': 39,
      'name': u'-자마자', 'cond': '.',
      'after': ['#동사', '-으시-'],
    },
]

endings_id = {}

for e in endings:
    endings_id[e['name']] = e['id']

def endings_generate():
    # 대충
    result = []
    working = []

    for e in endings:
        start = [a for a in e['after'] if a[0] != '-']
        if len(start) > 0:
            name = e['name']

            entry = {}
            entry['id'] = e['id']
            entry['start'] = start
            entry['cond'] = e['cond']
            entry['name'] = [name]
            if e.has_key('strip'):
                entry['strip'] = e['strip']
            if name[-1] != '-':
                result.append(entry) # 어말어미
            else:
                working.append(entry) # 선어말어미

    while len(working) > 0:
        working_new = []
        for w in working:
            last = w['name'][-1]
            lastid = endings_id[last]
            for e in endings:
                ## 다른 형태의 같은 어미 중 하나만 있어도 결합 (예 -었- vs -았-)
                ids = [endings_id[a] for a in e['after'] if endings_id.has_key(a)]
                if '-' in e['after'] or lastid in ids:
                    # 어미 연결!
                    k = w.copy()
                    k['name'] = k['name'] + [e['name']]
                    if e['name'][-1] != '-':
                        result.append(k.copy()) # 어말어미
                    else:
                        working_new.append(k.copy()) # 선어말어미
        working = working_new

    def suffixcmp(a,b):
        return cmp(a['name'][0],b['name'][0])
    return result

def endings_out(ll):
    keys = set([l['id'] for l in ll])

    for k in keys:
        mm = [l for l in ll if l['id'] == k]

        start = set()
        for l in mm:
            start = start.union(l['start'])
        out('# :%s\n' % ', '.join(["'%s'" % s for s in list(start)]))

        lines = []
        for l in mm:
            cond = l['cond']
            if l.has_key('strip'):
                strip = l['strip']
            else:
                strip = ''
            ending = nfc(''.join([s.replace('-', '') for s in l['name']]))

            if not isinstance(cond, type([])):
                cond = [ cond ]
            for c in cond:
                lines.append('SFX %d %s다 %s %s다\n' % (endings_flag_start + k, strip, ending, c))
        out('SFX %d Y %d\n' % (endings_flag_start + k, len(lines)))
        for line in lines:
            outnfd(line)

ending_list = endings_generate()
endings_out(ending_list)

flaginfo = open(flaginfo_filename, 'w')

def flaginfo_out(ll, filename):
    keys = set(map(lambda l: l['id'], ll))
    flaginfo.write('flaginfo = {\n')
    for k in keys:
        mm = filter(lambda l: l['id'] == k, ll)
        flaginfo.write('  %d: ' % (endings_flag_start + k))
        flaginfo.write(str(mm[0]['start']))
        flaginfo.write(',\n')
    flaginfo.write('}\n')
    
flaginfo_out(ending_list, flaginfo_filename)


## 조사

from config import josa_flag

josas = [('이', cond_trailing),
         ('가',	cond_vowel),
         ('을', cond_trailing),
         ('를', cond_vowel),
         ('과', cond_trailing),
         ('와', cond_vowel),
         ('은', cond_trailing),
         ('는', cond_vowel),
         ('으로', cond_trailing_r),
         ('로', cond_vowel_r),
         ('으로서', cond_trailing_r),
         ('로서', cond_vowel_r),
         ('으로써', cond_trailing_r),
         ('로써', cond_vowel_r),
         ('도', '.'),
         ('부터', '.'),
         ('에', '.'),
         ('에서', '.'),
         ('까지', '.'),
         ('의', '.'),
         ('에게', '.'),
         ('께', '.'),
         ('보다', '.'),
         ('이라', cond_trailing),
         ('라', cond_vowel),
         ('만', '.'),
         ('만이', '.'),
         ('이나', cond_trailing),
         ('나', cond_vowel),
         ('처럼', '.'),
         ('서', '.'),           # '~에서' 준말
         ('마다', '.'),         # 보조사, '모두'
         ('에는', '.'),         # 에+'는' 보조사
         ('엔', '.'),           # '에는' 준말
         ('이라도', cond_trailing),
         ('라도', cond_trailing),
         ('밖에', '.'),
         ('하고', '.'),         # 구어체
         ]

# 주격조사 활용 조사에 덧붙이기
# twofold suffix를 써먹기에는 아깝다
def ida_generate():
    result = []
    working = []

    for e in endings:
        if '#이다' in e['after']:
            if e['name'][-1] != '-':
                result.append(['이', e['name']])
            else:
                working.append(['이', e['name']])

    while len(working) > 0:
        working_new = []
        for w in working:
            last = w[-1]
            for e in endings:
                if last in e['after'] or '-' in e['after']: # 어미 연결!
                    k = w + [e['name']]
                    if e['name'][-1] != '-':
                        result.append(k) # 어말어미
                    else:
                        working_new.append(k) # 선어말어미
        working = working_new

    return [(nfc(''.join(r).replace('-', '')), '.') for r in result]

r = ida_generate()
josas += r


out('# 조사\n')
out('SFX %d Y %d\n' % (josa_flag, len(josas)))

for (suffix,cond) in josas:
    outnfd('SFX %d 0 %s %s\n' % (josa_flag, suffix, cond))

