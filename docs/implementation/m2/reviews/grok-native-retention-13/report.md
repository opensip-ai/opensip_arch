# Independent Grok advisory: native-retention-13

**Reviewer:** Grok (explicitly authorized). Root remains lead. Not Claude agreement.
**Kind:** Frozen-trial advisory. **Not runtime selection. Not ACCEPT-DESIGN-UNIT. Not inventory install. Not Plan/full Run/security/replay.**
**Fresh-blind:** **no.** Prior bounded editable advisory (`m2-grok-native-retention-boundary-01`) is not acceptance; item-2 kind/`visit` correction is already on that tree.
**Work tree:** `/tmp/opensip-implementation/m2-grok-native-retention-review-13/review`. Live, frozen, and history were not edited.

## Custody

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `subject.json` | 45461 | `72230f77a0ee0e4bb8b3ce58223ba13c757bf104303ad303275faafcca9eb2a6` |
| `subject.tar.gz` | 2704902 | `6f466c054d4ff7fbd2a9c2e16cd6717977c91ff2f9b3a043ab64805115ce59c0` |
| Files | 252 | 0 missing / 0 mismatch |
| `native_universe.rs` | 44549 | `a3bd2f5f…9269` (byte-identical to the pre-freeze editable trial) |
| identity-v3 / native-v2 | 197480 / 280357 | `311c1feb…` / `e5834d37…` |
| selected I / N | 158555 / 319944 | `619d6e3c…` / `e6784aa1…` |
| `Cargo.lock` / identity `closure.rs` / TCB policy | — | **unchanged vs 09/v2** |

Export `/tmp/opensip-implementation/m2-native-retention-subject-13` matches. Copied lock **9/15**. Live product is native-runtime **v3 / inventory 13** and does **not** contain this file. `native_universe.rs` / `native_retention.rs` are **not** in inventory-12. Planned 14 (split `native_retention.rs` + Plan owner) is **not** this freeze.

## Scope (what this freeze is)

`inspect_native_retention(inputs, digest, set, snapshot_id, budget)` rehashes an explicit snapshot, then walks one registered native root: snapshotJoins, nested **raw** canonical vs nested **H**, blobJoins with declared `lengthField`, closure **kind then** manifest/tree bytes. Universe roots also retain the named context and run actual `N.bind_*`. Context roots run `inspect_native_context`. Nested roots follow metadata only. Private `{frames,blobs,closures}` never mean every snapshot blob, Plan, custody, execution, or replay. General identity-walker native joins stay `Unsupported("payload-class owner joins")`.

Budget: `steps` = frame/closure/blob visits and registry-path expansions; `depth` = nested frames; `descriptor_work` = each schema call (copied, not a global Run/CPU clock). `steps=0`/`depth=0` is `Limit` before the walk.

Owners are **not** skipped by join-walk memo: context/universe owners still run; closure **kind is checked on every join** (selected `admit_frame` ~1629–1631 `get`+kind **then** `visit`). That matches Rust. The prior editable item-2 claim that `visit` memo hid kind is **wrong**; this freeze’s oracle extracts actual `admit_frame`, so it already uses the correct gate.

## Oracle (not full `open_run_closure`)

`oracle-scope-account.json` + `check_native_retention13.py`: AST extracts **six** nested functions from selected `open_run_closure` — `get`, `blob`, `canonical_bytes`, `snapshot_joins`, `path_values`, `admit_frame`. `visit` is an **explicit closure-only shim** (actual `get`; manifest/tree hashes; generic blob length; per-closure walk memo). Universe roots: after `admit_frame`, admit named context, then **actual** selected `e678` bind with merged retained/snapshot. Not full Run.

**Preserved fixture mistake:** `oracle.stderr` — `golden-nested-typescript-native.source-unit-ownership.v1` asserted checked, but extra unselected Rust nested records on a TS snapshot correctly **invalid**. Label changed to `nested-root-…`; **no runtime fix**. Historical **286**-case `corrected-oracle.stdout` retained; final corpus is **304**.

Expanded controls in the 304: rekeyed closure member length, dual-kind same closure id, noncanonical TS graph, binder-after-retention cfg refusal, lockfile snapshot digest, depth 1/2, unrelated extra blob, nested `lengthField` rekey, missing/corrupt every supplied blob.

## Independent reproduction

Trusted rustc/cargo **1.95.0** `--offline`. Did not rerun 07–12 giant corpora.

| Check | Result |
| --- | --- |
| 252-file pin + archive | match |
| AST six names in `open_run_closure` | present; `visit` nested but **not** extracted |
| `cargo test --workspace --all-targets` | **97** |
| compile-fail doctest | **1** → **98** |
| Clippy `-D warnings` | 0 |
| harness replay | **304** lines, 150 checked / 71 invalid / 67 unavailable / 16 limit, **0 mismatch**, byte-identical to prior actual |
| independent negatives | **ALL_PASS** |

Independent negatives: syntax-universe golden counts (2 frames, 1 closure); extra blob does not change counts; **context owner empty refusals when grammar tree bytes are missing**, retention `MissingBlob`; corrupt `BlobDigest`; `steps=1` and `steps=0` are `Limit`.

Host test `native_retention_requires_member_bytes_beyond_context_descriptors` is the same “descriptor can pass, retention must fail” claim.

## Findings

**Required:** none relative to the trial’s stated private-candidate standing.

**Should-fix:** none for this freeze. Splitting `native_retention.rs` and adding a Plan owner is **14**, not 13.

**Not findings**

- Kind-before-`visit` is selected reference behavior; freeze README/account already state it; prior advisory item 2 is a corrected historical error, not a product defect.
- Incorrect `golden-nested-…` assertion is fixture-label history, not a hidden runtime patch.
- Counts are not full closure of the snapshot.
- Live v3 lock does not install this slice.

## Limits

- Advisory only. Not acceptance of 13, 12, runtime-v3, native ADMIT, M2, or release.
- Did not execute `close_run`, Plan owner, metadata-security, compiler execution, or identity-walker native joins.
- Did not rerun 07–12 giant corpora.
- Additive inventory (and planned 14 file split) still required before install. Root remains lead.

**Verdict: NOT ACCEPTANCE.** Prototype matches its standing.
