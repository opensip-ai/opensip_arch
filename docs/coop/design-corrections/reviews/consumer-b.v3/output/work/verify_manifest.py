import hashlib, json, os, sys
BASE="/tmp/opensip-design-corrections/consumer-b.v3/subject"
m=json.load(open(os.path.join(BASE,"consumer-input-manifest.json")))
rows=[];ok=True
listed=set()
for f in m["files"]:
    p=os.path.join(BASE,f["path"]); listed.add(f["path"])
    if not os.path.exists(p):
        rows.append((f["path"],"MISSING","","")); ok=False; continue
    b=open(p,"rb").read()
    h=hashlib.sha256(b).hexdigest()
    good = (h==f["sha256"]) and (len(b)==f["bytes"])
    ok = ok and good
    rows.append((f["path"],"OK" if good else "MISMATCH",h,len(b)))
# extra files on disk?
onDisk=set()
for root,d,fs in os.walk(BASE):
    for x in fs:
        rp=os.path.relpath(os.path.join(root,x),BASE)
        if rp!="consumer-input-manifest.json": onDisk.add(rp)
extra=sorted(onDisk-listed); missing=sorted(listed-onDisk)
for r in rows:
    print(r[1], r[0], r[2][:16], r[3])
print("EXTRA_ON_DISK:",extra)
print("MISSING:",missing)
print("COUNT:",len(rows))
print("ALL_OK:",ok and not extra and not missing)
# parent-subject claim: compute an aggregate over manifest content itself
mb=open(os.path.join(BASE,"consumer-input-manifest.json"),"rb").read()
print("MANIFEST_SHA256:",hashlib.sha256(mb).hexdigest())
print("CLAIMED_PARENT:",m["parentSubjectSha256"])
