# Copycat — results summary

## Main checkpoints

| Checkpoint | Edit 04 | L05 | L06 | L07 | L08 | L09 |
|---|---:|---:|---:|---:|---:|---:|
| Copycat 05B e2 | 36/36 | 7/16 | 16/24 | 15/24 | 13/32 | — |
| Copycat 06 e1 | 36/36 | 5/16 | 15/24 | 16/24 | 10/32 | — |
| Copycat 07 e1 | 36/36 | 8/16 | 14/24 | 17/24 | 17/32 | 22/32 |
| Copycat 08 e1 | 36/36 | 10/16 | 10/24 | 17/24 | 19/32 | 18/32 |
| Copycat 09 e1 | 36/36 | 8/16 | 14/24 | 18/24 | 13/32 | 20/32 |
| Copycat 10 | 36/36 | 9/16 | 12/24 | 17/24 | 19/32 | 20/32 |

## Consolidation floor (Lessons 06–09)

| Model | Minimum normalized score |
|---|---:|
| Copycat 07 | 53.1% |
| Copycat 08 | 41.7% |
| Copycat 09 | 40.6% |
| Copycat 10 | 50.0% |

## Oracle union across Copycat 07–09

| Benchmark | Oracle union |
|---|---:|
| Lesson 06 | 18/24 |
| Lesson 07 | 23/24 |
| Lesson 08 | 26/32 |
| Lesson 09 | 29/32 |

## Interpretation

The checkpoint family is substantially more capable than any one checkpoint.

This is the central experimental observation behind the current investigation into LoRA capacity, interference, replay strategy, and adapter specialization.

## Publication v1 qualification

The 36-item editing scores above are historical: their referenced benchmark source is missing. Semantic scores are recorded annotations of archived outputs, not fresh inference or independent regrading. The elimination rule is a curriculum hypothesis under investigation. See [PUBLICATION_NOTES.md](PUBLICATION_NOTES.md).
