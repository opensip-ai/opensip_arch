#!/usr/bin/env python3
"""Stream gzip ndjson into the harness without buffering the uncompressed corpus."""
import gzip, hashlib, json, os, subprocess, sys, threading

def replay(gz_path, expected_path, harness, pin):
    h = hashlib.sha256()
    raw_bytes = 0
    lines = 0
    expected = open(expected_path, "r", encoding="ascii").read().splitlines()
    proc = subprocess.Popen(
        [harness],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    def _read(stream, bag):
        while True:
            block = stream.read(1 << 16)
            if not block:
                break
            bag.append(block)
    stdout_buf, stderr_buf = [], []
    t_out = threading.Thread(target=_read, args=(proc.stdout, stdout_buf), daemon=True)
    t_err = threading.Thread(target=_read, args=(proc.stderr, stderr_buf), daemon=True)
    t_out.start()
    t_err.start()
    mismatches = []
    with gzip.open(gz_path, "rb") as src:
        while True:
            line = src.readline()
            if not line:
                break
            h.update(line)
            raw_bytes += len(line)
            proc.stdin.write(line)
            lines += 1
            if lines % 5000 == 0:
                print(f"  streamed {lines} lines / {raw_bytes} bytes", flush=True)
    proc.stdin.close()
    t_out.join()
    t_err.join()
    proc.wait()
    stdout = b"".join(stdout_buf)
    stderr = b"".join(stderr_buf)
    actual = stdout.decode("ascii").splitlines()
    if proc.returncode != 0:
        return {
            "ok": False,
            "exitCode": proc.returncode,
            "stderr": stderr[:500].decode("utf-8", "replace"),
            "lines": lines,
        }
    for i, (e, a) in enumerate(zip(expected, actual)):
        if e != a:
            mismatches.append({"index": i, "expected": e, "actual": a})
            if len(mismatches) >= 20:
                break
    from collections import Counter
    result = {
        "ok": actual == expected and raw_bytes == pin["bytes"] and h.hexdigest() == pin["sha256"],
        "exitCode": proc.returncode,
        "lines": lines,
        "expectedLines": len(expected),
        "rawBytes": raw_bytes,
        "pinBytes": pin["bytes"],
        "sha256": h.hexdigest(),
        "pinSha256": pin["sha256"],
        "shaMatch": h.hexdigest() == pin["sha256"],
        "bytesMatch": raw_bytes == pin["bytes"],
        "outcomeMatch": actual == expected,
        "counts": dict(Counter(actual)),
        "mismatchCount": sum(1 for e, a in zip(expected, actual) if e != a) + abs(len(actual) - len(expected)),
        "mismatchesHead": mismatches,
        "stderrBytes": len(stderr),
    }
    return result

def main():
    root, harness, out = sys.argv[1], sys.argv[2], sys.argv[3]
    pins = {r["rawPath"]: r for r in json.load(open(os.path.join(root, "compressed-corpora.json")))}
    frozen = "/tmp/opensip-implementation/m2-retained-graph-trial-06"
    jobs = [
        ("law-requests.ndjson.gz", "law-expected.txt", "law-requests.ndjson"),
        ("source-requests.ndjson.gz", "source-expected.txt", "source-requests.ndjson"),
        ("relation-requests.ndjson.gz", "relation-expected.txt", "relation-requests.ndjson"),
    ]
    report = {}
    for gz_name, exp_name, raw_name in jobs:
        print("replay", gz_name, flush=True)
        report[raw_name] = replay(
            os.path.join(frozen, gz_name),
            os.path.join(root, exp_name),
            harness,
            pins[raw_name],
        )
        print(json.dumps(report[raw_name]), flush=True)
    # predecessor 4441 from payloads05 frozen requests
    p05 = "/tmp/opensip-implementation/m2-grok-retained-payloads-review-05/review/subject/payload-requests.ndjson"
    exp = os.path.join(frozen, "payload-predecessor-actual.txt")
    print("replay predecessor", flush=True)
    proc = subprocess.run([harness], stdin=open(p05, "rb"), capture_output=True)
    actual = proc.stdout
    expected = open(exp, "rb").read()
    report["payload-predecessor"] = {
        "ok": proc.returncode == 0 and actual == expected,
        "exitCode": proc.returncode,
        "bytes": len(actual),
        "match": actual == expected,
    }
    print(json.dumps(report["payload-predecessor"]), flush=True)
    open(out, "w").write(json.dumps(report, indent=2) + "\n")
    if not all(v.get("ok") for v in report.values()):
        sys.exit(1)

if __name__ == "__main__":
    main()
