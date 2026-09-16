# Independent design review — source42 (whole-design successor)

**Reviewer:** Claude (independent design review origin 85a08aec-9d22-4ac6-8ec2-c10170e727d7, continuing after the completed source40 review; source42 charter; authored none of the reviewed bytes)  
**Standing:** Source42 whole-design successor review. Not fresh-origin independence, blind reconstruction, application acceptance, implementation authorization or qualification.

## Verdict: ACCEPT

No MUST, no SHOULD, no blocker. S40-01 is resolved on the complete source42 bytes including the capture follow-on: section 3 publishes the view attribution predicate and the section 3 named-scope law now holds for every applicability; section 8 and the model make receipts capture explicit returns and make selection equal the union of complete receipts. Independent three-tree discrimination with full-Run closure confirms each change (26/26); the historical 76/86 execution-inputs and 46 enumeration cases are preserved field for field. The programEntry clarification is consistent and its enforcement is confirmed (24/24 owner cases). ADV40-01 is resolved without mutating layer8. ADV42-01 is a non-blocking advisory: admission does not state or check receipt/view producer equality, nor apply the PLAN_JOIN before the row filter; Run closure refuses every measured shape. Subject, archive, parent41, last-reviewed40, both deltas, six pinned groups, 17 children, planning and inventory checks, package v19 and every probe completed; all copies re-verified. Source-level acceptance only: no blind reconstruction, application, readiness, implementation authorization or product qualification is granted.

## Subject

| Item | Value |
|---|---|
| subjectManifestSha256 | `f602fc7e45a90e32e0d076aa27e4ee7e51d8c298727a69bdf32489d5a7b0b307` |
| liveManifestSha256Measured | `f602fc7e45a90e32e0d076aa27e4ee7e51d8c298727a69bdf32489d5a7b0b307` |
| verifiedManifest | `True` |
| subjectFileCount | `12913` |
| subjectTotalBytes | `737766584` |
| subjectArchiveSha256 | `2423c7807b489ef9af199f6eb4c44cc8a42b53160555621cf4b6a65d56fcb4c6` |
| archiveSha256Measured | `2423c7807b489ef9af199f6eb4c44cc8a42b53160555621cf4b6a65d56fcb4c6` |
| parent41 | `eb7a4c48d86c844914ffc0ef70743752655a411e453bbaa066cfaee572312236` declared by 42: True; snapshot verified: True (12912 members) |
| last-reviewed40 | `3be452843acb6f5f234dfc1826b627a234d81e5a45edd70715a03715d7467072` declared by 41: True; snapshot verified: True (12911 members) |
| delta 41to42 | 16 changed, 1 added, 0 removed |
| delta 40to42 | 16 changed, 2 added, 0 removed |
| delta 40to41 | 12 changed, 1 added, 0 removed |
| planning input layer v11 | `75ea60653d8c7c36d754b163a11c0cd63e3d963f59ab6ccfe12c3c2a34a0d2de` |

## Issues

No MUST issue. No SHOULD issue.

### ADV42-01 (ADVISORY): Execution-inputs admission neither states nor checks that a complete receipt's view outputRefs carry that receipt's producerClosure, and raises the section 3 PLAN_JOIN only for candidate views whose producer matches some row; Run closure is the backstop

- docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md:12 (section 1: receipts rooted in producer obligations; outputRefs constrained by domain only)
- execution-inputs-contract.v1.md:51 and :53 (section 3: stage-spec producerClosure and view planId checks; "a candidate view whose planId is not the Plan's refuses EXECUTION_INPUTS_PLAN_JOIN")
- execution-inputs-contract.v1.md:299 (section 8: the builder places each explicit returned view on the view stage whose producerClosure it carries)
- docs/coop/design-corrections/foundation/execution_inputs_model.v1.py:1057-1093 (receipt checks compare receipt and stage spec, never an outputRef view producer)
- execution_inputs_model.v1.py:1132-1139 (the per-row producer filter precedes the planId check)
- execution_inputs_model.v1.py:1626-1640 (an attributed view is compared with the producer of its ROW's receipt, not of the receipt that lists it)
- docs/coop/design-corrections/foundation/identity-model.v3.py:1842-1851 and identity-schemas.v3.json byField view.producerClosure=provider (Run closure: VIEW_PLAN_JOIN, UNSELECTED_PRODUCER, closure kind)

**Detail.** A captured, unattributed view whose producerClosure is not the receipt's producer admits at execution-inputs admission on source40, source41 and source42, even with a foreign planId, and the complete Run refuses it only at closure (CLOSURE_FIELD_KIND:view.producerClosure:provider). A foreign-planId view from the stage's own provider refuses EXECUTION_INPUTS_PLAN_JOIN as section 3 says, because it passes a row's producer filter first. By reading, the model never compares a complete receipt's outputRef views with that receipt's producerClosure, and it checks attributed views against their own row's receipt. In a Plan with two view stages of two Plan-selected providers, a view of provider P2 listed on P1's complete receipt would therefore pass admission and the closure checks measured here. No maintained multi-provider graph exists, so that shape was not exercised.

**Consequence.** No Run closes with the measured shapes; for them the contract's named refusal and the refusing owner differ. The unexercised multi-provider shape would be a self-contradictory stage-return record, a detectable host capture error rather than an omission. It is not attribution nondeterminism for one captured observation, and it is pre-existing since source40.

**Disposition.** ADVISORY, non-blocking. Owners may state in sections 1/3 that every complete-receipt view outputRef carries that receipt's producerClosure (existing EXECUTION_INPUTS_STAGE_PRODUCER), apply the planId check to every candidate view before the row filter, and add a two-stage two-provider control. Not a SHOULD: no contradiction reaches an admitted Run in any measured world, the refusal chain is closed by the Run owner, and the TCB boundary is unchanged.

**Measured**

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
 "threeTreesForeignPlanId": {
  "source40": {
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
   "marksOnRows": {
    "foreignPlan": []
   },
   "marksCaptured": {
    "foreignPlan": true
   },
   "marksSelected": {
    "foreignPlan": true
   },
   "executionInputsDigest": "e4b5d7d1999670d9283bd006e5843b3a3af3d5664d01e58b9c4dcad07ccac1d1"
  },
  "source41": {
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
   "marksOnRows": {
    "foreignPlan": []
   },
   "marksCaptured": {
    "foreignPlan": true
   },
   "marksSelected": {
    "foreignPlan": true
   },
   "executionInputsDigest": "e4b5d7d1999670d9283bd006e5843b3a3af3d5664d01e58b9c4dcad07ccac1d1"
  },
  "source42": {
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
   "marksOnRows": {
    "foreignPlan": []
   },
   "marksCaptured": {
    "foreignPlan": true
   },
   "marksSelected": {
    "foreignPlan": true
   },
   "executionInputsDigest": "e4b5d7d1999670d9283bd006e5843b3a3af3d5664d01e58b9c4dcad07ccac1d1"
  }
 },
 "threeTreesForeignProducer": {
  "source40": {
   "admission": {
    "result": "ADMIT",
    "refusals": []
   },
   "fullRun": {
    "closed": false,
    "refused": "AdmissionError:CLOSURE_FIELD_KIND:view.producerClosure:provider"
   },
   "marksOnRows": {
    "foreignProducer": []
   },
   "marksCaptured": {
    "foreignProducer": true
   },
   "marksSelected": {
    "foreignProducer": true
   },
   "executionInputsDigest": "e3116a31fb6ad99653556d8a0d3e614c69d9220d87679cf998c9e972c920a4d9"
  },
  "source41": {
   "admission": {
    "result": "ADMIT",
    "refusals": []
   },
   "fullRun": {
    "closed": false,
    "refused": "AdmissionError:CLOSURE_FIELD_KIND:view.producerClosure:provider"
   },
   "marksOnRows": {
    "foreignProducer": []
   },
   "marksCaptured": {
    "foreignProducer": true
   },
   "marksSelected": {
    "foreignProducer": true
   },
   "executionInputsDigest": "e3116a31fb6ad99653556d8a0d3e614c69d9220d87679cf998c9e972c920a4d9"
  },
  "source42": {
   "admission": {
    "result": "ADMIT",
    "refusals": []
   },
   "fullRun": {
    "closed": false,
    "refused": "AdmissionError:CLOSURE_FIELD_KIND:view.producerClosure:provider"
   },
   "marksOnRows": {
    "foreignProducer": []
   },
   "marksCaptured": {
    "foreignProducer": true
   },
   "marksSelected": {
    "foreignProducer": true
   },
   "executionInputsDigest": "e3116a31fb6ad99653556d8a0d3e614c69d9220d87679cf998c9e972c920a4d9"
  }
 }
}
```

## Observations (not defects)

- **OBS42-01** Reference builder limitation: execution_inputs_fixture.v3.py:228-243 attributes a returned view by the same-scope universe+relation test alone, without the section 3 producer or planId filter that execution_inputs_model.v1.py:1135-1139 applies. In a multi-producer graph the builder would name views the model refuses (VIEW_TOTALITY). Maintained graphs have one producer; this is a construction defect of the reference fixture, not missing law. (source read)
- **OBS42-02** Binder shorthand: enumeration-contract.v1.md:24 says the universe is the owner admission of "this selected context + this programEntry + this extent (bind_typescript_universe / bind_rust_universe / bind_syntax_universe)". The binders take (universe, admission, context, retained, snapshot_inventory) and no programEntry (native_evidence_model.v2.py:2939, 2988, 3229, signatures seen in search output). For TS/JS the entry reaches the universe through the retained TypeScriptConfigGraphV1.entryConfigPath that enumeration_model.v1.py:809-817 compares. The construction rule immediately after (:26-35) states that for Rust and syntax-only the retained entry is the universe H itself. The shorthand is imprecise but disambiguated within the same section and invents no Rust/syntax input: not a material ambiguity. (source read; receipts/probes/program-entry-x.json)
- **OBS42-03** Refs-only returned view: on source42 the builder captures a view named only on evaluationInputRefs, so a Run whose semantic evidence omits it refuses EVALUATION_VIEW_ROOTS; source40/41 dropped it and closed without it (FW7: {"source40": {"closed": true, "verdict": "indeterminate", "runId": "run3:f039aa034bb7bb19ab629a67add1873888490bd766e03260bbefe6bcddf3210e", "sameManifest": true}, "source41": {"closed": true, "verdict": "indeterminate", "runId": "run3:f039aa034bb7bb19ab629a67add1873888490bd766e03260bbefe6bcddf3210e", "sameManifest": true}, "source42": {"closed": false, "refused": "AdmissionError:EVALUATION_VIEW_ROOTS"}}). This follows the section 8 builder inputs and the root refs-only decision. (receipts/probes/view-attribution-x.json)
- **OBS42-04** Re-encoding under the selected same-scope interpretation: a view whose binding universe and capability relation sit on different scopes was attributed and closed on source40 under ExecutionInputsV1 digest 05f003891dfea7e8. Source42 captures it on no row and closes under digest ac865bcf2ef221a1. This is a published prerelease identity change for one capture, not two admissions of one observation. (receipts/probes/view-attribution-x.json)
- **OBS42-05** Explicit js-synthesized available bindings are now never admissible: the null entry refuses on source42 (['ENUMERATION_BINDING_PROGRAM_ENTRY']), and a non-null entry refuses on both trees because the retained entryConfigPath of a synthesized program is null (['ENUMERATION_BINDING_PROGRAM_ENTRY']). This is consistent with native section 2.2 (synthesized exactly when the entry is null) and the construction table (explicit TS/JS names a config). (receipts/probes/program-entry-x.json)
- **OBS42-06** Unavailable bindings keep programEntry freedom: default or explicit, null or non-null, all four variants admit on source41 and source42. No owner states a canonical encoding, and different values are different Plan inputs. (receipts/probes/program-entry-x.json)
- **OBS42-07** Against codex final-reference.v42 and root-source42-final-reference.v3, all six group stdouts are byte-equal (True) and 15 of 17 child stdouts are byte-equal; enumeration and execution-inputs differ only in ownedHashes/receiptPath. The codex runner-original equals root v3: True. (receipts/reference-comparison.json)
- **OBS42-08** Re-observed on unchanged bytes by the ported source40 probes on source42: the policy.show acceptance of an unregistered token, the fixture representation limit for available optional imported evidence without a row, the consistent mode-and-kind remint under trusted markers, the omitted-allowJs observation default, one broad installPath row, the case-variant segment, the suppressedCount join, a repair:2 declared unavailability class, and admit_repair_plan_v2 as identity admission. (receipts/probes (ported))

## Current dispositions of source40 findings, advisories and observations

| id | current disposition | basis |
|---|---|---|
| S40-01 | RESOLVED-ON-COMPLETE-SOURCE42-BYTES | Execution-inputs contract section 3 (:53) now publishes the attribution predicate: candidate views are the complete-receipt view outputRefs, exactly the view members of selectedRefs (SELECTED_COVER); same producer P; one and the same scope at U whose relation is the first element of a matrix [relation, resolution] pair; the matrix cell state plays no part; candidate-only capabilities attribute by U alone; one view may sit on several rows; an unselected enumerator or null U attributes nothing; the canonical set is exact (VIEW_TOTALITY); a captured unattributed view stays lawful and selected; and every named scope of an attributed view is at U (COVERAGE_DERIVE). Section 8 (:299) makes receipts capture the explicit returned views and never the census, and the model enforces exact stage-produced totality (:1671-1690). For one captured observation the attributed rows are now a deterministic published function. The source40 two-encoding demonstration (a returned view recorded or not recorded) is, as the charter notes, two different host observations; under source42 the builder records every explicit return, so only the observation itself stays host TCB. |
| ADV40-01 | RESOLVED | implementation-planning-sources.v1.json standing now selects architecture.manifestPath (v11) as current, marks previous layers historical, and names v8 a superseded intermediate whose native-evidence digest matches neither frozen39 nor frozen40. v8 bytes 99c8f876... are unchanged from source40 and listed in priorArchitectureInputLayers with their digest. No historical layer was mutated. |
| OBS40-01 | RETAINED-OBSERVATION | workflows-and-surfaces and policy_test_model bytes unchanged 40->42; the ported policy probe re-observes it. |
| OBS40-02 | RETAINED-OBSERVATION | Bytes unchanged; ported policy probe (26/26). |
| OBS40-03 | RETAINED-OBSERVATION (OBS42-08) | Bytes unchanged; policy.show remains inspection, not admission. |
| OBS40-04 | RETAINED-OBSERVATION | Native bytes unchanged; the ported native probe re-closes the consistent remint under trusted markers. |
| OBS40-05 | RETAINED-OBSERVATION | Native bytes unchanged; re-observed. |
| OBS40-06 | RETAINED-OBSERVATION | Native bytes unchanged; re-observed. |
| OBS40-07 | CLOSED | The no-op scope-level enumeratorClosure continue was removed by the attribution correction (execution_inputs_model.v1.py 40->42 diff; the loop now tests one same-scope condition). |
| OBS40-08 | SUPERSEDED (historical comparison not relabelled) | The source42 reference comparison is OBS42-07. |
| OBS40-09 | RETAINED (OBS42-08) | Ported probes re-observe it on unchanged owner bytes. |
| OBS40-10 | HISTORICAL CORRECTION STANDS | The mapping population is 322 on source40, source41 and source42 (measured), with 0 rows changed. |
| S39-01 | REMAINS CLOSED | policy_test_model and section 5 bytes unchanged 40->42; the ported discrimination against source39 bytes passes on source42. |
| S39-02 | REMAINS CLOSED | Bytes unchanged; the ported universe-token and imported-universe discrimination passes on source42. |
| ADV39-01 | REMAINS CLOSED | Native section 10 account and registered bytes unchanged; the ported run-termination/registration probe passes (24/24). |
| ADV38-01 | REMAINS CLOSED | Run-termination section 7 and model unchanged; ported section 7 probe passes (24/24). |
| ADV38-02 | REMAINS CLOSED | carrier-dispatch unchanged; ported read-only carrier probe passes (108 rows). |
| ADV38-03 | REMAINS CLOSED | commit-recovery-readonly unchanged 40->42; source39 measurement stands. |

## Item dispositions

### CH42-ATTRIBUTION-LAW: SUFFICIENT AND CONSISTENT

Each required property is stated in contract section 3 and implemented by the model; the table separates existing-law enforcement from the newly selected deterministic interpretation. Section 5 (:221-249) now refers to section 3 for which views are reached, and the schema description at execution-inputs.schema.v1.json:621 ("captured receipt views attributed to this cell/program/U/producer") agrees with the published candidate set. The remaining admission-scope note is ADV42-01. Joins verified at their owners: stage/receipt (model :1042-1093), row receipt producer (:1618-1640), plan (:883-894), selection (evaluator_input_model :26-45), Run closure (identity-model :1797-1851).

| property | classification | selectors | note |
|---|---|---|---|
| same producer P and the Plan | EXISTING LAW ENFORCED | contract :51 and :53; model :1135-1139; closure identity-model :1842-1845 | Unchanged across trees; admission scope limit recorded in ADV42-01. |
| universe and relation on ONE AND THE SAME scope | NEWLY SELECTED DETERMINISTIC INTERPRETATION (previously model-only separate booleans) | contract :53; model :1147-1155; fixture :232-243 | Re-encodes split-scope views (OBS42-04); consistent with section 5 :236-249. |
| relation-column membership (first element of [relation, resolution]) | PUBLISHED PIN OF EXISTING MODEL BEHAVIOUR | contract :53; model :1129 | Not independently probed beyond the checker run; the model reading is unchanged since source40. |
| matrix cell state plays no part (UNSUPPORTED-TYPED attributes like supported) | PUBLISHED EXISTING MODEL BEHAVIOUR | contract :53, section 5 :174-188 | The references view sits on the references row on every tree. |
| candidate-only capability attributes by U alone | PUBLISHED EXISTING MODEL BEHAVIOUR | contract :53; model :1152 (not cap_rels) | The any-scope-at-U and same-scope-at-U readings coincide when the relation set is empty; candidate cases are identical across trees. |
| exact canonical set (VIEW_TOTALITY) | EXISTING LAW ENFORCED | contract :53; model :1165-1168 | Identical on every tree. |
| no view names on an unselected enumerator or null U | EXISTING LAW ENFORCED | contract :53; model :1140-1141 | Identical on every tree. |
| every named scope of an attributed view at the binding U, for every applicability | EXISTING LAW NEWLY ENFORCED (unsupported and coverage-less scopes previously bypassed) | contract :51, :53, section 5 :236-249; model :1157-1164 | source40 admits and closes; source41/42 refuse at admission and in the Run. |
| valid captured unattributed views | EXISTING CAPTURE LAW, BUILDER NOW FAITHFUL | contract :12-19, :53, :299; fixture :341-353 | source40/41 builders dropped them (EVALUATION_VIEW_ROOTS). |
| cross-universe target relations | EXISTING LAW PRESERVED | section 5 :154-165, :236-239; model :1163 compares sourceUniverse only | Admits and closes on every tree. |
| one view on several rows of one program/U | PUBLISHED EXISTING MODEL BEHAVIOUR | contract :53 | Byte-identical manifest and RunId on every tree. |

### CH42-CAPTURE: SUFFICIENT AND CONSISTENT

Receipts capture the explicit returned views (viewIds/viewId and view refs on evaluationInputRefs) and never the ambient census: a census-only view is never captured and leaves the digest equal to the control on every tree. A captured unattributed view is selected and on no row, and closes on source42. Stage-produced selectedRefs equals the union of complete receipts exactly: a reminted receipt that omits a selected attributed view admitted and closed on source40/41 and refuses SELECTED_COVER on source42 in both worlds, and a receipt view missing from selectedRefs refuses on every tree. A refs-only view is captured, so evidence omitting it refuses (OBS42-03). Capture detects internal inconsistency, not malicious omission; the TCB limitation of section 1 :24 stands.

### CH42-HISTORICAL-POPULATIONS: ACCOUNTED

Each tree's own execution-inputs checker ran on its verified copy: source40 76 cases, source41 86, source42 95, 0 mismatches each. All shared cases are field-identical (path fields excluded) 40->41 (76 shared), 41->42 (86) and 40->42 (76), and the shared full-run RunIds are equal. The 10 cases added by the attribution correction include 7 closed-run cases (closed=False on naming-no-view, host-naming split scope and supported two-universe rows), and the 9 capture cases include 6 closed-run cases (closed=False on census-only, its control and the pair-reading encoding); both counts are read from the checker diff. Enumeration: source41 46 cases, source42 54, 46 shared cases field-identical, unit-kind and unit-root controls identical. These are reference self-consistency counts, not independent proof; the independent discrimination is CH42-ATTRIBUTION-LAW and CH42-CAPTURE.

### CH42-PROGRAM-ENTRY-CLARIFICATION: CONSISTENT; NO SEMANTIC CHANGE

Enumeration contract section 1 (:21-47) restates AvailableProgramBindingV1.programEntry (schema :380-390). A default available binding is null; for tsconfig/jsconfig markers the admission-derived entry is the U-1 marker, for js-synthesized a null entry with no nodes. An explicit TS/JS binding names the selected config and equals the retained entryConfigPath. Rust and syntax-only are keyed by the universe H. The syntax-only sentence (:21) now correctly cites the U-9 fallback unit. The WRONG example (:46) is exactly what admission refuses (ts-default-marker-nonnull refuses on both trees), and the explicit marker selection it keeps lawful admits on both. Unavailable bindings get no rule (OBS42-06).

### CH42-PROGRAM-ENTRY-ENFORCEMENT: CONFIRMED

enumeration_model.v1.py:803-807 now refuses ENUMERATION_BINDING_PROGRAM_ENTRY for an available explicit-plan-selection binding with a null entry in every TS/JS mode, enforcing the schema's non-null TS/JS extra-program law that source41 admitted when the null happened to equal the U-1 derivation. Independently discriminated at the enumeration owner: ts-tsconfig, js-allowjs and js-synthesized explicit null admit on source41 and refuse exactly on source42; defaults, explicit marker and build-config selections, Rust and syntax (null or non-null) and every unavailable variant are unchanged. Complete Run closure consumes the same owner admission (evaluator_input_model.v3.py:103-104), so the refusal reaches the Run as EVALUATOR_ENUMERATION_JOIN. The checker adds 8 cases; the 46 shared cases are identical. Standalone atom and workflow fragments with explicit null TS bindings never call admit_enumeration and are not complete Runs, so they are not an admission regression.

### CH42-IDENTITY-DIGEST-SCOPE: SUFFICIENTLY EXPLICIT; NO CLARIFICATION REQUIRED

identity-and-evidence.md:407-418 scopes the closing digest law to identity-schemas.v3. :420-433 extends the same law, with a named sweep refusal, to every foundation record document the closure walks through a {document, selector} record, lists them, and says identity-schemas and the relation payload document carry their own sweeps. :920-934 states that the native contract extends the law to its own bundle and that relation-payload-schemas.v2.json carries its own x-opensip-digest-law. Each vocabulary's owner is named, and an unannotated position refuses mechanically in each scope, so a reader cannot mistake which law governs a document.

### CH42-COMPOSITION7-AND-POLICY-DERIVATION3: SOURCE40 NO-GAP FINDINGS PRESERVED

evaluator-composition-contract.v3.md and evaluator_replay_model.v3.py are byte-identical 40->42 (True, True). This origin's source40 assessment stands on unchanged bytes. Section 7 closes OUTPUT typed-prefix references in their prefix-selected domains. Input identities named by outputs are fixed by the section 9 equality addresses to inputs admitted before replay. policy-derivation3 is a derived projection admitted by equality under section 9.7, carrying no runId. Not re-read this charter.

### CH42-PLANNING-V11: CONFIRMED (population measured)

v11 binds 31 current inputs with no mismatch and no self-binding. v11, v10 and v9 are byte-identical (75ea6065...); coverage subject and planning architecture name v11, and v10 is the previous layer. priorArchitectureInputLayers lists v1-v9 with digests matching their bytes. There are 322 mappings on source40, source41 and source42 with 0 rows changed; 24 report features; 198 paths in 20 packages; M0-M6; 54 recovery cases, none executed.

### CH42-PACKAGE19: VERIFIED AS AUTHOR EVIDENCE

See packageAssessment.

### CH42-CURRENT-REFERENCE: OWN EXECUTION PASSES; HEADER RECEIPTS CONSISTENT

This review's six groups and 17 children pass on its own verified copy, with 95 execution-inputs and 54 enumeration cases at 0 mismatches. The header-named codex final-reference.v42 report hashes to d46d0bf2..., binds f602fc7e... and passed; its runner-original equals root-source42-final-reference.v3. Root v1 and v2 were not used, and no source40 result is relabelled.

### CH42-SCOPE-PRESERVATION: RE-EXECUTED ON SOURCE42

The source40 scope probes were ported with only runtime paths changed (receipts/probe-port.json) and pass on source42: policy.test, native discovery/unitKind/allowJs/nested Cargo, run-termination and registration, nine command carriers and twenty operations, read-only carriers, comparison knowledge, repair:2, section 7 termination, custody and fallback. Their owner bytes are unchanged 40->42.

## Package v19

Package v19 verified as author evidence. Every one of its 387 files matches artifact manifest 346a4d4b...; the formal42 manifest f602fc7e... and the files-only projection e732b21b... are different objects with equal file members; the rebuild base is package15 constructors (6a8d4fec...) plus the native-v2 migration overlay (overlay base digests match retained package15), not package16/17/18, which remain unchanged history; all 17 exports carry new RunIds and no historical export is relabelled. This review re-executed verify-package.py and probe-native-v2.py on its own verified copy: groups checkpoint3 1 (passed True, exit 0), normalized-examples6 4 (passed True, exit 0), rust-selection-examples1 2 (passed True, exit 0), semantic-controls1 3 (passed True, exit 1), binding-controls 3 (passed True, exit 1), normalization-map-controls1 4 (passed True, exit 1), query 7 (passed True, exit None); 17 exports and 7 queries; three control groups exit 1 because their exported stores are refusing controls and the verifier records passed=true for every group. The verification and every compared output file are content-equal to the root final42 verification, and the 9 membership comparisons are content-equal to the root rebuild probe.

- Author construction and self-consistency evidence; verify-package.py and probe-native-v2.py are author tools re-executed here, not an independent or blind reconstruction.
- Four TypeScript normalization-map negatives ARE executed (exact refusals below). The Rust map negative is unexercised.
- The partial and/or/not consumer helper remains unexercised; count-at-most/all-covered remain unimplemented; two-binding qualification is incomplete.
- The binding-controls group now carries the explicit-selection and default-entry controls (ts-lawful-explicit-selection admits, ts-invalid-default-entry refuses ENUMERATION_BINDING_PROGRAM_ENTRY at semantic admission).
- No compiler, provider, OS or process-isolation qualification; independent grades granted: 0; all 30 author-proposed grades stay PENDING final application.

| control | owner admission | semantic admission | reason |
|---|---|---|---|
| ts-map-absent | REFUSE | NOT-REACHED | BODY_NORMALIZATION_MAP_MISSING:opensip-interface/normalization/specification-map.v1.json |
| ts-map-level-unmapped | REFUSE | NOT-REACHED | BODY_NORMALIZATION_LEVEL_UNMAPPED:L0-verbatim |
| ts-map-level-swapped | REFUSE | NOT-REACHED | BODY_NORMALIZATION_LEVEL_VERSION_MISMATCH:L0-verbatim |
| ts-spec-outside-closure | REFUSE | NOT-REACHED | BODY_NORMALIZATION_SPECIFICATION_NOT_IN_CLOSURE:L0-verbatim |

## Commands and probes

| group | exit | seconds | stdout sha256 |
|---|---|---|---|
| evaluator3 | 0 | 515.7 | `2ddf8f99c46365462636ae191ff71c1800424e00c460fc335bc47f9a3659ef1b` |
| foundation | 0 | 131.5 | `2a7cd6d84cf029f12d43c4a34c7a91b4817167f8d88e07dc1721c87f78ef3ded` |
| integration | 0 | 16.6 | `3fccd9e3a400774d6f411e530a22848ec38eae5a30e737f4c66bf75254d20112` |
| native | 0 | 3.0 | `49fca461221535d2306dfe19a99cec49a26e6bc78ed3c9f777473073b65a1406` |
| security | 0 | 0.9 | `60d498d317776373a82f941db5a82a78b5eca33ba6d8f57eeb387a9a081ca746` |
| workflows | 0 | 9.9 | `954ebf2eedafc242f2998bcfb9f4ff4c18bd80063ad9b0edce34b7beebd14e51` |

evaluator3 children: 17, all exit 0: True; execution-inputs cases 95, enumeration cases 54. Planning: {'check_implementation_planning': 0, 'check_repository_file_inventory': 0}. Planning counts ok: True.

| probe | rows | failed | run receipt | earlier attempts |
|---|---|---|---|---|
| P42-SUBJECT | (command receipt) | - | receipts/subject-verification.json, receipts/manifest42-index.json | - |
| P42-ARCHIVE | (command receipt) | - | receipts/archive-verification.source42.json, receipts/archive-verification.source42-pkg.json | - |
| P42-BASE-COPIES | (command receipt) | - | receipts/archive-verification.base40.json, receipts/archive-verification.base41.json | - |
| P42-DELTA | (command receipt) | - | receipts/delta-diff-summary.json | - |
| P42-GROUPS | (command receipt) | - | receipts/reference/groups-report.all.json, receipts/reference/evaluator3.stdout, receipts/reference/foundation.json | - |
| P42-REFERENCE-COMPARE | (command receipt) | - | receipts/reference-comparison.json | - |
| P42-COPIES-FINAL | (command receipt) | - | receipts/copy-verification-final.json | - |
| P42-VIEW-ATTRIBUTION-X | 26 | 0 | receipts/runs/view-attribution-x.run.json | 0 |
| P42-CAPTURE-JOINS | 4 | 0 | receipts/runs/capture-joins-42.run.json | 0 |
| P42-PROGRAM-ENTRY-X | 25 | 0 | receipts/runs/program-entry-x.attempt2.run.json | 1 |
| P42-CASE-POPULATIONS | - | 0 | receipts/runs/case-populations.run.json | 0 |
| P42-ENUMERATION-POPULATION | - | 0 | receipts/runs/enumeration-case-population.run.json | 0 |
| P42-PACKAGE19 | 22 | 0 | receipts/runs/package-v19-evidence.run.json | 0 |
| P42-PLANNING | - | 0 | receipts/runs/planning-checks.run.json | 0 |
| P42-PORTED-POLICY | 26 | 0 | receipts/runs/ported-policy.run.json | 0 |
| P42-PORTED-NATIVE | 39 | 0 | receipts/runs/ported-native.run.json | 0 |
| P42-PORTED-RUNTERM | 24 | 0 | receipts/runs/ported-runterm-adv.run.json | 0 |
| P42-PORTED-QUERY | 98 | 0 | receipts/runs/query-carriers.run.json | 0 |
| P42-PORTED-CARRIER | 108 | 0 | receipts/runs/carrier-readonly.run.json | 0 |
| P42-PORTED-COMPARISON | 28 | 0 | receipts/runs/comparison-knowledge.run.json | 0 |
| P42-PORTED-REPAIR2 | 16 | 0 | receipts/runs/repair2.run.json | 0 |
| P42-PORTED-TERM7 | 24 | 0 | receipts/runs/run-termination-s7.run.json | 0 |
| P42-PORTED-CUSTODY | 20 | 0 | receipts/runs/native-custody-fallback.run.json | 0 |

## Read coverage

Whole-file claims only for fresh42Read (every line read this charter) and inheritedUnchanged40Read (counted as completely read by this origin's completed source40 review and byte-identical now; not re-read). complete40ReadPlusComplete42Diff is a complete predecessor read plus the exact diff. delta reads, range reads, evidence reads and search-only sightings are not whole-file reads of source42 bytes. Hashes recomputed at build time.

```json
{
 "fresh42Read": 4,
 "fresh42RangeRead": 10,
 "deltaReads": 16,
 "complete40ReadPlusComplete42Diff": 0,
 "inheritedUnchanged40Read": 51,
 "changedPriorReadNotReread": 0,
 "evidenceReads": 14
}
```

Delta files without a read entry: none. Byte-identical to a fresh read: {"docs/v2/architecture/implementation-normative-inputs.v10.json": ["docs/v2/architecture/implementation-normative-inputs.v11.json"]}.

Fresh whole-file reads:

- docs/coop/design-corrections/foundation/enumeration-contract.v1.md (186 lines)
- docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md (303 lines)
- docs/coop/design-corrections/foundation/execution_inputs_fixture.v3.py (505 lines)
- docs/v2/architecture/implementation-normative-inputs.v11.json (160 lines)

Range reads:

- docs/coop/design-corrections/foundation/check-enumeration.v1.py: 60-349
- docs/coop/design-corrections/foundation/check-execution-inputs.v1.py: 1-108, 696-815
- docs/coop/design-corrections/foundation/enumeration-plan.schema.v1.json: 330-489
- docs/coop/design-corrections/foundation/enumeration_model.v1.py: 425-519, 740-879
- docs/coop/design-corrections/foundation/evaluator_graph_fixture.v3.py: 1-60, 280-390
- docs/coop/design-corrections/foundation/evaluator_input_model.v3.py: 1-175
- docs/coop/design-corrections/foundation/evaluator_semantic_fixture.v3.py: 148-307, 560-809
- docs/coop/design-corrections/foundation/execution_inputs_model.v1.py: 150-244, 860-1464, 1600-1733
- docs/coop/design-corrections/foundation/identity-model.v3.py: 866-960, 1760-1944
- docs/v2/contracts/product-v1/identity-and-evidence.md: 400-474, 912-966

Complete diff reads:

- docs/coop/design-corrections/foundation/check-execution-inputs.v1.py (delta40to42Read)
- docs/coop/design-corrections/foundation/evaluator3-source-pins.v1.json (delta40to42Read)
- docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md (delta40to42Read)
- docs/coop/design-corrections/foundation/execution_inputs_fixture.v3.py (delta40to42Read)
- docs/coop/design-corrections/foundation/execution_inputs_model.v1.py (delta40to42Read)
- docs/coop/design-corrections/foundation/source-pins.v1.json (delta40to42Read)
- docs/coop/design-corrections/native/source-pins.v2.json (delta40to42Read)
- docs/coop/design-corrections/security/source-pins.v1.json (delta40to42Read)
- docs/coop/design-corrections/workflows/source-pins.v1.json (delta40to42Read)
- docs/coop/design-corrections/workflows/workflows-report.v1.json (delta40to42Read)
- docs/v2/architecture/implementation-coverage.v1.json (delta40to42Read)
- docs/v2/architecture/implementation-planning-sources.v1.json (delta40to42Read)
- docs/coop/design-corrections/foundation/check-enumeration.v1.py (delta41to42Read)
- docs/coop/design-corrections/foundation/enumeration-contract.v1.md (delta41to42Read)
- docs/coop/design-corrections/foundation/enumeration_model.v1.py (delta41to42Read)
- docs/coop/design-corrections/foundation/evaluator_graph_fixture.v3.py (delta41to42Read)

Evidence reads:

- /private/tmp/opensip-design-corrections/claude-independent-design.v42/receipts/planning-clarification-after-to-source42.diff: 1-183
- /tmp/opensip-design-corrections/author-package-final42-verification.v1/verification.json: complete
- /tmp/opensip-design-corrections/claude-attribution-capture-assessment.v1/review.md: complete
- /tmp/opensip-design-corrections/claude-author-package-successor.v19/source-binding.v42.json: complete
- /tmp/opensip-design-corrections/claude-program-entry-clarification.v1/review.md: complete
- /tmp/opensip-design-corrections/claude-program-entry-enforcement.v1/review.md: complete
- /tmp/opensip-design-corrections/claude-view-attribution-assessment.v1/review.md: complete
- /tmp/opensip-design-corrections/root-author-package-final42-rebuild.v1/rebuild-report.json: 1-120
- /tmp/opensip-design-corrections/root-capture-integration.v1/integration.json: complete
- /tmp/opensip-design-corrections/root-planning-layer-history-clarification.v1/assessment.json: complete
- /tmp/opensip-design-corrections/root-planning-layer-history-clarification.v1/change.diff: complete
- /tmp/opensip-design-corrections/root-program-entry-clarification-integration.v1/integration.json: complete
- /tmp/opensip-design-corrections/root-program-entry-enforcement-integration.v1/assessment.json: complete
- /tmp/opensip-design-corrections/root-view-attribution-integration.v1/integration.json: complete

Inherited unchanged source40 whole-file reads (not re-read): 51 files, listed in review.json.

## TCB-SCOPE-01 (assessed once)

**Assumption.** Selected authenticated in-process host/evaluator code is trusted; providers and inert inputs are untrusted; adversarial code sharing the process is outside this product threat model.

**Consequence.** Rejecting or changing the assumption reopens all thirteen dependent rows jointly. It is a scope selection, not a containment proof; it repairs no historical attack and is not thirteen independent proofs. All thirteen author grades stay PENDING.

**Dependent rows (13).** RES-EP13-02, RES-EP13-04, RES-EP13-12, RES-EP13-13, RES-EP13-16, RES-EP13-18, IR-EP13-NB-01, IR-EP13-NB-03, IR-EP13-NB-04, AX6, AX9, MD5, RX2c

- Coherent as a scope selection on source42: admission section 5 (byte-identical 40->42: True) and prototype-report-inventory (byte-identical: True) still admit no untrusted native/WASM, imperative contributions or executable report hooks.
- The source42 changes add typed data admission, not trust: foreign named scopes, internally inconsistent receipts and explicit TS/JS null entries refuse at owner admission and in the Run.
- Capture remains a host TCB observation of stage returns (execution-inputs section 1 :24). SELECTED_COVER detects internal inconsistency, not malicious omission; ADV42-01 records a residual detectable inconsistency that admission does not check, which is not a trust-boundary violation.
- Providers stay untrusted: view producer closures must be Plan-selected providers at Run closure (CLOSURE_FIELD_KIND / UNSELECTED_PRODUCER measured).
- Unqualified: it rests on the authenticated closure/TCB inventory and provider process boundaries, and all 32 gates are unperformed (qualified=true 0).

**Position:** NOT REJECTED. **Standing:** ASSESSED-COHERENT-UNQUALIFIED-ON-SOURCE42; final application adjudication not granted. **Adjudication owner:** separate final application review, by a NEW different actual Claude origin (not this origin 85a08aec-9d22-4ac6-8ec2-c10170e727d7 and not any author, design or blind origin)

## Disposition rows (107)

All rows: appliedByThisReview=false, finalApplicationOutcomeGranted=false. No grade is assigned.

**Basis rule.** unchanged-40-basis: the governing owner bytes are byte-identical 40->42, and the conclusion rests on that identity plus this origin's named source40 row assessment, quoted in unchanged40Basis. Re-executed suites are corroboration only. new-42: the conclusion rests on a source42 read, diff, probe or measurement newly performed under this charter. Every row carries its own current text, current owner and consequence; no row is carried forward in bulk, and no grade is assigned. Counts: {"new-42": 36, "unchanged-40-basis": 71}.

| id | prior40 | disposition | basis | current assessment | owner | consequence |
|---|---|---|---|---|---|---|
| F-01 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | unchanged-40-basis | F-01: prior root standing RE-VERIFIED-ON-PACKAGE13 (root-independent36-completion-assessment.v1) carried. The F record lives outside the snapshot and none of the 19 source40->42 delta files is an F record. | root custody of the F record (outside the frozen snapshot) | No source42 change; remains carried without regrade and is not source42 acceptance. |
| F-02 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | unchanged-40-basis | F-02: prior root standing RE-VERIFIED-ON-PACKAGE13 (root-independent36-completion-assessment.v1) carried. The F record lives outside the snapshot and none of the 19 source40->42 delta files is an F record. | root custody of the F record (outside the frozen snapshot) | No source42 change; remains carried without regrade and is not source42 acceptance. |
| F-03 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | unchanged-40-basis | F-03: prior root standing RE-VERIFIED-ON-PACKAGE13 (root-independent36-completion-assessment.v1) carried. The F record lives outside the snapshot and none of the 19 source40->42 delta files is an F record. | root custody of the F record (outside the frozen snapshot) | No source42 change; remains carried without regrade and is not source42 acceptance. |
| F-04 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | unchanged-40-basis | F-04: prior root standing INHERITED (root-independent36-completion-assessment.v1) carried. The F record lives outside the snapshot and none of the 19 source40->42 delta files is an F record. | root custody of the F record (outside the frozen snapshot) | No source42 change; remains carried without regrade and is not source42 acceptance. |
| F-05 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | unchanged-40-basis | F-05: prior root standing RE-VERIFIED-ON-PACKAGE13 (root-independent36-completion-assessment.v1) carried. The F record lives outside the snapshot and none of the 19 source40->42 delta files is an F record. | root custody of the F record (outside the frozen snapshot) | No source42 change; remains carried without regrade and is not source42 acceptance. |
| F-06 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | unchanged-40-basis | F-06: prior root standing RE-VERIFIED-ON-PACKAGE13 (root-independent36-completion-assessment.v1) carried. The F record lives outside the snapshot and none of the 19 source40->42 delta files is an F record. | root custody of the F record (outside the frozen snapshot) | No source42 change; remains carried without regrade and is not source42 acceptance. |
| F-07 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | unchanged-40-basis | F-07: prior root standing INHERITED (root-independent36-completion-assessment.v1) carried. The F record lives outside the snapshot and none of the 19 source40->42 delta files is an F record. | root custody of the F record (outside the frozen snapshot) | No source42 change; remains carried without regrade and is not source42 acceptance. |
| F-08 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | unchanged-40-basis | F-08: prior root standing RE-VERIFIED-ON-PACKAGE13 (root-independent36-completion-assessment.v1) carried. The F record lives outside the snapshot and none of the 19 source40->42 delta files is an F record. | root custody of the F record (outside the frozen snapshot) | No source42 change; remains carried without regrade and is not source42 acceptance. |
| F-09 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | unchanged-40-basis | F-09: prior root standing INHERITED (root-independent36-completion-assessment.v1) carried. The F record lives outside the snapshot and none of the 19 source40->42 delta files is an F record. | root custody of the F record (outside the frozen snapshot) | No source42 change; remains carried without regrade and is not source42 acceptance. |
| F-10 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | unchanged-40-basis | F-10: prior root standing RE-VERIFIED-ON-PACKAGE13 (root-independent36-completion-assessment.v1) carried. The F record lives outside the snapshot and none of the 19 source40->42 delta files is an F record. | root custody of the F record (outside the frozen snapshot) | No source42 change; remains carried without regrade and is not source42 acceptance. |
| F-11 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | unchanged-40-basis | F-11: prior root standing RE-VERIFIED-ON-PACKAGE13 (root-independent36-completion-assessment.v1) carried. The F record lives outside the snapshot and none of the 19 source40->42 delta files is an F record. | root custody of the F record (outside the frozen snapshot) | No source42 change; remains carried without regrade and is not source42 acceptance. |
| F-12 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | unchanged-40-basis | F-12: prior root standing RE-VERIFIED-ON-PACKAGE13 (root-independent36-completion-assessment.v1) carried. The F record lives outside the snapshot and none of the 19 source40->42 delta files is an F record. | root custody of the F record (outside the frozen snapshot) | No source42 change; remains carried without regrade and is not source42 acceptance. |
| F-13 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | unchanged-40-basis | F-13: prior root standing RE-VERIFIED-ON-PACKAGE13 (root-independent36-completion-assessment.v1) carried. The F record lives outside the snapshot and none of the 19 source40->42 delta files is an F record. | root custody of the F record (outside the frozen snapshot) | No source42 change; remains carried without regrade and is not source42 acceptance. |
| F-14 | CARRIED-NOT-REGRADED | CARRIED-NOT-REGRADED | unchanged-40-basis | F-14: prior root standing RE-VERIFIED-ON-PACKAGE13 (root-independent36-completion-assessment.v1) carried. The F record lives outside the snapshot and none of the 19 source40->42 delta files is an F record. | root custody of the F record (outside the frozen snapshot) | No source42 change; remains carried without regrade and is not source42 acceptance. |
| RES-EP13-01 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-42 | Plan and derivation joins stay inside complete replay: the three-tree probe closes lawful worlds and refuses foreign named scopes and reminted receipts at Run closure on the same manifests (P42-VIEW-ATTRIBUTION-X), and the full-replay child passes. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING; residual retained. |
| RES-EP13-02 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-42 | Depends on TCB-SCOPE-01. Capture remains a host observation of stage returns; a non-provider-producer view on a receipt is refused only at closure (ADV42-01), so no answer-provenance claim against the host is made. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING; reopens with TCB-SCOPE-01 only. |
| RES-EP13-03 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | unchanged-40-basis | Admission contract and residual ledger are byte-identical 40->42. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING; finite historical measurement unchanged. |
| RES-EP13-04 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-42 | Depends on TCB-SCOPE-01. Closed input admission now also refuses foreign named scopes on attributed views, internally inconsistent receipts, and explicit TS/JS bindings with null entries (P42-VIEW-ATTRIBUTION-X, P42-PROGRAM-ENTRY-X). Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING; reopens with TCB-SCOPE-01 only. |
| RES-EP13-05 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-42 | The frozen subject was verified outside every author instrument: formal42 manifest, archive, all 12,913 members, parent41 (12,912) and last-reviewed40 (12,911), declared chain and both deltas. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING. |
| RES-EP13-06 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-42 | canonical.py is outside the delta; the ported run-termination probe recomputes the commit-inventory digest over a closed source42 Run with the reviewer's own C()/H(). Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING. |
| RES-EP13-07 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | unchanged-40-basis | Seal and replay owners are byte-identical 40->42; the analysis-seal child passes. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING. |
| RES-EP13-08 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | unchanged-40-basis | A bounded historical measurement; source42 claims no proof over all PlanIntents. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING. |
| RES-EP13-09 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-42 | Provenance stays distinct from correctness: semantic-controls1 keeps owner ADMIT and semantic REFUSE, content-equal to the root final42 verification, and a foreign coverage-less scope that source40 admitted and closed now refuses. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING. |
| RES-EP13-10 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-42 | Author self-counters did not decide this review: the 19 added checker cases are reference self-consistency, and the independent three-tree discrimination runs each tree's own modules. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING. |
| RES-EP13-11 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-42 | Failures stay recorded by cause: this review keeps its programEntry probe attempt 1 harness failure, and root reference v1 (pre-correction) and v2 (launch failure) are not used. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING. |
| RES-EP13-12 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-42 | Depends on TCB-SCOPE-01. No sole Python guard enters product authority; SELECTED_COVER detects internal capture inconsistency, never malicious omission. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING; reopens with TCB-SCOPE-01 only. |
| RES-EP13-13 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-42 | Depends on TCB-SCOPE-01. Discrimination probes run each tree in its own process on verified copies, all re-verified unchanged afterwards (copy-verification-final.json). Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING; reopens with TCB-SCOPE-01 only. |
| RES-EP13-14 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | unchanged-40-basis | The differential census is not used as an oracle; unchanged. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING. |
| RES-EP13-15 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-42 | The C-2 v4 self-census is not elevated: the enumeration programEntry change is exercised by the 54-case checker and the independent 24-case owner probe, not by a census. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING. |
| RES-EP13-16 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-42 | Depends on TCB-SCOPE-01. Producer flags cannot bypass replay: row attribution is re-derived at admission and compared exactly (VIEW_TOTALITY on every tree). Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING; reopens with TCB-SCOPE-01 only. |
| RES-EP13-17 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | unchanged-40-basis | Text-only disclosures remain text-only. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING. |
| RES-EP13-18 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | unchanged-40-basis | Depends on TCB-SCOPE-01. Native discovery and custody bytes are unchanged; marker observations stay trusted (ported native probe re-observes). Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING; reopens with TCB-SCOPE-01 only. |
| RES-EP13-19 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-42 | Substantive review with discriminating probes on three byte sets and full-Run closure; all pinned groups pass and an advisory was still found. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING. |
| IR-EP13-NB-01 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-42 | Depends on TCB-SCOPE-01. Every probe ran in-process with owner modules; containment is not claimed. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING; reopens with TCB-SCOPE-01 only. |
| IR-EP13-NB-02 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-42 | No name scan decides scope: attribution compares the first element of matrix pairs and universe values on one scope record, never spellings. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING. |
| IR-EP13-NB-03 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-42 | Depends on TCB-SCOPE-01. Loaded owner instances stay reachable in-process; the capture record is a trusted host observation, which is why the boundary is trust. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING; reopens with TCB-SCOPE-01 only. |
| IR-EP13-NB-04 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-42 | Depends on TCB-SCOPE-01; one TCB account covers all thirteen rows. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING; reopens with TCB-SCOPE-01 only. |
| IR-EP13-NB-05 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-42 | Contradictory prose still needed substantive review: the bounded author review found the section 5 "already decides today" sentence false for unsupported rows, and it was corrected with law-conforming controls. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING. |
| IR-EP13-NB-06 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | unchanged-40-basis | Historical attacker cost preserved as history. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING. |
| IR-EP13-NB-07 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | unchanged-40-basis | The original environment is preserved; this review names its interpreter (-I -B) and pins. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING. |
| AX6 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | unchanged-40-basis | Depends on TCB-SCOPE-01. No delta file claims same-process route-region protection. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING; reopens with TCB-SCOPE-01 only. |
| AX9 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-42 | Depends on TCB-SCOPE-01. The source42 additions (attribution predicate, capture exactness, programEntry enforcement) are typed data admission under a trusted evaluator. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING; reopens with TCB-SCOPE-01 only. |
| MD5 | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | unchanged-40-basis | Depends on TCB-SCOPE-01. Source42 adds no Python-containment mechanism. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING; reopens with TCB-SCOPE-01 only. |
| RX2c | ASSESSED-CONSISTENT-GRADE-PENDING | ASSESSED-CONSISTENT-GRADE-PENDING | new-42 | Depends on TCB-SCOPE-01. Complete replay and full-Run closure on the same manifest remain reproducibility evidence, not containment. Historical limitation preserved; no historical guard claimed repaired. | evaluation residual ledger (docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json); grade adjudication by the separate final application review | Grade PENDING; reopens with TCB-SCOPE-01 only. |
| AR-01 | NO-NEW-ISSUE | NO-NEW-ISSUE | unchanged-40-basis | Admission section 1 byte-identical; ported query carriers pass on source42. | docs/v2/contracts/product-v1/admission-and-qualification.md (§1) | No change required. |
| AR-02 | NO-NEW-ISSUE | NO-NEW-ISSUE | unchanged-40-basis | Admission sections 2-4 and gates byte-identical (32 gates, qualified=true 0). | docs/v2/contracts/product-v1/admission-and-qualification.md (§§2–4) | All gates stay unperformed. |
| AR-03 | NO-NEW-ISSUE | NO-NEW-ISSUE | unchanged-40-basis | Security contract byte-identical; ported custody probe passes. | docs/v2/contracts/product-v1/security-and-lifecycle.md (Discovery) | No change required. |
| AR-04 | NO-NEW-ISSUE | NO-NEW-ISSUE | unchanged-40-basis | Security trust time byte-identical. | docs/v2/contracts/product-v1/security-and-lifecycle.md (Trust time) | No change required. |
| AR-05 | NO-NEW-ISSUE | NO-NEW-ISSUE | unchanged-40-basis | Security root chain and revocation byte-identical. | docs/v2/contracts/product-v1/security-and-lifecycle.md (Root chain and revocation) | No change required. |
| AR-06 | NO-NEW-ISSUE | NO-NEW-ISSUE | unchanged-40-basis | Platform admission and carrier DDL byte-identical; security group passes. | docs/v2/contracts/product-v1/security-and-lifecycle.md (Platform admission) | No change required. |
| AR-07 | NO-NEW-ISSUE | NO-NEW-ISSUE | unchanged-40-basis | Native contract byte-identical 40->42; ported native probe passes (39 rows); native group 388/388. | docs/v2/contracts/product-v1/native-evidence.md (§§3/5/9) | No change required. |
| AR-08 | NO-NEW-ISSUE | NO-NEW-ISSUE | unchanged-40-basis | Invocation and repair text byte-identical; ported repair:2 probe passes. | docs/v2/contracts/product-v1/workflows-and-surfaces.md (Invocation and repair) | No change required. |
| AR-09 | CHANGES-REQUIRED (S40-01) | NO-NEW-ISSUE (ADVISORY ADV42-01) | new-42 | identity-and-evidence incorporates the execution-inputs and enumeration contracts, which changed. S40-01 is resolved: the attribution predicate and capture exactness are published and enforced, with independent three-tree discrimination and full-Run closure. ADV42-01 records the remaining admission-scope note; the closing digest law scope is sufficiently explicit. | docs/v2/contracts/product-v1/identity-and-evidence.md (§§1–6) | Source-level change requirement from source40 discharged; the advisory is optional. |
| AR-10 | NO-NEW-ISSUE | NO-NEW-ISSUE | unchanged-40-basis | Comparison text and model byte-identical; ported comparison knowledge passes. | docs/v2/contracts/product-v1/workflows-and-surfaces.md (Baseline and comparison) | No change required. |
| AR-11 | NO-NEW-ISSUE | NO-NEW-ISSUE | unchanged-40-basis | Comparison and import byte-identical; execution-inputs child passes with 95 cases. | docs/v2/contracts/product-v1/workflows-and-surfaces.md (Comparison and import) | No change required. |
| AR-12 | NO-NEW-ISSUE | NO-NEW-ISSUE | unchanged-40-basis | Native section 4 and atoms byte-identical; atoms child passes. | docs/v2/contracts/product-v1/native-evidence.md (§4) | No change required. |
| AR-13 | NO-NEW-ISSUE | NO-NEW-ISSUE | new-42 | The enumeration binding construction that native sections 1/2 bind into was clarified and enforced: explicit TS/JS null entries refuse, defaults and marker selections admit, and Rust/syntax/unavailable freedom is preserved (P42-PROGRAM-ENTRY-X). The binder shorthand is OBS42-02. | docs/v2/contracts/product-v1/native-evidence.md (§§1/2/6/8 plus workflow output/security discovery) | No change required. |
| AR-14 | NO-NEW-ISSUE | NO-NEW-ISSUE | unchanged-40-basis | Stage transition, lease and read-only carrier bytes unchanged; ported carrier probe passes. | docs/v2/contracts/product-v1/security-and-lifecycle.md (Stage transition and lease model) | No change required. |
| AR-15 | NO-NEW-ISSUE | NO-NEW-ISSUE | unchanged-40-basis | Contract index README byte-identical. | docs/v2/contracts/product-v1/README.md (Entire contract index and D-372 application) | No change required. |
| AR-16 | NO-NEW-ISSUE | NO-NEW-ISSUE | unchanged-40-basis | D9 and command-outcome text byte-identical; S39-01/S39-02 remain closed by the ported policy probe; D9 successor stays carried. | docs/v2/contracts/product-v1/workflows-and-surfaces.md (D9 and command outcomes plus native/security guidance) | No change required. |
| FW-01 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | new-42 | discovery.rs must emit default-unit bindings with a null programEntry (never the U-1 marker), explicit TS/JS programs with the selected config path equal to the retained entryConfigPath, and must not produce explicit js-synthesized available bindings (OBS42-05). Owner module and milestone match current-source-map and repository-file-inventory (both byte-identical 40->42: True). | crates/host/src/discovery.rs (M3) | Implementation obligation clarified; not executed. |
| FW-02 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | unchanged-40-basis | review.rs review-brief carriers unchanged; ported query probe passes. Owner module and milestone match current-source-map and repository-file-inventory (both byte-identical 40->42: True). | crates/host/src/review.rs (M5) | Not executed. |
| FW-03 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | new-42 | analysis.rs must capture explicit stage returns on the receipt of the producer that returned them, select exactly the union of complete receipts, and derive row viewDigests by the published section 3 predicate; ADV42-01 suggests checking receipt/view producer equality. Owner module and milestone match current-source-map and repository-file-inventory (both byte-identical 40->42: True). | crates/host/src/analysis.rs (M3) | Implementation obligation clarified; not executed. |
| FW-04 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | unchanged-40-basis | imports.rs unchanged; typed-null targetUniverse account stands. Owner module and milestone match current-source-map and repository-file-inventory (both byte-identical 40->42: True). | crates/host/src/imports.rs (M5) | Not executed. |
| FW-05 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | unchanged-40-basis | comparison.rs presence knowledge unchanged; ported probe passes. Owner module and milestone match current-source-map and repository-file-inventory (both byte-identical 40->42: True). | crates/host/src/comparison.rs (M5) | Not executed. |
| FW-06 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | unchanged-40-basis | finalization.rs delivery laws unchanged; commit-inventory recipe re-derived by the ported probe. Owner module and milestone match current-source-map and repository-file-inventory (both byte-identical 40->42: True). | crates/host/src/finalization.rs (M5) | Not executed. |
| FW-07 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | unchanged-40-basis | invocation.rs argvDigest unchanged. Owner module and milestone match current-source-map and repository-file-inventory (both byte-identical 40->42: True). | crates/host/src/invocation.rs (M5) | Not executed. |
| FW-08 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | unchanged-40-basis | outcomes.rs detail allowlist unchanged; ported section 7 probe passes. Owner module and milestone match current-source-map and repository-file-inventory (both byte-identical 40->42: True). | crates/host/src/outcomes.rs (M3) | Not executed. |
| FW-09 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | unchanged-40-basis | review.rs candidates/inspect carriers unchanged. Owner module and milestone match current-source-map and repository-file-inventory (both byte-identical 40->42: True). | crates/host/src/review.rs (M5) | Not executed. |
| FW-10 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | unchanged-40-basis | repair.rs repair:2 constructor unchanged; ported probe passes. Owner module and milestone match current-source-map and repository-file-inventory (both byte-identical 40->42: True). | crates/host/src/repair.rs (M5) | Not executed. |
| FW-11 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | unchanged-40-basis | comparison.rs baseline.show unchanged. Owner module and milestone match current-source-map and repository-file-inventory (both byte-identical 40->42: True). | crates/host/src/comparison.rs (M5) | Not executed. |
| FW-12 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | unchanged-40-basis | review.rs produce-brief host-only unchanged. Owner module and milestone match current-source-map and repository-file-inventory (both byte-identical 40->42: True). | crates/host/src/review.rs (M5) | Not executed. |
| FW-13 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | unchanged-40-basis | configuration.rs policy-test admission routes unchanged. Owner module and milestone match current-source-map and repository-file-inventory (both byte-identical 40->42: True). | crates/host/src/configuration.rs (M3) | Not executed. |
| FW-14 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | new-42 | discovery.rs recommend units: the same binding construction rule applies to recommended default and explicit programs (P42-PROGRAM-ENTRY-X). Owner module and milestone match current-source-map and repository-file-inventory (both byte-identical 40->42: True). | crates/host/src/discovery.rs (M3) | Implementation obligation clarified; not executed. |
| FW-15 | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | OWNER-ROUTING-ASSESSED-NOT-EXECUTED | unchanged-40-basis | policy.rs show/test unchanged; ported policy probe passes. Owner module and milestone match current-source-map and repository-file-inventory (both byte-identical 40->42: True). | crates/host/src/policy.rs (M5) | Not executed. |
| DR-001 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-40-basis | current-source-map and residual ledgers byte-identical. Successor routing in inherited-residuals.proposed.md (byte-identical 40->42: True) is consistent with source42. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Condition-1 obligation retained. |
| DR-002 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | new-42 | The identity/evidence chain now publishes ExecutionInputsV1 view attribution and exact stage-produced selection (S40-01 resolved). Successor routing in inherited-residuals.proposed.md (byte-identical 40->42: True) is consistent with source42. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Condition-1 obligation retained; source40 change requirement discharged at source level. |
| DR-003 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-40-basis | Read-only carrier routes unchanged; 54 recovery cases unexecuted. Successor routing in inherited-residuals.proposed.md (byte-identical 40->42: True) is consistent with source42. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Condition-1 obligation retained; release demonstration still required. |
| DR-004 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | new-42 | The native binding construction consumed by enumeration is clarified (programEntry discriminator versus retained entry) and enforced for explicit TS/JS nulls; native bytes unchanged. Successor routing in inherited-residuals.proposed.md (byte-identical 40->42: True) is consistent with source42. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Condition-1 obligation retained. |
| DR-005 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-40-basis | Custody reference groups pass; native carrier qualification still required. Successor routing in inherited-residuals.proposed.md (byte-identical 40->42: True) is consistent with source42. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Condition-1 obligation retained. |
| DR-006 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-40-basis | Descriptor graph unchanged; full-replay child passes. Successor routing in inherited-residuals.proposed.md (byte-identical 40->42: True) is consistent with source42. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Condition-1 obligation retained. |
| DR-007 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-40-basis | D9 published successor artifact remains a carried implementation-unit obligation; registry unchanged. Successor routing in inherited-residuals.proposed.md (byte-identical 40->42: True) is consistent with source42. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Mandatory future implementation-unit obligation; not a new blocker. |
| DR-008 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-40-basis | Applied retention posture unchanged. Successor routing in inherited-residuals.proposed.md (byte-identical 40->42: True) is consistent with source42. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Condition-1 obligation retained. |
| DR-009 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | new-42 | The host capture stays outside the sealed Run: selection equals the union of complete receipts exactly, and the operational census stays excluded (census-only digest equal to control). Successor routing in inherited-residuals.proposed.md (byte-identical 40->42: True) is consistent with source42. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Condition-1 obligation retained. |
| DR-010 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-40-basis | Bounded first-party composition unchanged. Successor routing in inherited-residuals.proposed.md (byte-identical 40->42: True) is consistent with source42. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Condition-1 obligation retained. |
| DR-011 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-40-basis | The blind implementer litmus follows final integration and is not closed here. Successor routing in inherited-residuals.proposed.md (byte-identical 40->42: True) is consistent with source42. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Condition-1 obligation retained. |
| DR-011-R01 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-40-basis | Fact-plane successor schemas unchanged. Successor routing in inherited-residuals.proposed.md (byte-identical 40->42: True) is consistent with source42. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Retained. |
| DR-011-R02 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-40-basis | Imperative plugins stay outside D-371. Successor routing in inherited-residuals.proposed.md (byte-identical 40->42: True) is consistent with source42. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Retained. |
| DR-011-R03 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | new-42 | plan2 EnumerationPlanV1 binding joins now refuse explicit TS/JS null entries; the 46 shared enumeration cases are identical. Successor routing in inherited-residuals.proposed.md (byte-identical 40->42: True) is consistent with source42. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Retained. |
| DR-011-R04 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-40-basis | carrierFormat mapping unchanged. Successor routing in inherited-residuals.proposed.md (byte-identical 40->42: True) is consistent with source42. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Retained. |
| DR-011-R05 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-40-basis | Rust protocol major 3 unchanged. Successor routing in inherited-residuals.proposed.md (byte-identical 40->42: True) is consistent with source42. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Retained. |
| DR-011-R06 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | new-42 | Typed close_run outcomes re-exercised: three-tree full Runs close or refuse with typed keys (EVALUATOR_EXECUTION_INPUTS_JOIN, EVALUATION_VIEW_ROOTS, CLOSURE_FIELD_KIND, REFERENCE_PLAN_JOIN). Successor routing in inherited-residuals.proposed.md (byte-identical 40->42: True) is consistent with source42. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Retained. |
| DR-011-R07 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-40-basis | Query retained availability routes unchanged; query-projection child passes. Successor routing in inherited-residuals.proposed.md (byte-identical 40->42: True) is consistent with source42. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Retained. |
| DR-011-R08 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-40-basis | D9 successor remains carried (DR-007). Successor routing in inherited-residuals.proposed.md (byte-identical 40->42: True) is consistent with source42. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Mandatory future implementation-unit obligation. |
| DR-011-R09 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | new-42 | Semantic identity still excludes attempt identity; the capture correction changes ExecutionInputsV1 only for graphs declaring unowned returned views, and shared cases and maintained RunIds are identical across trees. Successor routing in inherited-residuals.proposed.md (byte-identical 40->42: True) is consistent with source42. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Retained. |
| DR-011-R10 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-40-basis | OPEN: this nonblind review cannot close the fresh blind implementer litmus. Successor routing in inherited-residuals.proposed.md (byte-identical 40->42: True) is consistent with source42. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Retained open. |
| DR-011-R11 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-40-basis | Real platform durability unmeasured; 54 cases not executed. Successor routing in inherited-residuals.proposed.md (byte-identical 40->42: True) is consistent with source42. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Retained. |
| DR-011-R12 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | new-42 | Depends on TCB-SCOPE-01, assessed once on source42. Successor routing in inherited-residuals.proposed.md (byte-identical 40->42: True) is consistent with source42. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Retained; reopens with TCB-SCOPE-01 only. |
| DR-011-R13 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | new-42 | Prerelease identity changes (same-scope re-encoding, refs-only capture, explicit TS null refusal) change records without relabelling majors, consistent with the composition profile. Successor routing in inherited-residuals.proposed.md (byte-identical 40->42: True) is consistent with source42. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Retained. |
| DR-011-R14 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-40-basis | CFG-6/TM unchanged. Successor routing in inherited-residuals.proposed.md (byte-identical 40->42: True) is consistent with source42. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Retained. |
| DR-011-R15 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-40-basis | Trusted request context stays host-only. Successor routing in inherited-residuals.proposed.md (byte-identical 40->42: True) is consistent with source42. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Retained. |
| DR-011-R16 | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | CONDITION-1-OBLIGATION-RETAINED-ASSESSED | unchanged-40-basis | No executable report-hook admission; prototype-report-inventory and admission section 5 unchanged. Successor routing in inherited-residuals.proposed.md (byte-identical 40->42: True) is consistent with source42. | successor routing in docs/coop/design-corrections/inherited-residuals.proposed.md | Retained. |
| DR-201 | ROUTING-ASSESSED-ONLY-NOT-APPLIED | ROUTING-ASSESSED-ONLY-NOT-APPLIED | new-42 | Semantic-correctness owner row: the attribution and capture corrections and ADV42-01 fall in its area. Register 08 byte-identical 40->42 (True). | register 08 condition-3 review owner row DR-201 | Input to the integrated review; not applied. |
| DR-202 | ROUTING-ASSESSED-ONLY-NOT-APPLIED | ROUTING-ASSESSED-ONLY-NOT-APPLIED | unchanged-40-basis | Delivery/operations owner row: recovery, repair and loader TCB unchanged. Register 08 byte-identical 40->42 (True). | register 08 condition-3 review owner row DR-202 | Input to the integrated review; not applied. |
| DR-203 | ROUTING-ASSESSED-ONLY-NOT-APPLIED | ROUTING-ASSESSED-ONLY-NOT-APPLIED | unchanged-40-basis | Prototype-lessons owner row (PARTIAL-SCOPED): no delta file is the prototype reference. Register 08 byte-identical 40->42 (True). | register 08 condition-3 review owner row DR-203 | Input to the integrated review; not applied. |
| DR-204 | ROUTING-ASSESSED-ONLY-NOT-APPLIED | ROUTING-ASSESSED-ONLY-NOT-APPLIED | new-42 | V1/coop invariant owner row: selectors and digests independently validated; ADV40-01 resolved without mutating historical layer bytes; all pin ledgers repin only the eight changed files. Register 08 byte-identical 40->42 (True). | register 08 condition-3 review owner row DR-204 | Input to the integrated review; not applied. |
| DR-205 | ROUTING-ASSESSED-ONLY-NOT-APPLIED | ROUTING-ASSESSED-ONLY-NOT-APPLIED | new-42 | Small-core/components owner row: TCB-SCOPE-01 remains coherent on source42. Register 08 byte-identical 40->42 (True). | register 08 condition-3 review owner row DR-205 | Input to the integrated review; not applied. |

The quoted source40 basis of every unchanged-40-basis row is in review.json (`unchanged40Basis`).

## Retained obligations

```json
{
 "residuals": 30,
 "authorGradesPending": 30,
 "condition2Obligations": 28,
 "condition2Source": "docs/v2/architecture/08-decision-and-readiness-register.md:385-391 (byte-identical 40->42: True)",
 "qualificationGatesUnperformed": 32,
 "qualificationGatesQualifiedTrue": 0,
 "plannedRecoveryCasesUnperformed": 54,
 "condition5": "NOT MET (not a design defect)",
 "d9PublishedSuccessor": "Mandatory future implementation-unit obligation (DR-007 / DR-011-R08); not a newly invented design blocker.",
 "gradeAndConditionOwner": "All 30 evaluation grades and 28 condition-2 obligations belong to final application adjudication.",
 "finalApplication": "Requires a NEW different actual Claude origin, not this origin (85a08aec-9d22-4ac6-8ec2-c10170e727d7) and not any author, design or blind origin."
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
 "source40ReviewConclusionInherited": false,
 "frozenInputsModified": false,
 "applicationOrReadinessGranted": false,
 "productQualificationGranted": false,
 "consumerArtifactsAccessedOrRepaired": false,
 "historicalExportsRelabelled": false,
 "productCommitPushOrActivation": false,
 "subagentsWebOrPrivateLogsUsed": false
}
```

## Limitations

- Nonblind successor review by the same origin that completed the source40 review; not fresh-origin independence. Author proposals, root integration records, package evidence and codex/root reference receipts were read as evidence. No blind consumer artifact, result or implementation was read, and no blind link was followed.
- Reference Python models over synthetic inputs; no product code. No compiler, provider, host, OS durability, process isolation or cryptography is qualified. 32 gates and 54 recovery cases remain unperformed (condition 5 NOT MET).
- Whole-file claims are limited to fresh42Read and inheritedUnchanged40Read. Changed files not fresh-read were read as complete diffs (40->42 or 41->42). The v10 layer is byte-identical to the fully read v11. Range reads and search-only sightings are listed separately and are not whole-file reads.
- Closed-run discrimination used the maintained file fixture and the TypeScript semantic fixture; no multi-provider, multi-stage Plan was minted, so the ADV42-01 multi-provider shape is argued from source, not exercised. The relation-column pin and candidate-only attribution rest on reading plus unchanged shared checker cases, not an independent probe.
- programEntry discrimination is at the enumeration owner admission, which complete Run closure consumes; explicit-null full Runs were not re-closed independently.
- Failed attempt preserved and not counted: program-entry-x attempt 1 exited 1 because receipts/probes/ did not exist yet (harness defect); its children could not write side files. Kept at receipts/runs/program-entry-x.run.json with stdout/stderr; attempt 2 is the result.
- Ported source40 probes keep their original labels ("source40") as historical text; only runtime paths changed, and the current side is the verified source42 copy.
- The package verifier and native probe are author tools re-executed on this review's copy; content equality with root evidence is not independent reconstruction. Four TS normalization-map negatives are executed; the Rust map negative is unexercised; the partial and/or/not helper is unexercised; count/all are unimplemented; two-binding qualification is incomplete.
- Composition section 7, policy-derivation3 and other byte-identical owners rely on this origin's named source40 reads and assessments; they were not re-read this charter.
- No grade, activation, application, readiness, implementation authorization or product qualification is granted.

## Build gaps

none
