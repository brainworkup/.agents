# Patient RAG Robustness Checklist

## 1. Isolation And State

- Store uploaded files in patient-scoped paths, not only by original filename.
- Use immutable identifiers for document linkage (`patient_id`, `doc_id`, file hash).
- Clear or invalidate stale derived state after destructive operations (for example chat history after document delete).
- Enforce foreign keys and transaction boundaries for multi-step DB changes.

## 2. Failure Taxonomy

- Classify failures as `retryable`, `terminal`, or `misconfiguration`.
- Retry only retryable failures with bounded attempts and backoff.
- Return stable API errors with operation context and next action.
- Avoid bare `except Exception` unless converting to a typed error with logging.

## 3. Workflow Guardrails

- Upload: validate extension, file size, and destination path safety.
- Tree: poll with explicit timeout, clear terminal status, and structured reason on timeout.
- Chat: reject when no retrieval-ready docs; preserve source context metadata.
- Export: validate format, guard Quarto timeout, verify output exists before success.

## 4. Observability

- Add correlation IDs across request -> service -> external API boundaries.
- Log phase transitions: upload start/end, tree poll start/end, chat request/response, export render start/end.
- Include patient/document identifiers in logs, but avoid PHI in plaintext.

## 5. Release Gate

- Run smoke test across `health -> upload -> tree -> chat -> export -> cleanup`.
- Run lint and tests for touched modules.
- Document known degraded modes (`skip-chat`, `health-only`) and user-facing messages.
