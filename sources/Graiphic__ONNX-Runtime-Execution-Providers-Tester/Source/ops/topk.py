# ops/topk.py
import numpy as np
import onnx
import onnx.helper
from utils import SpecialModelBuilders, SpecialInputGenerators, ONNX_RUNTIME_IR_VERSION, ONNX_OPSET_VERSION

def topk_model_builder(op_type, cfg=None):
    X = onnx.helper.make_tensor_value_info("X", onnx.TensorProto.FLOAT, [5, 10])
    K = onnx.helper.make_tensor_value_info("K", onnx.TensorProto.INT64, [1])
    values = onnx.helper.make_tensor_value_info("Values", onnx.TensorProto.FLOAT, None)
    indices = onnx.helper.make_tensor_value_info("Indices", onnx.TensorProto.INT64, None)

    node = onnx.helper.make_node(
        "TopK",
        inputs=["X", "K"],
        outputs=["Values", "Indices"],
        axis=1,
        largest=1,
        sorted=1
    )

    graph = onnx.helper.make_graph(
        [node], "topk_graph",
        [X, K],
        [values, indices]
    )

    model = onnx.helper.make_model(
        graph,
        opset_imports=[onnx.helper.make_operatorsetid("", ONNX_OPSET_VERSION)]
    )
    model.ir_version = ONNX_RUNTIME_IR_VERSION
    return model

def topk_input_generator(session):
    X_info, K_info = session.get_inputs()
    shape = [d if isinstance(d, int) else 1 for d in X_info.shape]
    X = np.random.rand(*shape).astype(np.float32)
    K = np.array([3], dtype=np.int64)  # On veut top-3
    return {X_info.name: X, K_info.name: K}

SpecialModelBuilders["TopK"] = topk_model_builder
SpecialInputGenerators["TopK"] = topk_input_generator
