# ops/split.py
import numpy as np
import onnx
import onnx.helper
from utils import SpecialModelBuilders, SpecialInputGenerators, ONNX_RUNTIME_IR_VERSION, ONNX_OPSET_VERSION

def split_model_builder(op_type, cfg=None):
    input_val = onnx.helper.make_tensor_value_info("input", onnx.TensorProto.FLOAT, [6, 4])
    split_val = onnx.helper.make_tensor_value_info("split", onnx.TensorProto.INT64, [3])
    outputs = [
        onnx.helper.make_tensor_value_info(f"Y{i}", onnx.TensorProto.FLOAT, None)
        for i in range(3)
    ]

    node = onnx.helper.make_node(
        "Split",
        inputs=["input", "split"],
        outputs=[f"Y{i}" for i in range(3)],
        axis=0  # split sur la première dimension
    )

    graph = onnx.helper.make_graph([node], "split_graph", [input_val, split_val], outputs)
    model = onnx.helper.make_model(
        graph,
        opset_imports=[onnx.helper.make_operatorsetid("", ONNX_OPSET_VERSION)]
    )
    model.ir_version = ONNX_RUNTIME_IR_VERSION
    return model

def split_input_generator(session):
    input_info, split_info = session.get_inputs()
    x = np.random.rand(6, 4).astype(np.float32)
    split = np.array([2, 2, 2], dtype=np.int64)
    return {input_info.name: x, split_info.name: split}

SpecialModelBuilders["Split"] = split_model_builder
SpecialInputGenerators["Split"] = split_input_generator
