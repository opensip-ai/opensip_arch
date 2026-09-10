import glob, json, os
O = "/tmp/opensip-design-corrections/consumer-b.v8/output"
tot = {}
for p in sorted(glob.glob(O + "/vectors-*.json")):
    try:
        d = json.load(open(p))
    except Exception:
        continue
    n = os.path.basename(p)
    if isinstance(d, list):
        tot[n] = len(d)
    elif isinstance(d, dict):
        tot[n] = sum(len(v) for v in d.values() if isinstance(v, list)) or len(d)
ob = json.load(open(O + "/object-table.json"))
bl = json.load(open(O + "/blobs.b64.json"))
print("complete positive Runs closed and re-verified from the export:",
      len(ob["runs"]))
print("total closure checks executed over those Runs:",
      sum(r["closureChecks"] for r in ob["runs"]))
print("distinct retained objects in the exported store:", bl["count"])
print("h-identity frames:", sum(r["hIdentityCount"] for r in ob["runs"]))
print("canonical records:", sum(r["canonicalRecordCount"] for r in ob["runs"]))
print("raw artifacts:", sum(r["rawArtifactCount"] for r in ob["runs"]))
print()
for k in sorted(tot):
    print("  %-40s %s" % (k, tot[k]))
gaps = json.load(open(O + "/vectors-gaps.json"))
print()
print("measured design gaps:", [(g["id"], g["severity"]) for g in gaps])
