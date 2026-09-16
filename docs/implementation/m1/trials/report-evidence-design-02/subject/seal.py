"""Authoring seal (author-02; never run by check.py).
  --phase generate : regenerate owner/ and fixtures.json (plain loads, no closure claim)
  --phase pin      : run check.py in-process in trace mode, then write source-pins.json and subject-files.json from the in-memory trace
Run: TMPDIR=<scratch> PY -I -B seal.py --architecture ARCH --phase generate|pin
"""
import argparse
import hashlib
import importlib.util
import json
import runpy
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PARENT07 = Path("/tmp/opensip-implementation/m1-report-projection-subject-07")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--architecture", required=True)
    parser.add_argument("--phase", choices=["generate", "pin"], required=True)
    args = parser.parse_args()
    arch = Path(args.architecture)
    if args.phase == "generate":
        sys.pycache_prefix = "/nonexistent-author02-seal-pycache"
        canonical = load("foundation_canonical", arch / "docs/coop/design-corrections/foundation/canonical.py")
        rm = load("parent07_report_model", PARENT07 / "report_model.py")
        NM = load("native_model_v2", arch / "docs/coop/design-corrections/native/native_evidence_model.v2.py")
        M = load("evidence_reference_model", HERE / "reference_model.py")
        M.bind(canonical, rm)
        bridge = load("evidence_identity_bridge", HERE / "identity_bridge.py")
        owner = load("evidence_build_owner", HERE / "build_owner.py")
        builder = load("evidence_build_fixtures", HERE / "build_fixtures.py")
        (HERE / "owner").mkdir(exist_ok=True)
        for name, value in owner.build(arch, M, bridge).items():
            (HERE / name).write_bytes(owner.dump(value))
        fixtures = json.loads((PARENT07 / "fixtures.json").read_bytes())
        (HERE / "fixtures.json").write_bytes(owner.dump(builder.build(M, NM, fixtures)))
        print("generated")
        return
    sys.argv = [str(HERE / "check.py"), "--architecture", str(arch), "--trace-closure"]
    namespace = runpy.run_path(str(HERE / "check.py"), run_name="__main__")
    trace = namespace["main"].__globals__["TRACE_RESULT"]
    pins = {"schemaVersion": 1, "standing": "exact external closure observed by an audit-hooked, fresh-source-loaded check.py trace run; enforced before import and at every open/listing",
            "roots": [str(arch), "/tmp/opensip-implementation"], "files": trace["files"], "directoryListings": trace["directoryListings"]}
    (HERE / "source-pins.json").write_text(json.dumps(pins, indent=1) + "\n")
    rows = []
    for path in sorted(p for p in HERE.rglob("*") if p.is_file() and "__pycache__" not in p.parts and p.name != "subject-files.json"):
        raw = path.read_bytes()
        rows.append({"path": str(path.relative_to(HERE)), "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)})
    (HERE / "subject-files.json").write_text(json.dumps({"schemaVersion": 1, "standing": "complete author-02 subject file list (excludes only itself)", "files": rows}, indent=1) + "\n")
    print("pinned", len(trace["files"]), "files;", len(trace["directoryListings"]), "listings;", len(rows), "subject files")


if __name__ == "__main__":
    main()
