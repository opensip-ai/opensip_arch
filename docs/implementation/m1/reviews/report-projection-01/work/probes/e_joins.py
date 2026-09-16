import sys; sys.path.insert(0,'.')
from common import *
R={}
B=fixture["bases"]
# P0 baselines still accepted in my copy
for k in B: R["base:"+k]=admit(copy.deepcopy(B[k]))
# P1 fit kind=run without candidates/evidence-levels parity (RP-OBL-1) is admitted
R["P1-fit-run-without-candidate-parity"]=admit(copy.deepcopy(B["fit-budget-omission"]))
# P2 candidates: evidenceLevels miscount + advisory false + latest view (workflows candidates joins)
d=copy.deepcopy(B["candidates-latest-view"]); d["envelope"]["queryRecord"]["evidenceLevels"]["proof-backed"]=7; d["envelope"]["queryRecord"]["suppressedCount"]=3
R["P2-candidates-evidenceLevels-miscount"]=admit(d)
# P3 inspect: context Run differs from bundle Run (workflows: concrete Run equals the bundle Run)
d=copy.deepcopy(B["inspect-run-graph"]); d["envelope"]["queryRecord"]["context"]["resolvedView"]={"runId":"run3:"+"e"*64}
R["P3-inspect-context-run-not-bundle-run"]=admit(d)
d=copy.deepcopy(B["inspect-run-graph"]); d["envelope"]["queryRecord"]["context"]["projectId"]="prj1-"+"0"*64
R["P3b-inspect-context-other-project"]=admit(d)
# P4 audit: comparison unavailable, history present with an arbitrary baselineId (no in-document join)
d=copy.deepcopy(B["audit-full"]); d["panels"]["comparison"]={"state":"unavailable","reason":"evidence-purged"}
d["panels"]["history"]["data"]["selection"]["baselineId"]="baseline2:"+"1"*64
R["P4-history-unjoined-baseline-when-comparison-unavailable"]=admit(d)
# P5 audit run without comparisonResultId: comparison not-selected, history still present
d=copy.deepcopy(B["audit-full"]); del d["envelope"]["run"]["comparisonResultId"]; d["panels"]["comparison"]={"state":"omitted","reason":"not-selected"}
R["P5-audit-comparison-not-selected-history-present"]=admit(d)
# P6 depth: a rule its own owner codec refuses (PolicyDocumentV2 at depth 32) accepted in the report at 38
found=None
for n in range(26,40):
    d=chk.apply_ops(B["audit-full"],[{"op":"x-deep-rule-predicate","notChain":n}],fixture,schema)
    rule=d["panels"]["catalog"]["data"]["rules"]["data"]["rules"][0]
    pol={"schemaFamily":"opensip.product.policy","schemaMajor":2,"gateSeverityAtLeast":"warning","rules":[rule]}
    try:
        ref.canonical(pol); owner="owner-accepts"
    except ref.AdmissionError as e: owner="owner-refuses:"+str(e)
    rep=admit(d)
    R["P6-notChain-%d"%n]=owner+" | report:"+rep
    if owner.startswith("owner-refuses") and rep=="accept" and found is None: found=n
R["P6-first-owner-refused-report-accepted-notChain"]=found
# P7 history finding rows cannot be joined to the history Run (no runId on FindingSurface): copy current findings into history row
d=copy.deepcopy(B["audit-full"]); row=d["panels"]["history"]["data"]["runs"][0]
if row["state"]=="present":
    row["findings"]=copy.deepcopy(d["envelope"]["findings"]); row["findingsProjection"]={"total":len(row["findings"]),"omitted":0,"omissionCause":"none"}
R["P7-history-row-carries-current-run-findings"]=admit(d)
# P8 graph ordinal duplicate (schema x-opensip-order ordinal)
d=copy.deepcopy(B["audit-full"]); d["panels"]["graph"]["data"]["slots"][1]["ordinal"]=0
R["P8-graph-duplicate-ordinal"]=admit(d)
# P9 evidence item-limit with fewer than 3956 embedded because bytes forced it: refused, so byte pressure cannot prefix-truncate
d=copy.deepcopy(B["audit-full"]); pr=d["panels"]["evidence"]["data"]["entriesProjection"]; n=len(d["panels"]["evidence"]["data"]["entries"])
d["panels"]["evidence"]["data"]["entriesProjection"]={"total":n+10,"omitted":10,"omissionCause":"item-limit"}
R["P9-evidence-byte-driven-prefix"]=admit(d)
# P10 capabilities registry need not be the Run's release registry: empty registry with correct self-digest
d=copy.deepcopy(B["audit-full"]); cap=d["panels"]["catalog"]["data"]["capabilities"]
if cap["state"]=="present":
    cap["data"]["declarations"]=[]; cap["data"]["source"]["registrySha256"]=hashlib.sha256(chk.canonical([])).hexdigest()
R["P10-capability-registry-substituted-empty"]=admit(d)
# P11 fit: add a findings view / candidate-list view -> schema refuses (no successor path inside :1)
d=copy.deepcopy(B["fit-budget-omission"]); d["supportedReportViews"]=["overview","findings","candidate-list","evidence","catalog","graph","symbol-detail"]
R["P11-fit-with-findings-and-candidate-views"]=admit(d)
print(json.dumps(R, indent=1)); json.dump(R, open("e_joins.json","w"), indent=1)
