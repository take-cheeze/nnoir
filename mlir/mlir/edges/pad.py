import chainer.functions as F
from .edge import Edge
import numpy as np

class ConstantPadding(Edge):
    def __init__(self, inputs, outputs, **params):
        necessary_params = {'pads',
                            'value'}
        optional_params = set()
        super(ConstantPadding, self).__init__(inputs, outputs, params, necessary_params, optional_params)
    def run(self, x):
        return np.pad(x, self.params['pads'],
                      mode='constant', constant_values=(self.params['value'],))