# ops/sequenceerase.py
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

def sequenceerase_model_builder(op_type, cfg=None):
    # Création de trois tenseurs d'entrée
    tensor1 = onnx.helper.make_tensor('t1', TensorProto.FLOAT, [2, 2], np.random.rand(2, 2).astype(np.float32).flatten())
    tensor2 = onnx.helper.make_tensor('t2', TensorProto.FLOAT, [2, 2], np.random.rand(2, 2).astype(np.float32).flatten())
    tensor3 = onnx.helper.make_tensor('t3', TensorProto.FLOAT, [2, 2], np.random.rand(2, 2).astype(np.float32).flatten())

    # Création du nœud SequenceConstruct
    seq_node = onnx.helper.make_node(
        'SequenceConstruct',
        inputs=['t1', 't2', 't3'],
        outputs=['seq']
    )

    # Définition de l'entrée pour la position
    pos_input = onnx.helper.make_tensor_value_info('position', TensorProto.INT64, [])

    # Définition de la sortie
    output = make_sequence_value_info("seq_out", TensorProto.FLOAT)

    # Création du nœud SequenceErase
    erase_node = onnx.helper.make_node(
        'SequenceErase',
        inputs=['seq', 'position'],
        outputs=['seq_out']
    )

    # Création du graphe
    graph = onnx.helper.make_graph(
        nodes=[seq_node, erase_node],
        name='sequenceerase_graph',
        inputs=[pos_input],
        outputs=[output],
        initializer=[tensor1, tensor2, tensor3]
    )

    # Création du modèle
    model = onnx.helper.make_model(
        graph,
        opset_imports=[onnx.helper.make_operatorsetid("", ONNX_OPSET_VERSION)]
    )
    model.ir_version = ONNX_RUNTIME_IR_VERSION
    return model

def sequenceerase_input_generator(session):
    # Génération d'une position aléatoire valide
    position = np.array(1, dtype=np.int64)  # Par exemple, pour supprimer le deuxième tenseur
    return {'position': position}

# Enregistrement des fonctions dans les dictionnaires
SpecialModelBuilders["SequenceErase"] = sequenceerase_model_builder
SpecialInputGenerators["SequenceErase"] = sequenceerase_input_generator
