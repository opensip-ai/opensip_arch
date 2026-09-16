"""From-scratch recompute of every claimed complete positive Run (R-FROM-SCRATCH-COMMAND).

For each runs/<name>.store.json whose name has no mutation marker, spawn a fresh reference interpreter process
(/tmp/opensip-architecture-review-env/bin/python -I -B tools/replay_run.py) that loads only the exported store and the kit, recomputes
every identity, runs complete graph admission and the independent semantic replay, and writes runs/<name>.replay.fromscratch.json.
Usage (either):
  python3 tools/from_scratch.py
  /tmp/opensip-architecture-review-env/bin/python -I -B tools/from_scratch.py
"""
import glob
import json
import os
import subprocess
import sys

OUT = "/private/tmp/opensip-design-corrections/consumer-b.v24/output"
REF = ["/tmp/opensip-architecture-review-env/bin/python", "-I", "-B"]


def main():
    rows = []
    for store in sorted(glob.glob(f"{OUT}/runs/*.store.json")):
        name = os.path.basename(store)[:-len(".store.json")]
        if "~" in name or "." in name:
            continue
        dst = f"{OUT}/runs/{name}.replay.fromscratch.json"
        p = subprocess.run(REF + [f"{OUT}/tools/replay_run.py", store, dst], capture_output=True, text=True)
        rep = json.load(open(dst)) if os.path.exists(dst) else {}
        original = json.load(open(f"{OUT}/runs/{name}.replay.json"))["result"] if os.path.exists(f"{OUT}/runs/{name}.replay.json") else None
        rows.append({"run": name, "exit": p.returncode, "result": rep.get("result"), "originalResult": original,
                     "role": "claimed-positive" if original == "ADMIT" else "designed-negative",
                     "graphFaults": rep.get("graphAdmission", {}).get("faults", [])[:3],
                     "replayFaults": rep.get("semanticReplay", {}).get("faults"), "pid": rep.get("receipt", {}).get("pid")})
    positives = [r for r in rows if r["role"] == "claimed-positive"]
    agree = all(r["result"] == r["originalResult"] for r in rows)
    with open(f"{OUT}/runs/from-scratch.summary.json", "w") as fh:
        json.dump({"command": " ".join(REF + ["tools/from_scratch.py"]), "runs": rows, "claimedPositives": len(positives),
                   "allClaimedPositivesAdmitted": all(r["result"] == "ADMIT" for r in positives), "everyResultMatchesOriginal": agree}, fh, indent=1, sort_keys=True)
    for r in rows:
        print(r["run"], r["role"], r["result"], r["graphFaults"], r["replayFaults"])
    return 0 if agree and all(r["result"] == "ADMIT" for r in positives) else 1


if __name__ == "__main__":
    sys.exit(main())
