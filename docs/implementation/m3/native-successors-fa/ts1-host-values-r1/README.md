# TS1-HOST-VALUES — owners and lawful sources for the values the first TypeScript Run needs and nobody produces

2026-11-11. Drafted by a lead-dispatched design author (Claude Opus 5.5, route R2-DEEP) from the E2E gap inventory
(`LC/coordinator/E2E-GAP-INVENTORY-2026-11-11.md` §2, §3 G2-G4, G6, G7).
Status: **PROPOSED, r2, unreviewed.** r2 applies the lead's rulings on r1's open points (O1 yes; O2 kept open for release;
O3 the project owner's; O4 to C4a-TS-b; V1, V3, V4, V6 forms), adds V7 (the host inventory stage's Coverage) and aligns
with TSP2 r4. It needs one independent review, then a cross-vendor review, then adoption by the lead. It binds nothing,
changes no existing file, registry, inventory or lock, and has no subject manifest yet.

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
| **NE** / **IE** | `docs/v2/contracts/product-v1/native-evidence.md` / `identity-and-evidence.md` |
| **IDS** / **DSP** | `docs/coop/design-corrections/foundation/identity-schemas.v3.json` / `native/dispatch-binding.schema.v1.json` |
| **COMP** / **EXC** / **ENC** | `docs/coop/design-corrections/foundation/` `evaluator-composition-contract.v3.md` / `execution-inputs-contract.v1.md` / `enumeration-contract.v1.md` |
| **MC8** / **MH** / **MJ** / **MD** | `docs/implementation/m3/` `snapshot-plan-c/PROPOSAL-r8.md` / `fact-admission-h/PROPOSAL-r3.md` / `host-pipeline-j/PROPOSAL-r5.md` / `supervisor-d/PROPOSAL-r5.md` |
| **I1** / **D2B** | `docs/implementation/m3/preview-pack-i1/PROPOSAL.md` / `supervisor-d/d2b/PLAN-r3.md` (with `PLAN-r3-A2.md`) |
| **TSP2** | TS-STAGE-PLAN2 r4, branch `ts-stage-plan2-r1` @ `deef8c4f1` (PROPOSED) |
| **PA1** / **PLAN5** / **H5S** | `LC/pa1/PLAN-AMENDMENT-TS1-r3.md` / `LC/c4ats/PLAN-r5.md` / `LC/h5-ts/SCOPE-r1.md` |

**delivery.v4.** Its own header reads `"status": "CANDIDATE"`, `"applicationState": "NOT APPLIED"` (DLV4:6-7). The
distribution brief lists it as "applied 2026-08-05 as the verified `delivery.v2` plus 21-operation derivation"
(`docs/OPENSIP-DISTRIBUTION-AND-COMPONENT-TRANSITION-BRIEF.md:43`), the blueprint lists it as the DELIVERY head
(`docs/coop/IMPLEMENTER-BLUEPRINT.md:205`), and the native source pins name its bytes
(`docs/coop/design-corrections/native/source-pins.v2.json:54-55`). All three pin SHA-256 `3cffece0…`, which is the digest
of the file carrying that header. The record relies on the applied listing: the header is the candidate's authoring state
frozen into the bytes that were later applied, and changing it would change the pinned digest. A reviewer who reads the
header as authority loses V3's custody rule (DLV4:460-472) and must fall back to IE:224-235 alone.

## Subject

| Value | Consumed at | What the texts give |
|---|---|---|
| `hostBuildId` | `components/.../ts2/send.rs:124`, `:897`; B `host/src/plan_ts2.rs:602-608` | shape only (NE:2958; DLV:846) |
| `planIntentCommitment` | `send.rs:138`, `:949`; B `plan_ts2.rs:638` (`&str`) | a C-2 PlanIntent commitment (DLV:418; RI:668, :795); NE:3159 "keeps its owner" |
| capability manifest id and bytes digest | `host/src/plan.rs:143-144`, `:403-404`; `evaluator/src/plan_capability.rs:45-80` | "the committed CVE1 artifact" (IE:224-235; MC8:921) |
| inventory operation, schema, core tree | `plan.rs:706`, `:888`, `:1161` | MC8:998; X-9 (MC8:1271) |
| `semanticGrantDigest` | `plan.rs:149`, `:410`; `evaluator/src/run_links.rs:332-360` | IE:525-539; MC8:930-932 |
| `DispatchContext`, `DispatchBindingV1` | `ts2.rs:127-129`; `session_factory.rs:97-109`; H `fact_admission/occupancy.rs:69-81` | NE:3023-3044; DSP; D2B:142 |
| inventory stage Coverage | H `fact_admission/inventory.rs`; `evaluator/src/view_joins.rs:500-531` | MH:440 vs MH:649; H5S:109-114 |

It **extends** MC8 item 16 (V4, V5), NE §9.7 (V2), D2B LD-D2B-15 (V6) and MH item 18 (V7). For `plan2` Runs only it
**supersedes** NE:3159's `planIntentCommitment` owner (V2), D2B:142's and `ts2.rs:127-128`'s "built by D4's session
factory" (V6), and the MH sentences V7 names. Historical C-2 Plans keep every selector unchanged.

## Normative clauses

**V1. `hostBuildId`. PROPOSED (TS1); release OPEN (O3).** No text ties it to a release identity: it is only a Hello
member (NE:2817-2819, :2958; DLV:846), enters no identity or retained record, and the worker checks only its shape. The
compiled release identity is `hostRelease`, taken "solely from the CLI's `env!("CARGO_PKG_VERSION")`"
(`docs/implementation/m1/metadata-v2/README.md:93-94`; `host/src/outcomes.rs:280-281`). The provider's id is
`typescript-provider <version>` (`tools/typescript_closure.py:385`).
- **Rule.** One constant in `opensip-host`: `HOST_BUILD_ID = concat!("opensip-host ", env!("CARGO_PKG_VERSION"))`, with
  `HostBuildId::current()` its only production constructor and `HostBuildId::new` test-only. No other spelling exists.
- **Weakest point.** `opensip-host` and `opensip-cli` are both `0.1.0` by coincidence.

**V2. `planIntentCommitment` for a `plan2` Run. PROPOSED (TS1); release OPEN (O2).** By the texts it commits the C-2
PlanIntent (RI:795; C2S:550), frozen at request validation *before* attempt admission and stored with the ExecutionId
(C2S:98-99, :567; RI:668: "stored atomically in AttemptRecord at ExecutionId allocation"). No `plan2` record is that
PlanIntent: the product `AttemptRecord` is `{store, namespace, execution, operation, phase}` (`storage/src/commit.rs:352-361`);
`CommitSession::open` binds no intent (`security/src/custody/commit_session.rs:379-447`); MJ, MC8 and MH never name it, and
MD uses the word only for R1 refusals (MD:833-835). `plan2` commits its analysis content (`release` → capability manifest,
`capabilityGrants` → grant, `workflow` → `exec-plan2`, `budgets` → `budget`; IE:182; MC8:921-930).
- **Order.** The texts fix the intent before the draw. In MJ's order the ExecutionId is drawn at R12
  (`CommitSession::open`, MJ:351, item 2), the snapshot is sealed in J-δ, and the PlanId is minted at J-ε, MC8 row 14
  (MJ:398-399). A digest of the `plan2` id therefore exists only after the draw, at J-ε, before J-ζ's spawn.
- **Use.** The worker checks its closed shape only (`Ts2Sha256Text`, F `src/generated/protocol.ts:616`, through
  `closedCheck`, F `src/data/machine.ts:199`); no F source outside generated and test files reads it. The host receiver
  never reads it (`ts2.rs`: no reference; `DispatchContext` has no such member); UniverseAccepted does not echo it
  (DLV:849). It is sent, shape-checked, and discarded.
- **Rule.** `planIntentCommitment` = `sha256:` + hex(SHA-256(UTF8(`opensip.plan2-intent.v1`) ‖ 00 ‖ UTF8(plan2 text))),
  one pure function in `opensip-identity` beside `plan_intent_preimage` (`identity/src/digests.rs:115`) returning a
  `PlanIntentCommitment` newtype, the only value `Owners` accepts. Stored nowhere; recomputed from the verified Plan. A text
  not matching `^plan2:[0-9a-f]{64}$` yields none, refused as a host invariant before spawn.
- **Weakest point.** It commits nothing `planId` does not, and it exists after the draw, not before attempt admission.

**V3. The capability manifest. Recipe SETTLED-BY-TEXT; TS1 source PROPOSED; release reader OPEN (O3).** It is a release
artifact of media type `application/vnd.opensip.capability-manifest.v1`, bound by `ProfileEntry.capabilityManifestId`
(DLV4:460-467; DLV:1251), committed by the release builder as CVE1 of the profile's authoring value (DLV4:472); the host
recomputes the id and never trusts a supplied one (DLV4:286; IE:233-235). It is per profile, not NCM. Under TSP2 nothing on
the TS request path reads it (TSP2:49, row DLV:963-971).
- **Rule.** J2b-TS takes the manifest **bytes** only and derives both members through `admit_capability_manifest`
  (`evaluator/src/capabilities.rs:189`); the Run retains the bytes (`plan_capability.rs:53-65`).
- **TS1 source.** A labelled synthetic install profile in J3d-TS's `scenario-fixtures` fixture (MJ:820). **Advertise exactly
  what is implemented:** TypeScript `imports@resolved-target` and `unresolved-edge@observed`; the host's `file@enumerated`
  and `package@manifest-declared` under V7; `vcs-change` only as absent (LD8-3); no candidate-only capability (TSP2:63-73
  makes them unavailable). `DCM-2-typescript-deep` (DLV4:853) overclaims and is not used.
- **Fail closed.** Missing or refused bytes refuse before step 13; outside `scenario-fixtures` no reader exists.

**V4. Stages on the TS1 path. Syntax SETTLED-BY-TEXT; inventory PROPOSED (release and TS1).**
- **Syntax.** A TS1 Plan selects no syntax universe; H5-TS refuses one (PA1:163-168). Not on the path.
- **Inventory (lead ruling O1).** The M3-M-TS1 fixture configuration requests the `typescript` `inventory` cell. PA1 keeps
  it in scope: "The TS inventory widening is **not** deferred" (PA1:111); "a TS1 Plan may request `inventory` cells"
  (PA1:167). The chain: the cell → its binding's enumerator is the core provider closure (MC8:980) → one host inventory
  stage per universe (MC8:994; `plan.rs:880-920`), operation `host.inventory` → the schema in the core tree → H3-TS derives
  the inventories, facts, scopes and Coverage (MH item 18; V7) → H5-TS wires the stage and binds its `stageOrdinal`
  (MC8:999). It is needed because `module-import-cycle` enumerates `file` subjects (I1:122) and only an `inventory` cell
  gives a TS1 `file` population (COMP:26; `plan-metered/src/plan_inputs.rs:331-343`). A Run without the cell is lawful and
  leaves the rule indeterminate (`no-covering-program`, COMP:161): a diagnostic run, not the milestone record. See V7's
  verdict note before relying on a pass.
- **Token.** `host.inventory` (IE:1310), a constant in H3-TS's module, passed by J2b-TS; never a caller string.
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
**Carrier (lead ruling O4): C4a-TS-b**, as its own commit after the stage projection.

**V6. `DispatchContext` and `DispatchBindingV1`. PROPOSED (release and TS1); lead ruling H5-TS Q-C (a).** D2B:142 names
D4's session factory; MD item 26 (MD:852-860) omits it; the factory takes it "already assembled from C4's supplied
projections" (`session_factory.rs:97`). TSP2:203's "its existing owner" names none. Every member is a value of the built
`Ts2Request`, its `Ts2Plan`, or the verified descriptors (D2B-A2:36), as the fixture shows (`launch_recheck_ts2_fixture.rs:198`)
and as Rust3's sender does inside `build` (`rust3/send/request.rs:427-439`).
- **Rule.** One pure projection, H5-TS's code (ruling Q-C (a), H5S:115-119), maps the built request and its `Ts2Plan` to the
  context; C4a-TS-b's `admit_and_build` is its only production caller and returns `(Ts2Request, DispatchContext)` pairs. Stages, tokens and census from `Ts2Plan` (TSP2 T3-T8; `expectedStageId` by T4,
  TSP2:141-146); OpenUniverse, manifest and seal from the request; descriptor fields from the verified descriptors.
- **`DispatchBindingV1`.** The same projection emits each stage's static members (`retainedStageOrdinal` by TSP2's T1 map);
  H5-TS completes `expectedBatchIndex` and `expectedFirstCandidateOrdinal` per settled batch from the receiver's admitted
  counters (D2B:143) for H (H `occupancy.rs:71-81`). `joins` (`participant.rs:120`) and `PROVIDER_RETURN_DISPATCH`
  (NE:3044) still refuse.

**V7. The host inventory stage's Coverage. PROPOSED; erratum to MH.** The texts conflict: MH item 18 lists the stage's
"scopes and Coverage" as records no law mints and gives them to H3 (MH:644-660); MH:414 and MH:440 say the host writes
Coverage only for item 11's pre-Analyze entries, all `unknown`; H-C11 pins that (MH:785). But MC8 already makes the stage
write a non-provider entry: `vcs-change` `unknown`, `provider-unavailable`, `capability-missing` (LD8-3, MC8:331, :42).
- **What is owed.** An available `inventory` binding's accounts are `supported-available` (NCM `inventory` TS cells,
  `SUPPORTED-DESIGN`, deficiency null), so each needs returned Coverage; none gives `native-work-incomplete`, and every
  expected subject must sit in some returned partition (EXC:169). Required incomplete work is semantic indeterminate
  (EXC:190) and makes the verdict indeterminate unless a gating rule fails (COMP:58).
- **Who may write it.** The stage's producer is the core provider closure: the stage spec, its view and its subject
  scopes' `enumeratorClosure` (MC8:497-503, use 3). The records are host-derived (NCM:949, "Produced by host discovery and
  enumeration"); H3 is their one minting owner (MH:651-660). So H3 writes them under that closure; no language provider can.
- **Rule.** Per universe the stage's view carries one subject scope and one Coverage entry per inventory relation:
  - `file@enumerated`: subjects exactly the binding's file inventory rows (MH:658; ENC:172, membership exactly covers the
    snapshot); one admitted `file` fact per row; entry `complete`, `examinedExhaustive` true (NE RC-6), resolution
    `not-applicable` with `attempted=false` (NE:2045-2050), deficiency and cause null.
  - `package@manifest-declared`: subjects the package rows; `complete` when every named manifest parsed, otherwise `partial`
    with `source-syntax-invalid` and null cause, mirroring the inventory (ENC:147; MH:659).
  - `vcs-change@vcs-reported`: LD8-3's `unknown` entry; no fact.
- **What `complete` rests on.** The admitted file inventory, derived only from the sealed `snapshot2` inventory and
  `UnitMembershipV1` (MH:652-658), and re-checked at Run closure: every subject in the snapshot inventory must have a
  same-universe `file` fact in the view (`COVERAGE_INVENTORY_TOTALITY_OMITS_PATH`; NE:351-362;
  `evaluator/src/view_joins.rs:500-531`). It is not the unknown-to-covered conversion MH item 12 forbids (MH:440, citing REG:368): nothing was unknown.
- **Erratum.** MH:414 "This is the only case in which the host writes Coverage" → "This is the only case in which the host
  writes Coverage for a provider stage". MH:440 "The only entries the host writes are item 11's pre-Analyze conversion
  entries, and they are `unknown`." → "For a provider stage the only entries the host writes are item 11's pre-Analyze
  conversion entries, and they are `unknown`; item 18's host inventory stage entries are TS1-HOST-VALUES V7's." MH:443
  "a `complete` minted by the host" → "a `complete` minted by the host for a provider stage's key". H-C11 (MH:785) "host-minted
  entries are `unknown` only" → "host-minted entries of a provider stage are `unknown` only, and item 18's entries are V7's".
- **Verdict note (changes O1's value).** Even with V7, a **required** `inventory` cell's `vcs-change` account stays
  `unknown` at M3 in a Git snapshot (LD8-3), so the cell is never complete and the Run's verdict is `fail` or
  `indeterminate`, **never `pass`** (EXC:68, :190; COMP:58). Discovery requests every cell `required=true`
  (`host/src/discovery.rs:1255`) and `analysis.capabilities` has no optional form
  (`schemas/sources/product-configuration-v2.schema.json`, `analysis.capabilities`). A pass needs the fixture sealed with VCS
  kind `none` (`inapplicable-vcs`, EXC:122) or a lawful optional request (O5).

## Owners

| Value | Code | Unit |
|---|---|---|
| V1 | `opensip-host` constant | C4a-TS-b |
| V2 | `opensip-identity` function and newtype | C4a-TS-b (identity change flagged) |
| V3 | bytes input; TS1 fixture | J2b-TS; J3d-TS |
| V4 | token and schema bytes; TS1 core tree | H3-TS; security (synthetic core) |
| V5 | step 13 grant | C4a-TS-b, own commit after B7 |
| V6 | projection and per-batch binding (H5-TS); the call in `admit_and_build` (C4a-TS-b) | H5-TS; C4a-TS-b |
| V7 | inventory stage scopes and Coverage; MH erratum | H3-TS; lead (erratum adoption) |

## What this record does not do

It adds no wire field, Plan member, IDS row, refusal or public code; it does not decide a pre-draw intent (O2), release
identity, packaging or signing (O3), or the Rust provider's values.

## Open points

- **O2 (lead; R3 if contested).** Whether a released `plan2` Run needs a real pre-draw intent.
- **O3 (project owner).** V1's release form; who builds and signs the core inventory and the release profile's manifest;
  how an installed release's profile bytes are read (MJ item 1 takes no profile selector).
- **O5 (lead).** V7's verdict note: seal the TS1 fixture without VCS, admit an optional `inventory` request, or accept a
  milestone Run that can fail or be indeterminate but not pass.

## Consequences

- V4 and V7 change the synthetic core tree, so the core provider, evaluator and detector `closure2`s and every golden pinning
  them move; `host.inventory` literals become the constant; H3-TS's inventory leg mints Coverage.
- V2 changes B's `Owners` field type; V1 removes caller-built `HostBuildId`s; V6 adds an H5-TS projection and changes `admit_and_build`'s return.

## Rejected alternatives

- **V2: `sha256:` + the plan2 hex**, or `opensip.plan-intent.v1` over `{planId}`: a relabelled PlanId, or a false C-2 claim.
- **V3: a caller-supplied id** (DLV4:286). **V4: no inventory cell**: the rule is indeterminate by construction.
- **V6: the context built in D4's session factory**: a second derivation of values the request holds.
- **V7: no Coverage** (H5S Q-B (b)): every required `inventory` cell `native-work-incomplete`; **`complete` for `vcs-change`**:
  LD8-3 forbids it.
