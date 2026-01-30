from perf_measure.config import ATTACKS
import homoglyphs
from decancer_py import parse, CuredString
import json
import time
import argparse
import sys
import statistics
import string
from pathlib import Path
import random
import csv
from datetime import datetime

lengths = [1000, 5000, 10000]
perturbation_budget_percentages = [0.1, 0.2, 0.3, 0.4, 0.5]


"""
----------------
Benchmarking 
----------------
"""


def _make_text(length):
    alphabet = string.ascii_letters + string.digits + string.punctuation + " "
    return "".join(random.choice(alphabet) for _ in range(length))


def _measure(func, perturbed_text, runs=5):
    func(perturbed_text)

    times = []
    cpu_times = []
    for _ in range(runs):
        start = time.perf_counter()
        cpu_start = time.process_time()
        func(perturbed_text)
        cpu_end = time.process_time()
        end = time.perf_counter()
        times.append(end - start)
        cpu_times.append(cpu_end - cpu_start)

    return (
        statistics.mean(times),
        statistics.mean(cpu_times),
    )


def _get_attack_config(attack):
    try:
        cfg = ATTACKS[attack]
    except KeyError as exc:
        raise ValueError(f"Unknown attack: {attack}") from exc
    return cfg["attack_cls"], cfg["impls"]


def _get_output_path(mode, args):
    results_dir = Path(__file__).resolve().parent / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    filename = f"mode={args.mode}_length={args.length}_pct={args.pct}_attack={args.attack}_impl={args.impl}.csv"
    return results_dir / filename


def run_benchmark(runs=5, seed=7, attack="deletion", args=None):
    random.seed(seed)
    output_path = _get_output_path("benchmark", args)
    header = [
        "length",
        "pct",
        "attack",
        "impl",
        "time_ms",
        "cpu_ms",
    ]

    attack_cls, impls = _get_attack_config(attack)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for length in lengths:
            base_text = _make_text(length)
            for pct in perturbation_budget_percentages:
                perturbation_budget = max(1, int(length * pct))
                pert = attack_cls(perturbation_budget=perturbation_budget).perturb(
                    base_text
                )
                for impl_name in impls.keys():
                    func = impls[impl_name]
                    (
                        impl_time,
                        impl_cpu,
                    ) = _measure(func, pert, runs=runs)
                    writer.writerow(
                        [
                            length,
                            f"{pct:.1f}",
                            attack,
                            impl_name,
                            f"{impl_time * 1000:.3f}",
                            f"{impl_cpu * 1000:.3f}",
                        ]
                    )


def run_single(
    impl_name, length=1000, pct=0.1, runs=5, seed=7, attack="deletion", args=None
):
    random.seed(seed)
    base_text = _make_text(length)
    perturbation_budget = max(1, int(length * pct))
    attack_cls, impls = _get_attack_config(attack)
    pert = attack_cls(perturbation_budget=perturbation_budget).perturb(base_text)

    func = impls[impl_name]
    (
        time_s,
        cpu_s,
    ) = _measure(func, pert, runs=runs)

    output_path = _get_output_path("single", args)
    header = [
        "impl",
        "length",
        "pct",
        "time_ms",
        "cpu_ms",
    ]
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerow(
            [
                impl_name,
                length,
                f"{pct:.1f}",
                f"{time_s * 1000:.3f}",
                f"{cpu_s * 1000:.3f}",
            ]
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=["benchmark", "single"],
        default="benchmark",
        help="benchmark = run all impls for attack; single = one impl",
    )
    parser.add_argument("--length", type=int, default=1000)
    parser.add_argument("--pct", type=float, default=0.1)
    parser.add_argument("--runs", type=int, default=5)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument(
        "--attack",
        choices=list(ATTACKS.keys()),
        default="deletion",
        help="which attack type to run",
    )
    parser.add_argument(
        "--impl",
        default=None,
        help="implementation name for single mode (e.g., python, cpp, homoglyphs, decancer)",
    )
    args = parser.parse_args()

    if args.mode == "benchmark":
        run_benchmark(runs=args.runs, seed=args.seed, attack=args.attack, args=args)
    else:
        run_single(
            impl_name=args.impl,
            length=args.length,
            pct=args.pct,
            runs=args.runs,
            seed=args.seed,
            attack=args.attack,
            args=args,
        )
