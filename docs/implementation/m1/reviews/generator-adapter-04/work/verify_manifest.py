import hashlib, json, os, sys
MAN = "/tmp/opensip-implementation/m1-generator-adapter-subject-04.json"
EXPECT = "d25b7713ca29296df964497a75c6bef205edf5f08ac13f6b533dc99fd02d3f2f"
raw = open(MAN, "rb").read()
got = hashlib.sha256(raw).hexdigest()
m = json.loads(raw)
root = sys.argv[1] if len(sys.argv) > 1 else m["root"]
errs = []
if got != EXPECT: errs.append(f"manifest sha {got}")
listed = {f["path"]: f for f in m["files"]}
actual = set(); nonreg = []
for dp, dns, fns in os.walk(root, followlinks=False):
    for n in dns + fns:
        p = os.path.join(dp, n); st = os.lstat(p)
        rel = os.path.relpath(p, root)
        import stat
        if stat.S_ISDIR(st.st_mode): continue
        if not stat.S_ISREG(st.st_mode): nonreg.append(rel); continue
        if st.st_nlink != 1: errs.append(f"nlink {rel} {st.st_nlink}")
        actual.add(rel)
for rel in sorted(actual ^ set(listed)): errs.append(f"set-diff {rel}")
for rel in sorted(actual & set(listed)):
    b = open(os.path.join(root, rel), "rb").read()
    if hashlib.sha256(b).hexdigest() != listed[rel]["sha256"] or len(b) != listed[rel]["bytes"]:
        errs.append(f"hash {rel}")
errs += [f"nonregular {r}" for r in nonreg]
print(json.dumps({"manifestSha256": got, "root": root, "listed": len(listed), "actual": len(actual), "errors": errs}, indent=1))
sys.exit(1 if errs else 0)
