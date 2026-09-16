#!/usr/bin/env python3
"""Independent identity source-policy profiles and bypass attempts on the private copy."""
import copy, json, shutil, subprocess, sys, tempfile
from pathlib import Path
import importlib.util
import tomllib

ROOT = Path(sys.argv[1])
OUT = Path(sys.argv[2])
CARGO = sys.argv[3] if len(sys.argv) > 3 else "cargo"
P = ROOT / "product"
policy = json.loads((P / "tools/identity/dependency-policy.json").read_bytes())
spec = importlib.util.spec_from_file_location(
    "identity_policy", P / "tools/check_identity_dependencies.py"
)
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)
cache = Path.home() / ".cargo/registry/cache/index.crates.io-1949cf8c6b5b557f"

results = []
baseline = lock = None
for lane, manifest in [("host", P / "Cargo.toml"), ("provider", P / "providers/rust/Cargo.toml")]:
    for target in [
        "aarch64-apple-darwin",
        "x86_64-apple-darwin",
        "x86_64-unknown-linux-gnu",
        "aarch64-unknown-linux-gnu",
    ]:
        r = subprocess.run(
            [
                CARGO,
                "metadata",
                "--offline",
                "--locked",
                "--format-version",
                "1",
                "--filter-platform",
                target,
                "--manifest-path",
                str(manifest),
            ],
            capture_output=True,
        )
        if r.returncode != 0:
            results.append({"lane": lane, "target": target, "passed": False, "stderr": r.stderr.decode()[:400]})
            continue
        metadata = json.loads(r.stdout)
        current_lock = tomllib.loads((Path(metadata["workspace_root"]) / "Cargo.lock").read_text())
        result = M.check(metadata, current_lock, policy, cache)
        results.append({"lane": lane, "target": target, "result": result})
        if baseline is None:
            baseline, lock = metadata, current_lock

negative = []

def pkg(m, name):
    return next(p for p in m["packages"] if p["name"] == name)

def node(m, name):
    return next(n for n in m["resolve"]["nodes"] if n["id"] == pkg(m, name)["id"])

def reject(label, metadata, policy=policy, archives=cache, lock=lock):
    try:
        M.check(metadata, lock, policy, archives)
    except M.DependencyError as exc:
        negative.append({"label": label, "refusal": str(exc)})
    else:
        raise SystemExit(label + " unexpectedly passed")

for name in ["unicode-normalization", "tinyvec", "sha2-const-stable"]:
    m = copy.deepcopy(baseline)
    node(m, name)["features"].append("std")
    reject(name + "-extra-feature", m)
    m = copy.deepcopy(baseline)
    pkg(m, name)["source"] = None
    reject(name + "-local-substitute", m)
    m = copy.deepcopy(baseline)
    pkg(m, name)["links"] = "native"
    reject(name + "-native-links", m)
for kind in ["custom-build", "proc-macro"]:
    m = copy.deepcopy(baseline)
    pkg(m, "unicode-normalization")["targets"].append({"kind": [kind]})
    reject("extra-" + kind, m)
m = copy.deepcopy(baseline)
node(m, "opensip-identity")["features"].append("std")
reject("root-extra-feature", m)
m = copy.deepcopy(baseline)
pkg(m, "unicode-normalization")["version"] = "0.1.25"
reject("Unicode17-version", m)
m = copy.deepcopy(baseline)
pkg(m, "tinyvec")["targets"][0]["src_path"] = "/outside/lib.rs"
reject("source-target-escape", m)
p = copy.deepcopy(policy)
p["dependencies"].pop()
reject("unlisted-dependency", copy.deepcopy(baseline), policy=p)
l = copy.deepcopy(lock)
next(x for x in l["package"] if x["name"] == "tinyvec")["checksum"] = "0" * 64
reject("changed-lock-checksum", copy.deepcopy(baseline), lock=l)

with tempfile.TemporaryDirectory(prefix="identity-policy07-review-") as d:
    root = Path(d) / "identity"
    shutil.copytree(P / "crates/identity", root, ignore=shutil.ignore_patterns("target"))

    def relocated():
        m = copy.deepcopy(baseline)
        p = pkg(m, "opensip-identity")
        original = Path(p["manifest_path"]).parent
        p["manifest_path"] = str(root / "Cargo.toml")
        for t in p["targets"]:
            t["src_path"] = str(root / Path(t["src_path"]).relative_to(original))
        return m

    source = root / "src/canonical.rs"
    raw = source.read_bytes()
    source.write_bytes(raw + b"\n")
    reject("changed-local-source", relocated())
    source.write_bytes(raw)
    extra = root / "src/extra.rs"
    extra.write_text("")
    reject("extra-local-source", relocated())
    extra.unlink()
    source.unlink()
    source.symlink_to(P / "crates/identity/src/canonical.rs")
    reject("linked-local-source", relocated())
    source.unlink()
    source.write_bytes(raw)
    archives = Path(d) / "archives"
    archives.mkdir()
    for row in policy["dependencies"]:
        name = row["name"] + "-" + row["version"] + ".crate"
        shutil.copy2(cache / name, archives / name)
    (archives / "tinyvec-1.13.3.crate").write_bytes(b"changed")
    reject("changed-archive", copy.deepcopy(baseline), archives=archives)
    m = copy.deepcopy(baseline)
    p = pkg(m, "tinyvec")
    original = Path(p["manifest_path"]).parent
    external = Path(d) / "tinyvec"
    shutil.copytree(original, external)
    p["manifest_path"] = str(external / "Cargo.toml")
    for t in p["targets"]:
        t["src_path"] = str(external / Path(t["src_path"]).relative_to(original))
    source = external / "src/lib.rs"
    source.write_bytes(source.read_bytes() + b"\n")
    reject("changed-extracted-registry-source", m)

tinyvec = next(d for d in policy["dependencies"] if d["name"] == "tinyvec")
uni = next(d for d in policy["dependencies"] if d["name"] == "unicode-normalization")
out = {
    "profiles": results,
    "profileCount": len(results),
    "profilesPassed": all(r.get("result", {}).get("passed") for r in results),
    "negativeChecks": negative,
    "negativeCount": len(negative),
    "tinyvecFeatures": tinyvec["resolvedFeatures"],
    "unicodeFeatures": uni["resolvedFeatures"],
    "unicodeVersion": policy["unicodeVersion"],
    "passed": all(r.get("result", {}).get("passed") for r in results) and len(negative) == 21,
}
OUT.write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps({k: out[k] for k in ["profileCount", "profilesPassed", "negativeCount", "tinyvecFeatures", "unicodeFeatures", "unicodeVersion", "passed"]}))
if not out["passed"]:
    sys.exit(1)
