import mlir
import chainer
from mlir_chainer import MLIRFunction
import numpy as np
import util

def test_unpooling_2d():
    kh, kw = 2, 3
    sy, sx = 1, 2
    batch = 2
    ch = 3
    in_h, in_w = 5, 6
    out_h, out_w = 4, 9
    ph, pw = 1, 2
    inputs  = [mlir.Value(b'v0', 'float', (batch, ch, in_h, in_w))]
    outputs = [mlir.Value(b'v2', 'float', (batch, ch, out_h, out_w))]
    nodes = inputs + outputs
    input_names = [ x.name for x in inputs ]
    output_names = [ x.name for x in outputs ]
    function = mlir.functions.Unpooling2D(input_names, output_names, kh=kh, kw=kw, sy=sy, sx=sx, ph=ph, pw=pw,
                                      cover_all=False, outh=out_h, outw=out_w)
    result = mlir.MLIR(b'Unpooling2D', b'mlir2chainer_test', 0.1, input_names, output_names, nodes, [function])
    result.dump('unpooling_2d.mlir')

    x = np.random.randn(batch, ch, in_h, in_w)
    ref = function.run(x)
    m = MLIRFunction('unpooling_2d.mlir')
    with chainer.using_config('train', False):
        y = m(x)
        assert(np.all(abs(y-ref).data<util.epsilon))