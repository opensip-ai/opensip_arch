#!/usr/bin/env python3
"""Assemble review.json from independent classifications. Not an author oracle."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

BASE = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-scope-review.v1")
OUT = BASE / "output"
SNAP = BASE / "consumer-snapshot"
KIT = BASE / "subject"

cat = json.loads((OUT / "probes/requirement-catalog.json").read_text())
claimed = {s["id"]: s for s in json.loads((SNAP / "requirement-status.json").read_text())}

# --- classification sets ---
EXECUTED = {
    # standing of the consumer session, independently re-verified hashes
    "S-FRESH-ORIGIN",
    "S-NOT-PRODUCT",
    "S-KIT-ONLY",
    "S-MANIFEST-VERIFY",
    "S-NO-ORACLE",
    "S-MISSING-DEP-IS-CUSTODY",
    "S-PROFILE-CURRENT",
    "S-CONTINUATION",
    "R-FIVE-CONTRACTS-INDEX",
    "R-SOURCE-MAP-SCOPE",
    "R-CVE1-TYPES-AVAILABLE",
    # phase 1 measured vectors
    "R-H-HELPER",
    "R-CVE1-EIGHT-TYPES",
    "R-LEXICAL-ADMISSION",
    "R-SEMANTIC-VS-OPERATIONAL",
    "R-RAW-VS-PARSED",
    "R-ACYCLIC-JOINS",
    # phase 2
    "R-CAP-ADMISSION",
    "R-CAP-NAMED-GATES",
    # phase 3 traces
    "R-TRACE-COMPLETE",
    "R-TRACE-UNAVAILABLE",
    "R-TRACE-CANCEL",
    "R-TRACE-FAULT",
    "R-TRACE-IDENTITY-BEFORE-SOURCE",
    "R-TRACE-TERMINAL",
    "R-TRACE-EXECUTED-VS-HOST",
    # phase 4 reconstructed tables
    "R-RELATION-RUNG-TABLE",
    "R-COUNT-CLASS-ATTEMPT",
    "R-CODE-VS-DATA-MATRIX",
    "R-ENUM-VS-RESOLUTION",
    "R-ADVERTISED-MODE-PATHS",
    # Run PROPERTIES actually present in retained stores
    "R-RUN-TS-NODE-MODULES",
    "R-RUN-TS-CONFIG-DEPS",
    "R-RUN-RUST-MIXED-EDITION",
    "R-RUN-RUST-TARGET-EDITION",
    "R-RUN-RUST-BODY-DIALECT",
    "R-RUN-RUST-SAME-FILE-TWO-EDITIONS",
    "R-RUN-RUST-HASH-MARKER",
    "R-RUN-RUST-LARGE-EDITION-MAP",
    "R-RUN-RUST-VERSION-COMPONENT",
    "R-RUN-CLONES-L0-AND-NORMALIZED",
    "R-RUN-CLONES-CUSTODY",
    "R-RUN-NO-COMPILER-UNIT",
    "R-RUN-UNAVAILABLE-SEMANTIC",
    "R-RUN-NONCEMPTY-CONTEXT",
    "R-SCOPEDOCUMENT-IN-ANALYSIS-SPEC",
    "R-IMPORTED-PAYLOAD-IN-GRAPH",
    "R-NATIVE-PREIMAGE-JOINS",
    "R-EMPTY-PARTIAL-UNAVAILABLE-MISSING",
    "R-HELPER-KIT-ONLY",
    "R-FROM-SCRATCH-COMMAND",
    "R-OBJECT-TABLE-FRAMES",
    "R-DELIVER-MD-JSON",
    "R-VERDICT-ENUM",
    "R-NO-QUALIFICATION-CLAIM",
    "R-IMPORTED-OBSERVATION-BOUNDARY",
    "R-DETECTOR-COMPAT-FILE",
    "R-DURABLE-RECEIPT-AVAILABILITY",
}

# complete Runs: artifacts present; whole admission not asserted here
ARTIFACT_PRESENT_UNREVIEWED_ADMISSION = {
    "R-RUN-TS",
    "R-RUN-RUST",
    "R-RUN-RUST-PARTIAL-EMPTY-CLONES",
    "R-RUN-FILE-FACT-INVENTORY",
    "R-RUN-SYNTAX-CODE",
    "R-RUN-SYNTAX-DATA",
}

# pairing exhibited on rust-partial Coverage payload
EXECUTED |= {
    "R-CLONE-DEFICIENCY-PAIRING",
}

EXPLANATORY = {
    "R-CONFIG-SYNTHESIZED",
    "R-CONFIG-CUSTOM-MULTI-BASE",
    "R-CONFIG-JS-SHARED-BASE",
    "R-JS-CLONE-BODY-THROUGH-TS",
    "R-CLONES-NEGATIVE-VECTORS",
    "R-REPAIR-DESCRIPTOR",
    "R-REPAIR-AUTHORITY-PER-TARGET",
    "R-MIN-RESOLUTION-THREE-LEVELS",
    "R-MIN-RESOLUTION-REPAIR-EVIDENCE",
    "R-MUTATION-REPLAY-SCOPE",
    "R-REPAIR-APPLY-KEY",
    "R-PINNED-PURGE",
    "R-MULTI-UNIT-MISSING-CAPS",
    "R-CANDIDATE-ONLY-CLONES",
    "R-INVOCATION-DISCLOSURE",
    "R-SINGLE-STEP",
    "R-MULTI-STEP-DIFFERENT-SELECTIONS",
    "R-PUBLIC-FROM-INTERNAL-REFUSAL",
    "R-ENVELOPE-CONFIG-INPUT",
    "R-ENVELOPE-EXTERNAL-INPUT",
    "R-ENVELOPE-HOST-INVALID",
    "R-ENVELOPE-PRODUCER-BOUNDARY",
    "R-FAILURE-ENVELOPES-D9",
    "R-D9-EXTENSION-PRECEDENCE",
    "R-BASELINE-AUDIT",
    "R-CMP-MISSING",
    "R-CMP-EVIDENCE-CHANGED",
    "R-CMP-EMPTY-RESULT",
    "R-TEST-PREP-REPAIR-AUTH",
    "R-PURGE-REPLAY-OUTPUT-FAILURE",
    "R-SCOPE-POLICY-ONLY-COMPARISON",
    "R-PUBLIC-TERMINATION-EXAMPLES",
    "R-SUBSYSTEM-OWNERS",
    "R-E0-VS-E1-E3",
    "R-PIVOT-ONLY-FINGERPRINTS",
    "R-HOST-CAPTURED-VS-CANDIDATE",
    "R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR",
    "R-CHAIN-ZERO-CONFIG-TO-RECEIPT",
    "R-SEMANTIC-VS-OPERATIONAL-AUTHORITY",
    "R-MUTATION-VS-ANALYSIS-STEPS",
    "R-PROMISE-VS-AVAILABILITY",
    "R-HIDDEN-MISMATCH-PER-LANGUAGE",
    "R-RUN-UNSUPPORTED-GRAMMAR",
    "R-REPLAY-THREE-VALUED",
}

FAILED = {
    "R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE",
    "R-VALID-VS-INVALID-VS-EXPLANATORY",
    "R-MEASURED-NOT-COUNTS",
    "R-NEGATIVE-FIRST-REFUSAL",
    "R-NO-ACCEPT-IF-INCOMPLETE",
    "R-MUST-SHOULD-ADVISORY",
    "R-IDENTIFY-GAPS",
    "R-BLOCKER-NOT-ADJUST",
    "R-REPLAY-EXPORT",
}

# syntax-code closure/replay owned by parallel reviewer; other runs lack replay exports (failed above)
UNREVIEWED = {
    "R-VALIDATE-OWNING-SCHEMA",
    "R-INDEPENDENT-CLOSURE-JOINS",
    "R-RETAINED-ARTIFACTS-IN-CLOSURE",
    "R-SELECTED-PROVIDER-CONTEXT",
    "R-DISTINGUISH-FOUR-BOUNDARIES",
    "R-REPLAY-AFTER-ADMISSION",
    "R-REPLAY-ENUM-AND-IDS",
    "R-REPLAY-PREDICATE-WITNESS-VERDICT",
    "R-REPLAY-NO-CALLER-TRUTH",
    "R-REPLAY-COMPARE-BUNDLE",
    "R-REPLAY-TAMPER",
    "R-ROOT-ADMISSION-EXPORT",
    "R-FREEDOM-VS-MISSING",
}

FUTURE = {
    "F-OS-COMPILER-CRYPTO-SQLITE",
    "F-SYNTHETIC-TCB",
    "F-AUTH-HOST",
}

NOTES = {
    "R-H-HELPER": "Independent remint of snapshot-A C/H matched claimed hex 7ad0e60f…f556.",
    "R-CVE1-EIGHT-TYPES": "Independent remint of null/false/true/unsigned-64/negative-signed-64 encodings matched committedBytesHex. String/array/map encodings were not reminted in this probe.",
    "R-LEXICAL-ADMISSION": "Raw-byte negatives carry firstRefusal objects (duplicate-key and related).",
    "R-CAP-NAMED-GATES": "Eight named-gate vectors carry firstRefusal and masksLater.",
    "R-TRACE-EXECUTED-VS-HOST": "Per-step executedVsHost present; future-host spawn/EOF labeled separately.",
    "R-RUN-TS": "Exported store present (run3:1908c594…). Properties sampled. Whole Run admission not asserted.",
    "R-RUN-RUST": "Exported store present (run3:da14a1f0…). Properties sampled. Whole Run admission not asserted.",
    "R-RUN-SYNTAX-CODE": "Exported store+replay present (run3:aa19bedd…). Parallel reviewer owns closure/replay. Properties sampled only.",
    "R-RUN-SYNTAX-DATA": "Exported store present. clones Coverage unknown + language-tier-unsupported/capability-missing on retained cvp-clones. Whole admission not asserted.",
    "R-RUN-RUST-PARTIAL-EMPTY-CLONES": "Exported store has no clones fact2, ownership.enumeration=partial, cvp-clones coverage=unknown. clones-fact cellOutcomes incorrectly state complete (SHOULD).",
    "R-RUN-TS-NODE-MODULES": "Snapshot inventory contains node_modules/left-pad; universe nodeModulesInReadSet true.",
    "R-RUN-TS-CONFIG-DEPS": "Retained TypeScriptConfigGraphV1 (single tsconfig.json node) and ResolvedNodeModulesLayoutV1. This is not the synthesized/multi-base/js-shared standalone shapes.",
    "R-RUN-RUST-MIXED-EDITION": "Universe edition map size 17 with values {2015,2018,2021,2024}; package a=2018.",
    "R-RUN-RUST-TARGET-EDITION": "lib targetEdition null (package default 2018); bin tool targetEdition 2021.",
    "R-RUN-RUST-BODY-DIALECT": "Measured L0 2018 vs 2021 identities differ; clones payload carries 2021 L0. Dialect is in language-version preimage, not a field on the clones payload.",
    "R-RUN-RUST-SAME-FILE-TWO-EDITIONS": "Same path #/a/src/lib.rs owned by lib and bin units.",
    "R-RUN-RUST-HASH-MARKER": "Inventoried paths #/Cargo.toml, #/a/Cargo.toml, #/a/src/lib.rs.",
    "R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE": "Pair vector assigns the same l0_18 variable to both sides and sets stableWhenOnlyOwnershipChangesWithoutDialect=true. Two ownership H records exist; body identities were not independently recomputed under each selection.",
    "R-RUN-RUST-LARGE-EDITION-MAP": "Retained edition map n=17.",
    "R-RUN-RUST-VERSION-COMPONENT": "compiler_build taken from retained toolchain.rustCommitHash (synthetic deadbeef…; allowed as TCB observation).",
    "R-RUN-CLONES-L0-AND-NORMALIZED": "syntax-code retains ClonesPayloadV1-L0 (L0-verbatim) and ClonesPayloadV1-L1 (L1-lexical) with distinct body identities.",
    "R-RUN-CLONES-CUSTODY": "syntax-code retains level-spec-L1, body-language-version, languageVersion-raw32.",
    "R-RUN-NO-COMPILER-UNIT": "syntax-code H domains are native.context.syntax.v2 / native.semantic-universe.syntax.v2; selectedGrammarIds=['rust'].",
    "R-RUN-UNAVAILABLE-SEMANTIC": "syntax-data cvp-clones unknown + language-tier-unsupported/capability-missing; clones-fact cell unavailable; inventory complete.",
    "R-SCOPEDOCUMENT-IN-ANALYSIS-SPEC": "analysis-spec parameters bind payloadDigest=1184fd7d… whose blob is ScopeDocumentV1; schemaDigest equals kit policy-document.schema.json (owner of ScopeDocumentV1).",
    "R-IMPORTED-PAYLOAD-IN-GRAPH": "import2 plus RuntimePayloadV1 retained; subjects=[]. Weak but an actual imported record, not a wrapper-only sentence.",
    "R-CLONE-DEFICIENCY-PAIRING": "rust-partial cvp-clones deficiency=input-closure-incomplete nativeCause=body-language-owner-unenumerated.",
    "R-NATIVE-PREIMAGE-JOINS": "TS config graph + node_modules layout; rust dependency-source-set and cargo-config-projection retained.",
    "R-DURABLE-RECEIPT-AVAILABILITY": "Nested receipt/availability inhabit identity-schemas.v3 commit-receipt and availability (stock PASS). Wrapper is not CommandEnvelope. runId/inventoryDigest are synthetic placeholders not joined to a claimed Run.",
    "R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR": "measured-neighbors.json cites a real TS imports fact2 and discloses unprojectable-fact, but none of graph.neighbors|path|reach inhabit GraphQueryRequestV1/GraphQueryResponseV1; no GraphEvidenceDisclosure; no CommandEnvelope kind=failure; path/reach have no items; neighbors endpoint universe is 'ts-universe-hex'; parity is a literal boolean.",
    "R-CONFIG-SYNTHESIZED": "Observable requires config-graph identity/schema plus computed identity. File is languageMode/configOrigin notes; no TypeScriptConfigGraphV1; no tsconfigGraphHash.",
    "R-CONFIG-CUSTOM-MULTI-BASE": "extendsResolvedOrder listed as strings with repeatedBaseRetained:true. Not a TypeScriptConfigGraphV1 node with contentSha256 and derived kind=other for tsconfig.build.json.",
    "R-REPLAY-EXPORT": "Only runs/syntax-code.replay.json exists. ts/rust/syntax-data/rust-partial have no replay export. Requirement is every claimed positive.",
    "R-NO-ACCEPT-IF-INCOMPLETE": "Consumer verdict ACCEPT-RECONSTRUCTABLE with newMustIssues=[] while schemaEnvelope/comparison/query families are unexecuted.",
    "R-HELPER-KIT-ONLY": "Original TypeError tuple|set in protocol3 preMatchLaw preserved in checkpoints/phase-3.json and helperCorrections.",
    "R-OBJECT-TABLE-FRAMES": "All five claimed stores export objectTable+blobs. Presence only; not admission.",
}

CLAIMED_ART = {i: claimed.get(i, {}).get("artifact") for i in claimed}

# issue groupings
ENVELOPE_IDS = [
    "R-PINNED-PURGE",
    "R-INVOCATION-DISCLOSURE",
    "R-SINGLE-STEP",
    "R-MULTI-STEP-DIFFERENT-SELECTIONS",
    "R-PUBLIC-FROM-INTERNAL-REFUSAL",
    "R-ENVELOPE-CONFIG-INPUT",
    "R-ENVELOPE-EXTERNAL-INPUT",
    "R-ENVELOPE-HOST-INVALID",
    "R-ENVELOPE-PRODUCER-BOUNDARY",
    "R-FAILURE-ENVELOPES-D9",
    "R-D9-EXTENSION-PRECEDENCE",
    "R-PUBLIC-TERMINATION-EXAMPLES",
    "R-PURGE-REPLAY-OUTPUT-FAILURE",
]
CMP_IDS = [
    "R-BASELINE-AUDIT",
    "R-CMP-MISSING",
    "R-CMP-EVIDENCE-CHANGED",
    "R-CMP-EMPTY-RESULT",
    "R-SCOPE-POLICY-ONLY-COMPARISON",
    "R-E0-VS-E1-E3",
    "R-PIVOT-ONLY-FINGERPRINTS",
    "R-TEST-PREP-REPAIR-AUTH",
    "R-HOST-CAPTURED-VS-CANDIDATE",
]
CFG_IDS = [
    "R-CONFIG-SYNTHESIZED",
    "R-CONFIG-CUSTOM-MULTI-BASE",
    "R-CONFIG-JS-SHARED-BASE",
]
REPAIR_IDS = [
    "R-REPAIR-DESCRIPTOR",
    "R-REPAIR-AUTHORITY-PER-TARGET",
    "R-MIN-RESOLUTION-THREE-LEVELS",
    "R-MIN-RESOLUTION-REPAIR-EVIDENCE",
    "R-MUTATION-REPLAY-SCOPE",
    "R-REPAIR-APPLY-KEY",
    "R-CLONES-NEGATIVE-VECTORS",
    "R-JS-CLONE-BODY-THROUGH-TS",
    "R-HIDDEN-MISMATCH-PER-LANGUAGE",
]

must = [
    {
        "id": "MUST-SCHEMA-ENVELOPES-NOT-INHABITED",
        "requirementIds": ENVELOPE_IDS,
        "normativeSelectors": [
            "docs/coop/design-corrections/workflows/schemas/evaluator3/command-envelope.schema.json (schemaMajor 3, required schemaFamily/schemaMajor/kind/requestId/termination/exitCode)",
            "docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json#/$defs/StepTermination",
            "docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json#/$defs/DomainDetail",
            "docs/v2/contracts/product-v1/workflows-and-surfaces.md §8 (CommandEnvelope major 3 succeeds inherited D9 hostTerminationUnion for product envelopes)",
            "docs/coop/artifacts/d9-exit-contract.v1.14.json (inherited class/code/exit legality; no undeclared D9 field)",
            "docs/coop/design-corrections/current-source-map.proposed.md (workflow owner workflows/schemas/evaluator3/)",
        ],
        "finding": "Every claimed schemaEnvelope file is a narrative fragment (boundary/class labels, completeEnvelope:true, examples[{class,exit}]). Independent Draft 2020-12 validation against CommandEnvelope major 3 and StepTermination failed on all 12 envelope files (additionalProperties). Public-from-internal is not DomainDetail. Failure envelopes are not the selected D9/common/native composition.",
        "probes": [
            "envelope.CommandEnvelope:* stockOk=false",
            "envelope.StepTermination:* stockOk=false",
            "d9.public-from-internal.DomainDetail stockOk=false",
            "public-termination.examples-as-StepTermination stockOk=false",
        ],
    },
    {
        "id": "MUST-COMPARISON-BASELINE-AUTH-LITERALS",
        "requirementIds": CMP_IDS,
        "normativeSelectors": [
            "docs/coop/design-corrections/workflows/schemas/evaluator3/comparison-result.schema.json (required comparisonResultId, descriptor; E0–E4 pivot chain)",
            "docs/coop/design-corrections/workflows/schemas/evaluator3/baseline-artifact.schema.json",
            "docs/v2/contracts/product-v1/workflows-and-surfaces.md (baseline/comparison axes; E0 prior detector vs E1–E3 re-evaluation)",
            "docs/coop/design-corrections/workflows/schemas/evaluator3/repair.schema.json (test/preparation/repair authorization as records, not host execution)",
            "docs/coop/design-corrections/workflows/command-inventory.v3.json",
        ],
        "finding": "Comparison/baseline/authorization artifacts are case-label objects ({case: missing-evidence}, {notTheSame: true}, {test,preparation,repair} strings). None inhabit ComparisonResult or BaselineArtifact. Pivot-only fingerprints and host-captured vs candidate are literal booleans/phrases.",
        "probes": [
            "comparison.ComparisonResult:* stockOk=false",
            "comparison.BaselineArtifact:* stockOk=false",
            "auth.vector-is-three-labels",
        ],
    },
    {
        "id": "MUST-CONFIG-GRAPHS-NOT-COMPUTED",
        "requirementIds": CFG_IDS,
        "normativeSelectors": [
            "docs/coop/design-corrections/native/native-evidence.schemas.v2.json#/$defs/TypeScriptConfigGraphV1",
            "docs/coop/design-corrections/native/native-evidence.schemas.v2.json#/x-opensip-config-node-kind-law",
            "docs/v2/contracts/product-v1/native-evidence.md (js-synthesized, custom-named other entry, jsconfig shared base)",
        ],
        "finding": "Standalone config vectors do not inhabit TypeScriptConfigGraphV1 (required schemaVersion/entryConfigPath/nodes[].path,contentSha256,kind,extendsResolved). No computed tsconfigGraphHash. R-CONFIG-SYNTHESIZED observable explicitly requires identity/schema of the config graph plus computed identity. Repeated-base order is a string list with repeatedBaseRetained:true. The TS complete-Run graph is a different single-node tsconfig.json shape and does not satisfy these three standalone exercises.",
        "probes": [
            "config.TypeScriptConfigGraphV1:config-synthesized.json",
            "config.TypeScriptConfigGraphV1:config-custom-multi-base.json",
            "config.TypeScriptConfigGraphV1:config-js-shared-base.json",
            "store.ts.config-graph (single tsconfig.json node, extends=[])",
        ],
    },
    {
        "id": "MUST-REPAIR-CLONE-MINRES-NOT-EXECUTED",
        "requirementIds": REPAIR_IDS,
        "normativeSelectors": [
            "docs/coop/design-corrections/workflows/schemas/evaluator3/repair.schema.json#/$defs/RepairPlanV1",
            "docs/coop/design-corrections/workflows/schemas/evaluator3/repair.schema.json#/$defs/MutationReceiptV1",
            "docs/coop/design-corrections/workflows/schemas/evaluator3/invocation-record.schema.json MutationReplayScopeV1 / H('workflow.mutation-intent', …)",
            "docs/coop/design-corrections/workflows/schemas/policy-document.v2.schema.json Atom.minResolution",
            "docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json ladders",
            "docs/coop/design-corrections/foundation/identity-schemas.v3.json languageVersionBinding.bodyLanguageByVariant",
        ],
        "finding": "Repair/min-resolution/mutation/clone-negative/JS-body vectors are prose or declared firstRefusal without an input instance or helper process status. repair-apply-key sets measuredInequality:true with no hex keys. clones-negatives list FACT_ANCHOR_CARDINALITY etc. without a clone record. js-body-through-ts has notRelabelledAsTypescript:true and no .js body in any store. hidden-mismatch firstRefusal values are selector strings.",
        "probes": [
            "repair.RepairPlanV1:* stockOk=false",
            "clones-negatives.declared-firstRefusal-no-instance",
            "min-resolution.cases-are-strings",
            "repair-apply-key.computed-inequality",
            "store.ts.js-clone-body-through-ts src/util.js hits=0",
        ],
    },
    {
        "id": "MUST-GRAPH-QUERY-NOT-TYPED",
        "requirementIds": ["R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR"],
        "normativeSelectors": [
            "docs/coop/design-corrections/workflows/query-projection-contract.v3.md §§1–8",
            "docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json#/$defs/GraphQueryRequestV1",
            "docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json#/$defs/GraphQueryResponseV1",
            "docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json#/$defs/GraphEvidenceDisclosure",
            "docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json#/$defs/GraphOperationResponseContext",
            "docs/v2/contracts/product-v1/workflows-and-surfaces.md §8 (query parity fields resolved-view, availability, …)",
        ],
        "finding": "The charter requires independently derived complete typed responses for graph.neighbors, graph.path, and graph.reach, plus failure envelopes, bound/cursor cases, renderer/summary joins, and measured results over an admitted retained Run. Snapshot files are request-shaped notes plus one untyped neighbors row. Missing schemaFamily/schemaMajor/completeness/page; no items/context/evidence; path/reach have no result units; failures.json is a code map not CommandEnvelope kind=failure; parity.json is {completeParity:true}. graph-neighbors endpoint.universe is 'ts-universe-hex' (not 64-hex). measured-neighbors does cite a real TS fact2 and correctly refuses to invent an imports edge without TargetAttributionV1 — that fragment is not the complete reconstruction.",
        "probes": [
            "query.GraphQueryRequestV1:* stockOk=false",
            "query.GraphQueryResponseV1:measured-neighbors.json stockOk=false",
            "query.measured-neighbors.required-response-fields missing schemaFamily/schemaMajor/context/items",
            "query.graph-neighbors.endpoint-universe-is-64hex ok=false",
            "query.measured-neighbors.fact-in-ts-store ok=true (fact2:1e1e51fa…)",
            "query.failures.as-CommandEnvelope stockOk=false",
            "query.parity.literals",
        ],
    },
    {
        "id": "MUST-OWNERSHIP-STABILITY-NOT-MEASURED",
        "requirementIds": ["R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE"],
        "normativeSelectors": [
            "docs/coop/design-corrections/native/native-evidence.schemas.v2.json#/$defs/SourceUnitOwnershipV1",
            "docs/coop/artifacts/fact-identity-policy.v2.json canonicalisationSchema (body identity frame)",
        ],
        "finding": "Requirement: measured pair, not a sentence. Vector copies edition2018_L0 onto both libOnlySelectionIdentity and libAndSameEditionExtraTargetWouldMatch and sets a literal true. Distinct 2018 vs 2021 L0 hashes are a dialect measurement, not an ownership-stability measurement.",
        "probes": ["rust-pair.stable-ownership-is-literal-same-assignment"],
    },
    {
        "id": "MUST-ACCEPT-WHILE-UNEXECUTED",
        "requirementIds": [
            "R-NO-ACCEPT-IF-INCOMPLETE",
            "R-MUST-SHOULD-ADVISORY",
            "R-IDENTIFY-GAPS",
            "R-BLOCKER-NOT-ADJUST",
            "R-VALID-VS-INVALID-VS-EXPLANATORY",
            "R-MEASURED-NOT-COUNTS",
            "R-NEGATIVE-FIRST-REFUSAL",
            "R-REPLAY-EXPORT",
        ],
        "normativeSelectors": [
            "requirements.json stopCondition.acceptForbiddenIf",
            "requirements.json classificationRule",
            "requirements.json deliverables.statusEnum",
        ],
        "finding": "Consumer marked all 123 acceptBlocking reconstruction IDs executed, newMustIssues=[], verdict ACCEPT-RECONSTRUCTABLE. Independent measurement shows schemaEnvelope/comparison/config/repair/query families are explanatory literals. 37/43 vector files lack valid|invalid|explanatory classification. Replay export exists only for syntax-code. ACCEPT is forbidden while those acceptBlocking items remain unexecuted.",
        "probes": [
            "consumer.claimed-verdict ACCEPT-RECONSTRUCTABLE must=[]",
            "classification-field.coverage nUnclassified=37",
            "replay.export-per-claimed-positive ts/rust/syntax-data/rust-partial missing",
        ],
    },
]

should = [
    {
        "id": "SHOULD-RECEIPT-UNBOUND-SYNTHETIC-IDS",
        "requirementIds": ["R-DURABLE-RECEIPT-AVAILABILITY"],
        "normativeSelectors": [
            "docs/coop/design-corrections/foundation/identity-schemas.v3.json#/$defs/commit-receipt",
            "docs/coop/design-corrections/foundation/identity-schemas.v3.json#/$defs/availability",
        ],
        "finding": "Nested records stock-validate, but run3:abab… and inventoryDigest 11… are unbound placeholders, not a receipt of a retained reconstructed Run. Keep the nested shape; join to an exported Run or label synthetic host observation explicitly.",
        "probes": ["receipt-availability.commit-receipt stockOk=true", "receipt-availability.availability stockOk=true"],
    },
    {
        "id": "SHOULD-PARTIAL-CELL-COMPLETE-CONTRADICTION",
        "requirementIds": ["R-RUN-RUST-PARTIAL-EMPTY-CLONES", "R-CLONE-DEFICIENCY-PAIRING"],
        "normativeSelectors": [
            "docs/coop/design-corrections/native/native-evidence.schemas.v2.json#/$defs/SourceUnitOwnershipV1 enumeration=partial",
            "docs/coop/design-corrections/native/native-evidence.schemas.v2.json#/x-opensip-deficiency-cause-registry (input-closure-incomplete / body-language-owner-unenumerated)",
        ],
        "finding": "Coverage payload pairing is the published unknown + input-closure-incomplete / body-language-owner-unenumerated and there is no clones fact2. execution-inputs.cellOutcomes still marks clones-fact state=complete with deficiency null. A leftover clones payload `cl` is retained without a clones fact. Align cellOutcomes with Coverage.",
        "probes": ["store.rust-partial decoded cvp-clones vs ei.cellOutcomes"],
    },
    {
        "id": "SHOULD-IMPORT-SUBJECTS-EMPTY",
        "requirementIds": ["R-IMPORTED-PAYLOAD-IN-GRAPH"],
        "normativeSelectors": [
            "docs/coop/design-corrections/workflows/schemas/imported-evidence.schema.json#/$defs/RuntimePayloadV1",
        ],
        "finding": "An import2/RuntimePayloadV1 pair is retained on the TS graph, but subjects=[]. Strengthen with at least one mapped imported subject if claiming imported observation participates in evaluation.",
        "probes": ["store.ts import-runtime / RuntimePayloadV1"],
    },
    {
        "id": "SHOULD-CLASSIFICATION-AND-FIRST-REFUSAL-ON-STANDING-VECTORS",
        "requirementIds": [
            "R-CHAIN-ZERO-CONFIG-TO-RECEIPT",
            "R-SEMANTIC-VS-OPERATIONAL-AUTHORITY",
            "R-MUTATION-VS-ANALYSIS-STEPS",
            "R-PROMISE-VS-AVAILABILITY",
            "R-SUBSYSTEM-OWNERS",
            "R-MULTI-UNIT-MISSING-CAPS",
            "R-CANDIDATE-ONLY-CLONES",
            "R-RUN-UNSUPPORTED-GRAMMAR",
            "R-REPLAY-THREE-VALUED",
        ],
        "normativeSelectors": [
            "requirements.json R-VALID-VS-INVALID-VS-EXPLANATORY",
            "requirements.json R-NEGATIVE-FIRST-REFUSAL",
            "docs/coop/design-corrections/foundation/evaluator-composition-contract.v3.md (Kleene three-valued)",
        ],
        "finding": "These standing/config rows were satisfied with kit-standing citations, reused identity vectors, or three-word maps. Reconstruct the cited chain/availability/three-valued law as labeled valid|invalid|explanatory measurements. Unsupported-grammar is a path string plus a refusal name, not an executed helper refusal.",
        "probes": ["classification-field.coverage", "replay-three-valued.literals"],
    },
]


def disposition_of(i: str) -> str:
    if i in FUTURE:
        return "futureQualification"
    if i in FAILED:
        return "failed"
    if i in EXPLANATORY:
        return "explanatory"
    if i in ARTIFACT_PRESENT_UNREVIEWED_ADMISSION:
        return "artifact-present-unreviewed-admission"
    if i in UNREVIEWED:
        return "unreviewed"
    if i in EXECUTED:
        return "executed"
    raise SystemExit(f"unclassified {i}")


assessed = []
counts = {}
for row in cat:
    i = row["id"]
    disp = disposition_of(i)
    counts[disp] = counts.get(disp, 0) + 1
    cl = claimed.get(i) or {}
    assessed.append(
        {
            "id": i,
            "kind": row["kind"],
            "phase": row["phase"],
            "acceptBlocking": row["acceptBlocking"],
            "consumerClaimedStatus": cl.get("status"),
            "consumerClaimedArtifact": cl.get("artifact"),
            "disposition": disp,
            "measurement": NOTES.get(i),
        }
    )

# sanity
all_ids = {r["id"] for r in cat}
classified = EXECUTED | EXPLANATORY | FAILED | UNREVIEWED | FUTURE | ARTIFACT_PRESENT_UNREVIEWED_ADMISSION
missing = all_ids - classified
extra = classified - all_ids
if missing or extra:
    raise SystemExit(f"missing={sorted(missing)} extra={sorted(extra)}")

probe_results = json.loads((OUT / "probes/scope_probe.results.json").read_text())
probe_fail = [p["name"] for p in probe_results["probes"] if p.get("ok") is False]
probe_ok = [p["name"] for p in probe_results["probes"] if p.get("ok") is True]

review = {
    "reviewer": "consumer-b.v12-kit-scope-review.v1 independent kit-only reconstruction-scope reviewer",
    "verdict": "SCOPED_WORK_INCOMPLETE",
    "standing": "This is not product qualification, implementation authorization, or whole-design acceptance. It audits declared 123-scope reconstruction against measured artifacts in the frozen consumer snapshot.",
    "inputHashes": {
        "consumerInputManifestSha256": "ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8",
        "consumerInputManifestExpected": "ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8",
        "consumerInputManifestMatch": True,
        "parentSubjectSha256": "a70f5830c9d54f5a6bc3285cb05c34fb6331d5278ae1c46e12147a5f95a10bbb",
        "parentMatch": True,
        "kitFileCount": 80,
        "kitHashVerification": "PASS 80/80, 0 missing, 0 mismatch",
        "snapshotManifestSha256": "089b5f5deab3795a7c66cfe08aed22c8a167b318fa0228a58d7d83eb7dd1609f",
        "snapshotFileCount": 128,
        "snapshotHashVerification": "PASS 128/128, 0 missing, 0 mismatch",
        "requirementsSha256": "855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495",
        "requirementsCount": {"standing": 8, "requirements": 123, "futureQualification": 3, "assessed": 134},
    },
    "consumerClaimedVerdict": "ACCEPT-RECONSTRUCTABLE",
    "consumerClaimedStanding": "Claims are not design authority. ACCEPT-RECONSTRUCTABLE is rejected for this scoped audit because acceptBlocking envelope/comparison/config/repair/query rows are explanatory literals, not executed reconstructions.",
    "dispositionCounts": counts,
    "assessed": assessed,
    "newMustIssues": must,
    "newShouldIssues": should,
    "preservedHelperCorrections": [
        {
            "originalFailure": "TypeError: unsupported operand type(s) for |: 'tuple' and 'set' in protocol3.step post-terminal preMatchLaw",
            "kitSelector": "docs/coop/design-corrections/native/protocol3-transitions.v1.json preMatchLaw / wildcards.*PROCESS_FAULT",
            "correction": "Use a set literal for {zero-exit, eof} union PROCESS_FAULT_FRAMES. Not a design gap.",
            "retainedIn": ["consumer-snapshot/checkpoints/phase-3.json", "consumer-snapshot/blind-review.json helperCorrections"],
        }
    ],
    "ownExecutedProbes": {
        "runner": "/tmp/opensip-architecture-review-env/bin/python -I -B output/probes/scope_probe.py",
        "resultsPath": "probes/scope_probe.results.json",
        "nProbes": len(probe_results["probes"]),
        "nMarkedOk": len(probe_ok),
        "nMarkedNotOk": len(probe_fail),
        "highlights": {
            "kitHashes": "80/80 PASS",
            "snapshotHashes": "128/128 PASS",
            "hRemintSnapshotA": "PASS claimed H == independent H",
            "cve1IntegerBoolNullRemint": "8/8 PASS",
            "commandEnvelopeInhabitance": "0/12 envelope files stock-ok",
            "comparisonInhabitance": "0/7 comparison/baseline files stock-ok",
            "configGraphInhabitance": "0/3 config vectors stock-ok as TypeScriptConfigGraphV1",
            "graphQueryRequestResponse": "0/6 query files stock-ok as GraphQueryRequestV1/ResponseV1",
            "receiptNestedCommitReceipt": "PASS",
            "receiptNestedAvailability": "PASS",
            "tsNodeModulesInInventory": "PASS",
            "tsScopeDocumentBound": "PASS payloadDigest 1184fd7d…",
            "rustEditionMapN": 17,
            "rustSamePathTwoUnits": "PASS",
            "syntaxCodeL0L1Present": "PASS",
            "syntaxDataUnsupportedPairing": "PASS on cvp-clones",
            "replayExports": {"syntax-code": True, "ts": False, "rust": False, "syntax-data": False, "rust-partial": False},
        },
        "failedProbeNames": probe_fail,
    },
    "unreviewedScope": [
        "Whole recursive syntax-code identity/schema/closure/semantic-replay/root admission (assigned to a separate kit-only reviewer; not duplicated here).",
        "Whole Run admission of TS, Rust, syntax-data, and rust-partial graphs. Stores were inspected for named properties only; fragments are not close_run.",
        "Independent re-derivation of every relation-rung pair and every protocol3 transition row.",
        "CVE1 NFC-UTF8-string / array / string-keyed-map remint beyond integer/bool/null.",
        "Any original repository, author models, goldens, prior design reviews, root checks, or other /tmp/opensip-design-corrections trees.",
    ],
    "futureQualificationNotDemanded": [
        "F-OS-COMPILER-CRYPTO-SQLITE",
        "F-SYNTHETIC-TCB",
        "F-AUTH-HOST",
    ],
    "boundedCorrectionSequence": [
        {
            "step": 1,
            "keep": "Do not start from scratch. Retain independently authored C/H/CVE1/lexical/cap-admission/protocol3 helpers, traces, relation tables, helperCorrections, and the five exported Run stores plus useful Run-property records (TS node_modules/config/ScopeDocument/import2; Rust edition/ownership/#/ marker; syntax L0/L1; syntax-data unsupported pairing).",
        },
        {
            "step": 2,
            "do": "Rebuild every schemaEnvelope as an actual inhabitant of evaluator3 CommandEnvelope major 3 with StepTermination/DomainDetail from the selected D9/common composition. Map existing internal refusal names (ADM-ORDER, PINNED_PURGE_REFUSED, QUERY.*) into those envelopes. Keep synthetic TCB observations; do not demand OS/crypto.",
            "ids": ENVELOPE_IDS,
        },
        {
            "step": 3,
            "do": "Construct TypeScriptConfigGraphV1 records for synthesized (entryConfigPath null, empty nodes), custom-named tsconfig.build.json kind=other with ordered repeated extendsResolved, and jsconfig.json extending a shared base. Compute tsconfigGraphHash = SHA-256(C(record)). These remain standalone config vectors, not new complete Runs.",
            "ids": CFG_IDS,
        },
        {
            "step": 4,
            "do": "Inhabit evaluator3 ComparisonResult/BaselineArtifact for missing-evidence, evidence-changed, empty-result, scope-policy-only, E0 vs E1–E3, and pivot-only fingerprints. Reconstruct repair descriptor / per-target authority / min-resolution three-level qualifying+insufficient facts / mutation-intent vs repair-apply keys as schema records with independently computed H. Execute clone negatives and hidden-mismatch through helpers so firstRefusal is a process result. Construct a JS body through the TS universe without relabelling languageId.",
            "ids": CMP_IDS + REPAIR_IDS,
        },
        {
            "step": 5,
            "do": "Against an already retained Run (TS imports fact is a starting point), emit GraphQueryRequestV1 + GraphQueryResponseV1 for graph.neighbors, graph.path (including admitted start==target zero-hop), and graph.reach. Include GraphEvidenceDisclosure, GraphOperationResponseContext (countBasis, traversalCoverage, visitedNodes, cursor bind), and CommandEnvelope kind=failure for the published query fault table. Renderer parity is declared parity fields over the same ResolvedView, not completeParity:true. Do not invent TargetAttributionV1; keep unprojectable-fact disclosure where the kit omits the edge.",
            "ids": ["R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR"],
        },
        {
            "step": 6,
            "do": "Independently recompute body identity under lib-only vs lib+bin ownership with the same dialect; store both results. Set rust-partial clones-fact cellOutcomes to unavailable/indeterminate consistent with unknown Coverage. Export replay.json for every claimed complete positive after the parallel syntax-pilot reviewer lands; do not reset syntax-code bytes.",
            "ids": [
                "R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE",
                "R-RUN-RUST-PARTIAL-EMPTY-CLONES",
                "R-CLONE-DEFICIENCY-PAIRING",
                "R-REPLAY-EXPORT",
            ],
        },
        {
            "step": 7,
            "do": "Re-label remaining standing reconstructions (zero-config→receipt chain, promise vs availability, subsystem owners, three-valued missing Coverage) as executed measurements. Restore valid|invalid|explanatory and firstRefusal on every negative. Re-issue newMustIssues from remaining gaps. Verdict may not be ACCEPT-RECONSTRUCTABLE while any acceptBlocking row in this same 123-scope is explanatory or failed.",
            "ids": [
                "R-CHAIN-ZERO-CONFIG-TO-RECEIPT",
                "R-VALID-VS-INVALID-VS-EXPLANATORY",
                "R-NEGATIVE-FIRST-REFUSAL",
                "R-NO-ACCEPT-IF-INCOMPLETE",
            ],
        },
    ],
    "same123Scope": True,
    "didNotRepairConsumerFiles": True,
    "didNotSupplyAuthorOracle": True,
}

(OUT / "review.json").write_text(json.dumps(review, indent=2) + "\n")
print("wrote review.json")
print("counts", json.dumps(counts, indent=2))
print("assessed", len(assessed))
print("must", len(must), "should", len(should))
