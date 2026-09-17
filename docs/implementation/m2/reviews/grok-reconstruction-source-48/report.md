# Frozen SOURCE48 — retained evaluator input reconstruction

**Verdict: `NO-REQUIRED-FINDINGS`**

Root remains lead. Not Claude agreement. Not fresh-blind. Not live install. Not runtime24. Not atom truth, full composition, replay, custody, or M2. Formal runtime24 remains a separate review before installation.

**subjectManifestSha256** `1e6111fa54a40ef8f99b02d6afb349af4c349a612624e7ff27a65249955b8e0e`  
`docs/implementation/m2/trials/reconstruction-48/subject.json` **109162** bytes, **572** members, paths sorted unique, **0** pin mismatches. Export `/tmp/opensip-implementation/m2-reconstruction-subject-48`. Archive `docs/implementation/m2/trials/reconstruction-48/subject.tar.xz` **3743660** / `0de84d21e015c07bd35a65c8a4b19386c4c38e24682a904638a3f85ddeea6276`.

## Selected composition

Selected lock **30 inventory / 43 contract** (`86154` / `46268ef8be0e1094ed1e03b76e4d0134f6ea9fee0c0247495b6fa45add502be9`). Last inventory candidate **v32**. Last contracts **runtime23** then **reference49**. Accepted-inheritance records exact accepted runtime23 / source47 / reference49; this freeze does **not** self-accept 48.

**270** product files excluding `design-lock.json` (**271** including lock). Versus accepted runtime23 and source47: **265** unchanged non-lock files byte-equal; **3** changed + **2** new = **5** owned, all inventory-32 planned. Selected I in the freeze is reference49 **17561** / `4b2999ca…`.

| Owned | Role |
| --- | --- |
| `input_reconstruction.rs` (new) 30440 / `22968a00…` | public `reconstruct_evaluator_inputs` |
| `full_walk.rs` 19245 / `f3540a76…` | structure accessors used by reconstruction |
| `lib.rs` 3708 / `50df2cb9…` | exact source47 prefix plus the public export |
| `native_owner_tests.rs` 96579 / `4cfe8191…` | 87-case host driver |
| `reconstruction-fixtures.json` (new) 2727520 / `4cec309b…` | 87 durable cases |

The population helper probe exists only in the disposable portable copy.

## Public owner

`reconstruct_evaluator_inputs(inputs, plan_id, execution_id, evaluator_closure, evaluation_refs, limits)`:

- Invokes **`inspect_first_evaluation_structure` first** (SOURCE47). No Run, seal, proof, finding, semantic-evidence, or evaluation-subject objects. No caller-admitted maps or store census.
- Re-reads parameters and enumeration; inventory refs are collected as an **occurrence list**. Duplicate inventories refuse at enumeration (`EVALUATOR_ENUMERATION_JOIN:ENUMERATION_INVENTORY_DUPLICATE`) before population counts. Tests compare **category** plus the reference cause, not full nested diagnostic text.
- Private universe census from the structural owner's retained frames, not ambient objects. Cell/universe domain join uses that census.
- Scanner closures are **Plan.semanticClosures only** (reference49). Native interpreter closures remain required in the retained store via the 47 walk; named-only I-stage deletions are **excluded** from retained-positive claims (18 labels).
- Import observation payload joins for runtime/test/history. Incoming-search refs are a `Vec` (duplicates preserved). Target-attribution is keyed by `sourceFactId` (`EVALUATOR_TARGET_ATTRIBUTION_DUPLICATE` on collision).
- Execution deficiencies: only `None` / `source-syntax-invalid` map to `required-cell-unsatisfied`; other unknown causes `EVALUATOR_EXECUTION_CAUSE_UNREGISTERED`.
- `ReconstructedInputs` is opaque: private fields, getters only, no constructor. Raw `blobs` adapter omitted; future scanners read named retained bytes. Nested owners/globs/reader visits use separate local budgets, not aggregate Plan CPU.

## Independent reproductions

Portable `check-reconstruction.py` with CPython **3.12.13** `-I -B -X int_max_str_digits=0` (UCD 15.0.0) and cargo **1.95.0**, fresh `--output` under this review tree: **271** product pins, **159** reference pins, **18** original + **23** extra owner rederives, **78** retained reference comparisons, **9** structural controls, **87** durable cases, **324** pure population helpers (not full admission), **139** workspace tests with one injected private probe, exit **0**. Result byte-equal frozen `evidence/portable/result.json` (`c31a58516e8d4a17edbdecf271fb37afc1bc130acccfb1b66f1ff82385a2928a`).

Clean-product **clippy** `-D warnings` **0**, **fmt --check** **0**. **Workspace tests** **138** (137 named + 1 compile-fail doctest), including `reconstructs_retained_evaluator_inputs_without_run_outputs`. Isolation host **151** sources pin-equal product, **23** archives; isolation tests **137+1**. Provider **26/19** receipt byte-identical to the fresh runtime23 build (`11777b96…`); no new provider build.

Durable **87** = **55** reference49 retained (73 minus 18 named-only) + **21** extra + **2** observation + **9** controls. Extra-check still contains two historically labeled mismatch rows that are actually matching co-mutated positives; the permanent fixture keeps those as value cases and isolates the two true observation mismatches (`window`, `selection`) separately. Historical reader-check 18-case named-only failure is preserved and is not a retained ADMIT.

## requiredFindings

None.

## Limits

Not runtime24, not live write, not atom truth, not complete evaluator composition, not Run replay, not custody, not M6. Eighteen named-only stage controls are map-projection only. 324 population cases are synthetic helpers. Future findings need a new source version. Formal runtime24 review is required before installation.
