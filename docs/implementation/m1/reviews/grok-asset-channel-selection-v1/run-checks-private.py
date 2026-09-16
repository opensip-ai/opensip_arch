from pathlib import Path
import json, subprocess, hashlib
from jsonschema import Draft202012Validator

A = Path("/Users/sb/code/opensip-ai/opensip_arch")
B = Path("/tmp/opensip-implementation/m1-grok-asset-channel-selection-v1-review/review/subject")
P = B / "product"
F = B / "fixture"
binding = json.loads((A / "docs/v2/architecture/report-asset-binding.v1.json").read_bytes())
pin = json.loads((B / "fixture-pin.json").read_bytes())
row = {k: pin[k] for k in binding["privateSchemas"]["HostAssetPinV1"]["schema"]["required"]}
Draft202012Validator(binding["privateSchemas"]["HostAssetPinV1"]["schema"]).validate(row)
manifest = json.loads((F / "manifest.json").read_bytes())
Draft202012Validator(binding["privateSchemas"]["ReportAssetManifestV1"]["schema"]).validate(manifest)
raw = (F / "manifest.json").read_bytes()
assert row["assetManifestBytes"] == len(raw) and row["assetManifestSha256"] == hashlib.sha256(raw).hexdigest()
asset = (F / "fixture.js").read_bytes()
assert manifest["assets"][0]["sha256"] == hashlib.sha256(asset).hexdigest() and manifest["assets"][0]["bytes"] == len(asset)
assert manifest["projectionSchemaSha256s"] == [hashlib.sha256((P / pin["projectionSource"]).read_bytes()).hexdigest()]
(B / "fixture-validation.private.json").write_text(
    json.dumps(
        {
            "privatePinShape": True,
            "privateManifestShape": True,
            "rawManifestDigestAndLength": True,
            "actualFixtureAssetDigestAndLength": True,
            "actualSelectedProjectionSchema": True,
            "productionAssetPinInvented": False,
        },
        indent=2,
    )
    + "\n"
)
cargo = "/opt/homebrew/Cellar/rust/1.95.0/bin/cargo"
commands = []
out = Path("/tmp/opensip-implementation/m1-grok-asset-channel-selection-v1-review/review/evidence")
out.mkdir(parents=True, exist_ok=True)
for name, cmd in [
    ("tests", [cargo, "test", "--locked", "--offline", "--workspace", "--all-targets"]),
    ("clippy", [cargo, "clippy", "--locked", "--offline", "--workspace", "--all-targets", "--", "-D", "warnings"]),
    ("fmt", [cargo, "fmt", "--all", "--check"]),
]:
    r = subprocess.run(cmd, cwd=P, capture_output=True, timeout=600, env={**{k: v for k, v in __import__("os").environ.items()}, "CARGO_TARGET_DIR": str(out / "target-host"), "PATH": "/opt/homebrew/Cellar/rust/1.95.0/bin:" + __import__("os").environ.get("PATH", "")})
    (out / (name + ".stdout")).write_bytes(r.stdout)
    (out / (name + ".stderr")).write_bytes(r.stderr)
    commands.append({"name": name, "command": cmd, "exitCode": r.returncode})
    (out / "commands.json").write_text(json.dumps(commands, indent=2) + "\n")
    assert r.returncode == 0, (name, r.stderr.decode()[-3000:], r.stdout.decode()[-3000:])
    print(name + " passed", flush=True)
