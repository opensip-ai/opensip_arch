"""Candidate internal pipeline only. Does not forge public activation."""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import sys

REV = Path("/tmp/opensip-implementation/m1-grok-combined-generation-review-04/review")
COPY = REV / "copy"
OUT = REV / "generation-internal-01"
spec = importlib.util.spec_from_file_location("pipeline", COPY / "tools/contracts/pipeline.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
tools = json.loads((COPY / "local-tools.json").read_text())
closure = json.loads((COPY / "tools/contracts/generator-closure.json").read_text())
registry_raw = (COPY / "schemas/registry.json").read_bytes()
recipe = json.loads(registry_raw)["recipes"][0]
if OUT.exists():
    raise SystemExit("generation-internal-01 already exists")
args = argparse.Namespace(root=COPY, output=OUT, **{k: Path(v) for k, v in tools.items()})
result = m.run(
    args,
    selected_closure=closure["files"],
    provenance={
        "registrySha256": hashlib.sha256(registry_raw).hexdigest(),
        "generatorClosureSha256": recipe["generatorClosureSha256"],
    },
)
assert result["sourceApproved"] is False, result
assert result["passed"] is True
assert len(result["outputs"]) == 8
assert len(closure["files"]) == 348
(REV / "results" / "internal-pipeline.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"passed": True, "sourceApproved": result["sourceApproved"], "outputs": len(result["outputs"]), "inputClosure": result["inputClosure"]}))
