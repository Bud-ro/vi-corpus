# ops/bernoulli.py
import numpy as np
import onnx
import onnx.helper
from utils import SpecialModelBuilders, SpecialInputGenerators, ONNX_RUNTIME_IR_VERSION, ONNX_OPSET_VERSION

def bernoulli_model_builder(op_type, cfg=None):
    # Définition de l'entrée : tenseur de probabilités
    inp = onnx.helper.make_tensor_value_info("X", onnx.TensorProto.FLOAT, [1, 3, 4])
    # Définition de la sortie : même forme que l'entrée, valeurs 0 ou 1
    out = onnx.helper.make_tensor_value_info("Y", onnx.TensorProto.INT32, None)

    # Création du nœud Bernoulli avec un type de sortie spécifié
    node = onnx.helper.make_node(
        "Bernoulli",
        inputs=["X"],
        outputs=["Y"],
        dtype=onnx.TensorProto.INT32  # Spécification du type de sortie
        # seed peut être ajouté si nécessaire
    )

    # Construction du graphe
    graph = onnx.helper.make_graph(
        [node],
        "bernoulli_graph",
        [inp],
        [out]
    )

    # Création du modèle
    model = onnx.helper.make_model(
        graph,
        opset_imports=[onnx.helper.make_operatorsetid("", ONNX_OPSET_VERSION)]
    )
    model.ir_version = ONNX_RUNTIME_IR_VERSION
    return model

SpecialModelBuilders["Bernoulli"] = bernoulli_model_builder

def bernoulli_input_generator(session):
    # Récupération des informations sur l'entrée
    x_info = session.get_inputs()[0]
    shape = [d or 1 for d in x_info.shape]
    # Génération de probabilités aléatoires dans [0, 1]
    x = np.random.rand(*shape).astype(np.float32)
    return {x_info.name: x}

SpecialInputGenerators["Bernoulli"] = bernoulli_input_generator
