import numpy as np

class SimpleSampler(object):
    def __init__(self, weights, keys = None):
        if keys is None:
            self.keys = np.arange(len(weights))
        else:
            self.keys = np.array(keys)
        arr_weights = np.array(weights)
        self.weights = weights / weights.sum()
        self.cum = self.weights.cumsum()

    def random(self, count = None):
        if count is None:
            return self.keys[self.cum.searchsorted(np.random.random())][0]
        else:
            return self.keys[self.cum.searchsorted(np.random.random(count))]

