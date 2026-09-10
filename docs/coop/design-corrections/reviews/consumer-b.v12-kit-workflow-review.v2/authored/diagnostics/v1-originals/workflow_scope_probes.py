#!/usr/bin/env python3
"""Independent workflow-scope probes. Kit laws only. Consumer evaluators are not oracles."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
from pathlib import Path

V1 = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-validator.v1/output/diagnostics/syntax_code_pilot_probes.py")
spec = importlib.util.spec_from_file_location("v1probes", V1)
v1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v1)

C = v1.C
sha256 = v1.sha256
KIT = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-validator.v1/subject")
SNAP = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-workflow-review.v1/consumer-snapshot")
OUT = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-workflow-review.v1/output")
SRC = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-workflow-review.v1/consumer-snapshot/scripts/scope_reconstruct.py")

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

PROBES = []
FIRST = None


def record(name, ok, *, selector, detail=None, class_="check", req=None):
    global FIRST
    rec = {"name": name, "ok": bool(ok), "selector": selector, "class": class_, "detail": detail, "req": req}
    PROBES.append(rec)
    if (not ok) and FIRST is None and class_ in ("schema", "semantic", "replay"):
        FIRST = rec


def load(rel):
    return json.loads((SNAP / rel).read_text())


def kit_json(rel):
    return json.loads((KIT / rel).read_text())


def registry():
    files = [
        "docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json",
        "docs/coop/design-corrections/workflows/schemas/evaluator3/command-envelope.schema.json",
        "docs/coop/design-corrections/workflows/schemas/evaluator3/invocation-record.schema.json",
        "docs/coop/design-corrections/workflows/schemas/evaluator3/comparison-result.schema.json",
        "docs/coop/design-corrections/workflows/schemas/evaluator3/baseline-artifact.schema.json",
        "docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json",
        "docs/coop/design-corrections/workflows/schemas/evaluator3/repair.schema.json",
        "docs/coop/design-corrections/workflows/schemas/evaluator3/command-inventory.schema.json",
        "docs/coop/design-corrections/workflows/schemas/common.schema.json",
        "docs/coop/design-corrections/workflows/schemas/invocation-record.schema.json",
        "docs/coop/design-corrections/workflows/schemas/policy-document.schema.json",
        "docs/coop/design-corrections/workflows/schemas/repair.schema.json",
        "docs/coop/design-corrections/workflows/schemas/command-inventory.schema.json",
        "docs/coop/design-corrections/workflows/schemas/test-execution.schema.json",
        "docs/coop/design-corrections/workflows/schemas/evaluator3/invocation-record.schema.json",
        "docs/coop/design-corrections/foundation/identity-schemas.v3.json",
        "docs/coop/design-corrections/native/native-evidence.schemas.v2.json",
        "docs/coop/design-corrections/foundation/target-attribution.schema.v1.json",
        "docs/coop/design-corrections/workflows/schemas/policy-document.v2.schema.json",
        "docs/coop/design-corrections/workflows/schemas/imported-evidence.schema.json",
    ]
    res = []
    docs = {}
    for f in files:
        doc = kit_json(f)
        docs[f] = doc
        if doc.get("$id"):
            res.append((doc["$id"], Resource.from_contents(doc)))
    return Registry().with_resources(res), docs


def validate(inst, schema_rel, selector="#"):
    reg, docs = REG
    doc = docs[schema_rel]
    if selector == "#":
        schema = doc
    elif selector.startswith("#/$defs/"):
        name = selector.split("/")[-1]
        schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": (doc.get("$id") or "urn:local") + "/inline-" + name,
            "$defs": doc.get("$defs", {}),
            **doc["$defs"][name],
        }
    else:
        raise ValueError(selector)
    errs = []
    try:
        v = Draft202012Validator(schema, registry=reg)
        for e in v.iter_errors(inst):
            errs.append({"path": list(e.absolute_path), "message": e.message, "validator": e.validator})
    except Exception as ex:
        errs.append({"path": [], "message": str(ex), "validator": "setup"})
    return errs


CLASS_TO_EXIT = {
    "success": 0,
    "policy-failed": 1,
    "request-rejected": 2,
    "indeterminate": 3,
    "operational-failed": 4,
    "interrupted": 130,
}

GRAPH_PROJECTABLE = {
    ("calls", "resolved-callee"),
    ("references", "resolved-binding"),
    ("imports", "resolved-target"),
    ("control-flow", "syntactic"),
    ("reachability", "from-resolved-calls"),
}


def kind_from_path(path: str) -> str:
    base = path.rsplit("/", 1)[-1]
    if base == "tsconfig.json":
        return "tsconfig"
    if base == "jsconfig.json":
        return "jsconfig"
    return "other"


def exists_atom(*, facts, coverages, minr, rel):
    matching = [f for f in facts if f["relation"] == rel]
    # rung: only facts whose resolution index >= min
    ladders = {
        "imports": ["syntactic-specifier", "resolved-target"],
        "types": ["annotated", "checked"],
        "file": ["enumerated"],
    }
    ladder = ladders[rel]
    mi = ladder.index(minr)
    known = [f for f in matching if f["resolution"] in ladder and ladder.index(f["resolution"]) >= mi]
    covs = [c for c in coverages if c["relation"] == rel and c["resolution"] == minr]
    if known:
        return "true"
    if not covs:
        return "indeterminate"
    if any(c.get("coverage") == "complete" for c in covs):
        return "false"
    return "indeterminate"


def main():
    global REG
    REG = registry()
    src = SRC.read_text()
    mapping = json.loads((SNAP / "scope-correction-review.json").read_text())["mapping"]

    # frozen hashes
    frozen = load("frozen-run-hashes.json")["runs"]
    for name, rec in frozen.items():
        p = SNAP / "runs" / name
        b = p.read_bytes()
        record(
            f"frozen-store-{name}",
            sha256(b) == rec["sha256"] and len(b) == rec["bytes"],
            selector="scope-correction-review frozen Run stores; this review does not admit those Runs",
            detail={"actual": sha256(b), "claimed": rec["sha256"]},
            class_="check",
        )

    CE = "docs/coop/design-corrections/workflows/schemas/evaluator3/command-envelope.schema.json"
    INV = "docs/coop/design-corrections/workflows/schemas/evaluator3/invocation-record.schema.json"
    CMP = "docs/coop/design-corrections/workflows/schemas/evaluator3/comparison-result.schema.json"
    BASE = "docs/coop/design-corrections/workflows/schemas/evaluator3/baseline-artifact.schema.json"
    GQ = "docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json"
    REP = "docs/coop/design-corrections/workflows/schemas/evaluator3/repair.schema.json"
    MRS = "docs/coop/design-corrections/workflows/schemas/invocation-record.schema.json"
    NATIVE = "docs/coop/design-corrections/native/native-evidence.schemas.v2.json"
    IDENT = "docs/coop/design-corrections/foundation/identity-schemas.v3.json"
    COMMON3 = "docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json"
    TA = "docs/coop/design-corrections/foundation/target-attribution.schema.v1.json"

    d9 = kit_json("docs/coop/artifacts/d9-exit-contract.v1.14.json")["classToExitCode"]
    record("d9-classToExitCode-equals-selected-map", d9 == CLASS_TO_EXIT, selector="d9-exit-contract.v1.14.json#/classToExitCode; R-D9-EXTENSION-PRECEDENCE", req="R-D9-EXTENSION-PRECEDENCE", class_="semantic")

    envelopes = {
        "R-ENVELOPE-CONFIG-INPUT": "envelopes/config-input.json",
        "R-ENVELOPE-EXTERNAL-INPUT": "envelopes/retained-external-input.json",
        "R-ENVELOPE-HOST-INVALID": "envelopes/host-invalid-internal.json",
        "R-ENVELOPE-PRODUCER-BOUNDARY": "envelopes/producer-boundary.json",
        "R-PUBLIC-FROM-INTERNAL-REFUSAL": "envelopes/public-from-internal.json",
        "R-PINNED-PURGE": "envelopes/pinned-purge.json",
        "R-PURGE-REPLAY-OUTPUT-FAILURE": "envelopes/purge-replay-output-failure.json",
        "R-FAILURE-ENVELOPES-D9": "envelopes/failure-d9-complete.json",
        "R-TEST-PREP-REPAIR-AUTH": None,
    }
    for rid, rel in envelopes.items():
        if rel is None:
            continue
        env = load(rel)
        errs = validate(env, CE, "#")
        derived = CLASS_TO_EXIT[env["termination"]["class"]]
        record(
            f"schema-{rid}",
            not errs,
            selector=CE,
            detail=errs[:4],
            class_="schema",
            req=rid,
        )
        record(
            f"exitCode-derived-{rid}",
            env.get("exitCode") == derived,
            selector="d9-exit-contract.v1.14.json classToExitCode; CommandEnvelope stores derived exitCode",
            detail={"exitCode": env.get("exitCode"), "class": env["termination"]["class"], "derived": derived},
            class_="semantic",
            req=rid,
        )

    auth = load("vectors/test-prep-repair-authorization.json")
    for k, env in auth.items():
        errs = validate(env, CE, "#")
        record(f"schema-auth-{k}", not errs, selector=CE, detail=errs[:4], class_="schema", req="R-TEST-PREP-REPAIR-AUTH")

    terms = load("envelopes/public-termination.json")["examples"]
    for k, t in terms.items():
        errs = validate(t, COMMON3, "#/$defs/StepTermination")
        record(f"schema-term-{k}", not errs, selector="evaluator3/common.schema.json#/$defs/StepTermination", detail=errs[:4], class_="schema", req="R-PUBLIC-TERMINATION-EXAMPLES")

    for rid, rel in [("R-SINGLE-STEP", "envelopes/single-step.json"), ("R-MULTI-STEP-DIFFERENT-SELECTIONS", "envelopes/multi-step.json")]:
        inst = load(rel)
        errs = validate(inst, INV, "#")
        record(f"schema-{rid}", not errs, selector=INV, detail=errs[:4], class_="schema", req=rid)
    multi = load("envelopes/multi-step.json")
    profiles = [s["params"]["profile"] for s in multi["orderedSteps"]]
    record("multi-step-different-profiles", profiles == ["default", "fit"] and multi["orderedSteps"][1]["dependsOn"] == [0], selector="R-MULTI-STEP-DIFFERENT-SELECTIONS named multi-step with different selections", class_="semantic", req="R-MULTI-STEP-DIFFERENT-SELECTIONS")

    inv = kit_json("docs/coop/design-corrections/workflows/command-inventory.v3.json")
    disc = load("envelopes/invocation-disclosure.json")
    record("invocation-disclosure-command-count", disc["commandCount"] == len(inv["commands"]) == 45, selector="command-inventory.v3.json; R-INVOCATION-DISCLOSURE", detail={"disc": disc["commandCount"], "inventory": len(inv["commands"])}, class_="semantic", req="R-INVOCATION-DISCLOSURE")
    q = next(c for c in inv["commands"] if c["name"] == "query")
    record("invocation-disclosure-query-formats-from-inventory", disc["query"]["formats"] == q.get("formats") and disc["query"]["parityFields"] == q.get("parityFields"), selector="command-inventory.v3.json query command formats/parityFields", class_="semantic", req="R-INVOCATION-DISCLOSURE")

    recav = load("envelopes/receipt-availability.json")
    record("schema-commit-receipt", not validate(recav["receipt"], IDENT, "#/$defs/commit-receipt"), selector="identity-schemas.v3.json#/$defs/commit-receipt", class_="schema", req="R-DURABLE-RECEIPT-AVAILABILITY")
    record("schema-availability", not validate(recav["availability"], IDENT, "#/$defs/availability"), selector="identity-schemas.v3.json#/$defs/availability", class_="schema", req="R-DURABLE-RECEIPT-AVAILABILITY")
    record("receipt-synthetic-host-labeled", recav.get("syntheticHostObservation") is True, selector="R-DURABLE-RECEIPT-AVAILABILITY synthetic TCB observation labeled", class_="check", req="R-DURABLE-RECEIPT-AVAILABILITY")

    # config graphs
    for rid, rel in [
        ("R-CONFIG-SYNTHESIZED", "vectors/config-synthesized.json"),
        ("R-CONFIG-CUSTOM-MULTI-BASE", "vectors/config-custom-multi-base.json"),
        ("R-CONFIG-JS-SHARED-BASE", "vectors/config-js-shared-base.json"),
    ]:
        payload = load(rel)
        g = payload["graph"]
        errs = validate(g, NATIVE, "#/$defs/TypeScriptConfigGraphV1")
        record(f"schema-{rid}", not errs, selector="native-evidence.schemas.v2.json#/$defs/TypeScriptConfigGraphV1", detail=errs[:4], class_="schema", req=rid)
        recomputed = hashlib.sha256(C(g)).hexdigest()
        record(f"graphDigest-{rid}", payload["graphDigestSha256"] == recomputed and "tsconfigGraphHash" not in g, selector="native-evidence.schemas.v2.json TypeScriptConfigGraphV1 tsconfigGraphHash is SHA-256(C(this record)), not a graph field", detail={"claimed": payload["graphDigestSha256"], "recomputed": recomputed}, class_="semantic", req=rid)
        for n in g["nodes"]:
            derived = kind_from_path(n["path"])
            record(f"config-kind-{rid}-{n['path']}", n["kind"] == derived, selector="native-evidence.schemas.v2.json#/x-opensip-config-node-kind-law", class_="semantic", req=rid)
        paths = [n["path"] for n in g["nodes"]]
        record(f"config-path-order-{rid}", paths == sorted(paths, key=lambda p: p.encode()), selector="x-opensip-order by path on TypeScriptConfigGraphV1.nodes", class_="semantic", req=rid)

    syn = load("vectors/config-synthesized.json")["graph"]
    record("config-synthesized-null-entry-empty-nodes", syn["entryConfigPath"] is None and syn["nodes"] == [], selector="TypeScriptConfigGraphV1 entryConfigPath null exactly when synthesized", class_="semantic", req="R-CONFIG-SYNTHESIZED")
    custom = load("vectors/config-custom-multi-base.json")["graph"]
    app = next(n for n in custom["nodes"] if n["path"] == "tsconfig.app.json")
    record("config-custom-repeated-base-order", app["extendsResolved"] == ["tsconfig.strict.json", "tsconfig.base.json"], selector="R-CONFIG-CUSTOM-MULTI-BASE repeated-base order; extendsResolved sequence later-wins", class_="semantic", req="R-CONFIG-CUSTOM-MULTI-BASE")
    js = load("vectors/config-js-shared-base.json")["graph"]
    record("config-js-shared-base-entry-kind", js["entryConfigPath"] == "jsconfig.json" and kind_from_path("jsconfig.json") == "jsconfig", selector="R-CONFIG-JS-SHARED-BASE jsconfig inheriting shared base", class_="semantic", req="R-CONFIG-JS-SHARED-BASE")

    # comparisons
    for rid, rel in [
        ("R-CMP-EMPTY-RESULT", "vectors/comparison-empty-result.json"),
        ("R-CMP-MISSING", "vectors/comparison-missing.json"),
        ("R-CMP-EVIDENCE-CHANGED", "vectors/comparison-evidence-changed.json"),
        ("R-SCOPE-POLICY-ONLY-COMPARISON", "vectors/comparison-scope-policy-only.json"),
        ("R-PIVOT-ONLY-FINGERPRINTS", "vectors/pivot-only-fingerprints.json"),
        ("R-BASELINE-AUDIT", "vectors/baseline-audit.json"),
    ]:
        obj = load(rel)
        if rid == "R-BASELINE-AUDIT":
            errs = validate(obj, BASE, "#")
        else:
            errs = validate(obj, CMP, "#")
        record(f"schema-{rid}", not errs, selector=BASE if rid == "R-BASELINE-AUDIT" else CMP, detail=errs[:5], class_="schema", req=rid)

    e0e3 = load("vectors/baseline-e0-e3.json")
    record("schema-R-E0-VS-E1-E3-E0", not validate(e0e3["E0"], CMP, "#"), selector=CMP, class_="schema", req="R-E0-VS-E1-E3")
    record("schema-R-E0-VS-E1-E3-E13", not validate(e0e3["E1E3"], CMP, "#"), selector=CMP, class_="schema", req="R-E0-VS-E1-E3")
    e0p = e0e3["E0"]["descriptor"]["pivotsAvailable"]
    e13p = e0e3["E1E3"]["descriptor"]["pivotsAvailable"]
    record("e0-vs-e13-pivot-distinction", e0p["E0"] == "available" and e13p["E0"] == "not-needed" and e13p["E1"] == "available", selector="comparison-result.schema.json E0 prior detector vs E1–E3 re-evaluation of current retained evidence", class_="semantic", req="R-E0-VS-E1-E3")

    scope_cmp = load("vectors/comparison-scope-policy-only.json")
    bctx = scope_cmp["descriptor"]["baselineContext"]
    cctx = scope_cmp["descriptor"]["currentContext"]
    record(
        "scope-policy-only-scopeDigest-actually-differs",
        bctx["scopeDigest"] != cctx["scopeDigest"] and scope_cmp["descriptor"]["contextDelta"]["scopeChanged"] is True,
        selector="R-SCOPE-POLICY-ONLY-COMPARISON a comparison where only the bound ScopeDocumentV1 changes; contextDelta.scopeChanged is not a substitute for unequal scopeDigest",
        detail={"baselineScope": bctx["scopeDigest"], "currentScope": cctx["scopeDigest"], "policyEqual": bctx["policyDigest"] == cctx["policyDigest"]},
        class_="semantic",
        req="R-SCOPE-POLICY-ONLY-COMPARISON",
    )

    # repair
    repair = load("vectors/repair-descriptor.json")
    record("schema-R-REPAIR-DESCRIPTOR", not validate(repair, REP, "#/$defs/RepairPlanV1"), selector="evaluator3/repair.schema.json#/$defs/RepairPlanV1", detail=validate(repair, REP, "#/$defs/RepairPlanV1")[:5], class_="schema", req="R-REPAIR-DESCRIPTOR")
    mrs = load("vectors/mutation-replay-scope.json")
    record("schema-R-MUTATION-REPLAY-SCOPE", not validate(mrs, MRS, "#/$defs/MutationReplayScopeV1"), selector="invocation-record.schema.json#/$defs/MutationReplayScopeV1", detail=validate(mrs, MRS, "#/$defs/MutationReplayScopeV1")[:5], class_="schema", req="R-MUTATION-REPLAY-SCOPE")
    record("mutation-scope-operation-is-purge-not-repair-apply", mrs.get("operation") == "purge", selector="evaluator3/repair.schema.json x-opensip-mutation-operation-map: repair-apply excluded from MutationReplayScopeV1.operation", class_="semantic", req="R-MUTATION-REPLAY-SCOPE")
    keys = load("vectors/repair-apply-key.json")
    re_mrs = hashlib.sha256(C(keys["mutationReplayScope"])).hexdigest()
    re_apply = hashlib.sha256(C(keys["applyKey"])).hexdigest()
    record("repair-apply-key-unequal-mutation-scope", keys["unequal"] is True and keys["repairApplyKeyDigest"] == re_apply and keys["mutationReplayScopeDigest"] == re_mrs and re_apply != re_mrs, selector="R-REPAIR-APPLY-KEY distinct from mutation replay scope", class_="semantic", req="R-REPAIR-APPLY-KEY")

    # min-resolution independent
    minres = load("vectors/min-resolution.json")
    syn_q = exists_atom(facts=[{"relation": "imports", "resolution": "syntactic-specifier"}], coverages=[{"relation": "imports", "resolution": "syntactic-specifier", "coverage": "complete"}], minr="syntactic-specifier", rel="imports")
    syn_i = exists_atom(facts=[], coverages=[], minr="syntactic-specifier", rel="imports")
    res_q = exists_atom(facts=[{"relation": "imports", "resolution": "resolved-target"}], coverages=[{"relation": "imports", "resolution": "resolved-target", "coverage": "complete"}], minr="resolved-target", rel="imports")
    res_i = exists_atom(facts=[{"relation": "imports", "resolution": "syntactic-specifier"}], coverages=[{"relation": "imports", "resolution": "resolved-target", "coverage": "complete"}], minr="resolved-target", rel="imports")
    ty_i = exists_atom(facts=[], coverages=[{"relation": "types", "resolution": "checked", "coverage": "complete"}], minr="checked", rel="types")
    record("minres-syntactic-qualifying", minres["cases"][0]["qualifyingValue"] == syn_q == "true", selector="atom-evaluation-contract.v1.md exists true on known match; R-MIN-RESOLUTION-THREE-LEVELS", class_="semantic", req="R-MIN-RESOLUTION-THREE-LEVELS")
    record("minres-syntactic-insufficient", minres["cases"][0]["insufficientValue"] == syn_i == "indeterminate", selector="identity-and-evidence.md §4 exists otherwise indeterminate", class_="semantic", req="R-MIN-RESOLUTION-THREE-LEVELS")
    record("minres-resolved-qualifying", minres["cases"][1]["qualifyingValue"] == res_q == "true", selector="atom-evaluation-contract.v1.md rung ≥ minResolution", class_="semantic", req="R-MIN-RESOLUTION-THREE-LEVELS")
    record("minres-resolved-insufficient-is-complete-absence-false", res_i == "false" and minres["cases"][1]["insufficientValue"] == "false", selector="identity-and-evidence.md §4 exists false on complete absence (complete Coverage at requested rung, no match). Weaker-rung facts do not occupy the requested rung.", class_="semantic", req="R-MIN-RESOLUTION-THREE-LEVELS")
    record(
        "minres-resolved-insufficientExpected-agrees-with-kit",
        minres["cases"][1].get("insufficientExpected") == "false",
        selector="identity-and-evidence.md §4 exists false on complete absence. Vector insufficientExpected=indeterminate disagrees with the kit (measured value is correctly false).",
        class_="check",
        req="R-MIN-RESOLUTION-THREE-LEVELS",
    )
    has_type_qualifying = any("qualifyingValue" in c for c in minres["cases"] if c["level"] == "type")
    record("minres-type-has-qualifying-and-insufficient", has_type_qualifying, selector="R-MIN-RESOLUTION-THREE-LEVELS each of three levels × qualifying/insufficient", detail=minres["cases"][2], class_="semantic", req="R-MIN-RESOLUTION-THREE-LEVELS")

    tv = load("vectors/replay-three-valued.json")
    indep_tv = exists_atom(facts=[], coverages=[], minr="enumerated", rel="file")
    record("three-valued-exists-missing-coverage-indeterminate", tv["value"] == indep_tv == "indeterminate" and tv["notVacuousTrue"] and tv["notVacuousFalse"], selector="identity-and-evidence.md §4 exists otherwise indeterminate; R-REPLAY-THREE-VALUED", class_="semantic", req="R-REPLAY-THREE-VALUED")

    # JS body through TS: recompute identities independently using v1 C and fact-identity frame
    def u8pref(b: bytes) -> bytes:
        return bytes([len(b)]) + b

    def body_id(language_id, dialect, span, compiler_name="tsc"):
        blv = {"schemaVersion": 1, "languageId": language_id, "compilerName": compiler_name, "compilerVersion": "5.4.5", "compilerBuild": "a" * 64, "dialect": dialect}
        lv = hashlib.sha256(C(blv)).digest()
        payload = len(span).to_bytes(4, "big") + span
        pre = u8pref(b"opensip.fact-identity.v1") + u8pref(b"L0-verbatim") + u8pref(hashlib.sha256(b"L0-verbatim").digest()) + u8pref(language_id.encode()) + u8pref(lv) + len(payload).to_bytes(4, "big") + payload
        return "sha256:" + hashlib.sha256(pre).hexdigest()

    js_span = b"export const n = 1;\n"
    js_vec = load("vectors/js-body-through-ts.json")
    rec_js = body_id("javascript", {"grammarVariant": "js"}, js_span)
    rec_ts = body_id("typescript", {"grammarVariant": "ts"}, js_span)
    record("js-body-through-ts-languageId-not-provider", js_vec["bodyLanguageId"] == "javascript" and js_vec["providerLanguageId"] == "typescript" and js_vec["distinct"] is True and js_vec["javascriptL0"] == rec_js and js_vec["typescriptL0OverSameBytes"] == rec_ts and rec_js != rec_ts, selector="relation-payload-schemas.v2.json languageIdIsNotTheProviderLanguage; R-JS-CLONE-BODY-THROUGH-TS", class_="semantic", req="R-JS-CLONE-BODY-THROUGH-TS")

    own = load("vectors/rust-body-identity-pair.json")
    record(
        "ownership-pair-two-ownership-maps-derive-same-dialect",
        False,
        selector="R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE two retained graphs or an explicit pair vector comparing body identities when only ownership selection changes. Hashing the identical body-language-version twice is not two ownership maps.",
        detail=own["sameDialectOwnershipSelections"],
        class_="semantic",
        req="R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE",
    )
    record("ownership-pair-dialect-change-moves-identity", own["distinctWhenDialectChanges"] is True, selector="identity-schemas.v3.json rust languageVersionBinding dialect edition", class_="semantic", req="R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE")

    # fake firstRefusal: source raises AdmissionError by hand
    record(
        "clones-negatives-executed-admission",
        not ("def clones_zero_anchor" in src and "raise AdmissionError(\"FACT_ANCHOR_CARDINALITY\"" in src),
        selector="R-CLONES-NEGATIVE-VECTORS Actual negative vectors; a declared firstRefusal flag is not proof a behavior executed",
        detail="scope_reconstruct.py raises AdmissionError in wrapper functions and assigns constructed firstRefusal dicts",
        class_="semantic",
        req="R-CLONES-NEGATIVE-VECTORS",
    )
    record(
        "hidden-mismatch-executed-admission",
        False,
        selector="R-HIDDEN-MISMATCH-PER-LANGUAGE at least one refused hidden/mismatched input for TypeScript and Rust with first-refusal boundary. scope_reconstruct.py writes firstRefusal dicts without running native context/universe admission.",
        class_="semantic",
        req="R-HIDDEN-MISMATCH-PER-LANGUAGE",
    )
    record(
        "unsupported-grammar-executed-admission",
        False,
        selector="R-RUN-UNSUPPORTED-GRAMMAR Test an unsupported grammar without assuming a TypeScript compiler. Declared unsupported-file flag is not executed suffix/grammar-bundle admission.",
        class_="semantic",
        req="R-RUN-UNSUPPORTED-GRAMMAR",
    )
    record(
        "repair-authority-executed-correspondence-join",
        False,
        selector="R-REPAIR-AUTHORITY-PER-TARGET independently chosen discriminating controls. Negative is a constructed firstRefusal dict, not an executed fingerprint correspondence join.",
        class_="semantic",
        req="R-REPAIR-AUTHORITY-PER-TARGET",
    )

    # graph query
    gq = load("query/graph-query-bundle.json")
    record("graph-query-labels-run-admission-unverified", gq.get("underlyingRunAdmissionUnverified") is True and gq.get("didNotClaimCloseRun") is True, selector="query-projection-contract.v3.md execute_graph_query requires close_run; algorithm vectors must retain that limitation", class_="check", req="R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR")
    for name, req in gq["requests"].items():
        errs = validate(req, GQ, "#/$defs/GraphQueryRequestV1")
        record(f"schema-gq-req-{name}", not errs, selector="evaluator3/graph-query.schema.json#/$defs/GraphQueryRequestV1", detail=errs[:4], class_="schema", req="R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR")
        pair = (req["params"]["relation"], req["params"]["minResolution"])
        record(
            f"gq-{name}-relation-is-projectable",
            pair in GRAPH_PROJECTABLE,
            selector="query-projection-contract.v3.md §3 Request law: relation@minResolution not a row of the projection table is refused QUERY.RELATION_UNSUPPORTED. file/* is graph-projectable no.",
            detail={"operation": req["operation"], "pair": list(pair)},
            class_="semantic",
            req="R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR",
        )
        errs_r = validate(gq["responses"][name if name != "neighborsPaged" else "neighborsPaged"] if name in gq["responses"] else gq["responses"].get(name, gq["responses"]["neighbors"]), GQ, "#/$defs/GraphQueryResponseV1") if name in gq["responses"] else []
        if name in gq["responses"]:
            record(f"schema-gq-resp-{name}", not validate(gq["responses"][name], GQ, "#/$defs/GraphQueryResponseV1"), selector="GraphQueryResponseV1", detail=validate(gq["responses"][name], GQ, "#/$defs/GraphQueryResponseV1")[:4], class_="schema", req="R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR")
    cursor = gq.get("cursor") or {}
    record(
        "gq-cursor-is-reference-form",
        isinstance(cursor.get("nextCursor"), str) and cursor["nextCursor"].startswith("q3.") if cursor.get("nextCursor") else True,
        selector="query-projection-contract.v3.md §5 Cursor reference form q3.<runId-64hex>.<selectionHash64>.<position>",
        detail=cursor,
        class_="semantic",
        req="R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR",
    )
    # neighborsPaged cursor
    nc = gq["responses"]["neighborsPaged"]["context"].get("nextCursor")
    record("gq-neighborsPaged-cursor-token", nc is None or (isinstance(nc, str) and nc.startswith("q3.")), selector="query-projection-contract.v3.md §5", detail=nc, class_="semantic", req="R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR")
    record("gq-failure-envelope-schema", not validate(gq["failureEnvelope"], CE, "#"), selector="query-projection-contract.v3.md §7 public failure carrier CommandEnvelope kind=failure", class_="schema", req="R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR")
    if gq.get("syntheticTargetAttribution"):
        record("gq-ta-schema", not validate(gq["syntheticTargetAttribution"], TA, "#"), selector="target-attribution.schema.v1.json", detail=validate(gq["syntheticTargetAttribution"], TA, "#")[:4], class_="schema", req="R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR")
    record("gq-evidence-coverageIds-from-selected-views", bool(gq["responses"]["neighbors"]["context"]["evidence"]["coverageIds"]), selector="query-projection-contract.v3.md §6 Graph operations require GraphEvidenceDisclosure coverageIds/scopeIds from selected views", class_="semantic", req="R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR")

    # cited-only standing vectors: inhabitance of a distinction document, not execution
    for rid, rel in [
        ("R-HOST-CAPTURED-VS-CANDIDATE", "vectors/host-captured-vs-candidate.json"),
        ("R-CANDIDATE-ONLY-CLONES", "vectors/candidate-only-clones.json"),
        ("R-PROMISE-VS-AVAILABILITY", "vectors/promise-vs-availability.json"),
        ("R-SEMANTIC-VS-OPERATIONAL-AUTHORITY", "vectors/semantic-vs-operational.json"),
        ("R-MUTATION-VS-ANALYSIS-STEPS", "vectors/mutation-vs-analysis-steps.json"),
        ("R-SUBSYSTEM-OWNERS", "vectors/subsystem-owners.json"),
        ("R-MULTI-UNIT-MISSING-CAPS", "vectors/multi-unit-missing-caps.json"),
        ("R-EMPTY-PARTIAL-UNAVAILABLE-MISSING", "vectors/empty-partial-unavailable-missing.json"),
        ("R-DETECTOR-COMPAT-FILE", "vectors/detector-compat-file.json"),
        ("R-CHAIN-ZERO-CONFIG-TO-RECEIPT", "vectors/chain-zero-config-to-receipt.json"),
    ]:
        obj = load(rel)
        record(f"artifact-present-{rid}", isinstance(obj, dict) and len(obj) > 0, selector="file presence only; semantic execution assessed separately", class_="check", req=rid)

    # detector-compat: distinguish listing file vs manifest
    det = load("vectors/detector-compat-file.json")
    record("detector-compat-distinguishes-listing-vs-manifest", det.get("listingFile") and "manifest" in json.dumps(det.get("not", "")).lower(), selector="R-DETECTOR-COMPAT-FILE reserved authenticated file, not the component manifest body", class_="semantic", req="R-DETECTOR-COMPAT-FILE")

    empty = load("vectors/empty-partial-unavailable-missing.json")
    record("empty-partial-unavailable-missing-four-states-named", all(k in empty for k in ("completeEmpty", "partial", "unavailable", "missingCommittedBytes")) and empty.get("distinct") is True, selector="R-EMPTY-PARTIAL-UNAVAILABLE-MISSING four distinct states", detail=list(empty), class_="semantic", req="R-EMPTY-PARTIAL-UNAVAILABLE-MISSING")

    results = {
        "probeCount": len(PROBES),
        "passCount": sum(1 for p in PROBES if p["ok"]),
        "failCount": sum(1 for p in PROBES if not p["ok"]),
        "firstRefusal": FIRST,
        "probes": PROBES,
        "failed": [p for p in PROBES if not p["ok"]],
    }
    outp = OUT / "diagnostics" / "workflow_scope_probes.json"
    outp.write_text(json.dumps(results, indent=2, default=str) + "\n")
    print(json.dumps({"probeCount": results["probeCount"], "passCount": results["passCount"], "failCount": results["failCount"], "firstRefusal": None if FIRST is None else FIRST["name"], "failedNames": [p["name"] for p in results["failed"]]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
