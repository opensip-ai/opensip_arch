"""Run output scripts sequentially under the reference interpreter, retaining every execution log.

Usage: python3 tools/seq.py <label> <script> [args...] [-- <script> [args...]]...
Each script runs as /tmp/opensip-architecture-review-env/bin/python -I -B <script> with cwd = output/. The complete stdout/stderr and exit
status are retained at output/logs/<label>.<n>.<script-stem>.log (never overwritten: an existing log name gets a numeric suffix), and the
tail is printed. Exit status is nonzero if any script failed; later scripts still run.
"""
import os
import subprocess
import sys

OUT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source43.v1/output"
REF = ["/tmp/opensip-architecture-review-env/bin/python", "-I", "-B"]


def main(argv):
    label, rest = argv[0], argv[1:]
    groups, cur = [], []
    for a in rest:
        if a == "--":
            if cur:
                groups.append(cur)
            cur = []
        else:
            cur.append(a)
    if cur:
        groups.append(cur)
    for d in ("logs", "checkpoints", "notes", "vectors", "runs", "envelopes", "traces"):
        os.makedirs(os.path.join(OUT, d), exist_ok=True)
    worst = 0
    for i, g in enumerate(groups):
        stem = os.path.splitext(os.path.basename(g[0]))[0]
        base = os.path.join(OUT, "logs", f"{label}.{i}.{stem}")
        path, k = base + ".log", 1
        while os.path.exists(path):
            path, k = f"{base}.{k}.log", k + 1
        p = subprocess.run(REF + g, capture_output=True, text=True, cwd=OUT)
        with open(path, "w") as fh:
            fh.write(f"$ {' '.join(REF + g)}\nexit {p.returncode}\n--- stdout ---\n{p.stdout}\n--- stderr ---\n{p.stderr}\n")
        tail = (p.stdout[-2500:] + ("\nSTDERR: " + p.stderr[-2500:] if p.stderr else ""))
        print(f"=== {' '.join(g)} exit {p.returncode} log {os.path.relpath(path, OUT)}\n{tail}")
        worst = worst or p.returncode
    return worst


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
