# ops/shape.py
import numpy as np
import onnx
import onnx.helper
from onnx import TensorProto
from utils import SpecialModelBuilders, SpecialInputGenerators, ONNX_RUNTIME_IR_VERSION, ONNX_OPSET_VERSION

def shape_model_builder(op_type, cfg=None):
    # Définition de l'entrée
    input_tensor = onnx.helper.make_tensor_value_info("X", TensorProto.FLOAT, [2, 3, 4])
    # Définition de la sortie
    output_tensor = onnx.helper.make_tensor_value_info("shape_out", TensorProto.INT64, [3])

    # Création du nœud Shape
    node = onnx.helper.make_node(
        "Shape",
        inputs=["X"],
        outputs=["shape_out"]
        # Attributs optionnels 'start' et 'end' peuvent être ajoutés ici si nécessaire
    )

    # Construction du graphe
    graph = onnx.helper.make_graph(
        nodes=[node],
        name="shape_graph",
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

def shape_input_generator(session):
    # Génération d'un tenseur d'entrée aléatoire de forme [2, 3, 4]
    input_data = np.random.rand(2, 3, 4).astype(np.float32)
    return {"X": input_data}

# Enregistrement des fonctions dans les dictionnaires
SpecialModelBuilders["Shape"] = shape_model_builder
SpecialInputGenerators["Shape"] = shape_input_generator
