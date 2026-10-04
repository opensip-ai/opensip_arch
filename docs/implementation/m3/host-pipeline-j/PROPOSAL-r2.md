# The guarded durable host pipeline — proposal M3-J1 r2

2026-10-04. Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the overnight autonomous run. Law for unit **M3-J1** of the accepted M3 unit plan (`M3-PLAN-r6.md:217`).

**Draft r2, not accepted. Not code.** M2 is complete: its crash-matrix gate was met by Grok's accepted rerun on C = `3d2d5b5` (`m2/M2-COMPLETE.md`; M3P:5). J's code units still wait for P0, for the B, C, D and H laws and the units named in item 14, and for I1's product units.

r1 (`PROPOSAL-r1.md`, sha256 `ff5cb156…`, 75,581 bytes) was reviewed by CODEX2 (`reviews/codex2-host-pipeline-j-r1`; REQUIRED-FINDINGS, 7 required, 2 non-blocking). r2 answers all nine. Every other r1 decision stands, and CODEX2 found the rest sound.

## r2 changes and review responses

| Finding | Change |
|---|---|
| J1-R1 (precedence) | Item 8.3 now matches the X3d outcome first. Rule 1 is any `CommitUndetermined` (the durability row). Rule 2 is a `Committed(PublishedCommit)` whose `latchedAfterAdmission` is set (X7's F39 row). State 3 alone selects nothing. Phase C (8.2), matrix rows 38 and 42, J-C14 and S12-U follow. |
| J1-R2 (settlement) | The settlement point is now the moment the required output returns, when every required step is terminal (5.3). An **output decision point** (8.4) now ends phase D. From that point to settlement is the **final output section, phase O**: a cancellation-deferral exception that successor **S18** reconciles with the WS and OPP owners, and J3d's output code is gated on it. S12-D now holds at a cancellable D point (`x3d.finish.end-step.after`). The new S12-O holds inside O (`x7.delivery.required.before`). `bootstrap.rs:57-58` is kept. |
| J1-R3 (creation disclosure) | The durable entry's refusal now carries the value-only creation record (item 3, `EntryRefusal { termination, created }`). It is taken from this act's own result: `Published`, or a failure after the publication rename. Item 9's presence rule starts at publication and covers every envelope except the empty-errors `interrupted` branch. The new control is J-C6b. |
| J1-R4 (ExecutionId reservation) | Item 2: every ExecutionId is reserved, uniqueness-checked, in a process-custody `ExecutionIdReservations` before P0, a provider frame or a record uses it (IE:77-81). That reservation is distinct from the durable attempt row (IE:83-101; X3D:114). Only the reserved type reaches a writer. This touches successors S4 and S10 and unit J3a, and adds control J-C4b. |
| J1-R5 (J3d's dependencies) | J3d depends on F2 and G3 again (M3P:217, :309). The critical path is restated (item 14). |
| J1-R6 (refusal families) | Matrix rows 52 to 55 cover native contexts and universe binding (NE:3530), the preparation bound (NE:3531), ambient Cargo configuration (NE:3532; M3C:674) and the authenticated release declaration (NE:3540, :3574). The new control is J-C20b. |
| J1-R7 (audit at M4) | Item 1: the M4 CLI unit replaces the `opensip`, `analyze` and `fit` refusals. `audit`'s refusal stays until its M5 comparison prerequisite exists (BP:955). X11:28's "all four at once" is reconciled per command. |
| J1-N1 (latch minting and window) | Adopted: the latch is minted once per operation, and its window is two bits of the gate's own atomic word. The window is closed on every return of `prepare_commit` and `publish` (8.1). |
| J1-N2 (SOP2's implementation) | Adopted: J3d depends on O1 (M3P:221, :314). |
| Context | M3-PLAN r6 is accepted (`a6956e88…`). M3-C r5 is accepted in review (`7f76052d…`) and takes effect once M3-L and X12 r4 are accepted. X12 r4 and X2 r9 are accepted by Grok. S-OP-2 is cited by its r4 bytes while r5 is in progress. M2 is complete. Every citation and pin is renewed. |

**Standing direction.** Every item below that says "lead decision" is made under the owner's standing direction of 2026-09-30 to proceed on the lead's recommendation. Each names the alternative it rejects. The owner may reverse any of them. No item blocks on an owner decision (see "Open questions").

**What this law is.** The M3-J row asks J1 for four things (M3P:217):
1. the X11 successor (X11:64-81);
2. the invocation DAG (WS:76-256) as M3 implements it;
3. the backup-status successor;
4. the commit-phase cancellation join S-OP-12, with the X3D and X7 owners (OPP §5.5, §9).

It also fixes the M3 outcome matrix and breaks J2 to J4 into units.

**The X3D and X7 owners' assent.** OPP names S-OP-12's owning authority as "storage + security (X3D owner) + host finalization (X7 owner)" (OPP:417). Both laws, X3d r8 and X7 r6, are the lead's. Their amendments are written here as successors X3d r9 and X7 r7, as lead decisions under the standing direction. Neither changes before J1 is accepted, and each is reviewed with J1 or right after it.

## Short names

| Name | Document |
|---|---|
| **M3P** | `docs/implementation/m3/M3-PLAN-r6.md`, the accepted r6 bytes (sha256 `a6956e88…`). The live `M3-PLAN.md` carries the acceptance note. |
| **X11** | `docs/implementation/m2/cli-enablement-x11/PROPOSAL.md` (r1 accepted) |
| **X12r4** | `docs/implementation/m2/policy-admission-x12/PROPOSAL-r4.md`, the r4 bytes Grok accepted (`adc9a88a…`) |
| **X12** | `…/policy-admission-x12/PROPOSAL-r3.md` (r3 accepted). Its lines are cited the way other laws cite them. |
| **X3D** | `docs/implementation/m2/commit-session-x3d/PROPOSAL.md` (r8) |
| **X7** | `docs/implementation/m2/finalization-x7/PROPOSAL.md` (r6) |
| **L464, L468** | `docs/implementation/m2/{creation-ingress-464,existing-root-admission-468}/PROPOSAL.md` (r2, r5) |
| **X2** | `docs/implementation/m2/project-root-x2/PROPOSAL-r9.md`, the r9 bytes Grok accepted (`0d68e3a5…`) |
| **X1, X3A, X4, X4B, X4T, X5, X9, X10** | `docs/implementation/m2/{ordinary-platform-x1, store-admission-x3a, live-guards-x4, trust-bootstrap-x4b, trust-admission-x4t, replay-join-x5, crash-matrix-x9, read-cli-x10}/PROPOSAL.md` |
| **OWN** | `docs/implementation/m2/initial-root-binding-owner-selection-v1/owner.md` |
| **EXIT** | `docs/implementation/m2/EXIT-PLAN.md` |
| **M3B** | `docs/implementation/m3/config-discovery-b/PROPOSAL.md` (r2 accepted) |
| **M3C** | `docs/implementation/m3/snapshot-plan-c/PROPOSAL-r5.md`, the r5 bytes CODEX2 accepted in review (`7f76052d…`, 1183 lines). Under its own gate, it takes effect once M3-L and X12 r4 are accepted. |
| **M3L** | `docs/implementation/m3/provider-protocol-l/PROPOSAL.md` (r1 draft, not sent) |
| **I1** | `docs/implementation/m3/preview-pack-i1/PROPOSAL.md` (r2 accepted) |
| **OPP** | `docs/implementation/m3/operability/PLAN.md` (r3 accepted). It is cited by section and by its live lines. |
| **SOP2** | `docs/implementation/m3/operability/s-op-2/PROPOSAL-r4.md`, the r4 bytes (`db10e19c…`). Codex returned required findings on r4 (`reviews/codex-s-op-2-r4`), and r5 is in progress. J1 cites r4's lines and gains it no acceptance. |
| **AQP** | `docs/implementation/m3/analysis-quality/PLAN.md` (live r6) |
| **WS, IE, SL, NE** | `docs/v2/contracts/product-v1/{workflows-and-surfaces, identity-and-evidence, security-and-lifecycle, native-evidence}.md` |
| **BP** | `docs/v2/architecture/implementation-boundaries-and-build-plan.md` |
| **CINV, WFC** | `docs/coop/design-corrections/workflows/{command-inventory.v3.json, workflow-cases.v1.json}` |
| **ENV7, COMMON4, INV5** | `opensip/schemas/sources/{command-envelope-v7, common-v4, invocation-v5}.schema.json` |

Product paths are under `opensip/` at main `3e64266`. They were read, not run.

## Problem

**What exists at `3e64266`.**
- **The binary.** It wires metadata and `doctor` only (`apps/cli/src/arguments.rs:86-108`). `opensip`, `analyze`, `fit` and `audit` refuse, and X11a pins that byte for byte (`apps/cli/tests/creator_commands_tests.rs:484-554`).
- **The request identity.** RequestId is drawn under process custody before parsing (`apps/cli/src/bootstrap.rs:14-24`; `crates/host/src/request.rs:15-55`). That registry says that "durable host audit custody uses the separately implemented durable ingress" (`request.rs:16`), and no such ingress exists.
- **The creator.** `run_initial_creator` (`crates/security/src/custody/installation_routing.rs:66-86`) runs these steps on every call:
  - the attempt, actor, core and platform;
  - the creation intent, which draws its own RequestId and ExecutionId (`crates/security/src/initial_installation.rs:591`) and writes "first use creates the installation" to the disclosure writer (`:430-437`, `:602`);
  - only then the creator act, which may find I present (`NotPristine`);
  - and the gate (`installation_routing.rs:90-119`).
- **Finalization.** `finalize` replays the candidate first, then calls an `admit` closure for the X1 and X2 admissions, then opens the session (`crates/host/src/finalization.rs:395-422`). X3d draws the ExecutionId at `CommitSession::open` (`crates/security/src/custody/commit_session.rs:313-345`).
- **The commit gate.** It latches only from the observer or a failed checkpoint (`crates/security/src/commit_authority.rs:26-48`; `custody/operation_guard.rs:99-106`). Nothing reaches it from a signal.

**Five gaps.**
- **G1. No creator-class command can commit, even in steady state.** The creator's route drops `InitialCore` before the gate, so its `AdmittedInstallation` has no store (X3A:31-36) and no trust bootstrap (X4B:64, :181). X1 item 7 forbids a second entry in the process (X1:49-54). Every creator-class invocation would also mint an intent and print the first-use notice, whether or not I exists.
- **G2. The lease and the attempt identity are in the wrong place for analysis.**
  - IE:1657-1658 requires one writer to hold the lease "through source admission, evaluation and atomic commit". X5 item 3 and `finalize` replay before any admission (X5:39-43).
  - Providers carry the attempt's `executionId` on the wire before they spawn (M3L:120, :377). X3d draws it only at the session's open, which today follows evaluation.
- **G3. Two RequestIds.** The intent's and the envelope's are separate draws (X11:74).
- **G4. No signal reaches the commit gate.** That is S-OP-12 (OPP §5.5, OPP:330-340).
- **G5. Three things are missing:**
  - the backup-status carrier (X11:47-56; L468:53);
  - an ephemeral path;
  - the M3 outcome matrix.

## Decisions

### 1. Which commands go live at M3: none in the binary (lead decision)

- **Decision.**
  - **The binary.** No analysis word is wired in `opensip` at M3. `opensip`, `analyze`, `fit` and `audit` keep X11 r1 item 2's refusals byte for byte (X11:30-45). X11a's pins keep passing unchanged. `help` and `completion` keep the four-row catalogue. `doctor` and the metadata commands are unchanged.
  - **What goes live.** One host-library entry, `opensip_host::invocation::run` (the name is J2a's), for exactly three requests:
    - `default`, durable;
    - `analyze`, durable;
    - `analyze --ephemeral`.

    Each runs the step list `[analysis, render]` (item 5). Its callers are host tests (`workflow_tests.rs`, the COV:7865 owner) and the internal harness (AQP:500).
  - **Not at M3:** `fit` and `audit`. `fit`'s steps are `analysis, query, render` (CINV:188), and query is M4 (BP:956). `audit`'s steps are `analysis, analysis, comparison, render` (CINV:257), and comparison is M5 (BP:955). Neither is in the M3 request type. Their durable entry is item 3's, unchanged, when their commands land.
  - **Format.** The M3 request carries one format, JSON (ENV7). Human, SARIF, HTML and agent output are M4 (BP:888).
  - **What the entry takes.** It takes the disclosure writer, the output handle, `InvocationModeV1` and a cancellation source as typed arguments. It never takes a home, profile or release selector (X11:66; X10 r4 item 5).
  - **Which unit replaces which refusal (r2, J1-R7).** Each refusal is replaced by the unit that delivers its command, once every prerequisite of that command exists (BP:895, BP:951-955):
    - the **M4 CLI unit** replaces the `opensip` (default), `analyze` and `fit` refusals. `fit` also needs its M4 query step (BP:956);
    - **`audit` keeps X11 r1's refusal through M4.** Its comparison step is M5 (BP:955), and the M5 unit that delivers comparison replaces it.

    X11:28's "the M3 unit replaces all four refusals at once" was written before the milestones were split. It is reconciled per command here, and J1 does not call any collective enablement an M4 unit. The M4 CLI unit also wires:
    - standard error as the disclosure writer;
    - standard output as the output handle;
    - `isatty(0) && isatty(2)` into `InvocationModeV1` (M3B:114-118). No automation flag is added (M3B:118), so no CINV successor is needed at M3;
    - the SIGINT, SIGTERM and SIGHUP handlers into the cancellation source (item 8).
- **Basis:**
  - BP:887: "Complete CLI analysis delivery follows at M4 with every advertised renderer";
  - BP:895: "Every command delivery also waits for all of its advertised renderer milestones … not releases with silently reduced format contracts";
  - BP:951-955: `default`, `analyze` and `fit` are M4, `audit` is M5;
  - M3P:110 and M3P:468 ("nothing is wired. J1 fixes the order and identity rules");
  - AQP:500 (the dogfood checkpoint "is not CLI `analyze`") and AQP:502 (CLI dogfood is M4);
  - M3B:720, M3B:904.

  Every non-release build ends at InitialCore F0, and this host is BASELINE-ATTESTED (X11:42-45). A live command would therefore give the owner nothing observable at M3.
- **Rejected:**
  - **Wiring `analyze` and the default at M3 with JSON only.** That moves two command rows ahead of their renderer milestone (BP:895).
  - **A hidden or feature-gated CLI word for the harness.** X11:118 forbids an argument, feature or `cfg` seam in the binary. The harness calls the library.
  - **Shipping X11's "create, then refuse".** X11:20-21's reasons b and c still hold for the binary.
  - **Replacing all four refusals in one M4 unit (r2, J1-R7).** That would deliver `audit` before its M5 comparison prerequisite (BP:895, BP:955).
- **Forbidden substitutes:**
  - an analysis word wired in `apps/cli` at M3;
  - a binary seam;
  - a library entry that selects a home, profile or release;
  - `fit` or `audit` in the M3 request type;
  - an `audit` word wired before its M5 comparison step exists.
- **Controls:**
  - **J-C1.** X11a's tests stay green on every J unit's integration commit, its source pin included (`creator_commands_tests.rs:484-554`). J's units name no forbidden symbol in `apps/cli/src`, `host/src/{outcomes,doctor_ingress,request,lib}.rs`. The new security entry of item 3 is a different function, and `run_initial_creator` and `admit_ordinary_writer` stay `pub(crate)`, each defined once.

### 2. One request identity per invocation, and the attempt identities (lead decision)

- **Decision.**
  - **The RequestId.** One per invocation, minted at ingress before parsing and admission (WS:78; IE:61-62) by the host's process-custody `RequestAuthority` (`request.rs:15-55`). It serves as:
    - the envelope's `requestId`;
    - the correlator of every operational record (OPP §3.1; M3L:375);
    - on the creation route, the RequestId that P0's `OperationInputV1.invocation` records.
  - **The handoff to security (successor S4, a 464 r3 amendment).** A sealed value `RequestIdentity` lives in `opensip-platform`. It is minted only by the CSPRNG draw (`request_entropy`). It has no constructor from bytes or text, and it is not `Default` or deserializable. The host's registry reserves it, and the host lends `&RequestIdentity` to item 3's entry. `mint_intent` records it and draws no RequestId of its own: it still draws its ExecutionId (`initial_installation.rs:591`). An ephemeral request involves no security draw.
  - **Uniqueness (stated limit).** IE:77-79 requires a reservation "in the corresponding operational ledger before use". For a host that serves one request per process (X10:30), that ledger is the process-custody registry (`request.rs:15-16`, `:28-41`), as for metadata and doctor.
    - M3 keeps no durable RequestId registry. The 128-bit CSPRNG draw is the cross-process argument.
    - The durable traces are P0, on first use, and S-OP-1's file sink once it is accepted.
    - A retained invocation record, which WS:119-123's mutation replay scope needs, is M5's, with mutation steps.
  - **ExecutionIds.**
    - **The creation prelude** keeps the intent's own draw (L464:34). It names the creation act in P0 only.
    - **The durable analysis attempt** is X3d's draw at `CommitSession::open` (X3D:113-117). Item 7 opens the session at the handoff, so the id exists before any provider spawns. It is the id the attempt row reserves (X3D:130) and the receipt carries.
    - **The ephemeral attempt** gets a host draw at the attempt's start. It never reaches attempt custody (IE:88).
    - **The render step's attempt** gets a host draw that appears only in operational records.
  - **The ExecutionId reservation (r2, J1-R4; lead decision under IE:77-81).** IE §2 is the governing rule. Both identities use "independent 16-byte host-CSPRNG draws, reserved with uniqueness checked in the corresponding operational ledger before use", and that reservation "applies to **every** RequestId and ExecutionId, in every request mode" (IE:77-81). J1 names that ledger for ExecutionIds.
    - **The owner.** A process-custody registry, `ExecutionIdReservations`, lives in `opensip-platform` beside `request_entropy`, because both security and the host draw ExecutionIds. It applies `RequestAuthority`'s discipline (`request.rs:28-41`) to ExecutionIds.
    - **How it reserves.** It holds one reservation set per process. Each draw reserves its 16 bytes only after checking them against every ExecutionId already reserved in the process. A collision redraws, at most eight draws in all, as `RequestAuthority` does (`request.rs:32-40`).
    - **When it refuses.** Exhaustion, or a failed draw, refuses on the drawing owner's existing host-I/O row: security's HostIo row (X3D:278; L468:48), or the host's `HOST.IO_FAILURE`. No code is added.
    - **No release.** A reservation is never released or reused in the process.
    - **The sealed result.** The registry returns `ReservedExecutionId`. It has no constructor from bytes or text, and it is not `Default` or deserializable. P0's writer, the provider frame builders, `CommitSession`, the attempt row and the operational record take only that type or its read-only projection, so a bare draw reaches none of them.
    - **Who reserves which id:**
      - the prelude's, in `mint_intent`, before P0 is staged (S4);
      - the durable attempt's, in `CommitSession::open` (S10). It keeps its security-owned draw (X3D:114) and reserves it in the same step, before the session exists, so before any provider frame;
      - the ephemeral and render attempts', in the host, at each attempt's start.
    - **Its relation to attempt custody.** The process reservation is IE:77-81's pre-use uniqueness reservation. It is not a durable record.
      - A durable, commit-capable attempt is reserved a second time, durably, by X3c item 3's attempt row at `prepare_commit` step 4 (X3D:130; IE:83-101). That row's no-replace trigger refuses a reused ExecutionId (F34; X3D:134).
      - The ephemeral and render ids never reach attempt custody (IE:88).
    - **Stated limit.** Until an id reaches attempt custody, cross-process uniqueness rests on the 128-bit draw. As for RequestIds, M3 keeps no permanent ExecutionId ledger.
    - **The crash-matrix census.** `x3d.session.execution-draw` keeps its name and place (X9:939). The reservation is in memory and adds no durability point. F34's `inject-id` still reaches the attempt row's trigger, because an earlier run's injected id is not in this process's registry.
  - **Phase-lawful identities.** OPP §3.1's table holds, with one reading fixed. For a durable request the ExecutionId is lawful from the session's open (OPP:156's "attempt admission"; item 7), which is the attempt's start. That open precedes the attempt row (X3D:130), and item 8 uses "attempt admitted" for the attempt row only, as OPP §5.5 does (OPP:335).
- **Basis:** WS:78-82; IE:61-63, IE:77-81, IE:83-101, IE:88; L464:13-21 and :34; X3D:114, :130-134; X11:74; OPP §3.1 (OPP:145-160); M3L:375-382; `request.rs:28-41`.
- **Rejected:**
  - **Binding the envelope's id to the intent's.** The intent exists only on the creation route, after F0, the probe and the actor. A refusal before it (parse, F0, a probe custody row) still needs a RequestId, which is "retained for refusal as well as success" (WS:78-79).
  - **Binding the prelude's ExecutionId to the analysis attempt.** X3d item 2 would have to take an id carried across the creator/ordinary boundary, and the shared RequestId already gives the correlation.
  - **A durable RequestId ledger at M3.** It is a new state class with no carrier.
  - **(r2) Treating the CSPRNG draw, or the draw's ledger charge, as the ExecutionId reservation.** IE:77-81 asks for a uniqueness-checked reservation. A draw is not one, and a budget charge is not an identity reservation.
  - **(r2) A permanent ExecutionId ledger at M3.** It has no carrier, and attempt custody already reserves every id that can commit.
  - **(r2) One registry for RequestIds and ExecutionIds.** IE:77-79 reserves each "in the corresponding operational ledger".
- **Forbidden substitutes:**
  - two RequestIds in one invocation;
  - a RequestId from a caller, from text or from a draw other than the ingress's;
  - any identity on a provider's wire beyond M3L:377's;
  - a RunId before `Committed` (OPP:157);
  - (r2) an ExecutionId used by P0, a provider frame, a session or a record before its process reservation; a reservation released or reused.
- **Controls:**
  - **J-C2.** On the creation route, P0's `invocation.requestId` equals the envelope's `requestId` and every record's. No second RequestId appears anywhere in the invocation's output, records or P0.
  - **J-C3.** Provider frames carry the session's `execution_id()`, and the receipt carries the same ExecutionId.
  - **J-C4.** `RequestIdentity` has no constructor but the draw. This is a compile-fail fixture under X8's driver.
  - **J-C4b (r2).** The ExecutionId reservation, with forced draw sequences as `request.rs`'s `allocate` tests use:
    - a repeated draw is redrawn;
    - eight collisions refuse on the drawing owner's row;
    - `ReservedExecutionId` has no other constructor, and P0's writer, the frame builders and `CommitSession` accept nothing else (compile-fail fixtures);
    - a first-use durable invocation reserves three distinct ExecutionIds (prelude, session, render), and none of them is used before its reservation.

### 3. The durable entry: the creator's host entry, first use and steady state (lead decision)

- **Decision.** Each durable request makes exactly one security call: `enter_durable_analysis(command, backup_custody_flag, &RequestIdentity, disclosure) -> Result<DurableEntry, EntryRefusal>`. The name is J3a's. It is one call, with no producer injection and no home, profile or release selector (X11:66). It runs:
  1. **Producers, on the process's attempt A:** the attempt, the actor, InitialCore and InitialPlatform (`read_premise.rs:331`, `produce_on`).
     - A development build ends at F0 here, `CORE.NO_EMBEDDED_RELEASE`, before any path is opened and with no disclosure.
  2. **The presence probe.** One charged, fence-free, no-follow walk from `/` to I, under gate step 0's custody predicates and premise (L468:15; X1:32's positive absence). It has three outcomes:
     - `Present`;
     - `PositivelyAbsent`: the first missing fixed-suffix component, under its retained parent;
     - a custody, I/O or budget refusal on its L468 item 6 row.

     The probe selects a route and nothing else. It is never authority: the ordinary gate re-establishes presence under the fence, and owner §1a step 6 re-establishes absence for the permit (OWN:26).
  3. **Route.**
     - **3a. `Present` (steady state).** Attempt A's producers are sealed as `PlatformReceipt<Write>`, with no intent and no disclosure. Then X1 item 2's steps 2 to 4 run: recheck, gate, recheck (X1:22-30). The result is an `OrdinaryWriteAdmission`, from one attempt and one gate.
     - **3b. `PositivelyAbsent` (first use).**
       1. The intent is minted on attempt A with the lent RequestId (S4). Its notice is written and flushed before any effect, and a failed write is HostIo (L464:27-32).
       2. The creator act runs (465 to 467) and ends `Published`, `LostRace` or `NotPristine`.
       3. Attempt A is dropped with its core and platform (L468:7; 467 item 9). The creator act enters no gate.
       4. `admit_ordinary_writer()` runs on a second attempt B: X1 item 2's steps 1 to 4, with fresh producers and the process's one gate (X1:22-30; `custody/ordinary_writer.rs:493`).
       5. The result is an `OrdinaryWriteAdmission`.
  4. **What it returns (r2, J1-R3).** On success it returns `DurableEntry { admission, created }`. On refusal it returns `EntryRefusal { termination, created }`. In both, `created: Option<Created { classification, target }>` holds values only and carries no authority from attempt A.
     - **When `created` is `Some`.** Exactly when this invocation's creator act performed the exclusive publication rename. That covers the act's `Published` result, and a refusal after the rename, which L468's host-I/O row covers as "any failure after the rename" (L468:48).
     - **Where it comes from.** The act's own typed result, never a later existence scan or the fact that an intent was minted.
     - **When it is `None`.** For `LostRace` and `NotPristine`, which published nothing, and for every refusal before the rename.
     - **What carries it.** Every later path keeps it: attempt B's producers, gate, barriers and rechecks, and every refusal after R3. Today's `route` drops it (`installation_routing.rs:107-118`); S2 records the change.
- **The probe's race.** Suppose the probe says `Present`, but the gate's walk then finds I positively absent, because I was deleted outside OpenSIP. The request ends on L468's `INSTALLATION.NOT_INITIALIZED` row (L468:40), whose remedy, "run an admitted durable analysis", is the true next step.
  - **Rejected:** the custody row. I is absent, not foreign.
- **How the creator command ends (X11:67-73; X3A:36).** It does not end after creation. The first-use invocation continues as an ordinary writer through the whole durable DAG, and its termination is the analysis's (item 10). What it tells the user:
  - the standard-error notice (L464:27-32);
  - the envelope's `retentionDisclosure`, with `firstUse` and `backupStatus` (item 9).
- **The creator terminations (X11:74-75).** Every probe, creator, gate and recheck refusal ends on its L468 item 6 row (L468:35-50) through `installation_termination`. It is projected as X10 r4 item 3's refused branch: `kind: failure`, `errors` holding the row's detail (or `HOST.IO_FAILURE`), and exit 2 or 4. When `created` is `Some`, every such envelope, including a refusal at attempt B, carries `retentionDisclosure` with `firstUse: true` and `backupStatus` (X12r4:200; item 9). The empty-errors `interrupted` branch is the one exception (ENV7:790).
- **The F0 restatement (X11:78-80).**
  - A development build ends at F0 in step 1. That is before the probe, the intent, any disclosure, the fence and pack admission.
  - X11 r1 item 5.8's "after pack admission" followed X12 r3's order. Under X12 r4, pack admission follows the fence, so F0 now precedes it.
  - A release build on this BASELINE-ATTESTED host ends at the probe's custody refusal at `/` (L468:45; X10 r4 "Not claimed"), before any intent or notice. Today's composition mints the intent first.
- **The amendments.** All are lead decisions, recorded as successors S2 to S8. None changes a public code, class, exit, subject or remedy.
  - **L468 r6, item 1.** `Published`, `LostRace` and `NotPristine` end the creator act. The invocation continues through X1's ordinary admission on a fresh attempt, not through a gate lent by the creator's `InitialPlatform`. L468 item 2's sealed capability is unchanged, and attempt B's `InitialPlatform` lends it. **r2:** the act's result, and its post-rename refusals, carry the value-only `created` record above. Their rows are unchanged.
  - **X1 r2, item 1.** The durable creator-class entry is a third producing entry. It fixes the Write purpose after the probe and before any receipt exists, so no receipt converts.
  - **X1 r2, item 7.** One entry per process holds, with one exception, the creator-class sequence: one creator act on attempt A, then exactly one `admit_ordinary_writer` on attempt B. The sequence is allowed only after the creator act ended `Published`, `LostRace` or `NotPristine`.
    - The attempt allocation (`initial_installation.rs:28`, `:96-99`) becomes a two-slot sequence. A non-Clone `CreatorActEnded` token is returned only by the creator act and consumed only by attempt B's allocation. Any other second allocation stays `Invariant`.
    - There is still one gate per process (`installation_admission.rs:801`).
    - **Also (S3, the ephemeral clause of item 6):** the 458c read receipt is a lawful use of the process's one attempt with or without a session.
  - **X3A r6, item 2.** "A later, separately admitted invocation" becomes "a separately admitted ordinary write operation: a later invocation, or this invocation's attempt B (J1 item 3)". The creator act itself still produces no endpoint.
  - **X4B r6.** The forbidden substitute "acceptance in the creator invocation" (X4B:181) becomes "acceptance in the creator act". The rejected bullet at X4B:64 records that attempt B is an ordinary writer.
  - **X2 r10, item 6.** The branch "or under the creator's `AdmittedInstallation` from 468c" (X2:202) is withdrawn, so first registration runs under an `OrdinaryWriteAdmission` only.
  - **L464 r3, items 1 and 5.** The intent holds the invocation's lent RequestId and a fresh ExecutionId. Item 5's "if a later ordinary operation in the same process ever used these ids" now reads: the RequestId is the whole invocation's, and the prelude's ExecutionId is never reused.
  - **X11 r1, item 1a: reconciled.** Under X12 r4, the creator's installation effects precede pack admission on the creation route (X12r4:197-200). "Creating I first" is therefore the lawful order. X11's M2 decision stood on its other reasons (X12r4:44).
- **Basis:**
  - OWN:21: the four commands use "durable-authoritative mode and the same initialization effect before their named steps";
  - OWN:32: P0 "does not authorize the remaining requested analysis steps";
  - OWN:103: "the creator's first ordinary write admission … a separately admitted write operation";
  - OWN:114: the race loser ends its creator act, then is separately admitted;
  - WS:250-253 and CINV:1747 (`default-first-use-durable`: success 0, in one invocation); WS:1373;
  - IE:1633-1636.
- **Rejected:**
  - **End and rerun** (create, then end, telling the user to rerun). It breaks the first-use golden (CINV:1747; WS:1373) and WS:250-253.
  - **A second process.** It needs a self-exec path from the core tree and a continuation argument in the binary (forbidden by X11:118). It splits cancellation and output across two processes, and it carries the RequestId between them.
  - **Carrying the creator's `InitialCore` through `route`,** to give the creator's `AdmittedInstallation` a store. X3A:38-39 rejects it, and so does 467 item 9.
  - **Running the creator act on every creator-class invocation** (today's composition). Every steady-state `analyze` would print "first use creates the installation" and would still have no store.
  - **Ordinary admission first, then the creator on its `Absent`.** It spends the one gate on the absence, and needs a third attempt and a second gate.
  - **One attempt for both acts.** The creator act's shared budget (OWN:19) and the commit's attempt ledger (X3D:216) would share one ledger at the owner's caps, and attempt A's `InitialCore` would cross the creator/ordinary boundary.
- **Forbidden substitutes:**
  - an intent or notice on a `Present` probe;
  - authority drawn from the probe;
  - a creator observation, handle, lock or receipt reaching attempt B;
  - a second gate or a third attempt;
  - attempt B without `CreatorActEnded`;
  - a store, a trust acceptance or a registration inside the creator act;
  - (r2) a creation disclosure taken from an existence scan or from the minted intent, rather than from the act's own result.
- **Controls** (scratch homes and synthetic V2 profiles, as X1a's):
  - **J-C5.** Steady state:
    - one attempt and one gate;
    - no intent, no notice and no P0 change;
    - standard error is empty unless something else writes to it.
  - **J-C6.** First use:
    - the notice is flushed before the first creation effect;
    - attempt B is fresh: its core and platform identities are re-observed, and no handle of A is retained (a type-level pin);
    - a third allocation is refused `Invariant`.
  - **J-C7.** The probe's three outcomes, and the `Present`-then-`Absent` race ending on `NOT_INITIALIZED`.
  - **J-C6b (r2, J1-R3).** `Published`, then a failure of attempt B:
    - the producers;
    - the gate busy;
    - a barrier failure;
    - a recheck failure.

    Each envelope carries `retentionDisclosure` with `firstUse: true` and `backupStatus: unknown`. A failure after the rename carries the same. A refusal before the rename, `LostRace` and `NotPristine` each give `firstUse: false`, or no member before R3. An `interrupted` envelope never carries the member.
  - **J-C8.** `LostRace` and `NotPristine` each continue to attempt B and commit.
  - **J-C9.** A development build ends at F0 with no notice and no file access. X11a's binary test already pins the binary itself.

### 4. The request order before analysis, and the first-use clause (law)

The durable request runs this order. Each row ends with a typed value the next row consumes.

| Row | Step | Owner and basis |
|---|---|---|
| R0 | RequestId, before parsing | item 2; `bootstrap.rs:14-24` |
| R1 | Typed request admission: the command, the mode, the flags of M3B item 23's table (M3B:720-730), JSON and `InvocationModeV1`. The host builds the step list. A malformed library request is a host-generated layer: `SYSTEM.OUTCOME.ILLEGAL_STATE`, `host-invariant` (NE:3573). | J2a |
| R2 | `installation_entry`: `Creator` for a durable request, `Outside` for an ephemeral one | `request.rs:85-135` |
| R3 | Durable entry → `OrdinaryWriteAdmission`, with the fence held | item 3 |
| R4 | S3's selection walk; X2 r9 item 3a's placement check and chain walk; the carrier captures | M3C:822; M3B:98 |
| R5 | B1 configuration resolution | M3C:823; M3B items 1-11 |
| R6 | X12 pack admission | X12r4:195-206; M3C:824 |
| R7 | The S3.1 storage choice (`grants.rs`), which is pure. Under 464's constant `UNKNOWN` it admits with the notice's disclosure. A positive `BACKED_UP` without the flag is `storage.backup-choice-required` (L468:39). | M3B:378, :729 |
| R8 | X3a's endpoint admission, from the gate's own retained captures, with no new read | X3A:28-29 |
| R9 | X2 item 5's registry capture; X2 item 6's first registration when the root is unregistered, with item 6a's tracking observation | M3C:825; X2:192, :202 |
| R10 | X3b's floor step; the operation's `FreshnessMonitor` and `FinalGate`; X4T's fenced first read, with X4B's acceptance when F is absent | X4:44; X4B:42-56 |
| R11 | X2 item 7's `APPEND-WRITE` lease; X2e's handoff. The fence is released and the lease is held. | X2:328; `operation_handoff.rs:330` |
| R12 | `CommitSession::open`, which draws the ExecutionId | item 7 |

- **The S3.1 slot (lead decision).** M3B says J3 calls the S3.1 choice "at the first source-derived write" (M3B:378). J1 reads that as "before any project-scoped effect of the durable request" (R7). Like a pack refusal, a storage-choice refusal then leaves no project effect. On first use, the intent has already applied the same choice to the creation (L464:9), and R7 rechecks it against the same classification.
- **The first-use clause (X12r4:33-47, :197-200).** This law owns that clause's control.
  - **Control J-C10.** On the creation route (item 3b), a refused project-layer pack ID at R6 leaves:
    - a complete installation;
    - no registry row, namespace, `.opensip`, marker, lease or journal;
    - the refusal's disclosure of the creation, through the notice on standard error and `retentionDisclosure` with `firstUse: true` (item 9).

    This control is shared with M3C:906-910 (C4-T20) and B1-a.
- **Rejected:**
  - **Pack admission before the durable entry.** The project carrier is judged only by the fenced selection (X12r4:42; M3B:306).
  - **The S3.1 choice at the commit.** Its refusal would come after the whole analysis and after project-scoped effects.

### 5. The invocation DAG as M3 implements it (law)

**5.1 Step lists** (WS:76-104; CINV:7, CINV:114).

- **`default` and `analyze`, durable:**
  - step 0 is `analysis`: required, `dependsOn []`, gate `completed`, retry `none`, durability `authoritative`, `snapshotSource: live-worktree`;
  - step 1 is `render`: required, `dependsOn [0]`, gate `terminal`, retry `none`, `format: json`, the caller's output handle, `required: true`.

  This is WFC:3612's `default-analyze-render-success`, except for the retry policy.
- **`analyze --ephemeral`:** the same two steps, with step 0's durability `ephemeral` (WFC:3741).
- **`analyze`'s `import` step** (CINV:114) is instantiated only when an import is selected. M3 selects none: the `import` command is M5 (BP:957), and C3's library importer is not a step (M3C:475).
- **Retry is `none` (lead decision).** A second durable attempt would need a second write entry, which X1 item 7 forbids even after S3. WS:105-108 makes idempotent retry lawful, not mandatory. A ledger-busy attempt therefore ends on the busy row (X3D:277), with no `WORKFLOW.RETRY_BUDGET_EXHAUSTED`.

**5.2 The analysis step's joins.** Each join hands the next a typed value. No join is re-entered, and a refusal at any join ends step 0 (`rejected` or `failed`). Step 1's gate is `terminal`, so it then projects that refusal.

| Join | From → to | Owner |
|---|---|---|
| J-α | request → durable entry (R0-R3), or the ephemeral entry (item 6) | J2a; J3a |
| J-β | fence → project admission, configuration, pack and S3.1 (R4-R10) | X2; M3B; X12r4 |
| J-γ | handoff → the open session (R11-R12) | X2e; X3d; item 7 |
| J-δ | capture session → sealed `snapshot2`: M3C rows 5-9 (M3C:826-830), with downward discovery after the fence (M3B:336) | C1; B2 |
| J-ε | the Plan: M3C rows 10-16 (M3C:831-837). The PlanId is minted at row 14 (M3C:835). Row 15's pre-execution joins come before any provider (M3C:836). | C3; C4 |
| J-ζ | provider stages, one child per `(ExecutionId, SnapshotId, universe key)` (M3L:120), launched only under the D law and O7 (M3P:476) | D; F; G |
| J-η | H's fact admission; then the **full `admit_enumeration`**, after every stage return is admitted and the host-derived inventories exist, and before `derive_evaluation`. This places it, as M3C:854 asks J1 to. | H; J2b |
| J-θ | evaluation through `derive_evaluation` with I1-b2 (I1:406). The Plan's policy comes only from an `AdmittedPack` (X12r4:208). | I1; J2b |
| J-ι | finalization (item 7): replay (X5, with X12d's Run-closure join), `prepare_commit`, `publish`, `finish` | X5; X3d; X7 |
| J-κ | step 1, the render step: the projection of what step 0 holds, the **output decision point** (8.4), then the **final output section**: SOP2's finalization (SOP2:623-650), rendering of the decided envelope, and its output and flush (X7 item 4) | X7; SOP2; S18 |

**5.3 Settlement (r2, J1-R2).**
- Step outcomes are the closed set (WS:101-103).
- The aggregate is taken over required steps in D9 order (WS:233-240). The exit comes from the class by the fixed table only (WS:1355-1356; COMMON4 `StepTermination`).
- A required render failure dominates and keeps the runId (WS:236-238).
- **When each step is terminal:**
  - **Step 0** is terminal when its attempt ends. For a durable attempt, that is when `finish` has returned; for an ephemeral one, when the evaluation result is held.
  - **Step 1** is terminal only when its required work is done: projection, rendering and the output of the required envelope (X7:85; `finalization.rs:310-318`). It completes when `deliver_required` returns `Ok`. It fails when the renderer, the output or the flush fails.
- **The settlement point** is the moment step 1 becomes terminal. The invocation is settled there, and not earlier (WS:224-228; OPP:337-338).
- **The output decision point** (8.4) comes before settlement. It fixes which envelope is rendered: the decided class, or `interrupted` for a signal observed in D. It does not make step 1 terminal.
- **The final output section, phase O,** runs from the decision point to the settlement point. A signal observed there is deferred: it is recorded with arrival phase O and never changes the envelope already decided. This is a cancellation-deferral exception to WS's before-settle rule (WS:224-226), forced by the single required envelope (`bootstrap.rs:57-58`; L464:32).
  - J1 does not claim the existing rule covers it. Successor **S18** reconciles it with the WS and OPP owners (item 13), and J3d's output code is gated on S18's acceptance.
- Interruption follows item 8 (WS:224-231).

**5.4 The choices M3-C hands J1.**
- **(a) Candidate blob custody (M3C:115), lead decision.** Both modes capture into the invocation's private temporary custody. The durable commit publishes from the replay's retained evidence, through X3c item 4, at `prepare_commit` step 6 (`crates/storage/src/commit.rs:243-266`). Nothing is written to the store before the attempt row.
  - **Rejected:** capturing into `I/stores/S`'s CAS during analysis. That would mean store effects before attempt admission and before the publication reserve (X3D:128), orphans on every refusal or cancellation, and a contradiction of S-OP-8's placement, which assumes none (OPP §5.4).
- **(b) The lease (M3C:188).** The writer lease is held from R11 through the commit (IE:1657-1658). The capture walk and discovery run under it, never under the fence (M3B:336).
- **(c) The public projection of `SnapshotBound`, `DependencySetBound` and `DependencyAcquisitionBound`** (M3C:291, :557, :571). J1 adopts S-B: request-rejected 2, `REQUEST.UNSATISFIABLE`, detail `PROJECT.SCOPE_LIMIT`, subject `field:count>limit`, with no Plan and no Run (NE:3534; M3C:915). J's units that can reach these refusals are gated on S-B (M3C:1008).
- **(d) Where the full `admit_enumeration` runs:** J-η.

**5.5 Forbidden substitutes:**
- a step list other than 5.1's;
- a retry;
- a re-entered join;
- an evaluation before J-η;
- a Plan policy not taken from an `AdmittedPack`;
- a store write before the attempt row;
- a downward walk under the fence;
- a refusal with no route.

### 6. The ephemeral path (lead decision; four joins owed by other laws)

- **Decision.** An ephemeral request observes what is lawful to read and writes nothing durable.
  - **The entry.** `Outside` (`request.rs:92`). It goes through the 458c read entry (X1:52): the read receipt on the process's one attempt. It never uses the creator, the ordinary writer or the write gate. It never creates, registers, bootstraps, takes a lease or writes (OWN:28; SL:1521; IE:88, IE:1639-1641).
  - **Core identity.** The read receipt's InitialCore gives the Plan's evaluator closure (EC1; X3D:65-68). A development build ends at F0.
  - **I complete.** Under the read session's fence (X2:169; X12r4:195), the request runs:
    - S3's selection and captures;
    - layer 2, through the session's private-access judgment (M3B:91, :97);
    - configuration resolution and pack admission;
    - X4T's report-only trust admission (X4T:123), with no X4B acceptance (X4B:58);
    - the registered ProjectId when the root is registered, and E-2's otherwise.

    It reads no store and takes no lease. Then the read session's equivalent release (M3B:336; X2:84) comes before the capture session.
  - **I positively absent.** There is no session. Layer 2 is absent: "absent is no layer" (M3B:91). Joins E-1 to E-3 then apply.
  - **I present but incomplete.** The request refuses on the read path's row (L468:46). It never degrades to the absent shape.
  - **The projection.** X7 item 2's ephemeral projection: authority `ephemeral`, no runId (DR-G27; X7:87-93). A failing verdict is policy-failed 1 with `authority: ephemeral` (WS:247-248). Custody is temporary (5.4a). Cancellation has phase A only (item 8).
- **Joins owed by other laws.** J2c, the ephemeral entry end to end, waits on all four. J2a and J2b do not.

| Join | Owner | Need | Lead recommendation |
|---|---|---|---|
| **E-1** | M3-B and X2 (successor S7b) | S3's selection and carrier captures with no installation fence, when I is positively absent. They produce no `ProjectRootAdmission` and grant no registry read, registration, marker or lease. | the same custody predicates on the ephemeral ledger. The fence protects I, and no I exists. |
| **E-2** | M3-C (`snapshot2` takes `projectId` from X2, M3C:320) | the ProjectId of an unregistered root, or of a request with no I | a fresh per-invocation draw that is never persisted or compared. Such PlanIds are not comparable across invocations, and that is stated. |
| **E-3** | M3-C item 7 (closure admission is TR-INDEX-verified by the trust owner, M3C:340-343) and X4T | what an ephemeral request admits with no admitted trust view (I absent, or F absent) | no manifest-admitted closure. Each capability it would serve is provider-unavailable: indeterminate 3, `COVERAGE.PROVIDER_UNAVAILABLE` with `COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED` (WS:1374; NE:3370), never silently dropped (BP:887). |
| **E-4** | X4T | F absent under an ephemeral read session | not a refusal: there is no trust view (E-3). Every other X4T refusal (authentication, floor, rollback, continuation) refuses on its own row (X4T:139-150). |

- **Rejected:**
  - **An ephemeral path that never opens I.** It ignores the user's layer 2 (M3B:91, "always") and can admit no closure at all (M3C:340-343). That makes it indeterminate on every machine.
  - **Writing temporary custody inside I.** Forbidden by SL:1521.
- **Forbidden substitutes:**
  - any write, lease, registration, bootstrap or creation by an ephemeral request;
  - a runId or authoritative label on an ephemeral result;
  - an X4T refusal other than F absent degraded to "no trust";
  - an absent-shape run over an incomplete I.

### 7. Finalization: the session opens at the handoff (lead decision; successors X5 r4 and X7 r7)

- **Decision.**
  - **When the session opens.** It opens at R12, right after the handoff and before the capture session. There are two reasons:
    - the attempt's ExecutionId must exist before any provider spawns (M3L:120, :377; WS:81), and X3d draws it at `open` (X3D:114; `commit_session.rs:322-345`);
    - IE:1657-1658 requires the writer to hold the lease through source admission, evaluation and commit.

    Opening early changes no security or storage code. X9's census already reaches `x3d.session.execution-draw` right after the handoff (X9:939).
  - **What `finalize` takes** (`finalization.rs:395-445`). It takes the open `CommitSession` and the evaluation candidate, and no longer takes an `admit` closure.
    - Replay (X5) still runs first, before `prepare_commit`.
    - A replay refusal ends the session with `CommitSession::refused()` (`commit_session.rs:529-531`) and `finish`, then projects the replay row (X5 item 5). No reserve exists, so nothing is appended (X3D:120).
  - **Every other end after R12.** A refusal or cancellation during analysis ends the session the same way, exactly once: `refused()`, then `finish`.
  - **X5 r4, item 3.** "Replay before any custody" (X5:39) becomes: "replay after evaluation and before `prepare_commit`. A replay refusal ends the attempt before any attempt row, object or journal effect, and the lease and session end through `finish`."
    - The rejected bullet "replaying under the project lease" (X5:43) is withdrawn, because IE:1657-1658 fixes the lease through evaluation.
    - X5 items 4 and 6 stand.
  - **X7 r7, item 1.** The order becomes:
    1. the session, opened by the pipeline at the handoff;
    2. replay;
    3. `prepare_commit` and `publish`;
    4. `finish`, after which step 0 is terminal;
    5. step 1's projection of the committed Run, which is still cancellable (phase D);
    6. the output decision point (8.4);
    7. the final output section (phase O): SOP2's finalization (SOP2:623-650), then rendering and output of the decided envelope (the delivery phase, X7 item 4);
    8. the settlement point, when the output returns (5.3).

    X7 item 7 stands: finalization charges nothing.
  - **X3d r9 (record).** `refused()` also ends a session whose attempt never started. It latches the gate. With no reserve, `finish` appends nothing, and it runs its end step only on an open attempt ledger (X3D:204-210).
- **Rejected:**
  - **Drawing the ExecutionId inside `ProjectOperation` at the handoff.** It changes X2e and X3d item 2 and moves X9's census point.
  - **Opening the session only at the commit.** Providers would run under no ExecutionId, or under one the receipt does not carry.
  - **Keeping `finalize`'s `admit` closure, with X1 and X2 admission after evaluation.** That breaks IE:1657-1658 and X12r4's fenced order, and X1 item 7 forbids the second entry an earlier selection would need.
- **Controls:**
  - **J-C11.** The session opens before the capture session. Providers carry its ExecutionId.
  - **J-C12.** A replay refusal, an analysis refusal and a phase-A cancellation each end through `refused()` and `finish`, once, with nothing appended.
  - **J-C13.** X9's F01 host variant is re-transcribed by S12 if `finish`'s end step changes its post-state.

### 8. S-OP-12: the commit-phase cancellation join (lead decision; successors X3d r9 and X7 r7)

**8.1 The latch: a third source for the existing commit gate.**

The operation's one `FinalGate` (X4:44, :115-116; `commit_authority.rs:26-48`) already latches from the observer and from a failed checkpoint. X3d r9 adds the cancellation latch as a third source, with the same two-bit law.

- **The type, minted once per operation (r2, J1-N1).** `CommitSession::take_cancellation_latch(&mut self) -> Option<CancellationLatch>` returns `Some` once per operation and `None` after that. The latch is security-owned and `Send`. It is not `Clone` or `Default`, not serializable and not constructible. Its one-use method is `latch(self, signal: D9Signal) -> LatchOutcome`. So single use holds per operation, not only per token.
- **Its window, in the gate's own atomic word (r2, J1-N1).** The `FinalGate`'s `AtomicU8` (`commit_authority.rs:26-48`) gains two window bits, beside the two state bits that X4's law already fixes. They are `WINDOW_OPEN` and `WINDOW_CLOSED`, and only the cancellation latch reads them.
  - **Opening.** `WINDOW_OPEN` is set, with one `fetch_or`, when `prepare_commit`'s attempt row commits (X3D:130-133).
  - **Closing.** `WINDOW_CLOSED` is set, with one `fetch_or` whose returned prior value is the sample, on every return of `prepare_commit` and `publish`:
    - `Committed`, where the returned state bits are the `latchedAfterAdmission` sample (`commit_session.rs:953-954`);
    - `Refused`;
    - `CommitUndetermined`;
    - `CarrierCapacityExhausted`;
    - `ExistingAttempt`.

    The close is ordered before any later effect of the return path.
  - **The synchronization order.** `latch` is one compare-exchange loop on the same word. It succeeds only while `WINDOW_OPEN` is set and `WINDOW_CLOSED` is clear, and then it sets the latch bit (`commit_authority.rs:40-44`) in the same exchange. The `x4.gate.latch.after` point fires after it.
    - All of `admit`'s compare-exchange, the latch and the close are on one atomic, in one total order (SeqCst).
    - A latch is therefore either before the close, and so seen by the sample, or after it, and so a no-op returning `OutsideWindow`.
    - Outside the window, `latch` changes nothing.
  - **Results inside the window.** `latch` records `StopCause::Operator { signal }` only if it is the operation's first stop (`operation_guard.rs:99-106`). It returns `BeforeAdmission` (0→2), `AfterAdmission` (1→3) or `AlreadyStopped`.
  - **What does not change.** The admit and latch state law, F41, and every other latch source. `admit`, `observe` and the existing `latch` mask the window bits: `admit` becomes a compare-exchange loop over the word that still moves the two state bits only 0→1, and `state` decodes the state bits alone (`commit_authority.rs:17-25`, `:31-38`). The observer's and checkpoints' latches ignore the window bits.
  - **The successor.** This adds to X4's gate word, so S11 becomes an X4 r8 amendment, not record-only.
- **It grants nothing else:** no observation, admission, permit, effect, ledger charge, retry or reset (F41).
- **The REV reason.** The closed REV reason set (`commit_session.rs:62-104`) gains `operator`, which is S6's own word for an operator stop (SL:491). `StopCause::Operator` maps to it. The reason is shorter than `observer-fail-stop`, so the settlement reserve's exact cost (X3D:243-252) and its pin are unchanged.
- **The termination.** 468c's closed vocabulary gains `InstallationTermination::Interrupted { signal }`, the row of `StopCause::Operator`. It projects to D9 class `interrupted`, exit 130 and `signal`, with no errorCode, faultCause or detail (WS:1363-1364; COMMON4 `StepTermination`, `common-v4.schema.json:750`). `InstallationTerminationV1` requires an errorCode (`crates/host/src/installation_termination.rs:21-28`), so X7 r7's termination type carries the interrupted form separately.

**How X3D's latch rules are kept:**
- **X3D:168-172.** F38 is unchanged: state 2 means no permit, a rolled-back transaction, and the SEAL as history. F39 is unchanged: in state 3 the outcome stands.
- **X3D:261.** The latch retries nothing. The signal latches the gate, and the next checkpoint's refusal latches the attempt ledger as any failed checkpoint does. The settlement reserve funds the REV.
- **X3D:383.** The cancellation is never reported as a value to keep the ledger open.

**8.2 The five phases, and the final output section.**

A phase is fixed by the operation's state when the host **observes** the signal: at once by the latch watcher in B and C, or at the main thread's next decision point in A and D. SOP2's `host.signal.received` record keeps the arrival phase (SOP2:815). Phase O (r2) lies between OPP's D and E. It is the deferral exception of 5.3, and it is not one of OPP's five.

| Phase | Interval (code anchor) | What the signal does | Projection | Durable effect |
|---|---|---|---|---|
| **A.** Before attempt admission | From R0 until `prepare_commit` returns with the attempt row committed (X3D:130). It includes the durable entry, project admission, the whole analysis and replay. | It is cooperative. No new join starts. Providers get `cancel` (M3L:442-462). Native work already in flight completes, including the security entry's. With a session open, the host calls `refused()` and then `finish`. The cancellation latch is not used: `refused()` latches the gate as any refusal before admission does (X4:115), and with no reserve `finish` appends nothing (X3D:120). A signal seen during `prepare_commit`, when `prepare_commit` then returns the admitted attempt, is handled as B. | per 8.3: `interrupted` 130, `kind: failure`, `errors: []`, `termination {class, signal}` (ENV7:704-723), with no runId. A `CommitUndetermined` from the attempt row's own `COMMIT` takes rule 1. | Only what completed. An installation already created stays, and its notice is already on standard error. |
| **B.** Attempt admitted, before FinalGate admission | From the committed attempt row until the compare-exchange at `publish` step 3.9 (`commit_session.rs:930`) | The latch takes the gate 0→2 and records `Operator`. The next checkpoint (3.2, 3.7 or 3.9) refuses: no permit, the staged transaction rolls back, and a durable SEAL stays history (F36, F38). `finish` appends `REV(operator)`, plus `CLN` if a SEAL exists, from the settlement reserve. | per 8.3: `interrupted` 130, as A, unless an uncertain journal commit or barrier came first, which takes rule 1. | The attempt row stays `admitted` until X6's sweep settles it `refused` (X6 item 7). Orphan objects remain. |
| **C.** FinalGate admitted | From state 1 until `publish`'s sample (`commit_session.rs:953-954`) | The latch takes the gate 1→3. The evidence `COMMIT`'s own outcome stands (X3D:170; F39, F40). `finish` appends `REV(operator)` only after `Committed`, because an undetermined outcome forfeits the reserve (X3D:253-258). | per 8.3, matched on the outcome `publish` returned, never on the gate's state: **`CommitUndetermined`** is operational-failed 4, `DURABILITY.COMMIT_FAILED`, `durability-commit`, the ExecutionId as subject, the namespace disclosed, and no runId (X7:101, :120); **`Committed(PublishedCommit)` with `latchedAfterAdmission`** is X7's F39 row (X7:100): operational-failed 4, `DELIVERY.REQUIRED_FAILED`, `delivery-required`, detail `DELIVERY.RENDERER_FAILED_AFTER_COMMIT`, the runId, no delivery phase (SL:551-554). Neither is `interrupted`. | The Run is committed, or undetermined. |
| **D.** Committed, not latched; step 1 cancellable | From `publish` returning `Committed` unlatched (the window is closed) until the output decision point. It includes `finish` and step 1's projection. | There is no latch. `finish` runs to completion. At the decision point, step 1 is `cancelled` and its projection is discarded. | `interrupted` 130 on `kind: run`, with `run.authority: authoritative`, the runId, and `termination {class: interrupted, signal, runId}` (WS:224-227; WFC:4720). This envelope is the invocation's termination output. It is rendered and written in its own final output section. | The Run is committed. No REV is owed for the signal. |
| **O.** Final output section (r2; S18) | From the output decision point until the required output returns (5.3) | **Deferred.** It is recorded with arrival phase O and never changes the decided envelope. A second signal waits for an in-flight write, as for any native effect (OPP:341). A renderer failure inside O takes X7's F16 row in place of the decided envelope, before any byte is written. A write failure after the first byte ends exit 4 with no replacement envelope (`bootstrap.rs:55-60`). | the decided envelope; the exit follows it | as decided |
| **E.** Settled | After the settlement point (5.3) | Nothing is reclassified. The signal is recorded only. | The settled class stands (WS:227-228, WS:1393; WFC:4650). | none |

**8.3 Precedence (lead decision; r2, J1-R1).** For a signal observed before settlement, the rule matches the outcome X3d actually returned first. The gate's state 3 alone proves neither a commitment nor a RunId (X3D:170; X7:100-101; `commit_session.rs:939-958`, where an undetermined `COMMIT` builds no `PublishedCommit`). The first rule that applies decides:
1. **Any `CommitUndetermined`**: from the attempt row's `COMMIT`, a journal commit or barrier, or the evidence `COMMIT`, whatever the gate's state. It takes the durability row, with the ExecutionId (IE:1680-1681; X3D:283; X7:101). The uncertainty must be recovered, and the empty-errors `interrupted` branch can carry no ExecutionId (ENV7:704-723).
2. **A `Committed(PublishedCommit)` whose `latchedAfterAdmission` is set.** X7's F39 row, with the RunId the `PublishedCommit` carries (SL:551-554; X7:100).
3. **A `Committed(PublishedCommit)` not latched, with the signal observed in phase D.** `interrupted`, with that RunId.
4. **Otherwise:** `interrupted`, with no runId.

A signal observed in phase O or E is not "before settlement" for the envelope: O defers it (8.4), and E is settled.

End-path failures are disclosed beside the outcome and never rewrite it (X3D:289).

When another stop came first (`AlreadyStopped`), or a certain refusal ended the attempt before the signal was observed, the REV takes that cause's reason (S6), and the projection still follows rules 1 to 4. WS's before-settle rule makes the aggregate `interrupted` (WS:224-226). The refused attempt's own row is kept in the operational record (SOP2:816), not in the envelope: the empty-errors `interrupted` branch admits no other member (ENV7:704-723, :790).

**8.4 Phase D, the output decision point and phase O (OPP:337; lead decision, r2 J1-R2).**
- **D takes WS's before-settle row,** `interrupted` with the runId. X7's F39 row is reserved for a `Committed` that `publish` sampled as latched (8.3, rule 2).
- **The output decision point** is the single cancellation check after `finish` and step 1's projection. It comes before SOP2's finalization, because SOP2 finalizes once, "after the command's result is decided and before the required envelope is rendered or written" (SOP2:623). It decides which envelope the final output section renders. It does not make step 1 terminal (5.3).
- **Phase O defers a signal.** The required envelope is one, and once its first byte is written no replacement may follow (`bootstrap.rs:57-58`; L464:32). The envelope also carries its own `exitCode` (ENV7 `exitCode`), so a signal that changed the class mid-section would contradict bytes already decided or written. O therefore records the signal and defers it.
  - **This is an exception to WS:224-226's before-settle rule,** because step 1 is not terminal in O. J1 does not claim the existing rule covers it.
  - **S18** reconciles the exception with the WS owner (WS §1's cancellation paragraph) and the OPP owner (OPP §5.5's phase table) as a passage successor. J3d's output code is gated on S18's acceptance. Until then, J3d's other parts may land with their output path unwired.
  - **Its bound.** The section's length is SOP2's bounded finalization (SOP2:623-650) plus one rendering and one output. A blocked output has no elapsed bound (OPP:341), and that is stated, not hidden.
- **Rejected:**
  - **X7's latched row for D.** It would report a delivery failure that did not happen. X7's F39 row means the commit observed a latch after admission (X7:100).
  - **Treating the decision point as settlement (r1).** Step 1 is not terminal there, and a render failure can still follow (X7:85; `finalization.rs:310-318`).
  - **Re-deciding after SOP2's finalization, or interrupting the envelope mid-write.** The first contradicts SOP2:623. The second tears the single required envelope or appends a replacement (`bootstrap.rs:57-58`).
  - **Leaving the output section under the before-settle rule.** A signal there would have to change an envelope whose class and `exitCode` are already decided, or be emitted as exit 130 beside a success envelope.

**8.5 The second stage.**
- A second signal, or the grace expiring, forces provider-tree kill (M3L:442-462; OPP §5.5). The grace is the protocol member that M3L item 16c reconciles (M3L:450-457), not OPP's provisional 2 s. This answers M3L's cross-law finding X3 (M3L:548) for S-OP-12.
- Inside a native effect already in flight, the forced stage waits for it to return, with no elapsed bound (OPP:341):
  - in A, the security entry's native work;
  - in B, a journal commit, barrier or object write;
  - in C, the evidence `COMMIT`.
- SIGKILL leaves M2's recovery evidence (X3D:213). No outcome is invented.

**8.6 What changes in X3D and X7.**
- **X3d r9 (S10):**
  - item 5: the third latch source; `take_cancellation_latch`, minted once per operation; and the window, closed on every return of `prepare_commit` and `publish` (8.1);
  - items 7 and 8: `StopCause::Operator` and the REV reason `operator`, with the reserve cost unchanged;
  - item 9: `InstallationTermination::Interrupted { signal }`, row "operator stop", projected by X7;
  - item 13: unit J3b;
  - the record of item 7 above, on `refused()`;
  - item 2 (r2, J1-R4): `open` reserves its drawn ExecutionId in `ExecutionIdReservations` before the session exists (item 2);
  - new forbidden substitutes: a latch outside the window, a second latch for one operation, a latch used as authority, and the outcome selected from the gate's state rather than from the returned outcome.
- **X4 r8, an amendment (S11; r2).** X4 item 7's gate gains the cancellation latch as a source, and its atomic word gains the two window bits of 8.1. The two-bit state law is unchanged.
- **X7 r7 (S9):**
  - item 1: item 7's order;
  - item 3: a new row, `Refused(Interrupted { signal })`, projected as the A/B `interrupted` envelope. The F39 and `CommitUndetermined` rows are unchanged, and are named as applying whatever the latch source. They are selected by the returned outcome, `CommitUndetermined` first (8.3);
  - item 4: step 1's terminality and the settlement point (5.3), the output decision point, phase D's row and phase O's deferral (8.4, under S18). X7a's `DeliveryPhase::render` (`finalization.rs:256-262`) splits into a projection, which is cancellable in D, and the rendering of the decided envelope, which happens in O;
  - item 8: the termination type's interrupted branch, still with no wildcard arm;
  - new forbidden substitutes: projecting D as F39; F39 for a `CommitUndetermined`; re-deciding the envelope after the output decision point; and a replacement envelope after output has begun.

**8.7 Controls** (OPP §10's cancellation row, OPP:435, made concrete):
- **J-C14.** In-process: a signal at each of phases A to E and O, through the host cancellation source, gives 8.2's projection and durable effect. That includes:
  - "`Committed(PublishedCommit)` with the latch → exit 4 with the runId";
  - "`CommitUndetermined` → exit 4 with the ExecutionId", including **a latch 1→3 followed by an undetermined evidence `COMMIT`**, which must never give F39 or a runId (8.3, rule 1; r2, J1-R1);
  - "a signal in D → exit 130 with the runId";
  - "a signal in O → the decided envelope and its exit, with the signal recorded as O";
  - "a renderer failure in O → F16, with no byte of the decided envelope written".
- **J-C15.** `CancellationLatch` changes nothing outside its window. `take_cancellation_latch` returns `None` the second time. A second `latch` on one token is refused at compile time. A latch racing each of the five closing returns is either seen by that return's sample or is a no-op. `AlreadyStopped` keeps the first cause's REV reason.
- **J-C16.** An injected stall in the evidence `COMMIT` and in a barrier, with a second signal: the process keeps waiting, invents no refusal, and projects per X7 once the call returns.
- **J-C17.** X9 rows S12-B, S12-C, S12-U, S12-D and S12-O (S12, item 12).

### 9. The backup-status successor, J-BS (lead decision; contract successor S13)

- **Shape (the direction recorded at X11:49-54).** `invocation-v5` `$defs/RetentionDisclosure` (INV5:1863-1892) gains an optional member `backupStatus`. Its values are exactly `BackupClassification::disclosed`'s three spellings: `backed-up`, `not-backed-up` and `unknown` (`initial_installation.rs:335-340`). It is never `not-backed-up` from a missing detector.
- **Presence.** It is present exactly when `firstUse` is true. A schema `if`/`then`/`else` enforces both directions.
  - **`firstUse` (lead decision; r2, J1-R3)** is true exactly when item 3's `created` is `Some`: this invocation's creator act performed the publication rename, whether it ended `Published` or refused after the rename. `LostRace` and `NotPristine` minted an intent but created nothing, so `firstUse` is false there and the member is absent.
  - **Rejected:**
    - "true whenever an intent was minted", which would claim a creation this invocation did not perform;
    - a later existence scan, which cannot tell this invocation's creation from another's.
- **Value.** The classification held by this invocation's `CreationIntent`. Under L464 item 2 that is always `unknown`.
- **The notice stays.** It is still written and flushed before effects (L464:27-32). The field adds a carrier and replaces nothing. 464 item 4's acknowledgement member is not added, because no positive detector lands.
- **Versioning (lead decision).** An in-place optional-member append to `invocation-v5`, as a contract successor with regeneration (contracts crate and TypeScript types) and a registry re-pin. Precedents: 468a's in-place `DomainDetailCode` append (L468:52), and NE:3410-3419's prerelease document revision. The successor runs after F8b's execution, because the generator refuses until F8b.
  - **Rejected:** `invocation-6` with `command-envelope-8`. That moves every emitter (metadata, doctor, the delivery failure) and every golden for one optional member, before any release exists.
- **Which envelopes carry `retentionDisclosure` (r2, J1-R3; the existing carrier, ENV7's `retentionDisclosure`):**
  - **Durable, from publication.** Once item 3's `created` is `Some`, **every** envelope of the invocation carries it, success or failure, the one exception being the empty-errors `interrupted` branch. That includes a refusal of attempt B's producers, gate, barriers or rechecks (`EntryRefusal.created`), and every later refusal. Its form is `{policy: durable-unbounded, provenance: DEFAULTED, firstUse: true, storageRoot: the intent's disclosed target, backupStatus}`.
  - **Durable, otherwise,** once R3 has succeeded: the same form with `firstUse: false`, `storageRoot` set to the admitted I's account-derived target, and no `backupStatus`. Before R3, it is absent: no retention posture applies yet.
  - M3 applies no bounded retention (purge and GC are M5).
  - **Ephemeral**, once the capture session has opened: `{policy: ephemeral, provenance: EXPLICIT-FLAG, firstUse: false, storageRoot: the temporary custody root}`.
  - **The empty-errors `interrupted` branch never** carries it (ENV7:790). On a first-use interrupt, the notice is the carrier.
- **The first emitter** is J3d's durable envelope, validated end to end by `workflow_tests.rs`. That answers X11:55: the field is tested through the envelope that carries it.
- **Controls:**
  - **J-C18.** Schema validity of every combination, and absence on the `interrupted` branch.
  - **J-C19.** `firstUse: true` only when `created` is `Some`, on success and on every refusal after the rename (J-C6b). `backupStatus` equals the intent's classification, and its spelling is never `not-backed-up` while the classifier is constant.

### 10. The M3 outcome matrix (law): existing codes only

Every row uses an existing D9 class, error code, fault cause and detail. **No public code is added.** The internal additions are:
- `InstallationTermination::Interrupted`, which maps to the existing class `interrupted`;
- `StopCause::Operator`;
- the REV reason `operator`, which is S6's word (SL:491).

| # | Class (phase) | Class / exit | errorCode / faultCause | Detail or reasonCodes | runId / executionId | Basis |
|---|---|---|---|---|---|---|
| 1 | RequestId allocation fails | — / 4 (one fixed line on standard error, no envelope) | — | `HOST.IO_FAILURE: request identity allocation failed.` | none | `bootstrap.rs:17-23`; OPP:160 |
| 2 | Malformed library request or step list (host-built) | operational-failed / 4 | `SYSTEM.OUTCOME.ILLEGAL_STATE` / host-invariant | absent; the key goes to the operational record | none | NE:3573 |
| 3 | Embedded release absent (F0), durable or ephemeral | request-rejected / 2 | `REQUEST.PRECONDITION_FAILED` | `CORE.NO_EMBEDDED_RELEASE` | none | L468:37 |
| 4 | Actor; other core; platform decision; platform mismatch; H filesystem | request-rejected / 2 | as L468 | as L468:38, :41-44 | none | L468 item 6 |
| 5 | Custody at the probe, the chain, the creator, the gate or the rechecks (including `/` on this host) | request-rejected / 2 | `CONFIG.INVALID` | `CONFIG.CUSTODY_REFUSED`, with its sub-detail as subject | none | L468:45 |
| 6 | I present but incomplete (durable gate, or ephemeral read path) | request-rejected / 2 | `CONFIG.INVALID` | `CONFIG.CUSTODY_REFUSED`, `installation-incomplete` | none | L468:46 |
| 7 | Probe `Present`, gate `Absent` (race) | request-rejected / 2 | `REQUEST.PRECONDITION_FAILED` | `INSTALLATION.NOT_INITIALIZED` | none | item 3; L468:40 |
| 8 | Backup choice required (intent or R7) | request-rejected / 2 | `REQUEST.PRECONDITION_FAILED` | `storage.backup-choice-required` | none | L468:39; L464:9 |
| 9 | Fence busy (durable gate or read session) | operational-failed / 4 | `LEDGER.BUSY_TIMEOUT` / ledger-busy | `PROJECT.BUSY` | none | L468:47 |
| 10 | Notice write or flush failure; a creator or gate rename, barrier or I/O failure | operational-failed / 4 | `HOST.IO_FAILURE` / host-io | — (the envelope's `errors` carries `HOST.IO_FAILURE`) | none | L468:48; X10 r4 item 3 |
| 11 | An attempt or admission ledger charge refused | operational-failed / 4 | `SYSTEM.OUTCOME.ILLEGAL_STATE` / host-invariant | `WORK.BUDGET_EXHAUSTED` | none | L468:49 |
| 12 | Project carrier custody; invalid configuration | request-rejected / 2 | `CONFIG.INVALID` | `CONFIG.CUSTODY_REFUSED` / `CONFIG.INVALID` | none | M3B:99, :151-152 |
| 13 | Invalid compiled default or host-built flags layer | operational-failed / 4 | `SYSTEM.OUTCOME.ILLEGAL_STATE` / host-invariant | `HOST.INVARIANT_VIOLATED` | none | M3B:153 |
| 14 | Pack rows 1, 2 and 3a; row 3; row 4 | request-rejected 2; 2; operational-failed 4 | `CONFIG.INVALID`; `CONFIG.INVALID`; `SYSTEM.OUTCOME.ILLEGAL_STATE` / host-invariant | `CONFIG.INVALID` (X12-0 remedy); `POLICY.IMPERATIVE_KEY_REFUSED`; `HOST.INVARIANT_VIOLATED` | none; first use also discloses the creation | X12:105-111 |
| 15 | Project admission: scope limits; registry or identity refusals | as X2 item 8's rows | as X2 | as X2 (for example `PROJECT.SCOPE_LIMIT`) | none | X2 item 8 |
| 16 | Store endpoint (X3a) | as X3a's rows | as X3a | as X3a (`STATE.SCHEMA_UNSUPPORTED` and so on) | none | X3A item 5 |
| 17 | Trust at the fenced first read: F absent (durable only; item 6 and E-4 for ephemeral); continuation; root chain; payload; clock; incomplete trust records | per X4T item 10: F absent is request-rejected 2; continuation, root, payload and clock are request-rejected 2; incomplete records take row 6 | `REQUEST.PRECONDITION_FAILED` for F absent; `EXTENSION.ADMISSION_REJECTED` for continuation; the others as X4T item 10 fixes | `TRUST.NO_ADMITTED_TIME_CONTEXT`; `CONTINUE-CORE-NOT-TRUSTED`; S5 `ROOT.*`; `PAYLOAD-NOT-ADMISSIBLE`; `CLOCK-EXCURSION-FORWARD` | none | X4T:139-150 |
| 18 | Revoked during the operation | request-rejected / 2 | `EXTENSION.ADMISSION_REJECTED` | `TRUST.COMPONENT_REVOKED_DURING_OPERATION` | none | X4:120 |
| 19 | Observer or monitor fail-stop, including a starved observer during a long analysis | operational-failed / 4 | `HOST.IO_FAILURE` / host-io | `OBSERVER.FAIL_STOP`, subject the stop reason | none | X4:121 |
| 20 | Workspace-unit excess | request-rejected / 2 | `REQUEST.UNSATISFIABLE` | `PROJECT.WORKSPACE_UNIT_LIMIT` | none | NE:3533; M3B:370 |
| 21 | Discovery or snapshot ledger exhausted | operational-failed / 4 | `SYSTEM.OUTCOME.ILLEGAL_STATE` / host-invariant | `WORK.BUDGET_EXHAUSTED` | none | M3B:340 |
| 22 | Snapshot, dependency-set or acquisition bound; prospective-Plan bounds; selection arrays | request-rejected / 2 | `REQUEST.UNSATISFIABLE` | `PROJECT.SCOPE_LIMIT`, `field:count>limit` | none | 5.4c; NE:3534; M3C:915 |
| 23 | Host I/O during capture or discovery | operational-failed / 4 | `HOST.IO_FAILURE` / host-io | — | none | OPP:293 |
| 24 | Explicit root without a marker; root path invalid | request-rejected / 2 | `CONFIG.INVALID` | `native.explicit-root-without-marker` / `PROJECT.EXPLICIT_PATH_INVALID` | none | NE:3527 |
| 25 | Discovery inventory mismatch; stale or non-inert import or prepared row | request-rejected / 2 | `REQUEST.PRECONDITION_FAILED` | `PROJECT.DISCOVERY_INVENTORY_MISMATCH` / `native.stale-*` | none | NE:3525, :3528 |
| 26 | Capability request: invalid; contradictory; not selected | request-rejected / 2 | `CONFIG.INVALID`; per origin; `REQUEST.UNSATISFIABLE` | per NE's route registry | none | NE:3536-3539, :3569-3575 |
| 27 | Required provider closure not installed, or not admissible (including ephemeral with no trust, E-3) | indeterminate / 3 | — | `COVERAGE.PROVIDER_UNAVAILABLE`; `COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED` | runId if committed | WS:1374; NE:3370 |
| 28 | Installed closure bytes corrupt, or unspawnable | operational-failed / 4 | `HOST.IO_FAILURE` / host-io | `DELIVERY.CLOSURE_BYTES_CORRUPT` / `DELIVERY.CLOSURE_UNSPAWNABLE` | none | WS:1375 |
| 29 | Plan just built fails `check_plan_pack`, or the structural enumeration admission | operational-failed / 4 | `SYSTEM.OUTCOME.ILLEGAL_STATE` / host-invariant | `HOST.INVARIANT_VIOLATED` | none | X12:144; M3C:836 |
| 30 | Worker fault: process fault, protocol violation, `ProviderFault`, crash, deadline, liveness, RSS breach | operational-failed / 4 | `PROVIDER.PROTOCOL_VIOLATION` / provider-protocol | absent; the key goes to the operational record | none: no facts, Coverage or Run | NE:3529, :3837-3843; NE:3224 |
| 31 | Clean `Unavailable` or `BudgetExhausted` stage terminal; admitted incomplete inputs | indeterminate / 3 | — | the primary deficiency's route (NE:3364-3374) | runId (authoritative) or `authority: ephemeral` | NE:3844-3855 |
| 32 | Producer Coverage cause or carrier refusal; contradictory completeness | operational-failed / 4 | `PROVIDER.PROTOCOL_VIOLATION` / provider-protocol | absent | none | NE:3538, :3541 |
| 33 | Evaluator work budget | indeterminate / 3 | — | `COVERAGE.BUDGET_EXHAUSTED`; detail `EVALUATION.WORK_BUDGET_EXHAUSTED` | runId (sealed) | OPP:284 |
| 34 | Evaluation output bound | operational-failed / 4 | `OUTPUT.SERIALIZATION_FAILED` / output-serialization | `EVALUATION.OUTPUT_BOUND_EXCEEDED` | per that route (WPC:141, via OPP) | OPP:285 |
| 35 | Verdict: pass; fail; insufficient Coverage | success 0; policy-failed 1; indeterminate 3 | — | reasonCodes on indeterminate | runId, or `authority: ephemeral` | WS:233-248; NE:3364-3374 |
| 36 | Replay refusal (X5) | X5 item 5's rows | as X5 (`EVALUATION.INPUT_REFUSED` and so on) | as X5 | none | X5 item 5 |
| 37 | Commit: busy; host I/O; quarantine; invariant; budget | operational-failed / 4 | per X3D item 9 | per X3D:277-287 | none | X3D:276-289 |
| 38 | `CommitUndetermined`, in any phase, whatever the gate's state (8.3, rule 1) | operational-failed / 4 | `DURABILITY.COMMIT_FAILED` / durability-commit | the ExecutionId as subject; the namespace disclosed | executionId, no runId | X3D:283; X7:101, :120; 8.3 |
| 39 | `ExistingAttempt` (lawfully impossible) | operational-failed / 4 | `SYSTEM.OUTCOME.ILLEGAL_STATE` / host-invariant | `HOST.INVARIANT_VIOLATED`, with the requested binding | executionId | X7:103 |
| 40 | Carrier capacity exhausted | operational-failed / 4 | `LEDGER.BUSY_TIMEOUT` / ledger-busy | `PROJECT.BUSY`, with the rollover disclosed beside | none | X7:104, :165-177 |
| 41 | Capacity preflight (once S-OP-8 is accepted) | operational-failed / 4 | `HOST.IO_FAILURE` / host-io | as S-OP-8 fixes | none | OPP:294 |
| 42 | `Committed(PublishedCommit)` with `latchedAfterAdmission` (observer or signal), selected by the returned outcome, never by state 3 alone (8.3, rule 2) | operational-failed / 4 | `DELIVERY.REQUIRED_FAILED` / delivery-required | `DELIVERY.RENDERER_FAILED_AFTER_COMMIT` | the `PublishedCommit`'s runId | X7:100; SL:551-554 |
| 43 | Required renderer or output failure after commit | operational-failed / 4 | `DELIVERY.REQUIRED_FAILED` / delivery-required | `DELIVERY.RENDERER_FAILED_AFTER_COMMIT` | runId | WS:1376; X7:99 |
| 44 | Required projection failure with no committed Run | operational-failed / 4 | `DELIVERY.REQUIRED_FAILED` / delivery-required | `DELIVERY.REQUIRED_PROJECTION_FAILED` | none | WS:1377 |
| 45 | End-path settlement, end-step or rollover failure | disclosed beside the outcome; never rewrites it | its own row | its own row | — | X3D:289; X7:141-150 |
| 46 | Signal: phase A or B | interrupted / 130 | — | `signal` | none | 8.2; WS:224-227 |
| 47 | Signal: phase D (before the output decision point) | interrupted / 130 | — | `signal` | runId | 8.2; WFC:4720 |
| 48 | Signal: phase O (deferred under S18) or E; optional output failure | the decided or settled class | unchanged | unchanged | unchanged | 5.3; 8.4; WS:1393; X7:106 |
| 49 | Host panic before or after FinalGate admission | operational-failed 4, host-invariant, where the termination layer is reachable after unwinding / nothing manufactured | `SYSTEM.OUTCOME.ILLEGAL_STATE` | — | none / unchanged | OPP:296-297; X3D:213 |
| 50 | Observability loss (SOP2) | none, ever | — | counters only | — | OPP:298; SOP2:710 |
| 51 | `--ephemeral` with an authority prerequisite (not reachable at M3) | request-rejected / 2 | `REQUEST.UNSATISFIABLE` | `WORKFLOW.EPHEMERAL_CANNOT_SUPPLY_AUTHORITY` | none | WS:246; CINV `analyze-ephemeral-required-authority` |
| 52 | Native context or universe binding refused: a stdlib, rust-dev-llvm or tool closure that is unretained, recomputes to another identity or has the wrong kind; a suffix, component, `libSelection`, tool-member or compiler-version join that fails; a universe bound to a context this host did not mint, or to the other language's record. It is reached at J-ε (C2 contexts, M3C rows 10-13), before the PlanId, with no worker spawned. | request-rejected / 2 | `REQUEST.PRECONDITION_FAILED` / — | absent unless a registered `DomainDetailCode` names it. The `native.native-context-*`, `native.universe-context-binding-mismatch` or `native.native-context-language-mismatch` key goes to the operational record. | none | NE:3530; NE:3546-3555 |
| 53 | Preparation bound exceeded. Reached only by native preparation (M5, BP:992), not at M3; recorded as not reachable. | operational-failed / 4 | `HOST.IO_FAILURE` / host-io | per NE's route registry; the key `native.prepare-bound-exceeded` goes to the operational record | none | NE:3531; NE:3546-3555 |
| 54 | Ambient Cargo configuration in an ancestor, or an environment override, at the Rust context and adapter join (C3; M3C:674, C3-T9) | operational-failed / 4 | `HOST.IO_FAILURE` / host-io | per NE's route registry; the key `native.ambient-cargo-config` goes to the operational record | none | NE:3532; NE:3546-3555 |
| 55 | Invalid authenticated release declaration: a capability the matrix does not register, a mode outside the registered set, a `NOT-SELECTED` mode, a duplicate `capabilityId`, or a `preview-*` spelling. The origin is the authenticated release declaration (NE:3574), reached at B1's layer 1 (M3B:90), before any Plan, with no worker spawned. | request-rejected / 2 | `REQUEST.PRECONDITION_FAILED` / — | absent. The `native.release-capability-*` key goes to the operational record. | none | NE:3540, :3574 |

- **Totality.** J2a's projection is an exhaustive match with no wildcard arm (X7 item 8). A detail with no row is a model error, never exit 0 (NE:3543).
- **Control J-C20.** One test per row that M3 code can reach. Rows 41, 51 and 53 are skipped until their owners land, and the skip is recorded.
- **Control J-C20b (r2, J1-R6).**
  - At the C2 context boundary: each row 52 key refuses before the PlanId, with no worker spawned and its key in the operational record.
  - At the Cargo adapter boundary: an ancestor `.cargo/config.toml`, and an environment override, refuse on row 54. This shares C3-T9's fixture (M3C:674).
  - At the release boundary: a malformed declaration under the labelled synthetic signed release refuses on row 55, before any Plan.
- **The internal keys.** Where no registered public detail names a condition, `domainDetail` is absent and the key goes to the operational record (NE:3546-3555). No public code is added.

### 11. Re-commit and the resume writer: owned elsewhere (record of J's interface)

M3P r6 assigns both M2 carry-ins outside J1: re-commit to X3c r8 and X3c-3 (P5-2), and the resume writer to the separate law J-RW and its code unit J4 (P5-1) (M3P:156-157, :236-237, :572-578). J1 decides neither. It records what the pipeline needs from each.

- **Re-commit (X3c r8, X3c-3).** Two analyses of an unchanged project produce the same RunId (IE:104-107). Today the second commit is refused at staging (EXIT:169-171; X3D:51-54). Daily use needs it.
  - **What J needs.** The second commit of a byte-identical Run returns `Committed` with its own attempt row and receipt: "Duplicate retry can share a Run but has a separate attempt receipt" (IE:1683). It must not end on the invariant row.
  - **Order.** X3c-3 lands before J3d (M3P:217).
  - **Control J-C21 (J3d's).** Two durable analyses of an unchanged scratch project both end `Committed`, with two receipts for one RunId. Recovery of either ExecutionId reports committed. X3c-3's own tests own the storage half.
- **The resume writer (J-RW, J4).** The crash states M2 leaves permanently refused are listed at EXIT:186-191.
  - **J1's constraints on J-RW.** Any writer that resumes them is an X1 ordinary writer reached through item 3's durable entry, never the creator act. It adds no public code, class, exit or detail. It deletes no user data and adopts no foreign artifact (OWN:111-120).
  - **Recommendation for J-RW (not a decision).** Complete forward at the next durable request's admission, by each owner's own predicates, as X3b's floor and start steps already reconcile the carrier. A `repair recover` command is M5 (BP:973).
  - **Control J-C22** is J-RW's to define. J3d keeps one test: a durable request over a resumable fixture behaves exactly as J-RW fixes.

### 12. Controls, tests and the crash matrix

- **`workflow_tests.rs`** (COV:7865) carries J-C1 to J-C21 and J3d's half of J-C22, on scratch homes with labelled synthetic signed releases, profiles and closures under the existing `scenario-fixtures` surface (X3D:36-40). It adds no production seam. J's tests also cover:
  - every WFC invocation case M3's step lists can express: WFC:3612, :3741, :4592, :4650 and :4720, plus `operational-fault-dominates-committed-policy-failure`;
  - the CINV goldens `default-first-use-durable` (CINV:1747), `analyze-renderer-failed-after-commit` (:1793), `interrupted-before-settle` (:2047) and `interrupted-after-settle` (:2055).
- **The crash matrix rows J's code must keep passing.**
  - **Both lead sets** (storage 381, host 98 required runs at C = `3d2d5b5`) are rerun on each integration commit of a J unit that touches `crates/security`, `crates/storage` or `host/src/finalization.rs`. The runs are serialized with every other lead set. The 5000 ms timing guard means no concurrent matrix run (M3P:421).
  - **The rows J's units touch:**
    - F00 (census, `x3d.session.execution-draw`);
    - F01 (host replay refusal, with the new `finalize` signature);
    - F06, F11 to F17, F18 and F19;
    - F29 and F30 (lease contention; the lease is now held through analysis);
    - F32 (the capacity rollover, host);
    - F34, F38 to F42, and F44.
  - **Each must keep its transcribed expected value** (X9:1089). A changed driver or expectation (F01, F12, F16, F17, F32, F39 and F40 host halves, because of item 7's signature) is re-transcribed by **S12** (X9 r17, record) **before** that unit's review, never read back from a run.
- **New rows (S12).** Each is transcribed before any run:
  - **S12-B:** a hold at `x3d.publish.after-staging`; a signal through the support surface; the expectation is F38's with `REV(operator)` and the interrupted projection;
  - **S12-C:** a hold at `x3c.evidence.commit.before#1`; a signal; the expectation is F39's, with REV reason `operator`;
  - **S12-U:** S12-C with `fail-after` at `x3c.evidence.commit`; the expectation is F40's, never `interrupted`;
  - **S12-U (r2, J1-R1):** this is the row that pins 8.3's rule 1: a latch 1→3 followed by an undetermined evidence `COMMIT` gives the durability row, never F39 or a runId;
  - **S12-D (r2, J1-R2):** in a host run, a hold at `x3d.finish.end-step.after` (F15's point), which is after `finish` and before the output decision point, so a genuinely cancellable phase D point. Then a signal, then a resume. The expectation is `interrupted` with the runId, the Run committed (R1 CH), and no byte of a success envelope;
  - **S12-O (r2, J1-R2):** a host hold at `x7.delivery.required.before`, which is inside the final output section, after the output decision point and SOP2's finalization. Then a signal, then a resume. The expectation is the decided envelope and its exit, the signal recorded with arrival phase O, and the Run committed. This row exercises S18's deferral, and it is transcribed only once S18 is accepted.
- **Census.** Item 7 adds no durability point. S-OP-12 adds none: it reuses `x4.gate.latch.after`, and its window bits are in memory. The ExecutionId reservation is in memory too (item 2). The REV reason `operator` adds one end-path body inside the existing reserve.

### 13. Successors

| # | Successor | Owner (law) | Content | Gates |
|---|---|---|---|---|
| S1 | **This law** (the X11 successor) | lead | items 1 to 4; it supersedes X11 r1 items 1a, 3 and 5 for M3. X11 items 2 and 6 stand until the M4 CLI unit. | all J units |
| S2 | L468 r6 | security | item 1's route, and the value-only `created` record on the act's result and its post-rename refusals (item 3); item 7 landed by S13 | J3a |
| S3 | X1 r2 | security | items 1 and 7 (item 3); the read receipt with or without a session (item 6) | J3a, J2c |
| S4 | L464 r3 | security | items 1 and 5: the lent RequestId; the prelude's ExecutionId reserved before P0 (item 2) | J3a |
| S5 | X3A r6 | security | item 2's consequence | J3a |
| S6 | X4B r6 | security/trust | item 1's rejected bullet; forbidden-substitute wording | J3a |
| S7 | X2 r10 | security | item 6's creator branch withdrawn | J3a |
| S7b | M3-B and X2 successor (E-1); M3-C (E-2); M3-C item 7 and X4T (E-3, E-4) | B, C, trust owners | item 6's joins | J2c |
| S8 | X5 r4 | host | item 3's order (item 7) | J3b |
| S9 | X7 r7 | host | items 1, 3, 4 and 8 (items 7 and 8) | J3b |
| S10 | X3d r9 | security, storage | 8.1 and 8.6; the `refused()` record; item 2's reservation at `open` | J3a (item 2), J3b |
| S11 | X4 r8 (amendment; r2) | security | the cancellation latch as a gate source, and the two window bits in the gate's word (8.1) | J3b |
| S12 | X9 r17 (record and rows) | lead | re-transcribed host drivers; rows S12-B, -C, -U, -D and -O (-O after S18) | J3b, J3d |
| S13 | J-BS (contract) | workflows/identity | item 9; after F8b's execution | J3d |
| S14 | X3c r8 and X3c-3 (M3P P5-2, M3P:576-578) | storage | re-commit (item 11). J1 needs only its outcome. | J3d |
| S14b | J-RW and J4 (M3P P5-1, M3P:572-575) | M3-J, with the X2, X3c and X4T owners | the resume writer (item 11), under J1's constraints | M3-X |
| S15 | S-OP-12 closed | OPP §9 | item 8 with S9 to S11. OPP's next revision cites it. | — |
| S16 | S-B (M3-C) | native | the bounded projections (5.4c) | J units that reach them |
| S17 | M3-PLAN's next revision (record) | lead | the J row and its units (item 14); "J1 fixes the order" done; M3-C's "J1 chooses" items answered | — |
| S18 | **The final-output-section successor (r2, J1-R2):** a passage successor to WS §1's cancellation paragraph (WS:224-231) and to OPP §5.5's phase table (OPP:330-340) | the WS owner (product workflows) and the OPP owner (CLI and operability) | Step 1 is terminal when its required output returns. From the output decision point to that moment, a signal is recorded with arrival phase O and deferred: it never changes the decided envelope or its exit. A renderer failure there takes F16 before any byte; a write failure after the first byte ends exit 4 with no replacement envelope (5.3, 8.2, 8.4). It adds no class, code or exit. | J3d's output code; S12-O |

Not successors: X12r4, whose first-use clause J1 implements unchanged; and S-OP-2, whose finalization point J1 places (SOP2:623).

### 14. Units J2 to J4

Each unit is reviewed on its own. J4 is listed for its interface only; J-RW owns it (item 11). Inventory numbers are assigned at build time under the linear-chain rule.

| Unit | Content | Depends on | Size |
|---|---|---|---|
| **J2a** | `host/src/invocation.rs`: the typed request, the step lists, the join state machine, settlement, the cancellation source and phase recording. `outcomes.rs`: NE §10's deficiency-to-D9 bridge, the route and origin tables (NE:3364-3374, :3523-3575), and item 10's total projection. Pure, with no I/O. Tests: the WFC cases and D9 goldens. | P0, J1 | M |
| **J2b** | `host/src/analysis.rs`: the shared analysis core from the capture session through evaluation (J-δ to J-θ), on scratch projects with labelled synthetic closures. It is mode-agnostic and opens no installation. | J2a, and M3P's J2 set: H, C4a, C4c, X12d and its lead set, D3, CF-2, I1-b2, X4-F1 and X4-F2 (M3P:217, :309). Its provider stages also need O7 and D1's primitive (M3P:476). | L |
| **J2c** | The ephemeral entry end to end (item 6). | J2b, S3, S7b | M |
| **J3a** | Platform and security: `RequestIdentity` and `ExecutionIdReservations` (item 2); the durable entry, its probe, the two-slot attempt and `EntryRefusal` (item 3); the S2 to S7 code; `open`'s reservation (S10, item 2). Tests J-C2, J-C4, J-C4b and J-C5 to J-C9, with J-C6b. | J1, S2-S7, S10's item 2 | L |
| **J3b** | X3d r9, X4 r8, X7 r7 and X5 r4 code: `take_cancellation_latch`, the window bits, `Operator`, the `refused()` uses, `finalize`'s new signature, step 1's terminality, the output decision point. S12's rows S12-B, -C, -U and -D. | J3a, S8-S12 | L |
| **J3d** | The durable pipeline end to end, R0 to the settlement point; J-BS (S13); `workflow_tests.rs`; J-C10 to J-C21 and J-C20b. Its final output section, and row S12-O, wait for S18. | J2b, **F2 and G3** (M3P:217, :309; r2, J1-R5), J3a, J3b, X3c-3 and its rows, **O1** for SOP2's finalization (M3P:221, :314; r2, J1-N2), S13, S16, S18 | L |
| **J4** | J-RW's code unit (M3P P5-1), outside J1. It reaches the pipeline only through item 3's entry. | J-RW | L |

**Critical path (r2, J1-R5).** M3P r6 sizes J2 → J3 at 3 + 3, finishing on days 25 and 28. J3 needs J2, F2, G3, X3c-3 and its rows; J4 needs J-RW, not J3 (M3P:309-311, :322, :572-578). Under this breakdown:
- J2a, J3a and J3b run before or beside H, off the host chain.
- The chain is H → J2b (3) → J3d (3) → M3-M, so the host-chain figure is unchanged **only if** all of these finish by J2b's last day, M3P's day 25:
  - F2 and G3, whose M3P finishes leave slack against J3;
  - J3a, J3b, X3c-3 and its rows, with their serialized lead sets;
  - O1 and S18.

  If any of them is late, J3d waits for it, day for day, and the path runs through it. Their assumed early finish keeps the estimate, but it does not remove the dependency.
- J4 follows J-RW, as M3P has it.
- The whole-chain estimate stays M3P's conditional 33 days (M3P:320-322). Item 14 changes it only through the waits above, and S17 carries the unit names.

### 15. Record corrections (record only)

- **M3P:217.** J's units are item 14's. M3P:468's "J1 fixes the order and identity rules" is done by items 2 to 4.
- **X11:28's "The M3 unit replaces all four refusals at once"** reads per command (item 1; r2, J1-R7). `audit`'s refusal stays until M5.
- **X11:78-80 (F0 after pack admission)** reads per item 3 under X12 r4.
- **X7:11's "no CLI command is wired (X11 owns CLI enablement)"** now reads: J1 and the M4 CLI unit.
- **The M3C items J1 was asked to choose:** M3C:115 → 5.4a; M3C:188 → 5.4b; M3C:291, :557, :571 → 5.4c; M3C:854 → J-η.

## Forbidden substitutes

- An analysis word wired in the binary at M3; any binary or ingress seam (X11:118).
- Two RequestIds; a RequestId or ExecutionId from a caller or from text; an ExecutionId used before its process reservation (r2); a RunId before `Committed`.
- A creation intent or notice when I is present; authority from the probe; a creator observation reaching attempt B; a second gate; a third attempt; a creation disclosure dropped on a refusal after the rename, or taken from anything but the act's own result (r2).
- Pack admission after any project-scoped effect (X12r4:197-200); a storage-choice refusal after one.
- A store write before the attempt row; a downward walk under the fence; a lease released before the commit's `finish`.
- A retry of any attempt; a re-entered join.
- A signal latch outside its window, minted twice for one operation, or used as authority; a cancellation reported as a value to keep a ledger open (X3D:383).
- Selecting F39 from the gate's state rather than from a returned `Committed(PublishedCommit)`; F39 or a runId for any `CommitUndetermined` (r2); projecting a `Committed` with a latch, or any `CommitUndetermined`, as `interrupted`; projecting phase D as X7's F39 row.
- Calling the output decision point settlement; re-deciding the envelope after it; a replacement envelope after output has begun (r2); rewriting a settled class (WS:1393).
- `audit`'s refusal replaced before its M5 comparison step exists (r2).
- A `backupStatus` without `firstUse`, or `not-backed-up` from a missing detector.
- An ephemeral write, lease, registration, bootstrap, creation, runId or authoritative label.
- A new public code, class, exit, fault cause or detail; a wildcard termination arm.
- Any crash-matrix expectation read back from a run.

## Open questions

**No owner decision blocks J1.** O7 gates provider launch (J-ζ; J2c), not this law (M3P:476).

**Flagged for the owner (non-blocking lead decisions the owner may reverse):**
1. No CLI command at M3 (item 1). The owner's first daily use of `analyze` is M4, with signed releases.
2. First use creates I and then admits a fresh ordinary writer in the same process, running the core and platform producers twice on first use only (item 3).
3. `--ephemeral` reads the installation when one is complete. With no installation, it is indeterminate for every closure-backed capability, with WS:1374's install remedy (item 6).
4. M3 does not retry a busy durable attempt in-process (5.1).
5. (r2) A signal that arrives while the required envelope is being finalized, rendered or written is deferred: it never changes the envelope or the exit (phase O, S18). The alternative would be exit 130 beside a success envelope that has already been decided.

**For the reviewer:**
- **R1.** Is the presence probe (item 3, step 2) lawful against OWN §1a, §5 and §6, and against X1 item 1's purpose-typed receipts?
- **R2.** Does the two-slot attempt (S3) keep the purposes of the one-attempt rule, which are no laundered budget and no reused receipt?
- **R3.** Is opening the session at the handoff (item 7) sound against X5 item 3 and IE:1657-1658, with X3d unchanged?
- **R4.** Is the latch window (8.1), now in the gate's own word and closed on every return, the right boundary for phases B and C? Does 8.3's outcome-first precedence close J1-R1 against X3D:170 and X7:100-101?
- **R5.** Do 5.3, 8.2 and 8.4 close J1-R2? That is: step 1 terminal only when its output returns; the output decision point not called settlement; phase O routed as an exception through S18; S12-D at a cancellable D point and S12-O inside O.
- **R6.** Is J-BS's in-place append lawful under the versioning rules, and does item 9's presence rule from publication (with `EntryRefusal.created`) close J1-R3?
- **R7.** Does item 2's `ExecutionIdReservations` meet IE:77-81 for every ExecutionId, and is it kept distinct from the durable attempt row (IE:83-101; X3D:130-134)?
- **R8.** Are rows 52 to 55 routed exactly as NE:3530-3532, :3540 and :3574 fix them, and is any reachable M3 family still missing?

## Not claimed

- No command enabled; no CLI wiring; no M4 renderer; no `fit` or `audit` pipeline.
- No code, test, build or matrix run for this law.
- No measurement. The critical-path figures are planning assumptions.
- No positive backup detector; no bounded retention; no durable RequestId or ExecutionId registry beyond attempt custody.
- No confinement claim (O7, CF-1); no provider launch rule (D law).
- No settlement of `admitted` attempt rows at M3. X6's sweep reaches them when `store-gc` lands (M5, BP:990), as in M2.
- No elapsed bound on a second-signal wait inside a native effect, or on a blocked output in phase O (OPP:341).
- No acceptance for S-OP-2: J1 places its finalization point (SOP2:623), and its r5 is still in progress.
- No change to the binary's bytes, to `doctor`, or to any accepted public code, class, exit or detail.
- J1 was written from reading the product at `3e64266` and the laws named above. r2 rereads none of the product beyond the r1 citations and `commit_session.rs:939-958`.
