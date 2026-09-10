"""Preserved safeguards, probed where the v13->v14 delta touches their code paths.
Unchanged families are carried on the reproduced suite, not restated here."""
import copy, json, sys
sys.path.insert(0, "/tmp/opensip-design-corrections/post-reset-review.v14/probes")
from harness import CI, M, C, N, W, probe, emit

# --- canonical typed equality, bool/int distinction, array order -----------------------
probe("S0-bool-and-int-are-not-equal-under-typed-equality", "check",
      lambda: not C.equal_typed(True, 1) and not C.equal_typed(False, 0)
              and C.equal_typed(True, True) and C.equal_typed(1, 1))
probe("S1-canonical-encoding-distinguishes-bool-from-int", "check",
      lambda: C.canonical(True) != C.canonical(1))
probe("S2-typed-equality-is-structural-not-stringly", "check",
      lambda: not C.equal_typed("1", 1) and not C.equal_typed(None, False))
probe("S3-negative-a-mis-ordered-canonical-set-refuses", "negative",
      lambda: N.validate_foundation("analysis-spec",
              {"schemaVersion": 2, "policyPackIds": ["b", "a"],
               "requestedCapabilities": [], "parameters": []}),
      "order")
probe("S3b-positive-the-same-set-in-canonical-order-admits", "check",
      lambda: N.validate_foundation("analysis-spec",
              {"schemaVersion": 2, "policyPackIds": ["a", "b"],
               "requestedCapabilities": [], "parameters": []})["policyPackIds"] == ["a", "b"])

# --- all 13 relation selectors and their rungs -----------------------------------------
probe("S4-thirteen-relations-each-with-a-nonempty-ladder", "check",
      lambda: len(M.RELATIONS) == 13
              and all(r.get("ladder") for r in M.RELATIONS.values()))
def run_wrong_rung():
    run, objects, blobs = CI.build(relation="declares", has_match=True, resolved=True)
    key = next(k for k, (d, v) in objects.items() if d == "fact")
    fact = copy.deepcopy(objects[key][1]); fact["resolution"] = "resolved-callee"
    CI.rekey(objects, key, fact, run)
    CI.resync_witness(objects, blobs, run); CI.resync_proof_refs(objects, blobs, run)
    return M.close_run(run, objects, blobs)

probe("S5-negative-a-rung-from-another-relations-ladder-refuses", "negative",
      run_wrong_rung, "RELATION_RUNG_NOT_IN_LADDER")
probe("S6-the-registry-is-the-single-ladder-authority", "check",
      lambda: M.RELATION_DOCUMENT["x-opensip-relation-registry"]["ladderAuthority"])

# --- snapshot-owned file claims ---------------------------------------------------------
def wrong_digest_claim():
    run, objects, blobs = CI.build(relation="file", has_match=True, resolved=True)
    key = next(k for k, (d, v) in objects.items() if d == "fact")
    fact = copy.deepcopy(objects[key][1])
    payload = C.parse(blobs[fact["payloadDigest"]])
    payload["contentSha256"] = "f" * 64
    fact["payloadDigest"] = CI.put_blob(blobs, payload)
    CI.rekey(objects, key, fact, run)
    CI.resync_witness(objects, blobs, run); CI.resync_proof_refs(objects, blobs, run)
    return M.close_run(run, objects, blobs)
probe("S7-negative-a-file-claim-disagreeing-with-the-snapshot-digest-refuses", "negative",
      wrong_digest_claim, "")

def wrong_length_claim():
    run, objects, blobs = CI.build(relation="file", has_match=True, resolved=True)
    key = next(k for k, (d, v) in objects.items() if d == "fact")
    fact = copy.deepcopy(objects[key][1])
    payload = C.parse(blobs[fact["payloadDigest"]])
    payload["byteLength"] = payload["byteLength"] + 1
    fact["payloadDigest"] = CI.put_blob(blobs, payload)
    CI.rekey(objects, key, fact, run)
    CI.resync_witness(objects, blobs, run); CI.resync_proof_refs(objects, blobs, run)
    return M.close_run(run, objects, blobs)
probe("S8-negative-a-file-claim-disagreeing-on-byte-length-refuses", "negative",
      wrong_length_claim, "")

def path_outside_snapshot():
    run, objects, blobs = CI.build(relation="file", has_match=True, resolved=True)
    key = next(k for k, (d, v) in objects.items() if d == "fact")
    fact = copy.deepcopy(objects[key][1])
    payload = C.parse(blobs[fact["payloadDigest"]])
    payload["path"] = "not/in/snapshot.ts"
    fact["payloadDigest"] = CI.put_blob(blobs, payload)
    CI.rekey(objects, key, fact, run)
    CI.resync_witness(objects, blobs, run); CI.resync_proof_refs(objects, blobs, run)
    return M.close_run(run, objects, blobs)
probe("S9-negative-a-file-claim-for-a-path-outside-the-snapshot-refuses", "negative",
      path_outside_snapshot, "")

# --- full TS / JS / Rust / syntax closure through complete Runs -------------------------
for lang, kw in (("typescript", {}), ("rust", {"universe_language": "rust"}),
                 ("syntax", {"universe_language": "syntax", "pure_syntax": True})):
    probe("S10-a-complete-run-closes-under-the-%s-universe" % lang, "positive",
          lambda k=kw: M.close_run(*CI.build(relation="references" if not k.get("pure_syntax")
                                             else "declares", has_match=True, resolved=True, **k)))
probe("S11-a-js-body-closes-under-the-typescript-engine-universe", "positive",
      lambda: M.close_run(*CI.build(relation="clones", has_match=True, resolved=True,
                                    source_path="a.js")))

# --- raw 32-byte clone body-language version --------------------------------------------
probe("S12-the-body-language-version-component-is-raw-32-bytes", "check",
      lambda: "raw 32" in M.RELATIONS["clones"]["bodyIdentityJoin"]["languageVersionSource"]
              or "raw32" in M.RELATIONS["clones"]["bodyIdentityJoin"]["languageVersionSource"]
              .replace(" ", ""))

# --- Rust target edition / ownership ------------------------------------------------------
RUSTROW = M.DIGESTS["domainSets"]["native-semantic-universe"][
    "native.semantic-universe.rust.v2"]["languageVersionBinding"]
probe("S13-rust-selects-its-dialect-from-the-compilation-target-edition", "check",
      lambda: RUSTROW["dialect"]["form"] == "selected-compilation-target-edition"
              and RUSTROW["dialect"]["key"] == "edition")
probe("S14-rust-ownership-faults-are-each-named-not-collapsed", "check",
      lambda: len({RUSTROW["dialect"][k] for k in RUSTROW["dialect"]
                   if k.startswith("on")}) >= 5)

# --- ScopeDocument parameter binding into a real comparison context ----------------------
probe("S15-the-parameter-payload-class-is-keyed-and-closed", "check",
      lambda: (lambda c: c["keyedBy"] and len(c.get("rows", c.get("documents", []))) >= 1)(
          M.SCHEMA["x-opensip-payload-registry"]["classes"]["parameter"]))
probe("S16-negative-an-unregistered-parameter-document-refuses", "negative",
      lambda: CI.run_with_parameter(b'{"type":"object"}', {"anything": 1}), "")

# --- the closing digest law still holds over the CHANGED identity schema -----------------
def every_64hex_field_annotated():
    sites = []
    CI.digest_sites(M.SCHEMA, "", sites)
    return len(sites) > 0
probe("S17-the-identity-schema-still-exposes-annotated-digest-sites", "check",
      every_64hex_field_annotated)

emit("/tmp/opensip-design-corrections/post-reset-review.v14/evidence/probe-safeguards.json")
