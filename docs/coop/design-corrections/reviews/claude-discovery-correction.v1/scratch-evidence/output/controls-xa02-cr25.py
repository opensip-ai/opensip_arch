"""Claude XA-02 / CR-25 controls. Reference observations only; NOT product qualification."""
import argparse, copy, hashlib, importlib.util, json, sys
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument("--source", type=Path, required=True); p.add_argument("--out", type=Path, required=True)
args=p.parse_args()
def load(n, path):
    s=importlib.util.spec_from_file_location(n, path); m=importlib.util.module_from_spec(s); sys.modules[n]=m; s.loader.exec_module(m); return m
D=args.source/"docs/coop/design-corrections"
K=load("chk", D/"security/check-security-lifecycle.v1.py"); S=K.model
N=load("nat", D/"native/native_evidence_model.v2.py")
DD=load("dd", D/"discovery-defaults.py")
C=load("can", D/"foundation/canonical.py")
H=load("host", D/"integration-host-model.py")
R="/home/alice/repo"
rows=[]
def rec(name, expected, got, holds, note=""):
    rows.append({"control": name, "expected": expected, "observed": got, "holds": bool(holds), "note": note})
    print(("PASS " if holds else "FAIL ")+name)
def base_fs():
    d=lambda: {"kind":"dir","uid":1000,"mode":"0755","dev":1}
    f=lambda: {"kind":"file","uid":1000,"mode":"0644","nlink":1,"size":100}
    fs={"/":{"kind":"dir","uid":0,"mode":"0755","dev":1},"/home":{"kind":"dir","uid":0,"mode":"0755","dev":1},
        "/home/alice":{"kind":"dir","uid":1000,"mode":"0700","dev":1},
        R:{"kind":"dir","uid":1000,"mode":"0755","dev":1,"vcs":True}, R+"/package.json": f()}
    return fs, d, f
def markers_of(fs):
    return {p[len(R)+1:]:{"sha256":"a"*64} for p,e in fs.items() if p.startswith(R+"/") and e["kind"]=="file" and p.rpartition("/")[2] in DD.WORKSPACE_MARKERS}
def files_of(fs):
    return sorted(p[len(R)+1:] for p,e in fs.items() if p.startswith(R+"/") and e["kind"]=="file")
def disc(fs, **kw):
    inp={"invokingUid":1000,"accountHome":"/home/alice","cwd":R,"fs":fs}; inp.update(kw); return S.discovery(inp)
def anchors(prov):
    return sorted((t["path"], t["reason"], t["markerCount"], t["markerCountBasis"]) for t in prov["prunedTrees"])
fs,d,f=base_fs()
fs[R+"/node_modules"]=d(); fs[R+"/node_modules/pkg"]=d()
o=disc(fs); pr=anchors(o["provenance"])
rec("C1 no-marker node_modules anchor is reported", [(R+"/node_modules","dependency-tree",0,"observed-inventory")], pr, pr==[(R+"/node_modules","dependency-tree",0,"observed-inventory")], "CR-25: version 1 reported nothing here")
fs2,d2,f2=base_fs()
fs2[R+"/node_modules"]=d2(); fs2[R+"/node_modules/pkg"]=d2(); fs2[R+"/node_modules/pkg/index.js"]=f2()
o2=disc(fs2); pr2=anchors(o2["provenance"])
rec("C2 pruned tree with only non-marker files", [(R+"/node_modules","dependency-tree",0,"observed-inventory")], pr2, pr2==[(R+"/node_modules","dependency-tree",0,"observed-inventory")])
fs3,d3,f3=base_fs()
fs3[R+"/node_modules"]=dict(d3(), aclUnreadable=True); fs3[R+"/node_modules/p/package.json"]=f3()
o3=disc(fs3); pr3=anchors(o3["provenance"])
rec("C3 unreadable pruned directory keeps the anchor and nulls the count", [(R+"/node_modules","dependency-tree",None,"not-enumerated")], pr3, pr3==[(R+"/node_modules","dependency-tree",None,"not-enumerated")], "per-row basis; a global basis could not express this")
z=disc(base_fs()[0]); rec("C4a zero supplied marker observations beyond the root", [], anchors(z["provenance"]), anchors(z["provenance"])==[] and z["status"]=="ACCEPT")
big=K._synthetic_repo(0,4200); ob=S.discovery(big)
exp=[("/home/alice/big/node_modules","dependency-tree",4200,"observed-inventory")]
rec("C4b 4200 supplied installed markers stay one anchor with an exact supplied count", exp, anchors(ob["provenance"]), anchors(ob["provenance"])==exp and len(ob["provenance"]["units"])==1)
ne=disc(fs2, prunedTreeMarkerInventory="not-enumerated")
exp=[(R+"/node_modules","dependency-tree",None,"not-enumerated")]
rec("C4c declared not-enumerated inventory yields a null count, never zero", exp, anchors(ne["provenance"]), anchors(ne["provenance"])==exp, "zero observed is not zero hidden")
try:
    S.discovery({"invokingUid":1000,"accountHome":"/home/alice","cwd":R,"fs":fs2,"prunedTreeMarkerInventory":"guessed"}); bad="ACCEPTED"
except Exception as e: bad=type(e).__name__+":"+str(e)
rec("C4d unknown basis declaration is an instrument shape error", "Reject:DISCOVERY_OBSERVATION_SHAPE", bad, "DISCOVERY_OBSERVATION_SHAPE" in bad)
fsx,dx,fx=base_fs()
fsx[R+"/packages"]=dx(); fsx[R+"/packages/web"]=dx(); fsx[R+"/packages/web/package.json"]=fx()
fsx[R+"/packages/web/node_modules"]=dx(); fsx[R+"/packages/web/node_modules/dep"]=dx()
fsx[R+"/packages/web/node_modules/dep/package.json"]=fx()
fsx[R+"/vendorish"]=dx(); fsx[R+"/vendorish/.hg"]=dx()
ox=disc(fsx); inv=S.boundary_inventory(ox)
nd=N.discover_units(markers_of(fsx), None, inv)
adm=sorted((t["path"],t["reason"]) for t in inv["prunedTrees"])
car=sorted((t["path"],t["reason"]) for t in nd["prunedTrees"])
ok6 = nd["refused"] is None and car==adm and (("vendorish/.hg","vcs-tree") in car)
rec("C6 extra admitted anchor accepted and carried", adm, car, ok6, "vendorish/.hg holds no marker so native cannot derive it")
miss=copy.deepcopy(inv)
miss["prunedTrees"]=[t for t in miss["prunedTrees"] if not (t["path"]=="packages/web/node_modules")]
nm=N.discover_units(markers_of(fsx), None, miss)
d7=(nm["refused"] or {}).get("detail")
rec("C7 missing marker-implied anchor still refuses", "native.boundary-inventory-mismatch", d7, d7=="native.boundary-inventory-mismatch")
wrong=copy.deepcopy(inv)
for t in wrong["prunedTrees"]:
    if t["path"]=="packages/web/node_modules": t["reason"]="vcs-tree"
nw=N.discover_units(markers_of(fsx), None, wrong)
d8=(nw["refused"] or {}).get("detail")
rec("C8 mismatched reason refuses", "native.boundary-inventory-mismatch", d8, d8=="native.boundary-inventory-mismatch")
cnt=copy.deepcopy(inv)
for t in cnt["prunedTrees"]:
    t["markerCount"]=None; t["markerCountBasis"]="not-enumerated"
nc=N.discover_units(markers_of(fsx), None, cnt)
rec("C5a count and basis are not equality keys", "no refusal", (nc["refused"] or {}).get("detail"), nc["refused"] is None)
sb=N.unit_scope_descriptor(nd["units"], [], None, nd["prunedTrees"], inv)
sc=N.unit_scope_descriptor(nc["units"], [], None, nc["prunedTrees"], cnt)
ok5b = sb["scopeDescriptor"]==sc["scopeDescriptor"] and sb["scopeDigest"]==sc["scopeDigest"]
rec("C5b count or basis change leaves scopeDescriptor and scopeDigest bit-identical", sb["scopeDigest"], sc["scopeDigest"], ok5b, "only the path member reaches excludedPathPrefixes")
ub=sorted(u["rootPath"] for u in nd["units"]); uc=sorted(u["rootPath"] for u in nc["units"])
rec("C11a count or basis change leaves the selected unit set identical", ub, uc, ub==uc)
ob=hashlib.sha256(C.canonical(inv)).hexdigest(); oc=hashlib.sha256(C.canonical(cnt)).hexdigest()
rec("C5c count or basis change DOES change the operational provenance digest", "differs", {"base":ob[:16],"changed":oc[:16]}, not (ob==oc), "exact bytes changed; a truthful provenance change, not a semantic one")
fl=list(sb["scopeDescriptor"]["excludedPathPrefixes"])
rec("C11b a directory-only anchor DOES reach excludedPathPrefixes", "vendorish/.hg present", fl, "vendorish/.hg" in fl, "disclosed identity consequence of CR-25; the segment rule already pruned the tree so the analysed byte set is unchanged")
fsn,dn,fn=base_fs()
fsn[R+"/vendor"]=dn(); fsn[R+"/vendor/lib"]=dict(dn(), vcs=True); fsn[R+"/vendor/lib/package.json"]=fn()
fsn[R+"/apps"]=dn(); fsn[R+"/apps/site"]=dn(); fsn[R+"/apps/site/opensip.json"]=fn(); fsn[R+"/apps/site/package.json"]=fn()
fsn[R+"/ws"]=dn(); fsn[R+"/ws/Cargo.toml"]=dict(fn(), isCargoWorkspace=True)
fsn[R+"/ws/m"]=dn(); fsn[R+"/ws/m/Cargo.toml"]=fn(); fsn[R+"/ws/target"]=dn()
on=disc(fsn); ivn=S.boundary_inventory(on)
mk=markers_of(fsn)
mk["ws/Cargo.toml"]["isCargoWorkspace"]=True
nn=N.discover_units(mk, None, ivn)
rootsn=sorted(u["rootPath"] for u in nn["units"])
okpar = nn["refused"] is None and "vendor/lib" not in rootsn and "apps/site" not in rootsn
rec("C9a nested repository and nested project stay excluded under the corrected rule", "vendor/lib and apps/site absent", rootsn, okpar)
ws=[u for u in nn["units"] if u["rootPath"]=="ws"]
okws = len(ws)==1 and ws[0]["memberPackageRoots"]==["ws/m"]
rec("C9b Cargo member folding parity", ["ws/m"], (ws[0]["memberPackageRoots"] if ws else None), okws)
tgt=[(t["path"],t["reason"]) for t in nn["prunedTrees"]]
rec("C9c marker-less Cargo target anchor is now reported", "ws/target cargo-build-output present", tgt, ("ws/target","cargo-build-output") in tgt)
oe=disc(fsn, configWorkspaceRoots=["."]) 
ive=S.boundary_inventory(oe)
ne=N.discover_units(mk, ["."], ive)
rootse=sorted(u["rootPath"] for u in ne["units"])
rec("C9d explicit root selection parity", [""], rootse, ne["refused"] is None and rootse==[""])
def custody_case(total, bad_dir, bad_marker):
    ctx=K._synthetic_repo(total,0); RR=ctx["cwd"]
    names=sorted(k for k in ctx["fs"] if k.startswith(RR+"/pkg") and k.endswith("/package.json"))
    for i in range(bad_dir): ctx["fs"][names[i].rsplit("/",1)[0]]["mode"]="0757"
    for i in range(bad_dir,bad_dir+bad_marker): ctx["fs"][names[i]]["nlink"]=2
    sec=S.discovery(ctx)
    if not (sec["status"]=="ACCEPT"): return sec, None, None
    iv=S.boundary_inventory(sec)
    mkx={k[len(RR)+1:]:{"sha256":"a"*64} for k,e in ctx["fs"].items() if k.startswith(RR+"/") and e["kind"]=="file" and k.rpartition("/")[2] in DD.WORKSPACE_MARKERS}
    return sec, iv, N.discover_units(mkx, None, iv)
s1,i1,n1=custody_case(4200,150,0)
ok10a = s1["status"]=="ACCEPT" and len(s1["provenance"]["units"])==4051 and n1["refused"] is None and len(n1["units"])==4051
rec("C10a 4200 first-party with 150 directory-custody failures still admits 4051 in BOTH instruments", 4051, {"security":len(s1["provenance"]["units"]),"native":len(n1["units"]) if n1 else None}, ok10a, "preserves the corrected cap/custody behaviour verified in review pass 2")
s2,i2,n2=custody_case(4200,0,150)
ok10b = s2["status"]=="ACCEPT" and len(s2["provenance"]["units"])==4051 and n2["refused"] is None and len(n2["units"])==4051
rec("C10b same for 150 marker-custody failures", 4051, {"security":len(s2["provenance"]["units"]),"native":len(n2["units"]) if n2 else None}, ok10b)
s3,_,_=custody_case(4096,0,0)
ok10c = s3["status"]=="REFUSE" and s3["detail"]=="WORKSPACE_UNIT_LIMIT:4097>4096"
rec("C10c 4096 pkg dirs plus the root is 4097 selected directories and refuses", "WORKSPACE_UNIT_LIMIT:4097>4096", s3.get("detail"), ok10c)
s4,i4,n4=custody_case(4095,0,0)
ok10d = s4["status"]=="ACCEPT" and len(s4["provenance"]["units"])==4096 and n4["refused"] is None and len(n4["units"])==4096
rec("C10d exactly 4096 selected directories admit in both instruments", 4096, {"security":len(s4["provenance"]["units"]),"native":len(n4["units"]) if n4 else None}, ok10d)
try:
    N.require_admitted_boundaries(None); hb="ACCEPTED"
except Exception as e: hb=type(e).__name__+":"+str(e)
rec("C12a authoritative lane refuses a missing admitted inventory", "NativeRefusal:native.admitted-boundaries-required", hb, "admitted-boundaries-required" in hb)
alone=N.discover_units(markers_of(fsx), None, None)
rec("C12b standalone/algorithm lane still accepts no inventory", "no refusal", (alone["refused"] or {}).get("detail"), alone["refused"] is None and alone["boundaries"]["source"]=="none")
try:
    N.validate_boundary_inventory(dict(inv, schemaVersion=7)); vb="ACCEPTED"
except Exception as e: vb=type(e).__name__+":"+str(e)
rec("C12c unknown inventory version refuses rather than falling back to V1", "native.boundary-inventory-version-unknown:7", vb, "version-unknown:7" in vb)
try:
    S.validate_discovery_provenance(dict(ox["provenance"], schemaVersion=9)); pv="ACCEPTED"
except Exception as e: pv=type(e).__name__+":"+str(e)
rec("C12d unknown provenance version refuses", "DISCOVERY_PROVENANCE_VERSION_UNKNOWN:9", pv, "DISCOVERY_PROVENANCE_VERSION_UNKNOWN:9" in pv)
S.validate_input("DiscoveryProvenanceV2", ox["provenance"]); N.validate_native("AdmittedBoundaryInventoryV2", inv); N.validate_native("UnitDiscoveryV2", nd)
rec("C12e version-2 records validate under their own named definitions", "valid", "valid", True, "a changed record is never named V1")
hostres=H.admit_repository_discovery({"invokingUid":1000,"accountHome":"/home/alice","cwd":R,"fs":fsx}, markers_of(fsx), files_of(fsx))
okh = hostres["native"]["refused"] is None and hostres["boundaries"]["schemaVersion"]==2
rec("C13 full security to boundary to native host composition runs on version 2", "schemaVersion 2, no refusal", {"schemaVersion":hostres["boundaries"]["schemaVersion"],"units":len(hostres["native"]["units"])}, okh)
args.out.write_text(json.dumps({"standing":"CLAUDE reference controls for the XA-02 / CR-25 correction; synthetic trusted observations; NOT product qualification","source":str(args.source),"controls":rows,"passed":sum(1 for r in rows if r["holds"]),"failed":[r["control"] for r in rows if not r["holds"]]}, indent=2)+chr(10))
print("controls", sum(1 for r in rows if r["holds"]), "of", len(rows))
sys.exit(0 if all(r["holds"] for r in rows) else 1)
