---
name: hipaa-pii-redactor
description: Local HIPAA-compliant PII redaction pipeline for clinical assessment PDFs using OpenMed-PII NER models, regex safety net, and whitelist-only name propagation.
version: "1.1"
---

# HIPAA-Compliant PII Redaction Pipeline

Local, headless pipeline for redacting PHI from clinical/neuropsychological
assessment PDFs.  Combines transformer NER with a regex safety net and
whitelist-only name propagation, then validates against the 18 HIPAA Safe Harbor
identifiers.

## Architecture (3-layer + 2 filters)

```
PDF  -->  PyMuPDF text extraction
              |
              v
         NER per-page (OpenMed-PII)
              |
              v
         filter_subword_fragments  <-- Filter 1: remove mid-word NER artifacts
              |
              v
         Remap page offsets to full_text  <-- Fix: coordinate system alignment
              |
              v
         Regex post-processor
              |
              v
         Merge & dedup
              |
              v
         Name propagation (whitelist only)  <-- Filter 2: PII_KNOWN_NAMES env var
              |
              v
         Redacted Markdown + HIPAA report
```

### Layer 1 — NER (core)
- OpenMed-PII models (public, ~335-434M params, run fully local on CPU).
- Page-level processing with token-aware chunking (490-token window, 30-token overlap).
- `aggregation_strategy="simple"` merges subword fragments.
- **Filter 1**: `filter_subword_fragments()` removes entities where adjacent
  characters are letters (the model sometimes tags subword pieces like 'TRA',
  'MP', 'USH' from "TRAMPUSH", or 'Y' from "JOEY").
- **Coordinate fix**: NER runs per-page (page-relative spans), but regex runs
  on the full document. Page offsets are tracked and added to remap NER spans
  to full-text coordinates before merging.

### Layer 2 — Regex safety net
Catches domain-specific structured patterns that NER consistently misses.
Uses capture groups (`"group": 1`) so only the PII portion is redacted,
preserving surrounding boilerplate text.

#### Name patterns (HIPAA #1)
| Pattern key | Example | Notes |
|---|---|---|
| `patient_name_header_id` | `Matthew Meyer/MM25` | Name + ID suffix |
| `patient_name_header_report` | `Report for Cole Glaser` | Capture group isolates name |
| `patient_name_field_label` | `Child's Name/ID:\nCole Glaser` | Form field label + newline |
| `patient_name_parent_label` | `Parent's Name:\nGina Glaser` | Role-specific label |
| `patient_name_examinee_label` | `Examinee Name:\nMoses Goldschmidt` | No colon variant |
| `patient_name_role_label` | `Referral source:\nShannon Soller` | 12 role labels; handles `MRS.` all-caps honorifics |
| `patient_name_page_header` | `2025/12/07, Page 2\nMoses Goldschmidt\nCopyright` | Running page headers |

#### Other HIPAA patterns
| Pattern | HIPAA ID | Notes |
|---|---|---|
| `date_mm_dd_yyyy` | 3 | `MM/DD/YYYY` with common separators |
| `date_yyyy_mm_dd` | 3 | `YYYY-MM-DD` format |
| `date_month_dd_yyyy` | 3 | `April 4, 2025` |
| `street_address` | 2 | Number + street name + suffix (15 suffixes) |
| `phone_number` | 4 | North American format |
| `fax_number` | 5 | Prefixed with `fax:` or `f:` |
| `email` | 6 | Standard RFC pattern |
| `ssn` | 7 | `XXX-XX-XXXX` |
| `mrn` | 8 | Labeled: MRN, Patient ID, Chart No, etc. |
| `insurance_id` | 9 | Labeled: insurance, policy, plan, member |
| `account_number` | 10 | Labeled: account, acct, billing |
| `license_number` | 11 | Driver's license, DL, license # |
| `url` | 14 | `http://` or `https://` |
| `ip_address` | 15 | Standard IPv4 |

### Layer 3 — Name propagation (whitelist-only, via ENV VAR)
After NER+regex merge, scans for unredacted instances of names from an explicit
whitelist. **Requires `PII_KNOWN_NAMES` env var** — if not set, propagation is
skipped entirely (safe default).

```bash
# Only propagate these specific names
PII_KNOWN_NAMES="Moses,Natalie,Goldschmidt,Trampush,Joey"

# Skip propagation entirely (NER + regex still run)
# unset PII_KNOWN_NAMES
```

**Why whitelist-only?** The NER model produces false positives on common English
words that happen to be names ("May", "Max", "Rob", "Dr", "Ms"). The old
auto-propagation (propagate any name seen 2+ times) caused catastrophic
over-redaction — tagging 385+ false instances in a single PDF and shredding
readability by redacting inside words.

The whitelist approach ensures only verified patient/clinician names are
swept for leaks, while the NER + regex layers independently handle structured
contexts (headers, form fields, etc.).

## Quick Start

```bash
# 1. Create environment and install dependencies
cd /path/to/project
python -m venv .venv
source .venv/bin/activate
pip install transformers pymupdf pandas torch

# 2. Download models (public, no token needed)
huggingface-cli download OpenMed-LLM/OpenMed-PII-SuperClinical-Large-434M-v1 \
  --local-dir ./models/OpenMed-PII-SuperClinical-Large-434M-v1
huggingface-cli download OpenMed-LLM/OpenMed-PII-BiomedELECTRA-Large-335M-v1 \
  --local-dir ./models/OpenMed-PII-BiomedELECTRA-Large-335M-v1

# 3. Set known patient/clinician names for propagation
export PII_KNOWN_NAMES="Moses,Natalie,Goldschmidt,Trampush,Joey"

# 4. Place PDFs in ./pdfs/ and run
PYTORCH_ENABLE_MPS_FALLBACK=1 python pii_redactor.py
```

## Key Implementation Details

### Merge logic
- NER entities take priority over regex when spans overlap.
- Entities sorted by (start, -length) so longer matches win ties.
- Overlap check: `ent["start"] < merged[-1]["end"]`.

### Subword fragment filter
The OpenMed-PII models sometimes tokenize multi-word names into subword pieces
("JOEY TRAMPUSH" -> 'JOE', 'Y', 'TRA', 'MP', 'USH') and return them as
separate entities. The `filter_subword_fragments()` function removes any entity
where the character immediately before or after its span is a letter, indicating
it's inside a larger word rather than at a true word boundary.

### Page offset remapping
NER runs per-page (for manageable token counts), producing page-relative
character spans. Regex runs on the concatenated full text. Before merging,
NER spans are shifted by the cumulative page offset to align coordinate
systems. Without this, page 2+ NER entities land at wrong positions in the
full text, causing mid-word redactions.

### Token chunking (offset_mapping)
- Uses `tokenizer(..., return_offsets_mapping=True)` for accurate character
  positions, avoiding whitespace normalization mismatches from `text.find()`.
- `max_tokens=490` with 30-token overlap.

### Redaction format
- PII replaced with `[ENTITY_GROUP_UPPERCASE]` tags.
- Reverse-sorted application (end -> start) preserves span indices.

### HIPAA compliance report
Per-PDF, per-model report mapping entity types to the 18 Safe Harbor IDs.
Status: `PASS` (all text IDs found), `REVIEW` (some missing — OK if absent),
or `PARTIAL`. Non-text IDs (16: biometrics, 17: photographs) always flagged for
manual review.

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `PII_KNOWN_NAMES` | No | Comma-separated names for propagation. If unset, propagation skipped. |
| `PYTORCH_ENABLE_MPS_FALLBACK` | Yes (macOS) | Prevents MPS kernel timeouts on Apple Silicon. |

## Known Limitations and Pitfalls

### Street address false positives
The `street_address` regex can match numbered rating-scale items (e.g., "51 items
that best..." from Conners). Consider tightening by requiring a word boundary
after the suffix or adding a negative lookahead for common scale words.

### BiomedELECTRA tokenization artifacts
The BiomedELECTRA model sometimes produces subword tokens with `##` prefix
(e.g., `##the`, `##es`). The subword fragment filter handles this.

### Name propagation is only as good as the whitelist
If a patient name is not in `PII_KNOWN_NAMES`, the propagation layer won't
catch leaked instances in narrative text. The NER + regex layers may still
catch some, but not reliably. Always verify the whitelist covers all relevant
names before running.

### MPS memory issues on Apple Silicon
Use `PYTORCH_ENABLE_MPS_FALLBACK=1` and run on CPU (`device=-1`). MPS can
cause kernel timeouts or hangs with these models. CPU inference on Apple Silicon
is still fast (~2-20s per PDF depending on length).

### Python `re` limitation
No variable-width lookbehinds. All regex patterns use capture groups with
`"group": 1` to isolate PII from surrounding boilerplate text.

## Extending for New Document Types

When adding support for new PDF formats:
1. Extract text with PyMuPDF and inspect the raw layout (`fitz.open().get_text()`).
2. Check what NER catches vs misses by running the pipeline and grepping for known PII.
3. If structured headers are missed, add a new regex pattern following the existing convention:
   - Use a descriptive key (e.g., `patient_name_school_label`).
   - Use capture group `"group": 1` to isolate just the name.
4. Add the patient/clinician names to `PII_KNOWN_NAMES` for propagation.

## File Structure

```
project/
  pii_redactor.py          # Main pipeline script
  pdfs/                    # Input PDFs
  redacted_output/         # Output redacted Markdown files
    *_SuperClinical_redacted.md
    *_BiomedELECTRA_redacted.md
    comparison_summary.csv
  models/                  # Local model directories
    OpenMed-PII-SuperClinical-Large-434M-v1/
    OpenMed-PII-BiomedELECTRA-Large-335M-v1/
```

## Reference: 18 HIPAA Safe Harbor Identifiers

1. Names
2. Geographic subdivisions smaller than state (address, city, ZIP)
3. Dates (except year) — DOB, admission, discharge, service dates
4. Telephone numbers
5. Fax numbers
6. Email addresses
7. Social Security numbers
8. Medical record numbers
9. Health plan beneficiary numbers
10. Account numbers
11. Certificate/license numbers
12. Vehicle identifiers and serial numbers
13. Device identifiers and serial numbers
14. Web URLs
15. IP addresses
16. Biometric identifiers (fingerprints, voiceprints)
17. Full-face photographs
18. Any other unique identifying characteristic
