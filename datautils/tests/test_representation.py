from .. representation import RandBinRep
import unittest, sys

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
            print >> sys.stderr, rbr.item_to_idx
        for item in vocab:
            outrep = rbr[item]
            print >> sys.stderr, outrep
            outitem = rbr.itemfrom(outrep)
            self.assertEqual(item, outitem)


if __name__ == '__main__':
    unittest.main()
