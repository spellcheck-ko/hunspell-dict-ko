#!/usr/bin/python3

import glob
import os
import yaml
import json

def append_entry(entries, yaml):
    entry = {}
    if 'processed' in yaml and '맞춤법 검사' in yaml['processed']:
        entry = yaml['processed']['맞춤법 검사']
    if 'processed_overrides' in yaml and '맞춤법 검사' in yaml['processed_overrides']:
        for key in yaml['processed_overrides']['맞춤법 검사'].keys():
            entry[key] = yaml['processed_overrides']['맞춤법 검사'][key]
    if entry:
        keys = entry.keys()
        REPLACE = {'표제어':'word', '품사':'pos', '속성':'props'}
        e = {}
        for k in keys:
            if k in REPLACE:
                e[REPLACE[k]] = entry[k]
        if 'word' not in e or 'pos' not in e:
            print(entry)
            abort()
        if e['pos'] == '의존 명사':
            e['pos'] = '명사'
        elif e['pos'] == '보조 동사':
            e['pos'] = '동사'
        elif e['pos'] == '보조 형용사':
            e['pos'] = '형용사'
        entries.append(e)

def process_file(filename, entries_ccbysa, entries_mplgpllgpl):
    documents = yaml.load_all(open(filename).read())
    for k in documents:
        license = 'ccbysa'
        if 'imported' in k:
            if '한국어기초사전' in k['imported']:
                license = 'ccbysa'
            if '갈퀴 Django' in k['imported']:
                if k['imported']['갈퀴 Django']['라이선스'] == 'CC BY 4.0':
                    license = 'ccbysa'
                elif  k['imported']['갈퀴 Django']['라이선스'] == 'MPL 1.1/GPL 2.0/LGPL 2.1':
                    license = 'mplgpllgpl'
        if license == 'ccbysa':
            append_entry(entries_ccbysa, k)
        elif license == 'mplgpllgpl':
            append_entry(entries_mplgpllgpl, k)
        else:
            print(k)
            assert()

def output_file(filename, entries):
    entries.sort(key=lambda x : x['word'])
    json_entry = {'entries': entries}
    json.dump(json_entry, open(filename, 'w'), indent=1, ensure_ascii=False)
    print(filename)

def find_and_save(dir, filename_ccbysa, filename_mplgpllgpl):
    yaml_filenames = glob.glob(dir + '/*.yaml')
    entries_ccbysa = []
    entries_mplgpllgpl = []
    print('Total %d files...' % len(yaml_filenames))
    count = 0
    for yaml_filename in yaml_filenames:
        process_file(yaml_filename, entries_ccbysa, entries_mplgpllgpl)
        count += 1
        print('%d...' % count)
    output_file(filename_ccbysa, entries_ccbysa)
    output_file(filename_mplgpllgpl, entries_mplgpllgpl)

if __name__ == '__main__':
    dir = './entries'
    outfile_ccbysa = '../dict-ko-ccbysa.json'
    outfile_mplgpllgpl = '../dict-ko-mplgpllgpl.json'
    find_and_save(dir, outfile_ccbysa, outfile_mplgpllgpl)
