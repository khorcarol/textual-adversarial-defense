from perf_measure.config import ATTACKS
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

LENGTHS = [1000, 5000, 10000]
PERTURBATION_BUDGET_PERCENTAGES = [0.1, 0.2, 0.3, 0.4, 0.5]


"""
----------------
Benchmarking 
----------------
"""


def _make_text(length):
    alphabet = string.ascii_letters + string.digits + string.punctuation + " "
    return "".join(random.choice(alphabet) for _ in range(length))


def _measure(func, perturbed_text, runs=5, pipeline=None):
    times = []
    cpu_times = []
    for _ in range(runs):
        start = time.perf_counter()
        cpu_start = time.process_time()
        func(perturbed_text, pipeline)
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
    length = getattr(args, "length", "all")
    pct = getattr(args, "pct", "all")
    impl = getattr(args, "impl", "all")
    filename = f"mode={args.mode}_attack={args.attack}_impl={impl}.csv"
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
    import textual_adversarial_defense

    pipeline = textual_adversarial_defense._pipeline.Pipeline()
    if attack == "variation":
        pipeline.add_variation_selector_sanitizer()
    elif attack == "tag":
        pipeline.add_tag_sanitizer()
    elif attack == "homoglyph":
        pipeline.add_homoglyph_sanitizer()
    elif attack == "bidi":
        pipeline.add_bidi_sanitizer()
    elif attack == "deletion":
        pipeline.add_deletion_sanitizer()
    elif attack == "invisible":
        pipeline.add_invisible_sanitizer()

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for length in LENGTHS:
            base_text = _make_text(length)
            for pct in PERTURBATION_BUDGET_PERCENTAGES:
                perturbation_budget = max(1, int(length * pct))
                pert = attack_cls(perturbation_budget=perturbation_budget).perturb(
                    base_text
                )
                for impl_name in impls.keys():
                    func = impls[impl_name]
                    (
                        impl_time,
                        impl_cpu,
                    ) = _measure(func, pert, runs=runs, pipeline=pipeline)
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


def run_single(impl_name, runs=5, seed=7, attack="deletion", args=None):
    random.seed(seed)
    output_path = _get_output_path("single", args)
    header = [
        "impl",
        "length",
        "pct",
        "rss_delta_mb",
        "rss_peak_mb",
    ]
    import textual_adversarial_defense

    pipeline = textual_adversarial_defense._pipeline.Pipeline()
    if attack == "variation":
        pipeline.add_variation_selector_sanitizer()
    elif attack == "tag":
        pipeline.add_tag_sanitizer()
    elif attack == "homoglyph":
        pipeline.add_homoglyph_sanitizer()
    elif attack == "bidi":
        pipeline.add_bidi_sanitizer()
    elif attack == "deletion":
        pipeline.add_deletion_sanitizer()
    elif attack == "invisible":
        pipeline.add_invisible_sanitizer()

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        attack_cls, impls = _get_attack_config(attack)
        func = impls[impl_name]
        for length in LENGTHS:
            for pct in PERTURBATION_BUDGET_PERCENTAGES:
                rss_deltas = []
                rss_peaks = []
                for run in range(runs):
                    base_text = _make_text(length)
                    perturbation_budget = max(1, int(length * pct))
                    pert = attack_cls(perturbation_budget=perturbation_budget).perturb(
                        base_text
                    )
                    rss_before = rss_bytes_linux()

                    func(pert, pipeline)

                    rss_after = rss_bytes_linux()
                    rss_peak = peak_rss_bytes_linux()
                    rss_delta = rss_after - rss_before
                    rss_deltas.append(rss_delta)
                    rss_peaks.append(rss_peak)

                rss_delta_mean = statistics.mean(rss_deltas)
                rss_peak_mean = statistics.mean(rss_peaks)
                writer.writerow(
                    [
                        impl_name,
                        length,
                        f"{pct:.1f}",
                        f"{rss_delta_mean / 1024:.3f}",
                        f"{rss_peak_mean / 1024:.3f}",
                    ]
                )


def _read_proc_status_kb(key: str) -> int:
    with open("/proc/self/status", "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith(key + ":"):
                # e.g. "VmHWM:\t  12345 kB"
                return int(line.split()[1])  # kB
    raise KeyError(key)


def rss_bytes_linux() -> int:
    return _read_proc_status_kb("VmRSS")


def peak_rss_bytes_linux() -> int:
    return _read_proc_status_kb("VmHWM")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=["benchmark", "single"],
        default="benchmark",
        help="benchmark = run all impls for attack; single = one impl",
    )
    parser.add_argument("--runs", type=int, default=50)
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
            runs=args.runs,
            seed=args.seed,
            attack=args.attack,
            args=args,
        )
