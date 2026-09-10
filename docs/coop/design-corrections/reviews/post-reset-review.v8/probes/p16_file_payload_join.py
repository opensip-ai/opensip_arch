#!/usr/bin/env python3
"""P16: is a `file` relation payload's own path/contentSha256/byteLength joined
to the snapshot inventory, the way fact ANCHORS are?"""
import contextlib,hashlib,importlib.util,io,json,sys
from pathlib import Path
SUBJ=Path("/tmp/opensip-design-corrections/candidate-subject.v8"); DC=SUBJ/"docs/coop/design-corrections"; F=DC/"foundation"
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
R={"checks":[],"observations":{}}
def rec(n,ok,d=None): R["checks"].append({"id":n,"passed":bool(ok),"detail":d})

# 1. a deliberately false FilePayloadV1 validates against its REGISTERED selector
lying={"path":"a.ts","contentSha256":"f"*64,"byteLength":999999}
try:
    M.validate_registered_record("foundation/relation-payload-schemas.v2.json","#/$defs/FilePayloadV1",lying)
    ok=True; err=None
except Exception as e:
    ok=False; err=str(e)[:200]
R["observations"]["lyingFilePayloadValidates"]=ok
rec("FPJ-01-payload-layer-admits-a-content-claim-it-cannot-check", ok, {"error":err})

# 2. the relation registry declares NO snapshotJoins (the native registry does)
rel=json.loads((F/"relation-payload-schemas.v2.json").read_bytes())
ids=json.loads((F/"identity-schemas.v2.json").read_bytes())
R["observations"]["relationRegistryHasSnapshotJoins"]="snapshotJoins" in json.dumps(rel["x-opensip-relation-registry"])
nat_rows=ids["x-opensip-digest-domains"]["domainSets"]
R["observations"]["nativeRegistryHasSnapshotJoins"]="snapshotJoins" in json.dumps(nat_rows)
rec("FPJ-02-relation-registry-declares-no-snapshot-join",
    not R["observations"]["relationRegistryHasSnapshotJoins"],
    {"relation":R["observations"]["relationRegistryHasSnapshotJoins"],
     "native":R["observations"]["nativeRegistryHasSnapshotJoins"]})

# 3. the closure's relation rules perform no inventory lookup
src=(F/"identity-model.py").read_text()
seg=src[src.index("def relation_payload_rules"):src.index("def snapshot_joins")]
R["observations"]["relationRulesSource"]=seg
for tok in ("sourceInventory","inventory","snapshot"):
    rec("FPJ-03-no-"+tok+"-lookup-in-relation_payload_rules", tok not in seg, {"token":tok})

# 4. anchors, by contrast, ARE joined
anchor_seg=src[src.index("for anchor in fact['anchors']"):]
anchor_seg=anchor_seg[:anchor_seg.index("if any(cid not in")]
R["observations"]["anchorJoinSource"]=anchor_seg
rec("FPJ-04-anchors-are-joined-to-the-inventory",
    "sourceInventory" in anchor_seg and "ANCHOR_SOURCE" in anchor_seg)

# 5. which relation payload fields carry a digest at all
digest_fields=[]
for name,defn in rel["$defs"].items():
    for p,v in (defn.get("properties") or {}).items():
        if isinstance(v,dict) and v.get("$ref")=="#/$defs/DigestHex":
            digest_fields.append(name+"."+p)
R["observations"]["relationPayloadDigestFields"]=digest_fields
R["observations"]["scopeOfTheDigestLaw"]=(
  "identity-and-evidence section 3 scopes the closing digest law to "
  "identity-schemas.v2; native-evidence.schemas.v2 extends it to itself via its "
  "own x-opensip-digest-law. relation-payload-schemas.v2 is covered by NEITHER.")
R["summary"]={"total":len(R["checks"]),"passed":sum(c["passed"] for c in R["checks"]),
              "failed":[c for c in R["checks"] if not c["passed"]]}
json.dump(R,sys.stdout,indent=1,default=str); print()
