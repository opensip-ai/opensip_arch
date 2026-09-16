"""R2 fix 1 (after failed run r2-2-wp): the policy-test fixture must resolve workflow-cases `$` references exactly as the
owner checker check_workflows.v1.py does (sub(RAW) over constants, derived argv digests and policyDocs)."""
import json, sys
sys.path.insert(0, '/private/tmp/opensip-design-corrections/claude-consumer24-workflow-author.v2/tools')
from textedit import apply  # noqa: E402

CWP = 'docs/coop/design-corrections/workflows/check-workflow-projection.v3.py'

row = apply('R2 fix1 policy suite owner substitution', CWP, [
    ('''_r2_policy_result, _r2_policy_refusal = P.W.run_policy_test(json.loads((HERE / "workflow-cases.v1.json").read_text())["policySuite"])
''', '''_R2_RAW = canonical.parse((HERE / "workflow-cases.v1.json").read_bytes())
_R2_C = dict(_R2_RAW["constants"])
_R2_C["ARGV"] = P.W.raw_sha(canonical.canonical(["scripts/test.sh", "--ci"]))
_R2_C["ARGV2"] = P.W.raw_sha(canonical.canonical(["/usr/bin/bash", "-c", "rm -rf ."]))
_R2_C["TOOL0#bin/node"] = _R2_C["TOOL0"] + "#bin/node"
_R2_C["ARGV4"] = P.W.raw_sha(canonical.canonical(["node", "test.js"]))
_R2_C["ARGV3"] = P.W.raw_sha(canonical.canonical(["bin/node", "test.js"]))


def _r2_sub(o):
    """The owner checker's workflow-cases substitution (check_workflows.v1.py sub)."""
    if isinstance(o, str) and o.startswith("$"):
        if o[1:] in _R2_C:
            return _R2_C[o[1:]]
        if o[1:] in _R2_RAW["policyDocs"]:
            return _r2_sub(_R2_RAW["policyDocs"][o[1:]])
        raise KeyError(o)
    if isinstance(o, dict):
        return {_r2_sub(k) if isinstance(k, str) and k.startswith("$") else k: _r2_sub(v) for k, v in o.items()}
    if isinstance(o, list):
        return [_r2_sub(v) for v in o]
    return o


_r2_policy_result, _r2_policy_refusal = P.W.run_policy_test(_r2_sub(_R2_RAW)["policySuite"])
'''),
])
print(json.dumps(row, indent=1))
