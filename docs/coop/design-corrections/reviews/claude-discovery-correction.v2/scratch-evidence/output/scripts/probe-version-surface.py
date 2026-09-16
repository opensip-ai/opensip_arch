import json,importlib.util,sys,copy
from pathlib import Path
D=Path(sys.argv[1])/"docs/coop/design-corrections"
OUT=sys.argv[2]
def load(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);sys.modules[n]=m;s.loader.exec_module(m);return m
DD=load("dd",D/"discovery-defaults.py")
S=load("sec",D/"security/security_lifecycle_model_v1.py")
N=load("nat",D/"native/native_evidence_model.v2.py")
R="/home/alice/repo"
fs={"/":{"kind":"dir","uid":0,"mode":"0755","dev":1},"/home":{"kind":"dir","uid":0,"mode":"0755","dev":1},
    "/home/alice":{"kind":"dir","uid":1000,"mode":"0700","dev":1},
    R:{"kind":"dir","uid":1000,"mode":"0755","dev":1,"vcs":True},
    R+"/package.json":{"kind":"file","uid":1000,"mode":"0644","nlink":1,"size":100}}
prov=S.discovery({"invokingUid":1000,"accountHome":"/home/alice","cwd":R,"fs":fs})["provenance"]
rows=[]
def probe(name, fn):
    try:
        v=fn(); rows.append({"probe":name,"outcome":"accepted","detail":v})
    except Exception as e:
        rows.append({"probe":name,"outcome":"refused","error":type(e).__name__,"reason":str(e)[:200]})
    print(rows[-1]["probe"], rows[-1]["outcome"], rows[-1].get("error",""), str(rows[-1].get("reason") or rows[-1].get("detail"))[:110])
v1empty=copy.deepcopy(prov); v1empty["schemaVersion"]=1
probe("read: validate_discovery_provenance V1 empty prunes", lambda: S.validate_discovery_provenance(v1empty) and "valid")
probe("convert: boundary_inventory_from_provenance(V1 empty)", lambda: DD.boundary_inventory_from_provenance(v1empty)["schemaVersion"])
inv2=DD.boundary_inventory_from_provenance(prov)
v1inv=copy.deepcopy(inv2); v1inv["schemaVersion"]=1
v1inv["prunedTrees"]=[{"path":"node_modules","reason":"dependency-tree","markerCount":1}]
probe("read: validate_boundary_inventory V1 legacy row", lambda: N.validate_boundary_inventory(v1inv) and "valid")
mk={"package.json":{"sha256":"a"*64},"node_modules/pkg/package.json":{"sha256":"b"*64}}
probe("current: discover_units(V1 inventory)", lambda: N.discover_units(mk,None,v1inv))
probe("current: assign_membership(V1 inventory)", lambda: N.assign_membership([{"rootPath":"","languageFamily":"tsjs"}],["package.json"],v1inv) and "accepted")
probe("current: unit_scope_descriptor(V1 inventory)", lambda: N.unit_scope_descriptor([{"rootPath":""}],[],None,[],v1inv)["scopeDigest"][:12])
probe("current: require_admitted_boundaries(V1 inventory)", lambda: N.require_admitted_boundaries(v1inv)["schemaVersion"])
for bad in [7, True, "2", None, 2.0]:
    b=copy.deepcopy(inv2); b["schemaVersion"]=bad
    probe("read: validate_boundary_inventory version=%r"%(bad,), (lambda bb: (lambda: N.validate_boundary_inventory(bb) and "valid"))(b))
    p=copy.deepcopy(prov); p["schemaVersion"]=bad
    probe("read: validate_discovery_provenance version=%r"%(bad,), (lambda pp: (lambda: S.validate_discovery_provenance(pp) and "valid"))(p))
    probe("convert: boundary_inventory_from_provenance version=%r"%(bad,), (lambda pp: (lambda: DD.boundary_inventory_from_provenance(pp)["schemaVersion"]))(p))
Path(OUT).write_text(json.dumps({"standing":"Claude v2 probe of the v1 authored version surface; no product claim","source":sys.argv[1],"probes":rows},indent=2)+chr(10))
