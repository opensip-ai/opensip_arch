"""Source39.v2 self-audit setup: preserve own history, then port own helper code.

1. Copies the complete source39.v1 output tree byte-exact into output/preserved/source39-v1/ and writes a SHA-256 manifest of every file
   (source path, destination path, bytes, sha256). The v1 runtime itself is never written.
2. Writes a SHA-256 manifest (hash only, no copy) of the original consumer-b.v24 output tree, recording its immutable state.
3. Ports every *.py under v1 output/{ref,builders,tools,vectors} into this runtime, rebinding only the v1 runtime root to the v2 root
   (output/port-manifest.json). The original consumer-b.v24 base path is not rebound.
4. Seeds output/runs/ with v1's exported Run stores (*.store.json), byte-exact, as the starting bytes for the self-check.
Refuses to overwrite an existing preserved copy.
Usage: python3 output/port_and_preserve.py
"""
import hashlib
import json
import os
import shutil
import sys

V1 = "/private/tmp/opensip-design-corrections/consumer-b.v24-source39.v1"
V1_ALT = "/tmp/opensip-design-corrections/consumer-b.v24-source39.v1"
V24 = "/tmp/opensip-design-corrections/consumer-b.v24"
V2 = "/private/tmp/opensip-design-corrections/consumer-b.v24-source39.v2"
OUT = V2 + "/output"


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def tree_rows(root):
    rows = []
    for d, _, fs in sorted(os.walk(root)):
        for x in sorted(fs):
            p = os.path.join(d, x)
            rows.append({"path": os.path.relpath(p, root), "bytes": os.path.getsize(p), "sha256": sha(p)})
    return rows


def main():
    dst = OUT + "/preserved/source39-v1"
    if os.path.exists(dst + "/manifest.json"):
        print("preserved copy exists; refusing to overwrite")
        return 1
    os.makedirs(dst, exist_ok=True)
    v1_rows = tree_rows(V1 + "/output")
    for r in v1_rows:
        s, t = f"{V1}/output/{r['path']}", f"{dst}/{r['path']}"
        os.makedirs(os.path.dirname(t), exist_ok=True)
        shutil.copyfile(s, t)
        if sha(t) != r["sha256"]:
            raise SystemExit(f"copy mismatch {r['path']}")
    json.dump({"standing": "byte-exact copy of the completed source39.v1 output tree (own history of origin 9d3dfb70-b2d3-498c-a3c1-f8de9e488514); "
                           "immutable; not current evidence until re-checked in this runtime",
               "source": V1 + "/output", "files": v1_rows}, open(dst + "/manifest.json", "w"), indent=1)
    v24_rows = tree_rows(V24 + "/output")
    json.dump({"standing": "hash-only manifest of the original consumer-b.v24 output tree (own history); not copied, not current evidence",
               "source": V24 + "/output", "files": v24_rows}, open(OUT + "/preserved/consumer-b.v24-output.manifest.json", "w"), indent=1)
    ported = []
    for sub in ("ref", "builders", "tools", "vectors"):
        src_dir = f"{V1}/output/{sub}"
        for name in sorted(os.listdir(src_dir)):
            if not name.endswith(".py"):
                continue
            raw = open(os.path.join(src_dir, name), "rb").read()
            text = raw.decode("utf-8")
            new = text.replace(V1 + "/", V2 + "/").replace(V1_ALT + "/", V2 + "/").replace(f'"{V1}"', f'"{V2}"').replace(f"'{V1}'", f"'{V2}'")
            os.makedirs(f"{OUT}/{sub}", exist_ok=True)
            open(f"{OUT}/{sub}/{name}", "w").write(new)
            ported.append({"source": f"{V1}/output/{sub}/{name}", "sourceSha256": hashlib.sha256(raw).hexdigest(),
                           "destination": f"output/{sub}/{name}", "destinationSha256": hashlib.sha256(new.encode()).hexdigest(),
                           "rebound": text.count(V1) + text.count(V1_ALT)})
    json.dump({"standing": "own source39.v1 helper code rebound to source39.v2 by path only; any later change is a numbered helper correction",
               "files": ported}, open(OUT + "/port-manifest.json", "w"), indent=1)
    os.makedirs(OUT + "/runs", exist_ok=True)
    seeded = []
    for name in sorted(os.listdir(V1 + "/output/runs")):
        if name.endswith(".store.json"):
            shutil.copyfile(f"{V1}/output/runs/{name}", f"{OUT}/runs/{name}")
            seeded.append({"store": name, "sha256": sha(f"{OUT}/runs/{name}")})
    json.dump({"standing": "v1 exported stores seeded byte-exact for the v2 self-check", "stores": seeded},
              open(OUT + "/runs/seeded-from-v1.json", "w"), indent=1)
    print(json.dumps({"v1Files": len(v1_rows), "v24Files": len(v24_rows), "ported": len(ported), "seededStores": len(seeded)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
