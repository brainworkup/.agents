---
name: clinical-neuropsych-reports
description: Draft clinical and forensic neuropsychological evaluation reports—referral-driven structure, test documentation (edition, norms, language), domain-integrated interpretation, performance/ symptom validity, limitations, and recommendations. Cross-links HIPAA/de-identification and general clinical documentation to clinical-reports.
allowed-tools: Read Write Edit Bash
license: MIT License
metadata:
  skill-author: Adapted from clinical-reports (K-Dense Inc.) for neuropsychology practice
---

# Clinical Neuropsychological Evaluation Reports

## Overview

This skill guides generation of **clinical neuropsychological evaluation reports** and optional **forensic addenda**. Reports must be accurate, evidence-linked, and appropriate to the referral question; conclusions should integrate history, observations, validity indicators, and test data across cognitive domains rather than relying on isolated scores.

**Critical principles**

- **Privacy**: Treat all patient or evaluee information as protected health or sensitive personal information. Follow HIPAA Safe Harbor de-identification and consent norms described in the sibling skill **clinical-reports** (see [Cross-links to clinical-reports](#cross-links-to-clinical-reports)).
- **Scope**: Write within the evaluator’s role. Do not provide legal advice in forensic sections; document methodology, data, and psycholegal opinions only as a qualified professional would.
- **Scientific integrity**: Acknowledge limits of tests, norms, and causal inference; address validity and alternative explanations (medical, psychiatric, cultural, linguistic, sensory, effort).

## When to Use This Skill

Use this skill when the user is writing or revising:

- Clinical neuropsychological or neurocognitive evaluation reports
- “NP reports,” psychometric summaries integrated into narrative, or consultation letters after neuropsych testing
- Disability, rehabilitation, dementia, stroke, TBI, epilepsy, oncology, MS, ADHD, learning disorders, or psychiatric presentations with cognitive assessment
- Pediatric neuropsychological evaluations (use pediatric callouts below)
- Forensic or court-related neuropsychological work **with** the optional addendum template (IME, competency, personal injury, etc.)—always alongside clinical sections as appropriate

For generic SOAP notes, H&P, radiology/pathology/lab reports, trial CSRs, or journal case reports, use **clinical-reports** unless the task is specifically a neuropsychological evaluation narrative.

## Cross-links to clinical-reports

Reuse these resources from `~/.Codex/skills/clinical-reports/`:

| Need | Location |
|------|----------|
| HIPAA Safe Harbor and privacy | `references/regulatory_compliance.md`, `assets/hipaa_compliance_checklist.md` |
| Scan drafts for HIPAA identifiers | `scripts/check_deidentification.py` |
| General patient documentation patterns | `references/patient_documentation.md`, SOAP/H&P templates under `assets/` |
| Tables/figures conventions | `references/data_presentation.md` |
| CARE case reports (rare neuropsych case write-ups) | `references/case_report_guidelines.md`, `assets/case_report_template.md` |

## Visual Enhancement with Scientific Schematics

**MANDATORY: Every completed neuropsychological evaluation report delivered as a polished document SHOULD include at least one clear visual** (figure, table graphic, or AI-generated schematic) that aids the reader—typically a **domain profile**, **timeline**, or **brain–behavior integration** diagram.

Align with the **scientific-schematics** skill and, where available, the clinical-reports workflow:

```bash
# If your environment includes the clinical-reports schematic helper:
python ~/.Codex/skills/clinical-reports/scripts/generate_schematic.py "your diagram description" -o figures/neuropsych-profile.png
```

**Neuropsych-appropriate schematic ideas**

- Standardized score profile by cognitive domain (e.g., bar or line plot schematic: attention/executive, memory, language, visuospatial, processing speed)
- Timeline: injury, disease milestones, treatments, and dates of evaluation
- Simple brain–behavior diagram when imaging or lesion data is central to the case
- Flowchart: referral question → hypotheses → data sources → conclusions (useful for complex forensic cases)

Use colorblind-friendly palettes and label axes or domains explicitly.

---

## Report Philosophy

1. **Referral centric**: Every major conclusion should trace to the referral question(s) and documented data.
2. **Multi-method**: Integrate history, records, observation, and test results; note discrepancies and how you weighed them.
3. **Domain structure**: Present findings under coherent domains; avoid a bare list of subtests without integration.
4. **Validity first**: When data warrant, discuss performance validity and symptom validity/exaggeration in a professional, non-pejorative way, with implications for interpretation.
5. **Transparent limitations**: Norm sample match (age, education, language, culture), sensory capacity, fatigue, medications, and session splits belong in **Limitations**.
6. **Actionable recommendations**: Tie accommodations, therapies, referrals, and follow-up to specific findings and settings (home, school, work).

## Clinical Neuropsychological Report Outline

Section order may follow local institutional standards; this outline is a comprehensive default.

1. **Identifying information / dates of service** — De-identify in teaching drafts; use institution-approved headers for real records.
2. **Referral question and context** — Who referred, why now, specific questions (diagnosis, capacity, treatment planning, school/work).
3. **Relevant background** — Medical/neurological, psychiatric, developmental, educational, occupational, substance use, social, prior testing.
4. **Records reviewed** — List salient records; note gaps.
5. **Behavioral observations** — Appearance, engagement, language, motor/sensory needs, fatigue, emotional state, behaviors affecting validity; testing conditions.
6. **Assessment procedures** — Tests and procedures administered; editions; languages; computerized vs paper; norms reference (e.g., age-appropriate); brief rationale if selective battery.
7. **Validity / response bias** — Embedded and standalone measures as used; interpret conservatively with population base rates where applicable; state impact on confidence in domains.
8. **Intellectual functioning** — Only if assessed; reconcile with premorbid estimates when relevant.
9. **Attention and executive functioning**
10. **Learning and memory** — Encoding, retrieval, recognition; verbal vs visual as applicable.
11. **Language** — Comprehension, fluency, naming, academic skills tied to language if assessed.
12. **Visuospatial / visuoconstructional functioning**
13. **Motor and sensory** — If relevant to presentation or testing.
14. **Emotional status and personality** — When objective measures or clinical interview support this section; separate mood from cognition when possible.
15. **Integration and diagnostic impressions** — Synthesize with differential; ICD-10/DSM-5 as used locally; functional impact.
16. **Recommendations** — Medical, rehabilitative, educational, vocational, caregiving, safety, and follow-up testing.
17. **Limitations of evaluation** — Norms, language, culture, sensory, cooperation, incomplete records, comorbidities.

For a fill-in scaffold, use `assets/neuropsych_evaluation_template.md`.

## Forensic Neuropsychological Addendum (Optional)

Use when the evaluation is retained for legal, administrative, or court-related purposes. Append or integrate per jurisdiction and supervisor guidance. Template: `assets/forensic_neuropsych_addendum_template.md`.

Typical elements:

- **Purpose and scope** — Retention, role (e.g., third-party evaluation), who was examined, what was not done.
- **Materials reviewed** — Records, depositions index, prior reports.
- **Psycholegal questions addressed** — Tie opinions to questions actually asked; avoid answering questions outside expertise.
- **Methodology** — Standardized procedures, collateral limitations.
- **Factual bases vs opinions** — Clear distinction; cautious causal language.
- **Alternative hypotheses** — Neurological, psychiatric, malingering, cultural/linguistic, expectable stress.
- **Limits of opinion** — What data cannot support.

This skill does **not** supply legal strategy or legal conclusions; wording should be reviewed by the retaining professional and counsel when applicable.

## Interpretation Guidance

- **Avoid over-interpretation**: Single subtest lows or isolated “red” scores do not diagnose impairment; describe patterns, consistency across methods, and functional correlates.
- **Base rates**: When helpful, note that uncommon score combinations or large discrepancies occur at a known frequency in healthy samples; avoid deterministic language.
- **Premorbid estimation**: Use appropriate methods (education, reading-based estimates, prior achievement) when inferring change.
- **Cultural and linguistic factors**: Discuss bilingualism, acculturation, test language, and availability of appropriate norms; qualify conclusions when norms are a poor fit.
- **Pediatric callouts**: Emphasize developmental level, caregiver and teacher report, school services (IEP/504), and tests normed for age; separate maturational lag from disorder when data allow.

## Quality Assurance

Before sign-out, use `assets/quality_checklist_neuropsych.md`. Run `check_deidentification.py` on drafts that will leave a clinical environment.

## Resources in This Skill

- `assets/neuropsych_evaluation_template.md` — Full clinical report scaffold
- `assets/forensic_neuropsych_addendum_template.md` — Forensic sections scaffold
- `assets/quality_checklist_neuropsych.md` — Pre-final QA
- `references/neuropsych_reporting_standards.md` — Expectations summary and public references
- `references/README.md` — Index

## Common Pitfalls

- **Score dump**: Listing scores without narrative integration or referral linkage
- **Missing validity**: Ignoring PVT/SVT or cooperation when the battery includes them or when data are inconsistent
- **Causal overreach**: Stating lesion- or event-specific causation without converging evidence
- **Norm mismatch**: Applying English-language norms without comment to multilingual evaluees
- **Recommendations vague**: “Follow up with neurology” without indicating why and what question to resolve
- **Forensic boundary errors**: Answering legal questions (e.g., ultimate legal issue) outside professional or jurisdictional standards—flag for attorney and supervisor review

---

**Final note**: Neuropsychological reports influence medical care, education, benefits, and legal proceedings. Prioritize accuracy, clarity, appropriate humility, and respect for the evaluee. When in doubt, narrow the conclusion and broaden the limitations.
