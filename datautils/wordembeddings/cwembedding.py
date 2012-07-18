import pkgutil
import numpy as np

class ColWesEmbedding(object):
    def __init__(self):
        data = pkgutil.get_data('datautils', 'data/cw-50-dim-scaled.txt')
        splines = [line.split(' ') for line in data.split('\n')]
        emdict = dict([(line[0], np.array(map(float, line[1:])))
                       for line in splines])
        self.unknown = emdict['<UNK>'] = emdict['*UNKNOWN*']
        del emdict['*UNKNOWN*']
        self.emdict = emdict

    def __getitem__(self, key):
        try:
            return self.emdict[key]
        except KeyError:
            return self.unknown
