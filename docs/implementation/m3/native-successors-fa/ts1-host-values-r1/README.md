# TS1-HOST-VALUES — owners and lawful sources for the values the first TypeScript Run needs and nobody produces

2026-11-11. Drafted by a lead-dispatched design author (Claude Opus 5.5, route R2-DEEP) from the E2E gap inventory
(`LC/coordinator/E2E-GAP-INVENTORY-2026-11-11.md` §2, §3 G2-G4, G6, G7).
Status: **PROPOSED, r7.** History: r2 applied the lead's rulings on r1 and added V7; r3 closed O5; r4 applied an
independent review (`LC/ts1-host-values/review-opus/VERDICT.md`, R1-R6, A1-A8); r5 applied the lead's rulings on r4's open
items (V3's `syntax-all`; V8's carrier); r6 closed the V7 implementer's gaps (H5-TS Q-J, Q-K); r7 applies the r6 re-check
(`review-opus/VERDICT-r6.md`): one internal key on an existing route (R-1), a budget cut gives `unknown` / `budget-exhausted`
and only a manifest parse failure refuses, as a stated TS1 limit (R-2), five LD8-3 selectors superseded, led by the textual
reason (R-3), and V7's basis made non-normative. It needs a cross-vendor review, then adoption by the lead. It
binds nothing, changes no existing file, registry, inventory or lock, and has no subject manifest yet.

**Scope.** Milestone M3-M-TS1: a synthetic-trust Run (OD-SIGN-2 (A)) driven through `opensip_host::invocation::run` by host
tests or the harness (MJ item 1; PA1 §1.5, §6). Each clause says whether its rule can stand for a released product
(**release**) or is TS1-only (**TS1**). Marks: **SETTLED-BY-TEXT** (only an owner was missing), **PROPOSED** (new law,
needs review), **OPEN** (a named decision is needed).

## Short names

Base: architecture main `3e4203f0f`. Product: main `ff93e4c6` (paths without prefix); **B** = `opensip-c4ats-b` @ `3450957f`;
**H** = `opensip-h1` @ `3bb78e1b`; **F** = `opensip-f2min` @ `e526e873`. `LC` = `.opensip-implementation-cache/lead-2026-10-25`.

| Name | Document |
|---|---|
| **DLV** / **DLV4** | `docs/coop/artifacts/delivery.v2.json` / `delivery.v4.json` (standing: see "delivery.v4" below) |
| **RI** / **C2S** | `docs/coop/artifacts/resolved-inputs.v2.json` / `c2-plan-stage-schema.v3.json` |
| **NE** / **IE** / **AQ** | `docs/v2/contracts/product-v1/` `native-evidence.md` / `identity-and-evidence.md` / `admission-and-qualification.md` |
| **IDS** / **DSP** | `docs/coop/design-corrections/foundation/identity-schemas.v3.json` / `native/dispatch-binding.schema.v1.json` |
| **NCM** / **CMD2** | `docs/coop/design-corrections/native/` `native-capability-matrix.v2.json` / `capability-manifest-domains.v2.json` |
| **COMP** / **EXC** / **ENC** | `docs/coop/design-corrections/foundation/` `evaluator-composition-contract.v3.md` / `execution-inputs-contract.v1.md` / `enumeration-contract.v1.md` |
| **MC8** / **MH** / **MJ** / **MD** | `docs/implementation/m3/` `snapshot-plan-c/PROPOSAL-r8.md` / `fact-admission-h/PROPOSAL-r3.md` / `host-pipeline-j/PROPOSAL-r5.md` / `supervisor-d/PROPOSAL-r5.md` |
| **ME** / **I1** / **D2B** | `docs/implementation/m3/` `syntax-e/PROPOSAL-r3.md` (accepted) / `preview-pack-i1/PROPOSAL.md` / `supervisor-d/d2b/PLAN-r3.md` (with `PLAN-r3-A2.md`) |
| **TSP2** | TS-STAGE-PLAN2 r4, branch `ts-stage-plan2-r1` @ `deef8c4f1` (PROPOSED) |
| **PA1** / **PLAN5** / **H5S** / **J3S** / **Q13** | `LC/pa1/PLAN-AMENDMENT-TS1-r3.md` / `LC/c4ats/PLAN-r5.md` / `LC/h5-ts/SCOPE-r1.md` / `LC/j3d-ts/SCOPE-r1.md` / `LC/c4ats/b-r1/QUESTIONS.md` |

**delivery.v4.** Its own header reads `"status": "CANDIDATE"`, `"applicationState": "NOT APPLIED"` (DLV4:6-7). The
distribution brief lists it as "applied 2026-08-05" (`docs/OPENSIP-DISTRIBUTION-AND-COMPONENT-TRANSITION-BRIEF.md:43`), the
blueprint as the DELIVERY head (`docs/coop/IMPLEMENTER-BLUEPRINT.md:205`), and the native source pins name its bytes
(`docs/coop/design-corrections/native/source-pins.v2.json:54-55`); all three pin SHA-256 `3cffece0…`, the digest of the file
carrying that header. The record relies on the applied listing. Independently, IE §3 selects CMD2 as the current successor
of DLV4's value domains (IE:236-246; CMD2:5), so the manifest's admission law does not rest on the header alone.

## Subject

| Value | Consumed at | What the texts give |
|---|---|---|
| `hostBuildId` | `components/.../ts2/send.rs:124`, `:897`; B `host/src/plan_ts2.rs:598-607` | shape only (NE:2958; DLV:846) |
| `planIntentCommitment` | `send.rs:138`, `:949`; B `plan_ts2.rs:638` (`&str`) | a C-2 PlanIntent commitment (DLV:847; RI:792-795); NE:3159 "keep their owners" |
| capability manifest id, bytes digest, content | `host/src/plan.rs:143-144`, `:403-404`; `evaluator/src/plan_capability.rs:45-80` | "the committed CVE1 artifact" (IE:224-235; MC8:921); content: nothing |
| inventory operation, schema, core tree | `plan.rs:706`, `:888`, `:1161` | MC8:998; X-9 (MC8:1271) |
| `semanticGrantDigest` | `plan.rs:149`, `:410`; `evaluator/src/run_links.rs:332-360` | IE:525-539; MC8:930-932 |
| `DispatchContext`, `DispatchBindingV1` | `ts2.rs:127-129`; `session_factory.rs:97-109`; H `fact_admission/occupancy.rs:69-81` | NE:3023-3044; DSP; D2B:142 |
| inventory stage Coverage | H `fact_admission/inventory.rs`; `evaluator/src/view_joins.rs:500-531` | MH:440 vs MH:649; H5S:109-115 |
| requested capabilities of the milestone Run | `host/src/discovery.rs:1212-1272` | NE:1080-1092, :1183-1189; PA1:256-257; J3S:155-160 |

It **extends** MC8 item 16 (V4, V5), NE §9.7 (V2), D2B LD-D2B-15 (V6) and MH item 18 (V7). For `plan2` Runs only it
**supersedes** the `planIntentCommitment` selectors V2 lists, D2B:142's and `ts2.rs:127-128`'s "built by D4's session
factory" (V6), lead ruling Q13 item 1's "no production producer" (V1), the seven MH sentences V7 lists, and LD8-3's
statements of the `vcs-change` entry (MC8:42, :56, :331, :332, :1271; V7). Historical
C-2 Plans keep every selector unchanged.

## Normative clauses

**V1. `hostBuildId`. PROPOSED (TS1); release OPEN (O3).** No text ties it to a release identity: it is only a Hello
member (NE:2817-2819, :2958; DLV:846), enters no identity or retained record, and the worker checks only its shape. The
compiled release identity is `hostRelease`, taken "solely from the CLI's `env!("CARGO_PKG_VERSION")`"
(`docs/implementation/m1/metadata-v2/README.md:93-94`; `host/src/outcomes.rs:280-281`).
- **Rule.** One constant in `opensip-host`: `HOST_BUILD_ID = concat!("opensip-host ", env!("CARGO_PKG_VERSION"))`, with
  `HostBuildId::current()` its only production constructor and `HostBuildId::new` test-only. No other spelling exists.
- **Supersedes** lead ruling Q13 item 1 (Q13:476-479; B `plan_ts2.rs:598-600`), under which C4a-TS-b mints no host build id
  and takes it as an argument "typed by its owner when one exists". The type `HostBuildId` stays; this record names its one
  production value.
- **Weakest point.** `opensip-host` and `opensip-cli` are both `0.1.0` by coincidence. Nothing retains the value, so it is
  production code but no release commitment.

**V2. `planIntentCommitment` for a `plan2` Run. PROPOSED (TS1); release OPEN (O2).** By the texts it commits the C-2
PlanIntent, frozen at request validation *before* attempt admission and stored with the ExecutionId (RI:794; C2S:550-567;
RI:668). No `plan2` record is that PlanIntent: the product `AttemptRecord` is `{store, namespace, execution, operation,
phase}` (`storage/src/commit.rs:352-361`); `CommitSession::open` binds no intent (`security/src/custody/commit_session.rs:379-447`);
MJ, MC8 and MH never name it. In MJ's order the ExecutionId is drawn at R12 (MJ:351) and the PlanId is minted at J-ε (MJ:398-399).
- **Use.** The worker checks its closed shape only (F `src/generated/protocol.ts:616`, through `closedCheck`, F
  `src/data/machine.ts:199`); the host receiver never reads it; UniverseAccepted does not echo it (DLV:849). It is sent,
  shape-checked and discarded. Nothing durable stores it, so a later change of recipe breaks only test goldens.
- **Rule.** `planIntentCommitment` = `sha256:` + hex(SHA-256(UTF8(`opensip.plan2-intent.v1`) ‖ 00 ‖ UTF8(plan2 text))),
  one pure function in `opensip-identity` beside `plan_intent_preimage` (`identity/src/digests.rs:115`) returning a
  `PlanIntentCommitment` newtype, the only value `Owners` accepts. Stored nowhere; recomputed from the verified Plan. A text
  not matching `^plan2:[0-9a-f]{64}$` yields none, refused as a host invariant before spawn.
- **Supersedes, for `plan2` only.** This replaces the **meaning of the type**, not only its owner:
  - NE:125, "`ExecutionId` and `PlanIntentCommitment` are **retained**" for major 2: the member is retained, its meaning is V2's;
  - NE:3159, "`executionId` and `planIntentCommitment` keep their owners": the owner is V2's function;
  - RI:792-795, the source "canonical pre-admission PlanIntent commitment stored in AttemptRecord" and its recipe over PlanIntent;
  - C2S:550-567, the `canonicalCommitment` recipe and its `planIdentityJoin` (`plan2` has no such typed field, IE:182);
  - DLV:847, `OpenUniverseV1.planIntentCommitment` typed `PlanIntentCommitment`: the shape stands, the type's source is V2's.
- **Weakest point.** It commits nothing `planId` does not, and it exists after the draw, not before attempt admission.

**V3. The capability manifest. Recipe SETTLED-BY-TEXT; TS1 content PROPOSED (lead ruling r5); release reader and `vcs-change` form OPEN (O3).**
It is a release artifact of media type `application/vnd.opensip.capability-manifest.v1`, bound by
`ProfileEntry.capabilityManifestId` (DLV4:460-467; DLV:1251) and committed as CVE1 (DLV4:472; IE:224-235). The host
recomputes the id and never trusts a supplied one (DLV4:286; IE:233-235). Admission is CMD2's, which IE §3 selects by name
(IE:236-246); its `RELATION-DOMAIN-V2` adds `unresolved-edge` and its ladder adds `observed` (CMD2:23-59, :106), which
DLV4's twelve-member domain cannot express. **The manifest id enters the Plan id** (`plan2` commits the capability manifest,
IE:182; MC8:921), so the pinned content below is part of every TS1 Plan's identity. Nothing on the TS request path reads the
content (TSP2:49, row DLV:963-971); product admission checks identity and form only (`plan_capability.rs:45-80`).
- **Rule.** J2b-TS takes the manifest **bytes** only and derives both members through `admit_capability_manifest`
  (`evaluator/src/capabilities.rs:189`); the Run retains the bytes (`plan_capability.rs:53-65`).
- **TS1 source.** A labelled synthetic install profile in J3d-TS's `scenario-fixtures` fixture (MJ:820). It advertises
  exactly what TS1 implements. `DCM-2-typescript-deep` (DLV4:853) overclaims and is not used.
- **TS1 content (normative), the authoring value before CVE1:**
  - `schemaVersion` `1`. `profile` `"ts1-synthetic"`, equal to the fixture's `ProfileEntry.profileId` (DL-CUST-3; CMD2 declaredOPEN).
  - `providers`, sorted by `providerId` (DLV4:307-308):
    - `{"providerId": "syntax-all", "language": "*", "providerVersionSource": "release-manifest:syntax-grammars",
      "toolchainIdentitySource": "release-manifest", "relations": {"file": "enumerated", "package": "manifest-declared"},
      "platformIds": ["macos-aarch64"]}`: the id and both sources as every live manifest has them (DLV:1359, :1374, :1389,
      :1404), narrowed to the two relations TS1 delivers.
    - `{"providerId": "typescript-semantic", "language": "typescript", "providerVersionSource":
      "release-manifest:typescript-provider", "toolchainIdentitySource": "PlanId.typescriptUniverse", "relations":
      {"imports": "resolved-target", "unresolved-edge": "observed"}, "platformIds": ["macos-aarch64"]}`. The id and both
      sources are DCM-2's; the relations are F2-min's (PA1 §3).
  - `coverageForAbsent`: `[]` (CVE1 encodes it present, DLV4:1113). No Rust entry: the profile installs no Rust provider
    and the fixtures hold no Rust unit.
  - Not claimed: `references`, `calls`, `types`, `reachability`, `declares`, any syntax relation, `clones`, `vcs-change`.
    `platformIds` names the one platform the milestone Run is measured on; a member of that domain grants no support (CMD2:135).
- **Why `syntax-all` (lead ruling r5).** The producer and enumerator of host inventory records is the core provider closure
  (MC8:40, LD8-1; MC8:497-503, use 3; the stage's `producerClosure`, MC8:995), which is also the producer of syntax-universe
  work (use 2). The live manifests place exactly that closure's relations, the syntax relations and `file`, `package`,
  `vcs-change`, under the one id `syntax-all` (DLV:1359-1404; DLV4 DCM-1 to DCM-4, DLV4:803-975). No text binds a
  `providerId` to a closure (CMD2:230, "No provider registry exists"), so this is continuity, not identity proven by text;
  no text names a different id for the core. NCM names no provider id at all; it says only that inventory is "Produced by
  host discovery and enumeration, not by a language provider" (NCM:949), which fits the core. Weakest point: the version
  source names the syntax grammars, which a TS1 Plan does not select (PA1:163-168).
- **The core provider closure is in the TS1 Plan.** Selecting no syntax universe does not remove it: `semanticClosures`
  carries it "exactly when a syntax universe is selected **or** an `inventory` cell is requested" (MC8:922), and V8
  requests `inventory`.
- **`vcs-change`: TS1 form, and the release question.** The TS1 manifest neither claims `vcs-change` nor declares it absent.
  This is lawful: no text makes a manifest total over relations (CMD2's four gates check type, closure, domain membership and
  order only, IE:256-261), product admission checks identity and form only (`plan_capability.rs:45-80`), and with the
  run root outside every repository the account is `inapplicable-vcs`, which names no Coverage and needs none (EXC:122,
  :172). At run time the key is answered by that account (V7). Claiming it would overclaim (LD8-3); declaring it
  absent under `syntax-all` puts one id in both collections, which DLV4 leaves "OPEN -- DEPENDENCY ON DELIVERY PRODUCT"
  (DUD-V4-3, DLV4:611, :1852-1856). How a release manifest states `vcs-change` is **OPEN** with that question (O3).
- **Fail closed.** Missing or refused bytes refuse before step 13; outside `scenario-fixtures` no reader exists.

**V4. Stages on the TS1 path. Syntax SETTLED-BY-TEXT; inventory PROPOSED (release and TS1).**
- **Syntax.** A TS1 Plan selects no syntax universe; H5-TS refuses one (PA1:163-168). Not on the path.
- **Inventory (lead ruling O1).** The milestone Run requests the `typescript` `inventory` cell (V8). PA1 keeps it in scope
  (PA1:111, :167). The chain: the cell → its binding's enumerator is the core provider closure (MC8:980) → one host inventory
  stage per universe (MC8:994; `plan.rs:880-920`) → the schema in the core tree → H3-TS derives the inventories, facts, scopes
  and Coverage (MH item 18; V7) → H5-TS wires the stage and binds its `stageOrdinal` (MC8:999). It is needed because
  `module-import-cycle` enumerates `file` subjects (I1:122), and among the capabilities V8 requests only `inventory` stores a
  `file` population (COMP:26; `plan-metered/src/plan_inputs.rs:331-343`; `clones-fact` also would, and is not requested).
  Without the cell the rule is indeterminate (`no-covering-program`, COMP:161).
- **Token. PROPOSED:** `host.inventory`, a constant in H3-TS's module, passed by J2b-TS; never a caller string. IE:1310-1311
  fixes only its form (one path segment `^[a-z0-9][a-z0-9._-]{0,127}$`); the spelling appears only in product tests
  (`plan_tests.rs:656`, `:2350`).
- **Schema.** `opensip-interface/stage-output/host.inventory.schema.json`, identical in form to TSP2 T1's (TSP2:78-85): JSON
  Schema 2020-12; `x-opensip-stage-output: {schemaVersion: 1, operation: "host.inventory", outputDomains: ["view"]}`; body
  an object with one required `viewId` matching `^view2:[0-9a-f]{64}(?![\s\S])`, `additionalProperties: false`.
- **Core tree.** The core provider closure is the core inventory's platform descriptor with `kind: provider` (MC8:484,
  :486-503; `security/src/trust/core_inventory.rs:384-419`), so the file is a member of the signed core platform tree.
  **TS1:** security's synthetic core image (MC8 item 8) carries it. **Release:** the core inventory builder (O3).
- Unchanged: `STAGE_OUTPUT_SCHEMA_UNREGISTERED` (`plan.rs:1161`). Inventory stages follow the P stages (TSP2:90).

**V5. `semanticGrantDigest`. SETTLED-BY-TEXT (release and TS1).** C4a owns the grant and its check (MC8:930-932, :952,
:1185; PLAN5:122-126). Record: IDS `semantic-grant` v2 (`schemas/sources/identity-v3.schema.json:2236`): `projectId`; one
`first-party` principal, owner source null, per selected provider closure (P and, with the `inventory` cell, the core
provider closure, MC8:922); `analysisOperations` `[native-analysis, read-source]`; the Plan's `scopeDigest` (IE:525-539).
At TS1 the required set is always granted, so the permission check (IE:538-539; MC8:932) has no live refusal path; it is
held by a control with a `read-import` negative. **Carrier (lead ruling O4): C4a-TS-b**, its own commit after the stage projection.

**V6. `DispatchContext` and `DispatchBindingV1`. PROPOSED (release and TS1); lead ruling H5-TS Q-C (a).** D2B:142 names
D4's session factory; MD item 26 (MD:852-860) omits it; the factory takes it "already assembled from C4's supplied
projections" (`session_factory.rs:97`). TSP2:203's "its existing owner" names none. Every member is a value of the built
`Ts2Request`, its `Ts2Plan`, or the verified descriptors (D2B-A2:36), as the fixture shows (`launch_recheck_ts2_fixture.rs:198`)
and as Rust3's sender does inside `build` (`rust3/send/request.rs:427-439`); B's `Ts2Request` exposes each frame (B `send.rs:1579-1623`).
- **Rule.** One pure projection, H5-TS's code (H5S:116-119), maps the built request and its `Ts2Plan` to the context.
  C4a-TS-b's `admit_and_build` is its only production caller and returns the `(Ts2Request, DispatchContext)` pairs **and the
  retained Plan records**, as Q-C (a) states. Stages, tokens and census from `Ts2Plan` (TSP2 T3-T8; `expectedStageId` by
  T4, TSP2:141-146); OpenUniverse, manifest and seal from the request; descriptor fields from the verified descriptors.
- **`DispatchBindingV1`.** The same projection emits each stage's static members (`retainedStageOrdinal` by TSP2's T1 map);
  H5-TS completes `expectedBatchIndex` and `expectedFirstCandidateOrdinal` per settled batch from the receiver's admitted
  counters (D2B:143) for H (H `occupancy.rs:71-81`). `joins` (`participant.rs:120`) and `PROVIDER_RETURN_DISPATCH`
  (NE:3044) still refuse.

**V7. The host inventory stage's Coverage. PROPOSED; erratum to MH; narrows LD8-3.** H3 mints, per universe an available
`inventory` binding binds, the stage's view under the core provider closure (MC8:497-503, use 3; MH:651-660):
- **Scopes and facts.** Exactly two subject scopes: `file@enumerated` with subjects exactly the binding's file inventory rows,
  and `package@manifest-declared` with subjects exactly its package rows; one admitted fact per row.
- **Entry, inventory `complete`.** For each of the two scopes, one `ViewEntryV3`: `coverage` `complete`; `examinedUniverse`
  the scope's commitment and count; `resolutionCompleteness` `{state: not-applicable, attempted: false, examinedExhaustive:
  true, stageTerminal: complete, unresolvedEdgeCount: 0, unresolvedEdgeClasses: []}`; `closedWorld` **CW** (below);
  `derivationKinds` `[]`; `confidenceMillionths` `1000000`; `deficiency` null; `nativeCause` null.
- **Entry, inventory cut by a budget** (`partial`, deficiency `budget-exhausted`, ENC:120): the same scope and facts over the
  known rows, and the entry as above except `coverage` `unknown`, `examinedExhaustive` false, `stageTerminal`
  `budget-exhausted`, `deficiency` `budget-exhausted`, `nativeCause` null.
- **A package manifest that does not parse** (package inventory `partial`, `source-syntax-invalid`, ENC:118, :120), or an
  inventory not `complete` for any other reason: H3 refuses before anything is staged, with the internal key
  `H_INVENTORY_STAGE_COVERAGE` on MJ row 29's existing host-invariant route (`operational-failed` / 4,
  `SYSTEM.OUTCOME.ILLEGAL_STATE` / host-invariant, `HOST.INVARIANT_VIOLATED`, MJ:755; MH:738 routes item 18's refusals there).
  No new public code.
- **TS1 LIMIT: a repository whose package manifest does not parse cannot be analysed with `inventory` requested** until a
  later record registers a carrier for that case. The refusal is classed as a host invariant although its cause is the
  analysed repository: a known mis-classification, accepted for TS1 only. The fixtures' manifests parse.
- **No `vcs-change@vcs-reported` scope, fact or entry.** The key is answered by the execution-inputs account alone.
- **CW (V7's own value; no text fixes one):** `{"exportsClosed": "unknown", "entryPointsRecognized": "none",
  "nonliteralLoading": "none", "externalConsumers": "unknown", "dynamicDispatch": "not-applicable", "reasons":
  ["no-manifest"], "deadCodeRepairEligible": false}`. It is not an extension of the startup law's clause, which applies only
  to the pre-Analyze conversion (NE:3259).
- **Narrows LD8-3** for the host inventory stage of a `plan2` Run, superseding: MC8:42 "That key's Coverage is `unknown` …";
  MC8:56 "Its Coverage is `unknown`, `provider-unavailable`, `capability-missing`" and its rejection of "omitting the entry";
  MC8:331 "H mints the key's entry as `unknown`, with deficiency `provider-unavailable` and `nativeCause`
  `capability-missing` (NE:3370)"; MC8:332's rejection of "omitting the key's entry, which leaves a requested relation
  unanswered"; MC8:1271 "H3 and H5 also carry LD8-3's control: … the `unknown` entry with `provider-unavailable` and
  `capability-missing`". LD8-3's other rules stand: no `vcs-change` fact, never `complete`. MC8:1329 (V5's question on that
  pair) becomes moot for this stage.
- **Controls owed (H3-TS).** H-C11b (below); each entry member above, byte for byte, for both entry forms; no `vcs-change`
  entry or scope; a package parse failure refuses `H_INVENTORY_STAGE_COVERAGE` with nothing staged; a budget-cut inventory
  gives the `unknown` entry.

**V7 Basis (not normative).**
- **Precedent and owner.** Accepted ME item 10 has the host derive Coverage for the in-host syntax stage, `complete` for a
  `parsed` file (ME:385, :389); MH admits those host-minted entries (MH:585, :596), and 14.1 classes item 18's view as
  host-minted (MH:471). The records are host-derived (NCM:949). An available `inventory` binding's accounts are
  `supported-available` (NCM `inventory` TS cells, `SUPPORTED-DESIGN`), so each needs returned Coverage (EXC:169); required
  incomplete work is semantic indeterminate (EXC:190; COMP:58).
- **Members.** Both pairs are RC-1's one-rung pairs, "minted with `attempted=false`, `unresolvedEdgeCount=0` and
  `unresolvedEdgeClasses=[]`" (NE:2045-2046); `complete` requires `examinedExhaustive` (RC-6); `stageTerminal` is free on a
  `not-applicable` entry and retains the terminal the producer observed (NE:2101-2104); `derivationKinds` is a subset of the
  type derivation kinds (NE:2028); "no native provider of any relation emits a confidence below 1000000" (NE:2366-2372).
- **Budget cut.** NE §10 registers `budget-exhausted` with carrier `entry.resolutionCompleteness.stageTerminal` =
  `budget-exhausted` and a null cause (NE:3372; NES registry, `nativeCause` "must-be-null"); the registry is not scoped by
  relation, and the inventory's own deficiency is the same `DeficiencyV2` member (ENC:120; EXC:70). ME item 10's truncated
  row is the same form (ME:391).
- **Parse failure.** `coverage` is `complete` or `unknown` (NE:2020); `source-syntax-invalid` is "not a NativeCause / copied
  DeficiencyV2 member" (ENC:120). `input-closure-incomplete` requires one of twelve named causes, none a parse failure (NES
  `x-opensip-deficiency-cause-registry`; product `coverage-registry.current.json`); SYN-1's `source-parse-error` (ME:390) is
  bound only in the design lock (product `682991f`) and is in neither registry. `provider-unavailable` with a null cause is
  registered but would be false. A required partial inventory is indeterminate in any case (EXC:70).
- **CW.** ME r3 states no `closedWorld` for the syntax stage; MH:455 rejects host recomputation; the only published host value
  is the startup law's, limited to the pre-Analyze conversion (NE:3241-3261). An inventory relation carries no export,
  entry-point or loading observation, so CW records that none was made (as NE:3259-3261 reads the same value). Weakest
  point: `exportsClosed: unknown` is the `external-consumers-unknown` carrier (NE:3368), consulted only for a universal
  negative over exported subjects (NE:2226-2228); `no-manifest` means "no manifest observation was made".
- **`vcs-change`.** First, the texts: no text states the subject scope of a `vcs-change` key that has no fact, and the
  fact-admission law says the pair "is not decided here" by item 18 (MH:662). Second, the reviewed producer check admits only
  the `file` and `package` pairs on a core-produced language stage (H5-TS `opensip-h5-ts` @ `077916e4`,
  `host/src/fact_admission/candidates.rs:442-466`). The account then is: **`inapplicable-vcs`** (kind `none`), no Coverage
  named (EXC:122, :172), identical with or without an entry; **`supported-available`** (kind `git`), empty, so
  `native-work-incomplete` with the pair `(null, null)` (EXC:169, :70), where LD8-3's entry would carry
  `provider-unavailable` / `capability-missing`. Cell state (`partial`, EXC:67) and verdict are equal; the retained pair differs.
- **What `complete` rests on.** The totality check (`COVERAGE_INVENTORY_TOTALITY_OMITS_PATH`, `view_joins.rs:518-527`;
  NE:359-362) iterates the scope's own subjects, so it cannot find an omitted path. Two re-derivations do: ENC §7 replay
  (ENC:157-158) refuses a `complete` file inventory that differs from the binding's extent (ENC:117,
  `enumeration_join.rs:986-991`), the extent being re-derived from `UnitMembershipV1` and the sealed snapshot (ENC:172, :186,
  `enumeration_join.rs:748-764`; membership covers the snapshot, `enumeration.rs:346-348`; package rows by parsing, ENC:174,
  :178); and EXC:169's expected source census (`execution_inputs.rs:1202-1240`, :1707, :296) leaves the account incomplete
  for a subject the scope omits. They run at J-η (MJ:401) and in the evaluator's composition (`full_walk.rs:429` →
  `execution_reader.rs:221`). Trust limit: a path missing from the sealed snapshot or mis-excluded by membership is host TCB
  (ENC:172, :186), as for every cell (compare ME:398). Nothing was unknown, so this is not MH:440's forbidden conversion.
**V7, continued (normative).**
- **Erratum to MH (seven sentences).** "Provider-return stage" below means a stage whose returns form provider-return views
  (MH item 14.1, MH:470: a TS2 or Rust3 stage). Item 11's pre-Analyze conversion stands in for such a stage's return, which is
  why 14.1 lists it as host-minted (MH:471); a narrowing to "provider-return view" alone would exclude item 11's own entries.
  - MH:135 "H never edits an entry and never mints `complete`." → "… never mints `complete` for a provider-return stage."
  - MH:414 "This is the only case in which the host writes Coverage" → "… writes Coverage for a provider-return stage".
  - MH:429 "any host-minted entry other than `unknown`" → "… other than `unknown` for a provider-return stage".
  - MH:440 "The only entries the host writes are item 11's pre-Analyze conversion entries, and they are `unknown`." → "For a
    provider-return stage the only entries the host writes are item 11's …, and they are `unknown`. Items 16 and 18 write
    the Coverage of their host-minted views (ME item 10; TS1-HOST-VALUES V7)."
  - MH:443 "a `complete` minted by the host" → "a `complete` minted by the host for a provider-return stage's key".
  - MH:785 (H-C11) "host-minted entries are `unknown` only" → "host-minted entries of a provider-return stage are `unknown` only".
  - MH:891 "a host-minted entry other than `unknown`" → "… other than `unknown` for a provider-return stage".
  - **New control H-C11b (item 18), H3's:** a file scope omitting one inventoried path leaves the `file@enumerated` account
    incomplete (EXC:169); a view missing one `file` fact refuses `COVERAGE_INVENTORY_TOTALITY_OMITS_PATH`; a `complete` file
    inventory omitting one extent path refuses `ENUMERATION_INVENTORY_FILE_TOTALITY`. **Owed and not yet tested** by H3-TS
    (they need the execution-inputs and enumeration joins over a full world): the scope-only drop and the inventory drop.
- **Verdict note.** A **required** `inventory` cell (`discovery.rs:1255`; `analysis.capabilities` has no optional form)
  completes only if its `vcs-change` account is not `supported-available`, because that key gets no Coverage (above;
  EXC:122, :169, :190; COMP:58). It also needs the package inventory not `partial` (EXC:70: "Required partial inventory … still emits
  `required-cell-unsatisfied`") and, for the `imports` and `unresolved-edge` cells, the symbol census (FA-2; PA1 §3).
  - **The fixture fact.** The corpus trees contain no version-control directory: the fetch materializes `git ls-tree` blobs
    into `store/<treeDigest>/` and deletes its work directory (`docs/implementation/m3/corpus/FETCH-SPEC.md:16`, :43-66);
    `js-small-body-parser` (`t2-corpus-c8cc48e1/store/22cd9196…`, 25 files) and `ts-small-constructs` (`…/store/048425b5…`, 45
    files) hold no `.git`, and G-TS2's file lists have none (`LC/cf1/g-ts2/oracle/afe9cedba83c-33fc39aa/*.request.json`).
  - **The placement, chosen and disclosed.** The VCS kind is decided by an upward walk from the project root
    (`security/src/custody/git_tracking.rs:1-12`; MC8:321, "the innermost is used"); a tree inside any Git repository gets
    `kind: git`. So the milestone Run is made on a **copy** of the fixture tree placed at a run root outside every Git
    repository. X2's observation is then `NoRepository`, "kind: none" (MC8:321), the account is `inapplicable-vcs` (EXC:122),
    and with V7 the cell can complete. The placement is a choice, and the milestone record states it. MC8:336 rejects
    `kind: none` for a Git checkout; a copy outside every repository is not one. Under kind `none` the `vcs-change` account
    is `inapplicable` with no Coverage (EXC:172; `evaluator/src/execution_inputs.rs:1597-1613`). The milestone record
    discloses it.
  - **The project marker.** The copy carries no `.opensip/`. The Run's own first use creates `.opensip/project-id.v1` at R9
    (IE:43-49; MJ:347; `security/src/custody/first_registration.rs:13-15`), and the marker is not inventoried (MC8:228, C1-T25;
    MC8:945, SX-1's `.opensip` anchor). A reused run root must carry the marker its registry agrees with (IE:47-49).
  - **Harness requirement (J3d-TS and the lead-run harness, G9).** Before the Run, the harness places the copy, checks that
    no ancestor of the run root holds a VCS marker, and refuses to start otherwise. After it, the harness reads the retained
    `vcs-observation` and produces **no milestone record** unless its `kind` is `none`.

**V8. The requested capabilities of the M3-M-TS1 Run. PROPOSED (TS1); carrier by lead ruling r5.**
- **The set.** For every unit discovery finds in a fixture tree, exactly three rows, each `required: true`, at that unit's
  mode and root: `imports`, `inventory`, `unresolved-edge` (NCM capability ids). These are exactly the capabilities V3
  claims as delivered: no requested cell lacks a producer, and the verdict is decidable (COMP:58; EXC:190). Lead ruling O1
  gives the inventory cell; PA1:255-257 the rest: "C4a-TS's `requestedCapabilities` for the TS1 Run name only the cells
  F2-min implements (the fixture's configuration selects them; the analysis-spec takes "B's requested capabilities",
  MC:923)".
- **The carrier.** The lead-run harness writes one file, `opensip.json`, at the root of the run-root copy (V7), with
  exactly these 89 bytes, no trailing newline:
  `{"schemaVersion":2,"analysis":{"capabilities":["imports","inventory","unresolved-edge"]}}`
  (SHA-256 `e01e83bee7db2df0779600bbd4458d7d666a6383e7c8bbb90c4258e54c6a1b45`). `schemaVersion` is the schema's only required
  member and nothing else is set (product `schemas/sources/product-configuration-v2.schema.json`; `analysis.capabilities` is
  an ordered sequence of up to 128 ids). This is the texts' own narrowing: explicit configuration "overrides the request,
  not the obligation", "a recorded choice with its own provenance" (NE:1185-1189; AQ:102). The fixture's own files are
  unchanged. The milestone record discloses the file's bytes and digest and that the Run is of **the fixture plus this
  configuration file**.
- **Not compiled defaults.** r4's reading that the TS1 release's compiled defaults could carry the narrowed list is
  withdrawn: the default is "fixed by the matrix, not by a release" and requests every capability not `NOT-SELECTED`
  (NE:1080-1084); a release absence is "still requested" (NE:1089-1092); a build shipping fewer providers is "not a narrowed
  product" (NE:1183-1184). The product's default selection does exactly that (`host/src/discovery.rs:1212-1272`).
- **What the file does to the snapshot.** It is a sealed file of the tree: `opensip.json` at the project root "is a
  repository file, so it stays in the inventory", and sealing requires exactly one regular-file row whose digest equals the
  carrier B1 resolved (MC8:184, :92, :198). So the snapshot, its `resolvedConfigDigest`, the file inventory (one more `file`
  subject and `file` fact) and the Plan id all differ from a Run of the bare tree. It does **not** supply the project
  marker: that is `.opensip/project-id.v1`, created by first use (V7) and never source (MC8:103).
- **Consequence (owner: J2b-TS's `PlanRequest` producer, its scope commit 3, `LC/j2b-ts/SCOPE-r1.md:62-63`, :90).** No
  product code yet turns the resolved configuration's `analysis.capabilities` into `requestedCapabilities` tuples: main and B
  have only `default_capability_selection`, which reads no configuration (`discovery.rs:1217`). That producer must map each
  configured id to one row per unit whose mode does not mark it `NOT-SELECTED`, `required: true`, under the same admission
  order as the default (MC8:946; NE:4276-4278).

## Owners

| Value | Code | Unit |
|---|---|---|
| V1 | `opensip-host` constant | C4a-TS-b |
| V2 | `opensip-identity` function and newtype | C4a-TS-b (identity change flagged) |
| V3 | bytes input; TS1 manifest bytes in the fixture | J2b-TS; J3d-TS |
| V4 | token and schema bytes; TS1 core tree | H3-TS; security (synthetic core) |
| V5 | step 13 grant | C4a-TS-b, own commit after B7 |
| V6 | projection and per-batch binding (H5-TS); the call in `admit_and_build` (C4a-TS-b) | H5-TS; C4a-TS-b |
| V7 | inventory stage scopes and Coverage, H-C11b; MH erratum; run-root placement and its two checks | H3-TS; lead (erratum); J3d-TS and the lead-run harness |
| V8 | the requested set; the `opensip.json` in the run-root copy; configuration → requested rows | J3d-TS; lead-run harness; J2b-TS (commit 3) |

## What this record does not do

It adds no wire field, Plan member, IDS row or public code. It adds one internal refusal key, V7's
`H_INVENTORY_STAGE_COVERAGE`, on MJ row 29's existing host-invariant route (MJ:755).
**It does not make a repository with an unparsable package manifest analysable with `inventory` requested** (V7's TS1
limit): that Run refuses as a host invariant, a known mis-classification, until a later record registers a carrier. It it does not decide a pre-draw intent (O2), release
identity, packaging or signing (O3), or the Rust provider's values. It does not supply: the JS-synthesized profile for
`js-small-body-parser` (row 15b); the `VerifiedLauncher` signed state (CF-1 tier 2) and CF-2; the ExecutionInputsV1 and
Run-candidate builders; read-back (G8); the lead-run home (G9). Those are J2b-TS's, J3d-TS's and H5-TS's. The lead-run
harness reads V3's bytes only under `scenario-fixtures`, so it is built with that feature.

**It does not lift M3's `vcs-change` limitation.** On any Git working tree a Run that requests `inventory` cannot reach
`pass` until `vcs-change@vcs-reported` Coverage has a producer: LD8-3 forbids `complete` (MC8:331) and MC8 item 4 rejects a
Git object reader at M3 (MC8:323, :335). Which unit or milestone owns a VCS reader is **silent** (MC8:323 names only M5
consumers; `fact-admission-h/PROPOSAL.md:873` routed it to MC, which answered with LD8-3).

## Open points

- **O2 (lead; R3 if contested).** Whether a released `plan2` Run needs a real pre-draw intent. The possible pre-draw form: a
  commitment frozen at R10a, before R12's draw (MJ:343-351), over what is admitted by then: the resolved configuration
  (R5, with `analysis.capabilities`), the admitted pack set (R6) and the admitted component manifests (R10a). Discovery's
  capability selection and the snapshot come after the draw (MC8:945-946), so such an intent cannot commit them.
- **O3 (project owner).** V1's release form; who builds and signs the core inventory and the release profile's manifest;
  how a release manifest states `vcs-change` (DUD-V4-3, V3); how an installed release's profile bytes are read (MJ item 1
  takes no profile selector).
- **For the owner's awareness (existing law; no change proposed).** By design a Run with no explicit selection requests every
  capability the matrix does not mark `NOT-SELECTED`, as required (NE:1080-1092). Until each has a producer such a Run is
  indeterminate (EXC:190; COMP:58). On a Git working tree a Run requesting `inventory` cannot reach `pass` until
  version-control state has a reader (LD8-3, MC8:331); under V7 that `vcs-change` account carries no deficiency and no
  cause (`native-work-incomplete`, `(null, null)`, EXC:70, :169).

## Consequences

- V4 and V7 change the synthetic core tree, so the core provider, evaluator and detector `closure2`s and every golden pinning
  them move; `host.inventory` literals become the constant; H3-TS's inventory leg mints Coverage.
- V3's content and V8's configuration file each enter every TS1 Plan id; a later change to either moves every TS1 Plan golden.
- **M3 limitation (disclosure owed):** a Run requesting `inventory` on a Git working tree is `fail` or `indeterminate`, never
  `pass`, until `vcs-change` has a producer. The M3-M-TS1 record discloses the run-root placement, the added `opensip.json`, and why the cell can complete.
- **Alignment edit owed on TSP2 (not made here):** TSP2:203, "The dispatch binding: its existing owner, changed only by
  T4", should cite V6 (H5-TS's projection, called by C4a-TS-b).
- **H5-TS code change (V7 r7):** H3-TS's inventory leg currently refuses any non-`complete` inventory; a budget-cut
  inventory must instead give V7's `unknown` / `budget-exhausted` entry. Only a package parse failure (or another
  non-budget cause) still refuses `H_INVENTORY_STAGE_COVERAGE`.
- **Milestone record disclosures (V7):** the run-root placement, the added `opensip.json` (V8), and the TS1 limit that a
  package manifest that does not parse makes the Run refuse as a host invariant.
- V2 changes B's `Owners` field type; V1 removes caller-built `HostBuildId`s; V6 changes `admit_and_build`'s return.

## Rejected alternatives

- **V2: `sha256:` + the plan2 hex**, or `opensip.plan-intent.v1` over `{planId}`: a relabelled PlanId, or a false C-2 claim.
- **V3: a caller-supplied id** (DLV4:286); **DCM-2 as is**: it claims relations TS1 does not deliver.
- **V4: no inventory cell**: the rule is indeterminate by construction.
- **V6: the context built in D4's session factory**: a second derivation of values the request holds.
- **V7: no Coverage** (H5S Q-B (b)): every required `inventory` cell `native-work-incomplete`; **`partial` with
  `source-syntax-invalid`** (r5): not a Coverage value; **reusing the startup clause for `closedWorld`**: it limits itself
  to the pre-Analyze conversion; **`complete` for `vcs-change`**:
  LD8-3 forbids it; **resting `complete` on the totality check alone**: it reads the host's own subjects.
- **V8: the product's default request**: references, calls, types, reachability and candidate-only cells would hold the Run
  at indeterminate (EXC:190; COMP:58). **V8: a narrowed compiled default** in the TS1 release: NE:1080-1084, :1183-1184
  forbid it.
