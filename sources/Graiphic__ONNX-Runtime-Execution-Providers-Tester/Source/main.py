# main.py
import os
import argparse
from utils import (
    run_tests_and_generate_reports,
    run_all_providers_and_generate_reports,
    run_selected_providers_and_generate_reports,
    configure_opset,
)
from report import generate_full_readme, generate_root_readme

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--eps", nargs="+", help="EP list (exact ORT names), e.g. CUDAExecutionProvider DnnlExecutionProvider")
    p.add_argument("--opsets", nargs="+", type=int, help="Opset versions to run, e.g. 20 22")
    p.add_argument("--test_file", default="test.txt")
    p.add_argument("--profiling_dir", default="profiling")
    p.add_argument("--models_dir", default="models")
    return p.parse_args()

def main():
    args = parse_args()

    # défaut: une seule valeur -> 22
    opsets = args.opsets if args.opsets else [20]

    if args.eps:
        # Ne lance que les EP demandés (si dispos dans l'env)
        run_selected_providers_and_generate_reports(
            providers_to_run=args.eps,
            test_file=args.test_file,
            base_profiling_dir=args.profiling_dir,
            base_models_dir=args.models_dir,
            opsets=opsets,
        )
    else:
        # Comportement “comme aujourd’hui”: tous les EP disponibles dans l’env
        # mais on le fait pour chaque opset demandé.
        for opset in opsets:
            configure_opset(opset)
            run_all_providers_and_generate_reports(
                test_file=args.test_file,
                base_profiling_dir=os.path.join(args.profiling_dir, f"opset_{opset}"),
                base_models_dir=os.path.join(args.models_dir, f"opset_{opset}"),
            )

    # README global (agrège les README écrits dans EP/opset_XX/)
    generate_full_readme()
    generate_root_readme()

if __name__ == "__main__":
    main()
    #generate_full_readme()
    #generate_root_readme()