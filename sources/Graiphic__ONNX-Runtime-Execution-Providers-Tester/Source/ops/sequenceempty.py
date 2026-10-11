# ops/sequenceempty.py
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

def sequenceempty_model_builder(op_type, cfg=None):
    # Définition de la sortie : séquence vide de float
    output = make_sequence_value_info("seq_out", TensorProto.FLOAT)

    # Création du nœud SequenceEmpty
    node = onnx.helper.make_node(
        "SequenceEmpty",
        inputs=[],
        outputs=["seq_out"],
        dtype=TensorProto.FLOAT  # Spécifie le type des éléments de la séquence
    )

    # Construction du graphe
    graph = onnx.helper.make_graph(
        nodes=[node],
        name="sequenceempty_graph",
        inputs=[],
        outputs=[output]
    )

    # Création du modèle
    model = onnx.helper.make_model(
        graph,
        opset_imports=[onnx.helper.make_operatorsetid("", ONNX_OPSET_VERSION)]
    )
    model.ir_version = ONNX_RUNTIME_IR_VERSION
    return model

def sequenceempty_input_generator(session):
    # Aucun input requis pour SequenceEmpty
    return {}

# Enregistrement des fonctions dans les dictionnaires
SpecialModelBuilders["SequenceEmpty"] = sequenceempty_model_builder
SpecialInputGenerators["SequenceEmpty"] = sequenceempty_input_generator
