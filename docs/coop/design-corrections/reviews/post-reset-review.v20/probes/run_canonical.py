"""Reproduce the six canonical reference commands in the disposable exact copy.

No repinning: the ledgers and sources are used exactly as frozen. Records command,
exit code, elapsed, stdout/stderr digests, and the report file digest AFTER the run
so report-hash deltas versus the frozen report can be measured.
"""
import hashlib
import json
import os
import subprocess
import sys
import time

COPY = sys.argv[1]
OUT = sys.argv[2]
REF = json.load(
    open(
        os.path.join(
            COPY,
            "docs/coop/design-corrections/reviews/codex-post-reset.v1",
            "final-reference.v20/reference-checks.json",
        )
    )
)


def sha(p):
    if not os.path.isfile(p):
        return None
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def report_path(cmd):
    if "--report" in cmd:
        return cmd[cmd.index("--report") + 1]
    return None


results = []
for entry in REF["commands"]:
    cmd = list(entry["command"])
    name = entry["name"]
    rp = report_path(cmd)
    # digest of the report file as frozen, before we overwrite it
    before = sha(os.path.join(COPY, rp)) if rp else None
    src = entry["source"]
    src_actual = sha(os.path.join(COPY, src))
    t0 = time.monotonic()
    proc = subprocess.run(
        cmd, cwd=COPY, capture_output=True, timeout=1800
    )
    elapsed = time.monotonic() - t0
    after = sha(os.path.join(COPY, rp)) if rp else None
    outp = os.path.join(OUT, f"{name}.stdout")
    errp = os.path.join(OUT, f"{name}.stderr")
    open(outp, "wb").write(proc.stdout)
    open(errp, "wb").write(proc.stderr)
    results.append(
        {
            "name": name,
            "command": cmd,
            "source": src,
            "declaredSourceSha256": entry["sourceSha256"],
            "actualSourceSha256": src_actual,
            "sourcePinMatches": src_actual == entry["sourceSha256"],
            "declaredExitCode": entry["exitCode"],
            "actualExitCode": proc.returncode,
            "exitMatches": proc.returncode == entry["exitCode"],
            "elapsedSeconds": elapsed,
            "reportPath": rp,
            "reportSha256Before": before,
            "reportSha256After": after,
            "reportChanged": (before != after) if rp else None,
            "stdoutSha256": hashlib.sha256(proc.stdout).hexdigest(),
            "stderrSha256": hashlib.sha256(proc.stderr).hexdigest(),
            "stdoutBytes": len(proc.stdout),
            "stderrBytes": len(proc.stderr),
        }
    )
    print(
        f"{name}: exit={proc.returncode} (declared {entry['exitCode']}) "
        f"reportChanged={results[-1]['reportChanged']} {elapsed:.1f}s",
        flush=True,
    )

json.dump(
    {
        "copy": COPY,
        "repinned": False,
        "results": results,
        "allExitsMatch": all(r["exitMatches"] for r in results),
        "allSourcePinsMatch": all(r["sourcePinMatches"] for r in results),
        "reportsChanged": [
            r["name"] for r in results if r["reportChanged"]
        ],
    },
    open(os.path.join(OUT, "canonical-reproduction.json"), "w"),
    indent=2,
)
