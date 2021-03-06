from nnoir.functions import *
from .utils import *


class OpSoftmax(Op):

    def __init__(self, node):
        super(OpSoftmax, self).__init__(node)

        self.axis = 1
        for attr in self.node.attribute:
            if attr.name == 'axis':
                self.axis = attr.i

    def get_dummy_output(self, env):
        [x] = self.node.input
        return env[x]

    def to_function(self, env, constants):
        return [
            Softmax(
                list(self.node.input),
                list(self.node.output),
                axis=self.axis
            )
        ]
