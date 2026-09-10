#!/usr/bin/env python3
"""Standalone Phase 4 correction of R-COUNT-CLASS-ATTEMPT and R-CODE-VS-DATA-MATRIX.

StandaloneCanonicalVectors, not a new complete Run. Writes only those two
foundation vectors (plus a retained count-class store). Does not remint
five Run stores, traces, or other foundation exhibits.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v12-team-foundation-phase4-corrections.v3/output")
KIT = Path("/tmp/opensip-design-corrections/consumer-b.v12-team-foundation-phase4-corrections.v3/subject")
sys.path.insert(0, str(OUT))

from helper.body_identity import parse_body_identity_frame  # noqa: E402
from helper.canonical import C  # noqa: E402
from helper.graph_seal import IDENT, NATIVE, REL, make_closure, sort_set  # noqa: E402
from helper.identity import DOMAIN_PREFIX, H, h_frame, parse_h_frame, typed_id  # noqa: E402
from helper.lexical import admit_raw  # noqa: E402
from helper.schema_admit import validate_against  # noqa: E402
from helper.store import Store  # noqa: E402

FOUND = OUT / "foundation"
MATRIX = KIT / "docs/coop/design-corrections/native/native-capability-matrix.v2.json"
RESOLVED = {
    ("imports", "resolved-target"),
    ("references", "resolved-binding"),
    ("calls", "resolved-callee"),
    ("types", "checked"),
    ("reachability", "from-resolved-calls"),
}


def die(msg: str) -> None:
    print("PHASE4_ASSERTION_FAILED", msg, file=sys.stderr)
    raise SystemExit(1)


def exhibit(domain: str, rec) -> dict:
    cx = C(rec)
    frame = h_frame(domain, rec)
    parsed = parse_h_frame(frame)
    digest = hashlib.sha256(frame).hexdigest()
    if parsed["digest"] != digest:
        die(f"H mismatch {domain}")
    out = {
        "domain": domain,
        "record": rec,
        "C_hex": cx.hex(),
        "C_sha256": hashlib.sha256(cx).hexdigest(),
        "H": H(domain, rec),
        "frameHex": frame.hex(),
        "frameSha256": digest,
        "frameByteLength": len(frame),
    }
    if domain in DOMAIN_PREFIX:
        out["typedId"] = typed_id(domain, rec)
    return out


def stock(inst, rel, sel, label):
    r = validate_against(inst, rel, selector=sel, label=label)
    if not r["stockOk"]:
        die(f"{label} {r['errors'][:4]}")
    return r


def closed_world():
    return {
        "exportsClosed": "unknown",
        "entryPointsRecognized": "none",
        "nonliteralLoading": "none",
        "externalConsumers": "unknown",
        "dynamicDispatch": "not-applicable",
        "reasons": [],
        "deadCodeRepairEligible": False,
    }


def rc_na():
    return {
        "state": "not-applicable",
        "attempted": False,
        "examinedExhaustive": True,
        "stageTerminal": "complete",
        "unresolvedEdgeCount": 0,
        "unresolvedEdgeClasses": [],
    }


def rc_complete():
    return {
        "state": "complete",
        "attempted": True,
        "examinedExhaustive": True,
        "stageTerminal": "complete",
        "unresolvedEdgeCount": 0,
        "unresolvedEdgeClasses": [],
    }


def rc_incomplete(n, classes):
    return {
        "state": "incomplete",
        "attempted": True,
        "examinedExhaustive": True,
        "stageTerminal": "complete",
        "unresolvedEdgeCount": n,
        "unresolvedEdgeClasses": sorted(classes),
    }


def rc_not_attempted():
    return {
        "state": "not-attempted",
        "attempted": False,
        "examinedExhaustive": True,
        "stageTerminal": None,
        "unresolvedEdgeCount": 0,
        "unresolvedEdgeClasses": [],
    }


def derive_rc(*, ladders, relation, resolution, entry, unresolved_in_examined):
    """RC-0 then RC-1/RC-2 then RC-6 over retained Coverage + unresolved-edge facts."""
    if relation not in ladders or resolution not in ladders[relation]["ladder"]:
        return {"rc0": "unregistered-pair", "ok": False, "refusal": "RC-0"}
    rc0 = "registered-pair"
    rc = entry["resolutionCompleteness"]
    cov = entry["coverage"]
    rc6_ok = not (cov == "complete" and rc["examinedExhaustive"] is False)
    if not rc6_ok:
        return {"rc0": rc0, "rc6": "refuse-complete-without-exhaustive", "ok": False, "refusal": "RC-6"}
    if (relation, resolution) not in RESOLVED:
        expected = {
            "state": "not-applicable",
            "attempted": False,
            "unresolvedEdgeCount": 0,
            "unresolvedEdgeClasses": [],
        }
        ok = (
            rc["state"] == "not-applicable"
            and rc["attempted"] is False
            and rc["unresolvedEdgeCount"] == 0
            and rc["unresolvedEdgeClasses"] == []
        )
        return {"rc0": rc0, "rc1": "not-applicable-rung", "rc6": "hold" if rc6_ok else "n/a", "expected": expected, "observed": {k: rc[k] for k in expected}, "ok": ok}
    # resolved rung: RC-1 forbids not-applicable
    if rc["state"] == "not-applicable":
        return {"rc0": rc0, "rc1": "resolved-rung-must-not-claim-not-applicable", "ok": False, "refusal": "RC-1"}
    n_unres = len(unresolved_in_examined)
    if rc["attempted"] is False:
        expected_state = "not-attempted"
    elif rc["stageTerminal"] != "complete" or rc["examinedExhaustive"] is False:
        expected_state = "partial"
    elif n_unres >= 1 and rc["stageTerminal"] == "complete" and rc["examinedExhaustive"] is True:
        expected_state = "incomplete"
    elif (
        rc["attempted"] is True
        and rc["examinedExhaustive"] is True
        and rc["stageTerminal"] == "complete"
        and n_unres == 0
    ):
        expected_state = "complete"
    else:
        expected_state = "partial"
    # Zero count never implies complete by itself: complete requires the four RC-2 conjuncts.
    ok = rc["state"] == expected_state
    return {
        "rc0": rc0,
        "rc1": "resolved-rung",
        "rc2": expected_state,
        "rc6": "hold",
        "unresolvedEdgeFactsInExaminedSet": n_unres,
        "expectedState": expected_state,
        "observedState": rc["state"],
        "ok": ok,
    }


def main() -> int:
    store = Store()
    ladders = json.loads((KIT / REL).read_text())["x-opensip-relation-registry"]["relations"]
    native_schema_d = store.put_raw((KIT / NATIVE).read_bytes(), label="native-schema")
    rel_schema_d = store.put_raw((KIT / REL).read_bytes(), label="rel-schema")

    a_ts = b"export const a = 1;\n"
    a_d = store.put_raw(a_ts, label="src/a.ts")
    src_inv = sort_set([{"path": "src/a.ts", "sha256": a_d, "bytes": len(a_ts)}])
    inv_d = store.put_canonical(src_inv, label="source-inventory")
    vcs_d = store.put_canonical(
        {"schemaVersion": 2, "kind": "none", "commitId": None, "dirty": False, "sourceInventoryDigest": inv_d},
        label="vcs",
    )
    scope_d = store.put_canonical(
        {"schemaVersion": 2, "workspaceRoots": ["."], "pathPrefixes": [], "excludedPathPrefixes": []},
        label="scope-descriptor",
    )
    cfg_d = store.put_canonical(
        {
            "analysis": {"profileId": "core", "capabilities": ["inventory"], "budget": {"unit": "work-units", "limit": 10000}},
            "components": {},
            "discovery": {},
            "policy": {},
            "evidence": {},
        },
        label="semantic-configuration",
    )
    project_id = "prj1-" + hashlib.sha256(b"consumer-b.v12.phase4-count-class").hexdigest()
    snapshot = {
        "schemaVersion": 2,
        "projectId": project_id,
        "sourceInventory": src_inv,
        "resolvedConfigDigest": cfg_d,
        "scopeDigest": scope_d,
        "vcsDigest": vcs_d,
    }
    stock(snapshot, IDENT, "#/$defs/snapshot", "snapshot")
    snap_h = store.put_h("snapshot", snapshot, label="snapshot")

    prov_c, _ = make_closure(store, "provider")
    bundle_blob = store.put_raw(b"gb", label="gb")
    g_file = store.put_raw(b"ts-g", label="tg")
    spec_d = store.put_raw(b"spec", label="spec")
    g_c, g_rec = make_closure(
        store,
        "grammar",
        extra_files=[
            {"path": "bundle/archive", "sha256": bundle_blob, "bytes": 2},
            {"path": "grammars/typescript.bin", "sha256": g_file, "bytes": 4},
            {"path": "normalizer/specification", "sha256": spec_d, "bytes": 4},
        ],
    )
    gb = {
        "schemaVersion": 1,
        "closureId": g_c["typedId"],
        "parserName": "opensip-syntax-parser",
        "parserVersion": g_rec["semanticVersion"],
        "bundleDigest": bundle_blob,
        "grammars": [
            {
                "grammarId": "typescript",
                "grammarVersion": "1.0.0",
                "languageId": "typescript",
                "syntaxClass": "code",
                "suffixes": [".ts"],
                "grammarDigest": g_file,
            }
        ],
        "normalizer": {"normalizerId": "n", "normalizerVersion": "1.0.0", "specificationDigest": spec_d},
    }
    ctx = {"schemaVersion": 2, "grammarBundle": gb}
    ctx_h = store.put_h("native.context.syntax.v2", ctx, label="syntax-ctx")
    uni = {
        "schemaVersion": 2,
        "nativeContextId": ctx_h["sha256Text"],
        "selectedGrammarIds": ["typescript"],
        "resolutionAttempted": False,
    }
    stock(uni, NATIVE, "#/$defs/SyntaxUniverseV2ResolvedInputs", "syntax-universe")
    uni_h = store.put_h("native.semantic-universe.syntax.v2", uni, label="syntax-uni")
    uni_hex = uni_h["digest"]

    def mint_scope(relation, resolution, subjects):
        rec = {
            "schemaVersion": 2,
            "snapshotId": snap_h["typedId"],
            "sourceUniverse": uni_hex,
            "targetUniverse": uni_hex,
            "relation": relation,
            "resolution": resolution,
            "enumeratorClosure": prov_c["typedId"],
            "subjects": sort_set(list(subjects)),
        }
        stock(rec, IDENT, "#/$defs/subject-scope", f"scope-{relation}")
        h = store.put_h("subject-scope", rec, label=f"scope-{relation}-{resolution}")
        return h, rec

    def mint_coverage(scope_h, relation, resolution, nsubj, *, coverage, rc, deficiency=None, native_cause=None):
        commit = "sha256:" + scope_h["digest"]
        key = {
            "relation": relation,
            "resolution": resolution,
            "sourceUniverse": uni_hex,
            "targetUniverse": uni_hex,
            "subjectScopeCommitment": commit,
        }
        entry = {
            "relation": relation,
            "resolution": resolution,
            "coverage": coverage,
            "examinedUniverse": {"subjectScopeCommitment": commit, "subjectCount": nsubj},
            "resolutionCompleteness": rc,
            "closedWorld": closed_world(),
            "derivationKinds": [],
            "confidenceMillionths": 1000000,
            "deficiency": deficiency,
            "nativeCause": native_cause,
        }
        payload = {"schemaVersion": 3, "key": key, "entry": entry}
        stock(payload, NATIVE, "#/$defs/CoverageResultV3", f"covp-{relation}")
        pd = store.put_canonical(payload, label=f"covp-{relation}")
        env = {
            "schemaVersion": 2,
            "scopeId": scope_h["typedId"],
            "payloadSchemaDigest": native_schema_d,
            "payloadDigest": pd,
        }
        stock(env, IDENT, "#/$defs/coverage", f"cov-{relation}")
        h = store.put_h("coverage", env, label=f"cov-{relation}")
        return h, env, payload

    def mint_fact(relation, resolution, payload, anchors):
        pd = store.put_canonical(payload, label=f"fp-{relation}")
        rec = {
            "schemaVersion": 2,
            "snapshotId": snap_h["typedId"],
            "relation": relation,
            "resolution": resolution,
            "sourceUniverse": uni_hex,
            "targetUniverse": uni_hex,
            "producerClosure": prov_c["typedId"],
            "payloadSchemaDigest": rel_schema_d,
            "payloadDigest": pd,
            "anchors": sort_set(anchors),
            "confidenceMillionths": 1000000,
        }
        stock(rec, IDENT, "#/$defs/fact", f"fact-{relation}")
        h = store.put_h("fact", rec, label=f"fact-{relation}")
        return h, rec, payload

    # --- retained cases ---
    sf_with, sf_with_rec = mint_scope("file", "enumerated", ["src/a.ts"])
    file_pl = {"path": "src/a.ts", "contentSha256": a_d, "byteLength": len(a_ts)}
    ff, ffr, _ = mint_fact("file", "enumerated", file_pl, [])
    cf_with, cf_with_env, cf_with_p = mint_coverage(sf_with, "file", "enumerated", 1, coverage="complete", rc=rc_na())

    sf_absent, sf_absent_rec = mint_scope("file", "enumerated", ["absent.ts"])
    cf_absent, cf_absent_env, cf_absent_p = mint_coverage(
        sf_absent, "file", "enumerated", 1, coverage="complete", rc=rc_na()
    )

    sf_empty, sf_empty_rec = mint_scope("file", "enumerated", [])
    cf_empty, cf_empty_env, cf_empty_p = mint_coverage(
        sf_empty, "file", "enumerated", 0, coverage="complete", rc=rc_na()
    )

    si, si_rec = mint_scope("imports", "resolved-target", ["module:src/a.ts"])
    imp_pl = {"importer": "module:src/a.ts", "specifier": "./b", "resolvedTarget": "file:src/b.ts"}
    imf, imfr, _ = mint_fact("imports", "resolved-target", imp_pl, [{"path": "src/a.ts", "blobDigest": a_d, "startByte": 0, "endByte": len(a_ts)}])
    ci, ci_env, ci_p = mint_coverage(si, "imports", "resolved-target", 1, coverage="complete", rc=rc_complete())

    si2, si2_rec = mint_scope("imports", "resolved-target", ["module:src/a.ts"])
    ue_pl = {
        "referrer": "module:src/a.ts",
        "relation": "imports",
        "edgeKind": "unresolved-module-specifier",
        "targetScope": "unknown",
        "targetModule": None,
        "detail": "missing specifier",
    }
    uef, uefr, _ = mint_fact("unresolved-edge", "observed", ue_pl, [{"path": "src/a.ts", "blobDigest": a_d, "startByte": 0, "endByte": len(a_ts)}])
    ci2, ci2_env, ci2_p = mint_coverage(
        si2, "imports", "resolved-target", 1, coverage="complete", rc=rc_incomplete(1, ["unresolved-module-specifier"])
    )

    si3, si3_rec = mint_scope("imports", "resolved-target", ["module:src/a.ts"])
    ci3, ci3_env, ci3_p = mint_coverage(si3, "imports", "resolved-target", 1, coverage="complete", rc=rc_not_attempted())

    # Negative: RC-6 complete without exhaustive examination
    sf_bad, _ = mint_scope("file", "enumerated", ["src/a.ts"])
    bad_rc = dict(rc_na())
    bad_rc["examinedExhaustive"] = False
    commit_bad = "sha256:" + sf_bad["digest"]
    bad_payload = {
        "schemaVersion": 3,
        "key": {
            "relation": "file",
            "resolution": "enumerated",
            "sourceUniverse": uni_hex,
            "targetUniverse": uni_hex,
            "subjectScopeCommitment": commit_bad,
        },
        "entry": {
            "relation": "file",
            "resolution": "enumerated",
            "coverage": "complete",
            "examinedUniverse": {"subjectScopeCommitment": commit_bad, "subjectCount": 1},
            "resolutionCompleteness": bad_rc,
            "closedWorld": closed_world(),
            "derivationKinds": [],
            "confidenceMillionths": 1000000,
            "deficiency": None,
            "nativeCause": None,
        },
    }
    # Stock schema allows the pair; RC-6 is a producing/admission law beyond stock.
    stock(bad_payload, NATIVE, "#/$defs/CoverageResultV3", "rc6-negative-stock")

    cases = [
        {
            "name": "file-enumerated-with-fact",
            "relation": "file",
            "resolution": "enumerated",
            "scope": sf_with,
            "scopeRec": sf_with_rec,
            "cov": cf_with,
            "covEnv": cf_with_env,
            "covPayload": cf_with_p,
            "facts": [(ff, ffr, file_pl)],
            "unresolved": [],
        },
        {
            "name": "file-enumerated-fact-absent-examined-missing-path",
            "relation": "file",
            "resolution": "enumerated",
            "scope": sf_absent,
            "scopeRec": sf_absent_rec,
            "cov": cf_absent,
            "covEnv": cf_absent_env,
            "covPayload": cf_absent_p,
            "facts": [],
            "unresolved": [],
        },
        {
            "name": "file-enumerated-fact-free-empty-scope",
            "relation": "file",
            "resolution": "enumerated",
            "scope": sf_empty,
            "scopeRec": sf_empty_rec,
            "cov": cf_empty,
            "covEnv": cf_empty_env,
            "covPayload": cf_empty_p,
            "facts": [],
            "unresolved": [],
        },
        {
            "name": "imports-resolved-zero-unresolved-complete",
            "relation": "imports",
            "resolution": "resolved-target",
            "scope": si,
            "scopeRec": si_rec,
            "cov": ci,
            "covEnv": ci_env,
            "covPayload": ci_p,
            "facts": [(imf, imfr, imp_pl)],
            "unresolved": [],
        },
        {
            "name": "imports-resolved-unresolved-edge-incomplete",
            "relation": "imports",
            "resolution": "resolved-target",
            "scope": si2,
            "scopeRec": si2_rec,
            "cov": ci2,
            "covEnv": ci2_env,
            "covPayload": ci2_p,
            "facts": [],
            "unresolved": [(uef, uefr, ue_pl)],
        },
        {
            "name": "imports-resolved-skipped-not-attempted",
            "relation": "imports",
            "resolution": "resolved-target",
            "scope": si3,
            "scopeRec": si3_rec,
            "cov": ci3,
            "covEnv": ci3_env,
            "covPayload": ci3_p,
            "facts": [],
            "unresolved": [],
        },
    ]

    vectors = []
    for case in cases:
        entry = case["covPayload"]["entry"]
        subjects = set(case["scopeRec"]["subjects"])
        unres_in = []
        for h, rec, pl in case["unresolved"]:
            if pl.get("relation") == case["relation"] and pl.get("referrer") in subjects:
                unres_in.append(h["typedId"])
        derived = derive_rc(
            ladders=ladders,
            relation=case["relation"],
            resolution=case["resolution"],
            entry=entry,
            unresolved_in_examined=unres_in,
        )
        if not derived.get("ok"):
            die(f"{case['name']} RC derivation failed {derived}")
        # Joins: coverage key scope commitment == sha256 of scope H digest; subjectCount == len(subjects)
        commit = case["covPayload"]["key"]["subjectScopeCommitment"]
        if commit != "sha256:" + case["scope"]["digest"]:
            die(f"{case['name']} subject-scope-commitment-mismatch")
        if entry["examinedUniverse"]["subjectCount"] != len(case["scopeRec"]["subjects"]):
            die(f"{case['name']} examined-universe-subject-count-mismatch")
        in_snapshot = {r["path"] for r in snapshot["sourceInventory"]}
        facts_in = []
        for h, rec, pl in case["facts"]:
            if rec["relation"] == "file" and pl["path"] in subjects:
                facts_in.append(h["typedId"])
            if rec["relation"] == "imports" and pl["importer"] in subjects:
                facts_in.append(h["typedId"])
        vectors.append(
            {
                "name": case["name"],
                "relation": case["relation"],
                "resolution": case["resolution"],
                "retainedScope": exhibit("subject-scope", case["scopeRec"]),
                "retainedCoverageEnvelope": exhibit("coverage", case["covEnv"]),
                "retainedCoveragePayload": {
                    "record": case["covPayload"],
                    "C_sha256": hashlib.sha256(C(case["covPayload"])).hexdigest(),
                    "digest": case["covEnv"]["payloadDigest"],
                },
                "retainedFacts": [
                    {"typedId": h["typedId"], "record": rec, "payload": pl, "C_sha256": hashlib.sha256(C(rec)).hexdigest()}
                    for h, rec, pl in case["facts"] + case["unresolved"]
                ],
                "factsPresentInExaminedSet": facts_in,
                "unresolvedEdgeFactsInExaminedSet": unres_in,
                "snapshotContainsExaminedFileSubjects": {
                    s: (s in in_snapshot) for s in case["scopeRec"]["subjects"] if case["relation"] == "file"
                },
                "derivedFromRetained": derived,
                "ok": derived["ok"],
            }
        )

    rc6_neg = derive_rc(
        ladders=ladders,
        relation="file",
        resolution="enumerated",
        entry=bad_payload["entry"],
        unresolved_in_examined=[],
    )
    if rc6_neg.get("ok") or rc6_neg.get("refusal") != "RC-6":
        die(f"RC-6 negative did not refuse {rc6_neg}")
    rc0_neg = derive_rc(
        ladders=ladders,
        relation="unresolved-edge",
        resolution="enumerated",
        entry=cf_with_p["entry"],
        unresolved_in_examined=[],
    )
    if rc0_neg.get("ok") or rc0_neg.get("refusal") != "RC-0":
        die(f"RC-0 negative did not refuse {rc0_neg}")

    store.export(FOUND / "count-class-attempt.store.json")
    count_doc = {
        "kind": "standaloneCanonicalVector",
        "notACompleteRun": True,
        "selector": "native-evidence.md §4.3 RC-0/RC-1/RC-2/RC-6; identity-schemas.v3 subject-scope/coverage; CoverageResultV3",
        "resolvedRungs": sorted({p[1] for p in RESOLVED}),
        "retainedSnapshot": exhibit("snapshot", snapshot),
        "enumeratorClosure": prov_c["typedId"],
        "universe": uni_hex,
        "retainedStore": "foundation/count-class-attempt.store.json",
        "vectors": vectors,
        "negativeControls": [
            {
                "name": "rc6-complete-coverage-without-exhaustive-examination",
                "refusal": "RC-6",
                "derivedFromRetained": rc6_neg,
                "ok": False,
            },
            {
                "name": "rc0-unregistered-pair-unresolved-edge-enumerated",
                "refusal": "RC-0",
                "derivedFromRetained": rc0_neg,
                "ok": False,
            },
        ],
    }
    (FOUND / "count-class-attempt.json").write_text(json.dumps(count_doc, indent=2) + "\n")

    # Independent re-derive from exported store (no saved derived as truth).
    st2 = Store.load(FOUND / "count-class-attempt.store.json")
    for vec in count_doc["vectors"]:
        env = parse_h_frame(st2.get(vec["retainedCoverageEnvelope"]["frameSha256"]))["value"]
        payload = admit_raw(st2.get(env["payloadDigest"]))
        scope = parse_h_frame(st2.get(vec["retainedScope"]["frameSha256"]))["value"]
        unres = []
        for f in vec["retainedFacts"]:
            if f["record"]["relation"] == "unresolved-edge":
                pl = f["payload"]
                if pl.get("relation") == vec["relation"] and pl.get("referrer") in set(scope["subjects"]):
                    unres.append(f["typedId"])
        d2 = derive_rc(
            ladders=ladders,
            relation=vec["relation"],
            resolution=vec["resolution"],
            entry=payload["entry"],
            unresolved_in_examined=unres,
        )
        if not d2.get("ok") or d2.get("expectedState") != vec["derivedFromRetained"].get("expectedState") and (vec["relation"], vec["resolution"]) in RESOLVED:
            # For not-applicable rungs expectedState is inside expected dict
            if (vec["relation"], vec["resolution"]) not in RESOLVED:
                if not d2.get("ok"):
                    die(f"replay {vec['name']} {d2}")
            elif d2.get("expectedState") != vec["derivedFromRetained"].get("expectedState"):
                die(f"replay drift {vec['name']} {d2}")
        if not d2.get("ok"):
            die(f"replay {vec['name']} {d2}")

    # --- code vs data matrix ---
    native = json.loads((KIT / NATIVE).read_text())
    gcap = native["x-opensip-grammar-capability-registry"]
    matrix = json.loads(MATRIX.read_text())
    blv_enum = ["typescript", "javascript", "rust"]
    ident = json.loads((KIT / IDENT).read_text())
    schema_enum = ident["$defs"]["body-language-version"]["properties"]["languageId"]["enum"]
    if schema_enum != blv_enum:
        die(f"BLV enum drift {schema_enum}")

    def cell(cap, mode):
        for c in matrix["cells"]:
            if c.get("capability") == cap and c.get("mode") == mode:
                return c
        die(f"missing matrix cell {cap} x {mode}")

    clones_syntax = cell("clones-fact", "syntax-only")
    clones_ts = cell("clones-fact", "ts-tsconfig")
    inventory_syntax = cell("inventory", "syntax-only")

    def measure_store(stem):
        st = Store.load(OUT / "runs" / f"{stem}.store.json")
        facts = []
        for k, rec in st.object_table.items():
            if not str(k).startswith("fact2:"):
                continue
            parsed = parse_h_frame(st.get(rec["digest"]), allowed_domains={"fact"})["value"]
            pl = admit_raw(st.get(parsed["payloadDigest"]))
            facts.append({"id": k, "relation": parsed["relation"], "resolution": parsed["resolution"], "payload": pl})
        coverages = []
        for k, rec in st.object_table.items():
            if not str(k).startswith("coverage2:"):
                continue
            env = parse_h_frame(st.get(rec["digest"]), allowed_domains={"coverage"})["value"]
            payload = admit_raw(st.get(env["payloadDigest"]))
            coverages.append(
                {
                    "id": k,
                    "relation": payload["key"]["relation"],
                    "resolution": payload["key"]["resolution"],
                    "coverage": payload["entry"]["coverage"],
                    "deficiency": payload["entry"].get("deficiency"),
                    "nativeCause": payload["entry"].get("nativeCause"),
                    "resolutionCompleteness": payload["entry"]["resolutionCompleteness"],
                }
            )
        ctx_domain = None
        uni_sel = None
        grammar_rows = []
        normalizer = None
        language_mode = None
        for rec in st.object_table.values():
            if rec.get("kind") != "h-identity":
                continue
            if rec.get("domain") == "native.context.syntax.v2":
                ctx = parse_h_frame(st.get(rec["digest"]))["value"]
                ctx_domain = rec["domain"]
                gb2 = ctx.get("grammarBundle") or {}
                grammar_rows = gb2.get("grammars") or []
                normalizer = gb2.get("normalizer")
            if rec.get("domain") == "native.semantic-universe.syntax.v2":
                uni = parse_h_frame(st.get(rec["digest"]))["value"]
                uni_sel = uni.get("selectedGrammarIds")
        clones_facts = [f for f in facts if f["relation"] == "clones"]
        clones_cov = [c for c in coverages if c["relation"] == "clones"]
        body_frames = []
        for f in clones_facts:
            bid = f["payload"].get("bodyIdentity")
            if isinstance(bid, str) and bid.startswith("sha256:"):
                hx = bid.split(":", 1)[1]
                parsed_b = parse_body_identity_frame(st.get(hx))
                body_frames.append(
                    {
                        "factId": f["id"],
                        "levelId": parsed_b.get("levelId"),
                        "languageId": parsed_b.get("languageId"),
                        "normalisationLevel": f["payload"].get("normalisationLevel"),
                    }
                )
        return {
            "store": f"runs/{stem}.store.json",
            "admission": "unverified-frozen-raw-property-check-not-full-Run-admission",
            "contextDomain": ctx_domain,
            "selectedGrammarIds": uni_sel,
            "grammarRows": [
                {"grammarId": g.get("grammarId"), "languageId": g.get("languageId"), "syntaxClass": g.get("syntaxClass")}
                for g in grammar_rows
            ],
            "normalizerPresent": bool(normalizer),
            "normalizerSpecificationDigest": (normalizer or {}).get("specificationDigest"),
            "clonesFacts": [{"id": f["id"], "relation": f["relation"], "resolution": f["resolution"]} for f in clones_facts],
            "clonesCoverage": clones_cov,
            "bodyIdentityFrames": body_frames,
            "fileFacts": [{"id": f["id"], "resolution": f["resolution"]} for f in facts if f["relation"] == "file"],
        }

    syn_code = measure_store("syntax-code")
    syn_data = measure_store("syntax-data")
    if any(g["languageId"] == "json" and g["syntaxClass"] != "data-document" for g in syn_data["grammarRows"]):
        die("syntax-data json class")
    if syn_data["clonesFacts"]:
        die("syntax-data must not mint clones body identity")
    if not syn_data["clonesCoverage"]:
        die("syntax-data missing clones Coverage disclosure")
    cc0 = syn_data["clonesCoverage"][0]
    if cc0["coverage"] != "unknown" or cc0["deficiency"] != "language-tier-unsupported" or cc0["nativeCause"] != "capability-missing":
        die(f"syntax-data clones disclosure {cc0}")
    if not syn_code["clonesFacts"]:
        die("syntax-code expected clones facts")
    if any(b.get("languageId") not in blv_enum for b in syn_code["bodyIdentityFrames"]):
        die("syntax-code body languageId outside BLV enum")
    if any(g["languageId"] == "json" for g in syn_code["grammarRows"] if g.get("syntaxClass") == "code"):
        die("json must not be code")

    json_caps = set(gcap["languages"]["json"]["capabilities"])
    ts_caps = set(gcap["languages"]["typescript"]["capabilities"])
    if "clones@normalized-body-hash" in json_caps:
        die("json grammar must not bear clones")
    if "clones@normalized-body-hash" not in ts_caps:
        die("typescript grammar must bear clones")
    if "json" in blv_enum:
        die("json must not be in body-language-version.languageId")
    if clones_syntax["state"] != "SUPPORTED-DESIGN":
        die("clones-fact x syntax-only cell")

    matrix_doc = {
        "kind": "standaloneCanonicalVector",
        "notACompleteRun": True,
        "selector": "native-capability-matrix.v2.json cells; native-evidence.schemas.v2.json#/x-opensip-grammar-capability-registry; identity-schemas.v3 body-language-version.languageId",
        "classLaw": gcap["classLaw"],
        "publishedMatrixCells": {
            "clones-fact x syntax-only": {
                "capability": "clones-fact",
                "mode": "syntax-only",
                "state": clones_syntax["state"],
                "note": clones_syntax.get("note"),
                "deficiency": clones_syntax.get("deficiency"),
            },
            "clones-fact x ts-tsconfig": {
                "capability": "clones-fact",
                "mode": "ts-tsconfig",
                "state": clones_ts["state"],
            },
            "inventory x syntax-only": {
                "capability": "inventory",
                "mode": "syntax-only",
                "state": inventory_syntax["state"],
            },
        },
        "grammarRegistry": {
            "codeLanguages": sorted(k for k, v in gcap["languages"].items() if v["syntaxClass"] == "code"),
            "dataLanguages": sorted(k for k, v in gcap["languages"].items() if v["syntaxClass"] == "data-document"),
            "jsonCapabilities": sorted(json_caps),
            "typescriptCapabilities": sorted(ts_caps),
            "jsonBearsClones": "clones@normalized-body-hash" in json_caps,
            "typescriptBearsClones": "clones@normalized-body-hash" in ts_caps,
        },
        "bodyLanguageVersion": {
            "languageIdEnum": blv_enum,
            "jsonInEnum": False,
            "normalizerLaw": "A data-document languageId MUST NOT enter the clone preimage. Code languageId MUST be a member of this enum. Normalizer specification is retained on SyntaxGrammarBundleV1.normalizer.specificationDigest.",
        },
        "measuredFromCitedSyntaxStores": {
            "limit": "Raw property checks over retained H-frames and Coverage payloads. Not full Run admission or semantic replay of these stores in this Phase 4 vector.",
            "syntax-code": syn_code,
            "syntax-data": syn_data,
        },
        "application": {
            "matrixCellClonesFactSyntaxOnly": "SUPPORTED-DESIGN, grammar-bearing languages only",
            "syntax-code": "selected typescript code grammar; clones facts at normalized-body-hash; bodyIdentity languageId in BLV enum",
            "syntax-data": "selected json data-document grammar; no clones facts; clones Coverage unknown / language-tier-unsupported / capability-missing — unavailable disclosure, not a complete empty clone result",
        },
        "ok": True,
    }
    (FOUND / "code-vs-data-matrix.json").write_text(json.dumps(matrix_doc, indent=2) + "\n")

    # Citation census for enum-vs-resolution (do not overwrite unless necessary).
    cited = json.loads((FOUND / "enum-vs-resolution.json").read_text())
    current = []
    for stem in ["syntax-code", "ts", "rust", "syntax-data", "rust-partial-clones"]:
        st = Store.load(OUT / "runs" / f"{stem}.store.json")
        for k, rec in st.object_table.items():
            if not str(k).startswith("fact2:"):
                continue
            parsed = parse_h_frame(st.get(rec["digest"]), allowed_domains={"fact"})["value"]
            if parsed.get("relation") == "file":
                current.append({"store": stem, "id": k, "resolution": parsed.get("resolution")})
    cited_ids = {(r["store"], r["id"]) for r in cited["observedFileFacts"]}
    current_ids = {(r["store"], r["id"]) for r in current}
    refresh_needed = cited_ids != current_ids
    invented = [r for r in current if r["resolution"] != "enumerated"]
    census = {
        "kind": "citationCensus",
        "artifact": "foundation/enum-vs-resolution.json",
        "previousBytesPreserved": True,
        "refreshApplied": False,
        "refreshNeeded": refresh_needed,
        "currentFileFacts": current,
        "inventedResolvedFileRung": invented,
        "standingRuleStillHolds": not invented and all(r["resolution"] == "enumerated" for r in current),
        "note": "Previous exhibit bytes preserved. Current frozen stores still have only enumerated file facts. Cited IDs from an earlier freeze differ for rebuilt stores; standing rule does not require those particular identities.",
    }
    (FOUND / "enum-vs-resolution-citation-census.json").write_text(json.dumps(census, indent=2) + "\n")
    if invented:
        die(f"invented file resolved rung {invented}")

    print(
        json.dumps(
            {
                "countVectors": len(vectors),
                "countNegatives": 2,
                "allCountOk": all(v["ok"] for v in vectors),
                "matrixOk": True,
                "enumCensusRefreshNeeded": refresh_needed,
                "enumStandingHolds": census["standingRuleStillHolds"],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
