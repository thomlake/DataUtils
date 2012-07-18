from .. representation import RandBinRep, OneHotRep, OneHotOffsetRep, wheregt, onehotarray, binarray
import unittest, sys
import numpy as np

class TestFuncs(unittest.TestCase):
    def test_wheregt(self):
        a = np.array([0, 0, 1, 0, 1])
        idx_a = (2, 4)
        b = np.array([0.5, 0.51, 0.4, 0.6, 1.])
        idx_b = (1, 3, 4)
        idx = wheregt(a, 0)
        self.assertEqual(idx, idx_a)
        idx = wheregt(b, 0.5)
        self.assertEqual(idx, idx_b)

    def test_onehotarray(self):
        a = onehotarray(5, 2)
        b = np.array([0, 0, 1, 0, 0])
        self.assertTrue(not (a - b).any())

    def test_binarray(self):
        a = binarray(5, (0, 2, 4))
        b = np.array([1, 0, 1, 0, 1])
        self.assertTrue(not (a - b).any())

class TestOneHotRep(unittest.TestCase):
    def test_passed_vocab(self):
        vocab = ['the', 'cat', 'in', 'the', 'hat']
        n = 10
        ohr = OneHotRep(vocab = vocab)
        for item in vocab:
            outrep = ohr[item]
            outitem = ohr.itemfrom(outrep)
            self.assertEqual(item, outitem)
    
    def test_added_vocab(self):
        vocab = ['the', 'cat', 'in', 'the', 'hat']
        n = 10
        ohr = OneHotRep()
        for item in vocab:
            ohr.add(item)
        for item in vocab:
            outrep = ohr[item]
            outitem = ohr.itemfrom(outrep)
            self.assertEqual(item, outitem)

class TestOneHotOffsetRep(unittest.TestCase):
    def test_passed_vocab(self):
        vocab = ['the', 'cat', 'in', 'the', 'hat']
        n = 10
        ohr = OneHotOffsetRep(2, 3, vocab = vocab)
        for item in vocab:
            outrep = ohr[item]
            outitem = ohr.itemfrom(outrep)
            self.assertEqual(item, outitem)
    
    def test_added_vocab(self):
        vocab = ['the', 'cat', 'in', 'the', 'hat']
        n = 10
        ohr = OneHotOffsetRep(2, 3)
        for item in vocab:
            ohr.add(item)
        for item in vocab:
            outrep = ohr[item]
            print ohr.item_to_idx[item]
            print outrep
            outitem = ohr.itemfrom(outrep)
            self.assertEqual(item, outitem)

class TestRandBinRep(unittest.TestCase):
    def test_passed_vocab(self):
        vocab = ['the', 'cat', 'in', 'the', 'hat']
        n = 10
        rbr = RandBinRep(n, vocab = vocab)
        for item in vocab:
            outrep = rbr[item]
            outitem = rbr.itemfrom(outrep)
            self.assertEqual(item, outitem)
    
    def test_added_vocab(self):
        vocab = ['the', 'cat', 'in', 'the', 'hat']
        n = 10
        rbr = RandBinRep(n)
        for item in vocab:
            rbr.add(item)
        for item in vocab:
            outrep = rbr[item]
            outitem = rbr.itemfrom(outrep)
            self.assertEqual(item, outitem)

if __name__ == '__main__':
    unittest.main()
