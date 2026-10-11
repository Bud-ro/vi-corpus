# ops/unique.py
import numpy as np
import onnx
import onnx.helper
from utils import SpecialModelBuilders, SpecialInputGenerators, ONNX_RUNTIME_IR_VERSION, ONNX_OPSET_VERSION

def unique_model_builder(op_type, cfg=None):
    X = onnx.helper.make_tensor_value_info("X", onnx.TensorProto.INT64, [10])
    Y = onnx.helper.make_tensor_value_info("Y", onnx.TensorProto.INT64, None)
    indices = onnx.helper.make_tensor_value_info("indices", onnx.TensorProto.INT64, None)
    inverse_indices = onnx.helper.make_tensor_value_info("inverse_indices", onnx.TensorProto.INT64, None)
    counts = onnx.helper.make_tensor_value_info("counts", onnx.TensorProto.INT64, None)

    node = onnx.helper.make_node(
        "Unique",
        inputs=["X"],
        outputs=["Y", "indices", "inverse_indices", "counts"],
        axis=0
    )

    graph = onnx.helper.make_graph(
        [node], "unique_graph",
        [X],
        [Y, indices, inverse_indices, counts]
    )

    model = onnx.helper.make_model(
        graph,
        opset_imports=[onnx.helper.make_operatorsetid("", ONNX_OPSET_VERSION)]
    )
    model.ir_version = ONNX_RUNTIME_IR_VERSION
    return model

def unique_input_generator(session):
    X_info = session.get_inputs()[0]
    data = np.random.randint(0, 5, size=10).astype(np.int64)
    return {X_info.name: data}

SpecialModelBuilders["Unique"] = unique_model_builder
SpecialInputGenerators["Unique"] = unique_input_generator
