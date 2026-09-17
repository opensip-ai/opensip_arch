# Frozen SOURCE41 review — retained enumeration join

**Reviewer:** Grok. Root remains lead. Not Claude agreement.  
**Kind:** Independent frozen source review of complete Plan-bound enumeration join from retained owner-derived maps. **Not source acceptance. Not runtime-19. Not enumeration-41 product install. Not reconstruct/replay/custody. Not M2 complete. Not fresh-blind.**  
**Work tree:** `/tmp/opensip-implementation/m2-grok-enumeration-join-source-41-review/review` only. Frozen/export/live/history not edited. No commit/push. Future findings need a new source version; do not edit frozen 41. Source 43 parameter prototype is out of scope.

**subjectManifestSha256** `75b752ebda569d1ad94b1cf069d03cd5d412b9d46a18ad1733d8e93c84d49b77`

## Subject pin

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `docs/implementation/m2/trials/enumeration-join-41/subject.json` | 105409 | `75b752eb…49b77` |
| `archive-pin.json` → `subject.tar.xz` | 3394728 | `d097756f1073aac6a800242565c7dd39cfeabb65aac2f30549b50acf2a5a9a16` |
| export | `/tmp/opensip-implementation/m2-enumeration-join-subject-41` | **553/553** members, sorted unique, **0** mismatches, **0** extras |

Product lock in the freeze equals live **25 inventory / 37 contract** (`75079` / `813aa62f39230b654ca6856266d292be6c83eae070f7a2748e6bb9e4e9a5b4ac`). Last inventory: join-inventory **v27**. Last contract: locator-totality reference **v1** (E **50678** / `a02960c6…719d5c`, unit `327d9aec…12f0b` `ACCEPTED-DESIGN-UNIT`). Runtime-18 remains a selected parent. `source-delta.json`: **6** changed + **3** new = **9** owned; **260** non-lock product files; `product-inputs.json` **261** (includes `design-lock.json`).

| Path | Role | Bytes / sha256 |
| --- | --- | ---: |
| `crates/evaluator/src/enumeration_join.rs` | **new** private maps + public `inspect_enumeration_join` | 52825 / `ce09cc82…f49f` |
| `crates/evaluator/src/enumeration-registry.json` | **new** 48-fault law table | 11309 / `deecedc9…8aac` |
| `crates/host/tests/fixtures/enumeration-join-fixtures.json` | **new** 34 retained-boundary cases | 1494335 / `73d1bef0…7933` |
| `crates/evaluator/src/enumeration.rs` | membership/extent/package used by join | 27635 / `e1593cf5…85f3` |
| `crates/evaluator/src/lib.rs` | `pub use inspect_enumeration_join` only | 3074 / `b34b0007…e7ed` |
| `crates/evaluator/src/native_universe.rs` | nested TS/Rust frames (reader41 pin unchanged) | 30186 / `080ae8b7…f2f6` |
| `crates/host/src/native_owner_tests.rs` | public fixture test | 69834 / `a93a7ebc…6964` |
| `crates/identity/src/closure.rs` | identity record shapes | 56835 / `1b66d79a…6aa3` |
| `tools/identity/dependency-policy.json` | identity 8-tuple / 299 sources | 55526 / `b24da61a…5220` |

Evaluator still depends only on `opensip-identity`. Both crates `#![no_std] #![forbid(unsafe_code)]`.

## What the join is

Public `inspect_enumeration_join(inputs, plan_id, evaluation_refs, budget)`:

1. Rechecks each `evaluation_refs` member as `ProofInputRef`.
2. **Derives** the subject-inventory digest list from `domain == "subject-inventory"` (no caller `inventory_refs` argument).
3. `read_inputs` reconstructs Plan/snapshot/analysis/scope/enumeration-plan/membership/contexts/universes/closures/blobs from retained bytes. Universe census is binding-derived, then `inspect_plan_native`. `universe_domains` come from `frame.domain()`, not the caller. `bindResult` / membership-derivation are not API authority.
4. Typed `Err` (`Record` / `Native` / `Retention` / `Plan` / `Limit` / reconstruct `Refused`) **before** a join document exists.
5. After those preconditions, `complete_join` (private) returns the reference ADMIT/REFUSE document. REFUSE has empty index/population/subjects. Standing: `enumeration-join admission only; not a Run`.

`JoinInputs` and `complete_join` are crate-private. The portable checker injects a test-only map harness into a **copy**; frozen `enumeration_join.rs` contains no `cfg(test)` kernel constructor.

Reader41 inventory-ref taint is closed on the public path: digests are filtered from admitted evaluation refs, then INV_SCHEMA + `planId`/`parameterDigest` bind. Empty selection is join `ENUMERATION_INVENTORY_MISSING_RECORD`, not silent ADMIT (`missing-inventory-selection`).

## Law (reader / kernel / cause / order / reconcile / subject3 / native / malformed)

**Kernel vs selected reference42.** Test-only maps compare 1516 typed-list corpus rows; 21 non-list `inventories` containers are unreachable through `Vec<V>` / Rust slice and are explicitly excluded (labels match the freeze). Independent `check-join.py` exit 0, 261 source pins, corpus **18215825** / `f8a3fe77…4faf8b` (1537). Faults are first-seen (`fault` skips duplicates), matching Python `_add`.

**Cause.** Unavailable universe requires inventory `unavailable` and matching binding deficiency/nativeCause (`ENUMERATION_BINDING_CAUSE`). Complete forbids carriers; partial/unavailable require deficiency; `carrier` uses registry `must-be-null` / `required` / `optional` against `enumeration-registry.json`.

**Order.** SCHEMA is recorded at schema failure; MISSING is appended later iff the expected key is in neither `seen` nor `schema_failed`. Host `inventory-false-cell` / `inventory-false-program` are SCHEMA-only (False occupies 0). `inventory-nonobject` is SCHEMA then MISSING.

**Reconcile.** Same population key with distinct row payloads → `ENUMERATION_INVENTORY_RECONCILE`. `JsonValue` equality is typed (no Bool/Integer alias on payloads).

**subject3.** `mint` builds evaluation-subject v3 (`package` adds `packageManifestPath`), `check_identity_value_shape`, `hash_canonical_value`, `subject3:{hex}`. Schema mismatch becomes join `ENUMERATION_ADMISSION_PRECONDITION` (then REFUSE if any fault), not a minted ADMIT.

**Native owner.** Contexts retained as Context frames; universes after plan-native bind. TS `configGraph` / Rust `sourceUnitOwnership` nested; syntax none. Extra `bindResult` on an owner-admitted universe descriptor is defensive `Err(Refused(PRECONDITION))`; public retained packets with `bindResult` fail **earlier** owner schema (`additionalProperties: false`). Host cases `duplicate-snapshot-path-owner-refusal` and `universe-bindresult-owner-refusal` return typed `invalid` `Record(Input(Candidate(Schema(Mismatch))))` and `Plan(Retention(Owner(Frame(Schema(Mismatch)))))`. That matches the archived kernel addendum: those two public-guard lines are unreachable behind closed owner schemas. Map-injection can still emit a PRECONDITION **document** because it skips `object`/`frame_candidate`. That surface is not public authority.

**Malformed locators.** `failed_locator` aliases JSON-C `Bool(false)→0` / `Bool(true)→1` **only** for schema-failed slot tracking; valid rows use typed `locator` (`Integer` only). No `Float` variant exists in `JsonValue`. Array/object locators do not occupy (`Option::None`), so SCHEMA then MISSING — selected reference42 totality. Host False cases are SCHEMA-only, not ADMIT.

**Security / envelope.** Public API cannot be fed caller ADMIT maps, `bindResult`, membership derivation, or universe-domain tables. Test-only `kernel-probe.rs.txt` is not in the crate. Isolation provider remains unavailable by design (three commands expected exit 1). Local `TraversalBudget` copies per owner/schema; not an aggregate CPU/Plan/M6 bound. Inherited TOML profile (4 MiB / depth 80 / 1M nodes, 2 MiB development stack, winnow compiled-unsafe TCB, no memory-safety proof) is unchanged and not re-qualified here.

## Independent reproduction

Pinned CPython **3.12.13** `-I -B -X int_max_str_digits=0`; rustc/cargo **1.95.0** `--locked --offline`; `CARGO_TARGET_DIR` under this review tree.

```
python -I -B -X int_max_str_digits=0 check-join.py \
  --cargo /opt/homebrew/Cellar/rust/1.95.0/bin/cargo \
  --output …/review/reproduce-check-join
```

| Check | Independent |
| --- | --- |
| 261 product pins + corpus pin | yes |
| 1516 typed-list kernel parity, 21 excluded non-list | yes, exit 0 |
| Public host 34 cases (`enumeration_join_rederives`) | **ok** (20 ADMIT/REFUSE documents + 14 owner/missing/tamper/limit `Err`) |
| Identity policy 8 tuples / **299** sources | `passed: true` against frozen export policy |
| Frozen workspace `--workspace` | **131** passed (isolation host named **130**, including the join fixture test) |
| Frozen Clippy `-D warnings` (workspace-final) | exit 0 (earlier workspace-check 101 + 5 clippy-fix receipts preserved historically) |
| Isolation host **141** sources / **23** vendor archives | receipt + vendor dir count |
| Isolation provider **26** sources / **19** dep archives, unavailable | expected exit 1 × 3 |
| Reader-boundary 2 packets | frozen `readerRefusedBranchesReached: false` |
| Export `enumeration_join.rs` unmutated after checker | still `ce09cc82…` |

Kernel-check/mutation-check receipts that still mention E39 TypeError holes are **historical**; the selected 1537-case corpus and this freeze use reference42.

## requiredFindings

None.

## Limits (not required findings)

- Not source acceptance, not runtime-19, not live install.
- Not complete execution-input selection, predicate reconstruction/replay, Run, or publication custody.
- Map-injection 1516-case equality is not retained-reader proof; public proof is the 34 host cases plus typed `Err` envelope.
- 21 non-list inventory containers remain reference-only; Rust slice cannot express them.
- 1537 development controls are not totality for every input or M6 resource qualification.
- Inherited TOML 2 MiB stack / winnow TCB is not re-proven.
- Isolation host test count is 130 named tests; freeze README’s 131 is the full workspace sum.
- Combined later acceptance must not waive reader41 inventory derivation, reference42 defined outputs, or the JSON-C no-float law.

## Verdict

No required findings. Frozen SOURCE41 derives join maps from retained owners, keeps typed reconstruct `Err` off the ADMIT/REFUSE document, matches selected reference42 on 1516 typed-list cases and 34 public host cases, preserves Bool 0/1 schema-failed diagnostics without admitting bool rows or inventing floats, and does not expose test-only maps as public authority. Formal runtime-19 remains separate.
