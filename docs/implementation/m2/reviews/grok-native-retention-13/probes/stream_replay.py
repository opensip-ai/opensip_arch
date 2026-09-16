#!/usr/bin/env python3
import hashlib, json, os, subprocess, sys, threading

def pump(path, harness):
    proc = subprocess.Popen([harness], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
    with open(path, "rb") as src:
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

def classify(value):
    if value.get("result") != "error":
        return value
    err = value.get("error", "")
    if "MissingBlob" in err or "MissingObject" in err:
        return {"result": "unavailable"}
    if "Limit" in err:
        return {"result": "limit"}
    if "Unsupported" in err:
        return {"result": "unsupported"}
    return {"result": "invalid"}

def main():
    root, harness, out = sys.argv[1], sys.argv[2], sys.argv[3]
    req = os.path.join(root, "native-retention-requests.ndjson")
    expected = [json.loads(x) for x in open(os.path.join(root, "native-retention-expected.ndjson"))]
    got = pump(req, harness)
    actual = [json.loads(x) for x in got["stdout"].splitlines()]
    miss = []
    for i, (e, a) in enumerate(zip(expected, actual)):
        if classify(a) != e:
            miss.append({"index": i, "expected": e, "actual": a})
            if len(miss) >= 8:
                break
    extra = abs(len(expected) - len(actual))
    pin = json.load(open(os.path.join(root, "native-retention-result.json")))
    report = {
        "ok": got["exitCode"] == 0 and not miss and extra == 0 and len(expected) == pin["cases"],
        "exitCode": got["exitCode"],
        "lines": got["lines"],
        "rawBytes": got["rawBytes"],
        "rawSha256": got["rawSha256"],
        "checked": sum(1 for e in expected if e.get("result") == "checked"),
        "invalid": sum(1 for e in expected if e.get("result") == "invalid"),
        "unavailable": sum(1 for e in expected if e.get("result") == "unavailable"),
        "limit": sum(1 for e in expected if e.get("result") == "limit"),
        "mismatchCount": len(miss) + extra,
        "mismatchesHead": miss,
        "identicalToPriorActual": got["stdout"] == open(os.path.join(root, "native-retention-actual.ndjson"), "rb").read(),
        "stderrBytes": len(got["stderr"]),
    }
    open(out, "w").write(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != "mismatchesHead"}))
    if not report["ok"]:
        sys.exit(1)

if __name__ == "__main__":
    main()
