# Refactor Review for `neuropsych-reports`

## High-level findings

The current workspace has strong content, but the architecture is overloaded.

### Main code and design smells

1. **Monolithic skill design**
   - `SKILL.md` is very large and mixes orchestration, domain guidance, templates, compliance, and integration notes.
   - This makes maintenance hard and increases context load.

2. **Mixed concerns in directories**
   - `assets/` currently contains templates, prompts, checklists, Quarto resources, and general resources.
   - Several prompt files behave more like references than assets.

3. **Duplicate scoring logic**
   - `classify_scores.py` and `generate_score_table.py` both implement percentile conversion and classification logic.
   - This creates drift risk.

4. **Inconsistent classification language**
   - Some parts use Wechsler-style labels like `Very Superior` / `Borderline`.
   - Other parts of the skill describe AACN-style ranges like `Exceptionally high` / `Below average`.
   - This could create inconsistent downstream reports.

5. **Validator brittleness**
   - `validate_neuropsych_report.py` relies on regex phrase matching only.
   - It is useful, but fragile for template variation and could produce false positives/negatives.

6. **Compliance checker scope drift**
   - `compliance_checker.py` mixes HIPAA with GCP/FDA language that appears more appropriate for broader clinical research reporting than routine neuropsych reporting.
   - For Luria, this should probably be split into domain-specific validators.

7. **Knowledge duplication across `kb/` and `references/`**
   - Some topics look overlapping or adjacent without a clear loading rule.
   - This makes it harder to know what the main skill should read first.

## Script-specific recommendations

### `scripts/classify_scores.py`
**Issues**
- hard-coded classification systems
- no schema validation for CSV input
- minimal error handling for malformed rows
- output contract is implicit, not documented in a machine-readable way

**Refactor**
- extract shared conversion/classification logic into a reusable module
- define canonical classification systems explicitly
- add validation for required CSV columns
- emit structured JSON as an option

### `scripts/generate_score_table.py`
**Issues**
- duplicates logic from `classify_scores.py`
- formatting and business logic are tightly coupled
- CSV output is manually concatenated, which is fragile

**Refactor**
- import shared score engine from one place
- separate parsing, normalization, and rendering
- use Python CSV writer instead of raw string concatenation for CSV output

### `scripts/validate_neuropsych_report.py`
**Issues**
- regex-only section detection is brittle
- content quality checks are mixed with completeness checks
- warning logic is clever but hard to extend

**Refactor**
- split into `section_validator`, `quality_validator`, and `report_summary`
- support configurable rule sets by report type
- consider heading-based detection for markdown reports

### `scripts/compliance_checker.py`
**Issues**
- too broad for neuropsych workflow
- likely false confidence from simple pattern matching
- limited reporting detail

**Refactor**
- replace with separate neuropsych-focused review checks
- keep HIPAA/de-identification as one tool
- make consent/test-security/report-release checks separate

### `scripts/check_deidentification.py`
**Strengths**
- best-structured script of the current set
- clearer output and recommendation logic

**Remaining issues**
- regex examples can return tuples because of capture groups
- some patterns are noisy and may overflag
- scanning text only may not be enough for structured reports later

**Refactor**
- normalize regex capture behavior
- add ignore lists / allow-lists
- output line-based locations where possible

## Recommended target architecture

### Keep the repo organized like this

```text
neuropsych-reports/
├── SKILL.md
├── scripts/
│   ├── score_engine.py
│   ├── classify_scores.py
│   ├── generate_score_table.py
│   ├── validate_neuropsych_report.py
│   └── check_deidentification.py
├── references/
│   ├── architecture/
│   ├── workflows/
│   ├── prompts/
│   └── ...domain references...
├── assets/
│   ├── templates/
│   ├── checklists/
│   ├── quarto/
│   ├── resources/
│   └── examples/
└── kb/
```

## Immediate next refactors

1. Create a shared `score_engine.py`
2. Move prompt library documentation into `references/prompts/`
3. Move templates/checklists into dedicated `assets/` subfolders
4. Shrink the monolithic `SKILL.md` by moving detailed sections into references
5. Build the six Luria skills as a thin orchestrated system

## Prompts answer

For your prompt set:
- operational prompts used by the agent while reasoning → `references/prompts/`
- prompt templates used as resources → `assets/templates/`
- example prompt outputs → `assets/examples/`

That gives you a clean rule you can keep using.
