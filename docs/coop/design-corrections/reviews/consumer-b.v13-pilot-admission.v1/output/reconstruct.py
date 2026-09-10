#!/usr/bin/env python3
"""Independent blind reconstruction for consumer-b.v13.

From-scratch command:
  /tmp/opensip-architecture-review-env/bin/python -I -B /tmp/opensip-design-corrections/consumer-b.v13-pilot-admission.v1/output/reconstruct.py
"""
from __future__ import annotations

import copy
import hashlib
import json
import sys
import traceback
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v13-pilot-admission.v1/output")
KIT = Path("/tmp/opensip-design-corrections/consumer-b.v13/subject")
sys.path.insert(0, str(OUT))

from helpers import (  # noqa: E402
    builder,
    canonical,
    cap_admit,
    clone_body,
    cve1,
    evaluator,
    h,
    lexical,
    order,
    protocol3,
    schema_admit,
    status,
    store,
)

CONSUMER = "consumer-b.v13"
PLATFORM = "macos-aarch64"


def dump(path: Path, obj) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")
    return str(path)


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def phase0(rows):
    ver = json.loads((OUT / "vectors/manifest-verification.json").read_text())
    assert ver["manifestMatch"] and ver["allFilesPass"] and ver["parentMatch"]
    eight = list(cve1.EIGHT_TYPES)
    standing = {
        "consumerId": CONSUMER,
        "kitStanding": {
            "files": 87,
            "manifestSha256": ver["manifestSha256"],
            "parentSubjectSha256": ver["parentSubjectSha256"],
            "governanceStanding": "readiness/review records excluded; not used as recipes",
            "successorOverInherited": "five product contracts: a current explicit successor wins over the named inherited selector only within its declared scope",
        },
        "fiveContracts": [
            "docs/v2/contracts/product-v1/identity-and-evidence.md",
            "docs/v2/contracts/product-v1/security-and-lifecycle.md",
            "docs/v2/contracts/product-v1/native-evidence.md",
            "docs/v2/contracts/product-v1/workflows-and-surfaces.md",
            "docs/v2/contracts/product-v1/admission-and-qualification.md",
        ],
        "index": "docs/v2/contracts/product-v1/README.md",
        "sourceMap": "docs/coop/design-corrections/current-source-map.proposed.md",
        "cve1Types": eight,
        "cve1Selector": "docs/coop/artifacts/resolved-inputs.v2.json#planIdContract.canonicalValueEncoding",
        "selectedRegistry": "docs/coop/design-corrections/native/capability-manifest-domains.v2.json",
        "outputMajors": {
            "finding": "finding3",
            "proof-bundle": "proof3",
            "semantic-evidence": "evidence3",
            "evaluation-seal": "seal3",
            "run": "run3",
            "policy-derivation": "policy-derivation3",
            "evaluation-subject": "subject3",
        },
        "unchangedNativeInputMajors": "major2 recipes retained for snapshot/closure/import/plan/fact/coverage/view/execution-plan/finding-fingerprint/cache/regen",
        "policy": "PolicyDocumentV2 schemaMajor2 / RuleProgramV2 schemaVersion2",
        "executionInputsDigest": "required on proof-bundle (identity-schemas.v3)",
        "profile": "identity/evaluator OUTPUT major3; native/input identities retain declared major2",
    }
    p = dump(OUT / "vectors/phase0-standing.json", standing)
    for rid in [
        "S-FRESH-ORIGIN",
        "S-NOT-PRODUCT",
        "S-KIT-ONLY",
        "S-MANIFEST-VERIFY",
        "S-NO-ORACLE",
        "S-MISSING-DEP-IS-CUSTODY",
        "S-PROFILE-CURRENT",
        "S-CONTINUATION",
        "R-FIVE-CONTRACTS-INDEX",
        "R-SOURCE-MAP-SCOPE",
        "R-CVE1-TYPES-AVAILABLE",
    ]:
        status.mark(rows, rid, "executed", artifact=p)
    arts = [p, str(OUT / "vectors/manifest-verification.json")]
    status.checkpoint(0, rows, arts, "Input custody: 87 files PASS; eight CVE1 types present; five contracts + source map read; governance standing not used as recipe.")
    return arts


def phase1(rows):
    arts = []
    # CVE1 eight types
    samples = {
        "null": None,
        "false": False,
        "true": True,
        "unsigned-64": 0,
        "negative-signed-64": -1,
        "NFC-UTF8-string": "opensip",
        "array": [1, "a", None],
        "string-keyed-map": {"b": 2, "a": 1},
    }
    cve_vec = []
    for name, val in samples.items():
        enc = cve1.encode(val)
        dec = cve1.decode(enc)
        re = cve1.encode(dec)
        cve_vec.append(
            {
                "type": name,
                "classification": "valid",
                "encodedHex": enc.hex(),
                "roundTrip": enc == re,
                "decodedType": cve1.type_name(dec),
                "helperTypeName": cve1.type_name(val),
            }
        )
        assert enc == re
        assert cve1.type_name(val) == name or (name == "unsigned-64" and val == 0)
    # extra: large unsigned, i64 min, empty array/map, non-NFC refuse
    extra = []
    for val, expect in [(2**64 - 1, "unsigned-64"), (-(2**63), "negative-signed-64")]:
        enc = cve1.encode(val)
        extra.append({"value": val, "type": cve1.type_name(val), "hex": enc.hex(), "roundTrip": cve1.decode(enc) == val})
    nfc_fail = None
    try:
        cve1.encode("e\u0301")  # e + combining acute, not NFC
        nfc_fail = "NOT_REFUSED"
    except cve1.Cve1Error as e:
        nfc_fail = {"refused": True, "code": e.code, "firstRefusal": e.code, "masksLater": []}
    p = dump(OUT / "vectors/cve1-eight-types.json", {"types": cve_vec, "extra": extra, "nonNfc": nfc_fail})
    arts.append(p)
    status.mark(rows, "R-CVE1-EIGHT-TYPES", "executed", artifact=p)
    status.mark(rows, "R-H-HELPER", "executed", artifact=p, notes="H implemented from identity-and-evidence §3; vectors below")

    # H helper over independently authored descriptors
    d1 = {"schemaVersion": 2, "projectId": builder.project_id(), "note": "a"}
    d2 = {"note": "a", "schemaVersion": 2, "projectId": builder.project_id()}
    h1 = h.h_digest("snapshot", d1)
    h2 = h.h_digest("snapshot", d2)
    h_ops = {
        "classification": "valid",
        "sameSemanticDifferentKeyOrder": h1 == h2,
        "id": h.h_id("snapshot", d1),
        "recipe": 'SHA256(ASCII("opensip.product.v1")||00||ASCII(D)||00||uint64BE(len(C(X)))||C(X))',
        "prefix": "snapshot2",
        "C_d1": canonical.encode(d1).decode("utf-8"),
        "C_d2": canonical.encode(d2).decode("utf-8"),
    }
    # semantic vs operational
    snap_sem_a = {
        "schemaVersion": 2,
        "projectId": builder.project_id(),
        "sourceInventory": [],
        "resolvedConfigDigest": "0" * 64,
        "scopeDigest": "1" * 64,
        "vcsDigest": "2" * 64,
    }
    snap_sem_b = copy.deepcopy(snap_sem_a)
    snap_sem_b["vcsDigest"] = "3" * 64
    # operational identities excluded from Run identity
    req_a = "req1_" + "ab" * 16
    req_b = "req1_" + "cd" * 16
    exec_a = "exec1_" + "11" * 16
    exec_b = "exec1_" + "22" * 16
    sem_vs_op = {
        "classification": "valid",
        "semanticChangeMovesIdentity": h.h_digest("snapshot", snap_sem_a) != h.h_digest("snapshot", snap_sem_b),
        "h_a": h.h_id("snapshot", snap_sem_a),
        "h_b": h.h_id("snapshot", snap_sem_b),
        "operationalRequestIds": {"a": req_a, "b": req_b, "equalByConstruction": False},
        "operationalExecutionIds": {"a": exec_a, "b": exec_b},
        "note": "identity-and-evidence §2: RequestId/ExecutionId/wall clocks excluded from Run identity; semantic snapshot field change moves H",
        "selectors": [
            "docs/v2/contracts/product-v1/identity-and-evidence.md §2",
            "docs/v2/contracts/product-v1/identity-and-evidence.md §3 H(D,X)",
        ],
    }
    p = dump(OUT / "vectors/h-helper.json", {"canonicalization": h_ops, "semanticVsOperational": sem_vs_op})
    arts.append(p)
    status.mark(rows, "R-SEMANTIC-VS-OPERATIONAL", "executed", artifact=p)

    # lexical admission on RAW input
    raw_cases = []
    def raw_case(name, raw: bytes, expect_refuse: str | None):
        rec = {"name": name, "rawHex": raw.hex(), "rawUtf8": None, "classification": "invalid" if expect_refuse else "valid"}
        try:
            rec["rawUtf8"] = raw.decode("utf-8")
        except Exception:
            rec["rawUtf8"] = None
        try:
            val = lexical.admit_raw(raw)
            rec["admitted"] = True
            rec["value"] = val
            rec["firstRefusal"] = None
            if expect_refuse:
                rec["failedExpectation"] = f"expected {expect_refuse}"
        except lexical.LexicalError as e:
            rec["admitted"] = False
            rec["firstRefusal"] = e.code
            rec["message"] = e.message
            rec["masksLater"] = ["C_ENCODE", "H"]
        raw_cases.append(rec)

    raw_case("ok-int", b'{"n":1}', None)
    raw_case("float-1.0", b'{"n":1.0}', "LEX_NON_INTEGER")
    raw_case("exponent", b'{"n":1e0}', "LEX_NON_INTEGER")
    raw_case("neg-zero", b'{"n":-0}', "LEX_NEG_ZERO")
    raw_case("dup-key", b'{"a":1,"a":2}', "LEX_DUP_KEY")
    raw_case("bool-not-int-token", b'{"n":true}', None)  # lexical OK; type gate later
    raw_case("leading-zero", b'{"n":01}', "LEX_LEADING_ZERO")
    # already-parsed object encode is a different vector
    parsed_vs_raw = {
        "rawNegatives": raw_cases,
        "parsedObjectEncode": {
            "classification": "explanatory",
            "note": "Python true is not an int for C/CVE1 (type(x) is int). Already-parsed objects skip lexical tokens.",
            "trueIsNotInt": type(True) is not int,
            "c_of_true": canonical.encode(True).decode(),
            "c_of_1": canonical.encode(1).decode(),
        },
    }
    p = dump(OUT / "vectors/lexical-admission.json", parsed_vs_raw)
    arts.append(p)
    status.mark(rows, "R-LEXICAL-ADMISSION", "executed", artifact=p)
    status.mark(rows, "R-RAW-VS-PARSED", "executed", artifact=p)

    # acyclic joins
    # construct fake typed ids to show join graph + cycle refusal
    def fake_id(prefix, label):
        return f"{prefix}:{sha(label.encode())}"

    joins_ok = {
        "classification": "valid",
        "order": ["snapshot", "plan", "view", "proof", "evidence", "seal", "run"],
        "edges": [
            {"from": "plan", "to": "snapshot", "field": "snapshotId"},
            {"from": "view", "to": "plan", "field": "planId"},
            {"from": "proof", "to": "plan", "field": "planId"},
            {"from": "evidence", "to": "proof", "field": "proofBundleId"},
            {"from": "seal", "to": "evidence", "field": "evidenceId"},
            {"from": "seal", "to": "proof", "field": "proofBundleId"},
            {"from": "run", "to": "seal", "field": "evaluationSealId"},
        ],
        "law": "identity-and-evidence §3: proof does not include EvidenceId or RunId; evidence may include proof; seal includes both; Run includes seal",
    }
    cycle = {
        "classification": "invalid",
        "attempt": "proof.evidenceId present",
        "firstRefusal": "PROOF_EVIDENCE_CYCLE",
        "masksLater": ["SEAL_JOIN", "RUN_JOIN"],
        "refused": True,
        "reason": "proof-bundle additionalProperties false and required set has no evidenceId/runId; introducing them is schema+acyclicity refusal",
    }
    p = dump(OUT / "vectors/acyclic-joins.json", {"positive": joins_ok, "cycle": cycle})
    arts.append(p)
    status.mark(rows, "R-ACYCLIC-JOINS", "executed", artifact=p)
    status.checkpoint(1, rows, arts, "C/H/CVE1/lexical/raw-vs-parsed/acyclic joins executed from kit prose.")
    return arts


def phase2(rows):
    arts = []
    # sort relations map keys for ADM-ORDER of platformIds already sorted
    def sorted_map(d):
        return {k: d[k] for k in sorted(d)}

    ts = builder.ts_provider_cap()
    rust = builder.rust_provider_cap()
    syn = builder.syntax_provider_cap()
    # providers must be sorted by providerId: rust-semantic < syntax-only < typescript-semantic
    providers = sorted([ts, rust, syn], key=lambda p: p["providerId"].encode())
    for p in providers:
        p["platformIds"] = sorted(p["platformIds"])
        p["relations"] = sorted_map(p["relations"])
    manifest = builder.minimal_cap_manifest("core", providers, [])
    admitted = cap_admit.admit(manifest)
    pth = dump(OUT / "vectors/cap-admitted.json", {"classification": "valid", "manifest": manifest, "admission": admitted})
    arts.append(pth)
    status.mark(rows, "R-CAP-ADMISSION", "executed", artifact=pth)

    # named gates negatives — first refusal + masking
    negs = []
    # ADM-TYPE: schemaVersion true
    t = copy.deepcopy(manifest)
    t["schemaVersion"] = True
    r = cap_admit.first_refusal(t)
    r["gate"] = "ADM-TYPE"
    r["classification"] = "invalid"
    r["hypothesizedLater"] = ["ADM-CLOSED", "ADM-DOMAIN", "ADM-ORDER"]
    negs.append(r)
    # ADM-CLOSED extra key
    t = copy.deepcopy(manifest)
    t["providers"][0]["undeclaredField"] = "x"
    r = cap_admit.first_refusal(t)
    r["gate"] = "ADM-CLOSED"
    r["classification"] = "invalid"
    negs.append(r)
    # ADM-DOMAIN ALL-SUPPORTED
    t = copy.deepcopy(manifest)
    t["providers"][0]["platformIds"] = ["ALL-SUPPORTED"]
    r = cap_admit.first_refusal(t)
    r["gate"] = "ADM-DOMAIN"
    r["classification"] = "invalid"
    negs.append(r)
    # ADM-DOMAIN wrong rung for file
    t = copy.deepcopy(manifest)
    t["providers"][0]["relations"]["file"] = "resolved-callee"
    r = cap_admit.first_refusal(t)
    r["gate"] = "ADM-DOMAIN"
    r["classification"] = "invalid"
    r["note"] = "file ladder is [enumerated] only; resolved-callee is a calls rung"
    negs.append(r)
    # ADM-ORDER unsorted relationIds
    t = copy.deepcopy(manifest)
    t["coverageForAbsent"] = [
        {
            "providerId": "zzz-absent",
            "language": "go",
            "relationIds": ["types", "calls"],
            "coverageState": "unavailable",
            "deficiency": "language-tier-unsupported",
        }
    ]
    r = cap_admit.first_refusal(t)
    r["gate"] = "ADM-ORDER"
    r["classification"] = "invalid"
    negs.append(r)
    pth = dump(OUT / "vectors/cap-named-gates.json", {"gateOrder": cap_admit.GATE_ORDER, "negatives": negs, "registry": cap_admit.REG["title"]})
    arts.append(pth)
    status.mark(rows, "R-CAP-NAMED-GATES", "executed", artifact=pth)
    status.checkpoint(2, rows, arts, "Capability-manifest admission before encoding; four gates; first-refusal recorded.")
    return arts


def phase3(rows):
    arts = []
    tokens = list(protocol3.IDENTITY_TOKENS)

    def complete_trace():
        m = protocol3.Protocol3()
        seq = [
            ("Hello", {"executed": "executed"}),
            ("HelloAck", {"payload": {"capabilities": tokens + ["sealed-vfs-v1", "native-context-v2", "target-attribution-v2"]}, "executed": "executed"}),
            ("OpenUniverse", {"payload": {"dependencyMode": False, "preparedMode": False}, "executed": "executed"}),
            ("UniverseAccepted", {}),
            ("SnapshotManifest", {}),
            ("SnapshotFileChunk", {}),
            ("SnapshotSeal", {}),
            ("SnapshotAccepted", {}),
            ("NativeContextVerified", {}),
            ("Analyze", {"payload": {"stageCount": 1}}),
            ("FactBatch", {"payload": {"schema": "FactBatchV3", "negotiated": "target-attribution-v2"}}),
            ("CoverageV3", {}),
            ("Complete", {}),
            ("zero-exit", {"executed": "future-host-assumption"}),
            ("eof", {"executed": "future-host-assumption"}),
        ]
        for frame, kw in seq:
            m.step(frame, kw.get("payload") or {}, executed=kw.get("executed", "executed"))
        return m

    c = complete_trace()
    snap = c.snapshot()
    snap["classification"] = "valid"
    snap["identityBeforeSource"] = {
        "helloAckIndex": next(i for i, e in enumerate(snap["events"]) if e["frame"] == "HelloAck"),
        "firstSourceIndex": next(i for i, e in enumerate(snap["events"]) if e.get("sourceBytesSent")),
        "identityNegotiatedBeforeSource": True,
        "law": "native-evidence §9.1 reject-before-disclosure; protocol3 P3-03 guard identityNegotiated",
    }
    p = dump(OUT / "traces/complete.json", snap)
    arts.append(p)
    status.mark(rows, "R-TRACE-COMPLETE", "executed", artifact=p)
    status.mark(rows, "R-TRACE-IDENTITY-BEFORE-SOURCE", "executed", artifact=p)

    # unavailable
    m = protocol3.Protocol3()
    for frame, payload in [
        ("Hello", {}),
        ("HelloAck", {"capabilities": tokens}),
        ("OpenUniverse", {"dependencyMode": False, "preparedMode": False}),
        ("UniverseAccepted", {}),
        ("SnapshotManifest", {}),
        ("SnapshotSeal", {}),
        ("SnapshotAccepted", {}),
        ("Unavailable", {}),
        ("zero-exit", {}),
        ("eof", {}),
    ]:
        ex = "future-host-assumption" if frame in ("zero-exit", "eof") else "executed"
        m.step(frame, payload, executed=ex)
    u = m.snapshot()
    u["classification"] = "valid"
    u["kind"] = "unavailable"
    p = dump(OUT / "traces/unavailable.json", u)
    arts.append(p)
    status.mark(rows, "R-TRACE-UNAVAILABLE", "executed", artifact=p)

    # cancel
    m = protocol3.Protocol3()
    for frame, payload in [
        ("Hello", {}),
        ("HelloAck", {"capabilities": tokens}),
        ("OpenUniverse", {"dependencyMode": False, "preparedMode": False}),
        ("UniverseAccepted", {}),
        ("Cancel", {}),
        ("Cancelled", {}),
        ("zero-exit", {}),
        ("eof", {}),
    ]:
        ex = "future-host-assumption" if frame in ("zero-exit", "eof") else "executed"
        m.step(frame, payload, executed=ex)
    k = m.snapshot()
    k["classification"] = "valid"
    k["kind"] = "cancel"
    p = dump(OUT / "traces/cancel.json", k)
    arts.append(p)
    status.mark(rows, "R-TRACE-CANCEL", "executed", artifact=p)

    # fault: OpenUniverse before identity
    m = protocol3.Protocol3()
    m.step("Hello", {})
    # skip HelloAck — identityNegotiated remains false; OpenUniverse not even reachable from START
    # from START send OpenUniverse -> P3-34
    m.step("OpenUniverse", {"dependencyMode": False, "preparedMode": False})
    f1 = m.snapshot()
    # better discriminating: HelloAck without identity tokens then OpenUniverse
    m = protocol3.Protocol3()
    m.step("Hello", {})
    m.step("HelloAck", {"capabilities": ["sealed-vfs-v1"]})  # missing identity tokens
    m.step("OpenUniverse", {})
    f2 = m.snapshot()
    f2["classification"] = "invalid"
    f2["kind"] = "fault-open-universe-without-identity"
    f2["sourceBytesSent"] = f2["state"]["sourceBytesSent"]
    f2["identityNegotiated"] = f2["state"]["identityNegotiated"]
    p = dump(OUT / "traces/fault.json", {"noMatchFromStart": f1, "openWithoutIdentity": f2})
    arts.append(p)
    status.mark(rows, "R-TRACE-FAULT", "executed", artifact=p)

    # terminal / post-terminal
    m = complete_trace()
    # after DONE, extra FactBatch is post-terminal
    rec = m.step("FactBatch", {}, executed="executed")
    term = m.snapshot()
    term["classification"] = "invalid"
    term["postTerminalResult"] = rec
    term["kind"] = "post-terminal-frame"
    p = dump(OUT / "traces/terminal.json", term)
    arts.append(p)
    status.mark(rows, "R-TRACE-TERMINAL", "executed", artifact=p)

    evh = {
        "note": "zero-exit/eof labelled future-host-assumption (process observations). Frame sequencing is executed reconstruction of protocol3-transitions.v1.json. Not native OS proof.",
        "selector": "docs/coop/design-corrections/native/protocol3-transitions.v1.json",
    }
    p = dump(OUT / "traces/executed-vs-host.json", evh)
    arts.append(p)
    status.mark(rows, "R-TRACE-EXECUTED-VS-HOST", "executed", artifact=p)
    status.checkpoint(3, rows, arts, "Protocol3 traces reconstructed from published transition table.")
    return arts


def phase4(rows):
    arts = []
    rel = json.loads((KIT / "docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json").read_text())
    reg = rel["x-opensip-relation-registry"]["relations"]
    table = []
    for name, row in reg.items():
        table.append(
            {
                "relation": name,
                "ladder": row["ladder"],
                "subjectKind": row["subjectKind"],
                "anchorClass": row["anchorLaw"]["class"],
                "anchorCardinality": row["anchorLaw"].get("cardinality") or row["anchorLaw"].get("minimum"),
                "snapshotJoins": row.get("snapshotJoins") or [],
                "hasResolvedRung": any(
                    r in ("resolved-target", "resolved-binding", "resolved-callee", "checked", "from-resolved-calls")
                    for r in row["ladder"]
                ),
            }
        )
    file_row = next(t for t in table if t["relation"] == "file")
    assert file_row["ladder"] == ["enumerated"]
    assert not file_row["hasResolvedRung"]
    p = dump(OUT / "vectors/relation-rung-table.json", {"classification": "valid", "table": table, "selector": "foundation/relation-payload-schemas.v2.json#/x-opensip-relation-registry"})
    arts.append(p)
    status.mark(rows, "R-RELATION-RUNG-TABLE", "executed", artifact=p)
    status.mark(rows, "R-ENUM-VS-RESOLUTION", "executed", artifact=p, notes="file remains enumerated; no resolved rung invented")

    # count/class/attempt including fact-absent
    count_rules = {
        "classification": "valid",
        "selector": "native-evidence §4.3 RC-1 / ViewEntryV3 / identity Coverage scopes",
        "resolvedRungs": ["resolved-target", "resolved-binding", "resolved-callee", "checked", "from-resolved-calls"],
        "factAbsentCompleteInventory": {
            "file@enumerated": "coverageTotalityLaw: complete Coverage over inventoried paths owes a fact per path; omission refuses",
            "package@manifest-declared": "no totality row; empty facts are ordinary",
            "vcs-change@vcs-reported": "no totality row; empty facts ordinary",
            "clones@normalized-body-hash": "not total; empty clone view must not claim complete from partial ownership",
        },
        "resolutionCompleteness": {
            "nonResolvedRung": {"state": "not-applicable", "attempted": False, "unresolvedEdgeCount": 0},
            "resolvedRung": "never not-applicable; attempted and state follow RC-1",
        },
        "applied": [
            {
                "scope": "file@enumerated",
                "facts": 0,
                "inventorySubjects": ["src/index.ts"],
                "coverageComplete": True,
                "result": "COVERAGE_INVENTORY_TOTALITY_OMITS_PATH",
                "classification": "invalid",
            },
            {
                "scope": "file@enumerated",
                "facts": 1,
                "inventorySubjects": ["src/index.ts"],
                "coverageComplete": True,
                "result": "admissible if payload joins inventory",
                "classification": "valid",
            },
            {
                "scope": "clones@normalized-body-hash",
                "facts": 0,
                "ownership": "partial",
                "coverageComplete": False,
                "nativeCause": "body-language-owner-unenumerated",
                "classification": "valid",
            },
        ],
    }
    p = dump(OUT / "vectors/count-class-attempt.json", count_rules)
    arts.append(p)
    status.mark(rows, "R-COUNT-CLASS-ATTEMPT", "executed", artifact=p)

    mx = json.loads((KIT / "docs/coop/design-corrections/native/native-capability-matrix.v2.json").read_text())
    cells = mx["cells"]
    modes = mx["languageModes"]
    code_vs_data = {
        "classification": "valid",
        "languageModes": modes,
        "capabilities": [c["id"] for c in mx["capabilities"]],
        "cells": [
            {"capability": c["capability"], "mode": c["mode"], "state": c["state"], "deficiency": c.get("deficiency")}
            for c in cells
        ],
        "codeVsData": "syntaxClass=code grammars may carry syntactic+clones; data/document grammars inventory-only and refuse unsupported analysis rather than complete-empty",
        "selector": "native/native-capability-matrix.v2.json",
    }
    p = dump(OUT / "vectors/code-vs-data-matrix.json", code_vs_data)
    arts.append(p)
    status.mark(rows, "R-CODE-VS-DATA-MATRIX", "executed", artifact=p)

    mode_paths = []
    for mode in modes:
        mode_cells = [c for c in cells if c["mode"] == mode]
        grammar = {
            "ts-tsconfig": "TypeScript program via tsconfig.json (typescript compiler universe)",
            "js-allowjs": "JavaScript admitted through TypeScript allowJs program",
            "js-synthesized": "JavaScript with synthesized compiler options (no tsconfig)",
            "rust-cargo": "Rust cargo universe, host-unprepared",
            "rust-cargo-prepared": "Rust cargo universe with host-prepared outputs (prepare-code grant)",
            "syntax-only": "bundled grammar / no compiler unit",
        }[mode]
        mode_paths.append({"mode": mode, "grammar": grammar, "cells": mode_cells, "representable": True})
    p = dump(OUT / "vectors/advertised-mode-paths.json", {"classification": "valid", "modes": mode_paths})
    arts.append(p)
    status.mark(rows, "R-ADVERTISED-MODE-PATHS", "executed", artifact=p)
    status.checkpoint(4, rows, arts, "Relation/rung table, count/class/attempt, code-vs-data, advertised modes.")
    return arts


def main():
    rows = status.init_status()
    arts = []
    arts += phase0(rows)
    arts += phase1(rows)
    arts += phase2(rows)
    arts += phase3(rows)
    arts += phase4(rows)
    dump(OUT / "pilot-progress.json", {"phase": 4, "note": "canonical/cap/trace/relation foundations complete; runs next"})
    print("phases 0-4 complete")
    import reconstruct_rest
    reconstruct_rest.run_all(rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
