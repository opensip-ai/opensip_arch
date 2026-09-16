#!/usr/bin/env python3
"""Reference check of the native wire-carrier ROOT continuation of actual-Claude author06; not approval, not a production decoder, not product
qualification.

Run (from any copy of the tools/filelist.py INPUTS):
  OPENSIP_ARCH=/Users/sb/code/opensip-ai/opensip_arch TMPDIR=<subject>/tmp PYTHONDONTWRITEBYTECODE=1 \
    /tmp/opensip-implementation/metadata-reference-env/bin/python -I -B check.py [--out check-result.json]

Before importing any architecture code it verifies every architecture pin, forces a private bytecode prefix under the
subject tmp directory, and installs an audit hook for `open` and `subprocess.Popen`. Afterwards it fails on any
architecture read outside the pin set, any architecture .pyc read, any read under /tmp outside the subject, its TMPDIR and
the reference environment, any subject read outside tools/filelist.py INPUTS (or tmp/), and any executed program other
than the pinned ECMA-262 engine. The audit observes only those two event kinds: it is a closure record for these code
paths, not a general confinement proof (directory listings, stat calls and dynamic library loads are not observed).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TMP = os.path.join(HERE, "tmp")
os.makedirs(os.path.join(TMP, "pycache"), exist_ok=True)
sys.dont_write_bytecode = True
sys.pycache_prefix = os.path.join(TMP, "pycache")
import tempfile  # noqa: E402

tempfile.tempdir = TMP
OPENED, EXECS = [], []


def _audit(event, args):
    if event == "open" and args and isinstance(args[0], (str, bytes, os.PathLike)):
        OPENED.append(os.path.realpath(os.fsdecode(args[0])))
    elif event == "subprocess.Popen" and args:
        exe = args[0] if args[0] else (args[1][0] if args[1] else "")
        EXECS.append(os.fsdecode(exe))


sys.addaudithook(_audit)
sys.path.insert(0, os.path.join(HERE, "tools"))

import argparse, hashlib, json, signal  # noqa: E402,E401
from pathlib import Path  # noqa: E402

import common as CM  # noqa: E402
import filelist as FL  # noqa: E402

REF_ENV = "/private/tmp/opensip-implementation/metadata-reference-env"


def verify_pins(arch):
    bad = []
    for key, (path, sha, size) in CM.ARCH_PINS.items():
        raw = (arch / path).read_bytes()
        if hashlib.sha256(raw).hexdigest() != sha or len(raw) != size:
            bad.append(path)
    return bad


def closure_results(arch, subject):
    arch_real = os.path.realpath(str(arch)) + os.sep
    subject_real = os.path.realpath(str(subject)) + os.sep
    pinned = {os.path.realpath(str(arch / p)) for p, _, _ in CM.ARCH_PINS.values()}
    arch_reads = sorted({p for p in OPENED if p.startswith(arch_real)})
    unpinned = [p for p in arch_reads if p not in pinned and not p.endswith(os.sep)]
    pyc = [p for p in arch_reads if p.endswith(".pyc") or "__pycache__" in p]
    tmp_reads = sorted({p for p in OPENED if p.startswith("/private/tmp/") or p.startswith("/tmp/")})
    hidden = [p for p in tmp_reads if not (p.startswith(subject_real) or p.startswith(REF_ENV + os.sep))]
    listed = {os.path.realpath(os.path.join(str(subject), p)) for p in FL.INPUTS}
    subject_reads = sorted({p for p in OPENED if p.startswith(subject_real) and not p.startswith(subject_real + "tmp" + os.sep)})
    unlisted = [p for p in subject_reads if p not in listed]
    node = Path(CM.NODE["path"]).read_bytes()
    node_ok = hashlib.sha256(node).hexdigest() == CM.NODE["sha256"] and len(node) == CM.NODE["bytes"]
    return [
        {"id": "closure-architecture-reads-pinned", "ok": not unpinned, "detail": json.dumps({"read": len(arch_reads), "unpinned": unpinned})},
        {"id": "closure-no-architecture-bytecode", "ok": not pyc, "detail": json.dumps(pyc)},
        {"id": "closure-no-hidden-tmp-reads", "ok": not hidden, "detail": json.dumps(hidden[:20])},
        {"id": "closure-every-pin-used", "ok": pinned <= set(arch_reads), "detail": json.dumps(sorted(pinned - set(arch_reads)))},
        {"id": "closure-execution-inputs-listed", "ok": not unlisted and bool(subject_reads), "detail": json.dumps({"subjectReads": len(subject_reads), "listedInputs": len(FL.INPUTS), "unlisted": unlisted})},
        {"id": "closure-subprocess-exec-pinned", "ok": bool(EXECS) and set(EXECS) == {CM.NODE["path"]} and node_ok,
         "detail": json.dumps({"executions": len(EXECS), "programs": sorted(set(EXECS)), "engineBytesVerifiedAfterRun": node_ok, "unpinnedDynamicLibraries": CM.NODE["dynamicLibraries"]})},
    ]


def environment_results(subject):
    import importlib.metadata as md
    import platform
    declared = json.loads((subject / "reference-environment.json").read_text())
    actual = {"python": platform.python_version(), "packages": {n: md.version(n) for n in declared["packages"]}}
    import jsonschema, referencing  # noqa: E401
    origins = {m.__name__: os.path.realpath(m.__file__) for m in (jsonschema, referencing)}
    in_env = all(o.startswith(REF_ENV + os.sep) for o in origins.values())
    return [{"id": "reference-environment-matches", "ok": actual["python"] == declared["python"] and actual["packages"] == declared["packages"] and in_env,
             "detail": json.dumps({"declared": declared, "actual": actual, "origins": origins})}], actual


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(HERE, "check-result.json"))
    ap.add_argument("--subject", default=HERE, help="subject copy to check (selftest passes mutated copies)")
    ap.add_argument("--static-only", action="store_true")
    args = ap.parse_args()
    signal.alarm(2400)
    arch = CM.arch_root()
    subject = Path(args.subject)
    bad = verify_pins(arch)
    results = [{"id": "architecture-pins-verified-before-import", "ok": not bad, "detail": json.dumps(bad)}]
    if bad:
        doc = {"standing": "ROOT continuation of actual-Claude author06 reference check; refused before importing any architecture code",
               "architectureRoot": str(arch), "checks": len(results), "failed": 1, "failures": results, "results": results}
        Path(args.out).write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        print(json.dumps(doc["failures"]))
        return 1
    from jsonschema import Draft202012Validator
    from check_static import Static
    st = Static(arch, subject)
    results += st.run(Draft202012Validator)
    if not args.static_only:
        try:
            from check_reference import Reference
            results += Reference(arch, subject, st).run()
        except Exception as exc:  # noqa: BLE001 - a candidate the reference cannot even load is a failed named check
            results.append({"id": "step:reference-init", "ok": False, "detail": type(exc).__name__ + ": " + str(exc)[:400]})
    env_results, env = environment_results(Path(HERE))
    results += env_results
    results.append({"id": "architecture-pins-unchanged-after-run", "ok": not verify_pins(arch), "detail": ""})
    results += closure_results(arch, subject)
    ids = {r["id"] for r in results}
    present = lambda cid: cid in ids or any(i.startswith(cid + ":") for i in ids)
    for row in st.succ["rows"]:
        for cid in row["referenceChecks"]:
            if not present(cid):
                results.append({"id": "successor-check-exists:" + cid, "ok": False, "detail": row["id"]})
    for res in st.succ["reviewResolutions"]:
        for cid in res["checks"]:
            if cid != "isolation" and not present(cid):
                results.append({"id": "review-resolution-check-exists:" + cid, "ok": False, "detail": res["id"]})
    failed = [r for r in results if not r["ok"]]
    doc = {"standing": "ROOT continuation of actual-Claude author06 reference check; not approval, not a production wire decoder, not M2/M3 qualification",
           "architectureRoot": str(arch), "referenceEnvironment": env,
           "auditScope": "open and subprocess.Popen audit events only; not a general confinement proof",
           "checks": len(results), "failed": len(failed), "failures": failed, "results": results}
    Path(args.out).write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"checks": len(results), "failed": len(failed), "failures": failed[:40]}, indent=1, ensure_ascii=False)[:12000])
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
