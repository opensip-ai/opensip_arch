"""Adapted capture controls. Does not write into the freeze or copy evidence files."""
from pathlib import Path
import importlib.util
import json
import os
import signal
import sys
import time

OUT = Path("/tmp/opensip-implementation/m1-grok-combined-generation-review-03/review/results")
COPY = Path("/tmp/opensip-implementation/m1-grok-combined-generation-review-03/review/copy")
spec = importlib.util.spec_from_file_location("confine", COPY / "tools/contracts/confine.py")
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)
py = sys.executable
rows = []
for name, program, expected in [
    ("both-streams", 'import os; os.write(1,b"out"); os.write(2,b"err")', None),
    ("stdout-cap", 'import os; os.write(1,b"x"*2048)', "child combined log byte limit exceeded"),
    ("stderr-cap", 'import os; os.write(2,b"x"*2048)', "child combined log byte limit exceeded"),
    ("shared-cap", 'import os; os.write(1,b"x"*700); os.write(2,b"y"*700)', "child combined log byte limit exceeded"),
    ("time-bound", "while True: pass", "child time limit exceeded"),
    ("closed-pipes-time-bound", "import os; os.close(1); os.close(2)\nwhile True: pass", "child time limit exceeded"),
]:
    start = time.monotonic()
    status, out, err, failure = c.capture_child(
        [py, "-I", "-B", "-S", "-c", program],
        cwd=OUT,
        env={},
        timeout=0.5,
        max_bytes=1024,
    )
    assert failure == expected, (name, status, failure)
    assert len(out) + len(err) <= 1024
    if name == "both-streams":
        assert status == 0 and out == b"out" and err == b"err"
    else:
        assert status != 0
    rows.append(
        {
            "name": name,
            "passed": True,
            "exit": status,
            "stdoutBytes": len(out),
            "stderrBytes": len(err),
            "failure": failure,
            "seconds": time.monotonic() - start,
        }
    )

# Independent: grandchild in the same process group must die on timeout.
program = r"""
import os, time, pathlib, sys
path = pathlib.Path(sys.argv[1])
child = os.fork()
if child == 0:
    while True:
        time.sleep(0.05)
path.write_text(str(child))
while True:
    time.sleep(0.05)
"""
marker = OUT / "grandchild.pid"
if marker.exists():
    marker.unlink()
status, out, err, failure = c.capture_child(
    [py, "-I", "-B", "-S", "-c", program, str(marker)],
    cwd=OUT,
    env={},
    timeout=0.6,
    max_bytes=1024,
)
dead = False
if marker.exists():
    gpid = int(marker.read_text().strip())
    try:
        os.kill(gpid, 0)
        alive = True
    except ProcessLookupError:
        alive = False
    dead = not alive
else:
    gpid = None
    dead = True  # never spawned; still a timeout kill
rows.append(
    {
        "name": "grandchild-same-group-killed",
        "passed": failure == "child time limit exceeded" and status != 0 and dead,
        "exit": status,
        "failure": failure,
        "grandchildPid": gpid,
        "grandchildDead": dead,
    }
)
assert rows[-1]["passed"], rows[-1]

# Independent: empty env, no ambient PYTHONPATH/HOME in the child.
program = 'import os,sys; sys.stdout.buffer.write(repr({k:os.environ.get(k) for k in ["HOME","PYTHONPATH","PATH","PYTHONHOME"]}).encode())'
status, out, err, failure = c.capture_child(
    [py, "-I", "-B", "-S", "-c", program], cwd=OUT, env={"PATH": "/usr/bin:/bin"}, timeout=5, max_bytes=4096
)
env = eval(out.decode()) if status == 0 else None
rows.append(
    {
        "name": "child-env-is-only-what-parent-passed",
        "passed": status == 0 and failure is None and env == {"HOME": None, "PYTHONPATH": None, "PATH": "/usr/bin:/bin", "PYTHONHOME": None},
        "env": env,
        "exit": status,
        "failure": failure,
    }
)
assert rows[-1]["passed"], rows[-1]

(OUT / "capture-controls-independent.json").write_text(json.dumps({"cases": rows}, indent=2) + "\n")
print(json.dumps({"passed": True, "cases": len(rows)}))
