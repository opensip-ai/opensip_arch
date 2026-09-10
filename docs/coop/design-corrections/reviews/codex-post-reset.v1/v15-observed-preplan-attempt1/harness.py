"""Independent probe harness for the frozen v15 candidate.

Loads the candidate's OWN reference sources through their real module entry
points and binds each file's exact SHA256, so a probe cannot silently pass
against different bytes. Expected outcomes are authored in the probe files, not
imported from the candidate.
"""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

SUBJECT = Path("/tmp/opensip-design-corrections/candidate-subject.v15")
DC = SUBJECT / "docs/coop/design-corrections"

# Exact bytes this review is bound to. Recomputed at import; a mismatch is fatal.
BOUND = {
    "foundation/identity-model.py":
        "fe301a101ee3d05ecfd51338a46ae6a9fcc115478358a00482e239dc83f4816d",
    "foundation/identity-schemas.v2.json":
        "f127fb117c3f3526fa6fad62a63e203a75e510fc7950f8e3dfd5b736d614e287",
    "foundation/relation-payload-schemas.v2.json":
        "ef0c244e7817e8bda6039ec66fc3180114f8e9997b3eacee4fe313c7f3d737b8",
    "foundation/check-identity.py":
        "2724276f6e52345d8635e2848f90cdac97d50f57b199fe6e9f03f1f2ad33ab48",
    "native/native_evidence_model.v2.py":
        "3619accb0b190586cabd9fdcca41c9f4db981862d13ff2dd7953f5bf65a6566d",
    "native/native-evidence.schemas.v2.json":
        "9ef09ab70c280d63d390fcafef1254d74504fa12d3839823518a1cf111099602",
    "native/native-capability-matrix.v2.json":
        "f6c2f12d170f0c57d5a4fa391b9a435d04286f9dad70ded6b1e3f68ee4556997",
    "workflows/workflows_model.v1.py":
        "4b4dc9ed823674273ba3285a6bfcc56fc4499ad3b821cd0446c4ebcf137d8106",
    "workflows/schemas/common.schema.json":
        "3f84dff20cf87bb3c7ada028b7af68566846c5bdee2b070494940cc9abe17a8a",
    "workflows/schemas/command-envelope.schema.json":
        "cbd9b083924428aa2e2a52babe89862878387a99a729d0486e68712d6afa0663",
    "public-detail-registry.v1.json":
        "e54a395fdf40a33a7db9f94630ae7cc1f79b762014fbef804a9c03a754b53c0f",
    "integration-fixtures.py":
        "9c34823c51c3bd9398ffd9b19606d172bc91c8a16eb518376c519fa615521414",
}


def _bind():
    for rel, want in BOUND.items():
        got = hashlib.sha256((DC / rel).read_bytes()).hexdigest()
        if got != want:
            raise SystemExit(
                "BOUND SOURCE MISMATCH %s\n  expected %s\n  actual   %s" % (rel, want, got))


_bind()


def load(name, path):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s)
    sys.modules[name] = m
    s.loader.exec_module(m)
    return m


M = load("idmodel", DC / "foundation/identity-model.py")
C = M.C
N = load("nativemodel", DC / "native/native_evidence_model.v2.py")
W = load("wfmodel", DC / "workflows/workflows_model.v1.py")

_RESULTS = []


def check(name, value, detail=None):
    """Record one independently authored expectation."""
    rec = {"id": name, "passed": bool(value)}
    if detail is not None:
        rec["detail"] = detail
    _RESULTS.append(rec)
    return bool(value)


def raises(name, fn, exc_types, must_contain=None, must_not_contain=None):
    """Assert fn refuses with an EXACT expected class and message token.

    A refusal at the wrong place is never counted as coverage of the intended
    one, so the exception type and the message token are both asserted.
    """
    try:
        fn()
    except BaseException as e:  # noqa: BLE001 - the class is asserted below
        okc = isinstance(e, exc_types)
        okm = (must_contain is None) or (must_contain in str(e))
        okn = (must_not_contain is None) or (must_not_contain not in str(e))
        return check(name, okc and okm and okn,
                     {"exc": type(e).__name__, "msg": str(e)[:400]})
    return check(name, False, {"exc": None, "msg": "NO REFUSAL - admitted"})


def admits(name, fn):
    try:
        r = fn()
    except BaseException as e:  # noqa: BLE001
        return check(name, False, {"exc": type(e).__name__, "msg": str(e)[:400]})
    return check(name, True, {"returned": type(r).__name__})


def report(path, title, limitations):
    doc = {
        "probe": title,
        "authoredBy": "fresh independent review of frozen v15; expectations authored here, not imported",
        "boundSourceSha256": dict(BOUND),
        "limitations": limitations,
        "cases": _RESULTS,
        "total": len(_RESULTS),
        "passed": sum(c["passed"] for c in _RESULTS),
        "failed": sum(not c["passed"] for c in _RESULTS),
    }
    Path(path).write_text(json.dumps(doc, indent=1) + "\n")
    print(json.dumps({"probe": title, "total": doc["total"],
                      "passed": doc["passed"], "failed": doc["failed"]}))
    if doc["failed"]:
        print(json.dumps([c for c in _RESULTS if not c["passed"]], indent=1))
    return doc["failed"]
