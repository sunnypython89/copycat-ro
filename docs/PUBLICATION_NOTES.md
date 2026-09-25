# Publication notes — reproducible research artifacts v1

This publication preserves the local research originals. Selection is authorized by the publication request and supersedes the draft inventory’s default exclusion of raw results where those results support the selected experiments. No training or inference was started; no adapter is published.

## Reproducibility boundary and missing benchmark

`benchmark_copycat_03_on_04.py` was referenced historically and is absent from the current 240-file inventory. Its recorded expected SHA-256 is `8b27807ea0350b13297e4201234582a3a27a626047710f96c27ebe08ed247ad0`. It has NOT been reconstructed, renamed from another benchmark, or replaced with extracted result prompts.

It is not needed for the training data/updates of experiments 04–10 or for evaluation on the six available semantic JSONL benchmarks. However, the original historical training scripts 05–10 hash it, and the aggregate historical evaluators read it. Running those unmodified scripts therefore requires the missing file. The explicit available-benchmark workflow removes only that unavailable training integrity check in an isolated runtime copy, and uses a separate semantic-only evaluator. This is reduced-scope reproduction, not exact end-to-end historical reproduction. Scores depending exclusively on the missing file (notably the 36-item editing benchmark) remain historical and are not reproducible by fresh inference from this publication.

The original evaluators and scorers are retained as provenance. Several scorers encode fixed sets of passing IDs; they replay historical review decisions and MUST NOT grade new model outputs. Gold files and model responses are byte-identical copies. Full raw outputs, including historical editing responses, are evidence, not substitute benchmark definitions.

## Layout and modifications

Artifacts are organized under benchmarks/, gold/, training/, evaluation/, results/ and reports/. Historical scripts assume a flat runtime directory: use the explicit materialization tool documented in REPRODUCIBILITY.md. It does not train or download a model. Local workstation paths are changed only in public script/report copies and metadata; original/public hashes are recorded in PUBLICATION_MANIFEST.json. No benchmark values, Gold records or model responses were edited. No blanket license is added. Base-model attribution and the existing upstream-license note are retained; independently verifying rights for future reuse remains necessary.

Gold files are selected from recorded training sources, including filtered and replay subsets required for exact composition. Different subsets are not byte duplicates and must not be substituted for their parent files. Unfiltered precursor variants not used in the selected runs are omitted. Raw and scored results are both retained where they distinguish model output from human annotations or support baseline comparisons.

## Exclusions

All 13 adapter directories (91 files) are excluded, as are binary weights, caches, environment/credential files, runtime logs, conversation logs, chat clients and out-of-scope early/diagnostic artifacts. See EXCLUDED_ARTIFACTS.json for every inventoried omitted source file and its original hash. Derived experiment metadata in this publication is a curated documentation extract, not a copied adapter directory.

The six exact-duplicate groups contain 65 files: 6 canonical local references and 59 redundant copies. All 65 are inside excluded adapter directories, so none is republished. The canonical files remain unchanged locally; preserving one public copy would contradict the explicit complete adapter exclusion. Duplicate counts are a subset of the excluded-file count and must not be added again.

## Evidence and verification

Six frozen JSONL benchmark hashes are listed in benchmarks/HASHES.sha256. Static JSON/Python parsing, source/public hashes, dataset counts and annotation totals are verified by tools/verify_publication.py. The secret scan uses offline signatures for common credentials/private keys and literal credential assignments; it is not proof that no secret can exist. Publication stops if it reports any candidate. No fresh GPU experiment or bitwise training reproducibility is claimed: the original software environment and upstream model revision are not fully pinned.

Only lexical exact-prompt overlap was checked in the earlier inventory; semantic contamination or disputed annotations have not been ruled out. Review reports include real regressions and limits. The central elimination rule is an investigational curriculum hypothesis, not a universally demonstrated truth.

## Exact-duplicate register

### SHA-256 `ea0013a6c1f8e9aa2cb6fb8c760247655cfcaffe7b3de7184faf742f9b5a2b5f`

Canonical local reference: `copycat_05_adapter/adapter_config.json`. No public copy: the explicit adapter-directory exclusion takes precedence.

Omitted from publication:
- `copycat_05_adapter/adapter_config.json` (canonical local reference)
- `copycat_05b_epoch2_adapter/adapter_config.json`
- `copycat_06_epoch1_adapter/adapter_config.json`
- `copycat_07_epoch1_adapter/adapter_config.json`
- `copycat_09_epoch1_adapter/adapter_config.json`
- `copycat_editare_01_adapter/adapter_config.json`

### SHA-256 `7c1bba1675e657adc697a06d00b8e831745a79189f7533535f83f509774c79d0`

Canonical local reference: `copycat_10_consolidare_epoch1_adapter/chat_template.jinja`. No public copy: the explicit adapter-directory exclusion takes precedence.

Omitted from publication:
- `copycat_05_adapter/chat_template.jinja`
- `copycat_05b_adapter/chat_template.jinja`
- `copycat_05b_epoch2_adapter/chat_template.jinja`
- `copycat_06_epoch1_adapter/chat_template.jinja`
- `copycat_07_epoch1_adapter/chat_template.jinja`
- `copycat_08_epoch1_adapter/chat_template.jinja`
- `copycat_09_epoch1_adapter/chat_template.jinja`
- `copycat_10_consolidare_epoch1_adapter/chat_template.jinja` (canonical local reference)
- `copycat_editare_01_adapter/chat_template.jinja`
- `copycat_editare_02_adapter/chat_template.jinja`
- `copycat_editare_03_adapter/chat_template.jinja`
- `copycat_editare_04_adapter/chat_template.jinja`
- `copycat_romana_naturala_01_adapter/chat_template.jinja`

### SHA-256 `3a4cdebf423b58c80a626c8be1e8d8e735c1fdd7f95a3b7bae4857e4d29a8ba7`

Canonical local reference: `copycat_10_consolidare_epoch1_adapter/README.md`. No public copy: the explicit adapter-directory exclusion takes precedence.

Omitted from publication:
- `copycat_05_adapter/README.md`
- `copycat_05b_adapter/README.md`
- `copycat_05b_epoch2_adapter/README.md`
- `copycat_06_epoch1_adapter/README.md`
- `copycat_07_epoch1_adapter/README.md`
- `copycat_08_epoch1_adapter/README.md`
- `copycat_09_epoch1_adapter/README.md`
- `copycat_10_consolidare_epoch1_adapter/README.md` (canonical local reference)
- `copycat_editare_01_adapter/README.md`
- `copycat_editare_02_adapter/README.md`
- `copycat_editare_03_adapter/README.md`
- `copycat_editare_04_adapter/README.md`
- `copycat_romana_naturala_01_adapter/README.md`

### SHA-256 `107a53acc537db9efec29756024e117c2714e65487a7c7d898d5b90c24c4d209`

Canonical local reference: `copycat_10_consolidare_epoch1_adapter/tokenizer.json`. No public copy: the explicit adapter-directory exclusion takes precedence.

Omitted from publication:
- `copycat_05_adapter/tokenizer.json`
- `copycat_05b_adapter/tokenizer.json`
- `copycat_05b_epoch2_adapter/tokenizer.json`
- `copycat_06_epoch1_adapter/tokenizer.json`
- `copycat_07_epoch1_adapter/tokenizer.json`
- `copycat_08_epoch1_adapter/tokenizer.json`
- `copycat_09_epoch1_adapter/tokenizer.json`
- `copycat_10_consolidare_epoch1_adapter/tokenizer.json` (canonical local reference)
- `copycat_editare_01_adapter/tokenizer.json`
- `copycat_editare_02_adapter/tokenizer.json`
- `copycat_editare_03_adapter/tokenizer.json`
- `copycat_editare_04_adapter/tokenizer.json`
- `copycat_romana_naturala_01_adapter/tokenizer.json`

### SHA-256 `74730d5015df30bb40fbaee4f02a94540f61090470ac04c37daa2712b190b120`

Canonical local reference: `copycat_10_consolidare_epoch1_adapter/tokenizer_config.json`. No public copy: the explicit adapter-directory exclusion takes precedence.

Omitted from publication:
- `copycat_05_adapter/tokenizer_config.json`
- `copycat_05b_adapter/tokenizer_config.json`
- `copycat_05b_epoch2_adapter/tokenizer_config.json`
- `copycat_06_epoch1_adapter/tokenizer_config.json`
- `copycat_07_epoch1_adapter/tokenizer_config.json`
- `copycat_08_epoch1_adapter/tokenizer_config.json`
- `copycat_09_epoch1_adapter/tokenizer_config.json`
- `copycat_10_consolidare_epoch1_adapter/tokenizer_config.json` (canonical local reference)
- `copycat_editare_01_adapter/tokenizer_config.json`
- `copycat_editare_02_adapter/tokenizer_config.json`
- `copycat_editare_03_adapter/tokenizer_config.json`
- `copycat_editare_04_adapter/tokenizer_config.json`
- `copycat_romana_naturala_01_adapter/tokenizer_config.json`

### SHA-256 `e056b253f3ecf82fdd53f42bcbfc43ff0c542dc74f07ca7e64e88e521046c041`

Canonical local reference: `copycat_10_consolidare_epoch1_adapter/adapter_config.json`. No public copy: the explicit adapter-directory exclusion takes precedence.

Omitted from publication:
- `copycat_05b_adapter/adapter_config.json`
- `copycat_08_epoch1_adapter/adapter_config.json`
- `copycat_10_consolidare_epoch1_adapter/adapter_config.json` (canonical local reference)
- `copycat_editare_02_adapter/adapter_config.json`
- `copycat_editare_03_adapter/adapter_config.json`
- `copycat_editare_04_adapter/adapter_config.json`
- `copycat_romana_naturala_01_adapter/adapter_config.json`
