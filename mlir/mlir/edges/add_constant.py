import chainer.functions as F
from .edge import Edge

class AddConstant(Edge):
    def __init__(self, inputs, outputs, **params):
        necessary_params = {'value'}
        optional_params = set()
        super(AddConstant, self).__init__(inputs, outputs, params, necessary_params, optional_params)
    def run(self, x):
        return x + self.params['value']
