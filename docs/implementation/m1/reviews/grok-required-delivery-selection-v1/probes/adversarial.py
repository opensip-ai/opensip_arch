"""Real CLI write/flush observations on the private-built binary."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

REVIEW = Path("/tmp/opensip-implementation/m1-grok-required-delivery-selection-v1-review/review")
PRODUCT = REVIEW / "copy" / "frozen-subject" / "product"
TARGET = REVIEW / "probes" / "ws-target"
MSG = b"OUTPUT.SERIALIZATION_FAILED: required output emission failed.\n"
SAFE_PATH = "/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin:/usr/sbin:/sbin"


def run(exe: Path, args: list[str], stdout) -> subprocess.CompletedProcess:
    env = {
        "HOME": os.environ["HOME"],
        "PATH": SAFE_PATH,
        "TERM": "dumb",
        "TMPDIR": "/tmp/osip-rdlv",
    }
    return subprocess.run(
        [str(exe), *args],
        cwd=PRODUCT,
        env=env,
        stdout=stdout,
        stderr=subprocess.PIPE,
        timeout=30,
    )


def main() -> None:
    if not sys.flags.isolated or sys.flags.optimize:
        raise SystemExit("isolated Python without optimization required")
    bins = list(TARGET.glob("debug/opensip")) + list(TARGET.glob("debug/deps/opensip-*"))
    exe = TARGET / "debug" / "opensip"
    if not exe.is_file():
        raise SystemExit("opensip binary missing: " + str(exe) + " found " + str(bins[:5]))
    readonly = PRODUCT / "package.json"
    rows = []

    def record(name, proc, expect_code, expect_stderr=None, stdout_empty=None, stdout_has=None):
        ok = proc.returncode == expect_code
        if expect_stderr is not None:
            ok = ok and proc.stderr == expect_stderr
        if stdout_empty is True:
            ok = ok and (proc.stdout in (b"", None))
        if stdout_has is not None:
            ok = ok and stdout_has.encode() in (proc.stdout or b"")
        rows.append({
            "name": name,
            "code": proc.returncode,
            "expectCode": expect_code,
            "stderr": proc.stderr.decode("utf-8", "replace")[:200],
            "stdoutLen": 0 if proc.stdout is None else len(proc.stdout),
            "pass": ok,
        })

    ok = run(exe, ["version", "--format=json"], subprocess.PIPE)
    record("version-json-success", ok, 0, stdout_has="termination")
    human = run(exe, ["help"], subprocess.PIPE)
    record("help-human-success", human, 0, stdout_has="Termination: success")
    comp = run(exe, ["completion", "bash"], subprocess.PIPE)
    record("completion-bash-success", comp, 0, stdout_has="Termination: success")
    fail = subprocess.run(
        [str(exe), "version", "--format=json"],
        cwd=PRODUCT,
        env={"HOME": os.environ["HOME"], "PATH": SAFE_PATH, "TERM": "dumb"},
        stdout=open(readonly, "rb"),
        stderr=subprocess.PIPE,
        timeout=30,
    )
    # reopen as read-only fd: File.open rb used as stdout may still be readable;
    # the child inherits a read-only fd 1. Matches startup test.
    record(
        "readonly-stdout-json",
        fail,
        4,
        expect_stderr=MSG,
        stdout_empty=True,
    )
    fail_h = subprocess.run(
        [str(exe), "version"],
        cwd=PRODUCT,
        env={"HOME": os.environ["HOME"], "PATH": SAFE_PATH, "TERM": "dumb"},
        stdout=open(readonly, "rb"),
        stderr=subprocess.PIPE,
        timeout=30,
    )
    record("readonly-stdout-human", fail_h, 4, expect_stderr=MSG)
    # Closed-pipe: write to a pipe whose reader is gone.
    r_fd, w_fd = os.pipe()
    os.close(r_fd)
    pipe = subprocess.run(
        [str(exe), "version", "--format=json"],
        cwd=PRODUCT,
        env={"HOME": os.environ["HOME"], "PATH": SAFE_PATH, "TERM": "dumb"},
        stdout=w_fd,
        stderr=subprocess.PIPE,
        timeout=30,
    )
    os.close(w_fd)
    record("broken-pipe-stdout", pipe, 4, expect_stderr=MSG)
    no_second = (b"{" not in pipe.stderr) and (b"schemaVersion" not in pipe.stderr)
    rows.append({"name": "no-envelope-on-stderr", "pass": no_second and fail.stderr == MSG})
    success_no_fail_text = b"OUTPUT.SERIALIZATION_FAILED" not in ok.stdout
    rows.append({"name": "success-payload-has-no-failure-text", "pass": success_no_fail_text})
    out = {
        "binary": str(exe),
        "rows": rows,
        "allPass": all(r["pass"] for r in rows),
        "failed": [r["name"] for r in rows if not r["pass"]],
    }
    (REVIEW / "results" / "adversarial.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"allPass": out["allPass"], "failed": out["failed"], "rows": rows}, indent=2))


if __name__ == "__main__":
    main()
