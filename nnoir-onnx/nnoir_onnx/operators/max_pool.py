import numpy as np
from nnoir.functions import *
from .utils import *


class OpMaxPool(Op):

    def __init__(self, node):
        super(OpMaxPool, self).__init__(node)

        self.kernel_shape = None
        self.auto_pad = b'NOTSET'
        self.pads = None
        self.storage_order = 0
        self.strides = (1, 1)
        for attr in node.attribute:
            if attr.name == 'kernel_shape':
                self.kernel_shape = attr.ints
            if attr.name == 'storage_order':
                self.storage_order = attr.i
            if attr.name == 'strides':
                self.strides = attr.ints
            if attr.name == 'auto_pad':
                self.auto_pad = attr.s
            if attr.name == 'pads':
                self.pads = attr.ints

    def get_dummy_output(self, env):
        [x] = self.node.input

        _input = env[x]
        batch = _input.shape[0]
        channel = _input.shape[1]
        in_h = _input.shape[2]
        in_w = _input.shape[3]
        kh = self.kernel_shape[0]
        kw = self.kernel_shape[1]
        sy = self.strides[0]
        sx = self.strides[1]

        if self.auto_pad == b'NOTSET':
            pad_h = (0, 0)
            pad_w = (0, 0)
            if self.pads is not None:
                pad_h = (self.pads[0], self.pads[2])
                pad_w = (self.pads[1], self.pads[3])
        else:
            pad_h = auto_pad_to_manual_pad(in_h, kh, sy, 1, self.auto_pad)
            pad_w = auto_pad_to_manual_pad(in_w, kw, sx, 1, self.auto_pad)

        out_h = ((pad_h[0] + in_h + pad_h[1]) - ((kh - 1) * 1 + 1)) // sy + 1
        out_w = ((pad_w[0] + in_w + pad_w[1]) - ((kw - 1) * 1 + 1)) // sx + 1

        return np.zeros((batch, channel, out_h, out_w), dtype=env[x].dtype)

    def to_function(self, env, constants):
        [x] = self.node.input

        _input = env[x]
        batch = _input.shape[0]
        channel = _input.shape[1]
        in_h = _input.shape[2]
        in_w = _input.shape[3]
        kh = self.kernel_shape[0]
        kw = self.kernel_shape[1]
        sy = self.strides[0]
        sx = self.strides[1]

        if self.auto_pad == b'NOTSET':
            pad_h = (0, 0)
            pad_w = (0, 0)
            if self.pads is not None:
                pad_h = (self.pads[0], self.pads[2])
                pad_w = (self.pads[1], self.pads[3])
        else:
            pad_h = auto_pad_to_manual_pad(in_h, kh, sy, 1, self.auto_pad)
            pad_w = auto_pad_to_manual_pad(in_w, kw, sx, 1, self.auto_pad)

        return [
            MaxPooling2D(
                list(self.node.input),
                list(self.node.output),
                kernel=(kh, kw),
                stride=(sy, sx),
                pad_h=pad_h,
                pad_w=pad_w,
            )
        ]
