"""End-to-end: do laws 6 and 9 actually refuse, or only describe?

Mutates the native fixture's declared schemaDigests and reruns the owning checkers.
Includes an unmutated CONTROL; without a passing control no detection claim stands.

  stale-digest      : fixture names the pre-final route digest (law 9 drift guard)
  arbitrary-bytes   : fixture names a retained-but-unregistered digest (law 6)
  empty-set         : fixture declares no schema documents (must stay LEGAL)
  registered-extra  : fixture names an extra registered document (must stay LEGAL)
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys

SRC, WORK = sys.argv[1], sys.argv[2]
PY = "/tmp/opensip-architecture-review-env/bin/python"
CASES = "docs/coop/design-corrections/native/native-cases.v2.json"
NATIVE_CHECK = "docs/coop/design-corrections/native/check_native_evidence.v2.py"
ID_CHECK = "docs/coop/design-corrections/foundation/check-identity.py"
STALE = "82745fa9ec4b9cef0eb0f7653f975ea01fb0302d267d23404dd8236dc911d6c1"
ARBITRARY = hashlib.sha256(b"retained but unregistered").hexdigest()


def clone(root):
    shutil.copytree(
        os.path.join(SRC, "docs"), os.path.join(root, "docs"), symlinks=True,
        ignore=lambda d, n: {"reviews"} if os.path.basename(d) ==
        "design-corrections" else set())
    # the native checker pins this one file under the excluded reviews/ tree
    need = "docs/coop/design-corrections/reviews/native-author-feedback.v1.md"
    dst = os.path.join(root, need)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(os.path.join(SRC, need), dst)


def set_digests(root, fn):
    p = os.path.join(root, CASES)
    doc = json.load(open(p))

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k == "schemaDigests" and isinstance(v, list):
                    o[k] = fn(v)
                else:
                    walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(doc)
    json.dump(doc, open(p, "w"), indent=1)


def registered_extra(root):
    """another genuinely registered document digest"""
    d = os.path.join(root, "docs/coop/design-corrections")
    other = hashlib.sha256(open(os.path.join(
        d, "foundation/identity-schemas.v2.json"), "rb").read()).hexdigest()
    return lambda v: sorted(set(v) | {other})


MUTATIONS = [
    ("CONTROL-unmutated", None, None),
    ("law9-stale-route-digest", lambda root: set_digests(
        root, lambda v: [STALE]), "refuse"),
    ("law6-arbitrary-unregistered-bytes", lambda root: set_digests(
        root, lambda v: [ARBITRARY]), "refuse"),
    ("law6-empty-declaration-stays-legal", lambda root: set_digests(
        root, lambda v: []), "allow"),
    ("law6-registered-extra-stays-legal", lambda root: set_digests(
        root, registered_extra(root)), "allow"),
]

results = []
control = None
for name, fn, expect in MUTATIONS:
    root = os.path.join(WORK, name)
    shutil.rmtree(root, ignore_errors=True)
    os.makedirs(root)
    clone(root)
    if fn:
        fn(root)
    runs = {}
    for label, script in (("native", NATIVE_CHECK), ("identity", ID_CHECK)):
        args = [PY, "-I", "-B", os.path.join(root, script)]
        if label == "identity":
            args += ["--report", os.path.join(root, "r.json")]
        pr = subprocess.run(args, capture_output=True, text=True, timeout=1800)
        o = pr.stdout + pr.stderr
        runs[label] = {
            "exit": pr.returncode,
            "envError": "FileNotFoundError" in o or "ModuleNotFoundError" in o,
            "tail": o.strip().splitlines()[-3:],
        }
    refused = any(r["exit"] != 0 and not r["envError"] for r in runs.values())
    rec = {"case": name, "expect": expect, "refused": refused, "runs": runs}
    if expect:
        rec["asExpected"] = (refused if expect == "refuse" else not refused)
    else:
        control = all(r["exit"] == 0 and not r["envError"] for r in runs.values())
    results.append(rec)
    print(f"{name}: expect={expect} refused={refused} "
          f"ok={rec.get('asExpected')}", flush=True)
    shutil.rmtree(root, ignore_errors=True)

json.dump({"controlPassed": control, "results": results,
           "allAsExpected": bool(control) and all(
               r.get("asExpected") for r in results if r["expect"])},
          open(os.path.join(WORK, "law6-law9-mutations.json"), "w"), indent=2)
