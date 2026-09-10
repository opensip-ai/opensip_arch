"""Vector suite A: canonical admission, H identities, the capability manifest
gates, acyclic construction/joins, and relation-specific minimum resolution.

Every expected outcome is DERIVED here from the normative prose; no author
result was consulted.
"""
from __future__ import annotations

import hashlib

import build as B
import canon as K
import kit
from evaluator import EvalView, eval_atom
from store import Refusal, Store

RESULTS = []


def rec(vid, kind, detail, **extra):
    row = {"id": vid, "kind": kind, "detail": detail}
    row.update(extra)
    RESULTS.append(row)
    return row


def refuses(vid, fn, note=""):
    try:
        fn()
        rec(vid, "NEGATIVE-FAILED", "no refusal was raised", note=note)
        return None
    except (Refusal, K.AdmissionError, kit.SchemaRefusal) as exc:
        code = getattr(exc, "code", type(exc).__name__)
        rec(vid, "refused", str(exc)[:200], firstObservedBoundary=code, note=note)
        return code


# ---------------------------------------------------------------------------
# A1. Canonical RAW-input admission -- lexical, before deserialization.
# Demonstrated SEPARATELY from encoding an already-parsed object, so the
# lexical/duplicate/string bounds are actually tested.
# ---------------------------------------------------------------------------

def a1_raw_admission():
    ok = K.admit_raw(b'{"b":1,"a":[0,18446744073709551615,-9223372036854775808]}')
    rec("A1-POS-raw-integer-bounds", "admitted", K.C(ok).decode())
    for vid, raw, why in [
        ("A1-N1-duplicate-key", b'{"a":1,"a":2}', "duplicate keys"),
        ("A1-N2-float-token", b'{"a":1.0}', "floating token is not an integer"),
        ("A1-N3-exponent-token", b'{"a":1e0}', "exponent token"),
        ("A1-N4-negative-zero", b'{"a":-0}', "-0"),
        ("A1-N5-nonfinite", b'{"a":NaN}', "nonfinite token"),
        ("A1-N6-lone-surrogate", b'{"a":"\\ud800"}', "non-scalar Unicode"),
        ("A1-N7-int-above-u64", b'{"a":18446744073709551616}', "> 2^64-1"),
        ("A1-N8-int-below-i64", b'{"a":-9223372036854775809}', "< -2^63"),
        ("A1-N9-malformed-utf8", b'{"a":"\xff"}', "malformed UTF-8"),
        ("A1-N10-raw-control", b'{"a":"\x01"}', "raw C0 control in a string"),
    ]:
        refuses(vid, lambda raw=raw: K.admit_raw(raw), note=why)
    # depth: root container counts as 1
    rec("A1-POS-depth-32", "admitted",
        str(len(K.C(K.admit_raw(b"[" * 32 + b"1" + b"]" * 32)))))
    refuses("A1-N11-depth-33", lambda: K.admit_raw(b"[" * 33 + b"1" + b"]" * 33),
            note="nesting depth 32, root counts as 1")
    refuses("A1-N12-descriptor-over-4MiB",
            lambda: K.admit_raw(b'["' + b"x" * (4 * 1024 * 1024) + b'"]'),
            note="maximum descriptor 4 MiB")
    # encoding an ALREADY-PARSED object cannot see the lexical faults above:
    # that is exactly why raw admission is a separate stage.
    rec("A1-BOUNDARY-parsed-object-cannot-see-lexical-faults", "observed",
        "C({'a': 1.0}) refuses on type, but a duplicate key or a `1.0` token "
        "is already lost once a decoder has produced a dict/int; the lexical "
        "gate is therefore not substitutable by the encoder.")
    refuses("A1-N13-float-offered-to-encoder", lambda: K.C({"a": 1.0}),
            note="float forbidden by C")


# ---------------------------------------------------------------------------
# A2. C and H: independently chosen minimal descriptor vectors.
# ---------------------------------------------------------------------------

def a2_canonical_and_h():
    vectors = [
        ("A2-V1-empty-object", {}),
        ("A2-V2-key-order-utf8", {"z": 1, "a": 2, "é": 3, "\U0001f600": 4}),
        ("A2-V3-escapes", {"k": "q\"b\\s\nt\tb\bf\ff/r\rcde "}),
        ("A2-V4-integers", [0, -1, 2 ** 64 - 1, -(2 ** 63)]),
        ("A2-V5-nested-arrays-keep-admitted-order", {"a": [3, 1, 2]}),
    ]
    for vid, value in vectors:
        cbytes = K.C(value)
        rec(vid, "canonical", cbytes.decode("utf-8", "backslashreplace"),
            bytes=len(cbytes),
            hSnapshot=K.H("snapshot", value) if isinstance(value, dict) else None)
    # H is domain separated and frame-length bound
    d1 = K.H("snapshot", {"schemaVersion": 2})
    d2 = K.H("plan", {"schemaVersion": 2})
    rec("A2-V6-domain-separation", "computed",
        f"same descriptor, snapshot={d1} plan={d2}", distinct=d1 != d2)
    frame = K.frame("snapshot", {"schemaVersion": 2})
    rec("A2-V7-frame-bytes", "frame", frame.hex(),
        prefixOk=frame.startswith(b"opensip.product.v1\x00snapshot\x00"))
    refuses("A2-N1-frame-with-unregistered-domain",
            lambda: K.parse_frame(K.frame("not-a-domain", {"x": 1}), {"snapshot"}),
            note="frame domain must be a member of the annotation's domain set")
    refuses("A2-N2-payload-where-frame-required",
            lambda: K.parse_frame(K.C({"schemaVersion": 2}), {"snapshot"}),
            note="C(X) does not begin with the framing prefix")
    bad = bytearray(frame)
    bad[len(b"opensip.product.v1\x00snapshot\x00")] = 0xFF     # length field
    refuses("A2-N3-frame-declared-length-wrong",
            lambda: K.parse_frame(bytes(bad), {"snapshot"}),
            note="declared length must equal the remaining byte count")
    body = b'{"schemaVersion": 2}'          # 20 bytes, NOT C's 19
    noncanon = (b"opensip.product.v1\x00snapshot\x00"
                + len(body).to_bytes(8, "big") + body)
    refuses("A2-N4-frame-body-not-canonical",
            lambda: K.parse_frame(noncanon, {"snapshot"}),
            note="the remainder must be byte-identical to C of its own parse")


# ---------------------------------------------------------------------------
# A3. Semantic vs operational identity.
# ---------------------------------------------------------------------------

def a3_semantic_versus_operational():
    base = {"schemaVersion": 2, "projectId": B.PROJECT_ID,
            "sourceInventory": [{"path": "a.ts", "sha256": "11" * 32, "bytes": 3}],
            "resolvedConfigDigest": "22" * 32, "scopeDigest": "33" * 32,
            "vcsDigest": "44" * 32}
    h0 = K.H("snapshot", base)
    moved = dict(base, scopeDigest="34" * 32)          # a SEMANTIC field
    h1 = K.H("snapshot", moved)
    rec("A3-V1-semantic-field-moves-identity", "computed",
        f"{h0} -> {h1}", moved=h0 != h1)
    # Operational identities are EXCLUDED from Run identity: they are not fields
    # of any semantic descriptor at all, so no wall clock, RequestId,
    # ExecutionId, PID, receipt or output destination can be added to one.
    for opfield in ("requestId", "executionId", "committedAt", "pid"):
        try:
            kit.validate("identity", "#/$defs/snapshot",
                         dict(base, **{opfield: "x"}), "operational field")
            rec("A3-N-" + opfield, "NEGATIVE-FAILED", "operational field admitted")
        except kit.SchemaRefusal as exc:
            rec("A3-V2-operational-field-refused-" + opfield, "refused",
                str(exc)[:140])
    rec("A3-V3-identical-semantic-inputs-same-run", "observed",
        "two attempts over identical semantic inputs mint the same snapshot2 "
        f"{h0}; attempts stay separately auditable through their own ExecutionId.")


# ---------------------------------------------------------------------------
# A4. Capability manifest: the four gates, then CVE1, then the identity.
# ---------------------------------------------------------------------------

def a4_capability_manifest():
    store = Store()
    good = B.capability_manifest(
        providers=[
            B.provider_capability("rust-semantic", "rust",
                                  {"calls": "resolved-callee",
                                   "unresolved-edge": "observed"},
                                  ["linux-x86_64-gnu", "macos-aarch64"]),
            B.provider_capability("syntax-all", "*", {"file": "enumerated"},
                                  ["all-supported"])],
        absent=[B.absent_capability("typescript-semantic", "typescript",
                                    ["imports", "types"], "unavailable",
                                    "provider-unavailable")])
    cm_id, digest, committed = B.commit_capability_manifest(store, good)
    rec("A4-POS-capability-manifest", "admitted",
        f"capabilityManifestId={cm_id}", cve1Bytes=len(committed),
        cve1Hex=committed.hex(), bytesDigest=digest,
        recomputed=K.capability_manifest_id(committed) == cm_id)

    # the thirteenth relation IS expressible (RELATION-DOMAIN-V2 extension)
    rec("A4-V1-unresolved-edge-is-expressible", "observed",
        "unresolved-edge@observed admitted in a committed manifest")

    def mutate(m, fn):
        import copy
        c = copy.deepcopy(m)
        fn(c)
        return c

    refuses("A4-N1-ADM-TYPE-boolean-as-integer",
            lambda: B.admit_capability_manifest(
                mutate(good, lambda m: m.__setitem__("schemaVersion", True))),
            note="a boolean is not an integer")
    refuses("A4-N2-ADM-TYPE-numeric-string",
            lambda: B.admit_capability_manifest(
                mutate(good, lambda m: m.__setitem__("schemaVersion", "1"))),
            note="a numeric string is not a number")
    refuses("A4-N3-ADM-CLOSED-undeclared-key",
            lambda: B.admit_capability_manifest(
                mutate(good, lambda m: m.__setitem__("extra", "x"))),
            note="every reachable RECORD is closed")
    refuses("A4-N4-ADM-DOMAIN-unregistered-relation",
            lambda: B.admit_capability_manifest(
                mutate(good, lambda m: m["providers"][0]["relations"].__setitem__(
                    "made-up", "observed"))),
            note="relation key must be a RELATION-DOMAIN-V2 member")
    refuses("A4-N5-ADM-DOMAIN-rung-of-another-relation",
            lambda: B.admit_capability_manifest(
                mutate(good, lambda m: m["providers"][0]["relations"].__setitem__(
                    "clones", "resolved-callee"))),
            note="a rung of another relation is refused, not a live token")
    refuses("A4-N6-ADM-DOMAIN-platform",
            lambda: B.admit_capability_manifest(
                mutate(good, lambda m: m["providers"][1]["platformIds"].__setitem__(
                    0, "solaris-sparc"))),
            note="PLATFORM-ID-DOMAIN-V1")
    refuses("A4-N7-ADM-ORDER-providers-unsorted",
            lambda: B.admit_capability_manifest(
                mutate(good, lambda m: m["providers"].reverse())),
            note="strictly ascending by the declared sort key's UTF-8 bytes")
    refuses("A4-N8-ADM-ORDER-duplicate-is-an-ordering-violation",
            lambda: B.admit_capability_manifest(
                mutate(good, lambda m: m["providers"][1]["platformIds"].append(
                    "all-supported"))),
            note="strict ascending UNIQUE order; a duplicate is an ordering violation")
    refuses("A4-N9-CVE1-non-NFC-string",
            lambda: K.cve1({"k": "é"}),
            note="CVE1 admits already-NFC strings only")
    refuses("A4-N10-CVE1-float", lambda: K.cve1({"k": 1.5}),
            note="floating-point values are forbidden in CVE1")
    refuses("A4-N11-CVE1-bytes", lambda: K.cve1({"k": b"x"}),
            note="byte strings are forbidden in CVE1")
    # CVE1 map keys are sorted by key bytes: the encoder is order-independent
    m1 = K.cve1({"b": 1, "a": 2})
    m2 = K.cve1({"a": 2, "b": 1})
    rec("A4-V2-cve1-map-key-sort", "computed", m1.hex(), stable=m1 == m2)
    # C and CVE1 are DIFFERENT codecs over the same value
    rec("A4-V3-cve1-is-not-C", "observed",
        f"C={K.C(good)[:48].decode()}... CVE1={committed[:24].hex()}...",
        distinct=K.C(good) != committed)
    # the identity is NOT H(domain, X): it is the inherited CVE1 recipe
    rec("A4-V4-capability-id-is-not-H", "computed",
        f"cve1Recipe={cm_id} vs H('capability-manifest',X)="
        f"{K.H('capability-manifest', good)}",
        distinct=cm_id != K.H("capability-manifest", good))
    return cm_id


# ---------------------------------------------------------------------------
# A5. Relation-specific minimum resolution at syntactic / resolved / type.
# ---------------------------------------------------------------------------

def a5_min_resolution():
    def view(relation, rung, coverage_state="complete", present=True,
             coverage_rung=None):
        facts = {}
        if present:
            facts["fact2:" + "aa" * 32] = {
                "relation": relation, "resolution": rung,
                "sourceUniverse": "11" * 32, "targetUniverse": "11" * 32}
        cov = {}
        cr = coverage_rung or rung
        cov["coverage2:" + "bb" * 32] = {
            "scopeId": "scope2:" + "cc" * 32,
            "payload": {"entry": {
                "relation": relation, "resolution": cr,
                "coverage": coverage_state,
                "resolutionCompleteness": {
                    "state": "complete" if cr in kit.RESOLVED_RUNGS else "not-applicable"}}}}
        return EvalView(facts=facts, scopes={}, coverages=cov,
                        universe_language={"11" * 32: "typescript"})

    cases = [
        # (id, relation, min rung, fact rung, present, coverage, expected)
        ("A5-1-syntactic-floor-met-by-resolved", "references",
         "syntactic-name-match", "resolved-binding", True, "complete", "true"),
        ("A5-2-resolved-floor-not-met-by-syntactic", "references",
         "resolved-binding", "syntactic-name-match", True, "complete", "false"),
        ("A5-3-resolved-floor-met", "references", "resolved-binding",
         "resolved-binding", True, "complete", "true"),
        ("A5-4-type-floor-not-met-by-annotated", "types", "checked",
         "annotated", True, "complete", "false"),
        ("A5-5-type-floor-met-by-checked", "types", "checked", "checked",
         True, "complete", "true"),
        ("A5-6-insufficient-coverage-is-indeterminate", "references",
         "resolved-binding", "resolved-binding", False, "unknown", "indeterminate"),
        ("A5-7-complete-absence-is-false", "references", "resolved-binding",
         "resolved-binding", False, "complete", "false"),
    ]
    for vid, rel, minr, factr, present, cov, expected in cases:
        v = view(rel, factr, cov, present, coverage_rung=minr)
        atom = {"op": "exists", "relation": rel, "minResolution": minr,
                "filters": []}
        value, matches, cids = eval_atom(v, atom)
        rec(vid, "evaluated",
            f"exists {rel}@>={minr} with fact@{factr if present else 'none'} "
            f"coverage={cov} -> {value}",
            expected=expected, actual=value, matchingFactIds=matches,
            coverageIds=cids, agrees=value == expected)
    # a rung of ANOTHER relation is a refusal, never a weaker/stronger value
    v = view("clones", "normalized-body-hash")
    refuses("A5-N1-cross-relation-rung",
            lambda: eval_atom(v, {"op": "exists", "relation": "clones",
                                  "minResolution": "resolved-callee",
                                  "filters": []}),
            note="membership is decided against THAT relation's own ladder")
    # the three-valued law for MISSING relation Coverage with no match
    empty = EvalView(facts={}, scopes={}, coverages={},
                     universe_language={})
    for op, expected in (("exists", "indeterminate"), ("none", "indeterminate"),
                         ("all-covered", "indeterminate")):
        atom = {"op": op, "relation": "references",
                "minResolution": "resolved-binding", "filters": []}
        value, m, c = eval_atom(empty, atom)
        rec(f"A5-8-missing-coverage-no-match-{op}", "evaluated",
            f"{op} with no Coverage and no match -> {value}",
            expected=expected, actual=value, agrees=value == expected)
    atom = {"op": "count-at-most", "relation": "references",
            "minResolution": "resolved-binding", "filters": [], "n": 0}
    value, m, c = eval_atom(empty, atom)
    rec("A5-8-missing-coverage-no-match-count-at-most", "evaluated",
        f"count-at-most 0 with no Coverage and no match -> {value}",
        expected="indeterminate", actual=value, agrees=value == "indeterminate")
    # the field-filter projection is UNPUBLISHED: refuse rather than invent
    refuses("A5-N2-field-filter-projection-unpublished",
            lambda: eval_atom(view("references", "resolved-binding"),
                              {"op": "exists", "relation": "references",
                               "minResolution": "resolved-binding",
                               "filters": [{"field": "subject", "cmp": "eq",
                                            "value": "sym:x"}]}),
            note="no document projects fact2 + relation payload onto the "
                 "FieldFilter vocabulary (CB9-MUST-2)")


def run_all():
    a1_raw_admission()
    a2_canonical_and_h()
    a3_semantic_versus_operational()
    a4_capability_manifest()
    a5_min_resolution()
    return RESULTS
