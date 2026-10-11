# ops/bitshift.py
import numpy as np
import onnx
import onnx.helper
from utils import SpecialModelBuilders, SpecialInputGenerators, ONNX_RUNTIME_IR_VERSION, ONNX_OPSET_VERSION

def bitshift_model_builder(op_type, cfg=None):
    x1 = onnx.helper.make_tensor_value_info("X", onnx.TensorProto.UINT32, [2, 2])
    x2 = onnx.helper.make_tensor_value_info("Y", onnx.TensorProto.UINT32, [2, 2])
    out = onnx.helper.make_tensor_value_info("Z", onnx.TensorProto.UINT32, None)

    node = onnx.helper.make_node(
        "BitShift",
        inputs=["X", "Y"],
        outputs=["Z"],
        direction="LEFT"  # ou "RIGHT"
    )

    graph = onnx.helper.make_graph(
        [node],
        "bitshift_graph",
        [x1, x2],
        [out]
    )

    model = onnx.helper.make_model(
        graph,
        opset_imports=[onnx.helper.make_operatorsetid("", ONNX_OPSET_VERSION)]
    )
    model.ir_version = ONNX_RUNTIME_IR_VERSION
    return model

SpecialModelBuilders["BitShift"] = bitshift_model_builder

def bitshift_input_generator(session):
    x_info, y_info = session.get_inputs()
    shape = [d or 1 for d in x_info.shape]
    x = np.random.randint(1, 64, size=shape, dtype=np.uint32)
    y = np.random.randint(0, 5, size=shape, dtype=np.uint32)  # décalages raisonnables
    return {x_info.name: x, y_info.name: y}

SpecialInputGenerators["BitShift"] = bitshift_input_generator
