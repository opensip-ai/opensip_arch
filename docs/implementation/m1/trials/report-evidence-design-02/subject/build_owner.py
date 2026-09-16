"""Owner record builder (author-02). Deterministic: every owner/ file is a pure function of pinned parents, identity_bridge and reference_model constants.

build(arch, M, bridge) -> {relative name: JSON value}; dump(value) -> exact bytes.
"""
import copy
import hashlib
import json

GQ = "urn:opensip:product-v1:workflows:evaluator3:graph-query:3#/$defs/"
C3 = "urn:opensip:product-v1:workflows:evaluator3:common:3#/$defs/"
N = "urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/"
SCHEMA = "https://json-schema.org/draft/2020-12/schema"
PARENT07 = "/tmp/opensip-implementation/m1-report-projection-subject-07"
PARENT07_MANIFEST_SHA256 = "cee1eb24159187c3dc967493046eb08e2f86e242ed55eab23fe944c2cd43e6c8"
SUBJECT01 = "/tmp/opensip-implementation/m1-report-evidence-design-subject-01"
SUBJECT01_MANIFEST_SHA256 = "0af84231305e54ec218a5efeff4f0489b02f9dc69ade0c6101c632c96ffaaa11"
REVIEW01 = "/tmp/opensip-implementation/m1-report-evidence-design-review-01"
PARAMETER_ID = "opensip.product.framework-recognition-plan.1"
REMOVED_FEATURES = ["coupling-importer-package-membership", "entry-point-recognition", "symbol-metrics", "test-reachability"]
HEX = {"type": "string", "pattern": "^[0-9a-f]{64}(?![\\s\\S])"}
SHA256_TEXT = {"type": "string", "pattern": "^sha256:[0-9a-f]{64}(?![\\s\\S])"}
UINT = {"$ref": C3 + "Uint53"}


def dump(value):
    return json.dumps(value, indent=1, ensure_ascii=False).encode("utf-8") + b"\n"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def obj(props, required=None, **extra):
    out = {"type": "object", "additionalProperties": False, "required": list(required if required is not None else props), "properties": props}
    out.update(extra)
    return out


def arr(items, max_items, order, min_items=0, unique=True):
    out = {"type": "array", "items": items, "maxItems": max_items, "x-opensip-order": order}
    if min_items:
        out["minItems"] = min_items
    if unique:
        out["uniqueItems"] = True
    return out


def enum(values):
    return {"type": "string", "enum": list(values)}


def const(value):
    return {"const": value}


def ref(name):
    return {"$ref": "#/$defs/" + name}


def present_state(data_def):
    return {"oneOf": [obj({"state": const("present"), "data": ref(data_def)}), ref("PanelNotPresentV1")]}


def report_defs(M):
    limitation = {"$ref": GQ + "GraphEvidenceDisclosure/properties/resolutionLimitations/items/properties/kind"}
    owner_key = {"type": "string", "pattern": "^owner1:[0-9a-f]{64}(?![\\s\\S])"}
    subject = {"$ref": C3 + "SubjectId"}
    universe = {"$ref": C3 + "Sha256Hex"}
    exchange = obj({"request": {"$ref": GQ + "GraphQueryRequestV1"}, "response": {"$ref": GQ + "GraphQueryResponseV1"}})
    reach = obj({"request": {"$ref": GQ + "GraphQueryRequestV1"}, "responseContext": {"$ref": GQ + "GraphOperationResponseContext"}})
    workspace_unit = obj({"unitOrdinal": UINT, "rootPath": {"$ref": N + "InternalUnitRootV1"}, "markerPath": {"type": "string", "minLength": 1, "maxLength": 4096},
                          "unitKind": enum(["js-program", "ts-program"]), "languageFamily": const("tsjs")})
    unit_id = dict(SHA256_TEXT, **{"x-opensip-digest": {"representation": "h-identity", "domain": "native.compilation-unit.v1", "form": "sha256-text", "retention": "derived",
                                                        "authority": "native"}})
    cargo_target = obj({"unitId": unit_id, "markerPath": {"$ref": C3 + "LogicalPath"}, "targetKind": {"$ref": N + "UnitIdentityV1/properties/targetKind"},
                        "targetName": {"$ref": N + "UnitIdentityV1/properties/targetName"}})
    owners = {"oneOf": [
        obj({"ownerKey": owner_key, "keyKind": const("first-party-package"), "packageManifestPath": {"$ref": C3 + "LogicalPath"},
             "packageName": {"type": "string", "minLength": 1, "maxLength": 4096}, "cargoTargets": arr(ref("CargoTargetRefV1"), 65536, {"by": ["unitId"]}),
             "workspaceUnit": {"oneOf": [ref("WorkspaceUnitRefV1"), {"type": "null"}]}}),
        obj({"ownerKey": owner_key, "keyKind": const("workspace-unit"), "workspaceUnit": ref("WorkspaceUnitRefV1")}),
        obj({"ownerKey": owner_key, "keyKind": const("external-package"), "packageManifestPath": {"$ref": C3 + "LogicalPath"},
             "packageName": {"type": "string", "minLength": 1, "maxLength": 4096}, "universe": universe}),
    ]}
    cell = obj({"fromOwnerKey": owner_key, "toOwnerKey": owner_key, "facts": UINT, "programEdges": UINT, "sourceDependencies": UINT, "importerSymbols": UINT,
                "sharedImporterFacts": UINT, "sharedTargetFacts": UINT, "internal": {"type": "boolean"}, "importerUniverses": arr(universe, 4096, "utf8", min_items=1)},
               description="facts = distinct fact2 observations; programEdges = distinct importer/target endpoint pairs (per universe); sourceDependencies = distinct (importer anchor paths, universe-independent target identity): the same source import observed by two programs is 2 facts and 1 source dependency.")
    drill = obj({"fromOwnerKey": owner_key, "toOwnerKey": owner_key, "factId": {"$ref": GQ + "FactId"}, "importer": {"$ref": GQ + "GraphEndpoint"},
                 "target": {"$ref": GQ + "GraphEndpoint"}, "importerAnchorPaths": arr({"$ref": C3 + "LogicalPath"}, 100000, "utf8", min_items=1),
                 "importerTestOrigin": enum(["no-test-origin-identity", "not-identified-as-test-origin", "test-origin"])})
    coupling = obj({
        "policy": const(M.COUPLING_POLICY), "runId": {"$ref": C3 + "RunId"}, "relation": const("imports"), "minResolution": const("resolved-target"),
        "projection": obj({"countBasis": {"$ref": GQ + "CountBasis"}, "factViewDigests": arr({"$ref": GQ + "ViewDigest"}, 100000, "canonical-set"),
                           "coverageIds": arr({"$ref": C3 + "CoverageId"}, 100000, "canonical-set"), "limitationKinds": arr(limitation, 12, "utf8"),
                           "deficiencyCitationCount": UINT}),
        "countUnits": const({"facts": "distinct-fact2-observations", "programEdges": "distinct-importer-target-endpoint-pairs-per-universe",
                             "sourceDependencies": "distinct-importer-anchor-paths-and-universe-independent-target-identity"}),
        "owners": arr(ref("CouplingOwnerV1"), 65536, {"by": ["ownerKey"]}),
        "ownerClosure": obj({"total": UINT, "listed": UINT, "rule": const("owners-referenced-by-listed-cells-and-target-buckets")}),
        "cells": arr(ref("CouplingCellV1"), 1000000, "sequence"), "cellsProjection": ref("ItemProjectionV1"),
        "importerBuckets": arr(obj({"cause": enum(M.IMPORTER_CAUSES), "facts": UINT}), len(M.IMPORTER_CAUSES), {"by": ["cause"]}),
        "targetBuckets": arr(obj({"fromOwnerKey": owner_key, "cause": enum(M.TARGET_CAUSES), "facts": UINT}), 1000000, "sequence"),
        "targetBucketsProjection": ref("ItemProjectionV1"),
        "totals": obj({k: UINT for k in ("distinctFacts", "attributedFacts", "importerUnattributedFacts", "targetUnattributedFacts", "cellCount", "cellFactSum",
                                        "targetBucketCount", "ownerCount", "importerSymbolPathOutsideAnchors")}),
        "absence": obj({"blankCellMeans": enum(["no-projected-fact", "not-determined-cells-omitted"]), "absenceSupported": {"type": "boolean"},
                        "blockers": arr(enum(M.COUPLING_BLOCKERS), len(M.COUPLING_BLOCKERS), "utf8")}),
        "drilldown": arr(ref("CouplingDrilldownRowV1"), M.MAX_DRILLDOWN, {"by": ["fromOwnerKey", "toOwnerKey", "factId"]}), "drilldownProjection": ref("ItemProjectionV1"),
        "provenance": const(M.COUPLING_PROVENANCE),
    }, description="R08 coupling over the whole admitted imports@resolved-target view. Cells are listed in priority order (facts descending, then keys) and byte-bounded under the report-wide remaining exploration budget; omitted cells make a blank cell not-determined.")
    metric_common = {"subjectId": subject, "metricId": enum(M.METRIC_IDS)}
    metric = {"oneOf": [
        obj(dict(metric_common, interpretation=const("static-projected-count"), request={"$ref": GQ + "GraphQueryRequestV1"}, response={"$ref": GQ + "GraphQueryResponseV1"},
                 countState=enum(["exact", "lower-bound"]), value=UINT, limitationKinds=arr(limitation, 12, "utf8"), zeroSupportsAbsence={"type": "boolean"})),
        obj(dict(metric_common, interpretation=const("static-projected-count"), request={"$ref": GQ + "GraphQueryRequestV1"}, response={"$ref": GQ + "GraphQueryResponseV1"},
                 countState=const("unknown"), cause=const("native-evidence-unavailable"))),
        obj(dict(metric_common, countState=const("unknown"), cause=const("subject-descriptor-not-retained"))),
    ]}
    recognizer = obj({"recognizerId": {"$ref": N + "FrameworkRecognitionResultV1/properties/recognizerId"}, "recognizerVersion": const(1),
                      "assurance": {"$ref": N + "FrameworkRecognitionResultV1/properties/assurance"}, "evidence": {"$ref": N + "FrameworkRecognitionResultV1/properties/evidence"},
                      "unresolvedChoices": {"$ref": N + "FrameworkRecognitionResultV1/properties/unresolvedChoices"},
                      "entryPointCount": {"type": "integer", "minimum": 0, "maximum": 65536},
                      "testGlobs": {"$ref": N + "FrameworkRecognitionResultV1/properties/effects/properties/testGlobs"}})
    recognition_unit = obj({"unitOrdinal": UINT, "rootPath": {"$ref": N + "InternalUnitRootV1"}, "markerPath": {"type": "string", "minLength": 1, "maxLength": 4096},
                            "recognitionId": SHA256_TEXT, "entryPoints": {"$ref": N + "EntryPointRecognitionV1"}, "effectiveSource": enum(["explicit", "none", "recognized"]),
                            "effectiveEntryPointCount": UINT, "recognizers": arr(ref("RecognizerSummaryV1"), 32, "sequence")})
    cargo_entry_target = obj({"unitId": unit_id, "markerPath": {"$ref": C3 + "LogicalPath"}, "targetKind": enum(M.ENTRY_TARGET_KINDS),
                              "targetName": {"$ref": N + "UnitIdentityV1/properties/targetName"}, "crateRootPath": {"oneOf": [{"$ref": C3 + "LogicalPath"}, {"type": "null"}]}})
    cargo_entries = {"oneOf": [
        obj({"universe": universe, "state": enum(["all", "none", "partial"]), "sourceUnitOwnershipId": SHA256_TEXT,
             "targets": arr(ref("CargoEntryTargetV1"), 65536, {"by": ["unitId"]}), "missingCoverage": arr(enum(M.CARGO_MISSING), len(M.CARGO_MISSING), "utf8")}),
        obj({"universe": universe, "state": const("unknown"), "sourceUnitOwnershipId": {"type": "null"}, "targets": arr(ref("CargoEntryTargetV1"), 0, "sequence"),
             "missingCoverage": arr(enum(M.CARGO_MISSING), len(M.CARGO_MISSING), "utf8", min_items=1)}),
    ], "description": "Every SELECTED bin/lib target of a Rust universe with its unique owned crate root (SourceUnitOwnershipV1 x RustUniverseV2ResolvedInputs.crateRootPaths). all only when every such target root is resolved from complete ownership."}
    recognition_state = {"oneOf": [
        obj({"state": const("not-plan-bound")}, description="The admitted Run's analysis-spec selects no FrameworkRecognitionPlanV1 parameter (every predecessor evaluator3 Run)."),
        obj({"state": const("unavailable"), "parameterDigest": HEX, "availability": enum(["corrupt", "expired", "partial", "purged", "unavailable"])}),
        obj({"state": const("plan-bound"), "parameterDigest": HEX, "availability": enum(["partial", "retained"]), "explicitEntryPointCount": UINT,
             "units": arr(ref("EntryRecognitionUnitV1"), 4096, "sequence"), "cargoTargetEntries": arr(ref("CargoTargetEntriesV1"), 1024, {"by": ["universe"]})}),
    ]}
    provenance = {"oneOf": [obj({"source": const("explicit")}),
                            obj({"source": const("cargo-target"), "unitId": unit_id, "targetKind": enum(M.ENTRY_TARGET_KINDS),
                                 "targetName": {"$ref": N + "UnitIdentityV1/properties/targetName"}, "markerPath": {"$ref": C3 + "LogicalPath"}}),
                            obj({"source": const("recognized"), "unitOrdinal": UINT, "recognizerId": {"$ref": N + "FrameworkRecognitionResultV1/properties/recognizerId"},
                                 "recognizerVersion": const(1), "assurance": {"$ref": N + "FrameworkRecognitionResultV1/properties/assurance"},
                                 "evidence": {"$ref": N + "FrameworkRecognitionResultV1/properties/evidence"},
                                 "unresolvedChoices": {"$ref": N + "FrameworkRecognitionResultV1/properties/unresolvedChoices"}})]}
    scope = {"scopeUniverse": universe, "scopeUnitOrdinal": {"oneOf": [UINT, {"type": "null"}]}}
    trace = {"oneOf": [
        obj({"subjectId": subject, "state": const("unknown"), "cause": enum(["recognition-not-plan-bound", "recognition-unavailable", "subject-descriptor-not-retained"])}),
        obj(dict(scope, subjectId=subject, state=const("unknown"), cause=enum(["origin-page-set-not-embedded", "reachability-evidence-unavailable"]), originQuery=ref("ReportGraphExchangeV1"))),
        obj(dict(scope, subjectId=subject, state=const("no-entry-origin"), originQuery=ref("ReportGraphExchangeV1"), originsExamined=UINT, originsUnattributed=UINT,
                 originsOutsideEntrySet=UINT, originUniverses=arr(universe, 100, "utf8"), blockers=arr(enum(M.TRACE_BLOCKERS), 3, "utf8"),
                 interpretation=const("no-entry-origin-among-projected-reachability-origins-not-dead-code"))),
        obj(dict(scope, subjectId=subject, state=enum(["path-found", "path-not-within-bound"]), originQuery=ref("ReportGraphExchangeV1"),
                 start=obj({"endpoint": {"$ref": GQ + "GraphEndpoint"}, "viaReachabilityFactId": {"$ref": GQ + "FactId"}, "attributionPath": {"$ref": C3 + "LogicalPath"},
                            "entry": obj({"path": {"$ref": C3 + "LogicalPath"}, "provenance": arr(ref("EntryProvenanceV1"), 65536, "sequence", min_items=1)})}),
                 path=ref("ReportGraphExchangeV1"))),
    ]}
    origin_evidence = {"oneOf": [
        obj({"kind": const("rust-test-target"), "unitIds": arr(SHA256_TEXT, 65536, "utf8", min_items=1)}),
        obj({"kind": const("recognized-test-glob"), "unitOrdinal": UINT, "recognizerId": const("vitest-jest"), "glob": {"type": "string", "minLength": 1, "maxLength": 256},
             "relativePath": {"$ref": C3 + "LogicalPath"}}),
    ]}
    interp = const("native-static-origin-identity-not-imported-execution")
    origin_set = {"oneOf": [
        obj({"universe": universe, "interpretation": interp, "source": const("none"), "completeness": const("none"), "cause": enum(M.ORIGIN_NONE_CAUSES),
             "limitations": arr(enum(M.ORIGIN_LIMITATIONS), 0, "utf8"), "originCount": const(0)}),
        obj({"universe": universe, "interpretation": interp, "source": const("rust-test-targets"), "completeness": const("partial"),
             "limitations": arr(enum(M.ORIGIN_LIMITATIONS), len(M.ORIGIN_LIMITATIONS), "utf8", min_items=1), "originCount": UINT,
             "evidence": obj({"testTargets": arr(ref("CargoTargetRefV1"), 65536, {"by": ["unitId"]})})}),
        obj({"universe": universe, "interpretation": interp, "source": const("recognized-test-globs"), "completeness": const("partial"),
             "limitations": arr(enum(M.ORIGIN_LIMITATIONS), len(M.ORIGIN_LIMITATIONS), "utf8", min_items=1), "originCount": UINT,
             "evidence": obj({"unitOrdinal": UINT, "rootPath": {"$ref": N + "InternalUnitRootV1"}, "markerPath": {"type": "string", "minLength": 1, "maxLength": 4096},
                              "recognitionId": SHA256_TEXT,
                              "recognizers": arr(obj({"recognizerId": const("vitest-jest"), "testGlobs": {"$ref": N + "FrameworkRecognitionResultV1/properties/effects/properties/testGlobs"},
                                                      "unresolvedChoices": {"$ref": N + "FrameworkRecognitionResultV1/properties/unresolvedChoices"},
                                                      "evidence": {"$ref": N + "FrameworkRecognitionResultV1/properties/evidence"}}), 32, "sequence", min_items=1)})}),
    ], "description": "Exact static test origin identity of one program universe. No origin set is ever complete: recognizer globs are defaults, Rust in-target tests are not target facts, and imported TestPayloadV1 execution observations never identify origins."}
    reached = arr(universe, 100000, "utf8")
    test_reach = {"oneOf": [
        obj({"subjectId": subject, "state": const("unknown"), "cause": enum(["calls-evidence-unavailable", "subject-descriptor-not-retained"])}),
        obj({"subjectId": subject, "state": const("unknown"), "cause": const("no-test-origin-identity"), "reach": ref("ReportReachContextV1"), "reachedUniverses": reached}),
        obj({"subjectId": subject, "state": const("is-test-origin"), "attributionPath": {"$ref": C3 + "LogicalPath"}, "originEvidence": ref("TestOriginEvidenceV1")}),
        obj({"subjectId": subject, "state": const("static-path-from-test-origin"), "reach": ref("ReportReachContextV1"),
             "origin": obj({"endpoint": {"$ref": GQ + "GraphEndpoint"}, "attributionPath": {"$ref": C3 + "LogicalPath"}, "originEvidence": ref("TestOriginEvidenceV1")}),
             "witness": ref("ReportGraphExchangeV1"), "interpretation": const("static-calls-path-not-executed-coverage")}),
        obj({"subjectId": subject, "state": const("not-found-incomplete"), "reach": ref("ReportReachContextV1"), "reachedUniverses": reached,
             "blockers": arr(enum(M.TEST_BLOCKERS), len(M.TEST_BLOCKERS), "utf8", min_items=1),
             "interpretation": const("no-static-path-from-identified-test-origins-not-untested")}),
    ], "description": "R07 test reachability. There is deliberately no absence-style state: no retained evidence establishes a complete test origin set."}
    symbol_panel = obj({
        "policy": const(M.SYMBOL_EVIDENCE_POLICY), "runId": {"$ref": C3 + "RunId"}, "metricCatalog": const(M.METRIC_IDS),
        "metrics": arr(ref("SymbolMetricV1"), 320, {"by": ["subjectId", "metricId"]}), "metricsProjection": ref("ItemProjectionV1"),
        "entryRecognition": ref("EntryRecognitionStateV1"),
        "traces": arr(ref("EntryTraceV1"), M.MAX_TRACES, {"by": ["subjectId"]}), "tracesProjection": ref("ItemProjectionV1"),
        "testOrigins": arr(ref("TestOriginSetV1"), M.MAX_ORIGIN_SETS, {"by": ["universe"]}), "testOriginsProjection": ref("ItemProjectionV1"),
        "testReachability": arr(ref("TestReachabilityV1"), M.MAX_TEST_REACHABILITY, {"by": ["subjectId"]}), "testReachabilityProjection": ref("ItemProjectionV1"),
        "provenance": const(M.SYMBOL_EVIDENCE_PROVENANCE),
    })
    return {
        "ReportGraphExchangeV1": exchange, "ReportReachContextV1": reach, "WorkspaceUnitRefV1": workspace_unit, "CargoTargetRefV1": cargo_target,
        "CouplingOwnerV1": owners, "CouplingCellV1": cell, "CouplingDrilldownRowV1": drill, "CouplingPanelV1": coupling, "CouplingPanelStateV1": present_state("CouplingPanelV1"),
        "SymbolMetricV1": metric, "RecognizerSummaryV1": recognizer, "EntryRecognitionUnitV1": recognition_unit, "CargoEntryTargetV1": cargo_entry_target,
        "CargoTargetEntriesV1": cargo_entries, "EntryRecognitionStateV1": recognition_state, "EntryProvenanceV1": provenance, "EntryTraceV1": trace,
        "TestOriginEvidenceV1": origin_evidence, "TestOriginSetV1": origin_set, "TestReachabilityV1": test_reach,
        "SymbolEvidencePanelV1": symbol_panel, "SymbolEvidencePanelStateV1": present_state("SymbolEvidencePanelV1"),
    }


def pointer_token(key):
    return key.replace("~", "~0").replace("/", "~1")


def report_patch(parent_raw, defs):
    """Semantic, composable operations. Preconditions are checked on the CURRENT array at application time, never against a whole-array snapshot, so
    another obligation's operations on the same shared selectors can run before or after these. The pinned-parent result is recorded separately."""
    parent = json.loads(parent_raw)
    ops = [{"op": "remove-members", "path": "/$defs/FeatureId/enum", "members": REMOVED_FEATURES, "precondition": "each-member-present-exactly-once"}]
    for index, branch in enumerate(parent["allOf"]):
        states = branch.get("then", {}).get("properties", {}).get("featureStates", {}).get("const")
        if states is not None and any(s["featureId"] in REMOVED_FEATURES for s in states):
            ops.append({"op": "remove-members", "path": "/allOf/%d/then/properties/featureStates/const" % index, "key": "featureId",
                        "members": [f for f in REMOVED_FEATURES if f in {s["featureId"] for s in states}], "precondition": "each-member-present-exactly-once",
                        "selectorGuard": {"path": "/allOf/%d/if/properties/command/const" % index, "equals": branch["if"]["properties"]["command"]["const"]}})
    ops.append({"op": "insert-members-after", "path": "/$defs/BudgetProfileV1/properties/projectionPriority/const", "anchor": "history",
                "members": ["symbolEvidence", "coupling"], "precondition": "anchor-present-once-and-members-absent"})
    ops += [{"op": "add", "path": "/$defs/PanelsV1/properties/coupling", "value": {"$ref": "#/$defs/CouplingPanelStateV1"}, "precondition": "absent"},
            {"op": "add", "path": "/$defs/PanelsV1/properties/symbolEvidence", "value": {"$ref": "#/$defs/SymbolEvidencePanelStateV1"}, "precondition": "absent"}]
    ops += [{"op": "add", "path": "/$defs/" + pointer_token(name), "value": value, "precondition": "absent"} for name, value in sorted(defs.items())]
    return {
        "schemaVersion": 2,
        "standing": "author-02 proposed successor of the unaccepted parent07 report-projection:1 candidate schema; semantic composable operations; parents never edited",
        "parent": {"path": PARENT07 + "/report-projection.schema.json", "sha256": sha(parent_raw), "bytes": len(parent_raw), "$id": parent["$id"],
                   "subjectManifestSha256": PARENT07_MANIFEST_SHA256},
        "operationLaw": {
            "remove-members": "At application time every listed member (or row whose `key` equals it) is present exactly once in the current array; each is removed and nothing else changes. `selectorGuard` must still hold. Removals by different obligations over disjoint members commute.",
            "insert-members-after": "The anchor is present exactly once and no member is present; members are inserted immediately after the anchor in the listed order.",
            "add": "The target member is absent; it is created.",
            "failure": "Any unmet precondition refuses the whole patch (no partial application).",
        },
        "schemaIdDecision": "The $id stays report-projection:1 because no report-projection major was accepted. If one is accepted first, the same operations apply under :2 (RP-EV-INT-SCHEMA).",
        "panelPrerequisites": "symbolEvidence subjects are exactly the graph panel subjectResolution (J-SE-SUBJECTS); without a present graph panel it is unavailable/prerequisite-panel-not-present (J-SE-PREREQUISITE). Both successor panels come after history in projectionPriority; a successor panel omitted for budget forces the next omitted (J-BUDGET-ORDER).",
        "ops": ops,
    }


def recognition_parameter_schema(native):
    defs = native["$defs"]
    copies = {name: copy.deepcopy(defs[name]) for name in ("FrameworkRecognitionV1", "FrameworkRecognitionResultV1", "EntryPointRecognitionV1", "InternalUnitRootV1")}
    return {
        "$schema": SCHEMA,
        "$id": PARAMETER_ID,
        "title": "FrameworkRecognitionPlanV1 - Plan-bound per-unit framework recognition and explicit entry points (proposed OPTIONAL parameter)",
        "description": "Closed Draft 2020-12 analysis-spec PARAMETER payload, the same registry class as EnumerationPlanV1. Identity is raw SHA-256 of C(this record). The registry row is OPTIONAL: every retained predecessor evaluator3 Run (no such parameter) stays admissible and reads as not-plan-bound; a NEW Plan requesting a compiler language mode must select exactly one (pre-Plan duty NEW_PLAN_RECOGNITION_PARAMETER_REQUIRED). Records copied from native-evidence.schemas.v2 are drift-checked; no $ref leaves this document. MUST NOT contain planId or analysisSpecDigest.",
        "type": "object", "additionalProperties": False,
        "required": ["schemaVersion", "snapshotId", "membershipDigest", "explicitEntryPoints", "units"],
        "properties": {
            "schemaVersion": {"const": 1},
            "snapshotId": {"type": "string", "pattern": "^snapshot2:[0-9a-f]{64}(?![\\s\\S])"},
            "membershipDigest": {"type": "string", "pattern": "^[0-9a-f]{64}(?![\\s\\S])",
                                 "x-opensip-digest": {"representation": "canonical-record", "retention": "preimage", "authority": "native",
                                                      "record": {"document": "native/native-evidence.schemas.v2.json", "selector": "#/$defs/UnitMembershipV1"}}},
            "explicitEntryPoints": {"type": "array", "maxItems": 65536, "uniqueItems": True, "items": {"$ref": "#/$defs/LogicalPath"}, "x-opensip-order": "canonical-set"},
            "units": {"type": "array", "maxItems": 4096, "uniqueItems": True, "items": {"$ref": "#/$defs/UnitRecognitionV1"}, "x-opensip-order": "sequence"},
        },
        "x-opensip-parameter-registry-extension": {"standing": "PROPOSED optional row (owner/identity-parameter-registry-patch.v2.json)", "payloadClass": "parameter",
                                                   "document": "foundation/framework-recognition-plan.schema.v1.json", "selector": "#", "atMostOnePerSpec": True},
        "x-opensip-path-law": {"standing": "PROPOSED native section 8 FR-6/FR-8 (owner/native-recognition-successor.v1.json)",
                               "evidenceAndEntryPaths": "repository-relative snapshot inventory paths", "testGlobs": "unit-root-relative GlobPattern text under glob-pattern-contract.v1"},
        "$defs": dict(copies, **{
            "LogicalPath": {"type": "string", "minLength": 1, "maxLength": 4096, "pattern": "^[^/\\\\\\u0000]{1,255}(/[^/\\\\\\u0000]{1,255})*(?![\\s\\S])",
                            "not": {"pattern": "(^|/)\\.\\.?(/|$)"}},
            "UnitRecognitionV1": {"type": "object", "additionalProperties": False, "required": ["unitOrdinal", "rootPath", "markerPath", "recognitionId", "recognition"],
                                  "properties": {
                                      "unitOrdinal": {"type": "integer", "minimum": 0, "maximum": 18446744073709551615},
                                      "rootPath": {"$ref": "#/$defs/InternalUnitRootV1"},
                                      "markerPath": {"type": "string", "maxLength": 4096},
                                      "recognitionId": {"type": "string", "pattern": "^sha256:[0-9a-f]{64}(?![\\s\\S])",
                                                        "x-opensip-digest": {"representation": "h-identity", "domain": "native.framework-recognition.v1", "form": "sha256-text",
                                                                             "retention": "derived", "authority": "native"}},
                                      "recognition": {"$ref": "#/$defs/FrameworkRecognitionV1"}}},
        }),
    }


def identity_patch(identity_raw, model_raw, bridge):
    identity = json.loads(identity_raw)
    rows = identity["x-opensip-payload-registry"]["classes"]["parameter"]["rows"]
    assert bridge.PARAMETER_DOCUMENT not in rows
    transform = bridge.OWNER_TRANSFORMS[0]
    assert model_raw.decode("utf-8").count(transform["old"]) == 1
    return {
        "schemaVersion": 2,
        "standing": "author-02 proposed identity owner successor; parent bytes never edited; executed in check.py through identity_bridge against real retained evaluator3 Runs",
        "parents": {"identitySchemas": {"path": "docs/coop/design-corrections/foundation/identity-schemas.v3.json", "sha256": sha(identity_raw), "bytes": len(identity_raw)},
                    "identityModel": {"path": "docs/coop/design-corrections/foundation/identity-model.v3.py", "sha256": sha(model_raw), "bytes": len(model_raw)}},
        "ops": [{"op": "add", "path": "/x-opensip-payload-registry/classes/parameter/rows/" + pointer_token(bridge.PARAMETER_DOCUMENT), "precondition": "absent",
                 "value": bridge.REGISTRY_ROW}],
        "sourceTransforms": bridge.OWNER_TRANSFORMS,
        "newPlanDuty": {"boundary": "pre-Plan analysis-spec admission for a NEW evaluator3 Plan, after identity-model.v3 admit_parameter_selection",
                        "law": "reference_model.admit_new_plan_recognition_parameter: when any requestedCapabilities languageMode maps (identity x-opensip-digest-domains/languageModes/map) to typescript or rust, exactly one parameter resolves to this row; otherwise NEW_PLAN_RECOGNITION_PARAMETER_REQUIRED",
                        "notAtRetainedClosure": "close_run and open_run_closure never apply this duty, so historical Runs keep their admission",
                        "observation": "native_evidence_model.v2 admit_analysis_spec calls the historical foundation/identity-model.py (identity-schemas.v2 registry); this candidate binds the duty to identity-model.v3 and records the discrepancy for the native/identity owners without changing it"},
        "identityEffects": {
            "historicalRuns": "admitted unchanged by the successor model (executed: same run3 identity closes under the pinned and the successor model) and read as not-plan-bound from their own analysis-spec parameters",
            "newPlans": "a new Plan selecting the parameter has a different analysisSpecDigest, PlanId and RunId; the pinned predecessor model refuses it (PAYLOAD_PARAMETER_UNREGISTERED), so no predecessor admits evidence it cannot validate",
            "closedVocabularies": "the payload registry parameter rows gain one row and identity-model.v3's closed registered-record document list gains one document (T1); requiredForEvaluatorMajors is NOT used",
            "unchanged": "universe, context, fact2, coverage2, subject3 identities and every existing parameter row",
        },
    }


def native_successor():
    return {
        "schemaVersion": 1,
        "standing": "author-02 proposed native section 8 successor (S1); prose plus executable reference functions in reference_model.py; native bytes unchanged",
        "selector": "docs/v2/contracts/product-v1/native-evidence.md section 8, after FR-5",
        "clauses": [
            {"id": "FR-6", "text": "Evidence and entry paths of FrameworkRecognitionResultV1 are repository-relative snapshot inventory paths; the unit-root-relative paths the reference recognizer emits are joined with the unit rootPath. testGlobs stay unit-root-relative GlobPattern text.", "function": "successor_recognition"},
            {"id": "FR-7", "text": "One FrameworkRecognitionV1 per WorkspaceUnitV2 with languageFamily rust or tsjs is committed in FrameworkRecognitionPlanV1. Explicit entryPoints replace all other entry points as the effective set. For a Rust universe the effective entries are additionally the crate roots of every SELECTED bin and lib compilation target: the unique crateRootPaths member that the target owns in SourceUnitOwnershipV1; a target with zero or several owned roots, or partial ownership enumeration, is exact missing coverage and the state is partial. A cargo-workspace unit never reports all from its root package alone.", "function": "cargo_target_entries, effective_entries, scope_state"},
            {"id": "FR-8", "text": "When package.json carries a jest object that sets testMatch, testRegex, roots, projects or testPathIgnorePatterns, vitest-jest reports unresolvedChoices test-selection-configured. Recognized testGlobs are defaults and never establish a complete test population.", "function": "successor_recognition, derive_test_origins"},
        ],
        "executedAgainstPinnedModel": "check.py runs native_evidence_model.v2 discover_units, assign_membership and recognize_frameworks on the fixture worlds and applies these functions to their outputs",
    }


def successor_register(M, bridge, patch, ipatch, parameter_raw):
    return {
        "schemaVersion": 2,
        "standing": "author-02 report evidence design successor register for actual separate review and root acceptance; not approval. RP-DO-03/05/09/10 only.",
        "parents": {"reportParent07": {"subject": PARENT07, "manifestSha256": PARENT07_MANIFEST_SHA256},
                    "priorCandidate": {"subject": SUBJECT01, "manifestSha256": SUBJECT01_MANIFEST_SHA256, "standing": "historical, superseded by this candidate"},
                    "review": {"path": REVIEW01, "decision": "changes-required"}},
        "findingDispositions": [
            {"id": "F1", "severity": "high", "disposition": "corrected", "summary": "Registry row is optional (no requiredForEvaluatorMajors); identity-model.v3 registered-record list gains the document (T1); a separate pre-Plan duty requires it for new compiler-mode Plans. check.py closes real retained evaluator3 Runs through the pinned and successor identity models: predecessor Run admitted by both and custody not-plan-bound from its own parameters; new-Plan Run admitted by the successor and refused by the predecessor; lost parameter bytes refuse closure; the duty refuses a compiler-mode spec without the parameter.", "regression": ["identityBridge.*"]},
            {"id": "F2", "severity": "high", "disposition": "corrected", "summary": "Origin sets are derived for every universe among the reach rows and embedded; hits match per universe; reached universes without origin identity are a blocker. The reviewer C1 world is a permanent fixture (static path found across universes).", "regression": ["variants.cross-universe-test-caller"]},
            {"id": "F3", "severity": "high", "disposition": "corrected", "summary": "No TS/JS or Rust origin set can be complete (recognizer-globs-not-test-population always); the no-static-path-within-bound state is removed; configured jest selection is read as data (FR-8, test-selection-configured). The reviewer C2 world is a fixture: not-found-incomplete with test-origin-set-partial and test-selection-configured.", "regression": ["variants.jest-configured-selection"]},
            {"id": "F4", "severity": "high", "disposition": "corrected", "summary": "Rust entries are the crate roots of every selected bin/lib target from retained SourceUnitOwnershipV1 x crateRootPaths (FR-7), with missing coverage; the pinned native recognizer's root-only result is executed and kept as evidence. The member binary crates/app/src/main.rs is now an entry and the reviewer C3 trace is path-found; an unresolved member root gives partial with the entry-recognition-not-all blocker.", "regression": ["positive.mixedTraces", "variants.cargo-member-root-unresolved", "nativeModel"]},
            {"id": "F5", "severity": "medium", "disposition": "corrected", "summary": "remove-members / insert-members-after / add with application-time preconditions; check.py applies this patch and a real second obligation patch sequentially in both orders through one applier, requires identical results, and refuses unmet preconditions.", "regression": ["patchComposition"]},
            {"id": "F6", "severity": "medium", "disposition": "corrected", "summary": "Cells, target buckets and drilldown are byte-bounded prefixes in deterministic priority order with ItemProjectionV1 and an exact owner closure; omissions add blockers and make blank cells not-determined; both panels are placed after history under the report-wide remaining exploration budget with J-BUDGET-ORDER. The dense 120-package workspace is a fixture and stays within its budget.", "regression": ["denseCoupling", "integration"]},
            {"id": "F7", "severity": "medium", "disposition": "corrected", "summary": "New fixtures kill M4 (cross-universe caller), M7 (test-bound whole-view lower bound) and M8 (exact zero under a limitation); featureMap refs are fully resolved against the patched schema and a bogus ref is refused. A mutation run over the candidate is recorded beside it.", "regression": ["variants.whole-view-test-bound", "variants.zero-under-limitation", "register.featureMap"]},
            {"id": "F8", "severity": "low", "disposition": "corrected", "summary": "Cells expose facts (observations), programEdges and universe-independent sourceDependencies with a const countUnits disclosure; the reviewer C6 duplicate is a fixture (2 facts, 1 source dependency).", "regression": ["variants.cross-program-duplicate"]},
            {"id": "F9", "severity": "low", "disposition": "corrected", "summary": "Importer owners key on the imports fact anchor paths (native section 2.1: rows whose path equals the enclosing fact's anchor path); disagreeing anchor owners and missing anchors are explicit buckets; importer symbol inventory paths outside the anchors are counted, never used for ownership. A fixture whose symbol inventory path differs from the anchor path attributes by anchor.", "regression": ["variants.anchor-vs-symbol-path"]},
        ],
        "ownerSuccessors": [
            {"id": "S1", "owner": "native", "record": "owner/native-recognition-successor.v1.json"},
            {"id": "S2", "owner": "foundation/identity", "record": "owner/identity-parameter-registry-patch.v2.json", "document": bridge.PARAMETER_DOCUMENT,
             "documentSha256": sha(parameter_raw), "candidate": "owner/framework-recognition-plan.schema.v1.json"},
            {"id": "S3", "owner": "query", "selector": "query-projection-contract.v3.md new section 8a",
             "text": "Internal whole-view projection for host reporting: section 8 steps 1-4 and 7 without endpoint admission; every projectable fact of the selected views in fact2 order with reconciled target occupancy and the retained fact anchor paths; produced-item law as section 5 (host test bounds may only lower caps; a produced prefix is lower-bound with unexamined-work-bound); no cursor, no public operation."},
            {"id": "S4", "owner": "report", "record": "owner/report-projection-successor-patch.v2.json", "opsCount": len(patch["ops"])},
            {"id": "S5-S7", "owner": "workflows import; enumeration/inventory; native SourceUnitOwnershipV1", "change": "none"},
        ],
        "featureMapSuccessor": {
            "R07": [{"kind": "report", "ref": "/$defs/GraphPanelV1/properties/subjectIndex"}, {"kind": "report", "ref": "/$defs/SubjectResolutionV1"},
                    {"kind": "report", "ref": "/$defs/SymbolMetricV1"}, {"kind": "report", "ref": "/$defs/TestOriginSetV1"}, {"kind": "report", "ref": "/$defs/TestReachabilityV1"}],
            "R08": [{"kind": "report", "ref": "/$defs/GraphSlotV1/properties/purpose"}, {"kind": "report", "ref": "/$defs/CouplingPanelV1"}],
            "R12": [{"kind": "report", "ref": "/$defs/GraphSlotV1/properties/anchorSubjectIds"}, {"kind": "report", "ref": "/$defs/EntryRecognitionStateV1"},
                    {"kind": "report", "ref": "/$defs/CargoTargetEntriesV1"}, {"kind": "report", "ref": "/$defs/EntryTraceV1"}],
        },
        "integrationDuties": [
            {"id": "RP-EV-INT-SCHEMA", "owner": "report", "duty": "apply the semantic patch to the accepted report-projection bytes; drop the four featureStates rows and readiness blockers; swap featureMap rows"},
            {"id": "RP-EV-INT-BUDGET", "owner": "report", "duty": "projectionPriority gains symbolEvidence then coupling after history; project_exploration places them with place_successor_panels semantics; budgetProfile documents carry the successor priority"},
            {"id": "RP-EV-INT-STATIC", "owner": "report", "duty": "static parity names the host-asserted items of both provenance consts and the coupling omission counts"},
            {"id": "RP-EV-INT-GENERATOR", "owner": "generation registry", "duty": "register successor schema and parameter document sources; regenerate bindings (not run)"},
            {"id": "RP-EV-INT-COVERAGE", "owner": "implementation coverage", "duty": "close the four review issues only after S1-S4 review; add producer/projection delivery rows"},
            {"id": "RP-EV-INT-IDENTITY", "owner": "identity", "duty": "apply the optional row and T1; add the pre-Plan duty to the new-Plan boundary; reconcile native admit_analysis_spec's use of the v2 registry (observation, not changed here)"},
            {"id": "RP-EV-INT-RETENTION", "owner": "identity/lifecycle", "duty": "parameter custody from the Run's own parameters and availability generation (not-plan-bound / unavailable / plan-bound)"},
            {"id": "RP-EV-INT-BROWSER", "owner": "report browser lane", "duty": "render unknown, partial, omitted and blocker states and interpretations (not executed)"},
            {"id": "RP-EV-INT-MEASURE", "owner": "measurement", "duty": "whole-view projection, bounded coupling fitting and reach walks (not measured)"},
        ],
        "remainingBlockers": [],
        "remainingDependencies": ["S1-S4 owner acceptance", "report-projection successor acceptance and integration into parent report bytes"],
    }


def build(arch, M, bridge):
    native_raw = (arch / "docs/coop/design-corrections/native/native-evidence.schemas.v2.json").read_bytes()
    identity_raw = (arch / "docs/coop/design-corrections/foundation/identity-schemas.v3.json").read_bytes()
    model_raw = (arch / "docs/coop/design-corrections/foundation/identity-model.v3.py").read_bytes()
    report_raw = open(PARENT07 + "/report-projection.schema.json", "rb").read()
    parameter = recognition_parameter_schema(json.loads(native_raw))
    parameter_raw = dump(parameter)
    patch = report_patch(report_raw, report_defs(M))
    ipatch = identity_patch(identity_raw, model_raw, bridge)
    return {
        "owner/framework-recognition-plan.schema.v1.json": parameter,
        "owner/report-projection-successor-patch.v2.json": patch,
        "owner/identity-parameter-registry-patch.v2.json": ipatch,
        "owner/native-recognition-successor.v1.json": native_successor(),
        "owner/evidence-design-successor.v2.json": successor_register(M, bridge, patch, ipatch, parameter_raw),
    }
