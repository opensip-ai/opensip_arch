"""Discriminating controls: mutate the changed law bytes and confirm the checkers catch it.

A guard that no test detects is not enforced. Each mutation is a concrete counterexample
applied to a THROWAWAY copy; the frozen subject is never touched. For each we record the
first failing boundary (which named check fires).

Mutations target the specific changed laws under review, not incidental code.
"""
import json
import os
import re
import shutil
import subprocess
import sys

SRC = sys.argv[1]          # pristine snapshot (read only)
WORK = sys.argv[2]         # scratch root
PY = "/tmp/opensip-architecture-review-env/bin/python"

WF_MODEL = "docs/coop/design-corrections/workflows/workflows_model.v1.py"
REGISTRY = "docs/coop/design-corrections/public-detail-registry.v1.json"
COMMON = "docs/coop/design-corrections/workflows/schemas/common.schema.json"
IDCHECK = "docs/coop/design-corrections/foundation/check-identity.py"


def mutate_drop_cardinality(root):
    """Law 1: delete the at-most-one guard entirely."""
    p = os.path.join(root, WF_MODEL)
    t = open(p).read()
    new = t.replace(
        "    if len(rows) > 1:\n"
        "        raise Refusal('CONFIG.INVALID', 'CONFIG.INVALID',\n"
        "                      'the analysis spec selects more than one ScopeDocumentV1"
        " parameter; state exactly one',\n"
        "                      subject='parameters[schemaDigest=' + document + ']x'"
        " + str(len(rows)))\n",
        "",
    )
    assert new != t, "cardinality guard text not found"
    open(p, "w").write(new)


def mutate_reorder_cardinality(root):
    """Law 1: keep the guard but move it AFTER the payload match (ordering defect)."""
    p = os.path.join(root, WF_MODEL)
    t = open(p).read()
    guard = re.search(
        r"    if len\(rows\) > 1:\n(?:        .*\n)+?(?=    if not any)", t
    )
    assert guard, "guard block not found"
    g = guard.group(0)
    t2 = t.replace(g, "")
    match_blk = re.search(
        r"    if not any\(row\.get\('payloadDigest'\) == digest for row in rows\):\n"
        r"(?:        .*\n)+?(?=    return digest)",
        t2,
    )
    assert match_blk, "match block not found"
    m = match_blk.group(0)
    open(p, "w").write(t2.replace(m, m + g))


def mutate_unregister_detail(root):
    """Law 8: remove one baseline-scope detail from the closed registry."""
    p = os.path.join(root, REGISTRY)
    d = json.load(open(p))
    before = len(d["records"])
    d["records"] = [
        r for r in d["records"]
        if r["code"] != "BASELINE.SCOPE_PARAMETER_DIGEST_MISMATCH"
    ]
    assert len(d["records"]) == before - 1, "detail not present to remove"
    json.dump(d, open(p, "w"), indent=2)


def mutate_unregister_enum(root):
    """Law 8: remove the detail from the mirrored schema enum only (registry intact)."""
    p = os.path.join(root, COMMON)
    d = json.load(open(p))
    e = d["$defs"]["DomainDetailCode"]["enum"]
    assert "BASELINE.SCOPE_NOT_A_SELECTED_PARAMETER" in e
    d["$defs"]["DomainDetailCode"]["enum"] = [
        x for x in e if x != "BASELINE.SCOPE_NOT_A_SELECTED_PARAMETER"
    ]
    json.dump(d, open(p, "w"), indent=2)


def mutate_sentinel_to_is_none(root):
    """Root's superseded control: does `is None` still discriminate?

    Rewrites the positive to the earlier is-None form. If the checker still passes,
    the sentinel correction is cosmetic; if the positive becomes unable to fail, the
    correction is load-bearing. We assert on the WEAKENED positive by also breaking
    the binding, so a passing result means the weak form is blind.
    """
    p = os.path.join(root, IDCHECK)
    t = open(p).read()
    old = (
        "check('adopt_baseline-with-the-selected-document-returns-without-any-refusal',\n"
        "      _adopt_scope_detail([_SCOPE_ROW_A],SCOPE_DOCUMENT) is _NO_REFUSAL)"
    )
    assert old in t, "sentinel positive not found"
    # earlier root form: detail is None. Feed it a run that trips the duplicate-entry
    # guard (detail=None) instead of the selected document.
    new = (
        "check('adopt_baseline-with-the-selected-document-returns-without-any-refusal',\n"
        "      _refusal(lambda:W.adopt_baseline(_ADOPT_RUN,'plan2:x','proj',\n"
        "          {'schemaVersion':1,'rules':[]},SCOPE_DOCUMENT,\n"
        "          {'schemaVersion':1,'waivers':[]},[],\n"
        "          [{'fingerprint':'f'},{'fingerprint':'f'}],[],[],{},'0.0.0',\n"
        "          analysis_spec=_spec([_SCOPE_ROW_A]))).detail is None)"
    )
    open(p, "w").write(t.replace(old, new))


MUTATIONS = [
    ("law1-drop-at-most-one-guard", mutate_drop_cardinality),
    ("law1-check-cardinality-after-payload-match", mutate_reorder_cardinality),
    ("law8-unregister-detail-from-registry", mutate_unregister_detail),
    ("law8-unregister-detail-from-mirrored-enum", mutate_unregister_enum),
    ("sentinel-regress-to-is-none", mutate_sentinel_to_is_none),
]

results = []
for name, fn in MUTATIONS:
    root = os.path.join(WORK, name)
    if os.path.exists(root):
        shutil.rmtree(root)
    os.makedirs(root)
    # only the trees the identity checker reads
    for sub in ["docs/coop/design-corrections", "docs/v2"]:
        shutil.copytree(
            os.path.join(SRC, sub), os.path.join(root, sub), symlinks=True
        )
    try:
        fn(root)
        applied = True
        err = None
    except AssertionError as exc:
        applied, err = False, str(exc)
    rec = {"mutation": name, "applied": applied, "applyError": err}
    if applied:
        proc = subprocess.run(
            [PY, "-I", "-B",
             os.path.join(root, IDCHECK),
             "--report", os.path.join(root, "mut-report.json")],
            capture_output=True, text=True, timeout=1800,
        )
        tail = (proc.stdout + proc.stderr).strip().splitlines()
        rec.update({
            "exitCode": proc.returncode,
            "detected": proc.returncode != 0,
            "tail": tail[-6:],
        })
    results.append(rec)
    print(f"{name}: applied={applied} detected={rec.get('detected')}", flush=True)
    shutil.rmtree(root, ignore_errors=True)

json.dump(
    {"results": results,
     "allDetected": all(r.get("detected") for r in results if r["applied"])},
    open(os.path.join(WORK, "mutation-results.json"), "w"), indent=2,
)
