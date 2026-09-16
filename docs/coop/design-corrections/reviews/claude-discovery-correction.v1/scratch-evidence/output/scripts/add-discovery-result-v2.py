import json, hashlib, difflib, os, sys
SUCC=sys.argv[1]+chr(47); OUT=sys.argv[2]; os.makedirs(OUT, exist_ok=True)
rel="docs/coop/design-corrections/security/security-lifecycle.schemas.v1.json"
p=SUCC+rel; original=open(p).read(); d=json.loads(original)
sch=d["schemas"]
assert "DiscoveryResultV2" not in sch
r2=json.loads(json.dumps(sch["DiscoveryResultV1"]).replace("DiscoveryProvenanceV1","DiscoveryProvenanceV2"))
r2["description"]="Discovery result VERSION 2 (XA-02 / CR-25): identical shape to version 1 with a version-2 provenance record. Version 1 is retained as the historical result record for version-1 provenance bytes; an output is never validated under the version-1 name once its provenance changed."
sch["DiscoveryResultV2"]=r2
updated=json.dumps(d, indent=2, ensure_ascii=False)+chr(10)
open(p,"w").write(updated)
patch="".join(difflib.unified_diff(original.splitlines(True), updated.splitlines(True), fromfile=rel, tofile=rel))
open(OUT+chr(47)+"security-lifecycle.schemas.v1.json.discoveryresult.patch","w").write(patch)
print("OK DiscoveryResultV2", hashlib.sha256(original.encode()).hexdigest()[:12], "to", hashlib.sha256(updated.encode()).hexdigest()[:12], "patchLines", patch.count(chr(10)))
