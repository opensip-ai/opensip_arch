# J3D-DELIVERY: how the durable pipeline derives, decides and delivers a committed Run's result

2026-11-11. Drafted by a lead-dispatched design author (Claude Opus 5.5, route R2-DEEP, effort medium; preflight
`ROUTE-OK R2-DEEP claude claude-opus-5-5/medium`) for unit J3d-TS (`LC/j3d-ts/SCOPE-r1.md` C6-C8, questions Q3, Q4, Q8,
Q11), answering review finding R2 and its blob-lookup advisory (`LC/j3d-ts/review-opus/VERDICT.md`).
Status: **PROPOSED, r1.** It needs an independent review, a cross-vendor review, then adoption by the lead (clauses on
law records) and the project owner (clauses marked **owner**). It binds nothing and changes no existing file, schema,
registry or lock. Marks: **SETTLED-BY-TEXT** (the texts decide; only the reading is recorded), **PROPOSED** (new rule,
needs review), **OPEN** (a named decision is needed).

## Short names

Architecture main `3e4203f0f`. Product: **P** = branch `j3d-ts-r1` @ `16726a27` (worktree `opensip-j3d-ts`; paths
under `crates/`), whose finalize hook is commit `2bd68ae2`. `LC` = `.opensip-implementation-cache/lead-2026-10-25`.

| Name | Document |
|---|---|
| **MJ** | `docs/implementation/m3/host-pipeline-j/PROPOSAL.md` (M3-J1 r7, accepted; the live text) |
| **X7** / **X5** | `docs/implementation/m2/finalization-x7/PROPOSAL.md` (r7, accepted) / `replay-join-x5/PROPOSAL-r3.md` |
| **RTC** | `docs/coop/design-corrections/foundation/run-termination-contract.v1.md` |
| **WS** / **WPC** | `docs/v2/contracts/product-v1/workflows-and-surfaces.md` / `docs/coop/design-corrections/workflows/workflow-projection-contract.v3.md` (model `workflow_projection_model.v3.py`, **WPM**) |
| **CINV** / **MC8** | `docs/coop/design-corrections/workflows/command-inventory.v3.json` / `docs/implementation/m3/snapshot-plan-c/PROPOSAL-r8.md` |
| **ENV7** / **INV5** / **COMMON4** | product `schemas/sources/` `command-envelope-v7` / `invocation-v5` / `common-v4` `.schema.json` |
| **D8** | architecture branch `d8-finding-explanation-r1` @ `b58e92405`, `docs/implementation/m4/d8-finding-explanation-r1/CONTRACT.md` (draft) |

**Extends** MJ item 7 (the order, MJ:536-545) and item 10 (a basis on rows 13/29, MJ:801), X7 item 1 (order) and
item 4. **Supersedes, for the durable analysis path only,** X7:172 "`finalize` lends it `&PublishedCommit` only" (D1)
and P's `DeliveryPhase::replayed` comment (`host/src/finalization.rs:264-273`). Every other selector stands.

## Normative clauses

**D1. Where and when the analysis projection is derived. PROPOSED (lead: law records MJ items 7, 10 and X7).**
- *Texts.* X7 item 4: the delivery phase "runs after `StoppedSession::finish` has … released the writer lease"
  (X7:171); "`finalize` lends it `&PublishedCommit` only, and the phase itself holds just the evaluation result" (X7:172);
  rejected: "delivering inside the writer's session before `finish`" (X7:179). RTC derives "only" from content admitted
  by complete replay and applies "only when … the Run is committed" (RTC:18-19, :43-46); its §7.3 joins need the commit
  receipt (RTC:242-256). MJ assigns the derivation and §7 composition to J3d (MJ:932). `prepare_commit` consumes the
  `ReplayedRun` (`storage/src/commit.rs:460`). X5 item 6: only finalization calls `replay_candidate` (X5:123).
- *Rule.* `finalize` itself, after replay and the signal check and before `prepare_commit`, calls the pure
  `run_termination::derive(&replayed)` once. No phase code runs under the open session: `DeliveryPhase::replayed` is
  removed. On `Ok(DerivedRun)` finalize carries that value (plain data, nothing that can open the store) and, after
  `finish`, lends the phase `&PublishedCommit` and `&DerivedRun`; the phase composes RTC §7 there (`compose`).
- *Bound.* The derivation reads only the replayed Run in memory and is charged to no ledger, like replay (X5:45; X7:244).
  Its work is O(n log n) in the replay-admitted content that `REPLAY_LIMITS` bound: every retained lookup is keyed
  (the linear `Retained::blob` scan, `run_termination.rs:250-259`, becomes a keyed lookup).
- *A refused derivation (RTC §3-§5 and `Uncovered`) ends the attempt before commit*, as a replay refusal does
  (MJ:530-531): `refused()`, `finish`, nothing appended; projected on the host-invariant route of rows 13/29
  (operational-failed 4, `SYSTEM.OUTCOME.ILLEGAL_STATE` / host-invariant, `HOST.INVARIANT_VIOLATED`; the RTC key to the
  operational record; no runId; `Observation::HostInvariant`, `outcomes.rs:1183`). No Run is committed.
- *A refused composition (RTC §7.2-§7.3, §7.6) is after commit* and takes WS's projection-exception row with the runId:
  row 43 (WS:1128-1137; MJ:815). The derivation-before-commit makes this a host-bug path only.
- *Basis (not normative).* RTC §3 names its empty-population refusal "a host invariant violation" (RTC:84-87); no text
  says whether such a Run may be committed (**silent**). Committing it publishes a Run whose projection no conforming host
  or verifier can ever derive (RTC §2, :54-58); refusing first keeps that state unreachable. The §7.3 inventory join
  (receipt `inventoryDigest` = `commit_inventory` of the derived content) proves after commit that the derived content is
  the committed content, so deriving before commit loses nothing RTC:18-19 protects.
- *Strongest argument.* X7 item 4's order and lease release stand unchanged; only a pure function of finalization's own
  runs under the lease, as replay already does. *Weakest point.* It adds a second pre-commit refusal between replay and
  `prepare_commit`, and lends a second value, so MJ item 7's order list and X7:172's "only" are amended, not obeyed.

**D2. The output decision after R12. SETTLED-BY-TEXT (ownership); PROPOSED (equivalence).**
- *Texts.* The output decision point is "the single cancellation check after `finish` and step 1's projection"
  (MJ:676); it is J3b's code (MJ:931), in X7 item 4 r7 (X7:183); J2a owns the pure join state machine and item 10's
  projection (MJ:927). Phase D's runId comes "only through the `&PublishedCommit` projection" (X7:154); re-deciding the
  envelope is forbidden (X7:518).
- *Rule.* Every end after R12 (`open_finalization`'s refusal, `end_before_commit`, `finalize`) is decided once, by
  `finalization::output_decision`. Every end before R12 is decided by `Decision::decide` (`invocation.rs:843`). Neither
  calls the other: `Decision::decide` builds a runId from a `String` (`CommitEvidence::Committed`), which X7:150 forbids
  as the source of a post-R12 envelope. Owed: one equivalence test over the rows both express (38, 42, 46, 47, and the
  unsignalled committed and refused ends), comparing class, exit, code, detail and runId presence.
- *Weakest point.* Two codings of MJ 8.3 remain; only the test keeps them equal.

**D3. The analysis envelope at TS1. SETTLED-BY-TEXT (members); OPEN (producers; owner: what the user sees).**
- *Committed and delivered:* `kind: run` (ENV7:183-196 requires `run`, `projectId`). Members and sources:
  `requestId` (R0); `projectId` (R4); `termination` = WS's aggregate (WS:233-240) over step 0's RTC §7 composition and
  step 1; `exitCode` by class; `run` = INV5 `AnalysisResult` authoritative (INV5:1406): `authority`, `runId` from
  `&PublishedCommit` (X7:147), `planId` (DerivedRun), `verdict` (sealed; WPC:181), `durability: committed`,
  `deficiency`/`secondaryDeficiencies` (RTC §4), `coverageId` only when RTC §5 names one, **`requiredCoverage` (no
  producer)**; `retentionDisclosure` (MJ:753-755); **`findings` (no producer)**; **`availability` (no producer)**.
  Absent: `invocation` (optional; RTC §7.2's attempts are a composition input, not an envelope member), `errors`,
  `diagnostics`, `projectRoot`, and every query, mutation, doctor, meta and advisory member.
- *Totality.* `findings`, `required-coverage` and `capability-availability` are parity fields of `default` and
  `analyze` (CINV:7-34, :114-143); "the host projection must be total over the selected command's `parityFields`",
  "an empty findings array is a real empty result; it is never inferred", an omission is `DELIVERY.REQUIRED_FAILED`
  (WS:1124, :1128-1137; WS:1325-1332 for availability). **So no lawful `kind: run` envelope exists without the three
  producers;** `[]` is lawful only when derived.
- *The findings row has an owner today:* WPC's `FindingSurface` (`project_finding_surfaces`, WPM:1111-1135; WPC:117-118),
  a field copy of the Run's finding3 occurrences and waived ids. D8 changes it only at `command-envelope:8`
  (D8:545-546), an M4 surface; **D8 does not block TS1.**
- *Refusal ends:* `kind: failure`, J2a's item 10 projection and errors composition; `run` is forbidden even where a
  runId exists (ENV7:249; rows 42, 43 carry it in `termination` only). Row 46 is the empty-errors branch (no
  `retentionDisclosure`). Row 47 (phase D) is `kind: run` (MJ:603), so it needs the same `run` members: D1's
  `DerivedRun` supplies them.
- *Proposal (owner).* C7 ports `FindingSurface` and the Run-level `requiredCoverage` from their owners, and takes
  `availability` from the selection's producer, before any `kind: run` envelope is claimed. Until then a committed
  milestone Run truthfully ends on row 43 with its runId, and the M3-M-TS1 record claims the commit, the read-back and
  the derived projection (harness-checked), **not** a delivered analysis envelope.

**D4. The synthetic-trust label. PROPOSED (reading; owner to confirm).** X7 item 2 sets `run.authority:
authoritative` from every `PublishedCommit` (X7:147); INV5 admits no other value beside a `runId`. MC8 item 8 says
synthetic-trust runs "are never authoritative" and "a synthetic-labelled Run is refused by any authoritative surface"
(MC8:456, :466). *Reading:* `run.authority` is the committed-versus-ephemeral standing (WS's ephemeral paragraph), not
evidence standing; MC8's refusal is enforced by the consuming authoritative surfaces (baseline, repair, verify, qualification),
none of which exists at TS1. *Rule:* the envelope carries nothing new; the M3-M-TS1 record labels the Run
synthetic-trust with the R-TS1.4 disclosure; adding a member is a schema successor (owner). *Weakest point:* a reader of
the bare envelope sees `authoritative` on a synthetic Run.

**D5. Measuring replay. OPEN.** No text fixes how: OD-DESIGN-FOLLOWUPS-1 §2 asks for "the admission and replay phase
on its own"; O1-b's phase table has no `replay`. Lead's interim (Q8): the harness times `replay_candidate` on the same
candidate; under D1 it should time `derive` beside it.

## Open points

- **O1 (lead, before D1's code).** Whether the crash-matrix synthetic candidates (`synthetic_run_candidate`,
  `_distinct`) pass `derive`. Under D1 every committing crash-matrix row calls it; if they refuse, those rows change.
- **O2 (owner).** The `deficiency` pair of a `pass` or `fail` Run (`none`, `[]` reads COMMON4's `none`; no owner
  states it), and the Run-level `requiredCoverage` reduction (WPC:182 is per rule): owners not located.
- **O3 (lead).** Whether a refused derivation should instead be committed (the as-built hook's effect): see Rejected.
- **O4 (owner).** C2-T8's enforcement point (MC8:466) before any authoritative surface lands.

## Consequences (owning units)

- J3d-TS C6: revert `2bd68ae2`'s `replayed` method; finalize calls `derive` and carries `DerivedRun` (J3b's reviewed
  file; crash-matrix lead sets owed on the new change, not the hook); `project` takes `&DerivedRun`; keyed blob lookup.
- J3d-TS C7: `compose` in the phase after `finish`; the three producers of D3, or the row-43 TS1 limit.
- Lead: MJ item 7 order step "2a", a basis on rows 13/29, X7:172's lend; the M3-M-TS1 record's claims (D3, D4).

## Rejected alternatives

- **(a) The hook as built, bounded.** Phase code under the open writer session reverses X7:171 and X7:179's rejection;
  any bound is the phase's promise, not finalization's; and it commits a Run whose derivation already refused.
- **(c) The `ReplayedRun` outliving `prepare_commit`.** Changes storage's reviewed signature for a value D1 does not
  need; **(c2) a second replay after `finish`** breaks X5 item 6's single call and doubles the cost OD-DESIGN-FOLLOWUPS-1
  §2 measures.
- **Commit, then report an underivable projection on row 43.** Lawful by WS:1128-1137, but it publishes a permanently
  unprojectable Run (RTC §2) for a defect detectable before commit.
- **Emitting `findings: []` or omitting it on a committed Run** (WS:1124, :1128-1137).

## What this record does not do

It adds no public code, class, exit, detail, schema member or envelope major, and no ledger. It does not write C6-C8,
the FindingSurface port, the D8 successor, C2-T8, read-back (Q5), or any producer outside J3d. It does not decide the
owner's points O2 and O4, nor what the milestone record may claim beyond D3's statement.
