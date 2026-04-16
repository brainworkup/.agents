---
name: neuropsych-reports
description: "Generate clinical neuropsychological evaluation reports from intake data, NSE transcripts, and test score profiles. Covers full-length evaluations, brief/screening batteries, forensic neuropsych, pediatric evals, re-evaluations, and IME/disability reports. Use when writing neuropsychological reports, interpreting test scores, summarizing NSE interviews, or documenting cognitive evaluations."
allowed-tools: Read Write Edit Bash
license: MIT License
metadata:
  skill-author: Adapted from clinical-reports (K-Dense Inc.) for neuropsychology practice
---

# Clinical Neuropsychological Evaluation Reports

## Overview

Write comprehensive, publication-quality clinical neuropsychological evaluation reports that integrate clinical interview data, behavioral observations, standardized test results, and diagnostic impressions into a cohesive narrative. This skill adapts clinical report-writing principles for the specialized domain of neuropsychological assessment.

**Critical Principle:** Neuropsychological reports must be accurate, evidence-based, culturally sensitive, and compliant with APA ethical standards, HIPAA, and applicable state regulations. Reports should translate complex test data into practical, real-world recommendations.

### Critical Principles

- **Privacy**: Treat all patient or evaluee information as protected health or sensitive personal information. Follow HIPAA Safe Harbor de-identification and consent norms described in the sibling skill **clinical-reports** (see [Cross-links to clinical-reports](#cross-links-to-clinical-reports)).
- **Scope**: Write within the evaluator's role. Do not provide legal advice in forensic sections; document methodology, data, and psycholegal opinions only as a qualified professional would.
- **Scientific integrity**: Acknowledge limits of tests, norms, and causal inference; address validity and alternative explanations (medical, psychiatric, cultural, linguistic, sensory, effort).

## When to Use This Skill

- Writing full neuropsychological evaluation reports
- Summarizing Neurobehavioral Status Exam (NSE) transcripts
- Interpreting and presenting neuropsychological test score profiles
- Writing brief/screening cognitive assessment reports
- Documenting pediatric neuropsychological evaluations
- Writing geriatric/dementia evaluations
- Preparing forensic neuropsychological reports
- Creating Independent Medical Examination (IME) reports
- Writing re-evaluation/follow-up neuropsychological reports
- Documenting disability/accommodations evaluations
- Translating test scores into functional, daily-living implications

For generic SOAP notes, H&P, radiology/pathology/lab reports, trial CSRs, or journal case reports, use **clinical-reports** unless the task is specifically a neuropsychological evaluation narrative.

## Report Types

### 1. Full Neuropsychological Evaluation (Standard)
The most comprehensive report type. Typically 8–20 pages. Used for differential diagnosis, treatment planning, academic/vocational accommodations, and disability determination.

### 2. Brief/Screening Cognitive Assessment
Shorter report (3–6 pages) for focused referral questions, competency screenings, or bedside cognitive evaluations (e.g., MoCA, MMSE-based).

### 3. Pediatric Neuropsychological Evaluation
Adapted for children/adolescents. Emphasizes developmental history, school functioning, behavioral rating scales, and educational recommendations (IEP/504 plans).

### 4. Geriatric/Dementia Evaluation
Focused on progressive cognitive decline, capacity assessments, caregiver input, and staging of neurodegenerative disease.

### 5. Forensic Neuropsychological Report
For legal proceedings. Requires heightened attention to validity testing, malingering assessment, and Daubert/Frye admissibility standards.

### 6. Re-evaluation/Follow-up Report
Documents change from baseline. Emphasizes reliable change index (RCI) methodology, practice effects, and comparative analysis.

### 7. IME/Disability Evaluation
For insurance, workers' compensation, or Social Security Disability. Requires explicit functional capacity statements.

---

## Cross-links to clinical-reports

Reuse these resources from `~/.Codex/skills/clinical-reports/`:

| Need | Location |
|------|----------|
| HIPAA Safe Harbor and privacy | `references/regulatory_compliance.md`, `assets/hipaa_compliance_checklist.md` |
| Scan drafts for HIPAA identifiers | `scripts/check_deidentification.py` |
| General patient documentation patterns | `references/patient_documentation.md`, SOAP/H&P templates under `assets/` |
| Tables/figures conventions | `references/data_presentation.md` |
| CARE case reports (rare neuropsych case write-ups) | `references/case_report_guidelines.md`, `assets/case_report_template.md` |

---

## Visual Enhancement with Scientific Schematics

**MANDATORY: Every completed neuropsychological evaluation report delivered as a polished document SHOULD include at least one clear visual** (figure, table graphic, or AI-generated schematic) that aids the reader—typically a **domain profile**, **timeline**, or **brain–behavior integration** diagram.

Align with the **scientific-schematics** skill and, where available, the clinical-reports workflow:

```bash
# If your environment includes the clinical-reports schematic helper:
python ~/.Codex/skills/clinical-reports/scripts/generate_schematic.py "your diagram description" -o figures/neuropsych-profile.png
```

### Neuropsych-Appropriate Schematic Ideas

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

---

## Full Neuropsychological Evaluation Report Structure

### Report Header

```text
CONFIDENTIAL NEUROPSYCHOLOGICAL EVALUATION

Patient Name:          [Last, First]
Date of Birth:         [MM/DD/YYYY]
Age at Evaluation:     [X years, Y months]
Date(s) of Evaluation: [MM/DD/YYYY]
Date of Report:        [MM/DD/YYYY]
Referring Provider:    [Name, credentials]
Evaluating Clinician:  [Name, credentials]
```

### Section 1: Reason for Referral

**Purpose:** State why the evaluation was requested, by whom, and what questions the evaluation aims to answer.

**Alternative section order:** Section order may follow local institutional standards; this outline is a comprehensive default. Some clinicians prefer to place Records Reviewed after Background Information.

**Content:**
- Referral source and their specific questions
- Patient's/family's primary concerns
- Purpose of the evaluation (differential diagnosis, treatment planning, accommodations, forensic, disability, etc.)
- Brief description of presenting problems

**Style:**
- 1–2 paragraphs
- Third person, past tense
- Professional, neutral tone

**Example:**
```
[Patient] is a [age]-year-old [handedness], [language-dominant], [sex] who was
referred for neuropsychological evaluation by [referring provider, credentials] to
assess current cognitive functioning in the context of [presenting concern, e.g.,
reported memory difficulties, history of traumatic brain injury, academic
underperformance]. The evaluation was requested to [clarify diagnosis / establish
baseline / guide treatment planning / determine accommodations eligibility /
assess decision-making capacity].
```

### Section 2: Background Information

This section integrates all relevant history. Draw from the clinical interview (NSE transcript), collateral sources, medical records, and prior evaluations.

#### 2a. Developmental and Medical History

- Birth and perinatal history (especially for pediatric evals)
- Developmental milestones (motor, language, social)
- Significant medical conditions (neurological, psychiatric, systemic)
- Head injuries / concussions (with LOC duration, GCS if available)
- Surgeries, hospitalizations
- Seizure history
- Sleep disorders
- Pain conditions
- Current medications (with dosages)
- Substance use history (type, duration, frequency, sobriety)
- Relevant genetic/metabolic conditions

#### 2b. Psychiatric and Emotional History

- Current and past psychiatric diagnoses
- History of mental health treatment (therapy, medications, hospitalizations)
- Current mood and anxiety symptoms
- History of trauma or adverse childhood experiences
- Suicidal ideation or self-harm (past and current)
- Current psychological stressors

#### 2c. Family History

- Psychiatric diagnoses in biological relatives
- Neurological conditions (dementia, epilepsy, movement disorders)
- Learning disabilities and developmental disorders in family
- Substance use disorders in family
- Relevant medical conditions

#### 2d. Educational History

- Highest level of education attained
- Special education services / IEP / 504 plans
- Grade retention or acceleration
- Learning difficulties (reading, math, writing)
- Standardized test performance (SAT, GRE, etc.)
- Educational accommodations received
- For pediatric: current grade, school type, teacher concerns

#### 2e. Occupational / Vocational History

- Current and past employment
- Job performance and difficulties
- Military service
- Vocational training
- Impact of cognitive concerns on work functioning

#### 2f. Social and Functional History

- Living situation and support system
- Marital/relationship status
- Independence in activities of daily living (ADLs and IADLs)
- Driving status
- Leisure activities
- Social functioning and interpersonal relationships

**Writing Guidelines for Background:**
- Use Chain of Density (CoD) approach: start broad, progressively add detail
- Integrate information from multiple sources; note discrepancies
- Maintain chronological flow within each subsection
- Quote the patient when clinically illustrative
- Note the source of information (patient report, collateral, records)
- Do not make diagnostic inferences in this section

### Section 3: Behavioral Observations

Document the patient's presentation and behavior during testing. This section provides validity context and supports diagnostic formulation.

**Include:**
- General appearance (grooming, dress, apparent vs. stated age)
- Orientation (person, place, time, situation)
- Motor observations (gait, tremor, lateralized findings, fine motor)
- Speech and language (rate, rhythm, fluency, articulation, word-finding)
- Mood and affect (stated mood, observed affect, range, congruence)
- Effort and engagement (motivation, cooperation, frustration tolerance)
- Attention and arousal (sustained attention, distractibility, fatigue)
- Test-taking behavior (approach to tasks, response to difficulty, self-monitoring)
- Rapport and interpersonal style
- Sensory accommodations (glasses, hearing aids)
- Validity of results statement (is the profile considered valid and representative?)

**Example:**
```
[Patient] presented as a well-groomed [sex] who appeared [his/her/their] stated
age. [He/She/They] was alert, fully oriented, and cooperative throughout the
evaluation. Speech was fluent with normal rate and prosody. Mood was described
as "[patient's words]" and affect was [congruent/incongruent], [full-range/
restricted/blunted/flat]. [He/She/They] demonstrated adequate effort and
engagement, and performance validity measures fell within acceptable limits.
The current results are considered a valid and reliable estimate of [his/her/their]
current neurocognitive functioning.
```

### Section 4: Tests Administered

List all measures administered. Group by domain or list alphabetically. Include version numbers. Document editions, languages, computerized vs paper administration, and norms reference (e.g., age-appropriate). Brief rationale if selective battery.

**Standard Domains and Common Measures:**

| Domain | Common Measures |
|--------|----------------|
| **Intellectual Functioning** | WAIS-IV/V, WISC-V/VI, WASI-II, WRIT, KBIT-2 |
| **Achievement** | WIAT-4, WJ-IV ACH, WRAT-5, GORT-5, TOWRE-2 |
| **Attention/Executive** | CPT-3, DKEFS, TMT A&B, Stroop, WCST, BRIEF-2 |
| **Learning & Memory** | CVLT-3, RAVLT, WMS-IV, BVMT-R, RCFT, TOMAL-2 |
| **Language** | BNT, FAS/Animals, Token Test, PPVT-5, CELF-5 |
| **Visuospatial** | RCFT Copy, JLO, Block Design, Hooper VOT |
| **Motor** | Grooved Pegboard, Finger Tapping, Grip Strength |
| **Emotional/Behavioral** | BDI-II, BAI, MMPI-3, PAI, BASC-3, Conners-4 |
| **Adaptive Functioning** | Vineland-3, ABAS-3 |
| **Validity/Effort** | TOMM, WMT, RDS, MSVT, FBS, b Test |
| **Dementia Screening** | MoCA, MMSE, DRS-2, SLUMS |
| **Autism Screening** | ADOS-2, ADI-R, SRS-2, SCQ |

### Section 5: Test Results and Interpretation

This is the core clinical section. Present results domain-by-domain with interpretation anchored to normative classifications.

#### Score Classification System

Use a consistent normative framework throughout. Common systems:

| Standard Score Range | Percentile Range | Classification |
|---------------------|-----------------|----------------|
| ≥ 130 | ≥ 98th | Very Superior |
| 120–129 | 91st–97th | Superior |
| 110–119 | 75th–90th | High Average |
| 90–109 | 25th–74th | Average |
| 80–89 | 9th–24th | Low Average |
| 70–79 | 2nd–8th | Borderline |
| ≤ 69 | ≤ 1st | Extremely Low / Impaired |

**Alternatively (T-score system):**

| T-Score Range | Classification |
|--------------|----------------|
| ≥ 70 | Very Superior |
| 60–69 | Above Average |
| 40–59 | Average |
| 30–39 | Below Average |
| 20–29 | Impaired |
| < 20 | Severely Impaired |

#### Domain-by-Domain Interpretation Guide

For each cognitive domain, provide:
1. **Test(s) administered** and scores (SS, %ile, T-score, z-score as appropriate)
2. **Normative classification** (e.g., "Average range")
3. **Clinical interpretation** — what the score means functionally
4. **Pattern analysis** — how it relates to other domains and the referral question
5. **Contextual factors** — premorbid estimate, effort, cultural/linguistic considerations

**Domain Template:**
```
#### [Domain Name] (e.g., Attention and Executive Function)

[Patient]'s performance on measures of [domain] was [overall classification].
[He/She/They] [performed at / demonstrated / obtained scores in] the [classification]
range on [specific test] ([score type] = [value], [percentile]th percentile),
suggesting [functional interpretation]. [Relative strength/weakness statement if
applicable]. [Integration with clinical presentation and daily functioning].
```

**Score Table Format:**
```
| Measure | Subtest/Index | Raw | Standard Score | Percentile | Classification |
|---------|--------------|-----|---------------|------------|----------------|
| WAIS-V  | FSIQ         | --  | 98            | 45th       | Average        |
| WAIS-V  | VCI          | --  | 105           | 63rd       | Average        |
| WAIS-V  | PRI          | --  | 92            | 30th       | Average        |
```

#### Key Interpretive Principles

1. **Premorbid Estimation:** Anchor interpretation to estimated premorbid ability (TOPF, demographics, education, occupation). A "Low Average" score in someone with estimated Superior premorbid ability may represent significant decline.

2. **Pattern Analysis:** Look for convergent evidence across multiple measures within a domain before concluding impairment. Single low scores may reflect normal variability.

3. **Base Rates:** Consider the base rate of low scores in healthy populations. In a comprehensive battery, 1–2 low scores can be statistically expected.

4. **Ecological Validity:** Connect test performance to real-world functioning. "These memory scores suggest [Patient] may have difficulty [functional example]."

5. **Effort/Validity Integration:** If validity measures are failed, state clearly that results cannot be interpreted as reflecting true cognitive ability. Do not diagnose from invalid profiles.

6. **Cultural and Linguistic Factors:** Note when normative samples may not fully represent the patient. Interpret cautiously when language, education, or cultural factors may affect performance.

### Section 6: Summary and Diagnostic Impressions

Synthesize all findings into a cohesive clinical narrative.

**Structure:**
1. **Opening summary** — restate referral question and key demographics (1–2 sentences)
2. **Cognitive profile summary** — strengths, weaknesses, overall pattern (1 paragraph)
3. **Integration with history** — how cognitive findings relate to medical/psychiatric history (1–2 paragraphs)
4. **Diagnostic formulation** — primary and differential diagnoses with DSM-5-TR/ICD-10 codes (numbered list)
5. **Functional implications** — how findings affect daily living, school, work, social functioning (1 paragraph)
6. **Validity and limitations** — factors that may qualify interpretation (1–2 sentences)

**Diagnostic Considerations by Presentation:**

| Presentation | Key Diagnostic Possibilities |
|-------------|------------------------------|
| Memory complaint, older adult | MCI (amnestic vs. non-amnestic), Major/Minor NCD (Alzheimer's, vascular, Lewy body, frontotemporal), depression-related cognitive difficulties |
| Attention/executive difficulties | ADHD, executive dysfunction secondary to TBI, depression, anxiety, sleep disorder |
| Academic underperformance (child) | Specific Learning Disorder (reading, math, written expression), ADHD, Intellectual Disability, ASD, anxiety/depression |
| Post-TBI | Neurocognitive Disorder due to TBI (major/mild), PTSD, depression, persistent post-concussive symptoms |
| Forensic/disability | Consider malingering/symptom exaggeration if validity fails; diagnose only from valid profiles |

**DSM-5-TR Neurocognitive Disorder Framework:**

- **Major NCD:** Significant cognitive decline from prior level + interferes with independence in everyday activities
- **Mild NCD:** Modest cognitive decline + does NOT interfere with independence (may require compensatory strategies)
- **Specify etiology:** Alzheimer's, vascular, Lewy body, frontotemporal, TBI, substance-induced, HIV, Parkinson's, Huntington's, prion, other/unspecified
- **Specify:** With or without behavioral disturbance

### Section 7: Recommendations

Provide specific, actionable, numbered recommendations tailored to the individual. Avoid generic boilerplate.

### Section 8: Limitations of Evaluation

Document factors that may qualify interpretation:

- Norm sample match (age, education, language, culture)
- Sensory capacity (vision, hearing)
- Fatigue, medications, medical conditions
- Session splits or incomplete testing
- Incomplete records or collateral information
- Language of evaluation vs. patient's primary language
- Cultural factors affecting test validity

### Section 9: Signature Block

**Recommendation Categories:**

#### Medical/Neurological
- Referrals (neurology, psychiatry, primary care, sleep medicine)
- Neuroimaging (MRI, PET) if indicated
- Laboratory workup (B12, folate, thyroid, RPR, metabolic panel)
- Medication management
- Follow-up neuropsychological evaluation (with timeline)

#### Psychological/Psychiatric
- Psychotherapy modality (CBT, DBT, EMDR, supportive)
- Psychiatric medication consultation
- Support groups
- Crisis resources if applicable

#### Cognitive Rehabilitation / Compensatory Strategies
- Cognitive rehabilitation therapy
- External memory aids (calendars, smartphones, pill organizers, alarms)
- Environmental modifications (reduce distractions, structured routines)
- Cognitive exercises (specify type, not just "brain games")

#### Educational (for children/students)
- IEP or 504 plan recommendations
- Specific accommodations (extended time, preferential seating, reduced workload, assistive technology)
- Tutoring or specialized instruction (Orton-Gillingham for dyslexia, etc.)
- Grade retention or advancement considerations
- Transition planning (for adolescents)

#### Vocational/Occupational
- Vocational rehabilitation referral
- Workplace accommodations (written instructions, task checklists, reduced multitasking)
- Fitness for duty considerations
- Disability determination support

#### Safety / Functional
- Driving evaluation referral
- Independent living assessment
- Capacity considerations (medical, financial, legal)
- Supervision needs
- Fall prevention

#### Lifestyle
- Exercise recommendations
- Sleep hygiene
- Nutrition
- Cognitive engagement and social participation
- Substance use treatment if applicable

```
_________________________________
[Clinician Name], [Credentials]
[Title, e.g., Licensed Clinical Neuropsychologist]
[License Number]
[Institution/Practice Name]
[Contact Information]

This report is confidential and intended solely for the use of the referral
source and patient. Unauthorized distribution is prohibited. This evaluation
does not constitute an ongoing treatment relationship.
```

---

## NSE Transcript Summarization Protocol

When working from a Neurobehavioral Status Exam (NSE) transcript:

### Chain of Density (CoD) Method

1. **First pass:** Read entire transcript, noting key themes and structure
2. **Section-by-section analysis:** For each report section, extract relevant quotes and data points
3. **Integration:** Cross-reference information across sections (e.g., family history of ADHD mentioned in educational section)
4. **Density refinement:** Progressively add nuance and detail, resolving conflicts
5. **Final review:** Ensure no relevant information is omitted regardless of where it appeared in the transcript

### NSE Summary Output Target
- 1–3 pages covering Reason for Referral + Background/History
- Focus on information directly relevant to the chief complaint
- Note discrepancies between sources (patient vs. collateral vs. records)
- Maintain positive but neutral professional tone
- Third person, past tense throughout

---

## Score Presentation Standards

### Score Tables

Always include a comprehensive score table, either integrated within domain sections or as an appendix.

**Required columns:** Measure, Subtest/Index, Standard Score (or T-score/Scaled Score), Percentile, Classification

**Formatting rules:**
- Use consistent score metric within each table
- Bold or highlight significantly impaired scores
- Include confidence intervals where clinically relevant
- Note if age-corrected, education-corrected, or demographically adjusted norms were used
- Footnote any non-standard administration or accommodations

### Score Interpretation Caveats

Always include a paragraph explaining the normative framework:

```
Standard scores have a mean of 100 and standard deviation of 15. Scaled scores
have a mean of 10 and standard deviation of 3. T-scores have a mean of 50 and
standard deviation of 10. Percentile ranks indicate the percentage of same-age
peers in the normative sample who scored at or below that level.
```

---

## Validity Assessment

### Performance Validity Testing (PVT)

Document results of embedded and standalone validity measures. If PVT is failed:

```
Performance validity testing revealed scores below established cutoffs on
[measure(s)], raising concern for [suboptimal effort / non-credible cognitive
performance / symptom exaggeration]. As such, the current cognitive test results
cannot be interpreted as a reliable reflection of [Patient]'s true neurocognitive
abilities, and diagnostic conclusions based on the cognitive profile are
significantly limited.
```

### Symptom Validity Testing (SVT)

Document results of self-report validity scales (e.g., MMPI-3 validity scales, PAI validity scales):

```
Symptom validity indices on the [measure] were [within acceptable limits /
elevated], suggesting [a credible / a potentially exaggerated] self-report of
symptoms.
```

---

## Cultural and Linguistic Considerations

When evaluating patients from diverse backgrounds:

- Document primary language and language of evaluation
- Note interpreter use (if applicable) and impact on test validity
- Identify which tests have adequate normative data for the patient's demographic group
- Discuss limitations of cross-cultural assessment
- Consider alternative explanations for low scores (education quality, test-taking experience, acculturation)
- Reference appropriate culturally adapted norms when available

---

## Pediatric-Specific Sections

For evaluations of children/adolescents, add:

### Teacher/School Input
- Teacher rating scales (BRIEF, Conners, BASC)
- Classroom observations (if conducted)
- Review of educational records (report cards, standardized testing, IEP documents)

### Developmental History (Expanded)
- Pregnancy and birth complications
- Milestone achievement (sitting, walking, first words, sentences)
- Early intervention services
- Daycare/preschool concerns

### Adaptive Behavior
- Vineland-3 or ABAS-3 scores
- Self-care, communication, socialization, motor skills
- Comparison of adaptive functioning to cognitive ability

---

## Geriatric/Dementia-Specific Sections

For evaluations of older adults with suspected neurodegenerative disease:

### Collateral Interview Summary
- Informant relationship and reliability
- Onset and progression of cognitive/functional changes
- Comparison to prior level of functioning
- ADL and IADL changes (driving, finances, medication management, cooking)
- Behavioral changes (personality, apathy, disinhibition, psychosis)

### Functional Assessment
- Instrumental ADLs (finances, medications, transportation, meal preparation)
- Basic ADLs (grooming, dressing, toileting, feeding)
- Safety concerns (wandering, leaving stove on, falls)

### Capacity Considerations
- Medical decision-making capacity
- Financial capacity
- Testamentary capacity (if requested)
- Driving capacity

### Staging (if applicable)
- CDR (Clinical Dementia Rating) stage
- GDS (Global Deterioration Scale) stage
- Functional Assessment Staging (FAST) if applicable

---

## Regulatory and Ethical Compliance

### APA Ethical Standards
- Competence (Standard 2.01)
- Informed consent (Standard 3.10, 9.03)
- Maintaining test security (Standard 9.11)
- Release of test data vs. test materials (Standard 9.04)
- Bases for assessment (Standard 9.01)
- Use of assessments (Standard 9.02)

### HIPAA Compliance
- De-identify per Safe Harbor method (18 identifiers) for case examples
- Minimum necessary disclosure
- Secure storage and transmission of reports
- Patient authorization for release

### Test Security
- Do NOT include actual test items or stimuli in reports
- Do NOT include verbatim responses that reveal test content
- DO include scores, error types, and qualitative descriptions of performance

### Informed Consent Documentation
Include a statement such as:
```
Prior to the evaluation, informed consent was obtained. The purpose, nature, and
limitations of the evaluation were explained. [Patient / Patient's legal guardian]
indicated understanding and provided consent to proceed.
```

---

## Writing Style Guide

### Tone and Voice
- Third person, past tense (evaluation already occurred)
- Professional, clinical, and objective
- Positive but neutral (avoid pejorative language)
- Patient-centered (person-first language unless patient prefers otherwise)

### Language Precision
- Use "suggests" or "is consistent with" rather than "proves" or "confirms"
- Use "low average range" rather than "below average" when score is 80–89
- Avoid deficit language when scores are within normal limits
- Distinguish between "impaired" (statistically and clinically significant) and "relatively lower" (within normal variability)

### Readability
- Write for a professional but non-specialist audience (referring physicians, educators, attorneys)
- Define uncommon neuropsychological terms
- Avoid excessive jargon
- Use clear transitions between sections
- Keep paragraphs focused (one main idea per paragraph)

### Common Pitfalls

- **Score dump**: Listing scores without narrative integration or referral linkage
- **Missing validity**: Ignoring PVT/SVT or cooperation when the battery includes them or when data are inconsistent
- **Causal overreach**: Stating lesion- or event-specific causation without converging evidence
- **Norm mismatch**: Applying English-language norms without comment to multilingual evaluees
- **Recommendations vague**: "Follow up with neurology" without indicating why and what question to resolve
- **Forensic boundary errors**: Answering legal questions (e.g., ultimate legal issue) outside professional or jurisdictional standards—flag for attorney and supervisor review
- **Over-pathologizing:** Calling Average scores "weaknesses" without premorbid context
- **Under-contextualizing:** Reporting scores without functional implications
- **Boilerplate recommendations:** Generic suggestions not tailored to the individual
- **Missing integration:** Listing scores without explaining the cognitive profile pattern
- **Premature closure:** Diagnosing based on a single data point
- **Excessive length:** Including irrelevant details that dilute key findings

---

## Quality Assurance

Before sign-out, use `assets/quality_checklist_neuropsych.md`. Run `check_deidentification.py` on drafts that will leave a clinical environment.

---

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

---

## Integration with Other Skills

This skill integrates with:
- **clinical-reports**: General clinical documentation framework
- **scientific-writing**: Professional medical writing standards
- **scientific-schematics**: Generate cognitive profile visualizations
- **pdf**: Export finalized reports to PDF format
- **docx**: Format reports as Word documents for clinical use

---

## Resources

### Reference Files
- `references/neuropsych_test_compendium.md` — Common tests by domain with normative information
- `references/diagnostic_frameworks.md` — DSM-5-TR NCD criteria, ADHD, LD, ASD frameworks
- `references/score_classification_systems.md` — Normative classification tables
- `references/cultural_considerations.md` — Cross-cultural assessment guidelines
- `references/regulatory_and_ethical_compliance.md` — HIPAA, APA ethics, test security, billing/CPT codes, forensic standards
- `references/data_presentation_and_terminology.md` — Score table design, neuropsych abbreviations, ICD-10 codes, neuroanatomical terminology

### Template Assets
- `assets/full_neuropsych_report_template.md` — Complete report template
- `assets/brief_cognitive_assessment_template.md` — Screening/brief report template
- `assets/pediatric_neuropsych_template.md` — Pediatric evaluation template
- `assets/geriatric_dementia_template.md` — Dementia evaluation template
- `assets/forensic_neuropsych_template.md` — Forensic report template
- `assets/score_table_template.md` — Standardized score table format
- `assets/nse_summary_template.md` — NSE transcript summary template

### Automation Scripts
- `scripts/classify_scores.py` — Convert raw/standard scores to normative classifications
- `scripts/validate_neuropsych_report.py` — Check report completeness against required sections
- `scripts/generate_score_table.py` — Generate formatted score tables from data input

---

## Final Checklist

Before finalizing any neuropsychological report, verify:

- [ ] Reason for referral clearly stated with specific questions
- [ ] Background history comprehensive and sourced
- [ ] Behavioral observations support validity statement
- [ ] All tests administered are listed with versions
- [ ] Performance validity testing documented and interpreted
- [ ] Scores presented with normative classifications
- [ ] Domain-by-domain interpretation provided
- [ ] Scores anchored to premorbid estimate
- [ ] Pattern analysis across domains conducted
- [ ] Functional implications stated (school, work, home, social)
- [ ] Diagnostic impressions supported by converging evidence
- [ ] DSM-5-TR / ICD-10 codes included
- [ ] Recommendations specific, actionable, and individualized
- [ ] Cultural/linguistic factors addressed
- [ ] Limitations of evaluation documented
- [ ] Informed consent documented
- [ ] Test security maintained (no items/stimuli in report)
- [ ] HIPAA compliance verified
- [ ] Visual enhancement included (domain profile, timeline, or brain-behavior diagram)
- [ ] Report proofread for accuracy, grammar, and tone
- [ ] Signature block complete with credentials and license

---

**Final note**: Neuropsychological reports influence medical care, education, benefits, and legal proceedings. Prioritize accuracy, clarity, appropriate humility, and respect for the evaluee. When in doubt, narrow the conclusion and broaden the limitations.
