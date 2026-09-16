"""Focused controls for the consumer24 native/foundation corrections (M1 M2 M3 S1 S2 S3 S4 A1 A2 A4).

Each control names the law it exercises and the owner function it calls. Real complete Run controls go
through identity-model.v3.close_run over fixture graphs built by the maintained fixtures; helper controls
call the owning admission function directly. Design evidence over synthetic fixtures; not product
qualification.

Usage: python -I -B check-native-consumer24-corrections.v1.py [--only ITEM ...]
Stdout only; writes nothing.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import sys
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
KIT = HERE.parent


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, file)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


SR = load("c24_semantic_replay", HERE / "check-semantic-replay.v3.py")

# native-evidence section 1.4 U-4b.2, whitespace-normalised: the published TS/JS unitKind projection.
TSJS_UNIT_KIND_LAW = ("whose `unitKind` is `ts-program` exactly when that mode is `ts-tsconfig` and `js-program` "
                      "when it is `js-allowjs` or `js-synthesized`")
M = SR.M
C = M.C
ROWS: list[dict] = []


def row(item, case, ok, detail=None):
    ROWS.append({"item": item, "case": case, "ok": bool(ok), **({"detail": detail} if detail is not None else {})})


def refusal(fn):
    """The AdmissionError text fn raises, or None when it returns."""
    try:
        fn()
    except C.AdmissionError as exc:
        return str(exc)
    return None


def refuses_with(item, case, fn, token):
    got = refusal(fn)
    row(item, case, got is not None and token in got, got)


# ------------------------------------------------------------------------------------------------ M2
V1_POLICY = "workflows/schemas/policy-document.schema.json"
V2_POLICY = "workflows/schemas/policy-document.v2.schema.json"


def m2():
    record = M.SCHEMA["$defs"]["program-predicate"]["properties"]["nodeDigest"]["x-opensip-digest"]["record"]
    row("M2", "node-digest-record-names-the-v2-predicate", record == {"document": V2_POLICY, "selector": "#/$defs/Predicate"}, record)
    target = SR.REFS_EXISTS_TGT
    composite = {"op": "and", "operands": [target, {"op": "not", "operand": SR.REFS_NONE_SRC}]}
    for name, node in (("endpoint-target-atom", target), ("endpoint-source-atom", SR.REFS_EXISTS_SRC),
                       ("all-covered-atom", {"op": "all-covered", "relation": "references",
                                             "minResolution": "resolved-binding", "filters": []}),
                       ("and-not-composite", composite)):
        row("M2", "named-record-admits-" + name, refusal(lambda n=node: M.admit_program_predicate_node(n)) is None)
    row("M2", "the-v1-record-would-refuse-a-v2-endpoint-atom",
        refusal(lambda: M.validate_registered_record(V1_POLICY, "#/$defs/Predicate", target)) is not None)
    bad = {
        "unknown-op": {**target, "op": "xor"},
        "count-at-most-without-n": {**target, "op": "count-at-most"},
        "exists-with-n": {**target, "n": 1},
        "endpoint-outside-enum": {**target, "endpoint": "middle"},
        "undeclared-atom-key": {**target, "weight": 1},
        "and-with-one-operand": {"op": "and", "operands": [target]},
        "not-with-operands-list": {"op": "not", "operands": [target, target]},
        "nested-invalid-operand": {"op": "or", "operands": [target, {**target, "endpoint": "both"}]},
    }
    for name, node in bad.items():
        refuses_with("M2", "named-record-refuses-" + name, lambda n=node: M.admit_program_predicate_node(n),
                     "PROGRAM_PREDICATE_NODE_RECORD")

    # Real complete Runs: the v2 endpoint atoms close through close_run under the corrected record.
    for case_name, builder in (("endpoint-target", SR.case_incoming_known_hit),
                               ("endpoint-source", SR.case_references_exists_source)):
        _, (run, objects, blobs), _ = builder()
        run_id = M.close_run(run, objects, blobs)
        row("M2", "real-run-closes-with-" + case_name, run_id.startswith("run3:"), run_id)
        # The closure really consults the named record: pointing the annotation back at the v1 document
        # (the pre-correction value) refuses the very same Run at the node join. close_run replays through
        # its own loaded stack with its OWN identity-model copy, so every loaded copy is patched.
        copies = {id(m): m for m in (M, M.complete_replay().M)}.values()
        saved = []
        try:
            for m in copies:
                annotation = m.SCHEMA["$defs"]["program-predicate"]["properties"]["nodeDigest"]["x-opensip-digest"]
                saved.append((m, annotation, copy.deepcopy(annotation["record"])))
                annotation["record"]["document"] = V1_POLICY
                m._ADMITTED_PREDICATE_NODES.clear()
            refuses_with("M2", "real-run-refuses-under-the-pre-correction-v1-record-" + case_name,
                         lambda: M.close_run(run, objects, blobs), "PROGRAM_PREDICATE_NODE_RECORD")
        finally:
            for m, annotation, record in saved:
                annotation["record"] = record
                m._ADMITTED_PREDICATE_NODES.clear()
        row("M2", "real-run-closes-again-after-restoring-" + case_name, M.close_run(run, objects, blobs) == run_id)


_LOADED = {}


def owners():
    """The maintained execution-inputs checker (its owner fixtures and full_run) and the host-capture
    fixture, loaded once and only by the sections that need them."""
    if not _LOADED:
        _LOADED["EI"] = load("c24_execution_inputs_checker", HERE / "check-execution-inputs.v1.py")
        _LOADED["X"] = load("c24_execution_capture", HERE / "execution_inputs_fixture.v3.py")
    return _LOADED["EI"], _LOADED["X"]


def refusal_any(fn):
    """Any exception text fn raises (loaded stacks mint their own error classes), or None."""
    try:
        fn()
    except Exception as exc:  # noqa: BLE001 - every loaded copy has its own AdmissionError class
        return type(exc).__name__ + ":" + str(exc)
    return None


def identity_copies(EI):
    """Every identity-model.v3 copy a real Run passes through in these stacks."""
    found = {}
    for m in (M, M.complete_replay().M, EI.IDENTITY, EI.IDENTITY.complete_replay().M, EI.R.M):
        found[id(m)] = m
    return list(found.values())


# ------------------------------------------------------------------------------------------------ M1
def m1():
    EI, _ = owners()
    XM = EI.M
    N = M.native_admission()
    rows = M.DIGESTS["domainSets"]["native-semantic-universe"]
    ts, rs, sy = (rows["native.semantic-universe.typescript.v2"], rows["native.semantic-universe.rust.v2"],
                  rows["native.semantic-universe.syntax.v2"])
    row("M1", "typescript-eligibility-is-its-published-dialect-table",
        M.body_eligibility_table(ts) == ts["languageVersionBinding"]["dialect"]["table"])
    row("M1", "syntax-eligibility-is-its-published-dialect-table",
        M.body_eligibility_table(sy) == sy["languageVersionBinding"]["dialect"]["table"])
    row("M1", "rust-eligibility-is-its-closed-rs-set", M.body_eligibility_table(rs) == {".rs": ".rs"})
    undeclared = copy.deepcopy(rs)
    undeclared["languageVersionBinding"].pop("bodyEligibility")
    refuses_with("M1", "a-universe-row-without-eligibility-refuses", lambda: M.body_eligibility_table(undeclared),
                 "BODY_ELIGIBILITY_UNDECLARED")
    unknown_form = copy.deepcopy(ts)
    unknown_form["languageVersionBinding"]["bodyEligibility"] = {"form": "every-path"}
    refuses_with("M1", "an-unknown-eligibility-form-refuses", lambda: M.body_eligibility_table(unknown_form),
                 "BODY_ELIGIBILITY_FORM")

    mixed_ts = {"src/a.ts", "src/types.d.ts", "src/b.jsx", "package.json", "tsconfig.json", "README.md",
                "assets/logo.svg", "LICENSE"}
    for mode in ("ts-tsconfig", "js-allowjs", "js-synthesized"):
        row("M1", "default-clones-census-is-eligible-code-only-" + mode,
            XM.body_eligible_census("clones", {"languageMode": mode}, mixed_ts) == {"src/a.ts", "src/types.d.ts", "src/b.jsx"})
    mixed_rs = {"src/lib.rs", "src/bin/tool.rs", "tools/unowned.rs", "build.rs", "Cargo.toml", "Cargo.lock", "README.md"}
    for mode in ("rust-cargo", "rust-cargo-prepared"):
        # tools/unowned.rs is in no compilation target's ownership: eligibility never consults it.
        row("M1", "default-clones-census-is-rs-only-and-ownership-blind-" + mode,
            XM.body_eligible_census("clones", {"languageMode": mode}, mixed_rs)
            == {"src/lib.rs", "src/bin/tool.rs", "tools/unowned.rs", "build.rs"})
    mixed_sy = {"x.rs", "web/y.ts", "README.md", "data.json", "config.yaml", "extensionless"}
    row("M1", "default-clones-census-is-dialect-code-only-syntax-only",
        XM.body_eligible_census("clones", {"languageMode": "syntax-only"}, mixed_sy) == {"x.rs", "web/y.ts"})
    row("M1", "a-non-body-relation-keeps-the-full-census",
        XM.body_eligible_census("file", {"languageMode": "ts-tsconfig"}, mixed_ts) == mixed_ts)
    row("M1", "an-unmapped-mode-keeps-the-full-census",
        XM.body_eligible_census("clones", {"languageMode": "no-such-mode"}, mixed_ts) == mixed_ts)
    inventory = {"kind": "file", "rows": [{"nativeSubjectId": p, "path": p} for p in sorted(mixed_ts)]}
    row("M1", "expected-source-census-applies-eligibility-to-the-broad-inventory",
        XM.expected_source_census("clones", {"languageMode": "ts-tsconfig"}, {}, {"d": inventory}, ["d"])
        == {"src/a.ts", "src/types.d.ts", "src/b.jsx"})
    row("M1", "expected-source-census-for-file-still-names-every-inventoried-path",
        XM.expected_source_census("file", {"languageMode": "ts-tsconfig"}, {}, {"d": inventory}, ["d"]) == mixed_ts)

    # Scope-capability symmetry at the producer boundary.
    rust_dialect = rs["languageVersionBinding"]["dialect"]
    row("M1", "pre-correction-rust-dialect-made-no-decision-for-a-cargo-toml-clones-scope",
        N.source_variant_capability_support(rust_dialect, "clones", "normalized-body-hash", ["Cargo.toml"], True) is None)
    rust_eligible = {"table": M.body_eligibility_table(rs)}
    got = N.source_variant_capability_support(rust_eligible, "clones", "normalized-body-hash", ["Cargo.toml"], True)
    row("M1", "rust-clones-scope-over-cargo-toml-is-now-the-published-unknown-disclosure",
        got == N.SOURCE_VARIANT_UNAVAILABLE_DISCLOSURE, got)
    row("M1", "rust-clones-scope-over-an-unowned-rs-path-stays-eligible",
        N.source_variant_capability_support(rust_eligible, "clones", "normalized-body-hash", ["tools/unowned.rs"], True) is None)
    row("M1", "rust-mixed-clones-scope-cannot-hide-its-manifest-half",
        N.source_variant_capability_support(rust_eligible, "clones", "normalized-body-hash", ["src/lib.rs", "Cargo.toml"], True) is not None)
    row("M1", "rust-inventory-relation-is-never-eligibility-gated",
        N.source_variant_capability_support(rust_eligible, "file", "enumerated", ["Cargo.toml"], True) is None)

    # Real complete Runs over the syntax universe's mixed code-and-data sources with a REQUIRED clones-fact cell.
    # The rule is the maintained NONE_ATOM (`none file`), which emits no finding, so the verdict shows the
    # required cell's own effect instead of being decided by a live gating finding.
    def run_with(subjects):
        graph = EI.F.build_file_inputs(clones_fact_subjects=subjects, atom_override=EI.NONE_ATOM)
        result, proof = EI.full_run(graph)
        accounts = [a for a in graph["executionInputs"]["nativeCoverageAccounts"] if a["relation"] == "clones"]
        return result, proof, accounts

    def disclosed(proof):
        return any(x.get("cause") == "language-tier-unsupported" and x.get("nativeCause") == "capability-missing"
                   for x in proof["executionDeficiencies"])

    result, proof, accounts = run_with(["src/index.ts"])
    row("M1", "real-run-default-mixed-repo-clones-over-eligible-code-closes-determinate",
        result["runId"].startswith("run3:") and result["verdict"] == "pass" and proof["executionDeficiencies"] == []
        and len(accounts) == 1 and accounts[0]["applicability"] == "supported-available" and accounts[0]["coverageIds"],
        {"verdict": result["verdict"], "executionDeficiencies": proof["executionDeficiencies"], "accounts": accounts})
    result, proof, accounts = run_with([])
    row("M1", "real-run-missing-eligible-code-stays-required-indeterminate",
        result["runId"].startswith("run3:") and result["verdict"] == "indeterminate" and proof["executionDeficiencies"] != [],
        {"verdict": result["verdict"], "executionDeficiencies": proof["executionDeficiencies"]})
    result, proof, accounts = run_with(["README.md", "extensionless", "src/index.ts"])
    row("M1", "real-run-explicit-scope-over-ineligible-paths-is-disclosed-not-refused",
        result["runId"].startswith("run3:") and result["verdict"] == "indeterminate" and disclosed(proof),
        {"verdict": result["verdict"], "executionDeficiencies": proof["executionDeficiencies"]})


# ------------------------------------------------------------------------------------------------ S4
def s4():
    EI, X = owners()
    account = EI.M.SCHEMA["$defs"]["NativeCoverageAccountV1"]
    target = account["properties"]["targetUniverse"]
    row("S4", "account-target-universe-is-typed-null", target.get("type") == "null" and "oneOf" not in target, target)
    joins = account["x-opensip-external-joins"]
    row("S4", "published-law-names-null-as-the-single-canonical-value",
        joins.get("singleCanonicalTargetUniverse", {}).get("equals") == "null" and "deliberatelyNotJoined" not in joins)
    two = EI.manifest_from_owner(EI.F.build_file_inputs(multiple_universes=True))
    row("S4", "builder-emits-null-on-every-account",
        all(a["targetUniverse"] is None for a in two["execution_inputs"]["nativeCoverageAccounts"]))
    admitted = EI.admit(two)
    row("S4", "two-universe-owner-admits-with-null-targets", admitted["result"] == "ADMIT", admitted.get("refusals"))
    bindings = two["enumeration_plan"]["cells"][0]["programBindings"]
    for label, value in (("another-universe", bindings[1]["universe"]), ("its-own-source-universe", bindings[0]["universe"])):
        refused = EI.admit(EI.set_account_target_universe(two, lambda a: a["programOrdinal"] == 0, value))
        row("S4", "non-null-account-target-refuses-" + label,
            refused["result"] == "REFUSE" and "EXECUTION_INPUTS_SCHEMA" in refused["refusals"], refused.get("refusals"))

    graph = EI.F.build_file_inputs()
    result, _ = EI.full_run(graph)
    row("S4", "real-run-closes-with-null-account-targets",
        result["runId"].startswith("run3:") and all(a["targetUniverse"] is None for a in graph["executionInputs"]["nativeCoverageAccounts"]))

    # Real Run negative: the same graph whose hashed ExecutionInputsV1 carries a non-null account target.
    graph = EI.F.build_file_inputs()
    X.attach_host_capture(graph)
    manifest = copy.deepcopy(graph["executionInputs"])
    manifest["nativeCoverageAccounts"][0]["targetUniverse"] = manifest["nativeCoverageAccounts"][0]["sourceUniverse"]
    old = graph["inputs"]["executionInputsDigest"]
    raw = C.canonical(manifest)
    digest = hashlib.sha256(raw).hexdigest()
    graph["blobs"][digest] = raw
    graph["inputs"]["executionInputsDigest"] = digest
    graph["inputs"]["evaluationInputRefs"] = EI.canon_refs(
        [r for r in graph["inputs"]["evaluationInputRefs"] if r["digest"] != old] + [{"domain": "execution-inputs", "digest": digest}])
    graph["executionInputs"], graph["executionInputsDigest"] = manifest, digest
    got = refusal_any(lambda: EI.full_run(graph))
    row("S4", "real-run-with-a-non-null-account-target-does-not-close",
        got is not None and ("EXECUTION_INPUTS_SCHEMA" in got or "REGISTERED_RECORD" in got), got)


# ------------------------------------------------------------------------------------------------ A1
FOUNDATION_RECORD_DOCUMENTS = [
    "foundation/enumeration-plan.schema.v1.json", "foundation/subject-inventory.schema.v1.json",
    "foundation/evaluator-emission-plan.schema.v1.json", "foundation/target-attribution.schema.v1.json",
    "foundation/target-attribution.schema.v2.json", "foundation/incoming-search.schema.v1.json",
    "foundation/execution-inputs.schema.v1.json", "foundation/import-source-context.schema.json"]
EXECUTION_INPUTS_DOC = "foundation/execution-inputs.schema.v1.json"


def a1():
    EI, _ = owners()
    for document in FOUNDATION_RECORD_DOCUMENTS:
        coverage = M.foundation_digest_annotation_coverage(M.foundation_record_document(document))
        row("A1", "closing-law-covers-" + document.split("/")[-1], coverage["unannotated"] == [], coverage)
    ei = M.foundation_record_document(EXECUTION_INPUTS_DOC)
    inc = M.foundation_record_document("foundation/incoming-search.schema.v1.json")
    p, d = ei["properties"], ei["$defs"]
    pick = lambda node: node["x-opensip-digest"]  # noqa: E731
    declared = {
        "enumerationPlanDigest": pick(p["enumerationPlanDigest"]),
        "analysisSpecDigest": pick(p["analysisSpecDigest"]),
        "candidateResultRefs[]": pick(p["candidateResultRefs"]["items"]),
        "InputRefV1.digest": pick(d["InputRefV1"]["properties"]["digest"]),
        "StageReceiptV1.stageSpecDigest": pick(d["StageReceiptV1"]["properties"]["stageSpecDigest"]),
        "CellProgramOutcomeV1.universe": pick(d["CellProgramOutcomeV1"]["properties"]["universe"]),
        "CellProgramOutcomeV1.inventoryDigests[]": pick(d["CellProgramOutcomeV1"]["properties"]["inventoryDigests"]["items"]),
        "CellProgramOutcomeV1.viewDigests[]": pick(d["CellProgramOutcomeV1"]["properties"]["viewDigests"]["items"]),
        "CellProgramOutcomeV1.candidateResultDigest": pick(d["CellProgramOutcomeV1"]["properties"]["candidateResultDigest"]),
        "NativeCoverageAccountV1.sourceUniverse": pick(d["NativeCoverageAccountV1"]["properties"]["sourceUniverse"]),
        "NativeCoverageAccountV1.coverageIds[]": pick(d["NativeCoverageAccountV1"]["properties"]["coverageIds"]["items"]),
        "CandidateProducerResultV1.universe": pick(d["CandidateProducerResultV1"]["properties"]["universe"]),
        "CandidateProducerResultV1.groupDigests[]": pick(d["CandidateProducerResultV1"]["properties"]["groupDigests"]["items"]),
        "CandidateSourceBodyV1.contentSha256": pick(d["CandidateSourceBodyV1"]["properties"]["contentSha256"]),
        "CandidateSourceBodyV1.universe": pick(d["CandidateSourceBodyV1"]["properties"]["universe"]),
        "IncomingSearchV1.sourceUniverse": pick(inc["properties"]["sourceUniverse"]),
        "IncomingSearchV1.targetUniverse": pick(inc["properties"]["targetUniverse"]),
        "IncomingSearchV1.expectedInventoryRefs[]": pick(inc["properties"]["expectedInventoryRefs"]["items"]),
    }
    want = {
        "enumerationPlanDigest": ("canonical-record", "foundation/enumeration-plan.schema.v1.json#"),
        "analysisSpecDigest": ("canonical-record", "foundation/identity-schemas.v3.json#/$defs/analysis-spec"),
        "candidateResultRefs[]": ("canonical-record", EXECUTION_INPUTS_DOC + "#/$defs/CandidateProducerResultV1"),
        "InputRefV1.digest": ("by-domain", "x-opensip-digest-domains"),
        "StageReceiptV1.stageSpecDigest": ("canonical-record", "foundation/identity-schemas.v3.json#/$defs/stage-spec"),
        "CellProgramOutcomeV1.universe": ("h-identity", "native-semantic-universe"),
        "CellProgramOutcomeV1.inventoryDigests[]": ("canonical-record", "foundation/subject-inventory.schema.v1.json#"),
        "CellProgramOutcomeV1.viewDigests[]": ("h-identity", "view"),
        "CellProgramOutcomeV1.candidateResultDigest": ("canonical-record", EXECUTION_INPUTS_DOC + "#/$defs/CandidateProducerResultV1"),
        "NativeCoverageAccountV1.sourceUniverse": ("h-identity", "native-semantic-universe"),
        "NativeCoverageAccountV1.coverageIds[]": ("h-identity", "coverage"),
        "CandidateProducerResultV1.universe": ("h-identity", "native-semantic-universe"),
        "CandidateProducerResultV1.groupDigests[]": ("canonical-record", "native/native-evidence.schemas.v2.json#/$defs/CloneCandidateGroupV2"),
        "CandidateSourceBodyV1.contentSha256": ("raw-artifact", None),
        "CandidateSourceBodyV1.universe": ("h-identity", "native-semantic-universe"),
        "IncomingSearchV1.sourceUniverse": ("h-identity", "native-semantic-universe"),
        "IncomingSearchV1.targetUniverse": ("h-identity", "native-semantic-universe"),
        "IncomingSearchV1.expectedInventoryRefs[]": ("canonical-record", "foundation/subject-inventory.schema.v1.json#"),
    }

    def target_of(annotation):
        record = annotation.get("record") or {}
        if "document" in record:
            return record["document"] + record["selector"]
        return annotation.get("domainSet") or annotation.get("domain") or annotation.get("registry")

    mismatched = {k: (a["representation"], target_of(a)) for k, a in declared.items()
                  if (a["representation"], target_of(a)) != want[k]}
    row("A1", "each-of-the-18-positions-declares-its-own-representation-and-target", len(declared) == 18 and not mismatched, mismatched)
    row("A1", "not-every-position-is-raw-sha256",
        sorted({a["representation"] for a in declared.values()}) == ["by-domain", "canonical-record", "h-identity", "raw-artifact"])
    row("A1", "every-position-states-its-retention", all(a.get("retention", "preimage") == "preimage" for a in declared.values()))

    stripped = copy.deepcopy(ei)
    stripped["properties"]["enumerationPlanDigest"].pop("x-opensip-digest")
    row("A1", "sweep-sees-a-removed-leaf-annotation",
        M.foundation_digest_annotation_coverage(stripped)["unannotated"] == ["#/enumerationPlanDigest"])
    blanket = copy.deepcopy(ei)
    blanket["$defs"]["CellProgramOutcomeV1"]["properties"]["viewDigests"]["items"].pop("x-opensip-digest")
    blanket["$defs"]["DigestHex"]["x-opensip-digest"] = {"representation": "raw-artifact", "artifact": "blanket"}
    row("A1", "an-annotation-on-the-terminal-digest-def-is-not-a-blanket-exemption",
        "#/$defs/CellProgramOutcomeV1/viewDigests[]" in M.foundation_digest_annotation_coverage(blanket)["unannotated"])
    branch = copy.deepcopy(ei)
    universe = branch["$defs"]["CellProgramOutcomeV1"]["properties"]["universe"]
    universe["oneOf"][0] = dict(universe["oneOf"][0], **{"x-opensip-digest": universe.pop("x-opensip-digest")})
    row("A1", "a-nullable-branch-annotation-covers-its-branch", M.foundation_digest_annotation_coverage(branch)["unannotated"] == [])
    row("A1", "identity-schemas-and-relation-document-keep-their-own-sweeps",
        all(doc in M.FOUNDATION_DIGEST_LAW_OWN_SWEEP for doc in ("foundation/identity-schemas.v3.json", "foundation/relation-payload-schemas.v2.json")))

    graph = EI.F.build_file_inputs()
    result, _ = EI.full_run(graph)
    row("A1", "real-run-walks-the-annotated-execution-inputs-and-closes", result["runId"].startswith("run3:"), result["runId"])
    copies = identity_copies(EI)
    try:
        for m in copies:
            m._FOUNDATION_DOCUMENTS[EXECUTION_INPUTS_DOC] = stripped
            m._FOUNDATION_DIGEST_LAW_ADMITTED.discard(EXECUTION_INPUTS_DOC)
        got = refusal_any(lambda: EI.full_run(EI.F.build_file_inputs()))
        row("A1", "real-run-refuses-when-the-walked-document-loses-an-annotation",
            got is not None and "FOUNDATION_DIGEST_UNANNOTATED:" + EXECUTION_INPUTS_DOC + ":#/enumerationPlanDigest" in got, got)
    finally:
        for m in copies:
            m._FOUNDATION_DOCUMENTS.pop(EXECUTION_INPUTS_DOC, None)
            m._FOUNDATION_DIGEST_LAW_ADMITTED.discard(EXECUTION_INPUTS_DOC)


# ------------------------------------------------------------------------------------------------ A2
FROZEN_ENUMERATION_PLAN_DOCUMENT_SHA256 = "62ff499e024b83150fee7ce62c449553a3bc2021e0476975f922cdceef806237"


def a2():
    plan_doc = M.foundation_record_document("foundation/enumeration-plan.schema.v1.json")
    record = plan_doc["properties"]["scopeDigest"]["x-opensip-digest"]["record"]
    row("A2", "scope-digest-record-names-identity-schemas-v3",
        record == {"bundle": "identity", "document": "foundation/identity-schemas.v3.json", "selector": "#/$defs/scope-descriptor"}, record)
    texts = {name: (HERE / name).read_text() for name in ("enumeration-plan.schema.v1.json", "subject-inventory.schema.v1.json")}
    row("A2", "neither-document-still-names-identity-schemas-v2", all("identity-schemas.v2" not in t for t in texts.values()))
    row("A2", "every-named-v3-definition-exists",
        all(name in M.SCHEMA["$defs"] for name in ("scope-descriptor", "LogicalPath", "Text"))
        and set(M.DIGESTS["languageModes"]["map"]) == set(plan_doc["$defs"]["LanguageMode"]["enum"])
        if "LanguageMode" in plan_doc.get("$defs", {}) else all(name in M.SCHEMA["$defs"] for name in ("scope-descriptor", "LogicalPath", "Text")))
    digest = hashlib.sha256((HERE / "enumeration-plan.schema.v1.json").read_bytes()).hexdigest()
    row("A2", "registered-enumeration-plan-document-is-new-candidate-bytes", digest != FROZEN_ENUMERATION_PLAN_DOCUMENT_SHA256, digest)
    row("A2", "the-parameter-registry-resolves-the-new-document-bytes", M.parameter_row_of(digest) is not None)
    row("A2", "the-frozen-document-digest-no-longer-resolves-a-parameter-row",
        M.parameter_row_of(FROZEN_ENUMERATION_PLAN_DOCUMENT_SHA256) is None)


# ------------------------------------------------------------------------------------------------ M3
def native_cases_fixtures():
    return json.loads((KIT / "native/native-cases.v2.json").read_text())["fixtures"]


def m3():
    EI, _ = owners()
    ENUM = load("c24_enumeration_model", HERE / "enumeration_model.v1.py")
    NV = ENUM.NV
    colocated = NV.discover_units(native_cases_fixtures()["markersColocated"])
    files = ["src/main.rs", "src/lib.rs", "index.ts", "scripts/x.js", "Cargo.toml", "package.json", "tsconfig.json",
             "notes.xyz", "README.md"]
    base = NV.assign_membership(colocated["units"], files)

    def law(membership):
        faults = []
        ENUM._membership_order_law(membership, faults)
        return faults

    row("M3", "discovered-colocated-units-are-rust-then-tsjs-with-index-ordinals",
        [(u["rootPath"], u["languageFamily"], u["unitOrdinal"]) for u in base["units"]] == [("", "rust", 0), ("", "tsjs", 1)], base["units"])
    row("M3", "rows-are-utf8-path-ordered-and-projections-follow-row-order",
        [r["path"] for r in base["rows"]] == sorted(files, key=lambda p: p.encode("utf-8"))
        and base["unsupportedFiles"] == ["notes.xyz"], [r["path"] for r in base["rows"]])
    row("M3", "a-canonical-membership-passes-the-law", law(base) == [], law(base))
    ORDER, DERIVED = "ENUMERATION_MEMBERSHIP_ORDER", "ENUMERATION_MEMBERSHIP_ROW_DERIVATION"

    def swap_units(m):
        m["units"].reverse()
        remap = {}
        for index, unit in enumerate(m["units"]):
            remap[unit["unitOrdinal"]] = index
            unit["unitOrdinal"] = index
        for r in m["rows"]:
            if r["unitOrdinal"] is not None:
                r["unitOrdinal"] = remap[r["unitOrdinal"]]

    def reason_rewritten(m):
        readme = next(r for r in m["rows"] if r["path"] == "README.md")
        readme.update(membership="unsupported-file", reason="no-bundled-grammar")
        m["unsupportedFiles"] = [r["path"] for r in m["rows"] if r["membership"] == "unsupported-file"]

    def outside(ordinal):
        def go(m):
            notes = next(r for r in m["rows"] if r["path"] == "notes.xyz")
            notes.update(membership="outside-project-boundary", reason="nested-project", unitOrdinal=ordinal)
            m["unsupportedFiles"], m["outsideBoundaryFiles"] = [], ["notes.xyz"]
        return go

    controls = [
        ("rows-reversed", lambda m: m["rows"].reverse(), [ORDER]),
        ("duplicate-row", lambda m: m["rows"].insert(1, copy.deepcopy(m["rows"][0])), [ORDER]),
        ("units-out-of-order-with-consistent-ordinals", swap_units, [ORDER]),
        ("unit-ordinal-is-not-its-index", lambda m: m["units"][1].update(unitOrdinal=5), [ORDER, DERIVED]),
        ("member-package-roots-unsorted", lambda m: m["units"][0].update(memberPackageRoots=["crates/b", "crates/a"]), [ORDER]),
        ("unsupported-files-projection-dropped", lambda m: m.update(unsupportedFiles=[]), [ORDER]),
        ("row-membership-and-reason-rewritten", reason_rewritten, [DERIVED]),
        ("program-member-row-points-at-the-other-family", lambda m: next(r for r in m["rows"] if r["path"] == "index.ts").update(unitOrdinal=0), [DERIVED]),
        ("outside-boundary-row-with-an-ordinal", outside(0), [DERIVED]),
        ("outside-boundary-row-with-null-ordinal-is-lawful", outside(None), []),
        ("missing-row-is-left-to-the-coverage-join", lambda m: m["rows"].pop(0), []),
    ]
    for name, mutate, expected in controls:
        m = copy.deepcopy(base)
        mutate(m)
        got = law(m)
        row("M3", "law-" + name, got == expected, got)

    # native-evidence section 1.4 U-4b.2: a tsjs unit's unitKind is the projection of its languageMode, and the TS/JS kinds
    # belong to tsjs units only. unitKind enters PlanId through membershipDigest, so the published projection is checked at
    # the owner (NV.TSJS_UNIT_KIND, used by discover_units) and at every enumeration admission (the law, ORDER).
    published = {"ts-tsconfig": "ts-program", "js-allowjs": "js-program", "js-synthesized": "js-program"}
    table = getattr(NV, "TSJS_UNIT_KIND", None)
    row("M3", "tsjs-unit-kind-owner-projection-is-the-published-closed-table",
        table == published and set(published) == set(ENUM.TS_MODES)
        and set(published.values()) <= set(NV.SCHEMAS["$defs"]["WorkspaceUnitV2"]["properties"]["unitKind"]["enum"]), table)
    owner_text = " ".join((KIT.parents[1] / "v2/contracts/product-v1/native-evidence.md").read_text().split())
    row("M3", "tsjs-unit-kind-law-is-stated-in-the-normative-owner", TSJS_UNIT_KIND_LAW in owner_text)
    marker_sha = "d" * 64
    for label, markers, expected_unit in (
            ("ts-tsconfig", {"tsconfig.json": {"sha256": marker_sha}},
             ("ts-tsconfig", "ts-program", "tsconfig.json", "typescript-config")),
            ("js-allowjs-from-a-tsconfig-marker", {"tsconfig.json": {"sha256": marker_sha, "allowJs": True}},
             ("js-allowjs", "js-program", "tsconfig.json", "typescript-config")),
            ("js-allowjs-from-a-jsconfig-marker", {"jsconfig.json": {"sha256": marker_sha}},
             ("js-allowjs", "js-program", "jsconfig.json", "typescript-config")),
            ("js-synthesized", {"package.json": {"sha256": marker_sha}},
             ("js-synthesized", "js-program", "package.json", "node-package"))):
        found = NV.discover_units(markers)["units"]
        got_unit = tuple(found[0][k] for k in ("languageMode", "unitKind", "markerPath", "recognizerId")) if len(found) == 1 else found
        row("M3", "discovered-tsjs-unit-" + label, got_unit == expected_unit, got_unit)
        canonical = NV.assign_membership(found, ["index.ts", "lib.js", "README.md"])
        row("M3", "law-admits-the-published-unit-kind-" + label, law(canonical) == [], law(canonical))
        reminted = copy.deepcopy(canonical)
        reminted["units"][0]["unitKind"] = "js-program" if expected_unit[1] == "ts-program" else "ts-program"
        row("M3", "law-refuses-a-reminted-unit-kind-" + label, law(reminted) == [ORDER], law(reminted))
    rust = NV.assign_membership(NV.discover_units({"Cargo.toml": {"sha256": marker_sha, "isCargoWorkspace": False}})["units"], ["src/main.rs"])
    fallback_only = NV.assign_membership([dict(NV.SYNTAX_ONLY_FALLBACK_UNIT, unitOrdinal=0)], ["a.ts"])
    tsjs_ts = NV.assign_membership(NV.discover_units({"tsconfig.json": {"sha256": marker_sha}})["units"], ["index.ts"])
    for name, membership, mutate, expected in (
            ("rust-unit-canonical-kind-is-lawful", rust, lambda m: None, []),
            ("rust-unit-carrying-js-program", rust, lambda m: m["units"][0].update(unitKind="js-program"), [ORDER]),
            ("fallback-unit-carrying-ts-program", fallback_only, lambda m: m["units"][0].update(unitKind="ts-program"), [ORDER]),
            ("tsjs-unit-with-a-non-tsjs-mode", tsjs_ts, lambda m: m["units"][0].update(languageMode="rust-cargo"), [ORDER])):
        m = copy.deepcopy(membership)
        mutate(m)
        row("M3", "law-" + name, law(m) == expected, law(m))

    # Real complete Runs: the syntax graph fixture's membership is built by THE FIXTURE'S native copy and mutated before
    # it is hashed into membershipDigest, so the whole Plan is coherent and only the membership law can object. Run
    # closure re-derives with its own, unpatched copies. fixture_helpers() re-executes its definitions on every call,
    # so the build is given ONE cached namespace whose assign_membership is patched, then both are restored.
    real_fixture_helpers = EI.F.fixture_helpers
    helpers = real_fixture_helpers()
    original = helpers.N.assign_membership
    fallback = dict(NV.SYNTAX_ONLY_FALLBACK_UNIT, unitOrdinal=0)

    def run_with(build_membership):
        def patched(units, files, boundaries=None):
            return build_membership(list(files))
        helpers.N.assign_membership = patched
        EI.F.fixture_helpers = lambda: helpers
        try:
            graph = EI.F.build_file_inputs()
        finally:
            EI.F.fixture_helpers = real_fixture_helpers
            helpers.N.assign_membership = original
        return graph, refusal_any(lambda: EI.full_run(graph))

    def mutate_after(fn, units=()):
        def build(files):
            membership = original([dict(u) for u in units], files)
            fn(membership)
            return membership
        return build

    graph, got = run_with(mutate_after(lambda m: None))
    row("M3", "real-run-canonical-membership-closes", got is None, got)
    graph, got = run_with(mutate_after(lambda m: None, [fallback]))
    row("S3", "real-run-marker-free-membership-with-the-fallback-unit-closes",
        got is None and graph["membership"]["units"] == [fallback], got)

    def rewritten_reason(m):
        readme = next(r for r in m["rows"] if r["path"] == "README.md")
        readme.update(membership="unsupported-file", reason="no-bundled-grammar")
        m["unsupportedFiles"] = [r["path"] for r in m["rows"] if r["membership"] == "unsupported-file"]

    for name, fn, units, token in (
            ("rows-reversed", lambda m: m["rows"].reverse(), (), ORDER),
            ("row-reason-rewritten", rewritten_reason, (), DERIVED),
            ("fallback-unit-ordinal-not-its-index", lambda m: m["units"][0].update(unitOrdinal=1), [fallback], ORDER),
            ("unsupported-projection-dropped", lambda m: m.update(unsupportedFiles=[]), (), ORDER),
            ("missing-row", lambda m: m["rows"].pop(), (), "ENUMERATION_ADMISSION_PRECONDITION"),
            ("duplicate-row", lambda m: m["rows"].append(copy.deepcopy(m["rows"][-1])), (), ORDER),
            ("fallback-unit-reminted-with-a-tsjs-unit-kind", lambda m: m["units"][0].update(unitKind="js-program"), [fallback], ORDER)):
        graph, got = run_with(mutate_after(fn, units))
        row("M3", "real-run-refuses-" + name, got is not None and token in got, got)

<<<<<<< /tmp/opensip-design-corrections/root-nested-workspace-integration.v1/before/docs/coop/design-corrections/foundation/check-native-consumer24-corrections.v1.py
    # Real complete Runs with a discovered TS/JS unit: the published kind closes; a kind reminted BEFORE membershipDigest
    # (so the whole Plan is coherent) must refuse at Run closure rather than admit a second PlanId for the same project.
    for label, markers in (("ts-tsconfig", {"tsconfig.json": {"sha256": "d" * 64}}),
                           ("js-allowjs-from-a-tsconfig-marker", {"tsconfig.json": {"sha256": "d" * 64, "allowJs": True}}),
                           ("js-synthesized", {"package.json": {"sha256": "d" * 64}})):
        units = NV.discover_units(markers)["units"]
        graph, got = run_with(mutate_after(lambda m: None, units))
        row("M3", "real-run-closes-with-the-published-unit-kind-" + label,
            got is None and graph["membership"]["units"][0]["unitKind"] == units[0]["unitKind"], got)
        wrong = "js-program" if units[0]["unitKind"] == "ts-program" else "ts-program"
        graph, got = run_with(mutate_after(lambda m, w=wrong: m["units"][0].update(unitKind=w), units))
        row("M3", "real-run-refuses-a-reminted-unit-kind-" + label, got is not None and ORDER in got, got)
=======
    # U-4b.2 over a nested Cargo workspace: the fold target is the surviving outer workspace UNIT, never the folded
    # nested workspace manifest (looking that up as a unit raised StopIteration), and the law sees the fold through
    # the member roots that decide `target` pruning.
    cargo = lambda digit, ws: {"sha256": digit * 64, "isCargoWorkspace": ws}
    nested = NV.discover_units({"Cargo.toml": cargo("1", True), "nested/Cargo.toml": cargo("2", True),
                                "nested/pkg/Cargo.toml": cargo("3", False), "nested-x/Cargo.toml": cargo("4", False)})
    row("M3", "nested-cargo-workspace-folds-into-the-surviving-outer-unit",
        [(u["rootPath"], u["unitKind"], u["memberPackageRoots"]) for u in nested["units"]]
        == [("", "cargo-workspace", ["nested", "nested-x", "nested/pkg"])], nested["units"])
    nested_base = NV.assign_membership(nested["units"], ["nested-x/src/lib.rs", "nested/pkg/src/lib.rs",
                                                        "nested/pkg/target/debug/x.rs", "nested/target/debug/y.rs"])
    row("M3", "nested-cargo-workspace-membership-passes-the-law", law(nested_base) == [], law(nested_base))
    for name, roots, expected in (
            ("nested-member-roots-in-segment-not-utf8-order", ["nested", "nested/pkg", "nested-x"], [ORDER]),
            ("folded-nested-member-dropped-unprunes-its-target", ["nested", "nested-x"], [DERIVED])):
        m = copy.deepcopy(nested_base)
        m["units"][0]["memberPackageRoots"] = roots
        got = law(m)
        row("M3", "law-" + name, got == expected, got)
>>>>>>> /tmp/opensip-design-corrections/root-nested-workspace-integration.v1/author/docs/coop/design-corrections/foundation/check-native-consumer24-corrections.v1.py


# ------------------------------------------------------------------------------------------------ S3
def s3():
    N = M.native_admission()
    fixtures = native_cases_fixtures()
    fallback = dict(N.SYNTAX_ONLY_FALLBACK_UNIT, unitOrdinal=0)
    bare = N.discover_units({})
    row("S3", "marker-free-zero-config-discovery-yields-exactly-the-fallback-unit",
        bare["refused"] is None and bare["units"] == [fallback], bare["units"])
    installed = N.discover_units(N.synthetic_marker_set(0, 3, root_marker=False))
    row("S3", "installed-dependency-markers-only-still-yield-the-fallback",
        installed["refused"] is None and installed["units"] == [fallback]
        and [t["path"] for t in installed["prunedTrees"]] == ["node_modules"], installed["units"])
    inventory = {"schemaVersion": 2, "source": "security.discovery", "selectedRoot": "/home/alice/repo",
                 "nestedRepositories": [], "nestedProjects": ["apps/site"], "custodyExcludedUnits": [], "prunedTrees": []}
    nested = N.discover_units({"apps/site/package.json": {"sha256": "1" * 64}}, None, inventory)
    row("S3", "markers-only-inside-a-nested-project-yield-the-fallback-for-this-project",
        nested["refused"] is None and nested["units"] == [fallback]
        and [x["path"] for x in nested["boundaries"]["excludedUnits"]] == ["apps/site"], nested)
    explicit = N.discover_units({}, ["."])
    row("S3", "explicit-roots-get-no-fallback-and-still-refuse-without-a-marker",
        explicit["units"] == [] and (explicit["refused"] or {}).get("detail") == "native.explicit-root-without-marker",
        explicit.get("refused"))
    mixed = N.discover_units({"package.json": {"sha256": "1" * 64}})
    row("S3", "mixed-repositories-get-no-fallback", [u["languageFamily"] for u in mixed["units"]] == ["tsjs"], mixed["units"])
    colocated = N.discover_units(fixtures["markersColocated"])
    row("S3", "marker-bearing-discovery-is-unchanged",
        [(u["rootPath"], u["languageFamily"], u["unitOrdinal"], u["provenance"]) for u in colocated["units"]]
        == [("", "rust", 0, "DISCOVERED"), ("", "tsjs", 1, "DISCOVERED")], colocated["units"])
    files = ["a.rs", "web/b.ts", "README.md", "data.json", "blob.bin"]
    with_fallback, without = N.assign_membership([fallback], files), N.assign_membership([], files)
    row("S3", "the-fallback-claims-no-row",
        with_fallback["rows"] == without["rows"] and all(r["unitOrdinal"] is None for r in with_fallback["rows"]), with_fallback["rows"])
    mixed_rows = N.assign_membership(mixed["units"], ["index.ts", "tools/gen.rs", "README.md"])["rows"]
    row("S3", "mixed-repo-grammar-readable-file-outside-every-unit-is-disclosed-not-claimed",
        next(r for r in mixed_rows if r["path"] == "tools/gen.rs")
        == {"path": "tools/gen.rs", "languageFamily": "rust", "unitOrdinal": None, "membership": "syntax-only",
            "reason": "no-program-unit-for-language"}, mixed_rows)
    selection = N.default_capability_selection([fallback], fixtures["registry"])
    requested = selection["analysisSpec"]["requestedCapabilities"]
    row("S3", "default-selection-over-the-fallback-requests-the-full-syntax-only-product",
        requested != [] and sorted(r["capabilityId"] for r in requested) == N.required_default_capabilities("syntax-only")
        and all(r["languageMode"] == "syntax-only" and r["workspaceRoot"] == "." and r["required"] is True for r in requested),
        requested)
    got = refusal_any(lambda: N.default_capability_selection([], fixtures["registry"]))
    row("S3", "default-selection-over-zero-units-refuses-instead-of-an-empty-request",
        got is not None and "NATIVE_DEFAULT_SELECTION_WITHOUT_UNIT" in got, got)
    scope = N.unit_scope_descriptor([fallback], [], None, bare["prunedTrees"], None)["scopeDescriptor"]
    row("S3", "fallback-scope-is-the-project-root-with-conventional-exclusions",
        scope["workspaceRoots"] == ["."] and {".git", "node_modules"} <= set(scope["excludedPathPrefixes"]), scope)


# ------------------------------------------------------------------------------------------------ A4
def a4():
    layout = {"schemaVersion": 1, "entries": [
        {"packageName": "left-pad", "packageVersion": "1.3.0", "installPath": "node_modules/left-pad",
         "realPath": "node_modules/left-pad", "contentSha256": "1" * 64},
        {"packageName": "lib", "packageVersion": "0.1.0", "installPath": "node_modules/lib",
         "realPath": "packages/lib", "contentSha256": "2" * 64}]}

    def faults(paths, layouts=(layout,)):
        return M.snapshot_pruned_tree_faults([{"path": p} for p in paths], list(layouts))

    first_party = ["Cargo.toml", "src/lib.rs", "packages/target/index.ts", "src/target/x.ts", "web/a.ts"]
    row("A4", "first-party-custody-walk-rows-are-lawful", faults(first_party) == [])
    row("A4", "files-read-inside-listed-packages-are-lawful",
        faults(first_party + ["node_modules/left-pad/index.js", "node_modules/lib/dist/index.d.ts"]) == [])
    row("A4", "an-unlisted-package-file-is-not-a-read",
        faults(first_party + ["node_modules/other/index.js"]) == ["node_modules/other/index.js"])
    row("A4", "a-package-directory-prefix-is-segment-bounded",
        faults(["node_modules/left-pad-extra/index.js"]) == ["node_modules/left-pad-extra/index.js"])
    row("A4", "without-a-committed-read-set-no-dependency-row-is-lawful",
        faults(["node_modules/left-pad/index.js"], ()) == ["node_modules/left-pad/index.js"])
    row("A4", "vcs-tree-rows-are-never-reads", faults([".git/HEAD", "sub/.hg/store/data"]) == [".git/HEAD", "sub/.hg/store/data"])
    nested_vcs = ["node_modules/left-pad/" + segment + "/metadata" for segment in (".git", ".hg", ".svn", ".jj")]
    row("A4", "listed-package-read-allowance-never-overrides-nested-vcs", faults(nested_vcs) == sorted(nested_vcs))
    row("A4", "nested-vcs-lookalike-segments-remain-lawful-package-reads",
        faults(["node_modules/left-pad/.git-like/index.js", "node_modules/left-pad/.gitignore"]) == [])
    # Explicit nested package custody (identity section 3). Helper rows call the owner join directly over synthetic
    # layouts; the real-Run rows below admit altered layouts through the maintained fixture constructors.

    def with_rows(*extra_rows):
        return {"schemaVersion": 1, "entries": sorted(layout["entries"] + [
            {"packageName": name, "packageVersion": "1.0.0", "installPath": install, "realPath": real, "contentSha256": "4" * 64}
            for name, install, real in extra_rows], key=lambda r: r["installPath"].encode())}

    evil = "node_modules/left-pad/node_modules/evil"
    row("A4", "a-listed-package-authorizes-its-ordinary-descendants",
        faults(["node_modules/left-pad/index.js", "node_modules/left-pad/dist/index.d.ts"]) == [])
    row("A4", "an-enclosing-listed-package-never-authorizes-a-nested-installed-package",
        faults([evil + "/index.js", evil + "/package.json"]) == [evil + "/index.js", evil + "/package.json"])
    listed_evil = with_rows(("evil", evil, evil))
    row("A4", "a-separately-listed-nested-package-authorizes-its-own-files",
        faults([evil + "/index.js", evil + "/lib/x.js"], (listed_evil,)) == [])
    row("A4", "a-nested-package-row-does-not-authorize-deeper-or-sibling-nested-packages",
        faults([evil + "/node_modules/deeper/index.js", "node_modules/left-pad/node_modules/other/index.js"], (listed_evil,))
        == [evil + "/node_modules/deeper/index.js", "node_modules/left-pad/node_modules/other/index.js"])
    row("A4", "nested-vcs-refuses-even-inside-a-separately-listed-nested-package",
        faults([evil + "/.git/HEAD", evil + "/.jj/repo"], (listed_evil,)) == [evil + "/.git/HEAD", evil + "/.jj/repo"])
    scoped_inner = "node_modules/@scope/util/node_modules/@inner/pkg"
    scoped_row = ("@scope/util", "node_modules/@scope/util", "node_modules/@scope/util")
    row("A4", "a-listed-scoped-package-authorizes-its-ordinary-descendants",
        faults(["node_modules/@scope/util/index.js", "node_modules/@scope/util/lib/a.js"], (with_rows(scoped_row),)) == [])
    row("A4", "a-nested-scoped-package-needs-its-own-row",
        faults([scoped_inner + "/index.js"], (with_rows(scoped_row),)) == [scoped_inner + "/index.js"]
        and faults([scoped_inner + "/index.js"], (with_rows(scoped_row, ("@inner/pkg", scoped_inner, scoped_inner)),)) == [])
    row("A4", "lookalike-and-case-variant-segments-are-no-nested-package-boundary",
        faults(["node_modules/left-pad/node_modules-like/index.js", "node_modules/left-pad/Node_modules/x/index.js",
                "node_modules/left-pad/my_node_modules/index.js"]) == [])
    store = "node_modules/.pnpm/store-pkg@1.0.0/node_modules/store-pkg"
    store_rows = (("store-pkg", "node_modules/store-pkg", store), ("store-pkg", store, store))
    row("A4", "a-listed-store-realpath-authorizes-its-ordinary-descendants",
        faults([store + "/index.js", store + "/lib/deep/x.js", "node_modules/store-pkg/index.js"], (with_rows(*store_rows),)) == [])
    row("A4", "a-nested-package-below-a-listed-store-realpath-needs-its-own-row",
        faults([store + "/node_modules/dep/index.js", "node_modules/.pnpm/store-pkg@1.0.0/node_modules/dep/index.js"],
               (with_rows(*store_rows),))
        == ["node_modules/.pnpm/store-pkg@1.0.0/node_modules/dep/index.js", store + "/node_modules/dep/index.js"]
        and faults([store + "/node_modules/dep/index.js"],
                   (with_rows(*store_rows, ("dep", store + "/node_modules/dep", store + "/node_modules/dep")),)) == [])
    row("A4", "a-first-party-realpath-keeps-first-party-custody-and-its-nested-dependency-needs-a-row",
        faults(["packages/lib/src/index.ts"]) == []
        and faults(["packages/lib/node_modules/x/index.js"]) == ["packages/lib/node_modules/x/index.js"]
        and faults(["packages/lib/node_modules/x/index.js"],
                   (with_rows(("x", "packages/lib/node_modules/x", "packages/lib/node_modules/x")),)) == [])
    row("A4", "discovery-still-reports-the-outermost-anchor-for-a-nested-package-read",
        M.native_admission().DD.classify_path(evil + "/index.js", set()) == ("node_modules", "dependency-tree"))
    row("A4", "cargo-build-output-rows-are-never-reads",
        faults(first_party + ["target/debug/app.d"]) == ["target/debug/app.d"])
    native_schema = json.loads((KIT / "native/native-evidence.schemas.v2.json").read_text())
    layout_description = native_schema["$defs"]["ResolvedNodeModulesLayoutV1"]["description"]
    row("A4", "registered-layout-description-states-the-read-set-law",
        "SNAPSHOT_PRUNED_TREE_NOT_A_READ" in layout_description
        and "ARE snapshot inventory rows" in layout_description
        and "stay in their owning toolchain and stdlib closures" in layout_description
        and "so an inventory row could not exist for them" not in layout_description, layout_description[:200])

    def ts_run(extra, packages=None):
        """A real complete Run. `packages` adds installed-package manifests to the fixture's layout for this Run only:
        the maintained constructors mint the altered layout, native context, universe, Plan and every dependent
        identity, then seed admission, derive, replay and close_run run as usual. The global is restored afterwards."""
        scope = SR.S.helpers().native_inputs.__globals__
        saved = scope["TS_NODE_MODULES"]
        if packages is not None:
            scope["TS_NODE_MODULES"] = {**saved, **packages}
        try:
            graph = SR.S.build_ts_semantic_graph(atom=SR.REFS_EXISTS_SRC, has_declares=False, has_references_fact=True,
                                                 extra_sources=extra)
            return SR.close_positive(graph)
        finally:
            scope["TS_NODE_MODULES"] = saved

    def ts_context_layout(result):
        run, objects, blobs, _ = result
        for digest in objects[run["planId"]][1]["nativeContextDigests"]:
            domain, context = M.parse_h_frame(blobs[digest], "native-context")[:2]
            if domain == "native.context.typescript.v2":
                return context, sorted(e["installPath"] for e in C.parse(blobs[context["nodeModulesLayoutDigest"]])["entries"])
        return None, []

    got = refusal_any(lambda: ts_run({"node_modules/left-pad/index.js": b"module.exports = 1;\n"}))
    row("A4", "real-run-with-a-file-read-inside-a-listed-package-closes", got is None, got)
    got = refusal_any(lambda: ts_run({"docs/extra.md": b"# extra\n"}))
    row("A4", "real-run-control-with-an-extra-first-party-file-closes", got is None, got)
    got = refusal_any(lambda: ts_run({"node_modules/left-pad/.git-like/index.js": b"module.exports = 1;\n"}))
    row("A4", "real-run-package-vcs-lookalike-remains-lawful", got is None, got)
    for name, extra in (("an-unlisted-dependency-file", {"node_modules/unlisted/index.js": b"module.exports = 2;\n"}),
                        ("a-vcs-tree-file", {".git/HEAD": b"ref: refs/heads/main\n"}),
                        ("listed-package-nested-git-metadata", {"node_modules/left-pad/.git/HEAD": b"ref: refs/heads/main\n"}),
                        ("listed-package-nested-mercurial-metadata", {"node_modules/left-pad/.hg/store/data": b"metadata\n"})):
        got = refusal_any(lambda e=extra: ts_run(e))
        row("A4", "real-run-refuses-" + name, got is not None and "SNAPSHOT_PRUNED_TREE_NOT_A_READ" in got, got)
    # Explicit nested package custody on the same actual full-Run fixture.
    evil_manifest = {evil + "/package.json": b'{"name":"evil","version":"0.0.1"}\n'}
    inner_manifest = {scoped_inner + "/package.json": b'{"name":"@inner/pkg","version":"0.0.1"}\n'}
    for name, extra, packages in (
            ("an-unlisted-nested-package-under-a-listed-package", {evil + "/index.js": b"module.exports = 3;\n"}, None),
            ("an-unlisted-nested-scoped-package-under-a-listed-scoped-package", {scoped_inner + "/index.js": b"module.exports = 4;\n"}, None),
            ("nested-vcs-inside-a-separately-listed-nested-package", {evil + "/.git/HEAD": b"ref: refs/heads/main\n"}, evil_manifest)):
        path = next(iter(extra))
        got = refusal_any(lambda e=extra, p=packages: ts_run(e, p))
        row("A4", "real-run-refuses-" + name, got is not None and got.endswith("SNAPSHOT_PRUNED_TREE_NOT_A_READ:" + path), got)
    base_context, base_layout = ts_context_layout(ts_run({"node_modules/left-pad/index.js": b"module.exports = 1;\n"}))
    for name, extra, packages, installed in (
            ("the-nested-package-separately-listed", {evil + "/index.js": b"module.exports = 3;\n"}, evil_manifest, evil),
            ("the-nested-scoped-package-separately-listed", {scoped_inner + "/index.js": b"module.exports = 4;\n"}, inner_manifest,
             scoped_inner)):
        path = next(iter(extra))
        try:
            result = ts_run(extra, packages)
        except Exception as exc:  # noqa: BLE001 - a refused positive is a failed control
            row("A4", "real-run-closes-with-" + name, False, type(exc).__name__ + ":" + str(exc))
            continue
        run, objects, blobs, actual = result
        context, installs = ts_context_layout(result)
        ok = (installed in installs and installed not in base_layout
              and context["nodeModulesLayoutDigest"] != base_context["nodeModulesLayoutDigest"]
              and M.close_run(run, objects, blobs) == actual["runId"]
              and any(r["path"] == path for r in objects[run["snapshotId"]][1]["sourceInventory"]))
        row("A4", "real-run-closes-with-" + name, ok, {"runId": actual["runId"], "layout": installs})
    for name, path in (("a-nested-lookalike-segment", "node_modules/left-pad/node_modules-like/index.js"),
                       ("a-listed-scoped-package-file", "node_modules/@scope/util/index.js")):
        got = refusal_any(lambda p=path: ts_run({p: b"module.exports = 5;\n"}))
        row("A4", "real-run-closes-with-" + name, got is None, got)


# ------------------------------------------------------------------------------------------------ S1
def s1():
    semantic = SR.S
    operation = semantic.STAGE_OUTPUT_OPERATION
    path = M.stage_output_schema_member_path(operation)
    row("S1", "member-path-is-the-operation-segment-under-the-interface-directory",
        path == "opensip-interface/stage-output/derive-semantic-view.schema.json", path)
    for label, bad in (("parent-escape", "../escape"), ("two-segments", "a/b"), ("uppercase", "Upper"), ("empty", ""),
                       ("leading-dot", ".hidden"), ("too-long", "x" * 129), ("not-text", 7)):
        got = refusal(lambda b=bad: M.stage_output_schema_member_path(b))
        row("S1", "operation-that-is-not-one-path-segment-refuses-" + label,
            got is not None and "STAGE_OUTPUT_SCHEMA_OPERATION_NOT_A_PATH_SEGMENT" in got, got)
    annotation = M.SCHEMA["$defs"]["stage-spec"]["properties"]["outputSchemaDigest"]["x-opensip-digest"]
    row("S1", "annotation-publishes-the-producer-interface-registration",
        annotation.get("artifactClass") == "producer-interface-stage-output-schema"
        and annotation["registeredBy"]["closureField"] == "producerClosure"
        and annotation["registeredBy"]["treePath"] == "opensip-interface/stage-output/{operation}.schema.json", annotation)

    document = copy.deepcopy(semantic.STAGE_OUTPUT_SCHEMA)

    def member(raw_bytes, at=path):
        return {"path": at, "sha256": hashlib.sha256(raw_bytes).hexdigest(), "bytes": len(raw_bytes)}

    def spec_for(raw_bytes, **over):
        return dict({"operation": operation, "outputDomains": ["view"], "outputSchemaDigest": hashlib.sha256(raw_bytes).hexdigest()}, **over)

    raw = C.canonical(document)
    row("S1", "a-registered-member-admits", refusal(lambda: M.admit_stage_output_schema(spec_for(raw), {"tree": [member(raw)]}, raw)) is None)

    def refuses(case, spec, tree, raw_bytes, token):
        refuses_with("S1", case, lambda: M.admit_stage_output_schema(spec, {"tree": tree}, raw_bytes), token)

    refuses("retained-bytes-without-a-tree-member-are-not-a-registration", spec_for(raw), [], raw, "STAGE_OUTPUT_SCHEMA_UNREGISTERED")
    refuses("a-member-at-another-operations-path-does-not-register-this-one", spec_for(raw),
            [member(raw, M.stage_output_schema_member_path("derive-other-view"))], raw, "STAGE_OUTPUT_SCHEMA_UNREGISTERED")
    other = C.canonical(dict(document, **{"$id": "urn:opensip:fixture:other-output"}))
    refuses("a-member-with-other-bytes-is-a-registration-mismatch", spec_for(other), [member(raw)], other,
            "STAGE_OUTPUT_SCHEMA_REGISTRATION_MISMATCH")
    variants = {
        "registered-bytes-that-are-not-json": (b"not a schema document", "STAGE_OUTPUT_SCHEMA_DOCUMENT_INVALID"),
        "registered-document-without-the-2020-12-dialect": (C.canonical({k: v for k, v in document.items() if k != "$schema"}), "STAGE_OUTPUT_SCHEMA_DOCUMENT_INVALID"),
        "registered-document-that-is-not-a-valid-schema": (C.canonical(dict(document, type=5)), "STAGE_OUTPUT_SCHEMA_DOCUMENT_INVALID"),
        "declaration-names-another-operation": (C.canonical(dict(document, **{"x-opensip-stage-output": dict(document["x-opensip-stage-output"], operation="derive-other-view")})), "STAGE_OUTPUT_SCHEMA_DECLARATION_MISMATCH"),
        "declaration-names-other-output-domains": (C.canonical(dict(document, **{"x-opensip-stage-output": dict(document["x-opensip-stage-output"], outputDomains=["fact"])})), "STAGE_OUTPUT_SCHEMA_DECLARATION_MISMATCH"),
        "document-without-a-declaration": (C.canonical({k: v for k, v in document.items() if k != "x-opensip-stage-output"}), "STAGE_OUTPUT_SCHEMA_DECLARATION_MISMATCH"),
    }
    for case, (variant, token) in variants.items():
        refuses(case + "-refuses", spec_for(variant), [member(variant)], variant, token)

    # Real complete Runs through the TypeScript semantic fixture, whose provider closure registers the schema.
    def build(**patch):
        saved = {name: getattr(semantic, name) for name in patch}
        for name, value in patch.items():
            setattr(semantic, name, value)
        try:
            return semantic.build_ts_semantic_graph(atom=SR.REFS_EXISTS_SRC, has_declares=False, has_references_fact=True)
        finally:
            for name, value in saved.items():
                setattr(semantic, name, value)

    graph = build()
    got = refusal_any(lambda: SR.close_positive(graph))
    provider_trees = [v["tree"] for k, (d, v) in graph["objects"].items() if d == "closure" and v["kind"] == "provider"]
    row("S1", "real-run-with-a-producer-registered-output-schema-closes",
        got is None and any(any(r["path"] == path for r in tree) for tree in provider_trees), got)
    for case, patch, token in (
            ("schema-retained-but-registered-at-another-path", {"STAGE_OUTPUT_MEMBER_PATH": "opensip-interface/stage-output/somewhere-else.schema.json"}, "STAGE_OUTPUT_SCHEMA_UNREGISTERED"),
            ("declaration-for-another-operation", {"STAGE_OUTPUT_SCHEMA": dict(document, **{"x-opensip-stage-output": dict(document["x-opensip-stage-output"], operation="derive-other-view")})}, "STAGE_OUTPUT_SCHEMA_DECLARATION_MISMATCH"),
            ("document-without-the-2020-12-dialect", {"STAGE_OUTPUT_SCHEMA": {k: v for k, v in document.items() if k != "$schema"}}, "STAGE_OUTPUT_SCHEMA_DOCUMENT_INVALID")):
        graph = build(**patch)
        got = refusal_any(lambda g=graph: SR.close_positive(g))
        row("S1", "real-run-refuses-" + case, got is not None and token in got, got)


# ------------------------------------------------------------------------------------------------ S2
def s2():
    EI, _ = owners()
    sha = lambda raw: hashlib.sha256(raw).hexdigest()  # noqa: E731
    law = M.DIGESTS["normalizationSpecificationLaw"]
    row("S2", "law-names-one-record-and-one-closure-path",
        law["record"] == {"bundle": "identity", "selector": "#/$defs/normalization-specification-map"}
        and law["closureTreePath"] == "opensip-interface/normalization/specification-map.v1.json")
    rows = M.DIGESTS["domainSets"]["native-semantic-universe"]
    owners_by_domain = {name: (r["languageVersionBinding"]["normalizationClosure"]["path"], r["languageVersionBinding"]["normalizationClosure"]["kind"])
                        for name, r in rows.items()}
    row("S2", "every-universe-names-its-interpreting-closure",
        owners_by_domain == {"native.semantic-universe.typescript.v2": (["toolClosure", "closureId"], "toolchain"),
                             "native.semantic-universe.rust.v2": (["toolClosure", "closureId"], "toolchain"),
                             "native.semantic-universe.syntax.v2": (["grammarBundle", "closureId"], "grammar")}, owners_by_domain)
    row("S2", "each-named-closure-field-is-a-published-closure-join-of-that-context",
        all({"path": path, "form": "closure2-identity", "kind": kind} in M.DIGESTS["domainSets"]["native-context"][r["contextDomain"]]["closureJoins"]
            for r, (path, kind) in ((rows[n], owners_by_domain[n]) for n in rows)))

    l0, l1 = b'{"level":"L0-verbatim"}\n', b'{"level":"L1-lexical"}\n'
    store = {}

    def put(raw):
        store[sha(raw)] = raw
        return sha(raw)

    def blob_of(digest):
        if digest not in store:
            raise M.EvidenceUnavailable(digest)
        return store[digest]

    def mapping(*levels):
        return {"schemaVersion": 1, "normalizerId": "opensip-normalizer",
                "levels": [{"level": lv, "specificationDigest": dg} for lv, dg in levels]}

    def closure_of(files):
        for raw in files.values():
            put(raw)
        return {"tree": sorted(({"path": p, "sha256": sha(raw), "bytes": len(raw)} for p, raw in files.items()),
                               key=lambda r: r["path"].encode())}

    spec, other = put(l0), put(l1)
    good = closure_of({"grammar/normalize.l0.spec": l0, M.NORMALIZATION_MAP_PATH: C.canonical(mapping(("L0-verbatim", spec)))})
    row("S2", "a-mapped-in-closure-level-specification-admits",
        refusal(lambda: M.admit_normalization_specification("L0-verbatim", spec, good, blob_of)) is None)

    def refuses(case, level, version, closure, token):
        got = refusal_any(lambda: M.admit_normalization_specification(level, version, closure, blob_of))
        row("S2", case, got is not None and token in got, got)

    refuses("a-closure-without-a-map-refuses", "L0-verbatim", spec, closure_of({"grammar/normalize.l0.spec": l0}), "BODY_NORMALIZATION_MAP_MISSING")
    refuses("a-level-the-map-does-not-name-refuses", "L1-lexical", other, good, "BODY_NORMALIZATION_LEVEL_UNMAPPED")
    refuses("another-levels-specification-swapped-in-refuses", "L0-verbatim", other, good, "BODY_NORMALIZATION_LEVEL_VERSION_MISMATCH")
    outside = closure_of({"grammar/normalize.l0.spec": l0, M.NORMALIZATION_MAP_PATH: C.canonical(mapping(("L0-verbatim", other)))})
    outside["tree"] = [r for r in outside["tree"] if r["sha256"] != other or r["path"] == M.NORMALIZATION_MAP_PATH]
    refuses("a-map-pointing-outside-its-own-closure-refuses", "L0-verbatim", other, outside, "BODY_NORMALIZATION_SPECIFICATION_NOT_IN_CLOSURE")
    pretty = json.dumps(mapping(("L0-verbatim", spec)), indent=2).encode()
    refuses("non-canonical-map-bytes-refuse", "L0-verbatim", spec,
            closure_of({"grammar/normalize.l0.spec": l0, M.NORMALIZATION_MAP_PATH: pretty}), "BODY_NORMALIZATION_MAP_INVALID")
    refuses("an-unordered-map-refuses", "L0-verbatim", spec,
            closure_of({"a": l0, "b": l1, M.NORMALIZATION_MAP_PATH: C.canonical(mapping(("L1-lexical", other), ("L0-verbatim", spec)))}),
            "BODY_NORMALIZATION_MAP_INVALID")
    refuses("a-map-with-an-undeclared-key-refuses", "L0-verbatim", spec,
            closure_of({"grammar/normalize.l0.spec": l0, M.NORMALIZATION_MAP_PATH: C.canonical(dict(mapping(("L0-verbatim", spec)), extra=1))}),
            "BODY_NORMALIZATION_MAP_INVALID")
    lost_map = copy.deepcopy(good)
    lost_map["tree"].append({"path": "opensip-interface/normalization/specification-map.v1.json.lost", "sha256": "e" * 64, "bytes": 1})
    lost_map["tree"] = [dict(r, sha256="e" * 64) if r["path"] == M.NORMALIZATION_MAP_PATH else r for r in lost_map["tree"]]
    refuses("missing-map-bytes-are-retention-loss", "L0-verbatim", spec, lost_map, "EvidenceUnavailable")

    # Real complete Runs: one L0 clones body fact under the syntax universe of the mixed graph fixture.
    grammar_files = EI.F.fixture_helpers().GRAMMAR_FILES
    fixture_spec_bytes = grammar_files["grammar/normalize.l0.spec"]
    fixture_spec = sha(fixture_spec_bytes)
    manifest_digest = sha(grammar_files["grammar/bundle.manifest"])

    def run_with(option):
        graph = EI.F.build_file_inputs(clones_fact_subjects=["src/index.ts"], atom_override=EI.NONE_ATOM, clone_body_fact=option)
        facts = [v for k, (d, v) in graph["objects"].items() if d == "fact" and v["relation"] == "clones"]
        return graph, facts, refusal_any(lambda: EI.full_run(graph))

    graph, facts, got = run_with({"map": mapping(("L0-verbatim", fixture_spec)), "specificationBytes": fixture_spec_bytes})
    row("S2", "real-run-with-a-closure-mapped-level-specification-closes", got is None and len(facts) == 1, got)
    foreign = b'{"level":"L0-verbatim","owner":"not-the-grammar-closure"}\n'
    for case, option, token in (
            ("no-map-in-the-interpreting-closure", {"map": None, "specificationBytes": fixture_spec_bytes}, "BODY_NORMALIZATION_MAP_MISSING"),
            ("level-not-mapped", {"map": mapping(("L1-lexical", fixture_spec)), "specificationBytes": fixture_spec_bytes}, "BODY_NORMALIZATION_LEVEL_UNMAPPED"),
            ("another-closure-member-swapped-in-as-the-level-specification", {"map": mapping(("L0-verbatim", manifest_digest)), "specificationBytes": fixture_spec_bytes}, "BODY_NORMALIZATION_LEVEL_VERSION_MISMATCH"),
            ("retained-specification-outside-the-closure", {"map": mapping(("L0-verbatim", sha(foreign))), "specificationBytes": foreign}, "BODY_NORMALIZATION_SPECIFICATION_NOT_IN_CLOSURE")):
        graph, facts, got = run_with(option)
        row("S2", "real-run-refuses-" + case, len(facts) == 1 and got is not None and token in got, got)


SECTIONS = {"M1": m1, "M2": m2, "M3": m3, "S1": s1, "S2": s2, "S3": s3, "S4": s4, "A1": a1, "A2": a2, "A4": a4}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*")
    a = ap.parse_args(argv)
    for name, fn in SECTIONS.items():
        if a.only and name not in a.only:
            continue
        try:
            fn()
        except Exception as exc:  # a crashed section is a failed control, never a silent pass
            row(name, "section-crashed", False, "".join(traceback.format_exception_only(type(exc), exc)).strip()
                + " | " + traceback.format_exc().splitlines()[-3].strip())
    failed = [r for r in ROWS if not r["ok"]]
    print(json.dumps({"total": len(ROWS), "passed": len(ROWS) - len(failed), "failed": failed, "rows": ROWS}, indent=1))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
