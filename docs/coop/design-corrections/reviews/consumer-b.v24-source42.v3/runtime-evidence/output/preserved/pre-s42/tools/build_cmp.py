"""Build and freshly replay the phase-8 comparison family, after proving the builder extension left ts-pass byte-identical.

The pre-extension ts-pass store/build files are preserved as runs/ts-pass.pre-builder-extension.*; the rebuilt store must have the
same SHA-256. Every cmp-* Run is then closed and replayed in a separate process (tools/replay_run.py).
Usage: python3 tools/build_cmp.py
"""
import hashlib
import json
import shutil
import subprocess
import sys

OUT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source42.v3/output/preserved/pre-s42"
RUNREF = [sys.executable, OUT + "/tools/runref.py"]
FAMILY = ["cmp-base", "cmp-code", "cmp-hidden", "cmp-scope", "cmp-policy", "cmp-waiver", "cmp-evidence", "cmp-gbase", "cmp-gevidence",
          "cmp-gmissing", "cmp-empty", "cmp-code-det2", "cmp-code-detc", "cmp-budget"]


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def run(args):
    p = subprocess.run(RUNREF + args, capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr)[-3000:]


def main():
    summary = {"regression": {}, "family": {}}
    pre = f"{OUT}/runs/ts-pass.store.json"
    before = sha(pre)
    shutil.copyfile(pre, f"{OUT}/runs/ts-pass.pre-builder-extension.store.json")
    shutil.copyfile(f"{OUT}/runs/ts-pass.build.json", f"{OUT}/runs/ts-pass.pre-builder-extension.build.json")
    code, log = run([OUT + "/builders/ts_runs.py", "ts-pass"])
    after = sha(pre)
    summary["regression"] = {"variant": "ts-pass", "before": before, "after": after, "identical": before == after, "exit": code, "log": log[-400:]}
    for v in FAMILY:
        bcode, blog = run([OUT + "/builders/ts_runs.py", v])
        row = {"buildExit": bcode, "buildLog": blog[-1500:]}
        if bcode == 0:
            rcode, rlog = run([OUT + "/tools/replay_run.py", f"{OUT}/runs/{v}.store.json", f"{OUT}/runs/{v}.replay.json"])
            b = json.load(open(f"{OUT}/runs/{v}.build.json"))
            row.update({"replayExit": rcode, "replayLog": rlog[-1500:], "runId": b["runId"], "verdict": b["verdict"], "findings": b["findings"],
                        "ruleOutcomes": b["ruleOutcomes"], "builderFaults": b["builderFaults"]})
        summary["family"][v] = row
    with open(f"{OUT}/runs/cmp-family.summary.json", "w") as fh:
        json.dump(summary, fh, indent=1, sort_keys=True)
    print(json.dumps({"regressionIdentical": summary["regression"]["identical"],
                      "family": {v: (r["buildExit"], r.get("replayExit"), r.get("verdict")) for v, r in summary["family"].items()}}, indent=1))
    bad = [v for v, r in summary["family"].items() if r["buildExit"] or r.get("replayExit")]
    return 1 if bad or not summary["regression"]["identical"] else 0


if __name__ == "__main__":
    sys.exit(main())
