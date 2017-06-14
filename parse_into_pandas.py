from cedict import cedict_parser

with open("cedict_ts.u8") as dict_file:
    for ch, pinyin, pwot, tone, defs, variants, mw in cedict_parser.extract_single(dict_file):
        print pinyin
