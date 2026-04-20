#!/usr/bin/env python3
"""Classify neuropsychological test scores into normative categories."""

import argparse
from typing import Optional

from score_engine import classify_score, default_output_path, read_score_rows


def process_csv(input_path: str, output_path: Optional[str] = None) -> None:
    """Process a CSV file of scores and write classifications."""
    rows = read_score_rows(input_path)
    output_file = output_path or default_output_path(input_path, "classified")

    if rows:
        import csv

        with open(output_file, "w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)

    print(f"Classified {len(rows)} scores → {output_file}")


def interactive_mode() -> None:
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
        except (ValueError, EOFError) as exc:
            print(f"Invalid input: {exc}\n")
        except KeyboardInterrupt:
            break


def main() -> None:
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
