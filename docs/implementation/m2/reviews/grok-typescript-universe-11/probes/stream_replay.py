#!/usr/bin/env python3
import hashlib, json, os, subprocess, sys, threading

def sha_file(path):
    h = hashlib.sha256(); n = 0
    with open(path, "rb") as f:
        while True:
            b = f.read(1 << 20)
            if not b:
                break
            h.update(b); n += len(b)
    return n, h.hexdigest()

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
    req = os.path.join(root, "typescript-universe-requests.ndjson")
    expected = [json.loads(x) for x in open(os.path.join(root, "typescript-universe-expected.ndjson"))]
    got = pump(req, harness)
    actual = [json.loads(x) for x in got["stdout"].splitlines()]
    miss = []
    for i, (e, a) in enumerate(zip(expected, actual)):
        if classify(a) != e:
            miss.append({"index": i, "expected": e, "actual": a})
            if len(miss) >= 8:
                break
    extra = abs(len(expected) - len(actual))
    pin = json.load(open(os.path.join(root, "typescript-universe-result.json")))
    topologies = 0
    with open(req, "rb") as f:
        for line in f:
            if b'"label":"graph-topology-' in line or b'"label": "graph-topology-' in line:
                topologies += 1
            else:
                try:
                    o = json.loads(line)
                except Exception:
                    continue
                if str(o.get("label", "")).startswith("graph-topology-"):
                    topologies += 1
    report = {
        "ok": got["exitCode"] == 0 and not miss and extra == 0 and len(expected) == pin["cases"],
        "exitCode": got["exitCode"],
        "lines": got["lines"],
        "rawBytes": got["rawBytes"],
        "rawSha256": got["rawSha256"],
        "checked": sum(1 for e in expected if e.get("result") == "checked"),
        "nativeRefused": sum(1 for e in expected if e.get("refusals")),
        "mismatchCount": len(miss) + extra,
        "mismatchesHead": miss,
        "graphTopologies": topologies,
        "identicalToPriorActual": got["stdout"] == open(os.path.join(root, "typescript-universe-actual.ndjson"), "rb").read(),
        "stderrBytes": len(got["stderr"]),
    }
    open(out, "w").write(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != "mismatchesHead"}))
    if not report["ok"]:
        sys.exit(1)

if __name__ == "__main__":
    main()
