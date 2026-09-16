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

OUT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source44.v1/output/preserved/pre-s42"
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
        # HC-24: the role is the Run's declared purpose, never inferred from an earlier replay outcome. The original labelled every
        # refused positive a designed negative (logs/s39-original-closure.0.from_scratch.log).
        role = "designed-negative" if name in ("syntax-mixed-falsecomplete",) else "claimed-positive"
        rows.append({"run": name, "exit": p.returncode, "result": rep.get("result"), "originalResult": original, "role": role,
                     "firstRefusal": rep.get("firstRefusal"),
                     "retainedClosure": {k: rep.get("retainedClosure", {}).get(k) for k in ("result", "firstRefusal", "requiredPreimages", "retainedPreimages")},
                     "reachableOutputSet": rep.get("semanticReplay", {}).get("reachableOutputSet"),
                     "graphFaults": rep.get("graphAdmission", {}).get("faults", [])[:3],
                     "replayFaults": rep.get("semanticReplay", {}).get("faults"), "pid": rep.get("receipt", {}).get("pid")})
    positives = [r for r in rows if r["role"] == "claimed-positive"]
    negatives = [r for r in rows if r["role"] == "designed-negative"]
    agree = all(r["originalResult"] is None or r["result"] == r["originalResult"] for r in rows)
    positives_ok = all(r["result"] == "ADMIT" for r in positives)
    negatives_ok = all(r["result"] == "REFUSE" for r in negatives)
    with open(f"{OUT}/runs/from-scratch.summary.json", "w") as fh:
        json.dump({"command": " ".join(REF + ["tools/from_scratch.py"]), "runs": rows, "claimedPositives": len(positives),
                   "allClaimedPositivesAdmitted": positives_ok, "allDesignedNegativesRefused": negatives_ok,
                   "everyResultMatchesOriginal": agree}, fh, indent=1, sort_keys=True)
    for r in rows:
        print(r["run"], r["role"], r["result"], r["firstRefusal"], r["replayFaults"])
    return 0 if agree and positives_ok and negatives_ok else 1


if __name__ == "__main__":
    sys.exit(main())
