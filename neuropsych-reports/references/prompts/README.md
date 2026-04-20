# Prompt Library

## Purpose

This folder holds prompts that are meant to be read, reasoned over, refined, and versioned as part of the agent workflow.

## Put prompts here when they are:
- system prompts
- extraction prompts
- summarization prompts
- implementation prompts
- JSON prompt specs used by scripts or agents
- prompts you expect to revise often

## Keep in `assets/templates/` instead when they are:
- stable scaffold templates with placeholders
- output resources rendered into reports or downstream tools

## Current prompt groups

### Intake and transcript extraction
- `nse_intake_extraction_prompt.json`
- `transcribe_and_summarize_mental_status_exam.json`
- `transcribe_and_summarize_neurobehavioral_status_exam.json`

### Narrative generation
- `neurobehav.prompt`
- `neurocog.prompt`
- `summary.prompt`

### Quarto prompt templates still in assets
The `.qmd` files under `assets/prompts/` currently behave more like output/template resources. Keep them there unless you want to actively edit them as reasoning prompts.
