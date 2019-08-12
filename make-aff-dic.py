# aff/dic output

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
# Portions created by the Initial Developer are Copyright (C) 2009
# the Initial Developer. All Rights Reserved.
#
# Contributor(s): See CREDITS file
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
import copy
import unicodedata
import yaml

import config
import suffix
import josa
import encoding
import jamo
from flags import *


def ENC(unistr):
    if config.internal_encoding == '2+RST':
        return encoding.encode(unistr)
    else:
        return unicodedata.normalize('NFD', unistr)


def warn(s):
    return sys.stderr.write(s + '\n')


def progress(s):
    return sys.stderr.write('Progress: ' + s + '...\n')


def status(s):
    return sys.stderr.write('Status: ' + s + '...\n')


class Word:
    def __init__(self):
        self.word = ''
        self.pos = ''
        self.pos_detail = ''
        self.props = []
        self.stem = None
        self.pronounce = None

        self.flags = []
        self.flags_alias = -1
        self.morph_alias = -1

    def __hash__(self):
        return (self.word + self.pos).__hash__()

    # set element
    def __eq__(self, other):
        if self.word != other.word:
            return False
        elif self.pos != other.pos:
            return False
        elif sorted(self.props) !=  sorted(other.props):
            return False
        else:
            return True

    # to make it orderable
    def __lt__(self, other):
        if self.word < other.word:
            return True
        if self.pos < other.pos:
            return True
        if sorted(self.props) < sorted(other.props):
            return True
        return False

    def __repr__(self):
        return 'Word %s pos:%s' % (self.word, self.pos)

    def ends_with_vowel(self):
        if self.pronounce:
            lastsyl = self.pronounce[-1]
        else:
            lastsyl = self.word[-1]
        return ENC(lastsyl)[-1] in jamo.V_ALL

    def ends_with_consonant(self):
        return not self.ends_with_vowel()

    def attach_flags(self):
        pos_default_flags = {
            '명사': [substantive_flag, noun_flag],
            '대명사': [substantive_flag, pronoun_flag],
            '수사': [substantive_flag],
            '특수:복수접미사': [substantive_flag, plural_suffix_flag,
                                onlyincompound_flag],
            '특수:알파벳': [alpha_flag],
            '특수:숫자': [digit_flag],
            '특수:금지어': [forbidden_flag],
            '내부:활용:-어': [conjugation_eo_flag, onlyincompound_flag],
            '내부:활용:-은': [conjugation_eun_flag, onlyincompound_flag],
            '내부:활용:-을': [conjugation_eul_flag, onlyincompound_flag],
            '내부:이다:-어': [ida_eo_flag, onlyincompound_flag],
            '내부:이다:-은': [ida_eun_flag, onlyincompound_flag],
            '내부:이다:-을': [ida_eul_flag, onlyincompound_flag],
        }
        try:
            self.flags = pos_default_flags[self.pos]
        except KeyError:
            pass

        pos_detail_default_flags = {
            '명사:의존:단위성': [counter_flag],
        }
        try:
            self.flags += pos_detail_default_flags[self.pos_detail]
        except KeyError:
            pass

        if self.pos in ('명사', '대명사', '수사'):
            if self.ends_with_vowel():
                self.flags += [substantive_v_flag]
                if self.pos == '명사':
                    self.flags += [noun_v_flag]
            else:
                self.flags += [substantive_t_flag]
                if self.pos == '명사':
                    self.flags += [noun_t_flag]
            if self.pos == '대명사':
                if self.word == '너' or self.word == '나':
                    pass
                else:
                    self.flags += [pronoun_plural_flag]

        elif self.pos == '동사' or self.pos == '형용사':
            self.flags += suffix.find_flags(self.word, self.pos, self.props)
        self.flags += josa.find_flags(self.word, self.pos, self.props)

        prop_default_flags = {
            '단위명사': [counter_flag],
            '보조용언:-어': [auxiliary_eo_flag],
            '보조용언:-은': [auxiliary_eun_flag],
            '보조용언:-을': [auxiliary_eul_flag],
            '수:1': [number_1_flag],
            '수:10': [number_10_flag],
            '수:100': [number_100_flag],
            '수:1000': [number_1000_flag],
            '수:10000': [number_10000_flag],
            '고유수:1': [knumber_1_flag],
            '고유수:10': [knumber_10_flag],
        }
        for prop in self.props:
            try:
                self.flags += prop_default_flags[prop]
            except KeyError:
                pass
        self.flags.sort()


class Dictionary:
    def __init__(self):
        self.words = set()
        self.flag_aliases = []
        self.morph_aliases = []

    def add(self, word):
        self.words.add(word)

    def remove(self, word):
        self.words.remove(word)

    def append(self, words):
        for w in words:
            self.words.add(w)

    def load_yaml(self, infile):
        d = yaml.load(infile, Loader=yaml.FullLoader)
        for entry in d['entries']:
            w = Word()
            w.word = entry['word']
            w.pos_detail = entry['pos']

            base = w.pos_detail.split(':')[0]
            if base == '특수':
                w.pos = w.pos_detail
            else:
                w.pos = base

            if 'props' in entry:
                w.props = entry['props']
            if 'stem' in entry:
                w.stem = entry['stem']
            if 'pronounce' in entry:
                w.pronounce = entry['pronounce']
            self.add(w)

    def process(self):
        progress('중복 제거')
        self.remove_duplicates()
        status('중복 제거 후 단어 수: %d' % len(self.words))
        if config.expand_auxiliary_attached:
            progress('플래그 계산')
            self.attach_flags()
            progress('보조용언 확장')
            self.expand_auxiliary()
        else:
            progress('보조용언 확장')
            self.expand_auxiliary()
            progress('플래그 계산')
            self.attach_flags()
        if config.output_word_morph:
            self.attach_morph()

    def output(self, afffile, dicfile):
        progress('dic 출력')
        self.output_dic(dicfile)
        progress('aff 출력')
        self.output_aff(afffile)

    ######################################################################

    def output_dic(self, outfile):
        outfile.write('%d\n' % len(self.words))
        lines = []
        for word in self.words:
            line = '%s' % word.word
            if word.flags_alias > 0:
                line += ('/%d' % word.flags_alias)
            if config.output_word_stem:
                if word.stem:
                    line += (' st:%s' % word.stem)
            if config.output_word_morph:
                if word.morph_alias > 0:
                    line += (' %d' % word.morph_alias)
            lines.append(ENC(line))
        lines.sort()
        outfile.write('\n'.join(lines))

    def output_aff(self, outfile):
        from string import Template
        import aff
        template = Template(open('template.aff', encoding='utf-8').read())

        # 주의: flag alias를 변경하므로 get_AF() 앞에 와야 한다.
        suffix_str = aff.get_suffix_defines(self.flag_aliases)
        josa_str = aff.get_josa_defines(self.flag_aliases)
        af_str = self.get_AF()
        am_str = self.get_AM()

        d = {'version': config.version,
             'required_hunspell': '%d.%d.%d' % config.required_hunspell_version,
             'url': 'https://spellcheck-ko.github.io/',
             'CONV': aff.CONV_DEFINES,
             'AF': af_str,
             'AM': am_str,
             'forbidden_flag': str(forbidden_flag),
             'trychars': aff.TRYCHARS,
             'MAP': aff.MAP_DEFINES,
             'REP': aff.REP_DEFINES,
             'onlyincompound_flag': str(onlyincompound_flag),
             'COMPOUNDRULE': aff.COMPOUNDRULE_DEFINES,
             'JOSA': josa_str,
             'SUFFIX': suffix_str, }

        if config.required_hunspell_version < (1, 3, 1):
            d['suggest_settings'] = ''
        else:
            l = ('MAXCPDSUGS 4',
                 'MAXNGRAMSUGS 4',
                 'MAXDIFF 0',
                 'COMPOUNDMORESUFFIXES')
            d['suggest_settings'] = '\n'.join(l)

        outfile.write(template.substitute(d))

    def get_AF(self):
        aliases = self.flag_aliases
        if len(aliases) > 0:
            result = 'AF %d\n' % len(aliases)
            for flags in aliases:
                result += 'AF %s\n' % ','.join('%d' % f for f in flags)
            return result
        else:
            return ''

    def get_AM(self):
        aliases = self.morph_aliases
        if len(aliases) > 0:
            result = 'AM %d\n' % len(aliases)
            for morph in aliases:
                result += 'AM %s\n' % morph
            return result
        else:
            return ''

    ######################################################################

    def attach_flags(self):
        aliases = []
        for word in self.words:
            word.attach_flags()
            if word.flags:
                if word.flags not in aliases:
                    aliases.append(word.flags)
        aliases.sort()
        for word in self.words:
            if word.flags:
                word.flags_alias = aliases.index(word.flags) + 1
        self.flag_aliases = aliases

    def attach_morph(self):
        aliases = []
        for word in self.words:
            morph = ''
            if morph:
                if morph not in aliases:
                    aliases.append(morph)
                word.morph_alias = aliases.index(morph) + 1
        self.morph_aliases = aliases

    def remove_duplicates(self):
        remove_list = []
        for word in self.words:
            if word.pos in ('동사', '형용사'):
                if '보조용언:-어' in word.props:
                    have_aux = True
                    wc = copy.deepcopy(word)
                    wc.props.remove('보조용언:-어')
                elif '보조용언:-은' in word.props:
                    have_aux = True
                    wc = copy.deepcopy(word)
                    wc.props.remove('보조용언:-은')
                elif '보조용언:-을' in word.props:
                    have_aux = True
                    wc = copy.deepcopy(word)
                    wc.props.remove('보조용언:-을')
                else:
                    have_aux = False
                if have_aux and wc in self.words:
                    remove_list.append(wc)

        for word in remove_list:
            self.words.remove(word)

    def expand_auxiliary(self):
        new_words = []
        forms = ['-어', '-은', '-을']
        verbs = [w for w in self.words if w.pos in ['동사', '형용사']]
        for form in forms:
            auxiliaries = [w for w in verbs if ('보조용언:' + form) in w.props]
            for verb in verbs:
                # 본용언이 용언+용언 합성용언이면 붙여 쓸 수 없다
                if '용언합성' in verb.props:
                    continue
                prefixes = suffix.make_conjugations(verb.word,
                                                    verb.pos, verb.props, form)
                if config.expand_auxiliary_attached:
                    for auxiliary in auxiliaries:
                        # 본용언이 해당 보조용언으로 끝나는 합성어인 경우 생략
                        # 예: 다가오다 + 오다 => 다가와오다 (x)
                        if verb.word != auxiliary.word:
                            if verb.word.endswith(auxiliary.word):
                                continue
                        new_props = [p for p in auxiliary.props
                                     if not p.startswith('보조용언:')]
                        for prefix in prefixes:
                            new_word = Word()
                            new_word.word = prefix + auxiliary.word
                            new_word.pos = auxiliary.pos
                            new_word.stem = verb.word
                            new_word.props = new_props
                            new_word.flags = auxiliary.flags
                            new_word.flags_alias = auxiliary.flags_alias
                            new_words.append(new_word)
                else:
                    for prefix in prefixes:
                        new_word = Word()
                        new_word.word = prefix
                        new_word.stem = verb.word
                        new_word.pos = '내부:활용:' + form
                        new_words.append(new_word)
        # 서술격 조사
        new_word = Word()
        new_word.word = '이어'
        new_word.pos = '내부:이다:-어'
        new_word.stem = '이다'
        new_word.props = []
        new_words.append(new_word)
        new_word = Word()
        new_word.word = '이시어'
        new_word.pos = '내부:이다:-어'
        new_word.stem = '이다'
        new_word.props = []
        new_words.append(new_word)
        new_word = Word()
        new_word.word = '이셔'
        new_word.pos = '내부:이다:-어'
        new_word.stem = '이다'
        new_word.props = []
        new_words.append(new_word)
        new_word = Word()
        new_word.word = '인'
        new_word.pos = '내부:이다:-은'
        new_word.stem = '이다'
        new_word.props = []
        new_words.append(new_word)
        new_word = Word()
        new_word.word = '이신'
        new_word.pos = '내부:이다:-은'
        new_word.stem = '이다'
        new_word.props = []
        new_words.append(new_word)
        new_word = Word()
        new_word.word = '일'
        new_word.pos = '내부:이다:-을'
        new_word.stem = '이다'
        new_word.props = []
        new_words.append(new_word)
        new_word = Word()
        new_word.word = '이실'
        new_word.pos = '내부:이다:-을'
        new_word.stem = '이다'
        new_word.props = []
        new_words.append(new_word)

        self.append(new_words)

if __name__ == '__main__':
    afffilename = sys.argv[1]
    dicfilename = sys.argv[2]
    infilenames = sys.argv[3:]
    dic = Dictionary()
    for filename in infilenames:
        if filename.endswith('.yaml'):
            dic.load_yaml(open(filename, encoding='utf-8'))
        else:
            print('ERROR: unknown file type: ' + filename)
            sys.exit(1)
    dic.process()
    dic.output(open(afffilename, 'w', encoding='utf-8'),
               open(dicfilename, 'w', encoding='utf-8'))
