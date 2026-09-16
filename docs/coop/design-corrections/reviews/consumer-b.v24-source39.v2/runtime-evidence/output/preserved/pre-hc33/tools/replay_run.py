"""Fresh-process complete Run closure + semantic replay of an exported store.
Usage: python3 tools/runref.py tools/replay_run.py runs/<variant>.store.json runs/<variant>.replay.json
Reads only the exported store file and the kit (via ref/schemas.py)."""
import hashlib
import json
import os
import sys
import time

OUT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source39.v2/output/preserved/pre-hc33"
sys.path.insert(0, OUT + "/ref")

import closure  # noqa: E402
from store import Store  # noqa: E402


def main(src, dst):
    raw = open(src, "rb").read()
    exported = json.loads(raw)
    store = Store.load(exported)
    t0 = time.time()
    rep = closure.close_run(store, exported["runId"])
    rep["receipt"] = {"storeFile": src, "storeFileSha256": hashlib.sha256(raw).hexdigest(), "pid": os.getpid(),
                      "freshProcess": True, "seconds": round(time.time() - t0, 3), "modulesLoadedFrom": closure.__file__}
    with open(dst, "w") as fh:
        json.dump(rep, fh, indent=1, sort_keys=True)
    print(rep["result"], "graphFaults", rep["graphAdmission"]["faults"][:12])
    if rep["semanticReplay"].get("performed"):
        print("replayFaults", rep["semanticReplay"]["faults"][:12])
        print("recomputed", json.dumps({k: rep["semanticReplay"]["recomputed"][k] for k in ("verdict", "ruleOutcomes", "executionDeficiencies")}))
    return 0 if rep["result"] == "ADMIT" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
