Grok review: D1, the description-only contract successor that refreshes stale plain rows of inventory v119 (EXIT-PLAN.md "D1 (description batch)" and the later notes that add rows to it). Claude Opus 5.5 leads. You are the single reviewer. Do not edit any repository, commit, push or delegate. Write only under /tmp/opensip-implementation/reviews/grok-description-batch-d1-r1. If you run anything, use only the two evidence scripts named below or read-only commands, and run git only read-only. Run no product cargo.

## Subject

The pins are in hashes.txt:
- `docs/implementation/m2/description-batch-d1-subject.json`, the subject manifest;
- `docs/implementation/m2/description-batch-d1/`, which holds `successor.json`, `README.md`, `evidence/descriptions.json`, `evidence/build_d1.py` and `evidence/verify_scratch.py`.

All of these are untracked in arch until acceptance.

The product is main at 8240856 (X4B-b), read-only, and its lock selects inventory v119 with 72 contract successors and 16 inheritance rows. There is no product, schema, registry, generated-code or inventory change, so no worktree and no inventory successor are needed.

`rationales.json` in this directory is a convenience and is not part of the subject. For every candidate row it gives the lead's evidence: what was false or omitted, with file:line.

## What it does

It makes thirty-nine JSON Pointer `/files/N/description` overrides on v119, its only parent. Each one replaces a description that no longer describes the file at 8240856. The README tabulates every row and what was stale in it. The exact before and after text is in `evidence/descriptions.json`, and identically in `successor.json`.

**Where the rows come from.** They are:
- the D1 entry's rows;
- the F5 notes (`initial_core.rs`, `trust_bootstrap.rs`, `live_observation.rs`, `operation_live_tests.rs`, `commit_authority.rs`);
- every row an inventory README from v81 to v119, or a review judgment call, deferred to "the description-only successor". That covers X3a-1, X2b-1, X2b-2, X2c, X2d, X2e, X3b-1b, X3b-2, X3b-4, X3c-2, X3d-0, X3d-1, X4T-a, X4T-a3, X4T-b, X4a, X4B-a, X4B-b, X8a and X10a.

**How the descriptions were edited.** Every sentence that is still true is kept word for word. False text is replaced, and short clauses name what the file now does.

**Rows checked and kept:** `clock_observation.rs` and `operation_guard_tests.rs`.

## Mechanism (lead decision)

This is 461b's lawful route. verify_design's `contract_successor` accepts a passage override when:
- its parent is an accepted base or selected inventory;
- its `before` equals the parent's passage;
- its `after` is non-empty and different.

A direct override on the final selected inventory is not projected, so `inventoryPassageInheritance` stays at 16. An inventory successor cannot carry the change, because `inventory_successor` requires inherited rows to be equal by value (X4T-a3 call 1).

No D1 row is one of the 16 inherited projection rows. `build_d1.py` asserts this.

## Judgment calls: please rule on each

1. **VD1 is deferred, not done.** Four stale rows are inherited overrides:
   - `read_premise.rs`: X1b's proposed text, plus the X2e, X4a and X3d-1 additions;
   - `installation_session.rs`;
   - `store_lineage.rs`;
   - `initial_installation.rs`.

   A direct override on any of them conflicts with its projection (`stale-descriptions-x1b/probe.py`). They wait for VD1, a separately reviewed `tools/verify_design.py` change.

   Rejected: changing the trust anchor inside a description unit.
2. **Scope is wider than the D1 entry's list.** Rows that READMEs or reviews deferred to "the description-only successor", but that EXIT-PLAN never copied into D1, are included. Examples are the X3b-4 carrier rows, X4a's out-of-date rows, `admission_tests.rs` and `work_ledger.rs`. Leaving them would need a second batch for the same purpose.
3. **`revocation.rs` (408) is rewritten entirely.** Its planned text was never this file's content, which is the fail-stop FreshnessMonitor. Epoch observation is root_payload's `observe_revocation`, and the checkpoint is operation_guard's. No README listed it; the X4a re-read found it.
4. **`commit_authority.rs` (327) is rewritten from the plan's placement to its content.** The content is FinalGate, OperationGate and PreparedJournalSeal. It also says where CommitSession, JournalWriteTxn and JournalSealBinding now live.
5. **`admission_tests.rs` (134) keeps its planned first sentence.** That sentence is the file's purpose, which X8c completes. The new text adds X8a's compile-fail driver as it stands and says plainly that the behavioural cases are X8c's.
6. **Termination rows (118, 382) are described by kind, not by enumerating variants.** They say "existing codes" rather than "an existing detail", because the LEDGER.CORRUPT and DURABILITY.COMMIT_FAILED rows publish no domain detail.
7. **Some descriptions are long.** `operation_handoff.rs` (360) is 3989 characters; the longest existing v119 description is 3232. Keeping every true sentence verbatim forces the length. Rejected: rewording true text to save space.
8. **Things found but not changed here, because they are product code comments or code.**
   - `carrier_floor.rs`'s doc comments (around lines 114 to 116) still say there is no production constructor until X3b-3.
   - `installation_doctor.rs`'s header still says "Library only".
   - `installation_termination.rs`'s comment says only a broken caller reaches the invariant row, but X4B-b's second F absent now reaches it too.
   - The doctor ingress has no remedy for the X4a and X3d-1 termination rows. A detail with no remedy is a projection error there. Doctor runs no trust admission or operation, so these rows look unreachable from doctor. Please confirm.

   The lead will route these to a code follow-up.
9. **Next inventory successor.** Once D1 is selected, the next inventory successor must:
   - carry these 39 rows by value;
   - grow the lock's `inventoryPassageInheritance` from 16 to 55, in verify_design's canonical order;
   - raise its projection helper's count to 55.

   This is the same step 461b caused (8 to 16). If another inventory is selected first, `build_d1.py` rebuilds on it with no edit, because it finds rows by path. That rebuild needs a new review.

## Checks

- `python3.14 -I -B evidence/build_d1.py` produced the same bytes on two runs. It refuses on any of these: a before mismatch, an inherited row, a duplicate path, or an empty or unchanged after.
- `python3.14 -I -B evidence/verify_scratch.py` ran the real `tools/verify_design.py` at 8240856. The scratch lock is the real lock with D1 appended, and the review and assent are synthetic in memory. The result:
  - passed, with 73 contract successors and v119 still selected;
  - 16 inheritance rows, unchanged;
  - 39 overrides, all with parent v119;
  - 40 generation sources, 48 admission sources and 15 aliases verified.
- The live `verify_design --architecture ../opensip_arch` at 8240856 passes unchanged.

## Decide

- Is every new description true of the committed code at 8240856? Read the files. Is each one a fair, minimal edit of the old text?
- Is any changed sentence that was true now lost?
- Is any v119 plain row for a file changed since its description was written still stale and missing from this batch?
- Rule on judgment calls 1 to 9.
- Is the successor well-formed for selection, so the next inventory successor can carry these rows by value? Is anything else wrong?

review.json must contain:
- "verdict": `ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256": a single string, the sha256 of `description-batch-d1-subject.json`;
- "successor": {path, bytes, sha256} of `description-batch-d1/successor.json`.

This is a contract successor, so it has no `inventoryCandidateAssessment`. If you would change a description's bytes, give the exact replacement string.

Write REVIEW.md and review.json. Do not commit.
