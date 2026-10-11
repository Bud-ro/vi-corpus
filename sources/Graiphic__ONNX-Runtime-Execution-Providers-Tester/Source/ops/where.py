# ops/where.py
import numpy as np
import onnx
import onnx.helper
from utils import SpecialModelBuilders, SpecialInputGenerators, ONNX_RUNTIME_IR_VERSION, ONNX_OPSET_VERSION

def where_model_builder(op_type, cfg=None):
    cond = onnx.helper.make_tensor_value_info("condition", onnx.TensorProto.BOOL, [3, 3])
    x = onnx.helper.make_tensor_value_info("X", onnx.TensorProto.FLOAT, [3, 3])
    y = onnx.helper.make_tensor_value_info("Y", onnx.TensorProto.FLOAT, [3, 3])
    out = onnx.helper.make_tensor_value_info("Z", onnx.TensorProto.FLOAT, None)

    node = onnx.helper.make_node(
        "Where",
        inputs=["condition", "X", "Y"],
        outputs=["Z"]
    )

    graph = onnx.helper.make_graph(
        [node], "where_graph",
        [cond, x, y],
        [out]
    )

    model = onnx.helper.make_model(
        graph,
        opset_imports=[onnx.helper.make_operatorsetid("", ONNX_OPSET_VERSION)]
    )
    model.ir_version = ONNX_RUNTIME_IR_VERSION
    return model

def where_input_generator(session):
    cond_info, x_info, y_info = session.get_inputs()
    shape = [d if isinstance(d, int) else 1 for d in x_info.shape]
    condition = np.random.choice([True, False], size=shape)
    x = np.random.rand(*shape).astype(np.float32)
    y = np.random.rand(*shape).astype(np.float32)
    return {
        cond_info.name: condition,
        x_info.name: x,
        y_info.name: y
    }

SpecialModelBuilders["Where"] = where_model_builder
SpecialInputGenerators["Where"] = where_input_generator
