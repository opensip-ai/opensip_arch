# Independent inventory/layout review — shared work ledger inventory v60

Reviewer: actual Claude Opus 5 (model identity, not a task label), 2026-09-21.
Bounded layout review only, read-only. No product or architecture edits, no native or Node jobs,
no commits, no delegation, no selection, and no source approval of the unfrozen 418 draft. All
artifacts are written only under
`/tmp/opensip-implementation/reviews/claude-opus5-shared-work-inventory60-r1`.

## Verdict

**REQUIRED-FINDINGS — not ACCEPT-UNIT.** One required finding, stated in full below. Everything
else in the unit verifies: all 8 members, the additive row rules, the unchanged policy bodies, and —
critically — all five effective description meanings including the one the lock does not list.

The finding is a single frozen path string. It is cheap now, because the source is still unfrozen and
unselected, and expensive after selection, because a selected inventory row path can only be changed
by another successor, review and assent cycle.

## Required finding 1 — added test row violates the selected file-naming convention

`crates/platform/tests/work_ledger.rs` is a separate behavioral test file (`role: test`, a Cargo
integration target under `crates/platform/tests/`). The selected architecture layout document
`docs/v2/architecture/14-repository-and-module-layout.md`, section "File inventory and naming
conventions", requires:

```
| Separate behavioral test file | `<subject>_tests.rs` | `<subject>.test.ts` | Name the behavior or
module under test; small Rust unit tests may remain inline |
```

That document is a **selected input of the current design lock** (`lock.inputs`, sha
`c7b10bf6…6287e`) and an accepted application-manifest file, so this is a governing rule, not an
emergent habit. All **10** existing `*/tests/*.rs` inventory rows comply
(`startup_tests.rs`, `admission_tests.rs`, `discovery_tests.rs`, `retention_tests.rs`,
`workflow_tests.rs`, `html_renderer_tests.rs`, `projection_tests.rs`, `commit_tests.rs`,
`grammar_tests.rs`, `normalization_tests.rs`). The only four `role: test` `.rs` inventory rows
without the suffix are all inline `src/` modules, which the same convention row explicitly permits
("small Rust unit tests may remain inline"). The standard-spelling exemption list
(`lib.rs`, `main.rs`, `mod.rs`, …) does not cover this case.

**Action:** rename the added row to `crates/platform/tests/work_ledger_tests.rs`, re-emit the v60
candidate and this successor record, and rename the corresponding file in the unfrozen 418 source
(its `NOTES.md` states the delta is `platform/src/lib.rs` plus new `platform/src/work_ledger.rs` and
`platform/tests/work_ledger.rs`). The suffix exists precisely to disambiguate a test file from the
`src` module of the same name, which is the situation here. The src row
`crates/platform/src/work_ledger.rs` is correct as an ordinary `snake_case.rs` module and needs no
change.

## Frozen subject and members

Subject `docs/implementation/m2/shared-work-ledger-inventory-v60-subject.json`, 1685 bytes,
sha `7568cc68…dcedca0` — matches. All **8** members exist with exactly their pinned bytes and
digests; the member list is sorted and unique.

## Inventory successor rules (current `tools/verify_design.py`)

I replayed `inventory_successor`'s rules against the proposed v59 → v60 successor using the live
verifier and the live post-integration lock. Every rule holds:

- Parent pin equals the lock-selected inventory (`repository-file-inventory.v59.json`,
  280949 bytes, `c2400990…1cb815`); candidate path differs from parent and is not already accepted.
- `parentArtifactBytesUnchanged` and `inheritedRowsEqualByValue` are both `true`.
- Top-level key sets are identical, and **every key except `standing` and `files` is byte-equal** —
  which is what makes `packages` (20) and `pendingDecisions` (9) provably unchanged, not merely
  asserted.
- Candidate rows are sorted by path and form a **strict superset** of the parent's; no inherited row
  is changed or removed; **exactly two rows are added**, and they are exactly the two declared in
  `addedFiles`.
- Row counts **706 → 708**, matching the planned figure.
- No new crate directory: both additions land in the existing `crates/platform` tree, and
  `crates/platform/tests/` already exists.
- Added rows use the existing field keys and the existing role vocabulary (`service`, 43 prior uses;
  `test`, 72 prior uses) with `standing: proposed`.
- The record's key set is identical to the accepted v59 precedent record, and its
  `carriedUnresolvedObligations` are **byte-identical** to that record's — so the carried 211/218
  obligations are genuinely unchanged. They are labelled "retained outside selected inventory
  policy", which is why they correctly do not appear among the nine `pendingDecisions`.

## The projection — the part that could have gone wrong

The unit's central hazard is real and the unit clears it. I recomputed the effective meanings on v59
independently from the live lock:

- 4 rows in `inventoryPassageInheritance`, all on v59, at `/files/7`, `/files/13`, `/files/503`,
  `/files/570`.
- **1 direct override** from the selected `initial-root-binding-owner-selection-v1/successor.json`
  on v59 `/files/104/description` (`crates/host/src/installation_lineage.rs`), which appears in no
  `inventoryPassageInheritance` row.

That is 5 distinct meanings. I confirmed that copying only the lock's four inheritance rows would
lose row 104 — the exact failure the README warns about. The v59 precedent record carried 4
projection rows; v60 carries 5, because the initial-owner-406 override landed after v59 was
selected. For all five rows I verified: `filePath` matches the row path in both documents, `before`
equals the actual parent description *and* the lock's `before`, `effectiveDescription` equals the
lock's `after`, the candidate row still carries the **base** text (the override meaning stays in the
lock and is not baked into the inventory), and the projected index is right —
**7/13/104 unchanged, 503→505, 570→572**.

## Helper limits, stated honestly

`verify_projection.py` is genuinely substantive in `expected()`: it reconstructs the projection from
both sources (the lock's inheritance rows *and* every contract successor's `passageOverrides` on the
parent), verifies the parent pin, candidate pin and each contract record's pin, requires
`row['description'] == o['before']`, asserts the candidate row is byte-equal to the parent row, and
refuses duplicate overrides on one path unless identical. That reconstruction is what makes the
direct row-104 meaning impossible to miss.

Its limits are worth stating plainly:

1. `verify()` is a bare `assert rows == wanted`. The reported `corruptionsRefused: 28`
   (5 rows × 5 fields, plus three rowset mutations) is therefore near-vacuous — mutating a deep copy
   of the expected value must differ under `==`. Those 28 cases demonstrate the harness, not an
   independent property. The real assurance is in `expected()`.
2. Every check is a bare `assert`, so running under `python3 -O` would silently disable all of them.
   The recorded command uses `-I -B` and no `-O`, so the recorded evidence is valid, but the helper
   carries no guard.
3. `assert len(out) == 5` freezes today's count; a sixth future meaning would need a helper edit.
   Acceptable for a frozen unit, but it is a freeze, not a general rule.
4. It checks none of the additive row rules (sorted, strict superset, exactly two additions,
   unchanged non-`files` keys). Those belong to the product verifier; I checked them independently.
5. The lock is a command-line argument, so its evidence is only as strong as the lock passed in.

## Anchor staleness — disclosed, and I re-verified past it

`verifier-anchor.json` pins product head `f7f50d6` with `tools/verify_design.py` and
`design-lock.json`. Root has since integrated runtime36: live head is now **`117d0e3`**, the lock is
105618 bytes (`531734d9…`), and `contractSuccessors` is **58**. So the anchored lock has drifted, as
the README discloses, and a fresh selected-baseline verification remains owed. Two things make this
harmless here:

- `tools/verify_design.py` is still **byte-identical** to its anchored pin (`2764cf7b…`), so the
  "no verifier change" claim holds.
- I ran all of my projection and additive checks against the **current post-36 lock**, not the
  anchor, and still found exactly 4 inherited + 1 direct = 5 meanings, with the selected inventory
  still v59 (`inventorySuccessors` remains 35). The v36 record carries `passageOverrides: []`, so
  runtime36 changes no inventory meaning — consistent with the unit's claim and stronger than what
  the anchor alone would show.

## Layer suitability

The placement is right, and the dependency graph — unchanged by this unit — proves it.
`opensip-platform` is the lowest internal layer, and both `opensip-security` and `opensip-host`
depend on it (as do `storage`, `components` and `lifecycle`). A pure accounting mechanism needed by
the private attempt owner (host) and by retained identity/cache (security) therefore belongs in
platform as the lowest common existing layer; no new crate is required, and the unit adds none.

The two row descriptions keep ownership where the task states it should sit: platform owns "pure
accounting", while "retained evidence identity/cache and native authority remain with their owners".
The src row's clause "constructor alone cannot establish same-attempt discipline" is an honest
record of the external 416/417 probe result, where `*helper = WorkLedger::new(...)` erased charged
work through a `&mut WorkLedger` handed to a callback. Reading the 418 notes for placement context
only: the correction hands helpers a non-constructible `WorkScope` with a private original-ledger
reference, so a helper can charge and reborrow but cannot replace the owner. "Public" here means
exported from `opensip-platform`, which is what lets an integration test exercise it; it does not
weaken "host must hold the ledger privately". Nothing in this review approves that source.

One inherited inconsistency, noted but **not** attributable to this unit: the inventory's package
graph gives `opensip-platform` a dependency on `opensip-contracts`, while the live
`crates/platform/Cargo.toml` declares only `getrandom` and `libc`. The `packages` body is byte-equal
between v59 and v60, so this predates the unit and is out of its scope.

## Evidence and limits

- **My own evidence:** read-only Python checks and file reads only —
  `evidence/inventory-checks.py` / `.json` (34 checks, all pass) and
  `evidence/naming-convention-check.json`. No native or Node jobs, no staging, no builds, no tests.
- **Author evidence, attributed:** the unit's own `verification.json` / `verification.stdout`
  (`projectionRows: 5`, `positive: PASS`, `corruptionsRefused: 28`,
  `directParentOverrideIncluded: true`) was produced by the unit author against the pre-36 lock; I
  did not rerun it, and my own checks were computed independently against the current lock.
  The 418 build/test outputs under `/tmp/opensip-implementation/shared-work-ledger418/` are the
  root/author's development evidence for an unfrozen draft; I read `NOTES.md` for placement context
  only and ran nothing.
- **Limits:** this is a layout review. Selecting these rows selects no implementation. I did not
  review, and do not approve, the 418 source. A fresh selected-baseline verification against head
  `117d0e3` is still owed. No claim of creator qualification, shared native precharge, current
  authority, custody, profile, permit, P0, release or whole-M2/project completion; the real
  security-cache and native-capture join remains open. Root assent remains required, and cannot be
  given on this unit until the required finding is resolved.

## Non-blocking observations

1. `crates/platform/tests/` currently holds only `fixtures`, so this would be platform's first
   integration-test target. No defect — just a new target to keep in mind for build wiring.
2. The unit's recorded `verification.stdout` was produced against the pre-36 lock. Re-running the
   frozen helper against the current lock would refresh it at no cost; my independent recomputation
   already shows the projection still holds.
