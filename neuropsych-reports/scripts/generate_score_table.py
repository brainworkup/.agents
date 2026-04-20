#!/usr/bin/env python3
"""Generate formatted neuropsychological score tables from CSV input."""

import argparse
import csv
import sys
from pathlib import Path
from typing import List

from score_engine import format_score_value, read_score_rows


def format_markdown(rows: List[dict]) -> str:
    if not rows:
        return "No scores to display."

    groups = {}
    for row in rows:
        groups.setdefault(row["score_label"], []).append(row)

    lines = []
    for label, group_rows in groups.items():
        lines.append(f"### {label}-Based Measures\n")
        lines.append(f"| Measure | Subtest/Index | Raw | {label} | Percentile | Classification |")
        lines.append("|---------|--------------|-----|" + "-" * (len(label) + 2) + "|------------|----------------|")
        for row in group_rows:
            raw_value = str(row["raw"]) if row["raw"] else "—"
            score_value = format_score_value(row["score"])
            percentile = row["percentile"]
            percentile_text = f"{percentile:.0f}th" if percentile is not None else "—"
            lines.append(
                f"| {row['measure']} | {row['subtest']} | {raw_value} | {score_value} | {percentile_text} | {row['classification']} |"
            )
        lines.append("")

    return "\n".join(lines)


def format_csv_output(rows: List[dict]) -> str:
    if not rows:
        return ""

    output_lines = []
    header = ["measure", "subtest", "raw", "score", "metric", "percentile", "classification"]
    output_lines.append(",".join(header))
    for row in rows:
        buffer = [
            row["measure"],
            row["subtest"],
            str(row["raw"]),
            str(row["score"]),
            row["metric"],
            "" if row["percentile"] is None else f"{row['percentile']:.1f}",
            row["classification"],
        ]
        output_lines.append(",".join(buffer))
    return "\n".join(output_lines)


def write_csv_file(rows: List[dict], output_path: str) -> None:
    fieldnames = ["measure", "subtest", "raw", "score", "metric", "score_label", "percentile", "classification"]
    with open(output_path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate formatted neuropsychological score tables")
    parser.add_argument("file", help="Input CSV file with scores")
    parser.add_argument("--format", choices=["markdown", "csv"], default="markdown", help="Output format (default: markdown)")
    parser.add_argument("--output", type=str, help="Output file path (default: stdout)")
    args = parser.parse_args()

    input_path = Path(args.file)
    if not input_path.exists():
        print(f"Error: File not found: {input_path}")
        sys.exit(1)

    rows = read_score_rows(str(input_path))

    if args.format == "markdown":
        output = format_markdown(rows)
        if args.output:
            Path(args.output).write_text(output, encoding="utf-8")
            print(f"Score table written to {args.output}")
        else:
            print(output)
    else:
        if args.output:
            write_csv_file(rows, args.output)
            print(f"Score table written to {args.output}")
        else:
            print(format_csv_output(rows))


if __name__ == "__main__":
    main()
