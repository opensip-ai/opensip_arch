#!/usr/bin/env python3
"""Independent recheck of corrected R-COUNT-CLASS-ATTEMPT and R-CODE-VS-DATA-MATRIX.

Claimed ok/counts/flags are comparison targets, never oracles. Scope is standalone
vector plus raw retained Run properties, not whole-Run admission.
"""
from __future__ import annotations

import base64
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

PREV = Path("/tmp/opensip-design-corrections/consumer-b.v12-fresh-foundation-data-review.v1")
KIT = PREV / "subject"
HERE = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-foundation-phase4-recheck.v1")
DATA = HERE / "data"
OUT = Path(__file__).resolve().parent
PY = "/tmp/opensip-architecture-review-env/bin/python"
MANIFEST_EXPECTED = "0db360733a100cc56161de13389aa801f74d111b7b94b2c45a8925ce79c5017f"
KIT_MANIFEST_EXPECTED = "ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8"

RESOLVED_RUNGS = {
    "checked",
    "from-resolved-calls",
    "resolved-binding",
    "resolved-callee",
    "resolved-target",
}
DOMAIN_PREFIX = {
    "snapshot": "snapshot2",
    "subject-scope": "scope2",
    "coverage": "coverage2",
    "fact": "fact2",
    "import": "import2",
}


def sha256_file(p: Path) -> tuple[str, int]:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest(), p.stat().st_size


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def load(p: Path):
    return json.loads(p.read_text())


def c_encode(value: Any) -> bytes:
    return _c_text(value).encode("utf-8")


def _c_text(value: Any) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if type(value) is int:
        return str(value)
    if isinstance(value, str):
        return _c_string(value)
    if isinstance(value, list):
        return "[" + ",".join(_c_text(x) for x in value) + "]"
    if isinstance(value, dict):
        items = sorted(value.items(), key=lambda kv: kv[0].encode("utf-8"))
        inner = ",".join(_c_string(k) + ":" + _c_text(v) for k, v in items)
        return "{" + inner + "}"
    raise TypeError(type(value))


def _c_string(s: str) -> str:
    out = ['"']
    for ch in s:
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
    return "".join(out)


def h_frame(domain: str, record: Any) -> bytes:
    c = c_encode(record)
    return (
        b"opensip.product.v1"
        + b"\x00"
        + domain.encode("ascii")
        + b"\x00"
        + len(c).to_bytes(8, "big")
        + c
    )


def identity_bundle(domain: str, record: Any) -> dict:
    c = c_encode(record)
    frame = h_frame(domain, record)
    digest = sha256_bytes(frame)
    return {
        "C_hex": c.hex(),
        "C_sha256": sha256_bytes(c),
        "H": digest,
        "frameHex": frame.hex(),
        "frameSha256": digest,
        "frameByteLength": len(frame),
        "typedId": f"{DOMAIN_PREFIX[domain]}:{digest}",
    }


def parse_h_frame(raw: bytes) -> tuple[str, dict]:
    pfx = b"opensip.product.v1\x00"
    if not raw.startswith(pfx):
        raise ValueError("not H-frame")
    rest = raw[len(pfx) :]
    i = rest.index(b"\x00")
    domain = rest[:i].decode("ascii")
    rest = rest[i + 1 :]
    ln = int.from_bytes(rest[:8], "big")
    return domain, json.loads(rest[8 : 8 + ln].decode())


def decode_blob(blob: str):
    raw = base64.b64decode(blob)
    if raw.startswith(b"opensip.product.v1\x00"):
        return parse_h_frame(raw)
    try:
        return ("json", json.loads(raw.decode()))
    except Exception:
        return ("raw", raw)


def parse_body_identity_frame(raw: bytes) -> dict:
    """u8-len prefixed domainTag, levelId, levelVersion, languageId, languageVersion; u32 payload."""
    i = 0

    def u8_bytes():
        nonlocal i
        n = raw[i]
        i += 1
        b = raw[i : i + n]
        i += n
        return b

    tag = u8_bytes()
    level_id = u8_bytes()
    level_version = u8_bytes()
    language_id = u8_bytes()
    language_version = u8_bytes()
    plen = int.from_bytes(raw[i : i + 4], "big")
    i += 4
    payload = raw[i : i + plen]
    return {
        "domainTag": tag.decode("ascii"),
        "levelId": level_id.decode("ascii"),
        "levelVersionSha256": level_version.hex() if len(level_version) == 32 else level_version.decode("ascii", "replace"),
        "languageId": language_id.decode("ascii"),
        "languageVersionLen": len(language_version),
        "payloadLen": len(payload),
        "trailing": len(raw) - i - plen,
    }


def make_def_validator(schema: dict, def_name: str) -> Draft202012Validator:
    wrapper = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": f"urn:opensip:local:{def_name}",
        "$ref": f"#/$defs/{def_name}",
        "$defs": schema["$defs"],
    }
    resource = Resource.from_contents(wrapper, default_specification=DRAFT202012)
    registry = Registry().with_resource(wrapper["$id"], resource)
    return Draft202012Validator(wrapper, registry=registry)


def stock_errors(validator, instance) -> list:
    return [
        {"path": list(e.absolute_path), "message": e.message, "validator": e.validator}
        for e in validator.iter_errors(instance)
    ]


def compare_claimed_identity(claimed: dict, computed: dict) -> dict:
    mismatches = []
    for f in ("C_hex", "C_sha256", "H", "frameHex", "frameSha256", "frameByteLength", "typedId"):
        if f in claimed and claimed[f] != computed[f]:
            mismatches.append({"field": f, "claimed": claimed[f], "computed": computed[f]})
    return {"ok": not mismatches, "mismatches": mismatches, "computedTypedId": computed["typedId"]}


def rc_from_coverage(entry: dict, unresolved_edge_count_measured: int, ladders: dict) -> dict:
    rel = entry["relation"]
    res = entry["resolution"]
    rc = entry["resolutionCompleteness"]
    first = None
    if rel not in ladders or res not in ladders[rel]:
        return {"rc0": "unregistered-pair", "ok": False, "firstRefusal": "RC-0"}
    rc0 = "registered-pair"
    if res not in RESOLVED_RUNGS:
        expected = {
            "state": "not-applicable",
            "attempted": False,
            "unresolvedEdgeCount": 0,
            "unresolvedEdgeClasses": [],
        }
        match = (
            rc.get("state") == "not-applicable"
            and rc.get("attempted") is False
            and rc.get("unresolvedEdgeCount") == 0
            and rc.get("unresolvedEdgeClasses") == []
        )
        rc1 = "not-applicable-rung"
        rc2 = None
        if not match:
            first = "RC-1"
    else:
        rc1 = "resolved-rung"
        attempted = rc.get("attempted")
        exhaustive = rc.get("examinedExhaustive")
        terminal = rc.get("stageTerminal")
        n_unres = unresolved_edge_count_measured
        if attempted is False:
            expected_state = "not-attempted"
        elif terminal in {"unavailable", "budget-exhausted", "provider-fault", "cancelled", "crash"} or not exhaustive:
            expected_state = "partial"
        elif terminal == "complete" and exhaustive and n_unres == 0:
            expected_state = "complete"
        elif terminal == "complete" and exhaustive and n_unres >= 1:
            expected_state = "incomplete"
        else:
            expected_state = "partial"
        expected = {"state": expected_state, "attempted": bool(attempted) if expected_state != "not-attempted" else False}
        match = rc.get("state") == expected_state
        rc2 = expected_state
        if rc.get("state") == "not-applicable":
            first = "RC-1"
            match = False
        elif not match:
            first = "RC-2"
    cov = entry.get("coverage")
    exhaustive = rc.get("examinedExhaustive")
    rc6 = "hold"
    if cov == "complete" and exhaustive is not True:
        rc6 = "refuse-complete-without-exhaustive"
        first = first or "RC-6"
        match = False
    return {
        "rc0": rc0,
        "rc1": rc1,
        "rc2": rc2,
        "rc6": rc6,
        "matchObserved": match,
        "expectedState": (expected.get("state") if isinstance(expected, dict) else None),
        "observedState": rc.get("state"),
        "observedAttempted": rc.get("attempted"),
        "measuredUnresolvedEdgeCount": unresolved_edge_count_measured,
        "firstRefusal": first,
        "ok": match and rc6 == "hold" and rc0 == "registered-pair",
    }


def store_has(store: dict, digest_or_id: str) -> bool:
    ot = store.get("objectTable") or {}
    blobs = store.get("blobs") or {}
    if digest_or_id in ot or digest_or_id in blobs:
        return True
    if ":" in digest_or_id:
        d = digest_or_id.split(":", 1)[1]
        return d in ot or d in blobs
    return False


def syntax_store_measure(path: Path) -> dict:
    d = load(path)
    ctx = None
    uni = None
    facts = []
    coverages = []
    for digest, blob in (d.get("blobs") or {}).items():
        if not isinstance(blob, str):
            continue
        kind, rec = decode_blob(blob)
        if kind == "native.context.syntax.v2":
            ctx = rec
        elif kind == "native.semantic-universe.syntax.v2":
            uni = rec
        elif kind == "fact" and isinstance(rec, dict):
            facts.append({"digest": digest, "record": rec})
        elif kind == "coverage" and isinstance(rec, dict):
            # envelope; payload via payloadDigest
            coverages.append({"digest": digest, "envelope": rec})
    grammars = ((ctx or {}).get("grammarBundle") or {}).get("grammars") or []
    normalizer = ((ctx or {}).get("grammarBundle") or {}).get("normalizer") or {}
    selected = (uni or {}).get("selectedGrammarIds") or []
    clones_facts = []
    file_facts = []
    for f in facts:
        rec = f["record"]
        if rec.get("relation") == "clones":
            payload = None
            pd = rec.get("payloadDigest")
            if pd in d["blobs"]:
                k, payload = decode_blob(d["blobs"][pd])
                if k != "json":
                    payload = payload if isinstance(payload, dict) else None
            body_id = None
            language_id = None
            level_id = None
            if isinstance(payload, dict) and isinstance(payload.get("bodyIdentity"), str):
                bid = payload["bodyIdentity"]
                hexid = bid.split(":")[-1]
                if hexid in d["blobs"]:
                    raw = base64.b64decode(d["blobs"][hexid])
                    if raw.startswith(b"\x18opensip.fact-identity.v1") or raw[:1] == bytes([24]):
                        try:
                            parsed = parse_body_identity_frame(raw)
                            language_id = parsed["languageId"]
                            level_id = parsed["levelId"]
                            body_id = bid
                        except Exception as e:
                            parsed = {"error": str(e)}
                    else:
                        parsed = {"rawPrefix": raw[:20].hex()}
                else:
                    parsed = {"missingBodyIdentityBlob": True}
            clones_facts.append(
                {
                    "id": f"fact2:{f['digest']}",
                    "relation": rec.get("relation"),
                    "resolution": rec.get("resolution"),
                    "payload": payload,
                    "bodyIdentity": body_id,
                    "languageIdFromFrame": language_id,
                    "levelIdFromFrame": level_id,
                }
            )
        if rec.get("relation") == "file":
            file_facts.append({"id": f"fact2:{f['digest']}", "resolution": rec.get("resolution")})
    clones_cov = []
    for c in coverages:
        env = c["envelope"]
        pd = env.get("payloadDigest")
        payload = None
        if pd in d["blobs"]:
            k, payload = decode_blob(d["blobs"][pd])
            if k != "json":
                payload = None
        if isinstance(payload, dict) and payload.get("entry", {}).get("relation") == "clones":
            entry = payload["entry"]
            clones_cov.append(
                {
                    "id": f"coverage2:{c['digest']}",
                    "relation": entry.get("relation"),
                    "resolution": entry.get("resolution"),
                    "coverage": entry.get("coverage"),
                    "deficiency": entry.get("deficiency"),
                    "nativeCause": entry.get("nativeCause"),
                    "resolutionCompleteness": entry.get("resolutionCompleteness"),
                }
            )
    return {
        "contextDomain": "native.context.syntax.v2" if ctx else None,
        "selectedGrammarIds": selected,
        "grammarRows": [
            {
                "grammarId": g.get("grammarId"),
                "languageId": g.get("languageId"),
                "syntaxClass": g.get("syntaxClass"),
            }
            for g in grammars
        ],
        "normalizerPresent": bool(normalizer),
        "normalizerSpecificationDigest": normalizer.get("specificationDigest"),
        "clonesFacts": clones_facts,
        "clonesCoverage": clones_cov,
        "fileFacts": file_facts,
        "nFactFrames": len(facts),
    }


def main() -> int:
    first_failures = []
    not_reached = []

    man_path = DATA / "data-manifest.json"
    man_sha, man_bytes = sha256_file(man_path)
    man = load(man_path)
    file_rows = []
    for rec in man["files"]:
        p = DATA / rec["path"]
        a, s = sha256_file(p)
        file_rows.append(
            {
                "path": rec["path"],
                "expected": rec["sha256"],
                "actual": a,
                "expectedBytes": rec["bytes"],
                "actualBytes": s,
                "match": a == rec["sha256"] and s == rec["bytes"],
            }
        )
    kit_man_sha, _ = sha256_file(KIT / "consumer-input-manifest.json")
    hashes_ok = man_sha == MANIFEST_EXPECTED and all(r["match"] for r in file_rows) and kit_man_sha == KIT_MANIFEST_EXPECTED
    if not hashes_ok:
        first_failures.append({"stage": "hash", "detail": "manifest or file hash mismatch"})

    identity = load(KIT / "docs/coop/design-corrections/foundation/identity-schemas.v3.json")
    native_schema = load(KIT / "docs/coop/design-corrections/native/native-evidence.schemas.v2.json")
    rel_schema = load(KIT / "docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json")
    matrix = load(KIT / "docs/coop/design-corrections/native/native-capability-matrix.v2.json")
    grammar_reg = native_schema["x-opensip-grammar-capability-registry"]
    ladders = {n: r["ladder"] for n, r in rel_schema["x-opensip-relation-registry"]["relations"].items()}
    native_sha, _ = sha256_file(
        KIT / "docs/coop/design-corrections/native/native-evidence.schemas.v2.json"
    )
    rel_sha, _ = sha256_file(
        KIT / "docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json"
    )
    blv_enum = identity["$defs"]["body-language-version"]["properties"]["languageId"]["enum"]

    v_snapshot = make_def_validator(identity, "snapshot")
    v_scope = make_def_validator(identity, "subject-scope")
    v_cov = make_def_validator(identity, "coverage")
    v_fact = make_def_validator(identity, "fact")
    v_payload = make_def_validator(native_schema, "CoverageResultV3")

    cca = load(DATA / "foundation/count-class-attempt.json")
    cca_store = load(DATA / "foundation/count-class-attempt.store.json")
    snap = cca["retainedSnapshot"]
    snap_comp = identity_bundle("snapshot", snap["record"])
    snap_cmp = compare_claimed_identity(snap, snap_comp)
    snap_stock = stock_errors(v_snapshot, snap["record"])
    if not snap_cmp["ok"]:
        first_failures.append({"stage": "snapshot-identity", "mismatches": snap_cmp["mismatches"]})
    if snap_stock:
        first_failures.append({"stage": "snapshot-schema", "errors": snap_stock[:3]})

    cca_vectors = []
    for vec in cca.get("vectors") or []:
        name = vec["name"]
        scope = vec["retainedScope"]
        env = vec["retainedCoverageEnvelope"]
        payload = vec["retainedCoveragePayload"]
        scope_comp = identity_bundle("subject-scope", scope["record"])
        env_comp = identity_bundle("coverage", env["record"])
        payload_c = c_encode(payload["record"])
        payload_digest = sha256_bytes(payload_c)
        joins = {
            "scope.snapshotId==snapshot.typedId": scope["record"]["snapshotId"] == snap_comp["typedId"],
            "scope.relation==vector.relation": scope["record"]["relation"] == vec["relation"],
            "scope.resolution==vector.resolution": scope["record"]["resolution"] == vec["resolution"],
            "coverage.scopeId==scope.typedId": env["record"]["scopeId"] == scope_comp["typedId"],
            "coverage.payloadDigest==SHA256(C(payload))": env["record"]["payloadDigest"] == payload_digest,
            "coverage.payloadSchemaDigest==native-evidence.schemas.v2.json": env["record"]["payloadSchemaDigest"]
            == native_sha,
            "payload.key.subjectScopeCommitment==sha256:scopeH": payload["record"]["key"]["subjectScopeCommitment"]
            == "sha256:" + scope_comp["H"],
            "payload.entry.relation==scope.relation": payload["record"]["entry"]["relation"]
            == scope["record"]["relation"],
            "payload.entry.resolution==scope.resolution": payload["record"]["entry"]["resolution"]
            == scope["record"]["resolution"],
            "examinedUniverse.subjectCount==len(subjects)": payload["record"]["entry"]["examinedUniverse"][
                "subjectCount"
            ]
            == len(scope["record"]["subjects"]),
            "examinedUniverse.commitment==key.commitment": payload["record"]["entry"]["examinedUniverse"][
                "subjectScopeCommitment"
            ]
            == payload["record"]["key"]["subjectScopeCommitment"],
            "claimedPayloadDigest==computed": payload.get("digest") == payload_digest
            and payload.get("C_sha256") == payload_digest,
        }
        scope_cmp = compare_claimed_identity(scope, scope_comp)
        env_cmp = compare_claimed_identity(env, env_comp)
        stock = {
            "scope": stock_errors(v_scope, scope["record"]),
            "coverageEnvelope": stock_errors(v_cov, env["record"]),
            "coveragePayload": stock_errors(v_payload, payload["record"]),
        }
        facts = []
        for fr in vec.get("retainedFacts") or []:
            rec = fr["record"]
            fact_comp = identity_bundle("fact", rec)
            fact_cmp = compare_claimed_identity(fr, fact_comp)
            payload_obj = fr.get("payload")
            payload_digest_computed = sha256_bytes(c_encode(payload_obj)) if isinstance(payload_obj, dict) else None
            facts.append(
                {
                    "typedIdClaimed": fr.get("typedId"),
                    "typedIdComputed": fact_comp["typedId"],
                    "typedIdMatch": fr.get("typedId") == fact_comp["typedId"],
                    "identity": fact_cmp,
                    "C_sha256_computed": fact_comp["C_sha256"],
                    "C_sha256_claimed": fr.get("C_sha256"),
                    "cMatch": fact_comp["C_sha256"] == fr.get("C_sha256"),
                    "schemaErrors": stock_errors(v_fact, rec),
                    "relation": rec.get("relation"),
                    "resolution": rec.get("resolution"),
                    "payloadSchemaDigestIsRelationPayloadDoc": rec.get("payloadSchemaDigest") == rel_sha,
                    "payloadDigestJoin": payload_digest_computed == rec.get("payloadDigest")
                    if payload_digest_computed is not None
                    else None,
                    "snapshotIdJoin": rec.get("snapshotId") == snap_comp["typedId"],
                    "storeHas": store_has(cca_store, fact_comp["typedId"]),
                    "payload": payload_obj,
                }
            )
            if rec.get("relation") == "file" and isinstance(payload_obj, dict):
                path = payload_obj.get("path")
                inv = {row["path"]: row for row in snap["record"]["sourceInventory"]}
                facts[-1]["filePayloadSnapshotJoin"] = {
                    "pathInInventory": path in inv,
                    "contentSha256Match": inv.get(path, {}).get("sha256") == payload_obj.get("contentSha256"),
                    "byteLengthMatch": inv.get(path, {}).get("bytes") == payload_obj.get("byteLength"),
                    "pathInScopeSubjects": path in scope["record"]["subjects"],
                }
        unres = [
            f
            for f in (vec.get("retainedFacts") or [])
            if f["record"].get("relation") == "unresolved-edge"
            and (f.get("payload") or {}).get("relation") == vec["relation"]
        ]
        measured_unres = len(unres)
        measured_classes = sorted(
            {
                (f.get("payload") or {}).get("edgeKind")
                for f in unres
                if (f.get("payload") or {}).get("edgeKind")
            }
        )
        observed_classes = sorted(payload["record"]["entry"]["resolutionCompleteness"].get("unresolvedEdgeClasses") or [])
        rc = rc_from_coverage(payload["record"]["entry"], measured_unres, ladders)
        rc["measuredUnresolvedEdgeClasses"] = measured_classes
        rc["observedUnresolvedEdgeClasses"] = observed_classes
        rc["unresolvedClassJoin"] = measured_classes == observed_classes
        rc["unresolvedCountJoin"] = (
            payload["record"]["entry"]["resolutionCompleteness"].get("unresolvedEdgeCount") == measured_unres
        )
        if not rc["unresolvedClassJoin"] or not rc["unresolvedCountJoin"]:
            rc["ok"] = False
            rc["firstRefusal"] = rc["firstRefusal"] or "RC-2-unresolved-join"
        store_joins = {
            "scopeInStore": store_has(cca_store, scope_comp["typedId"]),
            "coverageInStore": store_has(cca_store, env_comp["typedId"]),
            "snapshotInStore": store_has(cca_store, snap_comp["typedId"]),
            "payloadBlobInStore": store_has(cca_store, payload_digest),
        }
        subjects_in_snapshot = {
            s: any(row["path"] == s for row in snap["record"]["sourceInventory"])
            for s in scope["record"]["subjects"]
            if "/" in s or s.endswith(".ts") or s.endswith(".rs")
        }
        join_ok = all(joins.values()) and scope_cmp["ok"] and env_cmp["ok"] and not any(stock[k] for k in stock)
        fact_ok = all(
            f["cMatch"]
            and f["typedIdMatch"]
            and f["identity"]["ok"]
            and not f["schemaErrors"]
            and f["snapshotIdJoin"]
            and f["payloadSchemaDigestIsRelationPayloadDoc"]
            and f["storeHas"]
            and (f["payloadDigestJoin"] is not False)
            and (
                all(f["filePayloadSnapshotJoin"].values())
                if "filePayloadSnapshotJoin" in f
                else True
            )
            for f in facts
        )
        row = {
            "name": name,
            "hasScopeRecord": True,
            "hasCoverageRecord": True,
            "nFacts": len(vec.get("retainedFacts") or []),
            "identity": {"scope": scope_cmp, "coverage": env_cmp, "payloadDigest": payload_digest},
            "joins": joins,
            "stockErrors": {k: v for k, v in stock.items() if v},
            "facts": facts,
            "storeJoins": store_joins,
            "subjectsInSnapshotInventory": subjects_in_snapshot,
            "claimedSnapshotContains": vec.get("snapshotContainsExaminedFileSubjects"),
            "rcIndependent": rc,
            "claimedDerived": vec.get("derivedFromRetained"),
            "claimedOk": vec.get("ok"),
            "independentOk": join_ok and fact_ok and rc["ok"] and all(store_joins.values()),
        }
        if not row["independentOk"] and not first_failures:
            first_failures.append({"stage": f"vector:{name}", "rc": rc, "joinsFailed": [k for k, v in joins.items() if not v]})
        cca_vectors.append(row)

    for neg in cca.get("negativeControls") or []:
        has_records = any(
            k in neg for k in ("retainedScope", "retainedCoverageEnvelope", "retainedCoveragePayload")
        )
        not_reached.append(
            {
                "control": neg.get("name"),
                "claimedRefusal": neg.get("refusal"),
                "retainedRecordsPresent": has_records,
                "status": "notReached-as-retained-record-refusal" if not has_records else "present",
            }
        )

    executed_fact_absent = any(
        v["independentOk"] and v["nFacts"] == 0 and ("fact-absent" in v["name"] or "fact-free" in v["name"])
        for v in cca_vectors
    )
    executed_rc1 = any(
        v["independentOk"] and v["rcIndependent"].get("rc1") == "not-applicable-rung" for v in cca_vectors
    )
    executed_rc2_complete = any(
        v["independentOk"] and v["rcIndependent"].get("rc2") == "complete" for v in cca_vectors
    )
    executed_rc2_incomplete = any(
        v["independentOk"]
        and v["rcIndependent"].get("rc2") == "incomplete"
        and v["rcIndependent"].get("measuredUnresolvedEdgeCount", 0) >= 1
        for v in cca_vectors
    )
    executed_rc2_not_attempted = any(
        v["independentOk"] and v["rcIndependent"].get("rc2") == "not-attempted" for v in cca_vectors
    )
    cca_pass = (
        snap_cmp["ok"]
        and not snap_stock
        and all(v["independentOk"] for v in cca_vectors)
        and executed_fact_absent
        and executed_rc1
        and executed_rc2_complete
        and executed_rc2_incomplete
        and executed_rc2_not_attempted
    )

    # ---- code vs data ------------------------------------------------------
    cvd = load(DATA / "foundation/code-vs-data-matrix.json")
    langs = grammar_reg["languages"]
    code_langs = sorted(k for k, v in langs.items() if v["syntaxClass"] == "code")
    data_langs = sorted(k for k, v in langs.items() if v["syntaxClass"] == "data-document")
    grammar_match = (
        sorted(cvd.get("grammarRegistry", {}).get("codeLanguages") or []) == code_langs
        and sorted(cvd.get("grammarRegistry", {}).get("dataLanguages") or []) == data_langs
        and cvd.get("classLaw") == grammar_reg["classLaw"]
        and ("clones@normalized-body-hash" in langs["typescript"]["capabilities"])
        is True
        and ("clones@normalized-body-hash" not in langs["json"]["capabilities"])
    )
    matrix_cells_needed = {
        ("clones-fact", "syntax-only"): None,
        ("clones-fact", "ts-tsconfig"): None,
        ("inventory", "syntax-only"): None,
    }
    for cell in matrix["cells"]:
        key = (cell["capability"], cell["mode"])
        if key in matrix_cells_needed:
            matrix_cells_needed[key] = {"state": cell["state"], "note": cell.get("note"), "deficiency": cell.get("deficiency")}
    claimed_cells = cvd.get("publishedMatrixCells") or {}
    matrix_cmp = []
    for label, claimed in claimed_cells.items():
        cap = claimed["capability"]
        mode = claimed["mode"]
        kit_cell = matrix_cells_needed.get((cap, mode))
        matrix_cmp.append(
            {
                "label": label,
                "claimedState": claimed.get("state"),
                "kitState": (kit_cell or {}).get("state"),
                "match": kit_cell is not None and kit_cell.get("state") == claimed.get("state"),
            }
        )
    blv_claimed = cvd.get("bodyLanguageVersion") or {}
    blv_match = blv_claimed.get("languageIdEnum") == blv_enum and blv_claimed.get("jsonInEnum") is ("json" in blv_enum)

    syn_code = syntax_store_measure(DATA / "runs/syntax-code.store.json")
    syn_data = syntax_store_measure(DATA / "runs/syntax-data.store.json")
    claimed_code = (cvd.get("measuredFromCitedSyntaxStores") or {}).get("syntax-code") or {}
    claimed_data = (cvd.get("measuredFromCitedSyntaxStores") or {}).get("syntax-data") or {}

    def measure_vs_claimed(measured, claimed, store_name):
        m_clone_ids = sorted(f["id"] for f in measured["clonesFacts"])
        c_clone_ids = sorted(f["id"] for f in claimed.get("clonesFacts") or [])
        m_cov_ids = sorted(c["id"] for c in measured["clonesCoverage"])
        c_cov_ids = sorted(c["id"] for c in claimed.get("clonesCoverage") or [])
        cov_fields = []
        for cc in claimed.get("clonesCoverage") or []:
            mm = next((x for x in measured["clonesCoverage"] if x["id"] == cc["id"]), None)
            cov_fields.append(
                {
                    "id": cc["id"],
                    "found": mm is not None,
                    "coverage": {"claimed": cc.get("coverage"), "measured": None if not mm else mm.get("coverage")},
                    "deficiency": {"claimed": cc.get("deficiency"), "measured": None if not mm else mm.get("deficiency")},
                    "nativeCause": {"claimed": cc.get("nativeCause"), "measured": None if not mm else mm.get("nativeCause")},
                    "match": mm is not None
                    and mm.get("coverage") == cc.get("coverage")
                    and mm.get("deficiency") == cc.get("deficiency")
                    and mm.get("nativeCause") == cc.get("nativeCause")
                    and mm.get("relation") == "clones"
                    and mm.get("resolution") == "normalized-body-hash",
                }
            )
        lang_ok = True
        body_rows = []
        for bf in claimed.get("bodyIdentityFrames") or []:
            mf = next((x for x in measured["clonesFacts"] if x["id"] == bf.get("factId")), None)
            body_rows.append(
                {
                    "factId": bf.get("factId"),
                    "claimedLanguageId": bf.get("languageId"),
                    "measuredLanguageId": None if not mf else mf.get("languageIdFromFrame"),
                    "claimedLevel": bf.get("normalisationLevel") or bf.get("levelId"),
                    "measuredLevel": None if not mf else mf.get("levelIdFromFrame"),
                    "languageIdInBLV": (None if not mf else mf.get("languageIdFromFrame") in blv_enum),
                    "match": mf is not None
                    and mf.get("languageIdFromFrame") == bf.get("languageId")
                    and mf.get("levelIdFromFrame") in {bf.get("normalisationLevel"), bf.get("levelId")},
                }
            )
            if not body_rows[-1]["match"]:
                lang_ok = False
        grammar_match_store = measured["grammarRows"] == claimed.get("grammarRows") and measured[
            "selectedGrammarIds"
        ] == claimed.get("selectedGrammarIds")
        return {
            "store": store_name,
            "selectedGrammarIdsMeasured": measured["selectedGrammarIds"],
            "selectedGrammarIdsClaimed": claimed.get("selectedGrammarIds"),
            "grammarRowsMeasured": measured["grammarRows"],
            "grammarRowsClaimed": claimed.get("grammarRows"),
            "grammarMatch": grammar_match_store,
            "normalizerDigestMeasured": measured["normalizerSpecificationDigest"],
            "normalizerDigestClaimed": claimed.get("normalizerSpecificationDigest"),
            "normalizerMatch": measured["normalizerSpecificationDigest"] == claimed.get("normalizerSpecificationDigest"),
            "clonesFactIdsMeasured": m_clone_ids,
            "clonesFactIdsClaimed": c_clone_ids,
            "clonesFactIdsMatch": m_clone_ids == c_clone_ids,
            "clonesCoverage": cov_fields,
            "bodyIdentity": body_rows,
            "fileFactsMeasured": measured["fileFacts"],
            "fileFactsClaimed": claimed.get("fileFacts"),
            "independentOk": grammar_match_store
            and measured["normalizerSpecificationDigest"] == claimed.get("normalizerSpecificationDigest")
            and m_clone_ids == c_clone_ids
            and all(c["match"] for c in cov_fields)
            and lang_ok
            and measured["fileFacts"] == (claimed.get("fileFacts") or measured["fileFacts"]),
        }

    code_cmp = measure_vs_claimed(syn_code, claimed_code, "syntax-code")
    data_cmp = measure_vs_claimed(syn_data, claimed_data, "syntax-data")

    # Original clause on MEASURED store fields (not claimed application prose)
    code_grammar = syn_code["grammarRows"][0] if syn_code["grammarRows"] else {}
    data_grammar = syn_data["grammarRows"][0] if syn_data["grammarRows"] else {}
    original_clause_measured = {
        "syntaxCodeIsCodeClass": code_grammar.get("syntaxClass") == "code",
        "syntaxCodeLanguageIdInBLV": code_grammar.get("languageId") in blv_enum,
        "syntaxCodeHasClonesFacts": len(syn_code["clonesFacts"]) > 0
        and all(f["resolution"] == "normalized-body-hash" for f in syn_code["clonesFacts"]),
        "syntaxCodeBodyLanguageIdInBLV": len(syn_code["clonesFacts"]) > 0
        and all(
            f.get("languageIdFromFrame") in blv_enum for f in syn_code["clonesFacts"]
        ),
        "syntaxCodeNormalizerDigestPresent": bool(syn_code["normalizerSpecificationDigest"]),
        "syntaxDataIsDataDocument": data_grammar.get("syntaxClass") == "data-document",
        "syntaxDataLanguageIdNotInBLV": data_grammar.get("languageId") not in blv_enum,
        "syntaxDataNoClonesFacts": syn_data["clonesFacts"] == [],
        "syntaxDataClonesCoverageUnavailable": all(
            c.get("coverage") == "unknown"
            and c.get("deficiency") == "language-tier-unsupported"
            and c.get("nativeCause") == "capability-missing"
            for c in syn_data["clonesCoverage"]
        )
        and len(syn_data["clonesCoverage"]) >= 1,
        "matrixClonesFactSyntaxOnlySupportedDesign": matrix_cells_needed[("clones-fact", "syntax-only")]["state"]
        == "SUPPORTED-DESIGN",
        "notCompleteEmptyClonesOnData": not (
            syn_data["clonesFacts"] == []
            and any(c.get("coverage") == "complete" and c.get("deficiency") is None for c in syn_data["clonesCoverage"])
        ),
    }
    application_prose = cvd.get("application") or {}
    application_mismatch = []
    if "typescript" in (application_prose.get("syntax-code") or "") and syn_code["selectedGrammarIds"] != ["typescript"]:
        application_mismatch.append(
            {
                "field": "application.syntax-code",
                "claimed": application_prose.get("syntax-code"),
                "measuredSelectedGrammarIds": syn_code["selectedGrammarIds"],
            }
        )

    cvd_pass = (
        grammar_match
        and all(c["match"] for c in matrix_cmp)
        and blv_match
        and code_cmp["independentOk"]
        and data_cmp["independentOk"]
        and all(original_clause_measured.values())
    )
    if not cvd_pass and not any(f.get("stage") == "code-vs-data" for f in first_failures):
        first_failures.append(
            {
                "stage": "code-vs-data",
                "originalClauseMeasured": {k: v for k, v in original_clause_measured.items() if not v},
                "codeCmpOk": code_cmp["independentOk"],
                "dataCmpOk": data_cmp["independentOk"],
            }
        )

    prior_selfaudit = load(
        Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-foundation-phase4-selfaudit.v1/output/foundation-phase4-selfaudit.json")
    )
    dispositions = {
        "R-COUNT-CLASS-ATTEMPT": {
            "priorSelfAudit": "withdrawn",
            "now": "executed-pass" if cca_pass else ("failed" if first_failures else "incomplete"),
            "classification": "existing-law-reconstruction-of-retained-scope-and-coverage",
            "closedIfPass": cca_pass,
        },
        "R-CODE-VS-DATA-MATRIX": {
            "priorSelfAudit": "withdrawn",
            "now": "executed-pass" if cvd_pass else "failed",
            "classification": "existing-law-reconstruction-of-matrix-and-measured-syntax-run-fields",
            "closedIfPass": cvd_pass,
            "claimedApplicationProseMismatch": application_mismatch,
        },
    }

    if not hashes_ok:
        verdict = "PHASE4_DATA_INCOMPLETE"
    elif not cca_pass or not cvd_pass:
        verdict = "PHASE4_DATA_REFUSED" if first_failures else "PHASE4_DATA_INCOMPLETE"
    else:
        verdict = "PHASE4_DATA_ADMITS"

    results = {
        "checker": "phase4_recheck.py",
        "command": f"{PY} -I -B {OUT / 'phase4_recheck.py'}",
        "verdict": verdict,
        "scope": "Bounded recheck of corrected standaloneCanonicalVectors for R-COUNT-CLASS-ATTEMPT and R-CODE-VS-DATA-MATRIX. Raw retained Run properties only; not whole-Run admission. Other Phase 4 grades retain prior scoped standing only.",
        "hashVerification": {
            "dataManifestExpected": MANIFEST_EXPECTED,
            "dataManifestActual": man_sha,
            "dataManifestBytes": man_bytes,
            "kitManifest": kit_man_sha,
            "files": file_rows,
            "allMatch": hashes_ok,
        },
        "R-COUNT-CLASS-ATTEMPT": {
            "pass": cca_pass,
            "snapshot": snap_cmp,
            "vectors": cca_vectors,
            "negativeControls": not_reached,
            "nVectorsWithScopeAndCoverage": sum(1 for v in cca_vectors if v["hasScopeRecord"] and v["hasCoverageRecord"]),
            "nFactAbsentVectors": sum(1 for v in cca_vectors if v["nFacts"] == 0),
            "executedOriginalClause": {
                "factAbsentCoverage": executed_fact_absent,
                "rc1NotApplicable": executed_rc1,
                "rc2Complete": executed_rc2_complete,
                "rc2Incomplete": executed_rc2_incomplete,
                "rc2NotAttempted": executed_rc2_not_attempted,
            },
        },
        "R-CODE-VS-DATA-MATRIX": {
            "pass": cvd_pass,
            "grammarTableMatch": grammar_match,
            "matrixCells": matrix_cmp,
            "bodyLanguageVersionMatch": blv_match,
            "syntaxCodeMeasured": syn_code,
            "syntaxDataMeasured": syn_data,
            "vsClaimed": {"syntax-code": code_cmp, "syntax-data": data_cmp},
            "originalClauseOnMeasuredFields": original_clause_measured,
            "applicationProseMismatch": application_mismatch,
        },
        "firstFailures": first_failures,
        "notReached": not_reached,
        "priorFindingDispositions": dispositions,
        "ownerMapping": {
            "countClass": [
                "native-evidence.md §4.3 RC-0/RC-1/RC-2/RC-6",
                "identity-schemas.v3.json#/$defs/subject-scope",
                "identity-schemas.v3.json#/$defs/coverage",
                "native-evidence.schemas.v2.json#/$defs/CoverageResultV3",
            ],
            "codeVsData": [
                "native-capability-matrix.v2.json cells",
                "native-evidence.schemas.v2.json#/x-opensip-grammar-capability-registry",
                "identity-schemas.v3.json#/$defs/body-language-version",
                "fact-identity-policy.v2.json body-identity framing languageId",
            ],
        },
        "otherPhase4StandingUnchanged": {
            "R-RELATION-RUNG-TABLE": "stands (prior self-audit)",
            "R-ENUM-VS-RESOLUTION": "stands (prior self-audit)",
            "R-ADVERTISED-MODE-PATHS": "stands (prior self-audit)",
        },
        "missingOrContradictoryNorm": [],
        "limitations": [
            "Cited syntax stores and count-class store are not whole-Run admitted.",
            "Negative RC-0/RC-6 controls in the vector have no retained Coverage/scope records; refusals were not executed on retained bytes.",
            "Other foundation IDs were not re-run.",
        ],
    }
    (OUT / "phase4-recheck-results.json").write_text(json.dumps(results, indent=2, default=str) + "\n")
    print(
        json.dumps(
            {
                "verdict": verdict,
                "cca": cca_pass,
                "cvd": cvd_pass,
                "firstFailures": first_failures,
                "applicationMismatch": application_mismatch,
                "ccaVectorOk": [v["name"] + ":" + str(v["independentOk"]) for v in cca_vectors],
            },
            indent=2,
        )
    )
    return 0 if verdict == "PHASE4_DATA_ADMITS" else 1


if __name__ == "__main__":
    sys.exit(main())
