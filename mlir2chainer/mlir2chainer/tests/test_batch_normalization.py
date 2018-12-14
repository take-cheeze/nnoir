import mlir
import chainer
import mlir2chainer
import numpy as np
import util
import chainer.links as L

def test_batch_normalization():
    shape = (2,3,4,5)
    channel = 3
    gamma = np.zeros(channel)
    beta = np.zeros(channel)
    avg_mean = np.zeros(channel)
    avg_var = np.zeros(channel)
    eps = 2e-05
    gamma[:] = 0.9
    beta[:] = 0.1
    avg_mean[:] = 0.2
    avg_var[:] = 0.8

    inputs  = [mlir.Node('v0', 'float', shape)]
    outputs = [mlir.Node('v2', 'float', shape)]
    nodes = inputs + outputs
    input_names = [ x.name for x in inputs ]
    output_names = [ x.name for x in outputs ]
    function = mlir.edges.BatchNormalization(input_names, output_names,
                                             eps=eps,
                                             avg_mean=avg_mean,
                                             avg_var=avg_var,
                                             gamma=gamma,
                                             beta=beta)
    result = mlir.MLIR('BatchNormalization', 'mlir2chainer_test', 0.1, input_names, output_names, nodes, [function])
    result.dump('batch_normalization.mlir')
    
    x = np.random.randn(2,3,4,5)
    ref = function.run(x)
    with chainer.using_config('train', False):
        m = mlir2chainer.ChainerNN('batch_normalization.mlir')
        y = m(x)
        assert(np.all(abs(y-ref).data<util.epsilon))