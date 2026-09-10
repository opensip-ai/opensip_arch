import importlib.util,json,copy
from pathlib import Path
root=Path("/tmp/opensip-design-corrections/candidate-subject.v1/docs/coop/design-corrections/workflows")
s=importlib.util.spec_from_file_location("w",root/"workflows_model.v1.py");M=importlib.util.module_from_spec(s);s.loader.exec_module(M)
j=json.loads((root/"workflow-cases.v1.json").read_text());C=j["constants"]
def sub(v):
 if isinstance(v,str) and v.startswith("$"):return C.get(v[1:],v)
 if isinstance(v,dict):return {sub(k):sub(x) for k,x in v.items()}
 if isinstance(v,list):return [sub(x) for x in v]
 return v
j=sub(j);bs=j["baselineSpec"];pol=j["policyDocs"]
evidence=copy.deepcopy(bs["evidenceAvailability"]);evidence["imports"]=[]
ctx={"detectorClosureIds":[x["closureId"] for x in bs["detectorClosure"]],"evidenceAvailability":evidence}
b=M.adopt_baseline({"authority":"authoritative","availability":"retained","snapshotId":C["SNAP0"],"runId":C["RUN0"]},C["PLAN0"],C["PRJ"],pol["basePolicy"],pol["scopeAll"],pol["waiversNone"],j["ruleCoverage"]["full"],[],bs["detectorClosure"],bs["pivotClosure"],ctx,"1.0.0")
bd=copy.deepcopy(b["descriptor"]);bd["_baselineId"]=b["baselineId"]
current={"runId":C["RUN1"],"snapshotId":C["SNAP1"],"projectId":C["PRJ"],"context":copy.deepcopy(bd["context"]),"ruleCoverage":{r["ruleId"]:r for r in j["ruleCoverage"]["full"]},"presence":{},"entryRules":{},"boundPivots":[]}
current["context"]["policyDigest"]=M.doc_digest(pol["policyDisabledUnused"])
result=M.compare(bd,current,j["hosts"]["sameDetector"],"code-regression",{"ts-detector":{"closureId":C["DET_A0"],"semanticsMajor":2}})
print(json.dumps({"observation":"Empty baseline and current finding sets with an unbound required policy pivot must not pass", "result":result["descriptor"]},indent=2))
