"""source41.v1 setup: preserve own history (read-only), then port own helper code from source39.v3.

1. Hash manifest of EVERY file of the completed source39.v3 output tree (read-only) and a copy of every non-store file
   (reports, logs, checkpoints, notes, helper code, review) into output/preserved/source39-v3/, so source39 failures and final
   claims stay available here. *.store.json files are covered by the manifest hashes only (exact bytes remain in that runtime).
2. Hash-only manifest of the original consumer-b.v24 output tree.
3. Port every *.py of source39.v3 output/{ref,builders,tools,vectors} into this runtime, rebinding only the source39.v3 runtime root
   to this runtime root (output/port-manifest.json). tools/v3_preserve_and_rebind.py is runtime-specific history and is not ported.
No Run store is seeded: every current-source claim is rebuilt and re-executed against the source41 kit.
Refuses to run twice.  Usage: python3 output/port_and_preserve.py
"""
import hashlib
import json
import os
import shutil
import sys

V3 = "/private/tmp/opensip-design-corrections/consumer-b.v24-source39.v3"
V3_ALT = "/tmp/opensip-design-corrections/consumer-b.v24-source39.v3"
V24 = "/tmp/opensip-design-corrections/consumer-b.v24"
S41 = "/private/tmp/opensip-design-corrections/consumer-b.v24-source41.v1"
OUT = S41 + "/output"
EXCLUDE = {"tools/v3_preserve_and_rebind.py"}


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def tree(root):
    rows = []
    for d, _, fs in sorted(os.walk(root)):
        for f in sorted(fs):
            p = os.path.join(d, f)
            rows.append({"path": os.path.relpath(p, root), "bytes": os.path.getsize(p), "sha256": sha(p)})
    return rows


def main():
    if os.path.exists(OUT + "/port-manifest.json"):
        print("already ported; refusing to run twice")
        return 1
    dst = OUT + "/preserved/source39-v3"
    os.makedirs(dst, exist_ok=True)
    v3_rows = tree(V3 + "/output")
    copied = 0
    for r in v3_rows:
        if r["path"].endswith(".store.json"):
            continue
        t = f"{dst}/{r['path']}"
        os.makedirs(os.path.dirname(t), exist_ok=True)
        shutil.copyfile(f"{V3}/output/{r['path']}", t)
        if sha(t) != r["sha256"]:
            raise SystemExit(f"copy mismatch {r['path']}")
        copied += 1
    json.dump({"standing": "completed source39.v3 output of origin 9d3dfb70-b2d3-498c-a3c1-f8de9e488514 (verdict CHANGES_REQUIRED on the source39 kit); "
                           "read-only own history, not current-source conformance. Non-store files copied here; stores hashed only.",
               "source": V3 + "/output", "files": v3_rows, "copiedNonStoreFiles": copied},
              open(dst + "/manifest.json", "w"), indent=1)
    v24_rows = tree(V24 + "/output")
    json.dump({"standing": "hash-only manifest of the original consumer-b.v24 output (own history)", "source": V24 + "/output", "files": v24_rows},
              open(OUT + "/preserved/consumer-b.v24-output.manifest.json", "w"), indent=1)
    ported = []
    for sub in ("ref", "builders", "tools", "vectors"):
        for name in sorted(os.listdir(f"{V3}/output/{sub}")):
            rel = f"{sub}/{name}"
            if not name.endswith(".py") or rel in EXCLUDE:
                continue
            raw = open(f"{V3}/output/{rel}", "rb").read()
            text = raw.decode("utf-8")
            n = text.count(V3) + text.count(V3_ALT)
            new = text.replace(V3, S41).replace(V3_ALT, S41)
            os.makedirs(f"{OUT}/{sub}", exist_ok=True)
            open(f"{OUT}/{rel}", "w").write(new)
            ported.append({"file": rel, "sourceSha256": hashlib.sha256(raw).hexdigest(), "portedSha256": hashlib.sha256(new.encode()).hexdigest(),
                           "rebound": n})
    json.dump({"standing": "own source39.v3 helper code rebound to source41.v1 by root path only; it is a starting point to be checked against the "
                           "source41 kit, and any later change is a numbered helper correction with the original failure preserved",
               "files": ported, "excluded": sorted(EXCLUDE)}, open(OUT + "/port-manifest.json", "w"), indent=1)
    print(json.dumps({"v3Files": len(v3_rows), "copiedNonStore": copied, "v24Files": len(v24_rows), "ported": len(ported)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
