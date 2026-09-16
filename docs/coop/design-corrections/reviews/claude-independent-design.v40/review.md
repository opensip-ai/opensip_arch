# Independent design review — source40 (whole-design successor)

**Reviewer:** Claude (independent design review origin 85a08aec-9d22-4ac6-8ec2-c10170e727d7; source40 charter; authored none of the reviewed bytes)  
**Standing:** Independent whole-design successor review of frozen source40. Not final application review, not inheritance of the source39 review, not blind reconstruction, not readiness, implementation authorization or product qualification.

## Verdict: CHANGES_REQUIRED

One SHOULD issue is unresolved (S40-01). CellProgramOutcomeV1.viewDigests attribution, and through it stage-receipt outputRefs and selectedRefs, has no published recipe. The reference decides it with an unpublished capability-relation criterion, the literal schema reading is refused, and two conforming encodings of the same stage returns both admit with different ExecutionInputsV1 digests, so different Run identities. It is pre-existing (owner bytes unchanged 39->40) and was demonstrated by reviewer-minted graphs through the maintained builder and reference admission. There is no MUST issue and no blocker. S39-01 and S39-02 are closed at source level with discriminating probes against source39 bytes; ADV39-01 is closed by an exact, truthful account; ADV38-01/02/03 remain closed; ADV40-01 is editorial. Subject, archive, all members, parent39, the delta, six pinned groups (all pass), 17 evaluator3 children, planning and inventory checks, package v17 content agreement and every reviewer probe ran to completion. Source-level result only.

## Subject

| Item | Value |
|---|---|
| subjectManifestSha256 | `3be452843acb6f5f234dfc1826b627a234d81e5a45edd70715a03715d7467072` |
| liveManifestSha256Measured | `3be452843acb6f5f234dfc1826b627a234d81e5a45edd70715a03715d7467072` |
| verifiedManifest | `True` |
| subjectFileCount | `12911` |
| subjectTotalBytes | `737700535` |
| subjectArchiveSha256 | `e9980bc4d30294380c2bb3b91d2d331419db615a7b1b6f41107c7298ba249814` |
| archiveSha256Measured | `e9980bc4d30294380c2bb3b91d2d331419db615a7b1b6f41107c7298ba249814` |
| parentManifestSha256 | `f71a59928d1b6aa84eed81b8cb49fd1fba91c65dd6599c58f99efcdc42569009` |
| parentUnchangedAndVerified | `True` |
| delta 39->40 | 22 changed, 2 added, 0 removed |
| planning input layer v9 | `75ea60653d8c7c36d754b163a11c0cd63e3d963f59ab6ccfe12c3c2a34a0d2de` |

## New issues

No MUST issue.

### S40-01 (SHOULD): Which returned views a cell/program row attributes (CellProgramOutcomeV1.viewDigests), and therefore stage-receipt outputRefs and selectedRefs, has no published recipe; the reference applies an unpublished capability-relation criterion, and two conforming encodings of the same stage returns both admit with different ExecutionInputsV1 digests

**Selectors**

- docs/coop/design-corrections/foundation/execution-inputs.schema.v1.json:621 (viewDigests: "Must equal captured receipt views attributed to this cell/program/U/producer"; the only statement of the attribution, and "attributed" is not defined)
- docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md:12-19 (section 1: the record is a host TCB observation of stage returns; stage-produced selectedRefs = union of complete receipt outputRefs; coverage = coverageIds of "those captured returned views")
- execution-inputs-contract.v1.md:51 (section 3 joins: enumerator closure, stage producerClosure, view planId, named scope sourceUniverse, receipt outputDomains; no relation or capability criterion)
- execution-inputs-contract.v1.md:114 and :219-231 (section 5 derives accounts from "this cell/program's returned views" and resolves "the views THAT cell/program returned, restricted to the binding's own enumerator/provider closure": it presupposes the attribution rather than defining it)
- execution-inputs-contract.v1.md:141-144 (a competing internally consistent rule is "exactly why the normative one is published here instead of living only in the reference implementation") and :152-158 (precedent: two admissible encodings gave conforming hosts different ExecutionInputsV1 digests, proofs and Run ids, and were closed)
- execution-inputs-contract.v1.md:294 (build_manifest: "selectedRefs = attributed views + ...", again undefined)
- docs/coop/design-corrections/foundation/execution_inputs_model.v1.py:1129-1159 (admission: a view is attributed to a row iff same producer, same Plan, some scope at binding U, and some scope relation in the cell capability matrix relations, or any such view for a capability without matrix relations; exact equality else EXECUTION_INPUTS_VIEW_TOTALITY)
- docs/coop/design-corrections/foundation/execution_inputs_fixture.v3.py:226-244 and :342-388 (the host-capture builder applies its own copy of the relation criterion and derives stage-receipt outputRefs from the attributed views)
- docs/coop/design-corrections/foundation/enumeration-contract.v1.md:17 (one cell per requested capability tuple, so a program of one language mode and workspace carries several capability cells bound to the same provider and universe; seen in search output) and native-capability-matrix.v2.json (inventory relations file/package/vcs-change; syntax declares/literal/control-flow; script-extracted)

**Measured**

```json
{
 "executionInputsOwnerBytesUnchanged39to40": true,
 "maintainedOwnerGraphRows (cellOrdinal, programOrdinal, capabilityId)": {
  "one-universe-owner-admits": [
   [
    0,
    0,
    "inventory"
   ]
  ],
  "missing-package-owner-admits": [
   [
    0,
    0,
    "inventory"
   ]
  ],
  "two-universes-owner-admits": [
   [
    0,
    0,
    "inventory"
   ],
   [
    0,
    1,
    "inventory"
   ]
  ]
 },
 "contractTextNamesViewDigests": false,
 "referenceAttributionOfMintedViews": {
  "attributedRows": {
   "V_file": [
    [
     0,
     "inventory"
    ]
   ],
   "V_decl": []
  },
  "inSelectedRefs": {
   "V_file": true,
   "V_decl": false
  }
 },
 "manifestAttributingEveryViewOfThisCellProgramUProducer": {
  "result": "REFUSE",
  "refusals": [
   "EXECUTION_INPUTS_VIEW_TOTALITY"
  ]
 },
 "hostRecordingTheReturnedViewInReceiptAndSelectedRefsOnNoRow": {
  "result": "ADMIT",
  "refusals": [],
  "storePointers": "promised_pointers",
  "V_declPointerPresent": true,
  "differsFromReferenceEncoding": true
 }
}
```

**Detail.** Into the maintained one-universe owner graph (one inventory cell) the probe minted two views returned by the binding's own producer for its own Plan, each with one subject-scope at the binding universe: V_file (relation file, an inventory relation) and V_decl (relation declares, not one). Rebuilt through the maintained host-capture builder, the reference attributes V_file to the inventory row and V_decl to no row, leaves V_decl out of the stage receipt and selectedRefs, and admits. A manifest naming every view of this cell/program/U/producer on the row, which is the literal schema sentence, is refused EXECUTION_INPUTS_VIEW_TOTALITY. A manifest recording V_decl as what the stage returned (receipt outputRefs and selectedRefs, per section 1) on no row, with store pointers recomputed by promised_pointers as section 2 requires, also admits, and its raw digest differs from the reference encoding. So for identical stage returns two admissible ExecutionInputsV1 records exist, giving different executionInputsDigest values and therefore different Run identities; section 5 closed exactly this class for targetUniverse. No contract or schema text states the deciding criterion (a scope relation among the cell capability's matrix relations), whether a view may be attributed to several rows, what a returned view that matches no requested cell does to the receipt and selectedRefs, or the rule for capabilities without matrix relations. Lawful plans reach the case: a program carries one cell per requested capability, all bound to the same provider and universe, so returned views must be divided among rows by some rule. No maintained control has more than one capability cell per program, so the passing suites cannot expose it. The execution-inputs owner bytes are unchanged 39->40, so this is a pre-existing gap. This origin's source39 review read the contract completely and did not find it; the charter's narrow question and a reviewer-minted graph found it now.

**Consequence.** An implementation written from the published law alone can mint a manifest that a conforming verifier refuses, or one that is admitted under a different RunId than another conforming host's for the same analysis. Retained Run identity is therefore not reproducible from published law.

**Required change.** Publish the attribution law in execution-inputs contract sections 1, 3 and 5 and align the schema description: (1) the predicate attributing a returned view to a cell/program row, including the capability-relation criterion; (2) whether one view may be attributed to several rows; (3) the treatment of a returned view matching no requested cell, and whether stage-receipt outputRefs are the observed returns or only attributed views; (4) the rule for capabilities without matrix relations. Make builder and admission implement that single stated predicate so exactly one encoding admits, and add controls with two capability cells on one program, a view shared by both, and a returned view matching neither.

**Owner.** foundation execution-inputs owner (execution-inputs-contract.v1.md, execution-inputs.schema.v1.json, execution_inputs_model.v1.py, execution_inputs_fixture.v3.py, check-execution-inputs.v1.py); planned host capture module crates/host/src/analysis.rs (inventory path, not present in the snapshot)  
**Receipts.** receipts/probes/viewdigests-v40b.json, receipts/probes/viewdigests-v40c.json, receipts/probes/viewdigests-v40.json

### ADV40-01 (EDITORIAL): The added implementation-normative-inputs.v8.json is a superseded mid-integration layer that binds native-evidence.md bytes present in no frozen subject, under the same standing text as the current layer

- docs/v2/architecture/implementation-normative-inputs.v8.json (read complete; standing identical to v9)
- docs/v2/architecture/implementation-planning-sources.v1.json (diff read; previous layer v8, current v9)

v8 differs from v9 in run-termination-contract.v1.md (source39 bytes) and native-evidence.md (a digest matching neither the source39 nor the source40 bytes). Its standing still reads as exact normative inputs consumed by implementation planning. v9, coverage and planning sources bind current bytes and the planning checker passes, so planning is consistent; a reader of v8 alone could take an unfrozen integration state for a frozen input layer.

**Disposition.** EDITORIAL at the next successor: mark v8 superseded (or name the unfrozen bytes it binds). Non-blocking.

## Observations (not defects)

- **OBS40-01** policy test: a rule with missing required evidence is listed in indeterminateRules even when a known gating finding makes the verdict fail (production rule outcome fail). Section 5 now states this (workflows-and-surfaces.md:671-673); CaseResult.indeterminateRules names rules without a per-rule cause. An advisory rule with a known hit displays verdict advisory where production passes. (receipts/probes/policy-v40.json)
- **OBS40-02** policy test fixture representation limit: optional imported evidence that is available but has no matching row is a blocking fixture unknown (verdict indeterminate), while the same rule with the evidence absent passes (pass) and bounded production composition of an optional-only unknown passes ({"verdict": "pass", "ruleOutcome": "pass", "findings": 0, "waived": 0}). The ruleLaw names a representation limit as blocking, while composition section 5 lets optional-only unknowns pass, so the fixture is conservative and disclosed and never gives a false pass. (receipts/probes/policy-v40.json)
- **OBS40-03** policy show resolves and reports: it accepts a PolicyDocumentV2 carrying an unregistered universe token, and its EffectivePolicyRecordV1 is schema-valid on both byte sets, while policy test refuses POLICY.UNKNOWN_RULE. No stated law makes show perform test or analysis admission, so this is not a violation; showing a policy that analysis would refuse is a presentation limit. (receipts/probes/policy-v40.json)
- **OBS40-04** U-4b.2 trusted-host scope: remint BOTH languageMode and unitKind consistently over a jsconfig allowJs:false marker and the full Run still closes, with a different RunId (run3:228bc3216d29da6b1bb5ac9f87ef85b85396547c6f39700429617d42f46fed86 versus run3:f731b5d95453c10a6ebdcfd199c97dcdbfcab67ba4d2bd228f60de97e2510d7c for the published unit). Closure checks kind against mode and re-derives membership from the supplied marker observations; the effective allowJs is the trusted pre-Plan marker observation (native section 1.2), not something closure re-derives from bytes. Measured on the syntax-universe fixture, which has no tsjs program cell. (receipts/probes/native-v40.json)
- **OBS40-05** U-1 omitted value: discover_units reads an omitted tsconfig allowJs observation as false, while typescript_mode derives true from checkJs. Native section 1.2 requires the marker observation to carry the effective value, so a host must supply allowJs=true for a checkJs-derived configuration; the model default is not a second law. (receipts/probes/native-v40.json)
- **OBS40-06** Nested Cargo: an explicitly named member root beside its explicit workspace root is folded (explicit a and a/b/c give one a workspace unit with members a/b and a/b/c), matching the retained explicit-root case. Marker observations do not prove that Cargo accepts a nested-workspace layout, as the native case note states. (receipts/probes/native-v40.json)
- **OBS40-07** execution-inputs reference: the scope-level enumeratorClosure test is the last statement of the attribution loop body, so its continue decides nothing (attribution already filters views by producer). Dead code with no behavioural effect. (receipts/probes/viewdigests-v40.json)
- **OBS40-08** Against the codex final-reference.v40 run: all six group stdouts byte-equal: True; 15 of 17 evaluator3 child stdouts byte-equal. enumeration and execution-inputs differ only in absolute copy paths inside ownedHashes and receiptPath. (receipts/reference-comparison.json)
- **OBS40-09** Re-observed on unchanged bytes by the ported source39 probes: one broad installPath row authorizes every top-level package; a case-variant node_modules segment stays first-party; a hidden candidates suppressedCount cannot be joined from the query record; a trusted retained view may declare any unavailability class; admit_repair_plan_v2 is schema and identity admission. (receipts/probes (ported probe receipts))
- **OBS40-10** Correction of this origin's source39 narrative. TOPIC-V7-PLANNING said the mapping population was preserved, but that review's own evidence recorded 320 in source38 and 322 in source39 (workflow goldens 43 to 45), so source39 changed the population. Source40 measures 322, equal to source39: 22 rows were rebound to changed selectors, none added or removed. (receipts/planning-checks.json)

## Item dispositions

### S39-01: CLOSED-AT-SOURCE-LEVEL

*Origin:* claude-independent-design.v39 SHOULD; prior39: OPEN-SHOULD

- docs/coop/design-corrections/workflows/policy_test_model.v3.py:230-255 (every selected subject evaluated; required-absent is a rule-level blocking deficiency; a known true root still emits and fails)
- docs/v2/contracts/product-v1/workflows-and-surfaces.md:644-647 and :671-673
- docs/coop/design-corrections/workflows/schemas/evaluator3/policy-test.schema.json (ruleLaw; read complete)
- docs/coop/design-corrections/foundation/evaluator-composition-contract.v3.md:36 and section 5 (optional-only root unknown passes)

Source39 bytes lose the known hit (verdict indeterminate, no finding). On source40 bytes the fixture equals bounded production composition on verdict and finding presence in all six discriminating cases: the or-rule cases (required evidence missing, optional missing, required present) all fail, and the known-false-root case under missing required evidence, the waived hit and the no-subjects case are all indeterminate. Required absence lists the rule in indeterminateRules and optional absence does not, so required and optional evidence are distinguished. Suite and result identities are H/policytest2 over the suite, and the same suite gives the same bytes.

### S39-02: CLOSED-AT-SOURCE-LEVEL

*Origin:* claude-independent-design.v39 SHOULD; prior39: OPEN-SHOULD

- docs/coop/design-corrections/workflows/workflows_model.v3.py:279-289 (resolver refusal POLICY.UNKNOWN_RULE, remedy EVALUATOR_POLICY_UNIVERSE_UNREGISTERED)
- docs/coop/design-corrections/workflows/policy_test_model.v3.py:37 (POLICY_UNIVERSES from identity-schemas policyUniverseMap), :71 (fact token), :76-79 (rule tokens), :132 (imported occupancy joins subject and universe)
- docs/v2/contracts/product-v1/workflows-and-surfaces.md:660-671
- docs/coop/design-corrections/workflows/policy-test-cases.v3.json (diff read; authored tokens registered)

Unregistered rule tokens, including one on a disabled rule, are resolver refusals POLICY.UNKNOWN_RULE; an unregistered fact token is admission CONFIG.INVALID; the three registered tokens admit with equal outcomes. A foreign-universe imported row created a known hit on source39 bytes and creates none on source40. The same-universe control fails on both byte sets, and a foreign native fact occupied on neither. The six-file correction is discriminated against the old bytes in separate processes. The policy show acceptance is OBS40-03, not a violation.

### ADV39-01: CLOSED-BY-EXPLICIT-TRUTHFUL-ACCOUNT

*Origin:* claude-independent-design.v39 ADVISORY; prior39: ROUTE-TO-NATIVE-OWNER

- docs/v2/contracts/product-v1/native-evidence.md:3113-3124

Every factual statement of the new paragraph was measured. The annotation bytes are unchanged 38 to 40; the only JSON difference is the ResolvedNodeModulesLayoutV1 description; the digests are exactly 3e37c7b7... and 2d37b810...; the registry registers only the latter and the rebuilt exports consume it; the registered bytes are unchanged 39 to 40. The paragraph calls this a prerelease document revision and re-registration and grants no cross-profile replay or migration acceptance, which is what the advisory asked for.

### ADV38-01: REMAINS CLOSED

*Origin:* claude-independent-design.v38 ADVISORY; prior39: CLOSED-AT-SOURCE-LEVEL

- docs/coop/design-corrections/foundation/run-termination-contract.v1.md section 7 (read complete; 39->40 edits confined to sections 3, 6 and 7.3 prose)
- run_termination_model.v1.py (unchanged 39->40: True)

The section 7 composition admission and closed detail allowlist are unchanged in substance, and the ported probe passes over golden Runs on source40.

### ADV38-02: REMAINS CLOSED

*Origin:* claude-independent-design.v38 ADVISORY; prior39: CLOSED-AT-SOURCE-LEVEL

- docs/coop/design-corrections/security/carrier-dispatch.v3.json (unchanged 39->40: True)

The read-only carrier route bytes are identical and every tabulated scenario still matches on source40.

### ADV38-03: REMAINS CLOSED (basis inherited, bytes unchanged)

*Origin:* claude-independent-design.v38 ADVISORY; prior39: CLOSED-AT-SOURCE-LEVEL

- docs/v2/architecture/commit-recovery-readonly.v3.md (unchanged 39->40: True)

The source39 whitespace-normalized measurement of the corrected phrases stands on byte-identical bytes; not re-measured.

### CHARTER-U4B-UNITKIND: CONFIRMED WITH FULL RUN CLOSURE (trusted-host scope in OBS40-04)

*Origin:* source40 charter

- docs/v2/contracts/product-v1/native-evidence.md:733-804 (U-4b; unitKind at :755-760; enforcement U-4b.5)
- docs/coop/design-corrections/native/native_evidence_model.v2.py:3764 (TSJS_UNIT_KIND), :3951-3957
- docs/coop/design-corrections/foundation/enumeration_model.v1.py:536-559 (diff read)

Published kinds close full Runs. A digest-consistent reminted kind (N2), a rust unit carrying js-program (N4) and a tsjs unit carrying cargo-package (N5) each refuse at full closure with EVALUATOR_ENUMERATION_JOIN:ENUMERATION_MEMBERSHIP_ORDER, and all three close on source39 bytes. Discovery and admission share one closed projection table. The one thing closure cannot check is the effective allowJs behind a consistent mode-and-kind remint (OBS40-04), which is the stated trusted marker observation.

### CHARTER-U1-ALLOWJS: CONFIRMED (identity consequence measured)

*Origin:* source40 charter

- native-evidence.md:652-662 (U-1)
- native-evidence.md:516-535 (section 1.2 effective allowJs)
- native-evidence.md:162-163 (mode table)
- native_evidence_model.v2.py:3951-3953 (discovery), :2207-2224 (typescript_mode)

jsconfig omitted or true selects js-allowjs, explicit false selects ts-tsconfig, tsconfig takes precedence, and package-only synthesizes; the source39 model read explicit jsconfig false as js-allowjs. For a jsconfig allowJs:false project the membershipDigest (a PlanId input) differs between the models: a prerelease identity change, consistent with the corrected law. The omitted-value default is OBS40-05.

### CHARTER-NESTED-CARGO: CONFIRMED (root and both coauthor edits carry controls, all executed)

*Origin:* source40 charter

- native-evidence.md:744-754 (U-4b.2 nested folding)
- native_evidence_model.v2.py:3930-3941
- check-enumeration.v1.py (diff read)
- check-native-consumer24-corrections.v1.py (diff read; ranges 1-140 and 370-619 read)
- native-cases.v2.json (diff read)

Triple nesting, explicit outer, root plus inner, inner alone, a nested project boundary, a root package over a nested workspace, a package between workspaces and UTF-8 member order all match the source40 text. Targets under folded member roots are pruned while src/target stays source, and dropping a folded member refuses row derivation. Source39 bytes raised StopIteration on triple nesting and on a package between workspaces. The checker controls ran in this review's groups: enumeration 46 cases with 0 mismatches; native-consumer24 212 of 212; native group 388/388.

### CHARTER-RUN-TERMINATION: CONFIRMED AGAINST THE UNCHANGED MODEL

*Origin:* source40 charter

- run-termination-contract.v1.md:83-87 (section 3), :170-180 (section 6), :246-256 (section 7.3)
- run_termination_model.v1.py (unchanged 39->40: True)

The named keys are the model's. errorCode, faultCause and signal are recognized fields that reach RUN_TERMINATION_NOT_DERIVED, and an unknown member refuses first. The commit-inventory recipe, recomputed independently over a closed Run, equals the owner digest and canonical-set order and validates against the owning schema; a non-canonical order refuses and an extra object changes the digest. Model, identity schemas and public registry are unchanged, so the clarifications add no public detail and no identity rule.

### CHARTER-ADVISORY-TOPICS: ASSESSED; no contradiction demonstrated

*Origin:* source40 charter

- public-detail-registry.v1.json (unchanged; 315 codes)
- native-evidence.md:3018 and :3031 (LIVE D9 not discharged; existing D9 codes only)
- workflows-and-surfaces.md:403 (first-applicable indeterminateReason order)
- workflows-and-surfaces.md:440, :475, :508 (evidence axis, single import identity, exact-snapshot correspondence)
- native-evidence.md:166 and :172 (rust-cargo-prepared mode row), :1261-1263 (preparedResolution, preparedOutputSetId)

Private diagnostic spellings (EVALUATOR_POLICY_UNIVERSE_UNREGISTERED as remedy text under the registered POLICY.UNKNOWN_RULE, ENUMERATION_MEMBERSHIP_ORDER, RUN_TERMINATION_*) are not public codes. The D9 successor remains the carried obligation (DR-007/DR-011-R08). An exact-snapshot import has one H identity over its wrapper, so a changed snapshot is a different import2 and an evidence-axis change, which comparison treats conservatively. The first-applicable reason order publishes exactly one reason per entry and, by design, makes later reasons unreachable for that entry. The prepared-Rust mode row still selects through an admitted PreparedOutputSetV3 with non-null preparedOutputSetId after U-1 yields a unit, which the source40 unit-kind change (cargo kinds for rust) does not touch.

### CHARTER-SCOPE-PRESERVATION: RE-EXECUTED ON SOURCE40

*Origin:* source40 charter

- receipts/probe-port.json

Six source39 probes were ported with their expectations unedited (query carriers, read-only carriers, comparison knowledge, repair:2, section 7 composition, custody and fallback), and all pass on source40. Their owner bytes are unchanged 39->40 except check-workflow-projection, whose added controls run in the workflow-projection child (860 checks).

### CHARTER-V9-PLANNING: CONFIRMED (population measured, not inherited)

*Origin:* source40 charter

- implementation-normative-inputs.v9.json (read complete)
- implementation-coverage.v1.json (diff read)
- implementation-planning-sources.v1.json (diff read)

v9 binds 31 current inputs with no mismatch and no self-binding, and coverage and planning sources name v9. There are 322 mappings (24 report features, 45 workflow goldens), equal to source39, with 22 rows rebound and none added or removed; 198 paths in 20 packages; M0-M6; 54 recovery cases, none executed. OBS40-10 records the source39 narrative correction.

### CHARTER-PACKAGE17: VERIFIED AS AUTHOR EVIDENCE (package15 constructors plus native-v2 overlay; package16 preserved; no relabel)

*Origin:* source40 charter

- /tmp/opensip-design-corrections/claude-author-package-successor.v17/artifact-manifest.json
- /tmp/opensip-design-corrections/claude-author-package-successor.v17/source-binding.v40.json
- /tmp/opensip-design-corrections/root-author-package-final40-rebuild.v1/rebuild-report.json

See packageAssessment.

### CHARTER-CURRENT-REFERENCE: OWN EXECUTION PASSES; HEADER RUN IS CONSISTENT EVIDENCE

*Origin:* source40 charter

- /Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/codex-post-reset.v1/final-reference.v40/reference-checks.json
- /tmp/opensip-design-corrections/root-source40-final-reference.v2/reference-checks.json

The header-named codex final-reference.v40 report hashes to 019c3397..., binds the source40 subject and passed; its runner-original equals root-source40-final-reference.v2. This review's own six groups and 17 children pass on its own verified copy and agree with it apart from path-only fields. The preliminary root source40 reference v1 predates final integration and was not used.

### NARROW-Q1-VIEWDIGESTS: MISSING RECIPE (S40-01)

*Origin:* source40 charter narrow question

- see S40-01

Already owned: producer closure, Plan, binding universe (per-scope sourceUniverse and the section 5 single-universe restriction), receipt outputDomains, coverage equality per (cell, program, relation, resolution, U, producer), and UNSUPPORTED-TYPED coverage handling. Missing: how the selected receipt relates to the returned views (are receipt outputRefs the observed returns or the attributed views), the capability-relation criterion, sharing a view across rows, unmatched returned views, and capabilities without matrix relations. Two admissible encodings with different digests demonstrate the consequence.

### NARROW-Q2-COMPOSITION-S7-CLOSURE: NO GAP

*Origin:* source40 charter narrow question

- evaluator-composition-contract.v3.md:70 (input admission precedes replay), :74 (output typed-reference closure), :76 (complete comparison, exact reachable output set)
- evaluator-composition-contract.v3.md:93-109, :271, :317 (section 9 owner-specific equality addresses)

Section 7 closes OUTPUT references: a typed-prefix identity field resolves and admits its descriptor in the prefix-selected domain, and subset comparison is forbidden. Output fields that name admitted inputs (planId, evaluatorClosure, EI-derived view/coverage/import ids, policyDigest) are fixed by section 9 equality to inputs already admitted, because input admission precedes replay. Resolving an admitted input again is idempotent and section 9 equality is the stronger law, so the two layers compose without conflict and leave no implementer choice.

### NARROW-Q3-POLICY-DERIVATION3: CONSISTENT

*Origin:* source40 charter narrow question

- evaluator-composition-contract.v3.md:288 and :317 (section 9.7)
- evaluator_replay_model.v3.py:86-107 (range read to end of file)

policy-derivation3 is exactly {schemaVersion, planId, proofBundleId, policyDigest, waiverDigest, verdict}, derived from a completely replayed Run's admitted Plan and seal and its recomputed proof, and a claim is admitted only by equality to that derivation. It carries no runId, so it is a derived and admitted projection keyed by Plan and proof, not a Run back-reference; a different policy or waiver set needs its own Plan and Run.

## Package v17

Package v17 verified as author evidence: every one of its files matches the artifact manifest f179b756...; the formal subject manifest and the files-only source manifest ec4f69fc... are different objects with equal file members; the rebuild base is package15 constructors plus the native-v2 migration overlay (overlay base digests match retained package15), not package16, which is preserved unchanged. This review re-executed verify-package.py and probe-native-v2.py on its own verified copy: groups checkpoint3 1 (passed True, exit 0), normalized-examples6 4 (passed True, exit 0), rust-selection-examples1 2 (passed True, exit 0), semantic-controls1 3 (passed True, exit 1), binding-controls 3 (passed True, exit 1), normalization-map-controls1 4 (passed True, exit 1), query 7 (passed True, exit None); 17 exports and 7 queries. A non-zero exit is recorded only for semantic-controls1, binding-controls, normalization-map-controls1, whose exported stores are refusing controls; the verifier records passed=true for every group, and this review reports that record without reinterpreting it. The verification and all compared output files are content-equal to the root verification, and the 9 membership probes are content-equal to the root rebuild probe.

- Author construction and self-consistency evidence; verify-package.py and probe-native-v2.py are author tools re-executed here, not an independent or blind reconstruction.
- Rebuilt by root from package15 constructors plus the migration overlay against source40; 17 of 17 exports carry new RunIds; package16 stays unchanged history; no export relabel.
- Preserved limitations: the partial TypeScript consumer helper leaves and/or/not unexercised; count-at-most/all-covered are unimplemented; two-binding qualification is incomplete (single explicit binding); all 30 evaluations remain PENDING.
- The 4 TypeScript normalization-map negatives are the exact refusals recorded below for those exported stores; they are not generalized to other map defects.
- No compiler, provider, OS or process-isolation qualification; independent grades granted: 0.

Normalization-map negatives (exact, not generalized):

| control | owner admission | semantic admission | reason |
|---|---|---|---|
| ts-map-absent | REFUSE | NOT-REACHED | BODY_NORMALIZATION_MAP_MISSING:opensip-interface/normalization/specification-map.v1.json |
| ts-map-level-unmapped | REFUSE | NOT-REACHED | BODY_NORMALIZATION_LEVEL_UNMAPPED:L0-verbatim |
| ts-map-level-swapped | REFUSE | NOT-REACHED | BODY_NORMALIZATION_LEVEL_VERSION_MISMATCH:L0-verbatim |
| ts-spec-outside-closure | REFUSE | NOT-REACHED | BODY_NORMALIZATION_SPECIFICATION_NOT_IN_CLOSURE:L0-verbatim |

## Commands and probes

| group | exit | seconds | stdout sha256 |
|---|---|---|---|
| evaluator3 | 0 | 479.2 | `2ddf8f99c46365462636ae191ff71c1800424e00c460fc335bc47f9a3659ef1b` |
| foundation | 0 | 134.3 | `2a7cd6d84cf029f12d43c4a34c7a91b4817167f8d88e07dc1721c87f78ef3ded` |
| integration | 0 | 17.3 | `3fccd9e3a400774d6f411e530a22848ec38eae5a30e737f4c66bf75254d20112` |
| native | 0 | 3.2 | `49fca461221535d2306dfe19a99cec49a26e6bc78ed3c9f777473073b65a1406` |
| security | 0 | 0.9 | `60d498d317776373a82f941db5a82a78b5eca33ba6d8f57eeb387a9a081ca746` |
| workflows | 0 | 10.4 | `954ebf2eedafc242f2998bcfb9f4ff4c18bd80063ad9b0edce34b7beebd14e51` |

evaluator3 children: 17, all exit 0: True. Planning: {'check_implementation_planning': 0, 'check_repository_file_inventory': 0}. Planning counts ok: True.

| probe | rows | failed | run receipt | earlier attempts |
|---|---|---|---|---|
| P40-SUBJECT | (command receipt) | - | receipts/subject-verification.json, receipts/manifest40-index.json | - |
| P40-ARCHIVE | (command receipt) | - | receipts/archive-verification.source40.json, receipts/archive-verification.source40-pkg.json | - |
| P40-DELTA | (command receipt) | - | receipts/delta-diff-summary.json | - |
| P40-GROUPS | (command receipt) | - | receipts/reference/groups-report.all.json, receipts/reference/evaluator3.stdout, receipts/reference/foundation.json | - |
| P40-PLAN | (command receipt) | - | receipts/planning-checks.json | - |
| P40-REFERENCE-COMPARE | (command receipt) | - | receipts/reference-comparison.json | - |
| P40-POLICY | 26 | 0 | receipts/runs/policy-v40.run.json | 0 |
| P40-NATIVE | 39 | 0 | receipts/runs/native-v40.run.json | 0 |
| P40-RUNTERM-ADV | 24 | 0 | receipts/runs/runterm-adv-v40.attempt2.run.json | 1 |
| P40-VIEWDIGESTS | 13 | 0 | receipts/runs/viewdigests-v40.run.json | 0 |
| P40-VIEWDIGESTS-B | 4 | 0 | receipts/runs/viewdigests-v40b.run.json | 0 |
| P40-VIEWDIGESTS-C | 3 | 0 | receipts/runs/viewdigests-v40c.attempt2.run.json | 1 |
| P40-PACKAGE | 20 | 0 | receipts/runs/package-v17-evidence.run.json | 0 |
| P40-PORTED-QUERY | 98 | 0 | receipts/runs/query-carriers.run.json | 0 |
| P40-PORTED-CARRIER | 108 | 0 | receipts/runs/carrier-readonly.run.json | 0 |
| P40-PORTED-COMPARISON | 28 | 0 | receipts/runs/comparison-knowledge.run.json | 0 |
| P40-PORTED-REPAIR2 | 16 | 0 | receipts/runs/repair2.run.json | 0 |
| P40-PORTED-TERM7 | 24 | 0 | receipts/runs/run-termination-s7.run.json | 0 |
| P40-PORTED-CUSTODY | 20 | 0 | receipts/runs/native-custody-fallback.run.json | 0 |

## Read coverage

Whole-file claims are made only for fresh40Read (every line read this charter) and inheritedUnchanged39Read (counted as completely read by this origin's source39 review and byte-identical now; not re-read). complete39ReadPlusComplete40Diff is a complete predecessor read plus the exact complete diff. delta40Read, fresh40RangeRead, prior39RangeReadOnly and searchOnlySightings are not whole-file reads. Hashes were recomputed at build time.

```json
{
 "fresh40Read": 11,
 "fresh40RangeRead": 9,
 "delta40Read": 22,
 "complete39ReadPlusComplete40Diff": 2,
 "inheritedUnchanged39Read": 40,
 "changedPriorReadNotReread": 0
}
```

Delta files without a read entry: none

Fresh whole-file reads this charter:

- docs/coop/design-corrections/foundation/check-composition.v3.py (98 lines)
- docs/coop/design-corrections/foundation/evaluator-composition-contract.v3.md (334 lines)
- docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md (298 lines)
- docs/coop/design-corrections/foundation/run-termination-contract.v1.md (379 lines)
- docs/coop/design-corrections/workflows/policy_test_model.v3.py (291 lines)
- docs/coop/design-corrections/workflows/schemas/evaluator3/policy-test.schema.json (93 lines)
- docs/coop/design-corrections/workflows/workflows_model.v3.py (314 lines)
- docs/v2/architecture/implementation-normative-inputs.v8.json (160 lines)
- docs/v2/architecture/implementation-normative-inputs.v9.json (160 lines)
- docs/v2/contracts/product-v1/native-evidence.md (3975 lines)
- docs/v2/contracts/product-v1/workflows-and-surfaces.md (1699 lines)

Range reads this charter:

- docs/coop/design-corrections/foundation/check-execution-inputs.v1.py: 1-170,270-349,825-914
- docs/coop/design-corrections/foundation/check-native-consumer24-corrections.v1.py: 1-140,420-619, 370-421
- docs/coop/design-corrections/foundation/evaluator_replay_model.v3.py: 86-121
- docs/coop/design-corrections/foundation/execution-inputs.schema.v1.json: 405-629
- docs/coop/design-corrections/foundation/execution_inputs_fixture.v3.py: 189-398
- docs/coop/design-corrections/foundation/execution_inputs_model.v1.py: 1095-1166
- docs/coop/design-corrections/foundation/identity-model.v3.py: 2056-2071
- docs/coop/design-corrections/native/native_evidence_model.v2.py: 2200-2251
- docs/coop/design-corrections/workflows/check-workflow-projection.v3.py: 3590-3615

Complete source39 read plus complete 39->40 diff: docs/coop/design-corrections/foundation/check-native-consumer24-corrections.v1.py, docs/coop/design-corrections/workflows/policy-test-cases.v3.json

Inherited unchanged source39 whole-file reads (not re-read): 40 files, listed in review.json.

## TCB-SCOPE-01 (assessed once)

**Assumption.** Selected authenticated in-process host/evaluator code is trusted; adversarial code sharing that process is outside this product threat model. Untrusted inputs are inert typed data and provider process boundaries still require real qualification.

**Consequence.** Rejecting or changing the assumption reopens all thirteen dependent rows together. It is a scope selection, not a containment guarantee, and repairs no historical attack. All thirteen author grades stay PENDING.

**Dependent rows (13).** RES-EP13-02, RES-EP13-04, RES-EP13-12, RES-EP13-13, RES-EP13-16, RES-EP13-18, IR-EP13-NB-01, IR-EP13-NB-03, IR-EP13-NB-04, AX6, AX9, MD5, RX2c

- It stays coherent as a scope selection on source40. Admission section 5 (no untrusted native/WASM, no imperative contributions or project hooks) is byte-identical 39->40: True; prototype-report-inventory still admits no executable report hooks and is byte-identical: True.
- Source40 adds trust surfaces and states them as trust. The effective allowJs marker observation is trusted pre-Plan input: a consistent mode-and-kind remint closes a full Run with a different RunId (OBS40-04). Marker observations do not prove Cargo accepts a nested layout (OBS40-06). ExecutionInputsV1 remains a host TCB observation of stage returns (execution-inputs section 1).
- Untrusted inputs stay inert typed data and are more closed than in source39: policy-test rule and fact universe tokens refuse typed, an imported row must match subject and universe, and unit kinds are a closed projection enforced at closure (P40-POLICY, P40-NATIVE).
- S40-01 is a determinism defect in the published capture law: two conforming hosts encode the same returns differently. It is not a trust-boundary violation and does not change the assumption, although a product relying on the host observation needs the attribution law published. ADV40-01 is editorial.
- It remains unqualified. It rests on the authenticated closure/TCB inventory and provider process boundaries, and all 32 gates are unperformed (qualified=true count 0).

**Position:** NOT REJECTED. **Standing:** ASSESSED-COHERENT-UNQUALIFIED-ON-SOURCE40; final application adjudication not granted. **Adjudication owner:** The separate final application review, performed by a NEW other actual Claude origin: not this origin (85a08aec-9d22-4ac6-8ec2-c10170e727d7) and not any author, design or blind origin. Not adjudicated here.

## Disposition rows (107)

All rows: appliedByThisReview=false, finalApplicationOutcomeGranted=false. Author grades are not assigned.

**Basis rule.** inherited-unchanged-39: the governing owner bytes are byte-identical 39->40, and the conclusion rests on that identity plus this origin's source39 assessment; any re-executed suite named in the row is corroboration only. new-40: the conclusion rests on a source40 read, diff, probe or measurement newly performed under this charter. No row is carried forward without its own text, and no grade is assigned. Counts: {"new-40": 71, "inherited-unchanged-39": 36}.

| id | prior39 | disposition | basis | assessment |
|---|---|---|---|---|
| F-01 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | inherited-unchanged-39 | F-01: identifier and prior root standing RE-VERIFIED-ON-PACKAGE13 (root-independent36-completion-assessment.v1) carried. The F record lives outside the snapshot and is not re-derived; none of the 24 delta files is an F record. The prior standing is not source40 acceptance. |
| F-02 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | inherited-unchanged-39 | F-02: identifier and prior root standing RE-VERIFIED-ON-PACKAGE13 (root-independent36-completion-assessment.v1) carried. The F record lives outside the snapshot and is not re-derived; none of the 24 delta files is an F record. The prior standing is not source40 acceptance. |
| F-03 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | inherited-unchanged-39 | F-03: identifier and prior root standing RE-VERIFIED-ON-PACKAGE13 (root-independent36-completion-assessment.v1) carried. The F record lives outside the snapshot and is not re-derived; none of the 24 delta files is an F record. The prior standing is not source40 acceptance. |
| F-04 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | inherited-unchanged-39 | F-04: identifier and prior root standing INHERITED (root-independent36-completion-assessment.v1) carried. The F record lives outside the snapshot and is not re-derived; none of the 24 delta files is an F record. The prior standing is not source40 acceptance. |
| F-05 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | inherited-unchanged-39 | F-05: identifier and prior root standing RE-VERIFIED-ON-PACKAGE13 (root-independent36-completion-assessment.v1) carried. The F record lives outside the snapshot and is not re-derived; none of the 24 delta files is an F record. The prior standing is not source40 acceptance. |
| F-06 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | inherited-unchanged-39 | F-06: identifier and prior root standing RE-VERIFIED-ON-PACKAGE13 (root-independent36-completion-assessment.v1) carried. The F record lives outside the snapshot and is not re-derived; none of the 24 delta files is an F record. The prior standing is not source40 acceptance. |
| F-07 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | inherited-unchanged-39 | F-07: identifier and prior root standing INHERITED (root-independent36-completion-assessment.v1) carried. The F record lives outside the snapshot and is not re-derived; none of the 24 delta files is an F record. The prior standing is not source40 acceptance. |
| F-08 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | inherited-unchanged-39 | F-08: identifier and prior root standing RE-VERIFIED-ON-PACKAGE13 (root-independent36-completion-assessment.v1) carried. The F record lives outside the snapshot and is not re-derived; none of the 24 delta files is an F record. The prior standing is not source40 acceptance. |
| F-09 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | inherited-unchanged-39 | F-09: identifier and prior root standing INHERITED (root-independent36-completion-assessment.v1) carried. The F record lives outside the snapshot and is not re-derived; none of the 24 delta files is an F record. The prior standing is not source40 acceptance. |
| F-10 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | inherited-unchanged-39 | F-10: identifier and prior root standing RE-VERIFIED-ON-PACKAGE13 (root-independent36-completion-assessment.v1) carried. The F record lives outside the snapshot and is not re-derived; none of the 24 delta files is an F record. The prior standing is not source40 acceptance. |
| F-11 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | inherited-unchanged-39 | F-11: identifier and prior root standing RE-VERIFIED-ON-PACKAGE13 (root-independent36-completion-assessment.v1) carried. The F record lives outside the snapshot and is not re-derived; none of the 24 delta files is an F record. The prior standing is not source40 acceptance. |
| F-12 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | inherited-unchanged-39 | F-12: identifier and prior root standing RE-VERIFIED-ON-PACKAGE13 (root-independent36-completion-assessment.v1) carried. The F record lives outside the snapshot and is not re-derived; none of the 24 delta files is an F record. The prior standing is not source40 acceptance. |
| F-13 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | inherited-unchanged-39 | F-13: identifier and prior root standing RE-VERIFIED-ON-PACKAGE13 (root-independent36-completion-assessment.v1) carried. The F record lives outside the snapshot and is not re-derived; none of the 24 delta files is an F record. The prior standing is not source40 acceptance. |
| F-14 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | inherited-unchanged-39 | F-14: identifier and prior root standing RE-VERIFIED-ON-PACKAGE13 (root-independent36-completion-assessment.v1) carried. The F record lives outside the snapshot and is not re-derived; none of the 24 delta files is an F record. The prior standing is not source40 acceptance. |
| RES-EP13-01 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-40 | Plan and derivation joins stay inside complete replay. On source40, full Runs built by the maintained fixture close with published unit kinds and refuse reminted ones at closure (P40-NATIVE N2/N4/N5), and the full-replay child passes 73 checks. The historical limitation is preserved; no historical guard is claimed repaired. |
| RES-EP13-02 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-40 | Depends on TCB-SCOPE-01. The effective allowJs marker observation is trusted pre-Plan input: a consistent mode-and-kind remint closes with a different RunId (OBS40-04), so no answer-provenance claim against the host is made. The historical limitation is preserved; no historical guard is claimed repaired. |
| RES-EP13-03 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | inherited-unchanged-39 | The seven-vector measurement stays finite history; admission-and-qualification.md (unchanged 39->40: True) and the residual ledger (unchanged: True) are byte-identical. The historical limitation is preserved; no historical guard is claimed repaired. |
| RES-EP13-04 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-40 | Depends on TCB-SCOPE-01. Closed input admission now also covers policy-test rule and fact universe tokens: unregistered rule tokens refuse POLICY.UNKNOWN_RULE and fact tokens CONFIG.INVALID (P40-POLICY). The historical limitation is preserved; no historical guard is claimed repaired. |
| RES-EP13-05 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-40 | The frozen subject was verified outside every author instrument: formal manifest, archive, all 12,911 members, parent39 and the exact 22/2/0 delta (P40-SUBJECT, P40-ARCHIVE). The historical limitation is preserved; no historical guard is claimed repaired. |
| RES-EP13-06 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-40 | canonical.py is outside the delta. The reviewer's own C()/H() reproduced policy-test suite and result identities for three authored suites and the commit-inventory digest over a closed Run (P40-POLICY, P40-RUNTERM-ADV). The historical limitation is preserved; no historical guard is claimed repaired. |
| RES-EP13-07 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | inherited-unchanged-39 | Seal and replay owners are outside the delta, and the analysis-seal child passes on source40. The historical limitation is preserved; no historical guard is claimed repaired. |
| RES-EP13-08 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | inherited-unchanged-39 | A bounded historical measurement; source40 claims no product proof over all PlanIntents. The historical limitation is preserved; no historical guard is claimed repaired. |
| RES-EP13-09 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-40 | Provenance stays distinct from correctness. Package semantic-controls1 keeps owner ADMIT and semantic REFUSE (content-equal to the root run), and a digest-consistent unit-kind remint closed on source39 but refuses on source40. The historical limitation is preserved; no historical guard is claimed repaired. |
| RES-EP13-10 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-40 | Author self-counters did not decide this review. S40-01 came from reviewer-minted graphs outside the maintained controls, which have one capability cell per program. The historical limitation is preserved; no historical guard is claimed repaired. |
| RES-EP13-11 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-40 | Failures stay recorded by cause. This review keeps its own run-termination attempt 1 defect and its view-attribution attempt 1 harness defect, and it does not use the preliminary root source40 reference v1 as current evidence. The historical limitation is preserved; no historical guard is claimed repaired. |
| RES-EP13-12 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-40 | Depends on TCB-SCOPE-01. No sole Python guard enters product authority; host stage-return capture (execution-inputs section 1) stays a TCB observation, and S40-01 concerns its determinism, not containment. The historical limitation is preserved; no historical guard is claimed repaired. |
| RES-EP13-13 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-40 | Depends on TCB-SCOPE-01. The probes restore the patched fixture helper and checker globals, run source39 and source40 sides in separate processes, and re-verify the probe copy after every run. The historical limitation is preserved; no historical guard is claimed repaired. |
| RES-EP13-14 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | inherited-unchanged-39 | The differential census is not used as an oracle; unchanged. The historical limitation is preserved; no historical guard is claimed repaired. |
| RES-EP13-15 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-40 | The C-2 v4 self-census is not elevated. The enumeration model change adds the unit-kind projection to the membership law, which the enumeration child (tsjs unit-kind controls) and full Runs exercise, not a census. The historical limitation is preserved; no historical guard is claimed repaired. |
| RES-EP13-16 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-40 | Depends on TCB-SCOPE-01. Producer flags cannot bypass replay; unit kinds are re-derived at every enumeration admission, and run-termination class and reasons are derived from the sealed Run. The historical limitation is preserved; no historical guard is claimed repaired. |
| RES-EP13-17 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | inherited-unchanged-39 | Text-only disclosures remain text-only. The historical limitation is preserved; no historical guard is claimed repaired. |
| RES-EP13-18 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-40 | Depends on TCB-SCOPE-01. Nested Cargo marker observations are trusted and do not prove Cargo accepts a layout (OBS40-06), and pruned-tree custody remains a host observation. The historical limitation is preserved; no historical guard is claimed repaired. |
| RES-EP13-19 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-40 | Substantive review with discriminating probes on both byte sets. All six pinned groups passed and a SHOULD was still found. The historical limitation is preserved; no historical guard is claimed repaired. |
| IR-EP13-NB-01 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-40 | Depends on TCB-SCOPE-01. Every probe ran in-process with owner modules; containment is not claimed. The historical limitation is preserved; no historical guard is claimed repaired. |
| IR-EP13-NB-02 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-40 | No name scan decides scope. Unit kind and universe tokens are closed tables, and imported occupancy compares subject and universe values, not spellings. The historical limitation is preserved; no historical guard is claimed repaired. |
| IR-EP13-NB-03 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-40 | Depends on TCB-SCOPE-01. Loaded owner instances stay reachable in-process, and the trusted marker observation (OBS40-04) is exactly why the boundary is trust. The historical limitation is preserved; no historical guard is claimed repaired. |
| IR-EP13-NB-04 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-40 | Depends on TCB-SCOPE-01; one TCB account covers all thirteen rows. The historical limitation is preserved; no historical guard is claimed repaired. |
| IR-EP13-NB-05 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-40 | Incomplete prose still needs substantive review: S40-01 is a schema sentence whose literal reading the reference refuses and whose gap admits two encodings, and every suite passes. The historical limitation is preserved; no historical guard is claimed repaired. |
| IR-EP13-NB-06 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | inherited-unchanged-39 | The historical attacker cost is preserved as history. The historical limitation is preserved; no historical guard is claimed repaired. |
| IR-EP13-NB-07 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | inherited-unchanged-39 | The original environment is preserved; this review names its interpreter (-I -B) and pins. The historical limitation is preserved; no historical guard is claimed repaired. |
| AX6 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-40 | Depends on TCB-SCOPE-01. The AX6 escape stays history; no delta file claims same-process route-region protection. The historical limitation is preserved; no historical guard is claimed repaired. |
| AX9 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-40 | Depends on TCB-SCOPE-01. The AX9 escape stays history; the source40 additions (token maps, unit-kind projection, nested folding) are typed data admission under a trusted evaluator. The historical limitation is preserved; no historical guard is claimed repaired. |
| MD5 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-40 | Depends on TCB-SCOPE-01. The MD5 escape stays history; source40 adds no Python-containment mechanism. The historical limitation is preserved; no historical guard is claimed repaired. |
| RX2c | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-40 | Depends on TCB-SCOPE-01. The RX2c escape stays history; complete replay and full-Run closure are reproducibility evidence, not containment. The historical limitation is preserved; no historical guard is claimed repaired. |
| AR-01 | NO-NEW-ISSUE | NO-NEW-ISSUE | new-40 | Admission section 1 is byte-identical 39->40. The ported query-carrier probe re-confirms both runId delivery directions of the StepTermination law on source40. |
| AR-02 | NO-NEW-ISSUE | NO-NEW-ISSUE | inherited-unchanged-39 | Admission sections 2-4 and the qualification gates are byte-identical 39->40 (32 gates, qualified=true 0); all gates stay unperformed. |
| AR-03 | NO-NEW-ISSUE | NO-NEW-ISSUE | new-40 | The security contract is byte-identical 39->40. The ported custody probe passes, and U-4b.2 nested project boundaries exclude nested workspace markers (P40-NATIVE C5). |
| AR-04 | NO-NEW-ISSUE | NO-NEW-ISSUE | inherited-unchanged-39 | The security contract is byte-identical 39->40 and no delta touches trust time. No probe. |
| AR-05 | NO-NEW-ISSUE | NO-NEW-ISSUE | inherited-unchanged-39 | The security contract is byte-identical 39->40 and no delta touches root chain or revocation. No probe. |
| AR-06 | NO-NEW-ISSUE | NO-NEW-ISSUE | new-40 | The platform admission text and carrier DDL are unchanged 39->40, and the security group passes on this review's source40 copy. |
| AR-07 | NO-NEW-ISSUE | NO-NEW-ISSUE | new-40 | native-evidence.md changed and was read complete. U-1 effective allowJs, U-4b.2 nested folding and the unit-kind projection were probed against source39 baselines and with full-Run closure; the native group passes 388/388 (source39: 380). |
| AR-08 | NO-NEW-ISSUE | NO-NEW-ISSUE | new-40 | workflows-and-surfaces.md changed and was read complete, but the invocation and repair text is outside the 39->40 diff. The ported repair:2 probe passes on source40; argvDigest is unchanged and not independently probed. |
| AR-09 | NO-NEW-ISSUE | CHANGES-REQUIRED (S40-01) | new-40 | identity-and-evidence.md is byte-identical 39->40 and incorporates the execution-inputs contract (identity section 4). S40-01: which returned views a cell row attributes has no published recipe, and two conforming encodings of the same stage returns admit with different ExecutionInputsV1 digests. The foundation group passes, and the commit-inventory recipe was recomputed independently. |
| AR-10 | NO-NEW-ISSUE | NO-NEW-ISSUE | new-40 | Baseline and comparison text changed (first-applicable indeterminateReason order, workflows-and-surfaces.md:403; the conservative evidence axis) and was read complete. The ported comparison-knowledge probe and child pass, and no contradiction was demonstrated. |
| AR-11 | NO-NEW-ISSUE | NO-NEW-ISSUE | new-40 | Comparison and import: the single H import identity (workflows-and-surfaces.md:475) and exact-snapshot correspondence (:508) were read, and the policy-test imported row now joins subject and universe (S39-02). The execution-inputs child passes. No independent import probe. |
| AR-12 | NO-NEW-ISSUE | NO-NEW-ISSUE | new-40 | Native section 4 atom semantics are unchanged in substance, and the atoms child passes (101 units). S39-01 is closed: the policy-test verifier now keeps known findings under missing required evidence, as fail dominance requires. |
| AR-13 | NO-NEW-ISSUE | NO-NEW-ISSUE | new-40 | Native sections 1 and 2 changed (U-1 effective allowJs, the mode table) and were probed. The U-9 fallback and its security S3 counterpart were re-run by the ported custody probe. OBS40-04 and OBS40-05 are stated trusted-host scope, not defects. |
| AR-14 | NO-NEW-ISSUE | NO-NEW-ISSUE | new-40 | ADV38-02 and ADV38-03 remain closed: carrier-dispatch and commit-recovery bytes are unchanged 39->40, and the ported read-only carrier probe passes on source40. |
| AR-15 | NO-NEW-ISSUE | NO-NEW-ISSUE | inherited-unchanged-39 | The contract index README is byte-identical 39->40. |
| AR-16 | CHANGES-REQUIRED (S39-01, S39-02) | NO-NEW-ISSUE | new-40 | S39-01 and S39-02 are closed at source level, and the run-termination clarifications are confirmed against the unchanged model. ADV38-01 remains closed and the D9 successor stays carried. The only addition in this row is observation OBS40-03 (policy show). |
| FW-01 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | new-40 | discovery.rs must implement U-4b.2 nested Cargo folding (the deepest surviving workspace, decided shallowest first), the closed unit-kind projection, the U-1 effective allowJs marker observation (including a checkJs-derived value, OBS40-05) and pruned-tree custody; all were confirmed at owner level and with full Runs. Owner module and milestone match the current-source-map and repository-file-inventory rows (both byte-identical 39->40: True); implementation not executed. |
| FW-02 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | new-40 | review.rs carries review-brief through query carriers; the ported query probe re-confirms the lawful control, the truncated variant and the another-run refusal. Owner module and milestone match the current-source-map and repository-file-inventory rows (both byte-identical 39->40: True); implementation not executed. |
| FW-03 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | new-40 | analysis.rs hands the host observation to run-termination section 7 (ported TERM7 passes) and captures stage returns into ExecutionInputsV1. S40-01 routes here too: the capture cannot be implemented deterministically from published text until the attribution law is published. Owner module and milestone match the current-source-map and repository-file-inventory rows (both byte-identical 39->40: True); implementation not executed. |
| FW-04 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | new-40 | imports.rs implements the typed-null targetUniverse account, the single H import identity and exact-snapshot correspondence; the policy-test imported-row subject-and-universe join is confirmed (P40-POLICY). Read and child evidence only. Owner module and milestone match the current-source-map and repository-file-inventory rows (both byte-identical 39->40: True); implementation not executed. |
| FW-05 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | new-40 | comparison.rs implements presence knowledge (ported probe passes) and the first-applicable indeterminateReason order, which was read; no independent probe of the order. Owner module and milestone match the current-source-map and repository-file-inventory rows (both byte-identical 39->40: True); implementation not executed. |
| FW-06 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | new-40 | finalization.rs projects the delivery laws (ported query probe) and the run-termination section 6 and 7.3 commit-inventory recipe, recomputed independently over a closed Run (P40-RUNTERM-ADV). Owner module and milestone match the current-source-map and repository-file-inventory rows (both byte-identical 39->40: True); implementation not executed. |
| FW-07 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | new-40 | invocation.rs computes argvDigest over C(argv); the text is unchanged 39->40, read-confirmed and covered by an executed author control, not independently probed. Owner module and milestone match the current-source-map and repository-file-inventory rows (both byte-identical 39->40: True); implementation not executed. |
| FW-08 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | new-40 | outcomes.rs implements the section 7 detail allowlist (ported TERM7) and the closed candidate comparison: errorCode, faultCause and signal reach NOT_DERIVED, and an unknown member refuses first (P40-RUNTERM-ADV). Owner module and milestone match the current-source-map and repository-file-inventory rows (both byte-identical 39->40: True); implementation not executed. |
| FW-09 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | new-40 | review.rs candidates/inspect carriers are re-confirmed by the ported query probe; the suppressedCount observation (OBS40-09) still means the host derives the count from the producing step. Owner module and milestone match the current-source-map and repository-file-inventory rows (both byte-identical 39->40: True); implementation not executed. |
| FW-10 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | new-40 | repair.rs is the repair:2 constructor owner; the ported probe re-confirms refusal before the descriptor and exact-class unavailability. Owner module and milestone match the current-source-map and repository-file-inventory rows (both byte-identical 39->40: True); implementation not executed. |
| FW-11 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | new-40 | comparison.rs baseline.show carriers and pivot closure availability are re-confirmed by the ported query controls. Owner module and milestone match the current-source-map and repository-file-inventory rows (both byte-identical 39->40: True); implementation not executed. |
| FW-12 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | new-40 | review.rs review.produce-brief stays a host-only query operation (ported query probe). Owner module and milestone match the current-source-map and repository-file-inventory rows (both byte-identical 39->40: True); implementation not executed. |
| FW-13 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | new-40 | configuration.rs routes policy-test admission: an unregistered fact universe token is CONFIG.INVALID on source40 (P40-POLICY); the recommend config2 joins are re-confirmed by the ported probe. Owner module and milestone match the current-source-map and repository-file-inventory rows (both byte-identical 39->40: True); implementation not executed. |
| FW-14 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | new-40 | discovery.rs recommend discovery units now follow U-1 effective allowJs and U-4b.2 folding (P40-NATIVE); NATIVE_DEFAULT_SELECTION_WITHOUT_UNIT is re-confirmed by the ported probes. Owner module and milestone match the current-source-map and repository-file-inventory rows (both byte-identical 39->40: True); implementation not executed. |
| FW-15 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | new-40 | policy.rs owns policy show/test: S39-01 and S39-02 are closed at source level (P40-POLICY); policy show accepting an unregistered token is inspection, not analysis admission (OBS40-03). Owner module and milestone match the current-source-map and repository-file-inventory rows (both byte-identical 39->40: True); implementation not executed. |
| DR-001 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | inherited-unchanged-39 | current-source-map and the residual ledgers are byte-identical 39->40, and the reading path was refreshed on source40. The successor routing in inherited-residuals.proposed.md (byte-identical 39->40: True) is consistent with source40; original custody and standing preserved. |
| DR-002 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | new-40 | The identity/evidence/proof chain holds: the commit-inventory recipe was recomputed over a closed Run. S40-01 is an identity-determinism gap in ExecutionInputsV1 attribution, routed to the execution-inputs owner, and it keeps this obligation open. The successor routing in inherited-residuals.proposed.md (byte-identical 39->40: True) is consistent with source40; original custody and standing preserved. |
| DR-003 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | new-40 | Read-only carrier routes are re-confirmed by the ported probe. The 54 recovery cases remain unexecuted, and real platform demonstration remains a release requirement. The successor routing in inherited-residuals.proposed.md (byte-identical 39->40: True) is consistent with source40; original custody and standing preserved. |
| DR-004 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | new-40 | The native contract changed (U-1 effective allowJs, U-4b.2 nested folding and unit kinds, ADV39-01 account) and was read complete. The native group passes 388/388 and unit kinds are enforced at full-Run closure. The successor routing in inherited-residuals.proposed.md (byte-identical 39->40: True) is consistent with source40; original custody and standing preserved. |
| DR-005 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | new-40 | Executable custody groups pass on source40, the ported custody probe passes, and nested project boundaries exclude nested workspace markers. Native product carrier qualification is still required. The successor routing in inherited-residuals.proposed.md (byte-identical 39->40: True) is consistent with source40; original custody and standing preserved. |
| DR-006 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | new-40 | The descriptor graph is unchanged: the ported query probe re-checks graph-query-3 bytes, and the full-replay child passes. The successor routing in inherited-residuals.proposed.md (byte-identical 39->40: True) is consistent with source40; original custody and standing preserved. |
| DR-007 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | new-40 | The D9 published successor artifact remains a carried implementation-unit obligation, not a new blocker. The run-termination clarifications add no D9 code or public detail (the registry is unchanged at 315 codes). The successor routing in inherited-residuals.proposed.md (byte-identical 39->40: True) is consistent with source40; original custody and standing preserved. |
| DR-008 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | inherited-unchanged-39 | The applied retention posture is unchanged. The successor routing in inherited-residuals.proposed.md (byte-identical 39->40: True) is consistent with source40; original custody and standing preserved. |
| DR-009 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | new-40 | The run-termination section 3, 6 and 7.3 clarifications keep the host observation outside the sealed Run; the commit inventory is a separate record over a closed Run, preserving lifetime neutrality. The successor routing in inherited-residuals.proposed.md (byte-identical 39->40: True) is consistent with source40; original custody and standing preserved. |
| DR-010 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | new-40 | Bounded first-party composition is unchanged (prototype-report-inventory byte-identical: True). The policy-test verifier now agrees with bounded composition on the six discriminating cases; it remains reference evidence, not composition authority. The successor routing in inherited-residuals.proposed.md (byte-identical 39->40: True) is consistent with source40; original custody and standing preserved. |
| DR-011 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | inherited-unchanged-39 | Individual dispositions exist; the blind implementer litmus follows final integration and is not closed here. The successor routing in inherited-residuals.proposed.md (byte-identical 39->40: True) is consistent with source40; original custody and standing preserved. |
| DR-011-R01 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | new-40 | The fact-plane successor schemas are unchanged 39->40 (identity-schemas byte-identical: True); policy test now consumes their policyUniverseMap as the closed token set. The successor routing in inherited-residuals.proposed.md (byte-identical 39->40: True) is consistent with source40; original custody and standing preserved. |
| DR-011-R02 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | new-40 | Imperative plugins stay outside D-371. PolicyTestSuiteV2 admission is closed, and rule and fact universe tokens now refuse typed (P40-POLICY). The successor routing in inherited-residuals.proposed.md (byte-identical 39->40: True) is consistent with source40; original custody and standing preserved. |
| DR-011-R03 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | new-40 | The plan2/exec-plan2 membership law gains the unit-kind projection check (enumeration_model diff read). The enumeration child passes and full Runs refuse reminted kinds. The successor routing in inherited-residuals.proposed.md (byte-identical 39->40: True) is consistent with source40; original custody and standing preserved. |
| DR-011-R04 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | inherited-unchanged-39 | The carrierFormat axis mapping is unchanged (carrier-dispatch byte-identical: True). The successor routing in inherited-residuals.proposed.md (byte-identical 39->40: True) is consistent with source40; original custody and standing preserved. |
| DR-011-R05 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | inherited-unchanged-39 | The Rust protocol major 3 is unchanged, and the native group passes. The successor routing in inherited-residuals.proposed.md (byte-identical 39->40: True) is consistent with source40; original custody and standing preserved. |
| DR-011-R06 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | new-40 | identity-model is byte-identical 39->40 (True); the analysis-seal and query-projection children re-exercise the typed close_run outcomes on source40. The successor routing in inherited-residuals.proposed.md (byte-identical 39->40: True) is consistent with source40; original custody and standing preserved. |
| DR-011-R07 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | inherited-unchanged-39 | Query retained availability routes are unchanged, and the query-projection child passes (204 checks). The successor routing in inherited-residuals.proposed.md (byte-identical 39->40: True) is consistent with source40; original custody and standing preserved. |
| DR-011-R08 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | new-40 | The D9 published successor artifact remains carried (DR-007); nothing in source40 claims to discharge LIVE D9 (native-evidence.md:3018). The successor routing in inherited-residuals.proposed.md (byte-identical 39->40: True) is consistent with source40; original custody and standing preserved. |
| DR-011-R09 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | new-40 | Semantic IDs still exclude attempt identity, and policytest2 identity is a function of the suite alone (P40-POLICY identity preimages). S40-01 is a capture-encoding ambiguity, not attempt identity leaking into semantics. The successor routing in inherited-residuals.proposed.md (byte-identical 39->40: True) is consistent with source40; original custody and standing preserved. |
| DR-011-R10 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | inherited-unchanged-39 | OPEN: this nonblind review cannot close the fresh blind implementer litmus. The successor routing in inherited-residuals.proposed.md (byte-identical 39->40: True) is consistent with source40; original custody and standing preserved. |
| DR-011-R11 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | new-40 | ADV38-02 and ADV38-03 remain closed. Real platform durability is unmeasured and the 54 cases are not executed. The successor routing in inherited-residuals.proposed.md (byte-identical 39->40: True) is consistent with source40; original custody and standing preserved. |
| DR-011-R12 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | new-40 | Depends on TCB-SCOPE-01, assessed once on source40. The successor routing in inherited-residuals.proposed.md (byte-identical 39->40: True) is consistent with source40; original custody and standing preserved. |
| DR-011-R13 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | new-40 | Source40 changes discovery outcomes without relabelling record majors (the jsconfig allowJs:false membershipDigest differs 39->40). The composition profile states that a changed value changes ancestor identity normally and an unchanged record shape needs no relabel; PolicyTestSuiteV2 and repair:2 still refuse major 1. The successor routing in inherited-residuals.proposed.md (byte-identical 39->40: True) is consistent with source40; original custody and standing preserved. |
| DR-011-R14 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | inherited-unchanged-39 | CFG-6/TM is unchanged. The successor routing in inherited-residuals.proposed.md (byte-identical 39->40: True) is consistent with source40; original custody and standing preserved. |
| DR-011-R15 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | new-40 | The trusted request context stays host-only: the ported query probe re-confirms that HostQueryParams operations are not public. The successor routing in inherited-residuals.proposed.md (byte-identical 39->40: True) is consistent with source40; original custody and standing preserved. |
| DR-011-R16 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | inherited-unchanged-39 | No executable report-hook admission: prototype-report-inventory (True) and admission section 5 (True) are byte-identical 39->40. The successor routing in inherited-residuals.proposed.md (byte-identical 39->40: True) is consistent with source40; original custody and standing preserved. |
| DR-201 | ROUTING-ASSESSED-ONLY-NOT-APPLIED | ROUTING-ASSESSED-ONLY-NOT-APPLIED | new-40 | The semantic-correctness owner row (Run versus command finalization, post-commit output failure) is byte-identical. The source40 run-termination clarifications and the S40-01 capture-determinism gap fall in its area. Register 08 is byte-identical 39->40 (True). This review is an input to the integrated review and is not applied. |
| DR-202 | ROUTING-ASSESSED-ONLY-NOT-APPLIED | ROUTING-ASSESSED-ONLY-NOT-APPLIED | inherited-unchanged-39 | The delivery/operations owner row (recovery, repair, loader TCB) is byte-identical. Read-only carriers and repair:2 are re-confirmed by the ported probes. Register 08 is byte-identical 39->40 (True). This review is an input to the integrated review and is not applied. |
| DR-203 | ROUTING-ASSESSED-ONLY-NOT-APPLIED | ROUTING-ASSESSED-ONLY-NOT-APPLIED | inherited-unchanged-39 | The prototype-lessons owner row (PARTIAL-SCOPED) is byte-identical. No delta file is the prototype reference, and prototype-report-inventory is byte-identical (True). Register 08 is byte-identical 39->40 (True). This review is an input to the integrated review and is not applied. |
| DR-204 | ROUTING-ASSESSED-ONLY-NOT-APPLIED | ROUTING-ASSESSED-ONLY-NOT-APPLIED | new-40 | The V1/coop invariant owner row (exact selector/digest posture) is byte-identical. This review validated selectors and digests independently; ADV40-01 is an editorial digest-posture note in its spirit, and S40-01 is an identity-determinism gap. Register 08 is byte-identical 39->40 (True). This review is an input to the integrated review and is not applied. |
| DR-205 | ROUTING-ASSESSED-ONLY-NOT-APPLIED | ROUTING-ASSESSED-ONLY-NOT-APPLIED | new-40 | The small-core/components owner row (core/TCB boundaries) is byte-identical. TCB-SCOPE-01 remains coherent on source40. Register 08 is byte-identical 39->40 (True). This review is an input to the integrated review and is not applied. |

## Retained obligations

```json
{
 "residuals": 30,
 "authorGradesPending": 30,
 "condition2Obligations": 28,
 "condition2Source": "docs/v2/architecture/08-decision-and-readiness-register.md:385-391 (byte-identical 39->40: True)",
 "qualificationGatesUnperformed": 32,
 "qualificationGatesQualifiedTrue": 0,
 "recoveryCasesNotExecuted": 54,
 "condition5": "NOT MET (not a design defect)",
 "d9PublishedSuccessor": "Carried implementation-unit obligation (DR-007 / DR-011-R08); not a new blocker.",
 "finalApplication": "Must be performed by a NEW other actual Claude origin, not this origin (85a08aec-9d22-4ac6-8ec2-c10170e727d7) and not any author, design or blind origin."
}
```

## Authority

```json
{
 "gradeGranted": false,
 "activationGranted": false,
 "implementationAuthorized": false,
 "blindReconstructionClaimed": false,
 "source39ReviewConclusionInherited": false,
 "frozenInputsModified": false,
 "applicationOrReadinessGranted": false,
 "consumerArtifactsAccessedOrRepaired": false,
 "historicalExportsRelabelled": false,
 "productCommitPushOrActivation": false,
 "subagentsOrWebUsed": false
}
```

## Limitations

- Nonblind review. The reviewer read the author package, header-named root and codex evidence, and its own source39 review. No blind consumer artifact, its implementation, root replay results, private logs or the preliminary root source40 reference v1 were used.
- Reference Python models over synthetic inputs; no product code exists. No compiler, provider, host, OS durability, process isolation or cryptography is qualified. All 32 gates are unperformed and the 54 recovery cases are not executed (condition 5 NOT MET).
- Changed files that were not fresh-read were read as complete 39->40 diffs (delta40Read), not as whole files. This includes the five source-pins ledgers, whose pins are additionally exercised by the six executed pin-gated groups. Whole-file claims are made only for fresh40Read and inheritedUnchanged39Read; range reads and search-only sightings are listed separately.
- Several probes are not full Runs. Policy test compares the fixture with bounded production composition. Nested Cargo is at discover_units and enumeration-law level (full-Run closure was used for unit kinds). Comparison knowledge and custody are helper-level. The viewDigests probes use the maintained owner graph with reviewer-minted views and do not mint a multi-capability enumeration plan: reachability rests on enumeration-contract cell law and the capability matrix, seen via search and script output.
- OBS40-04 (consistent remint) was measured on the syntax-universe fixture, which has no tsjs program cell.
- Failed attempts are preserved and not counted. Run-termination attempt 1 (a probe defect: commit_inventory returns (record, digest)) is in receipts/probes/runterm-adv-v40.attempt1-probe-defect.json and receipts/runs/runterm-adv-v40.run.json. View-attribution attempt 1 (a harness defect: store pointers not recomputed after mutation, so the refusal was EXECUTION_INPUTS_REF_POINTER) is in receipts/runs/viewdigests-v40c.run.json and its stdout. Its probe receipt path was overwritten by attempt 2 because a separate copy was not permitted.
- In-process patches (the fixture helper assign_membership during full Runs, checker globals) were restored, and the probe copy was re-verified against the formal manifest after every run.
- The six ported source39 probes run with unedited expectations. Their owner bytes are unchanged 39->40 except check-workflow-projection, whose changed controls ran as a child, not as a ported probe.
- The package verifier and native probe are author tools re-executed on this review's copy. Content equality with the root verification and rebuild is evidence, not independent reconstruction. The 4 normalization-map negatives are exact recorded refusals and are not generalized.
- F-01..F-14 content lives outside the snapshot and was not re-derived.
- S40-01 predates source40 (execution-inputs owner bytes unchanged 39->40); this origin's source39 review missed it.
- No grade, activation, application, readiness or implementation authorization is granted. The 30 residuals, 28 condition-2 obligations and the D9 successor obligation are retained.

## Build gaps

none
