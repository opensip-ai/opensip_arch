"""Explicit synthetic build fixture only; never a product asset build."""
import hashlib
import json
import os
from pathlib import Path
import types

HERE = Path(__file__).resolve().parent
module = types.ModuleType("asset_assembly")
source = HERE / "tools/report_asset_manifest.py"
exec(compile(source.read_bytes(), str(source), "exec"), module.__dict__)
root = HERE / "fixtures/release/report"
fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | os.O_NOFOLLOW)
try:
    manifest, pin = module.assemble(fd, asset_root="report", manifest_path="report/manifest.json",
                                    projection_digests=["1" * 64, "5" * 64, "a" * 64],
                                    roles={"report/app.js": "script", "report/main.css": "style", "report/notice.txt": "notice"},
                                    build_channel="development")
finally:
    os.close(fd)
owner = json.loads((HERE / "inputs/report-asset-binding.v1.json").read_bytes())
# Reference-only schema check: production tool has no jsonschema dependency.
from jsonschema import Draft202012Validator
Draft202012Validator(owner["privateSchemas"]["HostAssetPinV1"]["schema"]).validate(pin)
Draft202012Validator(owner["privateSchemas"]["ReportAssetManifestV1"]["schema"]).validate(json.loads(manifest))
(root / "manifest.json").write_bytes(manifest)
(HERE / "fixtures/pin.json").write_text(json.dumps(pin, indent=2) + "\n")
(HERE / "fixtures/manifest-digest.rs").write_text("[" + ", ".join(str(x) for x in hashlib.sha256(manifest).digest()) + "]\n")
print(json.dumps({"standing": "synthetic interoperability fixture, not actual report assets", "manifestBytes": len(manifest),
                  "memberBytes": sum(row["bytes"] for row in json.loads(manifest)["assets"]), "pin": pin}))
