from nnoir.functions import *
from .utils import *


class OpGemm(Op):

    def __init__(self, node):
        super(OpGemm, self).__init__(node)

        self.alpha = 1.0
        self.beta = 1.0
        self.transA = 0
        self.transB = 0
        for attr in node.attribute:
            if attr.name == 'alpha':
                self.alpha = attr.f
            if attr.name == 'beta':
                self.beta = attr.f
            if attr.name == 'transA':
                self.transA = attr.i
            if attr.name == 'transB':
                self.transB = attr.i

    def get_dummy_output(self, env):
        [A, B, C] = self.node.input
        a = env[A]
        if self.transA == 1:
            a = a.T
        b = env[B]
        if self.transB == 1:
            b = b.T
        return a.dot(b)+env[C]

    def to_function(self, env, constants):
        [A, B, C] = self.node.input

        if B not in constants:
            raise UnsupportedONNXOperation(self.node, 'B must be constant')
        if C not in constants:
            raise UnsupportedONNXOperation(self.node, 'C must be constant')

        b = env[B]
        if self.transB == 0:
            b = b.T
        c = env[C]

        if len(c.shape) == 2 and c.shape[0] != 1:
            raise UnsupportedONNXOperation(self.node, 'shapes mismatch')

        if self.transA == 1:
            internal_node = "{}_{}".format(A, id(A))
            env[internal_node] = env[A].T
            return [
                Transpose(
                    [A],
                    [internal_node],
                    axes=[1, 0]
                ),
                Linear(
                    [internal_node],
                    list(self.node.output),
                    W=encode_ndarray(self.alpha * b),
                    b=encode_ndarray(self.beta * c.ravel())
                )
            ]
        else:
            return [
                Linear(
                    [A],
                    list(self.node.output),
                    W=encode_ndarray(self.alpha * b),
                    b=encode_ndarray(self.beta * c.ravel())
                )
            ]
