# ops/sequencelength.py
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

def sequencelength_model_builder(op_type, cfg=None):
    # Définition des entrées
    input_names = ['X1', 'X2', 'X3']
    inputs = [
        onnx.helper.make_tensor_value_info(name, TensorProto.FLOAT, [2, 2])
        for name in input_names
    ]
    # Définition de la sortie
    output = onnx.helper.make_tensor_value_info("length", TensorProto.INT64, [])

    # Création des nœuds
    seq_construct_node = onnx.helper.make_node(
        "SequenceConstruct",
        inputs=input_names,
        outputs=["seq"]
    )

    seq_length_node = onnx.helper.make_node(
        "SequenceLength",
        inputs=["seq"],
        outputs=["length"]
    )

    # Construction du graphe
    graph = onnx.helper.make_graph(
        nodes=[seq_construct_node, seq_length_node],
        name="sequencelength_graph",
        inputs=inputs,
        outputs=[output]
    )

    # Création du modèle
    model = onnx.helper.make_model(
        graph,
        opset_imports=[onnx.helper.make_operatorsetid("", ONNX_OPSET_VERSION)]
    )
    model.ir_version = ONNX_RUNTIME_IR_VERSION
    return model

def sequencelength_input_generator(session):
    inputs = session.get_inputs()
    feed = {}
    for inp in inputs:
        shape = [d if isinstance(d, int) else 1 for d in inp.shape]
        feed[inp.name] = np.random.rand(*shape).astype(np.float32)
    return feed

# Enregistrement des fonctions dans les dictionnaires
SpecialModelBuilders["SequenceLength"] = sequencelength_model_builder
SpecialInputGenerators["SequenceLength"] = sequencelength_input_generator
