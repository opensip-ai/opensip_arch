import hashlib, json, os, sys
KIT = "/tmp/opensip-design-corrections/consumer-b.v8/subject"
m = json.load(open(KIT + "/consumer-input-manifest.json"))
ok = bad = 0
for f in m["files"]:
    p = os.path.join(KIT, f["path"])
    b = open(p, "rb").read()
    if hashlib.sha256(b).hexdigest() == f["sha256"] and len(b) == f["bytes"]:
        ok += 1
    else:
        bad += 1
        print("MISMATCH", f["path"])
listed = {f["path"] for f in m["files"]}
on_disk = set()
for r, d, fs in os.walk(KIT):
    for x in fs:
        on_disk.add(os.path.relpath(os.path.join(r, x), KIT))
extra = sorted(on_disk - listed - {"consumer-input-manifest.json"})
print("manifest files: %d  verified: %d  mismatched: %d  unlisted-on-disk: %d"
      % (len(m["files"]), ok, bad, len(extra)))
print("parentSubjectSha256 asserted by the manifest:", m["parentSubjectSha256"])
print("NOTE: this kit is a declared SUBSET of that parent, so the parent aggregate")
print("      is NOT recomputable from these bytes; it is an unverifiable assertion")
print("      of custody, recorded as an input-custody limitation, not a defect.")
sys.exit(1 if bad or extra else 0)
