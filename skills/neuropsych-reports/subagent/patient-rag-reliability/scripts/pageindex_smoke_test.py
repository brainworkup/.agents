#!/usr/bin/env python3
"""End-to-end smoke test for PageIndex patient workflow APIs."""

from __future__ import annotations

import argparse
import json
import mimetypes
import sys
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path


class SmokeTestError(RuntimeError):
    """Raised when a smoke-test step fails."""


def _build_url(base_url: str, path: str) -> str:
    return f"{base_url.rstrip('/')}{path}"


def _http_request(
    method: str,
    url: str,
    body: bytes | None = None,
    headers: dict[str, str] | None = None,
    timeout: int = 30,
) -> tuple[int, str]:
    req = urllib.request.Request(url, method=method, data=body)
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status = resp.getcode()
            text = resp.read().decode("utf-8", errors="replace")
            return status, text
    except urllib.error.HTTPError as exc:
        text = exc.read().decode("utf-8", errors="replace")
        return exc.code, text
    except urllib.error.URLError as exc:
        raise SmokeTestError(f"Network error calling {url}: {exc}") from exc


def _request_json(
    method: str,
    base_url: str,
    path: str,
    payload: dict | None = None,
    timeout: int = 30,
) -> tuple[int, dict | list | str]:
    body = None
    headers: dict[str, str] = {}
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    status, text = _http_request(
        method=method,
        url=_build_url(base_url, path),
        body=body,
        headers=headers,
        timeout=timeout,
    )
    if not text:
        return status, ""
    try:
        return status, json.loads(text)
    except json.JSONDecodeError:
        return status, text


def _multipart_file_body(field_name: str, file_path: Path) -> tuple[bytes, str]:
    boundary = f"----codex-{uuid.uuid4().hex}"
    filename = file_path.name
    content_type = mimetypes.guess_type(str(file_path))[0] or "application/octet-stream"
    file_bytes = file_path.read_bytes()

    lines: list[bytes] = [
        f"--{boundary}\r\n".encode(),
        (
            f'Content-Disposition: form-data; name="{field_name}"; '
            f'filename="{filename}"\r\n'
        ).encode(),
        f"Content-Type: {content_type}\r\n\r\n".encode(),
        file_bytes,
        b"\r\n",
        f"--{boundary}--\r\n".encode(),
    ]
    body = b"".join(lines)
    return body, f"multipart/form-data; boundary={boundary}"


def _log(msg: str) -> None:
    print(f"[smoke] {msg}")


def run(args: argparse.Namespace) -> int:
    base_url = args.base_url.rstrip("/")
    patient_id: str | None = None

    _log(f"Checking health at {base_url}/api/health")
    status, payload = _request_json("GET", base_url, "/api/health")
    if status != 200 or not isinstance(payload, dict) or payload.get("status") != "ok":
        raise SmokeTestError(f"Health check failed: status={status}, payload={payload}")
    _log("Health check passed")

    if args.health_only:
        _log("Health-only mode complete")
        return 0

    sample_file = Path(args.sample_file).expanduser().resolve() if args.sample_file else None
    if sample_file is None:
        raise SmokeTestError("Provide --sample-file or use --health-only")
    if not sample_file.exists():
        raise SmokeTestError(f"Sample file not found: {sample_file}")
    if not sample_file.is_file():
        raise SmokeTestError(f"Sample file is not a file: {sample_file}")

    display_name = f"SmokeTest-{time.strftime('%Y%m%d-%H%M%S')}"
    _log(f"Creating patient: {display_name}")
    status, payload = _request_json(
        "POST",
        base_url,
        "/api/patients",
        payload={"display_name": display_name},
    )
    if status != 200 or not isinstance(payload, dict) or "patient_id" not in payload:
        raise SmokeTestError(f"Create patient failed: status={status}, payload={payload}")
    patient_id = str(payload["patient_id"])
    _log(f"Patient created: {patient_id}")

    try:
        _log(f"Uploading sample document: {sample_file}")
        body, content_type = _multipart_file_body("file", sample_file)
        status, text = _http_request(
            "POST",
            _build_url(base_url, f"/api/patients/{patient_id}/documents"),
            body=body,
            headers={"Content-Type": content_type},
            timeout=120,
        )
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            payload = text
        if status != 200 or not isinstance(payload, dict) or "doc_id" not in payload:
            raise SmokeTestError(f"Upload failed: status={status}, payload={payload}")
        doc_id = str(payload["doc_id"])
        _log(f"Upload accepted, doc_id={doc_id}")

        _log("Polling tree readiness")
        deadline = time.time() + args.tree_timeout
        tree_ready = False
        while time.time() < deadline:
            status, _ = _request_json(
                "GET",
                base_url,
                f"/api/patients/{patient_id}/documents/{doc_id}/tree",
            )
            if status == 200:
                tree_ready = True
                break
            if status not in (404,):
                raise SmokeTestError(f"Unexpected tree poll status={status}")
            time.sleep(args.poll_interval)

        if not tree_ready:
            raise SmokeTestError("Tree readiness timeout")
        _log("Tree ready")

        if not args.skip_chat:
            _log("Running chat step")
            status, payload = _request_json(
                "POST",
                base_url,
                "/api/chat",
                payload={
                    "patient_id": patient_id,
                    "message": "Provide a one-sentence summary of this document.",
                },
                timeout=120,
            )
            if status != 200 or not isinstance(payload, dict):
                raise SmokeTestError(f"Chat failed: status={status}, payload={payload}")
            answer = str(payload.get("answer", "")).strip()
            if not answer:
                raise SmokeTestError("Chat returned an empty answer")
            _log("Chat step passed")
        else:
            _log("Skipping chat step")

        if not args.skip_export:
            _log(f"Running export step (fmt={args.export_format})")
            status, payload = _request_json(
                "POST",
                base_url,
                "/api/export",
                payload={
                    "patient_id": patient_id,
                    "fmt": args.export_format,
                    "include_chat": True,
                    "include_trees": True,
                },
                timeout=args.export_timeout,
            )
            if status != 200 or not isinstance(payload, dict):
                raise SmokeTestError(f"Export failed: status={status}, payload={payload}")
            if not str(payload.get("path", "")).strip():
                raise SmokeTestError(f"Export missing path: payload={payload}")
            _log("Export step passed")
        else:
            _log("Skipping export step")

    finally:
        if patient_id and not args.keep_patient:
            _log(f"Cleaning up patient {patient_id}")
            status, payload = _request_json(
                "DELETE",
                base_url,
                f"/api/patients/{patient_id}",
            )
            if status != 200:
                _log(f"Cleanup warning: status={status}, payload={payload}")
            else:
                _log("Cleanup complete")
        elif patient_id:
            _log(f"Keeping patient {patient_id}")

    _log("Smoke test passed")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run API smoke tests for the patient workflow: health, upload, tree, "
            "chat, export, cleanup."
        )
    )
    parser.add_argument("--base-url", default="http://localhost:8080")
    parser.add_argument("--sample-file", help="Path to a sample PDF/CSV/MD file")
    parser.add_argument(
        "--health-only",
        action="store_true",
        help="Run only /api/health and exit",
    )
    parser.add_argument(
        "--tree-timeout",
        type=int,
        default=300,
        help="Seconds to wait for retrieval tree readiness",
    )
    parser.add_argument(
        "--poll-interval",
        type=int,
        default=5,
        help="Seconds between tree readiness polls",
    )
    parser.add_argument(
        "--skip-chat",
        action="store_true",
        help="Skip chat step",
    )
    parser.add_argument(
        "--skip-export",
        action="store_true",
        help="Skip export step",
    )
    parser.add_argument(
        "--export-format",
        default="qmd",
        choices=["qmd", "pdf", "docx", "html"],
        help="Export format for /api/export step",
    )
    parser.add_argument(
        "--export-timeout",
        type=int,
        default=180,
        help="Seconds to wait for export request",
    )
    parser.add_argument(
        "--keep-patient",
        action="store_true",
        help="Do not delete created patient at the end",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        return run(args)
    except SmokeTestError as exc:
        print(f"[smoke] ERROR: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
