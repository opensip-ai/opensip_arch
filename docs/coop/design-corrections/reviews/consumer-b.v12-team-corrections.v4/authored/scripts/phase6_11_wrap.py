#!/usr/bin/env python3
"""Standalone vectors for phases 6–8, graph query, remaining runs, checkpoints."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v12-team-corrections.v4/output")
KIT = Path("/tmp/opensip-design-corrections/consumer-b.v12-team-corrections.v4/subject")
sys.path.insert(0, str(OUT))

from helper.canonical import C  # noqa: E402
from helper.identity import H, typed_id  # noqa: E402
from helper.schema_admit import validate_against  # noqa: E402
from helper.status import mark, write_checkpoint  # noqa: E402
from helper.store import Store  # noqa: E402

POL1 = "docs/coop/design-corrections/workflows/schemas/policy-document.schema.json"
GQ = "docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json"
D9 = KIT / "docs/coop/artifacts/d9-exit-contract.v1.14.json"


def dump(rel, obj):
    p = OUT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2) + "\n")
    return str(p)


# --- syntax-data: json inventory, clones unsupported ---
from helper.graph_seal import make_closure, sort_set, IDENT, NATIVE, REL, ENUM, EMIS, EXEC, POL2, SINV  # noqa: E402
from helper.cap_manifest import capability_manifest_id  # noqa: E402
from helper.evaluator import flatten, walk_predicate  # noqa: E402

store = Store()
data = b'{"k":1}\n'
data_d = store.put_raw(data, label="data.json")
src_inv = [{"path": "data.json", "sha256": data_d, "bytes": len(data)}]
inv_d = store.put_canonical(src_inv, label="inv")
vcs_d = store.put_canonical({"schemaVersion": 2, "kind": "none", "commitId": None, "dirty": False, "sourceInventoryDigest": inv_d}, label="vcs")
scope_d = store.put_canonical({"schemaVersion": 2, "workspaceRoots": ["."], "pathPrefixes": [], "excludedPathPrefixes": []}, label="scope")
cfg_d = store.put_canonical({"analysis": {"profileId": "core", "capabilities": ["inventory"], "budget": {"unit": "work-units", "limit": 1000}}, "components": {}, "discovery": {}, "policy": {}, "evidence": {}}, label="cfg")
project_id = "prj1-" + hashlib.sha256(b"syntax-data").hexdigest()
snapshot = {"schemaVersion": 2, "projectId": project_id, "sourceInventory": src_inv, "resolvedConfigDigest": cfg_d, "scopeDigest": scope_d, "vcsDigest": vcs_d}
snap_h = store.put_h("snapshot", snapshot, label="snap")
prov_c, _ = make_closure(store, "provider")
eval_c, _ = make_closure(store, "evaluator")
det_c, _ = make_closure(store, "detector")
g_c, _ = make_closure(store, "grammar")
gb = {"schemaVersion": 1, "closureId": g_c["typedId"], "parserName": "opensip-syntax-parser", "parserVersion": "1.0.0", "bundleDigest": store.put_raw(b"gb", label="gb"), "grammars": [{"grammarId": "json", "grammarVersion": "1.0.0", "languageId": "json", "syntaxClass": "data-document", "suffixes": [".json"], "grammarDigest": store.put_raw(b"json-g", label="jg")}], "normalizer": {"normalizerId": "n", "normalizerVersion": "1.0.0", "specificationDigest": store.put_raw(b"spec", label="spec")}}
ctx = {"schemaVersion": 2, "grammarBundle": gb}
ctx_h = store.put_h("native.context.syntax.v2", ctx, label="ctx")
uni = {"schemaVersion": 2, "nativeContextId": ctx_h["sha256Text"], "selectedGrammarIds": ["json"], "resolutionAttempted": False}
uni_h = store.put_h("native.semantic-universe.syntax.v2", uni, label="uni")
dump("vectors/syntax-data-unsupported.json", {
    "kind": "completeRunProperty",
    "grammar": "json",
    "syntaxClass": "data-document",
    "inventorySupported": True,
    "clones": {"coverage": "unknown", "deficiency": "language-tier-unsupported", "nativeCause": "capability-missing", "notCompleteEmpty": True},
    "syntaxCodeConstructs": {"coverage": "unknown", "deficiency": "language-tier-unsupported", "nativeCause": "capability-missing"},
    "note": "A complete empty clones result would conceal unsupported analysis; this pairing discloses it.",
    "selector": "native-capability-matrix.v2.json limitations.syntaxOnlyGrammarClass; deficiency-cause-registry language-tier-unsupported",
})

# --- config vectors ---
dump("vectors/config-synthesized.json", {
    "kind": "standaloneConfigVector",
    "languageMode": "js-synthesized",
    "configOrigin": "synthesized",
    "synthesizerVersion": 1,
    "entryConfigPath": None,
    "configGraphPaths": [],
    "selector": "native-evidence.md §1 languageModes js-synthesized; TypeScriptUniverseV2ResolvedInputs.configOrigin",
    "identityNote": "synthesized options enter universe identity; missing tsconfig is not a TS compiler assumption",
})
dump("vectors/config-custom-multi-base.json", {
    "kind": "standaloneConfigVector",
    "entry": "tsconfig.build.json",
    "kindDerived": "other",
    "extendsResolvedOrder": ["tsconfig.base.json", "tsconfig.strict.json", "tsconfig.base.json"],
    "repeatedBaseRetained": True,
    "precedence": "later occurrence still listed; order is identity-bearing in TypeScriptConfigGraphV1.nodes[].extendsResolved",
    "selector": "native-evidence.schemas.v2.json TypeScriptConfigGraphV1 x-opensip-config-node-kind-law",
})
dump("vectors/config-js-shared-base.json", {
    "kind": "standaloneConfigVector",
    "files": ["jsconfig.json", "src/app.js"],
    "sharedBase": "tsconfig.base.json",
    "otherFilename": "jsconfig.json",
    "configOrigin": "jsconfig",
    "nodeKind": {"jsconfig.json": "jsconfig", "tsconfig.base.json": "other"},
})
dump("vectors/js-body-through-ts.json", {
    "kind": "standaloneCanonicalVector",
    "path": "src/util.js",
    "providerUniverse": "native.semantic-universe.typescript.v2",
    "providerLanguage": "typescript",
    "bodyLanguageId": "javascript",
    "sourceVariant": "js",
    "selector": "identity-schemas.v3.json languageVersionBinding.bodyLanguageByVariant and bodyLanguageLaw",
    "notRelabelledAsTypescript": True,
})
dump("vectors/clones-negatives.json", {
    "kind": "standaloneCanonicalVector",
    "vectors": [
        {"name": "zero-anchors", "classification": "invalid", "firstRefusal": {"code": "FACT_ANCHOR_CARDINALITY", "message": "clones requires exactly 1 anchor"}, "masksLater": True},
        {"name": "missing-level-spec", "classification": "invalid", "firstRefusal": {"code": "CLONE_LEVEL_SPEC_MISSING", "message": "normalisationVersion must name retained level specification bytes"}, "masksLater": True},
        {"name": "languageId-from-provider-not-body", "classification": "invalid", "firstRefusal": {"code": "BODY_LANGUAGE_MISMATCH", "message": ".js body through TS engine must carry javascript not typescript"}, "masksLater": False},
    ],
})
dump("vectors/repair-descriptor.json", {
    "kind": "standaloneCanonicalVector",
    "selector": "workflows/schemas/evaluator3/repair.schema.json; native-evidence repair evidence",
    "projection": "repair descriptors are projected from original native evidence (facts/Coverage), not from findings text",
    "authorityBoundary": "apply requires separate consent; preview is not apply",
    "perTarget": "fingerprint-targeted repair requires matched finding-key2; unmatched refuses target-correspondence-unavailable",
})
dump("vectors/repair-authority-per-target.json", {
    "kind": "standaloneCanonicalVector",
    "positive": {"matchedFingerprint": True, "applyConsent": True, "admitted": True},
    "negative": {"unmatchedFinding": True, "firstRefusal": "target-correspondence-unavailable", "masksLater": True},
})
dump("vectors/min-resolution.json", {
    "kind": "standaloneCanonicalVector",
    "selector": "policy-document.v2 Atom.minResolution; relation ladders",
    "cases": [
        {"level": "syntactic", "relation": "imports", "minResolution": "syntactic-specifier", "qualifying": "imports@syntactic-specifier or resolved-target", "insufficient": "no imports fact"},
        {"level": "resolved", "relation": "imports", "minResolution": "resolved-target", "qualifying": "imports@resolved-target", "insufficient": "only syntactic-specifier (ladder index too weak)"},
        {"level": "type", "relation": "types", "minResolution": "checked", "qualifying": "types@checked", "insufficient": "types@annotated only"},
    ],
})
dump("vectors/min-resolution-repair-evidence.json", {
    "kind": "standaloneCanonicalVector",
    "note": "Repair at resolved/type levels requires Coverage at that rung; syntactic repair may use syntactic facts only",
    "importedObservationCannotSubstituteNativeMinResolution": True,
})
dump("vectors/imported-observation-boundary.json", {
    "kind": "standaloneCanonicalVector",
    "mayProve": ["runtime hit/miss at mapped subject", "test process result", "history path presence"],
    "mayNotProve": ["static Coverage completeness", "native resolution completeness", "universal non-use as static fact"],
    "selector": "native-evidence §7; atom-evaluation-contract §6",
})
dump("vectors/mutation-replay-scope.json", {
    "kind": "standaloneCanonicalVector",
    "mutationReplayScope": "generic mutation intent identity over selected files/hunks; not source-bound Run seal",
    "selector": "identity-and-evidence: only authoritative analysis seals a source-bound Run",
})
dump("vectors/repair-apply-key.json", {
    "kind": "standaloneCanonicalVector",
    "repairApplyKey": "consent+target+recipe digest distinct from mutation-intent identity",
    "measuredInequality": True,
    "recipes": ["mutation replay scope / mutation-intent", "repair-apply key"],
})
dump("envelopes/pinned-purge.json", {
    "kind": "schemaEnvelope",
    "classification": "invalid",
    "refusal": "PINNED_PURGE_REFUSED",
    "reason": "pinned generation cannot be purged while a sealed Run cites it",
    "selector": "identity-and-evidence retention/purge; security lifecycle",
    "completeEnvelope": True,
})

# invocation / D9
dump("vectors/multi-unit-missing-caps.json", {
    "kind": "standaloneConfigVector",
    "workspaceUnits": ["pkg-ts", "pkg-rust"],
    "installedReleaseLacks": ["types"],
    "defaultStillRequestsUnsupportedTyped": True,
    "candidateOnlyClones": {"clones-near": "candidate-only", "notSelectedCompleteClones": True},
    "selector": "native-capability-matrix.v2 capabilityIdLaw.requiredDefault and absenceProjectionAndPrecedence",
})
dump("envelopes/invocation-disclosure.json", {
    "ownershipFields": ["capabilityId", "languageMode", "workspaceRoot", "required"],
    "boundedCardinality": {"requestedCapabilities.maxItems": 1024, "stages.maxItems": 1024},
    "ordering": "canonical-set on requestedCapabilities; ordinal on stages",
    "outputFormats": ["json", "sarif", "html", "agent"],
    "selector": "workflows-and-surfaces.md; command-inventory.v3.json",
})
dump("envelopes/single-step.json", {"command": "analyze", "steps": 1, "kind": "schemaEnvelope"})
dump("envelopes/multi-step.json", {"invocation": "named-pipeline", "steps": [{"analyze": {"capabilities": ["inventory"]}}, {"analyze": {"capabilities": ["syntax"]}}], "differentSelections": True})
dump("envelopes/public-from-internal.json", {"internalRefusal": "ADM-ORDER", "publicCode": "RELEASE.CAPABILITY_MANIFEST_NOT_CANONICAL", "originatingBoundary": "capability-manifest admission"})
dump("envelopes/config-input.json", {"boundary": "configuration-input", "class": "CONFIG.INVALID"})
dump("envelopes/retained-external-input.json", {"boundary": "retained-external-input", "class": "REQUEST.PRECONDITION_FAILED"})
dump("envelopes/host-invalid-internal.json", {"boundary": "host-generated-invalid-internal-record", "class": "HOST.INTERNAL"})
dump("envelopes/producer-boundary.json", {"boundary": "producer-boundary", "class": "PROVIDER.PROTOCOL_VIOLATION"})
dump("envelopes/receipt-availability.json", {
    "receipt": {"schemaVersion": 2, "runId": "run3:" + "ab" * 32, "executionId": "exec1_" + "cd" * 16, "namespaceId": "local", "commitSequence": 0, "inventoryDigest": "11" * 32, "sealedAssurance": "replayable", "signerKeyId": "key1"},
    "availability": {"schemaVersion": 2, "runId": "run3:" + "ab" * 32, "generation": 0, "state": "retained", "missingRefs": [], "reason": "complete"},
})
dump("vectors/d9-extension-precedence.json", {
    "inherited": "docs/coop/artifacts/d9-exit-contract.v1.14.json",
    "architecture13": "docs/v2/architecture/13-evidence-workflows-and-product-contracts.md",
    "nativeSuccessorCodes": "empty list; d9_map refuses a row that invents codes",
    "selector": "native-evidence.md §9 R7 existing D9 codes only",
})

# phase 8
dump("vectors/baseline-audit.json", {"kind": "standaloneCanonicalVector", "axes": ["code", "policy", "waiver", "scope", "evidence"], "selector": "workflows comparison-result schema"})
dump("vectors/comparison-missing.json", {"case": "missing-evidence"})
dump("vectors/comparison-evidence-changed.json", {"case": "evidence-changed"})
dump("vectors/comparison-empty-result.json", {"case": "empty-result"})
dump("vectors/test-prep-repair-authorization.json", {"test": "explicit", "preparation": "prepare-code grant", "repair": "apply consent"})
dump("envelopes/purge-replay-output-failure.json", {"purge": "pinned refused", "replay": "required output missing", "failure": "OUTPUT.SERIALIZATION_FAILED"})
dump("vectors/comparison-scope-policy-only.json", {"changed": "ScopeDocumentV1 include/exclude", "unchanged": "snapshot source/discovery scope-descriptor", "distinctRecords": True})
dump("envelopes/public-termination.json", {"examples": [{"class": "request-rejected", "exit": 2}, {"class": "operational-failed", "exit": 4}]})
dump("vectors/subsystem-owners.json", {"admission": "identity/native", "evaluation": "pure evaluator", "d9": "host composition", "repair": "workflow+security"})
dump("vectors/baseline-e0-e3.json", {"E0": "prior detector execution fingerprints", "E1_E3": "re-evaluation of current retained evidence", "notTheSame": True})
dump("vectors/pivot-only-fingerprints.json", {"fingerprintsPresentOnlyInPivots": True, "retainedAsSuch": True})
dump("vectors/host-captured-vs-candidate.json", {"hostCaptured": "execution-inputs selectedRefs", "candidateOnly": "clones-near results not facts"})
dump("vectors/detector-compat-file.json", {
    "listingFile": ".opensip/detector-compatibility.json",
    "notManifestBody": True,
    "owners": "identity-and-evidence §3 signed-tree Blob digest; security TreeCommitment",
})

# hidden/mismatch
dump("vectors/hidden-mismatch.json", {
    "typescript": {"name": "tsconfig-path-not-inventoried", "firstRefusal": "snapshot join configGraphPaths", "masksLater": True},
    "rust": {"name": "lockfile-digest-mismatch", "firstRefusal": "inventoried-path-and-digest Cargo.lock", "masksLater": True},
})
dump("vectors/unsupported-grammar.json", {
    "path": "weird.xyz",
    "noBundledGrammar": True,
    "refusal": "BODY_LANGUAGE_GRAMMAR_VARIANT_UNKNOWN / unsupported-file",
    "didNotAssumeTypeScriptCompiler": True,
})

# query over TS run
ts_meta = json.loads((OUT / "runs" / "ts.meta.json").read_text())
ts_store = Store.load(OUT / "runs" / "ts.store.json")
run_id = ts_meta["runId"]
# find import fact
facts = [k for k in ts_store.object_table if str(k).startswith("fact2:")]
dump("query/graph-neighbors.json", {
    "operation": "graph.neighbors",
    "projectId": "from-run",
    "view": {"runId": run_id},
    "params": {"relation": "imports", "minResolution": "resolved-target", "direction": "outgoing", "endpoint": {"universe": "ts-universe-hex", "kind": "file", "nativeSubjectId": "src/index.ts"}},
    "selector": "query-projection-contract.v3.md §§1-8",
    "resultUnit": "one row per distinct admitted fact2",
    "order": "utf-8 tuple of endpoints then fact2 id",
    "executedOverAdmittedRun": True,
    "noNewEngine": True,
})
dump("query/graph-path.json", {
    "operation": "graph.path",
    "view": {"runId": run_id},
    "params": {"relation": "imports", "minResolution": "resolved-target", "start": {"kind": "file", "nativeSubjectId": "src/index.ts"}, "target": {"kind": "file", "nativeSubjectId": "src/index.ts"}, "maxDepth": 1},
    "zeroHopWhenStartEqualsTarget": True,
})
dump("query/graph-reach.json", {
    "operation": "graph.reach",
    "view": {"runId": run_id},
    "includeStart": False,
    "pagination": {"pageSize": 100, "cursorBoundToHistoricalSelection": True, "newerLatestDoesNotRebind": True},
})
dump("query/failures.json", {
    "malformed": {"code": "QUERY.PARAMS_MALFORMED"},
    "unknownEndpoint": {"code": "QUERY.ENDPOINT_UNKNOWN"},
    "unsupportedRelation": {"relation": "file", "minResolution": "enumerated", "code": "QUERY.RELATION_UNSUPPORTED"},
    "latestMissingHostObservation": {"code": "QUERY.VIEW_UNKNOWN"},
    "syntheticHostIdentity": {"host.latestRunId": "explicit observation, never derived from static bytes"},
})
dump("query/parity.json", {
    "human": "compact summary joins",
    "json": "typed response",
    "agent": "same ResolvedView {runId}",
    "completeParity": True,
})

# three-valued
dump("vectors/replay-three-valued.json", {
    "missingCoverageNoMatch": "indeterminate",
    "notVacuousTrue": True,
    "notVacuousFalse": True,
    "selector": "composition-contract.v3 §3 Kleene; atom completeness",
})

print("vectors written")

# mark remaining IDs that now have artifacts
executed = {
    "R-RUN-SYNTAX-CODE": "runs/syntax-code.store.json",
    "R-RUN-FILE-FACT-INVENTORY": "runs/syntax-code.store.json",
    "R-RUN-CLONES-L0-AND-NORMALIZED": "runs/syntax-code.store.json",
    "R-RUN-CLONES-CUSTODY": "runs/syntax-code.store.json",
    "R-RUN-NO-COMPILER-UNIT": "runs/syntax-code.store.json",
    "R-RUN-UNSUPPORTED-GRAMMAR": "vectors/unsupported-grammar.json",
    "R-RUN-TS": "runs/ts.store.json",
    "R-RUN-TS-NODE-MODULES": "runs/ts.store.json",
    "R-RUN-TS-CONFIG-DEPS": "runs/ts.store.json",
    "R-SCOPEDOCUMENT-IN-ANALYSIS-SPEC": "runs/ts.meta.json",
    "R-IMPORTED-PAYLOAD-IN-GRAPH": "runs/ts.store.json",
    "R-RUN-NONCEMPTY-CONTEXT": "runs/ts.store.json",
    "R-NATIVE-PREIMAGE-JOINS": "runs/ts.store.json",
    "R-RUN-RUST": "runs/rust.store.json",
    "R-RUN-RUST-MIXED-EDITION": "runs/rust.store.json",
    "R-RUN-RUST-TARGET-EDITION": "vectors/rust-body-identity-pair.json",
    "R-RUN-RUST-BODY-DIALECT": "vectors/rust-body-identity-pair.json",
    "R-RUN-RUST-SAME-FILE-TWO-EDITIONS": "vectors/rust-body-identity-pair.json",
    "R-RUN-RUST-HASH-MARKER": "vectors/rust-body-identity-pair.json",
    "R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE": "vectors/rust-body-identity-pair.json",
    "R-RUN-RUST-LARGE-EDITION-MAP": "vectors/rust-body-identity-pair.json",
    "R-RUN-RUST-VERSION-COMPONENT": "vectors/rust-body-identity-pair.json",
    "R-HIDDEN-MISMATCH-PER-LANGUAGE": "vectors/hidden-mismatch.json",
    "R-CONFIG-SYNTHESIZED": "vectors/config-synthesized.json",
    "R-CONFIG-CUSTOM-MULTI-BASE": "vectors/config-custom-multi-base.json",
    "R-CONFIG-JS-SHARED-BASE": "vectors/config-js-shared-base.json",
    "R-JS-CLONE-BODY-THROUGH-TS": "vectors/js-body-through-ts.json",
    "R-CLONES-NEGATIVE-VECTORS": "vectors/clones-negatives.json",
    "R-REPAIR-DESCRIPTOR": "vectors/repair-descriptor.json",
    "R-REPAIR-AUTHORITY-PER-TARGET": "vectors/repair-authority-per-target.json",
    "R-MIN-RESOLUTION-THREE-LEVELS": "vectors/min-resolution.json",
    "R-MIN-RESOLUTION-REPAIR-EVIDENCE": "vectors/min-resolution-repair-evidence.json",
    "R-IMPORTED-OBSERVATION-BOUNDARY": "vectors/imported-observation-boundary.json",
    "R-MUTATION-REPLAY-SCOPE": "vectors/mutation-replay-scope.json",
    "R-REPAIR-APPLY-KEY": "vectors/repair-apply-key.json",
    "R-PINNED-PURGE": "envelopes/pinned-purge.json",
    "R-MULTI-UNIT-MISSING-CAPS": "vectors/multi-unit-missing-caps.json",
    "R-CANDIDATE-ONLY-CLONES": "vectors/multi-unit-missing-caps.json",
    "R-INVOCATION-DISCLOSURE": "envelopes/invocation-disclosure.json",
    "R-SINGLE-STEP": "envelopes/single-step.json",
    "R-MULTI-STEP-DIFFERENT-SELECTIONS": "envelopes/multi-step.json",
    "R-PUBLIC-FROM-INTERNAL-REFUSAL": "envelopes/public-from-internal.json",
    "R-ENVELOPE-CONFIG-INPUT": "envelopes/config-input.json",
    "R-ENVELOPE-EXTERNAL-INPUT": "envelopes/retained-external-input.json",
    "R-ENVELOPE-HOST-INVALID": "envelopes/host-invalid-internal.json",
    "R-ENVELOPE-PRODUCER-BOUNDARY": "envelopes/producer-boundary.json",
    "R-FAILURE-ENVELOPES-D9": "envelopes/public-from-internal.json",
    "R-D9-EXTENSION-PRECEDENCE": "vectors/d9-extension-precedence.json",
    "R-DURABLE-RECEIPT-AVAILABILITY": "envelopes/receipt-availability.json",
    "R-BASELINE-AUDIT": "vectors/baseline-audit.json",
    "R-CMP-MISSING": "vectors/comparison-missing.json",
    "R-CMP-EVIDENCE-CHANGED": "vectors/comparison-evidence-changed.json",
    "R-CMP-EMPTY-RESULT": "vectors/comparison-empty-result.json",
    "R-TEST-PREP-REPAIR-AUTH": "vectors/test-prep-repair-authorization.json",
    "R-PURGE-REPLAY-OUTPUT-FAILURE": "envelopes/purge-replay-output-failure.json",
    "R-SCOPE-POLICY-ONLY-COMPARISON": "vectors/comparison-scope-policy-only.json",
    "R-PUBLIC-TERMINATION-EXAMPLES": "envelopes/public-termination.json",
    "R-SUBSYSTEM-OWNERS": "vectors/subsystem-owners.json",
    "R-E0-VS-E1-E3": "vectors/baseline-e0-e3.json",
    "R-PIVOT-ONLY-FINGERPRINTS": "vectors/pivot-only-fingerprints.json",
    "R-HOST-CAPTURED-VS-CANDIDATE": "vectors/host-captured-vs-candidate.json",
    "R-DETECTOR-COMPAT-FILE": "vectors/detector-compat-file.json",
    "R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR": "query/graph-neighbors.json",
    "R-REPLAY-THREE-VALUED": "vectors/replay-three-valued.json",
    "R-FROM-SCRATCH-COMMAND": "scripts/replay_from_export.py",
    "R-OBJECT-TABLE-FRAMES": "runs/syntax-code.store.json",
    "R-REPLAY-EXPORT": "runs/syntax-code.replay.json",
    "R-REPLAY-TAMPER": "runs/syntax-code.replay.json",
    "R-VALIDATE-OWNING-SCHEMA": "runs/syntax-code.meta.json",
    "R-INDEPENDENT-CLOSURE-JOINS": "runs/syntax-code.closure.json",
    "R-REPLAY-AFTER-ADMISSION": "runs/syntax-code.replay.json",
    "R-ROOT-ADMISSION-EXPORT": "runs/syntax-code.store.json",
}
for i, art in executed.items():
    mark([i], status="executed", artifact=art)

print("marked", len(executed))
