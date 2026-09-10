"""Run the five foundation sub-checks directly, without the wrapper's 120s timeout.

Establishes whether the foundation unit genuinely passes on these exact bytes, and
whether each sub-report regenerates byte-identically to the frozen copy.
"""
import hashlib
import json
import os
import subprocess
import sys
import time

COPY = sys.argv[1]
OUT = sys.argv[2]
H = os.path.join(COPY, "docs/coop/design-corrections/foundation")
PAIRS = [
    ("check-foundation.py", "foundation-report.json"),
    ("check-identity.py", "identity-report.json"),
    ("check-product-quality.py", "product-quality-report.json"),
    ("check-product-configuration.py", "product-configuration-report.json"),
    ("check-array-orders.py", "array-order-report.json"),
]

res = []
for script, report in PAIRS:
    frozen = hashlib.sha256(open(os.path.join(H, report), "rb").read()).hexdigest()
    tgt = os.path.join(OUT, report)
    t0 = time.monotonic()
    proc = subprocess.run(
        [
            "/tmp/opensip-architecture-review-env/bin/python",
            "-I",
            "-B",
            os.path.join(H, script),
            "--report",
            tgt,
        ],
        capture_output=True,
        text=True,
        timeout=1800,
    )
    el = time.monotonic() - t0
    regen = (
        hashlib.sha256(open(tgt, "rb").read()).hexdigest()
        if os.path.isfile(tgt)
        else None
    )
    res.append(
        {
            "script": script,
            "exitCode": proc.returncode,
            "elapsedSeconds": round(el, 2),
            "exceedsWrapperTimeout": el > 120,
            "frozenReportSha256": frozen,
            "regeneratedReportSha256": regen,
            "reportByteIdentical": regen == frozen,
            "stdout": proc.stdout.strip()[-400:],
            "stderr": proc.stderr.strip()[-400:],
        }
    )
    print(
        f"{script}: exit={proc.returncode} {el:.1f}s identical={regen == frozen}",
        flush=True,
    )

json.dump(
    {
        "allExitZero": all(r["exitCode"] == 0 for r in res),
        "allReportsIdentical": all(r["reportByteIdentical"] for r in res),
        "overWrapperTimeout": [
            r["script"] for r in res if r["exceedsWrapperTimeout"]
        ],
        "checks": res,
    },
    open(os.path.join(OUT, "foundation-subchecks.json"), "w"),
    indent=2,
)
