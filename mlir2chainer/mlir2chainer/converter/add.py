import chainer.functions as F

class ConvertAdd():
    def to_chainer(edge, *xs):
        return F.add(*xs)
