#!/usr/bin/env python3
"""Self-audit of v1 scope review; emit self-audit.json and successor review.json."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

V1 = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-scope-review.v1")
V2 = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-scope-review.v2/output")
KIT = V1 / "subject"
SNAP = V1 / "consumer-snapshot"

v1 = json.loads((V1 / "output/review.json").read_text())
req = json.loads((V1 / "requirements.json").read_text())
cat = {r["id"]: r for r in req["standing"]}
for r in req["requirements"]:
    cat[r["id"]] = r
for r in req["futureQualification"]:
    cat[r["id"]] = r
v1a = {a["id"]: a for a in v1["assessed"]}

# measurement kinds
SK_STANDING = "standing-record-presence"
SK_HASH = "independent-hash-verification"
SK_SAMPLED_ENC = "sampled-independent-encoding"
SK_DECLARED_REFUSAL = "declared-firstRefusal-inspection"
SK_STOCK = "stock-schema-pass"
SK_STORE_PROP = "store-property-presence"
SK_EXPORT_SHAPE = "export-shape-presence"
SK_FILE_PRESENT = "artifact-file-presence"
SK_TABLE_UNVERIFIED = "table-present-completeness-unverified"
SK_SAMPLED_BEHAVIOR = "sampled-behavior-or-trace"
SK_LITERAL = "literal-boolean-or-narrative"
SK_UNREVIEWED = "not-measured-here"
SK_FUTURE = "future-qualification-not-demanded"

# owning records for schemaEnvelope / related
OWNERS = {
    "R-PINNED-PURGE": "evaluator3 CommandEnvelope kind=failure + StepTermination (selected D9/common composition). Observable: schema-valid against the selected composition.",
    "R-INVOCATION-DISCLOSURE": "command-inventory.v3.json disclosure (ownership fields, bounded cardinality, ordering, formats). NOT CommandEnvelope outer fields.",
    "R-SINGLE-STEP": "evaluator3 invocation-record.schema.json InvocationRecord (orderedSteps length 1) from command-inventory.v3. NOT CommandEnvelope run/failure.",
    "R-MULTI-STEP-DIFFERENT-SELECTIONS": "evaluator3 InvocationRecord with named multi-step orderedSteps and different analysis selections. NOT CommandEnvelope.",
    "R-PUBLIC-FROM-INTERNAL-REFUSAL": "CommandEnvelope kind=failure with DomainDetail, built from an actual internal refusal + originating boundary.",
    "R-ENVELOPE-CONFIG-INPUT": "CommandEnvelope kind=failure / selected D9 composition for configuration-input.",
    "R-ENVELOPE-EXTERNAL-INPUT": "CommandEnvelope kind=failure for retained-external-input.",
    "R-ENVELOPE-HOST-INVALID": "CommandEnvelope kind=failure for host-generated invalid internal record.",
    "R-ENVELOPE-PRODUCER-BOUNDARY": "CommandEnvelope kind=failure for producer-boundary.",
    "R-FAILURE-ENVELOPES-D9": "Complete CommandEnvelope kind=failure including StepTermination + DomainDetail (D9/common/native composition), not a termination fragment alone.",
    "R-D9-EXTENSION-PRECEDENCE": "note+vector comparing selected composition vs inherited d9-exit-contract.v1.14.json. NOT a CommandEnvelope instance.",
    "R-DURABLE-RECEIPT-AVAILABILITY": "identity-schemas.v3.json#/$defs/commit-receipt and #/$defs/availability. NOT CommandEnvelope, NOT MutationReceiptV1.",
    "R-PUBLIC-TERMINATION-EXAMPLES": "evaluator3 common.schema.json#/$defs/StepTermination examples. NOT required to carry CommandEnvelope outer fields.",
    "R-PURGE-REPLAY-OUTPUT-FAILURE": "CommandEnvelope kind=failure covering purge/replay and required-output failure (e.g. OUTPUT.SERIALIZATION_FAILED).",
    "R-BASELINE-AUDIT": "evaluator3 baseline-artifact.schema.json (and comparison schema as used by that audit). NOT every comparison case.",
    "R-CMP-MISSING": "evaluator3 comparison-result.schema.json. NOT BaselineArtifact.",
    "R-CMP-EVIDENCE-CHANGED": "evaluator3 comparison-result.schema.json.",
    "R-CMP-EMPTY-RESULT": "evaluator3 comparison-result.schema.json.",
    "R-SCOPE-POLICY-ONLY-COMPARISON": "evaluator3 comparison-result.schema.json with ScopeDocumentV1-only change.",
    "R-E0-VS-E1-E3": "comparison/baseline pivot distinction (E0 prior detector vs E1–E3 re-evaluation). A ComparisonResult descriptor may exhibit it; {notTheSame:true} is not enough.",
    "R-PIVOT-ONLY-FINGERPRINTS": "comparison/baseline vector retaining pivot-only fingerprints.",
    "R-TEST-PREP-REPAIR-AUTH": "authorization records/envelopes from repair/command-inventory/security. NOT ComparisonResult, NOT host execution.",
    "R-HOST-CAPTURED-VS-CANDIDATE": "retained-observation distinction (execution-inputs selectedRefs vs candidate-only). NOT ComparisonResult.",
    "R-CONFIG-SYNTHESIZED": "native-evidence.schemas.v2.json#/$defs/TypeScriptConfigGraphV1 with entryConfigPath=null and nodes=[] (minItems 0). Computed identity = SHA-256(C(graph)), bound as TypeScriptUniverseV2ResolvedInputs.tsconfigGraphHash if a universe is present. tsconfigGraphHash is NOT a field of TypeScriptConfigGraphV1 (additionalProperties false).",
    "R-CONFIG-CUSTOM-MULTI-BASE": "TypeScriptConfigGraphV1: custom-named entry (basename not tsconfig.json/jsconfig.json → kind=other), ordered extendsResolved with repeats retained, nodes reachable/acyclic, contentSha256 preimages.",
    "R-CONFIG-JS-SHARED-BASE": "TypeScriptConfigGraphV1: jsconfig.json entry kind=jsconfig; shared base kind from basename law; configOrigin derived from ENTRY kind only.",
    "R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR": "evaluator3 graph-query.schema.json GraphQueryRequestV1 + GraphQueryResponseV1 for graph.neighbors|path|reach; GraphEvidenceDisclosure; GraphOperationResponseContext; CommandEnvelope kind=failure for the published query fault table; renderer parity fields. query-projection-contract.v3.md §§1–8.",
    "R-RUN-RUST-PARTIAL-EMPTY-CLONES": "exported graph; clones Coverage unknown pairing; CellProgramOutcomeV1.state CLOSED {complete,partial,unavailable} derived per execution-inputs-contract.v1.md §4 — not evaluator verdict.",
    "R-IMPORTED-PAYLOAD-IN-GRAPH": "foundation import2 member of a claimed Run plus registered imported payload (imported-evidence RuntimePayloadV1 etc.). subjects minItems=0; nonempty subjects is not an original obligation.",
}

# successor dispositions
# change codes: confirmed, measurement-filled, downgraded, upgraded, owning-record-corrected

SUCC = {}  # id -> dict


def put(i, disp, kind, meas, change, **extra):
    SUCC[i] = {
        "disposition": disp,
        "measurementKind": kind,
        "measurement": meas,
        "changeFromV1": change,
        **extra,
    }


# --- standing ---
put("S-FRESH-ORIGIN", "executed", SK_STANDING, "kit-standing.json names consumerId consumer-b.v12 and kit hashes.", "measurement-filled")
put("S-NOT-PRODUCT", "executed", SK_HASH, "Kit bytes still match the frozen 80-file manifest; this review did not observe product implementation.", "measurement-filled")
put("S-KIT-ONLY", "executed", SK_STANDING, "Consumer citations name kit selectors. This review did not observe the consumer process; citation surface only.", "measurement-filled")
put("S-MANIFEST-VERIFY", "executed", SK_HASH, "Independent 80/80 path/sha256/bytes PASS; parent a70f5830… match.", "confirmed")
put("S-NO-ORACLE", "executed", SK_STANDING, "No author-model/golden citations as expected outputs in kit-standing/blind-review. Citation surface only.", "measurement-filled")
put("S-MISSING-DEP-IS-CUSTODY", "executed", SK_HASH, "custodyGaps empty; this review also found no missing kit files.", "measurement-filled")
put("S-PROFILE-CURRENT", "executed", SK_STANDING, "kit-standing records identity-schemas.v3 and run3/proof3 majors; native majors retained as major2.", "measurement-filled")
put("S-CONTINUATION", "executed", SK_FILE_PRESENT, "checkpoints/phase-11.json unions the full required ID set.", "measurement-filled")
put("R-FIVE-CONTRACTS-INDEX", "executed", SK_STANDING, "kit-standing.fiveContracts lists the five product-v1 contracts and successor-over-inherited rule.", "measurement-filled")
put("R-SOURCE-MAP-SCOPE", "executed", SK_STANDING, "kit-standing.sourceMapScope records governance standing not used as recipe.", "measurement-filled")
put("R-CVE1-TYPES-AVAILABLE", "executed", SK_STANDING, "kit-standing lists eight closed CVE1 types from resolved-inputs.v2 canonicalValueEncoding.", "measurement-filled")

put("R-H-HELPER", "executed", SK_SAMPLED_ENC, "Independent remint of snapshot-A C/H matched 7ad0e60f…f556. Other vectors in the file were not reminted. Sampled encoding, not totality of the file.", "measurement-filled")
put("R-CVE1-EIGHT-TYPES", "executed", SK_SAMPLED_ENC, "Consumer vector lists all eight types with committedBytesHex. Independent remint confirmed null/false/true/unsigned-64/negative-signed-64 (8 integer/bool/null cases). NFC-UTF8-string, array, string-keyed-map were not independently reminted. Not a claim that this review round-tripped all eight.", "measurement-filled")
put("R-LEXICAL-ADMISSION", "executed", SK_DECLARED_REFUSAL, "lexical-admission.json carries rawUtf8/rawHex and firstRefusal on invalids. This review inspected those objects; did not re-execute the lexical helper.", "measurement-filled")
put("R-SEMANTIC-VS-OPERATIONAL", "executed", SK_SAMPLED_ENC, "Probe semantic-vs-operational.has-measured-ids: semantic vcsDigest change equal=false; operational requestId change equal=true; measured=true.", "measurement-filled")
put("R-RAW-VS-PARSED", "executed", SK_DECLARED_REFUSAL, "raw-vs-parsed.json distinguishes parsedObjectEncode vs rawDuplicate/rawFloat with firstRefusal codes DUPLICATE_KEY/FLOAT_FORBIDDEN. Inspected artifact; helper not re-run.", "measurement-filled")
put("R-ACYCLIC-JOINS", "artifact-present-content-unverified", SK_TABLE_UNVERIFIED, "acyclic-joins.json contains a positive chain and a cycle/refusal object. This review did not independently execute cycle refusal against identity-and-evidence join law.", "downgraded")
put("R-CAP-ADMISSION", "artifact-present-content-unverified", SK_TABLE_UNVERIFIED, "cap-admission.json names CAP-MANIFEST-ID-V1 and ADM-TYPE/CLOSED/DOMAIN/ORDER. This review did not independently remint capabilityManifestId.", "downgraded")
put("R-CAP-NAMED-GATES", "executed", SK_DECLARED_REFUSAL, "Eight gate vectors carry firstRefusal and masksLater. Inspected structure; cap_manifest helper not re-run.", "confirmed")

for i, art in [
    ("R-TRACE-COMPLETE", "traces/complete.json"),
    ("R-TRACE-UNAVAILABLE", "traces/unavailable.json"),
    ("R-TRACE-CANCEL", "traces/cancel.json"),
    ("R-TRACE-FAULT", "traces/fault.json"),
    ("R-TRACE-IDENTITY-BEFORE-SOURCE", "traces/identity-before-source.json"),
    ("R-TRACE-TERMINAL", "traces/terminal.json"),
]:
    if i == "R-TRACE-COMPLETE":
        put(i, "executed", SK_SAMPLED_BEHAVIOR, "complete.json sampled: identityNegotiated then sourceBytesSent; per-step executedVsHost=executed. Not a full 34-row independent replay.", "measurement-filled")
    else:
        put(i, "artifact-present-content-unverified", SK_FILE_PRESENT, f"{art} present with substantial bytes. This review did not independently replay protocol3-transitions.v1.json for this trace.", "downgraded")
put("R-TRACE-EXECUTED-VS-HOST", "executed", SK_SAMPLED_BEHAVIOR, "traces/executed-vs-host.json labels executed vs future-host spawn/EOF. Sampled together with complete.json per-step labels.", "confirmed")

put("R-RELATION-RUNG-TABLE", "artifact-present-content-unverified", SK_TABLE_UNVERIFIED, "relation-rung-table.json present (pairCount recorded). Independent re-derivation of every registered pair remains unreviewed.", "downgraded")
put("R-COUNT-CLASS-ATTEMPT", "artifact-present-content-unverified", SK_TABLE_UNVERIFIED, "count-class-attempt.json present. This review did not independently apply RC-0/1/2 to retained scopes.", "downgraded")
put("R-CODE-VS-DATA-MATRIX", "artifact-present-content-unverified", SK_TABLE_UNVERIFIED, "code-vs-data-matrix.json present as a reconstructed table. Not independently re-derived against native-capability-matrix.v2.json.", "downgraded")
put("R-ENUM-VS-RESOLUTION", "executed", SK_STORE_PROP, "Standing rule: do not invent a resolved file rung. Measured on stores: syntax-code and rust file facts use resolution=enumerated. The vector file itself is a three-line explanation.", "measurement-filled")
put("R-ADVERTISED-MODE-PATHS", "artifact-present-content-unverified", SK_TABLE_UNVERIFIED, "advertised-mode-paths.json lists six languageModes. Completeness vs the published matrix was not independently re-derived.", "downgraded")

# complete Runs
put("R-RUN-TS", "artifact-present-unreviewed-admission", SK_EXPORT_SHAPE, "runs/ts.store.json objectTable+blobs present (run3:1908c594…). Properties sampled separately. close_run not asserted. This review does not perform from-export proof reconstruction.", "confirmed")
put("R-RUN-RUST", "artifact-present-unreviewed-admission", SK_EXPORT_SHAPE, "runs/rust.store.json present (run3:da14a1f0…). close_run not asserted.", "confirmed")
put("R-RUN-RUST-PARTIAL-EMPTY-CLONES", "artifact-present-unreviewed-admission", SK_STORE_PROP, "Store: no clones fact2; ownership.enumeration=partial; cvp-clones coverage=unknown + input-closure-incomplete/body-language-owner-unenumerated. clones-fact CellProgramOutcomeV1.state=complete contradicts derivation (supported-available account not complete → partial). Whole admission unreviewed.", "confirmed")
put("R-RUN-FILE-FACT-INVENTORY", "artifact-present-unreviewed-admission", SK_STORE_PROP, "syntax-code retains fact-file-enumerated with FilePayloadV1 path/contentSha256/byteLength. Whole admission unreviewed.", "measurement-filled")
put("R-RUN-SYNTAX-CODE", "artifact-present-unreviewed-admission", SK_EXPORT_SHAPE, "runs/syntax-code.store.json and .replay.json present. Parallel reviewer owns closure/replay content. This review does not perform from-export proof reconstruction.", "confirmed")
put("R-RUN-SYNTAX-DATA", "artifact-present-unreviewed-admission", SK_STORE_PROP, "Store present; cvp-clones unknown + language-tier-unsupported/capability-missing. Whole admission unreviewed.", "confirmed")

# properties
put("R-RUN-TS-NODE-MODULES", "executed", SK_STORE_PROP, "Inventory contains node_modules/left-pad; universe nodeModulesInReadSet true. Parent Run admission unreviewed.", "confirmed")
put("R-RUN-TS-CONFIG-DEPS", "executed", SK_STORE_PROP, "Retained TypeScriptConfigGraphV1 (single tsconfig.json, extends=[]) and ResolvedNodeModulesLayoutV1. Distinct from standalone synthesized/multi-base/js-shared vectors.", "confirmed")
put("R-RUN-RUST-MIXED-EDITION", "executed", SK_STORE_PROP, "Universe edition map n=17 values {2015,2018,2021,2024}.", "confirmed")
put("R-RUN-RUST-TARGET-EDITION", "executed", SK_STORE_PROP, "lib targetEdition null (package default 2018); bin tool targetEdition 2021 on SourceUnitOwnershipV1.", "confirmed")
put("R-RUN-RUST-BODY-DIALECT", "executed", SK_SAMPLED_ENC, "Distinct L0 identities for edition 2018 vs 2021; clones payload carries 2021 L0. Dialect is in language-version preimage.", "confirmed")
put("R-RUN-RUST-SAME-FILE-TWO-EDITIONS", "executed", SK_STORE_PROP, "Same path #/a/src/lib.rs owned by lib and bin units.", "confirmed")
put("R-RUN-RUST-HASH-MARKER", "executed", SK_STORE_PROP, "Inventoried #/Cargo.toml, #/a/Cargo.toml, #/a/src/lib.rs.", "confirmed")
put("R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE", "failed", SK_LITERAL, "Pair vector copies edition2018_L0 onto both sides and sets a literal true. Two ownership H records exist; body identities were not independently recomputed under each selection. Original verb: measured pair, not a sentence.", "confirmed")
put("R-RUN-RUST-LARGE-EDITION-MAP", "executed", SK_STORE_PROP, "Retained edition map n=17.", "confirmed")
put("R-RUN-RUST-VERSION-COMPONENT", "executed", SK_STORE_PROP, "compiler_build from retained toolchain.rustCommitHash (synthetic deadbeef…; allowed TCB observation).", "confirmed")
put("R-RUN-CLONES-L0-AND-NORMALIZED", "executed", SK_STORE_PROP, "syntax-code ClonesPayloadV1-L0 (L0-verbatim) and ClonesPayloadV1-L1 (L1-lexical) with distinct body identities.", "confirmed")
put("R-RUN-CLONES-CUSTODY", "executed", SK_STORE_PROP, "syntax-code retains level-spec-L1, body-language-version, languageVersion-raw32.", "confirmed")
put("R-RUN-NO-COMPILER-UNIT", "executed", SK_STORE_PROP, "syntax-code H domains native.context.syntax.v2 / native.semantic-universe.syntax.v2; selectedGrammarIds=['rust'].", "confirmed")
put("R-RUN-UNAVAILABLE-SEMANTIC", "executed", SK_STORE_PROP, "syntax-data: clones-fact cell state=unavailable with language-tier-unsupported/capability-missing; inventory complete. Distinct from rust-partial cell complete.", "confirmed")
put("R-RUN-UNSUPPORTED-GRAMMAR", "explanatory", SK_LITERAL, "unsupported-grammar.json is a path string plus a refusal name. No executed helper refusal.", "confirmed")
put("R-RUN-NONCEMPTY-CONTEXT", "executed", SK_STORE_PROP, "TS and Rust plans have nonempty nativeContextDigests; corresponding native.context.* H frames retained.", "measurement-filled")
put("R-SCOPEDOCUMENT-IN-ANALYSIS-SPEC", "executed", SK_STORE_PROP, "analysis-spec parameters bind payloadDigest 1184fd7d… (ScopeDocumentV1 blob) with schemaDigest equal to kit policy-document.schema.json (owner of ScopeDocumentV1).", "confirmed")
put(
    "R-IMPORTED-PAYLOAD-IN-GRAPH",
    "executed",
    SK_STORE_PROP,
    "plan.importIds contains import2:62aab2a2…; RuntimePayloadV1-labeled blob retained. subjects=[] is schema-legal (minItems 0). Payload uses format='json' and null observationWindow/observedPopulation, which are not RuntimePayloadV1 closed members (format enum v8-json|istanbul-json|lcov|llvm-cov-json; observationWindow required object). Graph membership holds; named payload inhabitance is imperfect (advisory).",
    "measurement-filled",
)
put("R-CLONE-DEFICIENCY-PAIRING", "executed", SK_STORE_PROP, "rust-partial cvp-clones deficiency=input-closure-incomplete nativeCause=body-language-owner-unenumerated. CellProgramOutcomeV1.state=complete is a separate derivation defect (SHOULD, corrected vocabulary).", "confirmed")
put("R-HIDDEN-MISMATCH-PER-LANGUAGE", "explanatory", SK_LITERAL, "firstRefusal values are selector strings, not executed helper refusals.", "confirmed")
put("R-NATIVE-PREIMAGE-JOINS", "executed", SK_STORE_PROP, "TS TypeScriptConfigGraphV1 + ResolvedNodeModulesLayoutV1; rust dependency-source-set and cargo-config-projection retained. Joins sampled as retained preimages, not close_run.", "confirmed")

# phase 6+
put("R-CONFIG-SYNTHESIZED", "explanatory", SK_LITERAL, "Notes only; no TypeScriptConfigGraphV1. v1 wrongly spoke of putting tsconfigGraphHash on the graph record.", "confirmed")
put("R-CONFIG-CUSTOM-MULTI-BASE", "explanatory", SK_LITERAL, "String list of extendsResolvedOrder with repeatedBaseRetained:true; not TypeScriptConfigGraphV1 nodes.", "confirmed")
put("R-CONFIG-JS-SHARED-BASE", "explanatory", SK_LITERAL, "Filenames/nodeKind map; not TypeScriptConfigGraphV1.", "measurement-filled")
put("R-JS-CLONE-BODY-THROUGH-TS", "explanatory", SK_LITERAL, "notRelabelledAsTypescript:true; src/util.js hits=0 in stores.", "confirmed")
put("R-CLONES-NEGATIVE-VECTORS", "explanatory", SK_LITERAL, "Declared firstRefusal codes without input instance or helper process status.", "confirmed")
put("R-REPAIR-DESCRIPTOR", "explanatory", SK_LITERAL, "Prose projection note; not a repair.schema.json descriptor/plan inhabitant.", "confirmed")
put("R-REPAIR-AUTHORITY-PER-TARGET", "explanatory", SK_LITERAL, "positive/negative boolean flags; not executed repair-projection controls.", "confirmed")
put("R-MIN-RESOLUTION-THREE-LEVELS", "explanatory", SK_LITERAL, "String table of qualifying/insufficient phrases, not facts/Coverage. Owner is policy-document.v2 Atom.minResolution + relation ladders, not RepairPlanV1.", "confirmed")
put("R-MIN-RESOLUTION-REPAIR-EVIDENCE", "explanatory", SK_LITERAL, "Narrative note; not repair-evidence records tied to the three levels.", "confirmed")
put("R-IMPORTED-OBSERVATION-BOUNDARY", "executed", SK_FILE_PRESENT, "vectors/imported-observation-boundary.json reconstructs mayProve/mayNotProve with kit selectors. That is the required kind (reconstructed boundary vector), not a Run.", "measurement-filled")
put("R-MUTATION-REPLAY-SCOPE", "explanatory", SK_LITERAL, "Sentence about generic mutation intent. Owner is MutationReplayScopeV1 / H('workflow.mutation-intent', …), not RepairPlanV1.", "confirmed")
put("R-REPAIR-APPLY-KEY", "explanatory", SK_LITERAL, "measuredInequality:true with no computed hex keys.", "confirmed")
put("R-PINNED-PURGE", "explanatory", SK_LITERAL, "completeEnvelope:true plus refusal name. Required inhabitant: selected composition envelope (CommandEnvelope kind=failure + StepTermination), not a boolean.", "confirmed")

put("R-CHAIN-ZERO-CONFIG-TO-RECEIPT", "explanatory", SK_LITERAL, "Claimed kit-standing.json; no reconstruction section mapping each arrow to executed artifacts.", "confirmed")
put("R-SEMANTIC-VS-OPERATIONAL-AUTHORITY", "explanatory", SK_LITERAL, "Reuses identity vector; does not cite mutation vs analysis seal recipes.", "confirmed")
put("R-MUTATION-VS-ANALYSIS-STEPS", "explanatory", SK_LITERAL, "mutation-replay-scope sentence; not cited non-seal recipes.", "confirmed")
put("R-MULTI-UNIT-MISSING-CAPS", "explanatory", SK_LITERAL, "Notes about missing types / candidate-only; not an executed configuration shape.", "confirmed")
put("R-CANDIDATE-ONLY-CLONES", "explanatory", SK_LITERAL, "Same file as multi-unit; candidate-only vs selected not measured on a selection record.", "confirmed")
put("R-INVOCATION-DISCLOSURE", "explanatory", SK_LITERAL, "Lists ownership fields / maxItems / formats as notes. Owner is command-inventory.v3 extraction, not CommandEnvelope. v1 MUST that demanded CommandEnvelope for this row is withdrawn.", "owning-record-corrected")
put("R-SINGLE-STEP", "explanatory", SK_LITERAL, "{command:analyze, steps:1}. Owner is InvocationRecord orderedSteps length 1, not CommandEnvelope. Exploratory CommandEnvelope/StepTermination probes remain historically true as extra pairings, not the required inhabitant.", "owning-record-corrected")
put("R-MULTI-STEP-DIFFERENT-SELECTIONS", "explanatory", SK_LITERAL, "Named pipeline note with two analyze steps. Owner is InvocationRecord, not CommandEnvelope.", "owning-record-corrected")
put("R-PROMISE-VS-AVAILABILITY", "explanatory", SK_LITERAL, "Not applied as a cited distinction on availability vectors.", "confirmed")
put("R-PUBLIC-FROM-INTERNAL-REFUSAL", "explanatory", SK_LITERAL, "Three-field map internalRefusal→publicCode. Required: CommandEnvelope kind=failure from an actual internal refusal.", "confirmed")
put("R-ENVELOPE-CONFIG-INPUT", "explanatory", SK_LITERAL, "{boundary, class} only. Required: CommandEnvelope kind=failure for configuration-input.", "confirmed")
put("R-ENVELOPE-EXTERNAL-INPUT", "explanatory", SK_LITERAL, "Same shape. Required: CommandEnvelope kind=failure.", "confirmed")
put("R-ENVELOPE-HOST-INVALID", "explanatory", SK_LITERAL, "Same shape. Required: CommandEnvelope kind=failure.", "confirmed")
put("R-ENVELOPE-PRODUCER-BOUNDARY", "explanatory", SK_LITERAL, "Same shape. Required: CommandEnvelope kind=failure.", "confirmed")
put("R-FAILURE-ENVELOPES-D9", "explanatory", SK_LITERAL, "Reuses public-from-internal fragment. Required: complete D9/common/native composition, not a termination fragment alone.", "confirmed")
put("R-D9-EXTENSION-PRECEDENCE", "explanatory", SK_LITERAL, "Filenames of inherited vs architecture13. Observable is note+vector of selected composition vs inherited artifact — not CommandEnvelope. v1 inclusion in CommandEnvelope MUST withdrawn; the row remains unexecuted as a precedence check.", "owning-record-corrected")
put("R-DURABLE-RECEIPT-AVAILABILITY", "executed", SK_STOCK, "Nested receipt/availability stock-validate as identity-schemas.v3 commit-receipt and availability. Wrapper is not CommandEnvelope (not required). run3:abab… and inventoryDigest 11… are unbound synthetic placeholders (SHOULD).", "confirmed")
put("R-BASELINE-AUDIT", "explanatory", SK_LITERAL, "axes list only. Owner is BaselineArtifact, not ComparisonResult-by-default.", "owning-record-corrected")
put("R-CMP-MISSING", "explanatory", SK_LITERAL, "{case:missing-evidence}. Owner is ComparisonResult, not BaselineArtifact. Exploratory BaselineArtifact probe is extra pairing.", "owning-record-corrected")
put("R-CMP-EVIDENCE-CHANGED", "explanatory", SK_LITERAL, "{case:evidence-changed}. Owner: ComparisonResult.", "confirmed")
put("R-CMP-EMPTY-RESULT", "explanatory", SK_LITERAL, "{case:empty-result}. Owner: ComparisonResult.", "confirmed")
put("R-TEST-PREP-REPAIR-AUTH", "explanatory", SK_LITERAL, "Three labels. Owner: authorization records/envelopes, not ComparisonResult or RepairPlanV1.", "owning-record-corrected")
put("R-PURGE-REPLAY-OUTPUT-FAILURE", "explanatory", SK_LITERAL, "Three phrases. Required: failure envelope for purge/replay/required-output.", "confirmed")
put("R-SCOPE-POLICY-ONLY-COMPARISON", "explanatory", SK_LITERAL, "changed/unchanged strings. Owner: ComparisonResult.", "confirmed")
put("R-PUBLIC-TERMINATION-EXAMPLES", "explanatory", SK_LITERAL, "[{class,exit}]. Owner: StepTermination (branch contract), not CommandEnvelope outer fields. v1 CommandEnvelope MUST for this row withdrawn; StepTermination inhabitance remains required.", "owning-record-corrected")
put("R-SUBSYSTEM-OWNERS", "explanatory", SK_LITERAL, "Four-label map; not cited owners for envelope/comparison decisions.", "confirmed")
put("R-E0-VS-E1-E3", "explanatory", SK_LITERAL, "{notTheSame:true}. Must distinguish E0 prior-detector from E1–E3 re-evaluation as a measured comparison/baseline exhibit.", "confirmed")
put("R-PIVOT-ONLY-FINGERPRINTS", "explanatory", SK_LITERAL, "Two booleans; no retained pivot fingerprints.", "confirmed")
put("R-HOST-CAPTURED-VS-CANDIDATE", "explanatory", SK_LITERAL, "Two phrases; not retained observation records.", "confirmed")
put("R-EMPTY-PARTIAL-UNAVAILABLE-MISSING", "executed", SK_STORE_PROP, "Distinct states sampled: Coverage complete (syntax-code clones), unknown (syntax-data/rust-partial), cell unavailable (syntax-data clones-fact), partial enumeration (rust-partial ownership). Missing committed bytes was not specifically exhibited. Not a single label for all four.", "measurement-filled")
put("R-DETECTOR-COMPAT-FILE", "executed", SK_FILE_PRESENT, "detector-compat-file.json distinguishes .opensip/detector-compatibility.json vs manifest body and cites signed-tree/TreeCommitment owners. That matches the original verb (if reconstructed, listing file not manifest body).", "measurement-filled")

put("R-VALIDATE-OWNING-SCHEMA", "unreviewed", SK_UNREVIEWED, "Consumer schemaChecks arrays are not this review's independent per-record validation including x-opensip-order. Parallel syntax-pilot reviewer owns syntax-code. Not inferred from default executed.", "confirmed")
put("R-INDEPENDENT-CLOSURE-JOINS", "unreviewed", SK_UNREVIEWED, "syntax-code.closure.json is a consumer claim. This review did not independently close joins. Not from-export proof reconstruction.", "confirmed")
put("R-OBJECT-TABLE-FRAMES", "executed", SK_EXPORT_SHAPE, "All five claimed stores export objectTable+blobs. Export-shape presence, not admission.", "confirmed")
put("R-FROM-SCRATCH-COMMAND", "executed", SK_FILE_PRESENT, "scripts/replay_from_export.py and blind-review.json document a python -I -B command. This review did not execute that command (original absolute paths). Observable is a documented command, not a completed from-export proof by this reviewer.", "measurement-filled")
put("R-RETAINED-ARTIFACTS-IN-CLOSURE", "unreviewed", SK_UNREVIEWED, "Not independently closed.", "confirmed")
put("R-SELECTED-PROVIDER-CONTEXT", "unreviewed", SK_UNREVIEWED, "Provider/context fields exist on stores; independent closure of selected provider context unreviewed.", "confirmed")
put("R-VALID-VS-INVALID-VS-EXPLANATORY", "failed", SK_FILE_PRESENT, "37 of 43 vector files lack valid|invalid|explanatory. Probe classification-field.coverage.", "confirmed")
put("R-MEASURED-NOT-COUNTS", "failed", SK_LITERAL, "Many claimed-executed rows are PASS-style [label,true] or literal booleans. Row counts are not acceptance.", "confirmed")
put("R-NEGATIVE-FIRST-REFUSAL", "failed", SK_LITERAL, "Clone/hidden-mismatch/comparison negatives lack executed firstRefusal process results.", "confirmed")
put("R-DISTINGUISH-FOUR-BOUNDARIES", "unreviewed", SK_UNREVIEWED, "schema vs helper vs closure vs host not independently labeled per claimed positive.", "confirmed")
put("R-HELPER-KIT-ONLY", "executed", SK_FILE_PRESENT, "helperCorrections preserve original TypeError tuple|set and kit selector preMatchLaw. Not a design gap.", "confirmed")
put("R-REPLAY-AFTER-ADMISSION", "unreviewed", SK_UNREVIEWED, "Consumer-owned. This review does not perform from-export proof reconstruction. Syntax-code.replay.json content unreviewed (parallel reviewer). Other claimed positives have no replay export (see R-REPLAY-EXPORT).", "confirmed")
put("R-REPLAY-ENUM-AND-IDS", "unreviewed", SK_UNREVIEWED, "Consumer-owned replay reconstruction.", "confirmed")
put("R-REPLAY-PREDICATE-WITNESS-VERDICT", "unreviewed", SK_UNREVIEWED, "Consumer-owned replay reconstruction.", "confirmed")
put("R-REPLAY-NO-CALLER-TRUTH", "unreviewed", SK_UNREVIEWED, "Consumer-owned; helper/evaluator.py presence is not replay admission.", "confirmed")
put("R-REPLAY-COMPARE-BUNDLE", "unreviewed", SK_UNREVIEWED, "Consumer-owned replay reconstruction.", "confirmed")
put("R-REPLAY-EXPORT", "failed", SK_FILE_PRESENT, "runs/syntax-code.replay.json exists. ts/rust/syntax-data/rust-partial have no replay.json. Requirement is every claimed complete positive. Construction is the consumer's from-export work, not this reviewer's. Do not wait on the parallel syntax-pilot reviewer.", "confirmed")
put("R-REPLAY-THREE-VALUED", "explanatory", SK_LITERAL, "Literals indeterminate/notVacuousTrue. Not a measured missing-Coverage vector.", "confirmed")
put("R-REPLAY-TAMPER", "unreviewed", SK_UNREVIEWED, "syntax-code.replay.json contains a tamper object; content not independently validated here.", "confirmed")
put("R-ROOT-ADMISSION-EXPORT", "unreviewed", SK_UNREVIEWED, "Export shape present; root outcome unobserved. This review does not assume a root result.", "confirmed")
put("R-IDENTIFY-GAPS", "failed", SK_LITERAL, "Consumer newMustIssues=[] while acceptBlocking envelope/comparison/query rows are unexecuted. Gap identification standing failed.", "confirmed")
put("R-FREEDOM-VS-MISSING", "executed", SK_FILE_PRESENT, "Advisories treat L1 tokenisation as level-specification freedom vs L0 fully framed. Gap write-up uses the distinction.", "upgraded")
put("R-BLOCKER-NOT-ADJUST", "failed", SK_LITERAL, "ACCEPT-RECONSTRUCTABLE while unexecuted acceptBlocking rows remain.", "confirmed")
put("R-DELIVER-MD-JSON", "executed", SK_FILE_PRESENT, "blind-review.md and blind-review.json exist in the snapshot.", "measurement-filled")
put("R-VERDICT-ENUM", "executed", SK_FILE_PRESENT, "Verdict field is one of the three allowed tokens (ACCEPT-RECONSTRUCTABLE). Using a legal token is not ACCEPT permission; R-NO-ACCEPT-IF-INCOMPLETE fails separately.", "measurement-filled")
put("R-MUST-SHOULD-ADVISORY", "failed", SK_LITERAL, "newMustIssues empty while required findings remain.", "confirmed")
put("R-NO-ACCEPT-IF-INCOMPLETE", "failed", SK_LITERAL, "ACCEPT-RECONSTRUCTABLE with unexecuted acceptBlocking reconstruction.", "confirmed")
put("R-NO-QUALIFICATION-CLAIM", "executed", SK_FILE_PRESENT, "Standing text in both review files disclaims product qualification.", "measurement-filled")
put(
    "R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR",
    "explanatory",
    SK_LITERAL,
    "Request notes plus one untyped neighbors row. measured-neighbors cites real TS fact2:1e1e51fa… and discloses unprojectable-fact without TargetAttributionV1 — keep that disclosure for that retained fact. That is not GraphQueryRequestV1/ResponseV1 for all three operations, cursor bind, or renderer parity. Lawful synthetic TargetAttributionV1 under the published schema remains allowed for a projectable positive; host.targetAttributions is ignored. Notes must not substitute for graph.neighbors|path|reach.",
    "confirmed",
)
put("F-OS-COMPILER-CRYPTO-SQLITE", "futureQualification", SK_FUTURE, "Not demanded.", "confirmed")
put("F-SYNTHETIC-TCB", "futureQualification", SK_FUTURE, "Not demanded; synthetic observations are not native enforcement proof.", "confirmed")
put("F-AUTH-HOST", "futureQualification", SK_FUTURE, "Not demanded.", "confirmed")

missing = set(cat) - set(SUCC)
extra = set(SUCC) - set(cat)
if missing or extra:
    raise SystemExit(f"missing={sorted(missing)} extra={sorted(extra)}")

# --- row audits ---
row_audits = []
for i, spec in SUCC.items():
    orig = v1a[i]
    row_audits.append(
        {
            "id": i,
            "kind": orig["kind"],
            "phase": orig.get("phase"),
            "acceptBlocking": orig.get("acceptBlocking"),
            "originalVerb": cat[i].get("requirement"),
            "observable": cat[i].get("observable"),
            "owningRecord": OWNERS.get(i),
            "v1Disposition": orig["disposition"],
            "v1Measurement": orig.get("measurement"),
            "successorDisposition": spec["disposition"],
            "measurementKind": spec["measurementKind"],
            "successorMeasurement": spec["measurement"],
            "change": spec["changeFromV1"],
            "reason": spec["measurement"],
        }
    )

from collections import Counter

succ_counts = Counter(s["disposition"] for s in SUCC.values())
change_counts = Counter(s["changeFromV1"] for s in SUCC.values())

withdrawn = [
    {
        "id": "WITHDRAW-COMMANDENVELOPE-FOR-ALL-SCHEMAENVELOPES",
        "history": "v1 MUST-SCHEMA-ENVELOPES-NOT-INHABITED required evaluator3 CommandEnvelope major 3 for every schemaEnvelope row, and probed every envelope file against both CommandEnvelope and StepTermination.",
        "exactSelector": "requirements.json kinds.schemaEnvelope; per-row observables. evaluator3/command-envelope.schema.json is the failure/public-response carrier, not the owner of invocation disclosure, InvocationRecord, StepTermination examples, D9 precedence notes, or identity commit-receipt/availability.",
        "correction": "Keep CommandEnvelope kind=failure as the required inhabitant only for failure/public-from-internal/pinned-purge/purge-replay/D9-complete-failure rows. Single-step/multi-step → InvocationRecord. Invocation disclosure → command-inventory.v3 extraction. Public termination examples → StepTermination. D9 extension precedence → note+vector vs inherited d9-exit-contract.v1.14.json. Durable receipt → identity commit-receipt + availability. Exploratory extra pairings (MutationReceiptV1 vs commit-receipt, BaselineArtifact vs every comparison file, RepairPlanV1 vs min-resolution) are not additional required product work.",
        "classification": "review-quality-correction",
    },
    {
        "id": "WITHDRAW-CELL-STATE-UNAVAILABLE-INDETERMINATE",
        "history": "v1 correction step 6 and SHOULD-PARTIAL-CELL-COMPLETE-CONTRADICTION said set rust-partial clones-fact cellOutcomes to unavailable/indeterminate consistent with unknown Coverage.",
        "exactSelector": "foundation/execution-inputs.schema.v1.json#/$defs/CellProgramOutcomeV1/properties/state enum [complete, partial, unavailable]; execution-inputs-contract.v1.md §4 derive_outcome table; description: state/deficiency/nativeCause MUST equal the derived aggregate. Required unsupported/unavailable/incomplete work is semantic indeterminate via requiredCellDeficiencies — evaluator verdict, not CellProgramOutcomeV1.state.",
        "correction": "indeterminate is not a CellProgramOutcomeV1.state member. For selected universe with a supported-available clones account whose Coverage is not complete, derived state is partial. unavailable is only for enumerator unselected / universe null / provider-unavailable with no returned work. complete + unknown Coverage is EXECUTION_INPUTS_OUTCOME_DERIVE. Withdraw unavailable/indeterminate. Prescribe derived partial (joined to the retained deficiency/nativeCause pair on the Coverage record).",
        "classification": "review-quality-correction",
    },
    {
        "id": "WITHDRAW-TSCONFIGGRAPHHASH-ON-GRAPH-RECORD",
        "history": "v1 said compute tsconfigGraphHash = SHA-256(C(record)) as if it were a TypeScriptConfigGraphV1 field, and prescribed synthesized empty/null entry without saying the hash lives on the universe.",
        "exactSelector": "native-evidence.schemas.v2.json#/$defs/TypeScriptConfigGraphV1 additionalProperties false, required [entryConfigPath, nodes, schemaVersion]; #/$defs/TypeScriptUniverseV2ResolvedInputs/properties/tsconfigGraphHash x-opensip-digest codec C of TypeScriptConfigGraphV1; description: entryConfigPath null exactly when synthesized; nodes minItems 0; configGraphPaths empty under configOrigin=synthesized is on the projection, not the graph.",
        "correction": "Standalone synthesized vector: TypeScriptConfigGraphV1 {schemaVersion:1, entryConfigPath:null, nodes:[]}. Computed identity is SHA-256(C(graph)) recorded as a measured digest. If a universe is also built, that digest binds as TypeScriptUniverseV2ResolvedInputs.tsconfigGraphHash. Do not add tsconfigGraphHash onto the graph. Do not require a new complete Run. synthesizerVersion/synthesizedOptions are universe fields (js-synthesized), not graph fields.",
        "classification": "review-quality-correction",
    },
    {
        "id": "WITHDRAW-NONEMPTY-IMPORT-SUBJECTS",
        "history": "v1 SHOULD-IMPORT-SUBJECTS-EMPTY asked to strengthen RuntimePayloadV1 with at least one mapped imported subject.",
        "exactSelector": "imported-evidence.schema.json#/$defs/RuntimePayloadV1/properties/subjects minItems 0. R-IMPORTED-PAYLOAD-IN-GRAPH requires actual imported payload records as graph members with registered relation and native Coverage, not nonempty subjects.",
        "correction": "Withdraw the population requirement. Empty subjects is schema-legal. Optional advisory: if claiming RuntimePayloadV1, inhabit its closed format enum and required observationWindow object. That is payload-schema inhabitance of the named record, not extra product population.",
        "classification": "review-quality-correction",
    },
    {
        "id": "WITHDRAW-BAN-ON-SYNTHETIC-TARGETATTRIBUTION",
        "history": "v1 query correction said Do not invent TargetAttributionV1; keep unprojectable-fact disclosure where the kit omits the edge.",
        "exactSelector": "query-projection-contract.v3.md §3 Fact law: imports without TargetAttributionV1 omitted with unprojectable-fact. §8 step 4: project from admitted views, retained TargetAttributionV1, and retained payloads. Ignore host.targetAttributions.",
        "correction": "For the existing TS imports fact that has no TargetAttributionV1, disclosure as unprojectable-fact is required and must not be replaced by inventing host.standing attribution. Separately, the consumer may lawfully construct synthetic TargetAttributionV1 + matching retained payload under the published schemas to exhibit a projectable neighbors/path/reach positive. Do not ban that reconstructable case. Do not let the unprojectable note substitute for typed graph.neighbors|path|reach, cursor bind, or renderer parity. Do not assume a root/close_run result.",
        "classification": "review-quality-correction",
    },
    {
        "id": "WITHDRAW-REPLAY-AFTER-PARALLEL-REVIEWER",
        "history": "v1 correction step 6 said export replay.json for every claimed complete positive after the parallel syntax-pilot reviewer lands.",
        "exactSelector": "R-REPLAY-EXPORT / R-FROM-SCRATCH-COMMAND / R-REPLAY-AFTER-ADMISSION: consumer exports replayed inputs, computed proof, and comparison from retained frames. afterExport root admission is a later independent gate. This review does not perform from-export proof reconstruction.",
        "correction": "Replay construction is owned by the consumer. Missing replay.json on ts/rust/syntax-data/rust-partial remains a reconstruction-scope defect of R-REPLAY-EXPORT. Syntax-code.replay.json content stays unreviewed here (parallel reviewer). This review must not wait on, import, or perform that proof.",
        "classification": "review-quality-correction",
    },
    {
        "id": "WITHDRAW-REPAIRPLAN-AS-UNIVERSAL-OWNER",
        "history": "v1 probed repair-descriptor, min-resolution, mutation-replay-scope, clones-negatives, js-body, test-prep-auth all against RepairPlanV1 and treated those stock failures as required.",
        "exactSelector": "Per-row kinds: min-resolution → policy-document.v2 Atom.minResolution + ladders; mutation-replay-scope → MutationReplayScopeV1; test-prep-auth → authorization records; clones-negatives → clone body-identity/grammar custody refusals; RepairPlanV1 is the repair-plan record only.",
        "correction": "Exploratory RepairPlanV1 pairing may be recorded as extra; it is not a separate required failure. Keep the rows explanatory/unexecuted against their actual owners.",
        "classification": "review-quality-correction",
    },
]

must = [
    {
        "id": "MUST-FAILURE-PUBLIC-ENVELOPES",
        "classification": "reconstruction-scope-defect",
        "requirementIds": [
            "R-PINNED-PURGE",
            "R-PUBLIC-FROM-INTERNAL-REFUSAL",
            "R-ENVELOPE-CONFIG-INPUT",
            "R-ENVELOPE-EXTERNAL-INPUT",
            "R-ENVELOPE-HOST-INVALID",
            "R-ENVELOPE-PRODUCER-BOUNDARY",
            "R-FAILURE-ENVELOPES-D9",
            "R-PURGE-REPLAY-OUTPUT-FAILURE",
        ],
        "normativeSelectors": [
            "docs/coop/design-corrections/workflows/schemas/evaluator3/command-envelope.schema.json schemaMajor 3 kind=failure",
            "docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json#/$defs/StepTermination",
            "docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json#/$defs/DomainDetail",
            "docs/v2/contracts/product-v1/workflows-and-surfaces.md §8",
            "docs/coop/artifacts/d9-exit-contract.v1.14.json class/code/exit legality",
        ],
        "finding": "These schemaEnvelope rows require the selected D9/common CommandEnvelope kind=failure composition (complete fields, not {boundary,class} or completeEnvelope:true). Not a missing design law.",
    },
    {
        "id": "MUST-INVOCATION-RECORD-EXAMPLES",
        "classification": "reconstruction-scope-defect",
        "requirementIds": ["R-SINGLE-STEP", "R-MULTI-STEP-DIFFERENT-SELECTIONS"],
        "normativeSelectors": [
            "docs/coop/design-corrections/workflows/schemas/evaluator3/invocation-record.schema.json (schemaFamily opensip.product.invocation, schemaMajor 3, required orderedSteps)",
            "docs/coop/design-corrections/workflows/command-inventory.v3.json",
        ],
        "finding": "Single-step and named multi-step examples must inhabit InvocationRecord, not CommandEnvelope run/failure and not {command,steps:1}.",
    },
    {
        "id": "MUST-INVOCATION-DISCLOSURE-FROM-INVENTORY",
        "classification": "reconstruction-scope-defect",
        "requirementIds": ["R-INVOCATION-DISCLOSURE"],
        "normativeSelectors": [
            "docs/coop/design-corrections/workflows/command-inventory.v3.json (formats, parityFields, flags; command steps)",
            "docs/v2/contracts/product-v1/workflows-and-surfaces.md invocation ownership/cardinality/ordering",
        ],
        "finding": "Reconstruct ownership fields, bounded cardinality, ordering, and applicable output formats from the inventory/contracts. A CommandEnvelope is not the required record.",
    },
    {
        "id": "MUST-PUBLIC-TERMINATION-STEPTERMINATION",
        "classification": "reconstruction-scope-defect",
        "requirementIds": ["R-PUBLIC-TERMINATION-EXAMPLES"],
        "normativeSelectors": [
            "docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json#/$defs/StepTermination (class plus branch contract errorCode/reasonCodes/faultCause/signal)",
        ],
        "finding": "Public termination examples must stock-validate as StepTermination. They need not carry CommandEnvelope outer fields.",
    },
    {
        "id": "MUST-D9-PRECEDENCE-CHECK",
        "classification": "reconstruction-scope-defect",
        "requirementIds": ["R-D9-EXTENSION-PRECEDENCE"],
        "normativeSelectors": [
            "docs/coop/artifacts/d9-exit-contract.v1.14.json",
            "docs/v2/architecture/13-evidence-workflows-and-product-contracts.md",
            "docs/v2/contracts/product-v1/workflows-and-surfaces.md §8 successor-over-inherited for envelope major 3",
        ],
        "finding": "Observable is a note+vector of selected composition vs inherited artifact. Current file lists paths only. Not a CommandEnvelope demand and not a missing design law.",
    },
    {
        "id": "MUST-COMPARISON-AND-BASELINE-CASES",
        "classification": "reconstruction-scope-defect",
        "requirementIds": [
            "R-BASELINE-AUDIT",
            "R-CMP-MISSING",
            "R-CMP-EVIDENCE-CHANGED",
            "R-CMP-EMPTY-RESULT",
            "R-SCOPE-POLICY-ONLY-COMPARISON",
            "R-E0-VS-E1-E3",
            "R-PIVOT-ONLY-FINGERPRINTS",
        ],
        "normativeSelectors": [
            "docs/coop/design-corrections/workflows/schemas/evaluator3/comparison-result.schema.json",
            "docs/coop/design-corrections/workflows/schemas/evaluator3/baseline-artifact.schema.json",
        ],
        "finding": "Case-label literals are not the cases. Baseline-audit → BaselineArtifact; missing/evidence-changed/empty/scope-policy-only → ComparisonResult. E0 vs E1–E3 and pivot-only fingerprints must be exhibited on those records, not {notTheSame:true}.",
    },
    {
        "id": "MUST-AUTHORIZATION-RECORDS",
        "classification": "reconstruction-scope-defect",
        "requirementIds": ["R-TEST-PREP-REPAIR-AUTH"],
        "normativeSelectors": [
            "docs/coop/design-corrections/workflows/schemas/evaluator3/repair.schema.json (authorization, not host execution)",
            "docs/coop/design-corrections/workflows/command-inventory.v3.json authorizationClass",
            "docs/v2/contracts/product-v1/security-and-lifecycle.md / workflows-and-surfaces.md test/prep/repair consent",
        ],
        "finding": "Three labels are not reconstructed authorization records/envelopes.",
    },
    {
        "id": "MUST-CONFIG-GRAPH-SHAPES",
        "classification": "reconstruction-scope-defect",
        "requirementIds": ["R-CONFIG-SYNTHESIZED", "R-CONFIG-CUSTOM-MULTI-BASE", "R-CONFIG-JS-SHARED-BASE"],
        "normativeSelectors": [
            "docs/coop/design-corrections/native/native-evidence.schemas.v2.json#/$defs/TypeScriptConfigGraphV1",
            "docs/coop/design-corrections/native/native-evidence.schemas.v2.json#/x-opensip-config-node-kind-law",
            "docs/coop/design-corrections/native/native-evidence.schemas.v2.json#/$defs/TypeScriptUniverseV2ResolvedInputs/properties/tsconfigGraphHash",
        ],
        "finding": "Exercise the three configuration shapes as TypeScriptConfigGraphV1 plus computed C-digest. Not new complete Runs. Hash is not a graph field.",
    },
    {
        "id": "MUST-REPAIR-CLONE-MINRES-MUTATION",
        "classification": "reconstruction-scope-defect",
        "requirementIds": [
            "R-REPAIR-DESCRIPTOR",
            "R-REPAIR-AUTHORITY-PER-TARGET",
            "R-MIN-RESOLUTION-THREE-LEVELS",
            "R-MIN-RESOLUTION-REPAIR-EVIDENCE",
            "R-MUTATION-REPLAY-SCOPE",
            "R-REPAIR-APPLY-KEY",
            "R-CLONES-NEGATIVE-VECTORS",
            "R-JS-CLONE-BODY-THROUGH-TS",
            "R-HIDDEN-MISMATCH-PER-LANGUAGE",
        ],
        "normativeSelectors": [
            "evaluator3/repair.schema.json (descriptor/plan and per-target authority — not a universal owner)",
            "policy-document.v2.schema.json Atom.minResolution; relation-payload-schemas.v2.json ladders",
            "invocation-record MutationReplayScopeV1 / H('workflow.mutation-intent', …)",
            "identity-schemas.v3.json languageVersionBinding.bodyLanguageByVariant",
        ],
        "finding": "Prose/literals are not executed vectors. Negatives need executed refusals. JS body through TS must be constructed without relabelling languageId. Do not demand RepairPlanV1 for min-resolution or mutation-intent.",
    },
    {
        "id": "MUST-GRAPH-QUERY-THREE-OPS",
        "classification": "reconstruction-scope-defect",
        "requirementIds": ["R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR"],
        "normativeSelectors": [
            "docs/coop/design-corrections/workflows/query-projection-contract.v3.md §§1–8",
            "docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json GraphQueryRequestV1 GraphQueryResponseV1 GraphEvidenceDisclosure GraphOperationResponseContext",
            "docs/v2/contracts/product-v1/workflows-and-surfaces.md §8 query parity fields",
        ],
        "finding": "Need typed neighbors, path, and reach over a retained Run, plus failure envelopes, cursor bind, and renderer parity. Unprojectable-fact disclosure for the existing TS imports fact without TargetAttributionV1 is required for that fact and is not a substitute for the three operations. Synthetic TargetAttributionV1 under the published schema is lawful for a projectable positive. No root result assumed.",
    },
    {
        "id": "MUST-OWNERSHIP-STABILITY-MEASURED-PAIR",
        "classification": "reconstruction-scope-defect",
        "requirementIds": ["R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE"],
        "normativeSelectors": [
            "native-evidence.schemas.v2.json#/$defs/SourceUnitOwnershipV1",
            "fact-identity-policy.v2.json body identity frame",
        ],
        "finding": "Independently recompute body identity under each ownership selection at the same dialect. Literal true / same-variable assignment is not a measured pair.",
    },
    {
        "id": "MUST-REPLAY-EXPORT-EVERY-POSITIVE",
        "classification": "reconstruction-scope-defect",
        "requirementIds": ["R-REPLAY-EXPORT"],
        "normativeSelectors": [
            "requirements.json R-REPLAY-EXPORT observable runs/<id>.replay.json for each claimed complete positive",
            "requirements.json evaluatorReplay / afterExport (consumer constructs; later root admission is separate)",
        ],
        "finding": "Only syntax-code.replay.json exists. Consumer must export replayed inputs/proof/comparison for every claimed positive from their retained frames. This review does not perform that reconstruction.",
    },
    {
        "id": "MUST-ACCEPT-FORBIDDEN-WHILE-UNEXECUTED",
        "classification": "reconstruction-scope-defect",
        "requirementIds": [
            "R-NO-ACCEPT-IF-INCOMPLETE",
            "R-MUST-SHOULD-ADVISORY",
            "R-IDENTIFY-GAPS",
            "R-BLOCKER-NOT-ADJUST",
            "R-VALID-VS-INVALID-VS-EXPLANATORY",
            "R-MEASURED-NOT-COUNTS",
            "R-NEGATIVE-FIRST-REFUSAL",
        ],
        "normativeSelectors": ["requirements.json stopCondition.acceptForbiddenIf", "requirements.json classificationRule"],
        "finding": "ACCEPT-RECONSTRUCTABLE with empty newMustIssues while acceptBlocking reconstruction remains explanatory/failed. Row counts are not acceptance.",
    },
]

should = [
    {
        "id": "SHOULD-RECEIPT-UNBOUND-SYNTHETIC-IDS",
        "classification": "reconstruction-scope-defect",
        "requirementIds": ["R-DURABLE-RECEIPT-AVAILABILITY"],
        "normativeSelectors": [
            "identity-schemas.v3.json#/$defs/commit-receipt",
            "identity-schemas.v3.json#/$defs/availability",
        ],
        "finding": "Nested records stock-validate. run3:abab… and inventoryDigest 11… are unbound placeholders. Join to a retained Run or label an explicit synthetic host observation. Not a CommandEnvelope demand.",
    },
    {
        "id": "SHOULD-CELL-OUTCOME-DERIVED-PARTIAL",
        "classification": "reconstruction-scope-defect",
        "requirementIds": ["R-RUN-RUST-PARTIAL-EMPTY-CLONES", "R-CLONE-DEFICIENCY-PAIRING"],
        "normativeSelectors": [
            "execution-inputs.schema.v1.json#/$defs/CellProgramOutcomeV1/properties/state enum complete|partial|unavailable",
            "execution-inputs-contract.v1.md §4: any supported-available account not complete → partial; complete+partial inventory is EXECUTION_INPUTS_OUTCOME_DERIVE",
            "execution-inputs-contract.v1.md §5: required unsupported/unavailable/incomplete work is semantic indeterminate (requiredCellDeficiencies), distinct from cell state",
        ],
        "finding": "Coverage pairing is the published unknown + input-closure-incomplete / body-language-owner-unenumerated and there is no clones fact2. clones-fact CellProgramOutcomeV1.state=complete is underived. Correct derived state is partial (not unavailable, not indeterminate). Evaluator/proof indeterminacy is a different field.",
    },
    {
        "id": "SHOULD-RUNTIME-PAYLOAD-CLOSED-FIELDS",
        "classification": "reconstruction-scope-defect",
        "advisory": True,
        "requirementIds": ["R-IMPORTED-PAYLOAD-IN-GRAPH"],
        "normativeSelectors": [
            "imported-evidence.schema.json#/$defs/RuntimePayloadV1 format enum, required observationWindow object, required observedPopulation enum, subjects minItems 0",
        ],
        "finding": "import2 is a graph member (original graph-membership obligation). If the payload is claimed as RuntimePayloadV1, inhabit that closed vocabulary. Nonempty subjects is NOT required (minItems 0). v1 nonempty-subjects SHOULD is withdrawn.",
    },
    {
        "id": "SHOULD-CLASSIFICATION-AND-EXECUTED-REFUSALS",
        "classification": "reconstruction-scope-defect",
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
            "R-HOST-CAPTURED-VS-CANDIDATE",
        ],
        "normativeSelectors": [
            "requirements.json R-VALID-VS-INVALID-VS-EXPLANATORY",
            "requirements.json R-NEGATIVE-FIRST-REFUSAL",
        ],
        "finding": "Standing/config rows still need labeled measurements and executed refusals where negative. Not missing design laws.",
    },
]

# probe cross-check
probe_x = [
    {
        "probe": "envelope.CommandEnvelope:* stockOk=false",
        "v1Use": "Treated as required failure for every schemaEnvelope file.",
        "successor": "Required only for failure/public-from-internal/pinned-purge/purge-replay/D9-complete-failure files. Extra pairing for invocation-disclosure, single-step, multi-step, public-termination, receipt-availability, d9-precedence.",
    },
    {
        "probe": "envelope.StepTermination:* stockOk=false",
        "v1Use": "Required for every envelope.",
        "successor": "Required inhabitance for R-PUBLIC-TERMINATION-EXAMPLES and as part of CommandEnvelope.termination on failure envelopes. Not the sole owner of InvocationRecord or commit-receipt.",
    },
    {
        "probe": "receipt-availability.commit-receipt / availability stockOk=true; MutationReceiptV1 stockOk=false",
        "v1Use": "Correctly kept nested identity inhabitance; MutationReceipt pairing was extra.",
        "successor": "Confirm identity commit-receipt/availability as the owning records. MutationReceiptV1 extra pairing withdrawn as a required failure.",
    },
    {
        "probe": "comparison.ComparisonResult:* and BaselineArtifact:* both fail",
        "v1Use": "Both treated as required for every comparison/baseline file including test-prep-auth.",
        "successor": "ComparisonResult for cmp cases; BaselineArtifact for baseline-audit; neither for test-prep-auth.",
    },
    {
        "probe": "repair.RepairPlanV1:* stockOk=false",
        "v1Use": "Applied to min-resolution, mutation, clones-negatives, js-body, test-prep-auth.",
        "successor": "Extra pairing except where the row actually reconstructs a repair plan/descriptor.",
    },
    {
        "probe": "query.* GraphQueryRequestV1/ResponseV1 stockOk=false; measured-neighbors fact-in-ts-store ok=true",
        "v1Use": "Correctly refused typed query completeness; correctly noted real fact2 + unprojectable disclosure.",
        "successor": "Confirmed. Do not ban synthetic TargetAttributionV1 construction; do not let that disclosure replace all three operations.",
    },
    {
        "probe": "store.syntax-data.coverage-records ok=false then later H-frame decode found cvp-clones",
        "v1Use": "Assessed R-RUN-UNAVAILABLE-SEMANTIC executed from the later decode, not from the failed first decoder.",
        "successor": "Confirmed executed via H-frame measurement. First probe was a decoder false-negative, not a consumer failure.",
    },
    {
        "probe": "store.rust-partial.deficiency-pairing first ok=false then pairing found; cell complete remains",
        "v1Use": "Property executed; SHOULD on cell complete.",
        "successor": "Confirmed pairing. Cell-state prescription corrected to derived partial.",
    },
    {
        "probe": "rust-pair.stable-ownership-is-literal-same-assignment ok=false",
        "v1Use": "Aligned with failed disposition.",
        "successor": "Confirmed.",
    },
    {
        "probe": "replay.export-per-claimed-positive ok=false",
        "v1Use": "Aligned with R-REPLAY-EXPORT failed.",
        "successor": "Confirmed. Construction remains consumer-owned.",
    },
    {
        "probe": "h-helper.independent-remint-snapshot-A ok=true; CVE1 5 type families reminted",
        "v1Use": "Marked R-H-HELPER and R-CVE1-EIGHT-TYPES executed.",
        "successor": "Keep executed with measurementKind sampled-independent-encoding. Do not infer totality from the sample.",
    },
    {
        "probe": "34 v1 executed rows had measurement=null",
        "v1Use": "Inferred execution from default/filename.",
        "successor": "Every successor executed row has measurementKind + measurement. Tables/traces not walked are artifact-present-content-unverified, not executed.",
    },
]

self_audit = {
    "standing": "Bounded self-audit of consumer-b.v12-kit-scope-review.v1 before reconstruction authors use it. Not product qualification. Not another whole reconstruction. v1 reports/probes preserved.",
    "originalReviewPath": str(V1 / "output/review.json"),
    "originalReviewVerdict": "SCOPED_WORK_INCOMPLETE",
    "selfAuditVerdict": "REVIEW_QUALITY_CORRECTIONS_APPLIED",
    "successorVerdict": "SCOPED_WORK_INCOMPLETE",
    "reasonSuccessorUnchangedAtTopLevel": "Unexecuted acceptBlocking reconstruction remains. Quality corrections change owners/prescriptions/measurement sufficiency, not the scoped incompleteness.",
    "inputHashes": v1["inputHashes"],
    "v1DispositionCounts": v1["dispositionCounts"],
    "successorDispositionCounts": dict(succ_counts),
    "changeCounts": dict(change_counts),
    "rowAudits": row_audits,
    "withdrawnPrescriptions": withdrawn,
    "confirmedMustGroups": [m["id"] for m in must],
    "probeCrossCheck": probe_x,
    "cellProgramOutcomeLaw": {
        "stateEnum": ["complete", "partial", "unavailable"],
        "notAMember": ["indeterminate"],
        "derive": {
            "enumerator unselected or universe null": "unavailable",
            "selected U, provider-unavailable, no returned work": "unavailable",
            "any inventory partial, or any supported-available account not complete": "partial",
            "all inventories complete and every account complete/inapplicable/unsupported": "complete",
        },
        "semanticIndeterminate": "requiredCellDeficiencies / evaluator verdict — distinct from CellProgramOutcomeV1.state",
        "v1Prescription": "unavailable/indeterminate",
        "successorPrescription": "partial, joined to the retained Coverage deficiency/nativeCause pair",
    },
    "noMissingDesignLawsIdentified": True,
    "didNotWriteConsumerFiles": True,
    "didNotPerformFromExportProof": True,
    "didNotUseOtherSessionsOrRootResults": True,
}

assessed = []
for i, spec in SUCC.items():
    orig = v1a[i]
    assessed.append(
        {
            "id": i,
            "kind": orig["kind"],
            "phase": orig.get("phase"),
            "acceptBlocking": orig.get("acceptBlocking"),
            "consumerClaimedStatus": orig.get("consumerClaimedStatus"),
            "consumerClaimedArtifact": orig.get("consumerClaimedArtifact"),
            "disposition": spec["disposition"],
            "measurementKind": spec["measurementKind"],
            "measurement": spec["measurement"],
            "owningRecord": OWNERS.get(i),
            "v1Disposition": orig["disposition"],
            "changeFromV1": spec["changeFromV1"],
        }
    )

successor = {
    "reviewer": "consumer-b.v12-kit-scope-review.v2 successor of v1 self-audit",
    "verdict": "SCOPED_WORK_INCOMPLETE",
    "standing": "Kit-only reconstruction-scope audit. Not product qualification, implementation authorization, whole-design acceptance, or root admission. Replay construction remains the consumer's from-export work.",
    "supersedes": "consumer-b.v12-kit-scope-review.v1/output/review.json",
    "selfAudit": "consumer-b.v12-kit-scope-review.v2/output/self-audit.json",
    "inputHashes": v1["inputHashes"],
    "consumerClaimedVerdict": "ACCEPT-RECONSTRUCTABLE",
    "consumerClaimedStanding": "Claims are not design authority.",
    "dispositionCounts": dict(succ_counts),
    "assessed": assessed,
    "newMustIssues": must,
    "newShouldIssues": should,
    "withdrawnFromV1": [w["id"] for w in withdrawn],
    "preservedHelperCorrections": v1["preservedHelperCorrections"],
    "unreviewedScope": [
        "Whole recursive syntax-code identity/schema/closure/semantic-replay/root admission (parallel kit-only reviewer; results not used; this review does not perform from-export proof reconstruction).",
        "Whole Run admission of TS, Rust, syntax-data, and rust-partial. Named properties were sampled from retained stores only.",
        "Independent re-derivation of every relation-rung pair, protocol3 row, capability-manifest identity, and count-class application (those consumer tables remain artifact-present-content-unverified).",
        "CVE1 NFC-UTF8-string / array / string-keyed-map independent remint.",
        "Content of syntax-code.replay.json tamper/compare fields.",
        "Any original repository, author models, goldens, prior design reviews, root checks, active builder, or other /tmp/opensip-design-corrections trees.",
    ],
    "futureQualificationNotDemanded": ["F-OS-COMPILER-CRYPTO-SQLITE", "F-SYNTHETIC-TCB", "F-AUTH-HOST"],
    "boundedCorrectionSequence": [
        {
            "step": 1,
            "keep": "Do not start from scratch. Keep C/H/CVE1/lexical/cap-admission/protocol3 helpers, traces, relation tables, helperCorrections, and the five exported Run stores with useful property records.",
        },
        {
            "step": 2,
            "do": "Rebuild failure/public-from-internal/pinned-purge/purge-replay/D9-complete envelopes as CommandEnvelope kind=failure + StepTermination + DomainDetail. Rebuild single-step and multi-step as InvocationRecord schemaMajor 3. Reconstruct invocation disclosure from command-inventory.v3 (formats/parity/cardinality), not as a CommandEnvelope. Validate public termination examples as StepTermination. Check D9 extension precedence as note+vector vs inherited d9-exit-contract.v1.14.json. Keep nested commit-receipt/availability for durable receipt (identity family).",
        },
        {
            "step": 3,
            "do": "Construct TypeScriptConfigGraphV1: synthesized {schemaVersion:1, entryConfigPath:null, nodes:[]}; custom-named other entry with ordered repeated extendsResolved; jsconfig.json entry plus shared-base node with kind from basename law. Record SHA-256(C(graph)) as the computed identity. If a universe is present, bind that digest as TypeScriptUniverseV2ResolvedInputs.tsconfigGraphHash. Do not put tsconfigGraphHash on the graph. Not new complete Runs.",
        },
        {
            "step": 4,
            "do": "Inhabit ComparisonResult for the named comparison cases and BaselineArtifact for baseline-audit. Reconstruct test/prep/repair authorization records (not ComparisonResult). Reconstruct repair descriptor/per-target controls, min-resolution three-level facts/Coverage (policy minResolution + ladders), mutation-intent vs repair-apply keys, JS body through TS without relabelling languageId, and executed clone/hidden-mismatch refusals.",
        },
        {
            "step": 5,
            "do": "Execute graph.neighbors, graph.path, and graph.reach as GraphQueryRequestV1/GraphQueryResponseV1 with GraphEvidenceDisclosure, cursor bind, and CommandEnvelope kind=failure for published query faults. Renderer parity is declared fields over the same ResolvedView {runId}. For the existing TS imports fact without TargetAttributionV1, disclose unprojectable-fact. Optionally construct lawful synthetic TargetAttributionV1 under the published schema for a projectable positive. Ignore host.targetAttributions. Do not assume close_run/root results. Notes must not replace the three operations.",
        },
        {
            "step": 6,
            "do": "Independently recompute body identity under lib-only vs lib+bin ownership at the same dialect. Derive rust-partial clones-fact CellProgramOutcomeV1.state as partial (CLOSED vocabulary complete|partial|unavailable) from unknown Coverage; do not write indeterminate as cell state. Consumer exports replay.json for every claimed complete positive from retained frames; this review does not perform that proof and does not wait on the parallel syntax-pilot reviewer. Do not reset syntax-code bytes.",
        },
        {
            "step": 7,
            "do": "Label remaining standing reconstructions as measurements. Restore valid|invalid|explanatory and executed firstRefusal on negatives. Verdict cannot be ACCEPT-RECONSTRUCTABLE while any acceptBlocking row in this same 123-scope is explanatory, failed, or unverified-content where the original verb required execution.",
        },
    ],
    "same123Scope": True,
    "didNotRepairConsumerFiles": True,
    "didNotSupplyAuthorOracle": True,
    "didNotPerformFromExportProof": True,
}

(V2 / "self-audit.json").write_text(json.dumps(self_audit, indent=2) + "\n")
(V2 / "review.json").write_text(json.dumps(successor, indent=2) + "\n")
print("self-audit rows", len(row_audits), "succ assessed", len(assessed))
print("succ counts", dict(succ_counts))
print("changes", dict(change_counts))
print("must", len(must), "should", len(should), "withdrawn", len(withdrawn))
