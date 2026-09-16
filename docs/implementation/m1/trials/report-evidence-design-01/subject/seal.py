"""Authoring seal (author-01; never run by check.py): regenerate owner/ and fixtures.json, trace the check closure in-process, write source-pins.json
and subject-files.json. Run: TMPDIR=<scratch> PY -I -B seal.py --architecture ARCH --trace TRACE.json
"""
import argparse
import hashlib
import json
import runpy
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--architecture", required=True)
    parser.add_argument("--trace", required=True)
    parser.add_argument("--phase", choices=["generate", "pin"], required=True)
    args = parser.parse_args()
    if args.phase == "generate":
        sys.path[:0] = [str(HERE)]
        import importlib.util

        def load(name, path):
            spec = importlib.util.spec_from_file_location(name, path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[name] = module
            spec.loader.exec_module(module)
            return module
        arch = Path(args.architecture)
        canonical = load("foundation_canonical", arch / "docs/coop/design-corrections/foundation/canonical.py")
        rm = load("subject05_report_model", Path("/tmp/opensip-implementation/m1-report-projection-subject-05/report_model.py"))
        M = load("evidence_reference_model", HERE / "reference_model.py")
        M.bind(canonical, rm)
        owner = load("evidence_build_owner", HERE / "build_owner.py")
        builder = load("evidence_build_fixtures", HERE / "build_fixtures.py")
        (HERE / "owner").mkdir(exist_ok=True)
        for name, value in owner.build(arch, M).items():
            (HERE / name).write_bytes(owner.dump(value))
        s05 = json.loads(Path("/tmp/opensip-implementation/m1-report-projection-subject-05/fixtures.json").read_bytes())
        (HERE / "fixtures.json").write_bytes(owner.dump(builder.build(M, s05)))
        print("generated")
        return
    sys.argv = [str(HERE / "check.py"), "--architecture", args.architecture, "--trace-closure", args.trace]
    namespace = runpy.run_path(str(HERE / "check.py"), run_name="__main__")
    trace = namespace["main"].__globals__["TRACE_RESULT"]
    files, listings = trace["files"], trace["directoryListings"]
    pins = {"schemaVersion": 1, "standing": "exact external closure observed by an audit-hooked, fresh-source-loaded check.py trace run; enforced before import and at every open/listing",
            "roots": [args.architecture, "/tmp/opensip-implementation"], "files": files, "directoryListings": listings}
    (HERE / "source-pins.json").write_text(json.dumps(pins, indent=1) + "\n")
    rows = []
    for path in sorted(p for p in HERE.rglob("*") if p.is_file() and "__pycache__" not in p.parts and p.name != "subject-files.json"):
        raw = path.read_bytes()
        rows.append({"path": str(path.relative_to(HERE)), "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)})
    (HERE / "subject-files.json").write_text(json.dumps({"schemaVersion": 1, "standing": "complete author-01 subject file list (excludes only itself)", "files": rows}, indent=1) + "\n")
    print("pinned", len(files), "files;", len(listings), "listings;", len(rows), "subject files")


if __name__ == "__main__":
    main()
