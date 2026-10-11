# ops/arg_ops.py
import numpy as np
import onnx
import onnx.helper
from utils import SpecialModelBuilders, SpecialInputGenerators, ONNX_RUNTIME_IR_VERSION, ONNX_OPSET_VERSION

ARG_OPS = ["ArgMax", "ArgMin"]

def arg_model_builder(op_type, cfg=None):
    # Définition de l'entrée et de la sortie
    inp = onnx.helper.make_tensor_value_info("X", onnx.TensorProto.FLOAT, [3, 4, 5])
    out = onnx.helper.make_tensor_value_info("Y", onnx.TensorProto.INT64, None)

    # Création du nœud avec les attributs axis, keepdims et select_last_index
    node = onnx.helper.make_node(
        op_type,
        inputs=["X"],
        outputs=["Y"],
        axis=1,
        keepdims=1,
        select_last_index=0
    )

    # Construction du graphe et du modèle
    graph = onnx.helper.make_graph([node], f"{op_type}_graph", [inp], [out])
    model = onnx.helper.make_model(
        graph,
        opset_imports=[onnx.helper.make_operatorsetid("", ONNX_OPSET_VERSION)]
    )
    model.ir_version = ONNX_RUNTIME_IR_VERSION
    return model

def arg_input_generator(session):
    # Génération d'un tenseur d'entrée aléatoire
    inp_info = session.get_inputs()[0]
    shape = [d if isinstance(d, int) else 1 for d in inp_info.shape]
    X = np.random.rand(*shape).astype(np.float32)
    return {inp_info.name: X}

# Enregistrement des builders et générateurs pour chaque opérateur
for op_type in ARG_OPS:
    SpecialModelBuilders[op_type] = arg_model_builder
    SpecialInputGenerators[op_type] = arg_input_generator
