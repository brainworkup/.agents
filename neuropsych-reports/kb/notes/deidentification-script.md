---
tags:
  - neuropsychology
  - automation
  - scripts
  - de-identification
  - HIPAA
  - privacy
  - Python
type: reference
created: 2026-04-08
---

# De-identification Script

> Python script for scanning clinical reports for the 18 HIPAA identifiers that require removal for de-identified documentation.

## Related Topics
- [[automation-tools-reference]]
- [[hipaa-compliance-neuropsych]]
- [[compliance-checker-script]]

---

## Usage

```bash
# Scan and display violations
python check_deidentification.py <input_file>

# Save violations to JSON
python check_deidentification.py <input_file> --output violations.json
```

---

## What It Scans

The script checks for all 18 HIPAA identifiers:

1. Names (patient, family, providers)
2. Geographic subdivisions smaller than state
3. Dates (except year)
4. Phone numbers
5. Fax numbers
6. Email addresses
7. Social Security numbers
8. Medical record numbers
9. Health plan beneficiary numbers
10. Account numbers
11. Certificate/license numbers
12. Vehicle identifiers
13. Device identifiers
14. Web URLs
15. IP addresses
16. Biometric identifiers
17. Photographs
18. Other unique identifiers

---

## Features

- Regex-based pattern matching for each identifier type
- Severity ratings (HIGH, MEDIUM, LOW)
- Line-by-line violation reporting
- JSON export for integration with other tools
- Handles names, dates, SSNs, MRNs, geographic data, and more

---

## Location

[scripts/check_deidentification.py](/Users/joey/.agents/skills/neuropsych-reports/scripts/check_deidentification.py)
