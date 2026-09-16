"""Adapted checker-mode checks on the private copy; never original candidate/frozen tmp."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path

REVIEW = Path("/tmp/opensip-implementation/m1-grok-checker-mode-selection-v1-review/review")
LIVE = Path("/Users/sb/code/opensip-ai/opensip")
P = REVIEW / "copy" / "frozen-subject" / "product"
C = P / "tools/typescript-boundary"
B = REVIEW / "probes" / "check-work"
NODE = "/Users/sb/.nvm/versions/node/v24.16.0/bin/node"
NPM = "/Users/sb/.nvm/versions/node/v24.16.0/lib/node_modules/npm/bin/npm-cli.js"
CACHE = "/tmp/opensip-implementation/m1-typescript-bootstrap-candidate-01/provision-cache"
BIN_SHA = "76e31fbe92ce1586dea6be365b6a3e77d61dbf7e48e2a72dae683d728eff10f1"


def mode_octal(path: Path) -> str:
    return format(stat.S_IMODE(path.stat().st_mode), "04o")


def main() -> None:
    if not sys.flags.isolated or sys.flags.optimize:
        raise SystemExit("isolated Python without optimization required")
    if B.exists():
        shutil.rmtree(B)
    B.mkdir(parents=True)
    logs = REVIEW / "results" / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    checker = C / "bin/check-boundary.mjs"
    live = LIVE / "tools/typescript-boundary/bin/check-boundary.mjs"
    if checker.read_bytes() != live.read_bytes():
        raise SystemExit("runtime bytes changed vs live")
    if hashlib.sha256(checker.read_bytes()).hexdigest() != BIN_SHA:
        raise SystemExit("checker sha mismatch")
    if mode_octal(checker) != "0755":
        raise SystemExit("private copy checker not 0755: " + mode_octal(checker))
    old = json.loads((LIVE / "tools/typescript-boundary/tests/fixtures/staging-map.json").read_bytes())
    new = json.loads((C / "tests/fixtures/staging-map.json").read_bytes())
    changes = [(x, y) for x, y in zip(old["files"], new["files"]) if x != y]
    if not (len(old["files"]) == len(new["files"]) and len(changes) == 1 and changes[0][0]["path"] == "tests/support/cli-invocations.mjs"):
        raise SystemExit("staging-map change is not exactly one cli-invocations row")
    node_ver = subprocess.check_output([NODE, "--version"], text=True).strip()
    npm_ver = subprocess.check_output([NODE, NPM, "--version"], text=True).strip()
    env = dict(os.environ)
    env["PATH"] = str(Path(NODE).parent) + ":/usr/bin:/bin"
    env.pop("NODE_OPTIONS", None)
    commands = []

    def run(name, cmd, cwd, expected=0):
        r = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, timeout=300)
        (logs / f"{name}.stdout").write_bytes(r.stdout)
        (logs / f"{name}.stderr").write_bytes(r.stderr)
        commands.append({"name": name, "command": cmd, "exitCode": r.returncode, "expectedExitCode": expected})
        if r.returncode != expected:
            raise SystemExit(f"{name} exit {r.returncode} expected {expected}\n{r.stderr[-2000:]}\n{r.stdout[-2000:]}")
        print(name, "passed", flush=True)
        return r

    run("provision", [NODE, NPM, "ci", "--offline", "--ignore-scripts", "--no-audit", "--no-fund", "--cache", CACHE], C)
    if mode_octal(checker) != "0755":
        raise SystemExit("npm ci stripped execute bit: " + mode_octal(checker))
    run("regression234", [NODE, "tests/run.mjs"], C)
    N = B / "negative-checker"
    shutil.copytree(C, N, ignore=shutil.ignore_patterns("node_modules"))
    (N / "node_modules").symlink_to(C / "node_modules", target_is_directory=True)
    (N / "bin/check-boundary.mjs").chmod(0o644)
    if mode_octal(N / "bin/check-boundary.mjs") != "0644":
        raise SystemExit("negative copy not 0644")
    if mode_octal(checker) != "0755":
        raise SystemExit("chmod leaked onto 0755 copy")
    f = N / "tests/run.mjs"
    t = f.read_text().replace("'--test-concurrency=1', ...tests", "'--test-concurrency=1', '--test-name-pattern=real CLI invocations', ...tests")
    if "test-name-pattern" not in t:
        raise SystemExit("failed to filter negative tests")
    f.write_text(t)
    r = run("negative-no-execute", [NODE, "tests/run.mjs"], N, 1)
    combined = r.stdout + r.stderr
    if b"EACCES" not in combined:
        raise SystemExit("negative missing EACCES")
    if b"TypeError" in combined:
        raise SystemExit("negative has TypeError")
    result = {
        "nodeVersion": node_ver,
        "npmVersion": npm_ver,
        "runtimeBytesUnchanged": True,
        "executableModeAfterProvision": mode_octal(checker),
        "negativeMode": "0644",
        "commands": commands,
        "stagingRowsChanged": 1,
        "executedAgainstOriginalCandidate": False,
        "executedAgainstFrozenTmp": False,
    }
    (REVIEW / "results" / "run-checks.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: result[k] for k in ("nodeVersion", "npmVersion", "executableModeAfterProvision", "negativeMode")}, indent=2))


if __name__ == "__main__":
    main()
