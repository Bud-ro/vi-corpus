# ops/sequenceconstruct.py
import numpy as np
import onnx
import onnx.helper
from utils import SpecialModelBuilders, SpecialInputGenerators, ONNX_RUNTIME_IR_VERSION, ONNX_OPSET_VERSION

from onnx import helper, TensorProto, ValueInfoProto, TypeProto

def make_sequence_value_info(name, elem_type):
    t = TypeProto()
    t.sequence_type.elem_type.tensor_type.elem_type = elem_type
    vi = ValueInfoProto()
    vi.name = name
    vi.type.CopyFrom(t)
    return vi


def sequenceconstruct_model_builder(op_type, cfg=None):
    input_names = ['X1', 'X2', 'X3']
    inputs = [
        onnx.helper.make_tensor_value_info(name, onnx.TensorProto.FLOAT, [2, 2])
        for name in input_names
    ]
    output = make_sequence_value_info("seq_out", onnx.TensorProto.FLOAT)

    node = onnx.helper.make_node(
        "SequenceConstruct",
        inputs=input_names,
        outputs=["seq_out"]
    )

    graph = onnx.helper.make_graph([node], "sequenceconstruct_graph", inputs, [output])
    model = onnx.helper.make_model(
        graph,
        opset_imports=[onnx.helper.make_operatorsetid("", ONNX_OPSET_VERSION)]
    )
    model.ir_version = ONNX_RUNTIME_IR_VERSION
    return model

def sequenceconstruct_input_generator(session):
    inputs = session.get_inputs()
    feed = {}
    for inp in inputs:
        shape = [d if isinstance(d, int) else 1 for d in inp.shape]
        feed[inp.name] = np.random.rand(*shape).astype(np.float32)
    return feed

SpecialModelBuilders["SequenceConstruct"] = sequenceconstruct_model_builder
SpecialInputGenerators["SequenceConstruct"] = sequenceconstruct_input_generator
