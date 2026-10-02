Grok review: law X9 r10, an amendment found while starting X9-5. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT**.

**Rules:**
- No repository edits, commits, pushes or delegation.
- Write only under /tmp/opensip-implementation/reviews/grok-crash-matrix-x9-r10.
- This is a law review with no product cargo. Run git read-only, against product main `b999ae3` (X9-2 integrated).
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.

## What changed

Pins are in hashes.txt. `crash-matrix-x9/PROPOSAL-r9.md` is the accepted r9: 95579 bytes, `e6ff60c1…`, equal to the r9 review's subjectSha256. Diff PROPOSAL.md against it. The current file also carries r9's existing "r9 ACCEPTED" note, which isn't part of r10.

r10 is a lead decision under the owner's standing direction. X9-5 found that its rows have no lawful route. Item 12 puts them in host's integration target, but:
- `finalize` is `pub(crate)` in a private module (`crates/host/src/finalization.rs` line 395; `lib.rs` `mod finalization;`);
- `maintenance::run` and `sweep_store` are `pub(crate)` in a private module, and `sweep_store` admits natively;
- nothing public calls either one.

There was no X9-5 code and no run. r10 changes four things:
1. **Host's two runners (item 6).**
   - `finalize_commit(at, root, candidate)` calls host's own `finalize`, with `admit` set to `operation(at, root)` and a fixed delivery phase. Delivery faults come only from the `x7.delivery` `fail-before` arms.
   - `store_gc(at)` calls `maintenance::run(settlement_sweep(at))`.
   - Both live in the pinned module, under `crash-matrix` on macOS only, with no new cfg site and nothing widened.
   - Both return value reports only, never an authority type.
   - The one-entry rule and `publish_revocation`'s refusal carry over: a runner makes the process's one entry.
   - Rejected: children in host's unit-test binary; a `#[path]` copy of `finalization.rs` (a second coordinator); a public `finalize`.
2. **The host-only order (items 6 and 12).**
   - A `candidate` child (one entry: `operation`, then `open`) writes X3d-3's candidate to disk as canonical JSON. It then ends refused before `prepare_commit`: no attempt row, SEAL or object.
   - The `finalize` child reads that file, so host's own `finalize` replays before custody (X5 r3 item 3).
   - The ladder's ExecutionId is the `finalize` child's.
   - F01's variants are parent-written inputs from that file.
   - Storage's r5 matrix-only order is unchanged.
3. **A separate host required-runs file (items 7 and 9).**
   - **Evidence:** `check-unit` selects rows by case, and F12, F39, F40 and F53 are named for X9-3 or X9-4 and also for X9-5. With one file, each unit's `check-unit` would demand the other target's rows.
   - X9-5's rows go in `crates/host/tests/fixtures/crash-matrix/required-runs.v1.json`, with the same schema and `clockEpoch`.
   - `check-unit` is unchanged.
   - X9-6's `check` takes both files and both pairs of run sets, with a union census and kill-set coverage across both.
4. **The host census (item 5).**
   - It is the union of two unarmed `finalize` runs, each run twice and equal: (a) a lawful commit, and (b) an exhausted-carrier commit after F32's reserved-slot setup, whose `finish` runs the rollover.
   - A point reached in both takes the larger count.
   - The trace digest is over (a) then (b).
   - The fixture and `candidate` children are excluded.

Also:
- **In-place r10 notes** at item 5 (census), item 6 (after the three entries), item 7 (before the per-unit check), and item 12 (X9-5 and X9-6).
- **Five new forbidden substitutes.**
- **The title** is now r10.
- **X7 r6's session-level tests:** item 12 maps X7a call 16 and X7b call 10 to X9-5 rows. Two of them, `ExistingAttempt` (F34, X9-4's) and the gate-ledger balance, which isn't observable from a run record, stay with X7's next revision.

Nothing else changes: no point, kind, scope, label, evidence member, row, expected value or limit, and no accepted outcome of another law.

## Decide

- Are the two runners a lawful, minimal route?
  - Are they only routes into host's one coordinator and one sweep step?
  - Do they make no new cfg site and return no authority type?
  - Does the one-entry rule hold?
- Does the `candidate` child's order keep X5 r3 item 3 for host's children? Is the on-disk candidate within item 6's "inputs on disk"?
- Is the separate host file lawful under item 7? Is X9-6's union `check` a sound extension?
- Is the two-run host census right under r8's "a unit's census is its own drivers"?
- Does r10 change nothing else? Is anything else wrong?

Write REVIEW.md and review.json under the output directory. review.json needs:
- "verdict";
- "requiredFindings";
- "noAcceptedOutcomeChanged";
- "subjectSha256";
- "subject" (path, bytes, sha256);
- "preservedSnapshot": the accepted r9, `PROPOSAL-r9.md`, 95579 bytes, `e6ff60c1…`.

Do not commit.
