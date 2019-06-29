import glob
import sys
import yaml

def process_file(filename):
    k = yaml.load(open(filename).read())
    if 'processed' not in k:
        k['processed'] = {'사전':{}}
    if 'imported' in k and '한국어기초사전' in k['imported']:
        k['processed']['사전']['원본'] = '한국어기초사전'
        k['processed']['사전']['원본 라이선스'] = 'CC-BY-SA 2.0 KR'
        imported = k['imported']['한국어기초사전']
        if '맞춤법검사' not in k['processed']:
            k['processed']['맞춤법 검사'] = {}
        if imported['품사'] in ['접사','어미','조사']:
            k['processed']['맞춤법 검사'] = {}
        else:
            k['processed']['맞춤법 검사']['표제어'] = imported['표제어']
            k['processed']['맞춤법 검사']['품사'] = imported['품사']
    with open(filename, 'w') as fp:
        fp.write(yaml.dump(k, allow_unicode=True, default_flow_style=False, indent=2))

if __name__ == '__main__':
    for filename in sys.argv:
        process_file(filename)
