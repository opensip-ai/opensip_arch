# Frozen trial review: full-walk-32

**Reviewer:** Grok. Root remains lead. Not Claude agreement.
**Kind:** Scoped source review of private `inspect_retained_walk`. **Not runtime-16. Not layout-24 re-acceptance. Not ReplayedRun, native compiler, publication, or full M2.**
**Work tree:** `/tmp/opensip-implementation/m2-grok-full-walk-source-32-review/review`. Live, frozen, and history not edited. No commits.

Draft critique `/tmp/opensip-implementation/m2-grok-full-walk-draft-32/review` is **not edited here** (`review.md` 25191 / `26ea311738684d0274472b2cd0afb8bf64d982d2a618fdb2432efc3d91246768`, `review.json` 19254 / `370d2171d8517e0bb68516d617db63f6ffeee5cc86e763e8d622c401a41e83cb`) and is **not** source acceptance. wN reconsideration remains separate.

Private inherited lock is `515f092c…b523` / 36241 (**9/15**). Live independently **22 inventory / 31 contract** (`116fefcc033b2b7b2a441c6b55f414b581bada8586a3b3745ec39e0e445514e3` / 66066); last inventory candidate v24; last contract runtime-v15. Live has **no** `full_walk.rs`. Eventual runtime must compose **exact current live**, not this 9/15 lock. Three local identity sources changed, so runtime-16 **must rebuild** the provider export (no unchanged v10 carry).

## Subject pin

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `docs/implementation/m2/trials/full-walk-32/subject.json` | 97191 | `c52cf367757970cb072e8ae72e6c29fe8b60741719709eafda2cd5a6f464ec96` |
| export | `/tmp/opensip-implementation/m2-full-walk-subject-32` | **508/508** members; 0 extra; 0 missing |

508 paths unique and string-sorted. Adjacent gzip pin `a4fd601f…9f3e` / 154403601 is preserved privately (`packaging-correction.json`); this review verified the **subject file set**, not a GitHub-sized gzip in-tree.

Dependency pins hash-match: SOURCE-29 `9ea476e4…219a`; I `7b6750a9…0da2`; W 60dc `60dc11e2…b180`; inventory-24 unit `57252119…6067`; seam-31 advisory `871b9979…131f`; canonical-walk-33 advisory `e4944999…005f`.

## Source delta vs frozen 29

**243** product files byte-identical, including `Cargo.lock`, identity/evaluator Cargo.toml, and prior native/import-joins/import-payload fixtures. External TCB tuples unchanged.

**8** changed: `full_walk` wiring (`lib.rs`, `native_retention.rs`, `run_links.rs`), host tests, **three identity sources** (`closure.rs`, `lib.rs`, `relations.rs`), identity-policy pin file. **2** new: `full_walk.rs` (**13104** / `01dd5478c6fbd4f6f1c2248a35fbc15905ecc01808ad610f663655d77a666f54`), `full-walk-fixtures.json` (**3888036** / `bbec4505…9219`) under 4 MiB.

Preserved failure corpora in-subject: insertion-order oracle (2 shared class mismatches), wrong workflow wrapper, incomplete-rekey fixtures.

## Authority path (draft finding not adopted)

Draft `public-with-owner-deferred-ok` asked for `pub(crate) inspect_structure_with_owner`. That **cannot compile**: the walker lives in `opensip-identity`; `inspect_retained_walk` lives in `opensip-evaluator`. Cross-crate `pub(crate)` would hide the seam the evaluator must call.

Independently:

- Default `inspect_identity_record` / `inspect_current_record` / `inspect_local_structure` still construct **private `RejectOwner`**. `default-walk` host control still gets `Unsupported("capability derivation")`.
- Public `inspect_structure_with_owner` returns **`StructuralChecks` counts only**. Trait docs: callbacks cannot mint a Run, complete evaluator result, or replay. It is not the complete composition.
- Public **`inspect_retained_walk`** always allocates **private `ClosedOwner`**, then mandatory post-walk: run-links (walk-derived caps) → plan-native (derived frames) → `UNIVERSE_FRAME_UNRETAINED` → policy → stage specs → evidence roots → predicate witnesses → per-view joins → import joins. No caller owner/registry/census/ADMIT argument.

A custom `StructuralOwner` plus with-owner is a **diagnostic** walk, not semantic admission. Remaining issue is **not** substantiated as a required source defect. Do not treat the draft action as this unit’s gate.

## Law (order, resources, provenance)

Walk: source/Plan joins on object visit; payload decode before class; import uses import-descriptor identity + two-key registry; relation **prefix (ladder/anchors) → syntax → remaining laws/snapshot → body iff the relation row carries `bodyIdentityJoin`**. Native nested recursion uses the row **domain set**. Frames/caps derived from actual traversal. Stage schema / fragment obligations `Ok` only inside this composition’s later owners.

**Three separate limits:** walk steps/depth, owner-invocation count, per-owner local budget. Not one Plan work-unit aggregate.

Comparison domain is **C.parse(C.canonical(v))** / Rust `BTreeMap` (advisory-33). No identity-model successor. Insertion-order first-fault is extra-product.

## Reproduction (rustc 1.95.0, `--locked --offline`)

- Fixture **526** cases (507 reference + 19 local resource/default). Frozen corpus actual vs expected **526/526** after the same class mapping the host test uses (34 checked / 257 unavailable / 219 invalid / 15 limited / 1 unsupported). Host `full_retained_walk_checks_complete_inputs_faults_and_separate_limits` ok.
- Shared canonical-projection suite: **8/8**. Insertion-order oracle still records **2** class mismatches (preserved).
- `cargo test --workspace`: **122** passed. Clippy `-D warnings` Finished. Identity policy `sourceFilesVerified: 110`, same three registry tuples.

Did not re-pipe the 443 MiB request ndjson. Did not treat live 22/31 as this source.

## requiredFindings

None.

## Limits (not required findings)

- Diagnostic `inspect_structure_with_owner` remains public because the evaluator crate must call it; it still does not grant complete composition.
- Provider export **must be rebuilt** in runtime-16 (three identity sources changed).
- Not ReplayedRun, compiler qualification, publication custody, or M2 complete.
- Live 22/31 does not install `full_walk.rs`. Formal runtime composition is later.
- wN reconsideration of the draft is separate and pending.

## Verdict

No required findings. Private `inspect_retained_walk` is a fixed composition over the identity callback seam, uses private `ClosedOwner`, returns diagnostic counts, and matches 526 classified host/corpus cases on the canonical map domain. Not a live/runtime selection.
