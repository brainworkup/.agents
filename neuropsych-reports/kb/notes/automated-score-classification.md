---
tags:
  - neuropsychology
  - automation
  - scripts
  - scoring
  - classification
  - Python
type: reference
created: 2026-04-08
---

# Score Classification Script

> Python script for classifying neuropsychological test scores into normative categories. Supports Standard Score, T-Score, Scaled Score, z-Score, and Percentile metrics.

## Related Topics
- [[automation-tools-reference]]
- [[score-classification-wechsler]]
- [[score-classification-heaton]]
- [[score-conversion-metrics]]

---

## Usage

```bash
# Single score
python classify_scores.py --score 85 --metric ss
python classify_scores.py --score 42 --metric t
python classify_scores.py --score 7 --metric scaled

# Batch from CSV
python classify_scores.py --file scores.csv --output classified_scores.csv

# Interactive mode
python classify_scores.py --interactive
```

---

## Classification Systems

- **Wechsler SS:** Very Superior → Extremely Low (7 categories)
- **Heaton T-Score:** Above Average → Severely Impaired (7 categories)
- **Scaled Score:** Maps to Standard Score equivalents
- **z-Score:** Converts to SS then classifies
- **Percentile:** Direct classification from percentile rank

---

## Features

- Single score or batch CSV processing
- Supports all major score metrics
- Automatic metric conversion
- Interactive mode for quick lookups
- Output includes classification, percentile, and z-score equivalent

---

## Location

[scripts/classify_scores.py](/Users/joey/.agents/skills/neuropsych-reports/scripts/classify_scores.py)
