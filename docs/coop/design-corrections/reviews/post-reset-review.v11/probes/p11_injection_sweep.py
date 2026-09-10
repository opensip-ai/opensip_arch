#!/usr/bin/env python3
"""p11: independent reproduction of the 39-injection sweep, shape matrix and removal corpus.

Rebuilt from the law rather than by calling the candidate's helpers, and every arm carries its
positive control (annotate the SAME injected field and require admission), so a refusal can never
be credited to "injecting a field" rather than to the missing annotation.

Also asserts the non-governed distinction: removing the annotation from the UInt64 `byteLength`
must NOT produce a refusal, while removing it from any governed digest/path field must.
"""
import copy
import importlib.util
import json
import sys
from pathlib import Path

V11 = Path("/tmp/opensip-design-corrections/candidate-subject.v11/docs/coop/design-corrections/foundation")
spec = importlib.util.spec_from_file_location("m", V11 / "identity-model.py")
M = importlib.util.module_from_spec(spec)
sys.modules["m"] = M
spec.loader.exec_module(M)
C = M.C

FORMS = ("DigestHex", "Sha256Text", "CanonicalPath")
SHAPES = ("ref", "inline", "nullable", "aliased", "nested", "array",
          "container-ref", "cyclic-container-ref")
ANN = {"representation": "raw-artifact", "retention": "not-joined",
       "authority": "independent-probe", "reason": "reviewer control, not a shipped field"}


def inject(relation, form, shape="ref", annotate=False):
    d = copy.deepcopy(M.RELATION_DOCUMENT)
    selector = d["$defs"][M.RELATIONS[relation]["selector"].split("/")[-1]]
    node = {
        "ref": {"$ref": "#/$defs/" + form},
        "inline": dict(d["$defs"][form]),
        "nullable": {"oneOf": [{"$ref": "#/$defs/" + form}, {"type": "null"}]},
        "aliased": {"$ref": "#/$defs/ProbeAliasV1"},
        "nested": {"type": "object", "properties": {"inner": {"$ref": "#/$defs/" + form}}},
        "array": {"type": "array", "items": {"$ref": "#/$defs/" + form}},
        "container-ref": {"$ref": "#/$defs/ProbeContainerV1"},
        "cyclic-container-ref": {"$ref": "#/$defs/ProbeCycleV1"},
    }[shape]
    if shape == "aliased":
        d["$defs"]["ProbeAliasV1"] = {"$ref": "#/$defs/" + form}
    if shape == "container-ref":
        d["$defs"]["ProbeContainerV1"] = {
            "type": "object", "properties": {"hidden": {"$ref": "#/$defs/" + form}}}
    if shape == "cyclic-container-ref":
        d["$defs"]["ProbeCycleV1"] = {"type": "object", "properties": {
            "hidden": {"$ref": "#/$defs/" + form}, "again": {"$ref": "#/$defs/ProbeCycleV1"}}}
    if annotate:
        node = dict(node, **{"x-opensip-digest": ANN})
    selector["properties"]["probeGoverned"] = node
    return d


def verdict(relation, d):
    try:
        M.relation_annotation_closure(relation, d)
        return "ADMIT"
    except C.AdmissionError as exc:
        return str(exc)
    except Exception as exc:
        return "OTHER:" + type(exc).__name__


relations = sorted(M.RELATIONS)
out = {"relationCount": len(relations), "formCount": len(FORMS)}

# ---- 39 = 13 relations x 3 forms, unannotated: every one must refuse with the intended cause
admitted, wrong_cause, refused = [], [], 0
for r in relations:
    for f in FORMS:
        v = verdict(r, inject(r, f))
        if v == "ADMIT":
            admitted.append(f"{r}/{f}")
        elif not v.startswith(f"RELATION_DIGEST_UNANNOTATED:{r}:{r}.probeGoverned:{f}"):
            wrong_cause.append({"case": f"{r}/{f}", "cause": v})
        else:
            refused += 1
out["sweep39"] = {
    "cases": len(relations) * len(FORMS),
    "refusedWithIntendedCause": refused,
    "admitted": admitted,
    "wrongCause": wrong_cause,
    "allRefusedCorrectly": not admitted and not wrong_cause,
}

# ---- positive control: the SAME injected field, annotated, must admit everywhere
ctrl_fail = [f"{r}/{f}" for r in relations for f in FORMS
             if verdict(r, inject(r, f, annotate=True)) != "ADMIT"]
out["sweep39PositiveControl"] = {
    "cases": len(relations) * len(FORMS),
    "failures": ctrl_fail,
    "allAdmitted": not ctrl_fail,
}

# ---- shape matrix on one relation, negative and positive
shapes = {}
for s in SHAPES:
    neg = verdict("file", inject("file", "CanonicalPath", shape=s))
    pos = verdict("file", inject("file", "CanonicalPath", shape=s, annotate=True))
    shapes[s] = {
        "unannotated": neg,
        "unannotatedRefusesCorrectly": neg.startswith("RELATION_DIGEST_UNANNOTATED:file:"),
        "annotated": pos,
        "annotatedAdmits": pos == "ADMIT",
    }
out["shapeMatrix"] = shapes
out["shapeMatrixAllCorrect"] = all(
    v["unannotatedRefusesCorrectly"] and v["annotatedAdmits"] for v in shapes.values())

# ---- removal corpus: governed fields must refuse; non-governed byteLength must not
GOVERNED_FIELDS = [("clones", "bodyIdentity"), ("clones", "normalisationVersion"),
                   ("file", "path"), ("file", "contentSha256"),
                   ("package", "manifestPath"),
                   ("vcs-change", "path"), ("vcs-change", "previousPath")]


def strip(relation, field):
    d = copy.deepcopy(M.RELATION_DOCUMENT)
    props = d["$defs"][M.RELATIONS[relation]["selector"].split("/")[-1]]["properties"]
    props[field] = {k: v for k, v in props[field].items() if k != "x-opensip-digest"}
    return d


removals = {}
for r, f in GOVERNED_FIELDS:
    v = verdict(r, strip(r, f))
    removals[f"{r}.{f}"] = {
        "verdict": v,
        "refusesWithIntendedCause": v.startswith(
            f"RELATION_DIGEST_UNANNOTATED:{r}:{r}.{f}"),
        "governed": True,
    }
v = verdict("file", strip("file", "byteLength"))
removals["file.byteLength"] = {
    "verdict": v,
    "admitsAsRequired": v == "ADMIT",
    "governed": False,
    "note": "UInt64, annotated but NOT governed; its removal must not reach the third limb",
}
out["removalCorpus"] = removals
out["removalCorpusCorrect"] = (
    all(v["refusesWithIntendedCause"] for k, v in removals.items() if v["governed"])
    and removals["file.byteLength"]["admitsAsRequired"])

out["ALL_CORRECT"] = (out["sweep39"]["allRefusedCorrectly"]
                      and out["sweep39PositiveControl"]["allAdmitted"]
                      and out["shapeMatrixAllCorrect"]
                      and out["removalCorpusCorrect"])
print(json.dumps(out, indent=2))
