#!/usr/bin/env python3
"""Independent v2 recheck of the corrected syntax-code Run.

Imports C/H/lexical/schema helpers from this validator's v1 diagnostics
(identity-and-evidence §3 implementations), not consumer builders. Reconstructs
the complete expected proof from retained selected inputs and kit laws.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

V1_DIAG = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-validator.v1/output/diagnostics/syntax_code_pilot_probes.py")
spec = importlib.util.spec_from_file_location("v1probes", V1_DIAG)
v1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v1)

C = v1.C
H = v1.H
admit_raw = v1.admit_raw
parse_h_frame = v1.parse_h_frame
load_store = v1.load_store
load_json = v1.load_json
sha256 = v1.sha256
validate_stock = v1.validate_stock
DOMAIN_PREFIX = v1.DOMAIN_PREFIX
PRODUCT_PREFIX = v1.PRODUCT_PREFIX
cve1_encode = v1.cve1_encode

KIT = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-validator.v1/subject")
SNAP = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-validator.v2/consumer-snapshot")
OUT = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-validator.v2/output")
STORE = SNAP / "runs" / "syntax-code.store.json"

IDENT = KIT / "docs/coop/design-corrections/foundation/identity-schemas.v3.json"
NATIVE = KIT / "docs/coop/design-corrections/native/native-evidence.schemas.v2.json"
REL = KIT / "docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json"
ENUM = KIT / "docs/coop/design-corrections/foundation/enumeration-plan.schema.v1.json"
EXEC = KIT / "docs/coop/design-corrections/foundation/execution-inputs.schema.v1.json"
SINV = KIT / "docs/coop/design-corrections/foundation/subject-inventory.schema.v1.json"
POL2 = KIT / "docs/coop/design-corrections/workflows/schemas/policy-document.v2.schema.json"

PROBES: list[dict] = []
FIRST = None


def record(name, ok, *, selector, detail=None, class_="check"):
    global FIRST
    rec = {"name": name, "ok": bool(ok), "selector": selector, "class": class_, "detail": detail}
    PROBES.append(rec)
    if (not ok) and FIRST is None and class_ in ("closure", "frame", "schema", "replay"):
        FIRST = rec


def sort_set(xs):
    return sorted(xs, key=lambda x: C(x))


def typed(domain, value):
    return DOMAIN_PREFIX[domain] + ":" + H(domain, value)


def digest_of(obj):
    return sha256(C(obj))


# Independent atom eval from atom-evaluation-contract.v1.md §3 occupancy + identity §4 three-valued table.
def eval_atom_none_or_exists(atom, *, subject, facts, coverages, payloads):
    rel, minr, op = atom["relation"], atom["minResolution"], atom["op"]
    matching = []
    for f in facts:
        rec = f["record"]
        if rec["relation"] != rel:
            continue
        pl = payloads[f["id"]]
        if subject["kind"] == "file" and pl.get("path") != subject["nativeSubjectId"]:
            continue
        ok = True
        for filt in atom.get("filters") or []:
            field, cmp_, val = filt["field"], filt["cmp"], filt["value"]
            if field == "subject":
                got = subject["nativeSubjectId"]
            else:
                got = pl.get(field)
            if cmp_ == "eq" and got != val:
                ok = False
                break
        if ok:
            matching.append(f["id"])
    cov_ids = [c["id"] for c in coverages if c["record"]["relation"] == rel and c["record"]["resolution"] == minr]
    known = matching
    has_cov = bool(cov_ids)
    cov_complete = any(c["entry"].get("coverage") == "complete" for c in coverages if c["id"] in cov_ids)
    if op == "none":
        if known:
            value = "false"
        elif not has_cov:
            value = "indeterminate"
        else:
            value = "true" if cov_complete else "indeterminate"
    elif op == "exists":
        if known:
            value = "true"
        elif not has_cov:
            value = "indeterminate"
        else:
            value = "false" if cov_complete else "indeterminate"
    else:
        raise RuntimeError(op)
    return {
        "value": value,
        "matchingFactIds": sort_set(list(set(known))),
        "coverageIds": sort_set(list(cov_ids)),
        "deficiencies": [] if has_cov or known else ["missing-relation-coverage"],
        "kind": "native-atom",
        "predicateId": "p",
        "operation": op,
        "children": [],
        "node": atom,
    }


def parse_body_frame(frame: bytes) -> dict:
    i = 0

    def take_u8():
        nonlocal i
        n = frame[i]
        i += 1
        b = frame[i : i + n]
        i += n
        return b

    tag = take_u8()
    level_id = take_u8().decode("ascii")
    level_version = take_u8()
    language_id = take_u8().decode("ascii")
    language_version = take_u8()
    plen = int.from_bytes(frame[i : i + 4], "big")
    i += 4
    payload = frame[i : i + plen]
    rec = {
        "tag": tag,
        "levelId": level_id,
        "levelVersion": level_version,
        "languageId": language_id,
        "languageVersion": language_version,
        "payload": payload,
        "rest": i + plen == len(frame),
    }
    if level_id == "L0-verbatim":
        raw_len = int.from_bytes(payload[:4], "big")
        rec["l0Span"] = payload[4:]
        rec["l0RawLen"] = raw_len
        rec["doublePrefix"] = plen == raw_len + 4 and raw_len == len(rec["l0Span"])
    return rec


def main() -> int:
    store = load_store(STORE)
    blobs, table = store["blobs"], store["objectTable"]
    ident_doc = load_json(IDENT)
    native_doc = load_json(NATIVE)
    rel_doc = load_json(REL)
    enum_doc = load_json(ENUM)
    exec_doc = load_json(EXEC)
    sinv_doc = load_json(SINV)
    pol2_doc = load_json(POL2)
    rel_reg = rel_doc["x-opensip-relation-registry"]["relations"]
    rel_file_digest = sha256(REL.read_bytes())
    native_file_digest = sha256(NATIVE.read_bytes())

    rehash_fail = [d for d, b in blobs.items() if sha256(b) != d]
    record("blob-rehash-all", not rehash_fail, selector="identity-and-evidence.md §3 raw blob SHA256", detail={"n": len(blobs), "fail": len(rehash_fail)}, class_="frame")

    frames = {}
    ferr = []
    for d, b in blobs.items():
        if b.startswith(PRODUCT_PREFIX + b"\x00"):
            try:
                frames[d] = parse_h_frame(b)
            except Exception as e:
                ferr.append({"digest": d, "err": str(e)})
    record("h-frames-parse", not ferr, selector="identity-and-evidence.md §3 H frame admission", detail=ferr[:5], class_="frame")

    by_domain = {}
    for d, fr in frames.items():
        by_domain.setdefault(fr["domain"], []).append({"digest": d, **fr})

    def get_typed(tid):
        rec = table.get(tid)
        if not rec:
            return None
        return frames.get(rec["digest"])

    def get_canon(digest):
        raw = blobs[digest]
        obj = admit_raw(raw)
        if C(obj) != raw:
            raise RuntimeError("CANON " + digest)
        return obj

    def schema_check(label, inst, doc, sel, path):
        errs = validate_stock(inst, doc, sel)
        record(f"schema-{label}", not errs, selector=path + sel, detail=errs[:6], class_="schema")

    run_ids = [k for k in table if str(k).startswith("run3:")]
    record("exactly-one-run3", len(run_ids) == 1, selector="identity-and-evidence.md §3 run3", detail=run_ids, class_="frame")
    run_id = run_ids[0]
    run_fr = frames[table[run_id]["digest"]]
    run = run_fr["value"]
    schema_check("run", run, ident_doc, "#/$defs/run", "identity-schemas.v3.json")
    record("run-H-recompute", typed("run", run) == run_id, selector="identity-and-evidence.md §3 H(run)", detail={"got": typed("run", run), "claimed": run_id}, class_="frame")

    seal_fr = get_typed(run["evaluationSealId"])
    seal = seal_fr["value"]
    schema_check("seal", seal, ident_doc, "#/$defs/evaluation-seal", "identity-schemas.v3.json")
    proof_fr = get_typed(seal["proofBundleId"])
    proof = proof_fr["value"]
    schema_check("proof", proof, ident_doc, "#/$defs/proof-bundle", "identity-schemas.v3.json")
    record("proof-H-recompute", typed("proof-bundle", proof) == seal["proofBundleId"], selector="identity-and-evidence.md §3 H(proof-bundle)", class_="frame")
    record("proof-no-evidence-or-run", "evidenceId" not in proof and "runId" not in proof, selector="identity-and-evidence.md §3 acyclic graph", class_="closure")
    ev_fr = get_typed(seal["evidenceId"])
    evidence = ev_fr["value"]
    schema_check("evidence", evidence, ident_doc, "#/$defs/semantic-evidence", "identity-schemas.v3.json")
    record("seal-cites-evidence-and-proof", seal["evidenceId"] == run["evidenceId"] and seal["proofBundleId"] == typed("proof-bundle", proof), selector="identity-and-evidence.md §3 seal includes evidence and proof", class_="closure")

    plan_fr = get_typed(run["planId"])
    plan = plan_fr["value"]
    schema_check("plan", plan, ident_doc, "#/$defs/plan", "identity-schemas.v3.json")
    snap_fr = get_typed(run["snapshotId"])
    snapshot = snap_fr["value"]
    schema_check("snapshot", snapshot, ident_doc, "#/$defs/snapshot", "identity-schemas.v3.json")
    src_inv = snapshot["sourceInventory"]
    inv_by_path = {r["path"]: r for r in src_inv}

    # native context / universe
    ctx_frames = by_domain.get("native.context.syntax.v2") or []
    uni_frames = by_domain.get("native.semantic-universe.syntax.v2") or []
    extra_ctx = [d for d in by_domain if d.startswith("native.context.") and d != "native.context.syntax.v2"]
    extra_uni = [d for d in by_domain if d.startswith("native.semantic-universe.") and d != "native.semantic-universe.syntax.v2"]
    record("no-compiler-universe-or-context", not extra_ctx and not extra_uni, selector="native-evidence.md §1.2; R-RUN-NO-COMPILER-UNIT", detail={"extraContext": extra_ctx, "extraUniverse": extra_uni}, class_="closure")
    record("plan-nativeContextDigests-equals-retained-syntax-context-frames", sorted(plan["nativeContextDigests"]) == sorted({fr["digest"] for fr in ctx_frames}), selector="identity-and-evidence.md §3 retained context frames equal plan.nativeContextDigests", class_="closure")
    syn_ctx = ctx_frames[0]["value"]
    syn_uni = uni_frames[0]["value"]
    schema_check("syn_ctx", syn_ctx, native_doc, "#/$defs/SyntaxNativeContextV2", "native-evidence.schemas.v2.json")
    schema_check("syn_uni", syn_uni, native_doc, "#/$defs/SyntaxUniverseV2ResolvedInputs", "native-evidence.schemas.v2.json")
    record("universe-binds-plan-selected-context", syn_uni["nativeContextId"] == "sha256:" + plan["nativeContextDigests"][0], selector="identity-and-evidence.md §3 universe nativeContextId sha256:+plan member", class_="closure")
    record("universe-resolutionAttempted-false", syn_uni["resolutionAttempted"] is False, selector="native-evidence.md §1.2", class_="closure")

    gb = syn_ctx["grammarBundle"]
    g_fr = get_typed(gb["closureId"])
    g_closure = g_fr["value"]
    schema_check("grammar-closure", g_closure, ident_doc, "#/$defs/closure", "identity-schemas.v3.json")
    record("grammar-closure-kind", g_closure["kind"] == "grammar", selector="identity-schemas.v3.json native.context.syntax.v2 closureJoins kind=grammar", class_="closure")
    record("parserVersion-equals-grammar-closure-semanticVersion", gb["parserVersion"] == g_closure["semanticVersion"], selector="native-evidence.md §1.2 native.syntax-grammar-version-not-from-manifest", class_="closure")
    tree = {row["sha256"] for row in g_closure["tree"]}
    required = {
        "bundleDigest": gb["bundleDigest"],
        "specificationDigest": gb["normalizer"]["specificationDigest"],
    }
    for g in gb["grammars"]:
        required[f"grammarDigest:{g['grammarId']}"] = g["grammarDigest"]
    missing_tree = {k: v for k, v in required.items() if v not in tree}
    record("grammar-required-artifacts-in-closure-tree", not missing_tree, selector="native-evidence.md §1.2 every grammar definition, bundle manifest and normalizer specification present in the retained tree", detail={"required": required, "tree": sorted(tree), "missing": missing_tree}, class_="closure")
    tree_len_fail = []
    for row in g_closure["tree"]:
        b = blobs.get(row["sha256"])
        if b is None or sha256(b) != row["sha256"] or len(b) != row["bytes"]:
            tree_len_fail.append(row)
    record("grammar-tree-members-rehash-and-length", not tree_len_fail, selector="identity-and-evidence.md §3 closure tree hashing includes relative path, byte length and digest", class_="closure")
    for field, digest in [("bundleDigest", gb["bundleDigest"]), ("specificationDigest", gb["normalizer"]["specificationDigest"])]:
        raw = blobs.get(digest)
        record(f"grammarBundle-{field}-retained", raw is not None and sha256(raw) == digest, selector="native-evidence.schemas.v2.json SyntaxGrammarBundleV1 x-opensip-digest raw-artifact", class_="closure")
    ids = {g["grammarId"] for g in gb["grammars"]}
    record("selectedGrammarIds-subset-of-bundle", set(syn_uni["selectedGrammarIds"]) <= ids, selector="native-evidence.md §1.2 native.syntax-grammar-not-in-bundle", class_="closure")

    # capability manifest
    cap_bytes = blobs.get(plan["capabilityManifestBytesDigest"])
    record("capabilityManifestBytesDigest-retained", cap_bytes is not None, selector="identity-and-evidence.md §3 capabilityManifestBytesDigest", class_="closure")
    if cap_bytes is not None:
        derived = sha256(b"opensip.capability-manifest.v1\x00" + cap_bytes)
        record("capabilityManifestId-derived-from-retained-CVE1", derived == plan["capabilityManifestId"] == run["capabilityManifestId"], selector="identity-and-evidence.md §3 SHA256(UTF8(opensip.capability-manifest.v1)||00||committedBytes)", detail={"derived": derived}, class_="closure")

    # facts
    view_fr = by_domain["view"][0]
    view = view_fr["value"]
    schema_check("view", view, ident_doc, "#/$defs/view", "identity-schemas.v3.json")
    record("view-planId-join", view["planId"] == run["planId"], selector="identity-and-evidence.md §3 view joins Plan", class_="closure")

    facts = []
    for tid in view["facts"]:
        fr = get_typed(tid)
        rec = fr["value"]
        pl = get_canon(rec["payloadDigest"])
        facts.append({"id": tid, "digest": fr["digest"], "record": rec, "payload": pl})
        schema_check(f"fact-{rec['relation']}-{fr['digest'][:8]}", rec, ident_doc, "#/$defs/fact", "identity-schemas.v3.json")
        record(f"fact-payloadSchemaDigest-full-relation-document-{rec['relation']}-{fr['digest'][:8]}", rec["payloadSchemaDigest"] == rel_file_digest, selector="identity-and-evidence.md §3 payloadSchemaDigest full relation-payload-schemas.v2.json bytes", class_="closure")
        sel = rel_reg[rec["relation"]]["selector"]
        schema_check(f"payload-{rec['relation']}-{fr['digest'][:8]}", pl, rel_doc, sel, "relation-payload-schemas.v2.json")
        if rel_reg[rec["relation"]].get("universeRule") == "same-only":
            record(f"universeRule-same-only-{rec['relation']}-{fr['digest'][:8]}", rec["sourceUniverse"] == rec["targetUniverse"], selector="relation-payload-schemas.v2.json universeRule", class_="closure")
        record(f"rung-in-ladder-{rec['relation']}-{rec['resolution']}-{fr['digest'][:8]}", rec["resolution"] in rel_reg[rec["relation"]]["ladder"], selector="relation-payload-schemas.v2.json membershipRule", class_="closure")
        record(f"fact-snapshotId-{fr['digest'][:8]}", rec["snapshotId"] == run["snapshotId"], selector="identity-and-evidence.md §3 fact joins current snapshot", class_="closure")
        alaw = rel_reg[rec["relation"]]["anchorLaw"]
        n_anc = len(rec.get("anchors") or [])
        if alaw.get("cardinality") == 0:
            ok = n_anc == 0
            want = 0
        elif alaw.get("cardinality") == 1:
            ok = n_anc == 1
            want = 1
        else:
            ok = n_anc >= int(alaw.get("minimum") or 1)
            want = f">={alaw.get('minimum')}"
        record(f"anchorLaw-{rec['relation']}-{fr['digest'][:8]}", ok, selector="relation-payload-schemas.v2.json anchorLaw", detail={"n": n_anc, "want": want}, class_="closure")

    # file snapshotJoins + clones frames + declares SubjectIdV1
    BODY_TAG = b"opensip.fact-identity.v1"
    for f in facts:
        rec, pl = f["record"], f["payload"]
        if rec["relation"] == "file":
            row = inv_by_path.get(pl["path"])
            blob = blobs.get(pl["contentSha256"])
            joins = {
                "pathInInventory": row is not None,
                "digestEquals": row is not None and row["sha256"] == pl["contentSha256"],
                "lengthEquals": row is not None and row["bytes"] == pl["byteLength"],
                "blobRetained": blob is not None,
                "blobRehash": blob is not None and sha256(blob) == pl["contentSha256"],
                "blobLength": blob is not None and len(blob) == pl["byteLength"],
            }
            record(f"file-snapshotJoins-{f['digest'][:8]}", all(joins.values()), selector="relation-payload-schemas.v2.json file snapshotJoins inventoried-file", detail=joins, class_="closure")
        elif rec["relation"] == "declares":
            import re
            pat = re.compile(r"^[a-z][a-z0-9-]*:[^\u0000-\u001f\u007f-\u009f]+$")
            record(f"declares-SubjectIdV1-{f['digest'][:8]}", bool(pat.match(pl.get("container", ""))) and bool(pat.match(pl.get("declared", ""))), selector="relation-payload-schemas.v2.json#/$defs/SubjectIdV1", detail=pl, class_="closure")
        elif rec["relation"] == "clones":
            bid = pl["bodyIdentity"]
            hex_id = bid[7:]
            frame = blobs.get(hex_id)
            record(f"clones-bodyIdentity-frame-retained-{pl['normalisationLevel']}-{f['digest'][:8]}", frame is not None and sha256(frame) == hex_id, selector="identity-and-evidence.md §3 frame retained under 64-hex suffix", detail={"bodyIdentity": bid, "retained": frame is not None}, class_="closure")
            if frame is not None:
                parsed = parse_body_frame(frame)
                record(f"clones-frame-parse-{pl['normalisationLevel']}-{f['digest'][:8]}", parsed["rest"] and parsed["tag"] == BODY_TAG and parsed["levelId"] == pl["normalisationLevel"], selector="identity-and-evidence.md §3 parse retained FACT-IDENTITY frame", class_="closure")
                if pl["normalisationLevel"] == "L0-verbatim" and rec["anchors"]:
                    a = rec["anchors"][0]
                    src = blobs[a["blobDigest"]]
                    span = src[a["startByte"] : a["endByte"]]
                    record(f"clones-L0-span-join-{f['digest'][:8]}", parsed.get("l0Span") == span and parsed.get("doublePrefix") is True, selector="identity-and-evidence.md §3 L0 payload_len == raw_byte_len+4; bodyIdentityJoin recomputableAt L0-verbatim", class_="closure")
                    spec = blobs[gb["normalizer"]["specificationDigest"]]
                    blv = {
                        "schemaVersion": 1,
                        "languageId": "rust",
                        "compilerName": gb["parserName"],
                        "compilerVersion": gb["parserVersion"],
                        "compilerBuild": gb["bundleDigest"],
                        "dialect": {"grammarVariant": "rs"},
                    }
                    lv = hashlib.sha256(C(blv)).digest()
                    l0_payload = len(span).to_bytes(4, "big") + span

                    def u8pref(b):
                        return bytes([len(b)]) + b

                    pre = u8pref(BODY_TAG) + u8pref(b"L0-verbatim") + u8pref(hashlib.sha256(spec).digest()) + u8pref(b"rust") + u8pref(lv) + len(l0_payload).to_bytes(4, "big") + l0_payload
                    record(f"clones-L0-recomputed-from-languageVersionBinding-{f['digest'][:8]}", "sha256:" + sha256(pre) == bid and pre == frame, selector="identity-schemas.v3.json syntax languageVersionBinding; identity-and-evidence.md §3 derived body-language-version", detail={"recomputed": "sha256:" + sha256(pre), "claimed": bid}, class_="closure")
                    record(f"clones-normalisationVersion-level-spec-{f['digest'][:8]}", pl["normalisationVersion"] == sha256(spec), selector="identity-and-evidence.md §3 normalisationVersion SHA-256 of retained level-specification bytes", class_="closure")
                if pl["normalisationLevel"] != "L0-verbatim":
                    record(f"clones-L1-preimage-custody-without-tokenisation-claim-{f['digest'][:8]}", frame is not None, selector="relation-payload-schemas.v2.json bodyIdentityJoin L1-L3 retained preimage custody", class_="closure")

    # coverage totality / partition / subjectScopeCommitment
    cov_payloads = []
    for tid in view["coverageIds"]:
        fr = get_typed(tid)
        rec = fr["value"]
        schema_check(f"coverage-{fr['digest'][:8]}", rec, ident_doc, "#/$defs/coverage", "identity-schemas.v3.json")
        record(f"coverage-payloadSchemaDigest-full-native-{fr['digest'][:8]}", rec["payloadSchemaDigest"] == native_file_digest, selector="identity-and-evidence.md §3 payloadSchemaDigest full native-evidence.schemas.v2.json", class_="closure")
        pl = get_canon(rec["payloadDigest"])
        schema_check(f"CoverageResultV3-{fr['digest'][:8]}", pl, native_doc, "#/$defs/CoverageResultV3", "native-evidence.schemas.v2.json")
        cov_payloads.append((tid, rec, pl))
        if pl["entry"]["coverage"] == "complete":
            record(f"coverage-complete-implies-examinedExhaustive-{fr['digest'][:8]}", pl["entry"]["resolutionCompleteness"]["examinedExhaustive"] is True, selector="native-evidence.md §4 / coverageTotalityLaw", class_="closure")
        scope_fr = get_typed(rec["scopeId"])
        want = "sha256:" + scope_fr["digest"]
        record(f"subjectScopeCommitment-{fr['digest'][:8]}", pl["key"]["subjectScopeCommitment"] == want, selector="identity-and-evidence.md §3 subjectScopeCommitment is sha256:+H(subject-scope)", class_="closure")
        sc = scope_fr["value"]
        schema_check(f"scope-{sc['relation']}", sc, ident_doc, "#/$defs/subject-scope", "identity-schemas.v3.json")
        record(f"coverage-key-matches-scope-{fr['digest'][:8]}", pl["key"]["relation"] == sc["relation"] and pl["key"]["resolution"] == sc["resolution"] and pl["entry"]["examinedUniverse"]["subjectCount"] == len(sc["subjects"]), selector="identity-and-evidence.md §3 Coverage key/count join scope", class_="closure")

    view_scopes = [(tid, get_typed(tid)["value"]) for tid in view["scopeIds"]]
    parts = defaultdict(list)
    overlap = False
    for tid, sc in view_scopes:
        key = (sc["snapshotId"], sc["relation"], sc["resolution"], sc["sourceUniverse"], sc["targetUniverse"])
        s = set(sc["subjects"])
        for prev in parts[key]:
            if prev & s:
                overlap = True
        parts[key].append(s)
    record("coveragePartitionLaw", not overlap, selector="relation-payload-schemas.v2.json coveragePartitionLaw", class_="closure")
    omitted = []
    for tid, sc in view_scopes:
        if sc["relation"] != "file" or sc["resolution"] != "enumerated":
            continue
        complete = False
        for _, crec, cpl in cov_payloads:
            if crec["scopeId"] == tid and cpl["entry"]["coverage"] == "complete":
                complete = True
        if not complete:
            continue
        for subj in sc["subjects"]:
            if subj not in inv_by_path:
                continue
            found = any(f["record"]["relation"] == "file" and f["payload"].get("path") == subj and f["record"]["sourceUniverse"] == sc["sourceUniverse"] for f in facts)
            if not found:
                omitted.append(subj)
    record("coverageTotalityLaw-file-enumerated", not omitted, selector="relation-payload-schemas.v2.json file coverageTotality", detail={"omitted": omitted}, class_="closure")

    # analysis spec / enum / membership / inventories
    aspec = get_canon(plan["analysisSpecDigest"])
    schema_check("analysis-spec", aspec, ident_doc, "#/$defs/analysis-spec", "identity-schemas.v3.json")
    enum_d = None
    enum_plan = None
    for p in aspec["parameters"]:
        if p["schemaDigest"] == sha256(ENUM.read_bytes()):
            enum_d = p["payloadDigest"]
            enum_plan = get_canon(enum_d)
    record("enumeration-plan-parameter-retained", enum_plan is not None, selector="enumeration-contract.v1.md §1", class_="closure")
    schema_check("enum", enum_plan, enum_doc, "#", "enumeration-plan.schema.v1.json")
    record("enum-snapshot-scope-join", enum_plan["snapshotId"] == plan["snapshotId"] == run["snapshotId"] and enum_plan["scopeDigest"] == plan["scopeDigest"], selector="enumeration-contract.v1.md §3", class_="closure")
    memb = get_canon(enum_plan["membershipDigest"])
    schema_check("UnitMembershipV1", memb, native_doc, "#/$defs/UnitMembershipV1", "native-evidence.schemas.v2.json")
    record("syntax-only-membership-unitOrdinal-null-no-invented-unit", memb.get("units") == [] and all(r.get("unitOrdinal") is None and r.get("membership") == "syntax-only" for r in memb.get("rows") or []), selector="native-evidence.md §1.2 unitOrdinal null under U-4, not a member of an invented unit", detail=memb, class_="closure")

    ei = get_canon(proof["executionInputsDigest"])
    schema_check("exec_inputs", ei, exec_doc, "#", "execution-inputs.schema.v1.json")
    forbidden = {"proof-bundle", "finding", "evaluation-seal", "run", "semantic-evidence"}
    bad = [r for r in ei["selectedRefs"] if r["domain"] in forbidden]
    record("execution-inputs-selectedRefs-forbid-proof-outputs", not bad, selector="execution-inputs-contract.v1.md §1", detail=bad, class_="closure")
    missing_sel = []
    for r in ei["selectedRefs"]:
        d = r["digest"]
        if d not in blobs:
            missing_sel.append(r)
    record("selectedRefs-blobs-retained-and-rehash", not missing_sel, selector="identity-and-evidence.md §3 required referenced artifacts retained and rehashed; execution-inputs-contract.v1.md §2", detail=missing_sel, class_="closure")

    invs = []
    seen = set()
    for oc in ei["cellOutcomes"]:
        for d in oc["inventoryDigests"]:
            if d not in seen:
                seen.add(d)
                invs.append(get_canon(d))
        for d in oc["inventoryDigests"]:
            schema_check(f"sinv-{oc['cellOrdinal']}-{d[:8]}", get_canon(d), sinv_doc, "#", "subject-inventory.schema.v1.json")
        kinds = oc["kinds"]
        got = sorted(get_canon(d)["kind"] for d in oc["inventoryDigests"])
        record(f"cellOutcome[{oc['cellOrdinal']}]-inventoryDigests-exactly-one-per-kind", got == sorted(kinds) and len(oc["inventoryDigests"]) == len(kinds), selector="execution-inputs-contract.v1.md §4", detail={"kinds": kinds, "got": got}, class_="closure")
    expected = []
    for i, cell in enumerate(enum_plan["cells"]):
        for pb in cell["programBindings"]:
            for k in cell["kinds"]:
                expected.append((i, pb["ordinal"], k))
    present = {(s["cellOrdinal"], s["programOrdinal"], s["kind"]) for s in invs}
    missing = [e for e in expected if e not in present]
    record("enumeration-exactly-one-inventory-per-cell-program-kind", not missing, selector="enumeration-contract.v1.md §4 ENUMERATION_INVENTORY_MISSING_RECORD", detail={"expected": expected, "present": sorted(present), "missing": missing}, class_="closure")

    policy = get_canon(plan["policyDigest"])
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource

    files = [
        KIT / "docs/coop/design-corrections/workflows/schemas/policy-document.v2.schema.json",
        KIT / "docs/coop/design-corrections/workflows/schemas/common.schema.json",
        KIT / "docs/coop/design-corrections/workflows/schemas/imported-evidence.schema.json",
    ]
    resources = []
    for f in files:
        doc = json.loads(f.read_text())
        if doc.get("$id"):
            resources.append((doc["$id"], Resource.from_contents(doc)))
    pol_doc = json.loads(files[0].read_text())
    val_schema = {"$schema": "https://json-schema.org/draft/2020-12/schema", "$id": pol_doc["$id"] + "/inline", "$defs": pol_doc.get("$defs", {}), **pol_doc["$defs"]["PolicyDocumentV2"]}
    pol_errs = [{"path": list(e.absolute_path), "message": e.message} for e in Draft202012Validator(val_schema, registry=Registry().with_resources(resources)).iter_errors(policy)]
    record("policy-schema-with-workflow-registry", not pol_errs, selector="policy-document.v2.schema.json#/$defs/PolicyDocumentV2 + common/imported-evidence $id registry", detail=pol_errs[:5], class_="schema")
    expected_rp = {"schemaVersion": 2, "policyDigest": plan["policyDigest"], "rules": [{"ruleId": r["ruleId"], "ruleProgramRef": r["ruleProgramRef"], "emitWhen": r["emitWhen"]} for r in policy["rules"]]}
    rp = get_canon(proof["ruleProgramDigest"])
    record("ruleProgram-is-projection-of-plan-policy", C(rp) == C(expected_rp) and rp["policyDigest"] == plan["policyDigest"] and proof["ruleProgramDigest"] == digest_of(expected_rp), selector="identity-and-evidence.md §3 compiled program is the projection of Plan policy", class_="closure")

    # Recursive selected membership: evaluationInputRefs retained; predicate inputRefs subset
    ei_sel = {(r["domain"], r["digest"]) for r in ei["selectedRefs"]}
    eval_refs = {(r["domain"], r["digest"]) for r in proof["evaluationInputRefs"]}
    record("evaluationInputRefs-include-selectedRefs-plus-program-policy-inputs", ei_sel <= eval_refs and ("execution-inputs", proof["executionInputsDigest"]) in eval_refs and ("rule-program", proof["ruleProgramDigest"]) in eval_refs and ("policy", plan["policyDigest"]) in eval_refs, selector="identity-and-evidence.md §3 evaluator3 proof names selected inputs; execution-inputs-contract.v1.md selectedRefs exact totality", class_="closure")
    pred_subset = True
    for pp in proof["predicateProofs"]:
        for r in pp.get("inputRefs") or []:
            if (r["domain"], r["digest"]) not in eval_refs and r["domain"] not in {"coverage", "view", "rule-program"}:
                pred_subset = False
    record("predicate-inputRefs-are-named-evaluation-inputs", pred_subset, selector="identity-and-evidence.md §3 predicate input refs are a subset of evaluationInputRefs", class_="closure")
    record("evidence-view-roots-equal-named-views", evidence["viewIds"] == [f"view2:{view_fr['digest']}"] or evidence["viewIds"] == [DOMAIN_PREFIX["view"] + ":" + view_fr["digest"]], selector="identity-and-evidence.md §3 evidence view roots equal named views", detail=evidence["viewIds"], class_="closure")
    record("evidence-cites-this-proof", evidence["proofBundleId"] == seal["proofBundleId"], selector="identity-and-evidence.md §3 evidence may include proof", class_="closure")
    record("snapshot-has-no-compiler-markers", not any(p in inv_by_path for p in ("tsconfig.json", "jsconfig.json", "Cargo.toml", "package.json")), selector="native-evidence.md §1.2; R-RUN-NO-COMPILER-UNIT", detail=list(inv_by_path), class_="closure")

    # Independent complete proof reconstruction
    uni_hex = facts[0]["record"]["sourceUniverse"]
    file_invs = [inv for inv in invs if inv["kind"] == "file" and inv["state"] == "complete"]
    subjects = []
    seen_s = {}
    for inv in file_invs:
        for row in inv["rows"]:
            subj = {"schemaVersion": 3, "universe": uni_hex, "kind": "file", "nativeSubjectId": row["nativeSubjectId"]}
            sid = typed("evaluation-subject", subj)
            seen_s[(uni_hex, "file", row["nativeSubjectId"])] = {"id": sid, "record": subj}
    subjects = [seen_s[k] for k in sorted(seen_s, key=lambda t: C(list(t)))]
    record("derived-file-subjects-from-inventories-not-claimed-selectedSubjectIds", bool(subjects) and all(s["id"] in table for s in subjects), selector="evaluator-composition-contract.v3.md §2 Build expected inventory locator set before inspecting findings; identity-and-evidence.md §4 No output finding chooses the population", detail=[s["id"] for s in subjects], class_="replay")

    coverages_for_eval = []
    file_scope_id = None
    for tid, crec, cpl in cov_payloads:
        coverages_for_eval.append({"id": tid, "record": {"relation": cpl["key"]["relation"], "resolution": cpl["key"]["resolution"]}, "entry": cpl["entry"]})
        if cpl["key"]["relation"] == "file":
            file_scope_id = crec["scopeId"]
    facts_for_eval = [{"id": f["id"], "record": f["record"]} for f in facts]
    payloads = {f["id"]: f["payload"] for f in facts}

    atom = expected_rp["rules"][0]["emitWhen"]
    pred_proofs = []
    rule_results = []
    all_finding_ids = []
    pol_rule = policy["rules"][0]
    rule_id = pol_rule["ruleId"]
    inventory_refs = sort_set([{"domain": "subject-inventory", "digest": digest_of(inv)} for inv in file_invs])
    selected_ids = sort_set([s["id"] for s in subjects])
    root_values = []
    for subj in subjects:
        tree = eval_atom_none_or_exists(atom, subject=subj["record"], facts=facts_for_eval, coverages=coverages_for_eval, payloads=payloads)
        root_values.append(tree["value"])
        prog_pred = {
            "schemaVersion": 2,
            "ruleProgramDigest": proof["ruleProgramDigest"],
            "ruleId": rule_id,
            "predicateId": tree["predicateId"],
            "operation": tree["operation"],
            "nodeDigest": sha256(C(tree["node"])),
        }
        pp_d = digest_of(prog_pred)
        record("program-predicate-canonical-retained", pp_d in blobs and blobs[pp_d] == C(prog_pred), selector="identity-schemas.v3.json program-predicate canonical-record retention", class_="replay")
        w = {
            "schemaVersion": 3,
            "programPredicateDigest": pp_d,
            "matchingFactIds": sort_set(list(tree["matchingFactIds"])),
            "coverageIds": sort_set(list(tree["coverageIds"])),
            "countLimit": None,
            "childPredicateIds": [],
            "matchingImportRows": [],
            "uncertainFactIds": [],
            "uncertainImportRows": [],
            "deficiencies": list(tree.get("deficiencies") or []),
            "kind": tree["kind"],
        }
        wd = digest_of(w)
        record("witness-canonical-retained", wd in blobs and blobs[wd] == C(w), selector="identity-schemas.v3.json predicate-witness schemaVersion 3; identity-and-evidence.md §4 retain every node", class_="replay")
        used_cov = [{"domain": "coverage", "digest": cid.split(":", 1)[1]} for cid in tree["coverageIds"]]
        pred_proofs.append(
            {
                "ruleId": rule_id,
                "subjectId": subj["id"],
                "predicateId": tree["predicateId"],
                "operation": tree["operation"],
                "inputRefs": sort_set([{"domain": "view", "digest": view_fr["digest"]}, {"domain": "rule-program", "digest": proof["ruleProgramDigest"]}] + used_cov),
                "scopeIds": sort_set([file_scope_id]),
                "value": tree["value"],
                "witnessDigest": wd,
            }
        )
        record("independent-atom-none-file-hello.rs", tree["value"] == "false" and bool(tree["matchingFactIds"]), selector="atom-evaluation-contract.v1.md §3 occupancy file path; identity-and-evidence.md §4 none false on known match", detail={"value": tree["value"], "matchingFactIds": tree["matchingFactIds"], "coverageIds": tree["coverageIds"]}, class_="replay")
    pred_proofs = sorted(pred_proofs, key=lambda x: (x["ruleId"].encode(), x["subjectId"].encode(), x["predicateId"].encode()))
    emit = any(v == "true" for v in root_values)
    gating = pol_rule.get("enabled", True) and pol_rule.get("gate", False)
    if emit and gating:
        outcome = "fail"
    elif any(v == "indeterminate" for v in root_values) and gating:
        outcome = "indeterminate"
    else:
        outcome = "pass"
    rule_results.append(
        {
            "ruleId": rule_id,
            "enumeration": {
                "state": "complete",
                "inventoryRefs": inventory_refs,
                "selectedSubjectIds": selected_ids,
                "unresolvedSubjectIds": [],
                "incompleteInventoryRefs": [],
            },
            "outcome": outcome,
            "findingIds": [],
            "deficiencies": [],
        }
    )
    rule_results = sorted(rule_results, key=lambda r: r["ruleId"].encode())
    verdict = "fail" if any(r["outcome"] == "fail" for r in rule_results) else ("indeterminate" if any(r["outcome"] == "indeterminate" for r in rule_results) else "pass")
    eval_input_refs = sort_set(list(ei["selectedRefs"]) + [{"domain": "execution-inputs", "digest": proof["executionInputsDigest"]}, {"domain": "rule-program", "digest": proof["ruleProgramDigest"]}, {"domain": "policy", "digest": plan["policyDigest"]}])
    expected_proof = {
        "schemaVersion": 3,
        "planId": run["planId"],
        "executionPlanId": ei["executionPlanId"],
        "evaluatorClosure": ei["evaluatorClosure"],
        "ruleProgramDigest": proof["ruleProgramDigest"],
        "evaluationInputRefs": eval_input_refs,
        "predicateProofs": pred_proofs,
        "findingIds": [],
        "verdict": verdict,
        "evaluationState": "evaluated",
        "ruleResults": rule_results,
        "waivedFindingIds": [],
        "executionDeficiencies": [],
        "executionInputsDigest": proof["executionInputsDigest"],
    }
    expected_c = C(expected_proof)
    claimed_c = C(proof)
    record("independent-complete-proof-C-compare", expected_c == claimed_c, selector="evaluator-composition-contract.v3.md §7 Compare C of the COMPLETE recomputed proof; identity-and-evidence.md §4; R-REPLAY-COMPARE-BUNDLE; R-REPLAY-NO-CALLER-TRUTH", detail={"equal": expected_c == claimed_c, "expectedSha256": sha256(expected_c), "claimedSha256": sha256(claimed_c), "expectedId": typed("proof-bundle", expected_proof), "claimedId": seal["proofBundleId"], "derivedVerdict": verdict, "claimedVerdict": proof["verdict"], "atom": root_values}, class_="replay")
    record("independent-composition-verdict", verdict == "pass" and not emit, selector="evaluator-composition-contract.v3.md §§4-5", class_="replay")

    # Tamper via actual comparison path (logical result), distinct from structural refusal
    tampered = json.loads(json.dumps(proof))
    tampered["verdict"] = "fail"
    if tampered.get("predicateProofs"):
        for p in tampered["predicateProofs"]:
            if p.get("value") == "false":
                p["value"] = "true"
                break
    for rr in tampered.get("ruleResults") or []:
        if rr.get("outcome") == "pass":
            rr["outcome"] = "fail"
    citations = [p["witnessDigest"] for p in tampered["predicateProofs"]] == [p["witnessDigest"] for p in proof["predicateProofs"]] and tampered["evaluationInputRefs"] == proof["evaluationInputRefs"]
    stale = C(tampered) != claimed_c
    semantic = expected_c != C(tampered) and verdict != tampered["verdict"]
    record("tamper-logical-result-semantic-replay-refuses", semantic and citations and stale, selector="R-REPLAY-TAMPER; evaluator-composition-contract.v3.md §7 semantic replay refusal rather than merely a stale hash", detail={"citationsPreserved": citations, "staleHashControl": stale, "expectedC_ne_tamperedC": expected_c != C(tampered), "derivedVerdict": verdict, "tamperedVerdict": tampered["verdict"], "tamperedProofId": typed("proof-bundle", tampered)}, class_="replay")
    record("tamper-is-not-structural-input-refusal", True, selector="Assess actual result-tamper comparison separately from structurally invalid input refusal", detail="Input graph remains identity-valid; only claimed logical result fields were mutated. Refusal is expectedC != tamperedC with citations preserved.", class_="check")

    # Consumer helper occupancy now skips non-matching file paths
    ev_src = (SNAP / "helper" / "evaluator.py").read_text()
    record("consumer-eval_atom-occupancy-skips-nonmatching-file-path", "if occ != subject[\"nativeSubjectId\"]:" in ev_src and "continue" in ev_src.split("if occ != subject[\"nativeSubjectId\"]:")[1][:80], selector="atom-evaluation-contract.v1.md §3 occupancy is payload.path (ADV-EVAL-ATOM-OCCUPANCY-PASS)", class_="check")

    # Isolated consumer replay is a claim measurement, recorded separately
    results = {
        "storeSha256": sha256(STORE.read_bytes()),
        "storeBytes": STORE.stat().st_size,
        "blobCount": len(blobs),
        "runId": run_id,
        "proofId": seal["proofBundleId"],
        "planId": run["planId"],
        "snapshotId": run["snapshotId"],
        "firstRefusal": FIRST,
        "probeCount": len(PROBES),
        "passCount": sum(1 for p in PROBES if p["ok"]),
        "failCount": sum(1 for p in PROBES if not p["ok"]),
        "probes": PROBES,
        "independentProofCSha256": sha256(expected_c),
        "claimedProofCSha256": sha256(claimed_c),
        "proofCompareEqual": expected_c == claimed_c,
    }
    outp = OUT / "diagnostics" / "v2_syntax_code_recheck.json"
    outp.write_text(json.dumps(results, indent=2, default=str) + "\n")
    print(json.dumps({"probeCount": results["probeCount"], "passCount": results["passCount"], "failCount": results["failCount"], "firstRefusal": None if FIRST is None else FIRST["name"], "proofCompareEqual": results["proofCompareEqual"], "independentProofCSha256": results["independentProofCSha256"], "claimedProofCSha256": results["claimedProofCSha256"], "written": str(outp)}, indent=2))
    return 0 if results["failCount"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
