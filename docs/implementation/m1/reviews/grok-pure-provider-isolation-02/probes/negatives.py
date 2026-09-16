"""Independent isolation/negative probes against a private mutant copy only."""
from __future__ import annotations

import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

CARGO = "/opt/homebrew/Cellar/rust/1.95.0/bin/cargo"
PYTHON = "/tmp/opensip-implementation/metadata-reference-env/bin/python"
REVIEW = Path("/tmp/opensip-implementation/m1-grok-pure-provider-isolation-02-review/review")
SRC = REVIEW / "copy" / "export"
ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
PRODUCT = Path("/Users/sb/code/opensip-ai/opensip")
CHECKER = ARCH / "docs/implementation/m1/contracts-dependency-selection-v1/product/tools/check_dependencies.py"
POLICY = ARCH / "docs/implementation/m1/contracts-dependency-selection-v1/product/tools/contracts/dependency-policy.json"
EDGES = PRODUCT / "tools/check_package_edges.py"
INV10 = ARCH / "docs/implementation/m1/repository-file-inventory.v10.json"
TARGET = "aarch64-apple-darwin"
SAFE_PATH = "/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin:/usr/sbin:/sbin"


def env_for(target: Path) -> dict[str, str]:
    env = {
        "HOME": os.environ["HOME"],
        "PATH": SAFE_PATH,
        "CARGO_TARGET_DIR": str(target),
        "CARGO_TERM_COLOR": "never",
        "CARGO_HOME": os.environ.get("CARGO_HOME", str(Path(os.environ["HOME"]) / ".cargo")),
        "TMPDIR": str(REVIEW / "probes" / "tmp"),
        "TERM": "dumb",
    }
    sdk = os.environ.get("SDKROOT")
    if sdk:
        env["SDKROOT"] = sdk
    return env


def copy_tree(dest: Path) -> None:
    if dest.exists():
        def _onerror(func, path, _exc):
            os.chmod(path, 0o700)
            func(path)
        shutil.rmtree(dest, onerror=_onerror)
    shutil.copytree(SRC, dest, symlinks=False, copy_function=shutil.copy2)
    for p in dest.rglob("*"):
        if p.is_dir():
            os.chmod(p, 0o755)


def run_checker(root: Path, target: Path) -> dict:
    r = subprocess.run(
        [PYTHON, "-I", "-B", str(CHECKER),
         "--manifest", str(root / "providers/rust/Cargo.toml"),
         "--target", TARGET, "--cargo", CARGO, "--policy", str(POLICY)],
        env=env_for(target), capture_output=True, timeout=120, text=True,
    )
    parsed = None
    if r.returncode == 0 and r.stdout.strip():
        parsed = json.loads(r.stdout)
    return {"exitCode": r.returncode, "stdout": r.stdout, "stderr": r.stderr, "parsed": parsed}


def metadata(root: Path, target: Path, locked: bool = True) -> dict:
    cmd = [CARGO, "metadata", "--offline", "--format-version", "1",
           "--filter-platform", TARGET, "--manifest-path", str(root / "providers/rust/Cargo.toml")]
    if locked:
        cmd.insert(2, "--locked")
    r = subprocess.run(cmd, env=env_for(target), capture_output=True, timeout=120, text=True)
    return {"exitCode": r.returncode, "stdout": r.stdout, "stderr": r.stderr}


def run_edges(root: Path, meta_path: Path) -> dict:
    r = subprocess.run(
        [PYTHON, "-I", "-B", str(EDGES),
         "--repository", str(root), "--metadata", str(meta_path),
         "--inventory", str(INV10), "--lane", "rust-provider"],
        capture_output=True, timeout=30, text=True,
    )
    return {"exitCode": r.returncode, "stdout": r.stdout, "stderr": r.stderr}


def main() -> None:
    if not sys.flags.isolated or sys.flags.optimize:
        raise SystemExit("isolated Python without optimization required")
    rows = []
    scratch = Path(tempfile.mkdtemp(prefix="opensip-iso02-", dir=str(REVIEW / "copy")))
    target = REVIEW / "probes" / "mutant-target"
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)

    def record(name: str, body) -> None:
        try:
            rows.append({"name": name, **body()})
        except Exception as exc:
            rows.append({"name": name, "error": f"{type(exc).__name__}: {exc}"})
        print(name, {k: v for k, v in rows[-1].items() if k != "name"})

    readonly = SRC / "crates/contracts/src/lib.rs"

    def write_readonly():
        try:
            with open(readonly, "a", encoding="utf-8") as fh:
                fh.write("\n")
            return {"wrote": True, "expectedEACCES": False}
        except PermissionError as exc:
            return {"wrote": False, "expectedEACCES": True, "errno": getattr(exc, "errno", None), "strerror": str(exc)}

    record("write-readonly-shared-source", write_readonly)

    def extra_src():
        root = scratch / "extra-src"
        copy_tree(root)
        os.chmod(root / "crates/contracts/src", 0o755)
        extra = root / "crates/contracts/src" / "unselected.rs"
        extra.write_text("pub const EXTRA: bool = true;\n")
        r = run_checker(root, target / "extra-src")
        return {
            "exitCode": r["exitCode"],
            "stderr": r["stderr"].strip(),
            "refused": r["exitCode"] != 0,
            "reasonContainsSourceSet": "source set differs" in r["stderr"],
        }

    record("extra-contracts-src-file-refuses", extra_src)

    def extra_root():
        root = scratch / "extra-root"
        copy_tree(root)
        os.chmod(root / "crates/contracts", 0o755)
        extra = root / "crates/contracts" / "unselected_root.rs"
        extra.write_text("pub const EXTRA: bool = true;\n")
        r = run_checker(root, target / "extra-root")
        return {
            "exitCode": r["exitCode"],
            "passed": bool(r["parsed"] and r["parsed"].get("passed")),
            "falseNegativeIfPassed": r["exitCode"] == 0,
            "stderr": r["stderr"].strip(),
            "standing": "S1 census is src/ plus Cargo.toml only",
        }

    record("extra-contracts-package-root-still-passes-S1", extra_root)

    def extra_tests():
        root = scratch / "extra-tests"
        copy_tree(root)
        os.chmod(root / "crates/contracts", 0o755)
        tests = root / "crates/contracts" / "tests"
        tests.mkdir()
        (tests / "probe.rs").write_text("#[test] fn x() {}\n")
        r = run_checker(root, target / "extra-tests")
        return {
            "exitCode": r["exitCode"],
            "passed": bool(r["parsed"] and r["parsed"].get("passed")),
            "falseNegativeIfPassed": r["exitCode"] == 0,
            "stderr": r["stderr"].strip(),
            "standing": "S1 census is src/ plus Cargo.toml only",
        }

    record("extra-contracts-tests-dir-still-passes-S1", extra_tests)

    def implicit_build_rs():
        root = scratch / "build-rs"
        copy_tree(root)
        os.chmod(root / "crates/contracts", 0o755)
        (root / "crates/contracts" / "build.rs").write_text("fn main() {}\n")
        r = run_checker(root, target / "build-rs")
        return {
            "exitCode": r["exitCode"],
            "stderr": r["stderr"].strip(),
            "refused": r["exitCode"] != 0,
            "reasonContainsSourceSet": "source set differs" in r["stderr"],
            "reasonContainsLibraryTarget": "library target" in r["stderr"],
        }

    record("unexpected-implicit-build-rs-refuses", implicit_build_rs)

    def extra_identity_src():
        root = scratch / "extra-identity"
        copy_tree(root)
        os.chmod(root / "crates/identity/src", 0o755)
        (root / "crates/identity/src" / "unselected.rs").write_text("pub const EXTRA: bool = true;\n")
        r = run_checker(root, target / "extra-identity")
        return {
            "exitCode": r["exitCode"],
            "passed": bool(r["parsed"] and r["parsed"].get("passed")),
            "falseNegativeIfPassed": r["exitCode"] == 0,
            "stderr": r["stderr"].strip(),
            "standing": "contracts checker does not census identity sources",
        }

    record("extra-identity-src-still-passes-contracts-checker", extra_identity_src)

    def forbidden_platform_edge():
        root = scratch / "platform-edge"
        copy_tree(root)
        os.chmod(root / "crates", 0o755)
        plat = root / "crates" / "platform"
        plat.mkdir()
        (plat / "Cargo.toml").write_text(
            '[package]\nname = "opensip-platform"\nversion = "0.1.0"\nedition = "2024"\nrust-version = "1.95"\npublish = false\n\n[lib]\npath = "src/lib.rs"\n'
        )
        (plat / "src").mkdir()
        (plat / "src" / "lib.rs").write_text("pub fn probe() {}\n")
        os.chmod(root / "providers/rust", 0o755)
        os.chmod(root / "providers/rust/Cargo.toml", 0o644)
        manifest = (root / "providers/rust/Cargo.toml").read_text()
        if "opensip-platform" not in manifest:
            manifest = manifest + 'opensip-platform = { path = "../../crates/platform" }\n'
            (root / "providers/rust/Cargo.toml").write_text(manifest)
        os.chmod(root / "providers/rust/Cargo.lock", 0o644)
        meta = metadata(root, target / "platform-edge", locked=False)
        meta_path = REVIEW / "results" / "logs" / "forbidden-platform-metadata.stdout"
        meta_path.write_text(meta["stdout"])
        (REVIEW / "results" / "logs" / "forbidden-platform-metadata.stderr").write_text(meta["stderr"])
        if meta["exitCode"] != 0:
            return {"metadataExit": meta["exitCode"], "metadataStderr": meta["stderr"], "edgesSkipped": True}
        edges = run_edges(root, meta_path)
        return {
            "metadataExit": meta["exitCode"],
            "edgesExit": edges["exitCode"],
            "edgesStderr": edges["stderr"].strip(),
            "refused": edges["exitCode"] != 0,
            "forbiddenEdge": "forbidden" in edges["stderr"] or "internal edge" in edges["stderr"],
        }

    record("forbidden-platform-internal-edge-refuses", forbidden_platform_edge)

    def node_absent():
        r = subprocess.run(["/usr/bin/which", "node"], env=env_for(target), capture_output=True, text=True)
        return {"exitCode": r.returncode, "path": r.stdout.strip(), "absent": r.returncode != 0}

    record("node-absent-from-restricted-path", node_absent)

    def live_provider_missing():
        p = PRODUCT / "providers/rust"
        return {"exists": p.exists(), "expectedMissing": not p.exists()}

    record("live-product-has-no-providers-rust", live_provider_missing)

    def probe_not_inventory_provider_sources():
        inv = json.loads(INV10.read_bytes())
        expected = [row["path"] for row in inv["files"] if row["package"] == "opensip-rust-provider"]
        present = sorted(
            p.relative_to(SRC / "providers/rust").as_posix()
            for p in (SRC / "providers/rust").rglob("*")
            if p.is_file()
        )
        present_full = ["providers/rust/" + p for p in present]
        missing = sorted(set(expected) - set(present_full))
        extra = sorted(set(present_full) - set(expected))
        return {
            "inventoryProviderFiles": expected,
            "probeProviderFiles": present_full,
            "missingVsInventory": missing,
            "extraVsInventory": extra,
            "deliberatelyMinimal": bool(missing) and present_full == [
                "providers/rust/Cargo.lock",
                "providers/rust/Cargo.toml",
                "providers/rust/src/main.rs",
            ],
        }

    record("probe-provider-sources-are-minimal-not-inventory-implementation", probe_not_inventory_provider_sources)

    def export_has_no_host_root():
        return {
            "copyRootCargo": (SRC / "Cargo.toml").exists(),
            "copyApps": (SRC / "apps").exists(),
            "copyTools": (SRC / "tools").exists(),
            "copyPackageJson": (SRC / "package.json").exists(),
            "copyRustToolchain": (SRC / "providers/rust/rust-toolchain.toml").exists(),
        }

    record("copy-export-still-isolated", export_has_no_host_root)

    out = {
        "scratch": str(scratch),
        "probes": rows,
    }
    (REVIEW / "results" / "negatives.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "count": len(rows),
        "names": [r["name"] for r in rows],
        "summary": [
            {k: v for k, v in r.items() if k in {"name", "refused", "passed", "falseNegativeIfPassed", "absent", "expectedMissing", "deliberatelyMinimal", "wrote", "expectedEACCES", "forbiddenEdge", "edgesSkipped", "error"}}
            for r in rows
        ],
    }, indent=2))


if __name__ == "__main__":
    main()
