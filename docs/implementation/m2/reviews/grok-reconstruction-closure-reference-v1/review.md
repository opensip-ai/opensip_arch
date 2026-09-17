# Reconstruction-closure reference selection v1 — formal design-unit review

**Verdict: `ACCEPT-DESIGN-UNIT`**

Root remains lead. Not Claude agreement. Not live install. Not SOURCE48 or runtime24. Not full reconstruction, replay, custody, or M2. Root assent and private activation remain required. Selection changes only the design lock; **268** runtime-23 non-lock product files stay byte-identical.

**subjectManifestSha256** `0ce9f36e319659c9d69b916ea88333e79926fbad607f802711278f0547c7d890`  
`docs/implementation/m2/reconstruction-closure-reference-selection-v1-subject.json` **3977** bytes, **17** members (16 candidates + successor), paths sorted unique, **0** pin mismatches.

Successor `docs/implementation/m2/reconstruction-closure-reference-selection-v1/successor.json` **4344** / `54e84aed05f26bdd1f5a8744157be17447f21ec4c0c318e0eb11dae6a2b960d6`. `passageOverrides` is `[]`. Candidates cover the subject minus the record.

## Parents

Live lock **29 inventory / 42 contract** (`84078` / `980a7ed63eb5503e7e7f83c8895066265e0b3ecece063bda5aaf274a9d48fe6c`). Last inventory candidate **v31**. Last contract **runtime23** (`ACCEPTED-DESIGN-UNIT`). This unit is not yet in the lock.

| Parent | Bytes | SHA-256 | Live class |
| --- | ---: | --- | --- |
| selected I `evaluator_input_model.v3.py` | 17578 | `021cc9ac7351f20b82c935d7f5b15760f73fa86afb56f46cdd1520aed4c4ba8b` | currently selected reconstruction helper |
| runtime-23 successor | 17186 | `95bb1d57501fb06bc7bbf6a932fd5fe8f2508a5934471be89d4743997833b6b9` | last contract record |

Parents sorted unique. Architecture I bytes equal evidence `predecessor.py`. Candidate `reference/evaluator_input_model.v3.py` **17561** / `4b2999ca478cdf8959ab031b6cff951aeebe2af0fd659fc529d00a0f2584c769` equals evidence `candidate.py`.

## One-line delta

Exactly one comprehension, line 94:

- before: `closures={key:value for key,(domain,value) in objects.items() if domain=='closure'}`
- after: `closures={key:objects[key][1] for key in plan['semanticClosures']}`

`old.replace(needle, replacement) == candidate`. No other source bytes change. No schema, identity, capture selection, population, count, import, deficiency, sidecar, atom, or composition-law edits. Ambient store census no longer selects the reconstruction scanner map. Transitive native interpreter closures **must remain** in the retained store even when omitted from that map; SOURCE47 already refuses their deletion. Named-only corpus variants are **not** that owner ADMIT.

## Independent portable check

CPython **3.12.13** `-I -B -X int_max_str_digits=0` (UCD 15.0.0), fresh `--output` under this review tree: **159** reference pins extracted and verified, exact one-line patch, **18** original `open_run_closure` owner checks rederived from explicit `ownerRun` fields, **73** before/after results. `result.json` byte-equal frozen `comparison.json` / `expected-result.json` (`1e6681082101704d23b61b7e01bd5dc0d2c4cdfae8ffdebe9dbb486b03b5523b`).

Corpus **73** = 18 original + 18 named-only + 18 ambient-extra + 18 duplicate-inventory + 1 incoming-duplicate. **52** values, **21** refusals (18 `EVALUATOR_ENUMERATION_JOIN:ENUMERATION_INVENTORY_DUPLICATE` + 3 `candidate-forbidden-fact-authority` non-dup variants). **35** value cases differ **only** `normalized.closures` / `evidence.closures` (Plan `semanticClosures` projection). **38** fully unchanged. Incoming-duplicate preserves **2** attestations on both sides. Named-only: `before == after` (map-projection controls on the established owner cache). Duplicate inventories refuse **before** counting; occurrences are not deduped.

Initial checker omitted owner-run descriptors for eight graph builders. That failed portable is preserved: `initial-cases-without-owner-run.ndjson.xz` **145724** / `f523a9f7…`, uncompressed **63336841** / `8fb1ff9a…`. Current corpus **63377648** / `23beaa77…` adds explicit `ownerRun`; before/after results and the source patch are unchanged.

## Advisory / precision (archived, not this unit)

Boundary-48 advisory **1859** / `a4fd19d0…` and md **8270** / `fdf5c839…`. Precision addendum **1920** / `d71921f5…` corrects the doubled-count claim: all 18 duplicate-inventory variants refuse enumeration. Only `None` / `source-syntax-invalid` map to required-cell; other unknown execution causes refuse. Root dispositions **1088** / `908e4e59…` and **1270** / `6e0996b3…`. Fifty-five other no-output retained comparisons against draft Rust 48 are **candidate-only**, not SOURCE48 acceptance.

## requiredFindings

None.

## Limits / not claimed

Not live write. Not SOURCE48, not a runtime unit, not atom truth, not full reconstruction/replay/custody/M2. `atom_inputs.blobs` remains an inert scanner adapter. Formal composition of this helper into a later runtime is a separate review.
