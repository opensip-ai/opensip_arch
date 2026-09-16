"""Discriminating probes for consumer24 items M1, M2, M3, S1, S2, S3, S4, A1, A2, A4, A5 against actual owners.

Usage: probe_items.py ROOT   (ROOT = /tmp/opensip-design-corrections/candidate-subject.v37 or .v38)
Reads the frozen snapshot only; writes nothing into any tree (-B, stdout only). Standings are stated per result:
  helper    = direct call of a reference owner function (not a Run, not closure);
  schema    = JSON Schema validation against an owner document selector;
  closure   = actual identity-model.v3.close_run over a Run built by the maintained semantic fixture;
  static    = exact source/text presence check in a hashed owner file (reading, not execution).
No result here is product qualification, and none treats the consumer's exports as an oracle.
"""
import copy
import hashlib
import importlib.util
import json
import sys
import traceback
from pathlib import Path

ROOT = Path(sys.argv[1])
DC = ROOT / "docs/coop/design-corrections"
F = DC / "foundation"
TAG = ROOT.name.replace("candidate-subject.", "").replace("-", "_")
OUT = {"root": str(ROOT), "sections": {}}


def load(name, path):
    name = f"{TAG}_{name}"
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def sha_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def section(name):
    def wrap(fn):
        try:
            OUT["sections"][name] = {"result": fn()}
        except Exception as exc:  # recorded, never swallowed
            OUT["sections"][name] = {"error": type(exc).__name__ + ": " + str(exc)[:600], "traceback": traceback.format_exc()[-2500:]}
        return fn
    return wrap


INPUTS = [
    "docs/coop/design-corrections/native/native_evidence_model.v2.py",
    "docs/coop/design-corrections/native/native-evidence.schemas.v2.json",
    "docs/coop/design-corrections/native/native-capability-matrix.v2.json",
    "docs/coop/design-corrections/discovery-defaults.py",
    "docs/coop/design-corrections/foundation/identity-model.v3.py",
    "docs/coop/design-corrections/foundation/identity-schemas.v3.json",
    "docs/coop/design-corrections/foundation/identity-schemas.v2.json",
    "docs/coop/design-corrections/foundation/enumeration_model.v1.py",
    "docs/coop/design-corrections/foundation/enumeration-plan.schema.v1.json",
    "docs/coop/design-corrections/foundation/subject-inventory.schema.v1.json",
    "docs/coop/design-corrections/foundation/execution_inputs_model.v1.py",
    "docs/coop/design-corrections/foundation/execution_inputs_fixture.v3.py",
    "docs/coop/design-corrections/foundation/execution-inputs.schema.v1.json",
    "docs/coop/design-corrections/foundation/incoming-search.schema.v1.json",
    "docs/coop/design-corrections/foundation/evaluator_input_model.v3.py",
    "docs/coop/design-corrections/foundation/evaluator_semantic_fixture.v3.py",
    "docs/coop/design-corrections/foundation/check-semantic-replay.v3.py",
    "docs/coop/design-corrections/workflows/schemas/policy-document.schema.json",
    "docs/coop/design-corrections/workflows/schemas/policy-document.v2.schema.json",
    "docs/v2/contracts/product-v1/native-evidence.md",
    "docs/v2/contracts/product-v1/identity-and-evidence.md",
    "docs/coop/design-corrections/foundation/enumeration-contract.v1.md",
    "docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md",
]
OUT["inputSha256"] = {p: sha_file(ROOT / p) for p in INPUTS}

SR = load("semantic_replay", F / "check-semantic-replay.v3.py")
M = SR.M
C = M.C
N = load("native_model", DC / "native/native_evidence_model.v2.py")
EM = load("enumeration_model", F / "enumeration_model.v1.py")
XM = load("execution_inputs_model", F / "execution_inputs_model.v1.py")
IDS = json.loads((F / "identity-schemas.v3.json").read_text())
MATRIX = json.loads((DC / "native/native-capability-matrix.v2.json").read_text())
CLOSED = {}


def dialect(universe):
    return IDS["x-opensip-digest-domains"]["domainSets"]["native-semantic-universe"][universe]["languageVersionBinding"]["dialect"]


def refusal(fn):
    try:
        return {"outcome": "ADMIT", "value": fn()}
    except Exception as exc:
        return {"outcome": "REFUSE", "error": type(exc).__name__ + ": " + str(exc).split("\n")[0][:300]}


@section("M1-clones-census-chain")
def m1():
    ts, rust, syn = (dialect("native.semantic-universe.typescript.v2"), dialect("native.semantic-universe.rust.v2"),
                     dialect("native.semantic-universe.syntax.v2"))
    support = {}
    for label, d in (("typescript", ts), ("rust", rust), ("syntax", syn)):
        support[label] = {"form": d.get("form"), "hasTable": isinstance(d.get("table"), dict)}
        for paths in (["src/a.ts"], ["package.json"], ["tsconfig.json"], ["src/a.ts", "package.json"], ["Cargo.toml"],
                      ["src/main.rs"], ["src/main.rs", "Cargo.toml"], ["README.md"], ["data.json"]):
            support[label][",".join(paths)] = N.source_variant_capability_support(d, "clones", "normalized-body-hash", paths, True)
    files = ["package.json", "tsconfig.json", "src/a.ts", "src/b.ts", "README.md"]
    inv = {"kind": "file", "rows": [{"path": p, "nativeSubjectId": p} for p in files]}
    census = sorted(XM.expected_source_census("clones", {}, {}, {"d": inv}, ["d"]))
    cells = {c["mode"]: c["state"] for c in MATRIX["cells"] if c["capability"] == "clones-fact"}
    return {"standing": "helper + static registry reads",
            "enumerationKinds.clones-fact": EM._cap_kinds("clones-fact"),
            "fileKindExtentLaw": json.loads((F / "enumeration-plan.schema.v1.json").read_text())["x-opensip-file-membership-extent-law"]["fileKind"],
            "defaultRequiresClonesFact": {m: "clones-fact" in N.required_default_capabilities(m) for m in MATRIX["languageModes"]},
            "clonesFactMatrixCells": cells,
            "expectedClonesCensusOverTsUnitFiles": census,
            "sourceVariantCapabilitySupport(clones@normalized-body-hash, require_all)": support}


@section("M2-program-predicate-node-record")
def m2():
    atom = dict(SR.REFS_EXISTS_SRC)
    results = {}
    for doc in ("policy-document.schema.json", "policy-document.v2.schema.json"):
        schema = json.loads((DC / "workflows/schemas" / doc).read_text())
        schema["$ref"] = "#/$defs/Predicate"
        results[doc] = refusal(lambda s=schema: C.validate(s, atom) or "valid")
    annotation = IDS["$defs"]["program-predicate"]["properties"]["nodeDigest"]["x-opensip-digest"]
    source = (F / "identity-model.v3.py").read_text()
    graph, (run, objects, blobs), actual = SR.case_references_exists_source()
    CLOSED["references-exists-source"] = (graph, run, objects, blobs, actual)
    seal = objects[run["evaluationSealId"]][1]
    proof = objects[seal["proofBundleId"]][1]
    endpoint_nodes = []
    plan = objects[run["planId"]][1]
    policy = C.parse(blobs[plan["policyDigest"]])
    for rule in policy["rules"]:
        if "endpoint" in json.dumps(rule["emitWhen"]):
            endpoint_nodes.append(rule["emitWhen"])
    return {"standing": "schema (node against each Predicate selector) + closure (actual close_run over an endpoint atom) + static",
            "atom": atom, "validation": results, "nodeDigestAnnotation": annotation,
            "referenceSkipsFragmentRecordValidation": "if retention in ('fragment','owner-retained'):" in source,
            "referenceRecomputesNodeDigestJoin": "PROGRAM_PREDICATE_NODE_DIGEST" in source,
            "closedRunWithEndpointAtom": {"closeRun": "ADMIT", "runId": actual["runId"], "verdict": actual["verdict"],
                                          "policyEmitWhenWithEndpoint": endpoint_nodes,
                                          "predicateProofs": len(proof["predicateProofs"])}}


@section("M3-unit-membership-order")
def m3():
    markers = {"tsconfig.json": {"sha256": "a" * 64}, "Cargo.toml": {"sha256": "c" * 64},
               "packages/web/package.json": {"sha256": "b" * 64}}
    files = ["tsconfig.json", "Cargo.toml", "src/main.rs", "src/a.ts", "packages/web/package.json",
             "packages/web/index.ts", "README.md", "data.json", "notes.txt", "node_modules/x/index.js"]
    disc = N.discover_units(markers)
    membership = N.assign_membership(disc["units"], files)
    reversed_rows = copy.deepcopy(membership)
    reversed_rows["rows"].reverse()
    swapped = copy.deepcopy(membership)
    swapped["units"].reverse()
    remap = {u["unitOrdinal"]: i for i, u in enumerate(swapped["units"])}
    for i, u in enumerate(swapped["units"]):
        u["unitOrdinal"] = i
    for r in swapped["rows"]:
        if r["unitOrdinal"] is not None:
            r["unitOrdinal"] = remap[r["unitOrdinal"]]

    def digest(v):
        return hashlib.sha256(C.canonical(v)).hexdigest()

    consumer_order = copy.deepcopy(membership)
    consumer_order["units"] = sorted(consumer_order["units"], key=lambda u: (u["rootPath"].encode(), u["languageFamily"]))
    consumer_order["rows"] = sorted(consumer_order["rows"], key=lambda r: r["path"].encode())
    evaluator_input = (F / "evaluator_input_model.v3.py").read_text()
    return {"standing": "helper + schema + static",
            "units": [(u["unitOrdinal"], u["rootPath"], u["languageFamily"]) for u in membership["units"]],
            "rowOrder": [r["path"] for r in membership["rows"]],
            "schemaValid": {"reference": refusal(lambda: N.validate_native("UnitMembershipV1", membership) or "valid"),
                            "rowsReversed": refusal(lambda: N.validate_native("UnitMembershipV1", reversed_rows) or "valid"),
                            "unitsReversedOrdinalsRemapped": refusal(lambda: N.validate_native("UnitMembershipV1", swapped) or "valid")},
            "membershipDigest": {"reference": digest(membership), "rowsReversed": digest(reversed_rows),
                                 "unitsReversedOrdinalsRemapped": digest(swapped)},
            "optionalDerivationLaneEquality": {"rowsReversed": C.equal_typed(membership, reversed_rows),
                                               "unitsReversed": C.equal_typed(membership, swapped)},
            "consumerStatedOrderEqualsReference": C.equal_typed(consumer_order, membership),
            "runClosureCallsAdmitEnumerationWithMembershipDerivation": "membership_derivation" in evaluator_input,
            "discoveryDefaultsMentionsUnitOrdinalOrRowOrder": any(k in (DC / "discovery-defaults.py").read_text() for k in ("unitOrdinal", "UnitMembership")),
            "nativeContractStatesOrder": {k: k in (ROOT / "docs/v2/contracts/product-v1/native-evidence.md").read_text()
                                          for k in ("unitOrdinal", "sorted by", "UTF-8 bytes of `rootPath`")}}


@section("S1-stage-output-schema-registry")
def s1():
    if "references-exists-source" not in CLOSED:
        raise RuntimeError("M2 closed Run unavailable")
    graph, run, objects, blobs, actual = CLOSED["references-exists-source"]
    seal = objects[run["evaluationSealId"]][1]
    exec_plan = objects[seal["executionPlanId"]][1]
    registered = M.registered_schema_documents()
    rows = []
    for stage in exec_plan["stages"]:
        spec = C.parse(blobs[stage["stageSpecDigest"]])
        doc = C.parse(blobs[spec["outputSchemaDigest"]])
        rows.append({"operation": spec["operation"], "outputSchemaDigest": spec["outputSchemaDigest"],
                     "outputSchemaId": doc.get("$id"), "registered": spec["outputSchemaDigest"] in registered})
    props = IDS["$defs"]
    return {"standing": "closure (the admitted Run's own stage spec) + helper (registry) + static annotation",
            "closeRun": "ADMIT", "runId": actual["runId"], "stages": rows,
            "nativeSchemaDocumentRegistered": sha_file(DC / "native/native-evidence.schemas.v2.json") in registered,
            "stageSpecOutputSchemaAnnotation": props["stage-spec"]["properties"]["outputSchemaDigest"]["x-opensip-digest"],
            "viewSchemaDigestsAnnotationHasArtifactClass": props["view"]["properties"]["schemaDigests"]["items"]["x-opensip-digest"].get("artifactClass")}


@section("S2-clone-level-specification-join")
def s2():
    identity = (F / "identity-model.v3.py").read_text()
    native = (DC / "native/native_evidence_model.v2.py").read_text()
    schema = json.loads((DC / "native/native-evidence.schemas.v2.json").read_text())
    normalizer = schema["$defs"]["SyntaxGrammarBundleV1"]["properties"]["normalizer"]
    return {"standing": "static (exact source presence) + schema read; no clones Run executed",
            "closureLevelVersionOnlyRequiresRetainedBlob": "blob(level_version)" in identity,
            "closureJoinsLevelVersionToNormalizerSpecification": "specificationDigest" in identity,
            "nativeContextRequiresSyntaxNormalizerSpecInGrammarClosure": "native.syntax-normalizer-spec-not-in-closure" in native,
            "normalizerRequired": normalizer["required"],
            "specificationDigestIsSingular": normalizer["properties"]["specificationDigest"].get("type") != "array",
            "typescriptOrRustContextHasNormalizer": any("normalizer" in json.dumps(schema["$defs"].get(k, {}))
                                                        for k in ("TypeScriptNativeContextV2", "NativeContextV2"))}


@section("S3-zero-config-syntax-only")
def s3():
    registry = []
    for cap in MATRIX["capabilities"]:
        modes = sorted(c["mode"] for c in MATRIX["cells"] if c["capability"] == cap["id"] and c["state"] != "NOT-SELECTED")
        if modes:
            registry.append({"capabilityId": cap["id"], "languageModes": modes})
    none_found = N.discover_units({})
    explicit_dot = N.discover_units({}, ["."])
    selection = refusal(lambda: N.default_capability_selection([], registry))
    requested = None
    if selection["outcome"] == "ADMIT":
        text = json.dumps(selection["value"])
        requested = text.count('"capabilityId"')
    scope = refusal(lambda: N.unit_scope_descriptor([], []))
    fake_unit = {"rootPath": "", "languageFamily": "syntax", "languageMode": "syntax-only", "unitKind": "syntax-only",
                 "markerPath": "", "markerSha256": "0" * 64, "recognizerId": "none", "recognizerVersion": 1,
                 "provenance": "DISCOVERED", "memberPackageRoots": [], "unitOrdinal": 0}
    membership = N.assign_membership([], ["src/a.py", "README.md", "src/b.rs"])
    return {"standing": "helper",
            "discoverUnitsNoMarkers": {"units": none_found["units"], "refused": none_found["refused"]},
            "discoverUnitsExplicitDotNoMarker": explicit_dot["refused"],
            "defaultCapabilitySelectionWithNoUnits": {"outcome": selection["outcome"], "capabilityRows": requested,
                                                      "error": selection.get("error")},
            "unitScopeDescriptorWithNoUnits": scope if scope["outcome"] == "REFUSE" else {"outcome": "ADMIT", "descriptor": scope["value"]["scopeDescriptor"]},
            "syntaxOnlyWorkspaceUnitRepresentable": refusal(lambda: N.validate_native("WorkspaceUnitV2", fake_unit) or "valid"),
            "markerFreeMembershipRows": [(r["path"], r["membership"], r["reason"], r["unitOrdinal"]) for r in membership["rows"]],
            "enumerationContractClaimsSyntaxOnlyDefaultUnit": "tsjs`/`rust`/`syntax-only` unit per directory" in (F / "enumeration-contract.v1.md").read_text()}


@section("S4-native-account-target-universe")
def s4():
    X = load("execution_inputs_fixture", F / "execution_inputs_fixture.v3.py")
    g = SR.S.build_ts_semantic_graph(atom=SR.REFS_EXISTS_TGT, has_declares=False, has_references_fact=True,
                                     second_partition=True, second_universe=True, references_resolved=True,
                                     incoming_search=True, incoming_complete=True, target_sidecar=True, cross_u_binding="foo")
    captured = X.attach_host_capture(g)
    base = captured["manifest"]
    other = g["u2"] if g.get("u2") else "f" * 64
    rows = {"baseline": captured["admission"].get("result"), "baselineRefusals": captured["admission"].get("refusals")}
    accounts = [(a["relation"], a["resolution"], a["sourceUniverse"] == a["targetUniverse"]) for a in base["nativeCoverageAccounts"]]
    for label, value in (("targetUniverse=other-admitted-universe", other), ("targetUniverse=null", None),
                         ("targetUniverse=unbound-hex", "e" * 64)):
        m = copy.deepcopy(base)
        for acc in m["nativeCoverageAccounts"]:
            acc["targetUniverse"] = value
        g2 = copy.deepcopy(g)
        g2["executionInputs"] = m
        g2["executionInputsDigest"] = X.M.raw_digest(m)
        adm = X.M.admit_execution_inputs(**X.admission_kwargs(g2))
        rows[label] = {"result": adm.get("result"), "refusals": adm.get("refusals"),
                       "executionInputsDigestChanged": g2["executionInputsDigest"] != captured["digest"]}
    control = copy.deepcopy(base)
    for acc in control["nativeCoverageAccounts"]:
        acc["sourceUniverse"] = other
    g3 = copy.deepcopy(g)
    g3["executionInputs"] = control
    g3["executionInputsDigest"] = X.M.raw_digest(control)
    adm3 = X.M.admit_execution_inputs(**X.admission_kwargs(g3))
    rows["control:sourceUniverse=other-admitted-universe"] = {"result": adm3.get("result"), "refusals": adm3.get("refusals")}
    return {"standing": "helper (actual execution-inputs owner admission over a fixture graph; not a Run)",
            "accounts(relation,rung,sourceEqualsTarget)": accounts, "universes": g.get("universes"), "rows": rows}


@section("A1-unannotated-hex-fields")
def a1():
    hexes = ("^[0-9a-f]{64}(?![\\s\\S])", "^[0-9a-f]{64}$")
    report = {}
    for doc in ("execution-inputs.schema.v1.json", "incoming-search.schema.v1.json"):
        schema = json.loads((F / doc).read_text())
        defs = schema.get("$defs", {})
        hex_defs = {k for k, v in defs.items() if isinstance(v, dict) and v.get("pattern") in hexes}
        found, annotated = [], 0

        def walk(node, path, covered):
            nonlocal annotated
            if isinstance(node, dict):
                here = covered or "x-opensip-digest" in node
                if "x-opensip-digest" in node:
                    annotated += 1
                is_hex = node.get("pattern") in hexes or (isinstance(node.get("$ref"), str) and node["$ref"].split("/")[-1] in hex_defs)
                if is_hex and not path.startswith("/$defs/" + next(iter(hex_defs), "\0")):
                    found.append({"path": path, "annotated": here})
                for k, v in node.items():
                    walk(v, path + "/" + k, here)
            elif isinstance(node, list):
                for i, v in enumerate(node):
                    walk(v, path + "/" + str(i), covered)
        walk(schema, "", False)
        report[doc] = {"hexDefs": sorted(hex_defs), "hexOccurrences": len(found),
                       "unannotated": [f["path"] for f in found if not f["annotated"]], "annotationCount": annotated,
                       "declaresOwnDigestLaw": "x-opensip-digest-law" in schema}
    return {"standing": "static schema walk", "report": report,
            "closingLawScopeText": "governs identity-schemas.v3, and the native contract" in (ROOT / "docs/v2/contracts/product-v1/identity-and-evidence.md").read_text()}


@section("A2-identity-v2-selector-drift")
def a2():
    v2 = json.loads((F / "identity-schemas.v2.json").read_text())
    v3 = IDS
    same = {}
    for name in ("scope-descriptor", "LogicalPath", "Text"):
        a, b = v2["$defs"].get(name), v3["$defs"].get(name)
        same[name] = {"inV2": a is not None, "inV3": b is not None,
                      "canonicalEqual": a is not None and b is not None and C.canonical(a) == C.canonical(b)}
    lm2 = v2.get("x-opensip-digest-domains", {}).get("languageModes", {}).get("map")
    lm3 = v3.get("x-opensip-digest-domains", {}).get("languageModes", {}).get("map")
    return {"standing": "static", "defs": same,
            "languageModesMapKeysEqual": (sorted(lm2) == sorted(lm3)) if isinstance(lm2, dict) and isinstance(lm3, dict) else None,
            "enumerationPlanScopeDigestRecord": json.loads((F / "enumeration-plan.schema.v1.json").read_text())["properties"]["scopeDigest"]["x-opensip-digest"]["record"]}


@section("A4-pruned-tree-inventory")
def a4():
    markers = {"package.json": {"sha256": "b" * 64}, "Cargo.toml": {"sha256": "c" * 64}}
    units = N.discover_units(markers)["units"]
    files = ["package.json", "Cargo.toml", "src/a.ts", "node_modules/dep/index.js", "target/debug/x.rs", ".git/HEAD"]
    membership = N.assign_membership(units, files)
    return {"standing": "helper + static",
            "prunedFilesWhenSuppliedInInventory": [(r["path"], r["membership"], r["reason"]) for r in membership["rows"]
                                                   if r["reason"] == "host-ignore-convention"],
            "membershipWithoutPrunedFiles": [r["path"] for r in N.assign_membership(units, files[:3])["rows"]]}


@section("A5-typescript-js-flags")
def a5():
    rows = []
    for with_js in (True, False):
        listing = ["tsconfig.json", "package.json", "src/a.ts"] + (["src/b.js"] if with_js else [])
        for options in ({}, {"allowJs": True}, {"checkJs": True}, {"allowJs": True, "checkJs": True}):
            mode = N.typescript_mode(listing, "", {"name": "p"}, {"compilerOptions": options}, None, [], False)
            consumer = {"jsAdmittedToProgram": bool(options.get("allowJs")),
                        "jsDiagnosticsEnabled": bool(options.get("allowJs")) and bool(options.get("checkJs"))}
            ref = {k: mode[k] for k in ("jsAdmittedToProgram", "jsDiagnosticsEnabled")}
            rows.append({"jsFilePresent": with_js, "compilerOptions": options, "reference": ref,
                         "consumerStatedRule": consumer, "agree": ref == consumer, "jsRootFiles": mode["jsRootFiles"]})
    return {"standing": "helper", "rows": rows, "disagreements": sum(1 for r in rows if not r["agree"])}


print(json.dumps(OUT, indent=1, default=str))
