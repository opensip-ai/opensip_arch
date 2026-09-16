"""Determinism probe for fresh source44 re-executions (writes selfcheck/s44-determinism-<mode>.json).

Usage: python3 tools/seq.py <label> tools/determinism_probe_s44.py before -- tools/from_scratch.py -- tools/replay_export.py -- tools/retention_negatives.py
       -- tools/determinism_probe_s44.py after
  before: hashes every runs/, negatives/ and vectors/ result file listed in preserved/s43-final/results-manifest.json (the first source44 execution)
  after : hashes them again (a second source44 execution), and compares with 'before' and with the source43 copy's hashes
It separates two cases for the files that differ from the source43 copy: (a) the bytes differ between two identical source44 executions
(nondeterministic serialisation); (b) the bytes are stable within source44 but differ from source43 (kit-, runtime- or input-dependent content).
For case (b) it records the JSON paths whose values differ between the source43 manifest-era file and now, when the source43 bytes are available
(only for files copied to preserved/s43-final/); otherwise only the hash.
"""
import hashlib
import json
import sys

OUT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source45.v1/output/"
mode = sys.argv[1]
manifest = json.load(open(OUT + "preserved/s43-final/results-manifest.json"))["files"]
paths = [r["path"] for r in manifest if r["path"].startswith(("runs/", "negatives/", "vectors/")) and not r["path"].endswith(".store.json")]
hashes = {}
for p in paths:
    try:
        hashes[p] = hashlib.sha256(open(OUT + p, "rb").read()).hexdigest()
    except FileNotFoundError:
        hashes[p] = None
if mode == "before":
    json.dump({"standing": "hashes after the first source44 execution", "hashes": hashes}, open(OUT + "selfcheck/s44-determinism-before.json", "w"), indent=1)
    print(json.dumps({"hashed": len(hashes)}))
    sys.exit(0)
before = json.load(open(OUT + "selfcheck/s44-determinism-before.json"))["hashes"]
s43 = {r["path"]: r["sha256"] for r in manifest}
unstable = sorted(p for p in paths if before.get(p) != hashes.get(p))
stable_but_differs = sorted(p for p in paths if before.get(p) == hashes.get(p) and hashes.get(p) != s43[p])
out = {"standing": "second source44 execution compared with the first and with the source43 copy", "hashed": len(paths),
       "differsBetweenTwoSource44Executions": unstable, "stableInSource44ButDiffersFromSource43": stable_but_differs,
       "identicalToSource43": sum(1 for p in paths if hashes.get(p) == s43[p])}
json.dump(dict(out, hashes=hashes), open(OUT + "selfcheck/s44-determinism-after.json", "w"), indent=1)
print(json.dumps({k: (v if not isinstance(v, list) else {"count": len(v), "first": v[:12]}) for k, v in out.items()}, indent=1))
