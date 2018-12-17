import mlir
import chainer
from chainer.links.mlir import MLIRFunction
import numpy as np
import util

def test_linear():
    batch = 2
    in_ch = 3
    out_ch = 4
    inputs  = [mlir.Node('v0', 'float', (batch, in_ch))]
    outputs = [mlir.Node('v2', 'float', (batch, out_ch))]
    nodes = inputs + outputs
    input_names = [ x.name for x in inputs ]
    output_names = [ x.name for x in outputs ]
    W = np.random.randn(out_ch, in_ch).astype(np.float32)
    b = np.random.randn(out_ch).astype(np.float32)
    function = mlir.edges.Linear(input_names, output_names, W=W, b=b)
    result = mlir.MLIR('Linear', 'mlir2chainer_test', 0.1, input_names, output_names, nodes, [function])
    result.dump('linear.mlir')

    x = np.random.randn(batch, in_ch).astype(np.float32)
    ref = function.run(x)
    m = MLIRFunction('linear.mlir')
    with chainer.using_config('train', False):
        y = m(x)
        assert(np.all(abs(y-ref).data<util.epsilon))