"""Probe: the security lifecycle checker's cases and sweeps WITHOUT its source-pin gate.

check-security-lifecycle.v1.py main() refuses to run anything when source-pins.v1.json does not match, and this
runtime changes pinned native/foundation files on purpose (pins are root's integration job). This probe imports the
checker module and runs exactly its case runner and sweep list, reporting the pin mismatch separately. Stdout only.
Usage: security_no_pins.py ROOT
"""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

root = Path(sys.argv[1]) / "docs/coop/design-corrections/security"
spec = importlib.util.spec_from_file_location("c24_security_checker", root / "check-security-lifecycle.v1.py")
S = importlib.util.module_from_spec(spec)
sys.modules["c24_security_checker"] = S
spec.loader.exec_module(S)

from jsonschema import Draft202012Validator  # noqa: E402

pins = json.loads((root / "source-pins.v1.json").read_text())
changed = [p["path"] for p in pins["pins"]
           if not (S.ROOT / p["path"]).is_file() or hashlib.sha256((S.ROOT / p["path"]).read_bytes()).hexdigest() != p["sha256"]]
schemas = S.canonical.parse((root / "security-lifecycle.schemas.v1.json").read_bytes())
validators = {}


def validator_for(name):
    if name not in validators:
        if name not in schemas["schemas"]:
            raise KeyError("UNKNOWN_SCHEMA:" + name)
        s = {"$ref": "#/schemas/" + name, "$defs": schemas["$defs"], "schemas": schemas["schemas"]}
        Draft202012Validator.check_schema(s)
        validators[name] = S.canonical.ExactValidator(s)
    return validators[name]


cases = S.run_cases(schemas, validator_for)
sweeps = []
for sweep in (S.sweep_clock_monotone, S.sweep_recovery_replay, S.sweep_linearization, S.sweep_journal_record_dispatch,
              S.sweep_profile_separation, S.sweep_lease_modes, S.sweep_root_schema_readers,
              S.sweep_discovery_pruning_and_cap, S.sweep_platform_vocabulary_join, S.sweep_boundary_join_native,
              S.sweep_public_detail_closure):
    try:
        sweeps.append(sweep())
    except Exception as e:  # noqa: BLE001 - a failing sweep is a failed sweep
        sweeps.append({"name": sweep.__name__, "holds": False, "detail": ("%s: %s" % (type(e).__name__, e))[:500]})
failed_cases = [{"file": c["file"], "id": c["id"], "failures": c["failures"]} for c in cases if c["status"] != "PASS"]
out = {"pinMismatchPaths": changed, "cases": len(cases), "casesFailed": failed_cases,
       "sweeps": [(s["name"], s["holds"]) for s in sweeps],
       "sweepFailures": [s for s in sweeps if not s["holds"]]}
print(json.dumps(out, indent=1))
raise SystemExit(1 if failed_cases or out["sweepFailures"] else 0)
