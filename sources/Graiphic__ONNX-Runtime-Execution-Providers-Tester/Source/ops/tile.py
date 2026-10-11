# ops/tile.py
import numpy as np
import onnx
import onnx.helper
from utils import SpecialModelBuilders, SpecialInputGenerators, ONNX_RUNTIME_IR_VERSION, ONNX_OPSET_VERSION

def tile_model_builder(op_type, cfg=None):
    input_val = onnx.helper.make_tensor_value_info("input", onnx.TensorProto.FLOAT, [2, 2])
    repeats_val = onnx.helper.make_tensor_value_info("repeats", onnx.TensorProto.INT64, [2])
    output_val = onnx.helper.make_tensor_value_info("output", onnx.TensorProto.FLOAT, None)

    node = onnx.helper.make_node(
        "Tile",
        inputs=["input", "repeats"],
        outputs=["output"]
    )

    graph = onnx.helper.make_graph([node], "tile_graph", [input_val, repeats_val], [output_val])
    model = onnx.helper.make_model(
        graph,
        opset_imports=[onnx.helper.make_operatorsetid("", ONNX_OPSET_VERSION)]
    )
    model.ir_version = ONNX_RUNTIME_IR_VERSION
    return model

def tile_input_generator(session):
    input_info, repeats_info = session.get_inputs()
    x = np.random.rand(2, 2).astype(np.float32)
    repeats = np.array([2, 3], dtype=np.int64)  # Repeat 2 times on axis 0, 3 times on axis 1
    return {input_info.name: x, repeats_info.name: repeats}

SpecialModelBuilders["Tile"] = tile_model_builder
SpecialInputGenerators["Tile"] = tile_input_generator
