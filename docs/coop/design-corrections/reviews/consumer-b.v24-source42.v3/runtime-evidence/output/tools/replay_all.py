"""Build every declared input-mutation variant, then close and replay EVERY exported Run store in a fresh reference-interpreter
process, writing runs/<name>.replay.json (claimed positives, designed negatives and mutations; attempt copies containing '.' are
skipped) and runs/replay-all.summary.json.

The mutation lists are the builders' own MUTATIONS sets over their base variants (ts-pass, rust-mixed, syntax-code). A builder that
refuses its own mutated inputs before exporting a store is recorded as a build refusal, not hidden.
Usage: python3 tools/seq.py <label> tools/replay_all.py [--no-build]
"""
import glob
import json
import os
import subprocess
import sys

OUT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source42.v3/output"
REF = ["/tmp/opensip-architecture-review-env/bin/python", "-I", "-B"]
sys.path.insert(0, OUT + "/ref")
sys.path.insert(0, OUT + "/builders")
BASES = (("ts_runs", "ts-pass"), ("rust_runs", "rust-mixed"), ("syntax_runs", "syntax-code"))
# HC-27 (own tool error in the first version, logs/s39-replay-all.0.replay_all.log): a designed-negative mutation is built over the
# variant whose inputs it mutates; over rust-mixed these two mutations changed nothing and the Runs admitted.
MUTATION_BASE = {"ambiguous-fact-present": "rust-ambiguous", "partial-fact-present": "rust-partial"}


def main():
    summary = {"builds": [], "replays": []}
    if "--no-build" not in sys.argv:
        for module, base in BASES:
            mutations = sorted(__import__(module).MUTATIONS)
            for mut in mutations:
                variant = f"{MUTATION_BASE.get(mut, base)}~{mut}"
                p = subprocess.run(REF + [f"{OUT}/builders/{module}.py", variant], capture_output=True, text=True)
                summary["builds"].append({"variant": variant, "exit": p.returncode,
                                          "stored": os.path.exists(f"{OUT}/runs/{variant}.store.json"), "tail": (p.stdout + p.stderr)[-800:]})
    for store in sorted(glob.glob(f"{OUT}/runs/*.store.json")):
        name = os.path.basename(store)[:-len(".store.json")]
        if "." in name:
            continue
        dst = f"{OUT}/runs/{name}.replay.json"
        if os.path.exists(dst):
            os.remove(dst)
        p = subprocess.run(REF + [f"{OUT}/tools/replay_run.py", store, dst], capture_output=True, text=True)
        rep = json.load(open(dst)) if os.path.exists(dst) else {}
        # HC-33: stage-ordered faults include the retained-closure stage
        faults = rep.get("faultsInStageOrder") or (rep.get("graphAdmission", {}).get("faults", []) + rep.get("semanticReplay", {}).get("faults", []))
        summary["replays"].append({"run": name, "exit": p.returncode, "result": rep.get("result"), "firstFault": faults[0] if faults else None,
                                   "firstRefusalStage": (rep.get("firstRefusal") or {}).get("stage"),
                                   "faultCount": len(faults), "stderrTail": p.stderr[-400:] if not rep else None})
    with open(f"{OUT}/runs/replay-all.summary.json", "w") as fh:
        json.dump(summary, fh, indent=1, sort_keys=True)
    for b in summary["builds"]:
        if b["exit"] or not b["stored"]:
            print("BUILD", b["variant"], b["exit"], b["tail"][-300:].replace("\n", " | "))
    for r in summary["replays"]:
        print(r["run"], r["result"], r["firstFault"])
    missing = [r["run"] for r in summary["replays"] if r["result"] is None]
    print("replays", len(summary["replays"]), "without-result", missing)
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
