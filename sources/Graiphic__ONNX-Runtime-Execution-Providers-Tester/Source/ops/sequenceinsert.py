# ops/sequenceinsert.py
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

def sequenceinsert_model_builder(op_type, cfg=None):
    # Définition des entrées
    input_names = ['X1', 'X2']
    inputs = [
        onnx.helper.make_tensor_value_info(name, TensorProto.FLOAT, [2, 2])
        for name in input_names
    ]
    tensor_to_insert = onnx.helper.make_tensor_value_info('X_insert', TensorProto.FLOAT, [2, 2])
    position = onnx.helper.make_tensor_value_info('position', TensorProto.INT64, [])

    # Définition de la sortie
    output = make_sequence_value_info("seq_out", TensorProto.FLOAT)

    # Création des nœuds
    seq_construct_node = onnx.helper.make_node(
        "SequenceConstruct",
        inputs=input_names,
        outputs=["seq"]
    )

    seq_insert_node = onnx.helper.make_node(
        "SequenceInsert",
        inputs=["seq", "X_insert", "position"],
        outputs=["seq_out"]
    )

    # Construction du graphe
    graph = onnx.helper.make_graph(
        nodes=[seq_construct_node, seq_insert_node],
        name="sequenceinsert_graph",
        inputs=inputs + [tensor_to_insert, position],
        outputs=[output]
    )

    # Création du modèle
    model = onnx.helper.make_model(
        graph,
        opset_imports=[onnx.helper.make_operatorsetid("", ONNX_OPSET_VERSION)]
    )
    model.ir_version = ONNX_RUNTIME_IR_VERSION
    return model

def sequenceinsert_input_generator(session):
    inputs = session.get_inputs()
    feed = {}
    for inp in inputs:
        if inp.name == 'position':
            feed[inp.name] = np.array(1, dtype=np.int64)  # Insère à la position 1
        else:
            shape = [d if isinstance(d, int) else 1 for d in inp.shape]
            feed[inp.name] = np.random.rand(*shape).astype(np.float32)
    return feed

# Enregistrement des fonctions dans les dictionnaires
SpecialModelBuilders["SequenceInsert"] = sequenceinsert_model_builder
SpecialInputGenerators["SequenceInsert"] = sequenceinsert_input_generator
