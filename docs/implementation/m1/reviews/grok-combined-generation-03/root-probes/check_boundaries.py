"""Independent Node/native boundary probes against this review's generation-01 profiles."""
from pathlib import Path
import json
import os
import subprocess
import sys
import tempfile

REV = Path("/tmp/opensip-implementation/m1-root-generator03-reproduction")
GEN = REV / "generation-01"
OUT = REV / "results"
rows = []
secret = OUT / "outside-secret.txt"
secret.write_text("secret-value\n")
outside_write = OUT / "outside-escape.txt"
if outside_write.exists():
    outside_write.unlink()


def check(name, passed, detail=""):
    rows.append({"name": name, "passed": bool(passed), "detail": str(detail)[:500]})
    print(("PASS" if passed else "FAIL"), name, str(detail)[:200])


node = GEN / "tool-node"
py = "/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/Resources/Python.app/Contents/MacOS/Python"
env = {"HOME": str(GEN / "home"), "PATH": "/usr/bin:/bin", "LANG": "C", "LC_ALL": "C", "TZ": "UTC"}

# Node validation profile (same grants as generate_all validate step).
node_programs = [
    (
        "node-outside-read",
        f'const fs=require("node:fs"); try{{fs.readFileSync({json.dumps(str(secret))});process.exit(9)}}catch(e){{if(e.code!=="EPERM")throw e;console.log("refused")}}',
    ),
    (
        "node-outside-write",
        f'const fs=require("node:fs"); try{{fs.writeFileSync({json.dumps(str(outside_write))},"escape");process.exit(9)}}catch(e){{if(e.code!=="EPERM")throw e;console.log("refused")}}',
    ),
    (
        "node-network",
        'const s=require("node:net").connect({host:"127.0.0.1",port:9});s.on("connect",()=>process.exit(9));s.on("error",e=>{if(e.code!=="EPERM")throw e;console.log("refused")})',
    ),
    (
        "node-child-shell",
        'const p=require("node:child_process").spawnSync("/bin/sh",["-c","exit 0"]);if(!p.error||p.error.code!=="EPERM")throw Error(JSON.stringify(p));console.log("refused")',
    ),
    (
        "node-allowed-scratch",
        f'require("node:fs").writeFileSync({json.dumps(str(GEN/"runtime/control-independent.txt"))},"owned");console.log("allowed")',
    ),
]
for name, program in node_programs:
    p = subprocess.run(
        ["/usr/bin/sandbox-exec", "-f", str(GEN / "validate-profile.sb"), str(node), "-e", program],
        cwd=GEN / "runtime",
        env=env,
        capture_output=True,
        timeout=15,
    )
    ok = p.returncode == 0 and b"refused" in p.stdout or (name.endswith("scratch") and p.returncode == 0 and b"allowed" in p.stdout)
    if name.endswith("scratch"):
        ok = p.returncode == 0 and b"allowed" in p.stdout and (GEN / "runtime/control-independent.txt").read_text() == "owned"
    else:
        ok = p.returncode == 0 and p.stdout.strip() == b"refused"
    check(name, ok, f"exit={p.returncode} stdout={p.stdout!r} stderr={p.stderr[:200]!r}")
check("node-outside-write-absent", not outside_write.exists())

# Native python profile.
native_sb = GEN / "native-python-profile.sb"
lane = GEN / "native-work"
native_cases = [
    (
        "native-unselected-stdlib",
        "import sqlite3",
        False,
    ),
    (
        "native-site-module-absent",
        "import site",
        False,
    ),
    (
        "native-network",
        "import socket; s=socket.socket(); s.connect(('127.0.0.1', 9))",
        False,
    ),
    (
        "native-outside-read",
        f"open({secret.as_posix()!r}).read()",
        False,
    ),
    (
        "native-allowed-output",
        f"open({(lane/'control-independent.txt').as_posix()!r},'w').write('owned')",
        True,
    ),
]
for name, program, allowed in native_cases:
    p = subprocess.run(
        ["/usr/bin/sandbox-exec", "-f", str(native_sb), py, "-I", "-B", "-S", "-c", program],
        cwd=GEN / "runtime",
        env=env,
        capture_output=True,
        timeout=15,
    )
    if allowed:
        ok = p.returncode == 0 and (lane / "control-independent.txt").read_text() == "owned"
    else:
        ok = p.returncode != 0
    check(name, ok, f"exit={p.returncode} stderr={p.stderr[-300:]!r}")

# Ambient home/site: child env has no PYTHONPATH; isolated -S.
p = subprocess.run(
    [
        "/usr/bin/sandbox-exec",
        "-f",
        str(native_sb),
        py,
        "-I",
        "-B",
        "-S",
        "-c",
        "import sys,os; print(os.environ.get('PYTHONPATH')); print(any('site-packages' in p for p in sys.path))",
    ],
    cwd=GEN / "runtime",
    env=env,
    capture_output=True,
    timeout=15,
    text=True,
)
check(
    "native-no-ambient-site-path",
    p.returncode == 0 and "True" not in p.stdout.splitlines()[-1:] and (p.stdout.splitlines()[0] in ("None", "")),
    p.stdout,
)

failed = [r["name"] for r in rows if not r["passed"]]
(OUT / "boundary-independent.json").write_text(json.dumps({"caseCount": len(rows), "failedCount": len(failed), "failed": failed, "cases": rows}, indent=2) + "\n")
print(json.dumps({"caseCount": len(rows), "failedCount": len(failed), "failed": failed}))
if failed:
    raise SystemExit(1)
