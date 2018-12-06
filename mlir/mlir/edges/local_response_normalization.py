import chainer.functions as F
from .edge import Edge
import numpy as np

class LocalResponseNormalization(Edge):
    def __init__(self, inputs, outputs, **params):
        necessary_params = {'n',
                            'k',
                            'alpha',
                            'beta'}
        optional_params = set()
        super().__init__(inputs, outputs, params, necessary_params, optional_params)
    def run(self, x):
        RA2 = np.square(x)
        R = RA2.copy()
        for i in range(1, self.params['n']//2 + 1):
            R[:, i:] += RA2[:, :-i]
            R[:, :-i] += RA2[:, i:]
        R = self.params['k'] + self.params['alpha'] * R
        R = R ** -self.params['beta']
        R = x * R
        return R
