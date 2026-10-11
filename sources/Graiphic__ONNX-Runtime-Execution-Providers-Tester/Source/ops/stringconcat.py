# ops/stringconcat.py
import numpy as np
import onnx
import onnx.helper
from onnx import TensorProto
from utils import SpecialModelBuilders, SpecialInputGenerators, ONNX_RUNTIME_IR_VERSION, ONNX_OPSET_VERSION

def stringconcat_model_builder(op_type, cfg=None):
    input1 = onnx.helper.make_tensor_value_info("X", TensorProto.STRING, ["N"])
    input2 = onnx.helper.make_tensor_value_info("Y", TensorProto.STRING, ["N"])
    output = onnx.helper.make_tensor_value_info("Z", TensorProto.STRING, ["N"])

    node = onnx.helper.make_node(
        "StringConcat",
        inputs=["X", "Y"],
        outputs=["Z"]
    )

    graph = onnx.helper.make_graph(
        nodes=[node],
        name="stringconcat_graph",
        inputs=[input1, input2],
        outputs=[output]
    )

    model = onnx.helper.make_model(
        graph,
        opset_imports=[onnx.helper.make_operatorsetid("", 20)]
    )
    model.ir_version = ONNX_RUNTIME_IR_VERSION
    return model

def stringconcat_input_generator(session):
    inputs = session.get_inputs()
    feed = {}
    for inp in inputs:
        shape = [d if isinstance(d, int) else 3 for d in inp.shape]
        if inp.name == "X":
            feed[inp.name] = np.array(["foo", "bar", "baz"], dtype=object)
        elif inp.name == "Y":
            feed[inp.name] = np.array(["1", "2", "3"], dtype=object)
    return feed

SpecialModelBuilders["StringConcat"] = stringconcat_model_builder
SpecialInputGenerators["StringConcat"] = stringconcat_input_generator
