# Reading guide

This repository contains the full experimental record of Copycat RO. You do not need to read it in chronological order.

## If you have 3 minutes

Read:

1. the main [README](../README.md);
2. the first section of [LIMITS_v1.md](LIMITS_v1.md);
3. the oracle-union table in [RESULTS.md](RESULTS.md).

The central finding is that different checkpoints exhibit complementary semantic abilities, while a single LoRA adapter does not yet preserve all of them simultaneously.

## If you have 10–15 minutes

Read:

1. [README](../README.md) — motivation and main result;
2. [EXPERIMENT_INDEX.md](EXPERIMENT_INDEX.md) — exact training lineage;
3. [LIMITS_v1.md](LIMITS_v1.md) — failure families;
4. [RAPORT_COPYCAT_10_CONSOLIDARE.md](../reports/RAPORT_COPYCAT_10_CONSOLIDARE.md) — most recent consolidation experiment.

This gives enough context to understand the research direction without reading every intermediate report.

## If you want to reproduce or audit the work

Read:

1. [REPRODUCIBILITY.md](REPRODUCIBILITY.md);
2. [PUBLICATION_NOTES.md](PUBLICATION_NOTES.md);
3. [EXPERIMENT_INDEX.md](EXPERIMENT_INDEX.md);
4. `benchmarks/HASHES.sha256`;
5. the matching files in `training/`, `evaluation/`, `results/` and `reports/`.

The publication intentionally keeps benchmark hashes, raw outputs and historical scripts separate from the explanatory documentation.

## Core vocabulary

### Gold
Training examples created for a lesson.

### Benchmark
A frozen evaluation set kept separate from training data.

### Replay
Older examples mixed into a later lesson to reduce forgetting.

### Landmark
An informal project term for a behavioral rule that has become relatively stable.

Examples:
- do not modify text outside the requested scope;
- do not invent meaning without evidence.

### Oracle union
A diagnostic score where an item counts as solved if at least one checkpoint in a selected family solves it.

It is **not** the performance of a deployable model. It measures how much capability exists across the checkpoint family.

### Consolidation
Training intended to make several previously learned behaviors coexist in one adapter.

---

## The current research problem

The project began with local language-control tasks and gradually moved toward evidence-sensitive reasoning.

The current problem can be summarized as:

> **How should a model update its set of possible interpretations when new information arrives?**

A recurring failure is treating new information as automatically decisive.

The current curriculum rule is:

> **New information eliminates a candidate only if it contradicts that candidate or makes it incompatible with the available evidence.**

This rule connects several earlier lessons:

- ambiguity;
- uncertainty;
- relevance;
- elimination;
- sequential state tracking.

---

## What is already strong

Strict editing behavior became highly stable across later checkpoints.

The model also learned useful forms of uncertainty calibration and ambiguity handling.

The strongest evidence that the project is not simply memorizing one benchmark is that different checkpoints generalize differently to later unseen benchmark families.

---

## What is still weak

The largest unresolved issues are:

- semantic interference between lessons;
- deciding whether a clue is genuinely eliminative;
- sequential candidate tracking;
- distinguishing plausible interpretations from interpretations forced by evidence;
- preserving several learned decision boundaries in one adapter.

---

## Why older checkpoints are kept

An older checkpoint may outperform a newer one on a specific semantic family.

Deleting it would remove evidence about:
- catastrophic/interfering forgetting;
- complementary capabilities;
- which rule was gained or lost at each stage.

For this project, regressions are part of the result.

---

## Publication boundary

This repository contains 104 public files selected from a larger local research directory.

Model adapters are excluded.

The missing historical file `benchmark_copycat_03_on_04.py` was not reconstructed. Any historical score that depends exclusively on it is clearly marked as historical rather than freshly reproducible.

For the full publication boundary, see [PUBLICATION_NOTES.md](PUBLICATION_NOTES.md).
