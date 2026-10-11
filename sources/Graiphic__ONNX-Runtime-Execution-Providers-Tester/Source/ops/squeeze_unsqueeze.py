# ops/squeeze_unsqueeze.py
import numpy as np
import onnx
import onnx.helper
from utils import SpecialModelBuilders, SpecialInputGenerators, ONNX_RUNTIME_IR_VERSION, ONNX_OPSET_VERSION

def squeeze_model_builder(op_type=None, cfg=None):
    # Entrée utile : data
    data = onnx.helper.make_tensor_value_info("data", onnx.TensorProto.FLOAT, [1, 3, 1])
    out = onnx.helper.make_tensor_value_info("output", onnx.TensorProto.FLOAT, [3])
    
    # Ajout d'une ValueInfo facultative pour axes
    axes_value_info = onnx.helper.make_tensor_value_info("axes", onnx.TensorProto.INT64, [2])

    # Initializer pour axes = [0, 2]
    axes_initializer = onnx.helper.make_tensor(
        name="axes",
        data_type=onnx.TensorProto.INT64,
        dims=[2],
        vals=np.array([0, 2], dtype=np.int64)
    )

    # Création du nœud avec axes en entrée (mais statique via initializer)
    node = onnx.helper.make_node(
        "Squeeze",
        inputs=["data", "axes"],
        outputs=["output"]
    )

    # Construction du graph (pas besoin d’input explicite pour 'axes')
    graph = onnx.helper.make_graph(
        [node],
        "squeeze_graph",
        [data],  # seule entrée dynamique
        [out],
        initializer=[axes_initializer],
        value_info=[axes_value_info]  # bonne pratique pour la clarté
    )

    model = onnx.helper.make_model(
        graph,
        opset_imports=[onnx.helper.make_operatorsetid("", ONNX_OPSET_VERSION)]
    )
    model.ir_version = ONNX_RUNTIME_IR_VERSION
    return model

def squeeze_input_generator(session):
    data_info = session.get_inputs()[0]
    data = np.random.rand(1, 3, 1).astype(np.float32)
    return {data_info.name: data}

def unsqueeze_model_builder(op_type, cfg=None):
    data = onnx.helper.make_tensor_value_info("data", onnx.TensorProto.FLOAT, [3])
    axes = onnx.helper.make_tensor_value_info("axes", onnx.TensorProto.INT64, [1])
    out = onnx.helper.make_tensor_value_info("output", onnx.TensorProto.FLOAT, None)

    node = onnx.helper.make_node("Unsqueeze", ["data", "axes"], ["output"])

    graph = onnx.helper.make_graph([node], "unsqueeze_graph", [data, axes], [out])
    model = onnx.helper.make_model(
        graph,
        opset_imports=[onnx.helper.make_operatorsetid("", ONNX_OPSET_VERSION)]
    )
    model.ir_version = ONNX_RUNTIME_IR_VERSION
    return model

def unsqueeze_input_generator(session):
    data_info, axes_info = session.get_inputs()
    data = np.random.rand(3).astype(np.float32)
    axes = np.array([0], dtype=np.int64)
    return {data_info.name: data, axes_info.name: axes}

SpecialModelBuilders["Squeeze"] = squeeze_model_builder
SpecialInputGenerators["Squeeze"] = squeeze_input_generator
SpecialModelBuilders["Unsqueeze"] = unsqueeze_model_builder
SpecialInputGenerators["Unsqueeze"] = unsqueeze_input_generator
