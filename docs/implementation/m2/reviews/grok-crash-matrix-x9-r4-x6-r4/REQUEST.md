Grok review: two law revisions together, X9 r4 (an amendment) and X6 r4 (record-only). Claude Opus 5.5 leads. You are the single reviewer.

**Rules.**
- No repository edits, commits, pushes or delegation.
- Write only under /tmp/opensip-implementation/reviews/grok-crash-matrix-x9-r4-x6-r4.
- This is a law review with no product cargo. Run git only read-only. Product facts are pinned at product `a36da7c`; read them with `git show a36da7c:<path>` in `/Users/sb/code/opensip-ai/opensip`.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent. Never read the private 413 UUID fixture.

## Why there is an amendment

Unit X9-2 stopped before writing code. It found that its rows cannot be built in `crates/storage/tests/commit_tests.rs` without breaking X9 r3 item 6 and its forbidden substitutes. That target links security as an ordinary library. It needs three admissions over item 6's synthetic installation, and it can obtain none of them lawfully:
- **The operation** (the `commit` driver, and R2's next writer).
  - `admit_ordinary_writer`, `ordinary_writer::admit_with` and `begin_operation` are crate-private (`ordinary_writer.rs`, lines 220 and 493–506).
  - X9 forbids a support function that returns a `ProjectOperation`.
  - X8 r3's `scenario::operation` is X8b's. It is not integrated, and it is not among X9-2's dependencies.
- **The recovery admission** (R1 and R4).
  - `RecoveryAdmission::admit` always uses `HomeSource::Native`, the account database's home (`recovery_admission.rs`, lines 484–509). That is the real home, and this host refuses there anyway.
  - `admit_on` over `HomeSource::Fixture` is crate-private, and no law exposes it.
- **The sweep admission** (R3). `SettlementSweep::admit` is `admit_on(admit_ordinary_writer()?)`. It is native-only in the same way.

X9-1's census reaches all three only because it runs inside security. X9-1's request (call 7) left X9-2 needing "X8b's or this surface's operation path". The X9-1 review accepted that without ruling which.

Separately, `tools/check_crash_matrix.py check` requires two things that a unit's run set cannot meet before X9-6:
- the reviewed commit on a clean worktree;
- full kill-set coverage.

## Pins

Pins are in hashes.txt. Each accepted predecessor is preserved byte for byte, without its "ACCEPTED" note. Each snapshot's sha256 equals the subjectSha256 of the review that accepted it:
- `crash-matrix-x9/PROPOSAL-r3.md` is X9 r3, `1f270548…` (`reviews/grok-record-x3d-r7-x7-r6-x9-r3/x9/review.json`);
- `carrier-recovery-x6/PROPOSAL-r3.md` is X6 r3, `e57aef34…` (`reviews/grok-recovery-x6-r3-x7-r4-x9-r2/x6/review.json`).

Both snapshots already existed. They were checked, not rewritten. Each working PROPOSAL.md differed from its snapshot only by its "r3 ACCEPTED" note, which stays.

Diff each PROPOSAL.md against its snapshot. Every line of the predecessor survives verbatim, with these exceptions:
- the title;
- the ACCEPTED note that is already in the working law;
- marked "r4" insertions (sentences appended with "r4", "(r4)" or "**r4 (record):**").

Accepted text is never deleted.

## X9 r4 (an amendment; lead decisions)

Both decisions were taken by the coordinator as lead decisions under the owner's standing direction of 2026-09-30.

1. **The three driver entries** (the r4 header; item 6's new "The three driver entries (r4)" paragraph; the "What it exposes" pointer; the forbidden substitutes).
   - **The entries.** Security's `crash_matrix_support` exposes exactly three. Storage and host forward them unchanged:
     - `operation(at, root) -> Result<ProjectOperation, InstallationTermination>`;
     - `recovery_admission(at, request) -> Result<RecoveryAdmission, RecoveryRefusal>`;
     - `settlement_sweep(at) -> Result<SettlementSweep, InstallationTermination>`.
   - **What each may return.** Only what an existing crate-private production composition returns over the fixture home. This is the same exception X8 r3 item 4 gives `scenario::operation`.
   - **Constraints:**
     - it sits inside the pinned support module;
     - it calls only existing items and existing joint-predicate sites;
     - it adds no new cfg site and no home override on production entries;
     - it may widen a crate-private item at most to `pub(crate)`;
     - it is compiled only under `crash-matrix` and is absent from every release build;
     - it accepts no receipt, gate, guard, monitor, clock, session, permit or `ReplayedRun`;
     - it constructs nothing itself;
     - one entry per process (X1 items 1 and 7), enforced by the module's own flag;
     - `publish_revocation` refuses in a process that made an entry.
   - **Rejected, and recorded:**
     - the callback-style function, which hands out the type without returning it;
     - the home override on production entries, which adds a site outside the pin and still lacks the synthetic receipts;
     - waiting for X8b, which covers only the operation.
2. **The per-unit check** (the r4 header; item 7's new "The per-unit check (r4)" paragraph; X9-2's unit line; the forbidden substitute on a dirty matrix pass).
   - **Who checks what.** X9-2 to X9-5 apply the checker's per-run check and its repetition agreement to their own subset of `required-runs.v1.json`. The subset is selected by item 12's case lists.
   - **What changes in the check.** `product.commit` equals the stated base commit, and `worktreeClean` may be false. Every killed point must lie in the census-derived kill set, but full coverage is not required.
   - **X9-6 is unchanged.** The full `check` belongs to X9-6, with a clean committed tree and full coverage.
   - **Who adds it.** X9-2 adds the subset mode as `check-unit`.
   - **It is not a matrix pass.** The reviewed bytes are bound by the unit's review subject manifest.
3. **X8 cross-reference** (the r4 header). X8 r3 items 4b and 4e say that "`crash_matrix_support` still returns no authority type". From r4 on, that sentence reads with the three-entry exception. X8 is not edited; X8b is drafting X8 r4 separately.
   - The two exceptions stay separate, by feature.
   - Neither surface calls the other.
   - There is still one site list.
4. **G1.** The matrix half now has a lawful route. X9-2 closes G1 for its rows.

Everything else in r3 is stated unchanged:
- every mechanism, point, kind, scope, label, evidence member, row, expected value and limit;
- every other forbidden substitute;
- every other law's accepted outcome.

## X6 r4 (record-only; diff against PROPOSAL-r3.md)

Sources: X9 r4 item 6, and X9 r3 G1 ("X6 item 11's [one-line amendment] waits for X6's next revision").
- **The production constructors.** `RecoveryAdmission::admit` and `SettlementSweep::admit` stay the only production constructors of their types.
  - X9 r4's `recovery_admission` and `settlement_sweep` entries are test-only.
  - They run X6's crate-private `admit_on` compositions over X9's synthetic installation.
  - They add no admission step and no home override, and they keep one entry per process.
  - Notes are placed at item 2's read entry and at item 7's step 1.
- **Item 11's cross-crate fixtures (the G1 line owed).** The fresh-process runs take their fixtures and these entries from X9's `crash_matrix_support`. Item 11's in-process tests are unchanged.

## Decide

For each law separately:
- **X9 r4:**
  - Is the amendment sound, narrow, and consistent with X1 items 1 and 7, X6 r3 items 2 and 7, X8 r3 item 4, and X9's item 2 release guards?
  - Do the entries' constraints actually keep them test-only, non-minting and inside the one site list?
  - Is `check-unit` well defined, and is the full `check` at X9-6 unweakened?
  - Is any other accepted outcome changed?
- **X6 r4:**
  - Does it change any accepted outcome?
  - Is each record faithful to X9 r4 and to G1, going no further?
- **Both:**
  - Is each predecessor snapshot exact, and is every accepted sentence preserved?
  - Is anything else wrong?

Write one REVIEW.md and two verdict files, `x9/review.json` and `x6/review.json`. Each must contain:
- "verdict": ACCEPT or REQUIRED-FINDINGS;
- "requiredFindings";
- "noAcceptedOutcomeChanged": true or false (for X9 r4, true means no outcome changed beyond the two stated decisions);
- "subjectSha256": that law's PROPOSAL.md;
- "subject": its path, bytes and sha256;
- the preserved snapshot's path, bytes and sha256.

Do not commit.
