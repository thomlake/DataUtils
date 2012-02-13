#---------------------------------------#
#	This file is part of DataUtils.
#
#	DataUtils is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	BowNlPy is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with DataUtils.  If not, see <http://www.gnu.org/licenses/>.
#---------------------------------------#
# author:
#	tllake 
# email:
#	<thomas.l.lake@wmich.edu>
#	<thom.l.lake@gmail.com>
# date:
#	2012.02.12
# file:
#	representation.py
# description:
#	classes for storing vector representation of non vector things
#---------------------------------------#

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

def binarray(dim, onesat):
    z = np.zeros(dim)
    z[list(onesat)] = 1
    return z

def wheregt(x, t):
    return tuple([i for i in np.where(x > t)[0]])

class RandBinRep(object):
    def __init__(self, dim, vocab = None, p = 0.1, notfound = '<UNK?>'):
        self.dim = dim
        self.q = 1 - p
        self.notfound = notfound
        notfoundidx = wheregt(np.random.random(self.dim), self.q)
        self.item_to_idx = {notfound: notfoundidx}
        self.idx_to_item = {notfoundidx: notfound}
        self.item_to_rep = {notfound: binarray(dim, notfoundidx)}
        if vocab:
            for item in vocab:
                idx = self.__newidx()
                self.item_to_idx[item] = idx
                self.idx_to_item[idx] = item

    def __getitem__(self, x):
        try:
            return self.item_to_rep[x]
        except KeyError:
            try:
                idx = self.item_to_idx[x]
            except KeyError:
                return self.item_to_rep[self.notfound]
            z = binarray(self.dim, idx)
            self.item_to_rep[x] = z
            return z

    def __newidx(self):
        idx = wheregt(np.random.random(self.dim), self.q)
        patience = 1000
        while idx in self.idx_to_item and patience > 0:
            idx = wheregt(np.random.random(self.dim), self.q)
            patience -= 1
        if patience < 0:
            return ()
        return idx

    def add(self, item):
        try:
            self.item_to_idx[item]
        except KeyError:
            idx = self.__newidx()
            self.item_to_idx[item] = idx
            self.idx_to_item[idx] = item
    
    def itemfrom(self, rep, thresh = 0.):
        try:
            return self.idx_to_item[wheregt(rep, thresh)]
        except KeyError:
            pass
        return '__ITEM_NOT_FOUND__'

