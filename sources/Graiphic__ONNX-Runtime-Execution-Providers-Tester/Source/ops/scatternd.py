# ops/scatternd.py
import numpy as np
import onnx
import onnx.helper
from utils import SpecialModelBuilders, SpecialInputGenerators, ONNX_RUNTIME_IR_VERSION, ONNX_OPSET_VERSION

def scatternd_model_builder(op_type, cfg=None):
    data = onnx.helper.make_tensor_value_info("data", onnx.TensorProto.FLOAT, [4, 4])
    indices = onnx.helper.make_tensor_value_info("indices", onnx.TensorProto.INT64, [2, 1])
    updates = onnx.helper.make_tensor_value_info("updates", onnx.TensorProto.FLOAT, [2, 4])
    output = onnx.helper.make_tensor_value_info("output", onnx.TensorProto.FLOAT, None)

    node = onnx.helper.make_node(
        "ScatterND",
        inputs=["data", "indices", "updates"],
        outputs=["output"],
        reduction = "none"
    )

    graph = onnx.helper.make_graph([node], "scatternd_graph", [data, indices, updates], [output])
    model = onnx.helper.make_model(
        graph,
        opset_imports=[onnx.helper.make_operatorsetid("", ONNX_OPSET_VERSION)]
    )
    model.ir_version = ONNX_RUNTIME_IR_VERSION
    return model

def scatternd_input_generator(session):
    data_info, indices_info, updates_info = session.get_inputs()
    data = np.zeros((4, 4), dtype=np.float32)
    indices = np.array([[1], [3]], dtype=np.int64)  # On cible les lignes 1 et 3
    updates = np.random.rand(2, 4).astype(np.float32)
    return {
        data_info.name: data,
        indices_info.name: indices,
        updates_info.name: updates
    }



SpecialModelBuilders["ScatterND"] = scatternd_model_builder
SpecialInputGenerators["ScatterND"] = scatternd_input_generator
