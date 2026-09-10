#!/usr/bin/env python3
"""Bounded independent review of first-party FILE/PACKAGE target representability."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
PROBES = OUT / "probes"
PRIOR_OUT = Path(
    "/tmp/opensip-design-corrections/consumer-b.v12-kit-query-attribution-review.v1/output"
)
sys.path.insert(0, str(PRIOR_OUT))

from independent.admit_run import Store, hex_of  # noqa: E402
from independent.kit_core import parse_h_frame  # noqa: E402

NEW = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-query-attribution-review.v1/new-inputs")
SNAP_STORE = NEW / "runs/ts.store.json"
MAN = NEW / "input-manifest.json"
INV_CLAIM = NEW / "query-run-graph-inventory.json"
KIT_MANIFEST = Path(
    "/tmp/opensip-design-corrections/consumer-b.v12-kit-other-runs-review.v1/subject/consumer-input-manifest.json"
)
REQ = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-other-runs-review.v1/requirements.json")
CHARTER = Path(
    "/tmp/opensip-design-corrections/consumer-b.v12-kit-other-runs-selfaudit.v3/original-consumer-charter.txt"
)
PRIOR_MD = PRIOR_OUT / "query-attribution-review.md"
PRIOR_JSON = PRIOR_OUT / "query-attribution-review.json"
PYTHON = "/tmp/opensip-architecture-review-env/bin/python"

EXPECTED_MAN = "7ca1f3c9e8a68acecf23584998a90bd04ebac4c97f1310a6f076bb29c830003d"
EXPECTED_KIT = "ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8"
EXPECTED_REQ = "855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495"
EXPECTED_CHARTER = "57df2ed62cfb57173209dfcd55f8698c977173f4e854e42b7ad57e9e2eb8a8ec"
EXPECTED_PRIOR_MD = "65a15c505c2162552531b09e1c24f5a0233f90320cd87b4492bf3fdbdbc6d3ba"
EXPECTED_PRIOR_JSON = "6633c11f204c7792f7c62f449fd77dc860415abdd6701de49fe88d5d27ddba38"

SUBJECT_ID = re.compile(r"^[a-z][a-z0-9-]*:[^\u0000-\u001f\u007f-\u009f]+(?![\s\S])")
LOGICAL_PATH = re.compile(r"^[^/\\\u0000]{1,255}(/[^/\\\u0000]{1,255})*(?![\s\S])")
DOT_SEG = re.compile(r"(^|/)\.\.?(/|$)")
CANONICAL_TEXT = re.compile(r"^[^\u0000-\u001f\u007f-\u009f]+(?![\s\S])")
HEX64 = re.compile(r"^[0-9a-f]{64}(?![\s\S])")

# Independently chosen ordinary names. Not taken from the retained TS graph and
# not chosen to make LogicalPath/packageName intersect SubjectIdV1.
ORD_FILE = "src/lib/util.ts"
ORD_PKG = "demo-app"
ORD_MANIFEST = "package.json"
ORD_SYMBOL = "module:src/lib/util.ts"
ORD_FILE_AS_SID = "file:src/lib/util.ts"
ORD_PKG_AS_SID = "package:demo-app"
INTERSECTING_PATH = "file:src/lib/util.ts"  # valid LogicalPath AND SubjectIdV1; excluded from ordinary cases
U = "0" * 64


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def grammar(s: str) -> dict:
    lp = bool(LOGICAL_PATH.match(s)) and not DOT_SEG.search(s)
    return {
        "value": s,
        "subjectIdV1": bool(SUBJECT_ID.match(s)),
        "logicalPath": lp,
        "canonicalText": bool(CANONICAL_TEXT.match(s)) and 1 <= len(s) <= 4096,
    }


def endpoint(kind: str, native: str, pkg: str = "") -> dict:
    return {
        "universe": U,
        "kind": kind,
        "nativeSubjectId": native,
        "packageManifestPath": pkg,
    }


def load_diagnostic_store() -> dict:
    """Re-read authorized TS store for diagnostic identity inequality. Not Run admission."""
    store = Store.load(SNAP_STORE)
    run_id = sorted(k for k in store.object_table if str(k).startswith("run3:"))[0]
    run = parse_h_frame(store.rehash(store.object_table[run_id]["digest"]), allowed_domains={"run"})["value"]
    seal = parse_h_frame(
        store.rehash(store.object_table[run["evaluationSealId"]]["digest"]), allowed_domains={"evaluation-seal"}
    )["value"]
    proof = parse_h_frame(
        store.rehash(store.object_table[seal["proofBundleId"]]["digest"]), allowed_domains={"proof-bundle"}
    )["value"]
    ei = store.parse_canonical(proof["executionInputsDigest"])
    view_ref = next(r for r in ei["selectedRefs"] if r["domain"] == "view")
    view = parse_h_frame(store.rehash(view_ref["digest"]), allowed_domains={"view"})["value"]
    facts = []
    for fid in view["facts"]:
        rec = parse_h_frame(store.rehash(store.object_table[fid]["digest"]), allowed_domains={"fact"})["value"]
        if rec.get("relation") != "imports":
            continue
        pl = store.parse_canonical(rec["payloadDigest"])
        facts.append({"id": fid, "record": rec, "payload": pl})
    coverages = []
    for cid in view["coverageIds"]:
        crec = parse_h_frame(store.rehash(store.object_table[cid]["digest"]), allowed_domains={"coverage"})["value"]
        cpl = store.parse_canonical(crec["payloadDigest"])
        if (cpl.get("key") or {}).get("relation") != "imports":
            continue
        entry = cpl.get("entry") or {}
        rc = entry.get("resolutionCompleteness") if isinstance(entry.get("resolutionCompleteness"), dict) else {}
        coverages.append(
            {
                "id": cid,
                "coverage": entry.get("coverage"),
                "examinedExhaustive": rc.get("examinedExhaustive"),
                "key": cpl.get("key"),
                "closedWorldKeys": sorted((entry.get("closedWorld") or {}).keys())
                if isinstance(entry.get("closedWorld"), dict)
                else None,
                "resolutionCompletenessState": rc.get("state"),
            }
        )
    inventories = []
    seen = set()
    for r in ei["selectedRefs"]:
        if r["domain"] == "subject-inventory" and r["digest"] not in seen:
            seen.add(r["digest"])
            rec = store.parse_canonical(r["digest"])
            inventories.append(
                {
                    "digest": r["digest"],
                    "kind": rec.get("kind"),
                    "rows": [
                        {
                            "kind": row.get("kind"),
                            "nativeSubjectId": row.get("nativeSubjectId"),
                            "path": row.get("path"),
                            "qualifiedName": row.get("qualifiedName"),
                        }
                        for row in rec.get("rows") or []
                    ],
                }
            )
    attrs = []
    for r in ei["selectedRefs"]:
        if r["domain"] == "target-attribution":
            attrs.append({"digest": r["digest"], "record": store.parse_canonical(r["digest"])})
    uni = hex_of(facts[0]["record"]["sourceUniverse"]) if facts else None
    attr_by_fact = {a["record"]["sourceFactId"]: a for a in attrs}
    projected = []
    for f in facts:
        if f["record"].get("resolution") != "resolved-target":
            continue
        a = attr_by_fact.get(f["id"])
        if a is None:
            continue
        ar = a["record"]
        projected.append(
            {
                "factId": f["id"],
                "importer": f["payload"].get("importer"),
                "resolvedTarget": f["payload"].get("resolvedTarget"),
                "specifier": f["payload"].get("specifier"),
                "kind": ar.get("kind"),
                "occupancy": ar.get("occupancy"),
                "targetNativeId": ar.get("targetNativeId"),
                "logicalPath": ar.get("logicalPath"),
                "packageManifestPath": ar.get("packageManifestPath"),
                "payloadEqualsTargetNativeId": ar.get("targetNativeId") == f["payload"].get("resolvedTarget"),
            }
        )
    file_ids = sorted(
        {
            row["nativeSubjectId"]
            for inv in inventories
            for row in inv["rows"]
            if row["kind"] == "file"
        }
    )
    pkg_rows = [
        row for inv in inventories for row in inv["rows"] if row["kind"] == "package"
    ]
    return {
        "standing": "diagnostic observation of already-authorized TS store bytes; not whole-Run admission",
        "runId": run_id,
        "universe": uni,
        "fileInventoryNativeIds": file_ids,
        "packageInventoryRows": pkg_rows,
        "projectedImports": projected,
        "importsCoverage": coverages,
        "nativeIdEqualities": [
            {
                "resolvedTarget": e["resolvedTarget"],
                "equalsAnyFileInventoryNativeId": e["resolvedTarget"] in file_ids,
                "equalsAnyPackageNativeId": e["resolvedTarget"] in {r["nativeSubjectId"] for r in pkg_rows},
            }
            for e in projected
        ],
    }


def build_cases(grammars: dict) -> list[dict]:
    file_g = grammars["ordinaryFilePath"]
    pkg_g = grammars["ordinaryPackageName"]
    sym_g = grammars["ordinarySymbolId"]
    file_sid = grammars["namespacedFileSubjectId"]
    pkg_sid = grammars["namespacedPackageSubjectId"]
    assert file_g["logicalPath"] and not file_g["subjectIdV1"]
    assert pkg_g["canonicalText"] and not pkg_g["subjectIdV1"]
    assert sym_g["subjectIdV1"]
    assert file_sid["subjectIdV1"]
    assert pkg_sid["subjectIdV1"]
    assert file_g["value"] != file_sid["value"]
    assert pkg_g["value"] != pkg_sid["value"]

    e_file_inv = endpoint("file", ORD_FILE)
    e_file_proj = endpoint("file", ORD_FILE_AS_SID)
    e_pkg_inv = endpoint("package", ORD_PKG, ORD_MANIFEST)
    e_sym = endpoint("symbol", ORD_SYMBOL)

    return [
        {
            "id": "C1-ordinary-first-party-file-import-target",
            "advertised": True,
            "surface": "PolicyDocumentV2 rule subjectEnumeration.subjectKind=file, Atom.endpoint=target, relation=imports, minResolution=resolved-target. Registry relations.imports.targetKinds includes file; kindApplicability.endpointTarget requires the rule kind to be a member of targetKinds.",
            "exampleStanding": "reasoning-only; not Run admission",
            "inventory": {
                "kind": "file",
                "nativeSubjectId": ORD_FILE,
                "path": ORD_FILE,
                "qualifiedName": ORD_FILE,
            },
            "evaluationSubject": e_file_inv,
            "payload": {
                "importer": ORD_SYMBOL,
                "specifier": "./util",
                "resolvedTarget": ORD_FILE_AS_SID,
            },
            "targetAttributionAttempt": {
                "targetNativeId": ORD_FILE_AS_SID,
                "kind": "file",
                "occupancyTried": "first-party",
                "packageManifestPath": None,
                "logicalPath": None,
            },
            "joins": {
                "targetNativeIdEqualsPayload": True,
                "targetNativeIdEqualsInventoryNativeId": False,
                "parseForbidden": True,
                "ephemeralFirstPartySize": 0,
                "firstPartyJoin": "TARGET_ATTRIBUTION_FIRST_PARTY_NOT_IN_INVENTORY",
                "lawfulOccupancy": "external (sidecar) or unknown (absent sidecar)",
            },
            "atomIncoming": {
                "nativeIdCompare": "payload.resolvedTarget != E.nativeSubjectId => known nonmatch",
                "matchingFacts": [],
                "knownHitOnInventorySubject": False,
            },
            "query": {
                "inventoryVertex": e_file_inv,
                "projectedTargetVertex": e_file_proj,
                "verticesEqual": False,
                "neighborsAtInventoryFile": [],
                "neighborsAtProjectedFile": ["<the attributed imports fact>"],
                "emptyNeighborsMeansNoCallers": False,
            },
            "providerCanRepresentKnownPositiveToExactFirstPartySubject": False,
            "howHostPreservesRelationship": "As occupancy=external (or unknown) projected query vertex (U, file, file:src/lib/util.ts). Not as the first-party evaluation subject (U, file, src/lib/util.ts). logicalPath is not a native-id compare field and MUST be null on first-party occupancy.",
            "classification": "architectural-gap",
            "reason": "The combination is advertised and admitted (not ATOM_KIND_INCOMPATIBLE). Ordinary first-party file N cannot equal SubjectIdV1 resolvedTarget without parsing. Known-hit on that exact inventory subject is unreachable. External occupancy is a different subject.",
        },
        {
            "id": "C2-ordinary-first-party-package-import-target",
            "advertised": True,
            "surface": "subjectEnumeration.subjectKind=package, Atom.endpoint=target, imports@resolved-target. Registry imports.targetKinds includes package. First-party package occupancy additionally requires non-null packageManifestPath exact-matching inventory (packageName, path).",
            "exampleStanding": "reasoning-only; not Run admission",
            "inventory": {
                "kind": "package",
                "nativeSubjectId": ORD_PKG,
                "path": ORD_MANIFEST,
                "qualifiedName": ORD_PKG,
            },
            "evaluationSubject": e_pkg_inv,
            "payload": {
                "importer": ORD_SYMBOL,
                "specifier": "demo-app",
                "resolvedTarget": ORD_PKG_AS_SID,
            },
            "targetAttributionAttempt": {
                "targetNativeId": ORD_PKG_AS_SID,
                "kind": "package",
                "occupancyTried": "first-party",
                "packageManifestPath": ORD_MANIFEST,
                "logicalPath": None,
            },
            "joins": {
                "targetNativeIdEqualsPayload": True,
                "targetNativeIdEqualsInventoryNativeId": False,
                "packageManifestWouldMatchIfNativeIdMatched": True,
                "parseForbidden": True,
                "ephemeralFirstPartySize": 0,
                "firstPartyJoin": "TARGET_ATTRIBUTION_FIRST_PARTY_NOT_IN_INVENTORY",
                "lawfulOccupancy": "external (sidecar) or unknown (absent sidecar / ambiguous name)",
            },
            "atomIncoming": {
                "nativeIdCompare": "payload.resolvedTarget != E.nativeSubjectId => known nonmatch",
                "matchingFacts": [],
                "knownHitOnInventorySubject": False,
            },
            "query": {
                "inventoryVertex": e_pkg_inv,
                "projectedTargetVertex": endpoint("package", ORD_PKG_AS_SID, ""),
                "verticesEqual": False,
                "note": "Query package vertices from inventory include packageManifestPath; projected package targets only include it when kind is package AND the projection law supplies it. Native-id strings still differ.",
            },
            "providerCanRepresentKnownPositiveToExactFirstPartySubject": False,
            "howHostPreservesRelationship": "As occupancy=external/unknown projected imports target whose nativeSubjectId is the SubjectIdV1 payload, not (package, demo-app, package.json).",
            "classification": "architectural-gap",
            "reason": "Package is an advertised imports target kind and a first-party evaluation-subject kind, but ordinary packageName is not SubjectIdV1. Native-id compare cannot occupy the inventory package subject.",
        },
        {
            "id": "C3-ordinary-first-party-symbol-import-or-calls-target",
            "advertised": True,
            "surface": "subjectEnumeration.subjectKind=symbol|export, endpoint=target, imports@resolved-target or calls@resolved-callee or references@resolved-binding or control-flow/reachability. Symbol inventory nativeSubjectId is SubjectIdV1; payload target fields are SubjectIdV1.",
            "exampleStanding": "reasoning-only; not Run admission",
            "inventory": {
                "kind": "symbol",
                "nativeSubjectId": ORD_SYMBOL,
                "path": ORD_FILE,
            },
            "evaluationSubject": e_sym,
            "payload": {
                "importer": "module:src/app.ts",
                "specifier": "./util",
                "resolvedTarget": ORD_SYMBOL,
            },
            "targetAttributionAttempt": {
                "targetNativeId": ORD_SYMBOL,
                "kind": "symbol",
                "occupancyTried": "first-party",
                "exported": "exported",
                "packageManifestPath": None,
                "logicalPath": None,
            },
            "joins": {
                "targetNativeIdEqualsPayload": True,
                "targetNativeIdEqualsInventoryNativeId": True,
                "ephemeralFirstPartySize": 1,
                "firstPartyJoin": "admitted when unique identity",
                "lawfulOccupancy": "first-party",
            },
            "atomIncoming": {
                "nativeIdCompare": "equal => continue kind/occupancy reconcile",
                "matchingFacts": ["<the attributed fact>"],
                "knownHitOnInventorySubject": True,
            },
            "query": {
                "inventoryVertex": e_sym,
                "projectedTargetVertex": e_sym,
                "verticesEqual": True,
            },
            "providerCanRepresentKnownPositiveToExactFirstPartySubject": True,
            "howHostPreservesRelationship": "Payload native id, inventory nativeSubjectId, targetNativeId, evaluation-subject N, and query tuple nativeSubjectId are the same SubjectIdV1. Host ephemeral first-party projection size=1. Query and incoming occupy the same vertex.",
            "classification": "representable",
            "reason": "Symbol is the identity kind whose inventory grammar is already SubjectIdV1. This is the lawful positive first-party TARGET example. It does not substitute for advertised file/package target occupancy.",
        },
        {
            "id": "C4-external-file-import-target",
            "advertised": True,
            "surface": "Query vertex domain includes projected-fact endpoints that are not first-party inventory. occupancy=external is consistent when ephemeral size=0.",
            "exampleStanding": "reasoning-only; not Run admission",
            "payload": {"resolvedTarget": "file:node_modules/left-pad/index.js"},
            "targetAttribution": {
                "targetNativeId": "file:node_modules/left-pad/index.js",
                "kind": "file",
                "occupancy": "external",
                "logicalPath": None,
            },
            "providerCanRepresentKnownPositiveToExactFirstPartySubject": False,
            "howHostPreservesRelationship": "Query vertex (U, file, file:node_modules/left-pad/index.js). Not an inventory subject. First-party occupancy would refuse.",
            "classification": "representable",
            "reason": "External occupancy plus projected query vertex is the jointly satisfiable authoring already established. It does not represent a known-hit on a first-party file/package evaluation subject.",
        },
        {
            "id": "C5-first-party-file-as-source-not-target",
            "advertised": True,
            "surface": "relations.file / vcs-change / clones: sourceField is path (LogicalPath / CanonicalPath). endpointTarget=forbidden.",
            "exampleStanding": "reasoning-only; not Run admission",
            "inventory": {"kind": "file", "nativeSubjectId": ORD_FILE, "path": ORD_FILE},
            "payload": {"path": ORD_FILE},
            "sourceOccupancy": "payload.path equals evaluation-subject nativeSubjectId",
            "knownHitOnInventorySubject": True,
            "classification": "representable",
            "reason": "First-party FILE SOURCE occupancy is representable. Unary file/package relations do not advertise endpoint=target.",
        },
        {
            "id": "C6-first-party-package-as-source-not-target",
            "advertised": True,
            "surface": "relations.package sourceOccupancy: payload.packageName AND payload.manifestPath must equal evaluation-subject nativeSubjectId and packageManifestPath. endpointTarget=forbidden.",
            "exampleStanding": "reasoning-only; not Run admission",
            "inventory": {
                "kind": "package",
                "nativeSubjectId": ORD_PKG,
                "path": ORD_MANIFEST,
            },
            "payload": {"packageName": ORD_PKG, "manifestPath": ORD_MANIFEST, "packageVersion": "1.0.0"},
            "sourceOccupancy": "both name and manifest path",
            "knownHitOnInventorySubject": True,
            "classification": "representable",
            "reason": "First-party PACKAGE SOURCE occupancy is representable. The package relation is not a target endpoint.",
        },
        {
            "id": "C7-file-endpoint-target-on-calls",
            "advertised": False,
            "surface": "calls.targetKinds={symbol}. kindApplicability.endpointTarget: rule kind must be a member of targetKinds. Wrong kind is ATOM_KIND_INCOMPATIBLE, never vacuous none.",
            "exampleStanding": "reasoning-only; not Run admission",
            "attempt": "subjectKind=file, endpoint=target, calls@resolved-callee",
            "classification": "explicitlyunsupported",
            "refusal": "ATOM_KIND_INCOMPATIBLE",
            "reason": "File is not an advertised calls target kind. This is not the imports file-target gap.",
        },
        {
            "id": "C8-imports-syntactic-specifier-endpoint-target",
            "advertised": False,
            "surface": "imports.endpointTargetRungs=[resolved-target]. specifier is not a native id. Query table: imports@syntactic-specifier is not graph-projectable.",
            "exampleStanding": "reasoning-only; not Run admission",
            "attempt": "endpoint=target at syntactic-specifier",
            "classification": "explicitlyunsupported",
            "refusal": "ATOM_ENDPOINT_UNAVAILABLE (atom) / QUERY.RELATION_UNSUPPORTED (graph request)",
            "reason": "Deliberate rung unavailability, not identity inequality.",
        },
        {
            "id": "C9-unary-file-or-package-endpoint-target",
            "advertised": False,
            "surface": "file/package/declares/literal/types/clones/vcs-change/unresolved-edge: targetKinds=[], endpointTarget=forbidden.",
            "exampleStanding": "reasoning-only; not Run admission",
            "classification": "explicitlyunsupported",
            "refusal": "ATOM_ENDPOINT_UNAVAILABLE",
            "reason": "Unary relations do not advertise target occupancy.",
        },
        {
            "id": "C10-first-party-occupancy-on-namespaced-file-native-id",
            "advertised": True,
            "surface": "Join law sizeZero: sidecar occupancy=first-party while no exact inventory identity refuses TARGET_ATTRIBUTION_FIRST_PARTY_NOT_IN_INVENTORY.",
            "exampleStanding": "reasoning-only; not Run admission",
            "targetNativeId": ORD_FILE_AS_SID,
            "inventoryNativeId": ORD_FILE,
            "classification": "explicitlyunsupported",
            "refusal": "TARGET_ATTRIBUTION_FIRST_PARTY_NOT_IN_INVENTORY",
            "reason": "This is an explicit join refusal of first-party occupancy, not unknown and not a silent match. It does not withdraw the advertised file target kind.",
        },
        {
            "id": "C11-first-party-occupancy-forcing-inventory-spelling-into-targetNativeId",
            "advertised": True,
            "surface": "targetNativeId MUST equal the payload field named by relations[fact.relation].targetNativeIdField. Mismatch refuses TARGET_ATTRIBUTION_NATIVE_ID_MISMATCH. ImportsPayloadV1.resolvedTarget is SubjectIdV1, so ordinary LogicalPath is not a lawful payload value either.",
            "exampleStanding": "reasoning-only; not Run admission",
            "attempt": {
                "payload.resolvedTarget": ORD_FILE_AS_SID,
                "targetNativeId": ORD_FILE,
                "occupancy": "first-party",
            },
            "classification": "explicitlyunsupported",
            "refusal": "TARGET_ATTRIBUTION_NATIVE_ID_MISMATCH (and payload.resolvedTarget=src/lib/util.ts would fail SubjectIdV1 schema)",
            "reason": "Cannot sneak the inventory spelling into targetNativeId while the payload remains namespaced, and cannot lawfully write the inventory spelling as resolvedTarget.",
        },
        {
            "id": "C12-query-neighbors-at-unequal-file-identities",
            "advertised": True,
            "surface": "query-projection-contract.v3.md §0 zero neighbor rows is not no callers; §2 vertex domain is inventory rows UNION projected endpoints; no namespace stripping.",
            "exampleStanding": "reasoning-only; not Run admission",
            "neighborsAtInventoryFile": [],
            "neighborsAtProjectedFile": ["<attributed imports fact>"],
            "QUERY.ENDPOINT_UNKNOWN_at_inventory": False,
            "classification": "representable",
            "reason": "Query preserves the edge at the namespaced file vertex and admits the inventory file as an isolated vertex. Empty neighbors is not an absence claim. This guard is query-only.",
        },
        {
            "id": "C13-incoming-none-without-coverage-S-to-U",
            "advertised": True,
            "surface": "owedPartitions.incoming.attestation and atom contract Search of U: if no CoverageResultV3 with key.targetUniverse=U, incoming none/count-at-most-true/all-covered MUST NOT infer that S searched U. Require IncomingSearchV1 or report source-target-search-unattested.",
            "exampleStanding": "reasoning-only; not Run admission",
            "classification": "unknown",
            "result": "source-target-search-unattested / incoming unknown; not none=true",
            "reason": "This is the normative guard that prevents converting unattested search into proven absence. It does not fire when complete Coverage S→U exists.",
        },
        {
            "id": "C14-incoming-none-with-complete-search-and-unequal-native-ids",
            "advertised": True,
            "surface": "matchingFacts require target nativeId=N after native-id compare. Different targetNativeId is known nomatch even if kind/occupancy unknown. Complete Coverage S→U (or admitted complete IncomingSearchV1) plus sufficiency_v2 universal-negative at resolved rungs can make incoming none true.",
            "exampleStanding": "reasoning-only; not Run admission",
            "construction": {
                "E": e_file_inv,
                "fact.targetNativeId": ORD_FILE_AS_SID,
                "nativeIdEqual": False,
                "matchingFacts": [],
                "coverage": "complete at (imports, resolved-target, S=U, T=U)",
                "sufficiency_v2": "universal-negative success stipulated as a lawful reachable provider emission",
                "incomingNone": True,
            },
            "falseResultClass": "proved-construction",
            "not": "not a potential-risk-only claim and not an unreachable input",
            "classification": "architectural-gap",
            "reason": "Known incoming evidence exists at a distinct namespaced file identity. The advertised first-party file evaluation subject sees known nomatch. Complete search of U is about universes, not about equating those identities. Query §0 does not apply to atom none.",
        },
        {
            "id": "C15-specially-chosen-colon-path-excluded",
            "advertised": False,
            "surface": "LogicalPath grammar permits a colon in a segment, so file:src/lib/util.ts can be both LogicalPath and SubjectIdV1. This review forbids using such a name as an ordinary first-party example.",
            "exampleStanding": "reasoning-only; not Run admission",
            "value": INTERSECTING_PATH,
            "classification": "unreachable-as-ordinary-input",
            "reason": "Satisfiability via grammar intersection is not ordinary first-party file identity and is not a substitute for a general representability proof.",
        },
        {
            "id": "C16-outgoing-targetKind-file-filter-on-symbol-source",
            "advertised": True,
            "surface": "FieldFilter targetKind on imports@resolved-target projects targetAttribution.kind. Current subject is the SOURCE importer (symbol inventory). endpoint defaults to source.",
            "exampleStanding": "reasoning-only; not Run admission",
            "evaluationSubject": e_sym,
            "filter": {"field": "targetKind", "cmp": "eq", "value": "file"},
            "knownHit": True,
            "classification": "representable",
            "reason": "Outgoing targetKind filtering does not require the current subject to be a file inventory row. It is not first-party FILE target occupancy.",
        },
        {
            "id": "C17-occupancy-unknown-is-not-false-when-native-ids-match",
            "advertised": True,
            "surface": "Join law absence: no sidecar and no unique first-party identity => kind/occupancy unknown, not nomatch, not false. This clause applies after native-id compare already matched.",
            "exampleStanding": "reasoning-only; not Run admission",
            "classification": "unknown",
            "reason": "Guards unknown occupancy from becoming false. It never runs for ordinary file/package import targets because native-id compare already failed.",
        },
    ]


def main() -> int:
    PROBES.mkdir(parents=True, exist_ok=True)
    man = json.loads(MAN.read_text())
    file_ok = []
    for e in man["files"]:
        p = NEW / e["path"]
        file_ok.append(
            {
                "path": e["path"],
                "sha256": sha(p),
                "bytes": p.stat().st_size,
                "match": sha(p) == e["sha256"] and p.stat().st_size == e["bytes"],
            }
        )
    custody = {
        "inputManifestSha256": sha(MAN),
        "inputManifestMatch": sha(MAN) == EXPECTED_MAN,
        "files": file_ok,
        "kitManifestSha256": sha(KIT_MANIFEST),
        "kitMatch": sha(KIT_MANIFEST) == EXPECTED_KIT,
        "requirementsSha256": sha(REQ),
        "reqMatch": sha(REQ) == EXPECTED_REQ,
        "charterSha256": sha(CHARTER),
        "charterMatch": sha(CHARTER) == EXPECTED_CHARTER,
        "priorQueryAttributionMdSha256": sha(PRIOR_MD),
        "priorQueryAttributionMdMatch": sha(PRIOR_MD) == EXPECTED_PRIOR_MD,
        "priorQueryAttributionJsonSha256": sha(PRIOR_JSON),
        "priorQueryAttributionJsonMatch": sha(PRIOR_JSON) == EXPECTED_PRIOR_JSON,
        "storeSha256": sha(SNAP_STORE),
    }
    assert custody["inputManifestMatch"] and all(x["match"] for x in file_ok)
    assert custody["kitMatch"] and custody["reqMatch"] and custody["charterMatch"]
    assert custody["priorQueryAttributionMdMatch"] and custody["priorQueryAttributionJsonMatch"]

    grammars = {
        "ordinaryFilePath": grammar(ORD_FILE),
        "ordinaryPackageName": grammar(ORD_PKG),
        "ordinaryManifestPath": grammar(ORD_MANIFEST),
        "ordinarySymbolId": grammar(ORD_SYMBOL),
        "namespacedFileSubjectId": grammar(ORD_FILE_AS_SID),
        "namespacedPackageSubjectId": grammar(ORD_PKG_AS_SID),
        "intersectingColonPathExcludedFromOrdinaryCases": grammar(INTERSECTING_PATH),
    }
    cases = build_cases(grammars)
    diagnostic = load_diagnostic_store()

    advertised = {
        "standing": "Current normative kit, not a new product requirement",
        "incorporated": "identity-and-evidence.md §4 incorporates atom-evaluation-contract.v1.md as constituent intended-design semantics. Plan commits PolicyDocumentV2.",
        "endpointOwner": {
            "selector": "foundation/evaluator-projection-registry.v1.json#/kindApplicability/endpointTarget",
            "text": "Uses relation.targetKinds, NOT sourceSubjectKind. Rule kind file|symbol|package must be a member of targetKinds.",
        },
        "policyOwner": {
            "selector": "workflows/schemas/policy-document.v2.schema.json Atom.endpoint enum source|target (default source) and subjectEnumeration.subjectKind file|symbol|export|package",
            "note": "policy-document.schema.json v1 Atom has no endpoint field. PolicyDocumentV2 is the committed profile. AtomSuccessorV1 describes the same endpoint extension.",
        },
        "importsTargetKinds": {
            "selector": "evaluator-projection-registry.v1.json#/relations/imports",
            "targetKinds": ["file", "symbol", "package"],
            "endpointTarget": "admitted-at-rung",
            "endpointTargetRungs": ["resolved-target"],
            "note": "endpoint=target admission uses TARGET kinds {file,symbol,package}, not source subjectKind symbol.",
        },
        "otherBinaryTargetKinds": {
            "calls": ["symbol"],
            "references": ["symbol"],
            "control-flow": ["symbol"],
            "reachability": ["symbol"],
        },
        "unaryEndpointTarget": "forbidden / ATOM_ENDPOINT_UNAVAILABLE",
        "queryTable": {
            "selector": "workflows/query-projection-contract.v3.md §3",
            "imports": "resolved-target; target kinds file, symbol, package; target kind from admitted TargetAttributionV1",
        },
        "incomingBind": {
            "selector": "evaluator-projection-registry.v1.json#/owedPartitions/incoming/bind",
            "text": "current E=(U,K,N) occupies the target native-id field after native-id compare; fact.targetUniverse must equal U for a MATCH.",
        },
        "compositionEnumeration": {
            "selector": "evaluator-composition-contract.v3.md §2",
            "text": "Enabled rules select every admitted program of the required primary subject kind. Include/exclude apply to logical path, never opaque native IDs.",
        },
        "conclusion": "The current design advertises first-party FILE and PACKAGE inventory subjects as lawful current evaluation subjects for imports@resolved-target endpoint=target, and advertises graph navigation to file/package import targets. It does not advertise file/package as calls/references/control-flow/reachability targets.",
    }

    constraints = {
        "required": [
            {
                "id": "R1",
                "owner": "subject-inventory.schema.v1.json InventoryRowV1.path / enumeration-contract.v1.md",
                "text": "File nativeSubjectId is the snapshot LogicalPath (equals path; qualifiedName equals path).",
            },
            {
                "id": "R2",
                "owner": "enumeration-contract.v1.md / subject-inventory package rows",
                "text": "Package nativeSubjectId is the attested packageName (equals qualifiedName). Identity is (universe, package, packageName, packageManifestPath=row.path).",
            },
            {
                "id": "R3",
                "owner": "subject-inventory.schema.v1.json symbol nativeSubjectId",
                "text": "Symbol nativeSubjectId is owner SubjectIdV1.",
            },
            {
                "id": "R4",
                "owner": "relation-payload-schemas.v2.json#/$defs/ImportsPayloadV1",
                "text": "importer and resolvedTarget are SubjectIdV1. specifier is CanonicalText, not a native id.",
            },
            {
                "id": "R5",
                "owner": "target-attribution.schema.v1.json x-opensip-join-law.joins",
                "text": "targetNativeId equals the payload field named by relations[fact.relation].targetNativeIdField at fact.resolution (imports: resolvedTarget).",
            },
            {
                "id": "R6",
                "owner": "target-attribution occupancy / derivation.never",
                "text": "occupancy=first-party iff targetNativeId is a first-party inventory subject of targetUniverse (exact native id). Never parse SubjectIdV1 spelling to invent kind or occupancy. Never invent first-party packageManifestPath from logicalPath.",
            },
            {
                "id": "R7",
                "owner": "atom-evaluation-contract.v1.md §2",
                "text": "Native-id compare is first: payload target field != N => known nonmatch even if kind unknown.",
            },
            {
                "id": "R8",
                "owner": "owedPartitions.incoming.matchingFacts",
                "text": "matchingFacts are facts whose actual targetUniverse=U and target nativeId=N (and kind reconciled).",
            },
            {
                "id": "R9",
                "owner": "owedPartitions.incoming.attestation / incoming-search.schema.v1.json",
                "text": "If no CoverageResultV3 with key.targetUniverse=U, incoming none/count-at-most-true/all-covered MUST NOT infer that S searched U. Require IncomingSearchV1 or source-target-search-unattested. Attestation is not inferred from producer facts. examinedExhaustive=false never proves complete search.",
            },
            {
                "id": "R10",
                "owner": "query-projection-contract.v3.md §0 and §2–3",
                "text": "Zero neighbor rows is not no callers. Endpoint tuple is (universe, kind, nativeSubjectId, packageManifestPath or empty). Projected imports target nativeSubjectId is payload.resolvedTarget; no invented or stripped namespaces.",
            },
            {
                "id": "R11",
                "owner": "atom-evaluation-contract.v1.md §4",
                "text": "Wrong subject.kind for the relation/endpoint is ATOM_KIND_INCOMPATIBLE, never vacuous none.",
            },
            {
                "id": "R12",
                "owner": "target-attribution first-party package",
                "text": "occupancy=first-party and kind=package requires non-null packageManifestPath exact-matching inventory (packageName=targetNativeId, path=packageManifestPath). Ambiguity stays occupancy unknown.",
            },
        ],
        "permitted": [
            "occupancy external|unknown when ephemeral first-party identity set is empty",
            "external resolved targets that are not first-party inventory remain lawful query vertices",
            "logicalPath non-null only when occupancy is external or unknown; MUST be null on first-party",
            "targetKind FieldFilter on attribution.kind for imports@resolved-target",
            "outgoing known-hit on a first-party symbol importer whose payload.importer equals symbol inventory nativeSubjectId",
        ],
        "ordinaryGrammar": grammars,
        "unsatisfiableSetForOrdinaryFirstPartyFileTarget": [
            "R1 file inventory nativeSubjectId is ordinary LogicalPath src/lib/util.ts",
            "R4 resolvedTarget is SubjectIdV1",
            "R5 targetNativeId equals resolvedTarget",
            "R6 occupancy=first-party requires targetNativeId exact inventory native id",
            "R7 native-id compare is first and does not parse namespaces",
        ],
        "jointlySatisfiableWithExternalOccupancy": "Replace occupancy=first-party with occupancy=external (or unknown). Constraints hold. The evaluation subject and the projected target remain distinct tuples.",
    }

    reconsideration = {
        "priorClassification": "query-attribution-review G1: existing-law identity inequality; not a missing/contradictory law because occupancy=external is jointly satisfiable; first-party occupancy on namespaced file SubjectIdV1 is the unsatisfiable set if first-party is demanded",
        "priorStandingRetainedAs": "Still not a pairwise schema contradiction. External occupancy remains lawful. That statement is not withdrawn.",
        "priorStandingInsufficientFor": "Advertised first-party FILE and PACKAGE target filtering, incoming analysis/absence, and graph identity of inventory subjects.",
        "revisedClassification": "genuine architectural gap for advertised first-party FILE and PACKAGE import TARGET occupancy on ordinary identities",
        "not": "Not a newly invented product requirement: registry targetKinds, kindApplicability.endpointTarget, PolicyDocumentV2 endpoint, composition subject-kind enumeration, query table, and incoming bind already advertise the combination",
        "gapVsExplicitlyUnsupported": "C7–C9/C10–C11 are explicit refusals. C1/C2/C14 are advertised combinations whose known-hit is unreachable and whose incoming none can be true under complete search.",
    }

    corrections = {
        "standing": "Design-level options only. No kit edit, no graph remint, no claimed implemented fix.",
        "requirementForAnyCoherentFix": "Atom matchingFacts / native-id compare must occupy the same native string as the first-party evaluation subject N. Changing occupancy metadata alone (logicalPath, sidecar occupancy) cannot create a known-hit while R7 compares payload SubjectIdV1 to inventory LogicalPath/packageName.",
        "options": [
            {
                "id": "O1-withdraw-file-package-from-imports-target-kinds",
                "change": "imports.targetKinds becomes {symbol} for first-party evaluation; file/package subjectEnumeration + endpoint=target becomes ATOM_KIND_INCOMPATIBLE. Query may still project occupancy=external file/package vertices as non-inventory endpoints, or the query table may drop those target kinds in the same revision.",
                "compatibility": "Policy rules that enumerate file/package incoming imports start refusing. Existing external occupancy graphs remain lawful. Smallest if product intent is symbol-only first-party import targets.",
            },
            {
                "id": "O2-file-package-inventory-native-id-becomes-attested-SubjectIdV1",
                "change": "File/package inventory keep path/manifestPath as LogicalPath and attest nativeSubjectId as SubjectIdV1 independently (no parse of path). Evaluation subject N and query inventory vertices use that SubjectIdV1. Payload already uses SubjectIdV1.",
                "compatibility": "Remints every file/package evaluation-subject, inventory native id, and query inventory vertex. Fingerprints still use path. Breaking for consumers that treated LogicalPath as file nativeSubjectId.",
            },
            {
                "id": "O3-kind-discriminated-payload-target-native-id",
                "change": "When attribution.kind=file, the native-id field used for matching is LogicalPath (inventory spelling); when kind=package, packageName plus packageManifestPath; when kind=symbol, SubjectIdV1. Requires payload and/or targetNativeIdField law change.",
                "compatibility": "Remints imports facts and collapses today's two file vertices (src/lib/util.ts vs file:src/lib/util.ts) into one. Existing namespaced query vertices disappear.",
            },
            {
                "id": "O4-kind-discriminated-compare-using-typed-sidecar-fields-not-namespace-parse",
                "change": "Keep payload SubjectIdV1. For kind=file, matchingFacts compare E.nativeSubjectId to a typed LogicalPath sidecar field that is allowed on first-party occupancy; for kind=package, compare (packageName, packageManifestPath). This is a new compare law, not a parse of namespace:opaque.",
                "compatibility": "Requires reversing logicalPath MUST be null on first-party occupancy and reversing native-id-compare-is-first against payload. Existing external graphs would need a published migration for which vertex is the first-party subject.",
            },
        ],
        "rejectedAsCurrentLaw": [
            "Parsing file: off SubjectIdV1",
            "Inventing alias records that equate (file, src/lib/util.ts) with (file, file:src/lib/util.ts)",
            "Treating logicalPath as occupancy identity under current join law",
            "Treating empty query neighbors as no callers",
            "Treating unattested incoming search as none=true",
        ],
    }

    limitations = [
        "Not whole-Run close_run admission of the authorized TS store. Prior scoped identity-closure observation compilerPackageDigest-is-toolchain-tree-member remains. Query/atom interpretation of that store is diagnostic/not acceptance.",
        "Not execution of graph.neighbors/path/reach or evaluate_atom. Cases are kit-derived reasoning examples labeled not Run admission.",
        "Not a claim that occupancy=external is unsatisfiable. That authoring remains lawful for external vertices.",
        "Closed-world/sufficiency_v2 on the retained TS coverage entry is observed at Coverage key, coverage=complete, resolutionCompleteness.state, and examinedExhaustive when present on that record. C14's none=true construction stipulates lawful complete sufficiency as a reachable provider emission, not as a verified sufficiency_v2 replay of this store.",
        "policy-document.schema.json v1 Atom lacks endpoint; the committed profile is PolicyDocumentV2. If a consumer presented only v1 atoms, endpoint would default to source and file incoming imports would not be expressible in that older schema. That is a schema-generation standing note, not withdrawal of registry/atom/query advertisement.",
        "No reference implementation, fixtures, goldens, root reports, or other origins were read.",
        "No normative kit bytes or graph bytes were edited.",
    ]

    report = {
        "standing": "Same P4 original kit-only reviewer origin. Bounded follow-through on this origin's query-attribution-review.v1 COMPLETE13 conclusion about distinct namespaced file targets vs file/package inventory identity. Functional representability of advertised first-party FILE/PACKAGE target filtering, incoming analysis/absence, and graph navigation. Not whole-consumer ACCEPT. Not query execution. Not graph remint.",
        "command": f"{PYTHON} -I -B {HERE / 'target_representability_review.py'}",
        "custody": custody,
        "advertisedSurface": advertised,
        "constraintMap": constraints,
        "cases": cases,
        "diagnosticAuthorizedTsStore": diagnostic,
        "priorClassificationReconsideration": reconsideration,
        "correctionOptionsIfGap": corrections,
        "limitations": limitations,
        "verdict": {
            "genuineArchitecturalGap": True,
            "gapIds": ["C1-ordinary-first-party-file-import-target", "C2-ordinary-first-party-package-import-target", "C14-incoming-none-with-complete-search-and-unequal-native-ids"],
            "lawfulPositiveFirstPartyTarget": "C3-ordinary-first-party-symbol-import-or-calls-target",
            "externalOccupancyStillLawful": True,
            "queryEmptyNeighborsIsNotAbsence": True,
            "unattestedIncomingIsUnknownNotNone": True,
        },
    }

    (PROBES / "grammars.json").write_text(json.dumps(grammars, indent=2) + "\n")
    (PROBES / "diagnostic-ts-store.json").write_text(json.dumps(diagnostic, indent=2, default=str) + "\n")
    (OUT / "target-representability-review.json").write_text(json.dumps(report, indent=2, default=str) + "\n")
    (OUT / "target-representability-review.md").write_text(render_md(report) + "\n")
    return 0


def render_md(r: dict) -> str:
    c = r["custody"]
    a = r["advertisedSurface"]
    lines: list[str] = []
    lines.append("# Target representability independent architecture review")
    lines.append("")
    lines.append(r["standing"])
    lines.append("")
    lines.append("**Verdict:** genuine architectural gap for advertised first-party FILE and PACKAGE import TARGET occupancy on ordinary identities. First-party SYMBOL targets remain representable. occupancy=external remains lawful for a distinct namespaced vertex. That last fact is not a substitute for first-party file/package target representability.")
    lines.append("")
    lines.append("Query interpretation of the authorized TS store remains **diagnostic / not acceptance** (prior scoped MUST `ts.compilerPackageDigest-is-toolchain-tree-member`). Reasoning examples below are **not Run admission**.")
    lines.append("")
    lines.append("## Custody")
    lines.append("")
    lines.append(f"- new-inputs manifest `{c['inputManifestSha256']}` match={c['inputManifestMatch']}")
    for f in c["files"]:
        lines.append(f"- `{f['path']}` `{f['sha256']}` match={f['match']}")
    lines.append(f"- kit `{c['kitManifestSha256']}` match={c['kitMatch']}")
    lines.append(f"- requirements `{c['requirementsSha256']}` match={c['reqMatch']}")
    lines.append(f"- charter `{c['charterSha256']}` match={c['charterMatch']}")
    lines.append(f"- prior query-attribution-review.md `{c['priorQueryAttributionMdSha256']}` match={c['priorQueryAttributionMdMatch']}")
    lines.append(f"- prior query-attribution-review.json `{c['priorQueryAttributionJsonSha256']}` match={c['priorQueryAttributionJsonMatch']}")
    lines.append(f"- this store `{c['storeSha256']}`")
    lines.append("")
    lines.append(f"Command: `{r['command']}`")
    lines.append("")
    lines.append("Author helpers, root checkers, expected values, reference implementations, fixtures, and goldens were not read.")
    lines.append("")
    lines.append("## Advertised-surface proof")
    lines.append("")
    lines.append("This is not a newly invented product requirement. The following current owners already advertise first-party FILE and PACKAGE as import targets of incoming analysis and as graph target kinds.")
    lines.append("")
    lines.append(f"- Incorporated: {a['incorporated']}")
    lines.append(f"- Endpoint applicability: `{a['endpointOwner']['selector']}` — {a['endpointOwner']['text']}")
    lines.append(f"- Policy: {a['policyOwner']['selector']}. {a['policyOwner']['note']}")
    lines.append(f"- Imports: `{a['importsTargetKinds']['selector']}` targetKinds={a['importsTargetKinds']['targetKinds']}, endpointTarget={a['importsTargetKinds']['endpointTarget']} at {a['importsTargetKinds']['endpointTargetRungs']}. {a['importsTargetKinds']['note']}")
    lines.append(f"- Other binary native targetKinds: calls={a['otherBinaryTargetKinds']['calls']}, references={a['otherBinaryTargetKinds']['references']}, control-flow={a['otherBinaryTargetKinds']['control-flow']}, reachability={a['otherBinaryTargetKinds']['reachability']}.")
    lines.append(f"- Unary relations: {a['unaryEndpointTarget']}.")
    lines.append(f"- Query: `{a['queryTable']['selector']}` — {a['queryTable']['imports']}.")
    lines.append(f"- Incoming bind: `{a['incomingBind']['selector']}` — {a['incomingBind']['text']}")
    lines.append(f"- Enumeration: `{a['compositionEnumeration']['selector']}` — {a['compositionEnumeration']['text']}")
    lines.append("")
    lines.append(a["conclusion"])
    lines.append("")
    lines.append("File and package as SOURCE of unary inventory relations are a different advertised surface (endpointTarget forbidden) and remain representable. Outgoing `targetKind=file` filters on a symbol source are also a different surface (attribution.kind, not file-inventory occupancy).")
    lines.append("")
    lines.append("## Constraint map")
    lines.append("")
    lines.append("### Required")
    lines.append("")
    for item in r["constraintMap"]["required"]:
        lines.append(f"- **{item['id']}** (`{item['owner']}`): {item['text']}")
    lines.append("")
    lines.append("### Permitted")
    lines.append("")
    for item in r["constraintMap"]["permitted"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("### Ordinary grammars used in cases (independently chosen)")
    lines.append("")
    lines.append("These names were not chosen to intersect SubjectIdV1 with LogicalPath or packageName.")
    lines.append("")
    lines.append("| name | value | SubjectIdV1 | LogicalPath | CanonicalText |")
    lines.append("|---|---|---|---|---|")
    g = r["constraintMap"]["ordinaryGrammar"]
    rows = [
        ("ordinary file path", g["ordinaryFilePath"]),
        ("ordinary package name", g["ordinaryPackageName"]),
        ("ordinary manifest path", g["ordinaryManifestPath"]),
        ("ordinary symbol id", g["ordinarySymbolId"]),
        ("namespaced file SubjectIdV1", g["namespacedFileSubjectId"]),
        ("namespaced package SubjectIdV1", g["namespacedPackageSubjectId"]),
        ("colon path (excluded from ordinary cases)", g["intersectingColonPathExcludedFromOrdinaryCases"]),
    ]
    for label, row in rows:
        lines.append(
            f"| {label} | `{row['value']}` | {row['subjectIdV1']} | {row['logicalPath']} | {row['canonicalText']} |"
        )
    lines.append("")
    lines.append("Unsatisfiable set for ordinary first-party FILE import target occupancy:")
    for item in r["constraintMap"]["unsatisfiableSetForOrdinaryFirstPartyFileTarget"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append(r["constraintMap"]["jointlySatisfiableWithExternalOccupancy"])
    lines.append("")
    lines.append("## Discriminating cases")
    lines.append("")
    lines.append("All cases are kit-derived reasoning examples, **not replacement graph admission** and not `evaluate_atom` / `execute_graph_query` execution.")
    lines.append("")
    for case in r["cases"]:
        lines.append(f"### {case['id']}")
        lines.append("")
        lines.append(f"- Advertised combination: **{case['advertised']}**")
        lines.append(f"- Classification: **{case['classification']}**")
        lines.append(f"- Surface: {case['surface']}")
        lines.append(f"- Reason: {case['reason']}")
        if "providerCanRepresentKnownPositiveToExactFirstPartySubject" in case:
            lines.append(
                f"- Provider can lawfully represent a known positive to that exact first-party evaluation subject: **{case['providerCanRepresentKnownPositiveToExactFirstPartySubject']}**"
            )
        if case.get("howHostPreservesRelationship"):
            lines.append(f"- How the host preserves the relationship: {case['howHostPreservesRelationship']}")
        if case.get("refusal"):
            lines.append(f"- Exact refusal: `{case['refusal']}`")
        if case.get("falseResultClass"):
            lines.append(f"- False-result class: **{case['falseResultClass']}** — {case.get('not')}")
        if case.get("construction"):
            lines.append(f"- Construction: `{json.dumps(case['construction'], default=str)}`")
        lines.append("")
    lines.append("## Authorized TS store diagnostic (not admission)")
    lines.append("")
    d = r["diagnosticAuthorizedTsStore"]
    lines.append(f"Standing: {d['standing']}. run `{d['runId']}` universe `{d['universe']}`.")
    lines.append("")
    lines.append(f"- File inventory nativeSubjectId values: {d['fileInventoryNativeIds']}")
    lines.append(f"- Package inventory rows: `{json.dumps(d['packageInventoryRows'])}`")
    lines.append("- Projected imports@resolved-target facts:")
    for e in d["projectedImports"]:
        lines.append(
            f"  - `{e['factId']}` {e['importer']} → {e['resolvedTarget']} kind={e['kind']} occupancy={e['occupancy']} targetNativeId={e['targetNativeId']} logicalPath={e['logicalPath']}"
        )
    lines.append(f"- Native-id equalities vs inventory: `{json.dumps(d['nativeIdEqualities'])}`")
    lines.append(f"- Imports Coverage records: `{json.dumps(d['importsCoverage'])}`")
    lines.append("")
    lines.append("Observed: every projected file target native id is a SubjectIdV1 (`file:src/index.ts`, `file:node_modules/left-pad/index.js`) and none equals file inventory `src/index.ts` or package inventory `app`. One attributed fact has occupancy=external and logicalPath=`src/index.ts`. Native-id compare against the first-party file evaluation subject is known nonmatch. Query neighbors at `(file, src/index.ts)` are empty; neighbors at `(file, file:src/index.ts)` contain the attributed fact (prior tuple-law observation, not re-executed here as a query). Coverage of imports@resolved-target is `complete` with sourceUniverse=targetUniverse=this U and resolutionCompleteness.state complete, so the C13 unattested-search guard does **not** fire on this retained Coverage key. sufficiency_v2 closed-world polarity is not independently replayed here; C14 therefore uses a stipulated lawful complete sufficiency as a reachable construction, and treats this store as a live illustration of the native-id miss plus a represented S→U Coverage key, not as a verified none=true replay of this Run.")
    lines.append("")
    lines.append("## False absence versus guards")
    lines.append("")
    lines.append("| Situation | Result | Class |")
    lines.append("|---|---|---|")
    lines.append("| Query empty neighbors at inventory file | not “no callers” (query §0) | guarded; not absence |")
    lines.append("| Incoming none without Coverage S→U and without IncomingSearchV1 | `source-target-search-unattested` / unknown | guarded |")
    lines.append("| Occupancy unknown after a native-id **match** | unknown, not false | guarded; unreachable for ordinary file/package import targets |")
    lines.append("| Wrong kind for endpoint (file target of calls) | ATOM_KIND_INCOMPATIBLE | explicit unsupported; never vacuous none |")
    lines.append("| occupancy=first-party on namespaced id not in inventory | TARGET_ATTRIBUTION_FIRST_PARTY_NOT_IN_INVENTORY | explicit join refusal |")
    lines.append("| Complete Coverage S→U + sufficiency_v2 universal-negative + native-id inequality on advertised first-party file/package E | incoming none=true while a namespaced-id fact exists | **proved construction**, not merely a potential risk, not an unreachable input |")
    lines.append("")
    lines.append("Absence of representation at the inventory subject cannot silently become proven absence in query. It **can** become incoming none=true in atom evaluation once search of U is represented as complete, because matchingFacts use exact native-id equality and the namespaced fact is a known nomatch, not uncertain evidence.")
    lines.append("")
    lines.append("## Reconsideration of prior “not a gap”")
    lines.append("")
    rec = r["priorClassificationReconsideration"]
    lines.append(f"- Prior: {rec['priorClassification']}")
    lines.append(f"- Retained: {rec['priorStandingRetainedAs']}")
    lines.append(f"- Insufficient for: {rec['priorStandingInsufficientFor']}")
    lines.append(f"- Revised: **{rec['revisedClassification']}**")
    lines.append(f"- {rec['not']}")
    lines.append(f"- {rec['gapVsExplicitlyUnsupported']}")
    lines.append("")
    lines.append("## Smallest coherent design-level correction options")
    lines.append("")
    corr = r["correctionOptionsIfGap"]
    lines.append(corr["standing"])
    lines.append("")
    lines.append(corr["requirementForAnyCoherentFix"])
    lines.append("")
    for opt in corr["options"]:
        lines.append(f"### {opt['id']}")
        lines.append("")
        lines.append(opt["change"])
        lines.append("")
        lines.append(f"Compatibility: {opt['compatibility']}")
        lines.append("")
    lines.append("Not current law (must not be treated as already published):")
    for item in corr["rejectedAsCurrentLaw"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("No accepted candidate bytes were edited or replaced. No implemented fix is claimed.")
    lines.append("")
    lines.append("## Limitations")
    lines.append("")
    for item in r["limitations"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("No normative design edit. No graph remint.")
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
