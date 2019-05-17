import nnoir
import chainer
from nnoir_chainer import NNOIRFunction
import numpy as np
import util


def test_relu():
    inputs = [nnoir.Value(b'v0', np.zeros((10, 10)).astype('float32'))]
    outputs = [nnoir.Value(b'v2', np.zeros((10, 10)).astype('float32'))]
    nodes = inputs + outputs
    input_names = [x.name for x in inputs]
    output_names = [x.name for x in outputs]
    function = nnoir.functions.ReLU(input_names, output_names)
    result = nnoir.NNOIR(b'ReLU', b'nnoir2chainer_test', '0.1', input_names, output_names, nodes, [function])
    result.dump('relu.nnoir')

    x = np.random.randn(10, 10).astype('float32')
    ref = function.run(x)
    with chainer.using_config('train', False):
        m = NNOIRFunction('relu.nnoir')
        y = m(x)
        assert(np.all(abs(y-ref).data < util.epsilon))
