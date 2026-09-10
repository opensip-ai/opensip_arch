import json,hashlib
from pathlib import Path
W=Path('/tmp/opensip-design-corrections/post-reset-review.v19')
r=json.load(open(W/'review.json'))
r["registers"]={
 "arRows":16,"fwRows":15,"inheritedResiduals":27,
 "inheritedResidualNote":"DR-001..011 plus the DR-011 subledger R01..R16. DR-012 is header prose, explicitly excluded, not a table row.",
 "evaluationSubresiduals":30,"scopedReviewOwners":5,"qualificationGates":32,"gateIds":"DR-G01..DR-G32",
 "gatesDemonstrated":0,"gatesQualified":0,"gatesImplementationHarnessAuthored":0,
 "allGatesRemainUnperformed":True,"gatesPerformedByThisReview":0,
 "verification":("I read qualification-gates.proposed.json directly in the v19 snapshot: 32 rows, and every row carries demonstrated=false, "
  "qualified=false, implementationHarnessAuthored=false and standing DESIGN-CONTRACT-PENDING-REVIEW. Zero rows carry a non-false value. "
  "The file is byte-identical v18->v19."),
 "owningDocumentByteStatusV18ToV19":{
  "architecture-depth-review/REVIEW.md":"byte-identical",
  "correction-crosswalk.proposed.json":"CHANGED - routing pointers only (64 changed leaves, 96 appended historicalReviews, 0 removals, 0 structural)",
  "current-source-map.proposed.md":"byte-identical",
  "inherited-residuals.proposed.md":"byte-identical",
  "inherited-row-sources.proposed.json":"byte-identical",
  "evaluation-residual-dispositions.proposed.json":"byte-identical",
  "docs/v2/architecture/08-decision-and-readiness-register.md":"byte-identical",
  "qualification-gates.proposed.json":"byte-identical",
  "D-372-corrections.proposed.md":"byte-identical",
  "design-corrections/README.md":"CHANGED - a prepended v19 header; all prior text preserved as history"},
 "evaluationResidualDispositions":{"disposition":"CARRIED-UNCHANGED","count":30,
  "basis":"evaluation-residual-dispositions.proposed.json is byte-identical v18->v19 and absent from the changed set I computed.",
  "scope":"Preservation only.","appliedByThisReview":False,"finalApplicationOutcomeGranted":False},
 "d372":{"applied":False,"condition5":"NOT MET",
  "basis":("docs/coop/design-corrections/README.md still states 'D-372 has not been applied and the central readiness register is unchanged', "
   "and the register itself is byte-identical v18->v19 with its 'Condition 5 remains separately required' sentence intact. "
   "D-372-corrections.proposed.md is byte-identical. Nothing in v19 applies D-372 and nothing in this review does.")},
 "selectedMachineIdsAndLanguagePaths":("The four selected macOS/Linux machine platform ids and the TS/JS/Rust/bounded-grammar paths are "
  "retained unchanged; I re-measured the platform registry directly (8 inherited members, 4 selected). Carried, not regraded by me.")}
r["lawPreservation"]={
 "preservedCompleteDesignAreasChecked":[
  "zero-config capabilities/discovery/config","native ownership and clone progression",
  "static/runtime/test/history/import evidence authority","deterministic typed identity and closure",
  "changed-code and baseline semantics","invocation, repair, replay and error surfaces",
  "authorization and current availability"],
 "method":("For each area I first verified exact source identity through the four pin ledgers (1312 rows, zero mismatches), then re-executed "
  "all six canonical commands MYSELF in a disposable copy. Where v19 changed bytes I inspected the changed code and its surrounding control flow "
  "directly and authored my own controls; where it did not, I reused the retained suites rather than rerunning old broad probe suites without a "
  "concrete concern."),
 "result":("All six suites exit 0 and regenerate every report byte-identically, so the retained evidence for the unchanged areas is exactly what "
  "the retained sources produce. The two changed product contracts are native-evidence.md and workflows-and-surfaces.md; the other four contracts "
  "and the index are byte-identical.")}
r["evidenceKindDistinctions"]={
 "whatIExecuted":("The reference models and their checkers, in a disposable copy, under /tmp/opensip-architecture-review-env/bin/python -I -B."),
 "whatIDidNotExecute":("No compiler, parser, provider, cargo, OS, repository or product host. No real toolchain or grammar was measured and no "
  "platform was qualified."),
 "notReportedAsExecutedEnforcement":("My protocol3, capability, cardinality and repair results are DESIGN/REFERENCE evidence over literal and "
  "schema artifacts and reference admission logic. I do NOT report them as executed security, host or compiler enforcement, and I do NOT report "
  "any of them as a fully admitted product Run. Every TCB and provider observation in these suites remains an explicit synthetic trusted input, "
  "as the owning reports themselves declare."),
 "countsMeaning":"All control, case, call and row counts in this review are calls or cases executed, NEVER qualification."}
r["evidenceHonesty"]=("My verdict rests on controls I wrote and ran against these exact bytes. Where I reused retained evidence I say so and I "
 "verified exact source identity first. I treated every coauthor, root and blind assertion as a claim to assess, not an oracle: I re-measured all "
 "five advisories independently and found the blind's own ADV-1 count basis needed the correction its clarification had already made, and I "
 "withdrew one observation of my own when a call site I had missed disproved it.")
r["standing"]=("Completed fresh independent review of frozen v19 source bytes by actual Claude. This is the source-acceptance step only. It "
 "confers no readiness, no product qualification and no implementation authorization, and it does not stand in for the NEW blind or the complete "
 "separately independently reviewed application, whose agreement is NOT claimed here.")
json.dump(r,open(W/'review.json','w'),indent=1)
print('keys',len(r),'bytes',len(json.dumps(r,indent=1)))
