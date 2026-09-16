# Independent design review — source45 (whole-design successor)

**Reviewer:** Claude (independent design review origin 85a08aec-9d22-4ac6-8ec2-c10170e727d7, continuing after the completed source44 review; source45 charter; authored none of the reviewed bytes)  
**Standing:** Source45 whole-design successor review. Not fresh-origin independence, blind reconstruction, final application acceptance, implementation authorization or product qualification.

## Verdict: ACCEPT

No MUST, no SHOULD, no blocker. Source45 closes a real under-specification. Source44 section 9.7 named closed_world_v2 for the pre-analysis host-conversion closedWorld without publishing its output. Source45 publishes the complete record in section 9.7 and as the startup-law member hostConversionClosedWorld, and scopes it to this conversion and both languages, disclaiming any proof of absent dynamic loading or dispatch. Derived independently from section 4.5 and the registered ClosedWorldV2 schema, exportsClosed unknown, entryPointsRecognized none and deadCodeRepairEligible false are forced; the remaining members are lawful published choices that cannot enable closed exports or repair. For TypeScript and Rust, every minted entry carries exactly the published record and admits, and the entries and coverage2 identities are byte-identical to the source44 exchange, so no identity changes. The model now copies the published law. The two changed cases pin every field, and a law mutation is detected where the source44 cases could not detect a helper mutation. The checker refuses each of the three mutated sources with its exact binding fault. The repair consumer stays refused for conversion-only selections; a non-authoritative display artifact is observed. The native-cases change is a reindent plus two expectation additions, and the generic historical-batch prose is clarified per language with registered shapes unchanged. Planning v13 binds the two changed normative inputs and preserves v8-v12. ADV42-01 and ADV44-01 are retained as non-blocking advisories, and S40-01 and ADV40-01 remain resolved. The source44 reference-scope limits stay material (OBS45-10). Also completed on verified copies: subject, archive, all 12,920 members, parent44, the 14/1/0 delta, all 6,264 pins, six pinned groups, 17 children, planning and inventory, package v22 with RunIds measured unchanged, ten scope-preservation probes, startup re-execution and final copy re-verification. Source-level acceptance only: no blind reconstruction, application, readiness, implementation authorization or product qualification is granted.

## Subject

| Item | Value |
|---|---|
| subjectManifestSha256 | `8b4efbb04d9e25126ec7955931cf364f7013b3710a45c48bae8bc563a0c82155` |
| liveManifestSha256Measured | `8b4efbb04d9e25126ec7955931cf364f7013b3710a45c48bae8bc563a0c82155` |
| verifiedManifest | `True` |
| subjectFileCount | `12920` |
| subjectTotalBytes | `738315211` |
| subjectArchiveSha256 | `9536ebe3ffe27e2a99c7e02d8338738ae3d9a62a9000af4f3e5f5ce5793b909f` |
| archiveSha256Measured | `9536ebe3ffe27e2a99c7e02d8338738ae3d9a62a9000af4f3e5f5ce5793b909f` |
| parent44 | `e873c8db7b50f8d4bc4c6b1754239fb200b11f4e5d0f23b1ceaa6ea17297a32b` declared by 45: True; snapshot verified: True (12919 members); archive `c21d04914eaa07df967eeb945170a21d8ec8c7bc3c98573085522fab74b52bd5` |
| delta 44to45 | 14 changed, 1 added, 0 removed |
| owned source pins | 6264 entries; all match: True; 10 changed pins |
| planning input layer v13 | `af228325492828b0ea5d6779601725a981bb467d0195e976a4247350c972c153` (34 inputs; v8-v12 byte-identical to source44) |

Changed files: `docs/coop/design-corrections/foundation/evaluator3-source-pins.v1.json`, `docs/coop/design-corrections/foundation/provider-target-attribution-return.schema.v2.json`, `docs/coop/design-corrections/foundation/source-pins.v1.json`, `docs/coop/design-corrections/native/check_native_evidence.v2.py`, `docs/coop/design-corrections/native/native-cases.v2.json`, `docs/coop/design-corrections/native/native_evidence_model.v2.py`, `docs/coop/design-corrections/native/provider-startup.schemas.v1.json`, `docs/coop/design-corrections/native/source-pins.v2.json`, `docs/coop/design-corrections/security/source-pins.v1.json`, `docs/coop/design-corrections/workflows/source-pins.v1.json`, `docs/coop/design-corrections/workflows/workflows-report.v1.json`, `docs/v2/architecture/implementation-coverage.v1.json`, `docs/v2/architecture/implementation-planning-sources.v1.json`, `docs/v2/contracts/product-v1/native-evidence.md`

Added files: `docs/v2/architecture/implementation-normative-inputs.v13.json`

## Issues

No MUST issue. No SHOULD issue. No new advisory. ADV42-01 and ADV44-01 are retained as non-blocking advisories.

### ADV42-01 (ADVISORY, source42 review (retained; not new in source45)): Execution-inputs admission neither states nor checks that a complete receipt's view outputRefs carry that receipt's producerClosure, and raises the section 3 PLAN_JOIN only for candidate views whose producer matches some row; Run closure is the backstop

**Current standing.** RETAINED ADVISORY, NON-BLOCKING. The root implementation verification obligation for crates/host/src/analysis.rs remains correctly scoped; it is not a containment proof and no control was executed for it.

**Standing assessment.** Every selector owner is byte-identical 44->45 ({"execution-inputs-contract.v1.md": true, "execution_inputs_model.v1.py": true, "execution-inputs.schema.v1.json": true, "execution_inputs_fixture.v3.py": true, "identity-model.v3.py": true, "identity-schemas.v3.json": true}): source45 touches no execution-inputs, identity or capture byte. The ported measurement re-observes the source44 values exactly. J1 refuses EXECUTION_INPUTS_PLAN_JOIN. J2 and J3 admit at execution-inputs admission, and close_run refuses them with CLOSURE_FIELD_KIND:view.producerClosure:provider. Receipt/view producer equality and the plan check before the row filter are still not enforced at execution-input admission. The two-provider shape remains unexercised, and the fixture keeps its recorded multi-provider construction limitation. No measured world admits a contradictory Run. The source45 closed-world correction mints only host-derived provider-unavailable coverage and adds no view or receipt path, so it creates no contradiction with the advisory and no reason to reopen it.

- docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md:12 (section 1: receipts rooted in producer obligations; outputRefs constrained by domain only)
- execution-inputs-contract.v1.md:51 and :53 (section 3: stage-spec producerClosure and view planId checks; "a candidate view whose planId is not the Plan's refuses EXECUTION_INPUTS_PLAN_JOIN")
- execution-inputs-contract.v1.md:299 (section 8: the builder places each explicit returned view on the view stage whose producerClosure it carries)
- docs/coop/design-corrections/foundation/execution_inputs_model.v1.py:1057-1093 (receipt checks compare receipt and stage spec, never an outputRef view producer)
- execution_inputs_model.v1.py:1132-1139 (the per-row producer filter precedes the planId check)
- execution_inputs_model.v1.py:1626-1640 (an attributed view is compared with the producer of its ROW's receipt, not of the receipt that lists it)
- docs/coop/design-corrections/foundation/identity-model.v3.py:1842-1851 and identity-schemas.v3.json byField view.producerClosure=provider (Run closure: VIEW_PLAN_JOIN, UNSELECTED_PRODUCER, closure kind)

**Detail.** A captured, unattributed view whose producerClosure is not the receipt's producer admits at execution-inputs admission on source40, source41 and source42, even with a foreign planId, and the complete Run refuses it only at closure (CLOSURE_FIELD_KIND:view.producerClosure:provider). A foreign-planId view from the stage's own provider refuses EXECUTION_INPUTS_PLAN_JOIN as section 3 says, because it passes a row's producer filter first. By reading, the model never compares a complete receipt's outputRef views with that receipt's producerClosure, and it checks attributed views against their own row's receipt. In a Plan with two view stages of two Plan-selected providers, a view of provider P2 listed on P1's complete receipt would therefore pass admission and the closure checks measured here. No maintained multi-provider graph exists, so that shape was not exercised.

**Consequence.** No Run closes with the measured shapes; for them the contract's named refusal and the refusing owner differ. The unexercised multi-provider shape would be a self-contradictory stage-return record, a detectable host capture error rather than an omission. It is not attribution nondeterminism for one captured observation, and it is pre-existing since source40.

**Disposition.** ADVISORY, non-blocking; retained with owner routing (foundation execution-inputs owner for the optional contract clarifications; crates/host/src/analysis.rs implementation verification obligation at final application / implementation).

**Measured on source45**

```json
{
 "sameProviderForeignPlanId": {
  "admission": {
   "result": "REFUSE",
   "refusals": [
    "EXECUTION_INPUTS_PLAN_JOIN"
   ]
  },
  "fullRun": {
   "closed": false,
   "refused": "AdmissionError:REFERENCE_PLAN_JOIN"
  },
  "onRows": []
 },
 "foreignProducerSamePlan": {
  "admission": {
   "result": "ADMIT",
   "refusals": []
  },
  "fullRun": {
   "closed": false,
   "refused": "AdmissionError:CLOSURE_FIELD_KIND:view.producerClosure:provider"
  },
  "onRows": []
 },
 "foreignProducerForeignPlan": {
  "admission": {
   "result": "ADMIT",
   "refusals": []
  },
  "fullRun": {
   "closed": false,
   "refused": "AdmissionError:CLOSURE_FIELD_KIND:view.producerClosure:provider"
  },
  "onRows": []
 },
 "observedEqualToSource44Receipt": true
}
```

### ADV44-01 (ADVISORY, source44 review (retained; not new in source45)): Planning layer v12 binds the new typescript-semantic order table but not the rust-semantic protocol3 transition table, whose normative OpenUniverse state-update text and published annotations changed in source44

**Current standing.** RETAINED ADVISORY, NON-BLOCKING. The optional direct planning-input coverage of the protocol3 table and fact-batch v3 is still not taken up; neither document changed in source45.

**Standing assessment.** v13 correctly binds the two changed normative inputs, native-evidence.md and provider-startup.schemas.v1.json, and preserves v8-v12 byte-identically. The only changed self-declared normative documents it does not bind are the planning records themselves (['docs/v2/architecture/implementation-coverage.v1.json', 'docs/v2/architecture/implementation-normative-inputs.v13.json', 'docs/v2/architecture/implementation-planning-sources.v1.json']), which the layer standing excludes to avoid a self-hash cycle. protocol3-transitions.v1.json and fact-batch.schema.v3.json remain unbound and unchanged 44->45, so the source44 asymmetry persists without widening. No normative content is lost, because both restate law bound through native-evidence section 9.

- docs/v2/architecture/implementation-normative-inputs.v12.json (34 inputs: the 31 of v11 plus provider-handshake, provider-startup and typescript-protocol2-order; native-evidence.md updated; standing: "Exact normative/reference inputs consumed by implementation planning")
- docs/coop/design-corrections/native/protocol3-transitions.v1.json:99 (stateUpdates: dependencyMode/preparedMode as host-derived observations) and :129-145 (derivedObservations, rowPayloads); standing "NORMATIVE and CLOSED"
- docs/v2/contracts/product-v1/native-evidence.md section 9.2 (the Rust major-3 transition table) and section 9.7 :3193-3203 (derived modes)
- docs/operations/check_implementation_planning.py:1-44, 255-292 (binding rule: every coverage source must be in the selected layer; no rule for other normative documents)
- fact-batch.schema.v3.json ("CURRENT selected"; description, whenAbsent, commitments and wireProjection changed) and execution-inputs-contract.v1.md (changed wording) are likewise not layer inputs

**Detail.** v12 binds exactly the coverage sources (34), so the checker passes, and it correctly binds the one changed contract (native-evidence.md) and the three new incorporated documents while preserving v8-v11 byte-identically. The layer standing claims the exact normative/reference inputs consumed by planning, and it adds the typescript-semantic order table. It does not add the rust-semantic protocol3 transition table, although native-evidence section 9.2 names that table as the transition authority and source44 changed its normative OpenUniverse state update (frame booleans became host-derived observations) and added rowPayloads naming the new startup schemas. No layer v8-v12 has ever bound protocol3-transitions.v1.json or fact-batch.schema.v3.json, so this asymmetry predates source44; source44 is the first change that edits the P3 table's normative text while binding its TypeScript counterpart.

**Consequence.** No normative content is lost to planning. Every changed statement restates law bound through native-evidence sections 9.1, 9.2, 9.6 and 9.7 and through the bound provider-startup x-opensip-startup-law. The P3 rules, phases, wildcards and initial state are unchanged, and the final candidate manifest binds all bytes. A planning consumer reading v12 alone simply does not see the P3 derived-observation annotations next to the TypeScript table.

**Disposition.** ADVISORY, non-blocking. Optional planning-owner improvement: in a future layer, bind protocol3-transitions.v1.json (and fact-batch.schema.v3.json) as incorporated inputs, or state in the layer standing that native tables referenced by native-evidence.md are bound through the formal subject manifest.

**Measured on source45**

```json
{
 "v13Inputs": 34,
 "v13ChangedVsV12": [
  "docs/coop/design-corrections/native/provider-startup.schemas.v1.json",
  "docs/v2/contracts/product-v1/native-evidence.md"
 ],
 "protocol3AndFactBatchV3BoundByV13": {
  "docs/coop/design-corrections/native/protocol3-transitions.v1.json": false,
  "docs/coop/design-corrections/native/fact-batch.schema.v3.json": false
 },
 "protocol3AndFactBatchV3Unchanged44to45": {
  "protocol3-transitions.v1.json": true,
  "fact-batch.schema.v3.json": true
 },
 "changedSelfDeclaredNormativeDocumentsNotBoundByV13": [
  "docs/v2/architecture/implementation-coverage.v1.json",
  "docs/v2/architecture/implementation-normative-inputs.v13.json",
  "docs/v2/architecture/implementation-planning-sources.v1.json"
 ]
}
```

## Observations (not defects)

- **OBS45-01** Against root-source45-final-reference.v1 and codex final-reference.v45, all six group stdouts are byte-equal (True), and 15 of 17 child stdouts are byte-equal to root. Enumeration and execution-inputs differ from root only in path fields. Against this origin's source44 receipts, all six group stdouts are byte-equal and the same two children differ only in path fields; the native checker still reports 477/477. The codex runner-original equals the root reference-checks (True), and codex adds the formal subject binding (['currentProfilePinsSha256', 'standing', 'subjectManifestSha256']). (receipts/reference-comparison.json)
- **OBS45-02** The root reference and the root companion checks v2 were executed from a pre-freeze working tree (['/private/tmp/opensip-design-corrections/source44-closed-world-successor.v1/source']), not the frozen archive; companion v1 lacked the planning --source argument and is retained. The recorded script shas equal the frozen source45 bytes, all six group stdouts are byte-equal to this review's own runs, and the companion stdout text equals this review's planning and inventory output (True). This review's own executions are the acceptance input. (receipts/reference-comparison.json; receipts/planning-checks.json)
- **OBS45-03** Ten ported scope probes re-observe every value of this origin's source44 receipts on source45 (policy 26, native 39, runterm 24, query 98, carrier 108, comparison 28, repair2 16, term7 24, custody 20, capture-joins 4). The re-executed 162-row source44 startup discriminator is row-for-row identical (162 rows, 0 differing). This is corroboration, not fresh assessment. (receipts/ported45-vs44.json; receipts/probes/startup44-reexec-on45.json)
- **OBS45-04** Consumer effect of the fixed record. The workflows repair gate is the conjunction of deadCodeRepairEligible over the selected records (workflows 815-819), so a relevant universe whose only records are pre-analysis conversions stays ineligible. `RepairPlanDescriptor.closedWorld` (workflows 937-968) reduces each member to the least-closed value among the selected records. The display sentinel with nothing selected uses `nonliteralLoading: present`, the least-closed pole, to stand for absence. A summary whose selected records are all pre-analysis conversions therefore displays nonliteralLoading none and entryPointsRecognized none while exportsClosed is unknown and the boolean is false. That summary is non-authoritative (workflows 970-972), and section 9.7 (3259-3261) states that the fixed value proves no absence of dynamic loading or dispatch. This is display semantics, not a contradiction, and it predates source45: the source44 helper produced the same record. (workflows-and-surfaces.md 800-974 (read); receipts/probes/closed-world45.json)
- **OBS45-05** Editorial only: provider-target-attribution-return.schema.v2.json x-opensip-return-law.missingAndIncomplete.missingToken now reads "Historical the historical per-language payload (...)", a duplicated word in an annotation. Meaning is clear, and no $defs, property or registered shape changed (P45-CLOSED-WORLD shape rows). (receipts/delta-diffs-44to45/docs__coop__design-corrections__foundation__provider-target-attribution-return.schema.v2.json.diff)
- **OBS45-06** native-cases.v2.json was reindented: the text diff is 57096 lines, but the parsed structures differ only in the two pre-analysis conversion cases, which each add closedWorld expectations (TS 2, Rust 1). All 125 fixtures, the other 475 cases, case order and top-level members are equal. Neither source44 nor source45 bytes equal a stock json.dumps re-serialisation at indent none/1/2/4, so the whitespace layout is an author formatting choice; semantic identity is established structurally. (receipts/probes/cases-structure45.json)
- **OBS45-07** Law derivation boundary. Section 4.5 forces exportsClosed unknown, entryPointsRecognized none and deadCodeRepairEligible false for a conversion that observes no manifest and no recognizer. nonliteralLoading none, dynamicDispatch not-applicable, externalConsumers unknown and reasons ["no-manifest"] are not forced by 4.5; they are the published section 9.7 choice. ClosedWorldV2 has no unknown member for nonliteralLoading or dynamicDispatch, consistent with workflows 963-968. The disclaimer is text-only, and the value cannot enable closed exports or dead-code repair. (receipts/probes/closed-world45.json)
- **OBS45-08** Checker binding scope. check_native_evidence compares the law member, the helper's no-observation result and the first JSON fence of section 9.7 by parsed equality. Section 9.7 contains exactly one fence today, so a later fence placed before it would change which block is checked. The case expectations pin the minted entries independently of the checker, and all three mutation variants were refused with their exact faults. (receipts/probes/checker-binding45.json)
- **OBS45-09** Committed bytes. The published record's canonical JSON is {"deadCodeRepairEligible":false,"dynamicDispatch":"not-applicable","entryPointsRecognized":"none","exportsClosed":"unknown","externalConsumers":"unknown","nonliteralLoading":"none","reasons":["no-manifest"]} with SHA-256 bfffe09eee9f35181c414360a8e050c1ff73987855966b05ef6ed525214132e3. The pre-analysis entries minted by the source45 exchange are byte-identical to those minted by the source44 exchange, and their coverage identities are equal (TS ['coverage2:4fa63caae7a0a098f83b9b3632080bce6fcf0f5352b27be4de118b4c4d847cfe', 'coverage2:579461055bf30746c0129e67b473eed5f61ee0ee1b22f90bfe358e0cb8bbbdf0']; Rust ['coverage2:2dc6cb417fc4f0e972f01ebb070a9949e5567e49c010b2726f4a7e8f45f20a55']). Package RunIds are unchanged, so the correction publishes law without changing any retained or derived identity. (receipts/probes/closed-world45.json)
- **OBS45-10** The source44 reference-scope limits remain material and unchanged by source45. The reference takes planned stages, verified descriptors and the Plan identity row as trusted host inputs (OBS44-05, re-observed). It does not validate every provider-authored descriptor member, every Cancel/Cancelled correlation or Rust Cancelled phase, recomputes no stream or coverage commitment (OBS44-06/07), and exercises no framing, process or compiler. The closed-world discriminator is a measured subset of reference host-conversion behaviour over fixture inputs, not executed proof of the normative requirement in a product. (receipts/probes/startup44-reexec-on45.json; native-evidence.md 3304-3313 (read))

## Current dispositions of prior findings, advisories and observations

| id | current disposition | basis | reasoning |
|---|---|---|---|
| S40-01 | REMAINS RESOLVED ON SOURCE45 | unchanged-44-basis | The execution-inputs contract, schema, model and fixture and the enumeration contract/model are byte-identical 44->45 ({"execution-inputs-contract.v1.md": true, "execution-inputs.schema.v1.json": true, "execution_inputs_model.v1.py": true, "execution_inputs_fixture.v3.py": true, "enumeration-contract.v1.md": true, "enumeration_model.v1.py": true}), so the source44 assessment of the section 3 attribution predicate and section 8 capture exactness stands. Corroboration: the execution-inputs (95 cases) and enumeration (54 cases) children equal root and this origin's source44 receipts after removing path fields only, and the capture-join measurement is identical. |
| ADV40-01 | REMAINS RESOLVED ON SOURCE45 | new-45 | implementation-planning-sources.v1.json now selects v13 (af2283254928...) as current with v12 as previous and moves the v11 record into the prior-layer history (11 records, digests matching bytes: True). Layers v8-v12 are byte-identical to source44 ({'8': True, '9': True, '10': True, '11': True, '12': True}). No historical layer was mutated. |
| ADV42-01 | RETAINED ADVISORY (see advisories) | unchanged-44-basis | RETAINED ADVISORY, NON-BLOCKING. The root implementation verification obligation for crates/host/src/analysis.rs remains correctly scoped; it is not a containment proof and no control was executed for it. |
| ADV44-01 | RETAINED ADVISORY (see advisories) | new-45 | RETAINED ADVISORY, NON-BLOCKING. The optional direct planning-input coverage of the protocol3 table and fact-batch v3 is still not taken up; neither document changed in source45. |
| OBS44-01 | SUPERSEDED BY OBS45-01 (historical comparison not relabelled) | new-45 | The source44 comparison stays historical; the source45 comparison is OBS45-01. |
| OBS44-02 | SUPERSEDED BY OBS45-02 (historical record not relabelled) | new-45 | The source44 working-tree execution record stays historical; the source45 equivalent is OBS45-02. |
| OBS44-03 | RETAINED (OBS45-03) | new-45 | The ported probes re-observe every value on source45. |
| OBS44-04 | RETAINED OBSERVATION | unchanged-44-basis | rustCommitHash owners unchanged: the handshake schema, wire model and registered bundle are byte-identical 44->45 ({"provider-handshake.schemas.v1.json": true, "provider_wire_model.v1.py": true, "native-evidence.schemas.v2.json": true}), and the startup schema $defs are unchanged (only its x-opensip-startup-law annotation changed). |
| OBS44-05 | RETAINED OBSERVATION (OBS45-10) | new-45 | The re-executed startup discriminator re-observes the trusted plannedStages, raised host invariant and unjoined universe members identically. Source45 changes only the closedWorld construction. |
| OBS44-06 | RETAINED OBSERVATION | unchanged-44-basis | TS order table, protocol3 table and startup model byte-identical 44->45 ({"typescript-protocol2-order.v1.json": true, "protocol3-transitions.v1.json": true, "provider_startup_model.v1.py": true}); cancellation and exit asymmetries re-observed. |
| OBS44-07 | RETAINED OBSERVATION (OBS45-10) | new-45 | The section 9.7 reference-scope paragraph (3304-3313, read) is unchanged in wording, and commitments are still not recomputed (re-observed). |
| OBS44-08 | RETAINED OBSERVATION | unchanged-44-basis | Registered bundle and handshake schema byte-identical 44->45 (True, True). |
| OBS44-09 | HISTORICAL; STANDS | unchanged-44-basis | It concerns the source44 root clarification's before-bytes; source45 does not revisit it. |
| OBS44-10 | RETAINED OBSERVATION | unchanged-44-basis | provider_attribution_return_model.v2.py byte-identical 44->45 (True); the attribution-return schema changed only annotation prose (OBS45-05). |
| OBS44-11 | SUPERSEDED BY THE PACKAGE22 EQUIVALENT (packageAssessment) | new-45 | The bound package22 verification again differs from the root pre-binding verification only in package identity and file count. |
| OBS43-01 | RETAINED OBSERVATION (on source45) | unchanged-44-basis | Source44 disposition RETAINED OBSERVATION. The query projection contract, model, checker, surface projection and graph-query schema are byte-identical 44->45 ({"query-projection-contract.v3.md": true, "query_projection_model.v3.py": true, "check-query-projection.v3.py": true, "query_surface_projection.v3.py": true, "graph-query.schema.json": true}). |
| OBS43-02 | RETAINED OBSERVATION (on source45) | unchanged-44-basis | Source44 disposition RETAINED OBSERVATION. The query projection contract, model, checker, surface projection and graph-query schema are byte-identical 44->45 ({"query-projection-contract.v3.md": true, "query_projection_model.v3.py": true, "check-query-projection.v3.py": true, "query_surface_projection.v3.py": true, "graph-query.schema.json": true}). |
| OBS43-03 | RETAINED OBSERVATION (on source45) | unchanged-44-basis | Source44 disposition RETAINED OBSERVATION. The query projection contract, model, checker, surface projection and graph-query schema are byte-identical 44->45 ({"query-projection-contract.v3.md": true, "query_projection_model.v3.py": true, "check-query-projection.v3.py": true, "query_surface_projection.v3.py": true, "graph-query.schema.json": true}). |
| OBS43-04 | SUPERSEDED BY OBS44-01 (historical comparison not relabelled) (on source45) | unchanged-44-basis | Source44 disposition SUPERSEDED BY OBS44-01 (historical comparison not relabelled). The query projection contract, model, checker, surface projection and graph-query schema are byte-identical 44->45 ({"query-projection-contract.v3.md": true, "query_projection_model.v3.py": true, "check-query-projection.v3.py": true, "query_surface_projection.v3.py": true, "graph-query.schema.json": true}). |
| OBS43-05 | SUPERSEDED BY OBS44-02 (historical record not relabelled) (on source45) | unchanged-44-basis | Source44 disposition SUPERSEDED BY OBS44-02 (historical record not relabelled). The query projection contract, model, checker, surface projection and graph-query schema are byte-identical 44->45 ({"query-projection-contract.v3.md": true, "query_projection_model.v3.py": true, "check-query-projection.v3.py": true, "query_surface_projection.v3.py": true, "graph-query.schema.json": true}). |
| OBS43-06 | RETAINED (OBS44-03) (on source45) | unchanged-44-basis | Source44 disposition RETAINED (OBS44-03). The query projection contract, model, checker, surface projection and graph-query schema are byte-identical 44->45 ({"query-projection-contract.v3.md": true, "query_projection_model.v3.py": true, "check-query-projection.v3.py": true, "query_surface_projection.v3.py": true, "graph-query.schema.json": true}). |
| OBS43-07 | HISTORICAL; STANDS (query model unchanged 43->44) (on source45) | unchanged-44-basis | Source44 disposition HISTORICAL; STANDS (query model unchanged 43->44). The query projection contract, model, checker, surface projection and graph-query schema are byte-identical 44->45 ({"query-projection-contract.v3.md": true, "query_projection_model.v3.py": true, "check-query-projection.v3.py": true, "query_surface_projection.v3.py": true, "graph-query.schema.json": true}). |
| OBS42-01 | RETAINED OBSERVATION (on source45) | unchanged-44-basis | Source44 disposition RETAINED OBSERVATION (on source44). execution_inputs_model.v1.py and execution_inputs_fixture.v3.py are byte-identical 44->45 (True, True). |
| OBS42-02 | RETAINED OBSERVATION (on source45) | new-45 | Source44 disposition RETAINED OBSERVATION (on source44). enumeration-contract.v1.md is byte-identical 44->45 (True); native_evidence_model.v2.py changed only in the pre-analysis closedWorld construction and a comment (complete diff read), so the binder shorthand is unchanged. |
| OBS42-03 | RETAINED OBSERVATION (not re-probed) (on source45) | unchanged-44-basis | Source44 disposition RETAINED OBSERVATION (not re-probed) (on source44). execution_inputs_model.v1.py and execution_inputs_fixture.v3.py are byte-identical 44->45 (True, True). |
| OBS42-04 | RETAINED OBSERVATION (not re-probed) (on source45) | unchanged-44-basis | Source44 disposition RETAINED OBSERVATION (not re-probed) (on source44). execution_inputs_model.v1.py and execution_inputs_fixture.v3.py are byte-identical 44->45 (True, True). |
| OBS42-05 | RETAINED OBSERVATION (on source45) | unchanged-44-basis | Source44 disposition RETAINED OBSERVATION (on source44). enumeration_model.v1.py byte-identical 44->45 (True). |
| OBS42-06 | RETAINED OBSERVATION (on source45) | unchanged-44-basis | Source44 disposition RETAINED OBSERVATION (on source44). enumeration_model.v1.py byte-identical 44->45 (True). |
| OBS42-07 | SUPERSEDED BY OBS43-04 (historical comparison not relabelled) (on source45) | unchanged-44-basis | Source44 disposition SUPERSEDED BY OBS43-04 (historical comparison not relabelled) (on source44). Historical comparison records stay historical; the source45 comparison is OBS45-01 and the ported re-observation OBS45-03. |
| OBS42-08 | RETAINED (OBS43-06) (on source45) | unchanged-44-basis | Source44 disposition RETAINED (OBS43-06) (on source44). Historical comparison records stay historical; the source45 comparison is OBS45-01 and the ported re-observation OBS45-03. |
| OBS40-01 | RETAINED-OBSERVATION (on source45) | new-45 | Source44 disposition RETAINED-OBSERVATION (on source44). On source45 the owning probe P45-PORTED-POLICY re-observes every row identically (26 rows). |
| OBS40-02 | RETAINED-OBSERVATION (on source45) | new-45 | Source44 disposition RETAINED-OBSERVATION (on source44). On source45 the owning probe P45-PORTED-POLICY re-observes every row identically (26 rows). |
| OBS40-03 | RETAINED-OBSERVATION (OBS42-08) (on source45) | new-45 | Source44 disposition RETAINED-OBSERVATION (OBS42-08) (on source44). On source45 the owning probe P45-PORTED-POLICY re-observes every row identically (26 rows). |
| OBS40-04 | RETAINED-OBSERVATION (on source45) | new-45 | Source44 disposition RETAINED-OBSERVATION (on source44). On source45 the owning probe P45-PORTED-NATIVE re-observes every row identically (39 rows). |
| OBS40-05 | RETAINED-OBSERVATION (on source45) | new-45 | Source44 disposition RETAINED-OBSERVATION (on source44). On source45 the owning probe P45-PORTED-NATIVE re-observes every row identically (39 rows). |
| OBS40-06 | RETAINED-OBSERVATION (on source45) | new-45 | Source44 disposition RETAINED-OBSERVATION (on source44). On source45 the owning probe P45-PORTED-NATIVE re-observes every row identically (39 rows). |
| OBS40-07 | CLOSED (on source45) | unchanged-44-basis | Source44 disposition CLOSED (on source44). execution_inputs_model.v1.py and execution_inputs_fixture.v3.py are byte-identical 44->45 (True, True). |
| OBS40-08 | SUPERSEDED (historical comparison not relabelled) (on source45) | unchanged-44-basis | Source44 disposition SUPERSEDED (historical comparison not relabelled) (on source44). Historical comparison records stay historical; the source45 comparison is OBS45-01 and the ported re-observation OBS45-03. |
| OBS40-09 | RETAINED (OBS42-08) (on source45) | new-45 | Source44 disposition RETAINED (OBS42-08) (on source44). On source45 the owning probe P45-PORTED-POLICY re-observes every row identically (26 rows). |
| OBS40-10 | HISTORICAL CORRECTION STANDS (on source45) | new-45 | Source44 disposition HISTORICAL CORRECTION STANDS (on source44). The mapping population is 322 on source44 and source45; six native-evidence rows changed only selector lines and section digests, and no row id was added or removed (measured). |
| S39-01 | REMAINS CLOSED (on source45) | new-45 | Source44 disposition REMAINS CLOSED (on source44). On source45 the owning probe P45-PORTED-POLICY re-observes every row identically (26 rows). |
| S39-02 | REMAINS CLOSED (on source45) | new-45 | Source44 disposition REMAINS CLOSED (on source44). On source45 the owning probe P45-PORTED-POLICY re-observes every row identically (26 rows). |
| ADV39-01 | REMAINS CLOSED (on source45) | new-45 | Source44 disposition REMAINS CLOSED (on source44). On source45 the owning probe P45-PORTED-RUNTERM re-observes every row identically (24 rows). |
| ADV38-01 | REMAINS CLOSED (on source45) | new-45 | Source44 disposition REMAINS CLOSED (on source44). On source45 the owning probe P45-PORTED-TERM7 re-observes every row identically (24 rows). |
| ADV38-02 | REMAINS CLOSED (on source45) | new-45 | Source44 disposition REMAINS CLOSED (on source44). On source45 the owning probe P45-PORTED-CARRIER re-observes every row identically (108 rows). |
| ADV38-03 | REMAINS CLOSED (on source45) | unchanged-44-basis | Source44 disposition REMAINS CLOSED (on source44). commit-recovery-readonly.v3.md and carrier-dispatch.v3.json are byte-identical 44->45 (True, True). |

## Item dispositions

### CH45-CLOSED-WORLD-LAW: SUFFICIENT AND CONSISTENT; A MISSING NORMATIVE RECIPE IS NOW PUBLISHED; SCOPE CORRECT

Source44 section 9.7 and the startup law named closed_world_v2 over "no manifest, no recognized entry points and no edges" without publishing its output, so the exact record was fixed only by the Python helper. Source45 publishes the complete record in section 9.7 (3241-3261) and as provider-startup x-opensip-startup-law.preAnalyzeUnavailable.hostConversionClosedWorld; the hostConversion text now points to it "identically for both languages". Both copies equal the independently read value by parse and by this review's canonical bytes. Derived from published law without the helper, using section 4.5 (2208-2258) and registered ClosedWorldV2 (bundle 1112-1180). exportsClosed must be unknown: closed needs ingredient 1, an observed manifest publishing nothing, and open needs an observed published entry. entryPointsRecognized is none because no recognizer or explicit origin exists before analysis. deadCodeRepairEligible is false because it needs closed, all and no nonliteral loading. The other four members (nonliteralLoading none, dynamicDispatch not-applicable, externalConsumers unknown, reasons ["no-manifest"]) are lawful enum values fixed by the new publication rather than forced by 4.5. The derivation equals the published value, and the value cannot enable closed exports or repair (OBS45-07). Scope: the text limits the value to this pre-analysis host conversion, records absent manifest and analysis observations, disclaims any proof that the repository has no dynamic loading or dispatch, and keeps coverage unknown and repair ineligible. No other ClosedWorldV2 producer is restricted, and the checker comment says so explicitly. Registered bundle bytes are unchanged, and the startup and attribution-return schema $defs are unchanged; only x- annotations changed.

### CH45-BOTH-LANGUAGES-AND-COMMITTED-BYTES: CONFIRMED FOR BOTH LANGUAGES; NO IDENTITY CHANGE

typescript-semantic (two planned stages) and rust-semantic (one) pre-analysis conversions on source45 reach DONE unavailable (T2-10/T2-20/T2-21 and P3-21/P3-31/P3-32). Every minted entry carries exactly the published record and admits through admit_coverage_result_v3, and all source45 case expectations hold. The same exchanges on the verified source44 copy mint byte-identical CoverageResultV3 payloads with equal coverage2 identities, and the payload canonical bytes recomputed with this review's own serializer equal the foundation canonical form. The correction therefore publishes law that source44 already produced: committed bytes are reproducible across versions and from the published record, and package RunIds are unchanged (OBS45-09). The value is language-independent by construction (no cargo or package manifest branch applies), and the prose says both languages.

### CH45-CORRECTED-BOUNDARY: CONFIRMED: MODEL, CASES AND CHECKER NOW BIND THE PUBLISHED LAW

Model: pre_analyze_unavailable_conversion now deep-copies STARTUP.LAW hostConversionClosedWorld instead of calling closed_world_v2 (complete model diff read; `import copy` present). Positive reachability first, then a targeted discrimination. Mutating the in-process law member on source45 changes the minted closedWorld, and the source45 case expectations fail on it; restoring it passes again. The equivalent helper mutation on source44 changes the minted record, but the source44 cases do not detect it, because they carried no closedWorld expectation. That is the gap closed. Checker (scratch copy, native pins regenerated inside scratch so the law checks are reached): unmutated passes 477/477. Mutating the law member alone is refused with "pre-analysis closedWorld differs from the exact section 9.7 record", and both conversion cases also fail. Mutating the section 9.7 record alone is refused with "section 9.7 does not publish the exact complete pre-analysis closedWorld record". Mutating the retained helper alone is refused with "pre-analysis closedWorld differs from the retained helper's no-observation result", with cases still passing, which confirms the conversion no longer depends on the helper. The restored scratch passes, and its bytes equal the verified copy. These are reference self-consistency controls; the decisive law assessment is CH45-CLOSED-WORLD-LAW (OBS45-08).

### CH45-CONSUMER-IMPACT: CONSISTENT; DISPLAY-ONLY OBSERVATION

The only product consumer of ClosedWorldV2 members beyond the per-entry record is the workflows repair law, read at 800-974. Its selection is by relevant sourceUniverse, and its gate is the conjunction of deadCodeRepairEligible, so a pre-analysis conversion record cannot make repair eligible and yields REPAIR.CLOSED_WORLD_NOT_ESTABLISHED remedies carrying reasons ["no-manifest"]. dynamicDispatch is not read by the gate. The five-field display summary may show nonliteralLoading none for conversion-only selections, but it is non-authoritative and disclaimed (OBS45-04). workflows-and-surfaces and the repair schema and selection model are byte-identical 44->45 ({"workflows-and-surfaces.md": true, "repair_closed_world_selection.v1.py": true, "evaluator3/repair.schema.json": true}).

### CH45-HISTORICAL-BATCH-PROSE: CONSISTENT; EDITORIAL DUPLICATION NOTED

provider-target-attribution-return.schema.v2.json replaces three generic "Historical FactBatchV2" statements (standing, boundary.compilerWorkerTransport, missingAndIncomplete.missingToken) with the per-language historical payloads: delivery.v2 FactBatchV1 for typescript-semantic and rust-provider-protocol.v2 FactBatchV2 for rust-semantic. This matches section 0, section 9.6 and fact-batch v3 as assessed on source44. Only x-opensip-return-law changed; there are no $defs or property changes, and the registered-schema shapes stay unchanged (measured). One editorial duplicated word remains (OBS45-05). Earlier generic readings were ambiguous under those bytes and are not relabelled as reader errors.

### CH45-NATIVE-CASES-REINDENT: CONFIRMED: TWO SEMANTIC EXPECTATION ADDITIONS; REST WHITESPACE

native-cases.v2.json was reindented: the text diff is 57096 lines, but the parsed structures differ only in the two pre-analysis conversion cases, which each add closedWorld expectations (TS 2, Rust 1). All 125 fixtures, the other 475 cases, case order and top-level members are equal. Neither source44 nor source45 bytes equal a stock json.dumps re-serialisation at indent none/1/2/4, so the whitespace layout is an author formatting choice; semantic identity is established structurally. Both changed cases add only closedWorld expectations for every planned stage; no step, fixture or other expectation changed. The rationale's "two semantic case additions" are therefore additions inside two existing cases, not new case ids.

### CH45-PLANNING-V13: CONFIRMED (binds the actual changed normative inputs; predecessors preserved); ADV44-01 RETAINED

v13 (af2283254928...) binds 34 inputs with no mismatch: v12 with native-evidence.md and provider-startup.schemas.v1.json updated, and nothing added or removed. All 34 coverage sources are bound, and exactly those two changed. Layers v8-v12 are byte-identical to source44. The planning sources select v13, keep v12 as previous and record v11 in the history. The planning checker reports 322 source-bound mappings and 54 planned failure cases, and the inventory checker 198 paths in 20 packages; stdout equals the companion v2 (True). The six changed mapping rows (native-evidence sections 9-14) change only selector line numbers and section value digests. There are 24 report features, M0-M6, and 54 recovery cases, none executed. The only architecture files changed are the three planning records. The unbound changed self-declared normative documents are the planning records themselves (excluded by standing).

### CH45-PINS-AND-REPORTS: CONFIRMED

All 6264 entries of the five ledgers match the formal manifest (foundation 1252, evaluator3 1256, native 1252, security 1252, workflows 1252), with none added or removed. The union of changed pins is the attribution schema, checker, cases, model, startup schema, native-evidence.md and the sibling ledgers. The delta files pinned by no ledger are the planning records, the workflows report and the evaluator3 ledger itself. The workflows report updates only the workflows source-pins digest. The generated native report bytes are unchanged 44->45 (True): 477 cases, and its providerStartup summary carries no closedWorld count.

### CH45-PACKAGE22: VERIFIED AS AUTHOR EVIDENCE; RUNIDS UNCHANGED (MEASURED)

See packageAssessment.

### CH45-CURRENT-REFERENCE: OWN EXECUTION PASSES; ROOT RECEIPTS CONSISTENT

This review's six groups and 17 children pass on its own verified copy, unchanged before and after every group: native 477/477, query-projection 209 checks with 0 failed, execution-inputs 95, enumeration 54. The comparison is OBS45-01 and OBS45-02; historical source44 receipts are preserved and not relabelled.

### CH45-UNCHANGED-WIRE-STARTUP-BASIS: SOURCE44 PROVIDER WIRE/STARTUP ASSESSMENTS STAND ON NAMED UNCHANGED OWNERS

The source44 wire and startup items stand as individually named unchanged-44 basis, not relabelled fresh. Owner bytes: {"provider-handshake.schemas.v1.json": true, "provider_wire_model.v1.py": true, "provider_startup_model.v1.py": true, "typescript-protocol2-order.v1.json": true, "protocol3-transitions.v1.json": true, "fact-batch.schema.v3.json": true, "occupancy-companion.schema.v1.json": true, "provider_attribution_return_model.v2.py": true, "delivery.v2.json": true, "rust-provider-protocol.v2.json": true, "native-evidence.schemas.v2.json": true}. The wire discriminator (130 rows) was not re-executed because none of its owners changed; the startup discriminator (162 rows) was re-executed because the native model changed, and it is identical.

| source44 item | source44 disposition | unchanged basis on source45 |
|---|---|---|
| CH44-WIRE-HANDSHAKE | SUFFICIENT AND CONSISTENT (both languages) | handshake schema, wire model, delivery.v2 and rust-provider-protocol.v2 byte-identical; not re-executed |
| CH44-FACTBATCH-AND-OCCUPANCY | SUFFICIENT AND CONSISTENT; HISTORICAL WORDING DISAMBIGUATED, NOT RELABELLED | fact-batch v3, occupancy companion and attribution model byte-identical; the attribution-return schema changed annotation prose only (CH45-HISTORICAL-BATCH-PROSE); not re-executed |
| CH44-STARTUP-OPEN-UNIVERSE | SUFFICIENT AND CONSISTENT; HOST CONSTRUCTION TRUSTED (OBS44-05) | startup model byte-identical; startup schema $defs unchanged; the startup discriminator re-executed identically |
| CH44-PRE-ANALYZE-UNAVAILABLE | SUFFICIENT AND CONSISTENT; CONVERSION OVER TRUSTED PLANNED STAGES | payload, phase, correlation and process-fault law unchanged; the conversion closedWorld is now published (CH45 items); re-executed identically |
| CH44-COVERAGE-AND-CANCELLATION | SUFFICIENT AND CONSISTENT | TS order table and protocol3 table byte-identical; re-executed identically |
| CH44-RUST-COMMIT-REPRESENTATION | NO JOINED EQUALITY REQUIRED BEYOND THE 64-HEX PLAN/HANDSHAKE/UNIVERSE CHAIN; CONSISTENT | identity owners byte-identical |
| CH44-CROSS-OWNER-CONSISTENCY | CONSISTENT; NO FIELD OR ROUTE CONTRADICTION FOUND | section 0 and the other cross-owner texts outside the section 9.7 closedWorld hunk unchanged |

### CH45-SCOPE-PRESERVATION: SOURCE44 SCOPE RETAINED; NAMED BASIS

Each retained scope names its current source45 execution and its individually named unchanged-44 basis. Passing suites are corroboration, not assessment. The source45 change reaches native section 9.7, the startup law, the native model conversion, the checker, two cases and the attribution-return annotations. Its consumer effect on the workflows repair owner, whose bytes are unchanged, is assessed in CH45-CONSUMER-IMPACT.

| scope | basis | current source45 evidence | unchanged-44 basis |
|---|---|---|---|
| five product contracts and incorporated schemas | new-45 (native 9.7) + unchanged-44-basis (others) | identity, security, workflows and admission contracts and the README index byte-identical ({"identity-and-evidence.md": true, "security-and-lifecycle.md": true, "workflows-and-surfaces.md": true, "admission-and-qualification.md": true, "README.md": true}); native-evidence changed only in section 9.7 (complete diff read; section 9.7 read completely); provider-startup changed only its law annotation; all six groups pass | source44 AR row assessments for byte-identical contracts; inheritedUnchanged44Read whole-file reads |
| architecture, tool, layout and report decisions | unchanged-44-basis + current execution | 40 docs/v2/architecture files; only the three planning records changed; planning and inventory checks pass | source44 layout, build-plan and inventory decisions on byte-identical bytes |
| 198 files in 20 packages; 322 mappings; M0-M6; 24 report features; 54 recovery cases | current execution | measured: 198 paths, 20 packages, 322 mappings (6 rows with selector-line/digest updates only), M0-M6, 24 report features, 54 recovery cases not executed | - |
| native discovery, config, unitKind, allowJs, nested Cargo, clone normalization, custody | new-45 diff + current execution | the native model delta is confined to the pre-analysis conversion closedWorld line and a comment; native group 477/477; native-consumer24-corrections {'stdoutEqualRoot': True, 'stdoutEqualHistoricalMine44': True} and native-replay {'stdoutEqualRoot': True, 'stdoutEqualHistoricalMine44': True}; ported native (39 rows) and custody (20 rows) identical to source44; nine native-v2 membership probes content-equal to root | source44 native discovery/custody assessments on unchanged code |
| enumeration default-vs-explicit binding, attribution and capture | unchanged-44-basis + current execution | enumeration and execution-inputs owners byte-identical; children equal root and own source44 after removing path fields only; capture-join measurement identical; package binding-controls content-equal to root | source44 S40-01 and ADV42-01 assessments on byte-identical owners |
| policy.test known-hit, universe and import | unchanged-44-basis + current execution | ported policy probe 26 rows identical; policy-derivation child {'stdoutEqualRoot': True, 'stdoutEqualHistoricalMine44': True} | policy_test_model.v3.py unchanged (True) |
| comparison counterfactuals, knowledge and identities | unchanged-44-basis + current execution | ported comparison probe 28 rows identical; comparison-knowledge child {'stdoutEqualRoot': True, 'stdoutEqualHistoricalMine44': True} | source44 AR-10/AR-11 |
| nine command carriers and twenty operations; query availability, path, cursor and diagnostic decisions | unchanged-44-basis + current execution | ported query carriers 98 rows identical; query-projection 209 checks pass; query owners and command inventory byte-identical ({"query-projection-contract.v3.md": true, "query_projection_model.v3.py": true, "check-query-projection.v3.py": true, "query_surface_projection.v3.py": true, "graph-query.schema.json": true, "command-inventory.v3.json": true}) | CH43-AVAILABILITY-REPORTING, CH43-OBSERVATION-GRANTS-NOTHING, CH43-PATH-EDGE-ORIENTATION, CH43-CURSOR-BOUNDS-AND-PROSE (source43 items carried through source44 on byte-identical query owners) |
| repair2 | unchanged-44-basis + current execution | ported repair:2 probe 16 rows identical | repair_closed_world_selection.v1.py unchanged (True) |
| security, discovery, commit, recovery and read-only carrier boundaries | unchanged-44-basis + current execution | security group stdout equal root, codex and own source44; ported read-only carrier 108 rows and run-termination/commit-inventory 24 rows identical | carrier-dispatch.v3.json (True) and commit-recovery-readonly.v3.md (True) unchanged |
| evaluator, import and termination bridges | unchanged-44-basis + current execution | children full-replay {'stdoutEqualRoot': True, 'stdoutEqualHistoricalMine44': True}, execution-replay {'stdoutEqualRoot': True, 'stdoutEqualHistoricalMine44': True}, candidate-replay {'stdoutEqualRoot': True, 'stdoutEqualHistoricalMine44': True}, composition {'stdoutEqualRoot': True, 'stdoutEqualHistoricalMine44': True}, analysis-seal {'stdoutEqualRoot': True, 'stdoutEqualHistoricalMine44': True}, provider-attribution-return {'stdoutEqualRoot': True, 'stdoutEqualHistoricalMine44': True}, faults {'stdoutEqualRoot': True, 'stdoutEqualHistoricalMine44': True}, atoms {'stdoutEqualRoot': True, 'stdoutEqualHistoricalMine44': True}; ported section 7 termination 24 rows identical | composition, replay and identity owners byte-identical (True, True, True) |

| ported probe | rows | same case set as source44 | observations differing from source44 |
|---|---|---|---|
| P45-PORTED-POLICY | 26 | True | none |
| P45-PORTED-NATIVE | 39 | True | none |
| P45-PORTED-RUNTERM | 24 | True | none |
| P45-PORTED-QUERY | 98 | True | none |
| P45-PORTED-CARRIER | 108 | True | none |
| P45-PORTED-COMPARISON | 28 | True | none |
| P45-PORTED-REPAIR2 | 16 | True | none |
| P45-PORTED-TERM7 | 24 | True | none |
| P45-PORTED-CUSTODY | 20 | True | none |
| P45-PORTED-CAPTURE-JOINS | 4 | True | none |

## Package v22

Package v22 verified as author evidence. All 387 files match artifact manifest 03e35dc6...; the formal45 manifest 8b4efbb0... and the files-only projection 6a66d599... are different objects with equal file members (equal to this review's own verified manifest45 index), and the package copy of the formal manifest equals the live one. The rebuild (report c3e00832...) ran on frozen candidate-subject.v45 from package15 constructors (6a8d4fec...) plus the native-v2 migration overlay (overlay base digests match retained package15); packages 16-21 remain unchanged history, and the pre-binding package 50ea28c7... is retained inside package22 and equals the rebuild output. Metadata binding changed no export store or current replay helper byte. Every current export store is byte-equal to package21 at the same path, and the 17 measured RunIds and export digests equal the source44 rebuild, so the source45 correction does not alter any retained identity and nothing was reminted. This review re-executed verify-package.py and probe-native-v2.py on its own verified source45 copy: groups checkpoint3 1 (passed True, exit 0), normalized-examples6 4 (passed True, exit 0), rust-selection-examples1 2 (passed True, exit 0), semantic-controls1 3 (passed True, exit 1), binding-controls 3 (passed True, exit 1), normalization-map-controls1 4 (passed True, exit 1), query 7 (passed True, exit None); 17 exports and 7 queries. The verification of bound package22 equals the root verification of the pre-binding package except package identity and file count, every other output file is byte-equal, and the 9 membership comparisons are content-equal to the root rebuild probe.

Measured RunIds (17): `run3:111b6787faf1f2b3ac87bf06d49548fabb5517c15345301d88935327b9cffde3`, `run3:1a22aedd9488cd4ae9a52948fb7d6bab7cab894f8f03d07cd27106c46ab1f562`, `run3:28f72aa09e72928a22894de02569b322d702771f4821baeebe14703b1f63102d`, `run3:2e2e33c2abe280859a6c80513b3f8cc46a0de5307246edafc01c0bba34c41c91`, `run3:436519cef5d15be8a2e40e3093d7128a78eaab2cfb08c50100fb4a0af03f932b`, `run3:51e0318f0e9b2174e8df2c93fe77e6d0a21694f77fb8698ce709cdda07bc8019`, `run3:52cae22644baa89e2cc9455cad99cafb5516cf84c8ca2d9b01313d7f09b7601d`, `run3:52cae22644baa89e2cc9455cad99cafb5516cf84c8ca2d9b01313d7f09b7601d`, `run3:5dced4e0aefde0842c0247e6cf620d51d307891a76819e319ab085536954f909`, `run3:67947edc8cca117d7efe044306f4574fd2066dc22ae2e7381fe235eee13ec1bb`, `run3:8c135158ac25071331f656a953952d780b366ff42b5f83d43ab44a0c63c0826f`, `run3:b009ae65bf2954f319ddac7211f7eb76e346a10ee6bafb44d5fbbc26c21dba1d`, `run3:b193caaf82b361a6f97d7cadfc82821837829b55edd069878ceace836081ab45`, `run3:b5b86d6fd4144674216576572e3ac884fb19d3cfb750373c1d3a27a4a8d8ff1f`, `run3:d5e396e6d99601eee06015989e06295918bae989b1edd9403591cf6621320cdb`, `run3:e69a549c8fd9395ead86c514c921d135ed4fa0289443263a367e8c669acd2cfc`, `run3:e9aed8ce5dde727cf4929737c9be8ade1f3643ad39695f4ac9f4f225af3aaabd`

- Author construction and self-consistency evidence; verify-package.py and probe-native-v2.py are author tools re-executed here, not an independent or blind reconstruction.
- Four TypeScript normalization-map negatives ARE executed (exact refusals below). The Rust map negative is unexercised.
- The partial and/or/not consumer helper remains unexercised; count-at-most/all-covered remain unimplemented; two-binding qualification is incomplete.
- No compiler, provider, OS or process-isolation qualification; independent grades granted: 0; all 30 author-proposed grades stay PENDING final application.

| control | owner admission | semantic admission | reason |
|---|---|---|---|
| ts-map-absent | REFUSE | NOT-REACHED | BODY_NORMALIZATION_MAP_MISSING:opensip-interface/normalization/specification-map.v1.json |
| ts-map-level-unmapped | REFUSE | NOT-REACHED | BODY_NORMALIZATION_LEVEL_UNMAPPED:L0-verbatim |
| ts-map-level-swapped | REFUSE | NOT-REACHED | BODY_NORMALIZATION_LEVEL_VERSION_MISMATCH:L0-verbatim |
| ts-spec-outside-closure | REFUSE | NOT-REACHED | BODY_NORMALIZATION_SPECIFICATION_NOT_IN_CLOSURE:L0-verbatim |

## Commands and probes

| group | exit | seconds | stdout sha256 | equal root | equal codex | equal own source44 |
|---|---|---|---|---|---|---|
| evaluator3 | 0 | 510.0 | `2ddf8f99c46365462636ae191ff71c1800424e00c460fc335bc47f9a3659ef1b` | True | True | True |
| foundation | 0 | 131.6 | `bed9cf468e21e96428750551d36a6fb71fac816b92485dc3e0561a32f3c80497` | True | True | True |
| integration | 0 | 16.4 | `3fccd9e3a400774d6f411e530a22848ec38eae5a30e737f4c66bf75254d20112` | True | True | True |
| native | 0 | 3.2 | `3bfd3c46eff6a2f95f288cef44ebdf3429f373a694a0bd7973b4592b8a36878c` | True | True | True |
| security | 0 | 1.0 | `60d498d317776373a82f941db5a82a78b5eca33ba6d8f57eeb387a9a081ca746` | True | True | True |
| workflows | 0 | 9.6 | `973db2f1d7468567e04c0153323ec4d4746bf77aff2797c8d58fe32c4b7cb8dc` | True | True | True |

evaluator3 children: 17, all exit 0: True; query-projection checks 209 (failed 0); execution-inputs cases 95; enumeration cases 54. Native: PASS: 477/477 cases; matrix cells 66; open objects 0; uncovered feedback []. Planning: {'check_implementation_planning': 'PASS: 322 source-bound mappings, 54 planned failure cases, private schema, owners and generated plan', 'check_repository_file_inventory': 'PASS: 198 unique paths, naming/ownership checks, acyclic package dependencies, chapter matches'}. Planning counts ok: True.

| probe | rows | failed | run receipt | earlier attempts |
|---|---|---|---|---|
| P45-SUBJECT | (command receipt) | - | receipts/subject-verification.json, receipts/manifest45-index.json, receipts/manifest44-index.json | - |
| P45-ARCHIVE | (command receipt) | - | receipts/archive-verification.source45.json, receipts/archive-verification.source45-pkg.json, receipts/archive-verification.base44.json | - |
| P45-DELTA | (command receipt) | - | receipts/delta-diff-summary.json | - |
| P45-GROUPS | (command receipt) | - | receipts/reference/groups-report.all.json, receipts/reference/evaluator3.stdout, receipts/reference/foundation.json | - |
| P45-REFERENCE-COMPARE | - | 0 | receipts/runs/reference-comparison-v45.run.json | 0 |
| P45-PINS | - | 0 | receipts/runs/source-pins45.run.json | 0 |
| P45-PLANNING | - | 0 | receipts/runs/planning-checks-v45.run.json | 0 |
| P45-CASES-STRUCTURE | - | 0 | receipts/runs/cases-structure45.run.json | 0 |
| P45-CLOSED-WORLD | 19 | 0 | receipts/runs/probe-closed-world45.run.json | 0 |
| P45-CHECKER-BINDING | 6 | 0 | receipts/runs/probe-checker-binding45.run.json | 0 |
| P45-PORT | - | 0 | receipts/runs/port-v44-probes.run.json | 0 |
| P45-PORTED-POLICY | 26 | 0 | receipts/runs/ported45-policy-v40.run.json | 0 |
| P45-PORTED-NATIVE | 39 | 0 | receipts/runs/ported45-native-v40.run.json | 0 |
| P45-PORTED-RUNTERM | 24 | 0 | receipts/runs/ported45-runterm-adv-v40.run.json | 0 |
| P45-PORTED-QUERY | 98 | 0 | receipts/runs/ported45-query-carriers.run.json | 0 |
| P45-PORTED-CARRIER | 108 | 0 | receipts/runs/ported45-carrier-readonly.run.json | 0 |
| P45-PORTED-COMPARISON | 28 | 0 | receipts/runs/ported45-comparison-knowledge.run.json | 0 |
| P45-PORTED-REPAIR2 | 16 | 0 | receipts/runs/ported45-repair2.run.json | 0 |
| P45-PORTED-TERM7 | 24 | 0 | receipts/runs/ported45-run-termination-s7.run.json | 0 |
| P45-PORTED-CUSTODY | 20 | 0 | receipts/runs/ported45-native-custody-fallback.run.json | 0 |
| P45-PORTED-CAPTURE-JOINS | 4 | 0 | receipts/runs/ported45-capture-joins.run.json | 0 |
| P45-PORTED-VS44 | - | 0 | receipts/runs/ported45-vs44.run.json | 0 |
| P45-STARTUP-REEXEC-PORT | - | 0 | receipts/runs/port-startup-reexec45.run.json | 0 |
| P45-STARTUP-REEXEC | 162 | 0 | receipts/runs/reexec45-startup.run.json | 0 |
| P45-PACKAGE22 | 34 | 0 | receipts/runs/probe-package-v22.run.json | 0 |
| P45-COPIES-FINAL | - | 0 | receipts/runs/copies-final.run.json | 0 |

## Read coverage

Whole-file claims only for fresh45Read (every line read this charter) and inheritedUnchanged44Read (counted as completely read by this origin's completed source44 review and byte-identical now; not re-read). complete44ReadPlusComplete45Diff is a complete predecessor read plus the exact diff. Delta reads, range reads, structural comparisons, evidence reads and search-only sightings are not whole-file reads of source45 bytes. Hashes recomputed at build time.

```json
{
 "fresh45Read": 0,
 "fresh45RangeRead": 6,
 "deltaReads": 14,
 "deltaFilesStructurallyCompared": 1,
 "complete44ReadPlusComplete45Diff": 3,
 "inheritedUnchanged44Read": 59,
 "changedPriorReadNotReread": 0,
 "evidenceReads": 4,
 "searchOnlySightings": 6
}
```

Delta files without a read entry: none.

Delta files compared structurally: docs/coop/design-corrections/native/native-cases.v2.json (reindented reference data (57,096 text-diff lines): the complete parsed structures of source44 and source45 were compared - every top-level member, all 125 fixtures and all 477 cases by id and order - and the two changed cases' full expectation deltas were printed and read; this is a complete structural comparison, not a text read of the diff).

Fresh whole-file reads:

- none

Range reads:

- docs/coop/design-corrections/native/check_native_evidence.v2.py: 40-119,264-313 (sha256 `797b40e7811e07082917fae153c85e35e800eccd1d5296b70e277ab076741ac6`)
- docs/coop/design-corrections/native/native-evidence.schemas.v2.json: 1110-1189 (sha256 `2d37b810bd9ffed741d74241fc8a11051606862d8af2f152eed16b92bdc66043`)
- docs/coop/design-corrections/native/native_evidence_model.v2.py: 1545-1689 (sha256 `7d1c0acf2c7d74e52c6570bba66dcb846c03710f64cb61a2c83bd1c39abab8be`)
- docs/coop/design-corrections/native/provider-startup.schemas.v1.json: 1-110 (sha256 `1e35a77bae8d9c20171a934e9c16e4de4d7ce98bb024016d7e17cf9b0b38729c`)
- docs/v2/contracts/product-v1/native-evidence.md: 2010-2039,2195-2264,3151-3316 (sha256 `83b99783893bec4bcca76bc043310e1d33305fc41ef85e012fbcb19e5b222ca0`)
- docs/v2/contracts/product-v1/workflows-and-surfaces.md: 800-974 (sha256 `1ee203e3ce626d88a53d0247881cd3ffb0d52b421821ac798b9f0b57346ff6ed`)

Complete diff reads:

- docs/coop/design-corrections/foundation/evaluator3-source-pins.v1.json (delta44to45Read; diff `c6c8d392eccfafa31b669ad3d2c820b4a2a5b00bbd63ce8e30ad617292ea4621`)
- docs/coop/design-corrections/foundation/provider-target-attribution-return.schema.v2.json (delta44to45Read; diff `3fa0065f74c5cf3ef63c1c0baf0d726ef223b9031954c719fc898f2352a3761b`)
- docs/coop/design-corrections/foundation/source-pins.v1.json (delta44to45Read; diff `139e57a12b157bb51370950d835a66ea7feca8a2656e46703bff0986547a3952`)
- docs/coop/design-corrections/native/check_native_evidence.v2.py (delta44to45Read; diff `055ea4f699afca7aef68ab2fd2c7d6651bee22226a4699f804a1eff58674b06c`)
- docs/coop/design-corrections/native/native_evidence_model.v2.py (delta44to45Read; diff `7047c267011cb504fb3c72aac870fb66a98e636315c6b2bf73ba22ed52c80034`)
- docs/coop/design-corrections/native/provider-startup.schemas.v1.json (delta44to45Read; diff `042a4230386708a8bc9dd6d94887967ba3a02cb3b65891a0f966a456bf850d3a`)
- docs/coop/design-corrections/native/source-pins.v2.json (delta44to45Read; diff `ca09e90287490b82ceff53f0b2068e693063aa3d12666303d41e15c73e16b554`)
- docs/coop/design-corrections/security/source-pins.v1.json (delta44to45Read; diff `7acea9c98e2e6a101fe514a9b3ec358b889bb3bb4a630a07786dcb00e2818a23`)
- docs/coop/design-corrections/workflows/source-pins.v1.json (delta44to45Read; diff `531653d8d736ee5f2718b656f86980dae940fa6400a02c49ad9346330326f238`)
- docs/coop/design-corrections/workflows/workflows-report.v1.json (delta44to45Read; diff `b6f00046c5365beaa02c085338f8f3def5fc8c43701196e57d6c821a5a4119a5`)
- docs/v2/architecture/implementation-coverage.v1.json (delta44to45Read; diff `d40df4ecc2617121d188c5d1131e5f74df9428fb19016b61547d562e3dfacbea`)
- docs/v2/architecture/implementation-normative-inputs.v13.json (delta44to45Read; diff `d110073bcc78bbf102e532a8d885780dbf399a35b8ccb69d5cd88b3f190fdfe5`)
- docs/v2/architecture/implementation-planning-sources.v1.json (delta44to45Read; diff `461a35eff2ea3d40033a7aa975bad27a83033e67626655aa10c604fb468e5346`)
- docs/v2/contracts/product-v1/native-evidence.md (delta44to45Read; diff `7d14b22c68bf1957463886c8181082adc66696c9188426538fe4dfec112b1d9f`)

Evidence reads:

- /Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/root-source45-companion-checks.v2/checks.json: complete
- /tmp/opensip-design-corrections/claude-author-package-successor.v22/source-binding.v45.json: complete
- /tmp/opensip-design-corrections/root-author-package-final45-rebuild.v1/rebuild-report.json: inputs verification-head exportComparison
- /tmp/opensip-design-corrections/root-author-package-formal45-binding.v1/binding.json: complete

Search-only sightings (not reads):

- docs/v2/contracts/product-v1/native-evidence.md: 2027, 2210-2213, 2221, 2237-2254, 3242-3255, 3352, 3368, 4175 (closed-world member search output; 2010-2039, 2195-2264 and 3151-3316 were then read) — search output outside the ledgered ranges
- docs/v2/contracts/product-v1/workflows-and-surfaces.md: 815, 835, 841-842, 938-964 (search output; 800-974 then read) — search output within the later read range
- docs/coop/design-corrections/workflows/{workflows_model.v1.py, workflow-cases.v1.json, schemas/repair.schema.json, schemas/imported-evidence.schema.json, schemas/evaluator3/repair.schema.json, repair_closed_world_selection.v1.py, command-inventory.v3.json, command-inventory.v1.json, check-workflow-projection.v3.py}; docs/coop/design-corrections/foundation/{incoming-search.schema.v1.json, check-identity.py, check-atoms.v1.py, atom_model.v1.py, atom-evaluation-contract.v1.md}: file names only (ClosedWorldV2 member consumer search, files-with-matches output) — file names only; consumer law read in workflows-and-surfaces 800-974
- docs/coop/design-corrections/native/check_native_evidence.v2.py: def/marker lines 79-624 (search output); 40-119 and 264-313 then read; the changed region 573-594 read as the complete diff — search output
- docs/coop/design-corrections/native/{native_evidence_model.v2.py, native-evidence.schemas.v2.json}: imports 12-21, def lines 1545/1645, ClosedWorldV2 1112/1116/1176 (search output) — search output; 1545-1689 and 1110-1189 then read
- codex-post-reset.v1/final-reference.v45/*: file listing (glob) — names only; reference files compared by hash

Inherited unchanged source44 whole-file reads (not re-read): 59 files; complete source44 read plus complete 44->45 diff: 3 (docs/coop/design-corrections/native/provider-startup.schemas.v1.json, docs/v2/contracts/product-v1/native-evidence.md, docs/coop/design-corrections/foundation/provider-target-attribution-return.schema.v2.json); listed in review.json.

## TCB-SCOPE-01 (assessed once)

**Assumption.** Authenticated selected in-process host/evaluator code is trusted; providers and inert inputs are untrusted; adversarial code sharing the process is outside the product threat model.

**Consequence.** Rejecting or changing the assumption reopens the thirteen dependent rows jointly, not as thirteen independent proofs. It repairs no historical attack and qualifies no containment. All thirteen author grades stay PENDING.

**Dependent rows (13).** RES-EP13-02, RES-EP13-04, RES-EP13-12, RES-EP13-13, RES-EP13-16, RES-EP13-18, IR-EP13-NB-01, IR-EP13-NB-03, IR-EP13-NB-04, AX6, AX9, MD5, RX2c

**Current assessment.** NOT REJECTED: coherent as a scope selection on source45 and unqualified; the source45 correction publishes host law and adds no trust.

- Coherent: admission section 5 (byte-identical 44->45: True) and prototype-report-inventory (byte-identical: True) still admit no untrusted native/WASM, imperative contributions or executable report hooks.
- Providers stay untrusted: the pre-analysis closedWorld is host-minted from published law, and no provider-authored member reaches it; the provider-side startup admissions are unchanged (re-execution identical).
- Host inputs and loaded law stay TCB: planned stages remain trusted host inputs, and the in-process law member is mutable by same-process code (measured), which this assumption places outside the threat model.
- View producer closures must still be Plan-selected providers at Run closure (CLOSURE_FIELD_KIND re-measured on source45).
- Unqualified: it rests on the authenticated closure/TCB inventory and provider process boundaries; all 32 gates are unperformed (qualified=true 0).

**Position:** NOT REJECTED. **Standing:** ASSESSED-COHERENT-UNQUALIFIED-ON-SOURCE45; final application adjudication not granted. **Adjudication owner:** separate final application review, by a NEW different actual Claude origin (not this origin 85a08aec-9d22-4ac6-8ec2-c10170e727d7 and not any author, design or blind origin)

## Disposition rows (107)

All rows: appliedByThisReview=false, finalApplicationOutcomeGranted=false. No grade is assigned; scoped owner rows are routing only.

**Basis rule.** unchanged-44-basis: the named governing owner bytes (unchanged44GoverningOwners) are byte-identical 44->45, and the conclusion rests on that identity plus this origin's named source44 row assessment, quoted in unchanged44Basis. Re-executed suites and ported probes are corroboration only. new-45: the conclusion rests on a source45 read, diff, probe or measurement newly performed under this charter, including rows whose owners are unchanged but whose governing law, closed-world consumer or trust account is touched by the source45 correction. Every row carries its own current text, current owner and consequence. No row is carried forward in bulk, and no grade is assigned. Counts: {"new-45": 34, "unchanged-44-basis": 73}.

| id | prior44 | disposition | basis | current assessment | owner | consequence |
|---|---|---|---|---|---|---|
| F-01 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | unchanged-44-basis | F-01: prior root standing RE-VERIFIED-ON-PACKAGE13 (root-independent36-completion-assessment.v1) carried without regrade on source45. The F record lives outside the frozen snapshot, and none of the 15 source44->45 delta files is an F record. | root custody of the F record (outside the frozen snapshot) | No source45 change; remains carried without regrade and is not source45 acceptance. |
| F-02 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | unchanged-44-basis | F-02: prior root standing RE-VERIFIED-ON-PACKAGE13 (root-independent36-completion-assessment.v1) carried without regrade on source45. The F record lives outside the frozen snapshot, and none of the 15 source44->45 delta files is an F record. | root custody of the F record (outside the frozen snapshot) | No source45 change; remains carried without regrade and is not source45 acceptance. |
| F-03 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | unchanged-44-basis | F-03: prior root standing RE-VERIFIED-ON-PACKAGE13 (root-independent36-completion-assessment.v1) carried without regrade on source45. The F record lives outside the frozen snapshot, and none of the 15 source44->45 delta files is an F record. | root custody of the F record (outside the frozen snapshot) | No source45 change; remains carried without regrade and is not source45 acceptance. |
| F-04 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | unchanged-44-basis | F-04: prior root standing INHERITED (root-independent36-completion-assessment.v1) carried without regrade on source45. The F record lives outside the frozen snapshot, and none of the 15 source44->45 delta files is an F record. | root custody of the F record (outside the frozen snapshot) | No source45 change; remains carried without regrade and is not source45 acceptance. |
| F-05 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | unchanged-44-basis | F-05: prior root standing RE-VERIFIED-ON-PACKAGE13 (root-independent36-completion-assessment.v1) carried without regrade on source45. The F record lives outside the frozen snapshot, and none of the 15 source44->45 delta files is an F record. | root custody of the F record (outside the frozen snapshot) | No source45 change; remains carried without regrade and is not source45 acceptance. |
| F-06 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | unchanged-44-basis | F-06: prior root standing RE-VERIFIED-ON-PACKAGE13 (root-independent36-completion-assessment.v1) carried without regrade on source45. The F record lives outside the frozen snapshot, and none of the 15 source44->45 delta files is an F record. | root custody of the F record (outside the frozen snapshot) | No source45 change; remains carried without regrade and is not source45 acceptance. |
| F-07 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | unchanged-44-basis | F-07: prior root standing INHERITED (root-independent36-completion-assessment.v1) carried without regrade on source45. The F record lives outside the frozen snapshot, and none of the 15 source44->45 delta files is an F record. | root custody of the F record (outside the frozen snapshot) | No source45 change; remains carried without regrade and is not source45 acceptance. |
| F-08 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | unchanged-44-basis | F-08: prior root standing RE-VERIFIED-ON-PACKAGE13 (root-independent36-completion-assessment.v1) carried without regrade on source45. The F record lives outside the frozen snapshot, and none of the 15 source44->45 delta files is an F record. | root custody of the F record (outside the frozen snapshot) | No source45 change; remains carried without regrade and is not source45 acceptance. |
| F-09 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | unchanged-44-basis | F-09: prior root standing INHERITED (root-independent36-completion-assessment.v1) carried without regrade on source45. The F record lives outside the frozen snapshot, and none of the 15 source44->45 delta files is an F record. | root custody of the F record (outside the frozen snapshot) | No source45 change; remains carried without regrade and is not source45 acceptance. |
| F-10 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | unchanged-44-basis | F-10: prior root standing RE-VERIFIED-ON-PACKAGE13 (root-independent36-completion-assessment.v1) carried without regrade on source45. The F record lives outside the frozen snapshot, and none of the 15 source44->45 delta files is an F record. | root custody of the F record (outside the frozen snapshot) | No source45 change; remains carried without regrade and is not source45 acceptance. |
| F-11 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | unchanged-44-basis | F-11: prior root standing RE-VERIFIED-ON-PACKAGE13 (root-independent36-completion-assessment.v1) carried without regrade on source45. The F record lives outside the frozen snapshot, and none of the 15 source44->45 delta files is an F record. | root custody of the F record (outside the frozen snapshot) | No source45 change; remains carried without regrade and is not source45 acceptance. |
| F-12 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | unchanged-44-basis | F-12: prior root standing RE-VERIFIED-ON-PACKAGE13 (root-independent36-completion-assessment.v1) carried without regrade on source45. The F record lives outside the frozen snapshot, and none of the 15 source44->45 delta files is an F record. | root custody of the F record (outside the frozen snapshot) | No source45 change; remains carried without regrade and is not source45 acceptance. |
| F-13 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | unchanged-44-basis | F-13: prior root standing RE-VERIFIED-ON-PACKAGE13 (root-independent36-completion-assessment.v1) carried without regrade on source45. The F record lives outside the frozen snapshot, and none of the 15 source44->45 delta files is an F record. | root custody of the F record (outside the frozen snapshot) | No source45 change; remains carried without regrade and is not source45 acceptance. |
| F-14 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | unchanged-44-basis | F-14: prior root standing RE-VERIFIED-ON-PACKAGE13 (root-independent36-completion-assessment.v1) carried without regrade on source45. The F record lives outside the frozen snapshot, and none of the 15 source44->45 delta files is an F record. | root custody of the F record (outside the frozen snapshot) | No source45 change; remains carried without regrade and is not source45 acceptance. |
| RES-EP13-01 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | unchanged-44-basis | Plan and derivation joins stay inside complete replay on byte-identical owners 44->45; the full-replay child equals root and this origin's source44 receipt, and the 17 package RunIds are unchanged. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING; residual retained. |
| RES-EP13-02 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-45 | Depends on TCB-SCOPE-01. The pre-analysis conversion still takes the host's planned stages as a trusted input, now with a published closedWorld record instead of a helper result (re-execution identical). Capture stays a host observation (ADV42-01 re-measured). No provider-authored field reaches the minted record. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING; reopens with TCB-SCOPE-01 only. |
| RES-EP13-03 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | unchanged-44-basis | Admission contract and residual ledger byte-identical 44->45; the finite historical measurement is unchanged on source45. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING; finite historical measurement unchanged. |
| RES-EP13-04 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-45 | Depends on TCB-SCOPE-01. Closed input admission is unchanged: the provider-startup $defs and registered bundle are unchanged, the host-minted closedWorld is a complete closed ClosedWorldV2 value admitted under the registered schema, and no open member is introduced. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING; reopens with TCB-SCOPE-01 only. |
| RES-EP13-05 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-45 | The frozen subject was verified outside every author instrument: formal45 manifest 8b4efbb0..., archive 9536ebe3..., all 12,920 members by hash and length (738,157,930 -> 738,315,211 bytes), parent44 e873c8db... (12,919 members), the declared chain, the exact 14/1/0 delta and all 6,264 pin entries. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING. |
| RES-EP13-06 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-45 | canonical.py stays outside the delta (True). The published record's canonical bytes and the minted entries' canonical bytes were recomputed with this review's own serializer, and they equal the foundation canonical form and the source44 entries. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING. |
| RES-EP13-07 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | unchanged-44-basis | Seal and replay owners byte-identical 44->45; the analysis-seal child equals root and this origin's source44 receipt on source45. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING. |
| RES-EP13-08 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | unchanged-44-basis | A bounded historical measurement. Source45 publishes one fixed conversion record and claims no proof over all PlanIntents, repositories or providers. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING. |
| RES-EP13-09 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-45 | Provenance stays distinct from correctness: the published record keeps coverage unknown, exportsClosed unknown and deadCodeRepairEligible false, and the workflows repair gate cannot turn a pre-analysis conversion into repair eligibility (CH45-CONSUMER-IMPACT). Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING. |
| RES-EP13-10 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-45 | Author self-counters did not decide this review. The checker's three new bindings and the two case expectation additions are reference self-consistency. The decisive evidence is this review's derivation from section 4.5 and the registered schema, its byte and identity comparison against source44, and its mutation discriminators (P45-CLOSED-WORLD 19 rows, P45-CHECKER-BINDING 6 rows). Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING. |
| RES-EP13-11 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-45 | Failures stay recorded by cause: no probe attempt failed this charter. Two broad glob listings timed out and returned nothing, and one shell listing was denied by the harness; both were replaced by exact-path reads. Prior charters' failed attempts stay in their own receipts. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING. |
| RES-EP13-12 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-45 | Depends on TCB-SCOPE-01. No sole Python guard enters product authority. The checker's closed-world bindings are reference consistency checks, and the case expectations pin the minted entries; a product host must mint the published record as normative law, and nothing here executes that product obligation. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING; reopens with TCB-SCOPE-01 only. |
| RES-EP13-13 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-45 | Depends on TCB-SCOPE-01. The discriminators loaded owner modules from the verified source45 and source44 copies in their own processes, and the checker mutations ran only on a disposable scratch copy; every verified copy was re-verified unchanged afterwards. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING; reopens with TCB-SCOPE-01 only. |
| RES-EP13-14 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | unchanged-44-basis | The differential census is not used as an oracle on source45; no delta file is a census owner. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING. |
| RES-EP13-15 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | unchanged-44-basis | The C-2 v4 self-census is not elevated; enumeration owners are byte-identical 44->45 and their 54 cases equal this origin's source44 receipt modulo paths. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING. |
| RES-EP13-16 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | unchanged-44-basis | Depends on TCB-SCOPE-01. Producer flags cannot bypass replay: execution-inputs owners are byte-identical 44->45 and the 95 cases equal this origin's source44 receipt modulo paths. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING; reopens with TCB-SCOPE-01 only. |
| RES-EP13-17 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-45 | Text-only disclosures remain text-only. The section 9.7 statement that the fixed record proves no absence of dynamic loading or dispatch is a disclosure paired with a non-enabling value, a checker binding and case pins; it is not a guarantee about repositories. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING. |
| RES-EP13-18 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-45 | Depends on TCB-SCOPE-01. Native discovery and custody code is unchanged: the model delta is confined to the conversion closedWorld line and a comment. Marker observations stay trusted, and ported native (39 rows) and custody (20 rows) observations are identical to source44. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING; reopens with TCB-SCOPE-01 only. |
| RES-EP13-19 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-45 | Substantive review on source45: independent law derivation, scope and both-language challenge, committed-byte and identity comparison against source44, consumer impact, planning v13 binding, and both retained advisories reassessed with current reasoning. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING. |
| IR-EP13-NB-01 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-45 | Depends on TCB-SCOPE-01. Every source45 probe ran in-process with owner modules; the in-process law-member mutation shows loaded law is mutable in-process, which is exactly the same-process boundary this assumption excludes. Containment is not claimed. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING; reopens with TCB-SCOPE-01 only. |
| IR-EP13-NB-02 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-45 | No name scan decides a product route. The checker locates the section 9.7 record by heading and code fence in reference prose (OBS45-08), a documentation consistency check with no product route. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING. |
| IR-EP13-NB-03 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-45 | Depends on TCB-SCOPE-01. Loaded owner instances stay reachable in-process: the conversion reads STARTUP.LAW by deep copy, so a same-process writer could alter a later conversion before copy, as the reviewer's mutation showed. That is outside the threat model, not a provider path. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING; reopens with TCB-SCOPE-01 only. |
| IR-EP13-NB-04 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-45 | Depends on TCB-SCOPE-01; one TCB account, assessed once on source45, covers all thirteen rows. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING; reopens with TCB-SCOPE-01 only. |
| IR-EP13-NB-05 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-45 | Contradictory or under-specified prose still needed substantive review. Source44 named an unpublished helper for a normative record; source45 publishes the record and binds prose, law and helper, and clarifies three generic historical-batch statements (one editorial duplication). Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING. |
| IR-EP13-NB-06 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | unchanged-44-basis | Historical attacker cost preserved as history; no source45 file addresses it. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING. |
| IR-EP13-NB-07 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | unchanged-44-basis | The original environment is preserved; this review names /tmp/opensip-architecture-review-env/bin/python -I -B and verifies all 6,264 pins on source45. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING. |
| AX6 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-45 | Depends on TCB-SCOPE-01. None of the 14 changed files or the added v13 layer claims same-process route-region protection (all diffs read; native-cases compared structurally). Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING; reopens with TCB-SCOPE-01 only. |
| AX9 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-45 | Depends on TCB-SCOPE-01. The fixed closedWorld record is typed host-minted data under a trusted host, not a protection mechanism. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING; reopens with TCB-SCOPE-01 only. |
| MD5 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-45 | Depends on TCB-SCOPE-01. Source45 adds no Python-containment mechanism (delta read). Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING; reopens with TCB-SCOPE-01 only. |
| RX2c | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | unchanged-44-basis | Depends on TCB-SCOPE-01. Complete replay and full-Run closure remain reproducibility evidence, not containment; replay owners byte-identical 44->45. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING; reopens with TCB-SCOPE-01 only. |
| AR-01 | NO-NEW-ISSUE | NO-NEW-ISSUE | unchanged-44-basis | Admission section 1 byte-identical 44->45; ported query carriers (98 rows) identical to source44. | docs/v2/contracts/product-v1/admission-and-qualification.md (§1) | No change required. |
| AR-02 | NO-NEW-ISSUE | NO-NEW-ISSUE | unchanged-44-basis | Admission sections 2-4 and gate ledger byte-identical 44->45: 32 gates, none qualified. | docs/v2/contracts/product-v1/admission-and-qualification.md (§§2–4) | All gates stay unperformed. |
| AR-03 | NO-NEW-ISSUE | NO-NEW-ISSUE | unchanged-44-basis | Security discovery text byte-identical 44->45; ported custody rows identical to source44. | docs/v2/contracts/product-v1/security-and-lifecycle.md (Discovery) | No change required. |
| AR-04 | NO-NEW-ISSUE | NO-NEW-ISSUE | unchanged-44-basis | Security trust time byte-identical 44->45; the security group stdout equals root, codex and this origin's source44 receipt. | docs/v2/contracts/product-v1/security-and-lifecycle.md (Trust time) | No change required. |
| AR-05 | NO-NEW-ISSUE | NO-NEW-ISSUE | unchanged-44-basis | Security root chain and revocation byte-identical 44->45; untouched by the delta. | docs/v2/contracts/product-v1/security-and-lifecycle.md (Root chain and revocation) | No change required. |
| AR-06 | NO-NEW-ISSUE | NO-NEW-ISSUE | unchanged-44-basis | Platform admission and carrier DDL byte-identical 44->45; ported read-only carrier rows (108) identical. | docs/v2/contracts/product-v1/security-and-lifecycle.md (Platform admission) | No change required. |
| AR-07 | NO-NEW-ISSUE (ADVISORY ADV44-01 ON PLANNING BINDING) | NO-NEW-ISSUE (ADVISORY ADV44-01 RETAINED) | new-45 | Native section 9 changed only in 9.7: the pre-analysis host conversion now publishes its complete closedWorld record (3241-3261), with the machine owner in the startup law. Section 9.7 was read completely, and the record was derived from law, challenged for scope and both-language applicability, and shown byte-reproducible (CH45-CLOSED-WORLD-LAW, CH45-BOTH-LANGUAGES-AND-COMMITTED-BYTES). Sections 3 and 5 are unchanged; native group 477/477. | docs/v2/contracts/product-v1/native-evidence.md (§§3/5/9) | No change required; the planning advisory stays optional. |
| AR-08 | NO-NEW-ISSUE | NO-NEW-ISSUE | unchanged-44-basis | Invocation and repair text byte-identical 44->45; ported repair:2 rows identical. | docs/v2/contracts/product-v1/workflows-and-surfaces.md (Invocation and repair) | No change required. |
| AR-09 | NO-NEW-ISSUE (ADVISORY ADV42-01 RETAINED) | NO-NEW-ISSUE (ADVISORY ADV42-01 RETAINED) | unchanged-44-basis | identity-and-evidence and identity owners byte-identical 44->45; coverage2 identities of the conversion entries equal source44; S40-01 remains resolved and ADV42-01 retained on re-measured values. | docs/v2/contracts/product-v1/identity-and-evidence.md (§§1–6) | No change required; the advisory is optional. |
| AR-10 | NO-NEW-ISSUE | NO-NEW-ISSUE | unchanged-44-basis | Baseline and comparison text byte-identical 44->45; ported comparison-knowledge rows identical. | docs/v2/contracts/product-v1/workflows-and-surfaces.md (Baseline and comparison) | No change required. |
| AR-11 | NO-NEW-ISSUE | NO-NEW-ISSUE | unchanged-44-basis | Comparison and import text byte-identical 44->45; the execution-inputs child equals root after removing path fields only. | docs/v2/contracts/product-v1/workflows-and-surfaces.md (Comparison and import) | No change required. |
| AR-12 | NO-NEW-ISSUE | NO-NEW-ISSUE | new-45 | Native section 4 text is unchanged (outside the only hunk), and section 4.5's ClosedWorldV2 law is now directly instantiated by the section 9.7 record. The derivation shows the record honours every 4.5 ingredient rule and cannot claim closed exports or repair eligibility; the atoms child equals root and source44. | docs/v2/contracts/product-v1/native-evidence.md (§4) | No change required. |
| AR-13 | NO-NEW-ISSUE | NO-NEW-ISSUE | new-45 | Native sections 1, 2, 6 and 8 lie outside the only source45 hunk (complete diff read); enumeration cases equal source44 modulo paths and the nine native-v2 membership probes equal root. | docs/v2/contracts/product-v1/native-evidence.md (§§1/2/6/8 plus workflow output/security discovery) | No change required. |
| AR-14 | NO-NEW-ISSUE | NO-NEW-ISSUE | unchanged-44-basis | Stage transition and lease bytes unchanged 44->45; no delta file is a lifecycle owner. | docs/v2/contracts/product-v1/security-and-lifecycle.md (Stage transition and lease model) | No change required. |
| AR-15 | NO-NEW-ISSUE | NO-NEW-ISSUE | unchanged-44-basis | Contract index README and D-372 application text byte-identical 44->45. | docs/v2/contracts/product-v1/README.md (Entire contract index and D-372 application) | No change required. |
| AR-16 | NO-NEW-ISSUE | NO-NEW-ISSUE | new-45 | workflows-and-surfaces is byte-identical, but its repair closed-world gate and display summary consume the record source45 publishes: the gate stays refused for conversion-only selections, and the non-authoritative summary may display nonliteralLoading none (OBS45-04). No D9 code is added, and the D9 successor stays carried. | docs/v2/contracts/product-v1/workflows-and-surfaces.md (D9 and command outcomes plus native/security guidance) | No change required. |
| FW-01 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | unchanged-44-basis | discovery.rs binding construction obligation unchanged on source45; owner map and inventory byte-identical 44->45. | crates/host/src/discovery.rs (M3) | Not executed. |
| FW-02 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | unchanged-44-basis | review.rs review-brief carriers unchanged on source45; ported carriers identical. | crates/host/src/review.rs (M5) | Not executed. |
| FW-03 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | new-45 | analysis.rs composes provider work, admission and evaluation (inventory :695). For the pre-analysis native-context mismatch its host conversion must now mint exactly the published hostConversionClosedWorld for both languages, not a locally computed record. It keeps the ADV42-01 verification obligation. Owner map and inventory byte-identical 44->45. | crates/host/src/analysis.rs (M3) | Implementation obligations retained; not executed. |
| FW-04 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | unchanged-44-basis | imports.rs unchanged on source45; typed-null targetUniverse account stands. | crates/host/src/imports.rs (M5) | Not executed. |
| FW-05 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | unchanged-44-basis | comparison.rs presence knowledge unchanged on source45; ported comparison rows identical. | crates/host/src/comparison.rs (M5) | Not executed. |
| FW-06 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | unchanged-44-basis | finalization.rs delivery laws unchanged on source45; commit-inventory recipe re-derived identically. | crates/host/src/finalization.rs (M5) | Not executed. |
| FW-07 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | unchanged-44-basis | invocation.rs argvDigest unchanged on source45. | crates/host/src/invocation.rs (M5) | Not executed. |
| FW-08 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | unchanged-44-basis | outcomes.rs detail allowlist unchanged and sufficient on source45; no detail added by the closed-world correction. | crates/host/src/outcomes.rs (M3) | Not executed. |
| FW-09 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | unchanged-44-basis | review.rs candidates/inspect carriers unchanged on source45; ported carriers identical. | crates/host/src/review.rs (M5) | Not executed. |
| FW-10 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | unchanged-44-basis | repair.rs repair:2 constructor unchanged on source45; ported repair rows identical. | crates/host/src/repair.rs (M5) | Not executed. |
| FW-11 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | unchanged-44-basis | comparison.rs baseline.show unchanged on source45. | crates/host/src/comparison.rs (M5) | Not executed. |
| FW-12 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | unchanged-44-basis | review.rs produce-brief host-only unchanged on source45. | crates/host/src/review.rs (M5) | Not executed. |
| FW-13 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | unchanged-44-basis | configuration.rs policy-test admission routes unchanged on source45; ported policy rows identical. | crates/host/src/configuration.rs (M3) | Not executed. |
| FW-14 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | unchanged-44-basis | discovery.rs recommend units unchanged on source45. | crates/host/src/discovery.rs (M3) | Not executed. |
| FW-15 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | unchanged-44-basis | policy.rs show/test unchanged on source45; the policy-derivation child equals source44. | crates/host/src/policy.rs (M5) | Not executed. |
| DR-001 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-44-basis | current-source-map and residual ledgers byte-identical 44->45 on source45. Successor routing in inherited-residuals.proposed.md (byte-identical 44->45: True) is consistent with source45. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Condition-1 obligation retained. |
| DR-002 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-44-basis | ExecutionInputsV1 view attribution and exact selection remain published on byte-identical owners 44->45; S40-01 remains resolved. Successor routing in inherited-residuals.proposed.md (byte-identical 44->45: True) is consistent with source45. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Condition-1 obligation retained. |
| DR-003 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-44-basis | Read-only carrier routes unchanged 44->45; 54 recovery cases unexecuted on source45. Successor routing in inherited-residuals.proposed.md (byte-identical 44->45: True) is consistent with source45. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Condition-1 obligation retained; release demonstration still required. |
| DR-004 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-44-basis | Native binding construction consumed by enumeration unchanged; enumeration owners byte-identical 44->45. Successor routing in inherited-residuals.proposed.md (byte-identical 44->45: True) is consistent with source45. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Condition-1 obligation retained. |
| DR-005 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | new-45 | Custody reference groups pass on source45; the native model change is confined to the conversion closedWorld, and ported custody rows are identical. Native carrier qualification is still required. Successor routing in inherited-residuals.proposed.md (byte-identical 44->45: True) is consistent with source45. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Condition-1 obligation retained. |
| DR-006 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-44-basis | Descriptor graph unchanged 44->45; the full-replay child equals root and source44. Successor routing in inherited-residuals.proposed.md (byte-identical 44->45: True) is consistent with source45. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Condition-1 obligation retained. |
| DR-007 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-44-basis | The D9 published successor artifact remains a carried implementation-unit obligation; public-detail registry and workflows contract byte-identical 44->45. Successor routing in inherited-residuals.proposed.md (byte-identical 44->45: True) is consistent with source45. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Mandatory future implementation-unit obligation; not a new blocker. |
| DR-008 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-44-basis | The applied retention posture is unchanged 44->45 on source45. Successor routing in inherited-residuals.proposed.md (byte-identical 44->45: True) is consistent with source45. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Condition-1 obligation retained. |
| DR-009 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-44-basis | The host capture stays outside the sealed Run; execution-inputs model and fixture byte-identical 44->45. Successor routing in inherited-residuals.proposed.md (byte-identical 44->45: True) is consistent with source45. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Condition-1 obligation retained. |
| DR-010 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-44-basis | Bounded first-party composition unchanged 44->45 on source45. Successor routing in inherited-residuals.proposed.md (byte-identical 44->45: True) is consistent with source45. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Condition-1 obligation retained. |
| DR-011 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-44-basis | The blind implementer litmus follows final integration and is not closed by this nonblind source45 review. Successor routing in inherited-residuals.proposed.md (byte-identical 44->45: True) is consistent with source45. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Condition-1 obligation retained. |
| DR-011-R01 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-44-basis | Fact-plane successor schemas unchanged: fact-batch v3 and occupancy companion byte-identical 44->45. Successor routing in inherited-residuals.proposed.md (byte-identical 44->45: True) is consistent with source45. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Retained. |
| DR-011-R02 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-44-basis | Imperative plugins stay outside D-371 on source45. Successor routing in inherited-residuals.proposed.md (byte-identical 44->45: True) is consistent with source45. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Retained. |
| DR-011-R03 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-44-basis | plan2 EnumerationPlanV1 binding joins unchanged 44->45. Successor routing in inherited-residuals.proposed.md (byte-identical 44->45: True) is consistent with source45. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Retained. |
| DR-011-R04 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-44-basis | carrierFormat mapping unchanged 44->45 on source45. Successor routing in inherited-residuals.proposed.md (byte-identical 44->45: True) is consistent with source45. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Retained. |
| DR-011-R05 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | new-45 | Rust protocol major 3 and TypeScript major 2 unchanged; source45 changes only the startup law annotation for the pre-analysis conversion, with $defs unchanged (measured). Successor routing in inherited-residuals.proposed.md (byte-identical 44->45: True) is consistent with source45. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Retained. |
| DR-011-R06 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-44-basis | Typed close_run outcomes through the graph query unchanged; query owners byte-identical 44->45. Successor routing in inherited-residuals.proposed.md (byte-identical 44->45: True) is consistent with source45. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Retained. |
| DR-011-R07 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-44-basis | Query retained-availability routes and partial disclosure unchanged; query owners byte-identical 44->45. Successor routing in inherited-residuals.proposed.md (byte-identical 44->45: True) is consistent with source45. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Retained. |
| DR-011-R08 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-44-basis | D9 successor remains carried on source45 (DR-007). Successor routing in inherited-residuals.proposed.md (byte-identical 44->45: True) is consistent with source45. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Mandatory future implementation-unit obligation. |
| DR-011-R09 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | new-45 | Semantic identity still excludes attempt identity: the conversion entries' coverage2 identities equal source44, the 17 package export stores are byte-equal to package21, and the measured RunIds equal source44. Successor routing in inherited-residuals.proposed.md (byte-identical 44->45: True) is consistent with source45. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Retained. |
| DR-011-R10 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-44-basis | OPEN: this nonblind source45 review cannot close the fresh blind implementer litmus. Successor routing in inherited-residuals.proposed.md (byte-identical 44->45: True) is consistent with source45. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Retained open. |
| DR-011-R11 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-44-basis | Real platform durability unmeasured on source45; 54 cases not executed. Successor routing in inherited-residuals.proposed.md (byte-identical 44->45: True) is consistent with source45. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Retained. |
| DR-011-R12 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | new-45 | Depends on TCB-SCOPE-01, assessed once on source45. Successor routing in inherited-residuals.proposed.md (byte-identical 44->45: True) is consistent with source45. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Retained; reopens with TCB-SCOPE-01 only. |
| DR-011-R13 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | new-45 | Source45 adds an annotation-level law member and changes no registered schema document, schema $defs, identity record or schema major; the registered bundle digest is unchanged, consistent with the composition profile. Successor routing in inherited-residuals.proposed.md (byte-identical 44->45: True) is consistent with source45. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Retained. |
| DR-011-R14 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-44-basis | CFG-6/TM unchanged 44->45 on source45. Successor routing in inherited-residuals.proposed.md (byte-identical 44->45: True) is consistent with source45. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Retained. |
| DR-011-R15 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | new-45 | Trusted request context stays host-only: the conversion's planned stages and the published closedWorld are host inputs and host law, and none is provider-authored. Successor routing in inherited-residuals.proposed.md (byte-identical 44->45: True) is consistent with source45. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Retained. |
| DR-011-R16 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-44-basis | No executable report-hook admission; prototype-report-inventory and admission section 5 unchanged 44->45. Successor routing in inherited-residuals.proposed.md (byte-identical 44->45: True) is consistent with source45. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Retained. |
| DR-201 | ROUTING-ASSESSED-ONLY-NOT-APPLIED | ROUTING-ASSESSED-ONLY-NOT-APPLIED | new-45 | Semantic-correctness owner row: the published pre-analysis closedWorld law, its consumer effect and both retained advisories fall in its area. Register 08 byte-identical 44->45 (True). | register 08 condition-3 review owner row DR-201 | Input to the integrated review; routing only, not applied. |
| DR-202 | ROUTING-ASSESSED-ONLY-NOT-APPLIED | ROUTING-ASSESSED-ONLY-NOT-APPLIED | unchanged-44-basis | Delivery/operations owner row: recovery, repair and loader TCB unchanged 44->45. Register 08 byte-identical 44->45 (True). | register 08 condition-3 review owner row DR-202 | Input to the integrated review; routing only, not applied. |
| DR-203 | ROUTING-ASSESSED-ONLY-NOT-APPLIED | ROUTING-ASSESSED-ONLY-NOT-APPLIED | unchanged-44-basis | Prototype-lessons owner row (PARTIAL-SCOPED): no source45 delta file is the prototype reference. Register 08 byte-identical 44->45 (True). | register 08 condition-3 review owner row DR-203 | Input to the integrated review; routing only, not applied. |
| DR-204 | ROUTING-ASSESSED-ONLY-NOT-APPLIED | ROUTING-ASSESSED-ONLY-NOT-APPLIED | new-45 | V1/coop invariant owner row: all 6,264 pins verified; layer v13 binds the two changed normative inputs and preserves v8-v12 byte-identically; ADV44-01 retained. Register 08 byte-identical 44->45 (True). | register 08 condition-3 review owner row DR-204 | Input to the integrated review; routing only, not applied. |
| DR-205 | ROUTING-ASSESSED-ONLY-NOT-APPLIED | ROUTING-ASSESSED-ONLY-NOT-APPLIED | new-45 | Small-core/components owner row: TCB-SCOPE-01 remains coherent on source45; the correction is host law, not a component or trust change. Register 08 byte-identical 44->45 (True). | register 08 condition-3 review owner row DR-205 | Input to the integrated review; routing only, not applied. |

The quoted source44 basis and governing owners of every unchanged-44-basis row are in review.json (`unchanged44Basis`, `unchanged44GoverningOwners`).

## Retained obligations

```json
{
 "residuals": 30,
 "authorGradesPending": 30,
 "condition2Obligations": 28,
 "condition2Source": "docs/v2/architecture/08-decision-and-readiness-register.md:385-391 (byte-identical 44->45: True)",
 "productQualificationGates": {
  "count": 32,
  "qualifiedTrue": 0,
  "standing": "UNPERFORMED"
 },
 "plannedRecoveryCases": {
  "count": 54,
  "notExecuted": 54,
  "standing": "UNPERFORMED"
 },
 "condition5": "NOT MET (not a design defect)",
 "d9PublishedSuccessor": "Mandatory future implementation-unit obligation (DR-007 / DR-011-R08); not a newly invented design blocker.",
 "adv4201ImplementationVerification": "crates/host/src/analysis.rs verification that no returned view is listed on another producer's complete receipt (root routing; not executed).",
 "adv4401PlanningBinding": "Optional planning-owner improvement: bind protocol3-transitions.v1.json and fact-batch.schema.v3.json in a future layer, or state their binding through the formal manifest (non-blocking).",
 "closedWorldHostImplementation": "A product host must mint exactly the published hostConversionClosedWorld for pre-analysis provider-unavailable coverage in both languages (FW-03; not executed).",
 "providerImplementationObligations": "Framing, worker processes, compilers, descriptor members beyond the reference joins, Cancel/Cancelled correlation and Rust Cancelled phase, stream and coverage commitments, and host user-interruption reduction remain owned by their inherited laws and are unqualified (section 9.7 reference scope; OBS45-10).",
 "gradeAndConditionOwner": "All 30 evaluation grades and 28 condition-2 obligations belong to final application adjudication.",
 "finalApplication": "Requires a NEW different actual Claude origin, not this origin (85a08aec-9d22-4ac6-8ec2-c10170e727d7) and not any author, design or blind origin.",
 "acceptanceStanding": "Source-level acceptance only; distinct from final application, readiness and product qualification."
}
```

## Authority

```json
{
 "gradeGranted": false,
 "activationGranted": false,
 "implementationAuthorized": false,
 "blindReconstructionClaimed": false,
 "freshOriginIndependenceClaimed": false,
 "source44ReviewConclusionInherited": false,
 "frozenInputsModified": false,
 "applicationOrReadinessGranted": false,
 "productQualificationGranted": false,
 "blindConsumerArtifactsOrOutcomesAccessed": false,
 "authorRuntimeHistoriesRead": false,
 "historicalExportsRelabelled": false,
 "runIdsReminted": false,
 "productCommitPushOrActivation": false,
 "subagentsWebOrPrivateLogsUsed": false
}
```

## Limitations

- Nonblind successor review by the origin that completed the source40, 42, 43 and 44 reviews; not fresh-origin independence. No author report was header-bound for source45; the charter's source-only correction rationale was treated as author statement and re-measured. No author runtime history, blind consumer artifact, export, helper, report or root blind outcome was read; review directories named for blind consumers or root corrections that were not header-bound were not opened.
- The law derivation separates members forced by section 4.5 from members fixed by the new section 9.7 publication; the latter are assessed for lawfulness, scope and non-enabling effect, not derived as unique.
- Reference Python models over fixtures; no product code. The closed-world discriminator exercises the reference host conversion over trusted fixture host inputs; it is not complete retained Run replay and not a product host. No framing, worker, process or compiler is exercised. 32 gates and 54 recovery cases remain unperformed (condition 5 NOT MET).
- Whole-file claims are limited to fresh45Read and inheritedUnchanged44Read. native-evidence.md was read by range (4.3, 4.5, complete 9.7) plus its complete diff; the startup law object was read by range plus complete diff; native-cases was compared structurally, not read as a 57,096-line text diff.
- The source44 wire discriminator was not re-executed because its owners are byte-identical; its conclusions stand as named unchanged-44 basis. The startup discriminator was re-executed as corroboration only.
- The checker mutation probe regenerated the native pin ledger inside a disposable scratch copy so the targeted law checks could be reached; that scratch ledger is not a source artifact and no verified or frozen copy was modified.
- Ported probes keep their historical labels; only runtime paths changed, and the current side is the verified source45 copy.
- The package verifier and native probe are author tools re-executed on this review's copy; content equality with root evidence is not independent reconstruction. Four TS normalization-map negatives are executed; the Rust map negative and the partial and/or/not helper are unexercised; count/all are unimplemented; two-binding qualification is incomplete.
- Byte-identical owners outside the correction (query projection, composition, policy derivation, enumeration, identity, wire handshake) rely on this origin's named source44 assessments and were not re-read this charter.
- No grade, activation, application, readiness, implementation authorization or product qualification is granted.

## Build gaps

none
