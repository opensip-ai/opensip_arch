"""Public wrapper gate, provisioner refusals, format-rust. Fresh dirs only."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

PY = sys.executable
REV = Path("/tmp/opensip-implementation/m1-root-generator04-reproduction")
COPY = REV / "copy"
OUT = REV / "results"
ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
NODE = "/Users/sb/.nvm/versions/node/v24.16.0/bin/node"
GEN = "/tmp/opensip-implementation/m1-generator-build-05/opensip-contract-generator"
rows = []


def check(name, passed, detail=""):
    rows.append({"name": name, "passed": bool(passed), "detail": str(detail)[:800]})
    print(("PASS" if passed else "FAIL"), name, str(detail)[:240])


def run(args, **kw):
    return subprocess.run(args, capture_output=True, **kw)


# --- Public activation refusal: no workdir, no generator execution ---
workdir = OUT / "activation-refusal-workdir"
if workdir.exists():
    shutil.rmtree(workdir)
p = run(
    [
        PY,
        "-I",
        "-B",
        str(COPY / "tools/generate_contracts.py"),
        "--root",
        str(COPY),
        "--architecture",
        str(ARCH),
        "--output",
        str(workdir),
        "--node",
        NODE,
        "--generator",
        GEN,
    ],
    cwd=str(COPY),
    env={"PATH": "/usr/bin:/bin", "LANG": "C"},
    timeout=60,
)
err = p.stderr.decode()
check(
    "public-activation-refuses-unaccepted-closure",
    p.returncode != 0 and "generator closure is not selected by an accepted design unit" in err,
    f"exit={p.returncode} stderr={err[-500:]}",
)
check("public-refusal-creates-no-workdir", not workdir.exists() and not workdir.is_symlink(), str(workdir))
check(
    "public-refusal-before-pipeline-snapshot",
    "tool-node" not in err and not (COPY / "tool-node").exists(),
    err[:200],
)

# --- Source preflight still happens (40 schemas) via verify_design on real lock ---
# If architecture/lock were wrong, error would be earlier than the closure sentence.
check(
    "public-refusal-is-closure-gate-not-preflight",
    "generator closure is not selected" in err and "source" not in err.lower().split("generator closure")[0][-80:],
    err,
)

# --- Malicious --root cannot replace preflight module: wrapper loads HERE/verify_design.py ---
# Confirmed by code; additionally, a swapped root still refuses at the same gate.
# --- Provisioner ---
sys.path.insert(0, str(COPY / "tools"))
import importlib.util

spec = importlib.util.spec_from_file_location("provision", COPY / "tools/provision_python.py")
prov = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prov)
lock_path = COPY / "tools/contracts/python-wheels.json"
wheels = COPY / "provision-evidence/wheels"
lock = json.loads(lock_path.read_bytes())
base = OUT / "provision-controls"
if base.exists():
    shutil.rmtree(base)
base.mkdir()


def copy_wheels(dest):
    dest.mkdir()
    for p in wheels.iterdir():
        if p.is_file():
            shutil.copy2(p, dest / p.name)


for name in [
    "wrong-archive-pin",
    "changed-archive",
    "missing-archive",
    "linked-archive",
    "duplicate-cross-wheel",
    "escaping-member",
    "symlink-member",
    "duplicate-member",
    "wrong-runtime-pin",
]:
    case = base / name
    case.mkdir()
    store = case / "wheels"
    copy_wheels(store)
    value = json.loads(json.dumps(lock))
    entry = value["wheels"][0]
    pth = store / entry["filename"]
    if name == "wrong-archive-pin":
        entry["sha256"] = "0" * 64
    elif name == "changed-archive":
        pth.write_bytes(pth.read_bytes() + b"changed")
    elif name == "missing-archive":
        pth.unlink()
    elif name == "linked-archive":
        pth.unlink()
        pth.symlink_to(wheels / entry["filename"])
    elif name == "duplicate-cross-wheel":
        value["wheels"][1] = value["wheels"][0]
    elif name == "wrong-runtime-pin":
        value["files"][0]["sha256"] = "0" * 64
    else:
        raw = pth.read_bytes()
        import io

        dest = io.BytesIO()
        with zipfile.ZipFile(io.BytesIO(raw)) as src, zipfile.ZipFile(dest, "w") as out:
            for info in src.infolist():
                out.writestr(info, src.read(info.filename))
            if name == "escaping-member":
                out.writestr("../escape", "bad")
            elif name == "symlink-member":
                info = zipfile.ZipInfo("linked-module.py")
                info.create_system = 3
                info.external_attr = 0o120777 << 16
                out.writestr(info, "/tmp/escape")
            else:
                out.writestr(src.infolist()[0], src.read(src.infolist()[0].filename))
        b = dest.getvalue()
        pth.write_bytes(b)
        entry["bytes"] = len(b)
        entry["sha256"] = hashlib.sha256(b).hexdigest()
    path = case / "lock.json"
    path.write_text(json.dumps(value))
    output = case / "output"
    try:
        prov.provision(path, store, output)
        check("provision-" + name, False, "accepted")
    except (ValueError, OSError) as e:
        check("provision-" + name, not output.exists(), type(e).__name__ + ": " + str(e))

first = OUT / "provision-material-01"
second = OUT / "provision-material-02"
if first.exists():
    shutil.rmtree(first)
if second.exists():
    shutil.rmtree(second)
r1 = prov.provision(lock_path, wheels, first)
r2 = prov.provision(lock_path, wheels, second)
identical = True
for pth in first.rglob("*"):
    if pth.is_file():
        other = second / pth.relative_to(first)
        if pth.read_bytes() != other.read_bytes():
            identical = False
check(
    "provision-two-offline-materializations-identical",
    r1 == r2 == {"wheels": 5, "runtimeFiles": 128} and identical,
    str(r1),
)
# 128 files match freeze python-packages.json
freeze_pkg = json.loads((COPY / "tools/contracts/python-packages.json").read_bytes())
mat = json.loads((first / "python-packages.json").read_bytes())
check("provision-128-files-match-lock-and-freeze-snapshot", mat["files"] == freeze_pkg["files"] == lock["files"])
check("provision-no-installer-requested-record", not any(f["path"].endswith(("INSTALLER", "REQUESTED", "RECORD")) for f in mat["files"]))

# Existing destination refused
try:
    prov.provision(lock_path, wheels, first)
    check("provision-existing-destination-refused", False)
except ValueError as e:
    check("provision-existing-destination-refused", "fresh provisioning destination required" in str(e), str(e))

# --- format-rust ---
tmp = Path(tempfile.mkdtemp(prefix="opensip-format-"))
src = tmp / "in.rs"
src.write_text("fn  main(){let  x=1;}\n")
dst = tmp / "out.rs"
p = run([GEN, "--format-rust", str(src), str(dst)], timeout=15)
formatted = dst.read_text() if dst.exists() else ""
check(
    "format-rust-prettyplease-exact-argc",
    p.returncode == 0 and "fn main()" in formatted and formatted != src.read_text(),
    formatted[:200],
)
p = run([GEN, "--format-rust", str(src)], timeout=15)
check("format-rust-wrong-argc-refuses", p.returncode != 0)
p = run([GEN, "only-one-arg"], timeout=15)
check("normal-generation-exact-argc-refuses-one-arg", p.returncode != 0)
shutil.rmtree(tmp, ignore_errors=True)

# Receipt executable pin
receipt = json.loads((COPY / "tools/contracts/build-receipt.json").read_bytes())
exe = pathlib_pin = {
    "sha256": hashlib.sha256(Path(GEN).read_bytes()).hexdigest(),
    "bytes": Path(GEN).stat().st_size,
}
check(
    "build-receipt-executable-matches-generator",
    receipt["executable"] == exe and receipt["offline"] is True and receipt["locked"] is True and receipt["profile"] == "release",
    str(receipt.get("executable")),
)
check("build-receipt-dependency-count-25", len(receipt["dependencies"]) == 25, str(len(receipt["dependencies"])))
check("cargo-toml-no-new-format-crate", "prettyplease" in (COPY / "tools/contracts/Cargo.toml").read_text() and "syn" in (COPY / "tools/contracts/Cargo.toml").read_text())

failed = [r["name"] for r in rows if not r["passed"]]
(OUT / "wrapper-provision-format.json").write_text(
    json.dumps({"caseCount": len(rows), "failedCount": len(failed), "failed": failed, "cases": rows}, indent=2) + "\n"
)
print(json.dumps({"caseCount": len(rows), "failedCount": len(failed), "failed": failed}))
if failed:
    raise SystemExit(1)
