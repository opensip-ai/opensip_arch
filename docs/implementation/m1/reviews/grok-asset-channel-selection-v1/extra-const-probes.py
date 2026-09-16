"""Independent extra const-guard probes against production assets.rs."""
from pathlib import Path
import os, shutil, subprocess, json, tempfile, textwrap

cargo = "/opt/homebrew/Cellar/rust/1.95.0/bin/cargo"
prod = Path("/tmp/opensip-implementation/m1-grok-asset-channel-selection-v1-review/review/subject/product")
assets = prod / "crates/reporting/src/assets.rs"
contracts = prod / "crates/contracts"
sha = "d8870ab533155cd0fe020daae148f091abdd93bf1a35e45f02de47936aaf99ef"
base = f'''
const TEST_PIN: HostAssetPinV1 = HostAssetPinV1 {{
    schema_version: 1,
    asset_root: "fixture-assets",
    asset_manifest_path: "fixture-assets/manifest.json",
    asset_manifest_sha256: "{sha}",
    asset_manifest_bytes: 266,
    build_channel: BUILD_CHANNEL,
}};
const TEST_SELECTION: CompiledBuildSelection = CompiledBuildSelection::new(BUILD_CHANNEL, Some(TEST_PIN));
pub fn selected() -> Metadata1BuildMetadataV1BuildChannel {{ TEST_SELECTION.channel() }}
'''
cases = [
    ("dot-segment", base.replace('"fixture-assets"', '"."'), "invalid asset root"),
    ("dotdot-segment", base.replace("fixture-assets/manifest.json", "fixture-assets/../x.json"), "invalid manifest path"),
    ("backslash", base.replace("fixture-assets/manifest.json", r"fixture-assets\\manifest.json"), "invalid manifest path"),
    ("uppercase-digest", base.replace(sha, sha.upper()), "invalid raw manifest digest"),
    ("schema-version", base.replace("schema_version: 1,", "schema_version: 2,"), "asset pin schema version differs"),
    ("too-long-bytes", base.replace("asset_manifest_bytes: 266,", "asset_manifest_bytes: 9_007_199_254_740_991,"), "invalid manifest byte length"),
    ("trailing-slash-root", base.replace('asset_root: "fixture-assets"', 'asset_root: "fixture-assets/"'), "invalid asset root"),
]
results = []
root = Path("/tmp/opensip-implementation/m1-grok-asset-channel-selection-v1-review/review/evidence/const-probes")
if root.exists():
    shutil.rmtree(root)
root.mkdir(parents=True)
env = os.environ.copy()
env["PATH"] = "/opt/homebrew/Cellar/rust/1.95.0/bin:" + env.get("PATH", "")
for i, (name, body, message) in enumerate(cases):
    d = root / name
    src = d / "src"
    src.mkdir(parents=True)
    dep = json.dumps(str(contracts))
    (d / "Cargo.toml").write_text(f'[workspace]\n[package]\nname="probe-{name}"\nversion="0.0.0"\nedition="2024"\npublish=false\n[dependencies]\nopensip-contracts={{path={dep}}}\n')
    inc = "include!(" + json.dumps(str(assets)) + ");\n"
    (src / "lib.rs").write_text(inc + body)
    cmd = [cargo, "check", "--offline", "--manifest-path", str(d / "Cargo.toml")]
    if i > 0:
        # copy lock from first if present; first is also a failure so lock may still be created
        pass
    r = subprocess.run(cmd, capture_output=True, env={**env, "CARGO_TARGET_DIR": str(d / "target")}, timeout=180)
    stderr = r.stderr.decode()
    ok = (not r.returncode == 0) and ("E0080" in stderr) and (message in stderr)
    results.append({"name": name, "expect": message, "exit": r.returncode, "e0080": "E0080" in stderr, "message": message in stderr, "ok": ok, "stderrTail": stderr[-1500:]})
    print(name, "OK" if ok else "FAIL", "exit", r.returncode, flush=True)
    if not ok:
        print(stderr[-2000:])
(root / "results.json").write_text(json.dumps(results, indent=2) + "\n")
print("all", all(x["ok"] for x in results))
