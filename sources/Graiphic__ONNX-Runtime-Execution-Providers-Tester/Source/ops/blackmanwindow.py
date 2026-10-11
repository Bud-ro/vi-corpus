# ops/blackmanwindow.py
import numpy as np
import onnx
from onnx import helper, TensorProto
from utils import SpecialModelBuilders, SpecialInputGenerators, ONNX_RUNTIME_IR_VERSION, ONNX_OPSET_VERSION

def blackmanwindow_model_builder(op_type, cfg=None):
    # -- Entrée scalar (shape []) au lieu de [1]
    size_input = helper.make_tensor_value_info("size_input", TensorProto.INT64, [])
    output     = helper.make_tensor_value_info("output",      TensorProto.FLOAT,  None)

    # -- Noeud BlackmanWindow sans squeeze intermédiaire
    window_node = helper.make_node(
        "BlackmanWindow",
        inputs=["size_input"],
        outputs=["output"],
        periodic=1,
        output_datatype=1  # FLOAT
    )

    graph = helper.make_graph(
        [window_node],
        "blackmanwindow_graph",
        [size_input],
        [output]
    )

    model = helper.make_model(
        graph,
        opset_imports=[helper.make_operatorsetid("", ONNX_OPSET_VERSION)]
    )
    model.ir_version = ONNX_RUNTIME_IR_VERSION
    return model

SpecialModelBuilders["BlackmanWindow"] = blackmanwindow_model_builder


def blackmanwindow_input_generator(session):
    size_info, = session.get_inputs()  # récupère size_input seul
    # on peut passer un scalaire numpy.int64 directement
    return { size_info.name: np.array(16, dtype=np.int64) }

SpecialInputGenerators["BlackmanWindow"] = blackmanwindow_input_generator
