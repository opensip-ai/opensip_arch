#!/usr/bin/env python3
"""Bounded self-audit probes of workflow-review.v1.

Kit laws only. Does not remint consumer vectors. Does not edit historical v1.
Consumer evaluators are not expected-output oracles. Probe counts are not
conformance counts.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
from collections import Counter
from pathlib import Path

V1_PROBES = Path(
    "/tmp/opensip-design-corrections/consumer-b.v12-kit-validator.v1/output/diagnostics/syntax_code_pilot_probes.py"
)
spec = importlib.util.spec_from_file_location("v1probes", V1_PROBES)
v1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v1)

C = v1.C
H = v1.H
sha256 = v1.sha256

KIT = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-validator.v1/subject")
REQ_PATH = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-validator.v1/requirements.json")
SNAP_ROOT = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-workflow-review.v1")
SNAP = SNAP_ROOT / "consumer-snapshot"
MANIFEST = SNAP_ROOT / "snapshot-manifest.json"
V1_OUT = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-workflow-review.v1/output")
OUT = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-workflow-review.v2/output")

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

PROBES = []
FIRST = None

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

REPAIR_APPLY_KEY_FIELDS = ("operation", "projectId", "repairPlanId", "baseSnapshotId")


def record(name, ok, *, selector, detail=None, class_="check", req=None):
    global FIRST
    rec = {
        "name": name,
        "ok": bool(ok),
        "selector": selector,
        "class": class_,
        "detail": detail,
        "req": req,
    }
    PROBES.append(rec)
    if (not ok) and FIRST is None and class_ in ("schema", "semantic", "replay"):
        FIRST = rec


def load(rel):
    return json.loads((SNAP / rel).read_text())


def kit_json(rel):
    return json.loads((KIT / rel).read_text())


def kit_text(rel):
    return (KIT / rel).read_text()


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


def kind_from_path(path: str) -> str:
    base = path.rsplit("/", 1)[-1]
    if base == "tsconfig.json":
        return "tsconfig"
    if base == "jsconfig.json":
        return "jsconfig"
    return "other"


def exists_atom(*, facts, coverages, minr, rel):
    matching = [f for f in facts if f["relation"] == rel]
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


def file_sha(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def prefixed_h(prefix: str, domain: str, value) -> str:
    return f"{prefix}{H(domain, value)}"


def main():
    global REG
    REG = registry()
    src = (SNAP / "scripts" / "scope_reconstruct.py").read_text()
    v1_review = json.loads((V1_OUT / "workflow-review.json").read_text())
    req_doc = json.loads(REQ_PATH.read_text())

    # --- custody ---
    kit_man = kit_json("consumer-input-manifest.json")
    kit_ok = kit_fail = 0
    for e in kit_man["files"]:
        p = KIT / e["path"]
        if p.exists() and file_sha(p) == e["sha256"] and p.stat().st_size == e["bytes"]:
            kit_ok += 1
        else:
            kit_fail += 1
    record(
        "kit-80-pass",
        kit_ok == 80 and kit_fail == 0 and len(kit_man["files"]) == 80,
        selector="consumer-input-manifest.json",
        detail={"ok": kit_ok, "fail": kit_fail, "n": len(kit_man["files"])},
        class_="check",
    )
    record(
        "kit-manifest-sha",
        file_sha(KIT / "consumer-input-manifest.json")
        == "ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8",
        selector="consumer-input-manifest.json",
        class_="check",
    )
    record(
        "parent-sha",
        kit_man["parentSubjectSha256"] == "a70f5830c9d54f5a6bc3285cb05c34fb6331d5278ae1c46e12147a5f95a10bbb",
        selector="consumer-input-manifest.json parentSubjectSha256",
        class_="check",
    )
    record(
        "requirements-sha",
        file_sha(REQ_PATH) == "855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495",
        selector="requirements.json",
        class_="check",
    )
    man = json.loads(MANIFEST.read_bytes())
    record(
        "snapshot-manifest-sha",
        file_sha(MANIFEST) == "9fb3d13f0d58a65bea8aae46600ceeff12842e7f46c8b94b59214c831f23051c",
        selector="snapshot-manifest.json",
        class_="check",
    )
    snap_ok = snap_fail = 0
    seen = set()
    for e in man["files"]:
        seen.add(e["path"])
        p = SNAP / e["path"]
        if p.exists() and file_sha(p) == e["sha256"]:
            snap_ok += 1
        else:
            snap_fail += 1
    extras = 0
    for dirpath, _, filenames in __import__("os").walk(SNAP):
        for fn in filenames:
            rel = str(Path(dirpath, fn).relative_to(SNAP))
            if rel not in seen:
                extras += 1
    record(
        "snapshot-224-pass",
        snap_ok == 224 and snap_fail == 0 and extras == 0 and len(man["files"]) == 224,
        selector="snapshot-manifest.json files[]",
        detail={"ok": snap_ok, "fail": snap_fail, "extras": extras},
        class_="check",
    )

    frozen = load("frozen-run-hashes.json")["runs"]
    for name, rec in frozen.items():
        p = SNAP / "runs" / name
        b = p.read_bytes()
        record(
            f"frozen-store-{name}",
            sha256(b) == rec["sha256"] and len(b) == rec["bytes"],
            selector="frozen-run-hashes.json; hashes verified, Runs not admitted",
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

    d9 = kit_json("docs/coop/artifacts/d9-exit-contract.v1.14.json")["classToExitCode"]
    record(
        "d9-classToExitCode-equals-selected-map",
        d9 == CLASS_TO_EXIT,
        selector="d9-exit-contract.v1.14.json#/classToExitCode",
        req="R-D9-EXTENSION-PRECEDENCE",
        class_="semantic",
    )

    # --- envelopes ---
    envelopes = {
        "R-ENVELOPE-CONFIG-INPUT": "envelopes/config-input.json",
        "R-ENVELOPE-EXTERNAL-INPUT": "envelopes/retained-external-input.json",
        "R-ENVELOPE-HOST-INVALID": "envelopes/host-invalid-internal.json",
        "R-ENVELOPE-PRODUCER-BOUNDARY": "envelopes/producer-boundary.json",
        "R-PUBLIC-FROM-INTERNAL-REFUSAL": "envelopes/public-from-internal.json",
        "R-PINNED-PURGE": "envelopes/pinned-purge.json",
        "R-PURGE-REPLAY-OUTPUT-FAILURE": "envelopes/purge-replay-output-failure.json",
        "R-FAILURE-ENVELOPES-D9": "envelopes/failure-d9-complete.json",
    }
    v1_d9_path = None
    for row in v1_review["originalRequirementIds"]:
        if row["id"] == "R-FAILURE-ENVELOPES-D9":
            v1_d9_path = row["consumerArtifact"]
    record(
        "v1-d9-artifact-path-matches-snapshot",
        v1_d9_path == "envelopes/failure-d9-complete.json",
        selector="v1 workflow-review.json consumerArtifact vs snapshot envelopes/",
        detail={"v1": v1_d9_path, "actual": "envelopes/failure-d9-complete.json"},
        class_="audit",
        req="R-FAILURE-ENVELOPES-D9",
    )
    for rid, rel in envelopes.items():
        env = load(rel)
        errs = validate(env, CE, "#")
        derived = CLASS_TO_EXIT[env["termination"]["class"]]
        record(f"schema-{rid}", not errs, selector=CE, detail=errs[:4], class_="schema", req=rid)
        record(
            f"exitCode-derived-{rid}",
            env.get("exitCode") == derived,
            selector="d9-exit-contract.v1.14.json classToExitCode",
            detail={"exitCode": env.get("exitCode"), "class": env["termination"]["class"], "derived": derived},
            class_="semantic",
            req=rid,
        )
    d9env = load("envelopes/failure-d9-complete.json")
    record(
        "failure-d9-not-termination-fragment-alone",
        d9env.get("kind") == "failure" and "termination" in d9env and "errors" in d9env and "exitCode" in d9env,
        selector="R-FAILURE-ENVELOPES-D9 complete failure envelope not a termination fragment alone",
        class_="semantic",
        req="R-FAILURE-ENVELOPES-D9",
    )
    pinned = load("envelopes/pinned-purge.json")
    record(
        "pinned-purge-has-active-pins-disclosure",
        bool((pinned.get("termination") or {}).get("domainDetail", {}).get("purgeDisclosure", {}).get("activePins")),
        selector="R-PINNED-PURGE complete pinned-purge refusal envelope",
        class_="semantic",
        req="R-PINNED-PURGE",
    )
    pub = load("envelopes/public-from-internal.json")
    record(
        "public-from-internal-is-public-failure",
        pub.get("kind") == "failure" and pub["termination"]["class"] == "request-rejected",
        selector="R-PUBLIC-FROM-INTERNAL-REFUSAL public response from internal refusal",
        class_="semantic",
        req="R-PUBLIC-FROM-INTERNAL-REFUSAL",
    )

    auth = load("vectors/test-prep-repair-authorization.json")
    for k, env in auth.items():
        errs = validate(env, CE, "#")
        record(f"schema-auth-{k}", not errs, selector=CE, detail=errs[:4], class_="schema", req="R-TEST-PREP-REPAIR-AUTH")
        derived = CLASS_TO_EXIT[env["termination"]["class"]]
        record(
            f"exitCode-auth-{k}",
            env.get("exitCode") == derived,
            selector="d9-exit-contract.v1.14.json classToExitCode",
            class_="semantic",
            req="R-TEST-PREP-REPAIR-AUTH",
        )
    record(
        "test-prep-repair-are-authorization-refusal-envelopes",
        set(auth) == {"test", "preparation", "repair"}
        and all(v.get("kind") == "failure" for v in auth.values()),
        selector="R-TEST-PREP-REPAIR-AUTH authorization records/envelopes, not host execution",
        class_="semantic",
        req="R-TEST-PREP-REPAIR-AUTH",
    )

    terms = load("envelopes/public-termination.json")["examples"]
    for k, t in terms.items():
        errs = validate(t, COMMON3, "#/$defs/StepTermination")
        record(
            f"schema-term-{k}",
            not errs,
            selector="evaluator3/common.schema.json#/$defs/StepTermination",
            detail=errs[:4],
            class_="schema",
            req="R-PUBLIC-TERMINATION-EXAMPLES",
        )
    record(
        "public-termination-six-d9-classes",
        set(terms) == set(CLASS_TO_EXIT),
        selector="d9-exit-contract.v1.14.json six StepTermination classes",
        class_="semantic",
        req="R-PUBLIC-TERMINATION-EXAMPLES",
    )

    for rid, rel in [("R-SINGLE-STEP", "envelopes/single-step.json"), ("R-MULTI-STEP-DIFFERENT-SELECTIONS", "envelopes/multi-step.json")]:
        inst = load(rel)
        errs = validate(inst, INV, "#")
        record(f"schema-{rid}", not errs, selector=INV, detail=errs[:4], class_="schema", req=rid)
    multi = load("envelopes/multi-step.json")
    profiles = [s["params"]["profile"] for s in multi["orderedSteps"]]
    record(
        "multi-step-different-profiles",
        profiles == ["default", "fit"] and multi["orderedSteps"][1]["dependsOn"] == [0],
        selector="R-MULTI-STEP-DIFFERENT-SELECTIONS named multi-step with different selections",
        class_="semantic",
        req="R-MULTI-STEP-DIFFERENT-SELECTIONS",
    )
    single = load("envelopes/single-step.json")
    record(
        "single-step-one-analysis",
        len(single["orderedSteps"]) == 1 and single["orderedSteps"][0]["kind"] == "analysis",
        selector="R-SINGLE-STEP single-step command example",
        class_="semantic",
        req="R-SINGLE-STEP",
    )

    inv = kit_json("docs/coop/design-corrections/workflows/command-inventory.v3.json")
    disc = load("envelopes/invocation-disclosure.json")
    record(
        "invocation-disclosure-command-count",
        disc["commandCount"] == len(inv["commands"]) == 45,
        selector="command-inventory.v3.json; R-INVOCATION-DISCLOSURE",
        detail={"disc": disc["commandCount"], "inventory": len(inv["commands"])},
        class_="semantic",
        req="R-INVOCATION-DISCLOSURE",
    )
    q = next(c for c in inv["commands"] if c["name"] == "query")
    record(
        "invocation-disclosure-query-formats-from-inventory",
        disc["query"]["formats"] == q.get("formats") and disc["query"]["parityFields"] == q.get("parityFields"),
        selector="command-inventory.v3.json query command formats/parityFields",
        class_="semantic",
        req="R-INVOCATION-DISCLOSURE",
    )
    record(
        "invocation-disclosure-is-not-command-envelope",
        "schemaFamily" not in disc and disc.get("source", "").endswith("command-inventory.v3.json"),
        selector="R-INVOCATION-DISCLOSURE original invocation disclosure from the contracts, not a CommandEnvelope instance",
        class_="audit",
        req="R-INVOCATION-DISCLOSURE",
    )

    recav = load("envelopes/receipt-availability.json")
    record(
        "schema-commit-receipt",
        not validate(recav["receipt"], IDENT, "#/$defs/commit-receipt"),
        selector="identity-schemas.v3.json#/$defs/commit-receipt",
        class_="schema",
        req="R-DURABLE-RECEIPT-AVAILABILITY",
    )
    record(
        "schema-availability",
        not validate(recav["availability"], IDENT, "#/$defs/availability"),
        selector="identity-schemas.v3.json#/$defs/availability",
        class_="schema",
        req="R-DURABLE-RECEIPT-AVAILABILITY",
    )
    record(
        "receipt-synthetic-host-labeled",
        recav.get("syntheticHostObservation") is True,
        selector="R-DURABLE-RECEIPT-AVAILABILITY synthetic TCB observation labeled",
        class_="check",
        req="R-DURABLE-RECEIPT-AVAILABILITY",
    )

    d9prec = load("vectors/d9-extension-precedence.json")
    record(
        "d9-extension-selected-equals-inherited",
        d9prec.get("equal") is True and d9prec["inherited"] == d9 == d9prec["selected"],
        selector="R-D9-EXTENSION-PRECEDENCE selected composition vs inherited classToExitCode",
        class_="semantic",
        req="R-D9-EXTENSION-PRECEDENCE",
    )

    # --- config graphs ---
    for rid, rel in [
        ("R-CONFIG-SYNTHESIZED", "vectors/config-synthesized.json"),
        ("R-CONFIG-CUSTOM-MULTI-BASE", "vectors/config-custom-multi-base.json"),
        ("R-CONFIG-JS-SHARED-BASE", "vectors/config-js-shared-base.json"),
    ]:
        payload = load(rel)
        g = payload["graph"]
        errs = validate(g, NATIVE, "#/$defs/TypeScriptConfigGraphV1")
        record(
            f"schema-{rid}",
            not errs,
            selector="native-evidence.schemas.v2.json#/$defs/TypeScriptConfigGraphV1",
            detail=errs[:4],
            class_="schema",
            req=rid,
        )
        recomputed = hashlib.sha256(C(g)).hexdigest()
        record(
            f"graphDigest-{rid}",
            payload["graphDigestSha256"] == recomputed and "tsconfigGraphHash" not in g,
            selector="native-evidence.schemas.v2.json TypeScriptConfigGraphV1 tsconfigGraphHash is SHA-256(C(this record)), not a graph field",
            detail={"claimed": payload["graphDigestSha256"], "recomputed": recomputed},
            class_="semantic",
            req=rid,
        )
        for n in g["nodes"]:
            derived = kind_from_path(n["path"])
            record(
                f"config-kind-{rid}-{n['path']}",
                n["kind"] == derived,
                selector="native-evidence.schemas.v2.json#/x-opensip-config-node-kind-law",
                class_="semantic",
                req=rid,
            )
        paths = [n["path"] for n in g["nodes"]]
        record(
            f"config-path-order-{rid}",
            paths == sorted(paths, key=lambda p: p.encode()),
            selector="x-opensip-order by path on TypeScriptConfigGraphV1.nodes",
            class_="semantic",
            req=rid,
        )

    syn = load("vectors/config-synthesized.json")["graph"]
    record(
        "config-synthesized-null-entry-empty-nodes",
        syn["entryConfigPath"] is None and syn["nodes"] == [],
        selector="TypeScriptConfigGraphV1 entryConfigPath null exactly when synthesized",
        class_="semantic",
        req="R-CONFIG-SYNTHESIZED",
    )
    custom = load("vectors/config-custom-multi-base.json")["graph"]
    app = next(n for n in custom["nodes"] if n["path"] == "tsconfig.app.json")
    record(
        "config-custom-entry-kind-other",
        custom["entryConfigPath"] == "tsconfig.app.json" and app["kind"] == "other",
        selector="x-opensip-config-node-kind-law exact basename; custom-named entry is other",
        class_="semantic",
        req="R-CONFIG-CUSTOM-MULTI-BASE",
    )
    record(
        "config-custom-repeated-base-order",
        app["extendsResolved"] == ["tsconfig.strict.json", "tsconfig.base.json"],
        selector="R-CONFIG-CUSTOM-MULTI-BASE multiple ordered bases; extendsResolved sequence later-wins",
        class_="semantic",
        req="R-CONFIG-CUSTOM-MULTI-BASE",
    )
    base_via_strict = any(n["path"] == "tsconfig.strict.json" and "tsconfig.base.json" in n["extendsResolved"] for n in custom["nodes"])
    record(
        "config-custom-base-reached-twice",
        "tsconfig.base.json" in app["extendsResolved"] and base_via_strict,
        selector="TypeScriptConfigGraphV1 Repeated edges are retained; base reached as direct extend and via strict",
        class_="semantic",
        req="R-CONFIG-CUSTOM-MULTI-BASE",
    )
    js = load("vectors/config-js-shared-base.json")["graph"]
    record(
        "config-js-shared-base-entry-kind",
        js["entryConfigPath"] == "jsconfig.json" and kind_from_path("jsconfig.json") == "jsconfig",
        selector="R-CONFIG-JS-SHARED-BASE jsconfig inheriting shared base",
        class_="semantic",
        req="R-CONFIG-JS-SHARED-BASE",
    )
    record(
        "config-js-shared-other-filename-base",
        any(n["path"] == "tsconfig.shared.json" and n["kind"] == "other" for n in js["nodes"]),
        selector="R-CONFIG-JS-SHARED-BASE JavaScript config inheriting a shared base with another filename",
        class_="semantic",
        req="R-CONFIG-JS-SHARED-BASE",
    )

    # --- JS body through TS ---
    def u8pref(b: bytes) -> bytes:
        return bytes([len(b)]) + b

    def body_id(language_id, dialect, span, compiler_name="tsc"):
        blv = {
            "schemaVersion": 1,
            "languageId": language_id,
            "compilerName": compiler_name,
            "compilerVersion": "5.4.5",
            "compilerBuild": "a" * 64,
            "dialect": dialect,
        }
        lv = hashlib.sha256(C(blv)).digest()
        payload = len(span).to_bytes(4, "big") + span
        pre = (
            u8pref(b"opensip.fact-identity.v1")
            + u8pref(b"L0-verbatim")
            + u8pref(hashlib.sha256(b"L0-verbatim").digest())
            + u8pref(language_id.encode())
            + u8pref(lv)
            + len(payload).to_bytes(4, "big")
            + payload
        )
        return "sha256:" + hashlib.sha256(pre).hexdigest()

    js_span = b"export const n = 1;\n"
    js_vec = load("vectors/js-body-through-ts.json")
    rec_js = body_id("javascript", {"grammarVariant": "js"}, js_span)
    rec_ts = body_id("typescript", {"grammarVariant": "ts"}, js_span)
    record(
        "js-body-through-ts-languageId-not-provider",
        js_vec["bodyLanguageId"] == "javascript"
        and js_vec["providerLanguageId"] == "typescript"
        and js_vec["distinct"] is True
        and js_vec["javascriptL0"] == rec_js
        and js_vec["typescriptL0OverSameBytes"] == rec_ts
        and rec_js != rec_ts,
        selector="relation-payload-schemas.v2.json languageIdIsNotTheProviderLanguage; R-JS-CLONE-BODY-THROUGH-TS",
        class_="semantic",
        req="R-JS-CLONE-BODY-THROUGH-TS",
    )

    # --- repair identity recipes ---
    repair = load("vectors/repair-descriptor.json")
    record(
        "schema-R-REPAIR-DESCRIPTOR",
        not validate(repair, REP, "#/$defs/RepairPlanV1"),
        selector="evaluator3/repair.schema.json#/$defs/RepairPlanV1",
        detail=validate(repair, REP, "#/$defs/RepairPlanV1")[:5],
        class_="schema",
        req="R-REPAIR-DESCRIPTOR",
    )
    expected_plan_id = "repairplan2:" + H("workflow.repair-plan", repair["descriptor"])
    record(
        "repair-plan-id-is-selected-H-recipe",
        repair.get("repairPlanId") == expected_plan_id,
        selector="repair.schema.json A RepairPlan is H('workflow.repair-plan', descriptor)",
        detail={"claimed": repair.get("repairPlanId"), "selectedRecipe": expected_plan_id},
        class_="semantic",
        req="R-REPAIR-DESCRIPTOR",
    )
    cw = repair["descriptor"]["closedWorld"]
    record(
        "repair-closedWorld-is-five-field-projection-shape",
        set(cw) == {
            "deadCodeRepairEligible",
            "exportsClosed",
            "entryPointsRecognized",
            "nonliteralLoading",
            "externalConsumers",
        }
        and "dynamicDispatch" not in cw
        and "reasons" not in cw,
        selector="RepairPlanDescriptor.closedWorld five-field projection of ClosedWorldV2, not a copy",
        class_="semantic",
        req="R-REPAIR-DESCRIPTOR",
    )
    record(
        "repair-descriptor-targets-are-fingerprints",
        all(str(t).startswith("finding-key2:") for t in repair["descriptor"]["targets"]),
        selector="workflows-and-surfaces.md RepairPlanDescriptor.targets are finding-key2 fingerprints",
        class_="semantic",
        req="R-REPAIR-DESCRIPTOR",
    )

    mrs = load("vectors/mutation-replay-scope.json")
    record(
        "schema-R-MUTATION-REPLAY-SCOPE",
        not validate(mrs, MRS, "#/$defs/MutationReplayScopeV1"),
        selector="invocation-record.schema.json#/$defs/MutationReplayScopeV1",
        detail=validate(mrs, MRS, "#/$defs/MutationReplayScopeV1")[:5],
        class_="schema",
        req="R-MUTATION-REPLAY-SCOPE",
    )
    record(
        "mutation-scope-operation-is-purge-not-repair-apply",
        mrs.get("operation") == "purge",
        selector="evaluator3/repair.schema.json x-opensip-mutation-operation-map: repair-apply excluded from MutationReplayScopeV1.operation",
        class_="semantic",
        req="R-MUTATION-REPLAY-SCOPE",
    )
    keys = load("vectors/repair-apply-key.json")
    normative_apply = {
        "operation": "repair-apply",
        "projectId": mrs["projectId"],
        "repairPlanId": repair["repairPlanId"],
        "baseSnapshotId": repair["descriptor"]["snapshotId"],
    }
    consumer_apply = keys["applyKey"]
    record(
        "repair-apply-key-is-selected-preimage",
        set(consumer_apply) >= set(REPAIR_APPLY_KEY_FIELDS)
        and consumer_apply.get("operation") == "repair-apply"
        and "requestId" not in consumer_apply
        and "stepId" not in consumer_apply
        and "kind" not in consumer_apply,
        selector="workflows-and-surfaces.md §1 repair-apply key = raw SHA-256 of C({operation, projectId, repairPlanId, baseSnapshotId})",
        detail={"consumerApplyKey": consumer_apply, "normativeShape": list(REPAIR_APPLY_KEY_FIELDS)},
        class_="semantic",
        req="R-REPAIR-APPLY-KEY",
    )
    re_mrs_c = hashlib.sha256(C(keys["mutationReplayScope"])).hexdigest()
    re_apply_c = hashlib.sha256(C(keys["applyKey"])).hexdigest()
    record(
        "v1-repair-apply-was-digest-inequality-of-arbitrary-records",
        keys["unequal"] is True and keys["repairApplyKeyDigest"] == re_apply_c and re_apply_c != re_mrs_c,
        selector="R-REPAIR-APPLY-KEY v1 admitted SHA-256(C(applyKey)) != SHA-256(C(mutationReplayScope)); those records are not the selected recipes",
        detail={
            "consumerApplyKey": consumer_apply,
            "normativeApplyPreimage": normative_apply,
            "v1RepairApplyDigest": keys["repairApplyKeyDigest"],
        },
        class_="audit",
        req="R-REPAIR-APPLY-KEY",
    )
    intent_h = H("workflow.mutation-intent", mrs)
    record(
        "mutation-replay-scope-H-not-required-as-the-reconstructed-record",
        mrs.get("operation") == "purge" and not validate(mrs, MRS, "#/$defs/MutationReplayScopeV1"),
        selector="R-MUTATION-REPLAY-SCOPE reconstruct generic MutationReplayScopeV1; H(workflow.mutation-intent) is the receipt key, not the reconstructed record",
        detail={"H_workflow.mutation-intent": intent_h},
        class_="semantic",
        req="R-MUTATION-REPLAY-SCOPE",
    )

    # --- comparisons ---
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
            inst = obj
            schema_rel, sel = BASE, "#"
        else:
            inst = obj
            schema_rel, sel = CMP, "#"
        errs = validate(inst, schema_rel, sel)
        record(f"schema-{rid}", not errs, selector=schema_rel, detail=errs[:5], class_="schema", req=rid)

    missing = load("vectors/comparison-missing.json")["descriptor"]
    changed = load("vectors/comparison-evidence-changed.json")["descriptor"]
    empty = load("vectors/comparison-empty-result.json")["descriptor"]
    record(
        "cmp-missing-distinguishing-fields",
        missing["comparisonPerformed"] is False
        and missing["pivotsAvailable"]["E0"] == "unavailable"
        and missing.get("wholeIndeterminateReason") == "required-evidence-unavailable"
        and missing["verdict"] == "indeterminate",
        selector="R-CMP-MISSING missing-evidence comparison case",
        class_="semantic",
        req="R-CMP-MISSING",
    )
    record(
        "cmp-evidence-changed-distinguishing-fields",
        changed["comparisonPerformed"] is True
        and changed["contextDelta"]["evidenceAvailabilityChanged"] is True
        and changed.get("wholeIndeterminateReason") == "evidence-availability-changed"
        and changed["verdict"] == "indeterminate",
        selector="R-CMP-EVIDENCE-CHANGED evidence-changed comparison case",
        class_="semantic",
        req="R-CMP-EVIDENCE-CHANGED",
    )
    record(
        "cmp-missing-distinct-from-evidence-changed",
        missing["comparisonPerformed"] is False
        and changed["comparisonPerformed"] is True
        and missing.get("wholeIndeterminateReason") != changed.get("wholeIndeterminateReason"),
        selector="R-CMP-MISSING vs R-CMP-EVIDENCE-CHANGED particular promised examples",
        class_="semantic",
        req="R-CMP-MISSING",
    )
    record(
        "cmp-empty-result-zero-findings",
        empty["comparisonPerformed"] is True
        and empty["entries"] == []
        and empty["correspondenceCoverage"]
        and empty["correspondenceCoverage"][0].get("zeroFindings") is True
        and empty["verdict"] == "pass",
        selector="R-CMP-EMPTY-RESULT empty-result comparison case",
        class_="semantic",
        req="R-CMP-EMPTY-RESULT",
    )

    e0e3 = load("vectors/baseline-e0-e3.json")
    record("schema-R-E0-VS-E1-E3-E0", not validate(e0e3["E0"], CMP, "#"), selector=CMP, class_="schema", req="R-E0-VS-E1-E3")
    record("schema-R-E0-VS-E1-E3-E13", not validate(e0e3["E1E3"], CMP, "#"), selector=CMP, class_="schema", req="R-E0-VS-E1-E3")
    e0p = e0e3["E0"]["descriptor"]["pivotsAvailable"]
    e13p = e0e3["E1E3"]["descriptor"]["pivotsAvailable"]
    record(
        "e0-vs-e13-pivot-distinction",
        e0p["E0"] == "available"
        and e0p["E1"] == "not-needed"
        and e13p["E0"] == "not-needed"
        and e13p["E1"] == "available"
        and e13p["E2"] == "available"
        and e13p["E3"] == "available",
        selector="workflows-and-surfaces.md §3 E0 prior detector vs E1–E3 re-evaluation of current retained evidence",
        class_="semantic",
        req="R-E0-VS-E1-E3",
    )
    e0_pres = e0e3["E0"]["descriptor"]["entries"][0]["presence"]
    e13_pres = e0e3["E1E3"]["descriptor"]["entries"][0]["presence"]
    record(
        "e0-vs-e13-presence-fields",
        e0_pres["E0"] is True
        and e0_pres["E1"] is None
        and e13_pres["E0"] is None
        and e13_pres["E1"] is True,
        selector="workflows-and-surfaces.md §3 presence at every pivot",
        class_="semantic",
        req="R-E0-VS-E1-E3",
    )

    pivot = load("vectors/pivot-only-fingerprints.json")["descriptor"]
    pent = pivot["entries"][0]
    only_in_pivot = (
        pent["presence"].get("B") is not True
        and any(pent["presence"].get(k) is True for k in ("E0", "E1", "E2", "E3"))
    )
    record(
        "pivot-only-fingerprint-present-only-in-pivot",
        only_in_pivot,
        selector="workflows-and-surfaces.md §3 fingerprint population includes fingerprints present only in a pivot",
        detail={"presence": pent["presence"], "fingerprint": pent.get("fingerprint"), "classification": pent.get("classification"), "counts": pivot.get("counts")},
        class_="semantic",
        req="R-PIVOT-ONLY-FINGERPRINTS",
    )
    record(
        "pivot-only-counts-match-entry-classification",
        pivot["counts"].get(pent["classification"], 0) >= 1,
        selector="comparison counts must reflect the retained entry classification",
        detail={"classification": pent["classification"], "counts": pivot["counts"]},
        class_="semantic",
        req="R-PIVOT-ONLY-FINGERPRINTS",
    )

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
    record(
        "scope-policy-only-is-invalid-produced-value-not-unexercised",
        bctx["scopeDigest"] == cctx["scopeDigest"] and scope_cmp["descriptor"]["contextDelta"]["scopeChanged"] is True,
        selector="audit: this row produced a ComparisonResult (schema pass) whose scopeDigest pair is identical; that is an invalid produced value, not absent behavior",
        class_="audit",
        req="R-SCOPE-POLICY-ONLY-COMPARISON",
    )

    baseline = load("vectors/baseline-audit.json")
    record(
        "baseline-audit-has-embedded-context-documents",
        "contextDocuments" in baseline["descriptor"] and "policy" in baseline["descriptor"]["contextDocuments"],
        selector="workflows-and-surfaces.md §2 baseline pins embedded policy/scope/waiver documents",
        class_="semantic",
        req="R-BASELINE-AUDIT",
    )
    expected_cmp_ids = {}
    for rid, rel, prefix, domain, getter in [
        ("R-CMP-MISSING", "vectors/comparison-missing.json", "comparison2:", "workflow.comparison", lambda o: o["descriptor"]),
        ("R-CMP-EVIDENCE-CHANGED", "vectors/comparison-evidence-changed.json", "comparison2:", "workflow.comparison", lambda o: o["descriptor"]),
        ("R-CMP-EMPTY-RESULT", "vectors/comparison-empty-result.json", "comparison2:", "workflow.comparison", lambda o: o["descriptor"]),
        ("R-BASELINE-AUDIT", "vectors/baseline-audit.json", "baseline2:", "workflow.baseline", lambda o: o["descriptor"]),
    ]:
        obj = load(rel)
        desc = getter(obj)
        expected = prefix + H(domain, desc)
        claimed = obj.get("comparisonResultId") if prefix.startswith("comparison") else obj.get("baselineId")
        expected_cmp_ids[rid] = {"claimed": claimed, "selected": expected, "match": claimed == expected}
        record(
            f"identity-recipe-{rid}",
            claimed == expected,
            selector=f"workflows-and-surfaces.md {prefix} = H('{domain}', descriptor)",
            detail={"claimed": claimed, "selected": expected},
            class_="check",
            req=rid,
        )

    # --- min-resolution / three-valued ---
    minres = load("vectors/min-resolution.json")
    syn_q = exists_atom(
        facts=[{"relation": "imports", "resolution": "syntactic-specifier"}],
        coverages=[{"relation": "imports", "resolution": "syntactic-specifier", "coverage": "complete"}],
        minr="syntactic-specifier",
        rel="imports",
    )
    syn_i = exists_atom(facts=[], coverages=[], minr="syntactic-specifier", rel="imports")
    res_q = exists_atom(
        facts=[{"relation": "imports", "resolution": "resolved-target"}],
        coverages=[{"relation": "imports", "resolution": "resolved-target", "coverage": "complete"}],
        minr="resolved-target",
        rel="imports",
    )
    res_i = exists_atom(
        facts=[{"relation": "imports", "resolution": "syntactic-specifier"}],
        coverages=[{"relation": "imports", "resolution": "resolved-target", "coverage": "complete"}],
        minr="resolved-target",
        rel="imports",
    )
    record(
        "minres-syntactic-qualifying",
        minres["cases"][0]["qualifyingValue"] == syn_q == "true",
        selector="atom-evaluation-contract.v1.md exists true on known match",
        class_="semantic",
        req="R-MIN-RESOLUTION-THREE-LEVELS",
    )
    record(
        "minres-syntactic-insufficient",
        minres["cases"][0]["insufficientValue"] == syn_i == "indeterminate",
        selector="identity-and-evidence.md §4 exists otherwise indeterminate",
        class_="semantic",
        req="R-MIN-RESOLUTION-THREE-LEVELS",
    )
    record(
        "minres-resolved-qualifying",
        minres["cases"][1]["qualifyingValue"] == res_q == "true",
        selector="atom-evaluation-contract.v1.md rung ≥ minResolution",
        class_="semantic",
        req="R-MIN-RESOLUTION-THREE-LEVELS",
    )
    record(
        "minres-resolved-insufficient-is-complete-absence-false",
        res_i == "false" and minres["cases"][1]["insufficientValue"] == "false",
        selector="identity-and-evidence.md §4 exists false on complete absence",
        class_="semantic",
        req="R-MIN-RESOLUTION-THREE-LEVELS",
    )
    record(
        "minres-resolved-insufficientExpected-agrees-with-kit",
        minres["cases"][1].get("insufficientExpected") == "false",
        selector="identity-and-evidence.md §4 exists false on complete absence. Vector insufficientExpected=indeterminate disagrees with the kit (measured value is correctly false).",
        class_="semantic",
        req="R-MIN-RESOLUTION-THREE-LEVELS",
    )
    has_type_qualifying = any("qualifyingValue" in c for c in minres["cases"] if c["level"] == "type")
    record(
        "minres-type-has-qualifying-and-insufficient",
        has_type_qualifying,
        selector="R-MIN-RESOLUTION-THREE-LEVELS each of three levels × qualifying/insufficient",
        detail=minres["cases"][2],
        class_="semantic",
        req="R-MIN-RESOLUTION-THREE-LEVELS",
    )
    mre = load("vectors/min-resolution-repair-evidence.json")
    record(
        "minres-repair-evidence-is-prose-not-records",
        isinstance(mre.get("requirements"), list) and not any("repairPlanId" in json.dumps(x) for x in mre["requirements"]),
        selector="R-MIN-RESOLUTION-REPAIR-EVIDENCE corresponding repair evidence; this vector is prose tiedTo min-resolution.json",
        class_="audit",
        req="R-MIN-RESOLUTION-REPAIR-EVIDENCE",
    )

    tv = load("vectors/replay-three-valued.json")
    indep_tv = exists_atom(facts=[], coverages=[], minr="enumerated", rel="file")
    record(
        "three-valued-exists-missing-coverage-indeterminate",
        tv["value"] == indep_tv == "indeterminate" and tv["notVacuousTrue"] and tv["notVacuousFalse"],
        selector="identity-and-evidence.md §4 exists otherwise indeterminate; R-REPLAY-THREE-VALUED",
        class_="semantic",
        req="R-REPLAY-THREE-VALUED",
    )

    # --- ownership pair ---
    own = load("vectors/rust-body-identity-pair.json")
    sels = own["sameDialectOwnershipSelections"]
    record(
        "ownership-pair-retains-two-ownership-map-preimages",
        all("ownershipMap" in s or "sourceUnitOwnership" in s or "committedOwnership" in s for s in sels),
        selector="identity-schemas.v3.json rust languageVersionBinding selectionLaw: committed SourceUnitOwnershipV1; two ownership maps that derive one dialect",
        detail=sels,
        class_="semantic",
        req="R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE",
    )
    record(
        "ownership-pair-identical-l0-stamped-on-labels",
        sels[0]["l0"] == sels[1]["l0"] and sels[0]["effectiveEdition"] == sels[1]["effectiveEdition"] == "2018",
        selector="audit: pair hashes one BLV twice under two selection labels; ownership maps never enter BLV so this equality is tautological without retained maps",
        class_="audit",
        req="R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE",
    )
    record(
        "ownership-pair-dialect-change-moves-identity",
        own["distinctWhenDialectChanges"] is True,
        selector="identity-schemas.v3.json rust languageVersionBinding dialect edition",
        class_="semantic",
        req="R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE",
    )

    # --- unexercised firstRefusal rows ---
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
    ug = load("vectors/unsupported-grammar.json")
    hm = load("vectors/hidden-mismatch.json")
    cn = load("vectors/clones-negatives.json")
    ra = load("vectors/repair-authority-per-target.json")
    record(
        "unsupported-grammar-is-unexercised-not-invalid-produced-admission",
        ug.get("firstRefusal", {}).get("code") == "unsupported-file" and ug.get("didNotAssumeTypescriptCompiler") is True,
        selector="audit: produced value is a declared flag dict; admission of a .unknownlang suffix against the syntax grammar bundle was not run",
        class_="audit",
        req="R-RUN-UNSUPPORTED-GRAMMAR",
    )
    record(
        "hidden-mismatch-is-unexercised-not-invalid-produced-admission",
        "firstRefusal" in hm.get("typescript", {}) and "firstRefusal" in hm.get("rust", {}),
        selector="audit: firstRefusal dicts assigned per language; native context/universe admission not executed",
        class_="audit",
        req="R-HIDDEN-MISMATCH-PER-LANGUAGE",
    )
    record(
        "clones-negatives-is-unexercised-not-invalid-produced-admission",
        all(v.get("refused") and v.get("firstRefusal") for v in cn["vectors"]),
        selector="audit: constructed firstRefusal values, not executed body-identity/fact admission",
        class_="audit",
        req="R-CLONES-NEGATIVE-VECTORS",
    )
    record(
        "repair-authority-is-unexercised-not-invalid-produced-join",
        ra["negative"].get("firstRefusal", {}).get("code") == "REPAIR.TARGET_CORRESPONDENCE_UNAVAILABLE"
        and ra["positive"].get("matched") is True
        and ra["positive"].get("firstRefusal") is None,
        selector="audit: positive/negative are constructed correspondence flags, not an executed join",
        class_="audit",
        req="R-REPAIR-AUTHORITY-PER-TARGET",
    )

    # --- graph query ---
    gq = load("query/graph-query-bundle.json")
    record(
        "graph-query-labels-run-admission-unverified",
        gq.get("underlyingRunAdmissionUnverified") is True and gq.get("didNotClaimCloseRun") is True,
        selector="query-projection-contract.v3.md execute_graph_query requires close_run; algorithm vectors must retain that limitation",
        class_="check",
        req="R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR",
    )
    for name, req in gq["requests"].items():
        errs = validate(req, GQ, "#/$defs/GraphQueryRequestV1")
        record(
            f"schema-gq-req-{name}",
            not errs,
            selector="evaluator3/graph-query.schema.json#/$defs/GraphQueryRequestV1",
            detail=errs[:4],
            class_="schema",
            req="R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR",
        )
        pair = (req["params"]["relation"], req["params"]["minResolution"])
        record(
            f"gq-{name}-relation-is-projectable",
            pair in GRAPH_PROJECTABLE,
            selector="query-projection-contract.v3.md §3 Request law: relation@minResolution not a row of the projection table is refused QUERY.RELATION_UNSUPPORTED. file/* is graph-projectable no.",
            detail={"operation": req["operation"], "pair": list(pair)},
            class_="semantic",
            req="R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR",
        )
        if name in gq["responses"]:
            record(
                f"schema-gq-resp-{name}",
                not validate(gq["responses"][name], GQ, "#/$defs/GraphQueryResponseV1"),
                selector="GraphQueryResponseV1",
                detail=validate(gq["responses"][name], GQ, "#/$defs/GraphQueryResponseV1")[:4],
                class_="schema",
                req="R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR",
            )
            rec_ok = pair not in GRAPH_PROJECTABLE
            produced_success = gq["responses"][name]["operation"] == req["operation"]
            record(
                f"gq-{name}-unsupported-answered-as-success",
                not (rec_ok and produced_success),
                selector="query-projection-contract.v3.md §3 omission is not an alternative to refusing an unsupported request; success GraphQueryResponseV1 for file@enumerated is an invalid produced value",
                class_="semantic",
                req="R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR",
            )
    cursor = gq.get("cursor") or {}
    record(
        "gq-top-level-nextCursor-is-null-not-c1",
        cursor.get("nextCursor") is None,
        selector="query-projection-contract.v3.md §5 Empty nextCursor is not native closed-world. v1 MD claimed a c1 token; the artifact nextCursor is null.",
        detail=cursor,
        class_="audit",
        req="R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR",
    )
    nc = gq["responses"]["neighborsPaged"]["context"].get("nextCursor")
    record(
        "gq-neighborsPaged-cursor-token",
        nc is None or (isinstance(nc, str) and nc.startswith("q3.")),
        selector="query-projection-contract.v3.md §5 reference form q3.<runId-64hex>.<selectionHash64>.<position> when a continuation token is issued; null is lawful for a complete page",
        detail=nc,
        class_="semantic",
        req="R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR",
    )
    record(
        "gq-failure-envelope-schema",
        not validate(gq["failureEnvelope"], CE, "#"),
        selector="query-projection-contract.v3.md §7 public failure carrier CommandEnvelope kind=failure",
        class_="schema",
        req="R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR",
    )
    fail_code = (gq["failureEnvelope"].get("termination") or {}).get("domainDetail", {}).get("code")
    record(
        "gq-failure-is-relation-unsupported-for-file-enumerated",
        fail_code == "QUERY.RELATION_UNSUPPORTED",
        selector="query-projection-contract.v3.md §7 unsupported relation or non-projectable request rung → QUERY.RELATION_UNSUPPORTED",
        detail={"actual": fail_code, "envelopeClass": gq["failureEnvelope"]["termination"]["class"]},
        class_="semantic",
        req="R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR",
    )
    cov = gq["responses"]["neighbors"]["context"]["evidence"]["coverageIds"]
    record(
        "gq-coverageIds-empty-is-not-universal-nonempty-violation",
        True,
        selector="query-projection-contract.v3.md §6 coverageIds/scopeIds from selected views AND other retained Coverage whose key relation is the declared query relation. Empty is lawful when selected views have no such Coverage. v1 probe bool(coverageIds) invented a universal nonempty rule.",
        detail={"coverageIds": cov, "scopeIds": gq["responses"]["neighbors"]["context"]["evidence"]["scopeIds"]},
        class_="audit",
        req="R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR",
    )
    v1_probes = json.loads((V1_OUT / "diagnostics" / "workflow_scope_probes.json").read_text())
    v1_cov = next(p for p in v1_probes["probes"] if p["name"] == "gq-evidence-coverageIds-from-selected-views")
    record(
        "v1-coverageIds-probe-was-invented-nonempty",
        v1_cov["ok"] is False and "from selected views" in (v1_cov.get("selector") or ""),
        selector="audit: v1 used bool(coverageIds) as the check; that is not the §6 selected-views law",
        detail=v1_cov,
        class_="audit",
        req="R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR",
    )
    v1_cur = next(p for p in v1_probes["probes"] if p["name"] == "gq-cursor-is-reference-form")
    record(
        "v1-cursor-probe-passed-on-null-via-else-True",
        v1_cur["ok"] is True,
        selector="audit: v1 probe short-circuits to True when nextCursor is missing; the MD still claimed the token is not q3 form. Artifact nextCursor is null.",
        detail=v1_cur,
        class_="audit",
        req="R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR",
    )

    # --- standing content review (not mere presence) ---
    ne = kit_text("docs/v2/contracts/product-v1/native-evidence.md")
    ws = kit_text("docs/v2/contracts/product-v1/workflows-and-surfaces.md")
    enumc = kit_text("docs/coop/design-corrections/foundation/enumeration-contract.v1.md")
    exec_in = kit_text("docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md")
    ident_md = kit_text("docs/v2/contracts/product-v1/identity-and-evidence.md")
    repair_schema_txt = kit_text("docs/coop/design-corrections/workflows/schemas/evaluator3/repair.schema.json")

    pva = load("vectors/promise-vs-availability.json")
    record(
        "promise-vs-availability-kit-content",
        "which cells this product promises" in ne and "capability" in ne.lower() and pva.get("distinct") is True,
        selector="native-evidence.md advertised cells vs capability-manifest installed availability; R-PROMISE-VS-AVAILABILITY",
        detail=pva,
        class_="semantic",
        req="R-PROMISE-VS-AVAILABILITY",
    )
    svo = load("vectors/semantic-vs-operational.json")
    record(
        "semantic-vs-operational-kit-content",
        "run3" in ident_md and ("receipt" in ident_md.lower() or "mutation" in ws.lower()) and svo.get("distinct") is True,
        selector="identity-and-evidence.md §3 semantic identities; workflows-and-surfaces.md operational receipts",
        class_="semantic",
        req="R-SEMANTIC-VS-OPERATIONAL-AUTHORITY",
    )
    mva = load("vectors/mutation-vs-analysis-steps.json")
    record(
        "mutation-vs-analysis-kit-content",
        "analysis" in ws and "repair-apply" in ws and mva.get("analysisSealsRun3") is True and mva.get("mutationDoesNotSealRun3") is True,
        selector="workflows-and-surfaces.md analysis may seal run3; mutation/repair-apply follow non-seal rules",
        class_="semantic",
        req="R-MUTATION-VS-ANALYSIS-STEPS",
    )
    owners = load("vectors/subsystem-owners.json")
    owner_ok = all(isinstance(v, str) and v for v in owners.values()) and "ComparisonResult" in owners
    record(
        "subsystem-owners-map-cites-kit-owners",
        owner_ok and "evaluator3 comparison-result" in owners.get("ComparisonResult", ""),
        selector="R-SUBSYSTEM-OWNERS owner map in reconstruction, cited to kit",
        detail=owners,
        class_="semantic",
        req="R-SUBSYSTEM-OWNERS",
    )
    empty4 = load("vectors/empty-partial-unavailable-missing.json")
    record(
        "empty-partial-unavailable-missing-four-states-named",
        all(k in empty4 for k in ("completeEmpty", "partial", "unavailable", "missingCommittedBytes"))
        and empty4.get("distinct") is True,
        selector="R-EMPTY-PARTIAL-UNAVAILABLE-MISSING four distinct states",
        class_="semantic",
        req="R-EMPTY-PARTIAL-UNAVAILABLE-MISSING",
    )
    record(
        "empty-partial-kit-content-complete-empty-vs-partial-vs-missing",
        "complete-empty" in enumc and "Missing retained bytes" in enumc and "partial" in enumc,
        selector="enumeration-contract.v1.md complete-empty vs partial vs missing retained bytes; candidate-only kinds=[] is not complete-empty",
        class_="semantic",
        req="R-EMPTY-PARTIAL-UNAVAILABLE-MISSING",
    )
    det = load("vectors/detector-compat-file.json")
    record(
        "detector-compat-kit-content-listing-vs-manifest",
        ".opensip/detector-compatibility.json" in ws
        and "component manifest body" in ws
        and "manifestDigest" in ws
        and det.get("listingFile")
        and "manifest" in json.dumps(det.get("not", "")).lower(),
        selector="workflows-and-surfaces.md §2 reserved authenticated listing `.opensip/detector-compatibility.json` vs component manifest body (closure.manifestDigest)",
        class_="semantic",
        req="R-DETECTOR-COMPAT-FILE",
    )

    chain = load("vectors/chain-zero-config-to-receipt.json")
    record(
        "chain-zero-config-is-checklist",
        isinstance(chain.get("chain"), list) and all("arrow" in x and "artifact" in x for x in chain["chain"]),
        selector="R-CHAIN-ZERO-CONFIG-TO-RECEIPT exhibited by executed traces, envelopes, and complete Runs together, not by a checklist sentence",
        detail=chain,
        class_="semantic",
        req="R-CHAIN-ZERO-CONFIG-TO-RECEIPT",
    )

    muc = load("vectors/multi-unit-missing-caps.json")
    record(
        "multi-unit-missing-caps-is-citation-not-zero-config-selection",
        "units" in muc and "advertised" in muc and "graph" not in muc and "orderedSteps" not in muc,
        selector="R-MULTI-UNIT-MISSING-CAPS Zero-config selection over multiple workspace units; a named list of capabilities is not that selection",
        detail=muc,
        class_="semantic",
        req="R-MULTI-UNIT-MISSING-CAPS",
    )
    coc = load("vectors/candidate-only-clones.json")
    record(
        "candidate-only-clones-is-citation-not-kinds-empty-cells",
        coc.get("cellKindsMustBeEmpty") is True and "kinds" not in coc and "candidateSourcePaths" not in coc,
        selector="enumeration-contract.v1.md candidate-only cells kinds=[] and must name candidateSourcePaths; flags are not that representation",
        detail=coc,
        class_="semantic",
        req="R-CANDIDATE-ONLY-CLONES",
    )
    hcc = load("vectors/host-captured-vs-candidate.json")
    record(
        "host-captured-vs-candidate-is-citation-not-retained-observations",
        isinstance(hcc.get("hostCaptured"), str) and isinstance(hcc.get("candidateOnly"), str) and "observations" not in hcc,
        selector="R-HOST-CAPTURED-VS-CANDIDATE from retained observations; two gloss strings are not retained observation records",
        detail=hcc,
        class_="semantic",
        req="R-HOST-CAPTURED-VS-CANDIDATE",
    )
    record(
        "host-captured-kit-content-exists",
        "candidateSourcePaths" in exec_in or "hostCapture" in exec_in or "selectedRefs" in exec_in,
        selector="execution-inputs-contract.v1.md host-captured required work vs candidate-only",
        class_="check",
        req="R-HOST-CAPTURED-VS-CANDIDATE",
    )

    # --- v1 aggregate overlap ---
    v1_ids = [r["id"] for r in v1_review["originalRequirementIds"]]
    req_ids = [r["id"] for r in req_doc["standing"]] + [r["id"] for r in req_doc["requirements"]] + [r["id"] for r in req_doc["futureQualification"]]
    record(
        "v1-134-ids-exact-charter-overlap",
        v1_ids == req_ids and len(v1_ids) == 134 and len(set(v1_ids)) == 134,
        selector="requirements.json standing+requirements+futureQualification exact array union",
        detail={"v1": len(v1_ids), "charter": len(req_ids), "dupes": [i for i, c in Counter(v1_ids).items() if c > 1]},
        class_="audit",
    )
    v1_disp = Counter(r["validatorDisposition"] for r in v1_review["originalRequirementIds"])
    v1_scope = Counter(r["reviewedScope"] for r in v1_review["originalRequirementIds"])
    record(
        "v1-reviewedScope-sums-134",
        sum(v1_scope.values()) == 134,
        selector="v1 reviewedScope aggregate",
        detail=dict(v1_scope),
        class_="audit",
    )
    record(
        "v1-reconstructed-48",
        sum(1 for r in v1_review["originalRequirementIds"] if r["consumerThisPassStatus"] == "reconstructed-this-pass") == 48,
        selector="scope-correction 48 reconstructed IDs",
        class_="audit",
    )
    record(
        "v1-probe-counts-are-not-conformance-counts",
        v1_probes["probeCount"] == 114 and v1_probes["passCount"] == 101 and v1_probes["failCount"] == 13,
        selector="audit: 114/101/13 are diagnostic probe counts, not 134-ID conformance counts",
        class_="audit",
    )

    results = {
        "probeCount": len(PROBES),
        "passCount": sum(1 for p in PROBES if p["ok"]),
        "failCount": sum(1 for p in PROBES if not p["ok"]),
        "firstRefusal": FIRST,
        "probes": PROBES,
        "failed": [p for p in PROBES if not p["ok"]],
        "identityRecipeChecks": expected_cmp_ids,
        "note": "Probe counts are not conformance counts. Historical v1 114/101/13 likewise.",
    }
    outp = OUT / "diagnostics" / "self_audit_probes.json"
    outp.write_text(json.dumps(results, indent=2, default=str) + "\n")
    print(
        json.dumps(
            {
                "probeCount": results["probeCount"],
                "passCount": results["passCount"],
                "failCount": results["failCount"],
                "firstRefusal": None if FIRST is None else FIRST["name"],
                "failedNames": [p["name"] for p in results["failed"]],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
