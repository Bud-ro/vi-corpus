################################################################################
# main.py
################################################################################
import pkgutil
import importlib
import ops
import onnxruntime
from utils import OpTest, wrap_model_with_flatten_gemm_reshape

# Chargement dynamique des modules ops/
for _, name, _ in pkgutil.iter_modules(ops.__path__):
    importlib.import_module(f"ops.{name}")


def load_ops(path):
    with open(path, 'r') as f:
        return [l.strip() for l in f if l.strip() and not l.startswith('#')]

if __name__ == '__main__':
    ops    = load_ops('test.txt')
    providers   = ['CPUExecutionProvider']

    for op in ops:
        tester = OpTest(op)
        for provider in providers:
            # Génération modèle
            try:
                model = tester.generate_model()
                wrap_model_with_flatten_gemm_reshape(model)
                tester.save_model(model)
            except Exception as e:
                print(f"{op} generate_model: FAIL -> {e}")
                continue
            # Création session
            try:
                opts = onnxruntime.SessionOptions()
                opts.log_severity_level = 2
                #opts.optimized_model_filepath =  f"{op}_optimized.onnx"
                sess = onnxruntime.InferenceSession(
                    model.SerializeToString(),
                    sess_options=opts,
                    providers=[provider]
                )
            except Exception as e:
                print(f"{op} on {provider} session creation: FAIL -> {e}")
                continue
            # Génération inputs
            try:
                feed = tester.generate_input(sess)
            except Exception as e:
                print(f"{op} generate_input: FAIL -> {e}")
                continue
            # Exécution
            try:
                #print("feed : ", feed.shape)
                output = sess.run(None, feed)
                print("output ", output)
                print(f"{op} on {provider}: SUCCESS")
            except Exception as e:
                print(f"{op} on {provider}: RUN FAIL -> {e}")
