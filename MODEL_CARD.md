# Copycat RO — Model Card (Research)

## Overview

Copycat RO is an independent Romanian-language adaptation and evaluation project built on:

`OpenLLM-Ro/RoMistral-7b-Instruct-2025-04-23`

The project studies semantic precision, ambiguity handling, uncertainty calibration, controlled editing, evidence relevance, and multi-step elimination.

## Current research checkpoint

Current consolidation checkpoint:

`copycat_10_consolidare_epoch1_adapter`

This checkpoint is not yet distributed from this repository.

## Intended use

Research and evaluation of Romanian-language LLM behavior, especially:

- ambiguity preservation and resolution;
- evidence-based elimination;
- strict editing scope;
- uncertainty without unsupported invention;
- trace consistency;
- semantic interference across incremental LoRA lessons.

## Not intended as

- a production-ready assistant;
- a legal, medical, or safety-critical system;
- evidence of an official affiliation with Politehnica University of Bucharest;
- a commercial release of the base model or derived adapters.

## Base model attribution

Base model:
`OpenLLM-Ro/RoMistral-7b-Instruct-2025-04-23`

Any release of derived adapter weights must follow the base model's applicable license and attribution requirements.

## Training approach

The research uses incremental LoRA adapters with frozen benchmarks and replay.

Typical configuration:
- rank: `r=8`
- alpha: `16`
- dropout: `0.05`
- target modules: `q_proj`, `v_proj`
- seed: `42`

Later experiments vary the learning rate while keeping other variables controlled.

## Current central rule

> New information should eliminate a candidate only when it contradicts that candidate or makes it incompatible with the available evidence.

## Known limitations

See:
- `docs/LIMITS_v1.md`
- `docs/RESULTS.md`
- `docs/REPRODUCIBILITY.md`

The strongest current limitation is incomplete consolidation of several learned semantic constraints into a single adapter.

## Status

Research prototype. Benchmarks and training/evaluation code are being published incrementally for reproducibility.
