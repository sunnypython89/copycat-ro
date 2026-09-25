# Benchmarks

This directory contains the six available frozen semantic JSONL benchmarks, copied byte-for-byte. HASHES.sha256 uses paths relative to this directory.

## Rules

1. Benchmarks are created before the training run they evaluate.
2. Benchmark prompts are not copied into Gold training data.
3. Once used for official evaluation, a benchmark is frozen.
4. SHA-256 hashes are recorded where available.
5. Linguistically disputed items remain in the official benchmark for reproducibility, but may also be excluded from a separate diagnostic score.
6. New lessons should become harder rather than repeatedly testing memorized examples.

## Benchmark families

Current benchmark sequence:

- Editare 04 — strict editing and requested scope
- Lecția 05 — ambiguity, idioms, uncertainty, conversational tone
- Lecția 06 — ambiguity enumeration
- Lecția 07 — evidence-based elimination
- Lecția 08 — threshold between ambiguous and resolved
- Lecția 09 — sequential elimination
- Benchmark 10 — consolidation

## Important methodological distinction

An **unseen idiom** is partly a test of lexical-cultural knowledge in the base model.

A **taught idiom used in a new context** is a better test of learned generalization.

These should not be conflated.

The historical 36-item editing source is missing and is not reconstructed. The benchmark families list includes historical context, not a claim that an editing benchmark file is shipped.
