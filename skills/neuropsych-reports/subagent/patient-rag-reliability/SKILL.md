---
name: patient-rag-reliability
description: Harden reliability for patient-scoped RAG applications that ingest documents, build retrieval trees, answer chat queries, and export reports. Use when changing upload/tree/chat/export workflows, fixing flaky production behavior, diagnosing 4xx/5xx errors, adding retries/timeouts, enforcing data-isolation invariants, or validating end-to-end behavior with smoke tests.
---

# Patient RAG Reliability

## Overview

Apply a repeatable reliability workflow for patient-scoped RAG systems.
Enforce isolation and failure-handling invariants, then verify behavior with an end-to-end smoke test.

## Reliability Workflow

1. Identify the touched path: upload, tree retrieval, chat, export, or cross-cutting state.
2. Apply invariants from `references/robustness-checklist.md` before code edits.
3. Add explicit handling for retryable failures vs terminal failures.
4. Preserve actionable error messages at API boundaries.
5. Run the smoke test script and fail fast on regressions.
6. Keep or add targeted tests for the modified boundary logic.

## Core Invariants

- Keep uploaded files patient-isolated; avoid global filename collisions.
- Accept chat only when at least one document is retrieval-ready.
- Treat retries as bounded and observable; do not loop silently.
- Return typed, user-actionable failures from API handlers.
- Keep report generation deterministic (`fmt`, timeout, output existence).
- Preserve cleanup behavior for partial failures.

## Smoke Test

Run the smoke test after touching upload/tree/chat/export:

```bash
python scripts/pageindex_smoke_test.py \
  --base-url http://localhost:8080 \
  --sample-file /abs/path/to/test.pdf
```

Use `--health-only` for a fast API check when external dependencies are unavailable.
Use `--skip-chat` or `--skip-export` to isolate failure domains.

## Resources

- `scripts/pageindex_smoke_test.py`: End-to-end API smoke test for patient workflow.
- `references/robustness-checklist.md`: Guardrails for invariants, failure handling, and release checks.
