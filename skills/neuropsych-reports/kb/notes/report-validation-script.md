---
tags:
  - neuropsychology
  - automation
  - scripts
  - validation
  - report-quality
  - Python
type: reference
created: 2026-04-08
---

# Report Validation Script

> Python script for validating neuropsychological reports against required sections based on report type (full, brief, pediatric, geriatric, forensic).

## Related Topics
- [[automation-tools-reference]]
- [[report-writing-guide]]
- [[compliance-checker-script]]

---

## Usage

```bash
# Default (full report)
python validate_neuropsych_report.py report.md

# Specify report type
python validate_neuropsych_report.py report.md --type full
python validate_neuropsych_report.py report.md --type brief
python validate_neuropsych_report.py report.md --type pediatric
python validate_neuropsych_report.py report.md --type geriatric
python validate_neuropsych_report.py report.md --type forensic
```

---

## Required Sections by Report Type

**Full:** Header/Demographics, Reason for Referral, Background, Behavioral Observations, Test Results, Summary/Impressions, Recommendations

**Brief:** Abbreviated sections from full evaluation

**Pediatric:** Full + developmental history, school functioning

**Geriatric:** Full + functional status, dementia staging, capacity considerations

**Forensic:** Full + validity assessment, psycholegal question, chain of custody

---

## Features

- Checks for required sections and key elements
- Validates demographic fields
- Reports missing sections and warnings
- Supports multiple report types

---

## Location

[scripts/validate_neuropsych_report.py](/Users/joey/.agents/skills/neuropsych-reports/scripts/validate_neuropsych_report.py)
