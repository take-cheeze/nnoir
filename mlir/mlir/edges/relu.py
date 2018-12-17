import chainer.functions as F
from .edge import Edge

class ReLU(Edge):
    def __init__(self, inputs, outputs, **params):
        required_params = set()
        optional_params = set()
        super(ReLU, self).__init__(inputs, outputs, params, required_params, optional_params)
    def run(self, x):
        R = x.copy()
        R[R < 0] = 0
        return R
