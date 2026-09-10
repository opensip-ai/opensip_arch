# Blind consumer10 failure assessment

**Standing.** Actual Grok, known main coauthor session. Bounded read-only diagnosis. This is **not** a fresh blind review, **not** independent design ACCEPT, **not** application ACCEPT, and **not** implementation authorization. No feedback has been supplied to the blind origin. No graphs were repaired. Source23 was not edited.

**Verdict: `CONSUMER_CLAIM_REFUSED`.** The continuation’s `ACCEPT-RECONSTRUCTABLE` is refused. Root `rootBlindAssent` remains false. Independent Grok design ACCEPT of frozen23 (`reviews/grok-independent-design.v23`, session `01a082bd-172b-7f73-a896-33f7899338c3`) is a separate fact and does not validate these graphs or authorize application.

All six claimed complete positives fail actual source23 `open_run_closure` **before** `close_run`. Semantic replay was not reached. Consumer self-consistency (`schemaErrors=[]`, `replayMatch=true`, reminted C-byte equality) is not owner admission.

## Classification of the three first failures

| First owner refusal | Graphs | (a) importer misread? | (b) omitted kit law? | (c) recipe absent/contradictory? | Kind |
|---|---|---|---|---|---|
| `x-opensip-order` `canonical-set` on `subject-scope.subjects` | `rust-complete-lib-bin` | no | **yes** | no | ordinary consumer helper bug |
| `NATIVE_UNIVERSE_PATH_NOT_INVENTORIED:alpha` | `rust-complete-lib-only`, `rust-partial-lib-bin` | no | **yes** | no | ordinary consumer graph-construction bug |
| `FACT_ANCHOR_CARDINALITY:file:inventory:expected=0:declared=1` | `syntax-json`, `syntax-typescript`, `ts-ordinary` | no | **yes** | no | ordinary consumer helper bug |

No first failure is a design gap. No first failure is an importer misinterpretation.

## (a) is false: the exported frames contain the named faults

Root `checker.py` loads **only** `/tmp/opensip-design-corrections/candidate-subject.v23/docs/coop/design-corrections/foundation/identity-model.v3.py` (SHA-256 `e3fe8e5a103d68c90c21904a0a4ed1d557c02d10fb066c82854cd092896076fd`, matching `report.json` `sourceSha256`). It reconstructs objects/blobs from exported `opensip.product.v1\0` frames, asserts digest and typed-id match, then calls `open_run_closure` then `close_run`. It does not import consumer builders or author fixtures and does not repair bytes.

This assessment independently decoded the six `.store.json` files **without** importing consumer code or the owner. Store SHA-256 values match `report.json` exactly. The failing values are in the exported descriptors:

| Graph | storeSha256 | Exported first-failure evidence | Also present, not yet reached |
|---|---|---|---|
| `rust-complete-lib-bin` | `6ac3e6c9…` | clones `subjects` = `['alpha/src/lib.rs', 'alpha/src/bin.rs', 'alpha/src/shared.rs']` | `crateRootPaths` = `['alpha','beta','crates/foo#bar']` (none inventoried); 10 file facts with 1 anchor |
| `rust-complete-lib-only` | `8e2d6e93…` | `crateRootPaths` includes `alpha`; inventory has `alpha/src/lib.rs` but not `alpha`; clones subjects `['alpha/src/lib.rs']` (sorted) | 10 file facts with 1 anchor |
| `rust-partial-lib-bin` | `b8629146…` | same `crateRootPaths`; clones subjects `[]` | 10 file facts with 1 anchor |
| `syntax-json` | `a28e066f…` | 2 file facts, each `len(anchors)=1` | — |
| `syntax-typescript` | `cfeaa61f…` | 2 file facts, each 1 anchor; 1 clone fact with 1 anchor (lawful for clones) | — |
| `ts-ordinary` | `1273c2ba…` | 5 file facts, each 1 anchor; clones subjects `['src/index.ts','src/util.ts']` happen to be C-sorted | — |

Canonical-set / UTF-8 order of the mixed clones list is `bin.rs`, `lib.rs`, `shared.rs`. The exported order is `lib.rs`, `bin.rs`, `shared.rs`.

## Failure 1 — unsorted `Scope.subjects` (b)

**Selector.** `foundation/identity-schemas.v3.json#/$defs/subject-scope/properties/subjects`

**Meaning.** `subjects` is a unique string array annotated `"x-opensip-order": "canonical-set"`. Identity-and-evidence states that `canonical-set` is strict ascending canonical item bytes; `uniqueItems` neither selects nor overrides order; C never sorts. `foundation/canonical.py` `exact_order` keys each item with `canonical(v)` and refuses unless `keys == sorted(keys)` and unique. Owner `validate_registered_record` uses `ExactValidator`, which extends Draft 2020-12 with that keyword.

**What the consumer did.** `graphs_lang.py` sets `clone_subjects = ["alpha/src/lib.rs", "alpha/src/bin.rs", "alpha/src/shared.rs"]` and writes that list onto the clones `subject-scope`. File-scope subjects **are** `sort_utf8(...)`. `codec.sort_canonical_set` exists and is used for other collections (capability requests). The unsorted clones array is an ordinary omitted sort, not a missing recipe.

**Own validator.** `recon/schema_val.py` is stock `Draft202012Validator`. Measured here: that validator reports **0** errors on the unsorted list. Source23 `ExactValidator` refuses it with `ValidationError: array order canonical-set: strict unique order required` and admits the C-sorted permutation. Consumer `schemaErrors=[]` is therefore expected and is not owner admission.

First-failure discipline: if this array were sorted, the same export would still refuse `crateRootPaths` and then file-anchor cardinality.

## Failure 2 — native universe path `alpha` not inventoried (b)

**Selectors.**

- `foundation/identity-schemas.v3.json#/x-opensip-digest-domains/domainSets/native-semantic-universe/native.semantic-universe.rust.v2/snapshotJoins[0]` — `path: ["crateRootPaths"]`, `form: "inventoried-paths"`.
- Same document `#/x-opensip-digest-domains/domainSetLabels/native-semantic-universe` = `NATIVE_UNIVERSE`.
- `native/native-evidence.schemas.v2.json#/$defs/RustUniverseV2ResolvedInputs/properties/crateRootPaths` — unique path strings, `x-opensip-order: utf8`. Schema admits the strings; inventory membership is the domain-registry join.
- `docs/v2/contracts/product-v1/native-evidence.md` §2.1: `crateRootPaths` are “sorted unique canonical paths; every path must be in the analysed snapshot inventory.” `bind_rust_universe` refuses “a `crateRootPaths` entry not inventoried.”
- `identity-model.v3.py` `snapshot_joins`: for `inventoried-paths`, each named path must be a key of `snapshot.sourceInventory` or `NATIVE_UNIVERSE_PATH_NOT_INVENTORIED:<path>`.

**What the consumer did.** `graphs_lang.py` sets `"crateRootPaths": sort_utf8(["alpha", "beta", "crates/foo#bar"])`. Those strings are package directory names, reused as `memberPackageRoots`. Snapshot inventory is **files**: `alpha/src/lib.rs`, `alpha/Cargo.toml`, `beta/src/lib.rs`, `crates/foo#bar/src/lib.rs`, … — not `alpha`. UTF-8 order of the array is fine; the join fails on the first missing path, `alpha`.

**Why not (c).** The field name does not contradict the join. Snapshot inventory cannot contain directories. The kit’s published positive uses `crateRootPaths: ['src/lib.rs']`. The published negative `crateRootPaths: ['src/absent.rs']` refuses `NATIVE_UNIVERSE_PATH_NOT_INVENTORIED:src/absent.rs`. The recipe is present and executable. Treating crate roots as uninventoried directory strings is a consumer construction bug.

Own validator never runs `snapshotJoins`. `replay.py` joins file payload path/hash/length and native-context retention; it does not test `crateRootPaths` against inventory.

## Failure 3 — file facts declare 1 anchor; inventory law requires 0 (b)

**Selectors.**

- `foundation/relation-payload-schemas.v2.json#/x-opensip-relation-registry/anchorLaw/classes/inventory` — members `file`, `package`, `vcs-change`; cardinality **exactly 0**. An inventory fact is not read from a source span; its payload is already bound by `snapshotJoins`. An anchor is a free axis that gives one semantic input several spellings (`FACT_ANCHOR_CARDINALITY`).
- Same registry `relations/file/anchorLaw` — `class: inventory`, `cardinality: 0`. Enforced at retained Run closure **before** snapshot joins.
- `foundation/identity-schemas.v3.json#/$defs/fact/properties/anchors` — required array, `maxItems` 100000, `uniqueItems`, **no `minItems`**. Stock schema therefore admits both 0 and 1. Cardinality is the relation-registry law, not identity-schema `minItems`.
- `identity-model.v3.py` `anchor_law`: `expected=0:declared=1` for inventory.

Clones remain `body-identity` cardinality **exactly 1**. The consumer’s clone facts with one anchor match that law. First refusal on TS/syntax graphs is the **file** class.

**What the consumer did.** `graphs.py` and `graphs_lang.py` always attach

```text
"anchors": [{"path": p, "blobDigest": sha256(d), "startByte": 0, "endByte": len(d)}]
```

on every `file` fact. That is the exact second spelling the registry closed.

**Own validator / joins.** `schema_val.py` does not read `anchorLaw`. `replay.py` for `relation=="file"`:

- requires payload path in inventory and matching digest/length;
- if `anchors` is nonempty, checks `anchors[0].blobDigest == contentSha256`;
- **never** requires cardinality 0;
- increments `fileFactsJoined` on the forbidden spelling.

So `closureJoins.ok=true` and `fileFactsJoined: 5|10` are measurements of the inverted helper, not of owner inventory law. Clone cardinality `==1` in the same helper is the one fragment that matches the kit.

## Own validator vs owner (summary)

| Law | Owner | Consumer `schema_val.py` / `replay.py` |
|---|---|---|
| `x-opensip-order` `canonical-set` | `ExactValidator` keyword; refuses unsorted `subjects` | ignored; `schemaErrors=[]` |
| `crateRootPaths` inventoried-paths | `snapshot_joins` in `open_run_closure` | not implemented |
| file `anchorLaw` cardinality 0 | `anchor_law` before snapshot joins | not implemented; file helper **allows/rewards** 1 matching anchor |
| clones cardinality 1 | `anchor_law` + bodyIdentityJoin mirror | `replay.py` requires `len(anchors)==1` |
| semantic replay | `close_run` after admission | remint of consumer evaluator C bytes vs the claim it just minted |

Charter: “Semantic proof replay is a separate REQUIRED step **after** identity/schema/closure admission.” A linkage-valid self-remint that never passed owner closure is not a complete positive. Verdict/count/C-byte self-consistency is not admission.

## Charter items that independently preclude ACCEPT

Charter: “Do not return an accepting verdict while required reconstruction remains unexecuted or its complete positive controls fail.”

Two independent grounds, each sufficient:

1. **Complete positives failed.** Owner refused 6/6 at `open_run_closure`. `close_run` was not reached.
2. **Required reconstructions remain unexecuted**, listed by the consumer in `limitationsUnexecuted`, while `newMustIssues` / `newShouldIssues` are empty and the verdict is `ACCEPT-RECONSTRUCTABLE`.

| Unexecuted item | Kit recipe present? | Class | Precludes ACCEPT? |
|---|---|---|---|
| js-synthesized / custom-named / repeated-base tsconfig as **complete Runs** (executed only as a config-graph identity vector) | yes | (b) reconstruction omitted | yes |
| JavaScript clone body as a **sealed fact** under the TS universe (executed only as a body-identity vector) | yes | (b) | yes |
| imported-observation Run | yes (`imported-evidence.schema.json`, import-source-context) | (b) | yes |
| `sufficiency_v2` for resolved five-pair rungs; consumer says this is incomplete implementation, not a missing recipe | yes (`atom-evaluation-contract.v1.md`) | (b) | yes |
| `IncomingSearchV1` / `TargetAttributionV1` as graph members | yes (those two schema files are in the 79-file kit) | (b) | yes |
| Baseline E0 vs E1–E3, repair-apply, native-prepare as sealed Runs (keys/envelopes only) | yes | (b) | yes |

**Excluded as future qualification, as the charter requires:** `admit_native_context` compiler/cargo/provider execution; real OS/crypto/SQLite measurement. Synthetic TCB observations are not native enforcement proof.

**Not an unexecuted requirement:** L1 clone identity is retained framed-payload custody, not host-recomputed tokenisation. That is the design.

Helper bugs the consumer **did** list (`HB-LOGICAL-SUMMARY-REPLAY`, `HB-NODE-MODULES-INVENTORY`, …) are ordinary implementation bugs. They are not an admission of the three first failures above, which the report never named.

## What this is not

- Not a design-gap finding against frozen23 for these first failures.
- Not a finding that root mis-imported consumer bytes.
- Not permission to repair these graphs with author knowledge and call the result blind.
- Not application bind/assemble/activation.
- Not a re-opening of independent design ACCEPT of `652c800166a8d3f37eacfbf273c9786bb84f6fd6b5c6ead57b5a254315859a25`.

## Minimal remediation

1. Leave this continuation’s graphs and public report as evidence. Do not patch them from an author oracle.
2. Do not edit source23. The omitted laws are already in the allowed kit.
3. Keep `rootBlindAssent=false`. Do not treat `ACCEPT-RECONSTRUCTABLE` as a gate.
4. A **new independent origin** (not a same-origin continuation of consumer-b.v10) must:
   - implement `x-opensip-order` (`canonical-set` / `utf8` / the closed vocabulary) before claiming `schemaErrors=[]`;
   - sort every `subject-scope.subjects` array, including clones, as a canonical-set;
   - emit `file` / `package` / `vcs-change` facts with `anchors: []`;
   - put **inventoried file paths** in `crateRootPaths` (e.g. `alpha/src/lib.rs`, `beta/src/lib.rs`, `crates/foo#bar/src/lib.rs`), not directory names;
   - run owner-equivalent `open_run_closure` then `close_run` on **exported frames** before semantic replay;
   - either mint the remaining charter sealed Runs or return a non-accepting verdict while they remain unexecuted.

## Honest next independent-consumer review scope

- **Origin:** new independent session. Do not resume consumer-b.v10 or this continuation. Do not use these graphs as a template.
- **Kit:** the same normative-only 79-file kit (or the current frozen kit if the subject is unchanged). No author fixtures, goldens, or this assessment as an expected-output oracle.
- **Admission bar:** every claimed complete positive must survive independent import of exact exported frames through actual `identity-model.v3` `open_run_closure` then `close_run` (or a fully independent implementation of the same keywords, `anchorLaw`, `snapshotJoins`, and evaluator replay). Consumer remint of its own C bytes is not that bar.
- **Required sealed work:** ordinary TypeScript (node_modules as read-set, not inventory); mixed-edition Rust with inventoried crate roots, canonical-set subjects, partial-ownership pairing, lib-only complete-empty clones; syntax code and data/document Runs; JS clone body as a sealed TS-universe fact; synthesized and custom-named config as complete Runs; at least one imported-observation Run; resolved-rung sufficiency / incoming-attribution where claimed, or an honest non-accept; baseline E0 vs E1–E3 and repair-apply as sealed graphs or an honest non-accept.
- **Out of scope:** OS/compiler/cargo/crypto/SQLite qualification; application bind/assemble/activation; source23 edits; relabeling a repaired same-origin tree as fresh blind.

## Priority next steps

1. Keep root refusal. Do not feed consumer10 ACCEPT into application tooling.
2. Launch a new independent-origin consumer against the same kit, with owner-import of exported frames as the admission bar and the charter rule against accepting while reconstruction is unexecuted.
3. If that consumer is briefed at all, name the three kit laws (canonical-set subjects; inventory anchors at 0; `crateRootPaths` inventoried-paths) without supplying repaired graph bytes from this continuation.
4. Keep independent design ACCEPT of frozen23 separate from any later consumer result.

## Limits

- Did not read raw CLI reasoning, thought, or `response.raw.json`.
- Did not re-execute consumer `main.py` / `recompute.py`.
- Did not call `close_run`; owner never reached semantic replay. Masked-later defects are observed in exported bytes, not owner-replayed.
- Did not exhaust every possible later owner refusal beyond the two additional laws visible in the same frames.
- Did not re-grade core design.
- On-disk kit tree has 80 files including `consumer-input-manifest.json`; the manifest lists 79 hashed subject files. The consumer’s `fileCount: 79` is that list.
- This document is coauthor diagnosis, not a substitute for a new blind consumer.
