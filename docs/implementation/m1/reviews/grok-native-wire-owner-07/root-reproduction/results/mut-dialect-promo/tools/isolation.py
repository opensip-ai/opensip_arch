#!/usr/bin/env python3
"""Isolation demonstration (candidate 06): copy ONLY tools/filelist.py INPUTS (verified against the subject-files.json
input digests written just before) into tmp/isolation/subject, then run check.py and selftest.py there with a minimal
environment, that copy's own TMPDIR and bytecode prefix, against the pinned architecture snapshot, the declared reference
environment and the pinned ECMA-262 engine. subject-files.json is NOT copied: the copy proves the closure is exactly the
listed inputs. Writes isolation-result.json in the primary subject.

    OPENSIP_ARCH=... PYTHONDONTWRITEBYTECODE=1 /tmp/opensip-implementation/metadata-reference-env/bin/python -I -B tools/isolation.py
"""
import hashlib, json, os, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import filelist as FL  # noqa: E402

PY = "/tmp/opensip-implementation/metadata-reference-env/bin/python"


def main():
    digests = {f["path"]: f["sha256"] for f in json.loads((ROOT / "subject-files.json").read_text())["inputs"]}
    if sorted(digests) != sorted(FL.INPUTS):
        raise SystemExit("subject-files.json inputs differ from tools/filelist.py INPUTS")
    copy = ROOT / "tmp" / "isolation" / "subject"
    shutil.rmtree(copy.parent, ignore_errors=True)
    for p in FL.INPUTS:
        dst = copy / p
        dst.parent.mkdir(parents=True, exist_ok=True)
        b = (ROOT / p).read_bytes()
        if hashlib.sha256(b).hexdigest() != digests[p]:
            raise SystemExit("input drift before isolation: " + p)
        dst.write_bytes(b)
    (copy / "tmp").mkdir()
    env = {"PATH": "/usr/bin:/bin", "HOME": os.environ.get("HOME", "/tmp"), "OPENSIP_ARCH": os.environ.get("OPENSIP_ARCH", "/Users/sb/code/opensip-ai/opensip_arch"),
           "TMPDIR": str(copy / "tmp"), "PYTHONDONTWRITEBYTECODE": "1", "PYTHONPYCACHEPREFIX": str(copy / "tmp" / "pycache"),
           "SELFTEST_WORKERS": os.environ.get("SELFTEST_WORKERS", "6")}
    runs = {}
    for name, argv in (("check", ["check.py", "--out", str(copy / "check-result.json")]), ("selftest", ["selftest.py"])):
        p = subprocess.run([PY, "-I", "-B"] + argv, cwd=copy, env=env, capture_output=True, text=True, timeout=10800)
        runs[name] = {"returncode": p.returncode, "stdoutTail": p.stdout[-600:], "stderrTail": p.stderr[-300:]}
    iso_check = json.loads((copy / "check-result.json").read_text())
    iso_self = json.loads((copy / "selftest-result.json").read_text())
    primary = json.loads((ROOT / "check-result.json").read_text())
    same_ids = [r["id"] for r in iso_check["results"]] == [r["id"] for r in primary["results"]]
    same_ok = [r["ok"] for r in iso_check["results"]] == [r["ok"] for r in primary["results"]]
    extra = sorted(str(p.relative_to(copy)) for p in copy.rglob("*") if p.is_file() and "tmp" not in p.relative_to(copy).parts)
    doc = {"standing": "ROOT continuation of actual-Claude author06 isolation demonstration; not approval",
           "copiedInputs": len(FL.INPUTS), "subjectFilesJsonCopied": False, "copyPath": str(copy), "environment": {k: v for k, v in env.items() if k != "HOME"},
           "runs": runs, "check": {"checks": iso_check["checks"], "failed": iso_check["failed"], "sameIdsAsPrimary": same_ids, "sameOutcomesAsPrimary": same_ok},
           "selftest": {"caught": iso_self["caught"], "total": iso_self["total"], "allCaught": iso_self["allCaught"], "baselineFailures": iso_self["baselineFailures"]},
           "filesPresentAfterRuns": extra,
           "pass": runs["check"]["returncode"] == 0 and runs["selftest"]["returncode"] == 0 and iso_check["failed"] == 0 and same_ids and same_ok and iso_self["allCaught"]}
    (ROOT / "isolation-result.json").write_text(json.dumps(doc, indent=1) + "\n")
    shutil.rmtree(copy.parent, ignore_errors=True)
    print(json.dumps({k: doc[k] for k in ("copiedInputs", "check", "selftest", "pass")}, indent=1))
    return 0 if doc["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
