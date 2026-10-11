# ops/stft.py
import numpy as np
import onnx
import onnx.helper
from onnx import TensorProto
from utils import SpecialModelBuilders, SpecialInputGenerators, ONNX_RUNTIME_IR_VERSION

def stft_model_builder(op_type, cfg=None):
    signal = onnx.helper.make_tensor_value_info("signal", TensorProto.FLOAT, [1, 512, 1])
    frame_step = onnx.helper.make_tensor_value_info("frame_step", TensorProto.INT64, [])
    window = onnx.helper.make_tensor_value_info("window", TensorProto.FLOAT, [256])
    frame_length = onnx.helper.make_tensor_value_info("frame_length", TensorProto.INT64, [])
    output = onnx.helper.make_tensor_value_info("output", TensorProto.FLOAT, None)

    node = onnx.helper.make_node(
        "STFT",
        inputs=["signal", "frame_step", "window", "frame_length"],
        outputs=["output"],
        onesided=1
    )

    graph = onnx.helper.make_graph(
        [node],
        "stft_graph",
        inputs=[signal, frame_step, window, frame_length],
        outputs=[output]
    )

    model = onnx.helper.make_model(graph)
    model.ir_version = ONNX_RUNTIME_IR_VERSION
    model.opset_import[0].version = 17  # STFT est disponible depuis l'opset 17
    return model

def stft_input_generator(session):
    signal = np.random.randn(1, 512, 1).astype(np.float32)
    frame_step = np.array(128, dtype=np.int64)
    window = np.hanning(256).astype(np.float32)
    frame_length = np.array(256, dtype=np.int64)
    return {
        "signal": signal,
        "frame_step": frame_step,
        "window": window,
        "frame_length": frame_length
    }

SpecialModelBuilders["STFT"] = stft_model_builder
SpecialInputGenerators["STFT"] = stft_input_generator
