# onnx2mlir

onnx2mlir is a converter from onnx model to mlir model.

## Supported ONNX Model

A model must be runnable by [onnxruntime](https://pypi.org/project/onnxruntime/).

## Supported ONNX Operators

* [Add](https://github.com/onnx/onnx/blob/master/docs/Operators.md#Add)
* [AveragePool](https://github.com/onnx/onnx/blob/master/docs/Operators.md#AveragePool)
* [BatchNormalization](https://github.com/onnx/onnx/blob/master/docs/Operators.md#BatchNormalization)
* [Clip](https://github.com/onnx/onnx/blob/master/docs/Operators.md#Clip)
    * `min` must be 0
* [Concat](https://github.com/onnx/onnx/blob/master/docs/Operators.md#Concat)
* [Conv](https://github.com/onnx/onnx/blob/master/docs/Operators.md#Conv)
    * `W` must be [Constant](https://github.com/onnx/onnx/blob/master/docs/Operators.md#Constant) value or have initializer value
    * `b` must be [Constant](https://github.com/onnx/onnx/blob/master/docs/Operators.md#Constant) value or have initializer value
* [Dropout](https://github.com/onnx/onnx/blob/master/docs/Operators.md#Dropout)
    * equivalent identity function
* [Gemm](https://github.com/onnx/onnx/blob/master/docs/Operators.md#Gemm)
    * `B` must be [Constant](https://github.com/onnx/onnx/blob/master/docs/Operators.md#Constant) value or have initializer value
    * `C` must be [Constant](https://github.com/onnx/onnx/blob/master/docs/Operators.md#Constant) value or have initializer value
* [LRN](https://github.com/onnx/onnx/blob/master/docs/Operators.md#LRN)
* [MatMul](https://github.com/onnx/onnx/blob/master/docs/Operators.md#MatMul)
    * `B` must be [Constant](https://github.com/onnx/onnx/blob/master/docs/Operators.md#Constant) value or have initializer value
* [MaxPool](https://github.com/onnx/onnx/blob/master/docs/Operators.md#MaxPool)
* [Pad](https://github.com/onnx/onnx/blob/master/docs/Operators.md#Pad)
    * `mode` must be `"constant"`
* [Relu](https://github.com/onnx/onnx/blob/master/docs/Operators.md#Relu)
* [Reshape](https://github.com/onnx/onnx/blob/master/docs/Operators.md#Reshape)
* [Softmax](https://github.com/onnx/onnx/blob/master/docs/Operators.md#Softmax)
* [Sum](https://github.com/onnx/onnx/blob/master/docs/Operators.md#Sum)
    * 2 inputs
* [Transpose](https://github.com/onnx/onnx/blob/master/docs/Operators.md#Transpose)

## Example

~~~~bash
wget https://www.cntk.ai/OnnxModels/mnist/opset_7/mnist.tar.gz
tar xvzf mnist.tar.gz
onnx2mlir -o model.mlir mnist/model.onnx
~~~~