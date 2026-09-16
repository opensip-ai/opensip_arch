"""Materialise the PRE-correction closure code (ported source39.v1 ref/*.py and tools/replay_run.py, unchanged except path rebinding) at
output/preserved/pre-hc33/ so constructed negatives and rebuilt stores can be closed under both the pre and the post helper code.

Source bytes come from preserved/source39-v1/{ref,tools} and must equal the port-manifest sourceSha256 rows. Rebinding: the v1 output root
becomes preserved/pre-hc33 (so the copy imports its own ref/), and the v1 runtime root becomes this runtime root (kit path). Refuses to overwrite.
Usage: python3 tools/make_pre_hc33.py
"""
import hashlib
import json
import os
import sys

V2 = "/private/tmp/opensip-design-corrections/consumer-b.v24-source39.v2"
V1 = "/private/tmp/opensip-design-corrections/consumer-b.v24-source39.v1"
OUT = V2 + "/output"
DST = OUT + "/preserved/pre-hc33"


def main():
    if os.path.exists(DST + "/manifest.json"):
        print("exists; refusing to overwrite")
        return 1
    port = {f["source"]: f["sourceSha256"] for f in json.load(open(OUT + "/port-manifest.json"))["files"]}
    rows = []
    wanted = [("ref", n) for n in sorted(os.listdir(OUT + "/preserved/source39-v1/ref")) if n.endswith(".py")] + [("tools", "replay_run.py")]
    for sub, name in wanted:
        src = f"{OUT}/preserved/source39-v1/{sub}/{name}"
        raw = open(src, "rb").read()
        sha = hashlib.sha256(raw).hexdigest()
        if port.get(f"{V1}/output/{sub}/{name}") != sha:
            raise SystemExit(f"preserved source differs from port manifest: {sub}/{name}")
        text = raw.decode("utf-8").replace(V1 + "/output", DST).replace(V1 + "/", V2 + "/")
        os.makedirs(f"{DST}/{sub}", exist_ok=True)
        open(f"{DST}/{sub}/{name}", "w").write(text)
        rows.append({"file": f"{sub}/{name}", "sourceSha256": sha, "writtenSha256": hashlib.sha256(text.encode()).hexdigest()})
    json.dump({"standing": "pre-HC-33/34/35 closure, evaluator and replay code (source39.v1 ported helpers, unchanged except path rebinding)",
               "files": rows}, open(DST + "/manifest.json", "w"), indent=1)
    print(json.dumps({"files": len(rows)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
