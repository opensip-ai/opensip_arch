#!/usr/bin/env python3
"""Stream xz ndjson into the harness; classify Frame errors like check_native_context08.py."""
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

def normalize_plan(v):
    if v.get("result") != "error" or v.get("error") == "BytesJoin":
        return v
    if any(s in v.get("error", "") for s in ["MissingObject", "MissingBlob"]):
        return {"result": "unavailable"}
    return {"result": "invalid"}

def main():
    root, harness, out = sys.argv[1], sys.argv[2], sys.argv[3]
    pins = {row["compressed"]["path"]: row for row in json.load(open(os.path.join(root, "corpora.json")))}
    report = {}
    print("replay native-context", flush=True)
    pin = pins["native-context-requests.ndjson.xz"]
    xz = os.path.join(root, "native-context-requests.ndjson.xz")
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
    report["native-context"] = {
        "ok": got["exitCode"] == 0 and not miss and extra == 0 and got["rawBytes"] == pin["raw"]["bytes"] and got["rawSha256"] == pin["raw"]["sha256"] and zn == pin["compressed"]["bytes"] and zh == pin["compressed"]["sha256"],
        "exitCode": got["exitCode"],
        "lines": got["lines"],
        "rawBytes": got["rawBytes"],
        "rawSha256": got["rawSha256"],
        "xzMatch": zn == pin["compressed"]["bytes"] and zh == pin["compressed"]["sha256"],
        "checked": sum(1 for e in expected if e.get("result") == "checked"),
        "nativeRefused": sum(1 for e in expected if e.get("refusals")),
        "mismatchCount": len(miss) + extra,
        "mismatchesHead": miss,
        "stderrBytes": len(got["stderr"]),
    }
    print(json.dumps({k: v for k, v in report["native-context"].items() if k != "mismatchesHead"}), flush=True)

    print("replay plan-capability", flush=True)
    pin = pins["plan-capability-requests.ndjson.xz"]
    xz = os.path.join(root, "plan-capability-requests.ndjson.xz")
    zn, zh = sha_stream(xz)
    got = pump(xz, harness)
    expected = [json.loads(x) for x in open(os.path.join(root, "plan-capability-expected.ndjson"))]
    actual = [json.loads(x) for x in got["stdout"].splitlines()]
    miss = []
    for i, (e, a) in enumerate(zip(expected, actual)):
        if normalize_plan(a) != e:
            miss.append({"index": i, "expected": e, "actual": a})
            if len(miss) >= 8:
                break
    extra = abs(len(expected) - len(actual))
    report["plan-capability"] = {
        "ok": got["exitCode"] == 0 and not miss and extra == 0 and got["rawBytes"] == pin["raw"]["bytes"] and got["rawSha256"] == pin["raw"]["sha256"] and zn == pin["compressed"]["bytes"] and zh == pin["compressed"]["sha256"],
        "exitCode": got["exitCode"],
        "lines": got["lines"],
        "rawBytes": got["rawBytes"],
        "rawSha256": got["rawSha256"],
        "xzMatch": zn == pin["compressed"]["bytes"] and zh == pin["compressed"]["sha256"],
        "admit": sum(1 for e in expected if e.get("result") == "ADMIT"),
        "refuse": sum(1 for e in expected if e.get("result") == "REFUSE"),
        "bytesJoin": sum(1 for e in expected if e.get("error") == "BytesJoin"),
        "mismatchCount": len(miss) + extra,
        "mismatchesHead": miss,
        "stderrBytes": len(got["stderr"]),
    }
    print(json.dumps({k: v for k, v in report["plan-capability"].items() if k != "mismatchesHead"}), flush=True)
    open(out, "w").write(json.dumps(report, indent=2) + "\n")
    if not all(v.get("ok") for v in report.values()):
        sys.exit(1)

if __name__ == "__main__":
    main()
