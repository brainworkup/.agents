#!/usr/bin/env python3
"""
Classify neuropsychological test scores into normative categories.

Usage:
    python classify_scores.py --score 85 --metric ss
    python classify_scores.py --score 42 --metric t
    python classify_scores.py --score 7 --metric scaled
    python classify_scores.py --file scores.csv --output classified_scores.csv
    python classify_scores.py --interactive

Supports Standard Score (SS), T-Score, Scaled Score, z-Score, and Percentile metrics.
"""

import argparse
import csv
import math
import sys
from typing import Optional


# Classification systems
WECHSLER_SS = [
    (130, float("inf"), "Very Superior"),
    (120, 129, "Superior"),
    (110, 119, "High Average"),
    (90, 109, "Average"),
    (80, 89, "Low Average"),
    (70, 79, "Borderline"),
    (float("-inf"), 69, "Extremely Low"),
]

HEATON_T = [
    (60, float("inf"), "Above Average"),
    (40, 59, "Average"),
    (35, 39, "Low Average"),
    (30, 34, "Mildly Impaired"),
    (25, 29, "Mildly-to-Moderately Impaired"),
    (20, 24, "Moderately Impaired"),
    (float("-inf"), 19, "Severely Impaired"),
]

WECHSLER_SCALED = [
    (16, float("inf"), "Very Superior"),
    (14, 15, "Superior"),
    (12, 13, "High Average"),
    (8, 11, "Average"),
    (6, 7, "Low Average"),
    (4, 5, "Borderline"),
    (float("-inf"), 3, "Extremely Low"),
]

BDI_II = [
    (0, 13, "Minimal"),
    (14, 19, "Mild"),
    (20, 28, "Moderate"),
    (29, 63, "Severe"),
]

BAI = [
    (0, 7, "Minimal"),
    (8, 15, "Mild"),
    (16, 25, "Moderate"),
    (26, 63, "Severe"),
]

PHQ9 = [
    (0, 4, "Minimal/None"),
    (5, 9, "Mild"),
    (10, 14, "Moderate"),
    (15, 19, "Moderately Severe"),
    (20, 27, "Severe"),
]

GAD7 = [
    (0, 4, "Minimal"),
    (5, 9, "Mild"),
    (10, 14, "Moderate"),
    (15, 21, "Severe"),
]


def classify(score: float, system: list) -> str:
    for low, high, label in system:
        if low <= score <= high:
            return label
    return "Unclassified"


def normal_cdf(z: float) -> float:
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def ss_to_percentile(ss: float) -> float:
    return round(100 * normal_cdf((ss - 100) / 15), 1)


def t_to_percentile(t: float) -> float:
    return round(100 * normal_cdf((t - 50) / 10), 1)


def scaled_to_percentile(sc: float) -> float:
    return round(100 * normal_cdf((sc - 10) / 3), 1)


def z_to_percentile(z: float) -> float:
    return round(100 * normal_cdf(z), 1)


def classify_score(score: float, metric: str) -> dict:
    metric = metric.lower()
    result = {"score": score, "metric": metric, "classification": "", "percentile": None}

    if metric in ("ss", "standard", "standard_score"):
        result["classification"] = classify(score, WECHSLER_SS)
        result["percentile"] = ss_to_percentile(score)
    elif metric in ("t", "tscore", "t_score"):
        result["classification"] = classify(score, HEATON_T)
        result["percentile"] = t_to_percentile(score)
    elif metric in ("scaled", "scaledscore", "scaled_score"):
        result["classification"] = classify(score, WECHSLER_SCALED)
        result["percentile"] = scaled_to_percentile(score)
    elif metric in ("z", "zscore", "z_score"):
        result["percentile"] = z_to_percentile(score)
        ss_equiv = score * 15 + 100
        result["classification"] = classify(ss_equiv, WECHSLER_SS)
    elif metric in ("percentile", "pct", "%ile"):
        result["percentile"] = score
        if score >= 98:
            result["classification"] = "Very Superior"
        elif score >= 91:
            result["classification"] = "Superior"
        elif score >= 75:
            result["classification"] = "High Average"
        elif score >= 25:
            result["classification"] = "Average"
        elif score >= 9:
            result["classification"] = "Low Average"
        elif score >= 2:
            result["classification"] = "Borderline"
        else:
            result["classification"] = "Extremely Low"
    elif metric in ("bdi", "bdi-ii", "bdi2"):
        result["classification"] = classify(score, BDI_II)
    elif metric in ("bai",):
        result["classification"] = classify(score, BAI)
    elif metric in ("phq9", "phq-9"):
        result["classification"] = classify(score, PHQ9)
    elif metric in ("gad7", "gad-7"):
        result["classification"] = classify(score, GAD7)
    else:
        result["classification"] = f"Unknown metric: {metric}"

    return result


def process_csv(input_path: str, output_path: Optional[str] = None):
    """Process a CSV file of scores. Expected columns: measure, subtest, score, metric"""
    rows = []
    with open(input_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            score = float(row["score"])
            metric = row["metric"]
            result = classify_score(score, metric)
            row["classification"] = result["classification"]
            row["percentile"] = result["percentile"] if result["percentile"] is not None else ""
            rows.append(row)

    out = output_path or input_path.replace(".csv", "_classified.csv")
    if rows:
        with open(out, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
    print(f"Classified {len(rows)} scores → {out}")


def interactive_mode():
    print("Neuropsychological Score Classifier")
    print("=" * 40)
    print("Metrics: ss, t, scaled, z, percentile, bdi, bai, phq9, gad7")
    print("Type 'quit' to exit.\n")

    while True:
        try:
            raw = input("Score: ").strip()
            if raw.lower() in ("quit", "exit", "q"):
                break
            score = float(raw)
            metric = input("Metric (ss/t/scaled/z/percentile): ").strip()
            result = classify_score(score, metric)
            print(f"  Classification: {result['classification']}")
            if result["percentile"] is not None:
                print(f"  Percentile: {result['percentile']}")
            print()
        except (ValueError, EOFError):
            print("Invalid input. Enter a numeric score.\n")
        except KeyboardInterrupt:
            break


def main():
    parser = argparse.ArgumentParser(description="Classify neuropsychological test scores")
    parser.add_argument("--score", type=float, help="Single score to classify")
    parser.add_argument("--metric", type=str, help="Score metric (ss, t, scaled, z, percentile, bdi, bai, phq9, gad7)")
    parser.add_argument("--file", type=str, help="CSV file of scores to classify")
    parser.add_argument("--output", type=str, help="Output CSV path")
    parser.add_argument("--interactive", action="store_true", help="Interactive mode")
    args = parser.parse_args()

    if args.interactive:
        interactive_mode()
    elif args.file:
        process_csv(args.file, args.output)
    elif args.score is not None and args.metric:
        result = classify_score(args.score, args.metric)
        print(f"Score: {result['score']} ({result['metric']})")
        print(f"Classification: {result['classification']}")
        if result["percentile"] is not None:
            print(f"Percentile: {result['percentile']}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
