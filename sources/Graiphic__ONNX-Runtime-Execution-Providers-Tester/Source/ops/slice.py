# ops/slice.py
import numpy as np
import onnx
import onnx.helper
from utils import SpecialModelBuilders, SpecialInputGenerators, ONNX_RUNTIME_IR_VERSION, ONNX_OPSET_VERSION

def slice_model_builder(op_type, cfg=None):
    # Définition des entrées
    data = onnx.helper.make_tensor_value_info("data", onnx.TensorProto.FLOAT, [4, 5])
    starts = onnx.helper.make_tensor_value_info("starts", onnx.TensorProto.INT64, [2])
    ends = onnx.helper.make_tensor_value_info("ends", onnx.TensorProto.INT64, [2])
    axes = onnx.helper.make_tensor_value_info("axes", onnx.TensorProto.INT64, [2])
    steps = onnx.helper.make_tensor_value_info("steps", onnx.TensorProto.INT64, [2])
    output = onnx.helper.make_tensor_value_info("output", onnx.TensorProto.FLOAT, None)

    # Création du nœud Slice
    node = onnx.helper.make_node(
        "Slice",
        inputs=["data", "starts", "ends", "axes", "steps"],
        outputs=["output"]
    )

    # Construction du graphe et du modèle
    graph = onnx.helper.make_graph([node], "slice_graph", [data, starts, ends, axes, steps], [output])
    model = onnx.helper.make_model(
        graph,
        opset_imports=[onnx.helper.make_operatorsetid("", ONNX_OPSET_VERSION)]
    )
    model.ir_version = ONNX_RUNTIME_IR_VERSION
    return model

def slice_input_generator(session):
    inputs = session.get_inputs()
    feed = {}
    for inp in inputs:
        if inp.name == "data":
            feed[inp.name] = np.random.rand(4, 5).astype(np.float32)
        elif inp.name == "starts":
            feed[inp.name] = np.array([1, 0], dtype=np.int64)
        elif inp.name == "ends":
            feed[inp.name] = np.array([3, 4], dtype=np.int64)
        elif inp.name == "axes":
            feed[inp.name] = np.array([0, 1], dtype=np.int64)
        elif inp.name == "steps":
            feed[inp.name] = np.array([1, 2], dtype=np.int64)
    return feed

SpecialModelBuilders["Slice"] = slice_model_builder
SpecialInputGenerators["Slice"] = slice_input_generator
