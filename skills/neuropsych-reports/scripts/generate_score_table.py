#!/usr/bin/env python3
"""
Generate formatted neuropsychological score tables from CSV input.

Usage:
    python generate_score_table.py scores.csv
    python generate_score_table.py scores.csv --format markdown
    python generate_score_table.py scores.csv --format csv --output results.csv

Input CSV format:
    measure,subtest,raw,score,metric
    WAIS-V,FSIQ,,98,ss
    WAIS-V,VCI,,105,ss
    CVLT-3,Trial 1,7,42,t
    Grooved Pegboard,Dominant,72,35,t

Supported metrics: ss, t, scaled, z, percentile, bdi, bai, phq9, gad7
"""

import argparse
import csv
import math
import sys
from pathlib import Path
from typing import Optional


def normal_cdf(z: float) -> float:
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def score_to_percentile(score: float, metric: str) -> Optional[float]:
    metric = metric.lower()
    if metric in ("ss", "standard", "standard_score"):
        return round(100 * normal_cdf((score - 100) / 15), 1)
    elif metric in ("t", "tscore", "t_score"):
        return round(100 * normal_cdf((score - 50) / 10), 1)
    elif metric in ("scaled", "scaledscore", "scaled_score"):
        return round(100 * normal_cdf((score - 10) / 3), 1)
    elif metric in ("z", "zscore", "z_score"):
        return round(100 * normal_cdf(score), 1)
    elif metric in ("percentile", "pct", "%ile"):
        return score
    return None


def classify_ss(score: float) -> str:
    if score >= 130:
        return "Very Superior"
    elif score >= 120:
        return "Superior"
    elif score >= 110:
        return "High Average"
    elif score >= 90:
        return "Average"
    elif score >= 80:
        return "Low Average"
    elif score >= 70:
        return "Borderline"
    else:
        return "Extremely Low"


def classify_t(score: float) -> str:
    if score >= 60:
        return "Above Average"
    elif score >= 40:
        return "Average"
    elif score >= 35:
        return "Low Average"
    elif score >= 30:
        return "Mildly Impaired"
    elif score >= 25:
        return "Mildly-Mod Impaired"
    elif score >= 20:
        return "Moderately Impaired"
    else:
        return "Severely Impaired"


def classify_scaled(score: float) -> str:
    if score >= 16:
        return "Very Superior"
    elif score >= 14:
        return "Superior"
    elif score >= 12:
        return "High Average"
    elif score >= 8:
        return "Average"
    elif score >= 6:
        return "Low Average"
    elif score >= 4:
        return "Borderline"
    else:
        return "Extremely Low"


def classify_score(score: float, metric: str) -> str:
    metric = metric.lower()
    if metric in ("ss", "standard", "standard_score"):
        return classify_ss(score)
    elif metric in ("t", "tscore", "t_score"):
        return classify_t(score)
    elif metric in ("scaled", "scaledscore", "scaled_score"):
        return classify_scaled(score)
    elif metric in ("z", "zscore", "z_score"):
        return classify_ss(score * 15 + 100)
    elif metric in ("percentile", "pct", "%ile"):
        if score >= 98:
            return "Very Superior"
        elif score >= 91:
            return "Superior"
        elif score >= 75:
            return "High Average"
        elif score >= 25:
            return "Average"
        elif score >= 9:
            return "Low Average"
        elif score >= 2:
            return "Borderline"
        else:
            return "Extremely Low"
    return "—"


def score_label(metric: str) -> str:
    metric = metric.lower()
    labels = {
        "ss": "Standard Score",
        "standard": "Standard Score",
        "standard_score": "Standard Score",
        "t": "T-Score",
        "tscore": "T-Score",
        "t_score": "T-Score",
        "scaled": "Scaled Score",
        "scaledscore": "Scaled Score",
        "scaled_score": "Scaled Score",
        "z": "z-Score",
        "zscore": "z-Score",
        "z_score": "z-Score",
        "percentile": "Percentile",
        "pct": "Percentile",
        "%ile": "Percentile",
    }
    return labels.get(metric, "Score")


def process_csv(input_path: str) -> list:
    rows = []
    with open(input_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            score = float(row["score"])
            metric = row.get("metric", "ss")
            percentile = score_to_percentile(score, metric)
            classification = classify_score(score, metric)
            rows.append({
                "measure": row.get("measure", ""),
                "subtest": row.get("subtest", ""),
                "raw": row.get("raw", ""),
                "score": score,
                "metric": metric,
                "score_label": score_label(metric),
                "percentile": percentile,
                "classification": classification,
            })
    return rows


def format_markdown(rows: list) -> str:
    if not rows:
        return "No scores to display."

    # Group by score metric for cleaner tables
    groups = {}
    for row in rows:
        key = row["score_label"]
        groups.setdefault(key, []).append(row)

    lines = []
    for label, group_rows in groups.items():
        lines.append(f"### {label}-Based Measures\n")
        lines.append(f"| Measure | Subtest/Index | Raw | {label} | Percentile | Classification |")
        lines.append("|---------|--------------|-----|" + "-" * (len(label) + 2) + "|------------|----------------|")
        for r in group_rows:
            raw_str = str(r["raw"]) if r["raw"] else "—"
            score_str = f"{r['score']:.0f}" if r["score"] == int(r["score"]) else f"{r['score']:.1f}"
            pct_str = f"{r['percentile']:.0f}" if r["percentile"] is not None else "—"
            pct_display = f"{pct_str}th" if pct_str != "—" else "—"
            lines.append(f"| {r['measure']} | {r['subtest']} | {raw_str} | {score_str} | {pct_display} | {r['classification']} |")
        lines.append("")

    return "\n".join(lines)


def format_csv_output(rows: list) -> str:
    if not rows:
        return ""

    lines = ["measure,subtest,raw,score,metric,percentile,classification"]
    for r in rows:
        raw_str = str(r["raw"]) if r["raw"] else ""
        pct_str = f"{r['percentile']:.1f}" if r["percentile"] is not None else ""
        lines.append(f"{r['measure']},{r['subtest']},{raw_str},{r['score']},{r['metric']},{pct_str},{r['classification']}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate formatted neuropsychological score tables")
    parser.add_argument("file", help="Input CSV file with scores")
    parser.add_argument("--format", choices=["markdown", "csv"], default="markdown", help="Output format (default: markdown)")
    parser.add_argument("--output", type=str, help="Output file path (default: stdout)")
    args = parser.parse_args()

    if not Path(args.file).exists():
        print(f"Error: File not found: {args.file}")
        sys.exit(1)

    rows = process_csv(args.file)

    if args.format == "markdown":
        output = format_markdown(rows)
    else:
        output = format_csv_output(rows)

    if args.output:
        Path(args.output).write_text(output)
        print(f"Score table written to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
