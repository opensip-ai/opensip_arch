import json,hashlib
from pathlib import Path
OUT='/tmp/opensip-design-corrections/post-reset-review.v5/'
idx=json.load(open(OUT+'probes/probe-index.json'))
rep=json.load(open(OUT+'probes/report-comparison-final.json'))
delta=json.load(open(OUT+'probes/delta.json'))
def sha(f): return hashlib.sha256(Path(f).read_bytes()).hexdigest()

r={
 "artifact":"opensip design/reference independent review",
 "version":"post-reset-review.v5",
 "reviewer":"actual Claude (Opus 5), fresh independent reviewer session; authored none of the subject bytes",
 "standing":"INDEPENDENT DESIGN-LAYER REVIEW; not blind consumer B; not application acceptance; not product qualification",
 "verdict":"ACCEPT",
 "acceptanceRule":"Every required design gap means CHANGES_REQUIRED. No required design gap was found; five advisories are recorded and none blocks acceptance.",
 "productQualification":False,
 "implementationAuthorized":False,
 "readinessChanged":False,
 "condition5":"NOT MET",
 "historicalGradesExtended":False,
 "syntheticTcbInputs":True,
 "syntheticTcbNote":"Synthetic signatures, host/OS observations, evaluator callbacks and locks are stated TCB assumptions, never native measurement or qualification.",

 "subject":{
  "manifest":"docs/coop/design-corrections/reviews/candidate-subject.v5.json",
  "manifestSha256":"ccb2311ddbcaea7e8bd540030621c982fa6757792721095a505e4e47652c74cf",
  "requiredSha256":"ccb2311ddbcaea7e8bd540030621c982fa6757792721095a505e4e47652c74cf",
  "manifestMatchesRequired":True,
  "predecessorManifestSha256":"2a2168c3006174ab5d130054144374698f2026686a0daab7ed1eca38c365c2e2",
  "predecessorVerified":True,
  "snapshotRoot":"/tmp/opensip-design-corrections/candidate-subject.v5",
  "fileCount":1419,"filesVerified":1419,"totalBytes":14259899,"bytesVerified":14259899,
  "mismatched":0,"missing":0,"undeclaredOnDisk":0,
  "verifiedBeforeReview":True,"verifiedAfterReview":True,
  "v4SnapshotReverified":{"files":1378,"mismatched":0},
  "retainedV4ReviewSha256":"2b703388c4c2ba24f5bbc557167803d4698d60d921bac097fc1fa13cf50b3851",
  "retainedV4ReviewIdenticalToRepository":True,
  "snapshotOrRepositoryEdited":False,"repinned":False
 },

 "delta":{
  "added":len(delta['added']),"removed":len(delta['removed']),"modified":len(delta['modified']),
  "unchanged":1358,
  "addedAreNormative":False,
  "addedNonReviewArtifacts":["docs/coop/design-corrections/historical-preservation-report.v5.json",
                             "docs/coop/design-corrections/post-reset-dispositions.v5.proposed.json"],
  "modifiedFiles":delta['modified'],
  "confinement":{
   "foundationUnit":"unchanged except source-pins",
   "nativeUnit":"unchanged except source-pins",
   "securityUnit":"model (one additive hunk) + source-pins only",
   "workflowsUnit":"model, checker, inventory, schema, cases, pins, two reports",
   "identityModelSchemasAndContract":"byte-identical to v4",
   "publicDetailRegistry":"byte-identical to v4",
   "governanceArtifacts":"all seven byte-identical to v4",
   "productContractsChanged":["native-evidence.md","security-and-lifecycle.md","workflows-and-surfaces.md"],
   "productContractsUnchanged":["README.md","admission-and-qualification.md","identity-and-evidence.md"]
  }
 },

 "executedChecks":{
  "suitesRerunInScratch":True,"allExitZero":True,
  "foundation":{"checks":397,"pins":1091},
  "security":{"cases":444,"sweeps":9},
  "native":{"cases":101,"matrixCells":60,"qualifiedCells":0},
  "workflows":{"checks":1253,"commands":45,"goldens":43},
  "integration":{"checks":319,"distinctIds":319},
  "reportsReproducedByteIdentically":"10 of 10",
  "reportComparison":rep,
  "countDeltaReconstructed":{
    "workflows":"1206 -> 1253 = 28 schema negatives (4 commands x 7 fields) + 1 coverage check + 15 checks from 3 new render cases + 3 retrofitted SARIF checks = 47",
    "integration":"311 -> 319 = 10 added ids - 2 replaced duplicate ids = 8"},
  "referenceNotQualification":True
 },

 "independentProbes":{
  "totalRecords":idx['totalRecords'],
  "supersededProbeDefects":idx['supersededProbeDefects'],
  "liveProbes":idx['liveProbes'],"livePass":idx['livePass'],"liveFail":idx['liveFail'],
  "liveFailures":idx['liveFailures'],
  "note":"Superseded records are defects in my own probe construction, corrected in later files and preserved; none is a product failure. Both live failures are raised as advisories, not required gaps.",
  "index":"probes/probe-index.json"
 },

 "priorIssueDispositions":{
  "MUST-A(v4)":{"disposition":"CORRECTED","verifiedBy":["A1","A2","A3","A3b","A4","A5","A5b","A6","A6b","A7","A7b","A8","A9","A10","A11","A12","A13","A13b"],
   "evidence":{"sarifCommands":["analyze","audit","default","repair-verify"],
    "commonFields":["run-id","verdict","required-coverage","deficiency","findings","termination-class","retention-disclosure"],
    "schemaOmissionNegatives":28,"fabricationNegatives":12,
    "rendererLine":"results: parity['findings']; runProperties: {verdict: parity['verdict'], deficiency: parity['deficiency']} - one filtered declared projection, strict indexing",
    "undeclaredEnvelopeDataLeak":False,
    "auditRunProperties":{"verdict":"pass","deficiency":None},
    "repairVerifyRunProperties":{"verdict":"pass","deficiency":None},
    "renderCasesCoverAllFour":True,
    "emptyFindingsDistinguishableFromAbsentField":True,
    "ephemeralRunIdNullWithoutMintingRun":True,
    "proseSchemaInventoryCheckerAgree":True}},
  "ADV-a(v4)":{"disposition":"CORRECTED","verifiedBy":["B1","B1b","B1c","B1d"],
   "evidence":"319 checks / 319 distinct ids; missing-retained-closure-is-typed-operational-loss-{blobs,objects}; checker asserts its own id uniqueness; lane name matches the map actually left empty"},
  "ADV-b(v4)":{"disposition":"CORRECTED","verifiedBy":["B2","B2b","B2c","B2d","B2e"],
   "evidence":"operational-scope-1024/1025 drive real security discovery -> admitted boundaries -> native scope over one coherent host-observed inventory; 1024 asserts exactly 1024 admitted roots; 1025 asserts exit 2 and subject workspaceRoots:1025>1024; standalone unit evidence retained"},
  "ADV-c(v4)":{"disposition":"CORRECTED","verifiedBy":["B3"],
   "evidence":"native section 10 row now reads native.explicit-root-without-marker (missing marker); PROJECT.EXPLICIT_PATH_INVALID (grammar or boundary crossing)"},
  "ADV-d(v4)":{"disposition":"CORRECTED","verifiedBy":["B4","B4b","D5"],
   "evidence":"workflow contract restates equal metric definition / supplied diff scope / comparison base, incompatible reported incompatible, redistribution distinguished; names architecture 13 section 6 as inherited owner; source-map FW-11 row unchanged; architecture 13 byte-unchanged"},
  "ADV-e(v4)":{"disposition":"CORRECTED","verifiedBy":["B5","B5b","B5c","B5d","B5e","B5f","C3","C3b","C3c","C3d","E7","E7b","E7c","E7d"],
   "evidence":{"negatives":25,"positives":8,"olderValidCasesStillWork":True,
     "refusalToken":"DISCOVERY_OBSERVATION_SHAPE","isPublicD9Code":False,
     "absentFromPublicRegistryInventoryAndNativeContract":True,
     "boolsRejectedForUidAndGid":True,"readsNoEnvPathHome":True,
     "securityModelLinesAdded":20,"securityModelLinesRemoved":0,"hunks":1,
     "executionOrAuthorizationFunctionTouched":False,
     "regressionsFound":"none"}}
 },

 "newMustIssues":[],
 "newShouldIssues":[],
 "newAdvisories":[
  {"id":"ADV-1(v5)","title":"D-372 cites section 9 for declared parity fields, which section 8 owns",
   "owningSelector":"docs/coop/design-corrections/D-372-corrections.proposed.md, 'Explicit product and output re-entry acts'",
   "detail":"Line 80 attributes 'declared parity fields ... and post-commit required-output failure law' to Workflow section 9. Section 8 ('Command inventory, outputs and parity') owns the declared parity fields and the delivery-failure prose; section 9 ('D9 goldens and typed detail') carries only the golden table row. Bytes unchanged from v4; the law is determinate and correctly owned, only the section number misdirects a reader of the document MUST-A named as an owning selector.",
   "blocking":False},
  {"id":"ADV-2(v5)","title":"NEXT-REVIEW.md ships inside the v5 subject still describing the v4 review as active",
   "owningSelector":"docs/coop/design-corrections/reviews/NEXT-REVIEW.md",
   "detail":"Cites manifest 2a2168c3... and counts workflows1206 / integration311 while the subject it ships in is v5 with 1253 / 319. Non-normative and not source-pinned, and validation-summary.v1.json is correct and current (PENDING-FROZEN-V5), so there is no normative contradiction; but it is the designated resume pointer.",
   "probe":"D.D7","blocking":False},
  {"id":"ADV-3(v5)","title":"check-integration.py is covered by no source-pin set",
   "owningSelector":"docs/coop/design-corrections/check-integration.py; the four source-pins files",
   "detail":"All its model inputs are pinned, but the cross-unit harness itself is not. Pre-existing: equally unpinned in v4. Flagged so the scoping choice is explicit.",
   "probe":"B2.B6c","blocking":False},
  {"id":"ADV-4(v5)","title":"Reference render cases cannot discriminate filtered from unfiltered SARIF sourcing",
   "owningSelector":"docs/coop/design-corrections/workflows/check_workflows.v1.py render section; workflow-cases.v1.json /renderCases",
   "detail":"The cases construct parity exactly from parityFields, so filtered and unfiltered sourcing yield identical values; the suite could not have caught the v4 defect and would not catch a regression to unfiltered sourcing. My probe A4 supplies the discriminating input (undeclared keys in envelope['parity']). Test strength only: the model is single-sourced and the schema enforces declaration at admission. Consider one case with an undeclared envelope key.",
   "probe":"A2.A14","blocking":False},
  {"id":"ADV-5(v5)","title":"Totality of the host projection over parityFields is not stated",
   "owningSelector":"docs/v2/contracts/product-v1/workflows-and-surfaces.md section 8 renderers paragraph",
   "detail":"A declared parity field absent from the host projection raises an untyped KeyError. This satisfies MUST-A (loud, nothing fabricated), but section 8 does not state that the projection must be total over parityFields, nor which internal fault class a violation takes. One sentence closes it.",
   "probe":"A2.A5","blocking":False}
 ],

 "arDispositions":{
  "AR-01":{"disposition":"ACCEPT","basis":"foundation unit byte-unchanged except pins (F3); 397 reproduced; identity model/schemas identical to v4 (C2f); ADV-e closed"},
  "AR-02":{"disposition":"ACCEPT","basis":"product-configuration model byte-unchanged (F1); reports reproduced; 0 qualified cells"},
  "AR-03":{"disposition":"ACCEPT","changedFromV4":"was ACCEPT with advisory","basis":"ADV-b closed by the composed 1024/1025 path (B2-B2e); ADV-e closed (B5-B5f); security delta purely additive (E7-E7d)"},
  "AR-04":{"disposition":"ACCEPT","basis":"9/9 sweeps reproduced byte-identically; security report identical to v4 rerun"},
  "AR-05":{"disposition":"ACCEPT","basis":"sweeps reproduced; revocation/root-chain bytes unchanged"},
  "AR-06":{"disposition":"ACCEPT","basis":"security model unchanged apart from the additive discovery gate (E7)"},
  "AR-07":{"disposition":"ACCEPT","basis":"native unit byte-unchanged except pins (F2); 101 cases reproduced"},
  "AR-08":{"disposition":"ACCEPT","basis":"workflow steps/flags/formats/requestClass unchanged (C7); repair/test surfaces untouched"},
  "AR-09":{"disposition":"ACCEPT","basis":"identity model, schemas and contract byte-identical to v4 (C2f); identity report reproduced"},
  "AR-10":{"disposition":"ACCEPT","basis":"baseline/pivot bytes unchanged; comparison cases reproduced"},
  "AR-11":{"disposition":"ACCEPT","changedFromV4":"was ACCEPT with advisory","basis":"ADV-d closed: FW-11 restated in the owning contract without forking architecture 13 section 6 (B4, B4b, D5)"},
  "AR-12":{"disposition":"ACCEPT","basis":"native 101 reproduced; section 10 row now unambiguous (B3)"},
  "AR-13":{"disposition":"ACCEPT","changedFromV4":"was CHANGES_REQUIRED","basis":"MUST-A closed: A1-A14, 28 schema negatives, 12 fabrication negatives, all four commands cased"},
  "AR-14":{"disposition":"ACCEPT","basis":"host foundation model byte-unchanged (F1); required-output failure law intact (C5-C5c)"},
  "AR-15":{"disposition":"ACCEPT","basis":"policy/review bytes unchanged; workflows report reproduced"},
  "AR-16":{"disposition":"ACCEPT","changedFromV4":"was CHANGES_REQUIRED","basis":"MUST-A closed; ADV-a closed (319 distinct ids); ADV-c closed; registry byte-identical, no new public code (C5d, F5)"}
 },

 "fwDispositions":{
  "FW-01":{"disposition":"ACCEPT","basis":"owning bytes unchanged from v4; suites reproduced"},
  "FW-02":{"disposition":"ACCEPT","basis":"owning bytes unchanged from v4; suites reproduced"},
  "FW-03":{"disposition":"ACCEPT","basis":"native unit byte-unchanged except pins (F2)"},
  "FW-04":{"disposition":"ACCEPT","basis":"import/evidence bytes unchanged; identity schemas identical to v4"},
  "FW-05":{"disposition":"ACCEPT","basis":"comparison/baseline bytes unchanged; workflows report reproduced"},
  "FW-06":{"disposition":"ACCEPT","basis":"identity/proof/evidence/seal bytes identical to v4 (C2f); all ten reports reproduce byte-identically"},
  "FW-07":{"disposition":"ACCEPT","basis":"no command, step, flag or format added or removed (C6c, C7); required-output failure law intact"},
  "FW-08":{"disposition":"ACCEPT","basis":"native Coverage bytes unchanged; empty findings distinguishable from an absent projection field (A10)"},
  "FW-09":{"disposition":"ACCEPT","basis":"review/candidate bytes unchanged"},
  "FW-10":{"disposition":"ACCEPT","basis":"repair bytes unchanged; repair-verify remains non-executing while gaining analysis fields (C6b)"},
  "FW-11":{"disposition":"ACCEPT","changedFromV4":"advisory closed","basis":"ADV-d closed; owning workflow contract restates the architecture 13 section 6 restriction, which is byte-unchanged (B4, B4b, D5, D1)"},
  "FW-12":{"disposition":"ACCEPT","basis":"brief/truncation bytes unchanged"},
  "FW-13":{"disposition":"ACCEPT","changedFromV4":"was implicated by MUST-A","basis":"inventory now declares a complete schema-enforced SARIF parity field set; inventory outside parityFields and the SARIF parityRule is exactly equal to v4 (C8); 45 commands, 43 goldens, registry byte-identical with internal aliases distinct"},
  "FW-14":{"disposition":"ACCEPT","basis":"synthetic design cases still not the required corpus; no gate flipped to qualified or demonstrated (D4c)"},
  "FW-15":{"disposition":"ACCEPT","basis":"policy DSL/test bytes unchanged; workflows report reproduced"}
 },

 "inheritedResidualDispositions":{
  "parentRowsDR001to011":{"count":11,"disposition":"all carry an individual written disposition; none contradicted by the frozen bytes","probe":"E1c"},
  "DR-011-R01":"ACCEPT (unchanged bytes; v4 evidence carries with digest proof)",
  "DR-011-R02":"ACCEPT (unchanged bytes)",
  "DR-011-R03":"ACCEPT (unchanged bytes)",
  "DR-011-R04":"ACCEPT (unchanged bytes)",
  "DR-011-R05":"ACCEPT (unchanged bytes)",
  "DR-011-R06":"ACCEPT (unchanged bytes; identity schemas identical to v4, C2f)",
  "DR-011-R07":"ACCEPT (unchanged bytes)",
  "DR-011-R08":"ACCEPT (was CHANGES_REQUIRED; required-output failure law registered AND the SARIF field set now determined for all four commands - E6)",
  "DR-011-R09":"ACCEPT (unchanged bytes)",
  "DR-011-R10":"REMAINS OPEN BY DESIGN - the blind consumer-B litmus is a later distinct act this review does not perform and does not prejudge (E1b)",
  "DR-011-R11":"ACCEPT (unchanged bytes)",
  "DR-011-R12":"ACCEPT as prospective (30 subresiduals individually written, all PENDING, no containment claim - E2)",
  "DR-011-R13":"ACCEPT (was CHANGES_REQUIRED; audit determines its SARIF content and keeps its comparison account - E6b)",
  "DR-011-R14":"ACCEPT (unchanged bytes)",
  "DR-011-R15":"ACCEPT (unchanged bytes)",
  "DR-011-R16":"ACCEPT (unchanged bytes)",
  "sixCompatibilityRows":{"rows":["DR-102","DR-104","DR-115","DR-117","DR-119","DR-123"],
    "disposition":"ACCEPT","basis":"every source pin resolves to its declared digest; each row states a retained meaning, selector and custody rule rather than a bare pin (E3-E3c)"},
  "DR-003timingDisposition":{"disposition":"AFFIRMED AS PROPOSED","basis":"unchanged bytes; still not a SATISFIED or DEMONSTRATED claim; DR-G09/G18/G19/G21/G22 and DR-012 remain mandatory"},
  "historicalPreservation":{"files":31,"unchanged":31,"changed":0,"inDelta":0,"probe":"D1/D1b/D1f"},
  "condition5":"NOT MET and must remain NOT MET; no subject byte authorizes implementation (E4)"
 },

 "scopedReviewOwnerDispositions":{
  "note":"NEW full-product-scope dispositions by this review owner. The historical 2026-08-13 acceptances are untouched, retain their original subjects and digests, and are not extended.",
  "DR-201":{"title":"semantic correctness","disposition":"ACCEPT",
   "probes":["C2a","C2b","C2c","C2c2","C2c3","C2c4","C2c5","C2d","C2e","C2f","C1","C1b","C1c"],
   "basis":"identity layer byte-identical to v4 so its independent evidence carries with proof; re-derived the part the delta could disturb: closed identity domain registry refusing an output-shaped domain; no domain schema admits an output-projection or operational field; the run domain carries no exit code, renderer or delivery field; the sealed verdict is a closed pass/fail/indeterminate semantic enum, not the rendered projection; the derivation reads no output field name; adding output fields to audit/repair-verify changed no semantic identity",
   "owningSelectors":["docs/coop/design-corrections/foundation/identity-model.py","docs/coop/design-corrections/foundation/identity-schemas.v2.json","docs/v2/contracts/product-v1/identity-and-evidence.md"]},
  "DR-202":{"title":"delivery/operations","disposition":"ACCEPT","changedFromV4":"was CHANGES_REQUIRED",
   "probes":["A1","A2","A3","A3b","A4","A5","A5b","A6","A6b","A7","A7b","A8","A9","A10","A11","A12","A13","A13b","C5","C5b","C5c","C5d"],
   "basis":"the sole condition v4 set (MUST-A) is met: all four advertised SARIF commands declare the same seven common analysis fields; the schema refuses any omission (28 negatives); results and run properties come from one filtered declared projection with no undeclared read and no null fallback; a missing declared field cannot become fabricated valid output (12 negatives); audit preserves the current analysis findings and deficiency; repair-verify preserves the fresh Run verdict and findings and adds its verification counts; all four commands cased. Post-commit required-renderer failure law intact and re-verified.",
   "attachedAdvisories":["ADV-4(v5)","ADV-5(v5)"],
   "owningSelectors":["docs/v2/contracts/product-v1/workflows-and-surfaces.md sections 8 and 9","docs/coop/design-corrections/workflows/command-inventory.v1.json","docs/coop/design-corrections/workflows/schemas/command-inventory.schema.json","docs/coop/design-corrections/workflows/workflows_model.v1.py render","docs/coop/design-corrections/workflows/workflow-cases.v1.json"]},
  "DR-203":{"title":"prototype lessons","disposition":"ACCEPT",
   "probes":["D1","D1b","F4","D2"],
   "basis":"owning bytes unchanged from v4 (security S16, prototype-evidence-reference.md and architecture 05 all byte-identical and outside the delta), so v4's item-for-item check of five preserve obligations, five distinctions and six prohibitions, the pinned prototype commit and the routing to G06/G07/G11/G12/G18/G19/G21 as required future measurement carries unchanged; nothing in v5 executed the prototype and nothing claims to have",
   "owningSelectors":["docs/v2/contracts/product-v1/security-and-lifecycle.md S16","docs/v2/architecture/prototype-evidence-reference.md","docs/v2/architecture/05-v1-to-v2-relationship.md"]},
  "DR-204":{"title":"inherited invariants","disposition":"ACCEPT",
   "probes":["E1","E1b","E1c","E2","E3","E3b","E3c","D1","D1b","D1f","B6","B6d","E4","E4b"],
   "basis":"every inherited row carries an individual written disposition rather than an aggregate grade, verified independently: 16 R-rows, 11 parent rows, 30 PENDING subresiduals with no containment claim, 6 resolving compatibility pins with retained meaning and custody, 31 historical files byte-unchanged, all four pin sets resolving with no cross-suite disagreement. R08 and R13 move to ACCEPT on the MUST-A correction; R10 stays open by design. Nothing in the subject accepts its own bytes; this review supplies the independent oracle for the design layer only.",
   "owningSelectors":["docs/coop/design-corrections/inherited-residuals.proposed.md","docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json","docs/coop/design-corrections/inherited-row-sources.proposed.json","docs/coop/design-corrections/historical-preservation-report.v5.json"]},
  "DR-205":{"title":"core/components","disposition":"ACCEPT",
   "probes":["D2","D3","F1","F2","F3","F4","C6","C6b","C6c","C7"],
   "basis":"owning bytes unchanged from v4 (admission-and-qualification.md section 5's seven-item P-1/P-2/G3 account, identity-and-evidence.md, and the native/security sections outside the two-line and one-hunk deltas are byte-identical); the delta added no command, step, flag, format or authority, and audit/repair-verify remain non-executing despite gaining analysis fields, so no component gained host-reserved authority",
   "owningSelectors":["docs/v2/contracts/product-v1/admission-and-qualification.md section 5","docs/v2/contracts/product-v1/security-and-lifecycle.md S9.2 and S10","docs/v2/contracts/product-v1/native-evidence.md section 5.5","docs/v2/contracts/product-v1/workflows-and-surfaces.md sections 7, 8, 12"]}
 },

 "limitations":[
  "Not blind consumer B; that required distinct act has never run.",
  "Not application acceptance; the central/navigation application is deliberately still pending and was not accepted, nor treated as a false acceptance.",
  "Not product qualification; no OS, compiler, crypto, SQLite or end-to-end measurement was performed and none is implied.",
  "All synthetic signatures, host/OS observations, evaluator callbacks and locks are stated TCB assumptions.",
  "Reference suites are reference evidence only.",
  "Historical 2026-08-13 grades are not extended.",
  "Condition 5 remains NOT MET; no implementation is authorized."
 ],

 "remainingAcceptance":[
  "fresh blind consumer B (required distinct act, never run)",
  "complete final application package with its own actual independent application review",
  "apply accepted documentation/readiness records after the above; condition 5 remains NOT MET until its own evidence exists"
 ],

 "predecessorSession":{
  "interruptedRun":"docs/coop/design-corrections/reviews/post-reset-review.v5-interrupted",
  "producedVerdict":False,
  "agreementInferred":False,
  "note":"The interrupted run's is_error is a session limit, not a design finding."
 },

 "paths":{
  "reviewMd":"/tmp/opensip-design-corrections/post-reset-review.v5/review.md",
  "reviewJson":"/tmp/opensip-design-corrections/post-reset-review.v5/review.json",
  "probes":"/tmp/opensip-design-corrections/post-reset-review.v5/probes/",
  "probeIndex":"/tmp/opensip-design-corrections/post-reset-review.v5/probes/probe-index.json",
  "reports":"/tmp/opensip-design-corrections/post-reset-review.v5/reports/",
  "suiteRunner":"/tmp/opensip-design-corrections/post-reset-review.v5/run-suites.v5.sh",
  "custodyBefore":"/tmp/opensip-design-corrections/post-reset-review.v5/scratch/custody-before.v2.txt",
  "custodyAfter":"/tmp/opensip-design-corrections/post-reset-review.v5/scratch/custody-after.v2.txt"
 }
}
Path(OUT+'review.json').write_text(json.dumps(r,indent=1)+'\n')
print('written',OUT+'review.json',len(json.dumps(r)),'bytes of json')
