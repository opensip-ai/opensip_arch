import json,hashlib
from pathlib import Path
W=Path('/tmp/opensip-design-corrections/post-reset-review.v19')
def sh(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
REF="docs/coop/design-corrections/reviews/codex-post-reset.v1/"
def prior(sel): return {"path":REF+"successor-source-assessment.v19.json","sha256":"a055cef9d2b9b5ed08ba10c8bffdeed6693f80fa13c5ee76ef305a0572c05cbc","selector":sel}
def ctl(name): return {"path":"post-reset-review.v19/results/"+name,"sha256":sh(W/'results'/name)}

AR_BASIS=("Owning AR document docs/coop/architecture-depth-review/REVIEW.md is byte-identical v18->v19 (both manifests). "
 "correction-crosswalk.proposed.json did change; I diffed it leaf-by-leaf myself: 64 changed leaves are exactly the 16 rows' "
 "latestCompletedReview path/sha256/subjectManifestSha256/standing pointers, 96 added leaves are appended historicalReviews "
 "entries, 0 removals, and ZERO structural leaves (obligation, selector, owner, unit, contract, status, id, ownerRows) changed.")
ar={f"AR-{i:02d}":{"id":f"AR-{i:02d}","disposition":"CARRIED-UNCHANGED","basis":AR_BASIS,
    "scope":"Preservation and review-routing only; the obligation did not move. Not a new grade.",
    "authority":"The row's own owner and the separately reviewed application. Not this review's to grant.",
    "appliedByThisReview":False,"finalApplicationOutcomeGranted":False,
    "evidence":{"path":"post-reset-review.v19/results/manifest-delta.json","sha256":sh(W/'results/manifest-delta.json')}} for i in range(1,17)}
ar["AR-15"]["scope"]=("Preservation and review-routing only. AR-15 owns DR-201..205 as ownerRows; its ownerRows leaf is unchanged. "
    "Not a new grade and not a final application outcome for any owned row.")

fw={f"FW-{i:02d}":{"id":f"FW-{i:02d}","disposition":"CARRIED-UNCHANGED",
    "basis":"current-source-map.proposed.md is byte-identical v18->v19 and absent from the 23-path changed set I computed from the two manifests.",
    "scope":"Preservation only.","authority":"Not this review's to grant.",
    "appliedByThisReview":False,"finalApplicationOutcomeGranted":False} for i in range(1,16)}
fw["FW-03"]["basis"]+=(" FW-03 (native semantics) and FW-06 (determinism) are the frameworks the v19 changes touch; the changed "
    "native/foundation bytes are reviewed substantively under newMustIssues/priorFindingDispositions, not here. The FRAMEWORK row itself is unchanged.")
fw["FW-06"]["basis"]=fw["FW-03"]["basis"]
fw["FW-10"]["basis"]+=(" FW-10 (repair evidence) is the framework the S6 projection paragraph sits under; I verified the repair "
    "emission body is byte-identical to pre-v19, so the framework row is untouched by a documentation-only correction.")

INH_BASIS=("inherited-residuals.proposed.md and inherited-row-sources.proposed.json are both byte-identical v18->v19; "
 "neither appears in the changed set I computed.")
inh_ids=[f"DR-{i:03d}" for i in range(1,12)]+[f"DR-011-R{i:02d}" for i in range(1,17)]
inh={k:{"id":k,"disposition":"CARRIED-UNCHANGED","basis":INH_BASIS,
    "scope":"Preservation only. DR-011-R10 still requires a fresh blind implementer litmus that this review does not supply. "
            "DR-012 is header prose, explicitly excluded, not a row.",
    "authority":"Not this review's to grant.","appliedByThisReview":False,"finalApplicationOutcomeGranted":False} for k in inh_ids}

scoped={f"DR-{i}":{"id":f"DR-{i}","disposition":"ROUTING-ASSESSED-ONLY-NOT-APPLIED",
    "basis":("Owning register docs/v2/architecture/08-decision-and-readiness-register.md is byte-identical v18->v19 (verified against "
             "both manifests). Its Condition 5 sentence is unchanged. The row's own historical scoped disposition stands as history. "
             "I assessed review ROUTING only; I performed no gate and granted no outcome."),
    "scope":"Routing assessment of a scoped review owner. NOT a grade and NOT a final application outcome.",
    "authority":"The row's own owner and the separately reviewed application.",
    "appliedByThisReview":False,"finalApplicationOutcomeGranted":False} for i in range(201,206)}

review={
 "review":"post-reset-review.v19",
 "subjectManifestSha256":"312db9d904d0ec1f9c91d84137feb3277490b79b07bf3a6d5efc0380caa0f24b",
 "reviewer":"Actual Claude, fresh independent review. Not a source coauthor (4b48ccdd / f8404b42), not prior independent (87a6bcea), not blind (e6448709).",
 "verdict":"ACCEPT",
 "verdictScope":("Independent acceptance of the frozen v19 SOURCE bytes only. NOT a blind review, NOT an application, NOT a readiness "
   "reconciliation, NOT product qualification and NOT implementation authorization. A NEW blind consumer on these bytes and a complete, "
   "separately independently reviewed application/readiness reconciliation remain required and are NOT claimed here."),
 "custody":{
  "manifestRehashed":"312db9d904d0ec1f9c91d84137feb3277490b79b07bf3a6d5efc0380caa0f24b (matches declared)",
  "inventoryBefore":{"files":8653,"bytes":628224694,"missing":0,"hashMismatch":0,"lengthMismatch":0,"extra":0},
  "inventoryAfter":{"files":8653,"bytes":628224694,"missing":0,"hashMismatch":0,"lengthMismatch":0,"extra":0},
  "declaredReferencesVerified":{"checked":60,"mismatched":0,
    "covers":"final-source-account.v19 files + the four coauthor handoffs, four root coauthor assessments, prior independent review, "
             "prior root assessment, predecessor manifest, latest blind clarification, withdrawal evidence and root assessment, and "
             "every sourceDelta after-hash plus each sourceProposal byte-equality"},
  "sourcePinLedgers":{"foundation":{"pins":1100,"mismatched":0},"security":{"pins":74,"mismatched":0},
    "native":{"pins":72,"mismatched":0,"includesNewRuntimeTable":True},"workflows":{"pins":66,"mismatched":0},"totalRows":1312},
  "writeIsolation":"All probes, copies and reports under /tmp/opensip-design-corrections/post-reset-review.v19 only. No write to the frozen tree or the live checkout.",
  "evidence":ctl("ledger-verify.json")},
 "referenceChecks":{
  "method":"Six canonical commands from reviews/codex-post-reset.v1/final-reference.v19/reference-checks.json, reproduced in a DISPOSABLE FULL EXACT COPY of the snapshot, WITHOUT repinning.",
  "results":[{"name":"foundation","exit":0,"declaredExit":0,"sourceHashMatches":True,"reportByteStable":True,"seconds":112.59},
   {"name":"security","exit":0,"declaredExit":0,"sourceHashMatches":True,"reportByteStable":True,"seconds":0.70},
   {"name":"native","exit":0,"declaredExit":0,"sourceHashMatches":True,"reportByteStable":True,"seconds":2.73},
   {"name":"workflows","exit":0,"declaredExit":0,"sourceHashMatches":True,"reportByteStable":True,"seconds":9.44},
   {"name":"workflow-surface","exit":0,"declaredExit":0,"sourceHashMatches":True,"reportByteStable":True,"seconds":9.37},
   {"name":"integration","exit":0,"declaredExit":0,"sourceHashMatches":True,"reportByteStable":True,"seconds":15.40}],
  "observedTotals":"foundation passed/failed per its own report; native 355/355 cases, 66 matrix cells, 0 qualified; workflow-surface 1795/1795; integration 412 passed, 0 failed; identity 1431/0.",
  "actualSourceCopyDelta":{"changed":0,"added":0,"removed":0,
    "meaning":"The six commands REGENERATE every report byte-identically. The retained report bytes are exactly what the retained sources produce; nothing in the copy diverged from the frozen parent, before or after my probes."},
  "evidence":[ctl("canonical-six.json"),ctl("copy-delta.json")]},
 "executableDelta":{
  "declaredSourceDelta":11,"observedChangedPaths":23,"observedAddedPaths":789,"observedRemovedPaths":0,
  "reconciliation":("The 11 declared sourceDelta paths are a subset of changed+added. The other 12 changed paths are: 6 GENERATED reports "
    "(foundation identity-report/validation-report, integration-report.v1, workflows-report.v1, workflows-validation-report, "
    "validation-summary.v1) which my own runs reproduce byte-identically; the 4 pin ledgers, all verified; correction-crosswalk.proposed.json "
    "(routing pointers only, diffed leaf-by-leaf); README.md (a prepended v19 header, prior text preserved as history); and "
    "reviews/NEXT-REVIEW.md. 786 of the 789 additions are under reviews/ (retained coauthor/probe evidence); the 3 outside are "
    "historical-preservation-report.v19.json, post-reset-dispositions.v19.proposed.json and the NEW normative table."),
  "productContractsChanged":["docs/v2/contracts/product-v1/native-evidence.md","docs/v2/contracts/product-v1/workflows-and-surfaces.md"],
  "productContractsUnchanged":["README.md","admission-and-qualification.md","identity-and-evidence.md","security-and-lifecycle.md"],
  "evidence":ctl("manifest-delta.json")},
 "myControls":{
  "total":192,"failed":0,"authoredFreshForThisReview":True,
  "sets":[
   {"id":"A","area":"CB7-MUST-1 TS closed-suffix clone scope","controls":47,"failed":0,"evidence":ctl("ctrl-a.json")},
   {"id":"B","area":"CB7-SHOULD-2 prospective Plan cardinality","controls":56,"failed":0,"evidence":ctl("ctrl-b.json")},
   {"id":"C","area":"ACTUAL INVOCATION: refused step mints no Plan/Run; earlier outcomes preserved","controls":14,"failed":0,"evidence":ctl("ctrl-c.json")},
   {"id":"D","area":"protocol3 published table; independent interpreter equivalence","controls":21,"failed":0,
    "behaviouralCases":423,"permutationSweeps":25,"evidence":ctl("ctrl-d.json")},
   {"id":"E","area":"workflow S6 repair projection, subject projection, withdrawn premise","controls":22,"failed":0,"evidence":ctl("ctrl-e.json")},
   {"id":"F","area":"independent re-measurement of CB7-ADV-1..5","controls":22,"failed":0,"evidence":ctl("ctrl-f.json")},
   {"id":"G","area":"_SOURCE_FRAMES derivation counterexample (advisory basis)","controls":5,"failed":0,"evidence":ctl("ctrl-g.json")},
   {"id":"H","area":"producer-boundary dialect call sites","controls":5,"failed":0,"evidence":ctl("ctrl-h.json")}],
  "reusedRetainedEvidence":("For UNCHANGED areas (zero-config capabilities/discovery/config, native ownership/clone progression, "
    "static/runtime/test/history/import evidence authority, deterministic typed identity/closure, changed-code/baseline semantics, "
    "invocation/repair/replay/error surfaces, authorization and current availability) I reused the retained suites AFTER verifying exact "
    "source identity by pin ledger and re-executing all six canonical commands myself. I did not rerun old broad probe suites absent a concrete concern.")},
 "newMustIssues":[],
 "newShouldIssues":[],
 "newAdvisories":[
  {"id":"CX-CL19-ADV-1","severity":"ADVISORY","title":"The published transition table is kit-SHAPED but no v19 record binds it into the next blind kit",
   "observation":("protocol3-transitions.v1.json is a self-contained .json in native/, the same class the retained blind kit already carries "
     "(consumer-b.v7/subject/.../native/ holds exactly three .json files and no .py). My independent interpreter, written from the document's own "
     "laws, reproduces the model on 423 cases, so the artifact IS sufficient. But kits are assembled per blind pass and no v19 artifact declares "
     "the composition rule, so nothing in these bytes GUARANTEES blind 8 receives it."),
   "owningSelector":"docs/coop/design-corrections/native/protocol3-transitions.v1.json; consumer kit assembly for the NEW blind",
   "whyNotAFinding":"No byte in v19 is wrong. Kit assembly is a required NEXT act, not a defect in the reviewed bytes.",
   "action":"The NEW blind's kit must include this artifact, or CB7-ADV-4 recurs verbatim.",
   "evidence":ctl("ctrl-d.json")},
  {"id":"CX-CL19-ADV-2","severity":"ADVISORY","title":"The _SOURCE_FRAMES drift control is tautological",
   "observation":("The model derives _SOURCE_FRAMES as the union of stateUpdates[].onFrames, and the control at check-identity.py:3546 asserts "
     "that same expression equals the model value, so it cannot discriminate. TODAY the derived set equals the pre-v19 seven-frame literal exactly "
     "(I verified this by exec'ing the pre-v19 inline segment). The binding 'plural onFrames means sourceBytesSent' is a document CONVENTION - only "
     "one of four stateUpdates entries uses the plural form - not an asserted law. A future entry using onFrames for any other purpose would silently "
     "widen the observable that proves no source byte preceded negotiation, while the published control still passed."),
   "owningSelector":"native_evidence_model.v2.py _SOURCE_FRAMES; protocol3-transitions.v1.json#/stateUpdates; check-identity.py:3546",
   "whyNotAFinding":"No counterexample exists in these bytes; today's derived value is provably correct. The weakness is in a control's discriminating power, not in behaviour or a published law.",
   "action":"Bind _SOURCE_FRAMES to an independent authority (the entry's own `sets` text, or a named key) rather than to its own derivation.",
   "evidence":ctl("ctrl-g.json")}],
 "priorFindingDispositions":{},
 "arDispositions":ar,"fwDispositions":fw,"inheritedResidualDispositions":inh,"scopedReviewOwnerDispositions":scoped,
 "ownerRoutingScopeStatement":("For every AR, FW, inherited-residual and scoped-owner row I assessed ROUTING and byte-preservation only. "
   "Carry-forward and routing are NOT a fresh substantive readiness grade. appliedByThisReview and finalApplicationOutcomeGranted are false on "
   "every row, including all five DR-201..205."),
 "failedAttempts":{"count":9,"standing":"Defects in MY OWN controls, corrected and retained. None is a finding about the subject.",
   "evidence":{"path":"post-reset-review.v19/results/failed-attempts.json","sha256":sh(W/'results/failed-attempts.json')},
   "mostConsequential":"FA-9: my first reading of the producer-boundary call sites would have raised an unfounded advisory. check-identity.py:2677 DOES supply the dialect; I withdrew the observation rather than publish it."},
 "implementationAuthorized":False,"readinessChanged":False,"productQualification":False,
 "blindAgreementClaimed":False,"applicationAgreementClaimed":False,
 "requiredNextActs":[
  "Root/source acceptance of THIS independent result; source coauthors are not independent reviewers.",
  "A NEW blind consumer (blind 8) on these accepted normative bytes, with the published transition table in its kit.",
  "A complete, separately independently reviewed application and readiness reconciliation.",
  "A final AFTER-ALL-RECORDING live and copied pin seal."]}
json.dump(review,open(W/'review.json','w'),indent=1)
print('base written, keys',len(review))
