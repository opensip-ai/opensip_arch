import json,importlib.util,sys,copy
from pathlib import Path
D=Path(sys.argv[1])/"docs/coop/design-corrections"
def load(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);sys.modules[n]=m;s.loader.exec_module(m);return m
DD=load("dd",D/"discovery-defaults.py")
S=load("sec",D/"security/security_lifecycle_model_v1.py")
N=load("nat",D/"native/native_evidence_model.v2.py")
R="/home/alice/repo"
fs={"/":{"kind":"dir","uid":0,"mode":"0755","dev":1},"/home":{"kind":"dir","uid":0,"mode":"0755","dev":1},
    "/home/alice":{"kind":"dir","uid":1000,"mode":"0700","dev":1},
    R:{"kind":"dir","uid":1000,"mode":"0755","dev":1,"vcs":True},
    R+"/package.json":{"kind":"file","uid":1000,"mode":"0644","nlink":1,"size":100},
    R+"/node_modules":{"kind":"dir","uid":1000,"mode":"0755","dev":1},
    R+"/node_modules/pkg":{"kind":"dir","uid":1000,"mode":"0755","dev":1},
    R+"/node_modules/pkg/package.json":{"kind":"file","uid":1000,"mode":"0644","nlink":1,"size":100}}
prov=S.discovery({"invokingUid":1000,"accountHome":"/home/alice","cwd":R,"fs":fs})["provenance"]
inv2=DD.boundary_inventory_from_provenance(prov)
mk={"package.json":{"sha256":"a"*64},"node_modules/pkg/package.json":{"sha256":"b"*64}}
good=N.discover_units(mk,None,inv2)
print("V2 baseline units",len(good["units"]),"pruned",good["prunedTrees"])
v1inv=copy.deepcopy(inv2); v1inv["schemaVersion"]=1
v1inv["prunedTrees"]=[{"path":"node_modules","reason":"dependency-tree","markerCount":1}]
for name,fn in [("assign_membership", lambda: N.assign_membership(good["units"],["package.json"],v1inv)),
                ("unit_scope_descriptor", lambda: N.unit_scope_descriptor(good["units"],[],None,v1inv["prunedTrees"],v1inv))]:
    try:
        r=fn(); print("current:",name,"(V1 inventory) ACCEPTED", str(r)[:90])
    except Exception as e:
        print("current:",name,"(V1 inventory) refused", type(e).__name__, str(e)[:90])
