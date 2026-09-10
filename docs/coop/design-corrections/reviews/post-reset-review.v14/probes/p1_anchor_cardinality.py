"""CB4-MUST-1: anchor cardinality and inventory representability, probed through ACTUAL
complete Run admission, with positive controls carrying their own fact."""
import copy, sys
sys.path.insert(0, "/tmp/opensip-design-corrections/post-reset-review.v14/probes")
from harness import CI, M, C, probe, emit

build, rekey = CI.build, CI.rekey
resync_witness, resync_proof_refs = CI.resync_witness, CI.resync_proof_refs

ALL_RELATIONS = sorted(M.RELATIONS)

# --- 0. The law is total over the registry, and min/max are both closed. -------------------
def law_totality():
    missing = [n for n, r in M.RELATIONS.items() if "anchorLaw" not in r]
    unclosed = [n for n, r in M.RELATIONS.items()
                if "cardinality" not in r["anchorLaw"] and "minimum" not in r["anchorLaw"]]
    return not missing and not unclosed and len(M.RELATIONS) == 13
probe("A0-every-one-of-13-relations-has-a-closed-anchor-law", "check", law_totality)

def shared_max_is_the_authority():
    """The source-text class declines a per-relation ceiling; the closed MAXIMUM therefore has
    to come from the common schema, or 'closed min/max' would be false."""
    anchors = M.SCHEMA["$defs"]["fact"]["properties"]["anchors"]
    cls = M.RELATION_DOCUMENT["x-opensip-relation-registry"]["anchorLaw"]["classes"]["source-text"]
    return (anchors.get("maxItems") == 100000 and anchors.get("uniqueItems") is True
            and "no additional relation-specific maximum" in cls["cardinality"]
            and "maxItems 100000" in cls["noIdentityEqualityPromise"])
probe("A1-the-closed-maximum-is-the-shared-schema-bound-not-absent", "check", shared_max_is_the_authority)

# --- 1. Positive controls: each class closes a Run with ITS OWN fact. ----------------------
for rel in ("file", "package", "vcs-change"):
    probe("A2-positive-zero-anchor-%s-inventory-fact-closes-a-run" % rel, "positive",
          lambda r=rel: M.close_run(*build(relation=r, has_match=True, resolved=True)))
for rel in ("declares", "references", "imports", "calls", "types", "reachability", "unresolved-edge"):
    probe("A3-positive-anchored-%s-fact-closes-a-run" % rel, "positive",
          lambda r=rel: M.close_run(*build(relation=r, has_match=True, resolved=True)))
probe("A4-positive-single-anchor-clones-fact-closes-a-run", "positive",
      lambda: M.close_run(*build(relation="clones", has_match=True, resolved=True)))

# --- 2. Negatives: every relation, its own fact, its own exact refusal. --------------------
def mutate_anchors(relation, transform, language="typescript", pure=False, path=None):
    run, objects, blobs = build(relation=relation, has_match=True, resolved=True,
                                universe_language=language, pure_syntax=pure, source_path=path)
    key = next(k for k, (d, v) in objects.items() if d == "fact")
    fact = copy.deepcopy(objects[key][1])
    fact["anchors"] = transform(fact["anchors"], objects, run)
    rekey(objects, key, fact, run)
    resync_witness(objects, blobs, run); resync_proof_refs(objects, blobs, run)
    return M.close_run(run, objects, blobs)

def borrowed(anchors, objects, run):
    row = next(r for r in objects[run["snapshotId"]][1]["sourceInventory"] if r["path"] == "tsconfig.json")
    return [{"path": row["path"], "blobDigest": row["sha256"], "startByte": 0, "endByte": row["bytes"]}]

# 2a. inventory relations must refuse ANY anchor - including a self-consistent one, not only a
#     borrowed one, since the defect is the free spelling axis rather than the wrong file.
for rel in ("file", "package", "vcs-change"):
    probe("A5-negative-%s-with-one-borrowed-anchor-refuses" % rel, "negative",
          lambda r=rel: mutate_anchors(r, borrowed),
          "FACT_ANCHOR_CARDINALITY:%s:inventory:expected=0:declared=1" % rel)

def self_consistent_anchor(anchors, objects, run):
    row = next(r for r in objects[run["snapshotId"]][1]["sourceInventory"] if r["path"] == "a.ts")
    return [{"path": row["path"], "blobDigest": row["sha256"], "startByte": 0, "endByte": row["bytes"]}]
probe("A6-negative-file-anchored-into-its-OWN-path-still-refuses", "negative",
      lambda: mutate_anchors("file", self_consistent_anchor),
      "FACT_ANCHOR_CARDINALITY:file:inventory:expected=0:declared=1")

# 2b. every source-text relation, unanchored, under a COMPILER universe (the reading the blind
#     report showed was previously enforced only inside the syntax guard).
SOURCE_TEXT = sorted(n for n, r in M.RELATIONS.items()
                     if r["anchorLaw"].get("class") == "source-text")
for rel in [r for r in SOURCE_TEXT if r not in ("control-flow","literal")]:
    probe("A7-negative-unanchored-%s-refuses-under-typescript" % rel, "negative",
          lambda r=rel: mutate_anchors(r, lambda a, o, u: []),
          "FACT_ANCHOR_CARDINALITY:%s:source-text:minimum=1:declared=0" % rel)
probe("A8-negative-unanchored-declares-refuses-under-rust", "negative",
      lambda: mutate_anchors("declares", lambda a, o, u: [], language="rust"),
      "FACT_ANCHOR_CARDINALITY:declares:source-text:minimum=1:declared=0")
probe("A9-negative-unanchored-declares-refuses-under-syntax", "negative",
      lambda: mutate_anchors("declares", lambda a, o, u: [], language="syntax", pure=True),
      "FACT_ANCHOR_CARDINALITY:declares:source-text:minimum=1:declared=0")

# 2c. clones: zero and two.
probe("A10-negative-zero-anchor-clones-refuses", "negative",
      lambda: mutate_anchors("clones", lambda a, o, u: []),
      "FACT_ANCHOR_CARDINALITY:clones:body-identity:expected=1:declared=0")
probe("A11-negative-two-anchor-clones-refuses", "negative",
      lambda: mutate_anchors("clones", lambda a, o, u: sorted(
          [a[0], dict(a[0], endByte=a[0]["endByte"] - 1)], key=C.canonical)),
      "FACT_ANCHOR_CARDINALITY:clones:body-identity:expected=1:declared=2")

# 2d. the ordering claim: cardinality is judged BEFORE the snapshot joins, so a fault that is
#     also a join fault is still reported as itself.
probe("A12-cardinality-is-reported-before-the-payload-join", "negative",
      lambda: mutate_anchors("package", borrowed),
      "FACT_ANCHOR_CARDINALITY:package:inventory:expected=0:declared=1")

# --- 3. The declared mirror must AGREE rather than silently diverge. -----------------------
def drift():
    saved = M.RELATIONS["clones"]["bodyIdentityJoin"]["anchorCardinality"]
    M.RELATIONS["clones"]["bodyIdentityJoin"]["anchorCardinality"] = 2
    try:
        return M.close_run(*build(relation="clones", has_match=True, resolved=True))
    finally:
        M.RELATIONS["clones"]["bodyIdentityJoin"]["anchorCardinality"] = saved
probe("A13-negative-a-drifted-mirror-cardinality-refuses", "negative", drift,
      "RELATION_ANCHOR_LAW_DRIFT")

def missing_law():
    saved = M.RELATIONS["file"].pop("anchorLaw")
    try:
        return M.close_run(*build(relation="file", has_match=True, resolved=True))
    finally:
        M.RELATIONS["file"]["anchorLaw"] = saved
probe("A14-negative-a-relation-with-no-anchor-law-refuses-rather-than-defaulting", "negative",
      missing_law, "RELATION_ANCHOR_LAW_MISSING:file")

# --- 4. Raw-byte inventory: empty and arbitrary binary, no invented UTF-8 decoding. --------
probe("A15-positive-empty-file-is-ordinary-inventory", "positive",
      lambda: CI.inventoried_raw_bytes(CI.EMPTY_BYTES, "empty.bin"))
probe("A16-positive-non-utf8-binary-is-ordinary-inventory", "positive",
      lambda: CI.inventoried_raw_bytes(CI.NON_UTF8_BYTES, "assets/logo.png"))
probe("A17-positive-non-utf8-binary-at-an-extensionless-path", "positive",
      lambda: CI.inventoried_raw_bytes(CI.NON_UTF8_BYTES, "NOTICE"))
probe("A18-negative-the-same-non-utf8-bytes-still-refuse-as-a-code-span", "negative",
      lambda: CI.inventoried_raw_bytes(CI.NON_UTF8_BYTES, "assets/logo.png",
                                       anchor_a_code_fact=True), "ANCHOR_UTF8")

emit("/tmp/opensip-design-corrections/post-reset-review.v14/evidence/probe-cb4-must-1.json",
     {"relationsCovered": ALL_RELATIONS, "sourceTextClass": SOURCE_TEXT})
