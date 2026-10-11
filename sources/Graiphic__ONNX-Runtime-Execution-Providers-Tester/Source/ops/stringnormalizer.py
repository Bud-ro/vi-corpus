# ops/stringnormalizer.py
import numpy as np
import onnx
import onnx.helper
from onnx import TensorProto, ValueInfoProto, TypeProto
from utils import SpecialModelBuilders, SpecialInputGenerators, ONNX_RUNTIME_IR_VERSION, ONNX_OPSET_VERSION

def stringnormalizer_model_builder(op_type, cfg=None):
    # Définition de l'entrée
    input_tensor = onnx.helper.make_tensor_value_info("X", TensorProto.STRING, [1, 3])
    # Définition de la sortie
    output_tensor = onnx.helper.make_tensor_value_info("Y", TensorProto.STRING, [1, 3])

    # Création du nœud StringNormalizer
    node = onnx.helper.make_node(
        "StringNormalizer",
        inputs=["X"],
        outputs=["Y"],
        case_change_action="LOWER",
        is_case_sensitive=0,
        stopwords=["the", "a", "an"]
    )

    # Construction du graphe
    graph = onnx.helper.make_graph(
        nodes=[node],
        name="stringnormalizer_graph",
        inputs=[input_tensor],
        outputs=[output_tensor]
    )

    # Création du modèle
    model = onnx.helper.make_model(
        graph,
        opset_imports=[onnx.helper.make_operatorsetid("ai.onnx", ONNX_OPSET_VERSION)]
    )
    model.ir_version = ONNX_RUNTIME_IR_VERSION
    return model

def stringnormalizer_input_generator(session):
    # Génération d'un tenseur d'entrée avec des chaînes de caractères
    input_data = np.array([["The", "quick", "brown"]], dtype=object)
    return {"X": input_data}

# Enregistrement des fonctions dans les dictionnaires
SpecialModelBuilders["StringNormalizer"] = stringnormalizer_model_builder
SpecialInputGenerators["StringNormalizer"] = stringnormalizer_input_generator
