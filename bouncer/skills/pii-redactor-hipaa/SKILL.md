---
description: PII redaction pipeline combining NER models with regex post-processing and HIPAA Safe Harbor compliance validation for clinical PDF reports.
name: pii-redactor-hipaa
tags: [pii, hipaa, nlp, de-identification, clinical, pdf, transformers]
---

# PII Redactor with HIPAA Safe Harbor Compliance

## Overview

A 3-layer PII detection pipeline for clinical PDF reports:
1. **NER models** — transformer-based named entity recognition (e.g., OpenMed models)
2. **Regex post-processor** — pattern-based rules for HIPAA-specific formats NER misses
3. **HIPAA Safe Harbor validator** — checks all 18 identifiers are addressed

## Key Pitfalls

### marimo Notebooks
- `marimo run nb.py` starts a web server and renders in browser — it does NOT execute cells headlessly.
- For CLI/headless execution, extract the Python logic and run directly with `python script.py`.

### Model-Specific Issues
- **MPS (Apple Silicon GPU)**: OOMs on large PDF text (>500 tokens). Use `device=-1` to force CPU inference.
- **BiomedELECTRA-335M**: Has a 512 token limit. Use token-aware chunking (not word-based — tokenizer can exceed 512 even with 400 words). Decode chunks back to text and offset positions.
- **SuperClinical-434M**: Handles longer sequences natively.

### dotenvx Encrypted .env
- Private key env var is `DOTENV_PRIVATE_KEY` (not `DOTENV_KEY`).
- Key is stored in `.env.keys` file (convention, not the env var name).
- Test decryption round-trip before using: `export DOTENV_PRIVATE_KEY=<key> && dotenvx get VAR_NAME -f .env`

### Regex Pattern Debugging
- `\\b` word boundary doesn't work before `/` characters — use simpler patterns without `\\s*` between name and slash for patterns like "Matthew Meyer/MM25".
- Always `repr()` the actual PDF-extracted text to see hidden characters before writing regex.
- NER model overlapping spans can suppress regex matches during dedup — merge strategy matters (NER priority or longest span).
- **Python `re` does NOT support variable-width lookbehinds** (`re.PatternError: look-behind requires fixed-width pattern`). Use capture groups with a `"group": N` key instead.
- **Don't match standalone names without context** — a pattern like `(?:^|\n)\s*([A-Z][a-z]{2,}\s+[A-Z][a-z]{3,})\s*(?:\n|$)` matched 140+ false positives on CAARS (rating scales, section headers, etc.). Always anchor patterns to context (labels, "Report for", etc.).
- **Capture groups for selective redaction**: Use `"group": 1` in pattern definitions so only the PII portion gets redacted, not surrounding boilerplate (e.g., redact "Cole Glaser" but keep "Report for"). The `regex_scan` function must handle this: `grp = info.get("group", 0)` and use `m.start(grp)` / `m.end(grp)` for spans.

### Clinical Report Name Patterns (battle-tested across 13 PDF types)
These patterns catch names that NER consistently misses in clinical assessment headers.
All use `group: 1` to redact only the name, not surrounding boilerplate.

| Pattern Key | Regex (simplified) | Example | PDFs Found In |
|-------------|-------------------|---------|---------------|
| `patient_name_header_id` | Name/ID pattern | "Matthew Meyer/MM25" | CAARS |
| `patient_name_header_report` | "Report for FirstName LastName" (group 1) | "Report for Cole Glaser" | CEFI, Conners 4 |
| `patient_name_field_label` | `Name/ID:\nFirstName LastName` (group 1) | "Child's Name/ID:\nCole Glaser" | CEFI, Conners 4 |
| `patient_name_parent_label` | `Parent's Name:\nFirstName LastName` (group 1) | "Parent's Name:\nGina Glaser" | Conners 4 |
| `patient_name_examinee_label` | `Examinee Name\nFirstName LastName` (group 1) | "Examinee Name:\nMoses Goldschmidt" | WISC-5 |
| `patient_name_role_label` | Role label + honorific + name (group 1) | "Referral source:\nShannon Soller", "Teacher:\nMRS. Cohen", "Counselor:\nDr Robin" | BASC-3 SDH, CEFI |
| `patient_name_page_header` | Running page header date+page above name (group 1) | "2025/12/07, Page 2\n Moses Goldschmidt\n" | KTEA-3, D-KEFS, WISC-5 |

**Role label pattern details**: Covers `Referral source`, `Referred by`, `Teacher`, `Examiner`, `Evaluator`, `Psychologist`, `Counselor`, `Therapist`, `Case manager`, `Social worker`, `Clinician`. Handles both title-case honorifics (Dr, Mrs) and all-caps (MRS., MR.) plus up to 3-word names (honorific + first + last).

### Name Propagation (NER consistency fix)
NER models are inconsistent — they may catch "Natalie" 3 times but miss 17 other instances in the same document. The `propagate_names()` function solves this:
1. Collect all detected name words from NER + regex (strip `##` subword prefixes)
2. Filter to names seen 2+ times (avoids false positives on common words)
3. Sweep the full text for any unredacted instances of those names
4. Only add entities that don't overlap existing redacted spans

This caught +35 instances in nse_summary (Natalie), +6 in feedback (Moses), +188 in basc3_prs, and +385 in wisc5.

**Key threshold**: `c >= 2` (minimum 2 detections to propagate). Lower values cause over-redaction of common words like "High", "Step", "Report".

## Architecture

```
PDF → PyMuPDF (fitz) → page-by-page text
  ├─ NER models (per page, with token-aware chunking)
  │     → entity dicts {entity_group, word, start, end, score}
  ├─ Regex scanner (full text)
  │     → entity dicts {entity_group, word, start, end, score=1.0, source=regex}
  ├─ Merge + dedup (NER priority on overlap)
  ├─ Name propagation (sweep for unredacted instances of known names, min 2 detections)
  └─ Redact text (sort by start descending)
       → HIPAA 18-identifier validation
       → Compliance report + redacted markdown
```

## HIPAA 18 Safe Harbor Identifiers

Must all be removed/checked for de-identification:

| ID | Identifier | Detection Method |
|----|-----------|-----------------|
| 1  | Names | NER + regex (report header pattern) |
| 2  | Geographic data < state | NER + regex (street address) |
| 3  | Dates (except year) | NER + regex (multiple date formats) |
| 4  | Telephone numbers | regex |
| 5  | Fax numbers | regex |
| 6  | Email addresses | regex |
| 7  | SSN | regex (XXX-XX-XXXX) |
| 8  | Medical record numbers | regex (MRN, Chart No, etc.) |
| 9  | Health plan/beneficiary numbers | regex |
| 10 | Account numbers | regex + NER |
| 11 | Certificate/license numbers | regex |
| 12 | Vehicle identifiers | regex |
| 13 | Device identifiers/serial numbers | regex |
| 14 | Web URLs | regex |
| 15 | IP addresses | regex |
| 16 | Biometric identifiers | Manual review (non-text) |
| 17 | Photographs/images | Manual review (non-text) |
| 18 | Other unique characteristics | NER (catch-all) |

## Model Comparison Notes

Comparing OpenMed models on 13 clinical assessment PDFs (BASC-3 PRS/SDH, CAARS, CEFI, Conners-4, CVLT, Feedback, KTEA-3, D-KEFS, NEPSY-2, NSE Summary, Pegboard, WISC-5):

- **SuperClinical-434M** (DeBERTa): Better at clinical-specific types (DOB, education_level, postcode). More conservative overall. ~2x slower on CPU. Benefits more from name propagation (+188 in basc3_prs, +385 in wisc5).
- **BiomedELECTRA-335M** (BERT): Faster (~1.8x). Broader coverage (catches credit_card, account_number, user_name). Noisier on names (more false positives). Sometimes catches names SuperClinical misses entirely (e.g., CVLT child — 0 vs 26 NER entities).
- Both miss clinical report header patterns — regex post-processor essential for all PDF types.
- Both miss inline narrative name instances inconsistently — name propagation layer essential for narrative reports (NSE summary, feedback documents).

## Quick Commands

```bash
# Run PII redactor (all PDFs in pdfs/ → redacted_output/)
cd /Users/joey/PII && .venv/bin/python pii_redactor.py

# Check if a regex pattern matches actual PDF text
python3 -c "
import fitz, re
doc = fitz.open('file.pdf')
for page in doc:
    text = page.get_text()
    for m in re.finditer(r'PATTERN', text):
        print(repr(m.group()))
"

# Quick leak check: grep for known patient names in redacted output
grep -ci "Patient Name" redacted_output/*_SuperClinical_redacted.md

# Test dotenvx decryption
export DOTENV_PRIVATE_KEY=$(grep DOTENV_PRIVATE_KEY .env.keys | cut -d= -f2)
dotenvx get HF_TOKEN -f .env
```
