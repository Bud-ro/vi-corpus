# ops/spacetodepth.py
import numpy as np
import onnx
import onnx.helper
from onnx import TensorProto
from utils import SpecialModelBuilders, SpecialInputGenerators, ONNX_RUNTIME_IR_VERSION, ONNX_OPSET_VERSION

def spacetodepth_model_builder(op_type, cfg=None):
    blocksize = 2  # Vous pouvez ajuster cette valeur selon vos besoins
    input_tensor = onnx.helper.make_tensor_value_info("X", TensorProto.FLOAT, [1, 1, 4, 4])
    output_tensor = onnx.helper.make_tensor_value_info("Y", TensorProto.FLOAT, [1, 4, 2, 2])

    node = onnx.helper.make_node(
        "SpaceToDepth",
        inputs=["X"],
        outputs=["Y"],
        blocksize=blocksize
    )

    graph = onnx.helper.make_graph(
        nodes=[node],
        name="spacetodepth_graph",
        inputs=[input_tensor],
        outputs=[output_tensor]
    )

    model = onnx.helper.make_model(
        graph,
        opset_imports=[onnx.helper.make_operatorsetid("", ONNX_OPSET_VERSION)]
    )
    model.ir_version = ONNX_RUNTIME_IR_VERSION
    return model

def spacetodepth_input_generator(session):
    input_data = np.arange(1, 17, dtype=np.float32).reshape((1, 1, 4, 4))
    return {"X": input_data}

SpecialModelBuilders["SpaceToDepth"] = spacetodepth_model_builder
SpecialInputGenerators["SpaceToDepth"] = spacetodepth_input_generator
