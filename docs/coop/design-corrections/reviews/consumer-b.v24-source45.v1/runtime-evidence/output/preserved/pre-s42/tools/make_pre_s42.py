"""Materialise the UNCHANGED helper state of this runtime at output/preserved/pre-s42/.

Source: preserved/s42-original-state, the exact output tree after the ported source41.v1 helpers ran unchanged against the source42 kit
(logs s42-original.*, s42-original-mut.*, s42-original-disc.*) and before any source42 correction, including the stores those helpers
built. Only the live output root inside *.py files is rebound to preserved/pre-s42 (the kit path is untouched), so the rest of the
original chain and the new source42 closure controls can be executed under the unchanged helpers. Every copied file is checked against
preserved/s42-original-state/manifest.json, and every ported *.py against its port-manifest portedSha256. Refuses to overwrite.
Usage: python3 tools/make_pre_s42.py
"""
import hashlib
import json
import os
import sys

S42 = "/private/tmp/opensip-design-corrections/consumer-b.v24-source45.v1"
OUT = S42 + "/output"
SRC = OUT + "/preserved/s42-original-state"
DST = OUT + "/preserved/pre-s42"


def main():
    if os.path.exists(DST + "/manifest.json"):
        print("exists; refusing to overwrite")
        return 1
    ported = {f["file"]: f["portedSha256"] for f in json.load(open(OUT + "/port-manifest.json"))["files"]}
    rows, py_checked = [], 0
    for r in json.load(open(SRC + "/manifest.json"))["files"]:
        raw = open(f"{SRC}/{r['path']}", "rb").read()
        if hashlib.sha256(raw).hexdigest() != r["sha256"]:
            raise SystemExit(f"preserved copy differs from its manifest: {r['path']}")
        if r["path"] in ported:
            if ported[r["path"]] != r["sha256"]:
                raise SystemExit(f"unchanged-state helper differs from the port manifest: {r['path']}")
            py_checked += 1
        data, rebound = raw, 0
        if r["path"].endswith(".py"):
            text = raw.decode("utf-8")
            rebound = text.count(OUT)
            data = text.replace(OUT, DST).encode("utf-8")
        target = f"{DST}/{r['path']}"
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "wb") as fh:
            fh.write(data)
        rows.append({"path": r["path"], "sourceSha256": r["sha256"], "writtenSha256": hashlib.sha256(data).hexdigest(), "rebound": rebound})
    with open(DST + "/manifest.json", "w") as fh:
        json.dump({"standing": "unchanged ported helper state (source41.v1 code as run against the source42 kit before any source42 correction), "
                               "rebound to this directory for execution; not current conformance",
                   "source": SRC, "portManifestCheckedFiles": py_checked, "files": rows}, fh, indent=1)
    print(json.dumps({"files": len(rows), "portManifestCheckedFiles": py_checked, "reboundFiles": sum(1 for r in rows if r["rebound"])}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
