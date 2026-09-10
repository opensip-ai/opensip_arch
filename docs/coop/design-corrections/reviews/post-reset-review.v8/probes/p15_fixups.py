#!/usr/bin/env python3
"""P15: three checks P14 could not decide cleanly.
 (a) H domain separation, using the frame builder (which does not schema-validate)
 (b) the complete list of shared canonical-record recipes, each matched to the
     contract sentence that declares the sameness
 (c) FilePayloadV1.contentSha256: is it joined to the snapshot inventory?
     P14 refused at FACT_SCOPE_JOIN, so the scope must move to file/enumerated
     first for the question to be reached at all.
"""
import contextlib,copy,hashlib,importlib.util,io,json,re,sys
from pathlib import Path
SUBJ=Path("/tmp/opensip-design-corrections/candidate-subject.v8"); DC=SUBJ/"docs/coop/design-corrections"
F=DC/"foundation"; CT=SUBJ/"docs/v2/contracts/product-v1"
def load(n,p,iso=False):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s)
    if not iso: s.loader.exec_module(m);return m
    a,b=sys.argv,io.StringIO(); sys.argv=[str(p)]
    try:
        with contextlib.redirect_stdout(b):
            try: s.loader.exec_module(m)
            except SystemExit: pass
    finally: sys.argv=a
    return m
M=load("idmodel",F/"identity-model.py"); C=M.C
CHK=load("idcheck",F/"check-identity.py",True)
R={"checks":[],"observations":{}}
def rec(n,ok,d=None): R["checks"].append({"id":n,"passed":bool(ok),"detail":d})
def putblob(b,v):
    raw=v if isinstance(v,bytes) else C.canonical(v); d=hashlib.sha256(raw).hexdigest(); b[d]=raw; return d

# (a) H domain separation over the raw frame builder
ids=json.loads((F/"identity-schemas.v2.json").read_bytes())
doms=sorted(ids["x-opensip-digest-domains"]["byDomain"])
payload={"schemaVersion":2,"x":1}
minted={d:hashlib.sha256(M.h_preimage_frame(d,payload)).hexdigest() for d in doms}
rec("COL-02b-every-H-domain-mints-a-distinct-identity-for-one-payload",
    len(set(minted.values()))==len(minted), {"domains":len(minted),"distinct":len(set(minted.values()))})
R["observations"]["hDomains"]=doms

# (b) complete sharing inventory, matched to declaring prose
md=(CT/"identity-and-evidence.md").read_text()
def ann_of(n):
    if not isinstance(n,dict): return None
    if "x-opensip-digest" in n: return n["x-opensip-digest"]
    if "items" in n:
        a=ann_of(n["items"])
        if a: return a
    for b in n.get("oneOf",[])+n.get("anyOf",[]):
        if isinstance(b,dict) and b.get("type")=="null": continue
        a=ann_of(b)
        if a: return a
    return None
sites=[]
def walk(n,p):
    if isinstance(n,dict):
        for k,v in (n.get("properties") or {}).items():
            a=ann_of(v)
            if a: sites.append({"path":p+"/properties/"+k,"ann":a})
        for k,v in n.items(): walk(v,p+"/"+str(k))
    elif isinstance(n,list):
        for i,v in enumerate(n): walk(v,p+"/"+str(i))
walk(ids,"#")
groups={}
for s in sites:
    a=s["ann"]
    if isinstance(a,dict) and a.get("representation")=="canonical-record":
        groups.setdefault(json.dumps(a.get("record"),sort_keys=True),[]).append(s["path"])
shared={k:v for k,v in groups.items() if len(v)>1}
# for each sharing, find the field NAME and check the contract mentions the sameness
analysis={}
for k,v in shared.items():
    field=v[0].rsplit("/",1)[-1]
    # the contract must either name the field explicitly or state the agreement
    mentioned = field in md
    analysis[k]={"sites":v,"field":field,"fieldNamedInContract":mentioned}
R["observations"]["sharedRecipes"]=analysis
undeclared=[a for a in analysis.values() if not a["fieldNamedInContract"]]
rec("COL-01b-every-shared-canonical-record-recipe-is-named-in-the-contract",
    not undeclared, {"undeclared":undeclared,"sharedGroups":len(analysis)})

# (c) FilePayloadV1.contentSha256 join, reached properly
def file_fact(content_sha, byte_len, path="a.ts"):
    run,objects,blobs=CHK.build(has_match=True)
    # move the scope to file/enumerated so the fact is in-scope
    skey=next(k for k,(d,v) in objects.items() if d=='subject-scope')
    scope=copy.deepcopy(objects[skey][1]); scope.update(relation='file',resolution='enumerated')
    CHK.rekey(objects,skey,scope,run)
    key=next(k for k,(d,v) in objects.items() if d=='fact')
    fact=copy.deepcopy(objects[key][1]); fact.update(relation='file',resolution='enumerated')
    fact["payloadDigest"]=putblob(blobs,{"path":path,"contentSha256":content_sha,"byteLength":byte_len})
    CHK.rekey(objects,key,fact,run)
    CHK.resync_coverage(objects,blobs,run); CHK.resync_witness(objects,blobs,run); CHK.resync_proof_refs(objects,blobs,run)
    return M.close_run(run,objects,blobs)

# the TRUE content digest of a.ts in the fixture inventory
run,objects,blobs=CHK.build(has_match=True)
inv={r['path']:r for r in objects[run['snapshotId']][1]['sourceInventory']}
R["observations"]["inventoryRowForATs"]=inv.get('a.ts')
true_sha=inv['a.ts']['sha256']; true_len=inv['a.ts']['bytes']

try:
    file_fact(true_sha,true_len); rec("FP-02-truthful-file-fact-admits",True)
except Exception as e:
    rec("FP-02-truthful-file-fact-admits",False,{"got":str(e)[:280]})
try:
    file_fact("f"*64,true_len)
    R["observations"]["falseContentSha"]="ADMITTED"
    rec("FP-03-false-contentSha256-refused",False,
        {"got":"ADMITTED -- a `file` relation payload may claim a contentSha256 that "
               "is not the inventoried digest of the path it names"})
except Exception as e:
    R["observations"]["falseContentSha"]="REFUSED:"+str(e)[:250]
    rec("FP-03-false-contentSha256-refused",True,{"got":str(e)[:250]})
try:
    file_fact(true_sha,true_len+999)
    rec("FP-04-false-byteLength-refused",False,{"got":"ADMITTED"})
except Exception as e:
    rec("FP-04-false-byteLength-refused",True,{"got":str(e)[:250]})
try:
    file_fact(true_sha,true_len,path="not-in-snapshot.ts")
    rec("FP-05-uninventoried-path-refused",False,{"got":"ADMITTED"})
except Exception as e:
    rec("FP-05-uninventoried-path-refused",True,{"got":str(e)[:250]})

R["summary"]={"total":len(R["checks"]),"passed":sum(c["passed"] for c in R["checks"]),
              "failed":[c for c in R["checks"] if not c["passed"]]}
json.dump(R,sys.stdout,indent=1,default=str); print()
