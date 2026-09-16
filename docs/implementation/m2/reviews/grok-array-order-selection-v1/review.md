# Independent Grok review: array-order-selection v1

**Reviewer:** Grok (explicitly authorized). Codex remains lead. Not Claude agreement. Not fresh consumer B.
**Subject manifest:** `docs/implementation/m2/array-order-selection-v1-subject.json`
**Manifest SHA-256:** `db9194adb6cac4b755545c197916e22b921ba0e056d4fab1ae6eb48964c6500f`
**Members:** 26
**Verdict:** **ACCEPT-DESIGN-UNIT**

Opaque `ArrayOrder` parse + verify-only helper for the closed `x-opensip-order` vocabulary. No input rewriting, no schema dispatch, no descriptor/replay authority. Parent LogicalPath v1 is accepted and archived, **not live**; live remains 8 inventory / 10 contract without `descriptors.rs`. Prior LogicalPath acceptance does not imply acceptance here. Neither M1 nor M2 is complete.

## Custody and inheritance

26/26 selection members match. Frozen implementation subject `docs/implementation/m2/trials/array-order-01/subject.json` SHA `3fd8620a…ba10` — **205/205**. Adjacent archive matches `archive-pin.json` (`65dab969…8f6a` / 1755113). Candidates are exactly the subject minus `successor.json` (25). Parents pin-match architecture: LogicalPath v1 successor `c0782dfd…73e9` / 5312 and inventory v10 `6608fabd…8bc9` / 121810 (20 packages, no extra DAG). Both map rows match frozen product, candidate product, and inventory v10. Private copy only; original candidate path and frozen tmp tree were not executed against.

Only `crates/identity/src/descriptors.rs` and `lib.rs` are owned. Live `Cargo.toml` / `canonical.rs` / `canonical_tests.rs` / `digests.rs` equal the frozen product. Live has no `descriptors.rs`. `lib.rs` adds `ArrayOrder` / `ArrayOrderError` exports beside unchanged LogicalPath exports.

LogicalPath parse/API/tests are behaviorally identical to the parent except the two-line module doc (and one trailing blank line before the new type). `ArrayOrder` is a private tuple over a private `OrderKind`; no `Default` / public constructor / serde.

Selected baseline pins `docs/coop/design-corrections/foundation/canonical.py` SHA `d47f25db…b442` / 6465 (live `design-lock.json` inputs and source-manifest row). Independent census of product `schemas/sources/*.json`: **34** distinct `x-opensip-order` forms, **517** occurrences.

## Semantics (independent of the oracle corpus)

`parse` admits only: `sequence`, `utf8`, `canonical-set`, `canonical-order`, `numeric`, `ordinal`, `candidateOrdinal`, `path`/`ruleId`/`waiverId`, `predicate` (fixed `ruleId,subjectId,predicateId` tuple), and `{"by":[nonempty unique strings…]}` with no extra members. Unknown names, empty/duplicate `by`, non-string `by` entries, and extra annotation keys refuse **even on `[]`**.

`verify` never sorts or rewrites the slice. `sequence` is a no-op (duplicates and mixed types survive). Other laws compare adjacent keys only:

| Law | Key | Uniqueness | Notes |
| --- | --- | --- | --- |
| utf8 / path / ruleId / waiverId / predicate / `{by}` | raw UTF-8 (Unicode-scalar order ≡ UTF-8 bytes) | strict | extra object keys ignored; declared field order matters |
| canonical-set | complete canonical JSON bytes | strict | can disagree with utf8 (`\n` vs `!`) |
| canonical-order | same bytes | nondecreasing, duplicates allowed | the only duplicate-tolerant non-sequence law |
| numeric | exact `JsonInteger` / i128 | strict | `true` is not an integer; extrema `-2^63` … `2^64-1` |
| ordinal | `ordinal` field, must equal `0..n-1` | implied | gaps → `NonContiguousOrdinal` |
| candidateOrdinal | integer field, strictly increasing | unique, **gaps allowed** | negatives are not this helper’s sign bound |

Item schema, snapshot joins, and replay remain caller duties. Canonical encode failures surface as `Canonical` and do not silently skip items.

## Reproduction (private copy, Cargo/rustc 1.95)

| Check | Result |
| --- | --- |
| `cargo test --locked --offline -p opensip-identity --all-targets` | **25/25** |
| `cargo clippy ... -p opensip-identity --all-targets -- -D warnings` | pass |
| `cargo fmt --all --check` | pass |
| `Cargo.lock` | unchanged |
| Adapted `run-reference.py` on **private** product + pinned `exact_order` | **115817/115817**, 34 forms, 0 mismatches |
| Targeted adversarial controls (empty malformed annotations, utf8 vs canonical, bool refusal, extrema, ordinal gap vs candidateOrdinal gap, sequence vs set duplicates, tuple field order/missing types, NFC/NFD, all 34 selected forms on `[]`) | **all pass** |

Probe asserts canonical bytes of the request object are unchanged. Probe is evidence-only, not an installed product binary. Finite oracle is not whole-schema proof.

## Must-fix / should-fix

Must-fix: none. `requiredFindings` remain empty.

## Limits

- Order annotation parse/verify only. Not schema dispatch, descriptor assembly, item-shape admission, or replay.
- 115817 cases cover the selected 34 annotation forms plus generated scalars/records; not every schema combinator.
- LogicalPath v1 is parent-accepted, not live-installed. This unit is not live-installed.
- Not M1/M2 complete, not fresh consumer B, not release/sandbox.
- `exact_order` is design-reference Python, not a host runtime.
