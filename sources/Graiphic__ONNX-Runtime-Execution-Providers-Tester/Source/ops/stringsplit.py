# ops/stringsplit.py
import numpy as np
import onnx
import onnx.helper
from onnx import TensorProto
from utils import SpecialModelBuilders, SpecialInputGenerators, ONNX_RUNTIME_IR_VERSION, ONNX_OPSET_VERSION

def stringsplit_model_builder(op_type, cfg=None):
    # Définition de l'entrée
    input_tensor = onnx.helper.make_tensor_value_info("X", TensorProto.STRING, [None])
    # Définition des sorties
    output_tensor = onnx.helper.make_tensor_value_info("Y", TensorProto.STRING, [None, None])
    output_lengths = onnx.helper.make_tensor_value_info("Z", TensorProto.INT64, [None])

    # Création du nœud StringSplit
    node = onnx.helper.make_node(
        "StringSplit",
        inputs=["X"],
        outputs=["Y", "Z"],
        delimiter=" ",  # Vous pouvez ajuster le délimiteur selon vos besoins
        maxsplit=2      # Vous pouvez ajuster maxsplit selon vos besoins
    )

    # Construction du graphe
    graph = onnx.helper.make_graph(
        nodes=[node],
        name="stringsplit_graph",
        inputs=[input_tensor],
        outputs=[output_tensor, output_lengths]
    )

    # Création du modèle
    model = onnx.helper.make_model(
        graph,
        opset_imports=[onnx.helper.make_operatorsetid("", ONNX_OPSET_VERSION)]
    )
    model.ir_version = ONNX_RUNTIME_IR_VERSION
    return model

def stringsplit_input_generator(session):
    # Génération d'un tenseur d'entrée avec des chaînes de caractères
    input_data = np.array(["Bonjour le monde", "ONNX est génial", "Test de StringSplit"], dtype=object)
    return {"X": input_data}

# Enregistrement des fonctions dans les dictionnaires
SpecialModelBuilders["StringSplit"] = stringsplit_model_builder
SpecialInputGenerators["StringSplit"] = stringsplit_input_generator
