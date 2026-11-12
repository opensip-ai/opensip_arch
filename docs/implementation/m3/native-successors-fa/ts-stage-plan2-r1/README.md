# TS-STAGE-PLAN2 — the `typescript-semantic` provider stage in `exec-plan2` and the stage-request projection for a `plan2` Plan

2026-11-11. Drafted by a lead-dispatched design author (Claude Opus 5.5, route R2-DEEP) from the lead's rulings on gap Q14.
Status: **PROPOSED, r5.** r2 applied the lead's rulings on r1's open questions. r3 applied the lead's rulings on the
independent review of r2 (`review-opus/VERDICT.md`: R1-R5, A1-A6). r4 applied the rulings on its re-check
(`review-opus/VERDICT-r3.md`: N1, A7-A9). r5 applies lead decision LD-DEC-3
(`lead-2026-10-25/decisions/LD-DEC-3-multi-provider-run/DECISION.md`, "Decided", item 1). It adds a scope fence (Plans
with any other semantic provider's stage are refused under this record), states T3's "exactly one stage per Analyze"
as a property of the TypeScript protocol, adds the short name RPP, and adds the non-binding open point O4 on what a
successor for mixed Plans must satisfy. Reason: no rule for mixed Plans can be stated correctly before the Rust
provider's `plan2` stage shape exists, and the order clause must not read as binding on other providers. r5 changes
no order, stage id, key, byte or golden for a Plan whose provider stages are all the TypeScript provider's. The
directory name is kept. It needs a
cross-vendor review, then adoption by the lead. It binds nothing, changes no existing file, registry, inventory or lock, and
has no subject manifest yet.

**Scope.** TypeScript only, milestone M3-M-TS1. The Rust provider (`rust-semantic`) has the same gap
(`rust-provider-protocol.v2.json:222`, "exact C-2 value"; X-RL-C2, `rust3-lim/README.md:376`) and is out of scope.

**Scope fence (normative, r5).** This record governs `plan2` Plans whose provider stages are all the TypeScript
provider's, that is, whose every provider stage has `producerClosure` P (T1). Here a provider stage is an `exec-plan2`
stage whose `producerClosure` is a semantic provider closure other than the core provider closure; the core closure's
syntax and host inventory stages (MC8:993-1001) are not provider stages and keep their own law. A `plan2` Plan that
contains any other provider's stage is invalid under this record and is refused before spawn, as a host-generated
invalid Plan (MC8 item 17), until a successor record states the rule for mixed Plans. For such a Plan, T1's order and
map, T3 and T4-T8 bind nothing.
- **It matches the product today.** The Rust path fails closed before any Plan exists: a required Rust tuple, with a
  trust view admitted, falls under the C4ATS-GATE-RUST-ORCH or X-8 gate, "No Plan, no generic refusal" (B
  `crates/plan-priced/src/plan_domain.rs:1-16`, `domain_gate` :17-56, called at B `crates/host/src/plan.rs:896-901`; pinned
  for a Rust `inventory` tuple by B `crates/host/src/plan_tests.rs:3637-3654`). The fence makes this limit law, not an
  accident of the code.
- **Control.** A test that a Plan whose stages include a provider stage with a `producerClosure` other than P is refused
  before spawn, owned with T3's fail-closed counts (C4a-TS-b B7, T9).

## Short names

Base: architecture main `3e4203f0f`. Product citations: worktree `opensip-c4ats-b` at `1274eb86` (**B**); its B2 gating and
pairing code at the branch head `3450957f` (**B'**); provider worktree `opensip-f2min` at `e526e873` (**F**).

| Name | Document |
|---|---|
| **DLV** | `docs/coop/artifacts/delivery.v2.json` |
| **NE** | `docs/v2/contracts/product-v1/native-evidence.md` |
| **IE** | `docs/v2/contracts/product-v1/identity-and-evidence.md` |
| **IDS** | `docs/coop/design-corrections/foundation/identity-schemas.v3.json` |
| **ENP** | `docs/coop/design-corrections/foundation/enumeration-plan.schema.v1.json` |
| **EXC** / **EXS** | `docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md` / `execution-inputs.schema.v1.json` |
| **DSP** | `docs/coop/design-corrections/native/dispatch-binding.schema.v1.json` |
| **NCM** | `docs/coop/design-corrections/native/native-capability-matrix.v2.json`, design-locked at `docs/v2/architecture/implementation-normative-inputs.v13.json:50-51` (sha256 `4b1c19b0…`) |
| **MC8** | `docs/implementation/m3/snapshot-plan-c/PROPOSAL-r8.md` (M3-C r8) |
| **FA2** | `docs/implementation/m3/native-successors-fa/fa-2/section-9-8.md` |
| **RPP** | `docs/coop/artifacts/rust-provider-protocol.v2.json` (the Rust provider's protocol) |
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
| DLV:724, :914 | `relations` "exists in live fact-plane relationRegistry and equals this C-2 stage's relation set" / "copy … exactly" | T6 |
| DLV:896, :906, :898 (order and "copied exactly") | selection and order of C-2 stages | T3 |
| DLV:905 | `stageRequestProjection.sourceContract` | this record |
| DLV:963-971 | `relationResolutionById` (no `unresolved-edge`) and `relationSource` ("the signed install-profile capability manifest") | T6 "Source" |
| DLV:975-977 | cross-universe targets from "activated `PlanDescriptorV1.semanticUniverses`", "unique by providerId", at most 2 | T8 "Targets" |
| NE:3026, :3031 | "exact C-2 **text**" | T4 |
| EXC:276 | `FactBatch.stageId` "echoes the current requested C-2 stageId text" | T4 |
| DSP:45, :81 | `expectedStageId` "Exact C-2 stageId text" | T4 |

It **adds** a third bullet to MC8 item 16 beside the syntax (MC8:993) and inventory (MC8:994-1001) stages: T1.

## Normative clauses

**T1. The stage.** A **relation-bearing P binding** is an available binding (ENP `AvailableProgramBindingV1`) of a requested
cell whose `enumerator.closureId` is the selected provider closure P and whose capability has at least one relation pair in
NCM `capabilities[].relations`. Its `universe` is a **T1 universe**. `exec-plan2` has one `typescript-semantic` provider
stage per T1 universe U.
- **Candidate-only capabilities.** A candidate-only capability has no relation pair in NCM (today `clones-near` and
  `clones-cross-tsjs`, NCM `relations: []`). Until a design record gives one a producing stage, a binding of such a
  capability whose enumerator would be P is **unavailable**, with `enumerator` `{status: "selected", closureId: P}`,
  `universe` null, no `candidateSourcePaths`, and the pair `provider-unavailable` / `capability-missing`. Part b's gating (C4a-TS-b B2) decides this
  before any stage is built or anything is spawned. Reason: P's admitted interface advertises nothing that produces a
  candidate envelope, and "available" would promise an outcome no stage can deliver. An available binding with non-null U
  owes a non-null `stageOrdinal` matching a receipt (EXC:51), and a selected U "cannot become complete by omitting the stage
  and views" (EXC:55). The unavailable binding is a lawful Plan leg: ENC:51 and :53 admit an unavailable binding with the
  selected enumerator shape and a lawful `DeficiencyV2`/`nativeCause` pair; NCM:176 gives `provider-unavailable` /
  `capability-missing` as the applicable pair where nothing more specific applies, and says a candidate-only capability has
  no Coverage entry, its absence account being the selection record itself; NE:2848-2851 gives the same pair to work a
  selected row cannot serve. Such a binding names no stage. O3 stays open for the later producer.
- Its `producerClosure` is P. Its `operation` is `typescript.analyze`, one path segment (IE:1310-1311), defined by P's
  interface (IE:1327-1332).
- **Registration.** P's tree carries `opensip-interface/stage-output/typescript.analyze.schema.json`: a JSON Schema 2020-12
  document declaring `x-opensip-stage-output: {schemaVersion: 1, operation: "typescript.analyze", outputDomains: ["view"]}`
  (IE:1303-1318; IDS:3002-3014). Its body follows the owner fixture's precedent, the `derive-semantic-view` stage-output
  body (product `crates/evaluator/tests/fixtures/cycle-representative.current.v1.json`, `retainedBlobPool/449de99f…`): an
  object with one required member `viewId` whose pattern is the `view2` id form `^view2:[0-9a-f]{64}(?![\s\S])`, and
  `additionalProperties: false`. The body states what the stage returns, a view reference, and nothing about the view's
  contents, which IDS owns (`#/$defs/view`, IDS:726). It is not a `$ref`: nothing resolves one, and P's closure would not
  carry its target (O2).
- Its `outputDomains` are `["view"]`. A view carries its `facts` and `coverageIds` (IDS:726). Receipt `outputRefs` are the
  returned views and Coverage is reached through their `coverageIds` (EXC:12, :18-19, :299); "View-only stages stay
  `outputDomains: ["view"]`" (EXC:290); a fact must appear in a selected view of its producer on the receipt (NE:3122-3123).
- Its `parameters` are `[]`, as for the host inventory stages (MC8:997; B `crates/host/src/plan.rs:957-965`). Its
  `requires` is `[]`.
- **The stage map (one function).** The P stages follow the stages part a already places before them and precede the host
  inventory stages (B `plan.rs:955-966`). The k-th stage by ordinal whose spec `producerClosure` is P serves the k-th T1
  universe in byte order of U. Universe ids are 64-hex (ENP:371-373), so this order is total; it is the order part a builds
  inventory stages in (a byte-keyed set, B `crates/plan-metered/src/plan_values.rs:16`, walked at `plan_compose.rs:357`).
  This map is **one pure function**. Step 16 uses it to build the stages, the projection (T3) uses it to select, and the
  builder of `ExecutionInputsV1` uses it for `stageOrdinal`. It is stated nowhere else.
- **Standing of the map.** The Plan commits the map only through this order rule: no stage spec names a universe, and no
  binding names a stage (ENP `AvailableProgramBindingV1` is closed). It is a **builder invariant**. This record adds no
  Run-closure check and no refusal for it. Replay does not verify the map: a host that permuted it would pass every existing
  check (EXC:51 checks only that a binding's `stageOrdinal` matches a receipt, and every P spec is byte-identical, T4). Facts
  and Coverage stay bound to their universes through their own scope records (`sourceUniverse` on facts and on every
  subject scope a view names, EXC:53), whatever the stage label. The host inventory stages have had exactly this standing
  since MC8 r8 (MC8:994-999).
- Every relation-bearing P binding of U names U's stage; its post-execution `CellProgramOutcomeV1.stageOrdinal` (EXS:428,
  :563-574) is the map's value, written by the `ExecutionInputsV1` builder through the shared function.
- No stage exists for a universe with no relation-bearing P binding. An unavailable binding has no universe (MC8:1000).

**T2. No hidden input.** Every value T3-T8 project is a pure function of records the stage spec's `planId` commits, of
fixed law, and of the session's own verified values:
- the cells and bindings: the Plan's `EnumerationPlanV1`, an analysis-spec parameter row (MC8:923; IE:1508-1509;
  registry row IDS:4910-4918), committed through `plan.analysisSpecDigest`;
- the snapshot: `plan.snapshotId`;
- P: the stage spec's `producerClosure`, equal to every bound enumerator's `closureId` (FA2:27-28);
- U: the binding's `universe`, bare 64-hex (ENP:371-373). The wire spells it `sha256:` + the same hex (`OpenUniverse.universeKey`,
  `Ts2Sha256Text`, B `schemas/wire/native-carriers-v1.json:2383-2388`, :3621-3625);
- the capability-to-relation@rung table: NCM, design-locked law (T6 "Source");
- whether P serves a relation: P's admitted protocol row (T6 "Source");
- `producerVersion`: the verified HelloAck `providerBuildId` (DLV:986).

IE:1296-1298 forbids a stage **parameter** that the analysis spec does not carry; `[]` is a subset of the analysis-spec rows.
The projection adds no parameter: it reads only Plan-committed records through fixed law, as the inventory stage serves one
universe's bindings with no universe and no parameter in its spec (MC8:994-999). If a reviewer holds that the projected
values must sit inside `stageSpecDigest` itself, the lawful row is the existing `EnumerationPlanV1` parameter: the closed
registry is keyed by "analysis-spec/stage-spec parameter schemaDigest" and lists that document (IDS:4894-4918), at most one
entry per row (IDS:4931). No new row is needed. This record does not cite it. The stage spec's `planId` already commits the
row, and the specs of two universes would still be byte-identical. Citing it would also assert that P's interface takes
that document as a stage parameter, which is false on the wire: the worker receives the projected request, never the
`EnumerationPlanV1`.
**Weakest point:** NCM is not a Plan member. A matrix revision would change the projected relations under an unchanged
`planId`. The source this record replaces, DLV:971's signed install-profile capability manifest, was committed by the Plan
through `capabilityManifestId`; NCM is not, and is pinned by the design lock only. It is chosen because DLV's map has no
`unresolved-edge` (DLV:963-970) and the manifest has no producer for this request. The defence is that NCM is design-locked
law, not an input, and Run closure already depends on it (EXC:53).

**T3. Selection and order.** A universe U's Analyze contains exactly the stage the T1 map assigns to U. One worker
session and one Analyze serve one U. **Fail closed:** the number of Plan stages whose spec `producerClosure` is P must
equal the number of T1 universes, and each Analyze must contain exactly one stage. Any other count is a host-generated
invalid Plan (MC8 item 17), refused before spawn. "Exactly one stage per Analyze" is a property of the TypeScript
provider's protocol under this record, not of execution plans in general: the Rust provider's protocol puts "every
selected stage in exact verified ExecutionPlan order" into one Analyze (RPP:409; selection at RPP:222).
`StageRequestV1.stageOrdinal` stays the Analyze-relative position
(DLV:720, :910); it is never the Plan ordinal (NE:3027, :3042). `operator` (`semantic-provider`) and `providerId`
(`typescript-semantic`) are wire constants (DLV:721-722) and need no Plan source.

**T4. `stageId`.** For a `plan2` Plan, the stage id of the stage with Plan ordinal n is the ASCII text `stage-`
followed by n in decimal, with no sign and no leading zero (`stage-0`, `stage-17`). It is NFC and at most 26 scalars,
inside `StageIdText`'s 1..255 (B `schemas/sources/startup-v1.schema.json:142-147`; B `native-carriers-v1.json:2407-2419`).
One generic prefix serves every provider.
- It replaces "exact C-2 text" for `plan2` Plans.
- `DispatchBindingV1.expectedStageId` is the same function of the binding's `retainedStageOrdinal`.
- The host compares stage ids only for byte equality (DSP:81; NE:3039).
- Plan-stage lookup stays by `retainedStageOrdinal`, never by parsing the id (DSP:85; NE:3041-3042).
- The stage-spec digest is not used: two universes served by P have byte-identical stage specs (same `planId`, P,
  operation, `[]`, `["view"]`, schema digest), so the digest does not identify a stage. Identical specs are otherwise safe:
  a `cache-key` also commits `scopeIds`, which carry `sourceUniverse` (IDS `cache-key` required members), C4 mints no
  `cache2` (MC8:1003), `exec-plan2` stages stay unique by `ordinal` (IDS:870), and the inventory stages already have
  identical specs per universe.

**T5. `dependsOn`.** The T4 ids of the stage's `requires` ordinals whose stages are selected into the same Analyze,
sorted by UTF-8 bytes, not numerically (`stage-10` precedes `stage-9`; wire order `utf8-strict`, B
`native-carriers-v1.json:3184-3194`). None gives the present empty array, as the wire encodes absence (DLV:723, :898;
B `components/src/provider_protocol/ts2/send.rs:1185-1186`). A `requires` ordinal outside this Analyze is not sent. It must
have completed before the Analyze, or the host rejects the Plan before spawn (DLV:897). The provider never needs it: it
keeps an external id uninterpreted (F `providers/typescript/src/data/analyze.ts:88-95`). Under T1, `requires` is `[]`, so
`dependsOn` is `[]`.

**T6. `relations`.** The sorted unique set of the relations (first members of NCM pairs) of the capability of every
relation-bearing P binding of U.
- **Non-empty by construction.** T1 builds no stage for a universe with no relation-bearing binding, so the set is
  non-empty. An empty set that reaches the projection is a host-generated invalid Plan (MC8 item 17), refused before spawn.
- **Source.** For a `plan2` Plan the capability-to-relation@rung map is NCM (design-locked; Run closure already reads it,
  EXC:53), not DLV:963-971's map and manifest. `unresolved-edge@observed` is NE §4.4's (NE:601, NE:2187). Whether P serves a
  relation is decided from P's **admitted protocol row** (its `typescript-semantic.<relation>` capability rows, and the
  `unresolved-edge-v1` token for `unresolved-edge`; B' `crates/host/src/plan_gate.rs` `RELATION_ROWS`, `rows_of`,
  `relation_served`), never from the worker's source.
- **Availability decides first; the projection never filters.** Part b's gating (C4a-TS-b B2) makes a binding whose relation
  P's row does not serve unavailable (`capability-missing`, NE:2851) before any stage is built, so it names no stage. A
  relation P's row does not serve that still reaches the projection is a host-generated invalid Plan, refused before spawn.
- **Pairing.** A relation set that contains `imports` and not `unresolved-edge` is a host-generated invalid spec (MC8 item
  17: 4 / `SYSTEM.OUTCOME.ILLEGAL_STATE`), refused before any spawn; the host never adds a relation to an admitted spec
  (lead ruling Q3, as B' `crates/host/src/plan_pairing.rs:1-10` implements it). The provider refuses the same stage
  (F `providers/typescript/src/facts/admission.ts:68-69`). Draft erratum I1-E1 agrees (§I1-E1.3, C4-T13a).

**T7. `budget`.** The request carries no stage budget input; DLV `budgetProjection.absent` applies, and the six values are
P's signed default profile (DLV:915, :923-928). The Plan-wide `plan.budget` never substitutes (DLV:936; MC8:929).

**T8. Requested coverage domain.** DLV `coverageDomain` (DLV:954-988) applies with these committed sources:
`relation` from T6; `resolution` the rung of that relation's NCM pair (T6 "Source"); `sourceUniverseId` from T2's U;
`producerVersion` from T2.
- **Targets.** For a `plan2` Plan under this record the target universe set of every requested key is {U}, for an
  intra-universe and a cross-universe relation alike. P admits no other target (F `admission.ts:71-73`). Therefore **not
  requested**: `imports` targets in another TypeScript universe of the same Plan, or in any other semantic universe. No key
  exists for them, so no Coverage states anything about them; nothing about them is `complete`, and a consumer reads them
  as unknown, never complete (RC-2 states completeness per Coverage entry, NE:2113-2117).
- Each `symbol`-kind key carries FA-2's D∅ commitment (FA2:34-43) by NE §4.1a's recipe (NE:1894-1915), with
  `enumeratorClosure` = P and `snapshotId` = `plan.snapshotId`. The census request is FA-2's (FA2:34-36). This record
  restates neither recipe.

**T9. Owners.**
- **Step 16 (T1) is C4a-TS-a's** (`LC/c4ats/PLAN-r5.md:306`, "C4a-TS-a builds the stage set at step 16"). The change is a
  written delta to part a's plan, reviewed as a change to part a by C4a-TS-b's independent reviewer in the same review (one
  review per change), as the Q4 precedent was. The T1 map function lives there and is shared.
- **The provider schema file, the packager `tools/typescript_closure.py` and `providers/typescript/closure/closure-expected.v1.json`:
  F2-min repackaging**, the provider closure repackaging step already owed after F2-min (`LC/f2min/CLOSURE-REPACKAGING.md`).
  It changes P's `closure2` and every Plan that selects P (IE:1322-1325).
- **The projection T3-T8 and the single request builder:** C4a-TS-b, commit B7 (`LC/c4ats/PLAN-r5.md:312`, :402-403).
- **The dispatch binding:** its existing owner, changed only by T4.
- **`ExecutionInputsV1.stageOrdinal` for TypeScript bindings:** carry (Consequences).

## What this record does not do

- It adds no schema, registry row, wire field, Plan member, Run-closure check or refusal code.
- It does not cover the Rust provider.
- It does not settle cross-universe targets in general (O1).
- It does not define a producer for candidate-only capabilities at TypeScript modes (O3); it makes their P bindings
  unavailable (T1).
- It does not assign the `ExecutionInputsV1` builder.

## Open points (for review; not settled here)

- **O1. Cross-universe targets in general.** DLV:975-977 take `imports` targets from a C-2 source limited to one universe
  per provider. A `plan2` source for targets beyond {U} needs a P that admits them and a later successor.
- **O2. The output-schema body (T1, "Registration").** The `viewId` body and the refusal of a `$ref` or a copy of the view
  definition are a lead choice that reviewers may overturn.
- **O3. A producer for candidate-only capabilities at TypeScript modes.** Under T1 such a binding is unavailable until a
  design record gives the capability a producing stage (B `plan.rs:1620-1621`: every non-`inventory` cell's enumerator is
  P; B `crates/plan-metered/src/plan_inputs.rs:335`: no kinds). Which stage, producer and envelope that record names is not
  settled here. The default configuration requests both capabilities (B `crates/host/src/configuration_vectors.json:76-77`,
  case `zero-project-config-mixed-native-default`), so until then every default-configuration Run discloses them as
  unavailable.
- **O4. What a successor for mixed Plans must satisfy (r5; NON-BINDING).** This point binds nothing and states no order
  rule for mixed Plans. It records constraints a successor must meet (LD-DEC-3):
  - (i) On a Plan with one provider it reduces exactly to this record's order and ids (T1, T3, T4).
  - (ii) The stage map's key distinguishes stages by more than the producer closure. The core provider closure produces
    two kinds of stage: the syntax stage ("that stage's `producerClosure` is the core provider closure", MC8:993) and the
    host inventory stage ("Its `producerClosure` is the core provider closure", MC8:995). C4-T22's fixture has both in
    one Plan (MC8:1044-1047).
  - (iii) The Run-closure check of the stage ordinal (Consequences, "Erratum candidate"; today EXC:51 checks only a
    matching receipt) covers every provider family and is adopted before the first mixed Plan is committed. Stage order
    becomes durable through the execution plan, not the Plan record: `plan` has no execution-plan member (IDS:456-473),
    `evaluation-seal` requires `executionPlanId` (IDS:1416-1422) and `run` requires `evaluationSealId` (IDS:1474-1483).
  - (iv) The Rust provider's stage grouping is fixed with that provider's own record, after its owed measurements. Its
    protocol selects stages by the C-2 `providerId` (RPP:222), puts every selected stage into one Analyze (RPP:409),
    takes each stage's relations from that stage (RPP:234), and assumes one Rust row (RPP:225). The measurements are
    owed by RUST3-LIM: "What S-M must measure" (`rust3-lim/README.md:310`, SM-13 and SM-14 at :320-321), and the Rust
    stage budget X-RL-C2 is due "C4a, after S-M" (:376).

## Consequences

- **Part a (C4a-TS-a, by the T9 delta):** one P stage per T1 universe in step 16 through the shared T1 map; the stage
  records the projection reads retained beside `stage_spec_digests` (B `plan.rs:176-192` keeps only the digests); the test
  value `output_domains: vec!["fact".into()]` at B `crates/host/src/plan_tests.rs:634` becomes `["view"]`.
- **Part b's gating (C4a-TS-b B2), a flagged change:** a candidate-only capability at a TypeScript mode binds
  `provider-unavailable` / `capability-missing` (T1), where today B' `plan_gate.rs` `serves` passes it on the identity and
  native-context tokens alone. Control: a default-configuration request yields the `clones-near` and `clones-cross-tsjs`
  bindings unavailable with that pair and exactly the relation-bearing P stage.
- **F2-min repackaging:** ships `opensip-interface/stage-output/typescript.analyze.schema.json` in P's tree (packager
  `tools/typescript_closure.py`, F :412-430), and regenerates `closure-expected.v1.json`. P's `closure2`, every D∅
  commitment and every value that depends on P change. `LC/f2min/CLOSURE-REPACKAGING.md` is prepared, not performed, and
  lists neither change. It must be amended to add (1) the schema file under `providers/typescript/`, landing before its
  frozen provider commit `C` (the last change under `providers/typescript/`), and (2) the packager change that places that
  file at the `opensip-interface/` path in P's tree, as its own step.
- **Copies of the capability-to-relation table:** the product embeds two, B `crates/evaluator/src/execution-registry.json`
  (`capabilities[].relations`; read by part b's projection, pinned by `the_relation_projection_is_the_registrys`, B'
  `crates/host/src/plan_pairing_tests.rs:30`) and B `crates/host/src/native_capability_matrix.v2.json` (the embedded NCM).
  Each needs an equality control against the locked NCM (`implementation-normative-inputs.v13.json:50-51`), member by
  member for the relation table, owned by the unit that reads the copy (part b for `execution-registry.json`).
- **Golden sessions:** the TS2 golden sessions (B and F `crates/host/src/typescript_nss_f1_vectors_tests.rs`, F :508-519, and
  `crates/host/src/launch_recheck_ts2_fixture.rs`) change `"stage-one"` to `"stage-0"`, regenerated by their own generator.
- **C4a-TS-b B7** builds `StagePlan` (B `send.rs:107-117`) by T3-T8 only, through the shared T1 map and the T4 function.
- **Carry:** `ExecutionInputsV1.stageOrdinal` for TypeScript bindings is owned by the builder of `ExecutionInputsV1`, not
  yet assigned to a unit (H5-TS / J2b-TS). It must use the shared T1 map function.
- **Erratum candidate (a later record):** a Run-closure check, in the execution-inputs contract (EXC §3) and its reference
  model (`execution_inputs_model.v1.py`), that a binding's `stageOrdinal` equals the map for every family of per-universe
  stages with byte-identical specs: the host inventory stages and the TypeScript provider stages together.
- **Description text only, to be corrected with the next revision of those schemas:** B
  `schemas/sources/startup-v1.schema.json:146` (`StageIdText`, "C-2 stageId text") and B `schemas/wire/native-carriers-v1.json:6985`
  ("stageId is C-2 text (StageIdText)"). Their shape is unchanged; for a `plan2` Plan the text is T4's.

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
