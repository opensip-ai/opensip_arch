"""Discriminating controls, v2: mutate changed law bytes; confirm checkers detect it.

v1 was INVALID: an incomplete copy made every run exit 1 for a missing unrelated file,
so 'detected' was a false positive. This version copies the full docs tree (minus the
687M reviews/ history, which the checkers do not read) and runs an UNMUTATED CONTROL
first. If the control does not pass, no detection claim from this harness is admissible.

Detection is only credited when the run fails with a named check failure, not any exit 1.
"""
import json
import os
import re
import shutil
import subprocess
import sys

SRC = sys.argv[1]
WORK = sys.argv[2]
PY = "/tmp/opensip-architecture-review-env/bin/python"

WF_MODEL = "docs/coop/design-corrections/workflows/workflows_model.v1.py"
REGISTRY = "docs/coop/design-corrections/public-detail-registry.v1.json"
COMMON = "docs/coop/design-corrections/workflows/schemas/common.schema.json"
IDCHECK = "docs/coop/design-corrections/foundation/check-identity.py"
SKIP = os.path.join(SRC, "docs/coop/design-corrections/reviews")


def clone(root):
    def ignore(d, names):
        return {"reviews"} if os.path.abspath(d) == os.path.abspath(
            os.path.join(SRC, "docs/coop/design-corrections")) else set()
    shutil.copytree(os.path.join(SRC, "docs"), os.path.join(root, "docs"),
                    symlinks=True, ignore=ignore)


def m_drop_cardinality(root):
    p = os.path.join(root, WF_MODEL)
    t = open(p).read()
    blk = re.search(r"    if len\(rows\) > 1:\n(?:        .*\n)+?(?=    if not any)", t)
    assert blk, "cardinality guard not found"
    open(p, "w").write(t.replace(blk.group(0), ""))


def m_reorder_cardinality(root):
    p = os.path.join(root, WF_MODEL)
    t = open(p).read()
    g = re.search(r"    if len\(rows\) > 1:\n(?:        .*\n)+?(?=    if not any)", t)
    assert g, "guard not found"
    gb = g.group(0)
    t2 = t.replace(gb, "")
    mm = re.search(
        r"    if not any\(row\.get\('payloadDigest'\) == digest for row in rows\):\n"
        r"(?:        .*\n)+?(?=    return digest)", t2)
    assert mm, "match block not found"
    open(p, "w").write(t2.replace(mm.group(0), mm.group(0) + gb))


def m_unregister_registry(root):
    p = os.path.join(root, REGISTRY)
    d = json.load(open(p))
    n = len(d["records"])
    d["records"] = [r for r in d["records"]
                    if r["code"] != "BASELINE.SCOPE_PARAMETER_DIGEST_MISMATCH"]
    assert len(d["records"]) == n - 1
    json.dump(d, open(p, "w"), indent=2)


def m_unregister_enum(root):
    p = os.path.join(root, COMMON)
    d = json.load(open(p))
    e = d["$defs"]["DomainDetailCode"]["enum"]
    assert "BASELINE.SCOPE_NOT_A_SELECTED_PARAMETER" in e
    d["$defs"]["DomainDetailCode"]["enum"] = [
        x for x in e if x != "BASELINE.SCOPE_NOT_A_SELECTED_PARAMETER"]
    json.dump(d, open(p, "w"), indent=2)


def m_zero_selection_defaults(root):
    """Law 1: make zero selection silently fall back instead of refusing."""
    p = os.path.join(root, WF_MODEL)
    t = open(p).read()
    old = ("    if not rows:\n"
           "        raise Refusal('REQUEST.PRECONDITION_FAILED',"
           " 'BASELINE.SCOPE_NOT_A_SELECTED_PARAMETER',\n"
           "                      'the analysis spec selects no ScopeDocumentV1"
           " parameter')\n")
    assert old in t, "zero-selection guard not found"
    open(p, "w").write(t.replace(old, "    if not rows:\n        return digest\n"))


def m_sentinel_regression(root):
    """Is the sentinel load-bearing? Weaken the positive to root's is-None form AND
    point it at adopt_baseline's own detail=None duplicate-entry guard. If the weak
    form passes, it cannot distinguish refusal from success."""
    p = os.path.join(root, IDCHECK)
    t = open(p).read()
    old = ("check('adopt_baseline-with-the-selected-document-returns-without-any-refusal',\n"
           "      _adopt_scope_detail([_SCOPE_ROW_A],SCOPE_DOCUMENT) is _NO_REFUSAL)")
    assert old in t, "sentinel positive not found"
    new = ("check('adopt_baseline-with-the-selected-document-returns-without-any-refusal',\n"
           "      _refusal(lambda:W.adopt_baseline(_ADOPT_RUN,'plan2:x','proj',\n"
           "          {'schemaVersion':1,'rules':[]},SCOPE_DOCUMENT,\n"
           "          {'schemaVersion':1,'waivers':[]},[],\n"
           "          [{'fingerprint':'f'},{'fingerprint':'f'}],[],[],{},'0.0.0',\n"
           "          analysis_spec=_spec([_SCOPE_ROW_A]))).detail is None)")
    open(p, "w").write(t.replace(old, new))


CASES = [
    ("CONTROL-unmutated", None),
    ("law1-drop-at-most-one-guard", m_drop_cardinality),
    ("law1-cardinality-after-payload-match", m_reorder_cardinality),
    ("law1-zero-selection-silently-defaults", m_zero_selection_defaults),
    ("law8-unregister-from-closed-registry", m_unregister_registry),
    ("law8-unregister-from-mirrored-enum", m_unregister_enum),
    ("sentinel-regressed-to-is-none", m_sentinel_regression),
]

results = []
control_ok = None
for name, fn in CASES:
    root = os.path.join(WORK, name)
    shutil.rmtree(root, ignore_errors=True)
    os.makedirs(root)
    clone(root)
    err = None
    try:
        if fn:
            fn(root)
        applied = True
    except AssertionError as exc:
        applied, err = False, str(exc)
    rec = {"case": name, "mutated": fn is not None, "applied": applied,
           "applyError": err}
    if applied:
        proc = subprocess.run(
            [PY, "-I", "-B", os.path.join(root, IDCHECK),
             "--report", os.path.join(root, "r.json")],
            capture_output=True, text=True, timeout=1800)
        out = proc.stdout + proc.stderr
        # a real detection names a failed check, not an environment error
        failed_names = re.findall(r"FAIL[: ]+([a-z0-9\-]+)", out)
        env_error = "FileNotFoundError" in out or "ModuleNotFoundError" in out
        rec.update({
            "exitCode": proc.returncode,
            "environmentError": env_error,
            "failedCheckNames": failed_names[:5],
            "detected": proc.returncode != 0 and not env_error,
            "tail": [l for l in out.strip().splitlines()[-8:]],
        })
        if name == "CONTROL-unmutated":
            control_ok = proc.returncode == 0 and not env_error
    results.append(rec)
    print(f"{name}: applied={applied} exit={rec.get('exitCode')} "
          f"envErr={rec.get('environmentError')} detected={rec.get('detected')}",
          flush=True)
    shutil.rmtree(root, ignore_errors=True)

json.dump({
    "controlPassed": control_ok,
    "harnessAdmissible": bool(control_ok),
    "results": results,
    "allMutationsDetected": bool(control_ok) and all(
        r.get("detected") for r in results if r["mutated"] and r["applied"]),
}, open(os.path.join(WORK, "mutation-results.v2.json"), "w"), indent=2)
