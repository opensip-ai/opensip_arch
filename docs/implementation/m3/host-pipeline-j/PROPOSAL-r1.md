# The guarded durable host pipeline — proposal M3-J1 r1

2026-10-04. Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the overnight autonomous run. Law for unit **M3-J1** of the accepted M3 unit plan (`M3-PLAN-r4.md:168`; the live draft r5 has the row at `M3-PLAN.md:211`).

**Draft r1, not accepted. Not code.** The file is untracked in arch until acceptance. M2's exit gate X9-6 is integrated (C = `3d2d5b5`; M3P5:5). J's code units still wait for P0, for the B, C, D and H laws and the units named in item 14, and for I1's product units.

**Standing direction.** Every item below that says "lead decision" is made under the owner's standing direction of 2026-09-30 to proceed on the lead's recommendation. Each names the alternative it rejects. The owner may reverse any of them. No item blocks on an owner decision (see "Open questions").

**What this law is.** The M3-J row asks J1 for four things (M3P:168):
1. the X11 successor (X11:64-81);
2. the invocation DAG (WS:76-256) as M3 implements it;
3. the backup-status successor;
4. the commit-phase cancellation join S-OP-12, with the X3D and X7 owners (OPP §5.5, §9).

It also fixes the M3 outcome matrix and breaks J2 to J4 into units.

**The X3D and X7 owners' assent.** OPP names S-OP-12's owning authority as "storage + security (X3D owner) + host finalization (X7 owner)" (OPP:417). Both laws, X3d r8 and X7 r6, are the lead's. Their amendments are written here as successors X3d r9 and X7 r7, as lead decisions under the standing direction. Neither changes before J1 is accepted, and each is reviewed with J1 or right after it.

## Short names

| Name | Document |
|---|---|
| **M3P** | `docs/implementation/m3/M3-PLAN-r4.md`, the accepted r4 bytes. The live `M3-PLAN.md` is draft r5. |
| **M3P5** | `docs/implementation/m3/M3-PLAN.md`, draft r5 (not accepted). It is cited only for its P5 assignments, which J1 follows. |
| **X11** | `docs/implementation/m2/cli-enablement-x11/PROPOSAL.md` (r1 accepted) |
| **X12r4** | `docs/implementation/m2/policy-admission-x12/PROPOSAL.md`. This is r4, in review (`m2/reviews/grok-policy-admission-x12-r4`, ASSIGNED). It is cited by its live lines. |
| **X12** | `…/policy-admission-x12/PROPOSAL-r3.md` (r3 accepted). Its lines are cited the way other laws cite them. |
| **X3D** | `docs/implementation/m2/commit-session-x3d/PROPOSAL.md` (r8) |
| **X7** | `docs/implementation/m2/finalization-x7/PROPOSAL.md` (r6) |
| **L464, L468** | `docs/implementation/m2/{creation-ingress-464,existing-root-admission-468}/PROPOSAL.md` (r2, r5) |
| **X1, X2, X3A, X4, X4B, X4T, X5, X9, X10** | `docs/implementation/m2/{ordinary-platform-x1, project-root-x2, store-admission-x3a, live-guards-x4, trust-bootstrap-x4b, trust-admission-x4t, replay-join-x5, crash-matrix-x9, read-cli-x10}/PROPOSAL.md` |
| **OWN** | `docs/implementation/m2/initial-root-binding-owner-selection-v1/owner.md` |
| **EXIT** | `docs/implementation/m2/EXIT-PLAN.md` |
| **M3B** | `docs/implementation/m3/config-discovery-b/PROPOSAL.md` (r2 accepted) |
| **M3C** | `docs/implementation/m3/snapshot-plan-c/PROPOSAL-r4.md`, the r4 bytes (sha256 `bcf4baa1…`, 1148 lines), reviewed in `reviews/codex2-snapshot-plan-c-r4`. The live `PROPOSAL.md` has moved to draft r5. J1 cites r4's lines; r5 must keep the items J1 answers (item 15) or carry them. |
| **M3L** | `docs/implementation/m3/provider-protocol-l/PROPOSAL.md` (r1 draft, not sent) |
| **I1** | `docs/implementation/m3/preview-pack-i1/PROPOSAL.md` (r2 accepted) |
| **OPP** | `docs/implementation/m3/operability/PLAN.md` (r3 accepted). It is cited by section and by its live lines. |
| **SOP2** | `docs/implementation/m3/operability/s-op-2/PROPOSAL.md`. This is r4, in review (`reviews/codex-s-op-2-r4`; sha256 `db10e19c…`). It is cited by r4's lines. |
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
  - **The M4 CLI unit** replaces all four refusals at once (X11:28). It wires:
    - standard error as the disclosure writer;
    - standard output as the output handle;
    - `isatty(0) && isatty(2)` into `InvocationModeV1` (M3B:114-118). No automation flag is added (M3B:118), so no CINV successor is needed at M3;
    - the SIGINT, SIGTERM and SIGHUP handlers into the cancellation source (item 8).
- **Basis:**
  - BP:887: "Complete CLI analysis delivery follows at M4 with every advertised renderer";
  - BP:895: "Every command delivery also waits for all of its advertised renderer milestones … not releases with silently reduced format contracts";
  - BP:951-955: `default`, `analyze` and `fit` are M4, `audit` is M5;
  - M3P:64 and M3P:301 ("nothing is wired. J1 fixes the order and identity rules");
  - AQP:500 (the dogfood checkpoint "is not CLI `analyze`") and AQP:502 (CLI dogfood is M4);
  - M3B:720, M3B:904.

  Every non-release build ends at InitialCore F0, and this host is BASELINE-ATTESTED (X11:42-45). A live command would therefore give the owner nothing observable at M3.
- **Rejected:**
  - **Wiring `analyze` and the default at M3 with JSON only.** That moves two command rows ahead of their renderer milestone (BP:895).
  - **A hidden or feature-gated CLI word for the harness.** X11:118 forbids an argument, feature or `cfg` seam in the binary. The harness calls the library.
  - **Shipping X11's "create, then refuse".** X11:20-21's reasons b and c still hold for the binary.
- **Forbidden substitutes:**
  - an analysis word wired in `apps/cli` at M3;
  - a binary seam;
  - a library entry that selects a home, profile or release;
  - `fit` or `audit` in the M3 request type.
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
    - **The ephemeral attempt** gets a host process-custody draw at the attempt's start. It never reaches attempt custody (IE:88).
    - **The render step's attempt** gets a host process-custody draw that appears only in operational records.
  - **Phase-lawful identities.** OPP §3.1's table holds, with one reading fixed. For a durable request the ExecutionId is lawful from the session's open (OPP:156's "attempt admission"; item 7), which is the attempt's start. That open precedes the attempt row (X3D:130), and item 8 uses "attempt admitted" for the attempt row only, as OPP §5.5 does (OPP:335).
- **Basis:** WS:78-82; IE:61-63, IE:77-81, IE:88; L464:13-21 and :34; X11:74; OPP §3.1 (OPP:145-160); M3L:375-382.
- **Rejected:**
  - **Binding the envelope's id to the intent's.** The intent exists only on the creation route, after F0, the probe and the actor. A refusal before it (parse, F0, a probe custody row) still needs a RequestId, which is "retained for refusal as well as success" (WS:78-79).
  - **Binding the prelude's ExecutionId to the analysis attempt.** X3d item 2 would have to take an id carried across the creator/ordinary boundary, and the shared RequestId already gives the correlation.
  - **A durable RequestId ledger at M3.** It is a new state class with no carrier.
- **Forbidden substitutes:**
  - two RequestIds in one invocation;
  - a RequestId from a caller, from text or from a draw other than the ingress's;
  - any identity on a provider's wire beyond M3L:377's;
  - a RunId before `Committed` (OPP:157).
- **Controls:**
  - **J-C2.** On the creation route, P0's `invocation.requestId` equals the envelope's `requestId` and every record's. No second RequestId appears anywhere in the invocation's output, records or P0.
  - **J-C3.** Provider frames carry the session's `execution_id()`, and the receipt carries the same ExecutionId.
  - **J-C4.** `RequestIdentity` has no constructor but the draw. This is a compile-fail fixture under X8's driver.

### 3. The durable entry: the creator's host entry, first use and steady state (lead decision)

- **Decision.** Each durable request makes exactly one security call: `enter_durable_analysis(command, backup_custody_flag, &RequestIdentity, disclosure) -> Result<DurableEntry, InstallationTermination>`. The name is J3a's. It is one call, with no producer injection and no home, profile or release selector (X11:66). It runs:
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
  4. **What it returns.** `DurableEntry { admission, created: Option<Created { entered, classification, target }> }`. The `created` part holds values only.
- **The probe's race.** Suppose the probe says `Present`, but the gate's walk then finds I positively absent, because I was deleted outside OpenSIP. The request ends on L468's `INSTALLATION.NOT_INITIALIZED` row (L468:40), whose remedy, "run an admitted durable analysis", is the true next step.
  - **Rejected:** the custody row. I is absent, not foreign.
- **How the creator command ends (X11:67-73; X3A:36).** It does not end after creation. The first-use invocation continues as an ordinary writer through the whole durable DAG, and its termination is the analysis's (item 10). What it tells the user:
  - the standard-error notice (L464:27-32);
  - the envelope's `retentionDisclosure`, with `firstUse` and `backupStatus` (item 9).
- **The creator terminations (X11:74-75).** Every probe, creator, gate and recheck refusal ends on its L468 item 6 row (L468:35-50) through `installation_termination`. It is projected as X10 r4 item 3's refused branch: `kind: failure`, `errors` holding the row's detail (or `HOST.IO_FAILURE`), and exit 2 or 4. After a `Published` creation, a later refusal's envelope carries `retentionDisclosure` with `firstUse: true` (X12r4:200; item 9).
- **The F0 restatement (X11:78-80).**
  - A development build ends at F0 in step 1. That is before the probe, the intent, any disclosure, the fence and pack admission.
  - X11 r1 item 5.8's "after pack admission" followed X12 r3's order. Under X12 r4, pack admission follows the fence, so F0 now precedes it.
  - A release build on this BASELINE-ATTESTED host ends at the probe's custody refusal at `/` (L468:45; X10 r4 "Not claimed"), before any intent or notice. Today's composition mints the intent first.
- **The amendments.** All are lead decisions, recorded as successors S2 to S8. None changes a public code, class, exit, subject or remedy.
  - **L468 r6, item 1.** `Published`, `LostRace` and `NotPristine` end the creator act. The invocation continues through X1's ordinary admission on a fresh attempt, not through a gate lent by the creator's `InitialPlatform`. L468 item 2's sealed capability is unchanged, and attempt B's `InitialPlatform` lends it.
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
  - a store, a trust acceptance or a registration inside the creator act.
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
| R4 | S3's selection walk; X2 r9 item 3a's placement check and chain walk; the carrier captures | M3C:788; M3B:98 |
| R5 | B1 configuration resolution | M3C:789; M3B items 1-11 |
| R6 | X12 pack admission | X12r4:195-206; M3C:790 |
| R7 | The S3.1 storage choice (`grants.rs`), which is pure. Under 464's constant `UNKNOWN` it admits with the notice's disclosure. A positive `BACKED_UP` without the flag is `storage.backup-choice-required` (L468:39). | M3B:378, :729 |
| R8 | X3a's endpoint admission, from the gate's own retained captures, with no new read | X3A:28-29 |
| R9 | X2 item 5's registry capture; X2 item 6's first registration when the root is unregistered, with item 6a's tracking observation | M3C:791; X2:192, :202 |
| R10 | X3b's floor step; the operation's `FreshnessMonitor` and `FinalGate`; X4T's fenced first read, with X4B's acceptance when F is absent | X4:44; X4B:42-56 |
| R11 | X2 item 7's `APPEND-WRITE` lease; X2e's handoff. The fence is released and the lease is held. | X2:328; `operation_handoff.rs:330` |
| R12 | `CommitSession::open`, which draws the ExecutionId | item 7 |

- **The S3.1 slot (lead decision).** M3B says J3 calls the S3.1 choice "at the first source-derived write" (M3B:378). J1 reads that as "before any project-scoped effect of the durable request" (R7). Like a pack refusal, a storage-choice refusal then leaves no project effect. On first use, the intent has already applied the same choice to the creation (L464:9), and R7 rechecks it against the same classification.
- **The first-use clause (X12r4:33-47, :197-200).** This law owns that clause's control.
  - **Control J-C10.** On the creation route (item 3b), a refused project-layer pack ID at R6 leaves:
    - a complete installation;
    - no registry row, namespace, `.opensip`, marker, lease or journal;
    - the refusal's disclosure of the creation, through the notice on standard error and `retentionDisclosure` with `firstUse: true` (item 9).

    This control is shared with M3C:872-876 (C4-T20) and B1-a.
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
- **`analyze`'s `import` step** (CINV:114) is instantiated only when an import is selected. M3 selects none: the `import` command is M5 (BP:957), and C3's library importer is not a step (M3C:464).
- **Retry is `none` (lead decision).** A second durable attempt would need a second write entry, which X1 item 7 forbids even after S3. WS:105-108 makes idempotent retry lawful, not mandatory. A ledger-busy attempt therefore ends on the busy row (X3D:277), with no `WORKFLOW.RETRY_BUDGET_EXHAUSTED`.

**5.2 The analysis step's joins.** Each join hands the next a typed value. No join is re-entered, and a refusal at any join ends step 0 (`rejected` or `failed`). Step 1's gate is `terminal`, so it then projects that refusal.

| Join | From → to | Owner |
|---|---|---|
| J-α | request → durable entry (R0-R3), or the ephemeral entry (item 6) | J2a; J3a |
| J-β | fence → project admission, configuration, pack and S3.1 (R4-R10) | X2; M3B; X12r4 |
| J-γ | handoff → the open session (R11-R12) | X2e; X3d; item 7 |
| J-δ | capture session → sealed `snapshot2`: M3C rows 5-9 (M3C:792-796), with downward discovery after the fence (M3B:336) | C1; B2 |
| J-ε | the Plan: M3C rows 10-16 (M3C:797-803). The PlanId is minted at row 14 (M3C:801). Row 15's pre-execution joins come before any provider (M3C:802). | C3; C4 |
| J-ζ | provider stages, one child per `(ExecutionId, SnapshotId, universe key)` (M3L:120), launched only under the D law and O7 (M3P:308) | D; F; G |
| J-η | H's fact admission; then the **full `admit_enumeration`**, after every stage return is admitted and the host-derived inventories exist, and before `derive_evaluation`. This places it, as M3C:820 asks J1 to. | H; J2b |
| J-θ | evaluation through `derive_evaluation` with I1-b2 (I1:406). The Plan's policy comes only from an `AdmittedPack` (X12r4:208). | I1; J2b |
| J-ι | finalization (item 7): replay (X5, with X12d's Run-closure join), `prepare_commit`, `publish`, `finish` | X5; X3d; X7 |
| J-κ | step 1: the render decision point (item 8), SOP2's finalization (SOP2:623-650), then the delivery phase (X7 item 4) | X7; SOP2 |

**5.3 Settlement.**
- Step outcomes are the closed set (WS:101-103).
- The aggregate is taken over required steps in D9 order (WS:233-240). The exit comes from the class by the fixed table only (WS:1355-1356; COMMON4 `StepTermination`).
- A required render failure dominates and keeps the runId (WS:236-238).
- The invocation is **settled** when every required step is terminal at the render decision point (item 8).
- Interruption follows item 8 (WS:224-231).

**5.4 The choices M3-C hands J1.**
- **(a) Candidate blob custody (M3C:104), lead decision.** Both modes capture into the invocation's private temporary custody. The durable commit publishes from the replay's retained evidence, through X3c item 4, at `prepare_commit` step 6 (`crates/storage/src/commit.rs:243-266`). Nothing is written to the store before the attempt row.
  - **Rejected:** capturing into `I/stores/S`'s CAS during analysis. That would mean store effects before attempt admission and before the publication reserve (X3D:128), orphans on every refusal or cancellation, and a contradiction of S-OP-8's placement, which assumes none (OPP §5.4).
- **(b) The lease (M3C:177).** The writer lease is held from R11 through the commit (IE:1657-1658). The capture walk and discovery run under it, never under the fence (M3B:336).
- **(c) The public projection of `SnapshotBound`, `DependencySetBound` and `DependencyAcquisitionBound`** (M3C:280, :541, :550). J1 adopts S-B: request-rejected 2, `REQUEST.UNSATISFIABLE`, detail `PROJECT.SCOPE_LIMIT`, subject `field:count>limit`, with no Plan and no Run (NE:3534; M3C:881). J's units that can reach these refusals are gated on S-B (M3C:974).
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
| **E-2** | M3-C (`snapshot2` takes `projectId` from X2, M3C:309) | the ProjectId of an unregistered root, or of a request with no I | a fresh per-invocation draw that is never persisted or compared. Such PlanIds are not comparable across invocations, and that is stated. |
| **E-3** | M3-C item 7 (closure admission is TR-INDEX-verified by the trust owner, M3C:329-332) and X4T | what an ephemeral request admits with no admitted trust view (I absent, or F absent) | no manifest-admitted closure. Each capability it would serve is provider-unavailable: indeterminate 3, `COVERAGE.PROVIDER_UNAVAILABLE` with `COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED` (WS:1374; NE:3370), never silently dropped (BP:887). |
| **E-4** | X4T | F absent under an ephemeral read session | not a refusal: there is no trust view (E-3). Every other X4T refusal (authentication, floor, rollback, continuation) refuses on its own row (X4T:139-150). |

- **Rejected:**
  - **An ephemeral path that never opens I.** It ignores the user's layer 2 (M3B:91, "always") and can admit no closure at all (M3C:329-332). That makes it indeterminate on every machine.
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
    4. `finish`;
    5. the render decision point (item 8);
    6. SOP2's finalization (SOP2:623-650);
    7. the delivery phase.

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

- **The type.** `CommitSession::cancellation_latch(&self) -> CancellationLatch` is security-owned and `Send`. It is not `Clone` or `Default`, not serializable and not constructible. Its one-use method is `latch(self, signal: D9Signal) -> LatchOutcome`.
- **Its window.** The window opens when `prepare_commit`'s attempt row commits (X3D:130-133). It closes when `publish` samples `latchedAfterAdmission` (`commit_session.rs:953-954`). Outside the window, `latch` changes nothing and returns `OutsideWindow`.
- **Inside the window, `latch`:**
  - fetch-ORs `2` on the gate once (`commit_authority.rs:40-44`), so the `x4.gate.latch.after` point fires;
  - records `StopCause::Operator { signal }` only if it is the operation's first stop (`operation_guard.rs:99-106`);
  - returns `BeforeAdmission` (0→2), `AfterAdmission` (1→3) or `AlreadyStopped`.
- **It grants nothing else:** no observation, admission, permit, effect, ledger charge, retry or reset (F41).
- **The REV reason.** The closed REV reason set (`commit_session.rs:62-104`) gains `operator`, which is S6's own word for an operator stop (SL:491). `StopCause::Operator` maps to it. The reason is shorter than `observer-fail-stop`, so the settlement reserve's exact cost (X3D:243-252) and its pin are unchanged.
- **The termination.** 468c's closed vocabulary gains `InstallationTermination::Interrupted { signal }`, the row of `StopCause::Operator`. It projects to D9 class `interrupted`, exit 130 and `signal`, with no errorCode, faultCause or detail (WS:1363-1364; COMMON4 `StepTermination`, `common-v4.schema.json:750`). `InstallationTerminationV1` requires an errorCode (`crates/host/src/installation_termination.rs:21-28`), so X7 r7's termination type carries the interrupted form separately.

**How X3D's latch rules are kept:**
- **X3D:168-172.** F38 is unchanged: state 2 means no permit, a rolled-back transaction, and the SEAL as history. F39 is unchanged: in state 3 the outcome stands.
- **X3D:261.** The latch retries nothing. The signal latches the gate, and the next checkpoint's refusal latches the attempt ledger as any failed checkpoint does. The settlement reserve funds the REV.
- **X3D:383.** The cancellation is never reported as a value to keep the ledger open.

**8.2 The five phases.**

A phase is fixed by the operation's state when the host **observes** the signal: at once by the latch watcher in B and C, or at the main thread's next decision point in A and D. SOP2's `host.signal.received` record keeps the arrival phase (SOP2:815).

| Phase | Interval (code anchor) | What the signal does | Projection | Durable effect |
|---|---|---|---|---|
| **A.** Before attempt admission | From R0 until `prepare_commit` returns with the attempt row committed (X3D:130). It includes the durable entry, project admission, the whole analysis and replay. | It is cooperative. No new join starts. Providers get `cancel` (M3L:442-462). Native work already in flight completes, including the security entry's. With a session open, the host calls `refused()` and then `finish`. The cancellation latch is not used: `refused()` latches the gate as any refusal before admission does (X4:115), and with no reserve `finish` appends nothing (X3D:120). A signal seen during `prepare_commit`, when `prepare_commit` then returns the admitted attempt, is handled as B. | `interrupted` 130: `kind: failure`, `errors: []`, `termination {class, signal}` (ENV7:704-723). No runId. | Only what completed. An installation already created stays, and its notice is already on standard error. |
| **B.** Attempt admitted, before FinalGate admission | From the committed attempt row until the compare-exchange at `publish` step 3.9 (`commit_session.rs:930`) | The latch takes the gate 0→2 and records `Operator`. The next checkpoint (3.2, 3.7 or 3.9) refuses: no permit, the staged transaction rolls back, and a durable SEAL stays history (F36, F38). `finish` appends `REV(operator)`, plus `CLN` if a SEAL exists, from the settlement reserve. | `interrupted` 130, as A. **But** an uncertain journal commit or barrier that preceded the latch is the durability row (8.3). | The attempt row stays `admitted` until X6's sweep settles it `refused` (X6 item 7). Orphan objects remain. |
| **C.** FinalGate admitted | From state 1 until `publish`'s sample (`commit_session.rs:953-954`) | The latch takes the gate 1→3. The evidence `COMMIT`'s own outcome stands (X3D:170; F39, F40). `finish` appends `REV(operator)` only for `Committed`, because an undetermined outcome forfeits the reserve (X3D:253-258). | **`Committed` with the latch:** X7's F39 row (X7:100): operational-failed 4, `DELIVERY.REQUIRED_FAILED`, `delivery-required`, detail `DELIVERY.RENDERER_FAILED_AFTER_COMMIT`, the runId, no delivery phase (SL:551-554). **`CommitUndetermined`:** operational-failed 4, `DURABILITY.COMMIT_FAILED`, `durability-commit`, the ExecutionId as subject, the namespace disclosed, no runId (X7:101, :120). Never `interrupted`. | The Run is committed, or undetermined. |
| **D.** Committed, not latched; the render step not terminal | From `publish` returning `Committed` unlatched (the window is closed) until the render decision point | There is no latch. `finish` runs to completion. At the decision point, step 1 is `cancelled`. | `interrupted` 130 on `kind: run`, with `run.authority: authoritative`, the runId, and `termination {class: interrupted, signal, runId}` (WS:224-227; WFC:4720). | The Run is committed. No REV is owed for the signal. |
| **E.** Settled | After the decision point | Nothing is reclassified. The signal is recorded only. | The decided class stands (WS:227-228, WS:1393; WFC:4650). A later write failure keeps X7's F16 row. | none |

**8.3 Precedence (lead decision).** For a signal observed before settlement, the first rule that applies decides:
1. **The commit was admitted before the latch (state 3).** X7's F39 row, with the runId (SL:551-554; X3D:170).
2. **Any `CommitUndetermined`** (attempt admission, a journal commit or barrier, or the evidence `COMMIT`). The durability row, with the ExecutionId (IE:1680-1681; X3D:283). The uncertainty must be recovered, and the empty-errors `interrupted` branch can carry no ExecutionId (ENV7:704-723).
3. **Phase D.** `interrupted` with the runId.
4. **Otherwise** `interrupted`, with no runId.

End-path failures are disclosed beside the outcome and never rewrite it (X3D:289).

When another stop came first (`AlreadyStopped`), or a certain refusal ended the attempt before the signal was observed, the REV takes that cause's reason (S6), and the projection still follows rules 1 to 4. WS's before-settle rule makes the aggregate `interrupted` (WS:224-226). The refused attempt's own row is kept in the operational record (SOP2:816), not in the envelope: the empty-errors `interrupted` branch admits no other member (ENV7:704-723, :790).

**8.4 Phase D against X7's latched row (OPP:337), lead decision.**
- **Decision.** D takes WS's before-settle row, `interrupted` with the runId. X7's F39 row is reserved for a latch that `publish` sampled (state 3).
- **The render decision point** is the single check made after `finish` and before SOP2's finalization and the render. The result is decided there (SOP2:623). After it, a signal is E. The required envelope is then written as decided, and a write failure takes X7's F16 row.
- **Rejected:**
  - **X7's latched row for D.** It would report a delivery failure that did not happen. X7's F39 row means the commit observed a latch after admission (X7:100).
  - **Interrupting the envelope mid-write.** It would tear the single required envelope (`bootstrap.rs:57-58`).

**8.5 The second stage.**
- A second signal, or the grace expiring, forces provider-tree kill (M3L:442-462; OPP §5.5). The grace is the protocol member that M3L item 16c reconciles (M3L:450-457), not OPP's provisional 2 s. This answers M3L's cross-law finding X3 (M3L:548) for S-OP-12.
- Inside a native effect already in flight, the forced stage waits for it to return, with no elapsed bound (OPP:341):
  - in A, the security entry's native work;
  - in B, a journal commit, barrier or object write;
  - in C, the evidence `COMMIT`.
- SIGKILL leaves M2's recovery evidence (X3D:213). No outcome is invented.

**8.6 What changes in X3D and X7.**
- **X3d r9 (S10):**
  - item 5: the third latch source and `CancellationLatch` (8.1);
  - items 7 and 8: `StopCause::Operator` and the REV reason `operator`, with the reserve cost unchanged;
  - item 9: `InstallationTermination::Interrupted { signal }`, row "operator stop", projected by X7;
  - item 13: unit J3b;
  - the record of item 7 above, on `refused()`;
  - new forbidden substitutes: a latch outside the window, a second `latch`, and a latch used as authority.
- **X4 r8, record only (S11).** X4 item 7's gate gains the cancellation latch as a source. Its state law is unchanged.
- **X7 r7 (S9):**
  - item 1: item 7's order;
  - item 3: a new row, `Refused(Interrupted { signal })`, projected as the A/B `interrupted` envelope; the F39 and `CommitUndetermined` rows are unchanged, and are named as applying whatever the latch source;
  - item 4: the render decision point and phase D's row;
  - item 8: the termination type's interrupted branch, still with no wildcard arm;
  - new forbidden substitutes: projecting D as F39, and a cancelled render after the decision point.

**8.7 Controls** (OPP §10's cancellation row, OPP:435, made concrete):
- **J-C14.** In-process: a signal at each of phases A to E, through the host cancellation source, gives 8.2's projection and durable effect. That includes "Committed with the latch → exit 4 with the runId" and "`CommitUndetermined` → exit 4 with the ExecutionId".
- **J-C15.** `CancellationLatch` outside its window changes nothing, a second `latch` is refused at compile time, and `AlreadyStopped` keeps the first cause's REV reason.
- **J-C16.** An injected stall in the evidence `COMMIT` and in a barrier, with a second signal: the process keeps waiting, invents no refusal, and projects per X7 once the call returns.
- **J-C17.** X9 rows S12-B, S12-C, S12-U and S12-D (S12, item 12).

### 9. The backup-status successor, J-BS (lead decision; contract successor S13)

- **Shape (the direction recorded at X11:49-54).** `invocation-v5` `$defs/RetentionDisclosure` (INV5:1863-1892) gains an optional member `backupStatus`. Its values are exactly `BackupClassification::disclosed`'s three spellings: `backed-up`, `not-backed-up` and `unknown` (`initial_installation.rs:335-340`). It is never `not-backed-up` from a missing detector.
- **Presence.** It is present exactly when `firstUse` is true. A schema `if`/`then`/`else` enforces both directions.
  - **`firstUse` (lead decision)** is true exactly when this invocation's creator act ended `Published`. `LostRace` and `NotPristine` minted an intent, but this invocation created nothing, so `firstUse` is false there and the member is absent.
  - **Rejected:** "true whenever an intent was minted", which would claim a creation this invocation did not perform.
- **Value.** The classification held by this invocation's `CreationIntent`. Under L464 item 2 that is always `unknown`.
- **The notice stays.** It is still written and flushed before effects (L464:27-32). The field adds a carrier and replaces nothing. 464 item 4's acknowledgement member is not added, because no positive detector lands.
- **Versioning (lead decision).** An in-place optional-member append to `invocation-v5`, as a contract successor with regeneration (contracts crate and TypeScript types) and a registry re-pin. Precedents: 468a's in-place `DomainDetailCode` append (L468:52), and NE:3410-3419's prerelease document revision. The successor runs after F8b's execution, because the generator refuses until F8b.
  - **Rejected:** `invocation-6` with `command-envelope-8`. That moves every emitter (metadata, doctor, the delivery failure) and every golden for one optional member, before any release exists.
- **Which envelopes carry `retentionDisclosure`:**
  - **Durable**, once R3 has succeeded: `{policy: durable-unbounded, provenance: DEFAULTED, firstUse, storageRoot: I's account-derived target}`, with `backupStatus` when `firstUse` is true. M3 applies no bounded retention (purge and GC are M5).
  - **Ephemeral**, once the capture session has opened: `{policy: ephemeral, provenance: EXPLICIT-FLAG, firstUse: false, storageRoot: the temporary custody root}`.
  - **The empty-errors `interrupted` branch never** carries it (ENV7:790). On a first-use interrupt, the notice is the carrier.
- **The first emitter** is J3d's durable envelope, validated end to end by `workflow_tests.rs`. That answers X11:55: the field is tested through the envelope that carries it.
- **Controls:**
  - **J-C18.** Schema validity of every combination, and absence on the `interrupted` branch.
  - **J-C19.** `firstUse: true` only on `Published`. `backupStatus` equals the intent's classification, and its spelling is never `not-backed-up` while the classifier is constant.

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
| 22 | Snapshot, dependency-set or acquisition bound; prospective-Plan bounds; selection arrays | request-rejected / 2 | `REQUEST.UNSATISFIABLE` | `PROJECT.SCOPE_LIMIT`, `field:count>limit` | none | 5.4c; NE:3534; M3C:881 |
| 23 | Host I/O during capture or discovery | operational-failed / 4 | `HOST.IO_FAILURE` / host-io | — | none | OPP:293 |
| 24 | Explicit root without a marker; root path invalid | request-rejected / 2 | `CONFIG.INVALID` | `native.explicit-root-without-marker` / `PROJECT.EXPLICIT_PATH_INVALID` | none | NE:3527 |
| 25 | Discovery inventory mismatch; stale or non-inert import or prepared row | request-rejected / 2 | `REQUEST.PRECONDITION_FAILED` | `PROJECT.DISCOVERY_INVENTORY_MISMATCH` / `native.stale-*` | none | NE:3525, :3528 |
| 26 | Capability request: invalid; contradictory; not selected | request-rejected / 2 | `CONFIG.INVALID`; per origin; `REQUEST.UNSATISFIABLE` | per NE's route registry | none | NE:3536-3539, :3569-3575 |
| 27 | Required provider closure not installed, or not admissible (including ephemeral with no trust, E-3) | indeterminate / 3 | — | `COVERAGE.PROVIDER_UNAVAILABLE`; `COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED` | runId if committed | WS:1374; NE:3370 |
| 28 | Installed closure bytes corrupt, or unspawnable | operational-failed / 4 | `HOST.IO_FAILURE` / host-io | `DELIVERY.CLOSURE_BYTES_CORRUPT` / `DELIVERY.CLOSURE_UNSPAWNABLE` | none | WS:1375 |
| 29 | Plan just built fails `check_plan_pack`, or the structural enumeration admission | operational-failed / 4 | `SYSTEM.OUTCOME.ILLEGAL_STATE` / host-invariant | `HOST.INVARIANT_VIOLATED` | none | X12:144; M3C:802 |
| 30 | Worker fault: process fault, protocol violation, `ProviderFault`, crash, deadline, liveness, RSS breach | operational-failed / 4 | `PROVIDER.PROTOCOL_VIOLATION` / provider-protocol | absent; the key goes to the operational record | none: no facts, Coverage or Run | NE:3529, :3837-3843; NE:3224 |
| 31 | Clean `Unavailable` or `BudgetExhausted` stage terminal; admitted incomplete inputs | indeterminate / 3 | — | the primary deficiency's route (NE:3364-3374) | runId (authoritative) or `authority: ephemeral` | NE:3844-3855 |
| 32 | Producer Coverage cause or carrier refusal; contradictory completeness | operational-failed / 4 | `PROVIDER.PROTOCOL_VIOLATION` / provider-protocol | absent | none | NE:3538, :3541 |
| 33 | Evaluator work budget | indeterminate / 3 | — | `COVERAGE.BUDGET_EXHAUSTED`; detail `EVALUATION.WORK_BUDGET_EXHAUSTED` | runId (sealed) | OPP:284 |
| 34 | Evaluation output bound | operational-failed / 4 | `OUTPUT.SERIALIZATION_FAILED` / output-serialization | `EVALUATION.OUTPUT_BOUND_EXCEEDED` | per that route (WPC:141, via OPP) | OPP:285 |
| 35 | Verdict: pass; fail; insufficient Coverage | success 0; policy-failed 1; indeterminate 3 | — | reasonCodes on indeterminate | runId, or `authority: ephemeral` | WS:233-248; NE:3364-3374 |
| 36 | Replay refusal (X5) | X5 item 5's rows | as X5 (`EVALUATION.INPUT_REFUSED` and so on) | as X5 | none | X5 item 5 |
| 37 | Commit: busy; host I/O; quarantine; invariant; budget | operational-failed / 4 | per X3D item 9 | per X3D:277-287 | none | X3D:276-289 |
| 38 | `CommitUndetermined`, in any phase and whatever the latch | operational-failed / 4 | `DURABILITY.COMMIT_FAILED` / durability-commit | the ExecutionId as subject; the namespace disclosed | executionId, no runId | X3D:283; X7:101, :120; 8.3 |
| 39 | `ExistingAttempt` (lawfully impossible) | operational-failed / 4 | `SYSTEM.OUTCOME.ILLEGAL_STATE` / host-invariant | `HOST.INVARIANT_VIOLATED`, with the requested binding | executionId | X7:103 |
| 40 | Carrier capacity exhausted | operational-failed / 4 | `LEDGER.BUSY_TIMEOUT` / ledger-busy | `PROJECT.BUSY`, with the rollover disclosed beside | none | X7:104, :165-177 |
| 41 | Capacity preflight (once S-OP-8 is accepted) | operational-failed / 4 | `HOST.IO_FAILURE` / host-io | as S-OP-8 fixes | none | OPP:294 |
| 42 | `Committed` with a latch (observer or signal) | operational-failed / 4 | `DELIVERY.REQUIRED_FAILED` / delivery-required | `DELIVERY.RENDERER_FAILED_AFTER_COMMIT` | runId | X7:100; SL:551-554 |
| 43 | Required renderer or output failure after commit | operational-failed / 4 | `DELIVERY.REQUIRED_FAILED` / delivery-required | `DELIVERY.RENDERER_FAILED_AFTER_COMMIT` | runId | WS:1376; X7:99 |
| 44 | Required projection failure with no committed Run | operational-failed / 4 | `DELIVERY.REQUIRED_FAILED` / delivery-required | `DELIVERY.REQUIRED_PROJECTION_FAILED` | none | WS:1377 |
| 45 | End-path settlement, end-step or rollover failure | disclosed beside the outcome; never rewrites it | its own row | its own row | — | X3D:289; X7:141-150 |
| 46 | Signal: phase A or B | interrupted / 130 | — | `signal` | none | 8.2; WS:224-227 |
| 47 | Signal: phase D | interrupted / 130 | — | `signal` | runId | 8.2; WFC:4720 |
| 48 | Signal: phase E; optional output failure | the settled class | unchanged | unchanged | unchanged | WS:1393; X7:106 |
| 49 | Host panic before or after FinalGate admission | operational-failed 4, host-invariant, where the termination layer is reachable after unwinding / nothing manufactured | `SYSTEM.OUTCOME.ILLEGAL_STATE` | — | none / unchanged | OPP:296-297; X3D:213 |
| 50 | Observability loss (SOP2) | none, ever | — | counters only | — | OPP:298; SOP2:710 |
| 51 | `--ephemeral` with an authority prerequisite (not reachable at M3) | request-rejected / 2 | `REQUEST.UNSATISFIABLE` | `WORKFLOW.EPHEMERAL_CANNOT_SUPPLY_AUTHORITY` | none | WS:246; CINV `analyze-ephemeral-required-authority` |

- **Totality.** J2a's projection is an exhaustive match with no wildcard arm (X7 item 8). A detail with no row is a model error, never exit 0 (NE:3543).
- **Control J-C20.** One test per row that M3 code can reach. Rows 41 and 51 are skipped until their owners land, and the skip is recorded.

### 11. Re-commit and the resume writer: owned elsewhere (record of J's interface)

M3P5 assigns both M2 carry-ins outside J1: re-commit to X3c r8 and X3c-3 (P5-2), and the resume writer to the separate law J-RW and its code unit J4 (P5-1) (M3P5:150-151, :230-231, :566-570). J1 decides neither. It records what the pipeline needs from each.

- **Re-commit (X3c r8, X3c-3).** Two analyses of an unchanged project produce the same RunId (IE:104-107). Today the second commit is refused at staging (EXIT:169-171; X3D:51-54). Daily use needs it.
  - **What J needs.** The second commit of a byte-identical Run returns `Committed` with its own attempt row and receipt: "Duplicate retry can share a Run but has a separate attempt receipt" (IE:1683). It must not end on the invariant row.
  - **Order.** X3c-3 lands before J3d (M3P5:211).
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
  - **Both lead sets** (storage 381, host 98 required runs at C = `3d2d5b5`) are rerun on each integration commit of a J unit that touches `crates/security`, `crates/storage` or `host/src/finalization.rs`. The runs are serialized with every other lead set. The 5000 ms timing guard means no concurrent matrix run (M3P:268).
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
  - **S12-D:** a host hold at `x7.delivery.required.before`; a signal; the expectation is `interrupted` with the runId, and the Run committed (R1 CH).
- **Census.** Item 7 adds no durability point, and S-OP-12 adds none (it reuses `x4.gate.latch.after`). The REV reason `operator` adds one end-path body inside the existing reserve.

### 13. Successors

| # | Successor | Owner (law) | Content | Gates |
|---|---|---|---|---|
| S1 | **This law** (the X11 successor) | lead | items 1 to 4; it supersedes X11 r1 items 1a, 3 and 5 for M3. X11 items 2 and 6 stand until the M4 CLI unit. | all J units |
| S2 | L468 r6 | security | item 1's route (item 3); item 7 landed by S13 | J3a |
| S3 | X1 r2 | security | items 1 and 7 (item 3); the read receipt with or without a session (item 6) | J3a, J2c |
| S4 | L464 r3 | security | items 1 and 5: the lent RequestId | J3a |
| S5 | X3A r6 | security | item 2's consequence | J3a |
| S6 | X4B r6 | security/trust | item 1's rejected bullet; forbidden-substitute wording | J3a |
| S7 | X2 r10 | security | item 6's creator branch withdrawn | J3a |
| S7b | M3-B and X2 successor (E-1); M3-C (E-2); M3-C item 7 and X4T (E-3, E-4) | B, C, trust owners | item 6's joins | J2c |
| S8 | X5 r4 | host | item 3's order (item 7) | J3b |
| S9 | X7 r7 | host | items 1, 3, 4 and 8 (items 7 and 8) | J3b |
| S10 | X3d r9 | security, storage | 8.1 and 8.6; the `refused()` record | J3b |
| S11 | X4 r8 (record) | security | the cancellation latch as a gate source | J3b |
| S12 | X9 r17 (record and rows) | lead | re-transcribed host drivers; rows S12-B, -C, -U, -D | J3b, J3d |
| S13 | J-BS (contract) | workflows/identity | item 9; after F8b's execution | J3d |
| S14 | X3c r8 and X3c-3 (M3P5 P5-2) | storage | re-commit (item 11). J1 needs only its outcome. | J3d |
| S14b | J-RW and J4 (M3P5 P5-1) | M3-J, with the X2, X3c and X4T owners | the resume writer (item 11), under J1's constraints | M3-X |
| S15 | S-OP-12 closed | OPP §9 | item 8 with S9 to S11. OPP's next revision cites it. | — |
| S16 | S-B (M3-C) | native | the bounded projections (5.4c) | J units that reach them |
| S17 | M3P5 (draft r5, record) | lead | the J row and its units (item 14); "J1 fixes the order" done; M3-C's "J1 chooses" items answered | — |

Not successors: X12r4, whose first-use clause J1 implements unchanged; and S-OP-2, whose finalization point J1 places (SOP2:623).

### 14. Units J2 to J4

Each unit is reviewed on its own. J4 is listed for its interface only; J-RW owns it (item 11). Inventory numbers are assigned at build time under the linear-chain rule.

| Unit | Content | Depends on | Size |
|---|---|---|---|
| **J2a** | `host/src/invocation.rs`: the typed request, the step lists, the join state machine, settlement, the cancellation source and phase recording. `outcomes.rs`: NE §10's deficiency-to-D9 bridge, the route and origin tables (NE:3364-3374, :3523-3575), and item 10's total projection. Pure, with no I/O. Tests: the WFC cases and D9 goldens. | P0, J1 | M |
| **J2b** | `host/src/analysis.rs`: the shared analysis core from the capture session through evaluation (J-δ to J-θ), on scratch projects with labelled synthetic closures. It is mode-agnostic and opens no installation. | J2a, and M3P5's J2 set: H, C4a, C4c, X12d and its lead set, D3, CF-2, I1-b2, X4-F1 and X4-F2 (M3P5:211). Its provider stages also need O7 and D1's primitive (M3P:308). | L |
| **J2c** | The ephemeral entry end to end (item 6). | J2b, S3, S7b | M |
| **J3a** | Security: `RequestIdentity`; the durable entry, its probe and the two-slot attempt (item 3); the S2 to S7 code. Tests J-C2 and J-C5 to J-C9. | J1, S2-S7 | L |
| **J3b** | X3d r9, X7 r7 and X5 r4 code: `CancellationLatch`, `Operator`, the `refused()` uses, `finalize`'s new signature, the D decision point. S12's rows. | J3a, S8-S12 | L |
| **J3d** | The durable pipeline end to end, R0 to delivery; J-BS (S13); `workflow_tests.rs`; J-C10 to J-C21. | J2b, J3a, J3b, X3c-3, S13, S16 | L |
| **J4** | J-RW's code unit (M3P5 P5-1), outside J1. It reaches the pipeline only through item 3's entry. | J-RW | L |

**Critical path.** M3P:218-229 sizes J as J2 → J3 → J4, at 3 + 3 + 2 days. Draft M3P5 keeps J2 → J3 at 3 + 3 (days 25 and 28) and takes J4 off J3 (M3P5:303-305, :566-569). Under this breakdown:
- J2a, J3a and J3b run before or beside H, off the host chain.
- The chain is H → J2b (3) → J3d (3) → M3-M, so the host-chain figure is unchanged, provided J3a, J3b and X3c-3 integrate by J2b's finish.
- J4 follows J-RW, as M3P5 has it.
- If J3b's lead-set reruns slip, J3d waits for them, day for day.
- The current whole-chain estimates are M3P5's and M3-C r4's (M3C:1050-1056). Item 14 changes neither, and S17 carries the unit names.

### 15. Record corrections (record only)

- **M3P:168 and M3P5:211.** J's units are item 14's. M3P:301's "J1 fixes the order and identity rules" is done by items 2 to 4.
- **M3P:110-111 and M3P:168** cite EXIT:169 and EXIT:184-189. Those passages are now at EXIT:169-171 and EXIT:186-191, as M3P5:150-151 already has them.
- **X11:78-80 (F0 after pack admission)** reads per item 3 under X12 r4.
- **X7:11's "no CLI command is wired (X11 owns CLI enablement)"** now reads: J1 and the M4 CLI unit.
- **The M3C items J1 was asked to choose:** M3C:104 → 5.4a; M3C:177 → 5.4b; M3C:280, :541, :550 → 5.4c; M3C:820 → J-η.

## Forbidden substitutes

- An analysis word wired in the binary at M3; any binary or ingress seam (X11:118).
- Two RequestIds; a RequestId or ExecutionId from a caller or from text; a RunId before `Committed`.
- A creation intent or notice when I is present; authority from the probe; a creator observation reaching attempt B; a second gate; a third attempt.
- Pack admission after any project-scoped effect (X12r4:197-200); a storage-choice refusal after one.
- A store write before the attempt row; a downward walk under the fence; a lease released before the commit's `finish`.
- A retry of any attempt; a re-entered join.
- A signal latch outside its window, or used as authority; a cancellation reported as a value to keep a ledger open (X3D:383).
- Projecting a state-3 commit, or any `CommitUndetermined`, as `interrupted`; projecting phase D as X7's F39 row; rewriting a settled class (WS:1393).
- A `backupStatus` without `firstUse`, or `not-backed-up` from a missing detector.
- An ephemeral write, lease, registration, bootstrap, creation, runId or authoritative label.
- A new public code, class, exit, fault cause or detail; a wildcard termination arm.
- Any crash-matrix expectation read back from a run.

## Open questions

**No owner decision blocks J1.** O7 gates provider launch (J-ζ; J2c), not this law (M3P:308).

**Flagged for the owner (non-blocking lead decisions the owner may reverse):**
1. No CLI command at M3 (item 1). The owner's first daily use of `analyze` is M4, with signed releases.
2. First use creates I and then admits a fresh ordinary writer in the same process, running the core and platform producers twice on first use only (item 3).
3. `--ephemeral` reads the installation when one is complete. With no installation, it is indeterminate for every closure-backed capability, with WS:1374's install remedy (item 6).
4. M3 does not retry a busy durable attempt in-process (5.1).

**For the reviewer:**
- **R1.** Is the presence probe (item 3, step 2) lawful against OWN §1a, §5 and §6, and against X1 item 1's purpose-typed receipts?
- **R2.** Does the two-slot attempt (S3) keep the purposes of the one-attempt rule, which are no laundered budget and no reused receipt?
- **R3.** Is opening the session at the handoff (item 7) sound against X5 item 3 and IE:1657-1658, with X3d unchanged?
- **R4.** Is the latch window (8.1) the right boundary for phases B and C, and is 8.3's precedence sound against WS:224-227 and SL:551-554?
- **R5.** Is phase D's decision point (8.4) sound against the single-envelope rule?
- **R6.** Is J-BS's in-place append lawful under the versioning rules?
- **R7.** Is any row of item 10 mis-routed against NE §10, X3D item 9, X7 item 3 or the L468 table?

## Not claimed

- No command enabled; no CLI wiring; no M4 renderer; no `fit` or `audit` pipeline.
- No code, test, build or matrix run for this law.
- No measurement. The critical-path figures are planning assumptions.
- No positive backup detector; no bounded retention; no durable RequestId registry.
- No confinement claim (O7, CF-1); no provider launch rule (D law).
- No settlement of `admitted` attempt rows at M3. X6's sweep reaches them when `store-gc` lands (M5, BP:990), as in M2.
- No elapsed bound on a second-signal wait inside a native effect (OPP:341).
- No change to the binary's bytes, to `doctor`, or to any accepted public code, class, exit or detail.
- J1 was written from reading the product at `3e64266` and the laws named above.
