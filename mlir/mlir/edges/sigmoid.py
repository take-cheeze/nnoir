import chainer.functions as F
from .edge import Edge

class Sigmoid(Edge):
    def __init__(self, inputs, outputs, **params):
        necessary_params = set()
        optional_params = set()
        super(Sigmoid, self).__init__(inputs, outputs, params, necessary_params, optional_params)
