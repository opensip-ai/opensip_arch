# C2A-ORDER-E1: the R10 invocation identity, and the R8/R9 order, for the public durable pre-draw entry

2026-11-12. Drafted by a lead-dispatched design author (Claude Opus 5.5, route R2-DEEP, effort medium; preflight
`ROUTE-OK R2-DEEP claude claude-opus-5-5/medium`) for unit J3d-TS, scope row C2a (CP-J3D-SECPRE-1), questions Q35-Q37
(`LC/j3d-ts/QUESTIONS.md`:628-661), the lead's rulings (`QUESTIONS.md`:680-708, :710-728) and `LC/j3d-ts/C2A-ORDER.md`.
Status: **PROPOSED, r5.** **r5 changes** (lead rulings Q39, Q40, `LC/j3d-ts/QUESTIONS.md`:737-790): E3's open
sentence becomes the lead's ruling (a fresh classification on every route), with the routing fact and controls
E3-C2 to E3-C4; new open point O5 (Q39, which storage choice R7 calls). No sentence of the record said `grants.rs`
has no choice; that error was `C2A-ORDER.md`'s (R7 row). **r4 changes** (`LC/j3d-ts/review-opus-c2a-order/VERDICT-r3.md`, A-a to A-c): wording
only, in "For the project owner": the law records (a) amends; (a)'s dependence on O2; the erratum's leftover state.
**r3 changes** (re-check `LC/j3d-ts/review-opus-c2a-order/VERDICT-r2.md`, F1, F2,
A-i to A-iii): amendments A-11 (M3D:759-762 and :815) and A-12 (MJ:410); controls E1-C8 (an output scan) and E1-C9
(after the floor publication); A-9 names the census's files; A-7 states the attempt-A/attempt-B reading; a section
"For the project owner". r2 applied the independent review (`VERDICT.md`, R1-R3,
A1-A6) and the lead's ruling on Q37 (`QUESTIONS.md`:710-728). **r2 changes:** E1c records option (a) as PROPOSED by
the lead, with numbered amendments, the constructor's inputs, crash behaviour and controls (R1, A2, A5); (b) and the
new (d) become rejected alternatives with their true cost (R2); E3's recheck sentence becomes PROPOSED inside O3
(R3); E2 states that one adopted security record alone places the endpoint after registration (A3), and the code
list marks what depends on O4 (A4); A1 and A6 corrected citations. It needs the cross-vendor review, then adoption by
the lead. **The project owner is told of E1c's choice and of E2's erratum (A3), and may overrule either.** It binds
nothing and changes no existing file. Marks: **SETTLED-BY-TEXT** (the texts decide; only the reading is recorded),
**PROPOSED** (a new rule or a lead ruling no text states), **OPEN** (a named decision is needed).

## For the project owner

- **What (a) puts in the record, and why.** Each trust floor record (the record that moves the trust clock's floor
  forward before analysis) must name the act that wrote it, and the record format requires an execution id there.
  Today no lawful id exists at that point, so (a) gives that one act its own fresh id. That id identifies no analysis
  attempt, and no other record names it.
- **What (a) costs.** Twelve listed law-text items (A-1 to A-12; three are readings with no word change). They amend
  adopted and accepted law records: the pipeline law MJ, the supervisor law M3D (A-11), the pre-draw record SPD (A-9)
  and the trust law X4T (A-8). There is no change to any record format, schema, corpus or selection.
- **What (a) assumes (O2).** (a) assumes the identity contract allows an id that is not an analysis attempt's. If
  that reading is rejected, the identity and workflow contracts' wording changes too, which is yours to approve.
- **What (b), rejected, would cost.** A schema and selection successor, new versions of two record kinds, regenerated
  corpora, and two shapes of one record read back for ever.
- **The step-order erratum (E2).** The pipeline law's table puts the store-endpoint check before project
  registration. The adopted security record does the opposite, and the entry follows it. Visible consequence: when
  the endpoint check refuses on a project's first use, the project stays registered (its registry row, namespace and
  marker remain; the next run hits the same refusal until the core or store changes).
- **The storage check (E3).** The lead also ruled, without a deciding text, that the backup-storage check
  re-observes the installation's storage on every run instead of trusting the value recorded at creation.
- **You may overrule either choice.**

## Short names

Architecture main `fa6fa0fba` (every line below was read there). Product: **P** = `j3d-ts-r1` @ `780c52fc` (worktree
`opensip-j3d-ts`; paths under `crates/` unless stated); product is cited for facts only. `LC` =
`.opensip-implementation-cache/lead-2026-10-25`. SPD was read with its adopted errata E-1 to E-4
(`sec-predraw-1/record-r1/ERRATUM-E*.md`); none changes a line cited here (E-3:77 lists `join_store_endpoint` first
among the durable path's rechecks, inside `pre_draw`).

| Name | Document |
|---|---|
| **MJ** | `docs/implementation/m3/host-pipeline-j/PROPOSAL.md` (M3-J1 r7, accepted) |
| **SPD** | `docs/implementation/m3/sec-predraw-1/record-r1/SUCCESSOR-SEC-PREDRAW-1-r7.md` (adopted, `ADOPTION-SEC-PREDRAW-1.md`) |
| **IE** / **WS** | `docs/v2/contracts/product-v1/identity-and-evidence.md` / `workflows-and-surfaces.md` |
| **OPP** | `docs/implementation/m3/operability/PLAN-r3.md` (the snapshot MJ cites) |
| **L464** / **L467** | `docs/implementation/m2/creation-ingress-464/PROPOSAL.md` (r3) / `initial-publication-467/PROPOSAL.md` |
| **OWN** | `docs/implementation/m2/initial-root-binding-owner-selection-v1/owner.md` |
| **X2** / **X3A5** / **X4T** | `docs/implementation/m2/project-root-x2/PROPOSAL.md` (r10) / `store-admission-x3a/PROPOSAL-r5.md` / `trust-admission-x4t/PROPOSAL.md` (r13) |
| **M3D** | `docs/implementation/m3/supervisor-d/PROPOSAL.md` (M3-D r5, accepted) |
| **M3C** / **M3B** | `docs/implementation/m3/snapshot-plan-c/PROPOSAL-r7.md` / `config-discovery-b/PROPOSAL-r2.md` |
| **TRS** | the private trust record schema: P `tools/security/inputs/trust-record-schema.json`, sha256 `359345411d91…`, pinned by the architecture selection `docs/implementation/m2/core-inventory-v3-selection-v1` (README:39; `…-subject.json`:45) |

## Summary

| Clause | Question | Mark | Rule in one line |
|---|---|---|---|
| E1a | Q37, RequestId | SETTLED-BY-TEXT | The R10 record's `requestId` comes from the lent `&RequestIdentity`, never text. |
| E1b | Q37, ExecutionId | SETTLED-BY-TEXT | Under the present texts no ExecutionId exists that the R10 record may carry, on either route. |
| E1c | Q37, remedy | **PROPOSED** (lead; owner told) | A separately reserved ExecutionId for the R10 trust act, with amendments A-1 to A-12. |
| E2 | Q35, R8/R9 | PROPOSED (lead; owner told) | Registration (R9) before the endpoint (R8); MJ's table order is an erratum. |
| E3 | Q36, R7 | SETTLED-BY-TEXT; the classification PROPOSED (lead) | R7 runs on both routes, over a classification and the flag, before any project effect. |

## Normative clauses

**E1a. The record's RequestId. SETTLED-BY-TEXT.**
- *Texts.* "The RequestId. One per invocation ... It serves as: ... the correlator of every operational record"
  (MJ:235-237). The host "lends `&RequestIdentity` to item 3's entry" (MJ:239). Forbidden: "a RequestId from a caller,
  from text or from a draw other than the ingress's" (MJ:275). "Caller-supplied IDs and reuse are refused" (IE:101).
- *Rule.* The request id is built inside security from the `&RequestIdentity` the entry receives at R3 (its `bytes()`,
  P `platform/src/lib.rs:130-134`). P's `TrustInvocation::new(&str, &str, i64)` (`security/src/trust/live_observation.rs:73`)
  stays fixture-only.

**E1b. Under the present texts, no ExecutionId exists for the R10 record. SETTLED-BY-TEXT.**
- *What the record needs.* X4T's floor write publishes "a new capsule record ... its publication event and descriptor"
  (X4T:183-184) and "reuses 467's existing trust publication producers" (X4T:187). No X4T revision contains
  "invocation" or "ExecutionId". No prose law names the `host-trust-admission` binding. **The record shape is the
  architecture-selected TRS:** `OperationInputV1`'s `host-trust-admission` branch requires `invocation`;
  `InvocationBinding` requires `requestId`, `stepId` and `executionId`, closed; `S4EvaluationInputV2` requires
  `invocation`. P writes it at `trust/floor_publication.rs:798`; X4B's acceptance takes the same value
  (`trust/trust_bootstrap.rs:1311`). P's comment "law X4T r9 item 7" (`live_observation.rs:57-59`) has no text behind it.
- *The ExecutionIds of a durable invocation.* The prelude's "names the creation act in P0 only" (MJ:245); the durable
  attempt's is drawn at `CommitSession::open` (MJ:246); the ephemeral attempt's at its start (MJ:247); the render
  step's "appears only in operational records" (MJ:248). Who reserves: MJ:256-258 lists exactly these. Forbidden: "an
  ExecutionId used by P0, a provider frame, a session or a record before its process reservation" (MJ:278). "A
  reservation is never released or reused in the process" (MJ:253). J-C4b: a first-use invocation "reserves three
  distinct ExecutionIds (prelude, session, render)" (MJ:287).
- *ExecutionId belongs to an attempt.* "Each admitted attempt receives a fresh ExecutionId" (IE:62-63). "Each admitted
  attempt of a step receives a fresh `ExecutionId`" (WS:81). OPP's table: "`ExecutionId` | attempt admission
  (IE:61-63) | before" (OPP:154). "For a durable request the ExecutionId is lawful from the session's open" (MJ:264).
- *R10 and R10a.* R12 "draws the ExecutionId" (MJ:396). R10a: "No analysis-attempt ExecutionId is drawn or reserved"
  (MJ:394). J-C10b, at an R10a refusal: the set "equals its set at R10a's entry: empty on 3a and on the ephemeral path,
  and the creation prelude's alone on 3b" (MJ:413). SPD: "no path here draws or reserves an analysis-attempt
  ExecutionId; a source census over the boundary's sources finds no `ExecutionIdReservations`" (SPD:700-701).
- *Route 3a.* The set is empty at R10a's entry (MJ:413), and nothing is ever released (MJ:253), so nothing was reserved
  at R10. An unreserved id is forbidden (MJ:278). No ExecutionId is lawful at R10.
- *Route 3b.* Only the prelude's is reserved. MJ:268 ("Binding the prelude's ExecutionId to the analysis attempt",
  rejected) does not exclude it alone: R10 precedes the attempt, which starts at the open (MJ:246, :264). L464:68
  does: "The prelude's ExecutionId names the creation act in P0 only, and is never reused. No later operation of the
  invocation uses it". L467:69 agrees: the first ordinary operation enters with "fresh fence, its own barriers, id
  reservation". This holds for `Published`, `LostRace` and `NotPristine`.
- *Other ids.* The session's does not exist before R12 and may not be reserved early (MJ:394, :968). The render's
  appears only in operational records (MJ:248) and is reserved at its attempt's start (MJ:258). The RequestId is not
  an ExecutionId: they are "independent 16-byte host-CSPRNG draws" (IE:77).
- *Conflict.* MJ R10 (MJ:393) needs X4T's floor write, whose selected record needs an ExecutionId; MJ item 2, IE, WS,
  OPP, L464:68 and J-C10b leave none for it. A law change is required.

**E1c. A separately reserved ExecutionId for the R10 trust act. PROPOSED by the lead (`QUESTIONS.md`:712-722), AT
RISK until the cross-vendor review. Not settled by text. The project owner is told and may overrule.**
- *Rule.* The R10 floor publication and X4B's acceptance at R10 carry one ExecutionId, reserved for this invocation's
  durable trust act only, on the model of the creation prelude (MJ:245; L464:68): an id reserved for an act that
  precedes the analysis attempt and used by nothing later.
- *Lead's reasons (`QUESTIONS.md`:715-719).* It changes no pinned record shape, no architecture selection, no corpus and
  no shared binding definition; every trust operation keeps one binding shape; nothing reads this id today (P
  `trust_input_bindings.rs:491-492`, `:654-655` join `executionId` only for the absence and continuity kinds), and no
  production floor record exists yet. Its cost is law text, paid in full below.
- *Where and how.* The entry reserves it with `opensip_platform::reserve_execution_id()` after R9 returns and before it
  calls `durable_pre_draw` (so before R10), on both routes, in the entry's own module. A failed draw or exhaustion
  refuses on security's HostIo row (MJ:252), before any R10 effect, with `created` kept.
- *The constructor's exact inputs.* `TrustInvocation` gains a production constructor taking `&RequestIdentity`,
  `&ReservedExecutionId` and the StepId; no `&str` and no raw bytes. **StepId:** IE:103 makes it the step's position;
  L464:68 gives the prelude "of the command's first step" StepId 0; R10 serves the durable analysis step, so the record
  takes that step's position (0 when it is the first step). No text states this: PROPOSED with the rule.
- *Nothing later uses it.* The `ReservedExecutionId` is dropped by the entry once `durable_pre_draw` returns. It reaches
  no `CommitSession`, provider frame, attempt row, receipt or operational record.
- *Crash behaviour.* (i) When S4 proposes no floor change and F is present, nothing is written and the reservation is
  never used; that is lawful, since reservations are in memory and never released (MJ:253). (ii) A crash, or a refusal
  at R10a to R12, after the floor publication leaves a durable floor record whose ExecutionId names no attempt and no
  attempt row; it is still correlated by its `requestId`. A rerun is a new invocation with new ids.
- *Proposed amendments (each needed; none applied by this record).*
  - **A-1. MJ:256-258** (who reserves). Present: "the prelude's, in `mint_intent`, before P0 is staged (S4);" ...
    Proposed, a new line: "the durable trust act's, in the durable entry, after R9 and before R10 (C2A-ORDER-E1)."
  - **A-2. MJ:245-248** (the ids). Proposed, a new bullet after MJ:245: "**The durable trust act** gets its own draw
    before R10. It names R10's floor publication and X4B acceptance only, is never reused, and is never bound to the
    analysis attempt."
  - **A-3. MJ:264.** Present: "For a durable request the ExecutionId is lawful from the session's open". Proposed:
    "For a durable request the analysis attempt's ExecutionId is lawful from the session's open ... The creation
    prelude's and the durable trust act's ids are lawful from their own reservation, for their own act only."
  - **A-4. MJ:287** (J-C4b). Present: "reserves three distinct ExecutionIds (prelude, session, render)". Proposed:
    "reserves four distinct ExecutionIds (prelude, trust act, session, render); a steady-state invocation three".
  - **A-5. MJ:413** (J-C10b). Present: "holds no analysis-attempt reservation. Its set equals its set at R10a's entry:
    empty on 3a and on the ephemeral path, and the creation prelude's alone on 3b." Proposed: "holds no
    analysis-attempt reservation. Its set equals its set at R10a's entry: the trust act's alone on 3a, empty on the
    ephemeral path, and the creation prelude's and the trust act's on 3b."
  - **A-6. OPP:154.** Present: "`ExecutionId` | attempt admission (IE:61-63) | before". Restated, no word change: the
    table governs operational record fields; the trust act's id appears in no operational record (A-2). A reviewer
    who reads OPP:154 as covering durable records instead adds "(an attempt's; J1 item 2's prelude and trust act
    excepted)".
  - **A-7. WS:81 and IE:62-63.** Present: "Each admitted attempt of a step receives a fresh `ExecutionId`" (WS:81);
    "Each admitted attempt receives a fresh ExecutionId" (IE:62-63). Restated, no word change: they say every attempt
    gets one, not that every ExecutionId is an attempt's; the prelude, "not a step of its own" (L464:68), is the
    accepted precedent. *A second reading:* the prelude runs "on the process's attempt A" (MJ:292; OWN:59, "exactly
    one private `InitialInstallationAttempt`"), so its id can be read as attempt A's; R10 runs after
    "`admit_ordinary_writer()` runs on a second attempt B" (MJ:306) on 3b, and on 3a's one attempt. Read that way the
    trust act's id is the id of the process attempt R10 runs on, which also supports leaving IE and WS unchanged; but
    those are installation attempts, not attempts of a step (WS:81). **Both readings are the record's, not a text's;** if the cross-vendor reviewer rejects it, IE
    and WS are amended by their owner and the project owner, which is a contract change.
  - **A-8. X4T:187** (item 7). Present: "The writer reuses 467's existing trust publication producers." Proposed, an
    added sentence: "Its `OperationInputV1.invocation`, and X4B's acceptance's, is the invocation's RequestId, the
    StepId of the step it serves, and the durable trust act's reserved ExecutionId (J1 item 2)."
  - **A-9. SPD:700-701.** Present: "no path here draws or reserves an analysis-attempt ExecutionId; a source census
    over the boundary's sources finds no `ExecutionIdReservations`". SPD never defines "the boundary's sources", and
    SPD:870 names CP-J3D-SECPRE-1, this entry, among the boundary's owed carries. P's census
    (`security/src/custody/operation_live_tests.rs`:1498-1512) covers `custody/pre_draw.rs` and `trust_pre_draw.rs`
    for the tokens `ExecutionIdReservations`, `ExecutionId` and `reserve_execution`. **PROPOSED:** "The boundary's
    sources are `security/src/custody/pre_draw.rs` and `security/src/trust_pre_draw.rs`. The durable trust act's
    reservation is made in the public entry's own file (CP-J3D-SECPRE-1), outside them, and reaches R10 only inside
    `TrustInvocation`. In `security/src` outside tests, `reserve_execution_id` is called only in
    `initial_installation.rs`, `custody/commit_session.rs` and the entry's file."
  - **A-10. MJ:968** and **MJ:278**: no change. Both already allow a reserved, non-analysis-attempt id.
  - **A-11. M3D (accepted r5).** (i) M3D:759-762, "Where ExecutionIds are drawn", lists only "the durable analysis
    attempt's", "the ephemeral and render attempts'" and "the creation prelude's". Proposed, a bullet after M3D:762:
    "**the durable trust act's** is drawn and reserved by the durable entry after R9 and before R10, on both routes. It
    names R10's floor publication and X4B acceptance only and is not the analysis attempt's (J1 item 2)." (ii)
    M3D:815, D4-T1, of which J-C10b is "the placement half" (MJ:412). Present: "Its set equals its set at R10a's
    entry: empty, or the creation prelude's alone on first use." Proposed: "Its set equals its set at R10a's entry:
    on the durable path the trust act's alone, or the creation prelude's and the trust act's on first use; empty on
    the ephemeral path." Owner M3D, through a J1 successor row.
  - **A-12. MJ:410.** Present: "the prelude's reservation, made in `mint_intent` before P0 is staged (item 2; S4), may
    already be in `ExecutionIdReservations` when R10a runs." Proposed, added after it: "On both routes the durable
    trust act's reservation (item 2) is there too; it is not the analysis attempt's."
- *Controls (each must fail first).*
  - **E1-C1.** Census: `TrustInvocation::new` and every `exec1_` text draw in `security/src` have no caller outside the
    fixture predicate.
  - **E1-C2.** Compile-fail: the production constructor rejects `&str` for either id and any type other than
    `&RequestIdentity` / `&ReservedExecutionId`.
  - **E1-C3 (A-4).** First use reserves four distinct ids (prelude, trust, session, render); steady state three.
  - **E1-C4 (A-5).** At an injected R10a refusal: no analysis-attempt reservation; the set is {trust} on 3a and
    {prelude, trust} on 3b; `x3d.session.execution-draw` is not reached.
  - **E1-C5.** A forced floor advance (3a) and an F-absent acceptance: each record's `executionId` equals the trust
    act's reservation, differs from the prelude's and the later session's, and its `requestId` is the envelope's.
  - **E1-C6.** Eight forced collisions at the trust draw: security's HostIo row, nothing written by R10, `created` kept.
  - **E1-C7.** No floor change proposed: no record, no refusal; the reservation exists and is unused.
  - **E1-C8.** Census: after `durable_pre_draw` the entry holds no `ReservedExecutionId`; the session's id is never it.
    **Output scan:** on a full first-use run and a full steady-state run, each with a forced floor advance, the trust
    id's `exec1_` text appears only in the R10 floor and acceptance records (and their S4 time evidence). It is
    absent from the envelope, every operational record, the attempt row, the receipt, every provider frame and the
    render step's records. Planting it in any of them fails the scan.
  - **E1-C9 (after the floor publication).** A forced floor advance, then an injected R10a refusal; and separately a
    crash point after the confirmed floor publication and before R12. Must exist: the floor record carrying the
    trust id and the invocation's RequestId. Must not exist: an attempt row or receipt with that id, a
    `CommitSession`, a lease. A rerun reserves a different trust id; reusing it fails the control.
  - **E1-C10 (A-9).** Census: in `security/src` outside tests, `reserve_execution_id` is called only in the three
    files A-9 names, and the boundary's two files name none of the three tokens.

**E2. R8 (endpoint) after R9 (registration). PROPOSED (lead ruling Q35 (a); AT RISK; the owner is told).**
- *Texts.* "The durable request runs this order" (MJ:379); R8 "X3a's endpoint admission, from the gate's own retained
  captures, with no new read" (MJ:391); R9 "X2 item 5's registry capture; X2 item 6's first registration" (MJ:392).
  X3A5:28-29 states the one-read rule and the producers only. X2 item 7a step 1: "Join ... with X3a's
  `SelectedStoreEndpoint` from the same session or gate" (X2:430). M3C row 4: "The rest of X2's project admission
  (items 5 to 7 ...), then the handoff" (M3C:867). SPD: `pre_draw(writer, subject, lease, ...)` (SPD:606), where
  `subject` is R9's result, and "the endpoint join, the namespace admission, `trust_start` ... each run once, in
  `pre_draw`" (SPD:623-624). Adoption: "`begin` stays the composition of its two phases" (ADOPTION:10).
- *Reading.* X2:430 orders the **join** of the endpoint, not X3a's admission; X3A5 places nothing. MJ's table and
  X2/X3a can both hold: admit at R8, join at 7a. **SPD:623-624, an adopted security record, is the only text that
  places the endpoint after R9;** P follows it (`custody/operation_handoff.rs:1350`). The real conflict is MJ's table
  against SPD. The erratum therefore sets an adopted security record above an accepted law's table. The owner is told.
- *Rule.* The entry runs R9 (X2 items 5, 6a, 6) before R8, and R8 only inside `durable_pre_draw`. MJ:391-392 get the
  erratum: "R8 runs at X2 item 7a step 1, after R9"; R8's content is unchanged.
- *Consequence.* On a first-use candidate, an X3a refusal (row 16, MJ:788) comes after first registration. It leaves
  the ACTIVE row and the namespace, `.opensip` if absent and the marker (X2:272-274); a failed step latches "with no
  later registration step, no retry and no deletion" (X2:256). A later invocation sees `Eligible` (X2:213) and meets
  the same refusal until the core or store changes. On an Eligible root the registry is unchanged.
- *Does a text forbid it?* **Not located.** "Before any project-scoped effect" binds R6 (MJ:399-405) and R7 (MJ:398,
  :959) only; X12r4's clause is about packs. No text cleans up or reclaims the row.

**E3. R7, the storage choice. SETTLED-BY-TEXT, except the classification: PROPOSED (lead ruling Q40).**
- *Texts.* R7: "The S3.1 storage choice (`grants.rs`), which is pure ... A positive `BACKED_UP` without the flag is
  `storage.backup-choice-required`" (MJ:390). "On first use, the intent has already applied the same choice to the
  creation (L464:9), and R7 rechecks it against the same classification" (MJ:398). OWN: "Recheck the actual
  target/classification and delivered disclosure before effects; a changed target or stronger newly observed
  restriction refuses this act" (OWN:28). M3B:376 and :727; `created: Option<Created { classification, target }>`
  (MJ:308); `None` "For `LostRace` and `NotPristine`" (MJ:311).
- *Rule (SETTLED).* R7 runs on both routes, after R6 and before R9, over a backup classification and this invocation's
  `--allow-backup-custody` flag. The export takes the classification as an input, which serves every reading below.
- *Both sides.* MJ:398 "R7 rechecks it against the same classification" reads toward the intent's stored value;
  OWN:28 "Recheck the actual target/classification ... a changed target or stronger newly observed restriction
  refuses" reads toward a fresh observation. No text decides between them.
- *A fact (product, found in code).* The routing entry's value does not say which route ran: `DurableEntry` holds
  only `admission` and `created` (P @ `780c52fc` `security/src/custody/installation_routing.rs`:74-77), and `created`
  is `None` both on the steady state (no creator act) and after `LostRace` or `NotPristine` (MJ:309, :311; P :254,
  :334). So a rule that differs by route needs a new route field; a single rule does not.
- *PROPOSED (lead ruling Q40, `QUESTIONS.md`:780-788; a ruling, not settled by text; AT RISK until the
  cross-vendor review).* On every route (3a; 3b with `created: Some`; 3b after `LostRace` or `NotPristine`), R7
  takes a FRESH classification of the installation target from the 464 owner's classifier, then the storage choice
  with this invocation's backup flag. Where `created` exists, the fresh classification governs; if it is stronger
  than `created`'s, the request refuses (fail closed). Reasons (the lead's): OWN:28's "stronger newly observed
  restriction refuses"; a recheck of a stored value can never refuse; one code path; no route field and no change
  to the routing entry. Under the constant classifier (L464:51) every route gives `UNKNOWN` today.

## Open points

| # | Point | Decider |
|---|---|---|
| O1 | E1c: adopt (a) with A-1 to A-12, or overrule | lead after the cross-vendor review; project owner told, may overrule |
| O2 | A-7's reading (IE/WS unamended) | cross-vendor reviewer; if rejected, the contract owners and the project owner |
| O3 | E3: the fresh-classification ruling (Q40), AT RISK | lead; both reviewers; 464 owner |
| O5 | Q39: MJ:390 names "The S3.1 storage choice (`grants.rs`)" for R7; P's `grants.rs`:212 `storage_write_choice` is documented "S3.1 before the first source-derived write" (:208), as M3B:376 places it ("J3 calls it at the first source-derived write"); the entry rechecks the intent's choice (`initial_installation::storage_choice`) at R7. The lead's reading (Q39 (c), `QUESTIONS.md`:789-791): the intent's choice is rechecked at R7; the grants owner's choice belongs at the first source-derived write, with its extra inputs typed for their producers. Is that reading lawful against MJ:390? | lead; both reviewers; 464 and grants (B3-a) owners |
| O4 | E2: MJ:391-392 erratum | lead; cross-vendor review; project owner told, may overrule |

## Consequences for owning units

**Free of open points now:** Q36's export, taking the classification as an input (E3); Q38's public types and
compile-fail rows; control E1-C1.
**Dependent on O4 (AT RISK):** the R3-R9 crate-private composition with R9 before the endpoint, and control E2-C1,
which encodes the at-risk state and inverts if the erratum is rejected. J-C10 itself does not depend on O4.
**Waits for O1 (and O2):** the trust act's reservation, the production `TrustInvocation` constructor, any production
call of `durable_pre_draw`, the public function returning `DurablePreDraw`, and E1-C2 to E1-C10.
- **E2-C1 (O4).** First-use candidate, endpoint refusal injected: row 16; ACTIVE row, namespace and marker remain;
  `created` kept. Eligible root, same injection: registry bytes unchanged.
- **E2-C2.** Census: `join_store_endpoint` is called only inside `pre_draw_retaining`.
- **E3-C1.** A test classifier returning `BACKED_UP`, no flag, on 3a and 3b: `storage.backup-choice-required`, and no
  registry row, namespace, `.opensip`, marker, lease or journal. With the flag, or under `UNKNOWN`, R7 admits.
- **E3-C2 (O3).** On 3b after `LostRace` and after `NotPristine` (`created: None`), the same test classifier and no
  flag: R7 refuses on the same row. Today's fail-closed refusal for every `created: None` (`QUESTIONS.md`:752-753)
  makes 3a fail this control.
- **E3-C3 (O3).** `created` holds `UNKNOWN` and the fresh classification is `BACKED_UP`, no flag: refused; with the
  flag: admitted. Using `created`'s value instead fails it.
- **E3-C4 (O3).** Census: R7 reads no classification from `created`; it calls the owner's classifier once per
  request, on every route.

## Rejected alternatives

- **E1 (b), no ExecutionId in the R10 record.** TRS is pinned by an architecture selection, so this is a selection
  successor. `InvocationBinding` is shared by all 14 `OperationInputV1` actions (P0's `creation` among them) and 6
  other definitions, so a new binding definition is needed; the `host-trust-admission` branch is `operationSchema`
  const 1 and `S4EvaluationInputV2` is `inputSchema` const 2, so both need new versions. Also changed: the generated
  `security/src/generated/trust_record_shape_nodes.rs`, the floor writer and X4B acceptance, X4T item 7, and five
  corpora (`security/tests/fixtures/inputs275`, `current-bindings328`, `successor-link329`, `record270-records`,
  `record270-fragments`). Records are content-addressed predecessors, so the old shape is read back permanently.
- **E1 (d), a distinct non-ExecutionId identity in the record** (a per-write nonce or operation id): (b)'s whole
  schema cost plus a new identity kind.
- **E1 (c), reuse an existing id:** none exists on 3a; L464:68 bars the prelude's on 3b.
- **Opening the session before R10, or deferring the write past R11:** MJ:394, :968; X4T:187 writes trust state
  "only under the fence and never under a lease".
- **An unreserved draw in production** (MJ:278; IE:77-80); **the RequestId's bytes as `exec1_`** (IE:77; MJ:275).
- **E2 (b),** a second endpoint validation before R9, funded by no text; **E2 (c),** a successor to adopted SPD.
- **E3 by statement only** (R7 a no-op under `UNKNOWN`): it hides a step of MJ's order.

## What this record does not do

It applies no amendment: MJ, IE, WS, OPP, L464, X4T, SPD and TRS stay as they are until O1, O2 and O4 are adopted.
It does not decide the read entry's `TrustInvocation` (CP-J2C-SECPRE-1's report-mode read writes nothing), R10a's
store root, or the launch directory. It does not re-open J-C10, Q38 or the R3-R6 rows of `C2A-ORDER.md`.
