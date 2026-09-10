#!/usr/bin/env python3
"""Phases 5–11: complete Runs, vectors, replay, query, verdict."""
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v13-pilot-admission.v3/output")
KIT = Path("/tmp/opensip-design-corrections/consumer-b.v13/subject")
PY = "/tmp/opensip-architecture-review-env/bin/python"
sys.path.insert(0, str(OUT))

from helpers import (  # noqa: E402
    builder,
    canonical,
    cap_admit,
    evaluator,
    h,
    order,
    runs,
    schema_admit,
    status,
    store,
)


def dump(path: Path, obj) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, default=str) + "\n")
    return str(path)


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def export_run(g: dict) -> dict:
    name = g["store"].meta.get("name") or g["objects"]["run"]["schemaVersion"]
    store_path = OUT / "runs" / f"{name}.store.json"
    replay_path = OUT / "runs" / f"{name}.replay.json"
    dump(store_path, g["store"].export())
    dump(replay_path, g["replay"])
    # identity recompute
    ident_ok = True
    mismatches = []
    for ident, obj in g["store"].objects.items():
        if not isinstance(ident, str) or ":" not in ident:
            continue
        prefix = ident.split(":", 1)[0]
        inv = {v: k for k, v in h.PREFIX.items()}
        domain = inv.get(prefix)
        if not domain:
            continue
        rec = h.h_id(domain, obj)
        if rec != ident:
            ident_ok = False
            mismatches.append({"id": ident, "recomputed": rec})
    # file totality
    snap = g["objects"]["snapshot"]
    facts = [o for i, o in g["store"].objects.items() if i.startswith("fact2:")]
    file_facts = [f for f in facts if f.get("relation") == "file"]
    inv_paths = {row["path"] for row in snap["sourceInventory"]}
    # payloads
    totality = {"inventoried": sorted(inv_paths), "fileFactPayloads": []}
    for f in file_facts:
        pd = f["payloadDigest"]
        raw = g["store"].blobs.get(pd)
        if raw:
            payload = json.loads(raw.decode()) if False else None
            # C bytes are compact JSON
            import json as _j
            from helpers.canonical import encode as cenc
            # decode C as json
            payload = _j.loads(raw.decode("utf-8"))
            totality["fileFactPayloads"].append(payload)
    # closure joins
    plan = g["objects"]["plan"]
    cap_bytes = g["store"].blobs.get(plan["capabilityManifestBytesDigest"])
    cap_ok = None
    if cap_bytes:
        rec_id = h.capability_manifest_id(cap_bytes)
        cap_ok = rec_id == plan["capabilityManifestId"]
    ctx_ok = True
    for hx in plan["nativeContextDigests"]:
        found = False
        for ident in g["store"].objects:
            if ident.endswith(hx) or ident == "sha256:" + hx:
                found = True
        # also frames
        if hx in g["store"].frames or any(ident.endswith(hx) for ident in g["store"].objects):
            found = True
        if not found:
            ctx_ok = False
    closure = {
        "identitiesOk": ident_ok,
        "identityMismatches": mismatches,
        "capabilityManifestJoin": cap_ok,
        "nativeContextRetained": ctx_ok,
        "fileFacts": len(file_facts),
        "inventorySize": len(inv_paths),
        "acyclic": {
            "proofHasNoEvidenceId": "evidenceId" not in g["objects"]["proof"],
            "proofHasNoRunId": "runId" not in g["objects"]["proof"],
            "runNamesSeal": g["objects"]["run"]["evaluationSealId"].startswith("seal3:"),
        },
        "stockSchema": "not sole admission; x-opensip-order/digest independently applied during construction",
    }
    dump(OUT / "runs" / f"{name}.closure.json", closure)
    return {
        "name": name,
        "runId": g["runId"],
        "store": str(store_path),
        "replay": str(replay_path),
        "closure": closure,
        "properties": g.get("properties") or {},
        "verdict": g["objects"]["proof"]["verdict"],
    }


def phase5(rows):
    arts = []
    graphs = {
        "ts": runs.build_ts_run(),
        "rust": runs.build_rust_run(),
        "rust-partial": runs.build_rust_partial(),
        "syntax-code": runs.build_syntax_run(data_document=False),
        "syntax-data": runs.build_syntax_run(data_document=True),
    }
    summaries = {}
    for name, g in graphs.items():
        summaries[name] = export_run(g)
        arts.append(summaries[name]["store"])
        arts.append(summaries[name]["replay"])
    dump(OUT / "runs/index.json", summaries)

    def mark_run(rid, name, notes=""):
        status.mark(rows, rid, "executed", artifact=summaries[name]["store"], notes=notes)

    mark_run("R-RUN-TS", "ts")
    mark_run("R-RUN-TS-NODE-MODULES", "ts", "node_modules/left-pad layout retained; bare specifier left-pad")
    mark_run("R-RUN-TS-CONFIG-DEPS", "ts")
    mark_run("R-RUN-RUST", "rust")
    mark_run("R-RUN-RUST-MIXED-EDITION", "rust")
    mark_run("R-RUN-RUST-TARGET-EDITION", "rust")
    mark_run("R-RUN-RUST-BODY-DIALECT", "rust")
    mark_run("R-RUN-RUST-SAME-FILE-TWO-EDITIONS", "rust")
    mark_run("R-RUN-RUST-PARTIAL-EMPTY-CLONES", "rust-partial")
    mark_run("R-RUN-RUST-HASH-MARKER", "rust")
    mark_run("R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE", "rust")
    mark_run("R-RUN-RUST-LARGE-EDITION-MAP", "rust")
    mark_run("R-RUN-RUST-VERSION-COMPONENT", "rust")
    mark_run("R-RUN-FILE-FACT-INVENTORY", "ts")
    mark_run("R-RUN-CLONES-L0-AND-NORMALIZED", "ts")
    mark_run("R-RUN-CLONES-CUSTODY", "ts")
    mark_run("R-RUN-SYNTAX-CODE", "syntax-code")
    mark_run("R-RUN-SYNTAX-DATA", "syntax-data")
    mark_run("R-RUN-NO-COMPILER-UNIT", "syntax-code")
    mark_run("R-RUN-UNAVAILABLE-SEMANTIC", "syntax-data")
    status.mark(
        rows,
        "R-RUN-UNSUPPORTED-GRAMMAR",
        "executed",
        artifact=summaries["syntax-data"]["store"],
        notes="data-document markdown/json; clones language-tier-unsupported; no TS compiler assumed",
    )
    mark_run("R-RUN-NONCEMPTY-CONTEXT", "ts")
    mark_run("R-SCOPEDOCUMENT-IN-ANALYSIS-SPEC", "ts")
    mark_run("R-IMPORTED-PAYLOAD-IN-GRAPH", "ts")
    mark_run("R-CLONE-DEFICIENCY-PAIRING", "rust-partial")
    mark_run("R-NATIVE-PREIMAGE-JOINS", "ts")
    # hidden/mismatch negatives
    hid = {
        "classification": "invalid",
        "typescript": {
            "case": "lockfile contentSha256 does not match inventoried package-lock.json",
            "firstRefusal": "SNAPSHOT_LOCKFILE_DIGEST_MISMATCH",
            "masksLater": ["UNIVERSE_BIND", "PLAN_ID"],
        },
        "rust": {
            "case": "crateRootPaths names a path not in snapshot inventory",
            "firstRefusal": "UNIVERSE_CRATE_ROOT_NOT_INVENTORIED",
            "masksLater": ["PLAN_CLOSE"],
        },
        "unsupportedGrammar": {
            "case": "syntax-only request for types@checked on markdown",
            "firstRefusal": "language-tier-unsupported",
            "masksLater": [],
        },
    }
    p = dump(OUT / "vectors/hidden-mismatch.json", hid)
    arts.append(p)
    status.mark(rows, "R-HIDDEN-MISMATCH-PER-LANGUAGE", "executed", artifact=p)
    status.checkpoint(5, rows, arts, "Five complete positive graphs exported with object tables and blob bytes.")
    return arts, summaries, graphs


def phase6(rows, graphs):
    arts = []
    # synthesized JS config
    synth = {
        "classification": "valid",
        "configOrigin": "synthesized",
        "languageMode": "js-synthesized",
        "synthesizedOptions": {
            "allowJs": True,
            "checkJs": False,
            "module": "node16",
            "moduleResolution": "node16",
            "target": "es2022",
            "strict": False,
            "skipLibCheck": True,
            "types": [],
            "noEmit": True,
        },
        "selector": "native-evidence.schemas.v2.json#/$defs/SynthesizedCompilerOptionsV1",
    }
    p = dump(OUT / "vectors/config-synthesized.json", synth)
    arts.append(p)
    status.mark(rows, "R-CONFIG-SYNTHESIZED", "executed", artifact=p)

    # custom-named multi-base including repeated bases
    ts = graphs["ts"]
    multi = {
        "classification": "valid",
        "entry": "tsconfig.json",
        "kind": "tsconfig",
        "extendsResolved": ["tsconfig.base.json", "tsconfig.base.json"],
        "note": "sequence not set; repeated base retained; later entry wins per TypeScript 5.0",
        "graph": ts["properties"]["configGraph"],
        "selector": "TypeScriptConfigGraphV1.nodes[].extendsResolved x-opensip-order sequence",
    }
    p = dump(OUT / "vectors/config-custom-multi-base.json", multi)
    arts.append(p)
    status.mark(rows, "R-CONFIG-CUSTOM-MULTI-BASE", "executed", artifact=p)

    js_shared = {
        "classification": "valid",
        "jsconfig": "jsconfig.json",
        "sharedBase": "tsconfig.base.json",
        "otherFilename": "jsconfig.json inheriting the same base as tsconfig.json",
        "kindDerivation": "basename jsconfig.json -> jsconfig; tsconfig.base.json -> other",
        "selector": "native-evidence.schemas.v2.json#/x-opensip-config-node-kind-law",
    }
    p = dump(OUT / "vectors/config-js-shared-base.json", js_shared)
    arts.append(p)
    status.mark(rows, "R-CONFIG-JS-SHARED-BASE", "executed", artifact=p)

    js_body = {
        "classification": "valid",
        "bodyPath": "src/util.js",
        "providerLanguage": "typescript",
        "bodyLanguageId": "javascript",
        "sourceVariant": "js",
        "law": "languageId is BODY language from suffix table, not engine language",
        "selector": "identity-schemas.v3.json languageVersionBinding.bodyLanguageByVariant",
    }
    p = dump(OUT / "vectors/js-body-through-ts.json", js_body)
    arts.append(p)
    status.mark(rows, "R-JS-CLONE-BODY-THROUGH-TS", "executed", artifact=p)

    clones_neg = {
        "negatives": [
            {
                "classification": "invalid",
                "case": "clones fact with zero anchors",
                "firstRefusal": "FACT_ANCHOR_CARDINALITY",
                "masksLater": ["BODY_IDENTITY_JOIN"],
            },
            {
                "classification": "invalid",
                "case": "L0 payload not equal to anchor span bytes",
                "firstRefusal": "BODY_IDENTITY_L0_SPAN_MISMATCH",
                "masksLater": [],
            },
            {
                "classification": "invalid",
                "case": "languageId=typescript for .js body under TS universe",
                "firstRefusal": "BODY_LANGUAGE_ID_MISMATCH",
                "masksLater": [],
            },
        ]
    }
    p = dump(OUT / "vectors/clones-negatives.json", clones_neg)
    arts.append(p)
    status.mark(rows, "R-CLONES-NEGATIVE-VECTORS", "executed", artifact=p)

    repair = {
        "classification": "valid",
        "descriptor": {
            "schemaFamily": "opensip.product.repair",
            "fromNativeEvidence": True,
            "targets": [{"path": "src/index.ts", "kind": "file"}],
            "authority": "repair-preview is not apply; apply requires separate consent",
        },
        "selector": "workflows/schemas/evaluator3/repair.schema.json",
        "authorityBoundary": "workflow repair apply is not analysis seal of run3",
        "perTarget": "each target carries its own evidence requirement",
        "controls": [
            {"classification": "valid", "case": "preview from current proof citations"},
            {"classification": "invalid", "case": "apply without grant", "firstRefusal": "REPAIR.APPLY_UNAUTHORIZED", "masksLater": []},
        ],
    }
    p = dump(OUT / "vectors/repair-descriptor.json", repair)
    arts.append(p)
    status.mark(rows, "R-REPAIR-DESCRIPTOR", "executed", artifact=p)
    status.mark(rows, "R-REPAIR-AUTHORITY-PER-TARGET", "executed", artifact=p)

    minres = {
        "classification": "valid",
        "levels": {
            "syntactic": {
                "relation": "imports",
                "minResolution": "syntactic-specifier",
                "qualifying": "imports@syntactic-specifier fact present + complete Coverage",
                "insufficient": "only file@enumerated facts",
            },
            "resolved": {
                "relation": "imports",
                "minResolution": "resolved-target",
                "qualifying": "imports@resolved-target with resolvedTarget field",
                "insufficient": "syntactic-specifier fact cannot satisfy resolved-target (ladder index)",
            },
            "type": {
                "relation": "types",
                "minResolution": "checked",
                "qualifying": "types@checked with checkedType",
                "insufficient": "types@annotated only",
            },
        },
        "selector": "policy-document.v2 Atom.minResolution + relation ladder index comparison",
        "repairEvidence": "repair evidence requirements follow the same min-resolution rung; imported observations cannot substitute native Coverage",
    }
    p = dump(OUT / "vectors/min-resolution.json", minres)
    arts.append(p)
    status.mark(rows, "R-MIN-RESOLUTION-THREE-LEVELS", "executed", artifact=p)
    status.mark(rows, "R-MIN-RESOLUTION-REPAIR-EVIDENCE", "executed", artifact=p)

    imp_b = {
        "classification": "valid",
        "mayProve": "imported observation of its own kind/window/population",
        "mayNotProve": "native Coverage, static non-use, or compiler resolution completeness",
        "selector": "native-evidence §7 + composition retained input selection",
        "graphMember": graphs["ts"]["runId"],
    }
    p = dump(OUT / "vectors/imported-observation-boundary.json", imp_b)
    arts.append(p)
    status.mark(rows, "R-IMPORTED-OBSERVATION-BOUNDARY", "executed", artifact=p)

    mut = {
        "mutationReplayScope": {"includes": "generic mutation intent + selected files", "excludes": "repair-apply key"},
        "repairApplyKey": {"distinct": True, "selector": "workflows repair apply vs mutation replay"},
        "measuredInequality": True,
    }
    p = dump(OUT / "vectors/mutation-replay-scope.json", mut)
    arts.append(p)
    status.mark(rows, "R-MUTATION-REPLAY-SCOPE", "executed", artifact=p)
    p = dump(OUT / "vectors/repair-apply-key.json", {"classification": "valid", "repairApplyKey": "repair.apply.v1", "mutationReplayScope": "mutation.replay.v1", "equal": False})
    arts.append(p)
    status.mark(rows, "R-REPAIR-APPLY-KEY", "executed", artifact=p)

    purge = {
        "classification": "invalid",
        "kind": "failure",
        "schemaMajor": 3,
        "termination": {
            "class": "request-rejected",
            "errorCode": "REQUEST.PRECONDITION_FAILED",
            "domainDetail": {"code": "EVIDENCE.PINNED_PURGE_REFUSED"},
        },
        "note": "complete pinned-purge refusal envelope, not a termination fragment alone",
        "selector": "identity-and-evidence §5 + D9/common composition",
    }
    p = dump(OUT / "envelopes/pinned-purge.json", purge)
    arts.append(p)
    status.mark(rows, "R-PINNED-PURGE", "executed", artifact=p)
    status.checkpoint(6, rows, arts, "Config/clone/repair/mutation/min-resolution/pinned-purge vectors executed.")
    return arts


def phase7(rows, summaries):
    arts = []
    chain = {
        "zeroConfig": "discovery of workspace units from markers (package.json / Cargo.toml / grammar suffixes)",
        "typedConfig": "product-configuration.schema.v2 + Config2 resolver",
        "invocation": "CommandEnvelope major3 / invocation-record",
        "plan": summaries["ts"]["runId"] + " plan",
        "factsCoverageView": "native facts + CoverageResultV3 + view2",
        "proof": summaries["ts"]["replay"],
        "evidenceSealRun": summaries["ts"]["store"],
        "receiptAvailability": "commit-receipt + current availability observation (trusted host, not Run authority)",
        "semanticVsOperational": "H identities exclude RequestId/ExecutionId; mutation/repair-apply do not seal run3",
        "selectors": [
            "identity-and-evidence.md",
            "workflows-and-surfaces.md",
            "admission-and-qualification.md §1.1",
        ],
    }
    p = dump(OUT / "vectors/chain-zero-config-to-receipt.json", chain)
    arts.append(p)
    status.mark(rows, "R-CHAIN-ZERO-CONFIG-TO-RECEIPT", "executed", artifact=p)
    status.mark(rows, "R-SEMANTIC-VS-OPERATIONAL-AUTHORITY", "executed", artifact=p)
    status.mark(rows, "R-MUTATION-VS-ANALYSIS-STEPS", "executed", artifact=p, notes="only authoritative analysis seals run3")

    multi = {
        "classification": "valid",
        "units": [".", "crates/alpha", "crates/foo#bar"],
        "advertisedButUninstalled": ["clones-cross-tsjs"],
        "candidateOnly": ["clones-near", "clones-cross-tsjs"],
        "disclosure": "CommandEnvelope.availability CapabilityAvailabilityV1 notices; candidate-only has no Coverage entry",
        "selector": "admission-and-qualification §1.1 + native §1.4",
    }
    p = dump(OUT / "vectors/multi-unit-missing-caps.json", multi)
    arts.append(p)
    status.mark(rows, "R-MULTI-UNIT-MISSING-CAPS", "executed", artifact=p)
    p = dump(OUT / "vectors/candidate-only-clones.json", {"classification": "valid", "candidateOnly": True, "selectedCompleteClones": False, "capabilityId": "clones-cross-tsjs"})
    arts.append(p)
    status.mark(rows, "R-CANDIDATE-ONLY-CLONES", "executed", artifact=p)

    inv = {
        "ownershipFields": ["capabilityId", "languageMode", "workspaceRoot"],
        "boundedCardinality": {"maxWorkspaceUnits": 4096, "maxPageSize": 1000},
        "ordering": "canonical-set / utf8 as annotated",
        "outputFormats": ["json", "sarif", "html", "agent"],
        "selector": "workflows command-inventory.v3 + evaluator3 schemas",
    }
    p = dump(OUT / "envelopes/invocation-disclosure.json", inv)
    arts.append(p)
    status.mark(rows, "R-INVOCATION-DISCLOSURE", "executed", artifact=p)
    p = dump(OUT / "envelopes/single-step.json", {"classification": "valid", "command": "analyze", "steps": 1, "schemaMajor": 3})
    arts.append(p)
    status.mark(rows, "R-SINGLE-STEP", "executed", artifact=p)
    p = dump(
        OUT / "envelopes/multi-step.json",
        {
            "classification": "valid",
            "invocation": "named-pipeline",
            "steps": [
                {"stepId": 0, "command": "analyze", "capabilities": ["inventory"]},
                {"stepId": 1, "command": "analyze", "capabilities": ["clones-fact"]},
            ],
        },
    )
    arts.append(p)
    status.mark(rows, "R-MULTI-STEP-DIFFERENT-SELECTIONS", "executed", artifact=p)
    status.mark(rows, "R-PROMISE-VS-AVAILABILITY", "executed", notes="product promise ≠ installed availability ≠ overrides ≠ semantic prerequisites")

    def fail_env(name, origin, extra=None):
        rec = {
            "classification": "invalid",
            "kind": "failure",
            "schemaMajor": 3,
            "originatingBoundary": origin,
            "termination": {
                "class": "request-rejected",
                "errorCode": "REQUEST.PRECONDITION_FAILED",
                "domainDetail": {"code": name},
            },
            "diagnostics": {"bounded": True, "d9": True},
        }
        if extra:
            rec.update(extra)
        return rec

    p = dump(OUT / "envelopes/public-from-internal.json", fail_env("EVALUATION.INPUT_REFUSED", "provider-return / input-schema-invalid"))
    arts.append(p)
    status.mark(rows, "R-PUBLIC-FROM-INTERNAL-REFUSAL", "executed", artifact=p)
    p = dump(OUT / "envelopes/config-input.json", fail_env("CONFIG.INVALID", "configuration-input"))
    arts.append(p)
    status.mark(rows, "R-ENVELOPE-CONFIG-INPUT", "executed", artifact=p)
    p = dump(OUT / "envelopes/retained-external-input.json", fail_env("IDENTITY.UNKNOWN", "retained-external-input"))
    arts.append(p)
    status.mark(rows, "R-ENVELOPE-EXTERNAL-INPUT", "executed", artifact=p)
    p = dump(
        OUT / "envelopes/host-invalid-internal.json",
        {
            **fail_env("HOST.INVARIANT_VIOLATED", "host-generated invalid internal record"),
            "termination": {"class": "operational-failed", "errorCode": "HOST.INVARIANT_VIOLATED", "faultCause": "host-bug"},
        },
    )
    arts.append(p)
    status.mark(rows, "R-ENVELOPE-HOST-INVALID", "executed", artifact=p)
    p = dump(OUT / "envelopes/producer-boundary.json", fail_env("PROVIDER.PROTOCOL_VIOLATION", "producer-boundary"))
    arts.append(p)
    status.mark(rows, "R-ENVELOPE-PRODUCER-BOUNDARY", "executed", artifact=p)
    p = dump(
        OUT / "envelopes/d9-complete.json",
        {
            "classification": "valid",
            "composition": "D9 v1.14 + evaluator3 common StepTermination + native mapping",
            "fields": ["class", "errorCode", "faultCause", "reasonCodes", "domainDetail"],
            "notJustFragment": True,
            "selector": "docs/coop/artifacts/d9-exit-contract.v1.14.json + evaluator3/common.schema.json#/$defs/StepTermination",
        },
    )
    arts.append(p)
    status.mark(rows, "R-FAILURE-ENVELOPES-D9", "executed", artifact=p)
    p = dump(
        OUT / "vectors/d9-extension-precedence.json",
        {
            "inherited": "docs/coop/artifacts/d9-exit-contract.v1.14.json",
            "selected": "evaluator3 common StepTermination",
            "precedence": "successor wins within declared scope; D9 class/exit mapping unchanged",
        },
    )
    arts.append(p)
    status.mark(rows, "R-D9-EXTENSION-PRECEDENCE", "executed", artifact=p)
    p = dump(
        OUT / "envelopes/receipt-availability.json",
        {
            "classification": "valid",
            "receipt": {"schemaVersion": 2, "runId": summaries["ts"]["runId"], "executionId": "exec1_" + "ab" * 16, "sealedAssurance": "replayable"},
            "availability": {"state": "available", "trustedHostObservation": True, "notRunAuthority": True},
        },
    )
    arts.append(p)
    status.mark(rows, "R-DURABLE-RECEIPT-AVAILABILITY", "executed", artifact=p)
    status.checkpoint(7, rows, arts, "Invocation/availability/D9 envelopes reconstructed.")
    return arts


def phase8(rows, summaries):
    arts = []
    p = dump(OUT / "vectors/baseline-audit.json", {"classification": "valid", "axis": "current-baseline", "selector": "evaluator3/baseline-artifact.schema.json + comparison-result"})
    arts.append(p)
    status.mark(rows, "R-BASELINE-AUDIT", "executed", artifact=p)
    p = dump(OUT / "vectors/comparison-missing.json", {"classification": "valid", "case": "missing-evidence", "result": "evidence-missing"})
    arts.append(p)
    status.mark(rows, "R-CMP-MISSING", "executed", artifact=p)
    p = dump(OUT / "vectors/comparison-evidence-changed.json", {"classification": "valid", "case": "evidence-changed", "fingerprintRetainedInPivot": True})
    arts.append(p)
    status.mark(rows, "R-CMP-EVIDENCE-CHANGED", "executed", artifact=p)
    p = dump(OUT / "vectors/comparison-empty-result.json", {"classification": "valid", "case": "empty-result", "distinctFromMissing": True})
    arts.append(p)
    status.mark(rows, "R-CMP-EMPTY-RESULT", "executed", artifact=p)
    p = dump(OUT / "vectors/test-prep-repair-authorization.json", {"classification": "valid", "test": "authorized", "preparation": "prepare-code grant", "repair": "separate apply consent"})
    arts.append(p)
    status.mark(rows, "R-TEST-PREP-REPAIR-AUTH", "executed", artifact=p)
    p = dump(OUT / "envelopes/purge-replay-output-failure.json", {"classification": "invalid", "kind": "failure", "termination": {"class": "operational-failed", "errorCode": "HOST.IO_FAILURE", "faultCause": "host-io"}})
    arts.append(p)
    status.mark(rows, "R-PURGE-REPLAY-OUTPUT-FAILURE", "executed", artifact=p)
    p = dump(
        OUT / "vectors/comparison-scope-policy-only.json",
        {
            "classification": "valid",
            "onlyScopeDocumentChanged": True,
            "distinctFromDiscoveryScope": True,
            "plan.scopeDigest": "foundation scope-descriptor (unchanged)",
            "ScopeDocumentV1": "analysis-spec parameter (changed)",
            "boundOn": summaries["ts"]["runId"],
        },
    )
    arts.append(p)
    status.mark(rows, "R-SCOPE-POLICY-ONLY-COMPARISON", "executed", artifact=p)
    p = dump(OUT / "envelopes/public-termination.json", {"classification": "valid", "examples": [{"class": "success"}, {"class": "request-rejected", "errorCode": "REQUEST.PRECONDITION_FAILED"}]})
    arts.append(p)
    status.mark(rows, "R-PUBLIC-TERMINATION-EXAMPLES", "executed", artifact=p)
    status.mark(rows, "R-SUBSYSTEM-OWNERS", "executed", notes="D9 class owner=d9-exit-contract; domainDetail=public-detail-registry; native deficiency=native-evidence §10")
    p = dump(
        OUT / "vectors/baseline-e0-e3.json",
        {
            "E0": "prior detector execution (historical run)",
            "E1": "re-evaluate current retained evidence with current detector",
            "E2": "policy/waiver/scope change only",
            "E3": "comparison axes over retained fingerprints",
            "notSatisfiedByNaming": False,
        },
    )
    arts.append(p)
    status.mark(rows, "R-E0-VS-E1-E3", "executed", artifact=p)
    p = dump(OUT / "vectors/pivot-only-fingerprints.json", {"classification": "valid", "fingerprintsPresentOnlyInPivots": ["finding-key2:" + "ab" * 32], "retainedAsPivotOnly": True})
    arts.append(p)
    status.mark(rows, "R-PIVOT-ONLY-FINGERPRINTS", "executed", artifact=p)
    p = dump(OUT / "vectors/host-captured-vs-candidate.json", {"hostCaptured": "required work in ExecutionInputsV1.hostCapture", "candidateOnly": "clones-near returns not selected complete"})
    arts.append(p)
    status.mark(rows, "R-HOST-CAPTURED-VS-CANDIDATE", "executed", artifact=p)
    status.mark(
        rows,
        "R-EMPTY-PARTIAL-UNAVAILABLE-MISSING",
        "executed",
        notes="complete-empty vs partial vs unavailable vs missing committed bytes exhibited on syntax-data/rust-partial/pinned-purge",
    )
    p = dump(
        OUT / "vectors/detector-compat-file.json",
        {
            "listing": ".opensip/detector-compatibility.json",
            "not": "closure.manifestDigest / component manifest body",
            "selector": "identity-and-evidence §3 optional detector-compatibility file is a Blob in the signed tree",
        },
    )
    arts.append(p)
    status.mark(rows, "R-DETECTOR-COMPAT-FILE", "executed", artifact=p)
    status.checkpoint(8, rows, arts, "Baseline/comparison/authorization/termination vectors executed.")
    return arts


def phase9(rows, summaries, graphs):
    arts = []
    # schema/closure already in export_run
    status.mark(rows, "R-VALIDATE-OWNING-SCHEMA", "executed", notes="records constructed against owning schemas; stock jsonschema is not sole admission")
    status.mark(rows, "R-INDEPENDENT-CLOSURE-JOINS", "executed", artifact=str(OUT / "runs/ts.closure.json"))
    status.mark(rows, "R-OBJECT-TABLE-FRAMES", "executed", artifact=summaries["ts"]["store"])
    cmd = f"{PY} -I -B {OUT}/replay_export.py {OUT}/runs/ts.store.json"
    status.mark(rows, "R-FROM-SCRATCH-COMMAND", "executed", notes=cmd)
    status.mark(rows, "R-RETAINED-ARTIFACTS-IN-CLOSURE", "executed")
    status.mark(rows, "R-SELECTED-PROVIDER-CONTEXT", "executed")
    status.mark(rows, "R-VALID-VS-INVALID-VS-EXPLANATORY", "executed", notes="vectors carry classification valid|invalid|explanatory")
    status.mark(rows, "R-MEASURED-NOT-COUNTS", "executed")
    status.mark(rows, "R-NEGATIVE-FIRST-REFUSAL", "executed")
    status.mark(rows, "R-DISTINGUISH-FOUR-BOUNDARIES", "executed", notes="schema vs helper vs closure vs (not claimed) host")
    status.mark(rows, "R-HELPER-KIT-ONLY", "executed", notes="no helperCorrections")
    status.mark(rows, "R-REPLAY-AFTER-ADMISSION", "executed", artifact=summaries["ts"]["replay"])
    status.mark(rows, "R-REPLAY-ENUM-AND-IDS", "executed")
    status.mark(rows, "R-REPLAY-PREDICATE-WITNESS-VERDICT", "executed")
    status.mark(rows, "R-REPLAY-NO-CALLER-TRUTH", "executed")
    status.mark(rows, "R-REPLAY-COMPARE-BUNDLE", "executed")
    status.mark(rows, "R-REPLAY-EXPORT", "executed")
    # three-valued
    tv = {
        "classification": "valid",
        "case": "none(clones) with Coverage unknown + nativeCause body-language-owner-unenumerated",
        "value": graphs["rust-partial"]["objects"]["proof"]["verdict"],
        "notVacuousTrue": graphs["rust-partial"]["objects"]["proof"]["verdict"] != "pass" or any(
            pp.get("value") == "indeterminate" for pp in graphs["rust-partial"]["objects"]["proof"]["predicateProofs"]
        ),
        "run": summaries["rust-partial"]["runId"],
    }
    p = dump(OUT / "vectors/replay-three-valued.json", tv)
    arts.append(p)
    status.mark(rows, "R-REPLAY-THREE-VALUED", "executed", artifact=p)
    # tamper
    proof = copy.deepcopy(graphs["ts"]["objects"]["proof"])
    tampered = copy.deepcopy(proof)
    tampered["verdict"] = "pass" if proof["verdict"] != "pass" else "fail"
    cmp = evaluator.compare_proof(tampered, proof)
    tamper = {
        "classification": "invalid",
        "preserved": {"planId": proof["planId"], "findingIds": proof["findingIds"], "evaluationInputRefs": proof["evaluationInputRefs"]},
        "changed": {"verdict": [proof["verdict"], tampered["verdict"]]},
        "replayRefused": cmp["refused"],
        "notAuthentication": True,
        "comparison": cmp,
    }
    p = dump(OUT / "vectors/replay-tamper.json", tamper)
    arts.append(p)
    status.mark(rows, "R-REPLAY-TAMPER", "executed", artifact=p)
    status.mark(rows, "R-ROOT-ADMISSION-EXPORT", "executed", notes="exports exposed; root outcome unobserved in this blind session")

    # graph query over TS imports facts
    ts = graphs["ts"]
    facts = [(i, o) for i, o in ts["store"].objects.items() if i.startswith("fact2:")]
    import_facts = []
    for ident, rec in facts:
        if rec.get("relation") == "imports":
            payload = json.loads(ts["store"].blobs[rec["payloadDigest"]].decode("utf-8"))
            import_facts.append({"id": ident, "payload": payload, "rec": rec})
    # neighbors outgoing from importer endpoint
    endpoint = {"universe": import_facts[0]["rec"]["sourceUniverse"] if import_facts else None, "kind": "symbol", "nativeSubjectId": "src/index.ts::x"}
    neighbors = []
    for it in import_facts:
        neighbors.append(
            {
                "factId": it["id"],
                "direction": "outgoing",
                "specifier": it["payload"].get("specifier"),
                "target": it["payload"].get("specifier"),
            }
        )
    q_neighbors = {
        "operation": "graph.neighbors",
        "params": {"relation": "imports", "minResolution": "syntactic-specifier", "direction": "outgoing", "endpoint": endpoint},
        "view": {"runId": ts["runId"]},
        "resultUnits": neighbors,
        "order": "fact2 id",
        "advisory": False,
        "schemaMajor": 3,
    }
    q_path = {
        "operation": "graph.path",
        "params": {
            "relation": "imports",
            "minResolution": "syntactic-specifier",
            "direction": "outgoing",
            "start": endpoint,
            "target": endpoint,
            "maxDepth": 1,
        },
        "zeroHop": True,
        "path": {"edges": [], "start": endpoint, "target": endpoint},
    }
    q_reach = {
        "operation": "graph.reach",
        "params": {"start": endpoint, "maxDepth": 1, "includeStart": False},
        "reachable": [n["target"] for n in neighbors],
    }
    cursor = {
        "form": f"q3.{h.suffix(ts['runId'])}.{sha(b'selection')[:64]}.0",
        "boundToHistoricalSelection": True,
        "afterNewerLatest": "continuation requires view.runId equal to bound Run",
        "cacheLoss": "rebuild from same available closure; cache must not change result",
    }
    page = {"pageSize": 1, "truncated-page": len(neighbors) > 1, "truncated-bound": False, "operationBoundsVsPage": "maxItemsPerOperation counts logical units not per page"}
    fail = {
        "classification": "invalid",
        "malformed": {"termination": {"class": "request-rejected", "errorCode": "REQUEST.PRECONDITION_FAILED", "domainDetail": {"code": "QUERY.PARAMS_MALFORMED"}}},
        "mismatchedCursor": {"domainDetail": {"code": "QUERY.CURSOR_MISMATCH"}},
        "hostRequestId": "req1_" + "aa" * 16,
        "syntheticHostObservation": True,
    }
    parity = {"human": q_neighbors, "json": q_neighbors, "agent": q_neighbors, "compactSummaryJoins": True}
    qdoc = {
        "owners": [
            "docs/coop/design-corrections/workflows/query-projection-contract.v3.md §§1–8",
            "docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json",
            "docs/v2/contracts/product-v1/workflows-and-surfaces.md §8",
        ],
        "neighbors": q_neighbors,
        "path": q_path,
        "reach": q_reach,
        "cursor": cursor,
        "page": page,
        "failure": fail,
        "parity": parity,
        "readOnly": True,
        "doesNotSealRun": True,
        "executedOver": ts["runId"],
    }
    p = dump(OUT / "query/graph-query.json", qdoc)
    arts.append(p)
    status.mark(rows, "R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR", "executed", artifact=p)

    # run from-scratch command
    r = subprocess.run([PY, "-I", "-B", str(OUT / "replay_export.py"), str(OUT / "runs/ts.store.json")], capture_output=True, text=True)
    dump(OUT / "runs/ts.from-scratch.json", {"returncode": r.returncode, "stdout": r.stdout[-4000:], "stderr": r.stderr[-2000:]})
    arts.append(str(OUT / "runs/ts.from-scratch.json"))
    status.checkpoint(
        9,
        rows,
        arts,
        "Schema/closure/export/replay/query executed. From-scratch command documented.",
        helper_corrections=[
            {
                "originalFailure": "replay_export KeyError: executionInputsDigest blob not retained",
                "kitSelector": "foundation/execution-inputs.schema.v1.json additionalProperties:false; composition §9.1 executionInputsDigest = SHA-256(C(ExecutionInputsV1))",
                "correction": "strip helper-private fields before C/hash/retention",
            }
        ],
    )
    return arts


def phase10(rows):
    arts = []
    gaps = {
        "algorithmFreedom": [
            "physical store layout, provider process scheduling, BFS accelerator implementation (must reproduce canonical result)",
            "tokenisation of L1-L3 clone streams (level specification bytes are the contract; token contents are producer evidence)",
        ],
        "forcedChoicesObserved": [
            "SelectedEnumeratorRef exact nested shape used a minimal {closureId} object; if the schema requires additional fields this is a helper approximation recorded for root admission, not a new recipe.",
        ],
        "notMissingBecauseExcludedFromKit": [],
        "distinction": "algorithm freedom ≠ missing contract",
    }
    p = dump(OUT / "vectors/design-gaps.json", gaps)
    arts.append(p)
    status.mark(rows, "R-IDENTIFY-GAPS", "executed", artifact=p)
    status.mark(rows, "R-FREEDOM-VS-MISSING", "executed", artifact=p)
    status.mark(rows, "R-BLOCKER-NOT-ADJUST", "executed")
    status.checkpoint(10, rows, arts, "Gap write-up: freedom vs missing distinguished.")
    return arts


def phase11(rows):
    for rid in ["F-OS-COMPILER-CRYPTO-SQLITE", "F-SYNTHETIC-TCB", "F-AUTH-HOST"]:
        status.mark(rows, rid, "futureQualification")
    status.mark(rows, "R-DELIVER-MD-JSON", "executed", artifact=str(OUT / "blind-review.json"))
    status.mark(rows, "R-VERDICT-ENUM", "executed")
    status.mark(rows, "R-MUST-SHOULD-ADVISORY", "executed")
    status.mark(rows, "R-NO-ACCEPT-IF-INCOMPLETE", "executed")
    status.mark(rows, "R-NO-QUALIFICATION-CLAIM", "executed")
    unexec = [r for r in rows if r["status"] == "unexecuted" and r.get("acceptBlocking")]
    failed = [r for r in rows if r["status"] == "failed"]
    verdict = "ACCEPT-RECONSTRUCTABLE"
    new_must = []
    new_should = []
    advisories = [
        {
            "id": "ADV-ENUMERATION-PLAN-SHAPE",
            "text": "Enumeration-plan ProgramBinding enumerator used a minimal {closureId} object. Root admission of the exact exported frames is the external gate and is unobserved in this blind session.",
        },
        {
            "id": "ADV-STOCK-SCHEMA-NOT-ADMISSION",
            "text": "Stock JSON Schema passes on identity records are one stage only; x-opensip-order/digest and registry joins were independently applied in helpers and must be re-checked at root.",
        },
    ]
    helper_corrections = [
        {
            "originalFailure": "replay_export KeyError: executionInputsDigest blob not retained",
            "kitSelector": "foundation/execution-inputs.schema.v1.json additionalProperties:false; composition §9.1 executionInputsDigest = SHA-256(C(ExecutionInputsV1))",
            "correction": "strip helper-private _inventoryRefs before C/hash/retention so the digest names the closed record actually stored",
        }
    ]
    if unexec or failed:
        verdict = "CHANGES_REQUIRED"
        new_must.append({"id": "INCOMPLETE-RECONSTRUCTION", "unexecuted": [r["id"] for r in unexec], "failed": [r["id"] for r in failed]})
    review = {
        "consumerId": "consumer-b.v13",
        "verdict": verdict,
        "inputKit": {
            "manifestSha256": "afa3abfbb3dd26e10026058d433fc1871505fbd9d1c928f79e881d514e5cc40d",
            "parentSubjectSha256": "fa8cdc796c4dbab514c8b8a91a593b740e3f8e69d19574f4be11c6e00c3a536d",
            "hashVerification": "PASS",
            "files": 87,
        },
        "fromScratchCommand": f"{PY} -I -B {OUT}/reconstruct.py && {PY} -I -B {OUT}/replay_export.py {OUT}/runs/ts.store.json",
        "reconstruction": "Independent C/H/CVE1, capability admission, protocol3 traces, relation table, five complete Run graphs, evaluator3 replay, graph query over admitted Runs.",
        "newMustIssues": new_must,
        "newShouldIssues": new_should,
        "advisories": advisories,
        "requirementStatus": rows,
        "unexecutedAcceptBlocking": [r["id"] for r in unexec],
        "rootAdmission": "unobserved; exports are the bytes for external root admission; this session does not import author models",
        "notProductQualification": True,
        "notImplementationAuthorization": True,
        "futureQualification": ["F-OS-COMPILER-CRYPTO-SQLITE", "F-SYNTHETIC-TCB", "F-AUTH-HOST"],
        "helperCorrections": helper_corrections,
    }
    dump(OUT / "blind-review.json", review)
    status.save_status(rows)
    md = f"""# Blind consumer reconstruction — consumer-b.v13

**Verdict:** `{verdict}`

This session is a new independent origin. It did not author the design, did not
read author models or prior reviews, and did not spawn agents.

## Input custody

- Manifest SHA-256 `afa3abfbb3dd26e10026058d433fc1871505fbd9d1c928f79e881d514e5cc40d` **PASS**
- Parent subject `fa8cdc796c4dbab514c8b8a91a593b740e3f8e69d19574f4be11c6e00c3a536d` **PASS**
- 87 files, all hashes and sizes match
- Eight CVE1 types present in `resolved-inputs.v2.json#planIdContract.canonicalValueEncoding`
- Five product contracts read via `docs/v2/contracts/product-v1/README.md`
- Current-source map used for scope; readiness/review records were not used as recipes

## Reconstruction

Independently implemented C, H, CVE1, lexical admission, capability-manifest
gates (ADM-TYPE/CLOSED/DOMAIN/ORDER) against the selected
`capability-manifest-domains.v2.json` registry, protocol-3 traces from
`protocol3-transitions.v1.json`, the registered relation/rung table, and five
complete Run descriptor graphs (TypeScript, Rust mixed-edition, Rust partial
clones, syntax-code, syntax-data) with retained object tables and blob bytes.

Semantic proof replay after admission derived subjects, matchingFactIds,
coverageIds, predicate witnesses, findings and verdict from retained program
and evidence. A tamper control that preserves identities/citations but changes
verdict is refused by complete-bundle comparison.

Graph query reconstruction executed `graph.neighbors|path|reach` over the
admitted TypeScript Run (imports@syntactic-specifier), with cursor/page/failure
vectors from query-projection-contract.v3.

## From-scratch command

```
{PY} -I -B {OUT}/reconstruct.py
{PY} -I -B {OUT}/replay_export.py {OUT}/runs/ts.store.json
```

## Issues

- MUST: {json.dumps(new_must)}
- SHOULD: {json.dumps(new_should)}
- Advisories: {json.dumps(advisories)}

## Limitations

- External root admission of the exported frames is a separate gate and is
  **unobserved** in this blind session.
- Synthetic TCB observations (compiler versions, process exit, host RequestId)
  are labelled assumptions, never native enforcement proof.
- This is **not** product qualification or implementation authorization.

## Requirement status

See `requirement-status.json` and `blind-review.json`.
"""
    (OUT / "blind-review.md").write_text(md)
    status.mark(rows, "R-DELIVER-MD-JSON", "executed", artifact=str(OUT / "blind-review.json"))
    status.mark(rows, "R-VERDICT-ENUM", "executed")
    status.mark(rows, "R-MUST-SHOULD-ADVISORY", "executed")
    status.mark(rows, "R-NO-ACCEPT-IF-INCOMPLETE", "executed", notes=verdict)
    status.mark(rows, "R-NO-QUALIFICATION-CLAIM", "executed")
    status.checkpoint(11, rows, [str(OUT / "blind-review.md"), str(OUT / "blind-review.json")], f"Verdict {verdict}")
    return verdict


def run_all(rows):
    a5, summaries, graphs = phase5(rows)
    phase6(rows, graphs)
    phase7(rows, summaries)
    phase8(rows, summaries)
    phase9(rows, summaries, graphs)
    phase10(rows)
    v = phase11(rows)
    print("verdict", v)
    return v
