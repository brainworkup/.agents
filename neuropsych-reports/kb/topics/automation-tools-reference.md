---
tags:
  - neuropsychology
  - automation
  - scripts
  - python
  - tools
  - pillar-page
type: reference
created: 2026-04-08
---

# Automation Tools Reference

> Python scripts and utilities for neuropsychological report automation, including score classification, report validation, and compliance checking.

## Related Topics
- [[automated-score-classification]]
- [[report-validation-script]]
- [[compliance-checker-script]]
- [[deidentification-script]]
- [[score-table-generation]]

---

## Available Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `classify_scores.py` | Convert scores to normative classifications | CLI, interactive, or CSV batch |
| `validate_neuropsych_report.py` | Check report completeness | Validate sections |
| `compliance_checker.py` | HIPAA and ethical compliance | Check PHI exposure |
| `check_deidentification.py` | Verify de-identification | Safe Harbor compliance |
| `generate_score_table.py` | Format score tables | Generate tables from data |

---

## Score Classification Script

**Purpose:** Automatically classify neuropsychological test scores into normative categories.

**Supported Metrics:**
- Standard Score (SS)
- T-Score
- Scaled Score
- z-Score
- Percentile
- BDI-II, BAI, PHQ-9, GAD-7

**Usage:**
```bash
# Single score
python classify_scores.py --score 85 --metric ss

# CSV batch processing
python classify_scores.py --file scores.csv --output classified.csv

# Interactive mode
python classify_scores.py --interactive
```

**Classification Systems:**
- Wechsler (Very Superior to Extremely Low)
- Heaton T-Scores (Above Average to Severely Impaired)
- Self-report measures (Minimal to Severe)

**Output:** Score, classification, and percentile when applicable.

---

## Report Validation Script

**Purpose:** Verify report completeness against required sections.

**Checks:**
- Required sections present (Reason for Referral, Background, Behavioral Observations, etc.)
- Test list includes versions
- Validity statement present
- Recommendations section exists
- Signature block complete

---

## Compliance Checker

**Purpose:** Verify HIPAA compliance and ethical standards.

**Checks:**
- PHI exposure (18 identifiers)
- Test security violations (actual test items)
- Informed consent mention
- Validity documentation
- Appropriate language for scores

---

## De-identification Script

**Purpose:** Verify Safe Harbor de-identification.

**Checks:**
- All 18 HIPAA identifiers removed
- Dates limited to year only
- Ages >89 aggregated
- Indirect identifiers reviewed

---

## Score Table Generation

**Purpose:** Generate formatted score tables from data input.

**Output:**
- Markdown tables
- Proper formatting
- Consistent decimal places
- Automatic classification

---

## Implementation Notes

All scripts are located in: `/scripts/` directory

**Requirements:**
- Python 3.x
- Standard library only (no external dependencies for most)
- CSV processing support

---

## Source
- Original: Scripts in `scripts/` directory