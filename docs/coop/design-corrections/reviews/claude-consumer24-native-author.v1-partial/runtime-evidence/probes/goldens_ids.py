"""Probe: the Run id and every Coverage id of each run-termination golden Run built under ROOT, with a stable key.

The key omits closure identities (which S1 changes on purpose) and keeps what a Coverage is ABOUT: source/target
universe, relation, rung, committed subjects and the entry's coverage/deficiency/stageTerminal. Used to map the
frozen parent's pinned ids to the corrected source's ids for the same golden scenario. Read-only; stdout only.
Usage: goldens_ids.py ROOT
"""
import importlib.util
import json
import sys
from pathlib import Path

root = Path(sys.argv[1]) / "docs/coop/design-corrections/foundation"
spec = importlib.util.spec_from_file_location("gold_semantic_replay", root / "check-semantic-replay.v3.py")
SR = importlib.util.module_from_spec(spec)
sys.modules["gold_semantic_replay"] = SR
spec.loader.exec_module(SR)

doc = json.loads((root / "run-termination-goldens.v1.json").read_text())
terminations = [g for g in doc["goldens"] if g["kind"] == "termination"]
wanted = {g["build"]["export"] for g in terminations if "export" in g["build"]}
exports = {}
for name, fn in SR.POSITIVES:
    if name in wanted:
        _, packed, _ = fn()
        exports[name] = packed
atoms = {"REFS_NONE_TGT": SR.REFS_NONE_TGT, "DECLARES": SR.DECLARES}
T = SR.load("gold_run_termination", "run_termination_model.v1.py")
out = {}
for g in terminations:
    build = g["build"]
    if "export" in build:
        run, objects, blobs = exports[build["export"]]
    else:
        fixture = doc["fixtures"][build["fixture"]]
        params = dict(fixture["params"], **build["params"], atom=atoms[fixture["atom"]])
        run, objects, blobs, _ = SR.close_positive(SR.S.build_ts_semantic_graph(**params))
    coverages = {}
    for key, (domain, value) in objects.items():
        if domain != "coverage":
            continue
        scope = objects[value["scopeId"]][1]
        entry = SR.C.parse(blobs[value["payloadDigest"]])["entry"]
        coverages[key] = [scope["sourceUniverse"], scope["targetUniverse"], scope["relation"], scope["resolution"],
                          scope["subjects"], entry.get("coverage"), entry.get("deficiency"),
                          (entry.get("resolutionCompleteness") or {}).get("stageTerminal")]
    out[g["id"]] = {"runId": SR.M.identifier("run", run), "coverages": coverages,
                    "derivedTermination": T.finalize(run, objects, blobs)["termination"]}
print(json.dumps(out, indent=1, sort_keys=True))
