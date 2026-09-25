# Copycat RO

**Copycat RO** is an independent experimental project for training and evaluating Romanian-language LLM behavior on semantic precision, ambiguity, uncertainty, controlled editing, and evidence-based elimination.

Base model:

`OpenLLM-Ro/RoMistral-7b-Instruct-2025-04-23`

The project uses incremental LoRA adapters, frozen benchmarks, replay, error-driven curriculum design, and manual native-speaker review.

> **Core rule under investigation:** new information should eliminate a candidate only when it contradicts that candidate or makes it incompatible with the available evidence.

## Current status

Current consolidation checkpoint: **Copycat 10**

Stable capability:
- strict editing benchmark: **36/36**

Current semantic results:
- Lesson 05: **9/16**
- Lesson 06: **12/24**
- Lesson 07: **17/24**
- Lesson 08: **19/32**
- Lesson 09: **20/32**
- Benchmark 10: **22/32**

Benchmark 10:
- preserve ambiguity: **7/8**
- resolve ambiguity: **6/8**
- ignore irrelevant evidence: **5/8**
- sequential elimination: **4/8**
- correct final answer + correct trace: **21/32**

## Main research question

The project is currently investigating whether several semantic constraints can coexist stably in one adapter.

Different checkpoints already show complementary abilities. Oracle-union results across Copycat 07–09:

| Benchmark | Oracle union |
|---|---:|
| Lesson 06 | 18/24 |
| Lesson 07 | 23/24 |
| Lesson 08 | 26/32 |
| Lesson 09 | 29/32 |

This suggests that substantial capability exists across the checkpoint family, while consolidation into one adapter remains incomplete.

## Method

The curriculum grows from errors rather than from a fixed static syllabus:

1. run a frozen benchmark;
2. classify the error;
3. extract the violated rule;
4. build new examples that test the rule rather than copy the old question;
5. increase difficulty;
6. keep successful behavioral invariants as stable landmarks;
7. test conflicts between landmarks.

Observed landmarks include:
- do not edit outside the requested scope;
- do not invent a meaning without evidence;
- preserve ambiguity while multiple candidates remain valid;
- resolve ambiguity when evidence removes all but one candidate;
- ignore information that does not actually eliminate a candidate;
- preserve candidate state across sequential elimination.

## Important observed limitation

A recurring failure mode is confusing:

`new information appeared`

with:

`new information actually eliminates a candidate`

This is now a central curriculum target.

## Repository structure

- `docs/LIMITS_v1.md` — detailed report of observed limitations
- `docs/RESULTS.md` — checkpoint and benchmark history
- future: frozen benchmarks, training scripts, evaluation scripts, and reproducibility notes

## Academic review

This is an **independent project** and is not presented as an official project of Politehnica University of Bucharest or OpenLLM-Ro.

The repository is public to make the methodology, failures, benchmark evolution, and training results available for academic review and potential collaboration.

## Licensing note

The project builds on the OpenLLM-Ro RoMistral model. Any redistribution of model weights or derived adapters must respect the applicable base-model license and attribution requirements.

## Current diagnostic directions

- higher LoRA rank;
- adding `k_proj` and `o_proj`;
- interleaved instead of strictly sequential curriculum;
- hard-negative replay;
- specialized adapters with consolidation or routing.

The goal is not to maximize one benchmark score. The goal is to discover stable semantic rules that continue to work as tests become harder.
