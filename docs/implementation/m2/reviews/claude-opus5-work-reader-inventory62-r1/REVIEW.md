# Independent layout review — work reader inventory v62

Reviewer: actual Claude Opus 5 (model identity, not a task label), 2026-09-21.
Layout-only, read-only, bounded. No native or Node jobs (root owns the serial lane), no edits to
either repository, no selection, no commits or push, no delegation. Artifacts only under
`/tmp/opensip-implementation/reviews/claude-opus5-work-reader-inventory62-r1`. Prior review and
advisory evidence untouched.

**This is not approval of source430, of the 430 reader algorithm, or of the native postcheck
composition still open under audit 429.**

## Verdict

**ACCEPT-UNIT.** `requiredFindings: []`. 46 checks, all passing. Five non-blocking observations.

## Exact pins and members

| Artifact | Bytes | SHA-256 | Result |
| --- | --- | --- | --- |
| `work-reader-inventory-v62-subject.json` | 1636 | `c93420f5…1c61f82e` | matches pin |
| `repository-file-inventory.v62.json` | 283031 | `04cb5a98…8755200c` | matches pin |
| `work-reader-inventory-v62/successor.json` | 5999 | `a0c348a4…198ff6ba` | matches pin |

All **8** formal members verify byte-for-byte, sorted and unique. Product is clean at `5b42fd6` with
the lock at **36 inventory / 61 contract** successors and `repository-file-inventory.v61.json`
selected — the anchor's preparation state, confirmed live.

## Additive structure

Replaying the current `tools/verify_design.py` `inventory_successor` rules: the record's parent is
the lock-selected v61 with matching pins; the candidate path differs from its parent and is not
already accepted; `parentArtifactBytesUnchanged` and `inheritedRowsEqualByValue` are both true; the
top-level key sets are identical and **every key except `standing` and `files` is byte-equal**, which
is what *proves* rather than asserts that the 20 packages, the 9 pending decisions and the rest of
the body are unchanged. Rows are sorted and form a strict superset of the parent's, **all 708
inherited rows are unchanged by value**, and **exactly two** rows are added — precisely the two
declared planned files, matching the record's `addedFiles`. Counts move **708 → 710**. The record's
key set and its carried **211/218** obligations are byte-identical to the accepted v61 record.

## Naming and placement

This is the part the unit had to get right, and it does.

`docs/v2/architecture/14-repository-and-module-layout.md` is unchanged (`c7b10bf6…`) and still a
selected lock input, and its convention row still reads `` `<subject>_tests.rs` ``.

- `crates/platform/src/work_reader.rs` — an ordinary `snake_case.rs` module. Correct.
- `crates/platform/tests/work_reader_tests.rs` — satisfies `<subject>_tests.rs`, and its subject
  matches the src module's subject exactly. **The rule I raised as RF-1 against inventory60 was
  applied here proactively**, and every one of the **12** `*/tests/*.rs` rows in v62 now complies.

Placement is right by the same argument I gave for the ledger at inventory60: `opensip-platform` is
the lowest internal layer, with `security`, `host`, `storage`, `components` and `lifecycle` all
depending on it, so a generic caller-buffer and read-attempt helper that both the host and the
security cache will need belongs there. No new crate and no new dependency — the two rows land in the
existing `crates/platform` tree, `crates/platform/tests/` already holds `work_ledger_tests.rs` from
v61, and the `packages` body is byte-equal. The added rows reuse the existing role vocabulary
(`service` for the module, matching its sibling `work_ledger.rs`; `test` for the target, matching
`work_ledger_tests.rs`), the existing field keys, `package: opensip-platform`, `generated: false` and
`standing: proposed`.

## Non-authority descriptions

My automated scan flagged the words "custody" and "creator", so I read both rows rather than trusting
the scan. Both use them **only as disclaimers**:

- src: *"Generic reader accounting does not qualify arbitrary reader internals, allocator RSS, native
  custody or required postchecks."*
- test: *"Generic accounting fixtures, not native custody or creator qualification."*

Neither row claims authority, admitted evidence, a native creator, P0, current authority or shared
complete precharge. The src row's disclaimer of **"required postchecks"** is the important one: it is
exactly the boundary audit 429 identified and that my 429 advice and its correction analysed, so this
layout does **not** promise that the reader composes into the native `read_one` bracket. That is the
right scoping, and I want it on the record because it was the live open question when this unit was
frozen.

## The five effective meanings

Recomputed from the live lock rather than from the record: the lock now carries **five** inheritance
rows, all on v61, and **zero** direct overrides — the initial-owner-406 row-104 meaning was projected
into the inherited set when v61 was selected, exactly as I predicted at v60/v61. So "five is this
unit's count" is confirmed from the lock, not assumed.

All five projection rows match the live `before`/`after`, the parent's actual description text, and
the candidate's retention of the **base** text, with the moves being
**7/13/104 unchanged, 505 → 507, 572 → 574** — the two-row shift landing exactly where two additions
before those paths would put it.

## Helper and anchor

`verify_projection.py` is **byte-identical** (`bb82ef05…`) to the helper I reviewed at v60 and v61,
so that assessment carries over unchanged and I did not re-derive it: `expected()` is substantive
because it reconstructs from the lock's inheritance rows *and* every contract successor's direct
overrides, while `verify()` is a bare `assert rows == wanted`, which is why the advertised
**`corruptionsRefused: 28` remains near-vacuous** — harness exercise, not independent assurance. The
unit's own README says as much, which is the right posture. The recorded run correctly uses `-I -B`
with no `-O`, since those are bare asserts.

The anchor pins head `5b42fd6` and both anchored files are byte-identical live; the product verifier
is unchanged (`2764cf7b…`) and independently reconstructs final inheritance during guarded
activation. As the unit states, a later lock change requires fresh checking — the anchor is a
preparation state, not a licence.

Finally, both planned files are absent from the live product, which is as it should be: layout
precedes source.

## Evidence and limits

- **Mine:** read-only Python checks (46) plus direct reads of the added rows, the unit README and the
  layout convention. No native or Node job, no build, no test, no staging.
- **Author/root evidence, attributed, not rerun:** the unit's own `verification.json` /
  `verification.stdout`, and the private 428 result of eight public reader tests plus a workspace
  pass. I reproduced neither; my projection conclusions come from an independent recomputation
  against the live lock.
- **Limits.** Selecting these rows selects no implementation and no bytes. This review does not
  approve source430, its accounted/reserved reader algorithm, its exports, or the 430 formal unit —
  all of which the request says will receive separate source and formal review after layout
  selection. It does not settle the native error/postcheck finalization composition, which audit 429
  correctly holds open and which my 429 advice plus correction addressed advisorily without amending
  law or approving source. Generic `Read` internals, OS and allocator RSS, custody and required
  postchecks remain outside any claim here. The native file adapter is not rewired. No native
  creator, InitialActor, core, profile, permit, P0, current authority, shared complete precharge or
  public ingress is conferred, and no M2 or M2–M6 completion is claimed. Root substantive assent
  remains required before selection.

## Non-blocking observations

1. The `opensip-platform` package purpose still reads *"OS mechanisms behind explicit interfaces,
   without policy authority"*, while two `service` rows — `work_ledger.rs` from v61 and now
   `work_reader.rs` — are generic bookkeeping rather than OS mechanisms. The tension was introduced
   when the ledger landed, the `packages` body is byte-equal here, so it is out of this unit's scope;
   but the purpose line will read more loosely with each generic helper added, and is worth revisiting
   in whatever unit next touches the package graph.
2. The src description says the reader "preserves errors". That means the error *value*; per audit
   429 and my correction, this reader's errors latch the owner, which is precisely why it cannot be
   dropped into the native `read_one` bracket. The row's explicit disclaimer of required postchecks
   keeps this honest, but a reader skimming only the first clause could take "preserving errors" to
   mean composable error semantics.
3. The src description is quite specific about algorithm behavior ("charging before requested growth
   and every read attempt"). Selecting a row description is not source approval, and the unit README
   says so plainly — but the specificity means a later reader should still not treat the row as
   settled behavior for source430.
4. 12/12 `*/tests/*.rs` rows now satisfy the `<subject>_tests.rs` convention. Worth recording as a
   positive: the inventory60 finding has become a habit rather than a one-off correction.
5. `crates/platform/tests/` now holds two integration targets, so the convention there is
   established and future platform helpers have a pattern to follow.
