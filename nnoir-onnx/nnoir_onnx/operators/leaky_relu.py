from nnoir.functions import *
from .utils import *


class OpLeakyRelu(Op):

    def __init__(self, node):
        super(OpLeakyRelu, self).__init__(node)

        self.alpha = 0.01
        for attr in node.attribute:
            if attr.name == 'alpha':
                self.alpha = attr.f

    def get_dummy_output(self, env):
        [x] = self.node.input
        return env[x]

    def to_function(self, env, constants):
        return [LeakyReLU(list(self.node.input), list(self.node.output), slope=self.alpha)]
