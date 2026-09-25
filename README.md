# Copycat RO

**Copycat RO** is an independent research project exploring how a Romanian-language LLM can learn **semantic discipline**: when to stay uncertain, when evidence is strong enough to choose, and how to avoid changing or inferring more than the text supports.

It is built on:

`OpenLLM-Ro/RoMistral-7b-Instruct-2025-04-23`

The project combines incremental LoRA training, frozen benchmarks, replay, error analysis, and native-speaker review.

---

## The idea in one sentence

Copycat is trained not only to produce the right answer, but to respect the boundary between:

- what the text allows;
- what the text rules out;
- what is still ambiguous.

The current central curriculum hypothesis is:

> **New information eliminates a candidate only if it contradicts that candidate or makes it incompatible with the available evidence.**

Romanian:

> **Informația nouă elimină o variantă numai dacă o contrazice sau o face incompatibilă cu dovezile disponibile.**

This is a research hypothesis under investigation, not a claimed universal rule of language.

---

## Why this project exists

A language model can often give a plausible answer even when the evidence is incomplete.

Copycat studies a narrower question:

> **Can a model learn to control the strength of its conclusion according to the strength of the evidence?**

That question appears in several forms:

- preserve ambiguity when several interpretations remain possible;
- resolve ambiguity when evidence removes the alternatives;
- ignore irrelevant information;
- avoid inventing meanings that are not supported;
- keep track of candidates across several elimination steps;
- edit only what was explicitly requested.

The curriculum is built from the model's mistakes. A recurring failure becomes the next lesson.

---

## What has been learned so far

The strongest current finding is **complementarity between checkpoints**.

Different Copycat versions solve different parts of the same semantic problem. When their correct answers are combined diagnostically as an "oracle union", the family performs substantially better than any single checkpoint:

| Benchmark | Oracle union across Copycat 07–09 |
|---|---:|
| Lesson 06 | **18/24** |
| Lesson 07 | **23/24** |
| Lesson 08 | **26/32** |
| Lesson 09 | **29/32** |

This suggests that many capabilities are already reachable from the same base model, but they are not yet consolidated reliably into one LoRA adapter.

The present research problem is therefore less:

> "Can Copycat ever learn this?"

and more:

> "Can Copycat keep several learned semantic rules at the same time without one weakening another?"

---

## Current checkpoint

Current consolidation checkpoint:

`copycat_10_consolidare_epoch1_adapter`

Recorded results:

| Evaluation | Score |
|---|---:|
| Lesson 05 | **9/16** |
| Lesson 06 | **12/24** |
| Lesson 07 | **17/24** |
| Lesson 08 | **19/32** |
| Lesson 09 | **20/32** |
| Benchmark 10 | **22/32** |

Benchmark 10 breakdown:

| Skill | Score |
|---|---:|
| Preserve ambiguity | **7/8** |
| Resolve ambiguity | **6/8** |
| Ignore irrelevant evidence | **5/8** |
| Sequential elimination | **4/8** |
| Correct final answer + correct trace | **21/32** |

The historical strict-editing result is **36/36**, but its original benchmark source is missing from the current archive, so that result is documented as historical rather than freshly reproducible from this release.

---

## How the curriculum works

Each lesson follows the same research loop:

```
model error
    ↓
classify the failure
    ↓
extract the violated rule
    ↓
build new examples testing that rule
    ↓
freeze a new benchmark
    ↓
train one controlled step
    ↓
measure gains, regressions and new conflicts
```

Examples of learned "landmarks":

- do not edit outside the requested scope;
- do not invent a meaning when evidence is absent;
- preserve ambiguity while multiple candidates remain valid;
- resolve ambiguity once all but one candidate are eliminated;
- do not treat every new detail as evidence;
- do not reintroduce a candidate that was already eliminated.

The project deliberately keeps older checkpoints because regressions are useful evidence.

---

## Main limitation observed

The clearest repeatable limitation is **interference between learned rules**.

A simplified pattern is:

```
learn rule A
→ rule B weakens
→ repair B
→ A weakens again
```

Copycat 10 partially reduces this oscillation, but does not yet match the best behavior of every earlier checkpoint at once.

Current hypotheses include:

- LoRA rank `r=8` may be too restrictive;
- adapting only `q_proj` and `v_proj` may limit consolidation;
- strictly sequential lessons may encourage interference;
- hard-negative replay may preserve decision boundaries better;
- specialized adapters may eventually need consolidation or routing.

These are hypotheses to be tested separately, not conclusions already established.

---

## Start here

If you are reviewing the project for the first time:

1. **[Reading guide](docs/READING_GUIDE.md)** — fastest overview of what to read and why.
2. **[Experiment index](docs/EXPERIMENT_INDEX.md)** — exact checkpoint lineage, datasets, hyperparameters and scores.
3. **[Observed limits](docs/LIMITS_v1.md)** — current failure families and technical hypotheses.
4. **[Results summary](docs/RESULTS.md)** — compact score history.
5. **[Reproducibility](docs/REPRODUCIBILITY.md)** — what can and cannot be reproduced from this release.
6. **[Publication notes](docs/PUBLICATION_NOTES.md)** — exclusions, missing artifacts and reproducibility boundaries.

---

## Repository map

| Path | Purpose |
|---|---|
| `benchmarks/` | frozen semantic benchmarks and SHA-256 hashes |
| `gold/` | training Gold sets and replay subsets |
| `training/` | historical training scripts |
| `evaluation/` | evaluation and scoring scripts |
| `results/` | archived raw and scored outputs |
| `reports/` | detailed experiment reports |
| `docs/` | experiment index, limitations and reproducibility notes |
| `tools/` | publication verification and secret-scanning utilities |

No model weights or LoRA adapter directories are published in this repository.

---

## Reproducibility

From the repository root, publication integrity can be checked without GPU dependencies:

```bash
python tools/verify_publication.py
python tools/scan_secrets.py .
```

The six published semantic benchmark files match their recorded hashes.

This release supports verification of datasets, archived outputs, annotations, scripts and experiment metadata. It does **not** claim bit-for-bit historical training reproduction because the upstream model revision and full software environment were not completely pinned.

---

## Academic status

Copycat RO is an **independent research project**.

It is not presented as an official project of Politehnica University of Bucharest, OpenLLM-Ro, or another institution.

The repository is public so that the methodology, failures, regressions and experimental record can be inspected and discussed.

---

## Licensing note

The project builds on the OpenLLM-Ro RoMistral model. Any redistribution of derived model weights or adapters must respect the applicable upstream license and attribution requirements.

The public repository currently distributes research code, datasets, benchmarks, results and documentation, but **not model weights or adapters**.
