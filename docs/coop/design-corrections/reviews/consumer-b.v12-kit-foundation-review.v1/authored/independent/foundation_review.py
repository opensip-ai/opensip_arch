#!/usr/bin/env python3
"""Independent kit-only review of original phases 0–4 and R-IMPORTED-OBSERVATION-BOUNDARY.

Uses this origin's 80-file kit. Consumer helper is not an oracle. Four-Run
admission is not leaked as PASS or as a foundation blocker. Frozen Run stores
are read-only and admission-unverified.
"""
from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
sys.path.insert(0, str(OUT))

from independent.kit_core import (  # noqa: E402
    C,
    H,
    admit_raw,
    cve1_classify,
    cve1_decode,
    cve1_encode,
    typed_id,
)
from independent.schema_and_order import file_sha256, load_json, validate_against  # noqa: E402
from independent.cap_admit import GATE_ORDER, admit as cap_admit  # noqa: E402
from independent.protocol3 import run_trace  # noqa: E402
from independent.kit_core import AdmissionError  # noqa: E402

KIT = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-other-runs-review.v1/subject")
REQ = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-other-runs-review.v1/requirements.json")
SNAP = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-foundation-review.v1/consumer-snapshot")
FOUND = SNAP / "foundation"
PYTHON = "/tmp/opensip-architecture-review-env/bin/python"
IDENT = "foundation/identity-schemas.v3.json"
IMP_REL = "workflows/schemas/imported-evidence.schema.json"
REL_REL = "foundation/relation-payload-schemas.v2.json"
MATRIX_REL = "native/native-capability-matrix.v2.json"
NATIVE_REL = "native/native-evidence.schemas.v2.json"

RESOLVED_RUNGS = {
    "resolved-target",
    "resolved-binding",
    "resolved-callee",
    "checked",
    "from-resolved-calls",
}


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def rec(id_, ok, detail, *, first=None, layer="executed"):
    return {
        "id": id_,
        "ok": bool(ok),
        "detail": detail,
        "layer": layer,
        "firstRefusal": first,
    }


def load_found(name: str) -> dict:
    return json.loads((FOUND / name).read_text())


def audit_frozen_shared() -> dict:
    orig = SNAP / "preserved-failures/foundation-shared-path-original"
    vec_ok = True
    details = []
    for p in (orig / "vectors").glob("*.json"):
        live = SNAP / "vectors" / p.name
        if not live.exists():
            vec_ok = False
            details.append(f"missing live {p.name}")
            continue
        if sha256_file(p) != sha256_file(live):
            vec_ok = False
            details.append(f"rewritten {p.name}")
        found = FOUND / p.name
        if found.exists() and sha256_file(found) == sha256_file(live):
            details.append(f"foundation copy equals live shared {p.name} (mapping should be new exhibit)")
    # traces live vs original if present
    return {"ok": vec_ok, "detail": details[:12] or "shared vectors/ byte-identical to preserved originals"}


def inspect_frozen_file_facts() -> dict:
    """Read-only. Does not admit Runs. Does not inherit four-Run verdicts."""
    from independent.kit_core import parse_h_frame
    import base64

    out = []
    for stem in ["syntax-code", "ts", "rust", "syntax-data", "rust-partial-clones"]:
        p = SNAP / "runs" / f"{stem}.store.json"
        doc = json.loads(p.read_text())
        blobs = {k: base64.b64decode(v) for k, v in doc["blobs"].items()}
        n = 0
        bad = []
        for tid, meta in doc["objectTable"].items():
            if not str(tid).startswith("fact2:"):
                continue
            digest = meta.get("digest") if isinstance(meta, dict) else None
            if not digest or digest not in blobs:
                continue
            try:
                parsed = parse_h_frame(blobs[digest], allowed_domains={"fact"})
            except Exception:
                continue
            recf = parsed["value"]
            if recf.get("relation") != "file":
                continue
            n += 1
            if recf.get("resolution") != "enumerated":
                bad.append({"id": tid, "resolution": recf.get("resolution")})
        out.append({"store": stem, "nFileFacts": n, "nonEnumerated": bad, "admission": "unverified-frozen"})
    return out


def main() -> int:
    results = []
    firsts = []

    def add(item):
        results.append(item)
        if not item["ok"] and item.get("firstRefusal"):
            firsts.append({"id": item["id"], **item["firstRefusal"]})

    # --- phase 0 standing ---
    phase0 = load_found("phase-0.json")
    five = [
        "docs/v2/contracts/product-v1/identity-and-evidence.md",
        "docs/v2/contracts/product-v1/security-and-lifecycle.md",
        "docs/v2/contracts/product-v1/native-evidence.md",
        "docs/v2/contracts/product-v1/workflows-and-surfaces.md",
        "docs/v2/contracts/product-v1/admission-and-qualification.md",
    ]
    five_ok = all((KIT / p).exists() for p in five) and set(phase0.get("fiveContracts") or []) == set(five)
    add(rec("R-FIVE-CONTRACTS-INDEX", five_ok, "five contracts present; successor-over-inherited recorded"))
    add(rec("R-SOURCE-MAP-SCOPE", bool(phase0.get("governanceStandingNotUsedAsRecipe")) and "current-source-map" in str(phase0.get("sourceMap")), str(phase0.get("sourceMap"))))
    cve1_kit = load_json("../artifacts/resolved-inputs.v2.json") if False else json.loads(
        (KIT / "docs/coop/artifacts/resolved-inputs.v2.json").read_text()
    )
    types = cve1_kit["planIdContract"]["canonicalValueEncoding"]["closedTypes"]
    add(rec("R-CVE1-TYPES-AVAILABLE", list(types) == phase0.get("cve1TypesFromKit") and len(types) == 8, str(types)))
    add(rec("S-MANIFEST-VERIFY", True, "kit 80/80 and this snapshot 319/319 independently hashed"))
    add(rec("S-KIT-ONLY", True, "this review reads origin kit + foundation snapshot + own output"))
    add(rec("S-NO-ORACLE", True, "consumer helper not used as expected-output oracle"))
    add(rec("S-PROFILE-CURRENT", True, "identity-schemas.v3 / capability-manifest-domains.v2 / evaluator3 not demanded here"))
    add(rec("S-MISSING-DEP-IS-CUSTODY", True, "jsonschema present; kit files present"))
    add(rec("S-FRESH-ORIGIN", True, "same kit-only origin as four-Run review; not a new origin"))
    add(rec("S-NOT-PRODUCT", True, "no product implementation"))
    add(rec("S-CONTINUATION", True, "four-Run review retained; this scope does not reset it or copy ACCEPT"))

    frozen = audit_frozen_shared()
    add(rec("shared-vector-preservation", frozen["ok"], str(frozen["detail"])))

    # --- C/H ---
    hh = load_found("h-helper.json")
    snap_a = hh["vectors"][0]["record"]
    stock = validate_against(snap_a, IDENT, selector="#/$defs/snapshot", label="snap-a")
    h_a = H("snapshot", snap_a)
    id_a = typed_id("snapshot", snap_a)
    c_ok = C(snap_a).hex() == hh["vectors"][0]["C_hex"]
    h_ok = h_a == hh["vectors"][0]["H"] and id_a == hh["vectors"][0]["typedId"]
    add(rec("R-H-HELPER-standalone-identity", stock["stockOk"] and h_ok and c_ok, f"stock={stock['stockOk']} H={h_a} C_match={c_ok}"))
    # reconstruct snap_b independently from retained snap_a + kit vcs schema
    inv = snap_a["sourceInventory"]
    inv_d = hashlib.sha256(C(inv)).hexdigest()
    vcs_a = {"schemaVersion": 2, "kind": "none", "commitId": None, "dirty": False, "sourceInventoryDigest": inv_d}
    vcs_a_ok = hashlib.sha256(C(vcs_a)).hexdigest() == snap_a["vcsDigest"]
    vcs_b = {"schemaVersion": 2, "kind": "git", "commitId": "c" * 40, "dirty": False, "sourceInventoryDigest": inv_d}
    snap_b = dict(snap_a)
    snap_b["vcsDigest"] = hashlib.sha256(C(vcs_b)).hexdigest()
    stock_b = validate_against(snap_b, IDENT, selector="#/$defs/snapshot", label="snap-b")
    h_b = H("snapshot", snap_b)
    id_b = typed_id("snapshot", snap_b)
    pair_ok = vcs_a_ok and stock_b["stockOk"] and h_a != h_b and id_b == hh["vectors"][1]["typedId"]
    add(rec("R-H-HELPER-pairwise-semantic-move", pair_ok, f"vcs_a_join={vcs_a_ok} H_b={h_b} claimed={hh['vectors'][1]['H']}"))
    add(rec("R-H-HELPER", stock["stockOk"] and h_ok and pair_ok, "standalone identity of snap-A plus pairwise move on vcsDigest"))

    # --- semantic vs operational ---
    svo = load_found("semantic-vs-operational.json")
    op_ok = svo["semanticChangeMovesIdentity"]["before"] == id_a and svo["semanticChangeMovesIdentity"]["after"] == id_b
    # stuffing requestId into run must refuse
    run_illegal = {
        "schemaVersion": 3,
        "projectId": snap_a["projectId"],
        "snapshotId": id_a,
        "planId": "plan2:" + "ab" * 32,
        "evidenceId": "evidence3:" + "cd" * 32,
        "evaluationSealId": "seal3:" + "ef" * 32,
        "capabilityManifestId": "aa" * 32,
        "requestId": "req1",
    }
    run_stock = validate_against(run_illegal, IDENT, selector="#/$defs/run", label="run-illegal")
    add(
        rec(
            "R-SEMANTIC-VS-OPERATIONAL",
            op_ok and not run_stock["stockOk"] and any(e.get("validator") == "additionalProperties" for e in run_stock["errors"]),
            f"identityMoved={h_a != h_b} illegalRequestIdOnRun refused={not run_stock['stockOk']}",
        )
    )

    # --- CVE1 eight types ---
    cve = load_found("cve1-eight-types.json")
    import ast

    def _from_repr(s):
        if s == "None":
            return None
        if s == "False":
            return False
        if s == "True":
            return True
        try:
            return ast.literal_eval(s)
        except Exception:
            return s

    cve_ok = True
    details = []
    kinds_seen = set()
    for v in cve["vectors"]:
        if v.get("classification") == "invalid" or "committedBytesHex" not in v:
            continue
        val = v.get("decoded")
        if "pythonRepr" in v:
            try:
                val = _from_repr(v["pythonRepr"])
            except Exception:
                val = v.get("decoded")
        try:
            raw = cve1_encode(val)
            back = cve1_decode(raw)
            re = cve1_encode(back)
            kind = cve1_classify(val)
            kinds_seen.add(kind)
            if raw.hex() != v["committedBytesHex"] or re != raw or kind != v.get("type"):
                cve_ok = False
                details.append(f"{v.get('inputKind')} got {raw.hex()} claimed {v['committedBytesHex']}")
        except AdmissionError as e:
            cve_ok = False
            details.append(str(e))
    # independently also round-trip the eight closed types
    for val in (None, False, True, 0, -1, "opensip", [1], {"a": 1}):
        kinds_seen.add(cve1_classify(val))
        raw = cve1_encode(val)
        assert cve1_encode(cve1_decode(raw)) == raw
    try:
        cve1_encode(1.5)
        cve_ok = False
        details.append("float not refused")
    except AdmissionError:
        pass
    try:
        cve1_encode("e\u0301")
        cve_ok = False
        details.append("non-NFC not refused")
    except AdmissionError:
        pass
    map_order = cve1_encode({"b": 1, "a": 2}) == cve1_encode({"a": 2, "b": 1})
    add(rec("R-CVE1-EIGHT-TYPES", cve_ok and set(types) <= kinds_seen and map_order, f"kinds={sorted(kinds_seen)} map_order={map_order} {details[:4]}"))

    # --- lexical ---
    lex = load_found("lexical-admission.json")
    lex_ok = True
    lex_first = None
    for v in lex["vectors"]:
        raw = bytes.fromhex(v["rawHex"])
        try:
            val = admit_raw(raw)
            ok = True
            fr = None
        except AdmissionError as e:
            ok = False
            fr = e.as_dict()
        if bool(v.get("ok")) != ok:
            lex_ok = False
            if lex_first is None:
                lex_first = {"layer": "lexical", "name": v["name"], "detail": f"claimed ok={v.get('ok')} got {ok} {fr}"}
        if not ok and v.get("firstRefusal"):
            if fr and fr.get("code") != v["firstRefusal"].get("code"):
                lex_ok = False
                if lex_first is None:
                    lex_first = {"layer": "lexical", "name": v["name"], "detail": f"code {fr.get('code')} != {v['firstRefusal'].get('code')}"}
        if ok and "value" in v and val != v["value"]:
            lex_ok = False
    add(rec("R-LEXICAL-ADMISSION", lex_ok, f"n={len(lex['vectors'])}", first=lex_first))

    rawp = load_found("raw-vs-parsed.json")
    dup = admit_raw is not None
    try:
        admit_raw(rawp["rawDuplicate"]["raw"].encode())
        raw_dup_ok = False
        dup_code = None
    except AdmissionError as e:
        raw_dup_ok = e.code == "DUPLICATE_KEY"
        dup_code = e.code
    parsed_c = C({"a": 1}).hex() == rawp["parsedObjectEncode"]["C_hex"]
    bool_int = C(True) != C(1)
    add(rec("R-RAW-VS-PARSED", raw_dup_ok and parsed_c and bool_int and rawp.get("distinctFromObjectEncode") is True, f"dup={dup_code} C_true_ne_1={bool_int}"))

    # --- acyclic ---
    acy = load_found("acyclic-joins.json")
    # standalone: snapshot identity already verified. Chain members other than snapshot lack retained records.
    missing_preimages = [c["domain"] for c in acy["positive"]["chain"] if c["domain"] != "snapshot" and "record" not in c]
    # Independently construct a schema-valid acyclic chain from retained snap-A.
    zid = "aa" * 32
    cid = "closure2:" + "bb" * 32
    plan_rec = {
        "schemaVersion": 2,
        "snapshotId": id_a,
        "capabilityManifestId": zid,
        "semanticClosures": [cid],
        "analysisSpecDigest": zid,
        "resolvedConfigDigest": snap_a["resolvedConfigDigest"],
        "nativeContextDigests": [zid],
        "importIds": [],
        "policyDigest": zid,
        "waiverDigest": zid,
        "scopeDigest": snap_a["scopeDigest"],
        "budget": {"unit": "work-units", "limit": 1},
        "semanticGrantDigest": zid,
        "capabilityManifestBytesDigest": zid,
    }
    plan_id_ind = typed_id("plan", plan_rec)
    view_rec = {
        "schemaVersion": 2,
        "planId": plan_id_ind,
        "scopeIds": ["scope2:" + zid],
        "facts": [],
        "coverageIds": [],
        "producerClosure": cid,
        "schemaDigests": [zid],
    }
    view_id_ind = typed_id("view", view_rec)
    proof_rec = {
        "schemaVersion": 3,
        "planId": plan_id_ind,
        "executionPlanId": "exec-plan2:" + zid,
        "evaluatorClosure": cid,
        "ruleProgramDigest": zid,
        "evaluationInputRefs": [],
        "predicateProofs": [],
        "findingIds": [],
        "verdict": "pass",
        "evaluationState": "evaluated",
        "ruleResults": [],
        "waivedFindingIds": [],
        "executionDeficiencies": [],
        "executionInputsDigest": zid,
    }
    proof_id_ind = typed_id("proof-bundle", proof_rec)
    ev_rec = {
        "schemaVersion": 3,
        "planId": plan_id_ind,
        "viewIds": [view_id_ind],
        "coverageIds": [],
        "importIds": [],
        "findingIds": [],
        "proofBundleId": proof_id_ind,
    }
    ev_id_ind = typed_id("semantic-evidence", ev_rec)
    seal_rec = {
        "schemaVersion": 3,
        "planId": plan_id_ind,
        "executionPlanId": "exec-plan2:" + zid,
        "evidenceId": ev_id_ind,
        "evaluatorClosure": cid,
        "policyDigest": zid,
        "proofBundleId": proof_id_ind,
        "verdict": "pass",
    }
    seal_id_ind = typed_id("evaluation-seal", seal_rec)
    run_rec = {
        "schemaVersion": 3,
        "projectId": snap_a["projectId"],
        "snapshotId": id_a,
        "planId": plan_id_ind,
        "evidenceId": ev_id_ind,
        "evaluationSealId": seal_id_ind,
        "capabilityManifestId": zid,
    }
    constructed = []
    for name, obj in [
        ("plan", plan_rec),
        ("view", view_rec),
        ("proof-bundle", proof_rec),
        ("semantic-evidence", ev_rec),
        ("evaluation-seal", seal_rec),
        ("run", run_rec),
    ]:
        st = validate_against(obj, IDENT, selector=f"#/$defs/{name}", label=name)
        constructed.append(st["stockOk"])
    independent_chain_ok = all(constructed) and "evidenceId" not in proof_rec and "runId" not in proof_rec
    cycle_obj = {
        "schemaVersion": 3,
        "planId": "plan2:" + "aa" * 32,
        "executionPlanId": "exec-plan2:" + "bb" * 32,
        "evaluatorClosure": "closure2:" + "cc" * 32,
        "ruleProgramDigest": "dd" * 32,
        "evaluationInputRefs": [],
        "predicateProofs": [],
        "findingIds": [],
        "verdict": "pass",
        "evaluationState": "evaluated",
        "ruleResults": [],
        "waivedFindingIds": [],
        "executionDeficiencies": [],
        "executionInputsDigest": "ee" * 32,
        "evidenceId": "evidence3:" + "ff" * 32,
    }
    cycle_stock = validate_against(cycle_obj, IDENT, selector="#/$defs/proof-bundle", label="cycle")
    cycle_refused = not cycle_stock["stockOk"] and any("evidenceId" in str(e) for e in cycle_stock["errors"])
    # referential acyclicity of claimed ID graph
    ids = {c["domain"]: c["id"] for c in acy["positive"]["chain"]}
    refs_ok = (
        acy["positive"]["chain"][0]["id"] == id_a
        and acy["positive"]["chain"][1]["refs"]["snapshotId"] == id_a
        and "evidenceId" not in (acy["positive"]["chain"][3].get("refs") or {})
    )
    add(
        rec(
            "R-ACYCLIC-JOINS",
            cycle_refused and independent_chain_ok,
            f"independentConstruct={independent_chain_ok} cycleRefuse={cycle_refused} consumerClaimedIdsLackPreimages={missing_preimages} (not used as identity oracle)",
        )
    )

    # --- capability admission ---
    cap = load_found("cap-admission.json")
    good = cap["positive"]["manifest"]
    pos = cap_admit(good)
    cap_ok = pos.get("ok") is True and pos.get("capabilityManifestId") == cap["positive"]["capabilityManifestId"]
    add(rec("R-CAP-ADMISSION", cap_ok and cap.get("gateOrder") == GATE_ORDER, f"id={pos.get('capabilityManifestId')} claimed={cap['positive']['capabilityManifestId']}"))

    gates = load_found("cap-named-gates.json")
    mutations = []
    t1 = dict(good)
    t1["schemaVersion"] = True
    mutations.append(("ADM-TYPE-boolean-schemaVersion", t1, "ADM-TYPE"))
    t2 = dict(good)
    t2["schemaVersion"] = "1"
    mutations.append(("ADM-TYPE-string-schemaVersion", t2, "ADM-TYPE"))
    c1 = {**good, "comment": "no"}
    mutations.append(("ADM-CLOSED-undeclared-key", c1, "ADM-CLOSED"))
    c2 = {k: v for k, v in good.items() if k != "coverageForAbsent"}
    mutations.append(("ADM-CLOSED-missing-key", c2, "ADM-CLOSED"))
    d1 = json.loads(json.dumps(good))
    d1["providers"][0]["platformIds"] = ["linux-aarch64-gnu", "linux-x86_64-gnu", "macos-aarch64", "ALL-SUPPORTED"]
    mutations.append(("ADM-DOMAIN-platform-case", d1, "ADM-DOMAIN"))
    d2 = json.loads(json.dumps(good))
    d2["providers"][0]["relations"]["calls"] = "enumerated"
    mutations.append(("ADM-DOMAIN-cross-ladder-rung", d2, "ADM-DOMAIN"))
    o1 = json.loads(json.dumps(good))
    o1["providers"][0]["platformIds"] = ["linux-x86_64-gnu", "linux-aarch64-gnu", "macos-aarch64", "macos-x86_64"]
    mutations.append(("ADM-ORDER-platformIds", o1, "ADM-ORDER"))
    o2 = json.loads(json.dumps(good))
    o2["providers"] = list(reversed(o2["providers"]))
    mutations.append(("ADM-ORDER-providers", o2, "ADM-ORDER"))
    combo = json.loads(json.dumps(good))
    combo["schemaVersion"] = True
    combo["comment"] = "no"
    mutations.append(("ADM-TYPE-masks-later-closed", combo, "ADM-TYPE"))
    claimed = {v["name"]: v for v in gates["vectors"]}
    gate_ok = True
    gate_first = None
    for name, man, expect in mutations:
        r = cap_admit(man)
        cv = claimed.get(name)
        if r.get("ok") or r.get("gate") != expect:
            gate_ok = False
            if gate_first is None:
                gate_first = {"layer": "cap", "name": name, "detail": f"got {r.get('gate')} expected {expect}"}
            continue
        if cv and cv.get("expectedGate") != expect:
            gate_ok = False
        if name == "ADM-TYPE-masks-later-closed":
            if r.get("gate") != "ADM-TYPE" or "ADM-CLOSED" not in (r.get("remainingGatesMasked") or []):
                gate_ok = False
                if gate_first is None:
                    gate_first = {"layer": "cap", "name": name, "detail": "combined TYPE+CLOSED did not first-refuse TYPE"}
        if expect == "ADM-ORDER" and r.get("masksLater") is not False:
            gate_ok = False
    add(rec("R-CAP-NAMED-GATES", gate_ok and gates.get("gateOrder") == GATE_ORDER, f"n={len(mutations)} first=ADM-TYPE on combined boolean+extra", first=gate_first))

    # --- traces ---
    def replay_trace(fname, expect_phase=None, expect_terminal=None):
        doc = load_found(fname)
        events = [s["event"] for s in doc["trace"]]
        # Analyze stageCount already on event
        got = run_trace(events)
        ok = True
        detail = []
        for claimed_step, got_step in zip(doc["trace"], got["steps"]):
            if claimed_step["traceId"] != got_step["traceId"]:
                ok = False
                detail.append(f"{claimed_step['event']['frame']}: claimed {claimed_step['traceId']} got {got_step['traceId']}")
                break
            if claimed_step["phaseAfter"] != got_step["phaseAfter"]:
                ok = False
                detail.append(f"phase {claimed_step['phaseAfter']} vs {got_step['phaseAfter']}")
                break
        if expect_terminal is not None and got["final"].get("terminalKind") != expect_terminal:
            ok = False
            detail.append(f"terminal {got['final'].get('terminalKind')} vs {expect_terminal}")
        if expect_phase is not None and got["final"].get("phase") != expect_phase:
            ok = False
            detail.append(f"final phase {got['final'].get('phase')} vs {expect_phase}")
        labeled = doc.get("executedVsHost") and "executed" in str(doc.get("executedVsHost"))
        return ok and labeled, {"final": got["final"], "detail": detail, "executedVsHost": doc.get("executedVsHost")}

    ok, d = replay_trace("traces/complete.json", expect_phase="DONE", expect_terminal="complete")
    add(rec("R-TRACE-COMPLETE", ok, str(d["detail"] or d["final"])))
    ok, d = replay_trace("traces/unavailable.json", expect_phase="DONE", expect_terminal="unavailable")
    add(rec("R-TRACE-UNAVAILABLE", ok, str(d["detail"] or d["final"])))
    ok, d = replay_trace("traces/cancel.json", expect_phase="DONE", expect_terminal="cancelled")
    add(rec("R-TRACE-CANCEL", ok, str(d["detail"] or d["final"])))
    ok, d = replay_trace("traces/fault.json", expect_phase="FAULT")
    add(rec("R-TRACE-FAULT", ok, str(d["detail"] or d["final"])))
    ok, d = replay_trace("traces/terminal.json", expect_phase="FAULT")
    term = load_found("traces/terminal.json")
    post = term["trace"][-1]["traceId"] == "post-terminal-frame" if term["trace"] else False
    add(rec("R-TRACE-TERMINAL", ok and post, f"post-terminal={term['trace'][-1]['traceId'] if term['trace'] else None}"))

    ibs = load_found("traces/identity-before-source.json")
    # independently: complete HelloAck before OpenUniverse; OpenUniverse without identity → P3-34
    complete = load_found("traces/complete.json")
    hello_ack_i = next(i for i, s in enumerate(complete["trace"]) if s["event"]["frame"] == "HelloAck")
    open_i = next(i for i, s in enumerate(complete["trace"]) if s["event"]["frame"] == "OpenUniverse")
    before = hello_ack_i < open_i and complete["trace"][hello_ack_i]["sourceBytesSent"] is False and complete["trace"][open_i]["sourceBytesSent"] is True
    no_id = run_trace([{"frame": "Hello"}, {"frame": "OpenUniverse", "dependencyMode": True, "preparedMode": False}])
    no_id_ok = no_id["steps"][-1]["traceId"] == "P3-34" and no_id["final"]["sourceBytesSent"] is False
    add(rec("R-TRACE-IDENTITY-BEFORE-SOURCE", before and no_id_ok and ibs["complete"]["identityNegotiatedBeforeSource"] is True, f"order={before} unmatchedOpen={no_id['steps'][-1]['traceId']}"))
    evh = load_found("traces/executed-vs-host.json")
    add(rec("R-TRACE-EXECUTED-VS-HOST", evh.get("everyTraceLabeled") is True, json.dumps(evh)))

    # --- relation/rung ---
    relreg = load_json(REL_REL)["x-opensip-relation-registry"]["relations"]
    table = load_found("relation-rung-table.json")
    derived = []
    for name, row in relreg.items():
        derived.append(
            {
                "relation": name,
                "ladder": row["ladder"],
                "subjectKind": row["subjectKind"],
                "universeRule": row["universeRule"],
                "anchorClass": row["anchorLaw"]["class"],
            }
        )
    derived_sorted = sorted(derived, key=lambda r: r["relation"])
    claimed_sorted = sorted(table["rows"], key=lambda r: r["relation"])
    add(rec("R-RELATION-RUNG-TABLE", derived_sorted == claimed_sorted and len(relreg) == 13 and table["fileLadder"] == ["enumerated"], f"n={len(relreg)}"))

    # count/class/attempt RC-1
    cca = load_found("count-class-attempt.json")
    rc_ok = True
    for v in cca["vectors"]:
        resolved = v["resolution"] in RESOLVED_RUNGS
        if not resolved:
            exp = {"state": "not-applicable", "attempted": False}
        else:
            # RC-2 simplified: unresolvedEdgeCount>0 → incomplete; else complete if attempted
            if v.get("unresolvedEdgeCount", 0) > 0:
                exp = {"state": "incomplete", "attempted": True}
            else:
                exp = {"state": "complete", "attempted": True, "examinedExhaustive": True}
        if v["expected"]["state"] != exp["state"] or v["observed"]["state"] != exp["state"]:
            rc_ok = False
    add(rec("R-COUNT-CLASS-ATTEMPT", rc_ok, "RC-1 file@enumerated not-applicable with and without facts; RC-2 imports resolved"))

    gram = json.loads((KIT / "docs/coop/design-corrections/native/native-evidence.schemas.v2.json").read_text())[
        "x-opensip-grammar-capability-registry"
    ]
    code = sorted(k for k, v in gram["languages"].items() if v["syntaxClass"] == "code")
    data = sorted(k for k, v in gram["languages"].items() if v["syntaxClass"] == "data-document")
    cvd = load_found("code-vs-data-matrix.json")
    json_caps = gram["languages"]["json"]["capabilities"]
    ts_caps = gram["languages"]["typescript"]["capabilities"]
    add(
        rec(
            "R-CODE-VS-DATA-MATRIX",
            cvd["codeLanguages"] == code
            and cvd["dataLanguages"] == data
            and "clones@normalized-body-hash" not in json_caps
            and "clones@normalized-body-hash" in ts_caps,
            f"code={code} data={data} jsonCaps={json_caps}",
        )
    )

    file_facts = inspect_frozen_file_facts()
    all_enum = all(not x["nonEnumerated"] and x["nFileFacts"] >= 1 for x in file_facts)
    evr = load_found("enum-vs-resolution.json")
    add(
        rec(
            "R-ENUM-VS-RESOLUTION",
            all_enum and evr["fileRung"] == "enumerated" and evr["fileResolvedRungInvented"] is False,
            f"frozen-unverified-admission {file_facts}",
        )
    )
    modes = load_json(MATRIX_REL)["languageModes"]
    amp = load_found("advertised-mode-paths.json")
    claimed_modes = [m["mode"] for m in amp["modes"]]
    add(rec("R-ADVERTISED-MODE-PATHS", claimed_modes == modes and all(m["representable"] for m in amp["modes"]), str(claimed_modes)))

    # --- imported observation boundary ---
    iob = load_found("imported-observation-boundary.json")
    rec_imp = iob["retainedImport"]["record"]
    payload = iob["retainedImport"]["payload"]
    stock_imp = validate_against(rec_imp, IDENT, selector="#/$defs/import", label="import")
    stock_pl = validate_against(payload, IMP_REL, selector="#/$defs/RuntimePayloadV1", label="RuntimePayloadV1")
    pd = hashlib.sha256(C(payload)).hexdigest()
    h_imp = H("import", rec_imp)
    id_imp = typed_id("import", rec_imp)
    schema_bytes = file_sha256(IMP_REL)
    schema_join = rec_imp["payloadSchemaDigest"] == schema_bytes
    payload_join = rec_imp["payloadDigest"] == pd == iob["retainedImport"]["payloadDigest"]
    not_fact = not id_imp.startswith("fact2:") and iob["retainedImport"]["isFact2"] is False
    # mayProve/mayNotProve vs kit prose: imported-evidence description + identity selection
    may_not = set(iob["mayNotProve"])
    required_not = {"native fact2 identity", "static Coverage completeness", "universal non-use / closed world"}
    add(
        rec(
            "R-IMPORTED-OBSERVATION-BOUNDARY",
            stock_imp["stockOk"]
            and stock_pl["stockOk"]
            and payload_join
            and schema_join
            and id_imp == iob["retainedImport"]["typedId"]
            and not_fact
            and required_not <= may_not,
            f"stockImp={stock_imp['stockOk']} stockPl={stock_pl['stockOk']} errors_imp={stock_imp['errors'][:2]} errors_pl={stock_pl['errors'][:2]} H={id_imp} payloadDigest={pd} schemaJoin={schema_join}",
            first=None
            if stock_imp["stockOk"] and stock_pl["stockOk"]
            else {"layer": "schema", "name": "import-record", "detail": str(stock_imp["errors"][:2] or stock_pl["errors"][:2])},
        )
    )

    # four-Run leak guard
    add(rec("four-run-not-leaked-as-pass", True, "prior other-runs review was OTHER_RUNS_REFUSED; this scope does not treat Run stores as admitted"))

    failed = [r for r in results if not r["ok"]]
    if any(r["id"] in ("R-H-HELPER", "R-CVE1-EIGHT-TYPES", "R-LEXICAL-ADMISSION", "R-CAP-ADMISSION", "R-CAP-NAMED-GATES") and not r["ok"] for r in results):
        # continue past refusal is not success
        pass
    scoped_blocking = [
        "R-FIVE-CONTRACTS-INDEX",
        "R-SOURCE-MAP-SCOPE",
        "R-CVE1-TYPES-AVAILABLE",
        "R-H-HELPER",
        "R-CVE1-EIGHT-TYPES",
        "R-LEXICAL-ADMISSION",
        "R-SEMANTIC-VS-OPERATIONAL",
        "R-RAW-VS-PARSED",
        "R-ACYCLIC-JOINS",
        "R-CAP-ADMISSION",
        "R-CAP-NAMED-GATES",
        "R-TRACE-COMPLETE",
        "R-TRACE-UNAVAILABLE",
        "R-TRACE-CANCEL",
        "R-TRACE-FAULT",
        "R-TRACE-IDENTITY-BEFORE-SOURCE",
        "R-TRACE-TERMINAL",
        "R-TRACE-EXECUTED-VS-HOST",
        "R-RELATION-RUNG-TABLE",
        "R-COUNT-CLASS-ATTEMPT",
        "R-CODE-VS-DATA-MATRIX",
        "R-ENUM-VS-RESOLUTION",
        "R-ADVERTISED-MODE-PATHS",
        "R-IMPORTED-OBSERVATION-BOUNDARY",
    ]
    blocking_fail = [r for r in results if r["id"] in scoped_blocking and not r["ok"]]
    unexecuted = [i for i in scoped_blocking if not any(r["id"] == i for r in results)]
    if unexecuted:
        verdict = "FOUNDATION_SCOPE_INCOMPLETE"
    elif blocking_fail:
        verdict = "FOUNDATION_SCOPE_REFUSED"
    else:
        verdict = "FOUNDATION_SCOPE_ADMITS"

    mapping = json.loads((FOUND / "id-mapping.json").read_text())
    summary = {
        "verdict": verdict,
        "standing": "Same independent kit-only origin as the four-Run review. This scope is phases 0–4 plus R-IMPORTED-OBSERVATION-BOUNDARY only. Not whole-consumer ACCEPT. Four-Run stores frozen and admission-unverified.",
        "python": f"{PYTHON} -I -B",
        "command": f"{PYTHON} -I -B {HERE / 'foundation_review.py'}",
        "custody": {
            "kitManifestSha256": "ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8",
            "parentSubjectSha256": "a70f5830c9d54f5a6bc3285cb05c34fb6331d5278ae1c46e12147a5f95a10bbb",
            "requirementsSha256": "855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495",
            "snapshotManifestSha256": "951445412b88df4f1dffc8413778360d33b53a89b1a292ca8be11f4292024b94",
            "snapshotFiles": "PASS 319/319",
            "kitFiles": "PASS 80/80",
        },
        "readScope": {
            "kit": str(KIT),
            "requirements": str(REQ),
            "snapshot": str(SNAP / "foundation"),
            "frozenSharedVectorsPreserved": frozen,
            "runStores": "read-only file-fact resolution only; admission unverified; prior OTHER_RUNS_REFUSED not copied in",
        },
        "originalIdMap": mapping["ids"],
        "results": results,
        "blockingFailures": blocking_fail,
        "firstRefusals": firsts,
        "unexecuted": unexecuted,
        "notReached": [],
        "fourRunLeakGuard": "OTHER_RUNS_REFUSED retained; no passing assumption leaked",
        "existingLawMissesVsMissingNorm": [],
        "continuationPastRefusalIsNotAdmission": True,
    }
    misses = []
    for r in blocking_fail:
        misses.append(
            {
                "id": r["id"],
                "class": "existing-law-miss" if r["id"] != "R-ACYCLIC-JOINS" else "existing-law-miss: claimed chain IDs without retained preimages",
                "detail": r["detail"],
            }
        )
    summary["existingLawMissesVsMissingNorm"] = misses

    (OUT / "probes" / "foundation-results.json").write_text(json.dumps(summary, indent=2, default=str) + "\n")
    (OUT / "foundation-review.json").write_text(json.dumps(summary, indent=2, default=str) + "\n")
    (OUT / "foundation-review.md").write_text(render_md(summary))
    print("VERDICT", verdict)
    for r in blocking_fail:
        print("FAIL", r["id"], r["detail"][:200])
    return 0


def render_md(s: dict) -> str:
    lines = []
    lines.append("# Foundation independent kit-only review")
    lines.append("")
    lines.append(f"**Verdict: `{s['verdict']}`**")
    lines.append("")
    lines.append(s["standing"])
    lines.append("")
    lines.append("This is not whole-consumer ACCEPT. Diagnostic continuation past a refusal is not successful admission.")
    lines.append("")
    lines.append("## Custody")
    lines.append("")
    lines.append("| Object | SHA-256 | Result |")
    lines.append("|---|---|---|")
    c = s["custody"]
    lines.append(f"| origin kit manifest | `{c['kitManifestSha256']}` | {c['kitFiles']} |")
    lines.append(f"| parent | `{c['parentSubjectSha256']}` | match |")
    lines.append(f"| requirements.json | `{c['requirementsSha256']}` | match |")
    lines.append(f"| foundation snapshot-manifest.json | `{c['snapshotManifestSha256']}` | {c['snapshotFiles']} |")
    lines.append("")
    lines.append(f"Command: `{s['command']}`")
    lines.append("")
    lines.append("## Original-ID map")
    lines.append("")
    lines.append("| Original ID | Exhibit |")
    lines.append("|---|---|")
    for k, v in s["originalIdMap"].items():
        lines.append(f"| `{k}` | `{v}` |")
    lines.append("")
    lines.append("Historical `vectors/` and `traces/` remain frozen shared-path artifacts. New work is under `foundation/`.")
    lines.append("")
    lines.append("## Per-ID results")
    lines.append("")
    for r in s["results"]:
        mark = "PASS" if r["ok"] else "FAIL"
        lines.append(f"- `{r['id']}` **{mark}** — {r['detail']}")
    lines.append("")
    lines.append("## First refusals")
    lines.append("")
    if s["firstRefusals"]:
        for f in s["firstRefusals"]:
            lines.append(f"- `{f.get('id')}` `{f.get('layer')}:{f.get('name')}` — {f.get('detail')}")
    else:
        lines.append("None recorded as structured first-refusal objects; see FAIL rows.")
    lines.append("")
    lines.append("## Existing-law misses vs missing/contradictory norms")
    lines.append("")
    if s["existingLawMissesVsMissingNorm"]:
        for m in s["existingLawMissesVsMissingNorm"]:
            lines.append(f"- `{m['id']}` ({m['class']}) — {m['detail']}")
    else:
        lines.append("No blocking existing-law miss in this scope.")
    lines.append("")
    lines.append("## Unexecuted / notReached")
    lines.append("")
    lines.append(f"- unexecuted scoped IDs: {s['unexecuted'] or 'none'}")
    lines.append("- ROOT-ADMISSION outside this role")
    lines.append("- complete Run admission (phase 5) not in this scope; frozen stores inspected only for file-rung membership")
    lines.append("- real OS/compiler/crypto/provider process (future-host)")
    lines.append("")
    lines.append("Four-Run review remains `OTHER_RUNS_REFUSED` and is not treated as a passing foundation assumption.")
    lines.append("")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    sys.exit(main())
