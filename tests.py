# -*- coding: utf-8 -*-

import unittest
from io import StringIO
from cedict.cedict_parser import iter_cedict, extract_single
from cedict.pinyin import pinyinize, depinyinize

try:
    unicode('hi')
except NameError:
    def unicode(s, encoding):
        return s


SAMPLE_CEDICT = unicode("""齡 龄 [ling2] /age/length of experience, membership etc/
齢 齢 [ling2] /Japanese variant of 齡|龄/
咬 咬 [yao3] /to bite/to nip/
齩 咬 [yao3] /variant of 咬[yao3]/
麵包房 面包房 [mian4 bao1 fang2] /bakery/CL:家[jia1]/
鮎 鲇 [nian2] /sheatfish (Parasilurus asotus)/oriental catfish/see also 鯰|鲶[nian2]/
鯰 鲶 [nian2] /sheatfish (Parasilurus asotus)/oriental catfish/see also 鮎|鲇[nian2]/
包 鲶 [niant] /wrong entry/not right/see also 鮎|鲇[nian2]/""", 'utf-8')


class TestIterCEDict(unittest.TestCase):
    def setUp(self):
        self.f = StringIO(SAMPLE_CEDICT)

    def test_find_entries(self):
        entries = []
        for ch, chs, pinyin, defs, variants, mw in iter_cedict(self.f):
            entries.append(pinyin)

        self.assertEqual(8, len(entries))
        self.assertEqual('ling2 ling2 yao3 yao3 mian4 bao1 fang2 nian2 nian2 niant', ' '.join(entries))

    def test_defs_correct(self):
        d = {}
        for ch, chs, pinyin, defs, variants, mw in iter_cedict(self.f):
            d[ch] = defs

        self.assertEqual(d[u'咬'], ['to bite', 'to nip'],
                'should find 2 defs')
        self.assertEqual(d[u'齩'], [],
                'Variant notes are not definitions')
        self.assertEqual(d[u'麵包房'], ['bakery'],
                'Measure words should be removed from definitions')

    def test_measure_words_correct(self):
        d = {}
        for ch, chs, pinyin, defs, variants, mw in iter_cedict(self.f):
            d[ch] = mw

        self.assertEqual(d[u'麵包房'], [(u'家', u'家', u'jia1')],
                'This entry should have a measure word')
        self.assertEqual(len(d[u'鯰']), 0,
                'There is no measure word')


    def test_variants_correct(self):
        d = {}
        for ch, chs, pinyin, defs, variants, mw in iter_cedict(self.f):
            d[ch] = variants

    def test_extract_single(self):
        s_entries = []
        for ch, pinyin, pwt, tone, defs, variants, mw in extract_single(self.f):
            self.assertEqual(len(ch)==1, True)
            self.assertEqual(tone in ["1","2","3","4","5"], True)

            s_entries.append(ch)

        self.assertEqual(len(s_entries), 6)
        self.assertEqual("麵包房" in s_entries, False)
        self.assertEqual("包" in s_entries, False)

class TestPinyin(unittest.TestCase):

    def test_pinyinize(self):
        self.assertEqual(pinyinize('xi3huan1'), u'xǐhuān')
        self.assertEqual(pinyinize('xing2 dong4'), u'xíng dòng')
        self.assertEqual(pinyinize('ni3 hao3'), u'nǐ hǎo')
        self.assertEqual(pinyinize('ni3 hao5'), u'nǐ hao')
        self.assertEqual(pinyinize('hua4'), u'huà')

    def test_depinyinize(self):
        self.assertEqual('xi3huan1', depinyinize(u'xǐhuān'))
        self.assertEqual('xing2 dong4', depinyinize(u'xíng dòng'))
        self.assertEqual('ni3 hao3', depinyinize(u'nǐ hǎo'))
        self.assertEqual('ni3 hao', depinyinize(u'nǐ hao'))
        self.assertEqual('hua4', depinyinize(u'huà'))

    def test_double_dot(self):
        self.assertEqual(pinyinize('lu:4fa3'), u'lǜfǎ')
        self.assertEqual('lu:4fa3', depinyinize(u'lǜfǎ'))

        self.assertEqual(pinyinize('lu:4fa3'), u'lǜfǎ')
        self.assertEqual('lu:4fa3', depinyinize(u'lǜfǎ'))

        self.assertEqual(pinyinize('nu:e4dai4'), u'nüèdài')
        self.assertEqual('nu:e4dai4', depinyinize(u'nüèdài'))



if __name__ == '__main__':
    unittest.main()
