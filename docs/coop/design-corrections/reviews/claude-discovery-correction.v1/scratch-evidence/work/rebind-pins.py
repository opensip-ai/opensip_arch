"""Claude XA-02 / CR-25: explicit SCRATCH-ONLY source-pin rebinding.

Rebinds every pin ledger in the isolated successor copy to the bytes now in that copy and records the
exact before/after delta. Rebinding is bookkeeping for the reference suites; it grants no acceptance and
no product qualification. Root live files and frozen candidate25 are untouched.
"""
import argparse, hashlib, json, glob, os
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument("--copy", type=Path, required=True); p.add_argument("--out", type=Path, required=True)
a=p.parse_args(); changes=[]; ledgers=[]
for lp in sorted(glob.glob(str(a.copy)+"/docs/**/source-pins*.json", recursive=True)):
    d=json.loads(Path(lp).read_text())
    rel=os.path.relpath(lp, a.copy)
    rows=d.get("pins") or d.get("files") or []
    n=0
    for row in rows:
        t=a.copy/row["path"]
        if not t.exists():
            changes.append({"ledger":rel,"path":row["path"],"before":row.get("sha256"),"after":None,"note":"absent in isolated copy"}); continue
        actual=hashlib.sha256(t.read_bytes()).hexdigest()
        if actual != row.get("sha256"):
            changes.append({"ledger":rel,"path":row["path"],"before":row.get("sha256"),"after":actual})
            row["sha256"]=actual; n+=1
    ledgers.append({"ledger":rel,"pinRows":len(rows),"rebound":n})
    f=Path(lp); f.chmod(f.stat().st_mode|0o200); f.write_text(json.dumps(d, indent=2)+chr(10))
a.out.write_text(json.dumps({"standing":"CLAUDE SCRATCH-ONLY pin rebinding; not independent review, acceptance or source activation","ledgers":ledgers,"changes":changes}, indent=2)+chr(10))
print("Rebound", len(changes), "pins across", len(ledgers), "ledgers")
