# The CommitSession storage facade — proposal X3d r9

2026-10-01. Claude Opus 5.5, implementation lead. Law for unit X3d of `EXIT-PLAN.md`, under owner.md §5 and §8, the build plan's "Decision: require independently minted prerequisites at the storage boundary", "Security/storage ownership and the final commit gate" and "Publication sequence and lock discipline" (`docs/v2/architecture/implementation-boundaries-and-build-plan.md`, lines 25–190), and the accepted laws X1 r1, X2 r5, X3a r5, X3b r6, X3c r7, X4 r7 and X4T r5. The lead decisions here are made under the owner's standing direction of 2026-09-30 to proceed on the lead's recommendation. Each names the alternative it rejects. r2 answers Grok X3d r1 RF-1 to RF-5: the capacity threshold, the attempt-admission commit's outcomes, a single end-path REV owner, an end-path reserve taken first, and the exhaustive rows. r1 bytes are preserved in PROPOSAL-r1.md. r3 answers Grok X3d r2 RF-1 (a failed end-path reserve funds no append) and RF-2 (after an uncertain journal outcome, the writer reconciles before any floor copy). r2 bytes are preserved in PROPOSAL-r2.md. r3 ACCEPTED by Grok on 2026-10-01. r4 is an amendment required by X3b r8 item 5a: item 3's capacity threshold is X3b's `seal_fits` predicate (a SEAL needs the proven tail at most 9007199254740987), not the literal 9007199254740990. r3 bytes are preserved in PROPOSAL-r3.md. r4 ACCEPTED by Grok on 2026-10-01. Not code. Library only: no CLI command commits (X11 and M3).

**r5 (2026-10-01) is an amendment required by X3b r9** (item 5's uncertain-outcome rule, which is reviewed together with this revision). r4 bytes are preserved in PROPOSAL-r4.md. r5 ACCEPTED by Grok on 2026-10-01.
- **The defect.** r3 and r4 item 7 step 1 had `finish` reopen the carrier and run `reconcile_witness` after an uncertain journal commit or barrier, before releasing the lease. That work is charged to X1's attempt ledger (item 8). The attempt ledger is the platform's failure-latching `WorkLedger`, and the failure after visibility has already closed it. So the reconciliation is refused `Closed` before it reads anything, and could never run. X3d-1 would meet this at its first uncertain-outcome test.
- **The change (items 4, 7 and 8).** After an uncertain journal outcome, `finish` appends nothing, reconciles nothing and runs no end step. It releases the lease and stops. The next writer's floor step and carrier start reconcile the carrier before its next use (X3b r9 items 3, 4 and 5).
- **Rows.** No outcome or row changes. `CommitUndetermined { executionId }` stays on item 9's durability row. r4's reconciliation never changed that outcome either; it only decided whether the floor copy ran.
- **X7.** X7 r3 item 5's parenthetical "(X3d item 7 reconciles under the lease and copies the floor only on OK, REVERT or ADVANCE)" describes r4. X7's next revision corrects it to "finish appends nothing and copies no floor; the next writer reconciles". X7's projection, row and remedy are unchanged, and X7 r3 item 6 already says the rollover's uncertain append is "reconciled by the next writer's start".
- **Unchanged from r4:** everything else.

**r6 (2026-10-01) decides the question r5 disclosed and left open: the end-path `REV` after a certain refusal that closed the attempt ledger.** r5 bytes are preserved in PROPOSAL-r5.md. r6 ACCEPTED by Grok on 2026-10-02. It is reviewed together with X3b r10, which makes the matching change in the journal law.
- **The defect.** Item 8 says the end-path reserve "survives every later refusal", and item 7 has `finish` append F19's `REV`, and `CLN` where required, after certain refusals. The attempt ledger is the platform's `WorkLedger` (`crates/platform/src/work_ledger.rs` at 6dd7363). Any `Err` or unwind in any nested scope sets `failed`, and every later `scope`, `charge`, `run` or `effect` returns `Closed`. Most certain refusals in this composition are such failures. Examples: busy at the evidence ledger's `BEGIN IMMEDIATE` (`begin_prepared_ledger` returns it from inside `work.run`), a staging I/O error, a failed repeated checkpoint, and a publication-reserve overrun. The funded `REV` would then be refused `Closed` before it opened the carrier, and a durable SEAL would be left without its revocation, contrary to F19.
- **A second gap under the first.** The platform has no reservation that outlives a call. `effect`'s `ReservedPostchecks` exists only inside its closure. So "a reserve held by the session" (item 3 step 0, accepted since r2) has no platform form at 6dd7363 either.
- **The change (items 1, 3, 4, 7, 8, 9 and 13, and the forbidden substitutes).**
  - A settlement reserve in `WorkLedger`, from a new platform unit, X3d-0. It is taken once, at item 3 step 0, before the first attempt effect, in the same attempt ledger, sized at the exact `REV` and `CLN` append cost.
  - It stays spendable after the ledger latches, but only through `WorkLedger::settle`. Only `StoppedSession::finish` holds the typed capability that reaches it.
  - It cannot be refilled. It is spent at most once, and its own failure latches.
  - It is forfeited at any uncertain outcome.
  - The end step does not run on a closed attempt ledger.
- **Widened from r5 (lead decision).** r5 forbade the end-path append only after an uncertain *journal* outcome. r6 forfeits the reserve after every uncertain outcome: a journal commit or barrier, the attempt-admission `COMMIT`, or the evidence `COMMIT`. After any of them nothing follows (item 8).
- **Rows.** No outcome or row changes. A failed end-path append is an end failure on its existing X3b item 8 row and never rewrites the outcome (item 9). X7 r3's projection is unchanged.
- **Unchanged from r5:** everything else.

**r7 (2026-10-04) is record-only.** r6 bytes are preserved in PROPOSAL-r6.md. r7 ACCEPTED by Grok on 2026-10-04. It records decisions already accepted in other laws and unit reviews. It changes no decision, outcome, row, type, lock order, budget or forbidden substitute of r6, and no accepted outcome of any other law. The r6 sentences it touches stay in place, each followed by a short "r7 (record)" note that points here.
- **Compile-fail evidence: X8's fixtures, not doctests (X8 r3 items 1 and 2).** Item 11's "pinned by `compile_fail` doctests on the public types" and item 13's "the X8 doctests" for X3d-2 are superseded by X8's isolated compile-fail fixtures.
  - **The lane.** The fixtures live under `crates/host/tests/refusal/cases/`. The X8a driver in `crates/host/tests/admission_tests.rs` runs them with the pinned toolchain inside the documented `cargo test --locked --offline --workspace --all-targets` lane. Each case pins its error code, message fragment and line against a compiling control.
  - **Doctests.** A doctest may still illustrate a type, but it is never cited as evidence. On stable rustdoc, a `compile_fail` doctest passes on any error, and the documented lane never runs doctests (X8 r3, trial items 1 and 2).
  - **Who added which cases.** X3d-1 and X3d-2 added their cases as X8 fixtures: X8 r3 item 3's owner rows for `CommitSession`, `JournalWriteTxn`, `JournalSealBinding`, `StoppedSession`, `PreparedCommit` and `PublishedCommit`, the `open` arity case, and group H.
- **The adapter source pin (X8 r3 item 3b).** Item 11's case "passing a caller-implemented adapter or `SealOutcome` to storage's facade" splits in two.
  - **Compile-fail.** Storage's facade takes no adapter and no `SealOutcome`. That is pinned by group H (E0061 on `publish(adapter)` and on a three-argument `prepare_commit`).
  - **Source pin.** Rust visibility cannot confine the implementations of security's adapter trait, or the callers of `begin_journal_txn` and `seal_under_append_lock`, to one sibling crate. So that confinement is pinned by source, not by compile-fail. The pin is in `admission_tests.rs` and was added by X3d-2. As accepted in the X3d-2 review (call 12):
    - **Names.** It covers `CommitAdapter`, `StagedCommit`, `begin_journal_txn` and `seal_under_append_lock`.
    - **Where they may appear.** In production code, only in security's `custody/commit_session.rs` and its root `lib.rs`, and in `crates/storage/src/commit.rs`. Production code is every `.rs` under `crates/*/src` except files named `*_tests.rs` or `tests.rs`, with comments stripped. A use anywhere else fails.
  - **What a bypass could reach.** A caller that got around the pin could reach at most a durable SEAL without an evidence commit, which is F36's and F38's recoverable state. It still could not reach authority, because only storage constructs `PublishedCommit`.
- **Where cross-crate tests get their fixtures (X8 r3 item 4g; X9 gap G1).** Item 12's "only through crate-private, `cfg(test)` fixtures" cannot be met across a crate boundary, because Rust sets `cfg(test)` only for the crate under test.
  - **Ordinary lane.** Storage's and host's tests obtain a `ProjectOperation` through the `scenario-fixtures` feature. Only `[dev-dependencies]` enable it.
  - **Matrix rows.** These obtain theirs through X9's `crash-matrix` feature.
  - **One site list.** Both features reach a single shared site list: X8 r3 item 4b's list. It is X9-1's source pin, extended by name by X8b. Every site on it is written `cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))`.
  - **The forbidden seam still holds.** The forbidden "production seam that supplies a `ProjectOperation`" stands, because both features are absent from every release build (X8 r3 item 4f; X9 item 2).
- **Ordering: X3d-2 before X8b and X9-1 (lead decision, accepted in the X3d-2 review, call 1).**
  - **What landed.** X3d-2 integrated before X8b and X9-1. Its storage tests take no `ProjectOperation`. They run the storage functions that `prepare_commit` and `publish` compose, on a scratch `I/stores/S`, with a real replay and no session. X3d-1's tests cover the session half.
  - **The first end-to-end test.** `prepare_commit` and `publish` with a real `CommitSession` are first tested together by X8c's B0–B4, then by X9-2's matrix.
  - **What this leaves unmet.** No X3d requirement of the unit. X8 r3's unit-list sentence that X8b "lands before X3d-2" described storage tests that X3d-2 does not contain.
- **`ExistingAttempt` after X6 (X6 r3 items 2 and 6).** X6 r3 item 6 superseded "before X6 exists" for `ExistingAttempt`. That covers item 3 step 5's "Until X6 exists, `ExistingAttempt` terminates on the invariant row" and item 9's invariant-row entry "`ExistingAttempt` before X6 exists".
  - **The row.** The invariant row is the writer's permanent projection of `ExistingAttempt`. A writer's invocation has spent its one attempt and receipt on the write entry, so it can never recover (X1 r1 items 1 and 7).
  - **The variant.** It carries the requested binding: `NotPrepared::ExistingAttempt { execution_id, requested: RequestedBinding }`. Storage builds the binding from the plan it was about to write, never from a read (X6 r3 item 2, X6b).
  - **Who acts on it.** Finalization discloses the binding (X7 r4 item 3). A later read-entry invocation recovers the attempt.
  - **Item 3 step 5's routing.** Its "for the host to route to read-only recovery (X6)" is met by that disclosure and the later invocation.
  - **What stays the same.** The row, its code and its detail.
- **A known limit, left as follow-up for an X3c successor (X3d-2 review, call 8).** Re-committing a Run that is already committed in the same store and namespace (S, N) is refused at staging, on the invariant row.
  - **Why.** X3c-2 stages the initial availability record unconditionally. identity-and-evidence allows a duplicate retry to share a Run under a separate attempt receipt.
  - **The fix.** An X3c successor that stages availability only when none exists.
  - **Why it can wait.** M2 never commits one Run twice. This is a disclosed limit, not a change to X3d.
  - **r9 (record): lifted in law by X3c r8.** X3c r8 is the successor this bullet names. The product still refuses until X3c-3 integrates (X3c r8 item 13). X3c r8's rule differs from "The fix" above in one case: a Run that has Run material but no availability record. X3c r8 refuses it `LEDGER.CORRUPT` and does not stage a new availability record (X3c r8 item 6a.2). See the r9 header.
- **Unchanged from r6:** everything else.

**r8 (2026-10-02) is an amendment.** It fixes item 3 step 1's closure binding, which no real Run could meet. r7 bytes are preserved in PROPOSAL-r7.md. r8 ACCEPTED by Grok on 2026-10-02. It is reviewed together with the identity contract successor EC1 (`core-evaluator-closure-ec1/`) and the record-only X9 r7. The decision is the lead's, made under the owner's standing direction of 2026-09-30. It is flagged to the owner, who may override it, because EC1 gives every core release a new evaluator closure and so new PlanIds and RunIds.
- **The defect (found by X9-2; EXIT-PLAN "BLOCKER: commit closure binding").** r7 step 1 said: "Its evaluator closure equals the session's selected core closure." At a36da7c, `plan` (`crates/storage/src/commit.rs`, lines 248–256) enforces `run.evaluator_closure() == session.core_closure()`. The two sides can never be equal:
  - **The session side.** `core_closure()` is `InitialCore::closure()`, the authenticated core inventory's `closure2:` over a descriptor with `kind: "core"` (`crates/security/src/trust/core_inventory.rs`, `bind`).
  - **The Run side.** Replay requires the seal's `evaluatorClosure` to name a retained, Plan-selected closure with `kind: "evaluator"` (`crates/evaluator/src/execution_inputs.rs`, `capture_header`; `execution_reader.rs`).

  So `prepare_commit` refuses every real `ReplayedRun` on the invariant row. X3d-2's tests did not catch it, because their `bound()` took the closure from the Run itself (`crates/storage/src/commit_tests.rs`, `bound`), and the project too.
- **Why the design did not decide it.** The build plan binds the session to an "admitted producer closure" (line 51), and storage compares "producer selections" (line 67), without saying which closure that is. No accepted text relates the core closure to an evaluator closure. No authenticated record names one either: the core inventory has no evaluator member, and an admitted component manifest is `kind: "component"`, `role: "analyzer"`. r1 read "admitted producer closure" as "the receipt's selected core closure", and this defect follows from that reading.
- **The change (items 1, 2, 3, 12 and 13, and the forbidden substitutes).**
  - **EC1 defines the value.** A core release's evaluator closure is `closure2:` + H("closure", the authenticated core descriptor with `kind` = `"evaluator"`). For that kind, `manifestDigest` is the raw SHA-256 of the TR-CORE-signed inventory body. The core closure and the core evaluator closure differ only by `kind`.
  - **The session carries it.** Security derives it from the same authenticated inventory as the core closure, and the session exposes it as `CommitSession::core_evaluator_closure()`.
  - **Step 1 compares against it.** "Its evaluator closure equals the session's core evaluator closure, derived by security from the same authenticated inventory as the core closure." The core closure keeps every other use: the store pair, X4's closure subjects, and live revocation.
  - **Where the session's value comes from.** It is never read from the Run, a worker claim, a build-time string or a test binding.
- **Rows.** No outcome, row, code or detail changes. A mismatch is still item 9's invariant row, as a broken caller.
- **Rejected:**
  - **Fix (a) without a definition.** "The session exposes the evaluator closure the core admits" has nothing to expose: no authenticated record names one.
  - **Fix (b), a membership test.** "The core closure contains the Run's evaluator closure", by a tree subset, is stated nowhere. It leaves `manifestDigest`, version and platform unbound, and is a weaker new identity law.
  - **A signed core-inventory member naming the evaluator closure.** It changes the signed release format and 463h's builder, and still needs EC1's rule.
  - **The evaluator as a TR-COMPONENT component.** It contradicts "evaluator = pure core" (D1-plan G28) and the analyzer-only component role.
  - **Admitting kind `core` in replay.** It breaks the identity contract's `closureKinds`.
  - **Dropping the check.** It removes the build plan's producer-selection comparison (line 67).
- **Unchanged from r7:** everything else.

**r9 (2026-10-04) is an amendment: J1's successor S10, with X3c r8's CL-1 recorded beside it.** r8 bytes, as accepted (sha256 `5e491b92…`, without the acceptance note), are preserved in PROPOSAL-r8.md. **Draft r9, not accepted.** Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the overnight autonomous run. Not code.
- **Its two parts.**
  - **S10 (the main part; amendment).** J1 r5 item 8 closes S-OP-12, the commit-phase cancellation join, and writes its X3d half as successor S10 under the name "X3d r9" (J1 r5:80, :512, :651-658, :856). M3-PLAN r9 assigns X3d r9 S10 and CL-1 together (M3P:317). S10's decisions are J1's, accepted by Codex. This revision carries them into X3d in its own section, "S10 (r9)", after item 13. Where the consumers leave X3d's side open, it adds lead decisions LD9-1 to LD9-6.
  - **CL-1 (record).** X3c r8, the re-commit law, was accepted by GROK2 on 2026-10-04 with no findings (`ledger-blob-x3c/PROPOSAL-r8.md`, sha256 `ba638efb…`; `reviews/grok2-ledger-blob-x3c-r8/`). Its cross-law item CL-1 (X3c r8 item 16) finds that among accepted law, only this law's step 3.8 conflicts with it. CL-1 asks X3d's next revision to restate the step, and says "No X3d rule changes."
- **The consumers it is written for** (accepted snapshots): J1 r5 (`m3/host-pipeline-j/PROPOSAL-r5.md`, `4ccb2320…`); M3-PLAN r9 (M3P, `m3/M3-PLAN-r9.md`, `72bc7a13…`); X3c r8 items 15.1 and 16; M3-L r5, accepted in review (`m3/provider-protocol-l/PROPOSAL-r5.md`, `f654ee4e…`), items 16f and 18.
- **What it changes.**
  - **S10** changes items 1, 2, 5, 6, 7, 8, 9, 11 and 13 and the forbidden substitutes, as J1 r5 decided and the S10 section states. It adds:
    - one stop cause (`StopCause::Operator`), one `REV` reason (`operator`) and one row ("operator stop");
    - one security type (`CancellationLatch`), one session method (`take_cancellation_latch`), and the session step that opens the latch's window (LD9-1);
    - one read-only `StoppedSession` accessor (`admitted_at_close`; LD9-3).

    The session's ExecutionId becomes a `ReservedExecutionId`. S10 adds no crash point, outcome variant, code, class, exit or detail, and it changes no lock order or budget.
  - **CL-1** changes no decision, outcome, row, code, detail, type, lock order, budget, crash point or forbidden substitute of r8.
  - Neither changes an accepted outcome of another law. As in r7, every r8 sentence either part touches stays in place, followed by a short "r9 (S10)" or "r9 (record)" note.

**r9 changes.**

| # | Change | Where | Source |
|---|---|---|---|
| 1 | **S10, the commit-phase cancellation join (amendment).** A third latch source for the operation's `FinalGate`: `take_cancellation_latch`, minted once per operation, usable only in a window that opens when the attempt row commits, stays open across `Ok(PreparedCommit)`, and closes only where a `StoppedSession` is produced. `StopCause::Operator`, the `REV` reason `operator` (reserve unchanged), the row "operator stop" (`InstallationTermination::Interrupted { signal }`), the `refused()` record, `open`'s ExecutionId reservation, units J3a and J3b, X9 rows S12-B, -C and -U, and new forbidden substitutes. Lead decisions LD9-1 to LD9-6. | the S10 section; notes in items 1, 2, 5, 6, 7, 8, 9, 11 and 13; the forbidden substitutes | J1 r5 items 2, 7, 8.1 to 8.7, 12 to 14 (S10, J3a, J3b); M3P:317; X3c r8 item 15.1; M3-L r5 items 16f and 18 |
| 2 | **Step 3.8 restated (CL-1).** Availability and pins are staged on a Run's first commit in (S, N) only. A re-commit of an already-committed Run stages neither. | item 4 step 3.8 | X3c r8 item 6 (its r8 bullets); items 6a.2 (R8-2), 6a.4 (R8-4) and 6a.5 (R8-5); item 16, CL-1 |
| 3 | **The r7 known limit is lifted in law.** X3c r8 is the successor the limit named. The product lifts it when X3c-3 integrates. | the r7 header's known-limit bullet | X3c r8 items 6a.2 and 13; CL-1 |
| 4 | **X3c r8's re-commit refusals**, on rows item 9 already has | item 9 | X3c r8 item 10 |
| 5 | **X3c-3 changes doc comments in X3d-2's `commit.rs`**, and nothing else of X3d's | item 13, the X3d-2 line | X3c r8 items 6a.9 and 13 |
| 6 | **X3c r8's other references to X3d**, each checked; none changes X3d | this header | X3c r8 items 6a.1, 6a.8, 6a.9, 10, 12b, 14, 15.1 and 15.3 |
| 7 | **Crash windows and controls under CL-1:** no change implied. S10's are in its own section (S10.9). | this header | X3c r8 items 6a.9, 12b and 14 |
| 8 | **XL-1, S10 and the number "X3d r9": resolved.** Lead decision: S10 is folded into r9. | this header | J1 r5 items 8 and 13; M3P:317, :364; X3c r8 items 15.1 and 16; M3-L r5 items 16f and 18 |

**CL-1: standing, as X3c r8 decides it.** R is the Run's RunId. (S, N) is the attempt's store generation digest and namespace, the key of every per-Run row.
- **The read.** Inside the open level-3 ledger transaction, before any insert, X3c's staging reads R's committed per-Run rows only: R's current availability record, and whether any Run-material row names R (X3c r8 item 6a.2, R8-2).
  - **Neither exists: R's first commit** in (S, N). Staging stages the availability record (generation 0 `retained`) and the pins as a first publication, as r8's step 3.8 says.
  - **Both exist: R is already committed, and this is a re-commit.** Staging stages no availability record and no pin change (X3c r8 item 6a.4, R8-4; item 6a.5, R8-5). The re-commit's manifest and inventory must equal R's committed Run material byte for byte (item 6a.3, R8-3).
  - **Exactly one exists:** refused `LEDGER.CORRUPT` (item 6a.2; item 9's r9 note).
- **On every commit,** staging still stages the receipt and association pair (`stage_recovery_pair`), the Run material and its object references, each keyed by the attempt's own ExecutionId (X3c r8 item 6a.6).
- **"Already committed" means a landed `COMMIT`.**
  - An attempt that stopped before its `COMMIT` landed (an orphan `SEAL`) leaves no per-Run row. The next commit of R is a first commit (F36; X3c r8 item 6a.2).
  - A commit whose `COMMIT` landed makes R already committed, whatever its attempt phase, including one reported `CommitUndetermined`. The re-commit does not act on that earlier attempt, which stays X6's (X3c r8 item 6a.2).
- **What X3d keeps.**
  - The facade, its types and outcomes, item 4's order and its stop order are unchanged (X3c r8 items 6a.9 and 15.3).
  - A lawful re-commit returns `Committed(PublishedCommit)` with its own receipt, as a first commit does (X3c r8 item 6a.1, R8-1).
  - No outcome tells the two apart. X3c r8 rejects a `ReCommitted` outcome (item 6a.9).

**The r7 known limit.** Its r9 note is in the r7 header. The limit is lifted in law by X3c r8. The product refuses as before until X3c-3 integrates (X3c r8 item 13). X3c-3 is not integrated at product main `cca4fe4`.

The r7 bullet sketched the fix as "stages availability only when none exists". X3c r8 differs from that sketch in one case. It decides standing from both of R's per-Run rows. A Run whose material exists without its availability record is refused `LEDGER.CORRUPT`, never given a new generation 0 (X3c r8 item 6a.2, which rejects "treating a one-sided Run as a first commit"). That decision is X3c's. X3d records it and decides nothing.

**X3c r8's other references to X3d.** Each was checked against r8. None changes X3d.

| X3c r8 | What it says of X3d | In r9 |
|---|---|---|
| item 6a.1 | A re-commit draws a fresh ExecutionId (X3d item 2). It ends `Committed(PublishedCommit)` as a first commit does (item 6), built only after its own `COMMIT` returned success (item 1). | unchanged |
| items 6a.8 and 10 | A refused re-commit is a staging refusal after the durable `SEAL`. X3d's stop order and `finish`'s `REV` and `CLN` follow (items 4 and 7). | item 9's r9 note; items 4 and 7 unchanged |
| item 6a.9 | `prepare_commit`, `publish`, `CommitOutcome` and `PublishedCommit` are unchanged (items 1 and 6). There is no new crash point. `commit.rs` still builds the initial availability record and the empty pin set. | unchanged |
| item 12b | X3c-3's composition tests go through this facade with a real session, obtained through `scenario-fixtures` as X3d-3's tests obtain it (item 13). | unchanged; no X3d unit |
| item 13 | X3c-3 changes only doc comments in `commit.rs` (`:10-15`, `:701-710`). | item 13's r9 note |
| item 14 | A re-commit runs the same composition as a first commit (items 3, 4 and 7). The RC rows are X3c's, transcribed by X9 r17 (CL-2). | unchanged; see below |
| item 15.1 | In phase B, "J1's cancellation latch (X3d r9)" takes the gate 0→2. | S10.2, phase B; XL-1 |
| item 15.3 | The facade and its outcomes are unchanged. Step 3.8's list becomes conditional (CL-1). | item 4 step 3.8 |
| item 16, CL-1 | The r7 limit is lifted. Step 3.8 is restated. Its owner is "X3d r9, which J1's S10 already requires". | the r7 note; step 3.8; XL-1 |

**Crash windows and controls under CL-1: no change implied.** X3c r8 implies no change to X3d's crash points, end-path rules or tests, so r9 records no cross-law item for them. S10's crash windows and rows are in S10.9.
- **Crash points.** A re-commit adds none (X3c r8 item 6a.9). The RC rows kill or hold only at points X3d already supplies (item 10):
  - `x3d.publish.after-staging` (RC-8);
  - `x3d.publish.commit-returned` (RC-5, RC-8);
  - `x3d.publish.published` and `x3d.finish.end-step.after` (RC-5).
- **End-path values.** The RC rows' `end(…)` values follow items 7 and 8 as they stand:
  - `REV` and `CLN` after a certain staging refusal that leaves a durable `SEAL` (RC-6, RC-7);
  - nothing appended after an undetermined evidence `COMMIT`, whose reserve is forfeited (RC-4);
  - no `REV` where the process died before `finish` (RC-3).
- **X3d's tests.** At product main `cca4fe4`, no X3d-owned test commits one Run twice in one (S, N). X3d-2's staging test (`crates/storage/src/commit_tests.rs:493-603`) checks one availability row and no pin row after a first commit. X3c r8 keeps that (item 12b, "The first commit is unchanged").
- **Rows.** X3d has no X9 rows of its own (item 10). Nineteen accepted storage runs commit the candidate's Run a second time, and 18 of them change outcome under X3c r8. That record is X3c r8 item 14's, for X9 r17 (CL-2).

**XL-1. J1's S10 and the number "X3d r9" (cross-law item; resolved by lead decision).**
- **What accepted records expect of "X3d r9".**
  - J1 r5 writes its X3d amendment as successor S10, under that name (J1 r5:80, :512, :516, :651-658, :856, :882). S10 covers:
    - the cancellation latch as a third gate source, with `take_cancellation_latch` and the window bits (item 5);
    - `StopCause::Operator` and the `REV` reason `operator` (items 7 and 8);
    - `InstallationTermination::Interrupted { signal }` (item 9);
    - units J3a (item 2) and J3b (item 13);
    - the `refused()` record (J1 r5:502);
    - `open`'s ExecutionId reservation (item 2);
    - four forbidden substitutes.
  - M3-PLAN r9 assigns "X3d r9" both S10 and CL-1 (M3P:317), and routes CL-1 there (M3P:364).
  - X3c r8 names "X3d r9, which J1's S10 already requires" as CL-1's owner (item 16). It also writes "J1's cancellation latch (X3d r9)" (item 15.1).
  - M3-L r5 has "X3d r9, X4 r8 and X7 r7" land with unit J3b (items 16f and 18).
- **The lead's decision: S10 is folded into r9,** as its own marked section ("S10 (r9)", after item 13), beside CL-1. M3P:317 names the lead as X3d r9's writer.
  - **Why.** Every accepted reference to "X3d r9" stays true: J1 r5, M3P, X3c r8 item 15.1's "J1's cancellation latch (X3d r9)" and M3-L r5. X3d r9 is what M3P:317 says it is, S10 and CL-1 together.
  - **Rejected: S10 as X3d r10, on r9's accepted bytes.** The four laws that name "X3d r9" for S10's content (J1, M3-PLAN, X3c and M3-L) would each need a record note in their own next revision. That gains nothing.
- **Effect on the CL-1 part.** None. CL-1's notes and S10's sections touch different sentences. Neither relies on the other.

**Unchanged from r8:** everything else.

## Problem

Every piece of an authoritative commit now has an accepted law, but nothing composes them:
- the journal (X3b): floor, carrier, append, witness, `JournalAppendLock`, the SEAL-path level-4 hold and its stop order;
- the ledger and objects (X3c): locations, creation, attempt admission, staging, `COMMIT` and durability classification;
- the live guards (X4): `OperationGuard`, the observer, the checkpoint, `FinalGate` and `AdmissionPermit`;
- the operation (X2e's `ProjectOperation`) and current trust (X4T).

At 5b5f04c the product holds:
- the private gate primitive (`security::commit_authority`: `FinalGate`, `StopObserver`, `PreparedAttempt`, `AdmissionPermit`, the inert `PreparedJournalSeal`);
- the evaluator's opaque `ReplayedRun`;
- the ledger's private `stage_recovery_pair`;
- the private `storage::recovery` join.

It has no `CommitSession`, `PreparedCommit`, `PublishedCommit`, `JournalWriteTxn`, `JournalSealBinding` or `seal_under_append_lock`, and no `storage/src/commit.rs`. X3d supplies the build plan's named types, in its order, as the one facade through which an authoritative commit can be published. That covers F32, F34 and F38 to F41, and X4c's end path.

## Decisions

1. **The types, as the build plan names them (lead decision on ownership).** Every type below is private-fielded, not Clone, not Default, not serializable, and has no unchecked constructor.

   | Type | Crate | Created only by | Holds |
   |---|---|---|---|
   | `CommitSession` | security | `CommitSession::open(ProjectOperation)` (item 2) | The consumed `ProjectOperation`: lease, project owners, `SelectedStoreEndpoint`, carrier, `OperationGuard`, monitor, `FinalGate`, the N-bound binding. Also the drawn ExecutionId, the receipt's selected core closure and the permitted operation. From item 3 step 0, the end-path settlement reserve (item 8, r6). **r8:** also the receipt's core evaluator closure (EC1), derived from the same authenticated inventory. |
   | `JournalWriteTxn` | security | `begin_journal_txn(CommitSession)` | The live session and the open level-3 journal transaction. It has no SQL, write or checkpoint method. |
   | `JournalSealBinding` | security | `seal_under_append_lock` only | Read-only carrier, generation, SEAL sequence and body digest, operationRef, the replayed RunId. It is evidence of that append, never a grant. |
   | `PreparedCommit` | storage | `storage::prepare_commit(ReplayedRun, CommitSession)` | Both prerequisites, the exact binding, the verified object set and the reserved budget. |
   | `PublishedCommit` | storage | storage's commit path and X6's recovery validation only | The exact committed receipt and RunId, after the `COMMIT` returned success. |
   | `StoppedSession` | security | every end of `publish` | The operation lease and the end-path owners, admitting cleanup only. It also holds the end-path settlement reserve, if step 0 took it and no uncertain outcome forfeited it (item 8, r6). |

   - **The adapter.** The two-phase adapter trait (stage, then commit) is owned by security, and its implementation is private to storage (build plan line 112). **r7 (record):** Rust visibility cannot enforce that privacy, so a source pin does (X8 r3 item 3b; see the r7 header).
   - **What the facade refuses.** Storage's public facade accepts no external adapter and no external `SealOutcome`.
   - **Crate edge.** Storage gains the direct dependency on `opensip-evaluator` that the build plan selected (line 34). Neither evaluator nor security depends on storage. `check_package_edges` must admit that edge, and X3d's unit records it.
   - **Rejected:** a single storage-owned session type, which would let storage mint security's authority; and types in the inert contracts crate.
   - **r9 (S10):** `CommitSession` holds the `ReservedExecutionId` (S10.1). It mints the operation's one `CancellationLatch`, a security type that only `take_cancellation_latch` creates (S10.2).

2. **Opening a session: one ProjectOperation, one attempt (lead decision).** `CommitSession::open(operation: ProjectOperation)` consumes the operation, so one operation publishes at most one commit.
   - It draws the ExecutionId from 16 host-CSPRNG bytes (`exec1_` plus 32 hex, identity §2's grammar). That is its pre-use uniqueness draw. The durable reservation for an authoritative attempt is X3c item 3's `attempt_custody` row, whose no-replace trigger refuses a second insert.
   - It binds N, the endpoint's (S, G, K), the carrier's `project_key_digest`, the receipt's selected core closure and the permitted operation. These are X4 item 4's operation joins, now complete.
   - **r8:** it also binds the receipt's core evaluator closure. Security derives it from the receipt's authenticated core inventory by EC1's rule, never from the Run, and exposes it read-only as `CommitSession::core_evaluator_closure()`. It is the session's half of the build plan's "producer selections" (line 67).
   - **Rejected:** several commits per operation. That would need a reusable gate, which the one `FinalGate` per operation (X4 item 2) forbids, plus a second ExecutionId under one guard.
   - **r9 (S10):** `open` reserves its drawn ExecutionId in `ExecutionIdReservations` before the session exists, and the session holds the `ReservedExecutionId` (S10.1).

3. **`prepare_commit(ReplayedRun, CommitSession)`.** Under the writer lease, in this order. Steps 0 to 3 are preflight and take no level-3 lock. Step 4 is X3c's own attempt transaction. Steps 5 and 6 are the objects.
   0. **The end-path reserve (RF-4; lead decision).** First, before any check that can return a `StoppedSession`, reserve on the operation ledger the fixed cost of one `REV` and one `CLN` append. Each is a level-3-then-level-4 acquisition, a record, two witness writes and a commit, with its confirmations. The reserve is held by the session and spent only by `finish` (item 7). If it can't be reserved, `prepare_commit` refuses on the budget row before anything else, and the returned `StoppedSession` holds no end-path reserve. Its `finish` appends neither `REV` nor `CLN`, even if the gate is already latched (the observer was started at the lease-free point and may have latched). It releases the lease and runs the end step (item 7). An unfunded append is never attempted. **Rejected:** attempting the `REV` without a reserve, which could exhaust the ledger mid-append. **Rejected:** reserving it together with the publication budget, where a failed combined reserve would leave a latched operation's `REV` unfunded.
      **r6: it is the attempt ledger's settlement reserve (item 8).**
      - **Who takes it.** Security takes it, through the session's private end-path step (X3d-1). `prepare_commit` calls that step. Storage never holds the platform reserve or the ledger.
      - **Its size** is item 8's exact cost.
      - **Where it goes.** It moves with the session into the `StoppedSession`, unless an uncertain outcome forfeits it first.
      - **If it can't be reserved.** The refusal latches the attempt ledger, as any failed charge does. So `finish` runs no end step either (item 7 step 3): it releases the lease and stops. This replaces "and runs the end step" above, which a closed ledger would refuse.
   1. **Binding equality.** The `ReplayedRun`'s RunId, plan and proof bind to the session. Its evaluator closure equals the session's core evaluator closure, derived by security from the same authenticated inventory as the core closure (r8; EC1). A mismatch is the invariant row (item 9). It is a broken caller, never a retry.
      **r8:** r7 read "equals the session's selected core closure". That is a `kind: "core"` id, which no replayed Run can name (see the r8 header). The Run's `projectId` must still equal `CommitSession::project_id()` (X5 r3's target identity).
   2. **Retention feasibility and the publication budget.** The declared object bytes, pins and every post-effect confirmation of steps 4 to 6 and of `publish` are reserved on the operation ledger (X3c item 9). If this reservation fails, the attempt refuses on the budget row before the first write. Step 0's end-path reserve is kept.
   3. **Carrier capacity (F32, RF-1).** The reserved terminal slot is `9007199254740991`. X3b r8 item 5a reserves two ordinary slots after every SEAL for its `REV` and `CLN`, so a SEAL fits only when the proven tail is at most `9007199254740987`. When X3b's exported predicate `seal_fits(provenTail)` is false (proven tail `9007199254740988` or higher), `prepare_commit` returns `CarrierCapacityExhausted { grantGeneration, provenTailSeq }` before any write. X3d-1 calls `seal_fits` and writes no literal threshold (X3b r8 item 5a). Storage never calls lifecycle. Host finalization (X7) completes cleanup, releases the lease, then routes the rollover under the fence.
   4. **Attempt admission (X3c item 3, RF-2).** The `attempt_custody` row (`admitted`) is inserted in its own level-3, non-waiting ledger transaction and committed. Three outcomes, each stopping before any object:
      - the insert hits the no-replace trigger: step 5;
      - the `COMMIT` errors, or the connection is lost: `CommitUndetermined { executionId }` on item 9's durability row. The ExecutionId is retained, there is no RunId and no retry, and X6 decides the row;
      - busy, or an I/O failure before the `COMMIT`: the busy or host I/O row (item 9).
   5. **Duplicate ExecutionId (F34).** If the insert hits the no-replace trigger, an attempt with this exact ExecutionId already exists. `prepare_commit` writes nothing further, does not `INSERT OR REPLACE`, appends no SEAL, and returns `ExistingAttempt { executionId }` for the host to route to read-only recovery (X6). X6 compares the requested binding exactly and refuses a different one. Because a session's ExecutionId is a fresh CSPRNG draw, this cannot occur on a lawful first attempt. Until X6 exists, `ExistingAttempt` terminates on the invariant row. **Rejected:** treating the collision as a busy or corrupt ledger.
      **r7 (record):** X6 r3 item 6 superseded "Until X6 exists". The invariant row is the writer's permanent projection, and the outcome carries the requested binding (see the r7 header).
   6. **Objects (X3c item 4).** Each is published with its file and directory barriers.

   A refusal at any of these steps leaves no acknowledged Run, appends no SEAL, and returns the session's `StoppedSession`. A refusal after step 0 succeeded still holds the end-path reserve, even when the failure closed the attempt ledger (r6); a step-0 refusal holds none. **r6:** step 4's `CommitUndetermined` forfeits the reserve (item 8).
   - **`CarrierCapacityExhausted` keeps the ledger open (r6).** Step 3 is a decision over a completed read, not a native failure. `prepare_commit` returns it after the read's scope has completed, so the attempt ledger stays open for item 7's end step and X3b item 13's rollover. That is not a failure reported as a value (item 8): nothing failed.

4. **`PreparedCommit::publish`: the end-to-end order.** This is the order of X3c r7 item 8 and X3b r6 item 5. Locks are acquired only in the order shown.
   1. **Journal transaction.** `begin_journal_txn(session)` takes the journal `BEGIN IMMEDIATE` (level 3), never waiting.
   2. **Ledger transaction.** Storage takes the ledger `BEGIN IMMEDIATE` (level 3), never waiting. On failure: security's consuming abort releases the journal transaction (F06), and the result is the busy or I/O row with a `StoppedSession`.
   3. **SEAL under the append lock.** `seal_under_append_lock(txn, &replayed, adapter)`:
      1. take `JournalAppendLock` (level 4);
      2. run X4's checkpoint (steps 1 to 4, with no admission yet);
      3. build and validate the SEAL (`seal_run_id == replayed.run_id()`, through the existing `PreparedJournalSeal::bind`);
      4. witness `PENDING`;
      5. insert and commit the SEAL; the journal transaction closes;
      6. witness `COMMITTED`;
      7. repeat X4's checkpoint (F19);
      8. the adapter's staging phase: storage's `stage_recovery_pair` and the Run material, run material, references, availability and pins, all in the open ledger transaction with nothing committed (X3c item 6). It returns the prepared-commit adapter;
         **r9 (record; X3c r8 CL-1):** "availability and pins" is conditional. Step 3.8 reads: the adapter's staging phase, all in the open ledger transaction with nothing committed (X3c r8 item 6). Before any insert, staging reads the Run's standing in (S, N), and on a re-commit compares the Run material (X3c r8 items 6a.2 and 6a.3). It then stages storage's `stage_recovery_pair`, the Run material and its object references. **On the Run's first commit in (S, N)** it also stages the availability record (generation 0 `retained`) and the pins. **A re-commit of an already-committed Run stages neither** (X3c r8 item 6a.4, R8-4; item 6a.5, R8-5). It returns the prepared-commit adapter. "First commit" and "already committed" are X3c r8 item 6a.2's standing (see the r9 header).
      9. repeat X4's checkpoint, ending in `FinalGate::admit`. That mints the one `AdmissionPermit`;
      10. `permit.consume(adapter.commit)` performs the ledger `COMMIT`;
      11. release level 4 once the `COMMIT` returns.
   4. **The result.** Storage builds `PublishedCommit` only on a successful `COMMIT` (item 6).

   - **Stop order (RF-3).** If a certain refusal stops the path after step 3.1 and before 3.10 (a failed checkpoint, which latches the gate; a staging failure; no permit; or an observer latch), X3b r6 item 5 step 7's stop order applies exactly once inside `publish`:
     1. roll back the open ledger transaction;
     2. release level 4, then each level-3 transaction still open.

     `publish` appends nothing. The one `REV`, and any `CLN`, are appended only by `finish` (item 7). **r6:** they are funded by the settlement reserve. The stop's failure may have closed the attempt ledger, but it does not close the reserve (item 8).
   - **An uncertain journal commit or barrier** (step 3.4, 3.5 or 3.6 fails after visibility) does not enter that order. X3b r6 item 5's uncertain-outcome rule applies: refuse every further effect, roll back the open ledger transaction, release level 4 exactly once and any open level-3 transaction, and return `CommitUndetermined { executionId }` on item 9's durability row. Neither state is assumed, and nothing is appended. The `StoppedSession` is marked uncertain. Its `finish` appends nothing, reconciles nothing and copies no floor; the next writer reconciles (item 7, r5). **r6:** the end-path settlement reserve is forfeited where the outcome is classified, so the `StoppedSession` holds none (item 8).
   - **A returned evidence `COMMIT`** (step 3.10), whether `Committed` or `CommitUndetermined`, releases level 4 exactly once. That `COMMIT`'s outcome is the caller's outcome. **r6:** `CommitUndetermined` there also forfeits the reserve (item 8).
   - **Lock-order rules.** Level 3 is never acquired or reacquired under level 4, and nothing waits on a fence or lease inside `publish`.
   - **Rejected:** committing in the staging callback; and releasing level 4 before the `COMMIT` on a path that continues to it.

5. **The latch (F38, F39, F41).** It is the one `FinalGate` the operation already carries (X4 item 2), with its two-bit state law:
   - **State 2 before admission (F38).** The compare-exchange fails, no permit exists, the staged ledger transaction rolls back, and the durable SEAL stays uncommitted operational history (F36).
   - **State 3 after admission (F39).** The commit's own outcome stands: `Committed` stays committed, and `CommitUndetermined` stays undetermined (F40). `PublishedCommit` records `latchedAfterAdmission`, so required delivery reports `DELIVERY.REQUIRED_FAILED` (the delivery owner, X7). No further effect or retry is admitted.
   - **Every interleaving (F41).** At most one evidence commit is issued, and the state stays in 0..3 and never resets. This is pinned by the existing exhaustive gate-trace test, plus X9's process-level matrix.
   - **Rejected:** a second gate per commit.
   - **r9 (S10):** a third source, the cancellation latch. It is usable only in a window that opens when the attempt row commits and closes only where a `StoppedSession` is produced. The states above, F38, F39 and F41 are unchanged (S10.2).

6. **Outcomes returned to callers.** `publish(self) -> (CommitOutcome, StoppedSession)`:
   - **`Committed(PublishedCommit)`.** Only after the ledger `COMMIT` returned success (F13). It carries the exact receipt, RunId, ExecutionId and `latchedAfterAdmission`.
   - **`CommitUndetermined { executionId }`.** The evidence `COMMIT` errored or the connection was lost (F12, F40), or an uncertain journal commit or barrier stopped `publish` (item 4). `prepare_commit` returns the same outcome for an uncertain attempt-admission `COMMIT` (item 3 step 4). The ExecutionId is retained, there is no RunId, and nothing is retried. The `attempt_custody` row stays `admitted` for X6.
   - **`Refused(InstallationTermination)`.** Any refusal before a permit was used.
   - **`CarrierCapacityExhausted { grantGeneration, provenTailSeq }`, `ExistingAttempt { executionId }` and `CommitUndetermined`** can come from `prepare_commit` (item 3). **r7 (record):** `ExistingAttempt` also carries `requested` (X6 r3 item 2).
   - **r9 (S10):** `latchedAfterAdmission` is the window close's sample. The `StoppedSession` keeps the sample's admission bit as `admitted_at_close()` (S10.3; LD9-3). No outcome is added.

   Whatever the outcome, the caller holds a `StoppedSession` and must finish it (item 7). **Rejected:** a single error enum, which would let a caller confuse undetermined with refused.

7. **The end path, with X4c merged here.** `StoppedSession::finish(self)`:
   1. **Cleanup records (the only `REV` and `CLN` owner).** While the operation lease is still held, `finish` appends one `REV` if any of these holds:
      - a durable SEAL has no evidence commit;
      - the gate is latched (an observer latch, or a failed checkpoint that fetch-ORed 2);
      - a revocation was observed.

      It appends `CLN` when cleanup residue must be recorded, including F38's SEAL-without-commit pair. Both go through one fresh, lawful level-3-then-level-4 acquisition on the same carrier (build plan line 148; X3b r6 item 6; X4 items 5 and 7), funded by item 3 step 0's reserve. A `REV` blocks any later `RA`, intent, commit or `SEAL`. After an uncertain journal commit or barrier, `finish` appends nothing (RF-2). **r6:** the same holds after an uncertain attempt-admission or evidence `COMMIT`. The reserve was forfeited when the outcome was classified (item 8).
      **r6 (lead decision): the spend.** `finish` spends the settlement reserve in one `settle` call (item 8): the `REV` first, if owed, then the `CLN`, if owed.
      - **Each append.** Each is an X3b item 5 append on its own fresh level-3-then-level-4 acquisition. It runs no authority checkpoint: X4 item 3 checkpoints brokered effect requests and commit admission, and these records are neither.
      - **Open or closed ledger.** The spend is the same whether the attempt ledger is open or already closed. There is one path, not two.
      - **Nothing owed.** If neither record is owed, the reserve is dropped unspent. It is never refunded.
      - **A failure inside the settlement ends it.** Examples: busy at the carrier's `BEGIN IMMEDIATE`, I/O, quarantine, an overrun or an unwind. Nothing after it runs: there is no `CLN` after a failed `REV`. Nothing is retried, and the attempt ledger is closed if it was not already.
      - **An uncertain end-path append** latches the append lock as any uncertain append does, and nothing follows (X3b item 5). The next writer reconciles.
      - **Disclosure.** A failed end-path append is disclosed as an end failure (item 9).
      **r5 (lead decision, under X3b r9 item 5): no reconciliation after an uncertain outcome.** `finish` does not reopen the carrier and does not run `reconcile_witness`. It reads nothing, writes no witness and copies no floor.
      - **Where the carrier is reconciled.** Before its next use, the next writer's floor step and carrier start reconcile it (X3b items 3 and 4). Every state an uncertain journal outcome can leave is a state that process death at the same point leaves, so those steps already handle it. Read-only recovery (X6) reports it without writing.
      - **Why.** The failure after visibility has closed the attempt ledger (item 8), which is the platform's failure-latching `WorkLedger`. r4's reconciliation would be refused `Closed` before it read anything.
      - **Rejected:**
        - r4's reconciliation before releasing the lease: it cannot run on the one attempt ledger;
        - a post-failure allowance in that ledger, a second ledger, or reporting the failure as a value to keep the ledger open (X3b r9 item 5 gives the reasons). **r6:** the settlement reserve is not such an allowance for the reconciliation. It funds only the `REV` and `CLN` appends, and it is forfeited after an uncertain outcome (item 8).
      - **Reversed from r3.** r3 rejected "skipping the end step entirely, which would leave a reconcilable floor behind until the next writer". r5 adopts it for the uncertain path only. The floor then lags this operation. That stays inside v8 §5.4's detection bound, because an undetermined boundary is not an observed one.
   2. **Release.** Release the operation lease.
   3. **End step.** Run X3b item 4's end step: the floor copy under the fence, with no project lock held. **r5:** after an uncertain journal outcome the end step does not run. No fence is taken, nothing is read, and the floor is untouched (X3b r9 item 4). No other effect runs after an uncertain outcome.
      **r6: the end step on a closed attempt ledger.** The end step also does not run if the attempt ledger is closed when `finish` reaches step 3. That happens when a certain refusal closed it, or the settlement failed.
      - **Why.** The end step's first step, the fence walk, is charged. It would be refused `Closed` before any effect, so it is not attempted (X3b r10 item 4). Law does not name a step that cannot run.
      - **What it leaves.** The floor stays where this operation's floor step put it. That is the state process death after step 2 leaves. The next writer's floor step copies it forward.
      - **No disclosure.** A step not attempted is not a failure.
      - **What it is not.** The settlement reserve never funds the end step (item 8).
      - **On `CarrierCapacityExhausted`** the ledger is open (item 3), unless the settlement failed. In that case the rollover is not attempted either, and the next writer reaches the same exhaustion and route (X7 r3 item 6).

   - **What it swaps in.** `finish` replaces X4's test-only abstract lock with the real `JournalAppendLock` everywhere. After X3d, no production path names the abstract lock.
   - **If `finish` never runs.** A panic, `mem::forget` or abort leaves recovery evidence (`attempt_custody` `admitted`, an orphan SEAL), never a claimed cleanup success.
   - **Not claimed:** rollback of reversible brokered effects, because M2 performs none.
   - **r9 (S10):** the gate may also be latched by the cancellation latch, and that `REV`'s reason is `operator` (S10.4). `refused()` also ends a session whose attempt never started (S10.6).

8. **Budget.** All work is charged to the operation's ledger, which is X1's attempt ledger, already used by X3c item 9 and X4 item 9.
   - The end-path reserve (one `REV` and one `CLN`) is taken first, at item 3 step 0, and survives every later refusal. `finish` spends it. **r6:** it survives a refusal that closed the attempt ledger, because it is that ledger's settlement reserve (below).
   - The publication reserve (objects, confirmations, attempt admission, and `publish`'s fixed SEAL, witness, staging and commit costs) is taken at step 2. If it fails, the operation refuses before the first write.
   - The observer keeps its own per-observation ledger (X4 r7).
   - **r5.** After an uncertain journal outcome the attempt ledger is closed (the platform latch), and nothing further is charged to it: `finish` performs no reconciliation and no end step (item 7). **r6:** nothing is drawn from the settlement reserve either. It was forfeited.
   - **Rejected:** charging the end path at end time, or inside the publication reserve. Either could strand a latched operation's or an un-REVed SEAL's `REV`.

   **r6: the settlement reserve (lead decision).** This is the narrowest lawful way to keep F19's `REV` funded after the attempt ledger latches.
   - **What the platform provides (unit X3d-0).** `WorkLedger` gains one settlement reserve per instance.
     - **Taking it.** `WorkLedger::reserve_settlement(cost)` is a method on the owner's `WorkLedger` only. `WorkScope`, `ReservedPostchecks` and every helper borrow have no such method.
       - **Refusals.** It is refused, and takes nothing, when the ledger is closed or the cost exceeds the remaining limits. These use the existing `Closed`, `Objects`, `Edges`, `Bytes` and `Arithmetic` failures, which latch the ledger as any failed charge does.
       - **Charging.** On success the cost is charged to `used` at once, as any reservation is, and it is never refunded.
       - **One per instance.** A second `reserve_settlement` on the same instance is refused `Closed` and latches.
       - **No new variant.** `BudgetFailure` gains no variant, so no budget row changes.
     - **The value.** `SettlementReserve` has private fields. It is not `Clone`, `Copy`, `Default` or serializable, has no constructor but `reserve_settlement`, and is bound to the instance that issued it.
     - **Spending it.** `WorkLedger::settle(reserve, action)` consumes the reserve, so it is spent at most once.
       - **The allowance.** `action` receives a `WorkScope` on the same ledger. Every charge inside it, including nested `run`, `effect`, `ReservedPostchecks` and `prepaid`, draws only from the reserve's allowance, exactly as `prepaid` draws today, never from the limits, and `used` does not move.
       - **Admission.** `settle` is admitted whether or not the ledger has failed.
       - **Its own latch.** Inside `settle`, scopes are checked against the settlement's own latch, not the ledger's. Any `Err`, an overrun (`ReservedPostcheck`, before the work it covers) or an unwind latches both the settlement and the ledger. Nothing more can then be drawn, because the reserve is consumed.
       - **A foreign reserve.** A reserve offered to an instance that did not issue it is refused `Closed` before `action` runs, and latches.
     - **No refill.** No method adds to the allowance, and unused allowance never returns to the limits.
     - **What does not change.** Outside `settle`, a failed ledger refuses everything exactly as at 6dd7363. A ledger that never takes a settlement reserve behaves exactly as now. That includes 468's gate ledger, X4's per-observation ledgers and every ledger outside this facade.
   - **Who can spend it (security, X3d-1).**
     - Security takes the reserve at item 3 step 0. It wraps it in a private, non-Clone end-path type that only `CommitSession` and then `StoppedSession` hold.
     - Only `StoppedSession::finish` calls `settle`, and only for item 7's `REV` and `CLN` appends.
     - Storage never sees the reserve or the attempt ledger.
     - A source pin confirms that, in production code, `reserve_settlement` and `settle` each have exactly this one caller.
   - **Size: exact.** The reserve is the sum of what one `REV` append and one `CLN` append charge at their bounded maximum bodies. It is computed by the same cost functions the append path charges with (X3b-2 at 6dd7363):
     - the writer open and `BEGIN IMMEDIATE` (`open_writer`'s `carrier_creation_cost`);
     - the witness read (`operational_read_cost`);
     - X3b item 5's append cost (`append_cost` at the body bound and the longest witness): two witness publications with their confirmations, plus the insert and the commit.

     **Body bounds.** X3d-1 fixes each end-path body's bound:
     - the `REV`'s `reason` comes from a closed end-path set, and its `trustEpochObserved`, if X3d-1 records one, has a fixed bound;
     - the `CLN`'s residuals are F38's fixed pair.
     - **r9 (S10):** the closed `REV` reason set gains `operator`. The reserve and its pin are unchanged (S10.4).

     A larger draft is refused on the invariant row before any effect. A test pins that a maximum `REV` and `CLN` charge exactly the reserve, and that a draft one byte over its bound is refused before any effect.
   - **Forfeit after any uncertain outcome.** The session drops the reserve where any of these is classified:
     - an uncertain journal commit or barrier (item 4);
     - an undetermined attempt-admission `COMMIT` (item 3 step 4);
     - an undetermined evidence `COMMIT` (item 4 step 3.10).

     The `StoppedSession` then holds none, and `finish` cannot spend it. That is structural, not a flag `finish` reads. After an uncertain journal outcome, the append lock's own latch (X3b item 5) also refuses any later carrier `begin`.
     - **Why the COMMITs too (widened from r5).** After either undetermined `COMMIT`, it is undetermined whether a SEAL has its evidence commit, and that is exactly the condition that owes the `REV`. Reading it back is forbidden on the write path (item 10; F12). The attempt then belongs to X6, which must judge a carrier this operation did not touch after the uncertainty (X7 r3 item 5). Nothing follows any uncertain outcome, the same rule as X3b r9 item 5.
     - **The stop is still safe.** The `StoppedSession` admits no further effect, so S6's "no later `RA` or `SEAL`" already holds. An observed revocation stays in SC-TRUST, where the next admission meets it.
   - **Why this does not weaken the latch.** The latch makes sure that a failed native operation is never retried and that no further work follows it on that ledger (412 to 418; 468 item 3).
     - The settlement retries nothing. It funds two records that are different effects from the one that failed, fixed in kind and cost before the first attempt effect.
     - It can fund nothing else, it is spent once, and its own failure latches with no second chance.
     - Its work was charged inside the owner's caps before any effect.
     - Every other ledger is unchanged.

     This is the case r5 and X3b r9 named as the one where a post-failure allowance is justified. The `REV` carries S6 weight, F19 requires this invocation to record it, and no later writer can.
   - **Rejected:**
     - **A second ledger, or a child ledger carved from the attempt ledger,** for the end path. X3b item 9, X1 item 5, X4 items 6 and 9 and X7 r3 item 7 forbid a second ledger, and `WorkLedger`'s own rule is that a new ledger never licenses work after a failure. A carved child is a second instance with the full general API.
     - **Reporting certain native failures as values, so that their scopes do not fail.** That routes the failure around the latch. It leaves the whole ledger open to ordinary work after the failure. It would also have to be repeated at every native step in X3c and X3d, and an unwind would still close the ledger and lose the `REV`.
     - **Leaving the `REV` to the next writer.** F19 requires this invocation to "record REV through a new lawful journal call" after releasing its ordered locks. The next writer cannot know the latch or the observed revocation, which are this process's in-memory facts. A `REV` under the next writer's own lock would block that writer's own `SEAL` (S6). And no next writer may ever come.
     - **Appending the `REV` inside the failing scope, before it returns.** The nested failure has already latched the ledger. The staging, checkpoint and busy failures also happen under level 4, where F19's fresh level-3 acquisition is forbidden.
     - **Funding the end step's floor copy from the settlement.** The end step runs after the lease is released, under the fence, and writes trust state. Funding it would carry the settlement across the lease handoff, for a write that records nothing F19 requires. Without it, the floor lags exactly as after process death following the `REV`, which item 7 and X3b item 4 already accept.
     - **A general post-failure allowance any holder can spend.** The typed capability, its single spender and the source pin confine the allowance to the end path.

9. **Refusal rows (existing details only).** Every row maps through 468c's `InstallationTermination`, every match is exhaustive, and S12 prevails where it fixes a class.
   - **Busy journal or ledger transaction, or a lost lease:** operational-failed, 4, `LEDGER.BUSY_TIMEOUT`, `ledger-busy`, detail `PROJECT.BUSY`.
   - **Host I/O:** an object, directory, journal or ledger I/O failure before any `COMMIT` is operational-failed, 4, `HOST.IO_FAILURE`, `host-io`.
   - **Quarantine:** `LEDGER.CORRUPT`, `ledger-corrupt`, operational-failed, 4.
     - The domain detail is `MIGRATION.CORRUPT` only for a carrierFormat 3 footprint that isn't a lawful durable prefix at a writer or maintenance open (S12; X3b r6 item 8).
     - A ledger schema mismatch, a partial ledger creation footprint, or an unequal object keeps `domainDetail` omitted (X3c r7 item 10).
     - Other journal quarantines take X3b r6 item 8's rows.
   - **`CommitUndetermined`** (an attempt-admission or evidence `COMMIT`, or an uncertain journal commit or barrier): operational-failed, 4, `DURABILITY.COMMIT_FAILED`, `durability-commit`, with the ExecutionId and no RunId (F40).
   - **Revocation, observer fail-stop and stale guards:** X4 item 8's rows.
   - **Invariant:** a `ReplayedRun` or session binding mismatch, or `ExistingAttempt` before X6 exists. Operational-failed, 4, `SYSTEM.OUTCOME.ILLEGAL_STATE`, `host-invariant`, detail `HOST.INVARIANT_VIOLATED` (as X3c item 10 gives a reused ExecutionId). **r7 (record):** X6 r3 item 6 superseded "before X6 exists". This row is `ExistingAttempt`'s permanent row in the writer's invocation.
   - **`CarrierCapacityExhausted`:** no row of its own. X7 maps the outcome after rollover.
   - **Budget:** operational-failed, 4, `SYSTEM.OUTCOME.ILLEGAL_STATE`, `host-invariant`, detail `WORK.BUDGET_EXHAUSTED`.
   - **Post-admission latch:** `DELIVERY.REQUIRED_FAILED`, `delivery-required`, from X7.
   - **End-path failures (r6; no new row).** A failed `REV` or `CLN` in `finish` is an end failure under X3b item 4's existing rule. It is disclosed on its existing X3b item 8 row, never rewrites the outcome item 6 returned, and changes nothing in X7 r3 item 3's projection. The rows are busy, host I/O, quarantine, budget, or `DURABILITY.COMMIT_FAILED` for an uncertain end-path append. An end step that is not attempted (item 7 step 3) is not disclosed.
   - **r9 (record): X3c r8's re-commit refusals (X3c r8 item 10).** A lawful re-commit is not refused. X3c r8 adds three staging conditions, each on a row this item already has:
     - a re-commit whose manifest or inventory is not byte-identical to the Run's committed material (X3c r8 item 6a.3), or whose declared pin set is not empty (item 6a.5): the invariant row;
     - a one-sided Run, with an availability record and no Run material or the reverse (item 6a.2): the quarantine row, `LEDGER.CORRUPT`, `ledger-corrupt`, with `domainDetail` omitted.
     - Each is a staging refusal after the durable `SEAL`, so item 4's stop order and item 7's `REV` and `CLN` follow. No row, code or detail changes.
   - **r9 (S10): operator stop.** `InstallationTermination::Interrupted { signal }`: class `interrupted`, exit 130 and the signal, with no errorCode, faultCause or detail. X7 r7 projects it (S10.5).

10. **Boundaries.**
    - **X5:** produces the `ReplayedRun` from admitted facts (F01). X3d accepts only the evaluator's opaque `ReplayedRun` and never a caller-built RunId.
    - **X6:** owns read-only recovery: `RecoveredCommit`, settlement, the `ExistingAttempt` and `CommitUndetermined` follow-up, and F14 and F15's read side. X3d never reads its own outcome back and never settles `attempt_custody`.
    - **X7:** owns `host/finalization.rs`. It maps outcomes to envelopes, owns `DELIVERY.REQUIRED_FAILED` and the capacity rollover route, and must never promote a preview to a sealed Run (DR-G27).
    - **X9:** runs F00–F53 in fresh processes with crash barriers. X3d supplies named, test-only crash points before and after each durability step.

11. **The opaque surface X8 tests.** Each of these must fail to compile, pinned by `compile_fail` doctests on the public types:
    - constructing or `Default`ing `CommitSession`, `PreparedCommit`, `PublishedCommit`, `JournalWriteTxn`, `JournalSealBinding`, `AdmissionPermit` or `StoppedSession`;
    - cloning any of them;
    - deserializing any of them;
    - using a `CommitSession` after `prepare_commit` consumed it, or a `PreparedCommit` after `publish`;
    - calling `prepare_commit` with a boolean, a RunId string or a `RunCandidate` in place of `ReplayedRun`;
    - passing a caller-implemented adapter or `SealOutcome` to storage's facade;
    - reaching a SQL connection, a transaction handle or `stage_recovery_pair` from outside storage.

    Behavioural refusals, such as a binding mismatch or a reused ExecutionId, are tested in X3d's own tests and X8.

    **r7 (record):** "pinned by `compile_fail` doctests" is superseded by X8's isolated compile-fail fixtures, run by the X8a driver (X8 r3 items 1 and 2). The adapter case is split (X8 r3 item 3b):
    - group H pins that storage's facade takes no adapter and no `SealOutcome`;
    - a source pin confines security's adapter trait and functions to storage.

    The SQL-connection and `stage_recovery_pair` case is group I (E0603 on `ledger_store`). See the r7 header.

    **r9 (S10):** X8's fixtures gain the `CancellationLatch` and `ReservedExecutionId` cases (S10.7).

12. **Failure cases.**
    - **Covered by X3d:** F32, F34 (routing), F38, F39 (outcome and delivery flag), F40 (outcome), F41, F19 (completion, with X4c), F13, and the composition of F06 and F11.
    - **Covered elsewhere:** F12 and F14's write side (X3c); F36 (X3b and X3c); F34's binding comparison and F14 and F15's read side (X6); F16, F17 and DR-G27 (X7).
    - **Tests while X2e and X5 are pending.** Tests in `opensip-security` and `opensip-storage` build a `ProjectOperation` and a `ReplayedRun` only through crate-private, `cfg(test)` fixtures: X3b and X3c's scratch namespace, X4T-0's signed store, and an evaluator-owned test replay. There is no production seam.
      **r7 (record):** across a crate boundary, these fixtures come through `scenario-fixtures` (the ordinary lane) or `crash-matrix` (the matrix). Both reach X8 r3 item 4b's one shared site list under the joint predicate (X8 r3 item 4g; X9 G1). X3d-2 integrated before X8b and X9-1. Its end-to-end composition is first tested by X8c's B0–B4 (see the r7 header).
      **r8:** a test's binding values come from a real session, never from the Run under test. X3d-2's `bound()` copied the Run's own project and evaluator closure, which is how the step 1 defect went unseen (item 13, X3d-3).

13. **Units after the law.**
    - **X3d-0 (platform; r6, new):** the settlement reserve in `crates/platform/src/work_ledger.rs`, exactly as item 8 states: `reserve_settlement`, `SettlementReserve` and `settle`, with the platform re-export. It comes with an inventory successor for the platform crate. It has no dependency and lands before X3d-1. It is its own unit, not part of X3d-1, because it changes the platform crate's ledger, which every native unit since 412 relies on, and it is reviewed alone as 416 to 418 were.
      - **Tests:**
        - a settlement spendable after a nested failure, an unwind, a swallowed failure and a budget overrun have each closed the ledger;
        - charges inside `settle` drawing only from the allowance, with `used` unchanged, including nested `effect` and `prepaid`;
        - an overrun inside `settle` refused `ReservedPostcheck` before the work, latching both;
        - an `Err` or unwind inside `settle` latching both;
        - a second `reserve_settlement` refused `Closed`, and a reserve taken on a closed ledger refused `Closed`;
        - a reserve from another instance refused before its action;
        - every ledger without a settlement behaving exactly as before (the existing tests unchanged);
        - `compile_fail` doctests that `SettlementReserve` cannot be cloned, defaulted, constructed, or reached from a `WorkScope` or `ReservedPostchecks`.
    - **X3d-1 (security):** `CommitSession::open`, `begin_journal_txn` and its consuming abort, `JournalSealBinding`, `seal_under_append_lock` with the adapter trait, and `StoppedSession::finish`, including X4c's `REV` and `CLN` and the real-lock swap. Depends on X3b-1b and X3b-2, X4a, X2e and X4T-a. **r6:** it also depends on X3d-0, and adds:
      - the session's private end-path step that takes the settlement reserve at item 3 step 0, and the end-path wrapper type;
      - the end-path body bounds and the exact reserve cost function, built from X3b-2's cost functions with no literal;
      - the forfeit at each uncertain classification;
      - `finish`'s single `settle` for `REV` then `CLN`, and the end step skipped on a closed attempt ledger;
      - the source pin on `reserve_settlement` and `settle`.

      **Its tests:**
      - after each certain refusal that closes the attempt ledger (busy at the evidence ledger's `BEGIN IMMEDIATE`, a staging I/O error, a failed repeated checkpoint, a publication-reserve overrun), the `REV` is appended and the end step takes no fence;
      - a failed `REV` appends no `CLN`;
      - after each uncertain outcome, nothing is appended;
      - the exact-cost pin.
    - **X3d-2 (storage):** `commit.rs`: `prepare_commit` (items 3 and 8), `PreparedCommit::publish`, the private adapter implementation, `PublishedCommit`, the `storage → evaluator` edge, and the X8 doctests. Depends on X3c-2 and X3d-1. **r6:** step 0 calls the session's end-path step. `CarrierCapacityExhausted` is returned after a completed scope (item 3), and storage holds no settlement reserve.
      **r7 (record):** "the X8 doctests" became X8 r3 item 3's fixture rows A to D and G for `PreparedCommit` and `PublishedCommit`, group H, and item 3b's adapter source pin (X8 r3 item 2). X3d-2 is integrated. Its disclosed re-commit limit is a follow-up for an X3c successor (see the r7 header).
      **r9 (record):** that successor is X3c r8, and its code unit is X3c-3 (X3c r8 item 13). In X3d-2's `commit.rs`, X3c-3 changes only the doc comments at `:10-15` and `:701-710`, which still describe availability and pins as always staged. The values `stage` hands to X3c are unchanged. X3c's staging uses the initial availability record and the empty pin set only on a first commit (X3c r8 item 6a.9). See the r9 header.
    - **X3d-3 (security and storage; r8, new):** the step 1 closure binding. It depends on EC1's selection and on X8b (the `scenario-fixtures` dev-dependency that gives storage's tests a `ProjectOperation`). It lands before X8c and X9-2, which it unblocks. It comes with one inventory successor for both crates.
      - **security, `trust/core_inventory.rs`:** `Projection` gains the core evaluator closure, computed in `bind` from the descriptor it already builds, with `kind` set to `"evaluator"`, through the same `hash_canonical_value("closure", …)`. It has an accessor beside `closure()`.
        - **Tests:** EC1's vector (`core-evaluator-closure-ec1/evidence/vector.json`, fixture case `baseline-macos`), reproduced byte for byte: both ids, and both descriptors' canonical SHA-256. For every accepted `core-inventory318` case, the two descriptors are equal except `kind`, and the ids differ.
      - **security, `trust/initial_core.rs`:** `InitialCore::evaluator_closure()`, from the same `release.authentication().core().inventory()` as `closure()`, on both the running and the injected arm.
      - **security, `custody/read_premise.rs` and `custody/operation_handoff.rs`:** `PlatformReceipt::core_evaluator_closure()` and `ProjectOperation::core_evaluator_closure()`. These are read-only values beside `selected_core()`. `selected_core()` is unchanged.
      - **security, `custody/commit_session.rs`:** `pub fn core_evaluator_closure(&self) -> &str`, the new session getter. `core_closure()`'s doc comment no longer says a Run's evaluator closure must equal it. Its value and its other uses are unchanged.
      - **security, test support (one shared site):** for the synthetic candidate below, a `#[doc(hidden)]` accessor that returns the core evaluator closure's descriptor, the inventory body bytes, and each tree member's bytes, read through the core's retained handles. It is gated `cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))` and added by name to X8 r3 item 4b's one site list and its pin. It is absent from every release build, and no production path calls it.
      - **storage, `commit.rs`:** `Bound` gains `evaluator_closure`, from `CommitSession::core_evaluator_closure()`, and `plan` compares the Run's evaluator closure with it. The `PlanRefusal::Closure` doc comment names the core evaluator closure. The row is unchanged.
      - **storage, `crash_matrix_support.rs`:** X9 r6's synthetic run candidate lands here, in X3d-3 instead of X9-2, because X3d-3's own positive tests need a Run that binds to a real session (X9 r7 records the move). Its inputs, gate and limits are X9 r6's, with one change: it rewrites the evaluator closure to `CommitSession::core_evaluator_closure()`, never `core_closure()`, and retains that closure's descriptor with its manifest blob (the inventory body) and its tree blobs. It never returns a `ReplayedRun`.
      - **storage, `commit_tests.rs`:**
        - `bound()` takes `project` and `evaluator_closure` from a real `CommitSession`, obtained through X8b's `scenario-fixtures` `ProjectOperation`. It never copies them from the Run.
        - The positive tests replay the synthetic candidate built for that session.
        - The existing closure-mismatch test is rewritten. A pinned corpus Run, whose evaluator closure is not the session's, is refused `PlanRefusal::Closure` on the invariant row.
        - A new test pins that the session's `core_evaluator_closure()` differs from its `core_closure()`, and that a Run naming the session's core closure cannot be replayed (replay refuses kind `core`). So no Run can pass step 1 by naming the core closure.
      - **Product copies of the closure annotations:** `schemas/sources/identity-v3.schema.json` (the `manifestDigest` artifact text and the `closureKinds` note) and the generated `apps/report/src/generated/report.ts` keep their bytes, as stage-meta-reference-selection-v1 kept them. EC1's passage overrides are the semantic owner. There is no generation, registry or drift change. `crates/identity/src/closure.rs` and `crates/evaluator/src/view-joins-registry.json` are unchanged.
      - **Not changed:** no trust record, no signed release format, no component manifest and no 463h builder change. Security already holds the authenticated inventory.
    - **J3a and J3b (r9, S10):** S10's code, as S10.8 states.

## S10 (r9): the commit-phase cancellation join

**What this section is.** J1 r5 item 8 closes S-OP-12, the commit-phase cancellation join, and writes its X3d half as successor S10 (J1 r5:512-547, :650-658, :856). This section carries S10 into X3d. Its decisions are J1's, except those marked LD9-n. Each part names the X3d item it amends, and that item carries a short "r9 (S10)" note pointing here.
- **The consumers, and what each needs from X3d r9.**
  - **J1 r5:** 8.1 and 8.6, with the window closed only where a `StoppedSession` is produced; the `refused()` record (J1 r5:502); item 2's reservation at `open` (J1 r5:212); and units J3a (item 2) and J3b (J1 r5:856, :881-882).
  - **M3-PLAN r9:** the same list, gating J3a (item 2) and J3b (M3P:317).
  - **X3c r8 item 15.1:** in phase B, "J1's cancellation latch (X3d r9)" takes the gate 0→2. The staged re-commit rolls back, and `finish` appends `REV(operator)`, plus `CLN` for the durable `SEAL` (F38). The re-commit branch adds no window bit, latch source, checkpoint, crash point or `REV` reason.
  - **M3-L r5 items 16f and 18:** X3d r9, X4 r8 and X7 r7 are each reviewed on their own and land with unit J3b. Until then, no signal sets the latch.
- **What this section does not decide.**
  - The gate word's encoding, its masked compare-exchange loops and the never-reset rule for the window bits are X4's, through successor S11, X4 r8 (J1 r5:538-539, :659, :857).
  - The phases, projections and precedence are J1's and X7's, through successor S9, X7 r7 (J1 r5 8.2 to 8.4, :660-665).

  This section cites both and decides neither (LD9-5).

**S10.1 Item 2: `open` reserves its ExecutionId (J1 r5 item 2, J1-R4).**
- **The reservation.** `open` draws its ExecutionId as it does now: 16 host-CSPRNG bytes, `exec1_` and 32 hex, at `x3d.session.execution-draw`. In the same step it reserves the id in the process-custody `ExecutionIdReservations`, which lives in `opensip-platform` beside `request_entropy` (J1 r5:205, :212). That is before the session exists, and so before any provider frame.
- **How it reserves.** The draw is checked against every ExecutionId already reserved in the process. A collision redraws, at most eight draws in all (J1 r5:206). Exhaustion, or a failed draw, refuses on security's existing host I/O row, as a failed draw does today (item 9; J1 r5:207). A reservation is never released or reused (J1 r5:208).
- **The sealed value.** The session holds the registry's `ReservedExecutionId`. It has no constructor from bytes or text, and it is not `Default` or deserializable (J1 r5:209). `CommitSession` accepts no other ExecutionId. `execution_id()` returns the reservation's read-only projection, which storage's binding reads as now.
- **What stays.**
  - The durable reservation is still X3c item 3's attempt row at item 3 step 4. Its no-replace trigger refuses a reused ExecutionId (F34; J1 r5:214-215).
  - The `op-` operationRef draw is not an ExecutionId, and it is unchanged.
  - `x3d.session.execution-draw` keeps its name and place. The reservation is in memory and adds no durability point. F34's injected id still reaches the attempt row's trigger, because an earlier run's injected id is not in this process's registry (J1 r5:218).

**S10.2 Items 1 and 5: the cancellation latch, a third source for the one gate (J1 r5 8.1).**
- **The token.** `CommitSession::take_cancellation_latch(&mut self) -> Option<CancellationLatch>` returns `Some` once per operation and `None` after that (J1 r5:518).
  - `CancellationLatch` is security-owned and `Send`. It is not `Clone` or `Default`, not serializable and not constructible.
  - Its one-use method is `latch(self, signal: D9Signal) -> LatchOutcome`. So single use holds per operation, not only per token.
  - It joins item 1's types. Only `take_cancellation_latch` creates it. It holds only what it needs to latch the operation's gate and record the stop cause, and it grants nothing.
- **The window opens when item 3 step 4's attempt row commits** (J1 r5:520; LD9-1).
  - A session step opens it, with one `fetch_or`, and grants and charges nothing.
  - `prepare_commit` calls that step right after step 4's `COMMIT` returned success and before step 6's first object, as it calls step 0's end-path step.
- **The window closes exactly in the step that produces the operation's `StoppedSession`** (J1 r5:521; LD9-2).
  - The close is one `fetch_or`, whose returned prior value is the close's sample. Security builds every `StoppedSession`, so the close is security's. It is ordered before any later effect of the return path (J1 r5:531).
  - **The closing steps:**
    - `prepare_commit`'s error returns: `Refused` (any certain refusal, steps 0 to 6), `CarrierCapacityExhausted` (step 3), `CommitUndetermined` (step 4) and `ExistingAttempt` (step 5). The window may never have opened. The close is set anyway, so a later latch is a no-op (J1 r5:522).
    - Every return of `publish`: `Committed`, `Refused` (including step 2's busy abort) and `CommitUndetermined` (J1 r5:523-526).
    - `refused()` and `undetermined()` (J1 r5:527).
    - `open`'s refusal (LD9-2).
  - **`Ok(PreparedCommit)` does not close.** It is a continuing result, and the window stays open from the attempt row's commit through `publish` (J1 r5:528).
  - **A `PreparedCommit` dropped without `publish`** leaves the window open on an operation that admits no further effect. Its only consequence is recovery evidence (item 7), and no permit can follow (J1 r5:529).
- **Results** (J1 r5:532-537).
  - **Inside the window,** `latch` takes the gate 0→2 or 1→3 in one exchange. It records `StopCause::Operator { signal }` only if this is the operation's first stop. It returns `BeforeAdmission`, `AfterAdmission` or `AlreadyStopped`.
  - **Outside the window,** it changes nothing and returns `OutsideWindow`.
  - `x4.gate.latch.after` fires after it. A latch is either before the close, and so seen by the close's sample, or after it, and so a no-op.
- **It grants nothing else:** no observation, admission, permit, effect, attempt-ledger charge, retry or reset (F41; J1 r5:540).
- **Where a latch takes effect.**
  - **Phase B** (the attempt row committed, `FinalGate` not yet admitted). The next checkpoint (step 3.2, 3.7 or 3.9) refuses, and item 4's stop order applies: no permit, the staged transaction rolls back, and a durable `SEAL` stays history (F36, F38). `finish` appends `REV(operator)`, plus `CLN` if a `SEAL` is durable, from the settlement reserve (J1 r5:556).
    - A re-commit's staging rolls back the same way, and nothing of the Run changes (X3c r8 item 15.1).
    - A latch after `Ok(PreparedCommit)`, before `publish` is called, is seen by `publish`'s first checkpoint (J1 r5:691).
  - **Phase C** (admitted). The latch takes the gate 1→3. The evidence `COMMIT`'s own outcome stands (item 5's F39; F40). `finish` appends `REV(operator)` only after `Committed`, because an undetermined outcome forfeits the reserve (item 8; J1 r5:557).
  - **Phase A** (before the attempt row). The latch is not used. The host ends the session with `refused()` and `finish` (S10.6; J1 r5:555).
- **Item 5's law is kept** (J1 r5:544-547).
  - F38 and F39 are unchanged.
  - F41 is unchanged: at most one evidence commit, and the two state bits stay in 0..3 and never reset.
  - The latch retries nothing. The signal latches the gate, and the next checkpoint's refusal latches the attempt ledger as any failed checkpoint does. The settlement reserve funds the `REV`.
  - A cancellation is never reported as a value to keep the attempt ledger open.

**S10.3 Item 6: the close's sample.**
- **`latchedAfterAdmission`.** On `Committed(PublishedCommit)` it is the state bits of the window close's own sample, taken where `publish` returns `Committed` (J1 r5:524). That sample replaces today's separate load (`commit_session.rs:953-954`). The flag means what it meant: admitted, then latched (state 3).
- **The admission bit for the host (LD9-3).**
  - The `StoppedSession` keeps the close's sample as one read-only bit, `admitted_at_close()`. It is true when the sample's state bits were 1 or 3.
  - The host takes it with the returned outcome, to label a signal after a `publish` return that does not enter phase D (J1 r5:567, LD-r5-1; J3b, J1 r5:882).
  - It is held in memory and adds no durability point.
- **Outcomes.** No outcome variant is added. A checkpoint refusal after an operator latch is `Refused(InstallationTermination)`, on S10.5's row. The host projects from the returned outcome, never from the gate's state (J1 r5 8.3).

**S10.4 Items 7 and 8: `StopCause::Operator` and the `REV` reason `operator` (J1 r5:537, :541, :653).**
- **The stop cause.** The operation's stop causes gain `StopCause::Operator { signal }`. It is recorded only as the first stop, under the existing first-cause rule (`operation_guard.rs:96-106`; X4 r7 items 7 and 8). Its home is X4's type (LD9-4).
- **The reason.** The closed `REV` reason set (`commit_session.rs:62-104`) gains `operator`, S6's own word for an operator stop (SL:491). `StopCause::Operator` maps to it.
  - Item 7's "the gate is latched" now includes a cancellation latch.
  - When another stop came first (`AlreadyStopped`), the `REV` keeps that cause's reason (J1 r5:598).
- **The reserve.** Item 8's reserve is the largest bounded `REV` body cost over the closed set, plus the `CLN`'s. `operator` is shorter than `observer-fail-stop`, so the exact cost and its pin are unchanged (J1 r5:541).

**S10.5 Item 9: the row "operator stop" (J1 r5:542, :654).**
- **The row.** `InstallationTermination::Interrupted { signal }` is the row of `StopCause::Operator`. It projects to D9 class `interrupted`, exit 130, and the signal, with no errorCode, faultCause or detail (WS:1363-1364; COMMON4 `StepTermination`).
- **Its place.** It is a new variant of 468c's closed vocabulary, as item 9's r6 rows were. It is the one row of item 9 that is not operational-failed 4.
- **Its projection.** X7 r7 (S9) projects it as the A/B `interrupted` envelope. X7 r7 carries the interrupted form separately, because `InstallationTerminationV1` requires an errorCode (J1 r5:542, :662).
- **No code, class, exit or detail is added.**

**S10.6 Item 7: the `refused()` record (J1 r5:502, :656).**
- `refused()` also ends a session whose attempt never started. The host calls it after a replay refusal, an analysis refusal or a phase-A cancellation, then `finish`, exactly once (J1 r5:486-487; J-C12).
- It latches the gate.
- For such a session step 0 has not run, so there is no reserve. `finish` appends nothing, and it runs its end step only on an open attempt ledger (item 7 step 3).
- Under S10.2 it also closes the window.

**S10.7 Item 11: the opaque surface.** X8's isolated fixtures (r7) gain these cases:
- `CancellationLatch` constructed, `Default`ed, cloned or deserialized; a second `latch` on one token (J-C15);
- `ReservedExecutionId` built from bytes or text; `CommitSession` given any other ExecutionId (J-C4b).

J3a and J3b add them as X8 fixtures under X8 r3's driver, as X3d-1 and X3d-2 added theirs.

**S10.8 Item 13: units J3a and J3b (J1 r5:856, :881-882; M3P:317).**
- **J3a** carries S10.1: `open`'s reservation, with `ExecutionIdReservations` and `ReservedExecutionId`.
  - **Tests:** J-C4b.
  - **Depends on:** J1, S2 to S7, and S10's item 2.
- **J3b** carries the rest: `take_cancellation_latch`, the window's opening and closing steps, `StopCause::Operator`, the `REV` reason `operator`, the row, the `refused()` uses and `admitted_at_close()`.
  - **Tests:** J-C12, J-C15 and J-C15b, and the existing exhaustive gate-trace test extended to the third source (F41).
  - **Rows:** S10.9's.
  - **Depends on:** J3a and S8 to S12. S12-C and S12-U wait for S21.
- **With X4 r8.** S10's latch code lands only once S11, X4 r8, is accepted (LD9-5). Both land with J3b (M3-L r5 item 16f).

**S10.9 Crash windows and X9 rows (J1 r5 item 12; LD9-6).**
- **No new crash point.** The latch reuses `x4.gate.latch.after`. The window bits, the close's sample and the ExecutionId reservation are in memory. `operator` adds one end-path body inside the existing reserve (J1 r5:840).
- **The rows S10 needs are J1's, in X9 r17's `S12-` section** (J1 r5:833-839):
  - **S12-B** (phase B, after the `SEAL`): a hold at `x3d.publish.after-staging`, then a signal. F38's expectation, with `REV(operator)` and the interrupted projection.
  - **S12-C** (phase C): a hold at `x3c.evidence.commit.before#1`, then a signal. F39's expectation, with `REV` reason `operator`. It waits for S21.
  - **S12-U** (phase C, then an undetermined `COMMIT`): S12-C with `fail-after` at `x3c.evidence.commit`. F40's expectation, never `interrupted` and never F39. It waits for S21.
- **S12-D and S12-O** are the phase D and phase O rows, X7 r7's and S18's. There the window is closed and no latch is taken. They test nothing of S10's beyond what J-C15 tests in process.
- **Phase B before the `SEAL`** needs no row of its own (LD9-6). That is a latch seen at step 3.2. Its durable path is F18's: refused at the first checkpoint, no `SEAL`, the `REV` appended from the reserve, and no `CLN`. Only the in-memory source and the `REV` reason differ. J-C15b tests it in process at step 3.1.
- **Existing rows keep their transcribed values** (X9:1089; J1 r5:832): F00's census at `x3d.session.execution-draw`, F34's injected id, F18, F19, F38, F39, F40 and F41. The close's sample gives the same `latchedAfterAdmission` that the load did.

**S10.10 Lead decisions.** Each is made under the owner's standing direction of 2026-09-30, where the consumers leave X3d's side open.
- **LD9-1. Who opens the window, and when.** J1 fixes the point: "when `prepare_commit`'s attempt row commits" (J1 r5:520). Storage admits the attempt row, but the gate is security's.
  - **Decision.** A session step opens the window. `prepare_commit` calls it between step 4's successful `COMMIT` and step 6's first object (S10.2).
  - **Rejected:**
    - **Opening at `prepare_commit`'s `Ok` return.** Step 6's objects would fall outside the window, contrary to J1's point, and a latch there would be a no-op.
    - **Storage setting the bit.** Storage holds no security state and mints none (item 1).
    - **Opening at `open` or at step 0.** Phase A does not use the latch (J1 r5:555), and a latch before the attempt row would stop an attempt that has no row.
- **LD9-2. `open`'s refusal closes the window too.** J1's list of closing returns (J1 r5:522-527) omits it. That refusal also produces a `StoppedSession` (`commit_session.rs:572-587`).
  - **Decision.** J1's rule governs: the window closes in every step that produces a `StoppedSession` (J1 r5:521), `open`'s refusal included. No latch can exist there, because the token comes from a `CommitSession`, so the close changes no outcome.
  - **Rejected: a closed list of returns.** A producer left off the list would need its own ruling.
- **LD9-3. How the close's admission bit reaches the host.** J1 r5 8.2 (LD-r5-1) and J3b's row require it (J1 r5:567, :882). J1 8.6's X3d list does not say where it lives.
  - **Decision.** `StoppedSession::admitted_at_close()`, a read-only bit (S10.3).
  - **Rejected:**
    - **A new `CommitOutcome` field or variant.** Item 6's outcomes would change, and X7 matches them exhaustively. J1 8.6 changes no X3d outcome.
    - **The host reading the gate after the return.** The observer can still latch after the close, because it ignores the window bits (J1 r5:538). J1 also forbids selecting from the gate's state (8.3).
    - **Inferring B or C from the outcome alone.** A `CommitUndetermined` from `publish` can be either: an uncertain journal outcome (B) or an undetermined evidence `COMMIT` (C) (J1 r5:569-570).
- **LD9-4. `StopCause::Operator`'s home.** `StopCause` is X4's type (`operation_guard.rs:96-106`; X4 r7 items 7 and 8). J1 8.6 assigns the variant to X3d r9 (J1 r5:653), and S11's row does not name it (J1 r5:857).
  - **Decision.** This revision carries the variant, its `REV` mapping and its row, under X4's existing first-cause rule. X4 r8 records the variant in its own stop-cause list, as a record only (S10.11).
  - **Rejected:**
    - **Moving it to X4 r8.** J1 8.6 and M3P:317 expect X3d r9 to carry it.
    - **An operator record outside `StopCause`.** `AlreadyStopped` and the `REV` reason must come from one first-cause record (J1 r5:537, :598).
- **LD9-5. S10 before S11.** The latch and the window use the gate word that X4 r8 (S11) defines, and X4 r8 is not yet written. M3-L r5 item 16f has X3d r9, X4 r8 and X7 r7 each reviewed on their own, landing with J3b.
  - **Decision.** This section states X3d's half: the source, the token, where the window opens and closes, the results and the sample. For the word's encoding, the masked compare-exchange loops, the state decoding and the never-reset rule, it cites J1 8.1 and S11, and decides none of them. S10's latch code lands only once X4 r8 is accepted, which J3b's dependency on S8 to S12 already requires. S10.1 does not depend on S11, and it gates J3a (M3P:317).
  - **Rejected:**
    - **Writing the gate-word law here.** X4 owns `FinalGate` (`commit_authority.rs`; X4 item 7).
    - **Holding X3d r9 until X4 r8 exists.** It would hold J3a's reservation and CL-1 for no gain.
- **LD9-6. No X9 row beyond S12's.** J1 names S12-B, -C and -U for the latch.
  - **Decision.** S10 needs those three and no other (S10.9).
  - **Rejected:**
    - **A row for phase B before the `SEAL`.** F18 already qualifies that end path's durable steps. The difference is an in-memory source and a reason string, and J-C15b tests it in process.
    - **Latch variants of S12-D and S12-O.** The window is closed there.

**S10.11 Cross-law items (S10).**
- **X4 r8 (S11).** It owns the gate word's two window bits, the masked compare-exchange loops (`admit` among them), `state` decoding the state bits alone, and the never-reset rule (J1 r5:538-539, :857). It also records `StopCause::Operator` (LD9-4).
- **X7 r7 (S9).** It projects `Refused(Interrupted { signal })` (J1 r5:662). J3b's host side reads `admitted_at_close()` for the phase label (LD9-3).
- **S21.** S12-C and S12-U wait for it, as does every rule-1 or rule-2 termination delivered for a signal (J1 r5:606-610).
- **X8, record only.** X8's owner rows gain `CancellationLatch` when J3b adds its fixtures (S10.7). No X8 rule changes.
- **X9 r17.** Its `S12-` section transcribes S12-B, -C and -U before any run (J1 r5:833). S10 adds no row.

## Forbidden substitutes

- A storage-owned or contracts-owned `CommitSession`, or any authority type with a public constructor.
- More than one commit per `ProjectOperation`.
- A RunId, boolean or `RunCandidate` in place of `ReplayedRun`.
- `INSERT OR REPLACE`, or a new SEAL, on a duplicate ExecutionId.
- Acquiring the ledger before the journal, or either one under level 4.
- Committing in the staging callback, or without the `AdmissionPermit`.
- Releasing level 4 before `COMMIT` on a continuing path.
- A second gate, or a gate reset.
- Relabelling an admitted outcome after a latch.
- Retrying an undetermined commit, or reading back its outcome on the write path.
- Calling lifecycle from storage.
- An end path whose `REV` or `CLN` budget was not reserved first.
- A `REV` appended inside `publish`, or after an uncertain journal commit.
- (r5) A carrier read, reconciliation, end step or floor copy by `finish` after an uncertain journal commit or barrier.
- (r6) Spending the settlement reserve on anything but item 7's `REV` and `CLN` appends: a reconciliation, a witness write outside those appends, the end step, a floor copy or the rollover.
- (r6) Refilling the reserve, a second settlement reserve on one ledger, or a reserve held by storage or reachable from a `WorkScope`.
- (r6) Spending the reserve after any uncertain outcome, or a `CLN` after a failed end-path `REV`.
- (r6) The end step on a closed attempt ledger.
- (r6) A certain native failure reported as a value to keep the attempt ledger open, or a second or carved ledger for the end path.
- `PublishedCommit` before a successful `COMMIT`.
- An external adapter or `SealOutcome` accepted by storage.
- A production seam that supplies a `ProjectOperation` or `ReplayedRun`.
- (r8) Comparing a Run's evaluator closure with the session's core closure, or taking the session's side of step 1 from the Run, a worker claim, a build-time string or a test binding copied from the Run.
- (r9, S10) A cancellation latch outside its window, minted twice for one operation, or used as authority (J1 r5:658, :913).
- (r9, S10) The outcome selected from the gate's state rather than from the returned outcome (J1 r5:658, :914).
- (r9, S10) Closing the window on `Ok(PreparedCommit)`, or anywhere a `StoppedSession` is not produced (J1 r5:916).
- (r9, S10) A session ExecutionId used before its process reservation; a reservation released or reused (J1 r5:233, :908).

## Not claimed

- CLI enablement, and any command that commits (X11, M3).
- `ReplayedRun` production (X5), read-only recovery and settlement (X6), and finalization and delivery (X7).
- Brokered effects and their rollback (M5).
- Carrier migration (F46–F51).
- Generation rollover itself, which belongs to lifecycle under the fence and is routed by X7.
- Process-level crash qualification (X9).
- A positive backup detector.
