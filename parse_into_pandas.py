import sys
import pandas as pd

from cedict.cedict_parser import iter_cedict
from cedict.pinyin import ALL_SOUNDS, pinyinize

reload(sys)
sys.setdefaultencoding('utf8')

def extract_single(fileobj):
    """
    Get only the single-character entries from a fileobj dictionary and extract tone
    and raw pinyin, yielding a tuple for each entrie as
    (chinese-traditional, pinyin, pinyin(w/o tone), tone, definitions, variants, measure-words)
    """
    for ch, chs, pinyin, defs, variants, mw in iter_cedict(fileobj):
        ch_d = ch.decode('utf8')

        if len(ch_d) == 1:
            # skip latin characters
            if any((ord(c) < 128 and c != ' ') for c in ch):
                continue

            pin_wo_tone = pinyin[0:-1]
            tone = pinyin[-1]

            # only official tones and pinyins
            if tone in ["1","2","3","4","5"] and pin_wo_tone in ALL_SOUNDS:
                pinyin = pinyinize(pinyin)
                yield ch, pinyin, pin_wo_tone, tone, defs, variants, mw

class DictDF():
    def __init__(self):
        """
        self.s_df: single entries DataFrame
        self.dict_file_name: dictionary file address
        """
        self.s_df = pd.DataFrame(columns=('traditional','pinyin','pinyin(raw)','tone','definition','variants','measure-words'))
        self.dict_file_name = "cedict_ts.u8"

    def load_single_entries(self):
        """
        Takes single definitions from dictionary and stores them in a dataframe
        and a csv file for the first time.
        Subsequent times it reads the csv file for building the dataframe.
        """
        if len(self.s_df) == 0:
            ## It should have its own databases afterwards
            try:
                self.s_df = pd.read_csv('single_char_df.csv')
            except IOError:
                with open(self.dict_file_name) as dict_file:
                    i = 0
                    for ch, pinyin, pwot, tone, defs, variants, mw in extract_single(dict_file):
                        self.s_df.loc[i] = (ch, pinyin, pwot, tone, defs, variants, mw)
                        i = i + 1

                    self.s_df.to_csv('single_char_df.csv')

            print "Data frame loaded. \n Length of data frame: {}".format(len(self.s_df))
            print self.s_df.head(5)
