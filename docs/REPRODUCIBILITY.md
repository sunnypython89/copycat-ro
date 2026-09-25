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
- Runtime layout: flat working directory created explicitly by the materialization tool

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

## Published artifacts and supported workflow

The selected datasets, scripts, results and reports are now included. No adapter weights are distributed. The experiment index is the verified lineage: Copycat 05 is a separate fresh-LoRA branch; 05B starts from 04, and 10 starts from 07. The earlier approximate diagram omits intermediate branches.

### Offline verification (standard library only)

```bash
python tools/verify_publication.py
python tools/scan_secrets.py .
python tools/materialize_workspace.py ../copycat-runtime --available-benchmarks-only --with-results
```

The target directory must not exist. Materialization copies the archival scripts and data into their historical flat layout. `--available-benchmarks-only` removes the absent editing benchmark from BENCHMARKS/EXPECTED in runtime training-script copies only; it does not change Gold data, hyperparameters, training updates or the frozen semantic benchmarks. The publication keeps the original public-script versions. Omitting this flag preserves the historical missing-file dependency. `--with-results` is for historical analysis; omit it for new inference to avoid output-name collisions.

Historical scorers may be run only on those saved outputs, from the runtime directory. Their fixed ID labels do not measure a new model. New outputs require fresh review against the reference/criteria fields.

### New GPU experiments (not executed for this publication)

Install PyTorch with CUDA appropriate for your own system, transformers, peft, accelerate and bitsandbytes. Exact historical versions are not completely recorded; no speculative version lock is supplied. Obtain the attributed upstream base model under its applicable terms. The scripts use 4-bit NF4 with float16 compute; successful rerunning on a new environment and bitwise-identical weights are not certified.

In a fresh materialized runtime, the main training order is:

```bash
python train_copycat_04.py
python train_copycat_05b_epoch1.py
python train_copycat_05b_epoch2.py
python train_copycat_06_epoch1.py
python train_copycat_07_epoch1.py
python train_copycat_08_epoch1.py
python train_copycat_09_epoch1.py
python train_copycat_10_epoch1.py
```

`train_copycat_05.py` is an optional separate fresh-LoRA branch. Copycat 10 uses the saved 07 parent, not the 09 adapter. Never rerun the 04 script into an existing output directory: the original 04 script does not refuse overwriting. Use a fresh runtime per reproduction. Other historical branches used in older baseline evaluators are not all distributed in this selected release.

From the repository root, to evaluate an independently recreated adapter only on available semantic benchmarks:

```bash
python evaluation/evaluate_available.py --checkpoint 10 --adapter ../copycat-runtime/copycat_10_consolidare_epoch1_adapter --output ../copycat-runtime/new_semantic_10.jsonl
```

This new portability helper follows the recorded generation settings (160 new tokens for 04–09; 384 for 10), validates benchmark hashes and refuses to overwrite output. It omits editing entirely. It produces unscored new answers; historical pass-ID lists must not be reused. For the separate 09 route experiment the original script uses 384 tokens; the main 09 evaluation uses 160.

## Scope limitation

The missing editing benchmark is not required for training updates or the available semantic benchmark tasks, but it IS required by the original aggregate scripts. See PUBLICATION_NOTES.md for the precise distinction. No benchmark is reconstructed. This release reproduces data/annotation evidence and supplies a reduced-scope experiment workflow, not a claim that every historical score can be regenerated.

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

### Windows console encoding

Use `python -X utf8 script.py` for historical scorers on Windows. Their Romanian console output may otherwise fail under a legacy code page; saved annotations are not changed. The four included historical scoring scripts were replayed on isolated saved outputs and reproduced all 588 scored records exactly as parsed JSON.
