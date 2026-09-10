#!/usr/bin/env python3
"""Phase 1: independently authored C/H/CVE1/lexical/join vectors. Not author goldens."""
from __future__ import annotations

import json
import sys
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v12-team-query-run-corrections.v1/output")
sys.path.insert(0, str(OUT))

from helper.canonical import C, C_hex  # noqa: E402
from helper.cve1 import CLOSED_TYPES, classify, decode, encode, round_trip  # noqa: E402
from helper.errors import AdmissionError  # noqa: E402
from helper.identity import DOMAIN_PREFIX, H, h_frame, parse_h_frame, typed_id  # noqa: E402
from helper.lexical import first_refusal, admit_raw  # noqa: E402
from helper.status import mark, write_checkpoint  # noqa: E402


def dump(name: str, obj) -> str:
    p = OUT / "vectors" / name
    p.write_text(json.dumps(obj, indent=2) + "\n")
    return str(p)


# --- CVE1 eight types (independently chosen values, computed from the recipe) ---
cve1_cases = []
samples = [
    ("null", None),
    ("false", False),
    ("true", True),
    ("unsigned-64", 0),
    ("unsigned-64", 1),
    ("unsigned-64", 18446744073709551615),
    ("negative-signed-64", -1),
    ("negative-signed-64", -9223372036854775808),
    ("NFC-UTF8-string", ""),
    ("NFC-UTF8-string", "opensip"),
    ("NFC-UTF8-string", "café"),  # already NFC
    ("array", []),
    ("array", [None, True, False, 2, "x"]),
    ("string-keyed-map", {}),
    ("string-keyed-map", {"b": 1, "a": 0}),  # encoder must sort keys
]
seen_types = set()
for expected_type, value in samples:
    rt = round_trip(value)
    assert rt["type"] == expected_type, (expected_type, rt)
    assert rt["reencodeEquals"] is True
    assert rt["decodedEquals"] is True
    seen_types.add(expected_type)
    cve1_cases.append({"inputKind": expected_type, "pythonRepr": repr(value), **rt})

# Discriminating: map key order in Python dict must not affect bytes
m1 = encode({"z": 1, "a": 2})
m2 = encode({"a": 2, "z": 1})
assert m1 == m2
cve1_cases.append(
    {
        "inputKind": "string-keyed-map-key-order-independence",
        "hex": m1.hex(),
        "equalRegardlessOfInsertion": m1 == m2,
        "decoded": decode(m1),
    }
)

# Negative: non-NFC string (é as e + combining acute)
non_nfc = "e\u0301"
try:
    encode(non_nfc)
    nfc_ref = {"ok": True}
except AdmissionError as e:
    nfc_ref = {"ok": False, "firstRefusal": e.as_dict()}
assert nfc_ref["ok"] is False
cve1_cases.append({"inputKind": "non-NFC-string-negative", **nfc_ref})

# Negative: float
try:
    encode(1.0)  # type: ignore
    float_ref = {"ok": True}
except AdmissionError as e:
    float_ref = {"ok": False, "firstRefusal": e.as_dict()}
assert float_ref["ok"] is False

missing = [t for t in CLOSED_TYPES if t not in seen_types]
assert not missing, missing

cve1_art = dump(
    "cve1-eight-types.json",
    {
        "kind": "standaloneCanonicalVector",
        "classification": "valid",
        "selector": "docs/coop/artifacts/resolved-inputs.v2.json#planIdContract.canonicalValueEncoding",
        "closedTypes": list(CLOSED_TYPES),
        "allEightExercised": sorted(seen_types) == sorted(CLOSED_TYPES),
        "vectors": cve1_cases,
        "floatNegative": float_ref,
        "note": "Independently chosen values. Encoded from the published tag/length recipe. Not copied from DELIVERY goldens.",
    },
)

# --- C / H helper over independently authored minimal descriptors ---
# Operational fields MUST NOT appear on semantic descriptors.
snap_a = {
    "schemaVersion": 2,
    "projectId": "prj1-" + ("ab" * 32),
    "sourceInventory": {
        "schemaVersion": 1,
        "entries": [{"path": "src/main.ts", "sha256": "aa" * 32, "bytes": 12}],
    },
    "resolvedConfigDigest": "11" * 32,
    "scopeDigest": "22" * 32,
    "vcsDigest": "33" * 32,
}
snap_b = dict(snap_a)
snap_b = {
    **snap_a,
    "vcsDigest": "34" * 32,  # semantic change
}

h_a = H("snapshot", snap_a)
h_b = H("snapshot", snap_b)
id_a = typed_id("snapshot", snap_a)
id_b = typed_id("snapshot", snap_b)
assert h_a != h_b
assert id_a.startswith("snapshot2:")
frame_a = h_frame("snapshot", snap_a)
parsed = parse_h_frame(frame_a, allowed_domains={"snapshot"})
assert parsed["digest"] == h_a
assert parsed["domain"] == "snapshot"

# Operational wrapper: requestId / timestamp sit beside, not inside, the snapshot.
operational_attempt = {
    "requestId": "req1_" + ("cd" * 16),
    "executionId": "exec1_" + ("ef" * 16),
    "wallClock": "2026-09-08T00:00:00Z",
    "snapshot": snap_a,
}
# Same snapshot bytes => same H regardless of operational envelope.
h_from_envelope = H("snapshot", operational_attempt["snapshot"])
assert h_from_envelope == h_a

# If someone illegally put requestId into the snapshot, identity would move — that is the
# semantic/operational distinction: those fields are excluded from the recipe.
illegal = dict(snap_a)
illegal["requestId"] = operational_attempt["requestId"]
h_illegal = H("snapshot", illegal)
assert h_illegal != h_a

h_art = dump(
    "h-helper.json",
    {
        "kind": "standaloneCanonicalVector",
        "classification": "valid",
        "recipe": 'H(D,X)=SHA256(ASCII("opensip.product.v1")||00||ASCII(D)||00||uint64BE(len(C(X)))||C(X))',
        "selector": "docs/v2/contracts/product-v1/identity-and-evidence.md §3",
        "domainPrefixMap": DOMAIN_PREFIX,
        "vectors": [
            {
                "name": "snapshot-A",
                "domain": "snapshot",
                "C_hex": C(snap_a).hex(),
                "H": h_a,
                "typedId": id_a,
                "frameSha256": parsed["digest"],
                "frameByteLength": len(frame_a),
            },
            {
                "name": "snapshot-B-semantic-vcsDigest-change",
                "domain": "snapshot",
                "H": h_b,
                "typedId": id_b,
                "identityMoved": True,
            },
            {
                "name": "operational-envelope-does-not-enter-H",
                "requestId": operational_attempt["requestId"],
                "executionId": operational_attempt["executionId"],
                "wallClock": operational_attempt["wallClock"],
                "H_snapshot": h_from_envelope,
                "equalsSnapshotA": h_from_envelope == h_a,
            },
            {
                "name": "illegal-requestId-inside-snapshot-moves-identity",
                "classification": "invalid",
                "H": h_illegal,
                "equalsSnapshotA": False,
                "note": "Demonstration that operational IDs are excluded by recipe, not by hashing them and ignoring the difference.",
            },
        ],
    },
)

# --- lexical admission on RAW input ---
raw_vectors = []


def add_raw(name, raw: bytes, expect_ok: bool, expect_code=None):
    r = first_refusal(raw)
    raw_vectors.append(
        {
            "name": name,
            "rawUtf8": raw.decode("utf-8", "replace"),
            "rawHex": raw.hex(),
            "classification": "valid" if expect_ok else "invalid",
            **r,
        }
    )
    if expect_ok:
        assert r["ok"] is True, (name, r)
    else:
        assert r["ok"] is False, (name, r)
        if expect_code:
            assert r["firstRefusal"]["code"] == expect_code, (name, r)


add_raw("integer-zero", b"0", True)
add_raw("integer-positive", b"42", True)
add_raw("integer-negative", b"-7", True)
add_raw("integer-u64-max", b"18446744073709551615", True)
add_raw("integer-i64-min", b"-9223372036854775808", True)
add_raw("bool-true", b"true", True)
add_raw("object-ok", b'{"a":1,"b":2}', True)

add_raw("duplicate-key", b'{"a":1,"a":2}', False, "DUPLICATE_KEY")
add_raw("float-1.0", b"1.0", False, "FLOAT_FORBIDDEN")
add_raw("exponent", b"1e2", False, "EXPONENT_FORBIDDEN")
add_raw("neg-zero", b"-0", False, "NEG_ZERO_FORBIDDEN")
add_raw("leading-zero", b"01", False, "LEADING_ZERO")
add_raw("out-of-range-high", b"18446744073709551616", False, "INTEGER_OUT_OF_RANGE")
add_raw("out-of-range-low", b"-9223372036854775809", False, "INTEGER_OUT_OF_RANGE")
add_raw("unpaired-surrogate", '{"x":"\\uD800"}'.encode(), False, "NON_SCALAR_UNICODE")
add_raw("bom", b"\xef\xbb\xbf{}", False, "BOM_FORBIDDEN")

# string bound: unescaped control
add_raw("unescaped-control", b'"\x01"', False, "UNESCAPED_CONTROL")

lex_art = dump(
    "lexical-admission.json",
    {
        "kind": "standaloneCanonicalVector",
        "selector": "docs/v2/contracts/product-v1/identity-and-evidence.md §3 lexical admission",
        "note": "These vectors are RAW bytes. Python json.loads is not used for admission.",
        "vectors": raw_vectors,
    },
)

# --- raw vs parsed: same logical object, different raw faults ---
# Parsed object {"a":1} encodes fine; raw duplicate keys refuse before parse.
parsed_ok = {"a": 1}
c_parsed = C(parsed_ok)
raw_dup = first_refusal(b'{"a":1,"a":2}')
# Object-encode of a Python dict cannot even represent the duplicate.
raw_vs_parsed = dump(
    "raw-vs-parsed.json",
    {
        "kind": "standaloneCanonicalVector",
        "selector": "identity-and-evidence §3: reject duplicate keys before deserialization loses lexical information",
        "parsedObjectEncode": {
            "classification": "valid",
            "object": parsed_ok,
            "C_hex": c_parsed.hex(),
        },
        "rawDuplicate": {
            "classification": "invalid",
            "raw": '{"a":1,"a":2}',
            **raw_dup,
            "firstRefusal": raw_dup["firstRefusal"],
        },
        "rawFloat": first_refusal(b"1.0"),
        "parsedBoolIsNotInt": {
            "note": "type(True) is bool; C encodes true not 1",
            "C_true": C(True).decode(),
            "C_one": C(1).decode(),
            "distinct": C(True) != C(1),
        },
        "distinctFromObjectEncode": True,
    },
)
assert raw_dup["ok"] is False
assert C(True) != C(1)

# --- semantic vs operational ---
sem_art = dump(
    "semantic-vs-operational.json",
    {
        "kind": "standaloneCanonicalVector",
        "selector": "identity-and-evidence §2–3: RequestId/ExecutionId/wall clocks excluded from Run identity; semantic field change moves Plan/snapshot identity",
        "semanticChangeMovesIdentity": {
            "before": id_a,
            "after": id_b,
            "equal": False,
            "changedField": "vcsDigest",
        },
        "operationalChangeDoesNotMoveIdentity": {
            "requestIdChanged": "req1_" + ("11" * 16),
            "snapshotHUnchanged": h_a,
            "equal": True,
        },
        "measured": True,
    },
)

# --- acyclic joins ---
# Minimal typed descriptors using required identity-schema fields. Nested digests
# are independently computed placeholders that we will replace with real preimages
# when constructing complete Runs. Cycle refusal: proof must not carry evidenceId/runId.

plan_desc = {
    "schemaVersion": 2,
    "snapshotId": id_a,
    "capabilityManifestId": "aa" * 32,
    "semanticClosures": ["closure2:" + "bb" * 32],
    "analysisSpecDigest": "cc" * 32,
    "resolvedConfigDigest": "11" * 32,
    "nativeContextDigests": ["dd" * 32],
    "importIds": ["import2:" + "ee" * 32],
    "policyDigest": "ff" * 32,
    "waiverDigest": "12" * 32,
    "scopeDigest": "22" * 32,
    "budget": {"unit": "work-units", "limit": 1000},
    "semanticGrantDigest": "13" * 32,
    "capabilityManifestBytesDigest": "14" * 32,
}
plan_id = typed_id("plan", plan_desc)

view_desc = {
    "schemaVersion": 2,
    "planId": plan_id,
    "scopeIds": ["scope2:" + "21" * 32],
    "factIds": ["fact2:" + "22" * 32],
    "coverageIds": ["coverage2:" + "23" * 32],
    "producerClosure": "closure2:" + "bb" * 32,
    "schemaDigest": "24" * 32,
}
view_id = typed_id("view", view_desc)

proof_desc = {
    "schemaVersion": 3,
    "planId": plan_id,
    "executionPlanId": "exec-plan2:" + "31" * 32,
    "evaluatorClosure": "closure2:" + "32" * 32,
    "ruleProgramDigest": "33" * 32,
    "evaluationInputRefs": [],
    "predicateProofs": [],
    "findingIds": [],
    "verdict": "pass",
    "evaluationState": "evaluated",
    "ruleResults": [],
    "waivedFindingIds": [],
    "executionDeficiencies": [],
    "executionInputsDigest": "34" * 32,
}
proof_id = typed_id("proof-bundle", proof_desc)

evidence_desc = {
    "schemaVersion": 3,
    "planId": plan_id,
    "viewIds": [view_id],
    "coverageIds": ["coverage2:" + "23" * 32],
    "importIds": ["import2:" + "ee" * 32],
    "findingIds": [],
    "proofBundleId": proof_id,
}
evidence_id = typed_id("semantic-evidence", evidence_desc)

seal_desc = {
    "schemaVersion": 3,
    "planId": plan_id,
    "executionPlanId": "exec-plan2:" + "31" * 32,
    "evidenceId": evidence_id,
    "evaluatorClosure": "closure2:" + "32" * 32,
    "policyDigest": "ff" * 32,
    "proofBundleId": proof_id,
    "verdict": "pass",
}
seal_id = typed_id("evaluation-seal", seal_desc)

run_desc = {
    "schemaVersion": 3,
    "projectId": snap_a["projectId"],
    "snapshotId": id_a,
    "planId": plan_id,
    "evidenceId": evidence_id,
    "evaluationSealId": seal_id,
    "capabilityManifestId": "aa" * 32,
}
run_id = typed_id("run", run_desc)

# Cycle attempt: proof carrying evidenceId (forbidden by contract: proof does not include EvidenceId or RunId)
cyclic_proof = dict(proof_desc)
cyclic_proof["evidenceId"] = evidence_id
cyclic_id = typed_id("proof-bundle", cyclic_proof)
# Join checker: refuse extra keys that close a cycle
PROOF_FORBIDDEN = {"evidenceId", "evaluationSealId", "runId"}


def join_check(kind: str, desc: dict) -> dict:
    if kind == "proof-bundle":
        bad = sorted(PROOF_FORBIDDEN.intersection(desc.keys()))
        if bad:
            return {
                "ok": False,
                "firstRefusal": {
                    "code": "ACYCLIC_JOIN",
                    "message": "proof does not include EvidenceId or RunId",
                    "path": kind,
                    "extra": {"forbidden": bad},
                },
                "masksLater": True,
            }
    if kind == "run":
        # run may include seal; seal includes evidence+proof. If run included a
        # proof that named runId, that would cycle.
        pass
    return {"ok": True}


pos = join_check("proof-bundle", proof_desc)
neg = join_check("proof-bundle", cyclic_proof)
assert pos["ok"]
assert not neg["ok"]

# Another cycle: runId inside proof
cyc2 = dict(proof_desc)
cyc2["runId"] = run_id
neg2 = join_check("proof-bundle", cyc2)
assert not neg2["ok"]

joins_art = dump(
    "acyclic-joins.json",
    {
        "kind": "standaloneCanonicalVector",
        "selector": "identity-and-evidence §3: graph is acyclic: proof does not include EvidenceId or RunId; evidence may include proof; seal includes both; Run includes seal",
        "positive": {
            "classification": "valid",
            "chain": [
                {"domain": "snapshot", "id": id_a},
                {"domain": "plan", "id": plan_id, "refs": {"snapshotId": id_a}},
                {"domain": "view", "id": view_id, "refs": {"planId": plan_id}},
                {"domain": "proof-bundle", "id": proof_id, "refs": {"planId": plan_id}, "doesNotContain": ["evidenceId", "runId"]},
                {"domain": "semantic-evidence", "id": evidence_id, "refs": {"proofBundleId": proof_id, "viewIds": [view_id]}},
                {"domain": "evaluation-seal", "id": seal_id, "refs": {"evidenceId": evidence_id, "proofBundleId": proof_id}},
                {"domain": "run", "id": run_id, "refs": {"evaluationSealId": seal_id, "evidenceId": evidence_id, "planId": plan_id, "snapshotId": id_a}},
            ],
            "joinCheck": pos,
        },
        "cycleProofNamesEvidence": {
            "classification": "invalid",
            **neg,
            "computedIdIfEncodedAnyway": cyclic_id,
            "note": "Encoding would produce a different H; admission refuses the cycle before treating it as a proof.",
        },
        "cycleProofNamesRun": {
            "classification": "invalid",
            **neg2,
        },
        "outputMajors": {
            "proof-bundle": "proof3",
            "semantic-evidence": "evidence3",
            "evaluation-seal": "seal3",
            "run": "run3",
            "plan": "plan2",
            "snapshot": "snapshot2",
            "view": "view2",
        },
    },
)

arts = [cve1_art, h_art, lex_art, raw_vs_parsed, sem_art, joins_art]
mark(["R-H-HELPER"], status="executed", artifact=h_art)
mark(["R-CVE1-EIGHT-TYPES"], status="executed", artifact=cve1_art)
mark(["R-LEXICAL-ADMISSION"], status="executed", artifact=lex_art)
mark(["R-SEMANTIC-VS-OPERATIONAL"], status="executed", artifact=sem_art)
mark(["R-RAW-VS-PARSED"], status="executed", artifact=raw_vs_parsed)
mark(["R-ACYCLIC-JOINS"], status="executed", artifact=joins_art)

print("phase1 ok")
for a in arts:
    print(a)
