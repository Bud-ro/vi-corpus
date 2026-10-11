# ops/averagepool.py
import numpy as np
import onnx
import onnx.helper
from utils import SpecialModelBuilders, SpecialInputGenerators, ONNX_RUNTIME_IR_VERSION, ONNX_OPSET_VERSION

def averagepool_model_builder(op_type, cfg=None):
    X = onnx.helper.make_tensor_value_info("X", onnx.TensorProto.FLOAT, [1, 3, 32, 32])
    Y = onnx.helper.make_tensor_value_info("Y", onnx.TensorProto.FLOAT, None)

    node = onnx.helper.make_node(
        "AveragePool",
        inputs=["X"],
        outputs=["Y"],
        kernel_shape=[2, 2],
        strides=[2, 2],
        pads=[0, 0, 0, 0],
        ceil_mode=0,
        count_include_pad=0
    )

    graph = onnx.helper.make_graph([node], "averagepool_graph", [X], [Y])
    model = onnx.helper.make_model(
        graph,
        opset_imports=[onnx.helper.make_operatorsetid("", ONNX_OPSET_VERSION)]
    )
    model.ir_version = ONNX_RUNTIME_IR_VERSION
    return model

def averagepool_input_generator(session):
    X = np.random.rand(1, 3, 32, 32).astype(np.float32)
    return {"X": X}

SpecialModelBuilders["AveragePool"] = averagepool_model_builder
SpecialInputGenerators["AveragePool"] = averagepool_input_generator
