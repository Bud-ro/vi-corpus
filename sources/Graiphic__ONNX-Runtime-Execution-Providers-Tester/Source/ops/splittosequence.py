# ops/splittosequence.py
import numpy as np
import onnx
import onnx.helper
from onnx import TensorProto, ValueInfoProto, TypeProto
from utils import SpecialModelBuilders, SpecialInputGenerators, ONNX_RUNTIME_IR_VERSION, ONNX_OPSET_VERSION

def make_sequence_value_info(name, elem_type):
    t = TypeProto()
    t.sequence_type.elem_type.tensor_type.elem_type = elem_type
    vi = ValueInfoProto()
    vi.name = name
    vi.type.CopyFrom(t)
    return vi

def splittosequence_model_builder(op_type, cfg=None):
    # Définition de l'entrée
    input_tensor = onnx.helper.make_tensor_value_info("X", TensorProto.FLOAT, [4, 2])
    # Définition de la sortie
    output_sequence = make_sequence_value_info("Y", TensorProto.FLOAT)

    # Création du nœud SplitToSequence
    node = onnx.helper.make_node(
        "SplitToSequence",
        inputs=["X"],
        outputs=["Y"],
        axis=0,
        keepdims=1
    )

    # Construction du graphe
    graph = onnx.helper.make_graph(
        nodes=[node],
        name="splittosequence_graph",
        inputs=[input_tensor],
        outputs=[output_sequence]
    )

    # Création du modèle
    model = onnx.helper.make_model(
        graph,
        opset_imports=[onnx.helper.make_operatorsetid("", ONNX_OPSET_VERSION)]
    )
    model.ir_version = ONNX_RUNTIME_IR_VERSION
    return model

def splittosequence_input_generator(session):
    # Génération d'un tenseur d'entrée de forme [4, 2]
    input_data = np.random.rand(4, 2).astype(np.float32)
    return {"X": input_data}

# Enregistrement des fonctions dans les dictionnaires
SpecialModelBuilders["SplitToSequence"] = splittosequence_model_builder
SpecialInputGenerators["SplitToSequence"] = splittosequence_input_generator
