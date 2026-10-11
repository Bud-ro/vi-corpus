# ops/unary_bool.py
import numpy as np
import onnx
import onnx.helper
from utils import SpecialModelBuilders, SpecialInputGenerators, ONNX_RUNTIME_IR_VERSION, ONNX_OPSET_VERSION

UNARY_BOOL_OPS = ["Not", "IsNaN", "IsInf"]

def unary_bool_model_builder(op_type, cfg=None):
    if op_type == "Not":
        input_type = onnx.TensorProto.BOOL
    else:
        input_type = onnx.TensorProto.FLOAT

    inp = onnx.helper.make_tensor_value_info("X", input_type, [2, 3])
    out = onnx.helper.make_tensor_value_info("Y", onnx.TensorProto.BOOL, None)

    node = onnx.helper.make_node(op_type, ["X"], ["Y"])

    graph = onnx.helper.make_graph([node], f"{op_type}_graph", [inp], [out])
    model = onnx.helper.make_model(
        graph,
        opset_imports=[onnx.helper.make_operatorsetid("", ONNX_OPSET_VERSION)]
    )
    model.ir_version = ONNX_RUNTIME_IR_VERSION
    return model

def unary_bool_input_generator(session):
    input_info = session.get_inputs()[0]
    shape = [d if isinstance(d, int) else 1 for d in input_info.shape]
    dtype = input_info.type

    if dtype == 'tensor(bool)':
        X = np.random.choice([True, False], size=shape)
    else:
        X = np.random.randn(*shape).astype(np.float32)
        if session.get_inputs()[0].name == "IsNaN":
            X[0, 0] = np.nan
        elif session.get_inputs()[0].name == "IsInf":
            X[0, 0] = np.inf

    return {input_info.name: X}

for op_type in UNARY_BOOL_OPS:
    SpecialModelBuilders[op_type] = unary_bool_model_builder
    SpecialInputGenerators[op_type] = unary_bool_input_generator
