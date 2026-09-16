"""Independent wrapper helper/refusal controls. Does not manufacture lock approvals."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

PY = Path("/tmp/opensip-implementation/metadata-reference-env/bin/python")
NODE = Path("/Users/sb/.nvm/versions/node/v24.16.0/bin/node")
ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
LIVE = Path("/Users/sb/code/opensip-ai/opensip")
REVIEW = Path("/tmp/opensip-implementation/m1-grok-bootstrap-selection-v1-review/review")
COPY = REVIEW / "copy/docs/implementation/m1/bootstrap-selection-v1/product/tools"
WRAPPER = COPY / "check_typescript.py"
TEST = COPY / "tests/test_typescript_check.py"


def main() -> None:
    if not sys.flags.isolated or sys.flags.optimize:
        raise SystemExit("isolated Python without optimization required")
    results = REVIEW / "results"
    rows = []

    def record(name, passed, detail=""):
        rows.append({"name": name, "passed": bool(passed), "detail": str(detail)[:800]})
        print(("PASS" if passed else "FAIL"), name, str(detail)[:200])

    help_p = subprocess.run([str(PY), "-I", "-B", str(WRAPPER), "--help"], capture_output=True, text=True, timeout=30)
    record("help-lists-node", help_p.returncode == 0 and "--node" in help_p.stdout)

    missing = subprocess.run(
        [str(PY), "-I", "-B", str(WRAPPER), "--architecture", str(ARCH)],
        capture_output=True, text=True, timeout=30,
    )
    record("missing-node-argparse", missing.returncode == 2 and "--node" in missing.stderr, missing.stderr[-300:])

    tests = subprocess.run([str(PY), "-I", "-B", str(TEST)], capture_output=True, text=True, timeout=60)
    record("helper-unittests", tests.returncode == 0, tests.stderr[-400:] + tests.stdout[-200:])

    # Overlay registry onto a private live-product copy; lock still lacks the registry pin.
    root = REVIEW / "probes/refusal-root"
    if root.exists():
        shutil.rmtree(root)
    shutil.copytree(
        LIVE,
        root,
        ignore=shutil.ignore_patterns(".git", "target", "node_modules", "python-packages", "__pycache__", "dist", "*.rs.bk"),
        symlinks=True,
    )
    shutil.copy2(COPY / "check_typescript.py", root / "tools/check_typescript.py")
    shutil.copy2(COPY / "typescript-lanes.json", root / "tools/typescript-lanes.json")
    refuse = subprocess.run(
        [str(PY), "-I", "-B", str(root / "tools/check_typescript.py"), "--architecture", str(ARCH), "--node", str(NODE), "--root", str(root)],
        capture_output=True, text=True, timeout=120,
    )
    err = refuse.stderr + refuse.stdout
    record(
        "live-chain-unselected-registry",
        refuse.returncode != 0 and "TypeScript lane registry is not selected exactly once" in err,
        err[-500:],
    )
    record("live-chain-no-passed-json", "registrySha256" not in (refuse.stdout or ""))

    node_pin = json.loads((COPY / "typescript-lanes.json").read_text())["node"]
    raw = NODE.read_bytes()
    record("node-pin-matches-selected", len(raw) == node_pin["bytes"] and hashlib.sha256(raw).hexdigest() == node_pin["sha256"])

    leftover = [n for n in os.listdir("/tmp") if n.startswith("opensip-typescript-check-") or n.startswith("opensip-check-")]
    record("no-wrapper-temp-leftover", leftover == [], ",".join(leftover))

    failed = [r["name"] for r in rows if not r["passed"]]
    out = {"caseCount": len(rows), "failedCount": len(failed), "failed": failed, "cases": rows}
    (results / "wrapper-controls.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({"caseCount": len(rows), "failedCount": len(failed), "failed": failed}))
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
