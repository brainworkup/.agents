# Luria Skill Architecture

## Recommended Main Skill System

### Orchestrator
- `luria-neuropsych-orchestrator`
  - Purpose: route a case through intake, score processing, interpretation, report drafting, and quality review.
  - Role: coordinator, not the place for all detailed instructions.

### Supporting Skills
- `luria-case-intake`
  - Intake packet parsing
  - NSE transcript extraction
  - Records summary
  - Referral question normalization
  - Missing-data checklist

- `luria-score-processing`
  - Score normalization
  - Classification logic
  - Score table generation
  - Cross-test metric conversion
  - Structured intermediate outputs (JSON/CSV/Markdown)

- `luria-interpretation`
  - Domain-level interpretation
  - Premorbid/context anchoring
  - Pattern analysis across domains
  - Differential considerations
  - Functional implications

- `luria-report-writing`
  - Report assembly
  - Template selection by report type
  - Section drafting
  - Recommendation writing
  - Quarto/Markdown/DOCX/PDF output flow

- `luria-quality-review`
  - Completeness validation
  - PHI/HIPAA check
  - Internal consistency checks
  - Test security review
  - Style/tone/legal-risk review

## Why this is the best long-term architecture

1. Separates workflow stages cleanly.
2. Keeps each skill smaller and easier to maintain.
3. Allows reuse of helper skills by reference instead of duplication.
4. Makes future automation scripts easier to place and test.
5. Lets the orchestrator stay thin and stable while subskills evolve.

## Recommended internal layout for each skill

```text
skill-name/
├── SKILL.md
├── scripts/
├── references/
└── assets/
```

## What goes in each subdirectory

### `scripts/`
Put deterministic, executable logic here.

Examples:
- score classification scripts
- report validators
- de-identification scanners
- table renderers
- file converters
- prompt-to-template render helpers

Rule of thumb: if the same logic should run the same way every time, it belongs in `scripts/`.

### `references/`
Put guidance the model may need to read while working.

Examples:
- report-writing rules
- diagnostic framework notes
- score interpretation references
- workflow docs
- prompt library documentation
- schema definitions

Rule of thumb: if it is for reading, reasoning, or instruction lookup, it belongs in `references/`.

### `assets/`
Put files used as inputs or outputs but not primarily meant to be read into context.

Examples:
- report templates
- Quarto resources
- logos/signatures
- CSL/BIB files
- example outputs
- checklists used as deliverables

Rule of thumb: if a file is mainly a resource/template/artifact, it belongs in `assets/`.

## Where prompts should go

Prompts should usually **not** live in `assets/prompts` unless they are treated as static output resources.

Recommended split:

- Put **working prompts, system prompts, extraction prompts, and implementation prompts** in:
  - `references/prompts/`
- Put **prompt templates that are rendered into outputs or passed untouched to a downstream tool** in:
  - `assets/templates/` or `assets/examples/`

### Prompt placement rules
- `.md` or `.json` prompt specs used for reasoning/instructions → `references/prompts/`
- Example prompt outputs → `assets/examples/`
- Reusable scaffold prompt templates with placeholders → `assets/templates/`

## Can helper skills just be referenced?

Yes — and that is the preferred pattern.

Use helper skills by reference when:
- they are already well-scoped
- they solve a reusable subproblem
- you do not need to fork their logic

Preferred approach:
- mention them in the relevant skill’s `SKILL.md`
- link them with `skill:` links when appropriate
- describe when to invoke them
- keep only Luria-specific adaptations in your Luria skills

## Suggested mapping for your existing helper skills

Examples:
- brainstorming / hypothesis-generation → differential formulation support
- literature-review / paper-lookup / research-lookup → evidence support for interpretation
- clinical-reports / treatment-plans → shared report and recommendation patterns
- subagent-driven-development / executing-plans / verification-before-completion → meta-workflow support
- scientific-writing / peer-review → polishing and review

## Migration recommendation for current repo

### Current issue
The existing `neuropsych-reports` skill is acting like a monolith:
- too much domain guidance in one `SKILL.md`
- mixed concerns across prompts, templates, references, scripts, and knowledge base
- duplicate classification logic across scripts
- weak separation between reusable references and output assets

### Recommended transition
1. Keep `neuropsych-reports` as the working source during transition.
2. Move architecture/workflow docs into `references/architecture` and `references/workflows`.
3. Gradually spin out the six Luria skills in `~/.desktop-commander/skills/`.
4. Move prompt library into `references/prompts/` with clear categories.
5. Consolidate repeated scoring logic into a shared script or shared reference implementation.

## Subagent model

A practical mental model:

- Orchestrator = project manager
- Intake = chart reviewer
- Score processing = psychometrist/data processor
- Interpretation = neuropsychologist reasoning layer
- Report writing = medical writer
- Quality review = compliance/editorial reviewer

This makes the app easier to reason about and easier to test.
