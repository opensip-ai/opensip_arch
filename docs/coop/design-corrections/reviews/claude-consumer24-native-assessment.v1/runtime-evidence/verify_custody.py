"""Custody for the consumer24 native assessment: manifests, snapshots, consumer kit, and the v37->v38 delta.

Reads only. Writes stdout. Verifies:
- source37 and source38 manifest SHA-256 against the dispatch values, and every snapshot file against its manifest
  (plus unlisted files);
- the consumer kit manifest SHA-256, every kit member against its bytes in consumer-b.v24/subject, and that every
  kit member equals the same path in source37 (the kit's declared parent);
- the manifest-level v37 -> v38 delta (changed, added, removed paths), and which kit members changed in v38.
"""
import hashlib
import json
import os
import sys

M37 = "/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v37.json"
M38 = "/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v38.json"
KIT = "/tmp/opensip-design-corrections/consumer-b.v24/subject/consumer-input-manifest.json"
KIT_ROOT = "/tmp/opensip-design-corrections/consumer-b.v24/subject"
EXPECT = {"m37": "245ef613243aafeaac2dcdca7f0b398d5a770ec338abbf712039fdfd91676680",
          "m38": "2ddfa0dbfc101b264c24d2a1f63de1e4e70908ac2a7346eaf0dab09d37f7e5c5",
          "kit": "e57ef3a785d5e25cfdfd02955cb4249f5f2443da1790832dce50d9d64bb4cc3c"}


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha_file(p):
    with open(p, "rb") as fh:
        return sha_bytes(fh.read())


def load(path, key):
    raw = open(path, "rb").read()
    got = sha_bytes(raw)
    return json.loads(raw), {"path": path, "sha256": got, "expected": EXPECT[key], "matches": got == EXPECT[key]}


def verify_snapshot(manifest):
    root = manifest["snapshotRoot"]
    listed, bad, total = set(), [], 0
    for f in manifest["files"]:
        listed.add(f["path"])
        p = os.path.join(root, f["path"])
        if not os.path.isfile(p):
            bad.append({"path": f["path"], "state": "missing"})
            continue
        b = open(p, "rb").read()
        total += len(b)
        if sha_bytes(b) != f["sha256"] or len(b) != f["bytes"]:
            bad.append({"path": f["path"], "state": "changed"})
    extra = []
    for d, _, fs in os.walk(root):
        for fn in fs:
            rel = os.path.relpath(os.path.join(d, fn), root)
            if rel not in listed and "__pycache__" not in rel.split(os.sep):
                extra.append(rel)
    return {"root": root, "files": len(manifest["files"]), "fileCount": manifest.get("fileCount"), "bytes": total,
            "totalBytes": manifest.get("totalBytes"), "bad": bad, "extra": sorted(extra),
            "exact": not bad and not extra and total == manifest.get("totalBytes")}


m37, c37 = load(M37, "m37")
m38, c38 = load(M38, "m38")
kit, ckit = load(KIT, "kit")
out = {"manifests": {"source37": c37, "source38": c38, "kit": ckit},
       "source38ParentManifestSha256": m38.get("parentManifestSha256")}
if "--skip-trees" not in sys.argv:
    out["snapshot37"] = verify_snapshot(m37)
    out["snapshot38"] = verify_snapshot(m38)

rows37 = {f["path"]: f["sha256"] for f in m37["files"]}
rows38 = {f["path"]: f["sha256"] for f in m38["files"]}
out["delta37to38"] = {"changed": sorted(p for p in rows37 if p in rows38 and rows37[p] != rows38[p]),
                      "added": sorted(set(rows38) - set(rows37)), "removed": sorted(set(rows37) - set(rows38))}

kit_bad, kit_vs37, kit_changed38 = [], [], []
kit_listed = set()
for f in kit["files"]:
    kit_listed.add(f["path"])
    p = os.path.join(KIT_ROOT, f["path"])
    if not os.path.isfile(p) or sha_file(p) != f["sha256"] or os.path.getsize(p) != f["bytes"]:
        kit_bad.append(f["path"])
    if rows37.get(f["path"]) != f["sha256"]:
        kit_vs37.append(f["path"])
    if rows38.get(f["path"]) != f["sha256"]:
        kit_changed38.append({"path": f["path"], "in38": f["path"] in rows38, "sha38": rows38.get(f["path"])})
kit_extra = []
for d, _, fs in os.walk(KIT_ROOT):
    for fn in fs:
        rel = os.path.relpath(os.path.join(d, fn), KIT_ROOT)
        if rel != "consumer-input-manifest.json" and rel not in kit_listed:
            kit_extra.append(rel)
out["kit"] = {"members": len(kit["files"]), "memberFailures": kit_bad, "unlisted": sorted(kit_extra),
              "membersNotEqualToSource37": kit_vs37, "membersChangedOrAbsentInSource38": kit_changed38,
              "parentSubjectSha256": kit.get("parentSubjectSha256")}
print(json.dumps(out, indent=1))
