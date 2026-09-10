import hashlib, json, os, sys
root = sys.argv[1]
out = {}
for dp, dn, fn in os.walk(root):
    for f in fn:
        full = os.path.join(dp, f)
        rel = os.path.relpath(full, root)
        out[rel] = hashlib.sha256(open(full, "rb").read()).hexdigest()
json.dump(out, open(sys.argv[2], "w"))
print(len(out), "files ->", sys.argv[2])
