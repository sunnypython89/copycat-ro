# Reproducibility

This document describes the current experimental protocol for Copycat RO.

## Base model

- Model: `OpenLLM-Ro/RoMistral-7b-Instruct-2025-04-23`
- Language: Romanian
- Base-model license: CC BY-NC 4.0
- Training method: incremental LoRA / QLoRA-style local fine-tuning

## Hardware used in the reported experiments

- GPU: NVIDIA GeForce RTX 3080 Ti
- OS: Windows 11
- Local project directory used during development:
  `C:\Users\HomePc\Desktop\chatmistral`

Hardware details are reported for reproducibility, not as a requirement.

## Core LoRA configuration

Most reported checkpoints use:

- rank: `r=8`
- alpha: `16`
- dropout: `0.05`
- target modules: `q_proj`, `v_proj`
- seed: `42`

Learning rate and number of epochs vary by lesson and are recorded with each checkpoint report.

## Experimental protocol

The project follows a strict order:

1. build a Gold training set;
2. build a separate benchmark;
3. freeze the benchmark;
4. record its hash;
5. evaluate existing checkpoints before training when useful;
6. train a new adapter without overwriting previous adapters;
7. evaluate on both the new benchmark and earlier frozen benchmarks;
8. classify every meaningful error;
9. use the error family to design the next lesson.

Benchmarks must never be added to training data.

## Frozen benchmark principle

A benchmark is not edited after the first official evaluation.

If a prompt later proves linguistically disputable:
- the original benchmark remains unchanged;
- the item is marked as disputed;
- a diagnostic score may additionally exclude it.

This preserves reproducibility without pretending every annotation is perfect.

## Current checkpoint lineage

Approximate research lineage:

```
RoMistral base
  |
Copycat 04
  |
Copycat 05B e2
  |
Copycat 06 e1
  |
Copycat 07 e1
  |\
  | Copycat 08 e1
  |      |
  |   Copycat 09 e1
  |
Copycat 10 consolidation (trained from Copycat 07 with replay from later lessons)
```

Older experimental branches are intentionally retained because they contain complementary behavior.

## Evaluation dimensions

Current evaluation families include:

- strict edit scope / NOOP;
- uncertainty without unsupported invention;
- ambiguity preservation;
- ambiguity resolution through evidence;
- resistance to irrelevant information;
- local vs global modifier scope;
- multi-step candidate elimination;
- reasoning-trace consistency;
- conversational tone;
- Romanian idioms.

## Trace scoring

For later lessons, a correct final answer is not sufficient.

Responses can be scored as:

- correct final + correct trace;
- correct final + incorrect trace;
- incorrect final.

A correct conclusion produced through contradictory eliminations is not treated as full evidence of learning.

## Current key rule

> New information should eliminate a candidate only when it contradicts that candidate or makes it incompatible with the available evidence.

This rule emerged from repeated failures across Lessons 06–10.

## Files still to import from the local research folder

The public repository currently contains the research documentation first.

The following classes of local artifacts should be imported next:

- frozen benchmark JSONL files;
- Gold JSONL files;
- benchmark hashes;
- training scripts;
- evaluation scripts;
- scored raw result JSONL files;
- checkpoint metadata;
- selected error reports.

Large model/adaptor weights should not be committed directly to GitHub. A model hosting platform is more appropriate for those artifacts.

## Reproducibility rule for future commits

Every reported score should be traceable to:

- exact checkpoint name;
- benchmark filename;
- benchmark hash;
- training dataset composition;
- LoRA configuration;
- learning rate;
- epoch count;
- seed;
- raw evaluation output.
