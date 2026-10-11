# ops/binary.py
import numpy as np
import onnx
import onnx.helper
from utils import SpecialModelBuilders, SpecialInputGenerators, ONNX_RUNTIME_IR_VERSION, ONNX_OPSET_VERSION

# Familles d'opérateurs binaires
ARITHMETIC_OPS = ["Add", "Sub", "Mul", "Div", "Pow"]
BITWISE_OPS    = ["BitwiseAnd", "BitwiseOr", "BitwiseXor"]
LOGICAL_OPS    = ["And", "Or", "Xor"]

def arithmetic_model_builder(op_type, cfg=None):
    inp1 = onnx.helper.make_tensor_value_info("A", onnx.TensorProto.FLOAT, [2, 2])
    inp2 = onnx.helper.make_tensor_value_info("B", onnx.TensorProto.FLOAT, [2, 2])
    out  = onnx.helper.make_tensor_value_info("Y", onnx.TensorProto.FLOAT, None)

    node = onnx.helper.make_node(op_type, ["A", "B"], ["Y"])
    graph = onnx.helper.make_graph([node], f"{op_type}_graph", [inp1, inp2], [out])
    model = onnx.helper.make_model(graph, opset_imports=[onnx.helper.make_operatorsetid("", ONNX_OPSET_VERSION)])
    model.ir_version = ONNX_RUNTIME_IR_VERSION
    return model

def bitwise_model_builder(op_type, cfg=None):
    inp1 = onnx.helper.make_tensor_value_info("A", onnx.TensorProto.INT32, [2, 2])
    inp2 = onnx.helper.make_tensor_value_info("B", onnx.TensorProto.INT32, [2, 2])
    out  = onnx.helper.make_tensor_value_info("Y", onnx.TensorProto.INT32, None)

    node = onnx.helper.make_node(op_type, ["A", "B"], ["Y"])
    graph = onnx.helper.make_graph([node], f"{op_type}_graph", [inp1, inp2], [out])
    model = onnx.helper.make_model(graph, opset_imports=[onnx.helper.make_operatorsetid("", ONNX_OPSET_VERSION)])
    model.ir_version = ONNX_RUNTIME_IR_VERSION
    return model

def logical_model_builder(op_type, cfg=None):
    inp1 = onnx.helper.make_tensor_value_info("A", onnx.TensorProto.BOOL, [2, 2])
    inp2 = onnx.helper.make_tensor_value_info("B", onnx.TensorProto.BOOL, [2, 2])
    out  = onnx.helper.make_tensor_value_info("Y", onnx.TensorProto.BOOL, None)

    node = onnx.helper.make_node(op_type, ["A", "B"], ["Y"])
    graph = onnx.helper.make_graph([node], f"{op_type}_graph", [inp1, inp2], [out])
    model = onnx.helper.make_model(graph, opset_imports=[onnx.helper.make_operatorsetid("", ONNX_OPSET_VERSION)])
    model.ir_version = ONNX_RUNTIME_IR_VERSION
    return model

def binary_input_generator(session):
    input_infos = session.get_inputs()
    dtype = input_infos[0].type
    shape = [d or 1 for d in input_infos[0].shape]

    if dtype == 'tensor(float)':
        A = np.random.rand(*shape).astype(np.float32)
        B = np.random.rand(*shape).astype(np.float32)
    elif dtype == 'tensor(int32)':
        A = np.random.randint(0, 100, size=shape, dtype=np.int32)
        B = np.random.randint(0, 100, size=shape, dtype=np.int32)
    elif dtype == 'tensor(bool)':
        A = np.random.choice([True, False], size=shape)
        B = np.random.choice([True, False], size=shape)
    else:
        raise ValueError(f"Unsupported dtype: {dtype}")

    return {input_infos[0].name: A, input_infos[1].name: B}

# Enregistrement
for op in ARITHMETIC_OPS:
    SpecialModelBuilders[op] = arithmetic_model_builder
    SpecialInputGenerators[op] = binary_input_generator

for op in BITWISE_OPS:
    SpecialModelBuilders[op] = bitwise_model_builder
    SpecialInputGenerators[op] = binary_input_generator

for op in LOGICAL_OPS:
    SpecialModelBuilders[op] = logical_model_builder
    SpecialInputGenerators[op] = binary_input_generator
