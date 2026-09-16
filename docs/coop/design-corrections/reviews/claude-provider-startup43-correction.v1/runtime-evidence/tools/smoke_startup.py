"""Smoke check (not a control): the work-copy native model loads the startup module and the TS order table runs.

usage: smoke_startup.py <work-candidate-root>
"""
import importlib.util
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

root = Path(sys.argv[1])
path = root / "docs" / "coop" / "design-corrections" / "native" / "native_evidence_model.v2.py"
spec = importlib.util.spec_from_file_location("smoke_native", path)
model = importlib.util.module_from_spec(spec)
spec.loader.exec_module(model)
S = model.STARTUP
Draft202012Validator.check_schema(S.STARTUP)
out = {"exchange": hasattr(model, "provider_startup_exchange"), "startupDefs": len(S.STARTUP["$defs"]),
       "tsRules": S.TS_ORDER["ruleCount"]}
happy = [{"frame": "Hello"}, {"frame": "HelloAck", "capabilities": list(model.TS2_TOKENS)}, {"frame": "OpenUniverse"},
         {"frame": "UniverseAccepted"}, {"frame": "SnapshotManifest"}, {"frame": "SnapshotSeal"},
         {"frame": "SnapshotAccepted"}, {"frame": "NativeContextVerified"}, {"frame": "Analyze"}, {"frame": "Coverage"},
         {"frame": "Complete"}, {"frame": "zero-exit"}, {"frame": "eof"}]
out["tsHappy"] = S.typescript_protocol2_run(happy)
pre = happy[:7] + [{"frame": "Unavailable", "unavailablePayload": "pre-analyze"}, {"frame": "zero-exit"}, {"frame": "eof"}]
out["tsPreAnalyzeUnavailable"] = S.typescript_protocol2_run(pre)
print(json.dumps(out, indent=1))
