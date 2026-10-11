# ops/upsample.py
import numpy as np
import onnx
import onnx.helper
from utils import SpecialModelBuilders, SpecialInputGenerators, ONNX_RUNTIME_IR_VERSION, ONNX_OPSET_VERSION

def upsample_model_builder(op_type, cfg=None):
    inp  = onnx.helper.make_tensor_value_info("X", onnx.TensorProto.FLOAT, [1, 1, 2, 2])
    out  = onnx.helper.make_tensor_value_info("Y", onnx.TensorProto.FLOAT, None)
    
    scales = onnx.helper.make_tensor("scales", onnx.TensorProto.FLOAT, [4], [1.0, 1.0, 2.0, 2.0])
    
    node = onnx.helper.make_node(
        "Upsample",
        inputs=["X", "scales"],
        outputs=["Y"],
        mode="nearest"  # ou "linear" selon le test voulu
    )
    
    graph = onnx.helper.make_graph(
        [node],
        "upsample_graph",
        [inp],
        [out],
        initializer=[scales]
    )
    
    model = onnx.helper.make_model(
        graph,
        opset_imports=[onnx.helper.make_operatorsetid("", 10)]  # Upsample n'est défini que jusqu'à opset 10
    )
    model.ir_version = ONNX_RUNTIME_IR_VERSION
    return model

SpecialModelBuilders["Upsample"] = upsample_model_builder

def upsample_input_generator(session):
    x_info = session.get_inputs()[0]
    shape = [d or 1 for d in x_info.shape]
    x = np.random.rand(*shape).astype(np.float32)
    return {x_info.name: x}

SpecialInputGenerators["Upsample"] = upsample_input_generator
