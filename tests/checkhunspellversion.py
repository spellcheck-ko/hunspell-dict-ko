# check the minimum hunspell version

import os
import re
import subprocess
import sys

def check_version(numbers, required):
    return (numbers[0] > required[0]) or ((numbers[0] == required[0]) and ((numbers[1] >= required[1]) or ((numbers[1] == required[1]) and (numbers[2] >= required[2]))))

def main():
    if os.path.exists('./hunspell'):
        hunspell_cmd = './hunspell'
    else:
        hunspell_cmd = 'hunspell'
    args = [hunspell_cmd, '--version']
    hunspell = subprocess.Popen(args,
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    first_line = hunspell.stdout.readline().decode('UTF-8')
    hunspell.kill()

    m = re.match(r'^.*Hunspell ([0-9\.]+).$', first_line)
    numbers = [int(s) for s in m.group(1).split('.')]
    if len(numbers) >= 3:
        if check_version(numbers, [1, 6, 2]):
            sys.exit(0)
    sys.exit(1)

main()
