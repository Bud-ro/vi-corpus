# ops/size.py
import numpy as np
import onnx
import onnx.helper
from onnx import TensorProto
from utils import SpecialModelBuilders, SpecialInputGenerators, ONNX_RUNTIME_IR_VERSION, ONNX_OPSET_VERSION

def size_model_builder(op_type, cfg=None):
    # Définition de l'entrée
    input_tensor = onnx.helper.make_tensor_value_info("X", TensorProto.FLOAT, [2, 3, 4])
    # Définition de la sortie
    output_tensor = onnx.helper.make_tensor_value_info("size_out", TensorProto.INT64, [])

    # Création du nœud Size
    node = onnx.helper.make_node(
        "Size",
        inputs=["X"],
        outputs=["size_out"]
    )

    # Construction du graphe
    graph = onnx.helper.make_graph(
        nodes=[node],
        name="size_graph",
        inputs=[input_tensor],
        outputs=[output_tensor]
    )

    # Création du modèle
    model = onnx.helper.make_model(
        graph,
        opset_imports=[onnx.helper.make_operatorsetid("", ONNX_OPSET_VERSION)]
    )
    model.ir_version = ONNX_RUNTIME_IR_VERSION
    return model

def size_input_generator(session):
    # Génération d'un tenseur d'entrée aléatoire de forme [2, 3, 4]
    input_data = np.random.rand(2, 3, 4).astype(np.float32)
    return {"X": input_data}

# Enregistrement des fonctions dans les dictionnaires
SpecialModelBuilders["Size"] = size_model_builder
SpecialInputGenerators["Size"] = size_input_generator
