# ops/cast.py
import numpy as np
import onnx
import onnx.helper
from utils import SpecialModelBuilders, SpecialInputGenerators, ONNX_RUNTIME_IR_VERSION, ONNX_OPSET_VERSION

def cast_model_builder(op_type, cfg=None):
    inp = onnx.helper.make_tensor_value_info("X", onnx.TensorProto.FLOAT, [2, 2])
    out = onnx.helper.make_tensor_value_info("Y", onnx.TensorProto.DOUBLE, None)

    node = onnx.helper.make_node(
        "Cast",
        inputs=["X"],
        outputs=["Y"],
        to=onnx.TensorProto.DOUBLE  # on peut paramétrer ce type via `cfg` si besoin
    )

    graph = onnx.helper.make_graph(
        [node],
        "cast_graph",
        [inp],
        [out]
    )

    model = onnx.helper.make_model(
        graph,
        opset_imports=[onnx.helper.make_operatorsetid("", ONNX_OPSET_VERSION)]
    )
    model.ir_version = ONNX_RUNTIME_IR_VERSION
    return model

SpecialModelBuilders["Cast"] = cast_model_builder

def cast_input_generator(session):
    x_info = session.get_inputs()[0]
    shape = [d or 1 for d in x_info.shape]
    x = np.random.rand(*shape).astype(np.float32)
    return {x_info.name: x}

SpecialInputGenerators["Cast"] = cast_input_generator
