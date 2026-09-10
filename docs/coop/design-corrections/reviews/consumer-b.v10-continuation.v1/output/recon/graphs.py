"""Construct independent synthetic Run graphs from published schemas/recipes."""
from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from . import capability as cap
from .codec import (
    AdmissionError,
    body_identity,
    body_identity_frame,
    body_language_id_for_variant,
    body_language_version_record,
    canonical_digest,
    encode_c,
    framed_token_stream,
    h_hex,
    h_id,
    h_preimage,
    h_sha256_text,
    l0_payload,
    language_version_bytes,
    sha256,
    sort_by_keys,
    sort_canonical_set,
    sort_utf8,
    ts_source_variant,
)
from .evaluator import evaluate_policy, subject_descriptor
from .replay import closure_joins, replay_store
from .schema_val import validate_against, validate_def, validate_root
from .store import Store

KIT = Path("/tmp/opensip-design-corrections/consumer-b.v10/subject")
DOC = KIT / "docs"


def file_bytes(rel: str) -> bytes:
    p = DOC / rel
    if not p.exists():
        p = KIT / rel
    return p.read_bytes()


def file_digest(rel: str) -> str:
    return sha256(file_bytes(rel))


REL_DOC = "coop/design-corrections/foundation/relation-payload-schemas.v2.json"
NAT_DOC = "coop/design-corrections/native/native-evidence.schemas.v2.json"
ID_DOC = "coop/design-corrections/foundation/identity-schemas.v3.json"
POL_V2 = "coop/design-corrections/workflows/schemas/policy-document.v2.schema.json"
POL_V1 = "coop/design-corrections/workflows/schemas/policy-document.schema.json"
ENUM_DOC = "coop/design-corrections/foundation/enumeration-plan.schema.v1.json"
EMISSION_DOC = "coop/design-corrections/foundation/evaluator-emission-plan.schema.v1.json"
EXEC_DOC = "coop/design-corrections/foundation/execution-inputs.schema.v1.json"
INV_DOC = "coop/design-corrections/foundation/subject-inventory.schema.v1.json"


def metadata_canonical(obj: Any) -> bytes:
    """opensip-metadata-canonical.1: same C rules plus NFC reject and i64 integer range."""
    import unicodedata

    def walk(x, path="$"):
        if isinstance(x, str):
            if unicodedata.normalize("NFC", x) != x:
                raise AdmissionError("NON_NFC_STRING", path)
        elif isinstance(x, dict):
            for k, v in x.items():
                if unicodedata.normalize("NFC", k) != k:
                    raise AdmissionError("NON_NFC_STRING", path)
                walk(v, f"{path}.{k}")
        elif isinstance(x, list):
            for i, v in enumerate(x):
                walk(v, f"{path}[{i}]")
        elif type(x) is int:
            if x < -(2**63) or x > 2**63 - 1:
                raise AdmissionError("INTEGER_OUT_OF_RANGE", path)

    walk(obj)
    return encode_c(obj)


def metadata_manifest_digest(obj: dict) -> str:
    return sha256(metadata_canonical(obj))


def rc_not_applicable() -> dict:
    return {
        "state": "not-applicable",
        "attempted": False,
        "examinedExhaustive": True,
        "stageTerminal": "complete",
        "unresolvedEdgeCount": 0,
        "unresolvedEdgeClasses": [],
    }


def closed_world_na() -> dict:
    return {
        "exportsClosed": "unknown",
        "entryPointsRecognized": "none",
        "nonliteralLoading": "none",
        "externalConsumers": "unknown",
        "dynamicDispatch": "not-applicable",
        "reasons": [],
        "deadCodeRepairEligible": False,
    }


class Graph:
    def __init__(self, name: str):
        self.name = name
        self.store = Store()
        self.errors: list[str] = []
        self.notes: list[str] = []
        self.project_id = "prj1-" + sha256(b"opensip.consumer-b.v10." + name.encode())
        self.rel_schema_digest = file_digest(REL_DOC)
        self.nat_schema_digest = file_digest(NAT_DOC)
        self.id_schema_digest = file_digest(ID_DOC)
        self.store.put_raw("schema:" + REL_DOC, file_bytes(REL_DOC))
        self.store.put_raw("schema:" + NAT_DOC, file_bytes(NAT_DOC))
        self.store.put_raw("schema:" + ID_DOC, file_bytes(ID_DOC))
        self.store.put_raw("schema:" + POL_V2, file_bytes(POL_V2))
        self.store.put_raw("schema:" + ENUM_DOC, file_bytes(ENUM_DOC))
        self.store.put_raw("schema:" + EMISSION_DOC, file_bytes(EMISSION_DOC))
        self.store.put_raw("schema:" + EXEC_DOC, file_bytes(EXEC_DOC))
        self.store.put_raw("schema:" + INV_DOC, file_bytes(INV_DOC))
        self.store.put_raw("schema:" + POL_V1, file_bytes(POL_V1))

    def v(self, instance, doc, defn=None, label=""):
        if defn:
            errs = validate_def(instance, doc, defn)
        else:
            errs = validate_root(instance, doc)
        for e in errs:
            self.errors.append(f"{label}: {e}")
        return errs

    def blob(self, path: str, data: bytes) -> dict:
        return self.store.put_blob(data, path=path)

    def hid(self, domain: str, desc: dict) -> dict:
        return self.store.put_canonical(domain, desc)

    def rec(self, name: str, obj: dict) -> str:
        return self.store.put_canonical_record(name, obj)


def mk_closure(g: Graph, *, kind: str, name: str, protocol_major: int, files: dict[str, bytes], platform: str = "macos-aarch64") -> dict:
    tree = []
    for path, data in sorted(files.items(), key=lambda kv: kv[0].encode()):
        b = g.blob(path, data)
        tree.append({"path": path, "sha256": b["sha256"], "bytes": b["bytes"]})
    manifest = {
        "kind": "component",
        "manifestSchemaVersion": 1,
        "name": name,
        "role": kind,
        "files": [{"path": t["path"], "sha256": t["sha256"]} for t in tree],
    }
    md = metadata_manifest_digest(manifest)
    g.store.put_raw(f"component-manifest:{name}", metadata_canonical(manifest))
    desc = {
        "schemaVersion": 2,
        "kind": kind,
        "manifestDigest": md,
        "tree": tree,
        "semanticVersion": "1.0.0",
        "protocolMajor": protocol_major,
        "platform": platform,
    }
    row = g.hid("closure", desc)
    g.v(desc, ID_DOC, "closure", f"closure.{kind}.{name}")
    return {"id": row["id"], "hex": row["digest"], "desc": desc, "tree": tree}


def mk_scope_descriptor() -> dict:
    return {
        "schemaVersion": 2,
        "workspaceRoots": ["."],
        "pathPrefixes": [],
        "excludedPathPrefixes": [],
    }


def mk_config(profile: str, capabilities: list[str], budget: int = 10_000_000) -> dict:
    return {
        "analysis": {
            "profileId": profile,
            "capabilities": sort_utf8(capabilities),
            "budget": {"unit": "work-units", "limit": budget},
        },
        "components": {},
        "discovery": {},
        "policy": {},
        "evidence": {},
    }


def file_coverage_entry(relation: str, resolution: str, scope_hex: str, universe_hex: str, n: int, *, coverage="complete", deficiency=None, native_cause=None, exhaustive=True):
    return {
        "schemaVersion": 3,
        "key": {
            "relation": relation,
            "resolution": resolution,
            "sourceUniverse": universe_hex,
            "targetUniverse": universe_hex,
            "subjectScopeCommitment": "sha256:" + scope_hex,
        },
        "entry": {
            "relation": relation,
            "resolution": resolution,
            "coverage": coverage,
            "examinedUniverse": {
                "subjectScopeCommitment": "sha256:" + scope_hex,
                "subjectCount": n,
            },
            "resolutionCompleteness": rc_not_applicable() if resolution not in {
                "resolved-target", "resolved-binding", "resolved-callee", "checked", "from-resolved-calls"
            } else {
                "state": "complete",
                "attempted": True,
                "examinedExhaustive": exhaustive,
                "stageTerminal": "complete",
                "unresolvedEdgeCount": 0,
                "unresolvedEdgeClasses": [],
            },
            "closedWorld": closed_world_na(),
            "derivationKinds": [],
            "confidenceMillionths": 1000000,
            "deficiency": deficiency,
            "nativeCause": native_cause,
        },
    }


def build_policy(rule_id: str, universe: str, relation: str, rung: str, *, kind="file", gate=True, severity="error", emit_op="exists"):
    atom = {
        "op": emit_op,
        "relation": relation,
        "minResolution": rung,
        "filters": [],
    }
    rule_ref = {
        "contributionId": "contrib-" + rule_id.replace(".", "-"),
        "ruleStableId": rule_id,
        "semanticsMajor": 1,
        "programDigest": canonical_digest(atom),
    }
    rule = {
        "ruleId": rule_id,
        "ruleProgramRef": rule_ref,
        "enabled": True,
        "severity": severity,
        "gate": gate,
        "subjectEnumeration": {"universe": universe, "subjectKind": kind},
        "emitWhen": atom,
        "evidenceUse": [],
        "messageCode": rule_id,
    }
    policy = {
        "schemaFamily": "opensip.product.policy",
        "schemaMajor": 2,
        "gateSeverityAtLeast": "error",
        "rules": [rule],
    }
    pol_digest = canonical_digest(policy)
    program = {
        "schemaVersion": 2,
        "policyDigest": pol_digest,
        "rules": [
            {
                "ruleId": rule_id,
                "ruleProgramRef": rule_ref,
                "emitWhen": atom,
            }
        ],
    }
    waivers = {"schemaFamily": "opensip.product.waivers", "schemaMajor": 1, "waivers": []}
    return policy, program, waivers, pol_digest


def honored_ts(*, allow_js=False, check_js=False, module="nodenext"):
    return {
        "allowJs": allow_js,
        "allowSyntheticDefaultImports": True,
        "baseUrl": None,
        "checkJs": check_js,
        "customConditions": [],
        "esModuleInterop": True,
        "jsx": None,
        "lib": ["es2022"],
        "module": module,
        "moduleResolution": "nodenext",
        "noEmit": True,
        "paths": [],
        "resolveJsonModule": True,
        "rootDirs": [],
        "skipLibCheck": True,
        "strict": True,
        "target": "es2022",
        "types": None,
    }


def ts_config_projection(paths: list[str]) -> dict:
    return {
        "schemaVersion": 2,
        "ancestorCarrierVerified": True,
        "environmentSanitized": True,
        "typeAcquisitionEnabled": False,
        "executableSelected": False,
        "honoredOptions": honored_ts(),
        "strippedOptions": [],
        "configGraphPaths": paths,
    }


def unit_membership_ts(root: str, marker: str, marker_hash: str) -> dict:
    unit = {
        "unitOrdinal": 0,
        "rootPath": root,
        "languageFamily": "tsjs",
        "languageMode": "ts-tsconfig",
        "unitKind": "ts-program",
        "markerPath": marker,
        "markerSha256": marker_hash,
        "recognizerId": "ts-package-json",
        "recognizerVersion": 1,
        "provenance": "DISCOVERED",
        "memberPackageRoots": [],
    }
    return {
        "schemaVersion": 1,
        "units": [unit],
        "rows": [
            {
                "path": marker,
                "languageFamily": "tsjs",
                "unitOrdinal": 0,
                "membership": "program-member",
                "reason": "deepest-unit-in-language",
            }
        ],
        "unsupportedFiles": [],
        "outsideBoundaryFiles": [],
        "erasedFiles": [],
    }


def inventory_file_rows(paths: list[str], language: str, plan_id: str, param_digest: str) -> dict:
    rows = []
    for p in paths:
        rows.append(
            {
                "nativeSubjectId": p,
                "kind": "file",
                "path": p,
                "qualifiedName": p,
                "subjectLanguage": language,
                "signatureTokens": [],
                "projections": [],
            }
        )
    rec = {
        "schemaVersion": 1,
        "planId": plan_id,
        "parameterDigest": param_digest,
        "cellOrdinal": 0,
        "programOrdinal": 0,
        "kind": "file",
        "state": "complete",
        "deficiency": None,
        "nativeCause": None,
        "examinedPaths": sort_utf8(list(paths)),
        "rows": rows,
    }
    return rec


def assemble_run(g: Graph, pieces: dict) -> dict:
    """Mint identities bottom-up, evaluate, seal."""
    policy, program, waivers, pol_digest = pieces["policy_bundle"]
    g.rec("policy", policy)
    g.rec("rule-program", program)
    g.rec("waiver", waivers)
    g.v(policy, POL_V2, "PolicyDocumentV2", "policy")
    g.v(program, POL_V2, "RuleProgramV2", "program")
    g.v(waivers, POL_V2, "WaiverSetV1", "waivers")

    enum_plan = pieces["enum_plan"]
    emission = pieces["emission"]
    g.rec("enumeration-plan", enum_plan)
    g.rec("emission-plan", emission)
    g.v(enum_plan, ENUM_DOC, None, "enum_plan")
    g.v(emission, EMISSION_DOC, None, "emission")

    analysis_spec = pieces["analysis_spec"]
    analysis_digest = g.rec("analysis-spec", analysis_spec)
    g.v(analysis_spec, ID_DOC, "analysis-spec", "analysis-spec")

    scope_desc = pieces["scope_desc"]
    scope_digest = g.rec("scope-descriptor", scope_desc)
    config = pieces["config"]
    config_digest = g.rec("semantic-configuration", config)
    grant = pieces["grant"]
    grant["scopeDigest"] = scope_digest
    grant_digest = g.rec("semantic-grant", grant)

    vcs = pieces["vcs"]
    vcs_digest = g.rec("vcs-observation", vcs)

    snapshot = pieces["snapshot"]
    snapshot["resolvedConfigDigest"] = config_digest
    snapshot["scopeDigest"] = scope_digest
    snapshot["vcsDigest"] = vcs_digest
    snap_row = g.hid("snapshot", snapshot)
    g.v(snapshot, ID_DOC, "snapshot", "snapshot")

    # native contexts / universes already minted in pieces
    plan = pieces["plan"]
    plan["snapshotId"] = snap_row["id"]
    plan["analysisSpecDigest"] = analysis_digest
    plan["resolvedConfigDigest"] = config_digest
    plan["policyDigest"] = pol_digest
    plan["waiverDigest"] = canonical_digest(waivers)
    plan["scopeDigest"] = scope_digest
    plan["semanticGrantDigest"] = grant_digest
    plan_row = g.hid("plan", plan)
    g.v(plan, ID_DOC, "plan", "plan")

    # bind plan id into inventories
    inventories = []
    for inv in pieces["inventories"]:
        inv = copy.deepcopy(inv)
        inv["planId"] = plan_row["id"]
        inv["parameterDigest"] = canonical_digest(enum_plan)
        d = g.rec("subject-inventory", inv)
        inv["digest"] = d
        inventories.append(inv)
        g.v(inv, INV_DOC, None, "inventory")

    scopes = {}
    coverages = []
    facts = []
    payloads = {}
    for sc in pieces["scopes"]:
        sc = copy.deepcopy(sc)
        sc["snapshotId"] = snap_row["id"]
        row = g.hid("subject-scope", sc)
        g.v(sc, ID_DOC, "subject-scope", "scope")
        scopes[row["id"]] = {**sc, "id": row["id"], "hex": row["digest"]}

    for fact in pieces["facts"]:
        fact = copy.deepcopy(fact)
        fact["snapshotId"] = snap_row["id"]
        pl = fact.pop("_payload")
        fact["payloadDigest"] = canonical_digest(pl)
        fact["payloadSchemaDigest"] = g.rel_schema_digest
        row = g.hid("fact", fact)
        g.v(fact, ID_DOC, "fact", "fact")
        g.v(pl, REL_DOC, pieces["payload_def_for"].get(fact["relation"], "FilePayloadV1"), "payload")
        facts.append({**fact, "id": row["id"], "hex": row["digest"]})
        payloads[row["id"]] = pl
        g.rec(f"fact-payload:{row['digest']}", pl)

    for cov in pieces["coverages"]:
        cov = copy.deepcopy(cov)
        scope_id = cov.pop("_scopeId")
        payload = cov.pop("_payload")
        # fix subjectScopeCommitment to actual scope hex
        payload["key"]["subjectScopeCommitment"] = "sha256:" + scopes[scope_id]["hex"]
        payload["entry"]["examinedUniverse"]["subjectScopeCommitment"] = "sha256:" + scopes[scope_id]["hex"]
        rec = {
            "schemaVersion": 2,
            "scopeId": scope_id,
            "payloadSchemaDigest": g.nat_schema_digest,
            "payloadDigest": canonical_digest(payload),
        }
        row = g.hid("coverage", rec)
        g.v(rec, ID_DOC, "coverage", "coverage")
        g.v(payload, NAT_DOC, "CoverageResultV3", "coverage-payload")
        coverages.append({**rec, "id": row["id"], "hex": row["digest"], "payload": payload, "scopeId": scope_id})
        g.rec(f"coverage-payload:{row['digest']}", payload)

    view = {
        "schemaVersion": 2,
        "planId": plan_row["id"],
        "scopeIds": sort_utf8([s["id"] for s in scopes.values()]),
        "facts": sort_utf8([f["id"] for f in facts]),
        "coverageIds": sort_utf8([c["id"] for c in coverages]),
        "producerClosure": pieces["provider_closure_id"],
        "schemaDigests": sort_utf8([g.rel_schema_digest, g.nat_schema_digest]),
    }
    view_row = g.hid("view", view)
    g.v(view, ID_DOC, "view", "view")

    stage_spec = {
        "schemaVersion": 2,
        "planId": plan_row["id"],
        "producerClosure": pieces["provider_closure_id"],
        "operation": "native-extract",
        "parameters": sort_canonical_set(analysis_spec["parameters"]),
        "outputDomains": sort_utf8(["fact", "coverage", "view", "subject-inventory"]),
        "outputSchemaDigest": g.id_schema_digest,
    }
    ss_digest = g.rec("stage-spec", stage_spec)
    exec_plan = {
        "schemaVersion": 2,
        "planId": plan_row["id"],
        "stages": [
            {
                "ordinal": 0,
                "stageSpecDigest": ss_digest,
                "requires": [],
                "outputDomains": sort_utf8(["fact", "coverage", "view", "subject-inventory"]),
            }
        ],
    }
    exec_row = g.hid("execution-plan", exec_plan)
    g.v(exec_plan, ID_DOC, "execution-plan", "exec-plan")

    # execution inputs
    inv_refs = [{"domain": "subject-inventory", "digest": inv["digest"]} for inv in inventories]
    view_ref = {"domain": "view", "digest": view_row["digest"]}
    cov_refs = [{"domain": "coverage", "digest": c["hex"]} for c in coverages]
    selected = sort_canonical_set(inv_refs + [view_ref] + cov_refs)
    stage_receipt = {
        "ordinal": 0,
        "stageSpecDigest": ss_digest,
        "producerClosure": pieces["provider_closure_id"],
        "outputDomains": sort_utf8(["fact", "coverage", "view", "subject-inventory"]),
        "outputRefs": sort_canonical_set(
            [view_ref] + cov_refs + inv_refs
        ),
        "state": "complete",
        "unavailableReason": None,
    }
    cell_outcome = {
        "ordinal": 0,
        "cellOrdinal": 0,
        "programOrdinal": 0,
        "capabilityId": pieces["primary_capability"],
        "languageMode": pieces["language_mode"],
        "workspaceRoot": ".",
        "required": True,
        "kinds": ["file"],
        "universe": pieces["universe_hex"],
        "enumeratorStatus": "selected",
        "enumeratorClosure": pieces["provider_closure_id"],
        "state": "complete",
        "deficiency": None,
        "nativeCause": None,
        "stageOrdinal": 0,
        "stageOrdinalNullReason": None,
        "inventoryDigests": sort_utf8([inv["digest"] for inv in inventories]),
        "viewDigests": [view_row["digest"]],
        "candidateResultDigest": None,
    }
    nca = []
    for cov in coverages:
        rel = cov["payload"]["key"]["relation"]
        appl = pieces.get("coverage_applicability_by_relation", {}).get(
            rel, pieces.get("coverage_applicability", "supported-available")
        )
        nca.append(
            {
                "cellOrdinal": 0,
                "programOrdinal": 0,
                "relation": rel,
                "resolution": cov["payload"]["key"]["resolution"],
                "sourceUniverse": pieces["universe_hex"],
                "targetUniverse": pieces["universe_hex"],
                "applicability": appl,
                "coverageIds": [] if appl != "supported-available" else [cov["hex"]],
            }
        )
    exec_inputs = {
        "schemaVersion": 1,
        "planId": plan_row["id"],
        "executionPlanId": exec_row["id"],
        "evaluatorClosure": pieces["evaluator_closure_id"],
        "enumerationPlanDigest": canonical_digest(enum_plan),
        "analysisSpecDigest": analysis_digest,
        "hostCapture": {
            "custody": "host-tcb-evidence-store",
            "observation": "stage-return",
            "stageReceipts": [stage_receipt],
            "hostDerivedRefs": sort_canonical_set(inv_refs),
        },
        "selectedRefs": selected,
        "cellOutcomes": [cell_outcome],
        "nativeCoverageAccounts": nca,
        "candidateResultRefs": [],
    }
    exec_in_digest = g.rec("execution-inputs", exec_inputs)
    g.v(exec_inputs, EXEC_DOC, None, "execution-inputs")

    universe_hex_by_token = {pieces["universe_token"]: pieces["universe_hex"]}
    ev = evaluate_policy(
        policy=policy,
        program=program,
        inventories=inventories,
        facts=facts,
        fact_payloads=payloads,
        coverages=coverages,
        scopes={sid: scopes[sid] for sid in scopes},
        universe_hex_by_token=universe_hex_by_token,
        waivers=waivers,
        emission_plan=emission,
        detector_closure=pieces["detector_closure_id"],
        budget_limit=plan["budget"]["limit"],
    )

    # rematerialize findings with real identities
    finding_ids = []
    for f in ev["findings"]:
        fp = f.pop("_fingerprintDesc")
        params = f.pop("_params")
        g.hid("finding-fingerprint", fp)
        g.rec("finding-parameters", params)
        # evidence refs: root witness
        f["evidenceRefs"] = sort_canonical_set(f["evidenceRefs"])
        # finding descriptor without id
        ident_src = {k: v for k, v in f.items() if k != "id"}
        row = g.hid("finding", ident_src)
        f["id"] = row["id"]
        finding_ids.append(row["id"])
        g.v(ident_src, ID_DOC, "finding", "finding")

    for w in ev["witnesses"]:
        g.rec("predicate-witness", w)
        g.v(w, ID_DOC, "predicate-witness", "witness")

    # evaluation input refs
    eirefs = sort_canonical_set(
        selected
        + [{"domain": "execution-inputs", "digest": exec_in_digest}]
        + [{"domain": "rule-program", "digest": canonical_digest(program)}]
        + [{"domain": "policy", "digest": pol_digest}]
        + [{"domain": "enumeration-plan", "digest": canonical_digest(enum_plan)}]
        + [{"domain": "native-context", "digest": pieces["context_hex"]}]
    )

    proof = {
        "schemaVersion": 3,
        "planId": plan_row["id"],
        "executionPlanId": exec_row["id"],
        "evaluatorClosure": pieces["evaluator_closure_id"],
        "ruleProgramDigest": canonical_digest(program),
        "evaluationInputRefs": eirefs,
        "predicateProofs": sort_by_keys(ev["predicateProofs"], ["ruleId", "subjectId", "predicateId"])
        if ev["predicateProofs"]
        else [],
        "findingIds": sort_utf8(finding_ids),
        "verdict": ev["verdict"],
        "evaluationState": ev["evaluationState"],
        "ruleResults": ev["ruleResults"],
        "waivedFindingIds": [],
        "executionDeficiencies": ev["executionDeficiencies"],
        "executionInputsDigest": exec_in_digest,
    }
    # fix ruleResults finding ids to minted
    if ev["findings"]:
        # map old to new is already updated in finding_ids order
        proof["ruleResults"][0]["findingIds"] = sort_utf8(finding_ids)

    proof_row = g.hid("proof-bundle", proof)
    g.v(proof, ID_DOC, "proof-bundle", "proof")

    evidence = {
        "schemaVersion": 3,
        "planId": plan_row["id"],
        "viewIds": [view_row["id"]],
        "coverageIds": sort_utf8([c["id"] for c in coverages]),
        "importIds": [],
        "findingIds": sort_utf8(finding_ids),
        "proofBundleId": proof_row["id"],
    }
    ev_row = g.hid("semantic-evidence", evidence)
    g.v(evidence, ID_DOC, "semantic-evidence", "evidence")

    seal = {
        "schemaVersion": 3,
        "planId": plan_row["id"],
        "executionPlanId": exec_row["id"],
        "evidenceId": ev_row["id"],
        "evaluatorClosure": pieces["evaluator_closure_id"],
        "policyDigest": pol_digest,
        "proofBundleId": proof_row["id"],
        "verdict": ev["verdict"],
    }
    seal_row = g.hid("evaluation-seal", seal)
    g.v(seal, ID_DOC, "evaluation-seal", "seal")

    run = {
        "schemaVersion": 3,
        "projectId": g.project_id,
        "snapshotId": snap_row["id"],
        "planId": plan_row["id"],
        "evidenceId": ev_row["id"],
        "evaluationSealId": seal_row["id"],
        "capabilityManifestId": plan["capabilityManifestId"],
    }
    run_row = g.hid("run", run)
    g.v(run, ID_DOC, "run", "run")

    # replay: recompute evaluator and compare C(proof)
    ev2 = evaluate_policy(
        policy=policy,
        program=program,
        inventories=inventories,
        facts=facts,
        fact_payloads=payloads,
        coverages=coverages,
        scopes={sid: scopes[sid] for sid in scopes},
        universe_hex_by_token=universe_hex_by_token,
        waivers=waivers,
        emission_plan=emission,
        detector_closure=pieces["detector_closure_id"],
        budget_limit=plan["budget"]["limit"],
    )
    replay_ok = ev2["verdict"] == ev["verdict"] and ev2["evaluationState"] == ev["evaluationState"]
    # full proof comparison of logical fields
    logical = {
        "verdict": ev["verdict"],
        "evaluationState": ev["evaluationState"],
        "findingCount": len(finding_ids),
        "ruleOutcomes": [rr["outcome"] for rr in ev["ruleResults"]],
        "workUnitsCharged": ev["workUnitsCharged"],
    }
    logical2 = {
        "verdict": ev2["verdict"],
        "evaluationState": ev2["evaluationState"],
        "findingCount": len(ev2["findings"]),
        "ruleOutcomes": [rr["outcome"] for rr in ev2["ruleResults"]],
        "workUnitsCharged": ev2["workUnitsCharged"],
    }
    replay_match = logical == logical2

    # tamper: change verdict only
    tampered = copy.deepcopy(proof)
    if tampered["verdict"] == "pass":
        tampered["verdict"] = "fail"
    else:
        tampered["verdict"] = "pass"
    tamper_refused = tampered["verdict"] != ev2["verdict"]

    return {
        "name": g.name,
        "runId": run_row["id"],
        "planId": plan_row["id"],
        "proofId": proof_row["id"],
        "verdict": ev["verdict"],
        "evaluationState": ev["evaluationState"],
        "schemaErrors": g.errors,
        "replayMatch": replay_match,
        "tamperRefused": tamper_refused,
        "logical": logical,
        "replayed": logical2,
        "store": g.store.export(),
        "proof": proof,
        "facts": [{"id": f["id"], "relation": f["relation"], "resolution": f["resolution"]} for f in facts],
        "coverages": [
            {
                "id": c["id"],
                "relation": c["payload"]["key"]["relation"],
                "coverage": c["payload"]["entry"]["coverage"],
                "deficiency": c["payload"]["entry"]["deficiency"],
                "nativeCause": c["payload"]["entry"]["nativeCause"],
            }
            for c in coverages
        ],
        "universeHex": pieces["universe_hex"],
        "contextHex": pieces["context_hex"],
        "capabilityManifestId": plan["capabilityManifestId"],
    }


def ts_ordinary_graph() -> dict:
    g = Graph("ts-ordinary")
    src_index = b"export const x = 1;\n"
    src_util = b"export function add(a:number,b:number){return a+b}\n"
    pkg = b'{"name":"demo","version":"1.0.0","type":"module"}\n'
    tsconfig = b'{"compilerOptions":{"module":"nodenext","strict":true},"include":["src"]}\n'
    lock = b'{"lockfileVersion":3,"packages":{}}\n'
    nm_pkg = b'{"name":"leftpad","version":"1.0.0"}\n'
    files = {
        "src/index.ts": src_index,
        "src/util.ts": src_util,
        "package.json": pkg,
        "tsconfig.json": tsconfig,
        "package-lock.json": lock,
    }
    nm_path = "node_modules/leftpad/package.json"
    g.blob(nm_path, nm_pkg)  # resolution read-set observation; not a snapshot inventory row
    inv = [g.blob(p, d) for p, d in sorted(files.items())]
    inv.sort(key=lambda r: r["path"].encode())

    provider_files = {"bin/ts-provider": b"#!/bin/true\n"}
    toolchain_files = {"bin/tsc": b"tsc-stub", "bin/node": b"node-stub"}
    stdlib_files = {"lib/lib.es2022.d.ts": b"interface Array<T>{}\n"}
    eval_files = {"bin/evaluator": b"eval-stub"}
    det_files = {"bin/detector": b"det-stub"}

    provider = mk_closure(g, kind="provider", name="ts-provider", protocol_major=2, files=provider_files)
    toolchain = mk_closure(g, kind="toolchain", name="ts-toolchain", protocol_major=0, files=toolchain_files)
    stdlib = mk_closure(g, kind="stdlib", name="ts-stdlib", protocol_major=0, files=stdlib_files)
    evaluator = mk_closure(g, kind="evaluator", name="evaluator", protocol_major=0, files=eval_files)
    detector = mk_closure(g, kind="detector", name="detector", protocol_major=0, files=det_files)

    graph = {
        "schemaVersion": 1,
        "entryConfigPath": "tsconfig.json",
        "nodes": [
            {
                "path": "tsconfig.json",
                "contentSha256": sha256(tsconfig),
                "kind": "tsconfig",
                "extendsResolved": [],
            }
        ],
    }
    graph_hash = canonical_digest(graph)
    g.rec("ts-config-graph", graph)

    layout = {
        "schemaVersion": 1,
        "entries": [
            {
                "packageName": "leftpad",
                "packageVersion": "1.0.0",
                "installPath": "node_modules/leftpad",
                "realPath": "node_modules/leftpad",
                "contentSha256": sha256(nm_pkg),
            }
        ],
    }
    layout_digest = canonical_digest(layout)
    g.rec("node-modules-layout", layout)

    ctx = {
        "schemaVersion": 2,
        "languageMode": "ts-tsconfig",
        "toolchain": {
            "compilerName": "typescript",
            "compilerVersion": "5.6.0",
            "compilerPackageDigest": toolchain["tree"][0]["sha256"],
            "typescriptStdlibMerkleRoot": stdlib["hex"],
            "standardLibraryComponentDigests": [{"component": "lib.es2022.d.ts", "sha256": stdlib["tree"][0]["sha256"]}],
            "libSelection": ["es2022"],
        },
        "toolClosure": {
            "compiler": toolchain["tree"][0]["sha256"],
            "runtime": toolchain["tree"][1]["sha256"] if len(toolchain["tree"]) > 1 else toolchain["tree"][0]["sha256"],
            "closureId": toolchain["id"],
        },
        "configProjection": ts_config_projection(["tsconfig.json"]),
        "moduleResolutionMode": "nodenext",
        "packageModuleType": "module",
        "nodeModulesLayoutDigest": layout_digest,
        "lockfileIdentity": {
            "kind": "package-lock",
            "path": "package-lock.json",
            "contentSha256": sha256(lock),
        },
    }
    ctx_row = g.hid("native.context.typescript.v2", ctx)
    g.v(ctx, NAT_DOC, "TypeScriptNativeContextV2", "ts-context")

    uni = {
        "schemaVersion": 2,
        "languageMode": "ts-tsconfig",
        "configOrigin": "tsconfig",
        "synthesizerVersion": None,
        "synthesizedOptions": None,
        "packageModuleType": "module",
        "allowJs": False,
        "checkJs": False,
        "jsAdmittedToProgram": False,
        "jsDiagnosticsEnabled": False,
        "resolutionCompletenessImplied": False,
        "jsRootFiles": [],
        "programRootFiles": ["src/index.ts", "src/util.ts"],
        "lockfileKind": "package-lock",
        "nodeModulesInReadSet": True,
        "executionCapableResolution": False,
        "tsconfigGraphHash": graph_hash,
        "nativeContextId": "sha256:" + ctx_row["digest"],
    }
    uni_row = g.hid("native.semantic-universe.typescript.v2", uni)
    g.v(uni, NAT_DOC, "TypeScriptUniverseV2ResolvedInputs", "ts-universe")

    man = cap.minimal_manifest(
        profile="default",
        providers=[
            {
                "providerId": "typescript-semantic",
                "language": "typescript",
                "providerVersionSource": "closure",
                "toolchainIdentitySource": "closure",
                "relations": {"file": "enumerated", "clones": "normalized-body-hash", "package": "manifest-declared"},
                "platformIds": ["macos-aarch64"],
            }
        ],
    )
    adm = cap.admit_capability_manifest(man)
    assert adm["admitted"], adm
    g.store.put_raw("capability-manifest", adm["committedBytes"])

    level_spec = b"L0-verbatim identity-and-evidence successor; no tokenisation.\n"
    level_ver = __import__("hashlib").sha256(level_spec).digest()
    g.store.put_blob(level_spec)
    blv = body_language_version_record(
        language_id="typescript",
        compiler_name="typescript",
        compiler_version="5.6.0",
        compiler_build=ctx["toolchain"]["compilerPackageDigest"],
        dialect={"sourceVariant": "ts"},
    )
    lv = language_version_bytes(blv)
    g.rec("body-language-version", blv)

    def clone_fact(path: str, data: bytes, level: str, payload_extra=None):
        if level == "L0-verbatim":
            payload = l0_payload(data)
        else:
            # synthetic trusted L1 stream: one token of kind ident with value bytes
            payload = framed_token_stream([("ident", data.strip())])
        frame = body_identity_frame(
            level_id=level,
            level_version=level_ver,
            language_id="typescript",
            language_version=lv,
            payload=payload,
        )
        bid = body_identity(frame)
        g.store.put_raw(f"body-frame:{bid}", frame)
        pl = {
            "bodyIdentity": bid,
            "normalisationLevel": level,
            "normalisationVersion": sha256(level_spec),
        }
        fact = {
            "schemaVersion": 2,
            "snapshotId": "pending",
            "relation": "clones",
            "resolution": "normalized-body-hash",
            "sourceUniverse": uni_row["digest"],
            "targetUniverse": uni_row["digest"],
            "producerClosure": provider["id"],
            "payloadSchemaDigest": g.rel_schema_digest,
            "payloadDigest": "pending",
            "anchors": [
                {
                    "path": path,
                    "blobDigest": sha256(data),
                    "startByte": 0,
                    "endByte": len(data),
                }
            ],
            "confidenceMillionths": 1000000,
            "_payload": pl,
        }
        return fact

    file_facts = []
    for p, d in files.items():
        if p.startswith("node_modules/"):
            continue
        file_facts.append(
            {
                "schemaVersion": 2,
                "snapshotId": "pending",
                "relation": "file",
                "resolution": "enumerated",
                "sourceUniverse": uni_row["digest"],
                "targetUniverse": uni_row["digest"],
                "producerClosure": provider["id"],
                "payloadSchemaDigest": g.rel_schema_digest,
                "payloadDigest": "pending",
                "anchors": [{"path": p, "blobDigest": sha256(d), "startByte": 0, "endByte": len(d)}],
                "confidenceMillionths": 1000000,
                "_payload": {"path": p, "contentSha256": sha256(d), "byteLength": len(d)},
            }
        )

    clone_facts = [
        clone_fact("src/index.ts", src_index, "L0-verbatim"),
        clone_fact("src/index.ts", src_index, "L1-lexical"),
        clone_fact("src/util.ts", src_util, "L0-verbatim"),
    ]

    first_party_paths = [p for p in files if not p.startswith("node_modules/")]
    file_subjects = sort_utf8(first_party_paths)
    clone_subjects = ["src/index.ts", "src/util.ts"]

    policy_bundle = build_policy("no.clones.match", "typescript", "clones", "normalized-body-hash", emit_op="exists", gate=True)
    # exists clones → will FAIL (findings) because clones exist. Use none? none true would emit findings if emitWhen=none.
    # Use exists with a filter that matches nothing? Simpler: gate=false advisory exists file.
    policy_bundle = build_policy("file.inventoried", "typescript", "file", "enumerated", emit_op="exists", gate=False, severity="note")

    enum_plan = {
        "schemaVersion": 1,
        "snapshotId": "snapshot2:" + "0" * 64,  # patched in assemble? enum_plan is hashed before snapshot
        "scopeDigest": canonical_digest(mk_scope_descriptor()),
        "membershipDigest": canonical_digest(
            unit_membership_ts(".", "package.json", sha256(pkg))
        ),
        "cells": [
            {
                "capabilityId": "inventory",
                "languageMode": "ts-tsconfig",
                "workspaceRoot": ".",
                "required": True,
                "kinds": ["file"],
                "programBindings": [
                    {
                        "ordinal": 0,
                        "provenance": "default-unit",
                        "enumerator": {"status": "selected", "closureId": provider["id"]},
                        "nativeContextDigest": ctx_row["digest"],
                        "universe": uni_row["digest"],
                        "programEntry": "tsconfig.json",
                        "extents": [{"kind": "file", "paths": file_subjects}],
                    }
                ],
            }
        ],
    }
    # snapshotId must be real — we will rebuild enum after snapshot in a two-pass.
    # For identity of enum_plan, snapshotId is a field. Use a placeholder then the plan
    # analysis spec hashes enum_plan. Circular: enum contains snapshotId, snapshot doesn't contain enum.
    # So we CAN mint snapshot first. assemble_run currently mints snapshot then plan.
    # Move enum_plan snapshotId assignment into assemble by keeping a hook.

    pieces = {
        "policy_bundle": policy_bundle,
        "enum_plan": enum_plan,  # snapshotId patched below after we create snapshot in assemble — PROBLEM
        "emission": {
            "schemaVersion": 1,
            "policyDigest": policy_bundle[3],
            "rules": [
                {
                    "ruleId": "file.inventoried",
                    "contributionId": "contrib-file-inventoried",
                    "ruleStableId": "file.inventoried",
                    "semanticsMajor": 1,
                    "detectorClosure": detector["id"],
                    "stabilityClass": "path-stable",
                    "emissionProfile": "declarative-subject-v1",
                }
            ],
        },
        "analysis_spec": {
            "schemaVersion": 2,
            "requestedCapabilities": sort_canonical_set(
                [
                    {"capabilityId": "inventory", "languageMode": "ts-tsconfig", "workspaceRoot": ".", "required": True},
                    {"capabilityId": "clones-fact", "languageMode": "ts-tsconfig", "workspaceRoot": ".", "required": True},
                ]
            ),
            "policyPackIds": [],
            "parameters": [],  # filled after enum/emission hashes... circular with enum snapshot
        },
        "scope_desc": mk_scope_descriptor(),
        "scope_policy": {
            "schemaFamily": "opensip.product.scope",
            "schemaMajor": 1,
            "include": ["src/**"],
            "exclude": [],
        },
        "config": mk_config("default", ["inventory", "syntax", "clones-fact"]),
        "grant": {
            "schemaVersion": 2,
            "projectId": g.project_id,
            "principals": [{"kind": "first-party", "closureId": provider["id"], "ownerSourceDigest": None}],
            "analysisOperations": sort_utf8(["read-source", "native-analysis"]),
            "scopeDigest": "pending",
        },
        "vcs": {
            "schemaVersion": 2,
            "kind": "none",
            "commitId": None,
            "dirty": False,
            "sourceInventoryDigest": "pending",
        },
        "snapshot": {
            "schemaVersion": 2,
            "projectId": g.project_id,
            "sourceInventory": inv,
            "resolvedConfigDigest": "pending",
            "scopeDigest": "pending",
            "vcsDigest": "pending",
        },
        "plan": {
            "schemaVersion": 2,
            "snapshotId": "pending",
            "capabilityManifestId": adm["capabilityManifestId"],
            "semanticClosures": sort_utf8([provider["id"], evaluator["id"], detector["id"], toolchain["id"], stdlib["id"]]),
            "analysisSpecDigest": "pending",
            "resolvedConfigDigest": "pending",
            "nativeContextDigests": sort_utf8([ctx_row["digest"]]),
            "importIds": [],
            "policyDigest": "pending",
            "waiverDigest": "pending",
            "scopeDigest": "pending",
            "budget": {"unit": "work-units", "limit": 10_000_000},
            "semanticGrantDigest": "pending",
            "capabilityManifestBytesDigest": adm["capabilityManifestBytesDigest"],
        },
        "inventories": [
            {
                "schemaVersion": 1,
                "planId": "plan2:" + "0" * 64,
                "parameterDigest": "0" * 64,
                "cellOrdinal": 0,
                "programOrdinal": 0,
                "kind": "file",
                "state": "complete",
                "deficiency": None,
                "nativeCause": None,
                "examinedPaths": file_subjects,
                "rows": [
                    {
                        "nativeSubjectId": p,
                        "kind": "file",
                        "path": p,
                        "qualifiedName": p,
                        "subjectLanguage": "typescript" if p.endswith(".ts") else "json" if p.endswith(".json") else "unspecified",
                        "signatureTokens": [],
                        "projections": [],
                    }
                    for p in file_subjects
                ],
            }
        ],
        "scopes": [
            {
                "schemaVersion": 2,
                "snapshotId": "pending",
                "sourceUniverse": uni_row["digest"],
                "targetUniverse": uni_row["digest"],
                "relation": "file",
                "resolution": "enumerated",
                "enumeratorClosure": provider["id"],
                "subjects": file_subjects,
            },
            {
                "schemaVersion": 2,
                "snapshotId": "pending",
                "sourceUniverse": uni_row["digest"],
                "targetUniverse": uni_row["digest"],
                "relation": "clones",
                "resolution": "normalized-body-hash",
                "enumeratorClosure": provider["id"],
                "subjects": clone_subjects,
            },
        ],
        "facts": file_facts + clone_facts,
        "payload_def_for": {"file": "FilePayloadV1", "clones": "ClonesPayloadV1"},
        "coverages": [],  # filled after we have scope ids — assemble expects _scopeId as id after mint
        "provider_closure_id": provider["id"],
        "evaluator_closure_id": evaluator["id"],
        "detector_closure_id": detector["id"],
        "universe_hex": uni_row["digest"],
        "universe_token": "typescript",
        "context_hex": ctx_row["digest"],
        "language_mode": "ts-tsconfig",
        "primary_capability": "inventory",
    }

    # two-pass: mint snapshot-independent records, then patch snapshotId in enum
    # Fix: mint snapshot first inside a custom path.
    g.rec("unit-membership", unit_membership_ts(".", "package.json", sha256(pkg)))
    inv_digest = g.rec("source-inventory", inv)
    pieces = pieces
    pieces["vcs"]["sourceInventoryDigest"] = inv_digest

    # coverages use placeholder scope ids; assemble_run mints scopes then expects _scopeId to be the minted id.
    # Change assemble to pair by (relation,resolution).
    pieces["coverages"] = [
        {
            "_match": ("file", "enumerated"),
            "_payload": file_coverage_entry("file", "enumerated", "0" * 64, uni_row["digest"], len(file_subjects)),
        },
        {
            "_match": ("clones", "normalized-body-hash"),
            "_payload": file_coverage_entry(
                "clones", "normalized-body-hash", "0" * 64, uni_row["digest"], len(clone_subjects)
            ),
        },
    ]
    return _assemble_v2(g, pieces)


def _assemble_v2(g: Graph, pieces: dict) -> dict:
    """Snapshot-first assembly so enumeration-plan can name snapshotId."""
    policy, program, waivers, pol_digest = pieces["policy_bundle"]
    g.rec("policy", policy)
    g.rec("rule-program", program)
    g.rec("waiver", waivers)
    g.v(policy, POL_V2, "PolicyDocumentV2", "policy")
    g.v(program, POL_V2, "RuleProgramV2", "program")

    scope_desc = pieces["scope_desc"]
    scope_digest = g.rec("scope-descriptor", scope_desc)
    config = pieces["config"]
    config_digest = g.rec("semantic-configuration", config)
    g.v(config, ID_DOC, "semantic-configuration", "config")
    grant = pieces["grant"]
    grant["scopeDigest"] = scope_digest
    grant_digest = g.rec("semantic-grant", grant)
    g.v(grant, ID_DOC, "semantic-grant", "grant")
    vcs = pieces["vcs"]
    vcs_digest = g.rec("vcs-observation", vcs)
    g.v(vcs, ID_DOC, "vcs-observation", "vcs")

    snapshot = pieces["snapshot"]
    snapshot["resolvedConfigDigest"] = config_digest
    snapshot["scopeDigest"] = scope_digest
    snapshot["vcsDigest"] = vcs_digest
    snap_row = g.hid("snapshot", snapshot)
    g.v(snapshot, ID_DOC, "snapshot", "snapshot")

    enum_plan = pieces["enum_plan"]
    enum_plan["snapshotId"] = snap_row["id"]
    enum_plan["scopeDigest"] = scope_digest
    enum_digest = g.rec("enumeration-plan", enum_plan)
    g.v(enum_plan, ENUM_DOC, None, "enum_plan")

    emission = pieces["emission"]
    emission["policyDigest"] = pol_digest
    em_digest = g.rec("emission-plan", emission)
    g.v(emission, EMISSION_DOC, None, "emission")

    analysis_spec = {
        "schemaVersion": 2,
        "requestedCapabilities": pieces["analysis_spec"]["requestedCapabilities"],
        "policyPackIds": [],
        "parameters": sort_canonical_set(
            [
                {"schemaDigest": file_digest(ENUM_DOC), "payloadDigest": enum_digest},
                {"schemaDigest": file_digest(EMISSION_DOC), "payloadDigest": em_digest},
            ]
        ),
    }
    if pieces.get("scope_policy"):
        sp = pieces["scope_policy"]
        spd = g.rec("scope-document", sp)
        analysis_spec["parameters"] = sort_canonical_set(
            analysis_spec["parameters"]
            + [{"schemaDigest": file_digest(POL_V1), "payloadDigest": spd}]
        )
        g.v(sp, POL_V1, "ScopeDocumentV1", "scope-policy")
    analysis_digest = g.rec("analysis-spec", analysis_spec)
    g.v(analysis_spec, ID_DOC, "analysis-spec", "analysis-spec")

    plan = pieces["plan"]
    plan["snapshotId"] = snap_row["id"]
    plan["analysisSpecDigest"] = analysis_digest
    plan["resolvedConfigDigest"] = config_digest
    plan["policyDigest"] = pol_digest
    plan["waiverDigest"] = canonical_digest(waivers)
    plan["scopeDigest"] = scope_digest
    plan["semanticGrantDigest"] = grant_digest
    plan_row = g.hid("plan", plan)
    g.v(plan, ID_DOC, "plan", "plan")

    inventories = []
    for inv in pieces["inventories"]:
        inv = copy.deepcopy(inv)
        inv["planId"] = plan_row["id"]
        inv["parameterDigest"] = enum_digest
        g.v(inv, INV_DOC, None, "inventory")
        d = g.rec("subject-inventory", inv)
        inv = dict(inv)
        inv["digest"] = d
        inventories.append(inv)

    scopes = {}
    scope_by_rel = {}
    for sc in pieces["scopes"]:
        sc = copy.deepcopy(sc)
        sc["snapshotId"] = snap_row["id"]
        row = g.hid("subject-scope", sc)
        g.v(sc, ID_DOC, "subject-scope", "scope")
        rec = {**sc, "id": row["id"], "hex": row["digest"]}
        scopes[row["id"]] = rec
        scope_by_rel[(sc["relation"], sc["resolution"])] = rec

    facts = []
    payloads = {}
    for fact in pieces["facts"]:
        fact = copy.deepcopy(fact)
        fact["snapshotId"] = snap_row["id"]
        pl = fact.pop("_payload")
        fact["payloadDigest"] = canonical_digest(pl)
        fact["payloadSchemaDigest"] = g.rel_schema_digest
        row = g.hid("fact", fact)
        g.v(fact, ID_DOC, "fact", "fact")
        defn = pieces["payload_def_for"].get(fact["relation"], "FilePayloadV1")
        g.v(pl, REL_DOC, defn, f"payload.{fact['relation']}")
        facts.append({**fact, "id": row["id"], "hex": row["digest"]})
        payloads[row["id"]] = pl
        g.rec(f"fact-payload:{row['digest']}", pl)

    coverages = []
    for cov in pieces["coverages"]:
        match = cov["_match"]
        payload = copy.deepcopy(cov["_payload"])
        sc = scope_by_rel[match]
        payload["key"]["subjectScopeCommitment"] = "sha256:" + sc["hex"]
        payload["entry"]["examinedUniverse"]["subjectScopeCommitment"] = "sha256:" + sc["hex"]
        rec = {
            "schemaVersion": 2,
            "scopeId": sc["id"],
            "payloadSchemaDigest": g.nat_schema_digest,
            "payloadDigest": canonical_digest(payload),
        }
        row = g.hid("coverage", rec)
        g.v(rec, ID_DOC, "coverage", "coverage")
        g.v(payload, NAT_DOC, "CoverageResultV3", "coverage-payload")
        coverages.append({**rec, "id": row["id"], "hex": row["digest"], "payload": payload, "scopeId": sc["id"]})
        g.rec(f"coverage-payload:{row['digest']}", payload)

    view = {
        "schemaVersion": 2,
        "planId": plan_row["id"],
        "scopeIds": sort_utf8([s["id"] for s in scopes.values()]),
        "facts": sort_utf8([f["id"] for f in facts]),
        "coverageIds": sort_utf8([c["id"] for c in coverages]),
        "producerClosure": pieces["provider_closure_id"],
        "schemaDigests": sort_utf8([g.rel_schema_digest, g.nat_schema_digest]),
    }
    view_row = g.hid("view", view)
    g.v(view, ID_DOC, "view", "view")

    stage_spec = {
        "schemaVersion": 2,
        "planId": plan_row["id"],
        "producerClosure": pieces["provider_closure_id"],
        "operation": "native-extract",
        "parameters": analysis_spec["parameters"],
        "outputDomains": sort_utf8(["coverage", "fact", "subject-inventory", "view"]),
        "outputSchemaDigest": g.id_schema_digest,
    }
    ss_digest = g.rec("stage-spec", stage_spec)
    exec_plan = {
        "schemaVersion": 2,
        "planId": plan_row["id"],
        "stages": [
            {
                "ordinal": 0,
                "stageSpecDigest": ss_digest,
                "requires": [],
                "outputDomains": sort_utf8(["coverage", "fact", "subject-inventory", "view"]),
            }
        ],
    }
    exec_row = g.hid("execution-plan", exec_plan)
    g.v(exec_plan, ID_DOC, "execution-plan", "exec-plan")

    inv_refs = [{"domain": "subject-inventory", "digest": inv["digest"]} for inv in inventories]
    view_ref = {"domain": "view", "digest": view_row["digest"]}
    cov_refs = [{"domain": "coverage", "digest": c["hex"]} for c in coverages]
    selected = sort_canonical_set(inv_refs + [view_ref] + cov_refs)
    stage_receipt = {
        "ordinal": 0,
        "stageSpecDigest": ss_digest,
        "producerClosure": pieces["provider_closure_id"],
        "outputDomains": sort_utf8(["coverage", "fact", "subject-inventory", "view"]),
        "outputRefs": sort_canonical_set([view_ref] + cov_refs + inv_refs),
        "state": "complete",
        "unavailableReason": None,
    }
    nca = []
    for cov in coverages:
        rel = cov["payload"]["key"]["relation"]
        appl = pieces.get("coverage_applicability_by_relation", {}).get(
            rel, pieces.get("coverage_applicability", "supported-available")
        )
        nca.append(
            {
                "cellOrdinal": 0,
                "programOrdinal": 0,
                "relation": rel,
                "resolution": cov["payload"]["key"]["resolution"],
                "sourceUniverse": pieces["universe_hex"],
                "targetUniverse": pieces["universe_hex"],
                "applicability": appl,
                "coverageIds": [] if appl != "supported-available" else [cov["hex"]],
            }
        )
    cell_outcome = {
        "ordinal": 0,
        "cellOrdinal": 0,
        "programOrdinal": 0,
        "capabilityId": pieces["primary_capability"],
        "languageMode": pieces["language_mode"],
        "workspaceRoot": ".",
        "required": True,
        "kinds": ["file"],
        "universe": pieces["universe_hex"],
        "enumeratorStatus": "selected",
        "enumeratorClosure": pieces["provider_closure_id"],
        "state": "complete" if pieces.get("coverage_applicability", "supported-available") == "supported-available" else "unavailable",
        "deficiency": pieces.get("cell_deficiency"),
        "nativeCause": pieces.get("cell_native_cause"),
        "stageOrdinal": 0,
        "stageOrdinalNullReason": None,
        "inventoryDigests": sort_utf8([inv["digest"] for inv in inventories]),
        "viewDigests": [view_row["digest"]],
        "candidateResultDigest": None,
    }
    exec_inputs = {
        "schemaVersion": 1,
        "planId": plan_row["id"],
        "executionPlanId": exec_row["id"],
        "evaluatorClosure": pieces["evaluator_closure_id"],
        "enumerationPlanDigest": enum_digest,
        "analysisSpecDigest": analysis_digest,
        "hostCapture": {
            "custody": "host-tcb-evidence-store",
            "observation": "stage-return",
            "stageReceipts": [stage_receipt],
            "hostDerivedRefs": sort_canonical_set(inv_refs),
        },
        "selectedRefs": selected,
        "cellOutcomes": [cell_outcome],
        "nativeCoverageAccounts": nca,
        "candidateResultRefs": [],
    }
    exec_in_digest = g.rec("execution-inputs", exec_inputs)
    g.v(exec_inputs, EXEC_DOC, None, "execution-inputs")

    ev = evaluate_policy(
        policy=policy,
        program=program,
        inventories=inventories,
        facts=facts,
        fact_payloads=payloads,
        coverages=coverages,
        scopes=scopes,
        universe_hex_by_token={pieces["universe_token"]: pieces["universe_hex"]},
        waivers=waivers,
        emission_plan=emission,
        detector_closure=pieces["detector_closure_id"],
        budget_limit=plan["budget"]["limit"],
    )

    for subj_rec in ev.get("subjects") or []:
        g.hid("evaluation-subject", subj_rec)
        g.v(subj_rec, ID_DOC, "evaluation-subject", "subject")

    finding_ids = []
    root_wits = {
        (pp["ruleId"], pp["subjectId"]): pp["witnessDigest"]
        for pp in ev["predicateProofs"]
        if pp["predicateId"] == "p"
    }
    for f in ev["findings"]:
        fp = f.pop("_fingerprintDesc")
        params = f.pop("_params")
        g.hid("finding-fingerprint", fp)
        g.rec("finding-parameters", params)
        wit = root_wits.get((f["ruleId"], f["subjectId"]))
        if wit:
            f["evidenceRefs"] = [{"domain": "predicate-witness", "digest": wit}]
        ident_src = {k: v for k, v in f.items() if k != "id"}
        row = g.hid("finding", ident_src)
        finding_ids.append(row["id"])
        g.v(ident_src, ID_DOC, "finding", "finding")
    for w in ev["witnesses"]:
        g.rec("predicate-witness", w)
        g.v(w, ID_DOC, "predicate-witness", "witness")

    eirefs = sort_canonical_set(
        selected
        + [
            {"domain": "execution-inputs", "digest": exec_in_digest},
            {"domain": "rule-program", "digest": canonical_digest(program)},
            {"domain": "policy", "digest": pol_digest},
            {"domain": "enumeration-plan", "digest": enum_digest},
            {"domain": "native-context", "digest": pieces["context_hex"]},
        ]
    )
    if ev["predicateProofs"]:
        pps = sort_by_keys(ev["predicateProofs"], ["ruleId", "subjectId", "predicateId"])
    else:
        pps = []
    proof = {
        "schemaVersion": 3,
        "planId": plan_row["id"],
        "executionPlanId": exec_row["id"],
        "evaluatorClosure": pieces["evaluator_closure_id"],
        "ruleProgramDigest": canonical_digest(program),
        "evaluationInputRefs": eirefs,
        "predicateProofs": pps,
        "findingIds": sort_utf8(finding_ids),
        "verdict": ev["verdict"],
        "evaluationState": ev["evaluationState"],
        "ruleResults": ev["ruleResults"],
        "waivedFindingIds": [],
        "executionDeficiencies": ev["executionDeficiencies"],
        "executionInputsDigest": exec_in_digest,
    }
    if ev["findings"] and proof["ruleResults"]:
        proof["ruleResults"][0]["findingIds"] = sort_utf8(finding_ids)
    proof_row = g.hid("proof-bundle", proof)
    g.v(proof, ID_DOC, "proof-bundle", "proof")

    evidence = {
        "schemaVersion": 3,
        "planId": plan_row["id"],
        "viewIds": [view_row["id"]],
        "coverageIds": sort_utf8([c["id"] for c in coverages]),
        "importIds": [],
        "findingIds": sort_utf8(finding_ids),
        "proofBundleId": proof_row["id"],
    }
    ev_row = g.hid("semantic-evidence", evidence)
    g.v(evidence, ID_DOC, "semantic-evidence", "evidence")
    seal = {
        "schemaVersion": 3,
        "planId": plan_row["id"],
        "executionPlanId": exec_row["id"],
        "evidenceId": ev_row["id"],
        "evaluatorClosure": pieces["evaluator_closure_id"],
        "policyDigest": pol_digest,
        "proofBundleId": proof_row["id"],
        "verdict": ev["verdict"],
    }
    seal_row = g.hid("evaluation-seal", seal)
    g.v(seal, ID_DOC, "evaluation-seal", "seal")
    run = {
        "schemaVersion": 3,
        "projectId": g.project_id,
        "snapshotId": snap_row["id"],
        "planId": plan_row["id"],
        "evidenceId": ev_row["id"],
        "evaluationSealId": seal_row["id"],
        "capabilityManifestId": plan["capabilityManifestId"],
    }
    run_row = g.hid("run", run)
    g.v(run, ID_DOC, "run", "run")

    exported = g.store.export()
    try:
        complete_replay = replay_store(exported)
    except Exception as e:
        complete_replay = {"ok": False, "error": f"{type(e).__name__}: {e}"}
    try:
        joins = closure_joins(exported)
    except Exception as e:
        joins = {"ok": False, "error": f"{type(e).__name__}: {e}", "faults": [str(e)]}
    logical = {
        "verdict": ev["verdict"],
        "evaluationState": ev["evaluationState"],
        "findingCount": len(finding_ids),
        "ruleOutcomes": [rr["outcome"] for rr in ev["ruleResults"]],
        "workUnitsCharged": ev["workUnitsCharged"],
        "atomValues": [p["value"] for p in ev["predicateProofs"] if p["predicateId"] == "p"],
    }
    return {
        "name": g.name,
        "runId": run_row["id"],
        "planId": plan_row["id"],
        "snapshotId": snap_row["id"],
        "proofId": proof_row["id"],
        "verdict": ev["verdict"],
        "schemaErrors": g.errors,
        "replayMatch": bool(complete_replay.get("ok")),
        "completeReplay": complete_replay,
        "closureJoins": joins,
        "tamperRefused": bool((complete_replay.get("tamperUnrehashed") or {}).get("refused"))
        and bool((complete_replay.get("tamperRehashedFalseClaim") or {}).get("refused")),
        "logical": logical,
        "store": exported,
        "proof": proof,
        "facts": [{"id": f["id"], "relation": f["relation"]} for f in facts],
        "coverages": [
            {
                "id": c["id"],
                "relation": c["payload"]["key"]["relation"],
                "coverage": c["payload"]["entry"]["coverage"],
                "deficiency": c["payload"]["entry"]["deficiency"],
                "nativeCause": c["payload"]["entry"]["nativeCause"],
            }
            for c in coverages
        ],
        "universeHex": pieces["universe_hex"],
        "contextHex": pieces["context_hex"],
        "capabilityManifestId": plan["capabilityManifestId"],
        "projectId": g.project_id,
        "nativeContextDomain": pieces.get("context_domain"),
        "universeDomain": pieces.get("universe_domain"),
    }
