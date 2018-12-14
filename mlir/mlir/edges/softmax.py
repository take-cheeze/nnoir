import chainer.functions as F
from .edge import Edge
import numpy as np

class Softmax(Edge):
    def __init__(self, inputs, outputs, **params):
        necessary_params = {'axis'}
        optional_params = set()
        super(Softmax, self).__init__(inputs, outputs, params, necessary_params, optional_params)
    def run(self, x):
        return np.exp(x) / np.sum(np.exp(x), self.params['axis'], keepdims=True)