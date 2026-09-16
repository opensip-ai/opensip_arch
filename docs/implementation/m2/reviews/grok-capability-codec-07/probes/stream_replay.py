#!/usr/bin/env python3
"""Stream xz ndjson into the harness without buffering uncompressed corpora."""
import hashlib, json, lzma, os, subprocess, sys, threading
from collections import Counter

def sha_stream(path):
    h = hashlib.sha256(); n = 0
    with open(path, "rb") as f:
        while True:
            b = f.read(1 << 20)
            if not b:
                break
            h.update(b); n += len(b)
    return n, h.hexdigest()

def pump(gz_open, path, harness):
    proc = subprocess.Popen(
        [harness], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    out_buf, err_buf = [], []
    def _read(stream, bag):
        while True:
            block = stream.read(1 << 16)
            if not block:
                break
            bag.append(block)
    t_out = threading.Thread(target=_read, args=(proc.stdout, out_buf), daemon=True)
    t_err = threading.Thread(target=_read, args=(proc.stderr, err_buf), daemon=True)
    t_out.start(); t_err.start()
    h = hashlib.sha256(); n = 0; lines = 0
    with gz_open(path, "rb") as src:
        while True:
            line = src.readline()
            if not line:
                break
            h.update(line); n += len(line)
            proc.stdin.write(line)
            lines += 1
            if lines % 20000 == 0:
                print(f"  streamed {lines} / {n}", flush=True)
    proc.stdin.close()
    t_out.join(); t_err.join(); proc.wait()
    return {
        "exitCode": proc.returncode,
        "rawBytes": n,
        "rawSha256": h.hexdigest(),
        "lines": lines,
        "stdout": b"".join(out_buf),
        "stderr": b"".join(err_buf),
    }

def main():
    root, harness, out = sys.argv[1], sys.argv[2], sys.argv[3]
    pins = {row["compressed"]["path"]: row for row in json.load(open(os.path.join(root, "corpora.json")))}
    report = {}
    # CVE1 exact text
    print("replay cve1", flush=True)
    cve = pins["cve1-requests.ndjson.xz"]
    xz = os.path.join(root, "cve1-requests.ndjson.xz")
    zn, zh = sha_stream(xz)
    got = pump(lzma.open, xz, harness)
    expected = open(os.path.join(root, "cve1-expected.txt"), "rb").read()
    actual = got["stdout"]
    report["cve1"] = {
        "ok": got["exitCode"] == 0 and actual == expected and got["rawBytes"] == cve["raw"]["bytes"] and got["rawSha256"] == cve["raw"]["sha256"] and zn == cve["compressed"]["bytes"] and zh == cve["compressed"]["sha256"],
        "exitCode": got["exitCode"],
        "lines": got["lines"],
        "rawBytes": got["rawBytes"],
        "rawSha256": got["rawSha256"],
        "xzBytes": zn,
        "xzSha256": zh,
        "textMatch": actual == expected,
        "rawPinMatch": got["rawBytes"] == cve["raw"]["bytes"] and got["rawSha256"] == cve["raw"]["sha256"],
        "counts": dict(Counter(actual.decode().splitlines())),
        "stderrBytes": len(got["stderr"]),
    }
    print(json.dumps({k: v for k, v in report["cve1"].items() if k != "counts"} | {"accepted": report["cve1"]["counts"].get("invalid", None), "okLines": sum(1 for x in actual.decode().splitlines() if x.startswith("ok:"))}), flush=True)
    # capability parsed JSON
    print("replay capability", flush=True)
    cap = pins["capability-requests.ndjson.xz"]
    xz = os.path.join(root, "capability-requests.ndjson.xz")
    zn, zh = sha_stream(xz)
    got = pump(lzma.open, xz, harness)
    expected_lines = open(os.path.join(root, "capability-expected.ndjson")).read().splitlines()
    actual_lines = got["stdout"].decode().splitlines()
    mismatches = []
    admit = refuse = 0
    for i, (e, a) in enumerate(zip(expected_lines, actual_lines)):
        ev, av = json.loads(e), json.loads(a)
        if ev.get("result") == "ADMIT":
            admit += 1
        else:
            refuse += 1
        if ev != av:
            mismatches.append({"index": i, "expected": ev, "actual": av})
            if len(mismatches) >= 10:
                break
    extra = abs(len(expected_lines) - len(actual_lines))
    report["capability"] = {
        "ok": got["exitCode"] == 0 and not mismatches and extra == 0 and got["rawBytes"] == cap["raw"]["bytes"] and got["rawSha256"] == cap["raw"]["sha256"] and zn == cap["compressed"]["bytes"] and zh == cap["compressed"]["sha256"],
        "exitCode": got["exitCode"],
        "lines": got["lines"],
        "rawBytes": got["rawBytes"],
        "rawSha256": got["rawSha256"],
        "xzBytes": zn,
        "xzSha256": zh,
        "admit": admit,
        "refuse": refuse + extra,
        "mismatchCount": len(mismatches) + extra,
        "mismatchesHead": mismatches,
        "rawPinMatch": got["rawBytes"] == cap["raw"]["bytes"] and got["rawSha256"] == cap["raw"]["sha256"],
        "stderrBytes": len(got["stderr"]),
    }
    print(json.dumps({k: v for k, v in report["capability"].items() if k != "mismatchesHead"}), flush=True)
    open(out, "w").write(json.dumps(report, indent=2) + "\n")
    if not all(v.get("ok") for v in report.values()):
        sys.exit(1)

if __name__ == "__main__":
    main()
