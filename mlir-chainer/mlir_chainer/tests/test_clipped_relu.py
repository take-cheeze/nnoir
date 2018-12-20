import mlir
import chainer
from mlir_chainer import MLIRFunction
import numpy as np
import util

def test_clipped_relu():
    inputs  = [mlir.Node(b'v0', 'float', (10,10))]
    outputs = [mlir.Node(b'v2', 'float', (10,10))]
    nodes = inputs + outputs
    input_names = [ x.name for x in inputs ]
    output_names = [ x.name for x in outputs ]
    function = mlir.edges.ClippedReLU(input_names, output_names, upper=40.0)
    result = mlir.MLIR(b'ClippedReLU', b'mlir2chainer_test', 0.1, input_names, output_names, nodes, [function])
    result.dump('clipped_relu.mlir')

    x = np.random.randn(10,10)
    ref = function.run(x)
    m = MLIRFunction('clipped_relu.mlir')
    with chainer.using_config('train', False):
        y = m(x)
        assert(np.all(abs(y-ref).data<util.epsilon))
