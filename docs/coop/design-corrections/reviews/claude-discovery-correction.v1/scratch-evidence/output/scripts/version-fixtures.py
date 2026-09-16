"""Claude XA-02 / CR-25: version-2 fixture expectations in the isolated copy.

Each edit is reported so the reviewer sees WHAT changed, not only that a suite went green:
  * a pruned row gains markerCountBasis (the count itself is never altered here);
  * an admitted boundary inventory expectation moves to schemaVersion 2;
  * an explicit outputSchema naming a version-1 record moves to the version-2 record.
No expected count, anchor, unit, refusal or exit is rewritten by this script; a changed anchor set would
show up as a remaining suite failure and must be dispositioned by hand.
"""
import json, hashlib, difflib, os, sys
SUCC=sys.argv[1]+chr(47); OUT=sys.argv[2]; os.makedirs(OUT, exist_ok=True)
edits=[]; rows=[]
def walk(o, path):
    if isinstance(o, dict):
        if set(o)=={"path","reason","markerCount"}:
            o["markerCountBasis"]="observed-inventory"
            edits.append({"kind":"pruned-row-basis","at":path,"path":o["path"],"markerCount":o["markerCount"]})
            return
        if o.get("source")=="security.discovery" and "prunedTrees" in o and o.get("schemaVersion")==1:
            o["schemaVersion"]=2
            edits.append({"kind":"inventory-schema-version","at":path,"from":1,"to":2})
        if o.get("outputSchema")=="AdmittedBoundaryInventoryV1":
            o["outputSchema"]="AdmittedBoundaryInventoryV2"
            edits.append({"kind":"output-schema","at":path,"from":"AdmittedBoundaryInventoryV1","to":"AdmittedBoundaryInventoryV2"})
        for k,v in o.items(): walk(v, path+chr(47)+str(k))
    elif isinstance(o, list):
        for i,v in enumerate(o): walk(v, path+chr(47)+str(i))
for rel, ind in [("docs/coop/design-corrections/security/discovery-cases.v1.json",2),("docs/coop/design-corrections/native/native-cases.v2.json",1)]:
    p=SUCC+rel; original=open(p).read(); d=json.loads(original)
    before=len(edits); walk(d, "")
    for ea in (False, True):
        cand=json.dumps(d, indent=ind, ensure_ascii=ea)+chr(10)
        if json.dumps(json.loads(original), indent=ind, ensure_ascii=ea)+chr(10)==original: break
    updated=cand
    open(p,"w").write(updated)
    patch="".join(difflib.unified_diff(original.splitlines(True), updated.splitlines(True), fromfile=rel, tofile=rel))
    open(OUT+chr(47)+os.path.basename(rel)+".patch","w").write(patch)
    rows.append({"path":rel,"beforeSha256":hashlib.sha256(original.encode()).hexdigest(),"afterSha256":hashlib.sha256(updated.encode()).hexdigest(),"edits":len(edits)-before,"patchLines":patch.count(chr(10))})
    print("OK %-34s edits=%d patchLines=%d" % (os.path.basename(rel), len(edits)-before, patch.count(chr(10))))
json.dump({"standing":"CLAUDE AUTHORED CORRECTION; fixture version-2 stage","files":rows,"edits":edits}, open(OUT+chr(47)+"fixture-edits.json","w"), indent=2)
print("total edits", len(edits))
