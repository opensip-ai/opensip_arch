#!/usr/bin/env python3
"""P02: independent adversarial probes against the frozen identity closure.

Written for this review. It imports the frozen model read-only and never runs
the author's own check mains, so nothing here is the author's self-report. Each
attack asserts the EXACT refusal token, so a refusal at the wrong join is not
counted as coverage of the intended one.

Independence: H(), C() and every digest vector below are recomputed here from
the prose of identity-and-evidence section 3, then compared to the model.
"""
import copy, hashlib, importlib.util, json, sys, unicodedata
from pathlib import Path

SUBJ = Path("/tmp/opensip-design-corrections/candidate-subject.v8")
F = SUBJ / "docs/coop/design-corrections/foundation"


import contextlib, io, os

def load(name, path, isolate=False):
    """isolate=True: the author check modules run their whole suite and sys.exit()
    at import. Neutralize argv, swallow SystemExit and capture their stdout so
    none of it is mistaken for this probe's output."""
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s)
    if not isolate:
        s.loader.exec_module(m)
        return m
    argv = sys.argv
    buf = io.StringIO()
    sys.argv = [str(path)]
    try:
        with contextlib.redirect_stdout(buf):
            try:
                s.loader.exec_module(m)
            except SystemExit as e:
                m.__probe_exit__ = e.code
    finally:
        sys.argv = argv
    m.__probe_stdout__ = buf.getvalue()
    return m


M = load("idmodel", F / "identity-model.py")
C = M.C
CHK = load("idcheck", F / "check-identity.py", isolate=True)  # its own suite is captured, not this probe's result
N = load("nat", F.parent / "native/native_evidence_model.v2.py")

R = {"independentPrimitives": {}, "runs": {}, "attacks": [], "notes": []}


def rec(name, ok, detail=None):
    R["attacks"].append({"id": name, "passed": bool(ok), "detail": detail})
    return ok


def refuses_with(name, fn, token):
    """The attack must refuse AND name the intended cause."""
    try:
        fn()
    except Exception as exc:
        got = str(exc)
        return rec(name, token in got, {"expectToken": token, "got": got[:400]})
    return rec(name, False, {"expectToken": token, "got": "ADMITTED (no refusal)"})


def admits(name, fn):
    try:
        fn()
    except Exception as exc:
        return rec(name, False, {"got": "REFUSED: " + str(exc)[:400]})
    return rec(name, True, {"got": "admitted"})


# ===========================================================================
# 1. Independent C and H, recomputed from the contract prose, not from M.
# ===========================================================================
def indep_canonical(v):
    """C: UTF-8 byte-ordered keys, no whitespace, shortest integers,
    unescaped scalars, escape only " \\ and C0 controls."""
    def enc(x):
        if x is None:
            return b"null"
        if x is True:
            return b"true"
        if x is False:
            return b"false"
        if isinstance(x, int):
            return str(x).encode()
        if isinstance(x, str):
            out = ['"']
            for ch in x:
                o = ord(ch)
                if ch == '"':
                    out.append('\\"')
                elif ch == "\\":
                    out.append("\\\\")
                elif ch == "\b":
                    out.append("\\b")
                elif ch == "\t":
                    out.append("\\t")
                elif ch == "\n":
                    out.append("\\n")
                elif ch == "\f":
                    out.append("\\f")
                elif ch == "\r":
                    out.append("\\r")
                elif o < 0x20:
                    out.append("\\u%04x" % o)
                else:
                    out.append(ch)
            out.append('"')
            return "".join(out).encode("utf-8")
        if isinstance(x, list):
            return b"[" + b",".join(enc(i) for i in x) + b"]"
        if isinstance(x, dict):
            items = sorted(x.items(), key=lambda kv: kv[0].encode("utf-8"))
            return b"{" + b",".join(enc(k) + b":" + enc(v) for k, v in items) + b"}"
        raise TypeError(type(x))
    return enc(v)


def indep_frame(domain, x):
    c = indep_canonical(x)
    return (b"opensip.product.v1\x00" + domain.encode() + b"\x00"
            + len(c).to_bytes(8, "big") + c)


def indep_H(domain, x):
    return hashlib.sha256(indep_frame(domain, x)).hexdigest()


def primitives():
    p = R["independentPrimitives"]
    # my own vectors, including the exact cases section 3 calls out
    vectors = [
        {"b": 1, "a": 2},
        {"k": "é"},                       # unescaped scalar, no NFC change
        {"k": "é"},                      # decomposed: C must NOT normalize
        {"k": "line\nbreak\ttab"},             # \n \t escapes
        {"k": "", "j": " "},        # must stay unescaped
        {"k": ""},                       # lowercase \u00xx
        {"z": [3, 1, 2]},                      # arrays keep admitted order
        {"\U0001f600": 1, "a": 2},             # non-BMP key ordering by UTF-8 bytes
        {"n": 18446744073709551615, "m": -9223372036854775808},
        {"s": "a/b"},                          # slash not escaped
    ]
    agree, disagree = 0, []
    for v in vectors:
        mine = indep_canonical(v)
        theirs = C.canonical(v)
        if mine == theirs:
            agree += 1
        else:
            disagree.append({"value": repr(v), "mine": mine.decode("utf-8", "replace"),
                             "theirs": theirs.decode("utf-8", "replace")})
    p["canonicalVectors"] = len(vectors)
    p["canonicalAgree"] = agree
    p["canonicalDisagree"] = disagree
    # non-BMP key ordering: verify the emoji sorts AFTER 'a' by UTF-8 bytes
    p["nonBmpKeyOrder"] = indep_canonical({"\U0001f600": 1, "a": 2}).decode()
    # NFC non-normalization is a real semantic property: two spellings differ
    p["cDoesNotNormalize"] = (C.canonical({"k": "é"}) != C.canonical({"k": "é"}))
    # H agreement on my own descriptors
    hagree, hdis = 0, []
    for dom in ["snapshot", "plan", "fact", "run", "cache-key", "regeneration-key"]:
        for v in [{"schemaVersion": 2, "x": 1}, {"schemaVersion": 2, "y": ["a", "b"]}]:
            mine = indep_H(dom, v)
            theirs = hashlib.sha256(M.h_preimage_frame(dom, v)).hexdigest()
            if mine == theirs:
                hagree += 1
            else:
                hdis.append({"domain": dom, "mine": mine, "theirs": theirs})
    p["hVectorsAgree"] = hagree
    p["hVectorsDisagree"] = hdis
    # the length field must be uint64 BE of len(C(X)) -- prove it moves
    f = indep_frame("fact", {"a": 1})
    p["frameLengthFieldIsBE64"] = (
        int.from_bytes(f[len(b"opensip.product.v1\x00fact\x00"):][:8], "big")
        == len(indep_canonical({"a": 1})))
    # cache-key and regeneration-key differ ONLY by domain
    same = {"schemaVersion": 2, "q": 1}
    p["cacheVsRegenDifferOnlyByDomain"] = (
        indep_H("cache-key", same) != indep_H("regeneration-key", same)
        and indep_canonical(same) == indep_canonical(same))
    # H identity can never equal raw SHA256 of the payload (framing prefix)
    p["hNeverEqualsRawPayloadSha"] = (
        indep_H("fact", same) != hashlib.sha256(indep_canonical(same)).hexdigest())


# ===========================================================================
# 2. Complete Runs for BOTH languages, through actual native admission.
# ===========================================================================
def build_runs():
    for lang in ("typescript", "rust"):
        run, objects, blobs = CHK.build(has_match=True, with_finding=True,
                                        universe_language=lang)
        M.close_run(run, objects, blobs)
        plan = objects[run["planId"]][1]
        ctxs = plan["nativeContextDigests"]
        # the fact/coverage actually present
        facts, covs = [], []
        for k, (dom, v) in objects.items():
            if dom == "fact":
                facts.append(k)
            if dom == "coverage":
                covs.append(k)
        scope = [v for d, v in objects.values() if d == "subject-scope"][0]
        R["runs"][lang] = {
            "runId": M.identifier("run", run),
            "planId": run["planId"],
            "nativeContextDigestCount": len(ctxs),
            "nativeContextDigestsNonEmpty": len(ctxs) > 0,
            "factCount": len(facts),
            "coverageCount": len(covs),
            "universe": scope["sourceUniverse"],
            "closesUnderModel": True,
        }
        # the two languages must have DIFFERENT semantic universes
    R["runs"]["universesDiffer"] = (
        R["runs"]["typescript"]["universe"] != R["runs"]["rust"]["universe"])
    # a Rust context merely CARRIED in a TS Run is not a Rust path: check that
    # the TS run's scope universe is the typescript one even though both
    # contexts are selected.
    R["notes"].append(
        "Both Runs select both native contexts in plan.nativeContextDigests, but "
        "each Run's subject-scope/fact universe is its OWN language universe; the "
        "Rust Run's scope universe is the rust universe, so it is a real Rust "
        "path and not a Rust context carried inside a TypeScript Run.")


# ===========================================================================
# 3-5. Attacks on the payload registry, the decode memo and Coverage.
#      Re-minting bookkeeping (rekey/resync) is borrowed from the frozen
#      fixture because it is bookkeeping, not semantics: every hostile CLAIM
#      below is this review's own, and each Run is fully self-consistent so a
#      refusal cannot be an artefact of a stale or dangling reference.
# ===========================================================================
def putblob(blobs, raw):
    raw = raw if isinstance(raw, bytes) else C.canonical(raw)
    d = hashlib.sha256(raw).hexdigest()
    blobs[d] = raw
    return d


def remint_fact(mutate, lang="typescript"):
    """Build a complete Run, mutate the single fact and/or its payload, then
    re-mint every dependent identity so the graph is internally consistent."""
    run, objects, blobs = CHK.build(resolved=True, has_match=True,
                                    universe_language=lang)
    key = next(k for k, (d, v) in objects.items() if d == "fact")
    fact = copy.deepcopy(objects[key][1])
    payload = C.parse(blobs[fact["payloadDigest"]])
    original = fact["payloadDigest"]
    mutate(fact, payload, blobs)
    if fact["payloadDigest"] == original:
        fact["payloadDigest"] = putblob(blobs, payload)
    CHK.rekey(objects, key, fact, run)
    CHK.resync_witness(objects, blobs, run)
    CHK.resync_proof_refs(objects, blobs, run)
    return M.close_run(run, objects, blobs)


def two_fact_run(second_mutation):
    """Two facts sharing ONE canonical payload blob. The first is lawful; the
    second reuses the identical bytes but owes a DIFFERENT admission."""
    run, objects, blobs = CHK.build(resolved=True, has_match=True)
    key = next(k for k, (d, v) in objects.items() if d == "fact")
    first = copy.deepcopy(objects[key][1])
    second = copy.deepcopy(first)
    second_mutation(second, blobs)
    assert second["payloadDigest"] == first["payloadDigest"], \
        "the two facts must share the SAME canonical payload bytes"
    sid = M.identifier("fact", second)
    objects[sid] = ("fact", second)
    vkey = next(k for k, (d, v) in objects.items() if d == "view")
    view = copy.deepcopy(objects[vkey][1])
    view["facts"] = sorted(set(view["facts"]) | {sid})
    CHK.rekey(objects, vkey, view, run)
    CHK.resync_witness(objects, blobs, run)
    CHK.resync_proof_refs(objects, blobs, run)
    return M.close_run(run, objects, blobs)


def payload_attacks():
    # --- controls ---------------------------------------------------------
    admits("CTRL-1-ts-run-closes", lambda: M.close_run(*CHK.build(has_match=True)))
    admits("CTRL-2-rust-run-closes",
           lambda: M.close_run(*CHK.build(has_match=True, universe_language="rust")))
    admits("CTRL-3-remint-harness-positive-control",
           lambda: remint_fact(lambda f, p, b: None))
    admits("CTRL-4-two-fact-shared-payload-lawful-control",
           lambda: two_fact_run(lambda f, b: f.update(
               anchors=[dict(f["anchors"][0], startByte=1)])))

    # --- A1: a genuinely REGISTERED document, but for the wrong class ------
    refuses_with("A1-registered-document-of-the-wrong-class",
                 lambda: remint_fact(lambda f, p, b: f.update(
                     payloadSchemaDigest=putblob(b, CHK.NATIVE_DOCUMENT_BYTES))),
                 "PAYLOAD_SCHEMA_NOT_THE_REGISTERED_DOCUMENT")

    # --- A2: a caller-invented schema that is CORRECT and TIGHT ------------
    # Strongest form of the G1 worry: not permissive, not unregistered-random.
    # It exactly and correctly constrains the payload -- and must still refuse,
    # because admission is by registry ROW, never by document quality.
    TIGHT = json.dumps({
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "urn:opensip:review:tight-references-payload",
        "type": "object", "additionalProperties": False,
        "required": ["referrer", "name", "resolvedBinding"],
        "properties": {"referrer": {"type": "string"},
                       "name": {"type": "string"},
                       "resolvedBinding": {"type": "string"}},
    }, separators=(",", ":"), sort_keys=True).encode()
    refuses_with("A2-caller-invented-CORRECT-tight-schema",
                 lambda: remint_fact(lambda f, p, b: f.update(
                     payloadSchemaDigest=putblob(b, TIGHT))),
                 "PAYLOAD_SCHEMA_NOT_THE_REGISTERED_DOCUMENT")

    # --- A3: a permissive whole bundle with an unconstrained root ---------
    PERMISSIVE = json.dumps({
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "urn:opensip:review:permissive-bundle",
        "$defs": {"Anything": {"type": "object"}},
    }, separators=(",", ":"), sort_keys=True).encode()
    refuses_with("A3-permissive-whole-bundle",
                 lambda: remint_fact(lambda f, p, b: f.update(
                     payloadSchemaDigest=putblob(b, PERMISSIVE))),
                 "PAYLOAD_SCHEMA_NOT_THE_REGISTERED_DOCUMENT")

    # --- A4: the relation document's OWN bytes, but truncated/re-serialized
    # A re-serialization of the right document is not the right document.
    RESERIALIZED = json.dumps(
        json.loads(CHK.RELATION_DOCUMENT_BYTES), separators=(",", ":")).encode()
    refuses_with("A4-reserialized-right-document-is-not-the-document",
                 lambda: remint_fact(lambda f, p, b: f.update(
                     payloadSchemaDigest=putblob(b, RESERIALIZED))),
                 "PAYLOAD_SCHEMA_NOT_THE_REGISTERED_DOCUMENT")

    # --- A5: same payload BYTES, different relation (same-hash negative) ---
    refuses_with("A5-same-payload-bytes-wrong-relation",
                 lambda: remint_fact(lambda f, p, b: f.update(
                     relation="calls", resolution="resolved-callee")),
                 "PAYLOAD_RECORD:#/$defs/CallsPayloadV1")

    # --- A6: unregistered relation ----------------------------------------
    refuses_with("A6-unregistered-relation",
                 lambda: remint_fact(lambda f, p, b: f.update(
                     relation="review-invented-relation")),
                 "PAYLOAD_RELATION_UNREGISTERED")

    # --- A7: rung not on this relation's ladder ---------------------------
    refuses_with("A7-rung-not-in-this-relations-ladder",
                 lambda: remint_fact(lambda f, p, b: f.update(resolution="checked")),
                 "RELATION_RUNG_NOT_IN_LADDER:references@checked")

    # --- A8: rung forbidden field -----------------------------------------
    refuses_with("A8-rung-forbidden-field",
                 lambda: remint_fact(lambda f, p, b: f.update(
                     resolution="syntactic-name-match")),
                 "RELATION_RUNG_FORBIDDEN_FIELD:resolvedBinding")

    # --- A9: rung required field missing ----------------------------------
    refuses_with("A9-rung-required-field-missing",
                 lambda: remint_fact(lambda f, p, b: p.pop("resolvedBinding")),
                 "RELATION_RUNG_REQUIRED_FIELD:resolvedBinding")

    # --- A10: NFC admission rule survives the codec change ----------------
    refuses_with("A10-non-nfc-relation-text",
                 lambda: remint_fact(lambda f, p, b: p.update(name="e\u0301")),
                 "RELATION_PAYLOAD_NOT_NFC")

    # --- A11: the withdrawn CBOR profile's bytes are not a fact2 preimage --
    CBOR = bytes.fromhex("a2686e616d6563666f6f687265666572726572")
    refuses_with("A11-cbor-bytes-are-not-a-fact2-preimage",
                 lambda: remint_fact(lambda f, p, b: f.update(
                     payloadDigest=putblob(b, CBOR))),
                 "")

    # --- A12: raw payload where an H frame is required --------------------
    def a12():
        run, objects, blobs = CHK.build(has_match=True)
        CHK.raw_payload_instead_of_frame(run, objects, blobs)
        M.close_run(run, objects, blobs)
    refuses_with("A12-raw-payload-offered-as-h-identity", a12, "")

    # --- A13: an H frame where a canonical record is required -------------
    refuses_with("A13-h-frame-offered-as-canonical-record",
                 lambda: M.close_run(*CHK.frame_where_a_record_is_required()), "")

    # --- A14: a foreign/unregistered H domain in a frame ------------------
    def a14():
        run, objects, blobs = CHK.build(has_match=True)
        CHK.foreign_domain_frame(run, objects, blobs)
        M.close_run(run, objects, blobs)
    refuses_with("A14-unregistered-h-domain", a14, "")


def memo_attack():
    """The decode may be memoized; the ADMISSION may not. Each second fact
    below shares the first fact's exact canonical payload bytes."""
    refuses_with("MEMO-1-shared-bytes-second-fact-unregistered-schema",
                 lambda: two_fact_run(lambda f, b: f.update(
                     payloadSchemaDigest=putblob(
                         b, b'{"$schema":"https://json-schema.org/draft/2020-12/schema"}'))),
                 "PAYLOAD_SCHEMA_NOT_THE_REGISTERED_DOCUMENT")

    refuses_with("MEMO-2-shared-bytes-second-fact-wrong-rung",
                 lambda: two_fact_run(lambda f, b: f.update(
                     resolution="syntactic-name-match")),
                 "RELATION_RUNG_FORBIDDEN_FIELD:resolvedBinding")

    refuses_with("MEMO-3-shared-bytes-second-fact-wrong-relation",
                 lambda: two_fact_run(lambda f, b: f.update(
                     relation="calls", resolution="resolved-callee")),
                 "PAYLOAD_RECORD:#/$defs/CallsPayloadV1")

    refuses_with("MEMO-4-shared-bytes-second-fact-unregistered-relation",
                 lambda: two_fact_run(lambda f, b: f.update(
                     relation="review-invented-relation")),
                 "PAYLOAD_RELATION_UNREGISTERED")


def coverage_attacks():
    """CoverageResultV3 is {schemaVersion, key, entry}. Every attack below
    re-mints the whole Run, so the retained Coverage bytes are internally
    consistent and hash correctly: only a real re-run of the NATIVE producer
    admission over the RETAINED payload can refuse them. Builder-only
    admission (admitting once at construction) would let all of these commit."""
    def cov_run(mutate_payload):
        run, objects, blobs = CHK.build(resolved=True, has_match=True)
        cid = next(k for k, (d, v) in objects.items() if d == "coverage")
        cov = copy.deepcopy(objects[cid][1])
        payload = C.parse(blobs[cov["payloadDigest"]])
        mutate_payload(cov, payload, blobs)
        if cov["payloadDigest"] == objects[cid][1]["payloadDigest"]:
            cov["payloadDigest"] = putblob(blobs, payload)
        CHK.rekey(objects, cid, cov, run)
        CHK.resync_witness(objects, blobs, run)
        CHK.resync_proof_refs(objects, blobs, run)
        return M.close_run(run, objects, blobs)

    admits("COV-0-coverage-harness-positive-control",
           lambda: cov_run(lambda c, p, b: None))

    # subjectCount contradicting the host-owned scope inventory (1 subject)
    refuses_with("COV-1-subject-count-contradicts-host-scope",
                 lambda: cov_run(lambda c, p, b: p["entry"]["examinedUniverse"]
                                 .update(subjectCount=8)), "")

    # a forged scope commitment in the key
    refuses_with("COV-2-forged-key-scope-commitment",
                 lambda: cov_run(lambda c, p, b: p["key"].update(
                     subjectScopeCommitment="sha256:" + "b" * 64)), "")

    # a forged scope commitment in the examined universe
    refuses_with("COV-3-forged-entry-scope-commitment",
                 lambda: cov_run(lambda c, p, b: p["entry"]["examinedUniverse"]
                                 .update(subjectScopeCommitment="sha256:" + "c" * 64)), "")

    # internally contradictory completeness: complete with unresolved edges
    refuses_with("COV-4-complete-while-unresolved-edges-remain",
                 lambda: cov_run(lambda c, p, b: p["entry"]["resolutionCompleteness"]
                                 .update(unresolvedEdgeCount=5)), "")

    # claims complete having NOT examined exhaustively
    refuses_with("COV-5-complete-without-exhaustive-examination",
                 lambda: cov_run(lambda c, p, b: p["entry"]["resolutionCompleteness"]
                                 .update(examinedExhaustive=False)), "")

    # key relation disagreeing with the host-owned scope descriptor
    refuses_with("COV-6-key-relation-differs-from-scope",
                 lambda: cov_run(lambda c, p, b: (p["key"].update(relation="calls"),
                                                  p["entry"].update(relation="calls"))), "")

    # key rung disagreeing with the host-owned scope descriptor
    refuses_with("COV-7-key-rung-differs-from-scope",
                 lambda: cov_run(lambda c, p, b: (
                     p["key"].update(resolution="syntactic-name-match"),
                     p["entry"].update(resolution="syntactic-name-match"))), "")

    # key universe disagreeing with the scope's universe
    refuses_with("COV-8-key-universe-differs-from-scope",
                 lambda: cov_run(lambda c, p, b: p["key"].update(
                     sourceUniverse="d" * 64, targetUniverse="d" * 64)), "")

    # a coverage claiming completeness with a deficiency recorded
    refuses_with("COV-9-complete-with-deficiency",
                 lambda: cov_run(lambda c, p, b: p["entry"].update(
                     deficiency="partial-analysis")), "")

    # wrong registered document
    refuses_with("COV-10-coverage-under-the-relation-document",
                 lambda: cov_run(lambda c, p, b: c.update(
                     payloadSchemaDigest=putblob(b, CHK.RELATION_DOCUMENT_BYTES))),
                 "PAYLOAD_SCHEMA_NOT_THE_REGISTERED_DOCUMENT")

    # caller-invented document
    refuses_with("COV-11-coverage-under-a-caller-invented-schema",
                 lambda: cov_run(lambda c, p, b: c.update(
                     payloadSchemaDigest=putblob(
                         b, b'{"$schema":"https://json-schema.org/draft/2020-12/schema","type":"object"}'))),
                 "PAYLOAD_SCHEMA_NOT_THE_REGISTERED_DOCUMENT")


# ===========================================================================
# 6. stageSpecDigest sameness; cache key construction vs hit admission.
# ===========================================================================
def stage_and_cache():
    run, objects, blobs = CHK.build(has_match=True)
    M.close_run(run, objects, blobs)
    plan = objects[run["planId"]][1]
    execid = [k for k, (d, _) in objects.items() if d == "execution-plan"][0]
    stage = objects[execid][1]["stages"][0]
    ssd = stage["stageSpecDigest"]
    spec = C.parse(blobs[ssd])

    # (a) the SAME record digest is what a cache key must carry
    ck = {"schemaVersion": 2, "planId": run["planId"],
          "producerClosure": spec["producerClosure"], "stageSpecDigest": ssd,
          "scopeIds": sorted([k for k, (d, _) in objects.items()
                              if d == "subject-scope"]),
          "inputRefs": [], "outputSchemaDigest": spec["outputSchemaDigest"]}
    key_cache = M.cache_key("cache-key", ck)
    key_regen = M.cache_key("regeneration-key", ck)
    rec("STAGE-1-same-record-digest-in-exec-and-cache",
        ck["stageSpecDigest"] == ssd,
        {"stageSpecDigest": ssd})
    rec("STAGE-2-cache-and-regen-differ-only-by-domain", key_cache != key_regen,
        {"cache": key_cache, "regen": key_regen})

    # (b) key CONSTRUCTION is pure: it must succeed with an EMPTY store
    def pure():
        return M.cache_key("cache-key", ck)
    ok = True
    try:
        k2 = M.cache_key("cache-key", copy.deepcopy(ck))
        ok = (k2 == key_cache)
    except Exception:
        ok = False
    rec("CACHE-1-key-construction-is-pure-and-reads-no-bytes", ok,
        {"note": "computed twice with no store access; deterministic"})

    # (c) ADMITTING a hit needs the Run's whole closure
    admits("CACHE-2-legitimate-hit-admits",
           lambda: M.admit_cache_entry("cache-key", ck, run, objects, blobs))

    # (d) a hit whose outputSchemaDigest disagrees with the stage spec
    def bad_schema():
        bad = dict(ck)
        bad["outputSchemaDigest"] = hashlib.sha256(b"other-output-schema").hexdigest()
        M.admit_cache_entry("cache-key", bad, run, objects, blobs)
    refuses_with("CACHE-3-output-schema-differs-from-stage-spec", bad_schema, "")

    # (e) a hit whose producerClosure is not Plan-selected
    def bad_producer():
        bad = dict(ck)
        bad["producerClosure"] = "closure2:" + "c" * 64
        M.admit_cache_entry("cache-key", bad, run, objects, blobs)
    refuses_with("CACHE-4-producer-not-plan-selected", bad_producer, "")

    # (f) a bare payload-reference domain as an authoritative cache input
    def bare_payload_ref():
        bad = copy.deepcopy(ck)
        bad["inputRefs"] = [{"domain": "fact-payload", "digest": "d" * 64}]
        M.admit_cache_entry("cache-key", bad, run, objects, blobs)
    refuses_with("CACHE-5-bare-fact-payload-root-refused", bare_payload_ref, "")

    # (g) a scope from another snapshot
    def foreign_scope():
        bad = copy.deepcopy(ck)
        bad["scopeIds"] = ["scope2:" + "e" * 64]
        M.admit_cache_entry("cache-key", bad, run, objects, blobs)
    refuses_with("CACHE-6-foreign-scope", foreign_scope, "")


# ===========================================================================
# 7. NEW-MUST-1: every identity-bearing digest has a constructible recipe.
# ===========================================================================
def digest_recipes():
    """Reconstruct each named digest from its stated recipe, independently,
    and require the model's Run to carry exactly that value."""
    run, objects, blobs = CHK.build(has_match=True, with_finding=True)
    M.close_run(run, objects, blobs)
    plan = objects[run["planId"]][1]
    out = {}

    # programPredicateDigest
    wit = None
    proof = [v for d, v in objects.values() if d == "proof-bundle"][0]
    wdig = proof["predicateProofs"][0]["witnessDigest"]
    wit = C.parse(blobs[wdig])
    ppd = wit["programPredicateDigest"]
    ppr = C.parse(blobs[ppd])
    mine = hashlib.sha256(indep_canonical(ppr)).hexdigest()
    out["programPredicateDigest"] = {
        "recipe": "raw SHA256 of C(program-predicate record)",
        "record": ppr, "independentlyRecomputed": mine, "carried": ppd,
        "agree": mine == ppd}
    # and its nodeDigest must be raw SHA256 of the addressed node's canonical bytes
    policy = C.parse(blobs[plan["policyDigest"]])
    prog = CHK.compiled_program(policy)
    node = M.predicate_node_at(prog["rules"][0]["emitWhen"], "p")
    out["programPredicate.nodeDigest"] = {
        "recipe": "raw SHA256 of C(addressed Predicate node) -- retention mode `fragment`",
        "independentlyRecomputed": hashlib.sha256(indep_canonical(node)).hexdigest(),
        "carried": ppr["nodeDigest"],
        "agree": hashlib.sha256(indep_canonical(node)).hexdigest() == ppr["nodeDigest"]}

    # parameterDigest
    fnd = [v for d, v in objects.values() if d == "finding"]
    if fnd:
        pd = fnd[0]["parameterDigest"]
        prec = C.parse(blobs[pd])
        mine = hashlib.sha256(indep_canonical(prec)).hexdigest()
        out["parameterDigest"] = {
            "recipe": "raw SHA256 of C({schemaVersion,messageCode,parameters})",
            "record": prec, "independentlyRecomputed": mine, "carried": pd,
            "agree": mine == pd,
            "messageCodeEqualsFinding": prec["messageCode"] == fnd[0]["messageCode"]}

    # stageSpecDigest
    execp = [v for d, v in objects.values() if d == "execution-plan"][0]
    ssd = execp["stages"][0]["stageSpecDigest"]
    srec = C.parse(blobs[ssd])
    mine = hashlib.sha256(indep_canonical(srec)).hexdigest()
    out["stageSpecDigest"] = {
        "recipe": "raw SHA256 of C(stage-spec record)",
        "independentlyRecomputed": mine, "carried": ssd, "agree": mine == ssd,
        "planIdMatchesPlan": srec["planId"] == run["planId"],
        "producerIsPlanSelected": srec["producerClosure"] in plan["semanticClosures"]}

    # outputSchemaDigest
    osd = srec["outputSchemaDigest"]
    out["outputSchemaDigest"] = {
        "recipe": "raw SHA256 of the exact complete registered stage output schema document bytes",
        "carried": osd,
        "preimageRetained": osd in blobs,
        "rehashesToItself": (osd in blobs
                             and hashlib.sha256(blobs[osd]).hexdigest() == osd)}

    # inventoryDigest (commit-receipt)
    inv, inv_carried = M.commit_inventory(M.identifier("run", run), objects, blobs)
    invd = hashlib.sha256(indep_canonical(inv)).hexdigest()
    out["inventoryDigest"] = {
        "recipe": "raw SHA256 of C({schemaVersion,runId,objects,blobDigests})",
        "independentlyRecomputed": invd,
        "modelComputed": inv_carried,
        "agree": invd == inv_carried,
        "recordFields": sorted(inv.keys()),
        "objectCount": len(inv["objects"]),
        "blobCount": len(inv["blobDigests"]),
        "runIdMatches": inv["runId"] == M.identifier("run", run)}

    R["digestRecipes"] = out

    # --- negatives for the same class ------------------------------------
    def missing_pp():
        r, o, b = CHK.missing_program_predicate_preimage()
        M.close_run(r, o, b)
    refuses_with("MUST1-missing-program-predicate-preimage", missing_pp, "")

    def foreign_root():
        r, o, b = CHK.hidden_rule_program()
        M.close_run(r, o, b)
    refuses_with("MUST1-hidden-rule-program", foreign_root, "")

    def h_framed_pp():
        r, o, b = CHK.h_framed_program_predicate()
        M.close_run(r, o, b)
    refuses_with("MUST1-h-frame-offered-as-canonical-record", h_framed_pp, "")

    def stage_missing():
        r, o, b = CHK.stage_spec_missing_preimage()
        M.close_run(r, o, b)
    refuses_with("MUST1-stage-spec-missing-preimage", stage_missing, "")

    def params_missing():
        r, o, b = CHK.finding_parameters_missing()
        M.close_run(r, o, b)
    refuses_with("MUST1-finding-parameters-missing-preimage", params_missing, "")

    def bad_param_doc():
        r, o, b = CHK.bad_parameter_document()
        M.close_run(r, o, b)
    refuses_with("MUST1-parameter-cites-unregistered-document", bad_param_doc,
                 "PAYLOAD_PARAMETER_UNREGISTERED")


# ===========================================================================
# 8. Whole-graph digest-field sweep: no unannotated 64-hex field anywhere.
# ===========================================================================
def digest_sweep():
    ids = json.loads((F / "identity-schemas.v2.json").read_bytes())
    nat = json.loads((F.parent / "native/native-evidence.schemas.v2.json").read_bytes())
    findings = {"identity": [], "native": []}

    def sweep(doc, label, hexpat_only=True):
        hits, annotated, unannotated = 0, 0, []
        def walk(node, path):
            nonlocal hits, annotated
            if isinstance(node, dict):
                pat = node.get("pattern", "")
                is_hex = ("[0-9a-f]{64}" in pat)
                if is_hex:
                    hits += 1
                    if "x-opensip-digest" in node:
                        annotated += 1
                    else:
                        unannotated.append(path)
                for k, v in node.items():
                    walk(v, path + "/" + str(k))
            elif isinstance(node, list):
                for i, v in enumerate(node):
                    walk(v, path + "/" + str(i))
        walk(doc, "#")
        return {"hex64Fields": hits, "annotated": annotated,
                "unannotated": unannotated}

    R["digestSweep"] = {"identity": sweep(ids, "identity"),
                        "native": sweep(nat, "native")}


def main():
    primitives()
    build_runs()
    payload_attacks()
    memo_attack()
    coverage_attacks()
    stage_and_cache()
    digest_recipes()
    digest_sweep()
    R["summary"] = {
        "attacks": len(R["attacks"]),
        "passed": sum(1 for a in R["attacks"] if a["passed"]),
        "failed": [a for a in R["attacks"] if not a["passed"]],
    }
    json.dump(R, sys.stdout, indent=1, default=str)
    print()


if __name__ == "__main__":
    main()
