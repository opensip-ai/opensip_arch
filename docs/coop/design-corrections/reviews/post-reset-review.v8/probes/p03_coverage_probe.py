#!/usr/bin/env python3
"""P03: what does a CoverageResultV3 payload actually contain, and does the
native producer admission actually re-run at Run closure over RETAINED bytes?"""
import contextlib, copy, hashlib, importlib.util, io, json, sys
from pathlib import Path
SUBJ=Path("/tmp/opensip-design-corrections/candidate-subject.v8")
F=SUBJ/"docs/coop/design-corrections/foundation"
def load(name,path,isolate=False):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s)
    if not isolate:
        s.loader.exec_module(m);return m
    argv=sys.argv;sys.argv=[str(path)];buf=io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            try:s.loader.exec_module(m)
            except SystemExit:pass
    finally:sys.argv=argv
    return m
M=load("idmodel",F/"identity-model.py");C=M.C
CHK=load("idcheck",F/"check-identity.py",isolate=True)
N=load("nat",F.parent/"native/native_evidence_model.v2.py")
out={}
run,objects,blobs=CHK.build(resolved=True,has_match=True)
cid=next(k for k,(d,v) in objects.items() if d=='coverage')
cov=objects[cid][1]
payload=C.parse(blobs[cov['payloadDigest']])
out["coveragePayload"]=payload
out["coverageRecordFields"]=sorted(cov)
sch=json.load(open(F.parent/"native/native-evidence.schemas.v2.json"))
cv3=sch["$defs"]["CoverageResultV3"]
out["CoverageResultV3_properties"]=sorted(cv3.get("properties",{}))
out["CoverageResultV3_required"]=sorted(cv3.get("required",[]))
scope=objects[cov['scopeId']][1]
out["scopeDescriptor"]={k:(v if not isinstance(v,list) else v) for k,v in scope.items()}
json.dump(out,sys.stdout,indent=1,default=str);print()
