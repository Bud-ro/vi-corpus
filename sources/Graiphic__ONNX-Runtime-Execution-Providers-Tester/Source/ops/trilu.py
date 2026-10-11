# ops/trilu.py
import numpy as np
import onnx
import onnx.helper
from utils import SpecialModelBuilders, SpecialInputGenerators, ONNX_RUNTIME_IR_VERSION, ONNX_OPSET_VERSION

def trilu_model_builder(op_type, cfg=None):
    X = onnx.helper.make_tensor_value_info("X", onnx.TensorProto.FLOAT, [4, 4])
    K = onnx.helper.make_tensor_value_info("k", onnx.TensorProto.INT64, [1])
    Y = onnx.helper.make_tensor_value_info("Y", onnx.TensorProto.FLOAT, None)

    node = onnx.helper.make_node(
        "Trilu",
        inputs=["X", "k"],
        outputs=["Y"],
        upper=1  # 1 = upper triangle; 0 = lower triangle
    )

    graph = onnx.helper.make_graph(
        [node], "trilu_graph",
        [X, K],
        [Y]
    )

    model = onnx.helper.make_model(
        graph,
        opset_imports=[onnx.helper.make_operatorsetid("", ONNX_OPSET_VERSION)]
    )
    model.ir_version = ONNX_RUNTIME_IR_VERSION
    return model

def trilu_input_generator(session):
    X_info, K_info = session.get_inputs()
    shape = [d if isinstance(d, int) else 1 for d in X_info.shape]
    X = np.random.rand(*shape).astype(np.float32)
    k = np.array([0], dtype=np.int64)  # Diagonale principale
    return {X_info.name: X, K_info.name: k}

SpecialModelBuilders["Trilu"] = trilu_model_builder
SpecialInputGenerators["Trilu"] = trilu_input_generator
