#!/usr/bin/env python3
"""Shared score normalization and classification helpers for neuropsych scripts.

This module centralizes metric aliases, percentile conversion, and
classification logic so other scripts do not drift over time.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path
from typing import Dict, Iterable, List, Optional

CLASSIFICATION_SYSTEMS = {
    "wechsler_ss": [
        (130, float("inf"), "Very Superior"),
        (120, 129, "Superior"),
        (110, 119, "High Average"),
        (90, 109, "Average"),
        (80, 89, "Low Average"),
        (70, 79, "Borderline"),
        (float("-inf"), 69, "Extremely Low"),
    ],
    "heaton_t": [
        (60, float("inf"), "Above Average"),
        (40, 59, "Average"),
        (35, 39, "Low Average"),
        (30, 34, "Mildly Impaired"),
        (25, 29, "Mildly-to-Moderately Impaired"),
        (20, 24, "Moderately Impaired"),
        (float("-inf"), 19, "Severely Impaired"),
    ],
    "wechsler_scaled": [
        (16, float("inf"), "Very Superior"),
        (14, 15, "Superior"),
        (12, 13, "High Average"),
        (8, 11, "Average"),
        (6, 7, "Low Average"),
        (4, 5, "Borderline"),
        (float("-inf"), 3, "Extremely Low"),
    ],
    "bdi_ii": [
        (0, 13, "Minimal"),
        (14, 19, "Mild"),
        (20, 28, "Moderate"),
        (29, 63, "Severe"),
    ],
    "bai": [
        (0, 7, "Minimal"),
        (8, 15, "Mild"),
        (16, 25, "Moderate"),
        (26, 63, "Severe"),
    ],
    "phq9": [
        (0, 4, "Minimal/None"),
        (5, 9, "Mild"),
        (10, 14, "Moderate"),
        (15, 19, "Moderately Severe"),
        (20, 27, "Severe"),
    ],
    "gad7": [
        (0, 4, "Minimal"),
        (5, 9, "Mild"),
        (10, 14, "Moderate"),
        (15, 21, "Severe"),
    ],
}

METRIC_ALIASES = {
    "ss": "ss",
    "standard": "ss",
    "standard_score": "ss",
    "t": "t",
    "tscore": "t",
    "t_score": "t",
    "scaled": "scaled",
    "scaledscore": "scaled",
    "scaled_score": "scaled",
    "z": "z",
    "zscore": "z",
    "z_score": "z",
    "percentile": "percentile",
    "pct": "percentile",
    "%ile": "percentile",
    "bdi": "bdi",
    "bdi-ii": "bdi",
    "bdi2": "bdi",
    "bai": "bai",
    "phq9": "phq9",
    "phq-9": "phq9",
    "gad7": "gad7",
    "gad-7": "gad7",
}

SCORE_LABELS = {
    "ss": "Standard Score",
    "t": "T-Score",
    "scaled": "Scaled Score",
    "z": "z-Score",
    "percentile": "Percentile",
    "bdi": "BDI-II",
    "bai": "BAI",
    "phq9": "PHQ-9",
    "gad7": "GAD-7",
}

REQUIRED_SCORE_COLUMNS = {"score", "metric"}


def normalize_metric(metric: str) -> str:
    normalized = METRIC_ALIASES.get(metric.lower().strip())
    if not normalized:
        raise ValueError(f"Unsupported metric: {metric}")
    return normalized


def classify(score: float, ranges: Iterable[tuple]) -> str:
    for low, high, label in ranges:
        if low <= score <= high:
            return label
    return "Unclassified"


def normal_cdf(z_score: float) -> float:
    return 0.5 * (1 + math.erf(z_score / math.sqrt(2)))


def percentile_from_score(score: float, metric: str) -> Optional[float]:
    metric = normalize_metric(metric)
    if metric == "ss":
        return round(100 * normal_cdf((score - 100) / 15), 1)
    if metric == "t":
        return round(100 * normal_cdf((score - 50) / 10), 1)
    if metric == "scaled":
        return round(100 * normal_cdf((score - 10) / 3), 1)
    if metric == "z":
        return round(100 * normal_cdf(score), 1)
    if metric == "percentile":
        return score
    return None


def classification_from_percentile(percentile: float) -> str:
    if percentile >= 98:
        return "Very Superior"
    if percentile >= 91:
        return "Superior"
    if percentile >= 75:
        return "High Average"
    if percentile >= 25:
        return "Average"
    if percentile >= 9:
        return "Low Average"
    if percentile >= 2:
        return "Borderline"
    return "Extremely Low"


def classify_score(score: float, metric: str) -> Dict[str, Optional[float]]:
    metric = normalize_metric(metric)
    percentile = percentile_from_score(score, metric)

    if metric == "ss":
        classification = classify(score, CLASSIFICATION_SYSTEMS["wechsler_ss"])
    elif metric == "t":
        classification = classify(score, CLASSIFICATION_SYSTEMS["heaton_t"])
    elif metric == "scaled":
        classification = classify(score, CLASSIFICATION_SYSTEMS["wechsler_scaled"])
    elif metric == "z":
        classification = classify(score * 15 + 100, CLASSIFICATION_SYSTEMS["wechsler_ss"])
    elif metric == "percentile":
        classification = classification_from_percentile(score)
    else:
        classification = classify(score, CLASSIFICATION_SYSTEMS[metric])

    return {
        "score": score,
        "metric": metric,
        "score_label": SCORE_LABELS.get(metric, "Score"),
        "classification": classification,
        "percentile": percentile,
    }


def validate_score_csv_columns(fieldnames: Iterable[str]) -> None:
    available = set(fieldnames or [])
    missing = REQUIRED_SCORE_COLUMNS - available
    if missing:
        missing_text = ", ".join(sorted(missing))
        raise ValueError(f"Missing required CSV columns: {missing_text}")


def read_score_rows(input_path: str) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    with open(input_path, "r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        validate_score_csv_columns(reader.fieldnames or [])
        for line_number, row in enumerate(reader, start=2):
            try:
                score = float(row["score"])
                metric = normalize_metric(row["metric"])
                result = classify_score(score, metric)
            except Exception as exc:  # deliberate broad catch for row-level reporting
                raise ValueError(f"Error parsing row {line_number}: {exc}") from exc

            rows.append(
                {
                    "measure": row.get("measure", ""),
                    "subtest": row.get("subtest", ""),
                    "raw": row.get("raw", ""),
                    **result,
                }
            )
    return rows


def format_score_value(score: float) -> str:
    return f"{score:.0f}" if score == int(score) else f"{score:.1f}"


def default_output_path(input_path: str, suffix: str) -> str:
    source = Path(input_path)
    return str(source.with_name(f"{source.stem}_{suffix}{source.suffix}"))
