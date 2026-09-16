"""source43.v1 setup: before fresh source43 re-execution of the per-positive closure/replay chain overwrites them, record the sha256 of every
source42.v3 copied result under output/runs/ and output/selfcheck/ (stores, replays, summaries, records) in output/preserved/s42-v3-final/runs-manifest.json.
Stores are inputs and are not rewritten by the chain; the manifest lets later steps prove the exported stores are byte-identical to source42.v3.
The complete source42.v3 bytes remain in the preserved source42.v3 runtime. Refuses to run twice.
Usage: python3 output/preserve_s42v3_runs_manifest.py
"""
import hashlib
import json
import os
import sys

OUT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source43.v1/output/"
DEST = OUT + "preserved/s42-v3-final/runs-manifest.json"


def main():
    if os.path.exists(DEST):
        print("already recorded; refusing to run twice")
        return 1
    rows = []
    for sub in ("runs", "selfcheck", "negatives"):
        for name in sorted(os.listdir(OUT + sub)):
            p = f"{OUT}{sub}/{name}"
            if os.path.isfile(p):
                b = open(p, "rb").read()
                rows.append({"path": f"{sub}/{name}", "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)})
    with open(DEST, "w") as fh:
        json.dump({"standing": "sha256 of source42.v3 copied results before any source43 execution", "files": rows}, fh, indent=1)
    print(json.dumps({"recorded": len(rows), "stores": sum(1 for r in rows if r["path"].endswith(".store.json"))}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
