#!/usr/bin/env python3
"""p08: INDEPENDENT probes of the v11 relation annotation law.

Written against identity-model.py directly, from the law text in
`x-opensip-digest-law.residueRule`, NOT by reusing the candidate's check-identity.py helpers.
Every negative asserts its EXACT refusal cause, and every family carries a positive control so a
refusal cannot be credited to the wrong reason.

Each probe is run against BOTH the v11 model and the pre-fix v10 model. The v10 column is the
discrimination evidence: a probe that behaves identically under both proves nothing about the fix.
"""
import copy
import importlib.util
import json
import sys
from pathlib import Path

V11 = Path("/tmp/opensip-design-corrections/candidate-subject.v11/docs/coop/design-corrections/foundation")
V10 = Path("/tmp/opensip-design-corrections/candidate-subject.v10/docs/coop/design-corrections/foundation")


def load(tag, home):
    spec = importlib.util.spec_from_file_location(tag, home / "identity-model.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[tag] = mod
    spec.loader.exec_module(mod)
    return mod


def verdict(M, name, document):
    """ADMIT, or the exact refusal cause token."""
    try:
        M.relation_annotation_closure(name, document)
        return "ADMIT"
    except Exception as exc:  # cause token is the payload under test
        return str(exc).split(":")[0] if ":" in str(exc) else type(exc).__name__


def detail(M, name, document):
    try:
        M.relation_annotation_closure(name, document)
        return "ADMIT"
    except Exception as exc:
        return str(exc)


ANN = {"representation": "raw-artifact", "retention": "not-joined",
       "authority": "probe", "reason": "independent reviewer probe control"}
BARE = {"$ref": "#/$defs/DigestHex"}


def marked(annotation=None):
    return dict(BARE, **{"x-opensip-digest": annotation or ANN})


# --------------------------------------------------------------- document constructors (mine)
def doc(M):
    return copy.deepcopy(M.RELATION_DOCUMENT)


def same_path_container(M, order):
    """One path reached by a $ref'd container AND the local sibling refinement."""
    d = doc(M)
    d["$defs"]["RevContainerV1"] = {"type": "object", "properties": {
        "leaf": BARE if order == "unannotated-first" else marked()}}
    d["$defs"]["FilePayloadV1"]["properties"]["rev"] = {
        "$ref": "#/$defs/RevContainerV1",
        "properties": {"leaf": marked() if order == "unannotated-first" else BARE}}
    return d


def same_path_keyorder(M, order):
    """items/ and additionalProperties/ both map to the SAME `[]` path; only key order differs,
    so the two documents are canonically EQUAL and any verdict difference is pure artifact."""
    d = doc(M)
    d["$defs"]["FilePayloadV1"]["properties"]["rev"] = (
        {"items": BARE, "additionalProperties": marked()} if order == "unannotated-first"
        else {"additionalProperties": marked(), "items": BARE})
    return d


def three_sightings(M, missing_at):
    """Three schemas reaching ONE path via a two-level $ref chain plus a local refinement."""
    d = doc(M)
    nodes = [marked(), marked(), dict(BARE)]
    nodes.insert(missing_at, nodes.pop(2))
    d["$defs"]["RevInnerV1"] = {"type": "object", "properties": {"leaf": nodes[0]}}
    d["$defs"]["RevOuterV1"] = {"$ref": "#/$defs/RevInnerV1",
                                "properties": {"leaf": nodes[1]}}
    d["$defs"]["FilePayloadV1"]["properties"]["rev"] = {
        "$ref": "#/$defs/RevOuterV1", "properties": {"leaf": nodes[2]}}
    return d


def three_all_annotated(M):
    d = doc(M)
    d["$defs"]["RevInnerV1"] = {"type": "object", "properties": {"leaf": marked()}}
    d["$defs"]["RevOuterV1"] = {"$ref": "#/$defs/RevInnerV1",
                                "properties": {"leaf": marked()}}
    d["$defs"]["FilePayloadV1"]["properties"]["rev"] = {
        "$ref": "#/$defs/RevOuterV1", "properties": {"leaf": marked()}}
    return d


def conflicting(M, same):
    """Two annotations at one path: identical must admit, disagreeing must be a conflict."""
    d = doc(M)
    other = dict(ANN) if same else dict(ANN, authority="a-different-authority")
    d["$defs"]["RevAliasV1"] = dict(BARE, **{"x-opensip-digest": ANN})
    d["$defs"]["FilePayloadV1"]["properties"]["rev"] = {
        "$ref": "#/$defs/RevAliasV1", "x-opensip-digest": other}
    return d


def bad_retention(M):
    d = doc(M)
    d["$defs"]["FilePayloadV1"]["properties"]["rev"] = marked(
        dict(ANN, retention="invented-retention-value"))
    return d


def annotated_without_join(M):
    """Lawful retention, but the field is named by no join -> residue."""
    d = doc(M)
    d["$defs"]["FilePayloadV1"]["properties"]["rev"] = marked(
        dict(ANN, retention="preimage"))
    return d


def join_names_missing_field(M):
    d = doc(M)
    row = d["x-opensip-relation-registry"]["relations"]["file"]
    row["snapshotJoins"] = copy.deepcopy(row["snapshotJoins"])
    row["snapshotJoins"][0] = dict(row["snapshotJoins"][0],
                                   pathField="fieldThatDoesNotExist")
    return d


def unannotated_governed(M):
    d = doc(M)
    d["$defs"]["FilePayloadV1"]["properties"]["rev"] = dict(BARE)
    return d


def terminal_def_annotated(M):
    """Annotating the TERMINAL governed $def must NOT blanket-exempt every field of that form."""
    d = doc(M)
    d["$defs"]["DigestHex"] = dict(d["$defs"]["DigestHex"], **{"x-opensip-digest": ANN})
    d["$defs"]["FilePayloadV1"]["properties"]["rev"] = dict(BARE)
    return d


def alias_def_annotated(M):
    """An INTERMEDIATE alias $def annotation DOES cover the leaf that refs it."""
    d = doc(M)
    d["$defs"]["RevAliasV1"] = dict(BARE, **{"x-opensip-digest": ANN})
    d["$defs"]["FilePayloadV1"]["properties"]["rev"] = {"$ref": "#/$defs/RevAliasV1"}
    return d


def nullable_branch(M, annotate_parent):
    """Nullable oneOf: annotating the PARENT covers both branches; annotating only ONE branch
    leaves the sibling branch uncovered."""
    d = doc(M)
    node = {"oneOf": [dict(BARE), {"type": "null"}]}
    if annotate_parent:
        node["x-opensip-digest"] = ANN
    else:
        node["oneOf"][0] = marked()
    d["$defs"]["FilePayloadV1"]["properties"]["rev"] = node
    return d


def drop_bytelength_annotation(M):
    """file.byteLength is ANNOTATED but NOT governed (UInt64). Removing its annotation must not
    trigger the unannotated-governed limb: it is simply no longer a sighting."""
    d = doc(M)
    props = d["$defs"]["FilePayloadV1"]["properties"]
    assert "x-opensip-digest" in props["byteLength"], "precondition: byteLength is annotated"
    props["byteLength"] = {k: v for k, v in props["byteLength"].items()
                           if k != "x-opensip-digest"}
    return d


def nested_unjoinable(M):
    """A governed leaf nested one level deeper than the selector property cannot be addressed by
    value[field]; with a joined retention it must be refused as an unjoinable location."""
    d = doc(M)
    d["$defs"]["FilePayloadV1"]["properties"]["rev"] = {
        "type": "object",
        "properties": {"leaf": marked(dict(ANN, retention="preimage"))}}
    return d


# --------------------------------------------------------------------------------- probe table
PROBES = [
    ("container/unannotated-first refuses", "file",
     lambda M: same_path_container(M, "unannotated-first"), "RELATION_DIGEST_UNANNOTATED"),
    ("container/annotated-first refuses (THE v10 DEFECT)", "file",
     lambda M: same_path_container(M, "annotated-first"), "RELATION_DIGEST_UNANNOTATED"),
    ("keyorder/unannotated-first refuses", "file",
     lambda M: same_path_keyorder(M, "unannotated-first"), "RELATION_DIGEST_UNANNOTATED"),
    ("keyorder/annotated-first refuses (THE v10 DEFECT)", "file",
     lambda M: same_path_keyorder(M, "annotated-first"), "RELATION_DIGEST_UNANNOTATED"),
    ("three sightings, missing at 0", "file",
     lambda M: three_sightings(M, 0), "RELATION_DIGEST_UNANNOTATED"),
    ("three sightings, missing at 1", "file",
     lambda M: three_sightings(M, 1), "RELATION_DIGEST_UNANNOTATED"),
    ("three sightings, missing at 2", "file",
     lambda M: three_sightings(M, 2), "RELATION_DIGEST_UNANNOTATED"),
    ("POSITIVE CONTROL three all-annotated admits", "file",
     three_all_annotated, "ADMIT"),
    ("identical annotations admit", "file",
     lambda M: conflicting(M, True), "ADMIT"),
    ("conflicting annotations refuse", "file",
     lambda M: conflicting(M, False), "RELATION_DIGEST_ANNOTATION_CONFLICT"),
    ("invalid retention refuses", "file", bad_retention, "RELATION_DIGEST_RETENTION"),
    ("LIMB2 annotated field without join refuses", "file",
     annotated_without_join, "RELATION_DIGEST_LAW_RESIDUE"),
    ("LIMB3 join naming missing field refuses", "file",
     join_names_missing_field, "RELATION_JOIN_FIELD_UNKNOWN"),
    ("LIMB1 unannotated governed field refuses", "file",
     unannotated_governed, "RELATION_DIGEST_UNANNOTATED"),
    ("terminal governed $def does NOT blanket-exempt", "file",
     terminal_def_annotated, "RELATION_DIGEST_UNANNOTATED"),
    ("intermediate alias $def annotation DOES cover", "file",
     alias_def_annotated, "ADMIT"),
    ("nullable oneOf parent annotation covers branches", "file",
     lambda M: nullable_branch(M, True), "ADMIT"),
    ("nullable oneOf single-branch annotation leaves sibling uncovered", "file",
     lambda M: nullable_branch(M, False), "RELATION_DIGEST_UNANNOTATED"),
    ("non-governed byteLength annotation removal still ADMITS", "file",
     drop_bytelength_annotation, "ADMIT"),
    ("nested governed leaf with joined retention is unjoinable", "file",
     nested_unjoinable, "RELATION_DIGEST_UNJOINABLE_LOCATION"),
    ("POSITIVE CONTROL registered document admits", "file",
     lambda M: doc(M), "ADMIT"),
]

M11, M10 = load("m11", V11), load("m10", V10)
rows = []
for label, relation, build, expected in PROBES:
    r11 = verdict(M11, relation, build(M11))
    try:
        r10 = verdict(M10, relation, build(M10))
    except Exception as exc:
        r10 = "CONSTRUCTION_ERROR:" + type(exc).__name__
    rows.append({
        "probe": label,
        "expected": expected,
        "v11": r11,
        "v10": r10,
        "v11Correct": r11 == expected,
        "discriminates": r11 != r10,
        "v11Detail": detail(M11, relation, build(M11))[:200],
    })

summary = {
    "probeCount": len(rows),
    "allV11Correct": all(r["v11Correct"] for r in rows),
    "v11Failures": [r["probe"] for r in rows if not r["v11Correct"]],
    "discriminatingCount": sum(1 for r in rows if r["discriminates"]),
    "discriminating": [r["probe"] for r in rows if r["discriminates"]],
    "rows": rows,
}
print(json.dumps(summary, indent=2))
