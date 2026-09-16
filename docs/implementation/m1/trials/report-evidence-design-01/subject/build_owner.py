"""Owner record builder (author-01). Deterministic: every owner/ file is a pure function of pinned parents and reference_model constants.

build(arch, subject05, M) -> {relative name: JSON value}; dump(value) -> exact bytes.
"""
import copy
import hashlib
import json

GQ = "urn:opensip:product-v1:workflows:evaluator3:graph-query:3#/$defs/"
C3 = "urn:opensip:product-v1:workflows:evaluator3:common:3#/$defs/"
N = "urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/"
SCHEMA = "https://json-schema.org/draft/2020-12/schema"
SUBJECT05 = "/tmp/opensip-implementation/m1-report-projection-subject-05"
SUBJECT05_MANIFEST_SHA256 = "a9f6c22a9b2af9487fc9683fdef76c58e391f5a6f64e2f8b09bfa75d288de2a4"
PARAMETER_DOCUMENT = "foundation/framework-recognition-plan.schema.v1.json"
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
    owner_key = {"type": "string", "pattern": "^owner1:[0-9a-f]{64}(?![\\s\\S])",
                 "description": "owner1: + raw SHA-256 of C(key record): first-party-package {keyKind, path=packageManifestPath}; workspace-unit {keyKind, path=workspaceUnit.markerPath}; external-package {keyKind, universe, path, name}. Recomputed by admission."}
    exchange = obj({"request": {"$ref": GQ + "GraphQueryRequestV1"}, "response": {"$ref": GQ + "GraphQueryResponseV1"}})
    reach = obj({"request": {"$ref": GQ + "GraphQueryRequestV1"}, "responseContext": {"$ref": GQ + "GraphOperationResponseContext"}},
                description="The first page context of the owner graph.reach operation; rows are walked by the host and are not embedded.")
    workspace_unit = obj({"unitOrdinal": UINT, "rootPath": {"$ref": N + "InternalUnitRootV1"}, "markerPath": {"type": "string", "minLength": 1, "maxLength": 4096},
                          "unitKind": enum(["js-program", "ts-program"]), "languageFamily": const("tsjs")},
                         description="Retained WorkspaceUnitV2 projection of a TS/JS program unit (native section 1.4 U-1, U-3).")
    cargo_target = obj({"unitId": dict(SHA256_TEXT, **{"x-opensip-digest": {"representation": "h-identity", "domain": "native.compilation-unit.v1", "form": "sha256-text",
                                                                              "retention": "derived", "authority": "native"}}),
                        "markerPath": {"$ref": C3 + "LogicalPath"}, "targetKind": {"$ref": N + "UnitIdentityV1/properties/targetKind"},
                        "targetName": {"$ref": N + "UnitIdentityV1/properties/targetName"}},
                       description="SourceUnitOwnershipV1.units row projection; unitId is recomputed from its published UnitIdentityV1 preimage.")
    owners = {"oneOf": [
        obj({"ownerKey": owner_key, "keyKind": const("first-party-package"), "packageManifestPath": {"$ref": C3 + "LogicalPath"},
             "packageName": {"type": "string", "minLength": 1, "maxLength": 4096}, "cargoTargets": arr(ref("CargoTargetRefV1"), 65536, {"by": ["unitId"]}),
             "workspaceUnit": {"oneOf": [ref("WorkspaceUnitRefV1"), {"type": "null"}]}},
            description="First-party package: an inventoried manifest (SubjectInventoryV1 kind=package row). Rust owners come from selected SourceUnitOwnershipV1 targets whose markerPath is this manifest; TS/JS owners from the UnitMembershipV1 unit whose root holds this package.json."),
        obj({"ownerKey": owner_key, "keyKind": const("workspace-unit"), "workspaceUnit": ref("WorkspaceUnitRefV1")},
            description="TS/JS program unit whose root holds no inventoried package.json."),
        obj({"ownerKey": owner_key, "keyKind": const("external-package"), "packageManifestPath": {"$ref": C3 + "LogicalPath"},
             "packageName": {"type": "string", "minLength": 1, "maxLength": 4096}, "universe": {"$ref": C3 + "Sha256Hex"}},
            description="Target-side external package endpoint (reconciled occupancy external); never an importer."),
    ]}
    coupling = obj({
        "policy": const(M.COUPLING_POLICY), "runId": {"$ref": C3 + "RunId"}, "relation": const("imports"), "minResolution": const("resolved-target"),
        "projection": obj({"countBasis": {"$ref": GQ + "CountBasis"}, "factViewDigests": arr({"$ref": GQ + "ViewDigest"}, 100000, "canonical-set"),
                           "coverageIds": arr({"$ref": C3 + "CoverageId"}, 100000, "canonical-set"), "limitationKinds": arr(limitation, 12, "utf8"),
                           "deficiencyCitationCount": UINT}),
        "owners": arr(ref("CouplingOwnerV1"), 65536, {"by": ["ownerKey"]}),
        "cells": arr(ref("CouplingCellV1"), 1000000, {"by": ["fromOwnerKey", "toOwnerKey"]}),
        "importerBuckets": arr(obj({"cause": enum(M.IMPORTER_CAUSES), "facts": UINT}), len(M.IMPORTER_CAUSES), {"by": ["cause"]}),
        "targetBuckets": arr(obj({"fromOwnerKey": owner_key, "cause": enum(M.TARGET_CAUSES), "facts": UINT}), 1000000, {"by": ["fromOwnerKey", "cause"]}),
        "totals": obj({"distinctFacts": UINT, "attributedFacts": UINT, "importerUnattributedFacts": UINT, "targetUnattributedFacts": UINT}),
        "absence": obj({"blankCellMeans": const("no-projected-fact"), "absenceSupported": {"type": "boolean"}, "blockers": arr(enum(M.COUPLING_BLOCKERS), 4, "utf8")},
                       description="A blank cell only means no projected fact. absenceSupported is true only with no blockers; even then it is scoped to the admitted imports@resolved-target views of this Run."),
        "drilldown": arr(ref("CouplingDrilldownRowV1"), M.MAX_DRILLDOWN, {"by": ["fromOwnerKey", "toOwnerKey", "factId"]}),
        "drilldownProjection": ref("ItemProjectionV1"),
        "provenance": const(M.COUPLING_PROVENANCE),
    }, description="R08 package coupling: directional (importer owner -> target owner) counts over the whole admitted imports@resolved-target view, with explicit unattributed and external buckets.")
    cell = obj({"fromOwnerKey": owner_key, "toOwnerKey": owner_key, "facts": dict(UINT), "edges": UINT, "importerSymbols": UINT, "sharedImporterFacts": UINT,
                "sharedTargetFacts": UINT, "internal": {"type": "boolean"}, "importerUniverses": arr({"$ref": C3 + "Sha256Hex"}, 4096, "utf8", min_items=1)},
               description="facts: distinct fact2 (provenance duplicates stay distinct); edges: distinct (importer endpoint, target endpoint); shared*: facts whose importer or target has several owners and is counted in each owner's cell.")
    drill = obj({"fromOwnerKey": owner_key, "toOwnerKey": owner_key, "factId": {"$ref": GQ + "FactId"}, "importer": {"$ref": GQ + "GraphEndpoint"},
                 "target": {"$ref": GQ + "GraphEndpoint"}, "importerPath": {"$ref": C3 + "LogicalPath"},
                 "importerTestOrigin": enum(["no-test-origin-identity", "not-identified-as-test-origin", "test-origin"])},
                description="Includes test occurrences by default; importerTestOrigin feeds the visible filter state (R07/R08).")
    metric_common = {"subjectId": {"$ref": C3 + "SubjectId"}, "metricId": enum(M.METRIC_IDS)}
    metric = {"oneOf": [
        obj(dict(metric_common, interpretation=const("static-projected-count"), request={"$ref": GQ + "GraphQueryRequestV1"}, response={"$ref": GQ + "GraphQueryResponseV1"},
                 countState=enum(["exact", "lower-bound"]), value=UINT, limitationKinds=arr(limitation, 12, "utf8"), zeroSupportsAbsence={"type": "boolean"})),
        obj(dict(metric_common, interpretation=const("static-projected-count"), request={"$ref": GQ + "GraphQueryRequestV1"}, response={"$ref": GQ + "GraphQueryResponseV1"},
                 countState=const("unknown"), cause=const("native-evidence-unavailable"))),
        obj(dict(metric_common, countState=const("unknown"), cause=const("subject-descriptor-not-retained"))),
    ], "description": "R07 metric: the owner totalItems of one catalog graph operation over the exact subject endpoint, universe and admitted fact-view. Not runtime hotness; a zero supports absence only when exact and unlimited."}
    recognizer = obj({"recognizerId": {"$ref": N + "FrameworkRecognitionResultV1/properties/recognizerId"}, "recognizerVersion": const(1),
                      "assurance": {"$ref": N + "FrameworkRecognitionResultV1/properties/assurance"}, "evidence": {"$ref": N + "FrameworkRecognitionResultV1/properties/evidence"},
                      "unresolvedChoices": {"$ref": N + "FrameworkRecognitionResultV1/properties/unresolvedChoices"},
                      "entryPointCount": {"type": "integer", "minimum": 0, "maximum": 65536},
                      "testGlobs": {"$ref": N + "FrameworkRecognitionResultV1/properties/effects/properties/testGlobs"}})
    recognition_unit = obj({"unitOrdinal": UINT, "rootPath": {"$ref": N + "InternalUnitRootV1"}, "markerPath": {"type": "string", "minLength": 1, "maxLength": 4096},
                            "recognitionId": SHA256_TEXT, "entryPoints": {"$ref": N + "EntryPointRecognitionV1"}, "effectiveSource": enum(["explicit", "none", "recognized"]),
                            "effectiveEntryPointCount": UINT, "recognizers": arr(ref("RecognizerSummaryV1"), 32, "sequence")})
    recognition_state = {"oneOf": [
        obj({"state": const("not-plan-bound")}, description="The Run's Plan carries no FrameworkRecognitionPlanV1 parameter (historical profile): no entry-point evidence is inferred."),
        obj({"state": const("unavailable"), "parameterDigest": HEX, "availability": enum(["corrupt", "expired", "partial", "purged", "unavailable"])},
            description="Plan-bound but the parameter bytes are not available at the observed availability generation (partial: the parameter ref is missing)."),
        obj({"state": const("plan-bound"), "parameterDigest": HEX, "availability": enum(["partial", "retained"]), "explicitEntryPointCount": UINT,
             "units": arr(ref("EntryRecognitionUnitV1"), 4096, "sequence")}),
    ]}
    provenance = {"oneOf": [obj({"source": const("explicit")}),
                            obj({"source": const("recognized"), "unitOrdinal": UINT, "recognizerId": {"$ref": N + "FrameworkRecognitionResultV1/properties/recognizerId"},
                                 "recognizerVersion": const(1), "assurance": {"$ref": N + "FrameworkRecognitionResultV1/properties/assurance"},
                                 "evidence": {"$ref": N + "FrameworkRecognitionResultV1/properties/evidence"},
                                 "unresolvedChoices": {"$ref": N + "FrameworkRecognitionResultV1/properties/unresolvedChoices"}})]}
    scope_unit = {"oneOf": [UINT, {"type": "null"}]}
    trace = {"oneOf": [
        obj({"subjectId": {"$ref": C3 + "SubjectId"}, "state": const("unknown"), "cause": enum(["recognition-not-plan-bound", "recognition-unavailable", "subject-descriptor-not-retained"])}),
        obj({"subjectId": {"$ref": C3 + "SubjectId"}, "scopeUnitOrdinal": scope_unit, "state": const("unknown"),
             "cause": enum(["origin-page-set-not-embedded", "reachability-evidence-unavailable"]), "originQuery": ref("ReportGraphExchangeV1")}),
        obj({"subjectId": {"$ref": C3 + "SubjectId"}, "scopeUnitOrdinal": scope_unit, "state": const("no-entry-origin"), "originQuery": ref("ReportGraphExchangeV1"),
             "originsExamined": UINT, "originsUnattributed": UINT, "originsOutsideEntrySet": UINT, "blockers": arr(enum(M.TRACE_BLOCKERS), 3, "utf8"),
             "interpretation": const("no-entry-origin-among-projected-reachability-origins-not-dead-code")}),
        obj({"subjectId": {"$ref": C3 + "SubjectId"}, "scopeUnitOrdinal": scope_unit, "state": enum(["path-found", "path-not-within-bound"]),
             "originQuery": ref("ReportGraphExchangeV1"),
             "start": obj({"endpoint": {"$ref": GQ + "GraphEndpoint"}, "viaReachabilityFactId": {"$ref": GQ + "FactId"}, "attributionPath": {"$ref": C3 + "LogicalPath"},
                           "entry": obj({"path": {"$ref": C3 + "LogicalPath"}, "provenance": arr(ref("EntryProvenanceV1"), 33, "sequence", min_items=1)})}),
             "path": ref("ReportGraphExchangeV1")}),
    ], "description": "R12 trace: start is a native reachability origin of the subject whose native-attested path is a retained effective entry point; the bounded calls path is an owner graph.path answer. A missing path is never dead-code proof."}
    origin_evidence = {"oneOf": [
        obj({"kind": const("rust-test-target"), "unitIds": arr(SHA256_TEXT, 65536, "utf8", min_items=1)}),
        obj({"kind": const("recognized-test-glob"), "unitOrdinal": UINT, "recognizerId": const("vitest-jest"), "glob": {"type": "string", "minLength": 1, "maxLength": 256},
             "relativePath": {"$ref": C3 + "LogicalPath"}}),
    ]}
    origin_set = {"oneOf": [
        obj({"universe": {"$ref": C3 + "Sha256Hex"}, "source": const("none"), "completeness": const("none"), "cause": enum(M.ORIGIN_NONE_CAUSES),
             "limitations": arr(enum(M.ORIGIN_LIMITATIONS), 0, "utf8"), "originCount": const(0)}),
        obj({"universe": {"$ref": C3 + "Sha256Hex"}, "source": const("rust-test-targets"), "completeness": const("partial"),
             "limitations": arr(enum(M.ORIGIN_LIMITATIONS), len(M.ORIGIN_LIMITATIONS), "utf8", min_items=1), "originCount": UINT,
             "evidence": obj({"testTargets": arr(ref("CargoTargetRefV1"), 65536, {"by": ["unitId"]})})}),
        obj({"universe": {"$ref": C3 + "Sha256Hex"}, "source": const("recognized-test-globs"), "completeness": enum(["declared", "partial"]),
             "limitations": arr(enum(M.ORIGIN_LIMITATIONS), len(M.ORIGIN_LIMITATIONS), "utf8"), "originCount": UINT,
             "evidence": obj({"unitOrdinal": UINT, "rootPath": {"$ref": N + "InternalUnitRootV1"}, "markerPath": {"type": "string", "minLength": 1, "maxLength": 4096},
                              "recognitionId": SHA256_TEXT,
                              "recognizers": arr(obj({"recognizerId": const("vitest-jest"), "testGlobs": {"$ref": N + "FrameworkRecognitionResultV1/properties/effects/properties/testGlobs"},
                                                      "unresolvedChoices": {"$ref": N + "FrameworkRecognitionResultV1/properties/unresolvedChoices"},
                                                      "evidence": {"$ref": N + "FrameworkRecognitionResultV1/properties/evidence"}}), 32, "sequence", min_items=1)})}),
    ], "description": "Exact test origin identity for one program universe. Imported TestPayloadV1 testId/subjectPath is not an origin source."}
    reach_common = {"subjectId": {"$ref": C3 + "SubjectId"}}
    test_reach = {"oneOf": [
        obj(dict(reach_common, state=const("unknown"), cause=enum(M.TEST_UNKNOWN_CAUSES))),
        obj(dict(reach_common, state=const("is-test-origin"), attributionPath={"$ref": C3 + "LogicalPath"}, originEvidence=ref("TestOriginEvidenceV1"))),
        obj(dict(reach_common, state=const("static-path-from-test-origin"), reach=ref("ReportReachContextV1"),
                 origin=obj({"endpoint": {"$ref": GQ + "GraphEndpoint"}, "attributionPath": {"$ref": C3 + "LogicalPath"}, "originEvidence": ref("TestOriginEvidenceV1")}),
                 witness=ref("ReportGraphExchangeV1"), interpretation=const("static-calls-path-not-executed-coverage"))),
        obj(dict(reach_common, state=const("not-found-incomplete"), reach=ref("ReportReachContextV1"), blockers=arr(enum(M.TEST_BLOCKERS), 3, "utf8", min_items=1))),
        obj(dict(reach_common, state=const("no-static-path-within-bound"), reach=ref("ReportReachContextV1"), maxDepth=const(M.TEST_REACH_MAX_DEPTH),
                 interpretation=const("no-static-calls-path-from-identified-test-origins-within-bound-not-untested"))),
    ], "description": "R07 test reachability: static calls@resolved-callee reach from exact test origins; never executed coverage, runtime hotness or proof of being untested."}
    symbol_panel = obj({
        "policy": const(M.SYMBOL_EVIDENCE_POLICY), "runId": {"$ref": C3 + "RunId"}, "metricCatalog": const(M.METRIC_IDS),
        "metrics": arr(ref("SymbolMetricV1"), 320, {"by": ["subjectId", "metricId"]}), "metricsProjection": ref("ItemProjectionV1"),
        "entryRecognition": ref("EntryRecognitionStateV1"),
        "traces": arr(ref("EntryTraceV1"), M.MAX_TRACES, {"by": ["subjectId"]}), "tracesProjection": ref("ItemProjectionV1"),
        "testOrigins": arr(ref("TestOriginSetV1"), 64, {"by": ["universe"]}),
        "testReachability": arr(ref("TestReachabilityV1"), M.MAX_TEST_REACHABILITY, {"by": ["subjectId"]}), "testReachabilityProjection": ref("ItemProjectionV1"),
        "provenance": const(M.SYMBOL_EVIDENCE_PROVENANCE),
    }, description="symbol-detail evidence for the graph panel's planned subjects (J-SE-SUBJECTS): metrics, entry recognition and traces, test origins and static test reachability.")
    return {
        "ReportGraphExchangeV1": exchange, "ReportReachContextV1": reach, "WorkspaceUnitRefV1": workspace_unit, "CargoTargetRefV1": cargo_target,
        "CouplingOwnerV1": owners, "CouplingCellV1": cell, "CouplingDrilldownRowV1": drill, "CouplingPanelV1": coupling, "CouplingPanelStateV1": present_state("CouplingPanelV1"),
        "SymbolMetricV1": metric, "RecognizerSummaryV1": recognizer, "EntryRecognitionUnitV1": recognition_unit, "EntryRecognitionStateV1": recognition_state,
        "EntryProvenanceV1": provenance, "EntryTraceV1": trace, "TestOriginEvidenceV1": origin_evidence, "TestOriginSetV1": origin_set, "TestReachabilityV1": test_reach,
        "SymbolEvidencePanelV1": symbol_panel, "SymbolEvidencePanelStateV1": present_state("SymbolEvidencePanelV1"),
    }


def pointer_token(key):
    return key.replace("~", "~0").replace("/", "~1")


def report_patch(parent_raw, defs):
    parent = json.loads(parent_raw)
    features = parent["$defs"]["FeatureId"]["enum"]
    ops = [{"op": "remove-rows", "path": "/$defs/FeatureId/enum", "match": REMOVED_FEATURES, "before": features, "after": [f for f in features if f not in REMOVED_FEATURES]}]
    for index, branch in enumerate(parent["allOf"]):
        states = branch.get("then", {}).get("properties", {}).get("featureStates", {}).get("const")
        if states is not None and any(s["featureId"] in REMOVED_FEATURES for s in states):
            ops.append({"op": "remove-rows", "path": "/allOf/%d/then/properties/featureStates/const" % index, "match": REMOVED_FEATURES, "matchKey": "featureId",
                        "command": branch["if"]["properties"]["command"]["const"], "before": states, "after": [s for s in states if s["featureId"] not in REMOVED_FEATURES]})
    ops += [{"op": "add", "path": "/$defs/PanelsV1/properties/coupling", "after": {"$ref": "#/$defs/CouplingPanelStateV1"}},
            {"op": "add", "path": "/$defs/PanelsV1/properties/symbolEvidence", "after": {"$ref": "#/$defs/SymbolEvidencePanelStateV1"}}]
    ops += [{"op": "add", "path": "/$defs/" + pointer_token(name), "after": value} for name, value in sorted(defs.items())]
    return {
        "schemaVersion": 1,
        "standing": "author-01 proposed successor of the unaccepted subject-05 report-projection:1 candidate schema; exact before/after selectors; parents never edited",
        "parent": {"path": SUBJECT05 + "/report-projection.schema.json", "sha256": sha(parent_raw), "bytes": len(parent_raw),
                   "$id": parent["$id"], "subjectManifestSha256": SUBJECT05_MANIFEST_SHA256},
        "schemaIdDecision": "The $id stays urn:opensip:product-v1:workflows:evaluator3:report-projection:1 because no report-projection major was ever accepted or published; the FeatureId closed enum narrows and PanelsV1 gains two optional closed members. If any report-projection:1 bytes are accepted before this successor, the same ops apply under report-projection:2 and every consumer of FeatureId/PanelsV1 must rebind (integration duty RP-EV-INT-SCHEMA).",
        "compositionWithOtherObligations": "FeatureId/enum and the seven per-command featureStates consts (allOf 3-9: default, analyze, fit, audit, candidates, inspect, review-brief) are SHARED selectors that also hold rows of RP-DO-01/02/04/06/07/08/11/12. These ops are therefore remove-rows, not whole-array replaces: each removes exactly its matched members, `before` and `after` are exact for the pinned parent, and two successors' remove-rows over disjoint matches commute (applying both in either order gives the same array). The new PanelsV1 members and $defs names are otherwise disjoint; FeatureStateV1.reason, the other eight FeatureId members, allOf/10 (repair-preview) and every existing $def are unchanged.",
        "panelPrerequisites": "symbolEvidence is present only with a present graph panel (its subjects are the graph panel subjectResolution, J-SE-SUBJECTS); otherwise it is PanelNotPresentV1 unavailable/prerequisite-panel-not-present (J-SE-PREREQUISITE). coupling needs only the Run identity (no-run-identity otherwise).",
        "ops": ops,
    }


def recognition_parameter_schema(native):
    defs = native["$defs"]
    copies = {name: copy.deepcopy(defs[name]) for name in ("FrameworkRecognitionV1", "FrameworkRecognitionResultV1", "EntryPointRecognitionV1", "InternalUnitRootV1")}
    return {
        "$schema": SCHEMA,
        "$id": PARAMETER_ID,
        "title": "FrameworkRecognitionPlanV1 - Plan-bound per-unit framework recognition and explicit entry points (proposed parameter, author-01)",
        "description": "Closed Draft 2020-12 analysis-spec PARAMETER payload, the same registry class as EnumerationPlanV1. Identity is raw SHA-256 of C(this record); it enters PlanId through analysisSpecDigest exactly as native section 8 FR-5 already requires a recognizer change to be Plan-visible. It is not a Run output field and no cache: the preimage is retained under its digest in the Run's required closure and follows the Run's availability generation. Records copied from native-evidence.schemas.v2 are drift-checked byte-for-value; no $ref leaves this document so the payload registry key stays the whole document. MUST NOT contain planId or analysisSpecDigest (parent cycle).",
        "type": "object", "additionalProperties": False,
        "required": ["schemaVersion", "snapshotId", "membershipDigest", "explicitEntryPoints", "units"],
        "properties": {
            "schemaVersion": {"const": 1},
            "snapshotId": {"type": "string", "pattern": "^snapshot2:[0-9a-f]{64}(?![\\s\\S])", "description": "Closure join: equals plan.snapshotId."},
            "membershipDigest": {"type": "string", "pattern": "^[0-9a-f]{64}(?![\\s\\S])",
                                 "x-opensip-digest": {"representation": "canonical-record", "retention": "preimage", "authority": "native",
                                                      "record": {"document": "native/native-evidence.schemas.v2.json", "selector": "#/$defs/UnitMembershipV1"}},
                                 "description": "raw SHA-256 of C(UnitMembershipV1); closure join: equals EnumerationPlanV1.membershipDigest."},
            "explicitEntryPoints": {"type": "array", "maxItems": 65536, "uniqueItems": True, "items": {"$ref": "#/$defs/LogicalPath"}, "x-opensip-order": "canonical-set",
                                    "description": "Exactly the committed semantic-configuration discovery.entryPoints (empty when absent). When non-empty it replaces every recognized effect as the effective entry set (FR-2 'explicit configuration wins'); recognized results stay retained as evidence."},
            "units": {"type": "array", "maxItems": 4096, "uniqueItems": True, "items": {"$ref": "#/$defs/UnitRecognitionV1"}, "x-opensip-order": "sequence",
                      "description": "One row per retained WorkspaceUnitV2 with languageFamily rust or tsjs, strictly ascending unitOrdinal (J-FRP-ORDER, J-FRP-UNIT-TOTALITY)."},
        },
        "x-opensip-parameter-registry-extension": {"standing": "PROPOSED, pending identity owner acceptance (owner/identity-parameter-registry-patch.v1.json)",
                                                   "payloadClass": "parameter", "document": PARAMETER_DOCUMENT, "selector": "#", "atMostOnePerSpec": True,
                                                   "requiredForEvaluatorMajors": [3]},
        "x-opensip-path-law": {"standing": "PROPOSED native section 8 clarification FR-6 (owner/evidence-design-successor.v1.json#/ownerSuccessors/S1)",
                               "evidenceAndEntryPaths": "repository-relative snapshot inventory paths; evidence contentSha256 equals the inventory row sha256 (J-FRP-EVIDENCE); every entry path is inventoried (J-FRP-ENTRY)",
                               "testGlobs": "GlobPattern text matched under foundation/glob-pattern-contract.v1 against the UNIT-ROOT-RELATIVE path of a file whose retained UnitMembershipV1 row names this unit",
                               "whyStated": "native_evidence_model.recognize_frameworks keys its input by unit-root literals and every native case sits at root ''; the path base was not stated by the owner"},
        "x-opensip-new-internal-faults": {"standing": "NEW/internal pending root registry integration; no public DomainDetailCode",
                                          "keys": ["J-FRP-BOUNDS", "J-FRP-ENTRY", "J-FRP-EVIDENCE", "J-FRP-EXPLICIT", "J-FRP-ID", "J-FRP-MEMBERSHIP", "J-FRP-ORDER",
                                                   "J-FRP-PARAMETER-DIGEST", "J-FRP-SNAPSHOT", "J-FRP-SUMMARY", "J-FRP-UNIT", "J-FRP-UNIT-TOTALITY"]},
        "$defs": dict(copies, **{
            "LogicalPath": {"type": "string", "minLength": 1, "maxLength": 4096, "pattern": "^[^/\\\\\\u0000]{1,255}(/[^/\\\\\\u0000]{1,255})*(?![\\s\\S])",
                            "not": {"pattern": "(^|/)\\.\\.?(/|$)"}, "description": "Byte-identical constraint to identity-schemas.v3.json#/$defs/LogicalPath."},
            "UnitRecognitionV1": {"type": "object", "additionalProperties": False, "required": ["unitOrdinal", "rootPath", "markerPath", "recognitionId", "recognition"],
                                  "properties": {
                                      "unitOrdinal": {"type": "integer", "minimum": 0, "maximum": 18446744073709551615},
                                      "rootPath": {"$ref": "#/$defs/InternalUnitRootV1"},
                                      "markerPath": {"type": "string", "maxLength": 4096},
                                      "recognitionId": {"type": "string", "pattern": "^sha256:[0-9a-f]{64}(?![\\s\\S])",
                                                        "x-opensip-digest": {"representation": "h-identity", "domain": "native.framework-recognition.v1", "form": "sha256-text",
                                                                             "retention": "derived", "authority": "native"},
                                                        "description": "H(native.framework-recognition.v1, recognition) under native_identity; re-derived at admission (J-FRP-ID)."},
                                      "recognition": {"$ref": "#/$defs/FrameworkRecognitionV1"}}},
        }),
    }


def identity_patch(identity_raw):
    identity = json.loads(identity_raw)
    rows = identity["x-opensip-payload-registry"]["classes"]["parameter"]["rows"]
    assert PARAMETER_DOCUMENT not in rows
    return {
        "schemaVersion": 1,
        "standing": "author-01 proposed identity owner successor selector; parent bytes never edited",
        "parent": {"path": "docs/coop/design-corrections/foundation/identity-schemas.v3.json", "sha256": sha(identity_raw), "bytes": len(identity_raw)},
        "ops": [{"op": "add", "path": "/x-opensip-payload-registry/classes/parameter/rows/" + pointer_token(PARAMETER_DOCUMENT), "before": "absent",
                 "after": {"document": PARAMETER_DOCUMENT, "selector": "#", "owner": "foundation",
                           "note": "Exactly one FrameworkRecognitionPlanV1 for evaluator3: per-unit native recognition and explicit entry points, Plan-bound (native FR-5).",
                           "requiredForEvaluatorMajors": [3]}}],
        "identityEffects": {
            "planId": "changes for every evaluator3 Plan: a new required parameter enters analysis-spec.parameters and analysisSpecDigest. Not gratuitous: FR-5 already requires recognizer changes to be Plan-visible, reachability origins and ClosedWorldV2.entryPointsRecognized consume these entry points, and replayable assurance needs the exact input. No universe, context, fact2, coverage2 or subject3 identity changes.",
            "runId": "changes through planId only",
            "historicalRuns": "Runs sealed under the predecessor profile stay admitted under their own profile (the frozen24/V1 precedent in query-projection-contract.v3 section 3); the report shows entryRecognition.state=not-plan-bound and derives no entry evidence for them.",
            "closedVocabularies": "none widened: the row uses the existing requiredForEvaluatorMajors vocabulary; the foundation record-document digest sweep list (identity-and-evidence section 3 'foundation record document') must add this document (integration duty RP-EV-INT-IDENTITY)",
        },
    }


def successor_register(M, report_patch_doc, identity_patch_doc, parameter_raw):
    return {
        "schemaVersion": 1,
        "standing": "author-01 report evidence design successor register for actual separate review and root acceptance; not approval. Covers RP-DO-03, RP-DO-05, RP-DO-09, RP-DO-10 only; the other seven report feature obligations and every integration obligation of subject-05 are untouched.",
        "parent": {"subject": SUBJECT05, "subjectManifestSha256": SUBJECT05_MANIFEST_SHA256, "designObligations": SUBJECT05 + "/owner/design-obligations.v1.json",
                   "coverageOverlay": SUBJECT05 + "/owner/implementation-coverage-successor.v1.json"},
        "obligations": [
            {"id": "RP-DO-03", "featureId": "coupling-importer-package-membership", "requirement": "prototype-report-inventory.md R08",
             "registerSuggestion": "query owner coupling projection from retained UnitMembershipV1",
             "challenge": "UnitMembershipV1 is workspace granularity: a Rust file belongs to the cargo-workspace unit, not to a package, and #[path] or shared files defeat any directory inference. Package ownership therefore needs SourceUnitOwnershipV1 (target ownership) joined through the declaring manifest (target markerPath) to a first-party SubjectInventoryV1 package row; SourceUnitOwnership alone is target ownership, not package ownership. TS/JS keeps UnitMembershipV1 (its unit is the program directory). No public query operation is needed: a whole-view internal projection under the section 8 closure replaces per-endpoint admission.",
             "mechanism": ["S3 query section 8a internal whole-view imports@resolved-target projection with reconciled occupancy", "importer symbol -> path from Plan-bound symbol SubjectInventoryV1 rows (native attestation)",
                           "path -> owner keys by World.path_owner_keys (reference_model)", "report CouplingPanelV1"],
             "deliveredCarrier": "/$defs/CouplingPanelV1", "featureStateRemoved": True, "coverageIssue": "/reviewIssueAdditions/2", "status": "design-candidate"},
            {"id": "RP-DO-05", "featureId": "entry-point-recognition", "requirement": "prototype-report-inventory.md R12",
             "registerSuggestion": "retain FrameworkRecognitionV1.entryPoints with the Run; query admits them as path starts",
             "challenge": "FrameworkRecognitionV1.entryPoints is only {state, source}; actual paths are recognized effects per unit plus explicit configuration, and no owner binds a recognition to a unit or a Plan. It is retained as a Plan parameter (FR-5 Plan-visibility) rather than a new Run field or cache. The query start law is not changed: starts stay ordinary admitted endpoints (reachability origins); the host joins their native-attested paths to the retained effective entry set.",
             "mechanism": ["S1 native section 8 FR-6/FR-7 clarifications", "S2 FrameworkRecognitionPlanV1 parameter + identity registry row", "public graph.neighbors reachability@from-resolved-calls and graph.path calls@resolved-callee",
                           "report EntryRecognitionStateV1 and EntryTraceV1"],
             "deliveredCarrier": "/$defs/EntryTraceV1", "featureStateRemoved": True, "coverageIssue": "/reviewIssueAdditions/4", "status": "design-candidate"},
            {"id": "RP-DO-09", "featureId": "symbol-metrics", "requirement": "prototype-report-inventory.md R07",
             "registerSuggestion": "register metric relations with the native/foundation owners",
             "challenge": "A registered metric relation would mint fact2/Coverage claims that duplicate derived counts and would need its own totality law. The admitted graph operations already give exact-or-lower-bound counts qualified by countBasis and the section 6 disclosure over an exact endpoint, universe and fact-view; a closed metric catalog names them precisely. They are static projected counts, never runtime hotness, and a zero supports absence only when exact without limitations.",
             "mechanism": ["closed metric catalog of five graph operations", "report SymbolMetricV1 with recomputed reading"], "deliveredCarrier": "/$defs/SymbolMetricV1",
             "featureStateRemoved": True, "coverageIssue": "/reviewIssueAdditions/8", "status": "design-candidate",
             "catalogLimit": "Size and complexity metrics have no owned native producer; adding one is a catalog successor with its owner, not part of this candidate."},
            {"id": "RP-DO-10", "featureId": "test-reachability", "requirement": "prototype-report-inventory.md R07",
             "registerSuggestion": "workflow/native owners define a test-reachability fact with import provenance",
             "challenge": "Imported TestPayloadV1 carries a free testId and an optional file-level subjectPath with no owner-defined subject-under-test meaning; it is executed observation, not a static origin identity, and a test name or path guess is not identity. Exact origins exist natively: symbols attributed to paths owned only by selected Rust test targets, and TS/JS symbols of the unit whose unit-relative path matches a retained vitest-jest testGlob. Static reach uses public graph.reach/graph.path; no new fact or import kind.",
             "mechanism": ["S2 recognition parameter (testGlobs)", "SourceUnitOwnershipV1 test targets", "report TestOriginSetV1 and TestReachabilityV1"],
             "deliveredCarrier": "/$defs/TestReachabilityV1", "featureStateRemoved": True, "coverageIssue": "/reviewIssueAdditions/9", "status": "design-candidate"},
        ],
        "ownerSuccessors": [
            {"id": "S1", "owner": "native", "selector": "docs/v2/contracts/product-v1/native-evidence.md section 8 (after FR-5)", "kind": "prose addition; no schema change",
             "text": ["FR-6 Paths in FrameworkRecognitionResultV1.evidence[].path and effects.entryPoints are repository-relative snapshot inventory paths; testGlobs are GlobPattern text matched under foundation/glob-pattern-contract.v1 against the unit-root-relative path of a file whose retained UnitMembershipV1 row names the unit.",
                      "FR-7 One FrameworkRecognitionV1 is produced per WorkspaceUnitV2 with languageFamily rust or tsjs and is committed with its unit in FrameworkRecognitionPlanV1. When explicit entryPoints are configured they replace recognized effects as the effective entry set; recognized results remain retained evidence."],
             "modelDuty": "native_evidence_model.recognize_frameworks takes the unit root and emits repository-relative paths; cases gain a non-root unit"},
            {"id": "S2", "owner": "foundation/identity", "selector": identity_patch_doc["ops"][0]["path"], "document": PARAMETER_DOCUMENT,
             "documentSha256": sha(parameter_raw), "documentBytes": len(parameter_raw), "candidate": "owner/framework-recognition-plan.schema.v1.json",
             "patch": "owner/identity-parameter-registry-patch.v1.json"},
            {"id": "S3", "owner": "query", "selector": "docs/coop/design-corrections/workflows/query-projection-contract.v3.md new section 8a", "kind": "prose + model; no schema or Operation change",
             "text": "8a Internal whole-view projection for host reporting: project_whole_view(relation@rung) runs section 8 steps 1-4 and 7 without endpoint admission and returns every projectable fact of the selected views in fact2 order with its reconciled target occupancy (first-party|external|unknown), the same countBasis, produced-item law and GraphEvidenceDisclosure. It is not a public operation, grants no authority, and is consumed only by the reporting projection.",
             "modelDuty": "query_projection_model.v3 gains project_whole_view sharing traverse admission"},
            {"id": "S4", "owner": "report (this unit's parent)", "patch": "owner/report-projection-successor-patch.v1.json", "opsCount": len(report_patch_doc["ops"])},
            {"id": "S5", "owner": "workflows (imported evidence)", "change": "none: TestPayloadV1 and the import registry are unchanged and are not origin sources"},
            {"id": "S6", "owner": "enumeration / subject inventory", "change": "none: consumes SubjectInventoryV1 symbol row path (native attestation) and package rows"},
            {"id": "S7", "owner": "native SourceUnitOwnershipV1", "change": "none: consumed as target ownership; the package join is the declaring markerPath to a package inventory row"},
        ],
        "featureMapSuccessor": {
            "R07": [{"kind": "report", "ref": "/$defs/GraphPanelV1/properties/subjectIndex"}, {"kind": "report", "ref": "/$defs/SubjectResolutionV1"},
                    {"kind": "report", "ref": "/$defs/SymbolMetricV1"}, {"kind": "report", "ref": "/$defs/TestOriginSetV1"}, {"kind": "report", "ref": "/$defs/TestReachabilityV1"}],
            "R08": [{"kind": "report", "ref": "/$defs/GraphSlotV1/properties/purpose"}, {"kind": "report", "ref": "/$defs/CouplingPanelV1"}],
            "R12": [{"kind": "report", "ref": "/$defs/GraphSlotV1/properties/anchorSubjectIds"}, {"kind": "report", "ref": "/$defs/EntryRecognitionStateV1"},
                    {"kind": "report", "ref": "/$defs/EntryTraceV1"}],
        },
        "integrationDuties": [
            {"id": "RP-EV-INT-SCHEMA", "owner": "report", "duty": "apply owner/report-projection-successor-patch.v1.json to the accepted report-projection bytes; drop the four featureStates rows and RP-DO-03/05/09/10 from design-obligations readiness.blockers; replace fixtures featureMap R07/R08/R12 with featureMapSuccessor"},
            {"id": "RP-EV-INT-BUDGET", "owner": "report", "duty": "extend PROJECTION_PRIORITY to comparison, catalog, evidence, graph, symbolEvidence, coupling, history under the shared explorationMaxCanonicalBytes 4,194,304; documentMaxBytes is unchanged because both panels draw from that cap; byte-budget omission uses ItemProjectionV1 (metricsProjection, drilldownProjection)"},
            {"id": "RP-EV-INT-STATIC", "owner": "report", "duty": "static parity successor (labelled-canonical-lines.4) names the host-asserted items of both provenance consts (coupling per-cell counts and attribution, test-reach no-origin intersection, recognition custody)"},
            {"id": "RP-EV-INT-GENERATOR", "owner": "generation registry (RP-OBL-G01)", "duty": "register the successor report schema and FrameworkRecognitionPlanV1 source bytes; regenerate Rust/TypeScript bindings; not run by this author"},
            {"id": "RP-EV-INT-COVERAGE", "owner": "implementation coverage successor", "duty": "close review issues /reviewIssueAdditions/2,4,8,9 only after the S1-S4 successors are reviewed; add delivery rows for the reporting projection (coupling, symbol evidence), the query section 8a internal projection, native per-unit recognition emission and the identity parameter row (M4 report features, M2/M3 producers)"},
            {"id": "RP-EV-INT-IDENTITY", "owner": "identity", "duty": "add the parameter document to the foundation record-document digest sweep list and to Run closure required refs; close_run refuses a missing required parameter under the successor profile"},
            {"id": "RP-EV-INT-RETENTION", "owner": "identity/lifecycle", "duty": "the parameter preimage is a required closure ref: expiry/purge/corrupt/partial map to entryRecognition.state=unavailable with that availability; a report is an offline snapshot of the observed generation"},
            {"id": "RP-EV-INT-BROWSER", "owner": "report browser lane (RP-OBL-B01/B02)", "duty": "symbol-detail and coupling views render unknown/lower-bound/blocker states, interpretation consts and the test-origin filter state; not executed"},
            {"id": "RP-EV-INT-MEASURE", "owner": "measurement (RP-OBL-M01)", "duty": "whole-view imports projection cost, five metric queries per planned symbol and reach walks up to the public caps; not measured"},
        ],
        "remainingBlockers": [],
        "remainingDependencies": ["S1, S2 and S3 owner acceptance (proposals here, not accepted)", "report-projection successor acceptance (S4)"],
    }


def build(arch, M):
    native_raw = (arch / "docs/coop/design-corrections/native/native-evidence.schemas.v2.json").read_bytes()
    identity_raw = (arch / "docs/coop/design-corrections/foundation/identity-schemas.v3.json").read_bytes()
    report_raw = open(SUBJECT05 + "/report-projection.schema.json", "rb").read()
    parameter = recognition_parameter_schema(json.loads(native_raw))
    parameter_raw = dump(parameter)
    defs = report_defs(M)
    patch = report_patch(report_raw, defs)
    ipatch = identity_patch(identity_raw)
    return {
        "owner/framework-recognition-plan.schema.v1.json": parameter,
        "owner/report-projection-successor-patch.v1.json": patch,
        "owner/identity-parameter-registry-patch.v1.json": ipatch,
        "owner/evidence-design-successor.v1.json": successor_register(M, patch, ipatch, parameter_raw),
    }
