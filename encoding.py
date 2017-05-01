# Internal encoding conversion

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
# Portions created by the Initial Developer are Copyright (C) 2008, 2009, 2010
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

import unicodedata

RESET_CODE = '\uE000'


class Encoder:
    STATE_INITIAL = 0
    STATE_C = 1
    STATE_V = 2

    JAMO2STROKES = {
        '\u1100': 'ㄱ',
        '\u1101': 'ㄲ',
        '\u1102': 'ㄴ',
        '\u1103': 'ㄷ',
        '\u1104': 'ㄸ',
        '\u1105': 'ㄹ',
        '\u1106': 'ㅁ',
        '\u1107': 'ㅂ',
        '\u1108': 'ㅃ',
        '\u1109': 'ㅅ',
        '\u110A': 'ㅆ',
        '\u110B': 'ㅇ',
        '\u110C': 'ㅈ',
        '\u110D': 'ㅉ',
        '\u110E': 'ㅊ',
        '\u110F': 'ㅋ',
        '\u1110': 'ㅌ',
        '\u1111': 'ㅍ',
        '\u1112': 'ㅎ',
        '\u1161': 'ㅏ',
        '\u1162': 'ㅐ',
        '\u1163': 'ㅑ',
        '\u1164': 'ㅒ',
        '\u1165': 'ㅓ',
        '\u1166': 'ㅔ',
        '\u1167': 'ㅕ',
        '\u1168': 'ㅖ',
        '\u1169': 'ㅗ',
        '\u116A': 'ㅗㅏ',
        '\u116B': 'ㅗㅐ',
        '\u116C': 'ㅗㅣ',
        '\u116D': 'ㅛ',
        '\u116E': 'ㅜ',
        '\u116F': 'ㅜㅓ',
        '\u1170': 'ㅜㅔ',
        '\u1171': 'ㅜㅣ',
        '\u1172': 'ㅠ',
        '\u1173': 'ㅡ',
        '\u1174': 'ㅡㅣ',
        '\u1175': 'ㅣ',
        '\u11A8': 'ㄱ',
        '\u11A9': 'ㄲ',
        '\u11AA': 'ㄱㅅ',
        '\u11AB': 'ㄴ',
        '\u11AC': 'ㄴㅈ',
        '\u11AD': 'ㄴㅎ',
        '\u11AE': 'ㄷ',
        '\u11AF': 'ㄹ',
        '\u11B0': 'ㄹㄱ',
        '\u11B1': 'ㄹㅁ',
        '\u11B2': 'ㄹㅂ',
        '\u11B3': 'ㄹㅅ',
        '\u11B4': 'ㄹㅌ',
        '\u11B5': 'ㄹㅍ',
        '\u11B6': 'ㄹㅎ',
        '\u11B7': 'ㅁ',
        '\u11B8': 'ㅂ',
        '\u11B9': 'ㅂㅅ',
        '\u11BA': 'ㅅ',
        '\u11BB': 'ㅆ',
        '\u11BC': 'ㅇ',
        '\u11BD': 'ㅈ',
        '\u11BE': 'ㅊ',
        '\u11BF': 'ㅋ',
        '\u11C0': 'ㅌ',
        '\u11C1': 'ㅍ',
        '\u11C2': 'ㅎ',
    }

    JAMO2STROKES_ALL = {
        '\u1100': 'ㄱ',
        '\u1101': 'ㄲ',
        '\u1102': 'ㄴ',
        '\u1103': 'ㄷ',
        '\u1104': 'ㄸ',
        '\u1105': 'ㄹ',
        '\u1106': 'ㅁ',
        '\u1107': 'ㅂ',
        '\u1108': 'ㅃ',
        '\u1109': 'ㅅ',
        '\u110A': 'ㅆ',
        '\u110B': 'ㅇ',
        '\u110C': 'ㅈ',
        '\u110D': 'ㅉ',
        '\u110E': 'ㅊ',
        '\u110F': 'ㅋ',
        '\u1110': 'ㅌ',
        '\u1111': 'ㅍ',
        '\u1112': 'ㅎ',
        '\u1113': 'ㄴㄱ',
        '\u1114': 'ㄴㄴ',
        '\u1115': 'ㄴㄷ',
        '\u1116': 'ㄴㅂ',
        '\u1117': 'ㄷㄱ',
        '\u1118': 'ㄹㄴ',
        '\u1119': 'ㄹㄹ',
        '\u111A': 'ㄹㅎ',
        '\u111B': 'ㄹㅇ',
        '\u111C': 'ㅁㅂ',
        '\u111D': 'ㅁㅇ',
        '\u111E': 'ㅂㄱ',
        '\u111F': 'ㅂㄴ',
        '\u1120': 'ㅂㄷ',
        '\u1121': 'ㅂㅅ',
        '\u1122': 'ㅂㅅㄱ',
        '\u1123': 'ㅂㅅㄷ',
        '\u1124': 'ㅂㅅㅂ',
        '\u1125': 'ㅂㅆ',
        '\u1126': 'ㅂㅅㅈ',
        '\u1127': 'ㅂㅈ',
        '\u1128': 'ㅂㅊ',
        '\u1129': 'ㅂㅌ',
        '\u112A': 'ㅂㅍ',
        '\u112B': 'ㅂㅇ',
        '\u112C': 'ㅃㅇ',
        '\u112D': 'ㅅㄱ',
        '\u112E': 'ㅅㄴ',
        '\u112F': 'ㅅㄷ',
        '\u1130': 'ㅅㄹ',
        '\u1131': 'ㅅㅁ',
        '\u1132': 'ㅅㅂ',
        '\u1133': 'ㅅㅂㄱ',
        '\u1134': 'ㅆㅅ',
        '\u1135': 'ㅅㅇ',
        '\u1136': 'ㅅㅈ',
        '\u1137': 'ㅅㅊ',
        '\u1138': 'ㅅㅋ',
        '\u1139': 'ㅅㅌ',
        '\u113A': 'ㅅㅍ',
        '\u113B': 'ㅅㅎ',
        '\u1141': 'ㅇㄱ',
        '\u1142': 'ㅇㄷ',
        '\u1143': 'ㅇㅁ',
        '\u1144': 'ㅇㅂ',
        '\u1145': 'ㅇㅅ',
        '\u1146': 'ㅇㅿ',
        '\u1147': 'ㅇㅇ',
        '\u1148': 'ㅇㅈ',
        '\u1149': 'ㅇㅊ',
        '\u114A': 'ㅇㅌ',
        '\u114B': 'ㅇㅍ',
        '\u114D': 'ㅈㅇ',
        '\u1152': 'ㅊㅋ',
        '\u1153': 'ㅊㅎ',
        '\u1156': 'ㅍㅂ',
        '\u1157': 'ㅍㅇ',
        '\u1156': 'ㅎㅎ',
        '\u115A': 'ㄱㄷ',
        '\u115B': 'ㄴㅅ',
        '\u115C': 'ㄴㅈ',
        '\u115D': 'ㄴㅎ',
        '\u115E': 'ㄷㄹ',

        '\u1161': 'ㅏ',
        '\u1162': 'ㅐ',
        '\u1163': 'ㅑ',
        '\u1164': 'ㅒ',
        '\u1165': 'ㅓ',
        '\u1166': 'ㅔ',
        '\u1167': 'ㅕ',
        '\u1168': 'ㅖ',
        '\u1169': 'ㅗ',
        '\u116A': 'ㅗㅏ',
        '\u116B': 'ㅗㅐ',
        '\u116C': 'ㅗㅣ',
        '\u116D': 'ㅛ',
        '\u116E': 'ㅜ',
        '\u116F': 'ㅜㅓ',
        '\u1170': 'ㅜㅔ',
        '\u1171': 'ㅜㅣ',
        '\u1172': 'ㅠ',
        '\u1173': 'ㅡ',
        '\u1174': 'ㅡㅣ',
        '\u1175': 'ㅣ',
        '\u1176': 'ㅏㅗ',
        '\u1177': 'ㅏㅜ',
        '\u1178': 'ㅑㅗ',
        '\u1179': 'ㅑㅛ',
        '\u117A': 'ㅓㅗ',
        '\u117B': 'ㅓㅜ',
        '\u117C': 'ㅓㅡ',
        '\u117D': 'ㅓㅗ',
        '\u117E': 'ㅕㅜ',
        '\u117F': 'ㅗㅓ',
        '\u1180': 'ㅗㅔ',
        '\u1181': 'ㅗㅖ',
        '\u1182': 'ㅗㅗ',
        '\u1183': 'ㅗㅜ',
        '\u1184': 'ㅛㅑ',
        '\u1185': 'ㅛㅒ',
        '\u1186': 'ㅛㅕ',
        '\u1187': 'ㅛㅗ',
        '\u1188': 'ㅛㅣ',
        '\u1189': 'ㅜㅏ',
        '\u118A': 'ㅜㅐ',
        '\u118B': 'ㅜㅓㅡ',
        '\u118C': 'ㅜㅖ',
        '\u118D': 'ㅜㅜ',
        '\u118E': 'ㅠㅏ',
        '\u118F': 'ㅠㅓ',
        '\u1190': 'ㅠㅔ',
        '\u1191': 'ㅠㅕ',
        '\u1192': 'ㅠㅖ',
        '\u1193': 'ㅠㅜ',
        '\u1194': 'ㅠㅣ',
        '\u1195': 'ㅡㅜ',
        '\u1196': 'ㅡㅡ',
        '\u1197': 'ㅡㅣㅜ',
        '\u1198': 'ㅣㅏ',
        '\u1199': 'ㅣㅑ',
        '\u119A': 'ㅣㅗ',
        '\u119B': 'ㅣㅜ',
        '\u119C': 'ㅣㅡ',
        '\u119D': 'ㅣㆍ',
        '\u119F': 'ㆍㅓ',
        '\u11A0': 'ㆍㅜ',
        '\u11A1': 'ㆍㅣ',
        '\u11A2': 'ㆍㆍ',
        '\u11A3': 'ㅏㅡ',
        '\u11A4': 'ㅑㅜ',
        '\u11A5': 'ㅕㅑ',
        '\u11A6': 'ㅗㅑ',
        '\u11A7': 'ㅗㅒ',

        '\u11A8': 'ㄱ',
        '\u11A9': 'ㄲ',
        '\u11AA': 'ㄱㅅ',
        '\u11AB': 'ㄴ',
        '\u11AC': 'ㄴㅈ',
        '\u11AD': 'ㄴㅎ',
        '\u11AE': 'ㄷ',
        '\u11AF': 'ㄹ',
        '\u11B0': 'ㄹㄱ',
        '\u11B1': 'ㄹㅁ',
        '\u11B2': 'ㄹㅂ',
        '\u11B3': 'ㄹㅅ',
        '\u11B4': 'ㄹㅌ',
        '\u11B5': 'ㄹㅍ',
        '\u11B6': 'ㄹㅎ',
        '\u11B7': 'ㅁ',
        '\u11B8': 'ㅂ',
        '\u11B9': 'ㅂㅅ',
        '\u11BA': 'ㅅ',
        '\u11BB': 'ㅆ',
        '\u11BC': 'ㅇ',
        '\u11BD': 'ㅈ',
        '\u11BE': 'ㅊ',
        '\u11BF': 'ㅋ',
        '\u11C0': 'ㅌ',
        '\u11C1': 'ㅍ',
        '\u11C2': 'ㅎ',
        '\u11C3': 'ㄱㄹ',
        '\u11C4': 'ㄱㅅㄱ',
        '\u11C5': 'ㄴㄱ',
        '\u11C6': 'ㄴㄷ',
        '\u11C7': 'ㄴㅅ',
        '\u11C8': 'ㄴㅿ',
        '\u11C9': 'ㄴㅌ',
        '\u11CA': 'ㄷㄱ',
        '\u11CB': 'ㄷㄹ',
        '\u11CC': 'ㄹㄱㅅ',
        '\u11CD': 'ㄹㄴ',
        '\u11CE': 'ㄹㄷ',
        '\u11CF': 'ㄹㄷㅎ',
        '\u11D0': 'ㄹㄹ',
        '\u11D1': 'ㄹㅁㄱ',
        '\u11D2': 'ㄹㅁㅅ',
        '\u11D3': 'ㄹㅂㅅ',
        '\u11D4': 'ㄹㅂㅎ',
        '\u11D5': 'ㄹㅂㅇ',
        '\u11D6': 'ㄹㅆ',
        '\u11D7': 'ㄹㅿ',
        '\u11D8': 'ㄹㅋ',
        '\u11D9': 'ㄹㆆ',
        '\u11DA': 'ㅁㄱ',
        '\u11DB': 'ㅁㄹ',
        '\u11DC': 'ㅁㅂ',
        '\u11DD': 'ㅁㅅ',
        '\u11DE': 'ㅁㅆ',
        '\u11DF': 'ㅁㅿ',
        '\u11E0': 'ㅁㅊ',
        '\u11E1': 'ㅁㅎ',
        '\u11E2': 'ㅁㅇ',
        '\u11E3': 'ㅂㄹ',
        '\u11E4': 'ㅂㅍ',
        '\u11E5': 'ㅂㅎ',
        '\u11E6': 'ㅂㅇ',
        '\u11E7': 'ㅅㄱ',
        '\u11E8': 'ㅅㄷ',
        '\u11E9': 'ㅅㄹ',
        '\u11EA': 'ㅅㅂ',
        '\u11EC': 'ㅇㄱ',
        '\u11ED': 'ㅇㄲ',
        '\u11EE': 'ㅇㅇ',
        '\u11EF': 'ㅇㅋ',
        '\u11F1': 'ㆁㅅ',
        '\u11F2': 'ㆁㅿ',
        '\u11F3': 'ㅍㅂ',
        '\u11F4': 'ㅍㅇ',
        '\u11F5': 'ㅎㄴ',
        '\u11F6': 'ㅎㄹ',
        '\u11F7': 'ㅎㅁ',
        '\u11F8': 'ㅎㅂ',
        '\u11FA': 'ㄱㄴ',
        '\u11FB': 'ㄱㅂ',
        '\u11FC': 'ㄱㅊ',
        '\u11FD': 'ㄱㅋ',
        '\u11FE': 'ㄱㅎ',
        '\u11FF': 'ㄴㄴ',

        # Hangul Jamo Extended-A
        '\uA960': 'ㄷㅁ',
        '\uA961': 'ㄷㅂ',
        '\uA962': 'ㄷㅅ',
        '\uA963': 'ㄷㅈ',
        '\uA964': 'ㄹㄱ',
        '\uA965': 'ㄹㄲ',
        '\uA966': 'ㄹㄷ',
        '\uA967': 'ㄹㄸ',
        '\uA968': 'ㄹㅁ',
        '\uA969': 'ㄹㅂ',
        '\uA96A': 'ㄹㅃ',
        '\uA96B': 'ㄹㅂㅇ',
        '\uA96C': 'ㄹㅅ',
        '\uA96D': 'ㄹㅈ',
        '\uA96E': 'ㄹㅋ',
        '\uA96F': 'ㅁㄱ',
        '\uA970': 'ㅁㄷ',
        '\uA971': 'ㅁㅅ',
        '\uA972': 'ㅂㅅㅌ',
        '\uA973': 'ㅂㅋ',
        '\uA974': 'ㅂㅎ',
        '\uA975': 'ㅆㅂ',
        '\uA976': 'ㅇㄹ',
        '\uA977': 'ㅇㅎ',
        '\uA978': 'ㅉㅎ',
        '\uA979': 'ㅌㅌ',
        '\uA97A': 'ㅍㅎ',
        '\uA97B': 'ㅎㅅ',
        '\uA97C': 'ㆆㆆ',

        # Hangul Jamo Extended-B
        '\uD7B0': 'ㅗㅕ',
        '\uD7B1': 'ㅗㅗㅣ',
        '\uD7B2': 'ㅛㅏ',
        '\uD7B3': 'ㅛㅐ',
        '\uD7B4': 'ㅛㅓ',
        '\uD7B5': 'ㅜㅕ',
        '\uD7B6': 'ㅜㅣㅣ',
        '\uD7B7': 'ㅜㅐ',
        '\uD7B8': 'ㅠㅗ',
        '\uD7B9': 'ㅡㅏ',
        '\uD7BA': 'ㅡㅓ',
        '\uD7BB': 'ㅡㅔ',
        '\uD7BC': 'ㅡㅗ',
        '\uD7BD': 'ㅣㅑㅗ',
        '\uD7BE': 'ㅣㅒ',
        '\uD7BF': 'ㅣㅕ',
        '\uD7C0': 'ㅣㅖ',
        '\uD7C1': 'ㅣㅗㅣ',
        '\uD7C2': 'ㅣㅛ',
        '\uD7C3': 'ㅣㅠ',
        '\uD7C4': 'ㅣㅣ',
        '\uD7C5': 'ㆍㅏ',
        '\uD7C6': 'ㆍㅔ',

        '\uD7CB': 'ㄴㄹ',
        '\uD7CC': 'ㄴㅊ',
        '\uD7CD': 'ㄸ',
        '\uD7CE': 'ㄸㅂ',
        '\uD7CF': 'ㄷㅂ',
        '\uD7D0': 'ㄷㅅ',
        '\uD7D1': 'ㄷㅅㄱ',
        '\uD7D2': 'ㄷㅈ',
        '\uD7D3': 'ㄷㅊ',
        '\uD7D4': 'ㄷㅌ',
        '\uD7D5': 'ㄹㄲ',
        '\uD7D6': 'ㄹㄱㅎ',
        '\uD7D7': 'ㄹㄹㅋ',
        '\uD7D8': 'ㄹㅁㅎ',
        '\uD7D9': 'ㄹㅂㄷ',
        '\uD7DA': 'ㄹㅂㅍ',
        '\uD7DB': 'ㄹㆁ',
        '\uD7DC': 'ㄹㆆㅎ',
        '\uD7DD': 'ㄹㅇ',
        '\uD7DE': 'ㅁㄴ',
        '\uD7DF': 'ㅁㄴㄴ',
        '\uD7E0': 'ㅁㅁ',
        '\uD7E1': 'ㅁㅂㅅ',
        '\uD7E2': 'ㅁㅈ',
        '\uD7E3': 'ㅂㄷ',
        '\uD7E4': 'ㅂㄹㅍ',
        '\uD7E5': 'ㅂㅁ',
        '\uD7E6': 'ㅃ',
        '\uD7E7': 'ㅂㅅㄷ',
        '\uD7E8': 'ㅂㅈ',
        '\uD7E9': 'ㅂㅊ',
        '\uD7EA': 'ㅅㅁ',
        '\uD7EB': 'ㅅㅂㅇ',
        '\uD7EC': 'ㅆㄱ',
        '\uD7ED': 'ㅆㄷ',
        '\uD7EE': 'ㅅㅿ',
        '\uD7EF': 'ㅅㅈ',
        '\uD7F0': 'ㅅㅊ',
        '\uD7F1': 'ㅅㅌ',
        '\uD7F2': 'ㅅㅎ',
        '\uD7F3': 'ㅿㅂ',
        '\uD7F4': 'ㅿㅂㅇ',
        '\uD7F5': 'ㆁㅁ',
        '\uD7F6': 'ㆁㅎ',
        '\uD7F7': 'ㅈㅂ',
        '\uD7F8': 'ㅈㅃ',
        '\uD7F9': 'ㅉ',
        '\uD7FA': 'ㅍㅅ',
        '\uD7FB': 'ㅍㅌ',
    }

    COMP2STROKES = {
        'ㄳ': 'ㄱㅅ',
        'ㄵ': 'ㄴㅈ',
        'ㄶ': 'ㄴㅎ',
        'ㄺ': 'ㄹㄱ',
        'ㄻ': 'ㄹㅁ',
        'ㄼ': 'ㄹㅂ',
        'ㄽ': 'ㄹㅅ',
        'ㄾ': 'ㄹㅌ',
        'ㄿ': 'ㄹㅍ',
        'ㅀ': 'ㄹㅎ',
        'ㅄ': 'ㅂㅅ',
        'ㅘ': 'ㅗㅏ',
        'ㅙ': 'ㅗㅐ',
        'ㅚ': 'ㅗㅣ',
        'ㅝ': 'ㅜㅓ',
        'ㅞ': 'ㅜㅔ',
        'ㅟ': 'ㅜㅣ',
        'ㅢ': 'ㅡㅣ',

        'ㅥ': 'ㄴㄴ',
        'ㅦ': 'ㄴㄷ',
        'ㅧ': 'ㄴㅅ',
        'ㅨ': 'ㄴㅿ',
        'ㅩ': 'ㄹㄱㅅ',
        'ㅪ': 'ㄹㄷ',
        'ㅫ': 'ㄹㅂㅅ',
        'ㅬ': 'ㄹㅿ',
        'ㅭ': 'ㄹㆆ',
        'ㅮ': 'ㅁㅂ',
        'ㅯ': 'ㅁㅅ',
        'ㅰ': 'ㅇㅇ',
        'ㅱ': 'ㅁㅿ',
        'ㅲ': 'ㅂㄱ',
        'ㅳ': 'ㅂㄷ',
        'ㅴ': 'ㅂㅅㄱ',
        'ㅵ': 'ㅂㅅㄷ',
        'ㅶ': 'ㅂㅈ',
        'ㅷ': 'ㅂㅌ',
        'ㅸ': 'ㅂㅇ',
        'ㅹ': 'ㅃㅇ',
        'ㅺ': 'ㅅㄱ',
        'ㅻ': 'ㅅㄴ',
        'ㅼ': 'ㅅㄷ',
        'ㅽ': 'ㅅㅂ',
        'ㅾ': 'ㅅㅈ',
        'ㅿ': 'ㅿ',
        'ㆀ': 'ㅇㅇ',
        'ㆁ': 'ㆁ',
        'ㆂ': 'ㆁㅅ',
        'ㆃ': 'ㆁㅿ',
        'ㆄ': 'ㅍㅇ',
        'ㆅ': 'ㅎㅎ',
        'ㆆ': 'ㆆㆆ',
        'ㆇ': 'ㅛㅑ',
        'ㆈ': 'ㅛㅒ',
        'ㆉ': 'ㅛㅣ',
        'ㆊ': 'ㅠㅕ',
        'ㆋ': 'ㅠㅖ',
        'ㆌ': 'ㅠㅣ',
        'ㆍ': 'ㆍ',
        'ㆎ': 'ㆍㅣ',
    }

    STROKES2COMP = {
        'ㄱㅅ': 'ㄳ',
        'ㄴㅈ': 'ㄵ',
        'ㄴㅎ': 'ㄶ',
        'ㄹㄱ': 'ㄺ',
        'ㄹㅁ': 'ㄻ',
        'ㄹㅂ': 'ㄼ',
        'ㄹㅅ': 'ㄽ',
        'ㄹㅌ': 'ㄾ',
        'ㄹㅍ': 'ㄿ',
        'ㄹㅎ': 'ㅀ',
        'ㅂㅅ': 'ㅄ',
        'ㅗㅏ': 'ㅘ',
        'ㅗㅐ': 'ㅙ',
        'ㅗㅣ': 'ㅚ',
        'ㅜㅓ': 'ㅝ',
        'ㅜㅔ': 'ㅞ',
        'ㅜㅣ': 'ㅟ',
        'ㅡㅣ': 'ㅢ',
    }

    def __init__(self):
        self.state = Encoder.STATE_INITIAL
        self.last = ''
        self.result = []

    def encode_syllable(self, ch):
        result = []
        jamos = unicodedata.normalize('NFD', ch)
        c = Encoder.JAMO2STROKES[jamos[0]]
        result.append(c)
        c = Encoder.JAMO2STROKES[jamos[1]]
        result.append(c)
        if len(jamos) == 2:
            self.state = Encoder.STATE_V
        else:
            c = Encoder.JAMO2STROKES[jamos[2]]
            result.append(c)
            self.state = Encoder.STATE_C
        self.last = c[-1]
        return ''.join(result)

    def encode_compjamo(self, ch):
        result = []

        is_c = (ord(ch) >= 0x3131) and (ord(ch) <= 0x314E)

        if ch in Encoder.COMP2STROKES:
            s = Encoder.COMP2STROKES[ch]
        else:
            s = ch
        # reset 필요한 경우:
        # (1) 모음 뒤에 자음
        # (2) 자음 뒤에 모음
        # (3) 앞에 글자와 합쳐서 복합 자음 / 복합 모음인 경우
        if ((self.state == Encoder.STATE_V and is_c) or
                (self.state == Encoder.STATE_C and not is_c) or
                ((self.last + s[0]) in Encoder.STROKES2COMP)):
            result.append(RESET_CODE)
        result.append(s)
        if is_c:
            # 이 뒤에 모음이 오면 reset 필요
            self.state = Encoder.STATE_C
        else:
            # 호환성 모음 뒤에는 자음이 오더라도 음절을 조합하지 않으니 뒤에
            # reset 불필요
            self.state = Encoder.STATE_INITIAL
        self.last = s[-1]
        return ''.join(result)

    def encode_jamo(self, ch):
        result = []

        is_c = (((ord(ch) >= 0x1100) and (ord(ch) <= 0x115F)) or
                ((ord(ch) >= 0x11A8) and (ord(ch) <= 0x11FF)) or
                ((ord(ch) >= 0xA960) and (ord(ch) <= 0xA97F)) or
                ((ord(ch) >= 0xD7CB) and (ord(ch) <= 0xD7FF)))

        if ch in Encoder.JAMO2STROKES_ALL:
            s = Encoder.JAMO2STROKES_ALL[ch]
        else:
            s = ch

        if ((self.state == Encoder.STATE_V and is_c) or
                (self.state == Encoder.STATE_C and not is_c)):
            result.append(RESET_CODE)
        result.append(s)

        if is_c:
            # 이 뒤에 모음이 오면 reset 필요
            self.state = Encoder.STATE_C
        else:
            # 호환성 모음 뒤에는 자음이 오더라도 음절을 조합하지 않으니 뒤에
            # reset 불필요
            self.state = Encoder.STATE_V
        self.last = s[-1]
        return ''.join(result)

    def encode(self, s):
        s = unicodedata.normalize('NFC', s)
        outlist = []
        self.state = Encoder.STATE_INITIAL
        self.last = ''
        for ch in s:
            if (ord(ch) >= 0xAC00) and (ord(ch) <= 0xD7A3):
                outlist.append(self.encode_syllable(ch))
            elif (ord(ch) >= 0x3131) and (ord(ch) <= 0x3163):
                outlist.append(self.encode_compjamo(ch))
            elif (((ord(ch) >= 0x1100) and (ord(ch) <= 0x11FF)) or
                  ((ord(ch) >= 0xA960) and (ord(ch) <= 0xA97F)) or
                  ((ord(ch) >= 0xD7B0) and (ord(ch) <= 0xD7FF))):
                outlist.append(self.encode_jamo(ch))
            else:
                self.state = Encoder.STATE_INITIAL
                self.last = ''
                outlist.append(ch)
        return ''.join(outlist)


DUMP_DECODER = False


class Decoder:
    def __init__(self):
        pass

    def stroke_is_c(self, ch):
        return (ord(ch) >= 0x3131) and (ord(ch) <= 0x314E)

    def stroke_is_v(self, ch):
        return (ord(ch) >= 0x314F) and (ord(ch) <= 0x3163)

    def compose(self, s):
        l_table = {
            'ㄱ': '\u1100',
            'ㄲ': '\u1101',
            'ㄴ': '\u1102',
            'ㄷ': '\u1103',
            'ㄸ': '\u1104',
            'ㄹ': '\u1105',
            'ㅁ': '\u1106',
            'ㅂ': '\u1107',
            'ㅃ': '\u1108',
            'ㅅ': '\u1109',
            'ㅆ': '\u110A',
            'ㅇ': '\u110B',
            'ㅈ': '\u110C',
            'ㅉ': '\u110D',
            'ㅊ': '\u110E',
            'ㅋ': '\u110F',
            'ㅌ': '\u1110',
            'ㅍ': '\u1111',
            'ㅎ': '\u1112',
        }
        v_table = {
            'ㅏ': '\u1161',
            'ㅐ': '\u1162',
            'ㅑ': '\u1163',
            'ㅒ': '\u1164',
            'ㅓ': '\u1165',
            'ㅔ': '\u1166',
            'ㅕ': '\u1167',
            'ㅖ': '\u1168',
            'ㅗ': '\u1169',
            'ㅗㅏ': '\u116A',
            'ㅗㅐ': '\u116B',
            'ㅗㅣ': '\u116C',
            'ㅛ': '\u116D',
            'ㅜ': '\u116E',
            'ㅜㅓ': '\u116F',
            'ㅜㅔ': '\u1170',
            'ㅜㅣ': '\u1171',
            'ㅠ': '\u1172',
            'ㅡ': '\u1173',
            'ㅡㅣ': '\u1174',
            'ㅣ': '\u1175',
        }
        t_table = {
            'ㄱ': '\u11A8',
            'ㄲ': '\u11A9',
            'ㄱㅅ': '\u11AA',
            'ㄴ': '\u11AB',
            'ㄴㅈ': '\u11AC',
            'ㄴㅎ': '\u11AD',
            'ㄷ': '\u11AE',
            'ㄹ': '\u11AF',
            'ㄹㄱ': '\u11B0',
            'ㄹㅁ': '\u11B1',
            'ㄹㅂ': '\u11B2',
            'ㄹㅅ': '\u11B3',
            'ㄹㅌ': '\u11B4',
            'ㄹㅍ': '\u11B5',
            'ㄹㅎ': '\u11B6',
            'ㅁ': '\u11B7',
            'ㅂ': '\u11B8',
            'ㅂㅅ': '\u11B9',
            'ㅅ': '\u11BA',
            'ㅆ': '\u11BB',
            'ㅇ': '\u11BC',
            'ㅈ': '\u11BD',
            'ㅊ': '\u11BE',
            'ㅋ': '\u11BF',
            'ㅌ': '\u11C0',
            'ㅍ': '\u11C1',
            'ㅎ': '\u11C2',
        }
        vv_table = {'ㅗㅐ': 'ㅙ', 'ㅗㅣ': 'ㅚ', 'ㅜㅓ': 'ㅝ', 'ㅜㅔ': 'ㅞ',
                    'ㅡㅣ': 'ㅢ'}
        tt_table = {'ㄱㅅ': 'ㄳ', 'ㄴㅈ': 'ㄵ', 'ㄴㅎ': 'ㄶ', 'ㄹㄱ': 'ㄺ',
                    'ㄹㅁ': 'ㄻ', 'ㄹㅂ': 'ㄼ', 'ㄹㅅ': 'ㄽ', 'ㄹㅌ': 'ㄾ',
                    'ㄹㅍ': 'ㄿ', 'ㄹㅎ': 'ㅀ', 'ㅂㅅ': 'ㅄ'}

        assert len(s) >= 2
        nfd = l_table[s[0]]
        i = 1
        assert self.stroke_is_v(s[i])
        if len(s) > (i + 1) and self.stroke_is_v(s[i+1]):
            nfd += v_table[s[i:i+2]]
            i += 2
        else:
            nfd += v_table[s[i]]
            i += 1
        if len(s) >= (i + 1):
            if len(s) > (i + 1) and self.stroke_is_c(s[i+1]):
                nfd += t_table[s[i:i+2]]
                i += 2
            else:
                assert self.stroke_is_c(s[i])
                nfd += t_table[s[i]]
                i += 1
        assert len(s) == i
        return unicodedata.normalize('NFC', nfd)

    def decode(self, s):
        composed = []
        strokes = []
        precomposed = ''
        prestrokes = ''

        STATE_INITIAL = 1
        STATE_L = 2
        STATE_LL = 22
        STATE_V = 3
        STATE_VC = 33
        STATE_T = 4
        STATE_TT = 5
        state = STATE_INITIAL

        for ch in s:
            if ch == RESET_CODE:
                composed.append(precomposed)
                strokes.append(prestrokes)
                precomposed = ''
                prestrokes = ''
                state = STATE_INITIAL
            elif ch in 'ㄱㄲㄴㄷㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ':
                t_table = {'ㄱㅅ': 'ㄳ', 'ㄴㅈ': 'ㄵ', 'ㄴㅎ': 'ㄶ', 'ㄹㄱ': 'ㄺ',
                           'ㄹㅁ': 'ㄻ', 'ㄹㅂ': 'ㄼ', 'ㄹㅅ': 'ㄽ', 'ㄹㅌ': 'ㄾ',
                           'ㄹㅍ': 'ㄿ', 'ㄹㅎ': 'ㅀ', 'ㅂㅅ': 'ㅄ'}
                if ((state == STATE_INITIAL) or (state == STATE_LL) or
                        (state == STATE_VC)):
                    if precomposed:
                        composed.append(precomposed)
                        strokes.append(prestrokes)
                    precomposed = ch
                    prestrokes = ch
                    state = STATE_L
                elif state == STATE_L:
                    if (prestrokes + ch) in t_table:
                        precomposed = t_table[prestrokes + ch]
                        prestrokes += ch
                        state = STATE_LL
                    else:
                        composed.append(precomposed)
                        strokes.append(prestrokes)
                        precomposed = ch
                        prestrokes = ch
                        state = STATE_L
                elif state == STATE_V:
                    if ch in 'ㅃㅉ':
                        if precomposed:
                            composed.append(precomposed)
                            strokes.append(prestrokes)
                        precomposed = ch
                        prestrokes = ch
                        state = STATE_L
                    else:
                        prestrokes += ch
                        precomposed = self.compose(prestrokes)
                        state = STATE_T
                elif state == STATE_T:
                    if (prestrokes[-1] + ch) in t_table:
                        prestrokes += ch
                        precomposed = self.compose(prestrokes)
                        state = STATE_TT
                    else:
                        composed.append(precomposed)
                        strokes.append(prestrokes)
                        prestrokes = ch
                        precomposed = ch
                        state = STATE_L
                elif state == STATE_TT:
                    composed.append(precomposed)
                    strokes.append(prestrokes)
                    prestrokes = ch
                    precomposed = ch
                    state = STATE_L
                else:
                    assert False
            elif self.stroke_is_v(ch):
                v_table = {'ㅗㅏ': 'ㅘ', 'ㅗㅐ': 'ㅙ', 'ㅗㅣ': 'ㅚ',
                           'ㅜㅓ': 'ㅝ', 'ㅜㅔ': 'ㅞ', 'ㅜㅣ': 'ㅟ',
                           'ㅡㅣ': 'ㅢ'}
                if state == STATE_INITIAL:
                    composed.append(precomposed)
                    strokes.append(prestrokes)
                    precomposed = ch
                    prestrokes = ch
                    state = STATE_VC
                elif state == STATE_VC:
                    if (prestrokes + ch) in v_table:
                        precomposed = v_table[prestrokes + ch]
                        prestrokes += ch
                        state = STATE_VC
                    else:
                        composed.append(precomposed)
                        strokes.append(prestrokes)
                        precomposed = ch
                        prestrokes = ch
                        state = STATE_VC
                elif state == STATE_LL:
                    composed.append(prestrokes[0])
                    strokes.append(prestrokes[0])
                    prestrokes = prestrokes[1:] + ch
                    precomposed = self.compose(prestrokes)
                    state = STATE_V
                elif state == STATE_L:
                    prestrokes += ch
                    precomposed = self.compose(prestrokes)
                    state = STATE_V
                elif state == STATE_V:
                    if (prestrokes[-1] + ch) in v_table:
                        prestrokes += ch
                        precomposed = self.compose(prestrokes)
                        state = STATE_V
                    else:
                        composed.append(precomposed)
                        strokes.append(prestrokes)
                        prestrokes = ch
                        precomposed = ch
                        state = STATE_VC
                elif state == STATE_T or state == STATE_TT:
                    composed.append(self.compose(prestrokes[:-1]))
                    strokes.append(prestrokes[:-1])
                    prestrokes = prestrokes[-1] + ch
                    precomposed = self.compose(prestrokes)
                    state = STATE_V
                else:
                    assert False
            else:
                if precomposed:
                    composed.append(precomposed)
                    strokes.append(prestrokes)
                composed.append(ch)
                strokes.append(ch)
                precomposed = ''
                prestrokes = ''
                state = STATE_INITIAL
            if DUMP_DECODER:
                print('================')
                print('ch: %s' % ch)
                print('composed: %s' % composed)
                print('strokes: %s' % strokes)
                print('precomposed: %s' % precomposed)
                print('prestrokes: %s' % prestrokes)
        if precomposed:
            composed.append(precomposed)
            strokes.append(prestrokes)
        return ''.join(composed)


def encode(s):
    encoder = Encoder()
    return encoder.encode(s)


def decode(s):
    decoder = Decoder()
    return decoder.decode(s)


if __name__ == '__main__':
    import sys

    def assert_round_trip(decoded, encoded):
        if encode(decoded) != encoded:
            print('encode(%s) = %s != %s' % (decoded, encode(decoded),
                                             encoded))
        assert encode(decoded) == encoded
        if decode(encoded) != decoded:
            print('encode(%s) = %s != %s' % (decoded, encode(decoded),
                                             encoded))
        assert decode(encoded) == decoded

    def assert_encode(decoded, encoded):
        if encode(decoded) != encoded:
            print('encode(%s) = %s != %s' % (decoded, encode(decoded),
                                             encoded))
        assert encode(decoded) == encoded

    assert_round_trip('바둑이', 'ㅂㅏㄷㅜㄱㅇㅣ')
    assert_round_trip('과일', 'ㄱㅗㅏㅇㅣㄹ')
    assert_round_trip('뷁이', 'ㅂㅜㅔㄹㄱㅇㅣ')
    assert_round_trip('뷀기', 'ㅂㅜㅔㄹㄱㅣ')
    assert_round_trip('쌇아', 'ㅆㅏㄹㅎㅇㅏ')
    assert_round_trip('ㄳ', 'ㄱㅅ')
    assert_round_trip('ㅙ', 'ㅗㅐ')
    assert_round_trip('ㅙ', 'ㅗㅐ')
    assert_round_trip('ㄱ삯', 'ㄱㅅㅏㄱㅅ')
    assert_round_trip('ㄱ삭가', 'ㄱㅅㅏㄱㄱㅏ')
    assert_round_trip('ㅙㄱ', 'ㅗㅐㄱ')
    assert_round_trip('바둑이ㄱ', 'ㅂㅏㄷㅜㄱㅇㅣ' + RESET_CODE + 'ㄱ')
    assert_round_trip('ㄱㅅ', 'ㄱ' + RESET_CODE + 'ㅅ')
    assert_round_trip('ㅙㄱㅣ', 'ㅗㅐㄱ' + RESET_CODE + 'ㅣ')
    assert_round_trip('맨To맨', 'ㅁㅐㄴToㅁㅐㄴ')
    assert_round_trip('English맨', 'Englishㅁㅐㄴ')

    # one way
    assert_encode('\u1100\u1161\u11A8', 'ㄱㅏㄱ')
    assert_encode('\u1100\u1161\u11A8\u1161', 'ㄱㅏㄱ' + RESET_CODE + 'ㅏ')
    assert_encode('\u1100\u1161\u112D\u1161\u11A8', 'ㄱㅏ' + RESET_CODE +
                  'ㅅㄱ' + RESET_CODE + 'ㅏ' + RESET_CODE + 'ㄱ')
