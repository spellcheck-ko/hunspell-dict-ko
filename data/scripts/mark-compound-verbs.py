# 2개 이상의 용언으로 구성된 형태 찾아내기

# 보조용언 목록을 미리 만든다

import glob
import sys
import unicodedata
import yaml

L_RIEUL = '\u1105'
V_A = '\u1161'
V_AE = '\u1162'
V_EO = '\u1165'
V_E = '\u1166'
V_EU = '\u1173'
T_KIYEOK = '\u11A8'
T_NIEUN = '\u11AB'
T_TIKEUT = '\u11AE'
T_RIEUL = '\u11AF'
T_PIEUP = '\u11B8'
T_SIOS = '\u11BA'
T_HIEUH = '\u11C2'

def process_all(outdir):
    filenames = glob.glob(outdir + '/*/*__형용사*.yaml')
    filenames += glob.glob(outdir + '/*/*__동사*.yaml')
    for filename in filenames:
        process_file(outdir, filename)

def process_file(outdir, filename):
    k = yaml.load(open(filename).read())
    if  '속성' in k['import_derived']['맞춤법 검사'] and '용언합성' in k['import_derived']['맞춤법 검사']['속성']:
        return
    if check_compounds(k):
        if '속성' not in k['import_derived']['맞춤법 검사']:
            k['import_derived']['맞춤법 검사']['속성'] = []
        k['import_derived']['맞춤법 검사']['속성'].append('용언합성')
        with open(filename, 'w') as fp:
            fp.write(yaml.dump(k, allow_unicode=True, default_flow_style=False, indent=2))

def check_compounds(k):
    word = k['import_derived']['맞춤법 검사']['표제어']
    if len(word) < 4:
        return False
    if word.endswith('가다') or word.endswith('오다') or word.endswith('지다') or word.endswith('보내다') or word.endswith('치다') or word.endswith('놓다') or word.endswith('내다'):
        prefix_nfd = unicodedata.normalize('NFD', word[:-2])
        if prefix_nfd[-1] in [V_A, V_AE, V_E, V_EO]:
            return True
    return False

if __name__ == '__main__':
    outdir = './entries'
    process_all(outdir)
