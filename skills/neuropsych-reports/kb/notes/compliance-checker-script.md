---
tags:
  - neuropsychology
  - automation
  - scripts
  - compliance
  - HIPAA
  - GCP
  - FDA
  - Python
type: reference
created: 2026-04-08
---

# Compliance Checker Script

> Python script for checking clinical reports for regulatory compliance across HIPAA, Good Clinical Practice (GCP), and FDA requirements.

## Related Topics
- [[automation-tools-reference]]
- [[hipaa-compliance-neuropsych]]
- [[report-validation-script]]
- [[deidentification-script]]

---

## Usage

```bash
python compliance_checker.py <report_file>
```

---

## Compliance Checks

### HIPAA
- Consent statement present
- De-identification documentation

### GCP (Good Clinical Practice)
- IRB/ethics approval reference
- Protocol compliance statement
- Informed consent documentation

### FDA
- Study ID (IND/IDE/protocol number)
- Safety reporting (adverse events/SAE)

---

## Features

- Scans report text for required compliance elements
- Flags missing documentation
- Supports HIPAA, GCP, and FDA frameworks
- JSON output option

---

## Location

[scripts/compliance_checker.py](/Users/joey/.agents/skills/neuropsych-reports/scripts/compliance_checker.py)
