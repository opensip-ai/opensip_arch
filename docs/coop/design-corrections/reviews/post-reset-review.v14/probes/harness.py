"""Independent probe harness. Loads the ACTUAL candidate reference sources by path and
binds their SHA256, so every probe below runs against the frozen bytes rather than a
synthetic re-implementation of them."""
import hashlib, importlib.util, json, os, sys, io, contextlib
from pathlib import Path

ROOT = Path(os.environ.get("OSIP_WORK",
    "/tmp/opensip-design-corrections/post-reset-review.v14/work"))
F = ROOT / "docs/coop/design-corrections/foundation"

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

BOUND_SOURCES = {
    "identity-model.py": sha(F / "identity-model.py"),
    "check-identity.py": sha(F / "check-identity.py"),
    "relation-payload-schemas.v2.json": sha(F / "relation-payload-schemas.v2.json"),
    "identity-schemas.v2.json": sha(F / "identity-schemas.v2.json"),
    "native_evidence_model.v2.py": sha(ROOT / "docs/coop/design-corrections/native/native_evidence_model.v2.py"),
    "native-evidence.schemas.v2.json": sha(ROOT / "docs/coop/design-corrections/native/native-evidence.schemas.v2.json"),
    "native-capability-matrix.v2.json": sha(ROOT / "docs/coop/design-corrections/native/native-capability-matrix.v2.json"),
    "public-detail-registry.v1.json": sha(ROOT / "docs/coop/design-corrections/public-detail-registry.v1.json"),
    "workflows_model.v1.py": sha(ROOT / "docs/coop/design-corrections/workflows/workflows_model.v1.py"),
    "common.schema.json": sha(ROOT / "docs/coop/design-corrections/workflows/schemas/common.schema.json"),
}

# check-identity.py executes its own suite and sys.exit()s at import; that is the dependency
# interface it actually offers, so it is driven rather than re-implemented.
_argv, sys.argv = sys.argv, ["check-identity.py"]
_spec = importlib.util.spec_from_file_location("candidate_check_identity", F / "check-identity.py")
CI = importlib.util.module_from_spec(_spec)
_buf = io.StringIO()
try:
    with contextlib.redirect_stdout(_buf):
        _spec.loader.exec_module(CI)
    SELFTEST_EXIT = 0
except SystemExit as e:
    SELFTEST_EXIT = e.code
finally:
    sys.argv = _argv
SELFTEST_STDOUT = _buf.getvalue().strip()

M, C, N, W = CI.M, CI.C, CI.N, CI.W

RESULTS = []
def probe(pid, kind, fn, expect_token=None):
    """kind: 'positive' -> must close a Run; 'negative' -> must refuse with expect_token."""
    rec = {"id": pid, "kind": kind, "expectedRefusal": expect_token}
    try:
        out = fn()
        rec["outcome"] = "returned"
        rec["value"] = (out[:24] + "...") if isinstance(out, str) else repr(out)[:200]
        rec["holds"] = (kind == "positive" and isinstance(out, str) and out.startswith("run2:")) \
                       or (kind == "check" and bool(out))
        if kind == "negative": rec["holds"] = False
    except BaseException as exc:
        rec["outcome"] = "refused"
        rec["refusal"] = "%s: %s" % (type(exc).__name__, exc)
        rec["holds"] = (kind == "negative" and expect_token is not None
                        and expect_token in str(exc))
    RESULTS.append(rec)
    return rec

def emit(path, extra=None):
    out = {"boundSources": BOUND_SOURCES,
           "candidateSelfTestExit": SELFTEST_EXIT,
           "candidateSelfTestStdout": SELFTEST_STDOUT,
           "probes": RESULTS,
           "allHold": all(r["holds"] for r in RESULTS),
           "failed": [r for r in RESULTS if not r["holds"]]}
    if extra: out.update(extra)
    Path(path).write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps({"allHold": out["allHold"], "n": len(RESULTS),
                      "failed": [r["id"] for r in out["failed"]]}, indent=1))
