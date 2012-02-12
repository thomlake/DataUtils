import numpy as np

class OneHotRep(object):
    def __init__(self, vocab = None):
        self.item_to_idx = {}
        self.idx_to_item = {}
        self.item_to_rep = {}
        if vocab:
            self.n = len(vocab)
            self.vocab = vocab
            self.item_to_idx = dict([(item, i) for i, item in enumerate(vocab)])
            self.idx_to_item = dict([(i, item) for i, item in enumerate(vocab)])

    def add_to_vocab(self, item):
        self.item_to_idx[item] = self.n
        self.idx_to_item[self.n] = item
        self.n += 1

    def itemrep(self, item):
        try:
            return self.item_to_rep[item]
        except KeyError:
            z = np.zeros(self.n)
            z[self.item_to_idx[item]] = 1
            self.item_to_rep[item] = z
            return z

    def bagrep(self, items):
        z = np.zeros(self.n)
        z[[self.item_to_idx[item] for item in items]] = 1
        return z

    def bagfrom(self, rep, thresh = 0.):
        return [self.idx_to_item[idx] for idx in wheregt(rep, thresh)]

    def itemfrom(self, rep):
        return self.idx_to_item[rep.argmax()]

def wheregt(x, t):
    return tuple([i for i in np.where(x > t)[0]])

class RandBinRep(object):
    def __init__(self, n, vocab = None, p = 0.1):
        self.item_to_idx = {}
        self.idx_to_item = {}
        self.item_to_rep = {}
        self.n = n
        self.p = p
        self.q = 1 - p
        if vocab:
            self.vocab = vocab
            for item in vocab:
                rep = self.__findrep()
                self.item_to_idx[item] = rep
                self.idx_to_item[rep] = item

    def __findrep(self):
        tupidx = wheregt(np.random.random(self.n), self.q)
        patience = 1000
        while tupidx in self.idx_to_item and patience > 0:
            tupidx = wheregt(np.random.random(self.n), self.q)
            patience -= 1
        if patience < 0:
            return ()
        return tupidx

    def add_to_vocab(self, item):
        rep = self.__findrep()
        self.item_to_idx[item] = rep
        self.idx_to_item[rep] = item
    
    def itemrep(self, item):
        try:
            return self.item_to_rep[item]
        except KeyError:
            z = np.zeros(self.n)
            z[list(self.item_to_idx[item])] = 1
            self.item_to_rep[item] = z
            return z

    def itemfrom(self, rep, thresh = 0.):
        try:
            return self.idx_to_item[wheregt(rep, thresh)]
        except KeyError:
            pass
        return '__ITEM_NOT_FOUND__'

