# C2A-ORDER-E1: the R10 invocation identity, and the R8/R9 order, for the public durable pre-draw entry

2026-11-12. Drafted by a lead-dispatched design author (Claude Opus 5.5, route R2-DEEP, effort medium; preflight
`ROUTE-OK R2-DEEP claude claude-opus-5-5/medium`) for unit J3d-TS, scope row C2a (CP-J3D-SECPRE-1), questions Q35,
Q36 and Q37 (`LC/j3d-ts/QUESTIONS.md`:628-661) and the lead's rulings on them (`QUESTIONS.md`:680-708), over the
entry's order note `LC/j3d-ts/C2A-ORDER.md`.
Status: **PROPOSED, r1.** It needs an independent review, then a cross-vendor review, then adoption by the lead
(clauses on law records) and by the project owner, who must be told of E1 (what a durable record carries). It binds
nothing and changes no existing file, schema, registry or lock. Marks: **SETTLED-BY-TEXT** (the texts decide; only the
reading is recorded), **PROPOSED** (a new rule, or a lead ruling no text states), **OPEN** (a named decision is needed).

## Short names

Architecture main `fa6fa0fba` (every line below was read there). Product: **P** = branch `j3d-ts-r1` @ `780c52fc`
(worktree `opensip-j3d-ts`; paths under `crates/`). Product code is cited for facts only, never as law.
`LC` = `.opensip-implementation-cache/lead-2026-10-25`.

| Name | Document |
|---|---|
| **MJ** | `docs/implementation/m3/host-pipeline-j/PROPOSAL.md` (M3-J1 r7, accepted) |
| **SPD** | `docs/implementation/m3/sec-predraw-1/record-r1/SUCCESSOR-SEC-PREDRAW-1-r7.md` (adopted, `ADOPTION-SEC-PREDRAW-1.md`) |
| **IE** | `docs/v2/contracts/product-v1/identity-and-evidence.md` |
| **L464** | `docs/implementation/m2/creation-ingress-464/PROPOSAL.md` (r3, accepted; J1 successor S4) |
| **X2** | `docs/implementation/m2/project-root-x2/PROPOSAL.md` (r10, accepted; MJ cites the r9 snapshot) |
| **X3A5** | `docs/implementation/m2/store-admission-x3a/PROPOSAL-r5.md` (the snapshot MJ cites) |
| **X4T** | `docs/implementation/m2/trust-admission-x4t/PROPOSAL.md` (r13, accepted) |
| **M3C** / **M3B** | `docs/implementation/m3/snapshot-plan-c/PROPOSAL-r7.md` / `config-discovery-b/PROPOSAL-r2.md` |
| **TRS** | P `tools/security/inputs/trust-record-schema.json` (the private trust record schema; a product file, the same `InvocationBinding` as the copy in `docs/implementation/m2/core-inventory-v3-selection-v1/product/`) |

## Summary

| Clause | Question | Mark | Rule in one line |
|---|---|---|---|
| E1a | Q37, the RequestId half | SETTLED-BY-TEXT | The R10 record's `requestId` is the invocation's one RequestId, from the lent `&RequestIdentity`, never text. |
| E1b | Q37, the ExecutionId half | SETTLED-BY-TEXT | On neither route does any ExecutionId exist that the R10 record may lawfully carry. |
| E1c | Q37, the remedy | **OPEN** (owner told) | A law change is needed; three options, none chosen here. |
| E2 | Q35, R8 and R9 | PROPOSED (lead ruling) | Registration (R9) runs before the endpoint join (R8); MJ's table order is an erratum. |
| E3 | Q36, R7 | SETTLED-BY-TEXT | R7 runs on both routes, over a classification and the per-invocation flag, before any project effect. |

## Normative clauses

**E1a. The record's RequestId. SETTLED-BY-TEXT.**
- *Texts.* "The RequestId. One per invocation ... It serves as: ... the correlator of every operational record"
  (MJ:235-237). The host "lends `&RequestIdentity` to item 3's entry" (MJ:239). Forbidden: "two RequestIds in one
  invocation; a RequestId from a caller, from text or from a draw other than the ingress's" (MJ:274-275).
  "Caller-supplied IDs and reuse are refused" (IE:101).
- *Rule.* The R10 `TrustInvocation`'s request id is built inside security from the `&RequestIdentity` the entry already
  receives at R3 (its `bytes()` projection, P `platform/src/lib.rs:130-134`). The production constructor takes
  `&RequestIdentity`, never `&str`. P's `TrustInvocation::new(&str, &str, i64)` (`security/src/trust/live_observation.rs:73`)
  stays fixture-only.

**E1b. No lawful ExecutionId exists at R10, on either route. SETTLED-BY-TEXT.**
- *Texts: what the record needs.* X4T item 7's floor write publishes "a new capsule record ... its publication event and
  descriptor" (X4T:183-184) and "reuses 467's existing trust publication producers" (X4T:187). X4T r13 contains no
  occurrence of "invocation", "ExecutionId" or "RequestId" (grep). The record shape is TRS, a product file: its
  `OperationInputV1` branch for `host-trust-admission` requires `invocation`, and `InvocationBinding` requires
  `requestId`, `stepId` and `executionId` with `additionalProperties: false`; `S4EvaluationInputV2` also requires
  `invocation`. P writes it at `trust/floor_publication.rs:798`; X4B's acceptance at R10 takes the same value
  (`trust/trust_bootstrap.rs:1311`). **Reading:** no law text says the floor record carries an ExecutionId; the
  requirement is in the selected record shape only.
- *Texts: the ExecutionIds of a durable invocation.* "The creation prelude keeps the intent's own draw ... It names the
  creation act in P0 only" (MJ:245). The durable attempt's is "X3d's draw at `CommitSession::open`" (MJ:246). Who
  reserves: "the prelude's, in `mint_intent`, before P0 is staged"; "the durable attempt's, in `CommitSession::open`";
  "the ephemeral and render attempts', in the host, at each attempt's start" (MJ:256-258). Forbidden: "an ExecutionId
  used by P0, a provider frame, a session or a record before its process reservation" (MJ:278). J-C4b: "a first-use
  durable invocation reserves three distinct ExecutionIds (prelude, session, render)" (MJ:287). IE: "Each admitted
  attempt receives a fresh ExecutionId" (IE:62-63); reserved "before use", for "**every** RequestId and ExecutionId"
  (IE:77-80). "For a durable request the ExecutionId is lawful from the session's open" (MJ:264).
- *Texts: R10 and R10a.* R12 is "`CommitSession::open`, which draws the ExecutionId" (MJ:396). At R10a "No
  analysis-attempt ExecutionId is drawn or reserved" (MJ:394). J-C10b, sampled at an R10a refusal:
  `ExecutionIdReservations` "set equals its set at R10a's entry: empty on 3a and on the ephemeral path, and the creation
  prelude's alone on 3b" (MJ:413). SPD: "no path here draws or reserves an analysis-attempt ExecutionId; a source census
  over the boundary's sources finds no `ExecutionIdReservations`" (SPD:700-701). Public row 17 (trust at the fenced
  first read) has `runId / executionId` "none" (MJ:789).
- *Texts: the prelude.* "The prelude's ExecutionId names the creation act in P0 only, and is never reused. No later
  operation of the invocation uses it, and it is never bound to the analysis attempt" (L464:68). MJ's rejection:
  "Binding the prelude's ExecutionId to the analysis attempt" (MJ:268), in the item-2 "Rejected" list beside the
  envelope/intent binding.
- *Route 3a.* No ExecutionId is reserved before R10a: J-C10b fixes the set at R10a's entry as empty (MJ:413), and R10
  runs before R10a. An unreserved draw in the record is forbidden (MJ:278). A reservation at or before R10 contradicts
  MJ:413 and adds an id MJ:256-258 does not list. So no ExecutionId is lawful in the R10 record on 3a.
- *Route 3b.* Only the prelude's is reserved (MJ:413). MJ:268 alone would not exclude it: it rejects binding to the
  analysis attempt, and R10 is not that attempt, whose start is the session's open (MJ:246, :264). **But** L464:68 and
  MJ:245 do exclude it: the floor record is an `OperationInputV1` of a later operation (`host-trust-admission`), and
  the prelude's id "names the creation act in P0 only" and "No later operation of the invocation uses it". This holds
  for `Published`, `LostRace` and `NotPristine` alike. So no ExecutionId is lawful in the R10 record on 3b.
- *Other candidates.* The session's (drawn at R12, after R10; MJ:396) and the render's (after the analysis) do not
  exist at R10, and moving either before R10 is barred (MJ:394, :413, :968). The RequestId is not an ExecutionId: the
  two are "independent 16-byte host-CSPRNG draws" (IE:77).
- *Rule.* The texts decide the question negatively: with the record shape as selected (TRS), R10 cannot be performed
  lawfully on either route. **Conflict:** MJ R10 requires X4T's fenced first read with its floor write (MJ:393), whose
  selected record needs an ExecutionId, while MJ item 2, J-C10b, L464:68 and SPD:700-701 leave none for it.

**E1c. The remedy. OPEN: decided by the lead with two reviews; the project owner is told (it changes what a durable
record carries, or which identities a durable invocation reserves).** Exactly one of:
- **(a) A fourth, R10-scoped reserved ExecutionId.** The entry reserves one id through
  `opensip_platform::reserve_execution_id()` before R10, on both routes; `TrustInvocation` takes `&ReservedExecutionId`.
  It names the trust admission of this invocation only and never reaches attempt custody.
  *Changes:* MJ item 2 (a fourth "who reserves" line at :256-258; J-C4b's "three" becomes four, :287); J-C10b's sampled
  set (:413: "this id alone on 3a; the prelude's and this id on 3b"); IE:62-63 read so that this trust step is an
  "admitted attempt", or IE amended; SPD:701's census, unless the reservation sits outside the boundary's sources (the
  entry's own module). *Durable records:* no shape change; every floor/acceptance record gains an id that no
  operational record or receipt carries.
- **(b) No ExecutionId in the R10 record.** The `host-trust-admission` and `S4EvaluationInputV2` invocation becomes
  `{requestId, stepId}`. *Changes:* a TRS successor (a schema change, through product selection), its decoders accepting
  both shapes, X4T item 7 stating the binding, and `TrustInvocation` losing its ExecutionId. *Durable records:* new
  floor records differ in shape from M2-era ones. MJ item 2 is unchanged.
- **(c) Reuse a named existing id.** Ruled out by E1b on 3a (none exists) and on 3b (L464:68). Listed only so a
  reviewer can see it was weighed; it needs L464 and MJ item 2 amended, and still fails on 3a.
- *StepId.* IE:103: "StepId is the zero-based integer position in the invocation's ordered DAG." L464:68 gives the
  prelude StepId 0. Which step R10's record belongs to is **not located** (looked in MJ items 2-4, L464, X4T, SPD);
  the decider fixes it with (a) or (b). P's fixtures pass 0 (`pre_draw_fixture.rs:153`, `scenario.rs:477`).

**E2. R8 (endpoint) after R9 (registration). PROPOSED (lead ruling Q35 (a), AT RISK until reviewed).**
- *Texts.* MJ: "The durable request runs this order" (MJ:379); R8 "X3a's endpoint admission, from the gate's own
  retained captures, with no new read" (MJ:391); R9 "X2 item 5's registry capture; X2 item 6's first registration"
  (MJ:392). R8's basis X3A5:28-29 states only the one-read rule and the producers ("produced from
  `DurableInstallation`, reached through X1's `OrdinaryWriteAdmission`"); it places nothing relative to the registry.
  X2 item 7a (owner X2e, "after X2d and X3a-1", X2:429): step 1 "Join the Eligible row, root admission, marker,
  tracking observation and `FencedNamespace` with X3a's `SelectedStoreEndpoint` from the same session or gate"
  (X2:430). M3C row 4: "The rest of X2's project admission (items 5 to 7 ...), then the handoff" (M3C:867), with no
  endpoint step. SPD freezes `pre_draw(writer, subject, lease, ...)` (SPD:606) and `durable_pre_draw(writer, subject,
  ...)` (SPD:854-855), where `subject` is R9's result, and: "the endpoint join, the namespace admission, `trust_start`
  ... each run once, in `pre_draw`" (SPD:623-624). Adoption: "`begin` stays the composition of its two phases, so
  X2/X4 behaviour is unchanged" (`ADOPTION-SEC-PREDRAW-1.md`:10). P joins the endpoint only there
  (`security/src/custody/operation_handoff.rs:1350`).
- *Reading.* This is a **conflict** between MJ's table (R8 before R9) and the adopted SPD signatures with the X2e
  composition they preserve (R9 before the endpoint). No text other than MJ's table orders R8 before R9; X3A5 and X2
  7a do not. The lead's ruling is therefore a new rule that resolves a conflict: PROPOSED, not SETTLED-BY-TEXT. It is
  not wrong by any text located: MJ R8's stated content ("from the gate's own retained captures, with no new read")
  still holds in the owners' order.
- *Rule.* The entry runs R9 (X2 items 5, 6a, 6) before R8, and R8 only inside `durable_pre_draw` (one validation, one
  copy of the order). MJ's R8/R9 rows are recorded as an erratum of MJ's table: "R8 runs at X2 item 7a step 1, after
  R9", leaving R8's content unchanged.
- *Observable consequence.* On a first-use candidate (unregistered root), an X3a endpoint refusal (MJ row 16, e.g.
  `STATE.SCHEMA_UNSUPPORTED`; MJ:788) comes after first registration. It leaves the ACTIVE registry row and the
  owners X2 item 6 publishes: the namespace, `.opensip` if it was absent, and the marker (X2:272-274). X2 item 6 says
  a failed step latches "with no later registration step, no retry and no deletion" (X2:256-257). On an Eligible root
  the registry is unchanged.
- *Does a text forbid that state?* **Not located.** "Before any project-scoped effect" is required of R6 (J-C10,
  MJ:399-405) and R7 (MJ:398; :959), not of R8. Row 16 states no durable trace. X3A5 and X2 were searched for a
  rule that an endpoint refusal leaves no registration; none found. Reviewers should confirm this absence.

**E3. R7, the storage choice. SETTLED-BY-TEXT (the shape of the lead's Q36 (a) export: one point to record).**
- *Texts.* R7: "The S3.1 storage choice (`grants.rs`), which is pure. Under 464's constant `UNKNOWN` it admits with the
  notice's disclosure. A positive `BACKED_UP` without the flag is `storage.backup-choice-required`" (MJ:390). "J1 reads
  that as 'before any project-scoped effect of the durable request' (R7) ... On first use, the intent has already
  applied the same choice to the creation (L464:9), and R7 rechecks it against the same classification" (MJ:398).
  M3B: "J3 calls it at the first source-derived write" (M3B:376); the flag is "consumed only by the S3.1 admission"
  (M3B:727). `created: Option<Created { classification, target }>` (MJ:308).
- *Rule.* R7 exists on both routes (MJ:390 has no route qualifier; MJ:398 adds the 3b recheck). It takes a backup
  classification and this invocation's `--allow-backup-custody` flag, and runs after R6 and before R9. On 3b with
  `created: Some`, "the same classification" is `created`'s value, not a fresh classification. **So the export
  should take the classification as an input** (for example `storage_choice_for(classification, flag)`, with 3a
  supplying the classifier's value for I), or offer both forms; `storage_choice_at(target, flag)` alone would
  re-classify on 3b. Under the constant classifier (L464:51) both give `UNKNOWN`.
- *Silence.* On 3b with `LostRace` or `NotPristine`, `created` is `None` (MJ:311) and no value carries the intent's
  classification to R7. Not located: which classification R7 then rechecks. Reading: the classifier's value for I,
  as on 3a (equal today). Listed as O3.

## Open points

| # | Point | Decider |
|---|---|---|
| O1 | E1c: option (a) or (b), with the texts each amends | lead, both reviewers; project owner told |
| O2 | E1c: the StepId of the R10 record | with O1 |
| O3 | E3: R7's classification on 3b when `created` is `None` | lead (reading), with the 464 owner |
| O4 | E2: MJ table erratum (R8/R9) | lead; independent and cross-vendor review |

## Consequences for owning units

**The entry's author may code now** (lead rulings Q36, Q38 and the Q35 ruling AT RISK):
- Q36's export in its owner's module, test first, with the classification as an input (E3);
- Q38's public types and their compile-fail rows;
- R3 through R9 as a crate-private composition, R9 before any endpoint join (E2), with J-C10.

**What waits for O1:** any production `TrustInvocation` constructor; any production call of `durable_pre_draw`; the
public function returning `DurablePreDraw`; any `reserve_execution_id()` call for R10. Fixtures keep drawing text ids
only under the joint fixture predicate.

**Controls each clause implies (each must fail first):**
- **E1-C1 (now).** A census of P: `TrustInvocation::new` and every `exec1_` draw in `security/src` have no caller
  outside the fixture predicate. Planting a production caller fails it.
- **E1-C2 (after O1 (a)).** J-C4b counts four reservations on a first-use invocation; J-C10b's sampled set is the R10
  id alone on 3a, prelude plus R10 id on 3b; the floor record's `executionId` equals the R10 reservation and differs
  from the prelude's, the session's and the render's; the constructor accepts only `&ReservedExecutionId` (compile-fail).
- **E1-C3 (after O1 (b)).** A floor and an acceptance record written at R10 carry no `executionId`; the decoder admits
  both the old and the new shape; a record with a forged `executionId` in the new branch refuses.
- **E1-C4 (either).** The record's `requestId` equals the envelope's and every operational record's (J-C2's form); the
  constructor has no `&str` RequestId (compile-fail).
- **E2-C1.** First-use candidate, endpoint refusal injected (K unsupported): row 16; the registry holds the ACTIVE row,
  namespace and marker; `created` is kept. Eligible root, same injection: registry bytes unchanged.
- **E2-C2.** A source census: `join_store_endpoint` is called only inside `pre_draw_retaining`; a second call in the
  entry fails it.
- **E3-C1.** With a test classifier returning `BACKED_UP` and no flag, on 3a (`created: None`) and 3b (`created:
  Some`): `storage.backup-choice-required`, and no registry row, namespace, `.opensip`, marker, lease or journal.
  With the flag, or under `UNKNOWN`, R7 admits. On 3b the classification passed is `created`'s.

## Rejected alternatives

- **The prelude's ExecutionId in the R10 record.** L464:68: "No later operation of the invocation uses it."
- **Opening the session (R12) before R10.** MJ:394, :413, :968; and X4T writes the floor only "under the fence and
  never under a lease" (X4T:187), so the record cannot wait for R11/R12 either.
- **An unreserved draw in production, as the fixtures do.** MJ:278; IE:77-80.
- **The RequestId's bytes rendered as `exec1_`.** IE:77 (independent draws); MJ:275.
- **E2 (b), a second endpoint validation before R9,** charged on the gate with no text funding it; **E2 (c),** a
  security successor giving `durable_pre_draw` a joined writer: a change to an adopted interface for an order no
  owner's text asks for.
- **E3 by statement only (R7 a no-op under `UNKNOWN`).** It hides a step of MJ's order (the lead's Q36 reason).

## What this record does not do

It chooses no E1c option. It amends no law, schema, registry or code: MJ, IE, L464, X4T, SPD and TRS stay as they are
until O1 and O4 are adopted. It does not trace R10a's store root (C2A-ORDER "values" item 6) or the launch directory
(item 2). It does not re-open J-C10, Q38 or the R3-R6 rows of `C2A-ORDER.md`.
