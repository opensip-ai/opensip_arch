#!/usr/bin/env python3
import hashlib, json, lzma, os, subprocess, sys, threading

def sha_stream(path):
    h = hashlib.sha256(); n = 0
    with open(path, "rb") as f:
        while True:
            b = f.read(1 << 20)
            if not b:
                break
            h.update(b); n += len(b)
    return n, h.hexdigest()

def pump(path, harness):
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
    with lzma.open(path, "rb") as src:
        while True:
            line = src.readline()
            if not line:
                break
            h.update(line); n += len(line)
            proc.stdin.write(line)
            lines += 1
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

def classify_context(value):
    if value.get("result") != "error":
        return value
    err = value.get("error", "")
    if "MissingBlob" in err:
        return {"result": "unavailable"}
    if "Limit" in err:
        return {"result": "limit"}
    if "Unsupported" in err:
        return {"result": "unsupported"}
    return {"result": "invalid"}

def main():
    root, harness, out = sys.argv[1], sys.argv[2], sys.argv[3]
    report = {}
    print("replay case15", flush=True)
    xz = os.path.join(root, "case15-requests.ndjson.xz")
    pin = json.load(open(os.path.join(root, "case15-result.json")))
    zn, zh = sha_stream(xz)
    got = pump(xz, harness)
    expected = [json.loads(x) for x in open(os.path.join(root, "case15-expected.ndjson"))]
    actual = [json.loads(x) for x in got["stdout"].splitlines()]
    miss = sum(1 for e, a in zip(expected, actual) if e != a) + abs(len(expected) - len(actual))
    report["case15"] = {
        "ok": got["exitCode"] == 0 and miss == 0 and actual and actual[0].get("count") == 1112064 and actual[0].get("sha256") == pin["singleScalarDigest"]["sha256"],
        "exitCode": got["exitCode"],
        "lines": got["lines"],
        "rawBytes": got["rawBytes"],
        "rawSha256": got["rawSha256"],
        "xzBytes": zn,
        "xzSha256": zh,
        "mismatchCount": miss,
        "scalarCount": actual[0].get("count") if actual else None,
        "scalarDigest": actual[0].get("sha256") if actual else None,
        "stderrBytes": len(got["stderr"]),
        "identicalToFinalActual": got["stdout"] == open(os.path.join(root, "case15-final-actual.ndjson"), "rb").read() if os.path.exists(os.path.join(root, "case15-final-actual.ndjson")) else None,
        "identicalToPriorActual": got["stdout"] == open(os.path.join(root, "case15-actual.ndjson"), "rb").read() if os.path.exists(os.path.join(root, "case15-actual.ndjson")) else None,
    }
    print(json.dumps(report["case15"]), flush=True)

    print("replay native-context", flush=True)
    xz = os.path.join(root, "native-context-requests.ndjson.xz")
    corpora = {row["compressed"]["path"]: row for row in json.load(open(os.path.join(root, "corpora.json"))) } if os.path.exists(os.path.join(root, "corpora.json")) else {}
    zn, zh = sha_stream(xz)
    got = pump(xz, harness)
    expected = [json.loads(x) for x in open(os.path.join(root, "native-context-expected.ndjson"))]
    actual = [json.loads(x) for x in got["stdout"].splitlines()]
    miss = []
    for i, (e, a) in enumerate(zip(expected, actual)):
        if classify_context(a) != e:
            miss.append({"index": i, "expected": e, "actual": a})
            if len(miss) >= 8:
                break
    extra = abs(len(expected) - len(actual))
    domains = {}
    for e in expected:
        if e.get("result") == "checked":
            domains[e.get("domain")] = domains.get(e.get("domain"), 0) + 1
    pin = corpora.get("native-context-requests.ndjson.xz")
    report["native-context"] = {
        "ok": got["exitCode"] == 0 and not miss and extra == 0 and (not pin or (got["rawBytes"] == pin["raw"]["bytes"] and got["rawSha256"] == pin["raw"]["sha256"])),
        "exitCode": got["exitCode"],
        "lines": got["lines"],
        "rawBytes": got["rawBytes"],
        "rawSha256": got["rawSha256"],
        "xzBytes": zn,
        "xzSha256": zh,
        "checked": sum(1 for e in expected if e.get("result") == "checked"),
        "nativeRefused": sum(1 for e in expected if e.get("refusals")),
        "checkedDomains": domains,
        "mismatchCount": len(miss) + extra,
        "mismatchesHead": miss,
        "stderrBytes": len(got["stderr"]),
        "identicalToFinalActual": got["stdout"] == open(os.path.join(root, "native-context-final-actual.ndjson"), "rb").read() if os.path.exists(os.path.join(root, "native-context-final-actual.ndjson")) else None,
    }
    print(json.dumps({k: v for k, v in report["native-context"].items() if k != "mismatchesHead"}), flush=True)
    open(out, "w").write(json.dumps(report, indent=2) + "\n")
    if not all(v.get("ok") for v in report.values()):
        sys.exit(1)

if __name__ == "__main__":
    main()
