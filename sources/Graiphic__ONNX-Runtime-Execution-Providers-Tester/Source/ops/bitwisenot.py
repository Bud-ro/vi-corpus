# ops/bitwisenot.py
import numpy as np
import onnx
import onnx.helper
from utils import SpecialModelBuilders, SpecialInputGenerators, ONNX_RUNTIME_IR_VERSION, ONNX_OPSET_VERSION

def bitwisenot_model_builder(op_type, cfg=None):
    inp = onnx.helper.make_tensor_value_info("X", onnx.TensorProto.INT32, [3, 3])
    out = onnx.helper.make_tensor_value_info("Y", onnx.TensorProto.INT32, None)

    node = onnx.helper.make_node(
        "BitwiseNot",
        inputs=["X"],
        outputs=["Y"]
    )

    graph = onnx.helper.make_graph(
        [node],
        "bitwisenot_graph",
        [inp],
        [out]
    )

    model = onnx.helper.make_model(
        graph,
        opset_imports=[onnx.helper.make_operatorsetid("", ONNX_OPSET_VERSION)]
    )
    model.ir_version = ONNX_RUNTIME_IR_VERSION
    return model

SpecialModelBuilders["BitwiseNot"] = bitwisenot_model_builder

def bitwisenot_input_generator(session):
    x_info = session.get_inputs()[0]
    shape = [d or 1 for d in x_info.shape]
    x = np.random.randint(0, 256, size=shape, dtype=np.int32)
    return {x_info.name: x}

SpecialInputGenerators["BitwiseNot"] = bitwisenot_input_generator
