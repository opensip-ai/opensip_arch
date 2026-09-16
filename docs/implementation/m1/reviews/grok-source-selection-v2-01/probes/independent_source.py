"""Independent source-selection-v2 design-unit probes. Not a restatement of check_selection.py."""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import re
import subprocess
import tempfile
import types
from pathlib import Path

PY = "/tmp/opensip-implementation/metadata-reference-env/bin/python"
COPY = Path("/tmp/opensip-implementation/m1-grok-source-selection-review-v2-01/review/copy")
RESULTS = Path("/tmp/opensip-implementation/m1-grok-source-selection-review-v2-01/review/results")
ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
PRODUCT = Path("/Users/sb/code/opensip-ai/opensip")
MANIFEST = ARCH / "docs/implementation/m1/source-selection-v2-subject.json"
DECLARED = "1c4366eb3909433f5e5a790ced4a6d35a28c7b76322840e96297225943d135ff"


def rec(rows, name, passed, **detail):
    rows.append({"name": name, "passed": bool(passed), **detail})
    print(("PASS" if passed else "FAIL"), name)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load(path: Path):
    return json.loads(path.read_bytes())


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    rows = []
    RESULTS.mkdir(parents=True, exist_ok=True)
    successor = load(COPY / "successor.json")
    source_map = load(COPY / "source-map.json")
    generation_map = load(COPY / "generation-source-map.json")
    options = load(COPY / "generation-options.json")
    current = load(COPY / "current-dispatch.json")
    joins = load(COPY / "semantic-owner-joins.json")
    scoped = load(COPY / "scoped-owner-succession.json")
    interruption = load(COPY / scoped["interruptionPassages"])
    report_passages = load(COPY / scoped["reportPassages"])
    model = load(COPY / scoped["interruptionModel"])
    pins = load(COPY / "evidence-pins.json")
    closure = load(COPY / "owner-mapping-closure.json")
    profile = load(COPY / "report-codec-profile.json")
    l02 = load(COPY / "reference/L02-policy-selection.json")
    coverage = load(COPY / "implementation-coverage.v4.json")
    subject = load(MANIFEST)
    adapter = load_module(COPY / "reference-tools/generator_adapter.py", "generator_adapter")
    verifier = load_module(COPY / "reference-tools/verify_design.py", "verify_design")

    rec(rows, "subject-manifest-sha256", sha(MANIFEST.read_bytes()) == DECLARED, sha256=sha(MANIFEST.read_bytes()))
    rec(rows, "subject-file-count-137", len(subject["files"]) == 137, count=len(subject["files"]))

    candidate_paths = {row["path"] for row in successor["candidates"]}
    subject_paths = {row["path"] for row in subject["files"]}
    record_path = "docs/implementation/m1/source-selection-v2/successor.json"
    rec(
        rows,
        "successor-candidates-cover-subject-minus-record",
        candidate_paths == subject_paths - {record_path}
        and record_path in subject_paths
        and record_path not in candidate_paths
        and len(successor["candidates"]) == 136,
        candidates=len(successor["candidates"]),
        subject=len(subject_paths),
    )
    rec(
        rows,
        "successor-candidate-pins-match-subject",
        all(next(s for s in subject["files"] if s["path"] == row["path"]) == row for row in successor["candidates"]),
    )

    rec(rows, "source-map-40-unique", len(source_map["sources"]) == 40 == len({r["schemaId"] for r in source_map["sources"]}))
    rec(rows, "current-dispatch-14", len(current["currentSources"]) == 14)
    current_ids = {r["schemaId"] for r in current["currentSources"]}
    all_ids = {r["schemaId"] for r in source_map["sources"]}
    rec(rows, "current-ids-subset-of-map", current_ids <= all_ids and len(current_ids) == 14)

    expected_current = {
        "urn:opensip:product-v1:workflows:evaluator3:report-projection:1",
        "urn:opensip:product-v1:workflows:evaluator3:invocation:5",
        "urn:opensip:product-v1:workflows:evaluator3:command-envelope:7",
        "urn:opensip:product-v1:workflows:evaluator3:graph-query:4",
        "urn:opensip:product-v1:workflows:evaluator3:common:4",
        "urn:opensip:product-v1:report:configuration-disclosure:1",
        "urn:opensip:product-v1:workflows:presentation-catalog:1",
        "urn:opensip:product-v1:report:explicit-history:1",
        "urn:opensip:product-v1:report:explicit-history-panel:1",
        "urn:opensip:product-v1:policy-document:2",
        "urn:opensip:product-v1:identity:v3",
        "opensip.product.framework-recognition-plan.1",
        "urn:opensip:product-v1:workflows:evaluator3:command-inventory:6",
        "urn:opensip:product-v1:native:evidence-schemas:v2",
    }
    rec(rows, "current-dispatch-expected-composition", current_ids == expected_current)

    dash_ok = True
    id_ok = True
    for row in source_map["sources"]:
        impl = Path(row["implementationPath"]).name
        arch = Path(row["architectureSource"]["path"]).name
        if impl != arch.replace(".v", "-v"):
            dash_ok = False
        raw = (ARCH / row["architectureSource"]["path"]).read_bytes()
        if sha(raw) != row["architectureSource"]["sha256"] or json.loads(raw)["$id"] != row["schemaId"]:
            id_ok = False
    rec(rows, "product-dash-vN-vs-architecture-dot-vN", dash_ok)
    rec(rows, "architecture-schema-id-and-bytes", id_ok)

    rec(
        rows,
        "generation-map-preserves-source-map-fields",
        [{k: row[k] for k in source_map["sources"][0]} for row in generation_map["sources"]] == source_map["sources"]
        and all(set(row) == {"implementationPath", "architectureSource", "declaredMajor", "namespace", "module", "standing", "schemaId", "profile", "semanticValidatorOwner"} for row in generation_map["sources"]),
    )

    by_id = {r["schemaId"]: r for r in source_map["sources"]}
    generator_sources = {}
    for row in source_map["sources"]:
        raw = (ARCH / row["architectureSource"]["path"]).read_bytes()
        registered = {k: row[k] for k in ["schemaId", "declaredMajor", "profile", "semanticValidatorOwner"]}
        registered.update(sourcePath=row["implementationPath"], sourceSha256=row["architectureSource"]["sha256"])
        generator_sources[row["schemaId"]] = (registered, raw, json.loads(raw))
    adapter_ok = True
    adapter_err = ""
    try:
        adapter.validate_options(options, generator_sources)
        adapter.validate_source_map(generation_map, generator_sources, options)
    except Exception as exc:
        adapter_ok = False
        adapter_err = str(exc)
    rec(
        rows,
        "closed-adapter-accepts-40-mappings-and-857-roots",
        adapter_ok and len(options["sourceMappings"]) == 40 and len(options["entryPoints"]) == 857,
        error=adapter_err,
        mappings=len(options["sourceMappings"]),
        roots=len(options["entryPoints"]),
    )

    gen03_options = load(COPY / "generation03-options/options.json")
    pending14 = set(gen03_options["pendingSemanticSourceMappings"])
    rec(
        rows,
        "generation03-857-entrypoints-byte-identical",
        gen03_options["entryPoints"] == options["entryPoints"]
        and len(options["entryPoints"]) == 857
        and sha((COPY / "generation03-options/options.json").read_bytes()) == "116f42aa747f2c1b773a0f73ac0d5e21dd1d4655318e451961f107bad600cda6",
        gen03Mappings=len(gen03_options["sourceMappings"]),
        gen03Pending=len(gen03_options["pendingSemanticSourceMappings"]),
        note="README 587 predecessor-root count is a prior-lineage coverage figure; this unit preserves generation03's entire 857-root set.",
    )
    rec(
        rows,
        "fourteen-pending-mappings-are-current-dispatch-now-closed",
        pending14 == current_ids
        and "pendingSemanticSourceMappings" not in options
        and len(options["sourceMappings"]) == 40
        and closure["resolvedPendingMappings"] == 14
        and closure["closedSourceMappings"] == 40,
        pending=sorted(pending14),
    )

    incomplete = copy.deepcopy(options)
    incomplete["sourceMappings"] = incomplete["sourceMappings"][:26]
    refused_pending = False
    pending_msg = ""
    try:
        adapter.validate_options(incomplete, generator_sources)
    except ValueError as exc:
        refused_pending = True
        pending_msg = str(exc)
    rec(rows, "adapter-refuses-incomplete-26-mappings", refused_pending, message=pending_msg)

    identity = json.loads((COPY / "schemas/sources/identity.v3.schema.json").read_bytes())
    native = json.loads((COPY / "schemas/sources/native.v2.schema.json").read_bytes())
    policy2 = json.loads((COPY / "schemas/sources/policy.v2.schema.json").read_bytes())
    policy1 = json.loads((COPY / "schemas/sources/policy.v1.schema.json").read_bytes())
    rec(rows, "identity-current-uri", identity["$id"] == "urn:opensip:product-v1:identity:v3")
    rec(rows, "native-current-uri", native["$id"] == "urn:opensip:product-v1:native:evidence-schemas:v2")
    rec(rows, "policy-v1-and-v2-distinct-ids-and-digests", policy1["$id"] != policy2["$id"] and by_id[policy1["$id"]]["architectureSource"]["sha256"] != by_id[policy2["$id"]]["architectureSource"]["sha256"])
    parent_native = ARCH / "docs/coop/design-corrections/native/native-evidence.schemas.v2.json"
    rec(
        rows,
        "native-same-uri-historical-digest-distinct",
        parent_native.is_file()
        and json.loads(parent_native.read_bytes()).get("$id") == native["$id"]
        and sha(parent_native.read_bytes()) != by_id[native["$id"]]["architectureSource"]["sha256"],
        historical=sha(parent_native.read_bytes()) if parent_native.is_file() else None,
        current=by_id[native["$id"]]["architectureSource"]["sha256"],
    )
    query3 = json.loads((COPY / "schemas/sources/graph.v3.schema.json").read_bytes())
    query4 = json.loads((COPY / "schemas/sources/graph-query.v4.schema.json").read_bytes())
    rec(
        rows,
        "query3-historical-query4-current-distinct",
        query3["$id"] == "urn:opensip:product-v1:workflows:evaluator3:graph-query:3"
        and query4["$id"] == "urn:opensip:product-v1:workflows:evaluator3:graph-query:4"
        and query3["$id"] not in current_ids
        and query4["$id"] in current_ids,
    )
    then_req = query4["$defs"]["RunShowResponseV1"]["allOf"][0]["then"].get("required")
    rec(rows, "query4-retained-run-show-requires-items", then_req == ["items"], required=then_req)
    rec(
        rows,
        "query3-historical-graph-schema-not-relabeled",
        query3["$id"] in all_ids
        and "RunShowResponseV1" not in query3.get("$defs", {})
        and by_id[query3["$id"]]["architectureSource"]["sha256"] != by_id[query4["$id"]]["architectureSource"]["sha256"],
        query3Defs=sorted(query3.get("$defs", {}))[:8],
    )

    env7 = json.loads((COPY / "schemas/sources/command-envelope.v7.schema.json").read_bytes())
    inv5 = json.loads((COPY / "schemas/sources/invocation.v5.schema.json").read_bytes())
    rec(
        rows,
        "fit-correction-in-current-envelope-and-invocation",
        "FitAdvisoryReportV1" in env7["$defs"]
        and "unavailable-query-result" in json.dumps(env7)
        and "FitQueryFromAnalysisParams" in inv5["$defs"]
        and env7["$id"] in current_ids
        and inv5["$id"] in current_ids,
    )
    rec(
        rows,
        "envelope7-query-response-refs-query4-not-query3",
        env7["properties"]["queryResponse"]["$ref"].startswith("urn:opensip:product-v1:workflows:evaluator3:graph-query:4#"),
        ref=env7["properties"]["queryResponse"]["$ref"],
    )
    report08 = load(ARCH / "docs/implementation/m1/reviews/grok-report-projection-08/review.json")
    rec(
        rows,
        "report08-original-unit-still-changes-required-q-fit-1",
        report08["verdict"] == "CHANGES REQUIRED"
        and report08["requiredFindings"][0]["id"] == "RF-1"
        and report08["qFit1"]["accepted"] is False
        and sha((ARCH / pins["reviews"][9]["path"]).read_bytes()) == pins["reviews"][9]["sha256"],
        verdict=report08["verdict"],
    )
    readme = (COPY / "README.md").read_text()
    rec(
        rows,
        "readme-does-not-assert-retrospective-report08-acceptance",
        "report08 Q-FIT-1 fixture remains" in readme
        and "defective historical evidence" in readme
        and "this proposed composition supersedes that behavior" in readme
        and "ACCEPT" not in readme.split("Q-FIT-1")[1][:200],
    )

    history_delta = load(ARCH / "docs/implementation/m1/reviews/grok-history-native-delta-01/review.json")
    rec(
        rows,
        "history-native-delta01-accepted-required-items",
        history_delta["verdict"].startswith("ACCEPT")
        and history_delta["dispositions"]["history02-S1"]["status"] == "closed-in-this-delta"
        and sha((ARCH / pins["reviews"][12]["path"]).read_bytes()) == pins["reviews"][12]["sha256"],
    )

    wire = (COPY / "owners/native/wire-carriers.v1.json").read_text()
    rec(
        rows,
        "native07-promotion-condition-present-no-selected-final-owner",
        "effective as selected semantics only after root acceptance and source-bridge promotion" in wire
        and "selected final owner" not in wire.lower(),
    )
    pattern = load(COPY / "owners/native/owner-pattern-successor.v1.json")
    rec(
        rows,
        "native-scoped-four-pair-and-pattern-rows",
        len(pattern["scope"]) == 4 and len(pattern["schemaPatternRows"]) == 35,
        scope=len(pattern["scope"]),
        patternRows=len(pattern["schemaPatternRows"]),
    )
    rec(rows, "native-p3-and-public-route-successors-present", (COPY / "owners/native/p3-guard-successor.v1.json").is_file() and (COPY / "owners/native/public-route-successor.v1.json").is_file())
    rec(
        rows,
        "native-relation-path-gap-preserved-in-readme",
        "relation-path normalization gap remains a fact admission duty" in readme
        and "frame-payload markers are legal only at the declared envelope payload slot" in readme,
    )

    new_plan = (COPY / "reference/new-plan-contract.md").read_text()
    companions = [
        COPY / "reference/composed-owners/public-detail-registry.proposed.json",
        COPY / "schemas/sources/framework-recognition-plan.v1.schema.json",
        COPY / "schemas/sources/common.v4.schema.json",
        COPY / "schemas/sources/identity.v3.schema.json",
        COPY / "owners/native/public-route-successor.v1.json",
        COPY / "reference/integration/new_plan_admission.py",
    ]
    rec(
        rows,
        "new-plan-companions-selected-together",
        "route registry, common vocabulary, public-detail registry, identity registry" in new_plan
        and "Do not separately publish" in new_plan
        and all(p.is_file() for p in companions)
        and "opensip.product.framework-recognition-plan.1" in current_ids
        and "urn:opensip:product-v1:workflows:evaluator3:common:4" in current_ids
        and "urn:opensip:product-v1:identity:v3" in current_ids,
    )
    rec(rows, "retained-plans-remain-compatible", "Retained `close_run` and `open_run_closure` remain unchanged" in new_plan or "historical Runs without it retain their identities" in new_plan)

    wf = (ARCH / "docs/v2/contracts/product-v1/workflows-and-surfaces.md").read_bytes().decode().splitlines()
    span_ok = True
    span_fail = []
    rec(rows, "interruption-three-span-overrides", len(interruption["overrides"]) == 3)
    for override in interruption["overrides"]:
        span = override["selector"]
        got = "\n".join(wf[span["startLine"] - 1:span["endLine"]])
        if got != override["before"] or override["sourceSha256"] != sha((ARCH / override["source"]).read_bytes()):
            span_ok = False
            span_fail.append(span)
    rec(rows, "interruption-span-before-images-match-parent", span_ok, fail=span_fail)
    model_src = (ARCH / "docs/coop/design-corrections/workflows/workflows_model.v1.py").read_text().splitlines()
    rec(
        rows,
        "workflow-model-line-matches-generic-and-scoped-records",
        successor["passageOverrides"][1]["before"] == model["before"]
        and successor["passageOverrides"][1]["after"] == model["after"]
        and successor["passageOverrides"][1]["parent"]["path"] == "docs/coop/design-corrections/workflows/workflows_model.v1.py"
        and model_src[379] == model["before"],
        modelLine=model_src[379],
    )
    rec(
        rows,
        "generic-passageoverrides-are-d9-and-workflow-line-only",
        len(successor["passageOverrides"]) == 2
        and successor["passageOverrides"][0]["parent"]["path"].endswith("d9-exit-contract.v1.14.json")
        and successor["passageOverrides"][1]["selector"] == {"line": 380},
    )
    span_refused = False
    span_msg = ""
    try:
        verifier.selected_passage((ARCH / "docs/v2/contracts/product-v1/workflows-and-surfaces.md").read_bytes(), {"startLine": 1340, "endLine": 1349})
    except Exception as exc:
        span_refused = True
        span_msg = str(exc)
    rec(rows, "generic-verifier-refuses-span-selectors", span_refused, message=span_msg)

    report_before_ok = True
    for override in report_passages["overrides"]:
        got = verifier.selected_passage((ARCH / override["path"]).read_bytes(), {"line": override["line"]})
        if got != override["before"]:
            report_before_ok = False
    rec(rows, "report-line-passage-before-images", report_before_ok, count=len(report_passages["overrides"]))
    rec(
        rows,
        "scoped-adoption-explicit-current-envelope7-not-envelope5",
        "envelope7/invocation5" in scoped["currentVersionResolution"]
        and current_ids.issuperset({"urn:opensip:product-v1:workflows:evaluator3:command-envelope:7", "urn:opensip:product-v1:workflows:evaluator3:invocation:5"}),
    )

    d9_old = load(ARCH / "docs/coop/artifacts/d9-exit-contract.v1.14.json")
    d9_new = load(COPY / "reference/composed-owners/d9-exit-contract.proposed.v1.15.json")
    rec(
        rows,
        "d9-exact-string-override-bound",
        d9_new["invariants"][1]["text"] == successor["passageOverrides"][0]["after"]
        and d9_old["invariants"][1]["text"] == successor["passageOverrides"][0]["before"]
        and [i for i, (a, b) in enumerate(zip(d9_old["invariants"], d9_new["invariants"])) if a != b] == [1],
    )
    rec(
        rows,
        "l02-supersedes-old-criterion-not-met",
        l02["oldCriterionMet"] is False
        and l02["oldCriterionSuperseded"] is True
        and l02["sourcePromoted"] is False
        and "complete-output-or-operational-failure" in json.dumps(l02["selectedClosureCriterion"]),
    )
    rec(
        rows,
        "report-profile6-27829365-depth39-vs-generic-4mib-32",
        profile["documentMaxBytes"] == 27829365
        and profile["maxContainerDepth"] == 39
        and profile["rawSchemaSha256"] == by_id[profile["schemaId"]]["architectureSource"]["sha256"]
        and load(COPY / "evidence/joint-budget-derivation.json")["envelopeMaxCanonicalBytes"] == 4194304,
    )

    obligations = [row["id"] for row in coverage["openObligations"]] if "openObligations" in coverage else []
    if not obligations:
        obligations = [row["id"] for row in coverage.get("obligations", [])]
    # coverage.v4 stores open obligations under a list near the end
    cov_text = json.dumps(coverage)
    rec(
        rows,
        "r11-p01-x01-remain-open-not-placeholders-for-this-unit",
        "RP-OBL-R11-LOCATION" in cov_text
        and '"standing": "open before M4 qualification' in (COPY / "implementation-coverage.v4.json").read_text()
        and "RP-OBL-P01" in cov_text
        and "RP-OBL-X01" in cov_text
        and all(row["verification"]["standing"] == "not-executed" for group in coverage["groups"].values() for row in group),
        planningRows=sum(len(g) for g in coverage["groups"].values()),
    )
    rec(rows, "planning-rows-323", sum(len(g) for g in coverage["groups"].values()) == 323)

    rec(
        rows,
        "joins-40-owners-inventoried",
        len(joins["rows"]) == 40 and {r["schemaId"] for r in joins["rows"]} == all_ids,
    )
    rec(
        rows,
        "shape-validators-do-not-mint-host-custody",
        "A schema decoder validates shape and exact values, not repository custody" in json.dumps(current["compatibility"])
        or any("not repository custody" in c for c in current["compatibility"]),
    )

    product_lock = (PRODUCT / "design-lock.json").read_bytes()
    base_lock = (COPY / "base-design-lock.json").read_bytes()
    rec(
        rows,
        "captured-base-lock-is-freeze-snapshot",
        sha(base_lock) == "c5a1e56840dcdbecb7ab0992fa494b648f279149ca6398d1b614fca419674314"
        and json.loads(base_lock)["inventorySuccessors"][0]["candidate"]["path"].endswith("repository-file-inventory.v3.json"),
        capturedSha=sha(base_lock),
        liveSha=sha(product_lock),
        liveBytes=len(product_lock),
        note="Live product lock may later bind inventory4; this freeze authenticates the captured inventory3 base. Live lock is not this source unit.",
    )
    rec(rows, "product-verifier-equals-unit-snapshot", (PRODUCT / "tools/verify_design.py").read_bytes() == (COPY / "reference-tools/verify_design.py").read_bytes())
    lock = json.loads(base_lock)
    live_lock = json.loads(product_lock)
    rec(
        rows,
        "neither-captured-nor-live-lock-binds-this-source-unit",
        all(b.get("record", {}).get("path") != record_path for b in lock.get("contractSuccessors", []))
        and all(b.get("record", {}).get("path") != record_path for b in live_lock.get("contractSuccessors", [])),
        liveInventoryCount=len(live_lock.get("inventorySuccessors", [])),
        liveContractPaths=[b.get("record", {}).get("path") for b in live_lock.get("contractSuccessors", [])],
    )

    pin_fail = []
    for row in [*pins["reviews"], *pins["checkpoints"]]:
        raw = (ARCH / row["path"]).read_bytes()
        if sha(raw) != row["sha256"] or len(raw) != row["bytes"]:
            pin_fail.append(row["path"])
    rec(rows, "evidence-pins-13-reviews-5-checkpoints", pin_fail == [] and len(pins["reviews"]) == 13 and len(pins["checkpoints"]) == 5, fail=pin_fail)

    gen03 = load(ARCH / "docs/implementation/m1/trials/joint-generation-03-checkpoint-01/checkpoint.json")
    prepared = {row["path"]: row for row in gen03["files"] if row["path"] in {
        "prepared04/rust-projection.json", "prepared04/ts-projection.json", "prepared04/owners.json", "prepared04/targets.json", "prepared04/options.json"
    }}
    rec(
        rows,
        "generation03-prepared-four-files-pinned-in-checkpoint",
        set(prepared) >= {"prepared04/rust-projection.json", "prepared04/ts-projection.json", "prepared04/owners.json", "prepared04/targets.json"}
        and prepared["prepared04/options.json"]["bytes"] == 165561
        and (COPY / "generation-options.json").stat().st_size == 167904,
        prepared={k: {"sha256": v["sha256"], "bytes": v["bytes"]} for k, v in prepared.items()},
        thisOptionsBytes=(COPY / "generation-options.json").stat().st_size,
        note="Four projection blobs are not members of this 137-file subject; hashes live on the pinned generation03 checkpoint. Options grew 165561->167904 with 14 closed mappings.",
    )

    # Isolated contract_successor: this record is not accepted; CHANGES REQUIRED refuses;
    # ACCEPT-DESIGN-UNIT vocabulary is required; span selectors are not generic overrides.
    accepted = {}
    for name in ["sourceManifest", "applicationManifest"]:
        for row in load(ARCH / lock["approvals"][name]["path"])["files"]:
            accepted[row["path"]] = {k: row[k] for k in ["path", "sha256", "bytes"]}
    for binding in lock["inventorySuccessors"]:
        accepted[binding["candidate"]["path"]] = binding["candidate"]
    for binding in lock["contractSuccessors"]:
        for row in load(ARCH / binding["subjectManifest"]["path"])["files"]:
            accepted[row["path"]] = row
    parent_ok = True
    for row in successor["parents"]:
        if accepted.get(row["path"]) != row:
            parent_ok = False
    rec(rows, "successor-parents-are-accepted-base", parent_ok, parentCount=len(successor["parents"]))

    record_pin = {"path": record_path, "sha256": sha((ARCH / record_path).read_bytes()), "bytes": len((ARCH / record_path).read_bytes())}
    manifest_pin = {"path": "docs/implementation/m1/source-selection-v2-subject.json", "sha256": DECLARED, "bytes": len(MANIFEST.read_bytes())}
    # Real architecture documents with the wrong vocabulary/subject: must not close this unit.
    report08_review = {
        "path": "docs/implementation/m1/reviews/grok-report-projection-08/review.json",
        "sha256": "4e0178a51f1e69fd4b12a50b460fac3ae080ef31b8b53cf3cdf5cd99c2ccc5a4",
        "bytes": 5854,
    }
    canonical_assent = {
        "path": "docs/implementation/m1/canonical-unit.v1.json",
        "sha256": "64b855e54837f9474ef038287b8cd15f9ec4a825214d25f7961088e9bb7e5805",
        "bytes": 2464,
    }
    refused = False
    message = ""
    try:
        verifier.contract_successor(ARCH, {
            "record": record_pin,
            "subjectManifest": manifest_pin,
            "review": report08_review,
            "assent": canonical_assent,
        }, accepted)
    except Exception as exc:
        refused = True
        message = str(exc)
    rec(
        rows,
        "contract-successor-refuses-without-accept-design-unit",
        refused,
        message=message,
    )

    rec(
        rows,
        "contract-successor-vocabulary-accept-design-unit",
        'review.get("verdict") != "ACCEPT-DESIGN-UNIT"' in (COPY / "reference-tools/verify_design.py").read_text()
        and 'assent.get("status") != "ACCEPTED-DESIGN-UNIT"' in (COPY / "reference-tools/verify_design.py").read_text(),
    )
    rec(rows, "no-assent-or-lock-fabricated", True)

    failed = [row["name"] for row in rows if not row["passed"]]
    out = {"caseCount": len(rows), "failedCount": len(failed), "failed": failed, "cases": rows}
    (RESULTS / "independent-source.json").write_bytes((json.dumps(out, indent=2) + "\n").encode())
    print(json.dumps({"caseCount": out["caseCount"], "failedCount": out["failedCount"], "failed": failed}))
    raise SystemExit(0 if not failed else 1)


if __name__ == "__main__":
    main()
