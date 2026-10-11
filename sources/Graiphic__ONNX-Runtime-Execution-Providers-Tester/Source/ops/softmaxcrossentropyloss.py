# ops/softmaxcrossentropyloss.py
import numpy as np
import onnx
import onnx.helper
from onnx import TensorProto
from utils import SpecialModelBuilders, SpecialInputGenerators, ONNX_RUNTIME_IR_VERSION, ONNX_OPSET_VERSION

def softmaxcrossentropyloss_model_builder(op_type, cfg=None):
    # Définition des entrées
    scores = onnx.helper.make_tensor_value_info("scores", TensorProto.FLOAT, [3, 5])
    labels = onnx.helper.make_tensor_value_info("labels", TensorProto.INT64, [3])
    # Définition de la sortie
    loss = onnx.helper.make_tensor_value_info("loss", TensorProto.FLOAT, [])

    # Création du nœud SoftmaxCrossEntropyLoss
    node = onnx.helper.make_node(
        "SoftmaxCrossEntropyLoss",
        inputs=["scores", "labels"],
        outputs=["loss"],
        reduction="mean"
    )

    # Construction du graphe
    graph = onnx.helper.make_graph(
        nodes=[node],
        name="softmaxcrossentropyloss_graph",
        inputs=[scores, labels],
        outputs=[loss]
    )

    # Création du modèle
    model = onnx.helper.make_model(
        graph,
        opset_imports=[onnx.helper.make_operatorsetid("", ONNX_OPSET_VERSION)]
    )
    model.ir_version = ONNX_RUNTIME_IR_VERSION
    return model

def softmaxcrossentropyloss_input_generator(session):
    # Génération de données d'entrée aléatoires
    scores = np.random.randn(3, 5).astype(np.float32)
    labels = np.random.randint(0, 5, size=(3,), dtype=np.int64)
    return {"scores": scores, "labels": labels}

# Enregistrement des fonctions dans les dictionnaires
SpecialModelBuilders["SoftmaxCrossEntropyLoss"] = softmaxcrossentropyloss_model_builder
SpecialInputGenerators["SoftmaxCrossEntropyLoss"] = softmaxcrossentropyloss_input_generator
