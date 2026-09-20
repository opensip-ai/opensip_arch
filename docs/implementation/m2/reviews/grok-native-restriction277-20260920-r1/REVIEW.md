# Independent review — native restriction evidence bindings 277

**Standing:** bounded native-Rust review of frozen `native-restriction-bindings-checkpoint-277`. Conditional recorded restriction evidence, BEFORE history, accepted subject, recovery batch and quorum-context joins on the **same** guarded operation Budget. **Not** list/root envelope authentication, current key population, causal priority, role effects, native custody, selected runtime, authorization, current population, transition/effect proof, 273 prepared-outcome composition, 274 event replay, complete restore/clock/publication proof, historical/current population, non-key subjects, other-root contexts, private-policy merge, artifact/repair/S4/floors, command/role/batch/whole-image effects, fence/census/durability/writers, source selection, or M3–M6. Archived 276 (`500512a7…226c`) was not edited. Installed product remains `fa72e50`.

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Rust 1.95.0 `--offline --locked`. Review-local product copy only. Frozen fixture/key/result directories were not overwritten. Keys are **TEST ONLY**.

---

## Verification

Frozen archive: **5502580 B, 685 members, SHA256 `b0be547b4f6b65a5bc9516dc3bce602abd6fe8b6e15d48dc4140a0db0b74b921`**. Pin, tar, member count, and every `subject.json` hash matched **before** extract; extract rehashed **685/685**. Product-inputs **411/411** live-equal.

Nested parent 276 pin `3e4d5bf5…ffa9` (5389288 B / 682 / 409 files) equals the reviewed 276 freeze; live trial tar still matches; `trust-before.rs` equals that 276 `trust.rs`. Nested 265 `73c3b3f5…86df`. Nested 230 r3 helper `99288ae0…3c00` (66388 B / 38). Schema `1328ba16…4208`. `Cargo.lock` unchanged vs 276. Inherited 276/275 fixtures byte-identical. `lib.rs` unchanged.

Product vs 276: **411** files, **407** unchanged, **2** changed (`trust.rs` `53d39a5a…7bbc` — private `trust_input_bindings` restriction join plus tests; `trust_record_shapes.rs` `ed9ebaeefe…e972` — `loose_version` visibility `fn` → `pub(super)` only), **2** added (`restriction277.ndjson`, `restriction277-shapes.ndjson`). No public API.

---

## What 277 adds

Still a private module: `trust_input_bindings` is not in `lib.rs`. Closed `Input` now also routes Root, History, and Batch. Full `EventRef`/`NodeRef` is admitted **before** `{sha256,bytes}` projection for nodes; closed `BlobRef` bodies load from **Objects**. Every `Budget.load` charges; owner errors latch `budget.scope`.

**Restriction** (`restriction(budget, observation, store)`): 270 `RestrictionObservationInputV1` shape; loads actual `RestrictionEvidence` and BEFORE capsule. Exact `purpose`/`store`/`beforeClock`. BEGIN is the role's RECOVERY ceremony batch, or null; an actual `BeginBatch` must select that role. Revocation requires an established role, exact `acceptedUnder` root admission, exact BEFORE history, and either a namespace held by that role **or** INDEX `snapshotVersion` read from the actual OLD accepted catalog **body**. The claimed list node must be reachable in BEFORE history; its actual list body must contain the exact `subjectKind`/`subject` pair. Quorum loads the actual `RootAdmissionNode`: current context requires no recovery batch and exact accepted-head admission/binding; prospective context binds the actual batch replacement. History remains exact. `RestrictionBound` owns observation/evidence/before-image/inputs after store/Budget drop.

History traversal is iterative, SHA-seen, last parent first. Target **full reference equality** short-circuits **before** its one later load. This is targeted reachability with this owner's edge charges, not full 272 dependency traversal. **No** lifetime-64 cutoff.

**Bodies** use **product** canonical JSON (`parse_json` + exact `canonical_bytes` equality): 4MiB / depth 32 / product integers / **no NFC**. Catalog `schema_only` is prefix **plus** complete loose-version grammar (one final LF stripped) and a closed typed constraint (`min`/`max`/`includeMin`/`includeMax` with exact booleans). It does **not** invent calendar/current-time, unique-release, strict SemVer/interval, or NFC checks. Revocation schema-only likewise uses lexical timestamps. Authenticated `validate` / `revocation_shape` retain stricter calendar/semantic owners; inherited tests still run.

Initial author `schema_only` was prefix-only (`trust-before-schema-completion.rs`). The primary-schema corpus caught invalid version/constraint acceptance; the first fix used `crate::trust_record_shapes::loose_version` and did not compile (`trust-before-schema-module-path.rs`); current path is `crate::trust::trust_record_shapes::loose_version`. Production `loose_version` body is otherwise unchanged vs 276.

This helper does **not** call 273 `bind_descriptor_raw` or 274 event replay.

---

## Reproduction vs inspection

| Kind | Corpus | Result |
|---|---|---|
| Exact live | `cargo test -p opensip-security` | **218/218** |
| Exact live | `cargo test --workspace` | **517** passed (515 tests + 2 doctests) |
| Exact live | workspace Clippy `--all-targets -D warnings` | **pass** |
| Exact live | `cargo fmt --all --check` | **pass** |
| Exact live | 30 compiled r2 controls + baseline | **31/31**; core fields/patches/source SHA-equal frozen `mutation-check-r2` |
| Exact live | Python source/fixture probes | **45/45** |
| Inspected | 101 restriction rows / 43 positive | 37 `original-N`; 30 base/repeat/exact/one-short; 20 coherent body cases; 14 history/role (300-chain, six roles, same-SHA wrong length) |
| Inspected | 1278 primary body-shape rows / 113 positive | catalog 1020 / revocation 258; inherited **340** `267-` catalog values re-evaluated under schema-only (26 of those still valid) |
| Inspected | original 230 helper 195 checks | r1 fixture report `originalChecks` length **195**; traces only `join_restriction` (37 calls → 67/20 before body/history augment). Remaining owners are **reference coverage**. Not rerun here. |

**Controls (honest):**

Wrong admission (`left: true` / `right: false`): omit revocation-fact-absent, quorum-context, quorum-context-root, quorum-prospective-root, quorum-history-head; fact-matches-subject-only; fact-matches-kind-only; omit-catalog-version-constraint-schema.

First fail **other** assertions (not exploit proofs):

- `omit-evidence-purpose` / `store` / `before-clock` / `begin-binding` / `begin-role` / `revocation-accepted-under` / `revocation-history-head` / `revocation-subject-not-held` / `list-node-not-in-before-history` / `omit-noncanonical`: extra captures (e.g. original-13 **5 vs 2**; original-2 **6 vs 3**; catalog-noncanonical **6 vs 3**). Node loads always use Records; omitted guards can therefore capture before a later reason.
- `omit-revocation-never-established` / `omit-quorum-no-accepted-root` / `omit-accepted-catalog-shape`: panic `closed shape checked`.
- `omit-list-node-kind` / `omit-revocation-list-shape`: panic missing field.
- `omit-owned-body`: lost loaded-input facts (`original-0`).
- `target-compares-only-hash`: capture count **4 vs 5** on `target-same-sha-wrong-length` (not `left: true` / `right: false`).
- `reset-operation-budget`: `original-0` counters **(0,0,0) vs (5,5,4949)**.
- `history-lifetime-64`: over-refusal of valid `history-300-list-chain` (`invented-history-limit`).
- `omit-failure-latch`: follow-up call is not `BudgetError::Closed`.
- `authenticated-revocation-calendar`: over-refusal of `revocation-lexical-impossible-date`.
- `authenticated-catalog-instead-of-shape`: over-refusal of valid schema-only `267-calendar-issued`.

Frozen `mutation-check-r1`/`r2` were not overwritten. r2 baseline `sourceSha256` is current `trust.rs` `53d39a5a…7bbc`.

---

## Focused findings

### Same Budget and schema-before-body

Restriction, history reachability, catalog/revocation bodies, and nested BEGIN/root loads share one `budget.scope`. Nodes: `EventRef`/`NodeRef` shape, then physical `{sha256,bytes}`, then `Budget.load` on Records (or Events). Bodies: `BlobRef` shape, then Objects load, then product canonical equality, **then** `schema_only` / `revocation_schema_shape`. Store fixtures use actual typed collections from the original trace; unloaded unreachable raw is Records-only.

### Product JSON vs authenticated owners

Historical bodies admit under product JSON, not signed metadata (no NFC, product integers). Schema-only catalog **permits** lexical impossible calendar (`267-calendar-issued`, `catalog-lexical-impossible-date`), duplicate releases, loose version including a final LF (`catalog-lexical-version-'1.0.0\n'`), reversed interval, and non-NFC display. Authenticated `validate` still does calendar, unique-release, and SemVer/interval. `omit-catalog-version-constraint-schema` (prefix-only) is a **wrong admission** — the same gap the 217-pass/1-fail corpus caught.

### r1 hash-only target comparison

r1 `target-compares-only-hash` **escaped** (`expectedOutcome` false, exit 0): no case varied target **length** while keeping SHA. r2 added `target-same-sha-wrong-length` and `history-300-list-chain`. Live r2 replay catches the hash-only mutant by capture count **4 vs 5**, not by a boolean wrong-admission. `history-lifetime-64` is an over-refusal of the valid 300-chain, not an exploit. Production reachability still uses full reference equality and has no 64 cutoff.

---

## Independent probes

| Probe | Result |
|---|---|
| Public API | `trust_input_bindings` not exported from `lib.rs` |
| Grammar visibility | 276 `fn loose_version` → 277 `pub(super) fn loose_version`; body otherwise identical |
| Schema-only | prefix + loose_version (LF stripped) + closed bool constraint; no `timestamp_seconds` |
| Wrong module path | beforeimage `crate::trust_record_shapes::loose_version`; current `crate::trust::trust_record_shapes::loose_version` |
| BEGIN | `ST-RECOVERY` ceremony batch; selected role |
| INDEX snapshot | subject equals actual OLD catalog `snapshotVersion` |
| History | full ref equality before load; SHA-seen; no lifetime 64 |
| Subject pair | both `subjectKind` and `subject` |
| Current vs prospective | no batch + accepted head vs batch `replacement` |
| Corpus | 101/43 and 1278/113 asserted in tests and counted in fixtures |
| Six roles | namespace + current-quorum rows for all six |
| r1 vs r2 | hash-only escaped r1; r2 31/31, 8 wrong / 22 other-first |
| 273/274 | restriction helper does not call them |

---

## Remaining (do not count closed)

Full restore proof + optional prepared outcome + literal event composition; complete clock/publication/accepted-role effects/base selection; current/historical populations/nonkeys/other roots/private-policy merge/artifacts/repair/S4/floors/whole-state effects; native custody/fence/slots/census/durability/writers; runtime/source selection; M3–M6. Structural helper is not authentication, current population, transition, or whole-proof authority. These are private review candidates, not shipped behavior.

---

## Verdict

- [x] Archive/pins/members verified. 411 product files: 407 unchanged vs 276. Nested 276/265/230 pins match live trial archives.
- [x] **218** security tests, **515+2** workspace tests, Clippy, and fmt reproduced. Thirty compiled r2 controls behave as documented (eight wrong admissions; twenty-two other-first).
- [x] Same-budget restriction joins; product JSON bodies; schema-only weaker than authenticated owners; full-ref history reachability; r1 hash-only escape repaired by length-varying fixture, caught as capture 4 vs 5.
- [ ] **Not** authentication, current population, transition/effect proof, native custody, census, current authority, or product installation.
