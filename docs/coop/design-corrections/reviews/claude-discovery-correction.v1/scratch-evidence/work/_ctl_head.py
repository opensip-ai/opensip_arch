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
