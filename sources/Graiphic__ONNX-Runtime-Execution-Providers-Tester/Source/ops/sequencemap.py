# ops/sequencemap.py
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

def sequencemap_model_builder(op_type, cfg=None):
    # Définition des entrées
    input_seq = make_sequence_value_info("input_seq", TensorProto.FLOAT)

    # Définition du sous-graphe (body)
    # Ce sous-graphe prend un tenseur en entrée et retourne le même tenseur multiplié par 2
    subgraph_input = onnx.helper.make_tensor_value_info("x", TensorProto.FLOAT, [2, 2])
    subgraph_output = onnx.helper.make_tensor_value_info("y", TensorProto.FLOAT, [2, 2])
    mul_node = onnx.helper.make_node(
        "Mul",
        inputs=["x", "const_two"],
        outputs=["y"]
    )
    const_two = onnx.helper.make_tensor(
        name="const_two",
        data_type=TensorProto.FLOAT,
        dims=[1],
        vals=[2.0]
    )
    subgraph = onnx.helper.make_graph(
        nodes=[mul_node],
        name="subgraph",
        inputs=[subgraph_input],
        outputs=[subgraph_output],
        initializer=[const_two]
    )

    # Création du nœud SequenceMap
    node = onnx.helper.make_node(
        "SequenceMap",
        inputs=["input_seq"],
        outputs=["output_seq"],
        body=subgraph
    )

    # Définition de la sortie
    output_seq = make_sequence_value_info("output_seq", TensorProto.FLOAT)

    # Construction du graphe principal
    graph = onnx.helper.make_graph(
        nodes=[node],
        name="sequencemap_graph",
        inputs=[input_seq],
        outputs=[output_seq]
    )

    # Création du modèle
    model = onnx.helper.make_model(
        graph,
        opset_imports=[onnx.helper.make_operatorsetid("", ONNX_OPSET_VERSION)]
    )
    model.ir_version = ONNX_RUNTIME_IR_VERSION
    return model

def sequencemap_input_generator(session):
    # Génération d'une séquence de 3 tenseurs 2x2
    tensors = [np.random.rand(2, 2).astype(np.float32) for _ in range(3)]
    return {"input_seq": tensors}

# Enregistrement des fonctions dans les dictionnaires
SpecialModelBuilders["SequenceMap"] = sequencemap_model_builder
SpecialInputGenerators["SequenceMap"] = sequencemap_input_generator
