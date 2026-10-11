# ops/nary_elementwise.py
import numpy as np
import onnx
import onnx.helper
from utils import SpecialModelBuilders, SpecialInputGenerators, ONNX_RUNTIME_IR_VERSION, ONNX_OPSET_VERSION

NARY_OPS = ["Max", "Min", "Mean", "Sum"]

def nary_model_builder(op_type, cfg=None):
    input_names = [f"X{i}" for i in range(3)]
    inputs = [
        onnx.helper.make_tensor_value_info(name, onnx.TensorProto.FLOAT, [2, 2])
        for name in input_names
    ]
    output = onnx.helper.make_tensor_value_info("Y", onnx.TensorProto.FLOAT, None)

    node = onnx.helper.make_node(op_type, inputs=input_names, outputs=["Y"])

    graph = onnx.helper.make_graph([node], f"{op_type}_graph", inputs, [output])
    model = onnx.helper.make_model(
        graph,
        opset_imports=[onnx.helper.make_operatorsetid("", ONNX_OPSET_VERSION)]
    )
    model.ir_version = ONNX_RUNTIME_IR_VERSION
    return model

def nary_input_generator(session):
    feed = {}
    for inp in session.get_inputs():
        shape = [d if isinstance(d, int) else 1 for d in inp.shape]
        feed[inp.name] = np.random.rand(*shape).astype(np.float32)
    return feed

for op_type in NARY_OPS:
    SpecialModelBuilders[op_type] = nary_model_builder
    SpecialInputGenerators[op_type] = nary_input_generator
