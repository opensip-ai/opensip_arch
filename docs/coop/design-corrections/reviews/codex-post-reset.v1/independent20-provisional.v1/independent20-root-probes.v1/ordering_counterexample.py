"""Is the claimed ambiguity-BEFORE-digest-match precedence actually pinned by a test?

workflows_model.v1.py:689-696 claims the at-most-one guard must run BEFORE the payload
comparison, and check-identity.py names a control
'the-scope-binding-verifier-refuses-an-ambiguous-selection-before-any-digest-match'.

But both existing controls supply a document that IS one of the two candidate rows. For
those inputs BOTH orderings return CONFIG.INVALID, so they do not discriminate ordering.
The discriminating input is an ambiguous spec plus a document that is NEITHER candidate:
  guard-first  -> CONFIG.INVALID              (ambiguity)
  match-first  -> BASELINE.SCOPE_PARAMETER_DIGEST_MISMATCH
This probe measures the shipped behaviour and the reordered behaviour on that input.
"""
import importlib.util
import json
import os
import re
import shutil
import sys
import tempfile

SRC = sys.argv[1]
WF = "docs/coop/design-corrections/workflows/workflows_model.v1.py"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


def outcome(W, rows, document):
    try:
        return ("RETURNED", W.verify_scope_parameter_binding(
            {"parameters": rows}, document))
    except W.Refusal as exc:
        return ("REFUSED", exc.error_code, exc.detail)


def build(W):
    doc_a = {"schemaVersion": 2, "workspaceRoots": ["a"], "pathPrefixes": ["."],
             "excludedPathPrefixes": []}
    doc_b = {"schemaVersion": 2, "workspaceRoots": ["b"], "pathPrefixes": ["."],
             "excludedPathPrefixes": []}
    doc_c = {"schemaVersion": 2, "workspaceRoots": ["c"], "pathPrefixes": ["."],
             "excludedPathPrefixes": []}
    sd = W.raw_sha((os.path.join(
        os.path.dirname(os.path.dirname(W.__file__)),
        "workflows/schemas/policy-document.schema.json")).encode()) \
        if False else None
    # schemaDigest exactly as the model computes it
    from pathlib import Path
    schema = W.raw_sha((Path(W.__file__).resolve().parent.parent /
                        W.SCOPE_DOCUMENT_SCHEMA).read_bytes())
    row = lambda d: {"schemaDigest": schema, "payloadDigest": W.doc_digest(d)}
    return doc_a, doc_b, doc_c, row


# --- shipped bytes
W = load(os.path.join(SRC, WF), "wf_shipped")
a, b, c, row = build(W)
shipped = {
    "ambiguous+candidate-document": outcome(W, [row(a), row(b)], a),
    "ambiguous+NON-candidate-document": outcome(W, [row(a), row(b)], c),
    "single-row+non-matching-document": outcome(W, [row(a)], c),
}

# --- reordered variant (guard moved after the payload match)
tmp = tempfile.mkdtemp()
shutil.copytree(os.path.join(SRC, "docs/coop/design-corrections"),
                os.path.join(tmp, "dc"),
                ignore=lambda d, n: {"reviews"} if os.path.basename(d) ==
                "design-corrections" else set())
p = os.path.join(tmp, "dc/workflows/workflows_model.v1.py")
t = open(p).read()
g = re.search(r"    if len\(rows\) > 1:\n(?:        .*\n)+?(?=    if not any)", t)
gb = g.group(0)
t2 = t.replace(gb, "")
mm = re.search(
    r"    if not any\(row\.get\('payloadDigest'\) == digest for row in rows\):\n"
    r"(?:        .*\n)+?(?=    return digest)", t2)
open(p, "w").write(t2.replace(mm.group(0), mm.group(0) + gb))
W2 = load(p, "wf_reordered")
reordered = {
    "ambiguous+candidate-document": outcome(W2, [row(a), row(b)], a),
    "ambiguous+NON-candidate-document": outcome(W2, [row(a), row(b)], c),
    "single-row+non-matching-document": outcome(W2, [row(a)], c),
}

diffs = {k: {"shipped": shipped[k], "reordered": reordered[k]}
         for k in shipped if shipped[k] != reordered[k]}

print(json.dumps({
    "shipped": shipped,
    "reordered": reordered,
    "inputsWhereOrderingIsObservable": sorted(diffs),
    "diffs": diffs,
    "shippedIsCorrect": shipped["ambiguous+NON-candidate-document"][1:] ==
                        ("CONFIG.INVALID", "CONFIG.INVALID"),
}, indent=2))
shutil.rmtree(tmp, ignore_errors=True)
