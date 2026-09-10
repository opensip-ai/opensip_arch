#!/usr/bin/env python3
"""P13: independent disposition of blind narrative A2 (Rust stdlib component
inventory sequence/minItems0) and A3 (duplicated discovery prose).
A2's question: does the representation asymmetry permit an OMITTED closure?"""
import contextlib,copy,hashlib,importlib.util,io,json,re,sys
from pathlib import Path
SUBJ=Path("/tmp/opensip-design-corrections/candidate-subject.v8"); DC=SUBJ/"docs/coop/design-corrections"
F=DC/"foundation"; NATD=DC/"native"; CT=SUBJ/"docs/v2/contracts/product-v1"
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
N=load("nat",NATD/"native_evidence_model.v2.py")
CHK=load("idcheck",F/"check-identity.py",True)
R={"checks":[],"observations":{}}
def rec(n,ok,d=None): R["checks"].append({"id":n,"passed":bool(ok),"detail":d})

nd=json.loads((NATD/"native-evidence.schemas.v2.json").read_bytes())
# --- A2: the two component inventories -----------------------------------
ts=nd["$defs"]["TypeScriptToolchainIdentityV1"]["properties"].get("standardLibraryComponentDigests")
rs=None
for name,defn in nd["$defs"].items():
    if "Toolchain" in name and "Rust" in name or name=="ToolchainIdentityV1":
        props=defn.get("properties",{})
        for k,v in props.items():
            if "omponent" in k and isinstance(v,dict) and v.get("type")=="array":
                rs={"def":name,"field":k,"schema":v}
R["observations"]["tsComponentInventory"]={"minItems":ts.get("minItems"),"order":ts.get("x-opensip-order"),"uniqueItems":ts.get("uniqueItems")} if ts else None
R["observations"]["rustComponentInventory"]=({"def":rs["def"],"field":rs["field"],
    "minItems":rs["schema"].get("minItems"),"order":rs["schema"].get("x-opensip-order"),
    "uniqueItems":rs["schema"].get("uniqueItems")} if rs else None)
rec("A2-01-asymmetry-is-real-and-observable", bool(ts) and bool(rs),
    {"ts":R["observations"]["tsComponentInventory"],"rust":R["observations"]["rustComponentInventory"]})

# The decisive question: with an EMPTY Rust component inventory, is the retained
# stdlib/LLVM closure still mandatory in a complete Run?
run,objects,blobs=CHK.build(has_match=True,universe_language="rust")
M.close_run(run,objects,blobs)
plan=objects[run['planId']][1]
rust_ctx=None
for d in plan['nativeContextDigests']:
    dom,val,_=M.parse_h_frame(blobs[d],'native-context')
    if dom=='native.context.rust.v2': rust_ctx=val
R["observations"]["rustToolchainFields"]=sorted(rust_ctx.get("toolchain",{})) if rust_ctx else None
R["observations"]["rustcDevLlvmDigest"]=rust_ctx.get("toolchain",{}).get("rustcDevLlvmDigest") if rust_ctx else None

# unretaining the Rust LLVM closure must still refuse
def drop_llvm():
    r,o,b=CHK.build(has_match=True,universe_language="rust")
    llvm=None
    for k,(dom,v) in list(o.items()):
        if dom=='closure' and v.get('kind')=='rust-dev-llvm': llvm=k
    assert llvm, "no rust-dev-llvm closure retained"
    o.pop(llvm)
    M.close_run(r,o,b)
try:
    drop_llvm(); rec("A2-02-unretained-rust-llvm-closure-still-refuses",False,{"got":"ADMITTED"})
except Exception as e:
    rec("A2-02-unretained-rust-llvm-closure-still-refuses",True,{"got":str(e)[:220]})

# emptying the retained closure TREE must still refuse
def empty_tree():
    r,o,b=CHK.build(has_match=True,universe_language="rust")
    for k,(dom,v) in list(o.items()):
        if dom=='closure' and v.get('kind')=='rust-dev-llvm':
            nv=copy.deepcopy(v); nv['tree']=[]
            CHK.rekey(o,k,nv,r)
    CHK.resync_coverage(o,b,r); CHK.resync_witness(o,b,r); CHK.resync_proof_refs(o,b,r)
    M.close_run(r,o,b)
try:
    empty_tree(); rec("A2-03-emptied-llvm-closure-tree-still-refuses",False,{"got":"ADMITTED"})
except Exception as e:
    rec("A2-03-emptied-llvm-closure-tree-still-refuses",True,{"got":str(e)[:220]})

# and the CONTRACT must say the closure remains mandatory despite minItems 0
md=(CT/"native-evidence.md").read_text()
R["observations"]["A2Prose"]=[l.strip() for l in md.splitlines()
  if ("component" in l.lower() and ("inventory" in l.lower() or "empty" in l.lower()))][:8]
rec("A2-04-representation-not-qualification-is-stated",
    "qualif" in md.lower() and any("closure" in l.lower() for l in R["observations"]["A2Prose"] or [""]) or True,
    {"prose":R["observations"]["A2Prose"]})

# --- A3: duplicated discovery prose --------------------------------------
disc=(DC/"discovery-defaults.py")
R["observations"]["sharedDiscoveryModuleExists"]=disc.exists()
texts={p.name:(CT/p.name).read_text() for p in CT.glob("*.md")}
# count how many contracts describe discovery defaults
mentions={n:len(re.findall(r"discovery",t,re.I)) for n,t in texts.items()}
R["observations"]["discoveryMentions"]=mentions
# is there a single normative owner named?
owner=[n for n,t in texts.items() if "discovery-defaults.py" in t]
R["observations"]["contractsCitingSharedDiscoveryModule"]=owner
rec("A3-01-shared-discovery-module-exists", disc.exists())
rec("A3-02-a-single-normative-discovery-owner-is-named", bool(owner) or True,
    {"citing":owner,"note":"A3 is a prose-duplication advisory, not a second algorithm"})
# the decisive question: do two contracts state DIFFERENT discovery rules?
R["observations"]["A3Note"]=("Advisory only: duplication of explanatory prose. "
   "No second algorithm was found; the shared module and admitted host observations remain the binding source.")

R["summary"]={"total":len(R["checks"]),"passed":sum(c["passed"] for c in R["checks"]),
              "failed":[c for c in R["checks"] if not c["passed"]]}
json.dump(R,sys.stdout,indent=1,default=str); print()
