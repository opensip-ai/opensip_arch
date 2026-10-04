Codex review: law X4T r12, the law for unit X4-F2 (the expiry gap in the fenced read). Claude Opus 5.5 leads, and you are the single reviewer. You reviewed X4-F1, the reread half of this gap. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS** on the law. This is a law review. There is no product diff yet; unit X4-F2 is written after the law is accepted.

**Rules:**
- No repository edits, commits, pushes or delegation.
- Write only under `/tmp/opensip-implementation/reviews/grok2-x4t-f2-r1`.

**Lead note (reviewer change).** This request was written for GROK2. **Codex** reviews it, because Codex is free. The directory keeps its name. Write your output under `/tmp/opensip-implementation/reviews/grok2-x4t-f2-r1`. Don't run cargo, and don't run any crash-matrix set.

- No cargo, tests or crash-matrix sets are needed. If you want a run, say so in your review and the lead will run it.
- Run git read-only.
- Run any command at `nice -n 19`, with a private 0700 `TMPDIR` under `$(getconf DARWIN_USER_TEMP_DIR)`.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.

## Subject

- **The law:** `/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/trust-admission-x4t/PROPOSAL.md`, r12. Its size and sha256 are in `hashes.txt` beside this request.
- **The diff base:** `PROPOSAL-r11.md` in the same directory, 53342 bytes, sha256 `7fe098fd30de298cf1e09ca6514d8a50eef6a328cb25bda6ebcf4398353cd384`. These are exactly the accepted r11 bytes, the `subjectSha256` of `reviews/grok-trust-admission-x4t-r11/review.json`. Diff with `diff -u PROPOSAL-r11.md PROPOSAL.md`.
- **The live r11 file** (arch `5b506b59b`, before r12) was those bytes plus one acceptance sentence, which said "r11 ACCEPTED by Grok on 2026-10-03". The acceptance commit, `846071458`, is dated 2026-10-01, and so is M2-COMPLETE's X4T row. r12's header records 2026-10-01 and notes the slip.
- **Evidence:** in `evidence/`, pinned in `hashes.txt`:
  - `x9-rows.py` computes item 13's X9 selection from the product's required-runs files and checks it against the harness's prefix rule. It is read-only and writes nothing.
  - `x9-rows.json` is its output on product main `218465f`.

## Why X4T, and not X4 or X4B

The gap lies in X4T's own items:
- the fenced first read (item 9);
- its time admission and write-ahead (items 6 and 7);
- its refusal rows (item 10).

Neither of the other laws needs a change:
- **X4B r5 item 4** supplies the mapping, which r12 applies unchanged. Its confirming admission now also clocks, at the acceptance's own tEval, so its outcome does not change (the r12 note).
- **X4 r7** already routes the case. Item 8 gives X4T's own rows for "no admitted current trust" at the lease-free point, and its r5 note says `Continuation::Refuse` stays X4T's admission refusal there.

## The record

- **M2-COMPLETE r3 §5 row 23 (accepted).** "X4-F2. The fenced read computes the expiry flags but never applies them, which X4T-a r1 call 6 accepted. A store already expired at the handoff is admitted, then fail-stops at its first tick or checkpoint. The fix publishes the continuation row at the lease-free point."
- **EXIT-PLAN** ("Follow-ups found by X4-F1") says the same.
- **M3-PLAN r9** (`m3/M3-PLAN-r9.md:282`, P5-4 at `:770-773`): X4-F2 is an X4T successor, provisionally sized M plus one lead set, that must land before J2b.
- **Your X4-F1 r1 review,** judgment call 6: "The fenced branch still returns the stored roles and the standing taken before the clock … A store already expired at the handoff's tEval is admitted there; the first reread, at T ≥ tEval, applies the clock. Whether the fenced read should publish item 10's continuation row is outside this unit." Your "Not in this unit" list is: the fenced read's own `EV-CLOCK`, expiry detected before the next read, native scheduling of the 5 s and 10 s bounds, and Linux.

## What r12 decides

The table "r12 changes" at the top of the law lists every edit. The semantics:

1. **Expiry at the fenced read (item 6, lead decision).**
   - **The instant** is tEval: S4 step 5's admitted instant (`TimeAdmission.evaluation`), whose floor item 7 writes. It is never W, never F, and never a monitor sample.
   - **The states** are S4's three, as `finish` computes them (`TimeAdmission.expired`). The rule is `expiry_states`, the same one X4-F1's reread uses.
   - **The mapping** is X4B r5 item 4's, through `role_machine::clock` (`decide(Event::Clock)`), exactly as X4-F1's `clock_roles` applies it.
   - **The join.** Then the role machine's second join:
     - root expiry gives `core:expired`;
     - staleness gives `core:stale-revocation`;
     - with both, expiry wins;
     - a catalog expiry alone gives `ExistingOnly`, which is admitted.
   - **Placement.** It is the admission's last decision, after every refusal of items 2 to 5 and after S4's own refusals.
   - **Nothing is recorded.** No `EV-CLOCK` is written, and no stored role state is rewritten. The view carries the clocked states and standing.
   - **Report-only** computes the same result and writes nothing.
2. **The write-ahead comes before the clocked refusal (item 7, lead decision).**
   - **Why.** S4 step 5 requires the floor equal to tEval before any decision at tEval is used, and an expiry refusal is decided at tEval. S4's refusals in steps 1 to 4 write nothing because no instant is admitted yet.
   - **What happens.** The fenced read performs item 7's write-ahead exactly as for an admitted view, and then publishes the continuation row instead of returning the view.
   - **The hold after the refusal** matches X4B-b's refusal after a recorded acceptance. The owner advances inside the read, the gate step fails and is spent, and the refusal is never relabelled.
   - **Rejected:** refusing before the write. With the wall clock set back, a later read would evaluate earlier and admit the store, which is weaker than r11 as built: r11 admits such a store, so its write-ahead already runs.
3. **Rows (item 10, lead decision).** The clocked refusal takes the existing continuation row: `CONTINUE-CORE-NOT-TRUSTED`, request-rejected, exit 2, `EXTENSION.ADMISSION_REJECTED`, with subject `core:expired` or `core:stale-revocation`. Both subjects are already published for stored states.
   - **A final root expired at tEval** takes this row, never `ROOT.FINAL_EXPIRED`. The view authenticates its chain without time (`trust_ordinary_roots::authenticate_shared` → `verified_root_chains::authenticate_root_chain`), so the root's expiry reaches the view only through S4's first state.
   - **At the handoff** this is the existing `trust_termination` mapping to `TrustContinuation`.
   - **No new code or subject.**
4. **Composition with X4-F1: each read clocks once (item 6).** Each read clocks the stored states of its own capsule, once, at its own instant.
   - **The fenced read** clocks at tEval.
   - **A reread** clocks at T = tEval + elapsed, over its own capsule, never over the start view's clocked states. The start view's roles and standing feed neither the reread nor X4's S6 predicate, which compares the epoch, floors and closure.
   - **Monotone.** S4's states are monotone in the instant and `Clock` is idempotent, so for the same documents a reread is never in better standing than the fenced read. A double application would equal a single one at T, but r12 still forbids it.
5. **X4-F2, the code unit (item 13).**
   - **The changes.** `admit_bound`'s fenced branch clocks after S4's refusals, and the refusal travels with the pending write. `fenced_first_read` publishes the refusal where r11 returns the view.
   - **Test fixtures.** X4T-0 gains three `cfg(test)` knobs: a later issue time for one document, the root's `expiresAt`, and the catalog's `expiresAt`. They are needed because the default store's A is the list's issue time, so S4's plausibility bound keeps a fenced read off every boundary.
   - **The controls** are X4-F1's lanes.
6. **X9 (item 13, lead decision): no row moves and none is added.**
   - **Why no outcome moves.** X9 r16 item 3's scripted wall (2026-10-04 plus 3600 s per ordinal) stays inside every validity window of the matrix's stores. The nearest boundary is 2026-12-30T00:00:00Z.
   - **The regression subset,** by X4-F1's method:
     - storage, 54 rows, all F00: 34 kill inside `x4t.floor-publication`, and 20 kill at `x3b.floor`, the first durable points after the fenced read returns;
     - host: no row, so the host census runs alone;
     - both censuses.

     It runs as two sets through `x9_6_matrix`, compared field by field with the accepted X9-6 evidence by X4-F1's `compare.py`.
   - **Excluded:** X4-F1's tick-armed rows and checkpoint kills, because the reread and the S6 predicate's inputs are unchanged.
   - **The basis still holds.** At `218465f` the X9 harness sources are byte-identical to X9-6's C `3d2d5b5`. The security, storage, host and platform crates are unchanged since `15c0779`.
7. **Deferred (Not claimed):**
   - expiry detected between reads;
   - native scheduling of the 5 s and 10 s bounds;
   - recording `EV-CLOCK` transitions;
   - Linux (already not claimed);
   - F9. F9's date does not move: r12 makes self-constructed stores refuse at the fenced read from 2026-12-30T00:00:01Z, the second X4-F1 already moved rereads to.

## Evidence (product main `218465f`, read-only; pins in `hashes.txt`)

**The fenced read and the reread**
- `crates/security/src/trust/current_trust_admission.rs`:
  - `ReadMode`, `:153`;
  - `standing_of`, `:922`;
  - `clock_roles`, `:951`;
  - `admit_bound`, `:969`: the stored-state join at `:981`; the fenced branch at `:1026-1059`, which returns `(roles, standing, Some(admission))` unclocked; the reread branch above it, clocked.
- `crates/security/src/trust/floor_publication.rs`:
  - `needs_write`, `:744`;
  - `fenced_first_read`, `:945`: check 3 at `:972`, and the write-ahead at `:974-989`, which runs only on an `Ok` view.
- `crates/security/src/trust/live_observation.rs`:
  - `fenced_operation_read`, `:113`, whose confirmations are returned only with a view;
  - `classify`, `:432`;
  - `predicate`, `:678`, which reads the start view's epoch, floors and closure.

**The bootstrap path and the role machine**
- `crates/security/src/trust/trust_bootstrap.rs`:
  - X4B-a's per-role clock inputs, `:639-656`, the same mapping as `clock_roles`;
  - `first_read_sequence`, `:1199`;
  - `bootstrapping_first_read`, `:1229`.
- `crates/security/src/trust/trust_bootstrap_tests.rs:1139-1157`: the precedent, an acceptance recorded, then a continuation refusal, with one confirmation on the owner.
- `crates/security/src/trust/role_machine.rs`:
  - `continuation`, `:56`;
  - `decide`'s `Clock`, `:200-208`;
  - `clock`, `:294`.

**Time and the root chain**
- `crates/security/src/trust_time.rs`:
  - `finish`, `:136`;
  - `expiry_states`, `:181`;
  - `admission_of`, `:495`;
  - `evaluate_retained_ordinary`, `:590`;
  - `evaluate_reread_expiry`, `:617`.
- `crates/security/src/trust/verified_root_chains.rs`: `verify_root_chain` (timed), `:18`; `authenticate_root_chain` (time-free), `:32`; `FinalExpired`, `:183`.
- `crates/security/src/trust_ordinary_roots.rs:268`: `authenticate_shared`, the view's path.

**The handoff and the gate**
- `crates/security/src/custody/operation_handoff.rs`: `trust_start`, `:997`; `begin`'s lease-free order, `:1170-1180`, where the trust start runs before X3b's floor step and the lease.
- `crates/security/src/custody/operation_guard.rs:646`: `trust_termination`.
- `crates/security/src/custody/ordinary_writer.rs:314-345`: `gate_step`, which spends the gate on a failed step, with no recheck.

**Fixtures and the crash matrix**
- `crates/security/src/trust/accepted_store_fixture.rs`: the default dates. The list is issued 2026-10-01, the catalog expires 2027-04-01, and the root expires 2027-10-01. Self-constructed stores have F = L = 2026-10-02.
- `crates/security/src/trust/current_trust_admission_tests.rs:280-311`: X4-F1's reread boundary test.
- `crates/storage/tests/fixtures/crash-matrix/required-runs.v1.json` and `crates/host/tests/fixtures/crash-matrix/required-runs.v1.json`.

**The laws, the record and the X9 evidence** (arch)
- Security contract S4: `docs/v2/contracts/product-v1/security-and-lifecycle.md:333-377`.
- `trust-bootstrap-x4b/PROPOSAL.md` (X4B r5): items 1 and 4.
- `live-guards-x4/PROPOSAL.md` (X4 r7): item 8 and the r5 note (`:157-166`).
- `crash-matrix-x9/PROPOSAL.md` (X9 r16): item 3's scripted wall clock.
- `reviews/grok2-observer-expiry-x4f1-r1/`: `REQUEST.md`, `REVIEW.md` and the `evidence/` scripts. Item 13 reuses its method.
- `reviews/grok-current-trust-x4ta-r1/REVIEW.md`: call 6.
- The X9-6 evidence: `crash-matrix-x9/evidence/3d2d5b5a5e5cabd1768b02e29eb3c0928264fb4f/{storage,host}/matrix.json`.

## Decide

1. **The diff.** Diff r11 to r12 and confirm that only the places in the "r12 changes" table changed, and that the r11 text stands everywhere else.
2. **Item 6.** Is `EV-CLOCK` at tEval on the fenced read the law S4 requires ("fail closed at tEval")? Are the instant, the three states, the mapping and the placement after S4's refusals exact? Is a view-only clock, with nothing recorded, right?
3. **Item 7.** Is the write-ahead before a clocked refusal what S4 step 5 requires? Is the hold after the refusal sound: the owner advanced, the gate spent, and no relabel as `required-files-changed`? Is the rejection of refusing before the write right?
4. **Item 10.** Is the continuation row, with `core:expired` or `core:stale-revocation`, the right route? In particular, is "never `ROOT.FINAL_EXPIRED` for a final root expired at tEval" consistent with S5 and with your X4T-a r1 call 6?
5. **Composition.** Is "each read clocks its own stored states once, at its own instant" sound with X4-F1's reread? Is there any path that applies `EV-CLOCK` twice, or that lets the start view's clocked state leak into a reread or into X4's S6 predicate?
6. **X4B.** Is the claim right that the confirming admission's clock, at the acceptance's tEval over the same documents, changes no X4B outcome?
7. **X9.** Is "no row moves, none is added" right? Is item 13's subset (54 storage rows, the host census alone, both censuses), compared against X9-6, sufficient by X4-F1's method? Should any row be added?
8. **Tests and the unit.** Do item 12's r12 cases pin each boundary, the write-before-refusal, stickiness, report-only and the handoff outcome? Are X4T-0's three test-only knobs the right means?
9. **Deferrals and cross-law.** Are the r12 Not-claimed items and the r12 note (no X4, X4B or X9 amendment) right?

Write REVIEW.md and review.json under the output directory. review.json needs:
- `"verdict"`: `ACCEPT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`;
- `"subjectSha256"`: the r12 `PROPOSAL.md` sha256 from `hashes.txt`, as a single string.

Do not commit.
