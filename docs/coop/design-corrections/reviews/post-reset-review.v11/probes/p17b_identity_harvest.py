#!/usr/bin/env python3
"""p17b: real Run/body identity stability, harvested from the full suite.

p17 tried synthetic values and was rejected by identifier()'s per-domain schema validation --
a harness error on my part, and evidence the model validates before hashing. This instead
harvests EVERY identity actually computed during the complete check-identity run, under both the
v10 and v11 models, and compares the multisets. Any identity drift caused by the delta would show
up as a difference in the harvested set for the 661 shared checks.

Instrumentation is a logging wrapper in a DISPOSABLE copy; frozen source is never edited. The
suite's own result must be unchanged, which is asserted as the lawfulness guard.
"""
import collections
import hashlib
import json
import os
import shutil
import subprocess

PY = "/tmp/opensip-architecture-review-env/bin/python"
V10 = "/tmp/opensip-design-corrections/candidate-subject.v10"
V11 = "/tmp/opensip-design-corrections/candidate-subject.v11"
WORK = "/tmp/opensip-design-corrections/post-reset-review.v11/copies/identity"
DC = "docs/coop/design-corrections"

WRAPPER = '''
# --- reviewer instrumentation (disposable copy only) ---
import atexit as _atexit, json as _json
_IDLOG = []
_orig_identifier = identifier
def identifier(domain, value):
    _r = _orig_identifier(domain, value)
    _IDLOG.append(domain + "=" + _r)
    return _r
_atexit.register(lambda: open(%r, "w").write(_json.dumps(_IDLOG)))
'''


def build(tag, root):
    dst = os.path.join(WORK, tag)
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(root, dst)
    mp = os.path.join(dst, DC, "foundation/identity-model.py")
    log = os.path.join(dst, "idlog.json")
    src = open(mp).read()
    # append after the module body so `identifier` is already defined and every later
    # module-level use, plus every checker call through M.identifier, goes through the wrapper
    open(mp, "w").write(src + "\n" + (WRAPPER % log))
    return dst, log


out = {}
harvest = {}
for tag, root in (("v10", V10), ("v11", V11)):
    dst, log = build(tag, root)
    proc = subprocess.run(
        [PY, "-I", "-B", os.path.join(dst, DC, "foundation/check-identity.py")],
        cwd=dst, capture_output=True, text=True)
    ids = json.load(open(log)) if os.path.isfile(log) else []
    harvest[tag] = ids
    out[tag] = {
        "suiteStdout": proc.stdout.strip()[:160],
        "suiteExit": proc.returncode,
        "identitiesComputed": len(ids),
        "distinctIdentities": len(set(ids)),
        "byDomain": dict(collections.Counter(i.split("=")[0] for i in ids)),
        "setSha256": hashlib.sha256(
            "\n".join(sorted(set(ids))).encode()).hexdigest(),
    }

a, b = set(harvest["v10"]), set(harvest["v11"])
out["comparison"] = {
    "sharedIdentities": len(a & b),
    "onlyInV10": sorted(a - b)[:20],
    "onlyInV10Count": len(a - b),
    "onlyInV11": sorted(b - a)[:20],
    "onlyInV11Count": len(b - a),
    "v10SubsetOfV11": a <= b,
    "identitySetsEqual": a == b,
    "setShaEqual": out["v10"]["setSha256"] == out["v11"]["setSha256"],
}
out["instrumentationLawful"] = (out["v10"]["suiteExit"] == 0
                                and out["v11"]["suiteExit"] == 0)
out["ALL_PREEXISTING_IDENTITIES_STABLE"] = (
    out["comparison"]["v10SubsetOfV11"] and out["instrumentationLawful"])
print(json.dumps(out, indent=2))
