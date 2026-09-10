import hashlib, json, os, sys

MAN = "/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v14.json"
EXPECT_MAN = "45b1e128ca51d114895f3c406cc92575e6efe95051bf319023dc1f3180c2f92c"

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

man_sha = sha(MAN)
d = json.load(open(MAN))
root = d["snapshotRoot"]

declared = {e["path"]: e for e in d["files"]}
assert len(declared) == len(d["files"]), "duplicate declared paths"

present = set()
nonregular = []
for dirpath, dirnames, filenames in os.walk(root):
    for fn in filenames:
        full = os.path.join(dirpath, fn)
        rel = os.path.relpath(full, root)
        if os.path.islink(full):
            nonregular.append(rel)
        present.add(rel)

missing = sorted(set(declared) - present)
undeclared = sorted(present - set(declared))
bad_hash, bad_len = [], []
total = 0
for rel, e in declared.items():
    full = os.path.join(root, rel)
    if rel in missing:
        continue
    n = os.path.getsize(full)
    total += n
    if n != e["bytes"]:
        bad_len.append((rel, e["bytes"], n))
    a = sha(full)
    if a != e["sha256"]:
        bad_hash.append((rel, e["sha256"], a))

out = {
    "manifestPath": MAN,
    "manifestSha256Actual": man_sha,
    "manifestSha256Expected": EXPECT_MAN,
    "manifestSha256Match": man_sha == EXPECT_MAN,
    "snapshotRoot": root,
    "declaredFileCount": d["fileCount"],
    "declaredEntries": len(declared),
    "presentFileCount": len(present),
    "declaredTotalBytes": d["totalBytes"],
    "measuredTotalBytes": total,
    "totalBytesMatch": total == d["totalBytes"],
    "missing": missing,
    "undeclared": undeclared,
    "symlinksOrNonRegular": nonregular,
    "hashMismatches": bad_hash,
    "lengthMismatches": bad_len,
    "clean": not (missing or undeclared or nonregular or bad_hash or bad_len)
              and man_sha == EXPECT_MAN and total == d["totalBytes"]
              and len(present) == d["fileCount"],
}
phase = sys.argv[1] if len(sys.argv) > 1 else "unknown"
out["phase"] = phase
p = "/tmp/opensip-design-corrections/post-reset-review.v14/evidence/custody-%s.json" % phase
json.dump(out, open(p, "w"), indent=2)
print(json.dumps({k: v for k, v in out.items() if k not in ()}, indent=2)[:2500])
