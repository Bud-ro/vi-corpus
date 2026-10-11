# ops/tfidfvectorizer.py
import numpy as np
import onnx
import onnx.helper
from onnx import TensorProto
from utils import SpecialModelBuilders, SpecialInputGenerators, ONNX_RUNTIME_IR_VERSION, ONNX_OPSET_VERSION

def tfidfvectorizer_model_builder(op_type, cfg=None):
    # Entrée : un tableau 1D de chaînes
    input_tensor = onnx.helper.make_tensor_value_info("X", TensorProto.STRING, [None])
    # Sortie : vecteur de taille 7 (4 unigrams + 3 bigrams)
    output_tensor = onnx.helper.make_tensor_value_info("Y", TensorProto.FLOAT, [7])

    # 4 unigrams + (3 bigrams × 2 tokens chacun) = 10 entrées pool
    pool_strings = [
        "this", "is", "a", "test",      # 4 unigrams
        "this", "is",                   # bigram "this is"
        "is", "a",                      # bigram "is a"
        "a", "test"                     # bigram "a test"
    ]

    # CSR-style : [début unigrams, début bigrams, fin totale]
    ngram_counts = [0, 4, 10]  # 0→4 pour unigrams, 4→10 pour bigrams

    # Chaque entrée de pool_strings a une coordonnée dans la sortie Y (7 positions)
    ngram_indexes = [
        0, 1, 2, 3,  # unigrams "this","is","a","test" → idx 0..3
        4, 4,       # bigram "this is"   → coordonnée 4 (répétée)
        5, 5,       # bigram "is a"      → coordonnée 5
        6, 6        # bigram "a test"    → coordonnée 6
    ]

    # Poids associés à chaque entrée pool_strings (10 au total)
    weights = [1.0] * 10

    node = onnx.helper.make_node(
        "TfIdfVectorizer",
        inputs=["X"],
        outputs=["Y"],
        mode="TFIDF",
        min_gram_length=1,
        max_gram_length=2,
        max_skip_count=0,
        ngram_counts=ngram_counts,
        ngram_indexes=ngram_indexes,
        pool_strings=pool_strings,
        weights=weights
    )

    graph = onnx.helper.make_graph(
        nodes=[node],
        name="tfidf_graph",
        inputs=[input_tensor],
        outputs=[output_tensor]
    )

    model = onnx.helper.make_model(
        graph,
        opset_imports=[onnx.helper.make_operatorsetid("", ONNX_OPSET_VERSION)]
    )
    model.ir_version = ONNX_RUNTIME_IR_VERSION
    return model

def tfidfvectorizer_input_generator(session):
    # On passe un tableau 1D de tokens (dtype=object)
    return {"X": np.array(["this", "is", "a", "test"], dtype=object)}

SpecialModelBuilders["TfIdfVectorizer"] = tfidfvectorizer_model_builder
SpecialInputGenerators["TfIdfVectorizer"] = tfidfvectorizer_input_generator
