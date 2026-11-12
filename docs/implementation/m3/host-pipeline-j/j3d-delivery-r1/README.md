# J3D-DELIVERY: how the durable pipeline derives, decides and delivers a committed Run's result

2026-11-11. Drafted by a lead-dispatched design author (Claude Opus 5.5, route R2-DEEP, effort medium; preflight
`ROUTE-OK R2-DEEP claude claude-opus-5-5/medium`) for unit J3d-TS (`LC/j3d-ts/SCOPE-r1.md` C6-C8, questions Q3, Q4, Q8,
Q11), answering review finding R2 and its blob-lookup advisory (`LC/j3d-ts/review-opus/VERDICT.md`).
Status: **PROPOSED, r2.** r2 applies the independent review (`LC/j3d-ts/review-opus-delivery/VERDICT.md`, R1-R5,
A1-A7) under the lead's rulings: **D1's refusal rule is reversed** (a refused derivation no longer stops the commit);
the derivation runs before the signal check; R2-R5 and A1-A7 are applied. It needs a cross-vendor review, then adoption
by the lead (clauses on law records) and the project owner (clauses marked **owner**). It binds nothing and changes no
existing file, schema, registry or lock. Marks: **SETTLED-BY-TEXT** (the texts decide; only the reading is recorded),
**PROPOSED** (new rule, or a lead ruling not stated by a text), **OPEN** (a named decision is needed).

## Short names

Architecture main `3e4203f0f`. Product: **P** = branch `j3d-ts-r1` @ `16726a27` (worktree `opensip-j3d-ts`; paths
under `crates/`), whose finalize hook is commits `eb7e5d99` (tests), `2bd68ae2`, `6fe8135a` (tests).
`LC` = `.opensip-implementation-cache/lead-2026-10-25`.

| Name | Document |
|---|---|
| **MJ** | `docs/implementation/m3/host-pipeline-j/PROPOSAL.md` (M3-J1 r7, accepted; the live text) |
| **X7** / **X5** | `docs/implementation/m2/finalization-x7/PROPOSAL.md` (r7, accepted) / `replay-join-x5/PROPOSAL-r3.md` |
| **RTC** | `docs/coop/design-corrections/foundation/run-termination-contract.v1.md` |
| **WS** / **WPC** | `docs/v2/contracts/product-v1/workflows-and-surfaces.md` / `docs/coop/design-corrections/workflows/workflow-projection-contract.v3.md` (model `workflow_projection_model.v3.py`, **WPM**) |
| **CINV** / **MC8** | `docs/coop/design-corrections/workflows/command-inventory.v3.json` / `docs/implementation/m3/snapshot-plan-c/PROPOSAL-r8.md` |
| **ENV7** / **INV5** / **COMMON4** | product `schemas/sources/` `command-envelope-v7` / `invocation-v5` / `common-v4` `.schema.json` |
| **PA1** | `LC/pa1/PLAN-AMENDMENT-TS1-r3.md` (the TS1 plan amendment) |
| **D8** | architecture branch `d8-finding-explanation-r1` @ `b58e92405`, `docs/implementation/m4/d8-finding-explanation-r1/CONTRACT.md` (draft) |

**Extends** MJ item 7 (the order, MJ:536-545) and X7 item 1 (order) by one pure step that changes no outcome.
**Supersedes, for the durable analysis path only,** X7:172 "`finalize` lends it `&PublishedCommit` only" (what the
phase is lent; nothing else in X7 item 4 changes) and P's `DeliveryPhase::replayed` comment
(`host/src/finalization.rs:264-273`). Every other selector stands.

## Normative clauses

**D1. Where and when the analysis projection is derived, and what a refusal does. PROPOSED (lead ruling; law
records: MJ item 7, X7:172).**
- *Texts.* The delivery phase "runs after `StoppedSession::finish` has … released the writer lease" (X7:171); "`finalize`
  lends it `&PublishedCommit` only" (X7:172); rejected: "delivering inside the writer's session before `finish`"
  (X7:179). RTC derives only from content admitted by complete replay (RTC:43-46) and applies "only when … the Run is
  committed" (RTC:18-19); §7.3 needs the receipt (RTC:242-256). MJ assigns derivation and composition to J3d (MJ:932).
  `prepare_commit` consumes the `ReplayedRun` (`storage/src/commit.rs:460`); X5 item 6: only finalization replays (X5:123).
- *Rule.* `finalize` calls the pure `run_termination::derive(&replayed)` once, **after replay and before the signal
  check** (`port.observed()`), and so before `prepare_commit`. No delivery-phase code runs under the open session:
  `DeliveryPhase::replayed` is removed. The result is carried as a value, `Result<Derived, Refusal>` (plain data, nothing
  that can open the store). **The derivation never changes whether or how the Run commits:** the commit proceeds exactly
  as it would without it. After `finish` the phase is lent `&PublishedCommit` and that value, and composes RTC §7 there.
  If the attempt does not commit, the value is dropped unread.
- *Why before the signal check.* `observed()` moves the port to `preparing` (`finalization/cancellation.rs:124-131`), so
  a signal during a later `derive` would be latched at `arm` and handled as phase B (an attempt row and a REV). Before the
  check it ends in phase A with nothing appended (MJ:600).
- *Bound.* In memory, charged to no ledger, like replay (X5:45; X7:244); every retained lookup keyed (the linear
  `Retained::blob` scan, `run_termination.rs:250-259`, is replaced). X5:43's "lengthens the lease hold with pure work"
  was withdrawn for replay only (MJ:534), so the added hold is **owed a measurement before the code lands**: `derive`
  timed beside `replay_candidate` on both crash-matrix synthetic candidates (including the rows under the 5000 ms timing
  guard, `host/tests/commit_matrix_tests.rs:1620-1637`, `security/src/crash_matrix_support/run_record.rs:152`), both TS1
  fixtures, and a candidate at the `REPLAY_LIMITS` bounds.
- *Rows.* (i) **Derivation refused** (RTC §3-§5, `CauseUnregistered`, `Uncovered`): the Run commits as it would have;
  the delivery phase reports **row 43**: operational-failed 4, `DELIVERY.REQUIRED_FAILED` / delivery-required,
  `DELIVERY.RENDERER_FAILED_AFTER_COMMIT`, the runId (MJ:815); the RTC key goes to the operational record.
  (ii) **Composition refused** (RTC §7.2-§7.3, §7.6): the same row 43. (iii) **Commit refused, undetermined,
  exhausted or existing-attempt:** their own rows (36-40), unchanged; the value is dropped. (iv) **Latched commit**:
  row 42, unchanged; no delivery phase.
- *Basis (not normative).* The Run record is the evidence; the projection is a view derived from it. A refusal can be a
  defect or gap in this host's derivation code or registry copy (`Uncovered`, `run_termination.rs:58-60`; a registry copy
  not pinned; equivalence with the contract's goldens not yet shown, Q12), which a corrected host could project from
  the same retained bytes (RTC:54-58). Reporting no outcome is fail-closed for what is claimed; committing is fail-safe
  for what is kept. Row 43's own condition holds: "a missing field or projection exception is a required-delivery
  operational fault … If a Run was already committed, the termination retains its RunId and the after-commit detail"
  (WS:1128-1134). A committed Run whose delivery failed is already a known state: the F16 row keeps the runId (X7:160);
  "a delivery failure never retries the commit and never relabels the Run" (X7:174; WS:1141-1145, "no rewrite of the
  Run"); its remedy is "the Run is committed; rerun opensip query run.show with the runId" (CINV:1800); read-only
  recovery reports it committed (MJ:860, J-C21; lead ruling Q5). **No text forbids committing after a refused derivation:**
  RTC §2's "no termination" is for a Run `close_run` refuses (RTC:45-46), which replay already stops; RTC §3 forbids a
  *silent* `VERDICT.INDETERMINATE` (RTC:84-85), and row 43 is not silent.
- *Strongest argument.* X7 item 4's order stands and only its lend changes; no admitted evidence is lost to a host
  defect; crash-matrix outcomes are unchanged. *Weakest point.* A committed Run whose projection no current host can
  derive exists durably. Its reader sees exit 4 `DELIVERY.REQUIRED_FAILED`, `RENDERER_FAILED_AFTER_COMMIT` and the
  runId, a `committed-historically` recovery, and no verdict, reasons or findings until a corrected host re-derives them;
  the RTC key is only in the operational record. RTC §3 calls its own refusal a host invariant violation (RTC:84-87),
  yet its public termination here is WS's delivery-required row, not host-invariant.

**D2. The output decision after R12. PROPOSED (lead ruling Q3; no text states the split).**
- *Texts.* The output decision point is "the single cancellation check after `finish` and step 1's projection"
  (MJ:676); MJ assigns modules (J2a's pure state machine, MJ:927; J3b's output decision point, MJ:931) but never says
  which function decides the ends before R12. Phase D's runId comes "only through the `&PublishedCommit` projection"
  (X7:154); re-deciding is forbidden (X7:518).
- *Rule.* Every end after R12 is decided once, by `finalization::output_decision`; every end before R12 by
  `Decision::decide` (`invocation.rs:843`). Neither calls the other: `decide` takes a runId from a `String`
  (`invocation.rs:751-753`, :863-864), which X7:154 excludes as the post-session envelope's source. `decide` has no
  production caller today, so its commit branches (rows 38, 42, 47) are never reached in production. **The equivalence
  test covers only the rows both reach in production:** 44, 46, 48 and the refusals before commit; rows 38, 42, 43 and
  47 are excluded (only `output_decision` reaches them). Whether `decide`'s commit branches stay is the lead's.

**D3. The analysis envelope at TS1. SETTLED-BY-TEXT (members); OPEN (producers; owner: what the user sees).**
- *Committed and delivered:* `kind: run` (ENV7:183-196 requires `run`, `projectId`). Members and sources:

| Member | Source | Producer today |
|---|---|---|
| `requestId`, `projectId`, `exitCode` | R0; R4; class | J2a / J3d |
| `termination` | WS:233-240 aggregate over step 0's RTC §7 composition and step 1 | port (interim) |
| `run.authority`, `run.runId` | `&PublishedCommit` (X7:147, :154) | X7 |
| `run.planId`, `verdict`, `deficiency`, `secondaryDeficiencies`, `coverageId` | the carried value; sealed verdict (WPC:181); RTC §4-§5 | port (pass/fail pair: O2) |
| `run.requiredCoverage` | WPC:182, :196 (per rule; Run-level reduction: O2) | **none** |
| `findings` | WPC `FindingSurface`, `project_finding_surfaces` (WPM:1111-1135; WPC:117-118) | **none** |
| `availability` | the invocation's selection (WS:1318-1332) | **none** (J2b-TS) |
| `comparison-counts` (`analyze` only, CINV:142) | **no owning text located** | **none** |
| `retentionDisclosure` | MJ:753-755 | J3d (J-BS) |

  Absent: `invocation` (RTC §7.2's attempts are a composition input), `errors`, `diagnostics`, `projectRoot`, and every
  query, mutation, doctor, meta and advisory member. Durable `analyze` is reachable (`invocation.rs:56-62`).
- *Totality.* `findings`, `required-coverage`, `capability-availability` (both commands) and `comparison-counts`
  (`analyze`) are parity fields (CINV:7-34, :114-143); the projection must be total, an empty findings array is "a real
  empty result; it is never inferred", an omission is `DELIVERY.REQUIRED_FAILED` (WS:1124, :1128-1137, :1325-1332).
  **No lawful `kind: run` envelope exists without these producers.** D8 changes the findings row only at
  `command-envelope:8` (D8:546), an M4 surface, so it does not block TS1.
- *Refusal ends:* `kind: failure`; J2a's item 10 projection; `run` is forbidden even with a runId (ENV7:249; rows 42, 43
  carry it in `termination`). Row 46 is the empty-errors branch.
- **Owner option 1: port the producers.** Their Run-derived inputs come from the same carried value, computed inside
  `finalize` with `derive` by D1's rule (one pure call, before the signal check; a refusal of any part is D1's case (i)):
  the `FindingSurface` rows from the Run's finding3 occurrences and the proof's `waivedFindingIds`; the per-rule and
  Run-level `requiredCoverage` from the sealed rule results. Invocation-held inputs reach the phase from its caller,
  never from the Run: `availability` (the selection), the attempts (C8) and RTC §7.5 row 2's installation observation
  (RTC:235; without it a `PROVIDER_UNAVAILABLE` Run refuses `DETAIL_REQUIRED` and takes row 43). `comparison-counts`
  needs an owning text first, or TS1 is restricted to `default`. Then the committed Run and row 47 deliver `kind: run`.
- **Owner option 2: the milestone Run ends on row 43.** Lawful and honest only if PA1 §1.7 (PA1:210) names the envelope
  producers as a deferred edge of J3d-TS, carried to J3d-RS (R-TS1.1, PA1:61: "Nothing else is removed"), and the
  R-TS1.4 disclosure line carries it. The M3-M-TS1 record then claims exit 4 `DELIVERY.REQUIRED_FAILED` with the runId,
  the commit, the read-back and the harness-checked projection, not a delivered envelope.
- *Row 47 (phase D signal).* `kind: run` needs the full `run` member (MJ:603; INV5:1406), including `requiredCoverage`,
  which the carried value lacks today. Under option 1 it is delivered from the ported value. Under option 2 its
  projection fails and is replaced by row 43 with the runId (MJ:604; WS:1128-1134): a phase-D signal ends exit 4, not
  130, and the record says so.

**D4. The synthetic-trust label. PROPOSED (reading; owner to confirm).** X7 item 2 sets `run.authority:
authoritative` from every `PublishedCommit` (X7:147); INV5: "authoritative: a committed Run with receipt". MC8 item 8:
synthetic-trust runs "are never authoritative", and C2-T8 refuses a synthetic-labelled Run on any authoritative surface
(MC8:456, :465). *Reading:* `run.authority` is committed-versus-ephemeral standing (RTC §7.4), not evidence standing;
C2-T8 is enforced by consuming surfaces, none at TS1. *Rule:* the envelope carries nothing new; the M3-M-TS1 record
labels the Run synthetic-trust with the R-TS1.4 disclosure. Under option 2 no `run` member is emitted at all
(ENV7:249), so the reading never reaches a TS1 consumer. *Weakest point:* under option 1 a bare-envelope reader sees
`authoritative` on a synthetic Run.

**D5. Measuring replay. OPEN.** No text fixes how (OD-DESIGN-FOLLOWUPS-1 §2; O1-b's table has no `replay`). Lead's
interim (Q8): the harness times `replay_candidate` on the same candidate, and `derive` beside it (D1's owed measurement).

## Open points

- **O1 (lead, before D1's code).** D1's measurement; whether the synthetic candidates pass `derive` now only decides
  whether those rows show row 43, not whether they commit.
- **O2 (owner; lead authors a WPC successor).** The `deficiency` pair of a `pass`/`fail` Run, and the Run-level
  `requiredCoverage` reduction (WPC:182 is per rule); also an owner for `comparison-counts`.
- **O3. Closed** (lead ruling on this review, R1): a refused derivation commits and is reported on row 43 (D1).
- **O4 (owner).** C2-T8's enforcement point (MC8:465) before any authoritative surface lands.

## Consequences (owning units)

- J3d-TS C6 (J3b's reviewed file): revert the hook's three commits (`eb7e5d99`, `2bd68ae2`, `6fe8135a`): the trait
  method, the call, the test phase's `replayed` (`finalization_tests.rs:572-614`), the lend tests (:855, :883-925), and
  the order pin entry `"phase.replayed(&replayed);"` (:1021). Add `derive` to the order pin between replay and
  `port.observed()`; controls: a refused derivation commits with an unchanged commit outcome and gives row 43 with the
  runId; a signal during `derive` is phase A. Keyed lookups. Crash-matrix outcomes unchanged; only timing (D1's
  measurement) and the lead sets owed on the new change.
- J3d-TS C7: `compose` in the phase after `finish`; D3's producers (option 1) or the row-43 TS1 limit (option 2).
- Lead: MJ item 7 order step and X7:172's lend (law records); D2's equivalence test scope and `decide`'s commit
  branches; with the owner's decision, the PA1 §1.7 and R-TS1.4 amendment under option 2.

## Rejected alternatives

- **(a) The hook as built, bounded.** Phase code under the open session reverses X7:171 and X7:179's rejection.
- **(c) The `ReplayedRun` outliving `prepare_commit`.** Changes storage's reviewed signature for nothing D1 needs;
  **(c2) a second replay after `finish`** breaks X5 item 6's single call and doubles the measured cost.
- **(r1) Refusing the commit on a refused derivation.** It loses admitted evidence to a defect in this host's port or
  registry copy, and makes the derivation decide what commits (lead ruling R1).
- **`derive` after the signal check:** a signal during it becomes phase B for no benefit.
- **Emitting `findings: []` or omitting a parity field** on a committed Run (WS:1124, :1128-1137).

## What this record does not do

It adds no public code, class, exit, detail, schema member or envelope major, and no ledger. It does not write C6-C8,
the producers, the D8 successor, C2-T8 or read-back (Q5). It does not decide O2, O4, owner options 1 or 2, or amend PA1.
