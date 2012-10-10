#!/usr/bin/python3

import sys
from urllib2 import urlopen, HTTPError

def URL(start):
    return 'http://galkwi.appspot.com/tasks/export/?start=%s' % start

def get(start):
    while True:
        print 'Retrieving words data starting from "%s"...' % start
        try:
            url = urlopen(URL(start))
            n = url.read()
        except HTTPError:
            pass
        else:
            break
    return n

def trim_entries(xml):
    xml = xml[xml.find('<Entry>'):]
    xml = xml[:xml.rfind('</exported-data>')]
    return xml

# NOTE: 다운로드한 데이터 형식을 가정하고 XML 파서를 쓰지 않는다.
def split_last(xml):
    # only <Entry> tags..
    xml = trim_entries(xml)

    # last word
    last = xml[xml.rfind('<word>') + len('<word>'): xml.rfind('</word>')]
    # trim last word data
    output = xml[:xml.find('<Entry>\n<word>%s</word>' % last)]

    return (output, last)

def output_all(outfile):
    outfile.write('<?xml version="1.0" ?>\n')
    outfile.write('<exported-data>\n')
    start = ''
    xml = ''
    while True:
        xml = get(start)
        (output, last) = split_last(xml)
        if (start == last):
            print 'last word %s' % last
            outfile.write(trim_entries(xml))
            break
        else:
            outfile.write(output)
            start = last
    outfile.write('</exported-data>\n')

def output_start(outfile, start):
    xml = get(start)
    outfile.write(xml)

from optparse import OptionParser

parser = OptionParser(usage='usage: %prog [options] outfilename')
parser.add_option("-a", "--all", action="store_true", dest="dump_all")
parser.add_option("-s", "--start", action="store", dest="start_word")

(options, args) = parser.parse_args()

if not options.dump_all and not options.start_word:
    print 'need -a or -s option'
    sys.exit(1)
if len(args) == 0:
    print 'need a output filename'
    sys.exit(1)

outfile = open(args[0], 'w')
if options.dump_all:
    output_all(open(args[0], 'w'))
elif options.start_word:
    output_start(open(args[0], 'w'), options.start_word)
