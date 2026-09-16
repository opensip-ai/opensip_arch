"""Probe: which (capability, mode) cells are usable for lawful precedence controls."""
import importlib.util
import json
from pathlib import Path

SRC = Path("/tmp/opensip-design-corrections/execution-account-successor.v1/source/docs/coop/design-corrections/foundation")


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, SRC / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


M = load("p2_model", "execution_inputs_model.v1.py")
F = load("p2_graph", "evaluator_graph_fixture.v3.py")
H = F.fixture_helpers()

out = {}
out["cells"] = sorted(
    [
        {
            "capability": cap, "mode": mode, "state": row.get("state"),
            "deficiency": row.get("deficiency"),
            "kinds": M._cap_kinds(cap), "pairs": M._matrix_pairs(cap),
        }
        for (cap, mode), row in M.CELL_STATE.items()
        if mode == "syntax-only"
    ],
    key=lambda r: (r["state"], r["capability"]),
)
cap_bytes = H.CURRENT_CAPABILITY_MANIFEST_BYTES
out["capabilityManifestHead"] = cap_bytes[:400].decode("utf-8", "replace")
try:
    manifest = M.C.parse(cap_bytes)
    out["capabilityManifestTop"] = sorted(manifest)
    caps = manifest.get("capabilities")
    if isinstance(caps, list):
        out["manifestCapabilities"] = [
            {k: v for k, v in c.items() if k in ("id", "capabilityId", "languageModes", "modes")}
            for c in caps
        ]
except Exception as exc:  # noqa: BLE001
    out["capabilityManifestParse"] = repr(exc)
out["kindDerivation"] = M.KIND_MAP
print(json.dumps(out, indent=2, default=str))
