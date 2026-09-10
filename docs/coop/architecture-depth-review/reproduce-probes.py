"""Reproduce audit observations against retained design models, without editing them.

Use the dependency environment in ../completion/review-dependencies/requirements.txt.
Run: python -I -B reproduce-probes.py --repo /path/to/opensip_arch --report /tmp/probes.json
Exit zero means the probe ran; it does NOT mean these design defects are fixed.
"""
import argparse
import copy
import hashlib
import importlib.metadata
import importlib.util
import json
import platform
from pathlib import Path


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    root = args.repo.resolve()
    base = root / "docs/coop/completion"
    foundation = load("audit_foundation", base / "host-foundation-model.v1.py")
    g13 = load("audit_g13", base / "check_g13_result_design_v4.py")
    cases = json.loads((base / "host-foundation-cases.v1.json").read_text())["cases"]
    config = copy.deepcopy(next(c["input"] for c in cases if c["id"] == "compiled-profile-only"))
    config.pop("solverFixtureId", None)
    numeric = []
    for field, literals in [
        ("budget", ["1", "1.0", "1e0", "1.0000000000000001", "9007199254740991.1"]),
        ("schemaVersion", ["1", "1.0", "1e0"]),
    ]:
        for literal in literals:
            raw = ('{"schemaVersion":1,"analysis":{"budget":{"unit":"work-units","limit":'
                   + literal + '}}}') if field == "budget" else '{"schemaVersion":' + literal + '}'
            request = copy.deepcopy(config)
            request["files"] = {"project/opensip.json": {"raw": raw}}
            result = foundation.configuration(request)
            budget = result["semantic"].get("analysis.budget")
            numeric.append({
                "field": field, "literal": literal, "status": result["status"],
                "budget": budget, "reason": result.get("reason"),
                "pythonType": type(budget["limit"]).__name__ if budget else None,
                "expectedByExactIntegerLaw": "ACCEPT" if literal == "1" else "REFUSE",
            })
    reference = g13.reference()
    trusted = {p["platform"]: {k: p["runner"][k] for k in g13.HARDWARE}
               for p in reference["performance"]}
    probes = [("positive-control", copy.deepcopy(reference))]
    altered = copy.deepcopy(reference)
    altered.update(hostDigest="b" * 64, providerClosureDigest="c" * 64)
    for p in altered["performance"]:
        p["runner"].update(hostDigest="b" * 64, providerClosureDigest="c" * 64)
    probes.append(("all-candidate-subject-digests-relabelled-trusted-inventory-unchanged", altered))
    altered = copy.deepcopy(reference)
    for cell in altered["cells"]:
        for fixture in cell["fixtureResults"]:
            fixture.update(expectedCount=0, actualCount=0)
    probes.append(("every-fixture-claims-zero-expected-and-zero-actual", altered))
    altered = copy.deepcopy(reference)
    altered["schemaMajor"] = 1.0
    probes.append(("schema-major-float", altered))
    observations = [{"case": name, "accepted": g13.valid(value, None, trusted)}
                    for name, value in probes]
    files = ["host-foundation-model.v1.py", "host-foundation-cases.v1.json",
             "preview-configuration.schema.v1.json", "check_g13_result_design_v4.py",
             "g13-result-schema.v4.json", "language-quality-matrix.completed.v2.json",
             "quality-corpus-manifest.v1.json"]
    report = {
        "standing": "Audit observations; not product qualification or repaired-contract acceptance",
        "environment": {"python": platform.python_version(),
                        "jsonschema": importlib.metadata.version("jsonschema")},
        "sourcePins": [{"path": str((base / f).relative_to(root)),
                        "sha256": hashlib.sha256((base / f).read_bytes()).hexdigest()} for f in files],
        "numericAdmission": numeric, "g13Admission": observations,
    }
    args.report.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"observations": len(numeric) + len(observations),
                      "report": str(args.report), "productQualification": False}))


if __name__ == "__main__":
    main()
