# 모든 보조용언에 대해, 앞에 어떤 형태로 붙여 쓰이는지 찾아낸다.

import glob
import sys
import yaml
import re

def process_all(outdir):
    filenames = glob.glob(outdir + '/*/*__보조_*.yaml')
    for filename in filenames:
        process_file(filename)

def process_file(filename):
    k = yaml.load(open(filename).read())
    word = k['import']['한국어기초사전']['표제어']
    clue = k['import']['한국어기초사전']['의미'][0]['의미 참고']
    props = []

    examples = []
    if '뒤에서 ' in clue:
        examples = clue.split('뒤에서 ')[1].split('로 쓴다.')[0].split(', ')
    elif '뒤에 ' in clue:
        examples = clue.split('뒤에 ')[1].split('로 쓴다.')[0].split(', ')

    if examples:
        if len(examples) > 0:
            examples = [k[1:-1] for k in examples]
            for example in examples:
                prefixes = example.split(' ')[0].split('/')
                for prefix in prefixes:
                    if prefix[0] != '-':
                        prefix = '-' + prefix
                    props.append('보조용언:' + prefix)
    else:
        if word == '드리다':
            props.append('보조용언:-어')

    if len(props) == 0:
        print(filename)
        print('*** UNKNOWN:' + clue)
        return

    if '속성' not in k['import_derived']['맞춤법 검사']:
        result_props = k['import_derived']['맞춤법 검사']['속성']
    else:
        result_props = []

    result_props = [k for p in result_props if not k.startswith('보조용언:')]
    result_props += props
    result_props.sort()
    k['import_derived']['맞춤법 검사']['속성'] = result_props

    with open(filename, 'w') as fp:
        fp.write(yaml.dump(k, allow_unicode=True, default_flow_style=False, indent=2))

if __name__ == '__main__':
    outdir = './entries'
    process_all(outdir)
