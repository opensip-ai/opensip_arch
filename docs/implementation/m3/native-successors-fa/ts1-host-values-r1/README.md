# TS1-HOST-VALUES — owners and lawful sources for six values the first TypeScript Run needs and nobody produces

2026-11-11. Drafted by a lead-dispatched design author (Claude Opus 5.5, route R2-DEEP) from the E2E gap inventory
(`LC/coordinator/E2E-GAP-INVENTORY-2026-11-11.md` §2, §3 G2-G4, G6, G7).
Status: **PROPOSED, r1, unreviewed.** It needs one independent review, then a cross-vendor review, then adoption by the
lead. It binds nothing, changes no existing file, registry, inventory or lock, and has no subject manifest yet.

**Scope.** Milestone M3-M-TS1: a synthetic-trust Run (OD-SIGN-2 (A)) driven through `opensip_host::invocation::run` by host
tests or the harness (MJ item 1; PA1 §1.5, §6). Each clause says whether its rule can stand for a released product
(**release**) or is TS1-only (**TS1**). Marks: **SETTLED-BY-TEXT** (only an owner was missing), **PROPOSED** (new law,
needs review), **OPEN** (a named decision is needed).

## Short names

Base: architecture main `3e4203f0f`. Product: main `ff93e4c6` (paths without prefix); **B** = `opensip-c4ats-b` @ `3450957f`;
**H** = `opensip-h1` @ `3bb78e1b`. `LC` = `.opensip-implementation-cache/lead-2026-10-25`.

| Name | Document |
|---|---|
| **DLV** / **DLV4** | `docs/coop/artifacts/delivery.v2.json` / `delivery.v4.json` (applied head, `OPENSIP-DISTRIBUTION-AND-COMPONENT-TRANSITION-BRIEF.md:43`) |
| **RI** / **C2S** | `docs/coop/artifacts/resolved-inputs.v2.json` / `c2-plan-stage-schema.v3.json` |
| **NE** / **IE** | `docs/v2/contracts/product-v1/native-evidence.md` / `identity-and-evidence.md` |
| **IDS** / **DSP** | `docs/coop/design-corrections/foundation/identity-schemas.v3.json` / `native/dispatch-binding.schema.v1.json` |
| **COMP** | `docs/coop/design-corrections/foundation/evaluator-composition-contract.v3.md` |
| **MC8** / **MH** / **MJ** / **MD** | `docs/implementation/m3/` `snapshot-plan-c/PROPOSAL-r8.md` / `fact-admission-h/PROPOSAL-r3.md` / `host-pipeline-j/PROPOSAL-r5.md` / `supervisor-d/PROPOSAL-r5.md` |
| **I1** / **D2B** | `docs/implementation/m3/preview-pack-i1/PROPOSAL.md` / `supervisor-d/d2b/PLAN-r3.md` (with `PLAN-r3-A2.md`) |
| **TSP2** | TS-STAGE-PLAN2 r4, branch `ts-stage-plan2-r1` @ `deef8c4f1` (PROPOSED) |
| **PA1** / **PLAN5** | `LC/pa1/PLAN-AMENDMENT-TS1-r3.md` / `LC/c4ats/PLAN-r5.md` |

## Subject

| Value | Consumed at | What the texts give |
|---|---|---|
| `hostBuildId` | `components/.../ts2/send.rs:124`, `:897`; B `host/src/plan_ts2.rs:602-608` (`HostBuildId`) | shape only: "non-empty NFC text" (NE:2958; DLV:846) |
| `planIntentCommitment` | `send.rs:138`, `:949`; B `plan_ts2.rs:638` (`&str`) | a C-2 `PlanIntent` commitment (DLV:418; RI:668, :795); NE:3159 "keeps its owner" |
| `capabilityManifestId`, `capabilityManifestBytesDigest` | `host/src/plan.rs:143-144`, `:403-404`; `evaluator/src/plan_capability.rs:45-80` | "the committed CVE1 artifact" (IE:224-235; MC8:921) |
| host inventory operation and schema; core tree | `plan.rs:706`, `:888`; `plan.rs:1161` | "the core's inventory interface registers" (MC8:998); X-9 (MC8:1271) |
| `semanticGrantDigest` | `plan.rs:149`, `:410`; `evaluator/src/run_links.rs:339-352` | IE:525-539; MC8:930-932 |
| `DispatchContext`, `DispatchBindingV1` | `ts2.rs:127-129`; `session_factory.rs:97-109`; H `fact_admission/occupancy.rs:69-81` | NE:3023-3045; DSP; D2B:142 |

It **extends** MC8 item 16 (V4, V5), NE §9.7 (V2) and D2B LD-D2B-15 (V6) for `plan2` Runs. It **supersedes**, for `plan2`
Runs only: NE:3159 and DSP's `planIntentCommitment` "exact AttemptRecord/ExecutionPlan value" (by V2); D2B:142 and the
`ts2.rs:127-128` comment "built by D4's session factory" (by V6). Historical C-2 Plans keep every selector unchanged.

## Normative clauses

**V1. `hostBuildId`. PROPOSED (TS1); release OPEN.** No text relates it to any release identity: it occurs only as a
Hello member (NE:2817-2819, :2958; DLV:846), enters no Plan, identity, receipt or retained record, and the worker only
checks its shape. The product's one compiled release identity is the `version` command's `hostRelease`, a semver taken
"solely from the CLI's `env!("CARGO_PKG_VERSION")`" (`docs/implementation/m1/metadata-v2/README.md:93-94`;
`apps/cli/src/bootstrap.rs:32`; `host/src/outcomes.rs:280-281`; `schemas/sources/metadata-v1.schema.json:56-61`). The
provider's build id is `typescript-provider <version>` (`tools/typescript_closure.py:385`).
- **Rule.** One constant in `opensip-host`: `HOST_BUILD_ID = concat!("opensip-host ", env!("CARGO_PKG_VERSION"))`.
  `HostBuildId::current()` is its only production constructor; `HostBuildId::new` becomes test-only. ASCII, so NFC.
- **Fail closed.** No caller text reaches `Ts2Plan.host_build_id`; a test pins the constant against NE:2958's predicate.
- **Weakest point.** `opensip-host`'s version is not the CLI's: both are `0.1.0` by coincidence (two `Cargo.toml`s). The
  release rule (equal to `hostRelease`, to the signed `ReleaseManifestV1.releaseVersion` (DLV:1240), or both) is the
  project owner's (release identity).

**V2. `planIntentCommitment` for a `plan2` Run. PROPOSED (release and TS1).** By the texts it is
SHA-256(`opensip.plan-intent.v1` ‖ 00 ‖ canonical-json-v1(PlanIntent)) (RI:795; C2S:550), where PlanIntent is the C-2
request record frozen *before* attempt admission and stored with the ExecutionId in the AttemptRecord (C2S:98-99, :567;
RI:668). For a `plan2` Run **no record is that PlanIntent**: the product's `AttemptRecord` is `{store, namespace,
execution, operation, phase}` (`storage/src/commit.rs:352-361`) and is written at commit; `CommitSession::open` binds no
intent (`security/src/custody/commit_session.rs:379-447`); MJ, MC8 and MH never name it; MD item 25 uses the word only
for R1 request-class refusals (MD:833-835). Its analysis content is committed by `plan2`: `release` by
`capabilityManifestId`, `capabilityGrants` by `semanticGrantDigest`, `workflow` by `exec-plan2`, `budgets` by `budget`,
`resolvedConfiguration` and `scope` by their digests (IE:182; MC8:921-930). Network, remote and repository-execution
intents are fixed by product law and refused at R1 (MD:833-835). On the TS wire it is a required member that nothing echoes,
checks or retains (DLV:848; NE:3166-3167).
- **Rule.** For a `plan2` Run, `planIntentCommitment` = `sha256:` + hex(SHA-256(UTF8(`opensip.plan2-intent.v1`) ‖ 00 ‖
  UTF8(plan2 text))). One pure function in `opensip-identity` beside `plan_intent_preimage` (`identity/src/digests.rs:115`)
  returns a `PlanIntentCommitment` newtype, the only value `Owners` accepts. It is stored nowhere new: it is recomputed from
  the verified Plan.
- **Fail closed.** A text that is not `^plan2:[0-9a-f]{64}$` yields no value; the build refuses as a host invariant
  before spawn.
- **Weakest point.** It commits nothing `planId` does not, and it is computed after the ExecutionId draw, not before
  attempt admission. A reviewer who holds that a `plan2` Run needs a real pre-draw intent needs a larger design (a
  record frozen at R6-R10a, an IDS row and an attempt-row field); see O2.

**V3. The capability manifest. Recipe SETTLED-BY-TEXT; TS1 source PROPOSED; release reader OPEN.** It is a release
artifact: an `ArtifactEntry` of media type `application/vnd.opensip.capability-manifest.v1` in the signed host release,
bound by `ProfileEntry.capabilityManifestId` (DLV4:460-467; DLV:1251). The release builder commits CVE1(canonicalise(the
profile's authoring value)) (DLV4:472). The host recomputes the id from the bytes and never trusts a supplied one
(DLV4:286; IE:233-235). It is per profile, not the capability matrix: NCM is design law; the manifest declares what one
profile's providers deliver. Under TSP2 nothing on the TS request path reads its content (TSP2 table row DLV:963-971).
- **Rule.** J2b-TS takes the manifest **bytes** only and derives both members through the evaluator's owner,
  `admit_capability_manifest` (`evaluator/src/capabilities.rs:189`): id = `identity()`, bytes digest = raw SHA-256. The
  Run retains the bytes as a blob (`plan_capability.rs:53-65`).
- **TS1 source.** A labelled synthetic install profile in J3d-TS's `scenario-fixtures` release fixture ("labelled
  synthetic signed releases, profiles and closures", MJ:820). Its manifest declares no relation the TS1 closures do not
  deliver. DLV4's `DCM-2-typescript-deep` (DLV4:853) is not used: it declares `references`, `calls`, `types`,
  `reachability` and `syntax-all`, and lacks `unresolved-edge`.
- **Fail closed.** No bytes, or bytes `admit_capability_manifest` refuses, refuse before step 13. Outside
  `scenario-fixtures` no reader exists, so the entry refuses.

**V4. Stages on the TS1 path; the host inventory stage. Syntax SETTLED-BY-TEXT; inventory PROPOSED.**
- **Syntax.** A TS1 Plan selects no syntax universe and H5-TS refuses one (PA1 §1.3). The syntax stage and E1's schema are
  not on the TS1 path.
- **Inventory is on the path if the Run is to decide its rule.** A stage exists exactly when an `inventory` cell is
  requested (MC8:994; `plan.rs:880-920`). The only rule, `module-import-cycle`, enumerates `file` subjects (I1:122),
  and a file population needs a covering binding of kind `file` (COMP:26), which at TS1 only an `inventory` cell gives
  (`plan-metered/src/plan_inputs.rs:331-343`). Without it the rule is indeterminate by construction. F2-min's cell list
  names none (`LC/f2min/PLAN-r1.md:6-11`). Whether the TS1 fixture requests `inventory` is O1.
- **Token.** `host.inventory`: one path segment (IE:1310-1311), defined by H's inventory interface (MC8:998), as a
  constant in H3-TS's module; J2b-TS passes that constant, never a caller string.
- **Schema.** `opensip-interface/stage-output/host.inventory.schema.json` in the core provider closure's tree: JSON Schema
  2020-12 declaring `x-opensip-stage-output: {schemaVersion: 1, operation: "host.inventory", outputDomains: ["view"]}`
  (IE:1303-1318). Body: whatever the lead rules for TSP2's provider schema (TSP2 O2), applied identically.
- **Core tree.** The core provider closure is the core inventory's platform descriptor with `kind: provider` (MC8:484, :486-503;
  `security/src/trust/core_inventory.rs:384-419`), so the file must be a member of the signed core inventory's platform
  tree. **TS1:** security's synthetic core image (MC8 item 8, "The core") carries it. **Release:** the core inventory
  builder, which has no unit (O3).
- **Fail closed.** Unchanged: `STAGE_OUTPUT_SCHEMA_UNREGISTERED` (`plan.rs:1161`).

**V5. `semanticGrantDigest`. SETTLED-BY-TEXT (release and TS1).** C4a owns the grant and its check (MC8:930-932, :952,
:1185; PLAN5:122-126). The record is IDS `semantic-grant` v2 (`schemas/sources/identity-v3.schema.json:2236`): `projectId`;
one `first-party` principal with null owner source per selected provider closure (P, and the core provider closure when
it is a member, MC8:922); `analysisOperations` `[native-analysis, read-source]`; the Plan's `scopeDigest`. It is a
function of admitted inputs only. Part a did not build it (`plan.rs:149` takes a digest). The Run retains the record
(`run_links.rs:339`). Only the carry's unit is open (O4).

**V6. `DispatchContext` and `DispatchBindingV1`. PROPOSED (release and TS1).** D2B:142 says D4's session factory builds
the context; MD item 26 (MD:852-860) lists the factory's outputs without it; the factory takes it "already assembled from
C4's supplied projections" (`session_factory.rs:97-109`). Every member is a value of the built `Ts2Request`, its
`Ts2Plan`, or the verified signed descriptors (D2B-A2:36); the fixture already builds it that way
(`launch_recheck_ts2_fixture.rs:198`), and Rust3's sender builds its own inside `build`
(`rust3/send/request.rs:427-439`).
- **Rule.** One pure projection beside `Ts2Request::build` returns the request and its `DispatchContext`; C4a-TS-b's
  `admit_and_build` (the single route to `build`) is its only production caller. Sources: tokens, census and stages from
  `Ts2Plan` (TSP2 T3-T8; `expectedStageId` by TSP2 T4); OpenUniverse, manifest and seal values from the built request;
  descriptor fields from the verified signed descriptors.
- **`DispatchBindingV1`** (DSP; H `occupancy.rs:71-81`). The same projection emits each stage's static members
  (`planId`, `retainedStageOrdinal` by the TSP2 T1 map, `analyzeRequestOrdinal`, `expectedStageId`,
  `expectedAnalysisOrdinal`, `producerClosure`, `stageSpecDigest`). H5-TS completes `expectedBatchIndex` and
  `expectedFirstCandidateOrdinal` per settled batch from the receiver's admitted counters (D2B:143) and hands the record to H.
- **Fail closed.** `participant.rs:120` `joins` still refuses a context that disagrees with the request; an absent
  binding refuses `PROVIDER_RETURN_DISPATCH` (NE:3044).

## Owners

| Value | Code owner | Unit |
|---|---|---|
| V1 | `opensip-host` constant | C4a-TS-b (it owns `HostBuildId`) |
| V2 | `opensip-identity` function and newtype | C4a-TS-b (consumer); identity change flagged |
| V3 | evaluator recipe (exists); bytes input to J2b-TS; TS1 fixture | J2b-TS; J3d-TS (fixture) |
| V4 | token constant and schema bytes: H3-TS; TS1 core tree: security fixture | H3-TS; security (synthetic core) |
| V5 | `plan.rs` step 13 | C4a-TS (a carry; O4) |
| V6 | projection: components TS2 sender; per-batch binding: H5-TS | C4a-TS-b; H5-TS |

## What this record does not do

It adds no wire field, Plan member, IDS row, refusal code or public code. It does not decide the TS1 cell list (O1), a
pre-draw intent (O2), release packaging or signing (O3), or the Rust provider's values.

## Open points

- **O1 (lead).** Does the TS1 fixture request a `typescript` `inventory` cell? Yes puts V4 on the path and makes
  `module-import-cycle` decidable; no leaves it indeterminate and removes V4 and H3-TS's inventory leg from the path.
- **O2 (lead, then R3).** Whether a released `plan2` Run needs a pre-draw intent record (V2's weakest point).
- **O3 (project owner).** Release identity: V1's release form; who builds and signs the core inventory with the schema
  and the release profile's capability manifest; how an installed release's profile bytes are read (MJ item 1 takes no
  profile selector).
- **O4 (lead).** Which unit carries V5: a C4a-TS-a carry or C4a-TS-b.

## Consequences

- V4 changes the synthetic core tree, hence the core provider, evaluator and detector `closure2`s and every golden that
  pins them; C4a-TS's `host.inventory` literals become the constant.
- V2 changes the `Owners` field type in B; V1 removes caller-built `HostBuildId`s from production.
- V6 adds a projection in `components` and deletes the D2B:142 attribution.

## Rejected alternatives

- **V2: `sha256:` + the plan2 hex itself.** It labels the PlanId digest as a different commitment.
- **V2: re-using `opensip.plan-intent.v1` over `{planId}`.** It would claim a C-2 PlanIntent commitment.
- **V3: a caller-supplied id.** DLV4:286 forbids it.
- **V4: no inventory cell, silently.** It leaves the Run's only rule indeterminate without anyone deciding it.
- **V6: building the context in D4's session factory.** It would re-derive values the request already holds.
