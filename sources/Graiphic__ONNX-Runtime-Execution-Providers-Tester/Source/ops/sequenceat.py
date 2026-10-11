# ops/sequenceat.py
import numpy as np
import onnx
import onnx.helper
from utils import SpecialModelBuilders, SpecialInputGenerators, ONNX_RUNTIME_IR_VERSION, ONNX_OPSET_VERSION

def sequenceat_model_builder(op_type, cfg=None):
    # Création de trois tenseurs d'entrée
    tensor1 = onnx.helper.make_tensor('t1', onnx.TensorProto.FLOAT, [2, 2], np.random.rand(2, 2).astype(np.float32).flatten())
    tensor2 = onnx.helper.make_tensor('t2', onnx.TensorProto.FLOAT, [2, 2], np.random.rand(2, 2).astype(np.float32).flatten())
    tensor3 = onnx.helper.make_tensor('t3', onnx.TensorProto.FLOAT, [2, 2], np.random.rand(2, 2).astype(np.float32).flatten())

    # Création du nœud SequenceConstruct
    seq_node = onnx.helper.make_node(
        'SequenceConstruct',
        inputs=['t1', 't2', 't3'],
        outputs=['seq']
    )

    # Définition de l'entrée pour la position
    pos_input = onnx.helper.make_tensor_value_info('position', onnx.TensorProto.INT64, [])

    # Définition de la sortie
    output = onnx.helper.make_tensor_value_info('output', onnx.TensorProto.FLOAT, None)

    # Création du nœud SequenceAt
    seq_at_node = onnx.helper.make_node(
        'SequenceAt',
        inputs=['seq', 'position'],
        outputs=['output']
    )

    # Création du graphe
    graph = onnx.helper.make_graph(
        nodes=[seq_node, seq_at_node],
        name='sequenceat_graph',
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

def sequenceat_input_generator(session):
    # Génération d'une position aléatoire valide
    position = np.array(1, dtype=np.int64)  # Par exemple, pour extraire le deuxième tenseur
    return {'position': position}

# Enregistrement des fonctions dans les dictionnaires
SpecialModelBuilders['SequenceAt'] = sequenceat_model_builder
SpecialInputGenerators['SequenceAt'] = sequenceat_input_generator
