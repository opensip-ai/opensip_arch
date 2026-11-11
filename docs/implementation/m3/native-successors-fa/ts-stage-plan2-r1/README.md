# TS-STAGE-PLAN2-r1 — the `typescript-semantic` provider stage in `exec-plan2` and the stage-request projection for a `plan2` Plan

2026-11-11. Drafted by a lead-dispatched design author (Claude Opus 5.5, route R2-DEEP) from the lead's rulings on gap Q14.
Status: **PROPOSED, r1, unreviewed.** It needs one independent review, then a cross-vendor review, then adoption by the
lead. It binds nothing, changes no existing file, registry, inventory or lock, and has no subject manifest yet.

**Scope.** TypeScript only, milestone M3-M-TS1. The Rust provider (`rust-semantic`) has the same gap
(`rust-provider-protocol.v2.json:222`, "exact C-2 value"; X-RL-C2, `rust3-lim/README.md:376`) and is out of scope.

## Short names

Base: architecture main `3e4203f0f`. Product citations: worktree `opensip-c4ats-b` at `1274eb86` (**B**); provider
worktree `opensip-f2min` at `e526e873` (**F**).

| Name | Document |
|---|---|
| **DLV** | `docs/coop/artifacts/delivery.v2.json` |
| **NE** | `docs/v2/contracts/product-v1/native-evidence.md` |
| **IE** | `docs/v2/contracts/product-v1/identity-and-evidence.md` |
| **IDS** | `docs/coop/design-corrections/foundation/identity-schemas.v3.json` |
| **ENP** | `docs/coop/design-corrections/foundation/enumeration-plan.schema.v1.json` |
| **EXC** / **EXS** | `docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md` / `execution-inputs.schema.v1.json` |
| **DSP** | `docs/coop/design-corrections/native/dispatch-binding.schema.v1.json` |
| **NCM** | `docs/coop/design-corrections/native/native-capability-matrix.v2.json` |
| **MC8** | `docs/implementation/m3/snapshot-plan-c/PROPOSAL-r8.md` (M3-C r8) |
| **FA2** | `docs/implementation/m3/native-successors-fa/fa-2/section-9-8.md` |
| **I1-E1** | draft erratum, branch `errata-2026-11-11-r1` @ `112aa8528`, `docs/implementation/m3/errata-2026-11-11/ERRATUM-I1-E1.md` (PROPOSED) |

## Subject and superseded selectors

A `plan2` Plan's `exec-plan2` stage is `{ordinal, stageSpecDigest, requires, outputDomains}` (IDS:819-866) and its stage
spec is `{schemaVersion, planId, producerClosure, operation, parameters, outputDomains, outputSchemaDigest}` (IE:1288-1290).
Neither carries a stage id, an operator, a provider id, a relation set, a budget or a universe. The TypeScript stage request
is still defined as a copy of a "C-2" stage (DLV:905, "`planDescriptorSchema.workflow`"), which no `plan2` Plan has.
MC8 item 16 specifies the syntax and inventory stages (MC8:993-1001) and is silent on the TypeScript provider stage.

**For a `plan2` Plan only**, this record replaces these selectors. Historical (C-2) Plans keep them unchanged.

| Selector | Text | Replaced by |
|---|---|---|
| DLV:719, :909 | `stageId` "exact C-2 stageId text" / "copy exact stage.stageId" | T4 |
| DLV:723, :913 | `dependsOn` from the C-2 stage | T5 |
| DLV:724, :914 | `relations` "equals this C-2 stage's relation set" / "copy … exactly" | T6 |
| DLV:896, :906, :898 (order and "copied exactly") | selection and order of C-2 stages | T3 |
| DLV:905 | `stageRequestProjection.sourceContract` | this record |
| NE:3026, :3031 | "exact C-2 **text**" | T4 |
| DSP:45, :81 | `expectedStageId` "Exact C-2 stageId text" | T4 |

It **adds** a third bullet to MC8 item 16 beside the syntax (MC8:993) and inventory (MC8:994-1001) stages: T1.

## Normative clauses

**T1. The stage.** `exec-plan2` has one `typescript-semantic` provider stage per selected TypeScript semantic universe U
that an available binding (ENP `AvailableProgramBindingV1`) of a requested cell binds, where that binding's
`enumerator.closureId` is the selected provider closure P.
- Its `producerClosure` is P.
- Its `operation` is `typescript.analyze`. It is one path segment (IE:1310-1311). P's interface defines it (IE:1327-1332).
- Its output schema is the document P's tree carries at `opensip-interface/stage-output/typescript.analyze.schema.json`,
  declaring `x-opensip-stage-output: {schemaVersion: 1, operation: "typescript.analyze", outputDomains: ["view"]}`
  (IE:1303-1318; IDS:3002-3014).
- Its `outputDomains` are `["view"]`. A producer stage returns views; a view carries its `facts` and `coverageIds`
  (IDS:726, `view` required members). Receipt `outputRefs` are the returned views (EXC:12, :18, :299); a fact must appear
  in a selected view of its producer on the receipt (NE:3122-3123). Facts, Coverage and target attribution are not
  separate stage output domains (EXC:268-270, :290).
- Its `parameters` are `[]`, as for the host inventory stages part a builds (B `crates/host/src/plan.rs:957-965`). Every
  row a stage cites must be an analysis-spec row (IE:1296-1298); citing none satisfies that. T2 states why nothing more is
  needed.
- Its `requires` is `[]`.
- **Order.** The P stages follow the stages part a already places before them and precede the host inventory stages
  (B `plan.rs:955-966` appends inventory stages after the request's stages). Among themselves they are in ascending
  byte order of U, the order in which part a builds one inventory stage per universe (a byte-keyed set,
  B `crates/plan-metered/src/plan_values.rs:16`, walked at `plan_compose.rs:357`). This order is the stage-to-universe map: the k-th P stage by
  ordinal serves the k-th such universe.
- **Binding.** Every available binding of U whose enumerator is P names this stage as its `stageOrdinal`, as MC8:993 and
  :999 state for the syntax and inventory stages. The Plan's binding record carries no stage field (ENP
  `AvailableProgramBindingV1`, `additionalProperties: false`); the naming is realized in the post-execution
  `CellProgramOutcomeV1.stageOrdinal` (EXS:428, :563-574; EXC:51).
- **Rejected placement.** No stage when no available binding names P; an unavailable binding has no universe and so no
  stage (MC8:1000).

**T2. No hidden input.** Every value T3-T8 project is a pure function of records the stage spec's `planId` commits, of
fixed law, and of the session's own verified values:
- the cells and bindings: the Plan's `EnumerationPlanV1`, an analysis-spec parameter row (MC8:923; IE:1508-1509;
  registry row IDS:4910-4918), committed through `plan.analysisSpecDigest`;
- the snapshot: `plan.snapshotId`;
- P: the stage spec's `producerClosure`, equal to every bound enumerator's `closureId` (FA2:27-28);
- U: the binding's `universe`, and the session's `OpenUniverse.universeKey`, which is its text spelling;
- the capability-to-relation table: NCM `capabilities[].relations`, fixed law, already used by Run closure for view
  attribution (EXC:53);
- `producerVersion`: the verified HelloAck `providerBuildId` (DLV:986).

IE:1296-1298 forbids a stage **parameter** that the analysis spec does not carry. The projection adds no parameter: it
reads only Plan-committed records through fixed law, exactly as the inventory stage, whose spec carries no universe and no
parameter, serves one universe's bindings (MC8:994-999). If a reviewer holds that the projected values must sit inside
`stageSpecDigest` itself, the lawful row is the existing `EnumerationPlanV1` parameter: the closed registry is keyed by
"analysis-spec/stage-spec parameter schemaDigest" and lists that document (IDS:4894-4918), and a stage may cite at most
one entry per row (IDS:4942). No new row is needed. This record does not cite it, because the stage spec's `planId`
already commits the same row and the two universes' specs would still be byte-identical.
**Weakest point:** NCM is not a Plan member. A matrix revision would change the projected relations under an unchanged
`planId`. The defence is that NCM is design-locked law, not an input, and Run closure already depends on it (EXC:53).

**T3. Selection and order.** A universe U's Analyze contains exactly the `exec-plan2` stages whose stage spec
`producerClosure` is P and which U's bindings name (T1), in ascending Plan ordinal. Under T1 that is exactly one stage.
One worker session and one Analyze serve one U. `StageRequestV1.stageOrdinal` stays the Analyze-relative position
(DLV:720, :910); it is never the Plan ordinal (NE:3027, :3042).

**T4. `stageId`.** For a `plan2` Plan, the stage id of the stage with Plan ordinal n is the ASCII text `stage-`
followed by n in decimal, with no sign and no leading zero (`stage-0`, `stage-17`). It is NFC and at most 26 scalars, inside
`StageIdText`'s 1..255 (B `schemas/sources/startup-v1.schema.json:142-147`; B `schemas/wire/native-carriers-v1.json:2407-2419`).
- It replaces "exact C-2 text" for `plan2` Plans.
- `DispatchBindingV1.expectedStageId` is the same function of the binding's `retainedStageOrdinal`.
- The host compares stage ids only for byte equality (DSP:81; NE:3039).
- Plan-stage lookup stays by `retainedStageOrdinal`, never by parsing the id (DSP:85; NE:3041-3042).
- The stage-spec digest is not used: two universes served by P have byte-identical stage specs under T1 (same `planId`,
  P, operation, `[]`, `["view"]`, schema digest), so the digest does not identify a stage.

**T5. `dependsOn`.** The T4 ids of the stage's `requires` ordinals whose stages are selected into the same Analyze,
sorted by UTF-8 bytes, not numerically (`stage-10` precedes `stage-9`; wire order `utf8-strict`, B
`native-carriers-v1.json:3184-3194`). None gives
the present empty array, as the wire encodes absence (DLV:723, :898; B `components/src/provider_protocol/ts2/send.rs:1185-1186`).
A `requires` ordinal outside this Analyze is not sent. It must have completed before the Analyze, or the host rejects the
Plan before spawn (DLV:897). The provider never needs it: it keeps an external id uninterpreted (F
`providers/typescript/src/data/analyze.ts:88-95`). Under T1, `requires` is `[]`, so `dependsOn` is `[]`.

**T6. `relations`.** The sorted unique set of the relations (first members of NCM `capabilities[].relations` pairs) of
the capability of every cell whose available binding names this stage. An empty set is a host-generated invalid spec
(MC8 item 17); it cannot arise, because T1 builds no stage without such a binding.
P's advertised interface admits only `imports` and `unresolved-edge`, and refuses a stage that requests `imports`
without `unresolved-edge` (F `providers/typescript/src/facts/admission.ts:26`, :68-69). Draft erratum I1-E1 makes the Plan
request the pair (I1-E1 §I1-E1.3, amendment 2) and refuses an `imports`-alone selection "at the point where the provider
request is built" (I1-E1 §I1-E1.3, C4-T13a). That point is this projection.

**T7. `budget`.** The request carries no stage budget input; DLV `budgetProjection.absent` applies, and the six values are P's
signed default profile (DLV:915, :923-928). The Plan-wide `plan.budget` never substitutes (DLV:936; MC8:929).

**T8. Requested coverage domain.** DLV `coverageDomain` (DLV:954-988) applies with these committed sources:
`relation` from T6; `resolution` the rung of that relation's NCM pair (DLV:963-970; NE §4.4, NE:601, for
`unresolved-edge@observed`); `sourceUniverseId` from T2's U; `targetUniverseId` by DLV:973-977 (see Open point O1);
`producerVersion` from T2. Each `symbol`-kind key carries FA-2's D∅ commitment (FA2:34-43) by NE §4.1a's recipe
(NE:1894-1915), with `enumeratorClosure` = P and `snapshotId` = `plan.snapshotId`. The census request is FA-2's
(FA2:34-36). This record restates neither recipe.

**T9. Owners.**
- The stage in `exec-plan2` (T1) and the retained stage records the projection reads: part a's step 16 (B `plan.rs`),
  changed in C4a-TS-b as one flagged commit.
- The binding-to-stage naming (T1, "Binding"): the existing builder of `ExecutionInputsV1`, unchanged in kind.
- The stage-output schema in P's tree: the provider closure. It changes P's `closure2` and every Plan that selects P
  (IE:1322-1325).
- The projection T3-T8 and the single request builder: C4a-TS-b, commit B7 (`LC/c4ats/PLAN-r5.md:312`, :402-403).
- The dispatch binding: its existing owner, changed only by T4.

## Open points (for review; not settled here)

- **O1. Cross-universe targets.** DLV:975 takes `imports` targets from "activated `PlanDescriptorV1.semanticUniverses`",
  a C-2 source, limited to one universe per provider (DLV:976). P admits only keys that target its own universe
  (F `admission.ts:71-73`). For M3-M-TS1 the only lawful target set is {U}. A `plan2` source for the general set is not
  settled here.
- **O2. Unadvertised relations.** A cell bound to P whose relation P does not advertise makes P refuse the whole Analyze
  (F `admission.ts:65-67`). Whether part b's token gating turns such a binding unavailable first is part b's (B2).

## Consequences

- Part a's code: one P stage per T1 universe in step 16; the projection's stage records retained beside
  `stage_spec_digests` (B `plan.rs:176-192` keeps only the digests).
- The provider closure ships `opensip-interface/stage-output/typescript.analyze.schema.json`, so P's `closure2`, every
  D∅ commitment and every golden value that depends on P change.
- C4a-TS-b B7 builds `StagePlan` (B `send.rs:107-117`) by T3-T8 only.
- No schema, registry, matrix or wire record changes. `StageIdText`'s description ("C-2 stageId text") is read as "stage
  id text" for `plan2` Plans; its shape is unchanged.

## Rejected alternatives

- **Admit a C-2 PlanIntent workflow, as DLV:905 literally says.** No unit admits one and no owner exists; it needs a
  second stage graph and a rule equating it with `exec-plan2`. It is the largest change and adds an input the Plan
  does not commit.
- **A stage id from the stage-spec digest.** Two universes served by P have byte-identical stage specs (T4), so the id
  would not identify the stage.
- **Relations in a new stage parameter row.** The parameter registry is closed (IDS:4929); a new row is a versioned
  correction for a value the Plan's `EnumerationPlanV1` already commits (T2).
- **Leaving the projection to a later unit.** C4a-TS-b's accepted plan commits it to the projection and the first
  production request (`LC/c4ats/PLAN-r5.md:312`, :402-403); with no projection there is no production Run.
