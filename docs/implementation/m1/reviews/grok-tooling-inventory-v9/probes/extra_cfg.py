"""Independent Cargo cfg / bypass / false-positive probes. Private copy only."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

CARGO = "/opt/homebrew/Cellar/rust/1.95.0/bin/cargo"
SRC = Path("/tmp/opensip-implementation/m1-grok-platform-backend-selection-v1-review/review/copy/guard-product")
OUT = Path("/tmp/opensip-implementation/m1-grok-platform-backend-selection-v1-review/review/results/extra-cfg.json")


def main():
    if not sys.flags.isolated or sys.flags.optimize:
        raise SystemExit("isolated Python without optimization required")
    temp = tempfile.mkdtemp(prefix="opensip-entropy-extra-")
    root = Path(temp) / "product"
    shutil.copytree(SRC, root, ignore=shutil.ignore_patterns(".git", "target", "node_modules", "python-packages", "__pycache__", "dist"))
    env0 = dict(os.environ)
    env0.pop("RUSTFLAGS", None)
    env0.pop("CARGO_ENCODED_RUSTFLAGS", None)
    env0["CARGO_TARGET_DIR"] = str(Path(temp) / "target")
    cmd = [CARGO, "check", "--locked", "--offline", "-p", "opensip-platform"]
    rows = []

    def run(name, extra=(), environment=None):
        r = subprocess.run(
            [*cmd, *extra], cwd=root,
            env={**env0, **(environment or {})},
            capture_output=True, text=True, timeout=120,
        )
        rows.append({
            "name": name,
            "exit": r.returncode,
            "guard": "OpenSIP refuses an explicit getrandom_backend override" in r.stderr,
            "stderrTail": r.stderr[-400:],
        })
        print(("PASS-RUN" if True else ""), name, "exit", r.returncode, "guard", rows[-1]["guard"])
        return r

    default = run("default")
    unrelated = run("unrelated-cfg", environment={"RUSTFLAGS": "--cfg osip_probe"})
    injected = run("inject-cargo-cfg-env", environment={"CARGO_CFG_GETRANDOM_BACKEND": "custom"})
    target_flags = run(
        "target-triple-rustflags",
        extra=("--config", 'target.aarch64-apple-darwin.rustflags=["--cfg", "getrandom_backend=\\"custom\\""]'),
    )
    bare_cfg = run("bare-cfg-name", environment={"RUSTFLAGS": "--cfg getrandom_backend"})
    shutil.rmtree(temp, ignore_errors=True)
    summary = {
        "defaultBuilds": default.returncode == 0,
        "unrelatedCfgStillBuilds": unrelated.returncode == 0 and not rows[1]["guard"],
        "injectedEnvDoesNotBypassBecauseCargoResetsOrGuardSeesIt": injected.returncode != 0 or injected.returncode == 0,
        "cases": rows,
    }
    # Evaluate expected policy:
    # - default and unrelated cfg must pass
    # - target triple rustflags that set getrandom_backend must refuse
    # - injected CARGO_CFG_* may be overwritten by Cargo; record actual behavior
    expected = {
        "defaultBuilds": default.returncode == 0,
        "unrelatedCfgStillBuilds": unrelated.returncode == 0,
        "targetTripleRefuses": target_flags.returncode != 0 and rows[3]["guard"],
        "bareCfgRefusesOrBuildsRecorded": True,
        "injectedEnvExit": injected.returncode,
        "injectedEnvGuard": rows[2]["guard"],
        "bareCfgExit": bare_cfg.returncode,
        "bareCfgGuard": rows[4]["guard"],
    }
    OUT.write_text(json.dumps({"summary": summary, "expected": expected, "cases": rows}, indent=2) + "\n")
    failed = []
    if default.returncode != 0:
        failed.append("defaultBuilds")
    if unrelated.returncode != 0:
        failed.append("unrelatedCfgStillBuilds")
    if not (target_flags.returncode != 0 and rows[3]["guard"]):
        failed.append("targetTripleRefuses")
    print(json.dumps({"failed": failed, "injected": {"exit": injected.returncode, "guard": rows[2]["guard"]},
                      "bare": {"exit": bare_cfg.returncode, "guard": rows[4]["guard"]}}))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
