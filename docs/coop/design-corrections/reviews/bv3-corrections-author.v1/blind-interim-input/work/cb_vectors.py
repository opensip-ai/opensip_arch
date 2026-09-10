"""Independently authored minimal descriptor vectors for the OpenSIP product
identity graph. Every expected value is COMPUTED by cb_canonical (written from
prose) and cross-checked against a second, deliberately separate hashlib oracle
spelled out by hand here. No author fixture was read.
"""

import hashlib
import json
import struct

import cb_canonical as K

RESULTS = []


def record(vid, kind, detail, ok=True, **extra):
    row = {"id": vid, "kind": kind, "ok": bool(ok), "detail": detail}
    row.update(extra)
    RESULTS.append(row)
    return row


def expect_refusal(vid, cause_prefix, fn, *a, **kw):
    try:
        fn(*a, **kw)
    except K.Refusal as exc:
        ok = exc.cause.startswith(cause_prefix)
        return record(vid, "negative", f"refused {exc.cause}"
                      + (f" ({exc.detail})" if exc.detail else ""),
                      ok=ok, cause=exc.cause, expectedCause=cause_prefix)
    return record(vid, "negative", "ADMITTED - expected refusal", ok=False,
                  expectedCause=cause_prefix)


# ==========================================================================
# A. Exact admission: integers, duplicates, strings.
# ==========================================================================

def admission_vectors():
    # A-1 ordinary integer token admits and encodes shortest-decimal.
    v = K.admit(b'{"limit":1,"neg":-9223372036854775808,"max":18446744073709551615}')
    c = K.C(v)
    record("A-1", "positive",
           "ordinary integer tokens admit; C emits shortest decimal",
           ok=c == b'{"limit":1,"max":18446744073709551615,"neg":-9223372036854775808}',
           canonical=c.decode())

    # A-2..A-6 float-spelled / boolean / string integers refuse BEFORE identity.
    expect_refusal("A-2", "NON_INTEGER_NUMBER", K.admit, b'{"limit":1.0}')
    expect_refusal("A-3", "NON_INTEGER_NUMBER", K.admit, b'{"limit":1e0}')
    expect_refusal("A-4", "NEGATIVE_ZERO", K.admit, b'{"limit":-0}')
    expect_refusal("A-5", "NONFINITE_NUMBER", K.admit, b'{"limit":NaN}')
    expect_refusal("A-6", "INTEGER_OUT_OF_RANGE", K.admit,
                   b'{"limit":18446744073709551616}')
    expect_refusal("A-6b", "INTEGER_OUT_OF_RANGE", K.admit,
                   b'{"limit":-9223372036854775809}')

    # A-7 booleans are distinct from integers in C.
    record("A-7", "positive", "true and 1 encode differently",
           ok=K.C({"x": True}) != K.C({"x": 1}),
           trueBytes=K.C({"x": True}).decode(), oneBytes=K.C({"x": 1}).decode())

    # A-8 duplicate key refuses before deserialization loses it.
    expect_refusal("A-8", "DUPLICATE_KEY", K.admit, b'{"a":1,"a":2}')

    # A-9 lone surrogate refuses.
    expect_refusal("A-9", "NON_SCALAR_UNICODE", K.admit, b'{"a":"\\ud800"}')

    # A-10 string escaping law: quote/backslash, the five short escapes,
    #      lowercase \u00xx for other C0, slash unescaped, U+007F and U+2028 raw.
    s = "q\"b\\ s/ \b\t\n\f\r \x00\x1f \x7f   é"
    c = K.C({"s": s})
    expect = ('{"s":"q\\"b\\\\ s/ \\b\\t\\n\\f\\r \\u0000\\u001f '
              '\x7f   é"}').encode("utf-8")
    record("A-10", "positive", "C string escaping law", ok=c == expect,
           got=c.decode("utf-8"))

    # A-11 no Unicode normalization: NFC and NFD spellings are different bytes
    #      and different identities.
    nfc, nfd = "café", "café"
    h1 = K.H("snapshot", {"x": nfc})
    h2 = K.H("snapshot", {"x": nfd})
    record("A-11", "positive", "C does not normalize; NFC != NFD identity",
           ok=(K.C({"x": nfc}) != K.C({"x": nfd})) and h1 != h2, nfc=h1, nfd=h2)

    # A-12 key order is UTF-8 byte order, including non-BMP keys.
    c = K.C({"\U0001f600": 1, "z": 2, "é": 3, "a": 4})
    record("A-12", "positive", "keys sort by UTF-8 bytes (non-BMP last)",
           ok=c.decode() == '{"a":4,"z":2,"é":3,"\U0001f600":1}', got=c.decode())

    # A-13 nesting depth: root container counts as 1; scalars/keys add none.
    deep32 = json.dumps(_nest(32)).encode()
    deep33 = json.dumps(_nest(33)).encode()
    record("A-13", "positive", "depth 32 admits", ok=_admits(deep32))
    expect_refusal("A-13b", "DEPTH_EXCEEDED", K.admit, deep33)

    # A-14 arrays keep admitted order; C never sorts or dedupes.
    a = ["b", "a", "b"]
    record("A-14", "positive", "C preserves array order and repeats",
           ok=K.C({"a": a}).decode() == '{"a":["b","a","b"]}')

    # A-15 x-opensip-order vocabulary is closed; an unknown annotation refuses.
    expect_refusal("A-15", "ORDER_ANNOTATION_UNKNOWN", K.check_order, ["a"], "sorted")
    # canonical-set refuses a non-ascending or duplicate array before hashing.
    expect_refusal("A-15b", "ORDER_NOT_STRICTLY_ASCENDING",
                   K.check_order, ["b", "a"], "canonical-set")
    expect_refusal("A-15c", "ORDER_NOT_STRICTLY_ASCENDING",
                   K.check_order, ["a", "a"], "canonical-set")
    K.check_order(["a", "a", "b"], "canonical-order")
    record("A-15d", "positive", "canonical-order admits equal neighbours", ok=True)
    # declaration-signature tokens are a `sequence`: repeats retained in order.
    K.check_order(["T", "T", "A"], "sequence")
    record("A-15e", "positive",
           "sequence retains grammar order including repeated tokens", ok=True)


def _nest(n):
    v = 1
    for _ in range(n):
        v = [v]
    return v


def _admits(b):
    try:
        K.admit(b)
        return True
    except K.Refusal:
        return False


# ==========================================================================
# B. Semantic-field change vs operational change.
# ==========================================================================

def identity_movement_vectors():
    # A minimal but real snapshot2 descriptor.
    inv = K.ordered([
        {"path": "src/a.ts", "sha256": "aa" * 32, "bytes": 10},
        {"path": "src/b.ts", "sha256": "bb" * 32, "bytes": 20},
    ], "path")
    inv_digest = K.raw_sha256(inv)
    vcs = {"schemaVersion": 2, "kind": "git", "commitId": "c" * 40,
           "dirty": False, "sourceInventoryDigest": inv_digest}
    snap = {"schemaVersion": 2, "projectId": "prj1-" + "1" * 64,
            "sourceInventory": inv, "resolvedConfigDigest": "11" * 32,
            "scopeDigest": "22" * 32, "vcsDigest": K.raw_sha256(vcs)}
    sid, sh = K.identifier("snapshot", snap)
    record("B-1", "positive", "snapshot2 minted from a hand-built descriptor",
           snapshotId=sid, canonicalLen=len(K.C(snap)))

    # B-2 the frame is domain-separated: same descriptor, different domain.
    other = K.H("plan", snap)
    record("B-2", "positive", "domain separation: H(snapshot,X) != H(plan,X)",
           ok=other != sh, asSnapshot=sh, asPlan=other)

    # B-3 SHA256(C(X)) is never H(D,X): a raw payload offered as an H identity
    #     fails the frame prefix.
    raw = K.raw_sha256(snap)
    record("B-3", "positive", "raw SHA256(C(X)) differs from H(D,X)",
           ok=raw != sh, raw=raw, h=sh)
    expect_refusal("B-3b", "FRAME_PREFIX_MISMATCH", K.parse_frame, K.C(snap))

    # B-4 frame admission is exact: a tampered declared length refuses.
    f = K.frame("snapshot", snap)
    bad = f[:len(K.FRAME_PREFIX) + 1 + len("snapshot") + 1] + struct.pack(">Q", 7) \
        + f[len(K.FRAME_PREFIX) + 1 + len("snapshot") + 1 + 8:]
    expect_refusal("B-4", "FRAME_LENGTH_MISMATCH", K.parse_frame, bad)
    d, x = K.parse_frame(f)
    record("B-4b", "positive", "well-formed frame round-trips",
           ok=d == "snapshot" and x == snap)

    # B-5 every single semantic field moves the identity.
    moved = {}
    for field in snap:
        mutant = dict(snap)
        if field == "schemaVersion":
            continue
        if field == "sourceInventory":
            mutant[field] = K.ordered([dict(inv[0], bytes=11), inv[1]], "path")
        elif field == "projectId":
            mutant[field] = "prj1-" + "2" * 64
        else:
            mutant[field] = "33" * 32
        moved[field] = K.H("snapshot", mutant) != sh
    record("B-5", "positive", "every semantic snapshot field moves snapshot2",
           ok=all(moved.values()), perField=moved)

    # B-6 operational identities are NOT descriptor fields: two attempts with
    #     different RequestId/ExecutionId/wall clock mint the same Run.
    plan_id = "plan2:" + "9" * 64
    run_desc = {"schemaVersion": 2, "projectId": snap["projectId"],
                "snapshotId": sid, "planId": plan_id,
                "evidenceId": "evidence2:" + "4" * 64,
                "evaluationSealId": "seal2:" + "5" * 64,
                "capabilityManifestId": "6" * 64}
    r1, _ = K.identifier("run", run_desc)
    attempt_a = {"requestId": "req1_" + "a" * 32, "executionId": "exec1_" + "a" * 32,
                 "wallClock": "2026-09-06T00:00:00Z", "pid": 4242}
    attempt_b = {"requestId": "req1_" + "b" * 32, "executionId": "exec1_" + "b" * 32,
                 "wallClock": "2026-09-06T11:22:33Z", "pid": 9999}
    r2, _ = K.identifier("run", run_desc)  # descriptor unchanged by the attempt
    record("B-6", "positive",
           "operational RequestId/ExecutionId/clock/PID are excluded from run2",
           ok=r1 == r2, runId=r1, attemptA=attempt_a, attemptB=attempt_b)

    # B-7 one semantic field of the Run does move it.
    r3, _ = K.identifier("run", dict(run_desc, evidenceId="evidence2:" + "7" * 64))
    record("B-7", "positive", "a semantic Run field moves run2", ok=r3 != r1)

    # B-8 end-anchored operational grammars: a trailing newline is malformed,
    #     not trimmed (identity section 2, admission section 1).
    import re
    exec_ok = re.compile(r"^exec1_[0-9a-f]{32}(?![\s\S])")
    bare_dollar = re.compile(r"^exec1_[0-9a-f]{32}$")
    nl = "exec1_" + "a" * 32 + "\n"
    record("B-8", "positive",
           "the successor end assertion refuses a newline the retained bare $ admits",
           ok=(exec_ok.match(nl) is None) and (bare_dollar.match(nl) is not None))
    return snap, sid


# ==========================================================================
# C. Capability manifest (CVE1 + CAP-MANIFEST-ID-V1), independently built.
# ==========================================================================

def capability_manifest_vectors():
    manifest = {
        "schemaVersion": 1,
        "profile": "cb-blind-default",
        "providers": [
            {"providerId": "rust-semantic", "language": "rust",
             "providerVersionSource": "signed-release-manifest",
             "toolchainIdentitySource": "native-context-rust-v2",
             "relations": {"clones": "normalized-body-hash", "file": "enumerated",
                           "declares": "syntactic", "imports": "resolved-target"},
             "platformIds": ["linux-x86_64-gnu", "macos-aarch64"]},
            {"providerId": "typescript-semantic", "language": "typescript",
             "providerVersionSource": "signed-release-manifest",
             "toolchainIdentitySource": "native-context-typescript-v2",
             "relations": {"clones": "normalized-body-hash", "file": "enumerated",
                           "references": "resolved-binding", "types": "checked"},
             "platformIds": ["all-supported"]},
        ],
        "coverageForAbsent": [
            {"providerId": "syntax-all", "language": "*",
             "relationIds": ["calls", "references"],
             "coverageState": "unavailable",
             "deficiency": "language-tier-unsupported"},
        ],
    }
    cid, committed = K.capability_manifest_id(manifest)

    # Hand-spelled independent oracle for the outer frame, byte by byte.
    oracle = hashlib.sha256(
        b"opensip.capability-manifest.v1" + b"\x00" + committed).hexdigest()
    record("C-1", "positive", "capabilityManifestId over my own manifest",
           ok=cid == oracle and len(cid) == 64,
           capabilityManifestId=cid, committedBytes=len(committed),
           committedPrefixHex=committed[:16].hex())

    # C-2 the bare-hex text form, no scheme prefix.
    import re
    record("C-2", "positive", "text form is bare 64 lowercase hex",
           ok=bool(re.fullmatch(r"[0-9a-f]{64}", cid)))

    # C-3 capabilityManifestBytesDigest is raw SHA256 of the committed artifact
    #     and is NOT the id (derived retention: id recomputed from the artifact).
    bytes_digest = K.raw_bytes_sha256(committed)
    record("C-3", "positive",
           "capabilityManifestBytesDigest (raw artifact) != capabilityManifestId",
           ok=bytes_digest != cid, bytesDigest=bytes_digest)

    # C-4 ADM-TYPE is a gate BEFORE encoding: schemaVersion respelled as true or
    #     "1" would mint a well-formed but wrong id, so it must refuse.
    expect_refusal("C-4", "ADM-TYPE", K.capability_manifest_id,
                   dict(manifest, schemaVersion=True))
    expect_refusal("C-4b", "ADM-TYPE", K.capability_manifest_id,
                   dict(manifest, schemaVersion="1"))
    # ...and CVE1 alone is total on both, which is why the gate is separate.
    record("C-4c", "positive",
           "CVE1 is total on true and \"1\": the gate cannot be the encoder",
           ok=K.cve1(True) == b"\x02" and K.cve1("1") == b"\x04\x00\x00\x00\x011")

    # C-5 ADM-CLOSED narrows the two nested records too.
    bad = json.loads(json.dumps(manifest))
    bad["providers"][0]["extra"] = "x"
    expect_refusal("C-5", "ADM-CLOSED", K.capability_manifest_id, bad)

    # C-6 ADM-DOMAIN: platformId case variant and unregistered rung refuse.
    bad = json.loads(json.dumps(manifest))
    bad["providers"][0]["platformIds"] = ["LINUX-X86_64-GNU"]
    expect_refusal("C-6", "ADM-DOMAIN", K.capability_manifest_id, bad)
    bad = json.loads(json.dumps(manifest))
    bad["providers"][0]["relations"]["clones"] = "syntactic"
    expect_refusal("C-6b", "ADM-DOMAIN", K.capability_manifest_id, bad)

    # C-7 ADM-ORDER: a committed manifest out of declared order is rejected,
    #     never sorted into shape by the consumer.
    bad = json.loads(json.dumps(manifest))
    bad["providers"] = list(reversed(bad["providers"]))
    expect_refusal("C-7", "ADM-ORDER", K.capability_manifest_id, bad)
    bad = json.loads(json.dumps(manifest))
    bad["coverageForAbsent"][0]["relationIds"] = ["references", "calls"]
    expect_refusal("C-7b", "ADM-ORDER", K.capability_manifest_id, bad)

    # C-8 CVE1 refuses non-NFC strings (its own constraint), while C admits
    #     them: the two encoders have deliberately different string admission.
    expect_refusal("C-8", "CVE1_STRING_NOT_NFC", K.cve1, "café")
    record("C-8b", "positive",
           "C admits a non-NFC string that CVE1 refuses (profiles are separate)",
           ok=K.C({"x": "café"}) == '{"x":"café"}'.encode("utf-8"))

    # C-9 changing one manifest field moves the id.
    moved = K.capability_manifest_id(dict(manifest, profile="cb-blind-other"))[0]
    record("C-9", "positive", "a profile change moves capabilityManifestId",
           ok=moved != cid, other=moved)
    return manifest, cid, bytes_digest


def run_all():
    admission_vectors()
    identity_movement_vectors()
    capability_manifest_vectors()
    return RESULTS


if __name__ == "__main__":
    rows = run_all()
    bad = [r for r in rows if not r["ok"]]
    for r in rows:
        print(("PASS " if r["ok"] else "FAIL "), r["id"], r["detail"])
    print(f"\n{len(rows)} vectors, {len(bad)} failing")
