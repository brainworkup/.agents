#!/usr/bin/env python3
"""
Validate a neuropsychological report for completeness against required sections.

Usage:
    python validate_neuropsych_report.py report.md
    python validate_neuropsych_report.py report.md --type full
    python validate_neuropsych_report.py report.md --type brief
    python validate_neuropsych_report.py report.md --type pediatric
    python validate_neuropsych_report.py report.md --type geriatric
    python validate_neuropsych_report.py report.md --type forensic
"""

import argparse
import re
import sys
from pathlib import Path

# Required sections by report type
REQUIRED_SECTIONS = {
    "full": [
        ("Header / Demographics", [
            r"patient\s*name",
            r"date\s*of\s*birth",
            r"age\s*at\s*evaluation",
            r"date.*of\s*evaluation",
            r"referring\s*provider",
            r"evaluating\s*clinician",
        ]),
        ("Reason for Referral", [r"reason\s*for\s*referral"]),
        ("Sources of Information", [r"sources?\s*of\s*information"]),
        ("Background Information", [
            r"background\s*information|background\s*history",
            r"medical\s*history|developmental.*history",
            r"psychiatric|emotional\s*history",
            r"family\s*history",
            r"educational\s*history",
        ]),
        ("Behavioral Observations", [r"behavioral\s*observations?"]),
        ("Tests Administered", [r"tests?\s*administered"]),
        ("Premorbid Estimate", [r"premorbid"]),
        ("Performance Validity", [r"(performance\s*)?validity"]),
        ("Test Results", [r"test\s*results|results?\s*and\s*interpretation"]),
        ("Summary and Diagnostic Impressions", [
            r"summary|diagnostic\s*impressions?",
            r"(dsm|icd|f\d{2}|[0-9]{3}\.[0-9])",
        ]),
        ("Recommendations", [r"recommendations?"]),
        ("Informed Consent", [r"informed\s*consent"]),
        ("Signature Block", [r"clinician\s*name|signature|license\s*number"]),
    ],
    "brief": [
        ("Header / Demographics", [r"patient\s*name", r"date\s*of\s*birth"]),
        ("Reason for Assessment", [r"reason\s*for\s*(assessment|referral)"]),
        ("Relevant Background", [r"(relevant\s*)?background"]),
        ("Behavioral Observations", [r"behavioral\s*observations?"]),
        ("Measures Administered", [r"measures?\s*administered|tests?\s*administered"]),
        ("Results", [r"results?"]),
        ("Impressions", [r"impressions?"]),
        ("Recommendations", [r"recommendations?"]),
    ],
    "pediatric": [
        ("Header / Demographics", [
            r"patient\s*name",
            r"date\s*of\s*birth",
            r"grade",
            r"school",
        ]),
        ("Reason for Referral", [r"reason\s*for\s*referral"]),
        ("Sources of Information", [r"sources?\s*of\s*information"]),
        ("Developmental History", [r"developmental\s*history"]),
        ("Educational History", [r"educational\s*history"]),
        ("Behavioral Observations", [r"behavioral\s*observations?"]),
        ("Tests Administered", [r"tests?\s*administered"]),
        ("Intellectual Functioning", [r"intellectual\s*functioning"]),
        ("Academic Achievement", [r"academic\s*achievement"]),
        ("Attention and Executive Function", [r"attention|executive\s*function"]),
        ("Emotional/Behavioral Functioning", [r"emotional|behavioral\s*functioning"]),
        ("Adaptive Behavior", [r"adaptive\s*(behavior|functioning)"]),
        ("Summary and Diagnostic Impressions", [r"summary|diagnostic\s*impressions?"]),
        ("Educational Recommendations", [r"educational\s*recommendations?|iep|504"]),
        ("Informed Consent", [r"informed\s*consent"]),
    ],
    "geriatric": [
        ("Header / Demographics", [r"patient\s*name", r"years\s*of\s*education"]),
        ("Reason for Referral", [r"reason\s*for\s*referral"]),
        ("Collateral Interview", [r"collateral\s*interview"]),
        ("Cognitive Decline Timeline", [r"(cognitive|functional)\s*decline\s*timeline"]),
        ("Functional Status / ADLs", [r"(functional\s*status|iadl|adl)"]),
        ("Behavioral Observations", [r"behavioral\s*observations?"]),
        ("Tests Administered", [r"tests?\s*administered"]),
        ("Premorbid Estimate", [r"premorbid"]),
        ("Test Results", [r"test\s*results|results?\s*and\s*interpretation"]),
        ("Capacity Considerations", [r"capacity\s*considerations?"]),
        ("Summary and Diagnostic Impressions", [r"summary|diagnostic\s*impressions?"]),
        ("Recommendations", [r"recommendations?"]),
    ],
    "forensic": [
        ("Header / Demographics", [r"examinee\s*name", r"requesting\s*party", r"case\s*number"]),
        ("Psycholegal Question", [r"psycholegal\s*question|referral\s*information"]),
        ("Notification of Purpose", [r"notification|limits\s*of\s*confidentiality"]),
        ("Sources of Information / Records Reviewed", [r"sources?\s*of\s*information|records?\s*reviewed"]),
        ("Pre-Incident Functioning", [r"pre-incident\s*functioning"]),
        ("Incident Description", [r"incident\s*description"]),
        ("Behavioral Observations", [r"behavioral\s*observations?"]),
        ("Tests Administered", [r"tests?\s*administered"]),
        ("Validity Assessment (before results)", [r"validity\s*assessment|performance\s*validity"]),
        ("Test Results", [r"test\s*results|results?\s*and\s*interpretation"]),
        ("Opinions", [r"opinions?|summary\s*and\s*opinions?"]),
        ("Causation Opinion", [r"causation|etiology"]),
        ("Certification", [r"certif(y|ication)|reasonable\s*degree"]),
    ],
}

# Content quality checks (applied to all report types)
QUALITY_CHECKS = [
    ("Score normative explanation", r"(mean\s*of\s*100|standard\s*deviation|percentile\s*rank)", "Include a paragraph explaining the normative framework (SS mean=100 SD=15, etc.)"),
    ("No test items/stimuli", r"(what\s*does?\s*.*\s*mean|tell\s*me\s*what\s*you\s*see|repeat\s*after\s*me)", "WARNING: Possible test items or stimuli detected — verify test security"),
    ("Functional implications", r"(daily\s*living|functional|real-world|everyday\s*activit)", "Include functional/real-world implications of test findings"),
    ("Person-first language", r"(the\s*patient\s*is\s*ADHD|is\s*autistic|is\s*retarded|is\s*demented)", "WARNING: Possible non-person-first language detected"),
]


def validate_report(text: str, report_type: str = "full") -> dict:
    sections = REQUIRED_SECTIONS.get(report_type, REQUIRED_SECTIONS["full"])
    text_lower = text.lower()

    results = {"type": report_type, "sections": [], "quality": [], "score": 0, "total": 0}

    # Check required sections
    for section_name, patterns in sections:
        found = any(re.search(p, text_lower) for p in patterns)
        results["sections"].append({"name": section_name, "found": found})
        results["total"] += 1
        if found:
            results["score"] += 1

    # Quality checks
    for check_name, pattern, message in QUALITY_CHECKS:
        match = re.search(pattern, text_lower)
        is_warning = check_name.startswith("No ") or "WARNING" in message
        results["quality"].append({
            "name": check_name,
            "found": bool(match),
            "message": message,
            "is_warning": is_warning,
        })

    return results


def print_results(results: dict):
    print(f"\n{'=' * 60}")
    print(f"NEUROPSYCHOLOGICAL REPORT VALIDATION ({results['type'].upper()})")
    print(f"{'=' * 60}\n")

    # Section completeness
    print("REQUIRED SECTIONS:")
    print("-" * 40)
    for section in results["sections"]:
        status = "✅" if section["found"] else "❌"
        print(f"  {status} {section['name']}")

    pct = (results["score"] / results["total"] * 100) if results["total"] > 0 else 0
    print(f"\nCompleteness: {results['score']}/{results['total']} ({pct:.0f}%)")

    # Quality checks
    print(f"\nQUALITY CHECKS:")
    print("-" * 40)
    for check in results["quality"]:
        if check["is_warning"]:
            status = "⚠️ " if check["found"] else "✅"
        else:
            status = "✅" if check["found"] else "⚠️ "
        print(f"  {status} {check['name']}")
        if (check["is_warning"] and check["found"]) or (not check["is_warning"] and not check["found"]):
            print(f"     → {check['message']}")

    # Overall assessment
    print(f"\n{'=' * 60}")
    if pct == 100:
        print("✅ All required sections present.")
    elif pct >= 80:
        print(f"⚠️  Report is mostly complete but missing {results['total'] - results['score']} section(s).")
    else:
        print(f"❌ Report is incomplete — missing {results['total'] - results['score']} required section(s).")
    print(f"{'=' * 60}\n")


def main():
    parser = argparse.ArgumentParser(description="Validate neuropsychological report completeness")
    parser.add_argument("file", help="Path to report file (Markdown or plain text)")
    parser.add_argument(
        "--type",
        choices=["full", "brief", "pediatric", "geriatric", "forensic"],
        default="full",
        help="Report type to validate against (default: full)",
    )
    args = parser.parse_args()

    filepath = Path(args.file)
    if not filepath.exists():
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    text = filepath.read_text(encoding="utf-8")
    results = validate_report(text, args.type)
    print_results(results)

    # Exit with non-zero if incomplete
    pct = (results["score"] / results["total"] * 100) if results["total"] > 0 else 0
    sys.exit(0 if pct == 100 else 1)


if __name__ == "__main__":
    main()
