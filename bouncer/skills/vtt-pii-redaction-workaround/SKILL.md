---
description: Workaround approach for PII redacting VTT files when the full pipeline times out.
name: vtt-pii-redaction-workaround
tags: [pii, vtt, subtitle, redaction, workaround, timeout]
---

# VTT File PII Redaction (Workaround for Timeout Issues)

## Overview

When the full PII redactor pipeline times out on large VTT files, use a simpler regex-based approach to redact key identifiers.

## When to Use

- VTT subtitle files that are too large for the full pipeline
- When the PII redactor script times out (>60s)
- When read_file tool returns stale/cached content
- Simple name/location redaction is sufficient (no need for NER models)

## Approach

### Step 1: Extract Transcript Text

```python
import re

with open('file.vtt', 'r') as f:
    full_text = f.read()

lines = full_text.split('\n')
transcript_lines = []
for line in lines:
    # Remove line number prefix like "     1|" or "     5|"
    line = re.sub(r'^\s*\d+\|\s*', '', line)
    # Skip WEBVTT header
    if line.startswith('WEBVTT'):
        continue
    # Skip timestamp lines (e.g., "00:01:16.930 --> 00:01:17.930")
    if re.match(r'^\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}$', line):
        continue
    # Skip sequence numbers
    if re.match(r'^\d+$', line):
        continue
    # Skip empty lines
    if not line.strip():
        continue
    transcript_lines.append(line)

transcript_text = '\n'.join(transcript_lines)
```

### Step 2: Define PII Patterns

```python
pii_patterns = [
    # Patient name - "R Connor Wark" (appears as speaker)
    (r'\bR\s+Connor\s+Wark\b', '[REDACTED-PATIENT-NAME]'),
    # Clinician name - "Joey Trampush" (appears as speaker)
    (r'\bJoey\s+Trampush\b', '[REDACTED-CLINICIAN-NAME]'),
    # Geographic locations
    (r'\bNevada\b', '[REDACTED-STATE]'),
    (r'\bVegas\b', '[REDACTED-CITY]'),
    (r'\bLas Vegas\b', '[REDACTED-CITY]'),
    (r'\bTexas\b', '[REDACTED-STATE]'),
    (r'\bSan Diego\b', '[REDACTED-CITY]'),
    # Company names
    (r'\bMZM Resorts International\b', '[REDACTED-EMPLOYER]'),
    (r'\bOracle\b', '[REDACTED-EMPLOYER]'),
    # University reference
    (r'\bTCU\b', '[REDACTED-UNIVERSITY]'),
]
```

### Step 3: Apply Redactions

```python
redacted_text = transcript_text
for pattern, replacement in pii_patterns:
    redacted_text = re.sub(pattern, replacement, redacted_text)

with open('redacted_output.txt', 'w') as f:
    f.write(redacted_text)
```

## Pitfalls

### read_file Tool Caching
- The read_file tool may return stale content: "File unchanged since last read"
- **Workaround:** Use terminal heredoc or read in chunks with offset

### PII Redactor Timeout
- Full pipeline can timeout after 60s on large files
- **Workaround:** Use simpler regex-based approach for VTT files

### Speaker Labels
- VTT files use speaker labels like `R Connor Wark:` or `Joey Trampush:`
- These are the primary PII source in clinical interview transcripts
- Redact the name portion before the colon

## Verification

```bash
# Check redaction coverage
grep -ci "Patient Name" redacted_output/*_SuperClinical_redacted.md
grep -ci "Joey" redacted_output/*_SuperClinical_redacted.md
```

## When to Use Full Pipeline Instead

- PDF clinical reports with complex layouts
- Need for NER-based entity detection
- When HIPAA Safe Harbor validation is required
- When name propagation is needed for consistency

## Notes

- This approach is simpler but less comprehensive than the full 3-layer pipeline
- Best for VTT files where names are primarily in speaker labels
- For full HIPAA compliance, still run the full pipeline on PDF reports
