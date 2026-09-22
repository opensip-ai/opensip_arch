# Closure review — shared work ledger inventory v61 (RF-1 correction)

Reviewer: actual Claude Opus 5 (model identity, not a task label), 2026-09-21.
Narrow bounded closure of the single required finding I raised against inventory v60. Read-only. No
product or architecture edits, no native or Node jobs, no commits, no delegation, no selection, and
no source approval. Artifacts only under
`/tmp/opensip-implementation/reviews/claude-opus5-shared-work-inventory61-r1`.

This is a fresh-byte closure, not a restart. My v60 review already established the substantive
properties — additivity, unchanged policy bodies, the five-meaning projection hazard, layer
suitability, and the projection helper's real strengths and real limits. Root's disposition records
agreement with all of it. I re-verify here only what new bytes can change, and I say explicitly
which conclusions I am inheriting rather than re-deriving.

## Verdict

**ACCEPT-UNIT.** `requiredFindings: []`. **RF-1 is CLOSED.** 52 checks, all passing.

## RF-1 closed

The corrected row is `crates/platform/tests/work_ledger_tests.rs`. The governing document
`docs/v2/architecture/14-repository-and-module-layout.md` is unchanged (sha `c7b10bf6…6287e`) and is
still a selected input of the live lock, and its convention row still reads
`` `<subject>_tests.rs` ``. The corrected path satisfies it. The non-compliant
`crates/platform/tests/work_ledger.rs` is absent from v61, and **every** `*/tests/*.rs` row in the
v61 candidate now complies — the condition I could not assert for v60. The ordinary source module row
`crates/platform/src/work_ledger.rs` is byte-identical to its v60 row and remains correct as
`snake_case.rs`, exactly as the finding said it should be.

## The delta is the rename and nothing else

This is the check that matters most for a correction, because a re-freeze is an opportunity for
unrelated drift:

- Row-set delta from the rejected v60 is exactly `{-work_ledger.rs, +work_ledger_tests.rs}`.
- The renamed row differs **only** in its `path` field — `package`, `role`, `description`,
  `generated` and `standing` are byte-equal.
- **No other row changed** between v60 and v61.
- The candidate file is exactly **6 bytes** larger than v60's, which is the length of the inserted
  `_tests` and nothing more.
- The record's `descriptionOverrideProjection` is **byte-identical** to the v60 record's, confirming
  the rename shifts no selector. The record's key set matches the v60 record's, and its
  `carriedUnresolvedObligations` are byte-identical to it.

## Fresh bytes re-verified

Subject `docs/implementation/m2/shared-work-ledger-inventory-v61-subject.json`, **1890 bytes**,
sha `1c0a4222…b9908d8` — matches. **9** members, sorted and unique, all verifying byte-for-byte
against their pins. The member set is entirely documentation and inventory JSON: there is no source
archive here, so this unit can select no source bytes even in principle.

Against the selected parent, the verifier's additive rules all hold. The record's parent pin equals
the lock-selected inventory (`repository-file-inventory.v59.json`), and the record carries **no
reference to the rejected v60** — it extends v59 directly, as required.
`parentArtifactBytesUnchanged` and `inheritedRowsEqualByValue` are `true`; top-level key sets are
identical and every key except `standing` and `files` is byte-equal, which is what proves rather than
asserts **20 packages** and **9 pending decisions** unchanged; rows are sorted and form a strict
superset of the parent's; no inherited row changed or was removed; **706 → 708**; no new crate
directory; `addedFiles` names the corrected path.

## Five effective projections still hold

I recomputed the effective meanings from the live lock rather than trusting the record or the
helper's recorded output. The live lock still yields **4 inherited rows + 1 direct override = 5**,
with the direct one still `initial-root-binding-owner-selection-v1` on v59 `/files/104/description`
(`crates/host/src/installation_lineage.rs`) — still absent from `inventoryPassageInheritance`, so
still the meaning a naive copy would drop. All five projection rows match the live `before`/`after`,
the parent's actual description text, and the candidate's retention of the **base** text. Selectors
are **7/13/104 unchanged, 503→505, 570→572**.

## Helper and anchor

`verify_projection.py` is **byte-identical** to the helper I reviewed at v60
(`bb82ef05…2f9dd110`), so my v60 assessment of it carries over unchanged and I did not re-derive it.
For the record, that assessment stands in both directions: `expected()` is genuinely substantive
because it reconstructs the projection from the lock's inheritance rows *and* every contract
successor's overrides, which is what makes the direct row-104 meaning impossible to miss; while
`verify()` is a bare `assert rows == wanted`, so the advertised **`corruptionsRefused: 28` remains
near-vacuous** — it exercises the harness, not an independent property. Root's disposition records
agreement on exactly this point, and the v61 README now states it in the unit's own words. The
recorded run is honest about the conditions that matter: `-I -B` with **no `-O`** (bare asserts would
otherwise be silently disabled), exit 0, targeting the v61 helper and the product lock, with stdout
reporting 5 rows, `PASS`, and `directParentOverrideIncluded: true`.

The anchor is now fresh rather than stale, which resolves the drift I reported at v60. It pins head
**`117d0e3`** — the current live product head — and both anchored files are byte-identical live:
`tools/verify_design.py` (`2764cf7b…`, still the unchanged selected verifier) and `design-lock.json`
(105618 bytes, `531734d9…`). The anchored baseline is **35 inventory / 58 contract successors**, as
claimed. The product working tree is clean, so nothing mutated under me while root runs its serial
native 420 suite.

## Correction provenance

`correction.json` pins my original `review.json` by exact bytes and digest
(12512 bytes, `6ae4be0b…be194` — the value in my own v60 `hashes.txt`), together with the original
v60 subject (`7568cc68…`) and the governing layout document. It names `RF-1`, both the old and new
paths, and records `originalNotSelected: true`. I confirmed independently that **v60 is not selected
in the live lock**, that v61 is **not yet selected** either — review still precedes selection — and
that the frozen v60 artifacts are still present and unmodified, including the v60 candidate at its
original digest. The rejected unit is preserved as history, not rewritten.

## What I am inheriting, and what I am not asserting

Inherited from my v60 review and unchanged by these bytes: layer suitability (platform is the lowest
internal layer; `security`, `host`, `storage`, `components` and `lifecycle` all depend on it, so a
pure accounting mechanism needed by the host's private attempt and by security's retained
identity/cache belongs there), the ownership boundaries carried in the two row descriptions, and the
helper assessment above. The inventory's planned `opensip-platform → opensip-contracts` package edge
is unchanged from v59 and remains a *planned* edge; root's disposition is right that a planned edge
need not be an implemented dependency, and nothing here should be read as requiring it to be created.

Not asserted by this review: no approval of any source. The corrected test filename must reach
product code through the separate new source421 candidate; frozen source419 remains historical and
unselected and must not be rewritten, and my v60 reference to the 418 draft was accurate for that
draft at that time. Source review, root assent and integration obligations all remain open before any
code selection. No claim of creator qualification, native custody, shared capture precharge, current
authority, profile, permit, P0, release, or whole-M2/project completion. Root assent on this unit
remains required; selecting these rows selects no implementation. My evidence here is read-only
Python checks and file reads only — no builds, tests, staging, or native or Node jobs.

## Observations

None blocking. One note carried forward for whoever prepares source421: the two inventory row
descriptions are unchanged from v60, so the src row still reads "Includes focused accounting
regressions" while the separate integration test now lives at `work_ledger_tests.rs`. Both statements
are accurate — inline unit tests in the module plus a separate behavioral test file — and the
convention explicitly permits that split, so no change is needed; it is worth keeping in mind only so
the source delta matches the row text.
