"""Independent CAT-F1–F7 / association / retention probes against copy bytes."""
from __future__ import annotations

import copy
import hashlib
import json
import types
from pathlib import Path

COPY = Path("/tmp/opensip-implementation/m1-grok-presentation-catalog-review-02/review/copy")
RESULTS = Path("/tmp/opensip-implementation/m1-grok-presentation-catalog-review-02/review/results")


def rec(rows, name, passed, **detail):
    rows.append({"name": name, "passed": bool(passed), **detail})
    print(("PASS" if passed else "FAIL"), name, detail.get("observed", ""))


def load_copy(name):
    p = COPY / f"{name}.py"
    m = types.ModuleType(name)
    m.__file__ = str(p)
    exec(compile(p.read_bytes(), str(p), "exec"), m.__dict__)
    return m


def code_of(fn):
    try:
        return "accepted", fn()
    except Exception as exc:  # noqa: BLE001
        return type(exc).__name__ + ":" + str(exc)[:180], None


def main():
    rows = []
    pins = json.loads((COPY / "input-pins.json").read_bytes())["files"]
    raws = {}
    for pin in pins:
        raw = Path(pin["path"]).read_bytes()
        assert len(raw) == pin["bytes"] and hashlib.sha256(raw).hexdigest() == pin["sha256"]
        raws[pin["role"]] = raw
    ref = types.ModuleType("pinned_canonical")
    exec(compile(raws["canonical"], "pinned-canonical-owner", "exec"), ref.__dict__)
    catalog = load_copy("catalog")
    schema = json.loads((COPY / "presentation-catalog.schema.json").read_bytes())
    docs = {k: json.loads(v) for k, v in raws.items() if k in ("common", "legacy-common", "policy", "repair", "invocation", "native-schema")}
    from referencing import Registry, Resource
    from referencing.jsonschema import DRAFT202012
    all_docs = [*docs.values(), schema]
    registry = Registry().with_resources((d["$id"], Resource(contents={k: v for k, v in d.items() if k != "$schema"}, specification=DRAFT202012)) for d in all_docs)
    matrix = json.loads(raws["native-matrix"])

    display = {"name": "Unused symbol", "description": "Static reachability; unknown callers remain explicit.", "tags": ["static", "unused"]}
    rule = {"contributionId": "acme.rules", "ruleStableId": "unused", "semanticsMajor": 1, "programDigest": "1" * 64}
    recipe = {"contributionId": "acme.rules", "recipeId": "remove-unused", "recipeVersion": "1.0.0"}
    data = {
        "schemaFamily": "opensip.presentation-catalog",
        "schemaMajor": 1,
        "capabilities": [{"capabilityId": "reachability", **copy.deepcopy(display)}],
        "rules": [{"ruleProgramRef": rule, **copy.deepcopy(display)}],
        "recipes": [{
            "recipeKey": recipe, **copy.deepcopy(display),
            "targetBounds": {"kind": "finding-fingerprints", "minimumTargets": 1, "maximumTargets": 4096},
            "parameterDescriptions": {"evidenceSource": "Select the exact evidence Run or earlier step.", "targets": "Select the finding fingerprints to preview."},
        }],
    }

    def bound(payload, raw=None):
        raw = ref.canonical(payload) if raw is None else raw
        blob = {"path": catalog.CATALOG_PATH, "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}
        ctx = {
            "closureId": "closure2:" + "2" * 64,
            "closure": {"manifestDigest": "3" * 64, "tree": [blob], "platform": "test-platform", "protocolMajor": 3},
            "tree": [{"type": "file", "path": blob["path"], "sha256": blob["sha256"], "length": blob["bytes"]}],
            "trustOrigin": "retained-generation",
            "selectedPlatform": "test-platform",
        }
        declared = {g: {catalog.entry_key(g, row) for row in payload[g]} for g in ("capabilities", "rules", "recipes")}
        return ctx, raw, declared

    def authority_for(ctx, declarations=None, selection=None):
        declarations = [{"capabilityId": "reachability", "languageModes": ["syntax-only"]}] if declarations is None else declarations
        selection = {
            "registrySha256": hashlib.sha256(ref.canonical(declarations)).hexdigest(),
            "catalogClosureId": ctx["closureId"],
            "semanticClosureIds": [ctx["closureId"]],
            "platform": "test-platform",
        } if selection is None else selection
        return catalog.capability_authority(declarations, selection, ref, docs["native-schema"], registry, matrix)

    def admit(ctx, raw, declared, authority="default"):
        auth = None if authority is None else (authority if authority != "default" else authority_for(ctx))
        return catalog.admit_catalog(ctx, raw, declared, ref, schema, registry, auth)

    # Positive
    ctx, raw, declared = bound(data)
    receipt = admit(ctx, raw, declared)
    rec(rows, "positive-present-receipt", receipt["state"] == "present" and receipt["catalog"] == data)

    # CAT-F1/F2/F3: no-catalogue vs unassociated vs not-retained vs corrupt vs missing descriptor
    ctx2, raw2, declared2 = bound(data)
    ctx2["tree"] = []
    ctx2["closure"]["tree"] = []
    absence = admit(ctx2, None, declared2)
    rec(rows, "no-catalogue-declared-when-both-trees-omit-path", absence["state"] == "no-catalogue-declared", observed=absence["state"])
    kind, _ = code_of(lambda: admit(ctx2, raw2, declared2))
    rec(rows, "unassociated-bytes-refused-when-no-listing", "UNASSOCIATED-BYTES" in kind, observed=kind)
    selected = {g: list(k) for g, k in declared.items()}
    out = catalog.select_descriptions(None, selected, ctx["closureId"], selected, source_state="not-retained")
    rec(rows, "not-retained-is-unavailable-not-no-catalogue", out["reason"] == "catalog-not-retained" and out["state"] == "unavailable")
    out = catalog.select_descriptions(None, selected, ctx["closureId"], selected, source_state="corrupt")
    rec(rows, "corrupt-is-unavailable-catalog-corrupt", out["reason"] == "catalog-corrupt")
    kind, _ = code_of(lambda: catalog.select_descriptions(None, selected, ctx["closureId"], selected, source_state="retained"))
    rec(rows, "retained-without-receipt-refuses", "RETAINED-RECEIPT" in kind, observed=kind)
    # missing descriptor in retained listing
    data_empty_rules = copy.deepcopy(data)
    data_empty_rules["rules"] = []
    ctx3, raw3, _ = bound(data_empty_rules)
    receipt3 = admit(ctx3, raw3, declared)
    out = catalog.select_descriptions(receipt3, selected, ctx3["closureId"], selected, expected_authority=receipt3["capabilityAuthority"])
    rec(rows, "missing-descriptor-is-not-declared-not-retention-failure", out["rules"][0]["reason"] == "descriptor-not-declared", observed=out["rules"][0])
    rec(rows, "no-catalogue-select-keeps-admitted-absence", catalog.select_descriptions(absence, selected, ctx2["closureId"], selected, expected_authority=absence["capabilityAuthority"])["state"] == "no-catalogue-declared")

    # CAT-F4 singular release association
    kind, _ = code_of(lambda: admit(ctx, raw, declared, authority=None))
    rec(rows, "capabilities-without-authority-refused", "RELEASE-AUTHORITY-REQUIRED" in kind, observed=kind)
    other = copy.deepcopy(ctx)
    other["closureId"] = "closure2:" + "9" * 64
    kind, _ = code_of(lambda: admit(other, raw, declared, authority=authority_for(ctx)))
    rec(rows, "second-closure-cannot-reuse-first-authority", "RELEASE-CLOSURE" in kind, observed=kind)
    rules_only = copy.deepcopy(data)
    rules_only["capabilities"] = []
    ctx4, raw4, declared4 = bound(rules_only)
    rec(rows, "rules-recipes-without-capability-authority-admitted", admit(ctx4, raw4, declared4, authority=None)["state"] == "present")
    # caller-matching digest is not authentication: same function accepts any declarations whose hash is copied into selection
    forged = [{"capabilityId": "reachability", "languageModes": ["syntax-only"]}]
    forged_sel = {
        "registrySha256": hashlib.sha256(ref.canonical(forged)).hexdigest(),
        "catalogClosureId": ctx["closureId"],
        "semanticClosureIds": [ctx["closureId"]],
        "platform": "test-platform",
    }
    kind, val = code_of(lambda: catalog.capability_authority(forged, forged_sel, ref, docs["native-schema"], registry, matrix))
    rec(rows, "matching-caller-digest-is-not-authentication", kind == "accepted",
        note="reference joins caller dictionaries; host must supply admitted handles. This documents the disclosed precondition, not a product signature.")

    # Plan membership: designated closure not in semanticClosures
    sel = {"registrySha256": hashlib.sha256(ref.canonical(forged)).hexdigest(), "catalogClosureId": ctx["closureId"], "semanticClosureIds": [], "platform": "test-platform"}
    kind, _ = code_of(lambda: catalog.capability_authority(forged, sel, ref, docs["native-schema"], registry, matrix))
    rec(rows, "designated-closure-must-be-in-plan-semantic-closures", "RELEASE-PLAN-CLOSURE" in kind, observed=kind)

    # CAT-F5 hostile text
    data_h = copy.deepcopy(data)
    data_h["rules"][0]["name"] = "text\u202e x"
    ctxh, rawh, declaredh = bound(data_h)
    kind, _ = code_of(lambda: admit(ctxh, rawh, declaredh))
    rec(rows, "hostile-bidi-name-refused", "ValidationError" in kind or "AdmissionError" in kind, observed=kind)

    # CAT-F6 recipe targetBounds / extra parameter
    data_p = copy.deepcopy(data)
    data_p["recipes"][0]["parameterDescriptions"]["force"] = "Bypass"
    ctxp, rawp, declaredp = bound(data_p)
    kind, _ = code_of(lambda: admit(ctxp, rawp, declaredp))
    rec(rows, "extra-recipe-parameter-refused", "ValidationError" in kind, observed=kind)
    rec(rows, "recipe-key-omits-closureId", "closureId" not in data["recipes"][0]["recipeKey"])

    # CAT-F7 full receipt + platform
    rec(rows, "receipt-copies-tree-platform-protocolMajor",
        receipt["tree"] == ctx["closure"]["tree"] and receipt["platform"] == "test-platform" and receipt["protocolMajor"] == 3)
    ctx_plat = copy.deepcopy(ctx)
    ctx_plat["selectedPlatform"] = "other-platform"
    kind, _ = code_of(lambda: admit(ctx_plat, raw, declared))
    rec(rows, "platform-mismatch-refused", "CATALOG.PLATFORM" in kind, observed=kind)

    # Delivery tree omit vs committed listing
    ctx_d = copy.deepcopy(ctx)
    ctx_d["tree"] = []
    kind, _ = code_of(lambda: admit(ctx_d, None, declared))
    rec(rows, "delivery-omit-cannot-hide-committed-listing", "CLOSURE-TREE" in kind, observed=kind)

    # CAT-M3: extra whitespace raw under 4MiB still admits; canonical shrinks
    pretty = json.dumps(data, indent=2).encode()
    ctxw, raww, declaredw = bound(data, pretty)
    rec(rows, "pretty-raw-sha-is-tree-binding-not-canonical",
        hashlib.sha256(pretty).hexdigest() != hashlib.sha256(ref.canonical(data)).hexdigest() and admit(ctxw, raww, declaredw)["listing"]["sha256"] == hashlib.sha256(pretty).hexdigest())
    rec(rows, "canonical-bytes-le-raw-pretty", len(ref.canonical(data)) <= len(pretty))
    # 4MiB+1 raw refuses before canonical
    huge = b" " * (4 * 1024 * 1024 + 1)
    ctxu, rawu, declaredu = bound(data, huge)
    kind, _ = code_of(lambda: admit(ctxu, rawu, declaredu))
    rec(rows, "raw-over-4mib-refused", "AdmissionError" in kind, observed=kind)

    # Run-selected key subset
    run_sel = copy.deepcopy(selected)
    run_sel["rules"] = []
    kind, _ = code_of(lambda: catalog.select_descriptions(receipt, selected, ctx["closureId"], run_sel, expected_authority=receipt["capabilityAuthority"]))
    rec(rows, "selected-key-not-in-run-selection-refused", "RUN-SELECTION" in kind, observed=kind)

    # Undeclared capability
    ctx5, raw5, declared5 = bound(data)
    declared5["capabilities"] = set()
    kind, _ = code_of(lambda: admit(ctx5, raw5, declared5))
    rec(rows, "undeclared-capability-key-refused", "UNDECLARED-KEY" in kind, observed=kind)

    failed = [r for r in rows if not r["passed"]]
    out = {"standing": "independent Grok presentation-catalog02 probes; synthetic host contexts; not product signatures",
           "passed": not failed, "caseCount": len(rows), "failedCount": len(failed), "failed": [r["name"] for r in failed], "checks": rows}
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / "independent-catalog.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({"passed": out["passed"], "caseCount": out["caseCount"], "failed": out["failed"]}))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
