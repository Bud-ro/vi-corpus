# ops/affinegrid.py
import numpy as np
import onnx
import onnx.helper
from utils import SpecialModelBuilders, SpecialInputGenerators, ONNX_RUNTIME_IR_VERSION, ONNX_OPSET_VERSION

def affinegrid_model_builder(op_type, cfg=None):
    theta = onnx.helper.make_tensor_value_info("theta", onnx.TensorProto.FLOAT, [1, 2, 3])
    size = onnx.helper.make_tensor_value_info("size", onnx.TensorProto.INT64, [4])
    grid = onnx.helper.make_tensor_value_info("grid", onnx.TensorProto.FLOAT, None)

    node = onnx.helper.make_node(
        "AffineGrid",
        inputs=["theta", "size"],
        outputs=["grid"],
        align_corners=True
    )

    graph = onnx.helper.make_graph([node], "affinegrid_graph", [theta, size], [grid])
    model = onnx.helper.make_model(
        graph,
        opset_imports=[onnx.helper.make_operatorsetid("", ONNX_OPSET_VERSION)]
    )
    model.ir_version = ONNX_RUNTIME_IR_VERSION
    return model

def affinegrid_input_generator(session):
    theta = np.array([[[1.0, 0.0, 0.0],
                       [0.0, 1.0, 0.0]]], dtype=np.float32)  # Identité 2D
    size = np.array([1, 1, 64, 64], dtype=np.int64)  # Batch=1, Canaux=1, Hauteur=64, Largeur=64
    return {
        "theta": theta,
        "size": size
    }

SpecialModelBuilders["AffineGrid"] = affinegrid_model_builder
SpecialInputGenerators["AffineGrid"] = affinegrid_input_generator
