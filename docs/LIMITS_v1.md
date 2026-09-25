# Copycat — observed limits, v1

This document summarizes the first repeatable limits observed after Lessons 04–10.

## Executive summary

Copycat does **not** yet look conclusively capped by the base RoMistral model. The clearest current limitation is the ability of one LoRA adapter to preserve several learned semantic constraints at the same time.

The strongest evidence is the gap between individual checkpoints and the oracle union across checkpoints.

| Benchmark | Oracle union |
|---|---:|
| Lesson 06 | 18/24 |
| Lesson 07 | 23/24 |
| Lesson 08 | 26/32 |
| Lesson 09 | 29/32 |

Many failures of one checkpoint are solved by another checkpoint using the same base model. This points to **interference / consolidation limits**, not necessarily a hard limit of the base model.

## Stable capability

Strict editing remains the most stable landmark:
- Copycat 04: 36/36
- Copycat 05B e2: 36/36
- Copycat 06: 36/36
- Copycat 07: 36/36
- Copycat 08: 36/36
- Copycat 09: 36/36
- Copycat 10: 36/36

## Main observed limits

### 1. Interference between learned landmarks
Repeated pattern: learn A, weaken B, repair B, weaken A again.

### 2. Evidence threshold instability
Copycat can learn both preserving ambiguity and resolving ambiguity, but the transition between them is unstable.

### 3. Relevance of new information
A recurring error is treating any new information as eliminative evidence.

> New information should eliminate a candidate only when it contradicts that candidate or makes it incompatible with the available evidence.

### 4. Sequential elimination / state tracking
Copycat may ignore a later clue, reintroduce an already eliminated candidate, or reach a correct final answer through an inconsistent trace.

### 5. Local vs global scope
Persistent errors occur when a modifier can apply only to the nearest coordinated element or to the whole coordination.

### 6. Lexical-cultural knowledge
The RoMistral base model performed poorly on several Romanian idioms. This is distinct from reasoning failure.

### 7. Benchmark uncertainty
Some prompts proved debatable for native speakers. Frozen official scores are preserved for reproducibility, while diagnostic scores may exclude disputed items.

## Copycat 10

| Benchmark | Score |
|---|---:|
| Editing 04 | 36/36 |
| Lesson 05 | 9/16 |
| Lesson 06 | 12/24 |
| Lesson 07 | 17/24 |
| Lesson 08 | 19/32 |
| Lesson 09 | 20/32 |
| Benchmark 10 | 22/32 |

Benchmark 10:
- ambiguity preserved: 7/8
- ambiguity resolved: 6/8
- irrelevant evidence ignored: 5/8
- sequential elimination: 4/8
- correct final + correct trace: 21/32

## Current technical hypotheses

To be tested separately:
1. LoRA rank may be too small at `r=8`.
2. Targeting only `q_proj` and `v_proj` may be too restrictive.
3. Sequential curriculum may produce avoidable interference.
4. Hard-negative replay may preserve boundaries better than clean replay alone.
5. Specialized adapters plus routing/consolidation may preserve complementary skills better.

## Most useful conceptual direction

> **The strength of the conclusion should be proportional to the strength of the evidence.**

This may unify ambiguity, uncertainty, evidence relevance, elimination, and resistance to overconfident guessing.
