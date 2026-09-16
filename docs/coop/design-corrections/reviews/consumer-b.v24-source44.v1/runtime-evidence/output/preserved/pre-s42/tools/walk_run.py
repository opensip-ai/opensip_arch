"""Fresh-process independent retained-closure walk of one exported store (no owner admission, no replay).
Usage: /tmp/opensip-architecture-review-env/bin/python -I -B tools/walk_run.py runs/<name>.store.json <dst.json>"""
import hashlib
import json
import os
import sys
import time

OUT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source44.v1/output/preserved/pre-s42"
sys.path.insert(0, OUT + "/ref")

import retained_graph as RG  # noqa: E402


def main(src, dst):
    raw = open(src, "rb").read()
    t0 = time.time()
    rep = RG.close_retained_graph(json.loads(raw))
    rep["receipt"] = {"storeFile": os.path.relpath(src, OUT), "storeFileSha256": hashlib.sha256(raw).hexdigest(), "pid": os.getpid(),
                      "seconds": round(time.time() - t0, 3), "walker": os.path.relpath(RG.__file__, OUT),
                      "walkerSha256": hashlib.sha256(open(RG.__file__, "rb").read()).hexdigest()}
    with open(dst, "w") as fh:
        json.dump(rep, fh, indent=1, sort_keys=True)
    print(rep["result"], json.dumps(rep["firstRefusal"])[:300])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
