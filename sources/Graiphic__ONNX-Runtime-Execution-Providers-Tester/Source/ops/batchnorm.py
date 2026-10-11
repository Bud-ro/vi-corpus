# ops/batchnorm.py
import numpy as np
import onnx
import onnx.helper
from utils import SpecialModelBuilders, SpecialInputGenerators, ONNX_RUNTIME_IR_VERSION, ONNX_OPSET_VERSION

def batchnorm_model_builder(op_type, cfg=None):
    X     = onnx.helper.make_tensor_value_info("X",     onnx.TensorProto.FLOAT, [1, 3, 4, 4])
    scale = onnx.helper.make_tensor_value_info("scale", onnx.TensorProto.FLOAT, [3])
    bias  = onnx.helper.make_tensor_value_info("bias",  onnx.TensorProto.FLOAT, [3])
    mean  = onnx.helper.make_tensor_value_info("mean",  onnx.TensorProto.FLOAT, [3])
    var   = onnx.helper.make_tensor_value_info("var",   onnx.TensorProto.FLOAT, [3])
    Y     = onnx.helper.make_tensor_value_info("Y",     onnx.TensorProto.FLOAT, None)

    node = onnx.helper.make_node(
        "BatchNormalization",
        inputs=["X", "scale", "bias", "mean", "var"],
        outputs=["Y"],
        epsilon=1e-5,
        momentum=0.9
    )

    graph = onnx.helper.make_graph([node], "batchnorm_graph", [X, scale, bias, mean, var], [Y])
    model = onnx.helper.make_model(
        graph,
        opset_imports=[onnx.helper.make_operatorsetid("", ONNX_OPSET_VERSION)]
    )
    model.ir_version = ONNX_RUNTIME_IR_VERSION
    return model

def batchnorm_input_generator(session):
    X = np.random.rand(1, 3, 4, 4).astype(np.float32)
    scale = np.ones(3, dtype=np.float32)
    bias  = np.zeros(3, dtype=np.float32)
    mean  = np.random.rand(3).astype(np.float32)
    var   = np.random.rand(3).astype(np.float32) + 0.5  # éviter var ≈ 0
    return {
        "X": X,
        "scale": scale,
        "bias": bias,
        "mean": mean,
        "var": var
    }

SpecialModelBuilders["BatchNormalization"] = batchnorm_model_builder
SpecialInputGenerators["BatchNormalization"] = batchnorm_input_generator
