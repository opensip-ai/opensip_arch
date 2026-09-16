"""Assemble review.json for the consumer24 native/identity/enumeration/execution-input/zero-config assessment.

Every hash and probe result is read back from retained receipts or recomputed from the read-only inputs.
The dispositions are the author's assessment (nonblind, not acceptance) and cite the probe rows they rest on.
"""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
R = HERE / "receipts"
S37 = Path("/tmp/opensip-design-corrections/candidate-subject.v37")
S38 = Path("/tmp/opensip-design-corrections/candidate-subject.v38")
CONSUMER = Path("/tmp/opensip-design-corrections/consumer-b.v24")


def js(p):
    return json.loads(Path(p).read_text())


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def receipt(label):
    d = R / label
    return {"label": label, **js(d / "command.json"), "exit": int((d / "exit.txt").read_text()), **js(d / "digests.json")}


custody = js(R / "custody/stdout.txt")
p37, p38 = js(R / "probe-items-v37/stdout.txt"), js(R / "probe-items-v38/stdout.txt")
q37, q38 = js(R / "probe-items-v2-v37/stdout.txt"), js(R / "probe-items-v2-v38/stdout.txt")
s1, s2 = p38["sections"], q38["sections"]

OWNER_FILES = [
    "docs/v2/contracts/product-v1/native-evidence.md",
    "docs/v2/contracts/product-v1/identity-and-evidence.md",
    "docs/v2/contracts/product-v1/security-and-lifecycle.md",
    "docs/coop/design-corrections/native/native-evidence.schemas.v2.json",
    "docs/coop/design-corrections/native/native-capability-matrix.v2.json",
    "docs/coop/design-corrections/native/native_evidence_model.v2.py",
    "docs/coop/design-corrections/discovery-defaults.py",
    "docs/coop/design-corrections/foundation/identity-schemas.v3.json",
    "docs/coop/design-corrections/foundation/identity-schemas.v2.json",
    "docs/coop/design-corrections/foundation/identity-model.v3.py",
    "docs/coop/design-corrections/foundation/enumeration-contract.v1.md",
    "docs/coop/design-corrections/foundation/enumeration-plan.schema.v1.json",
    "docs/coop/design-corrections/foundation/enumeration_model.v1.py",
    "docs/coop/design-corrections/foundation/subject-inventory.schema.v1.json",
    "docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md",
    "docs/coop/design-corrections/foundation/execution-inputs.schema.v1.json",
    "docs/coop/design-corrections/foundation/execution_inputs_model.v1.py",
    "docs/coop/design-corrections/foundation/execution_inputs_fixture.v3.py",
    "docs/coop/design-corrections/foundation/incoming-search.schema.v1.json",
    "docs/coop/design-corrections/foundation/evaluator_input_model.v3.py",
    "docs/coop/design-corrections/foundation/evaluator-composition-contract.v3.md",
    "docs/coop/design-corrections/foundation/evaluator_composition_model.v3.py",
    "docs/coop/design-corrections/foundation/evaluator_semantic_fixture.v3.py",
    "docs/coop/design-corrections/foundation/check-semantic-replay.v3.py",
    "docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json",
    "docs/coop/design-corrections/workflows/schemas/policy-document.schema.json",
    "docs/coop/design-corrections/workflows/schemas/policy-document.v2.schema.json",
    "docs/coop/design-corrections/workflows/workflows_model.v1.py",
    "docs/coop/artifacts/fact-identity-policy.v2.json",
    "docs/coop/artifacts/d9-exit-contract.v1.14.json",
]
kit_rows = {f["path"]: f["sha256"] for f in js(CONSUMER / "subject/consumer-input-manifest.json")["files"]}
owner_hashes = [{"path": p, "source37": sha(S37 / p), "source38": sha(S38 / p), "changed37to38": sha(S37 / p) != sha(S38 / p),
                 "inConsumerKit": p in kit_rows} for p in OWNER_FILES]
consumer_read = ["output/blind-review.md", "output/blind-review.json", "output/notes/10-gaps.md",
                 "output/runs/ts-clones-required.replay.json", "output/runs/syntax-code~explicit-endpoint-source.replay.json"]
ids = js(S38 / "docs/coop/design-corrections/foundation/identity-schemas.v3.json")
registered_docs = set()
for body in ids["x-opensip-payload-registry"]["classes"].values():
    if "document" in body:
        registered_docs.add(body["document"])
    for row in body.get("rows", {}).values():
        registered_docs.add(row["document"])

doc = {
    "review": "consumer24 findings M1 M2 M3 S1 S2 S3 S4 A1 A2 A4 A5: native, identity, enumeration, execution-input and zero-configuration owners",
    "authorOrigin": "823bf66b-e92a-4789-ab81-63a1a9dc371d",
    "standing": "NONBLIND bounded substantive assessment by a coauthor. Not independent design acceptance, not blind continuation, not a patch, not product qualification, no readiness claim. No source, live, pin, planning, suite or review-grade edits. The consumer's exports and code were read as diagnostic evidence only, never as an oracle.",
    "custody": {
        "manifests": custody["manifests"],
        "source38ParentManifestSha256": custody["source38ParentManifestSha256"],
        "snapshot37": {k: custody["snapshot37"][k] for k in ("files", "bytes", "exact")},
        "snapshot38": {k: custody["snapshot38"][k] for k in ("files", "bytes", "exact")},
        "kit": {k: custody["kit"][k] for k in ("members", "memberFailures", "unlisted", "membersNotEqualToSource37")},
        "kitMembersChangedIn38": [r["path"] for r in custody["kit"]["membersChangedOrAbsentInSource38"]],
        "delta37to38": custody["delta37to38"],
        "ownerFileHashes": owner_hashes,
        "consumerFilesRead": {p: sha(CONSUMER / p) for p in consumer_read},
        "registeredPayloadSchemaDocuments": sorted(registered_docs),
    },
    "probeEquivalence37vs38": {
        "attempt1": {k: p37["sections"][k] == p38["sections"][k] for k in p38["sections"]},
        "attempt2": {k: q37["sections"][k] == q38["sections"][k] for k in q38["sections"]},
        "probeInputsChanged37to38": sorted(k for k in p38["inputSha256"] if p37["inputSha256"][k] != p38["inputSha256"][k]),
    },
    "failedProbeAttempts": [
        {"receipt": "probe-items-v38 / probe-items-v37 section M2-program-predicate-node-record.validation",
         "defect": "bare-document validation could not resolve urn:opensip:product-v1:workflows:common; a probe error, not an owner verdict",
         "correctedBy": "probe-items-v2-* M2-node-against-each-Predicate-selector (workflows_model.validate_import_record)"},
        {"receipt": "probe-items-v38 / probe-items-v37 section S3-zero-config-syntax-only",
         "defect": "registry rows were not in canonical-set order, and the hand-built syntax-only unit used languageFamily 'syntax' (outside the enum)",
         "correctedBy": "probe-items-v2-* S3-default-selection-and-syntax-only-unit"},
    ],
    "items": {},
    "commands": [receipt(d.name) for d in sorted(R.iterdir()) if (d / "command.json").exists() and (d / "exit.txt").exists()],
    "grantsNothing": True,
}

I = doc["items"]
I["M1"] = {
    "consumerSeverity": "MUST", "disposition": "REAL-DESIGN-GAP (cross-owner composition), MUST confirmed; NOT corrected between 37 and 38",
    "summary": "The default profile requires clones-fact for every unit in every mode; clones-fact's enumeration kind is `file`, whose extent law is every first-party path in the cell workspace (markers, data documents, extensionless files); execution-inputs requires every expected source-path subject to be in a returned partition; and the TypeScript and syntax scope-capability law must disclose language-tier-unsupported/capability-missing for any path the dialect table cannot read. A TypeScript unit always contains tsconfig.json or package.json, so its required clones account can never be complete and the Run can never seal pass. Rust's dialect form has no suffix table, so the same law answers 'supported' for Cargo.toml, README.md and even src/a.ts: the asymmetry the consumer measured is the owner law, not a consumer error.",
    "ownerSelectors": [
        "native-evidence.md s1.4 'Default discovery selects the full registered TS/JS/Rust capability set' (native_evidence_model required_default_capabilities)",
        "foundation/enumeration-plan.schema.v1.json#/x-opensip-kind-derivation/clones-fact and #/x-opensip-file-membership-extent-law/fileKind",
        "foundation/execution-inputs-contract.v1.md s5 applicability table row supported-available (every expected source subject must be a member of a returned partition; mixed complete+unknown is not complete)",
        "foundation/identity-schemas.v3.json#/x-opensip-digest-domains/scopeCapabilityLaw (appliesToDialectForm closed-suffix-table; subjectLaw source-path judged on ALL subjects)",
        "native-evidence.md s1.2 lines 436-445 ('No syntax Run is made blanket-indeterminate')",
    ],
    "probes": {"standing": "helper-level chain over actual owner functions; the consumer's closed Runs corroborate but were not rerun here",
               "clonesFactKinds": s2["M1-enumeration-file-extent-for-tsjs-cell"]["result"]["clonesFactKinds"],
               "tsjsCellFileExtent": s2["M1-enumeration-file-extent-for-tsjs-cell"]["result"]["fileExtentForCellRootDot"],
               "defaultRequiresClonesFact": s1["M1-clones-census-chain"]["result"]["defaultRequiresClonesFact"],
               "expectedClonesCensus": s1["M1-clones-census-chain"]["result"]["expectedClonesCensusOverTsUnitFiles"],
               "scopeCapabilitySupport": s1["M1-clones-census-chain"]["result"]["sourceVariantCapabilitySupport(clones@normalized-body-hash, require_all)"]},
    "consequence": "No default TypeScript/JavaScript unit and no syntax scope containing a non-body file can seal pass; a lawful required result is unreachable. Rust clones scopes over non-Rust files claim complete with no capability gate.",
    "remedyForRoot": [
        "Decide the clones-fact census: a body-readable source-path extent per universe (TypeScript: paths whose suffix is in the dialect table among program members; syntax: paths a selected code grammar reads; Rust: owned .rs sources) rather than the inventory `file` extent, OR keep the census and state that an honestly disclosed unsupported non-body partition answers a required clones account the way unsupported-typed does.",
        "Make the Rust branch symmetric with whichever rule is chosen (today it never gates a non-Rust path).",
        "Affected: native-evidence.md s1.2/s1.4 and s10 scope-capability text; enumeration-plan.schema.v1.json kind derivation/extent law (a registered parameter schema document whose raw SHA-256 enters analysis-spec parameters and PlanId, so a schema-byte change is a successor); execution-inputs-contract.v1.md s5; identity-schemas.v3.json scopeCapabilityLaw prose; reference models enumeration_model/execution_inputs_model/native_evidence_model and their cases.",
    ],
    "limits": "No reference closed Run with a default-selected TypeScript unit exists in the maintained fixtures; the chain is shown at helper level and in prose. Whether the chosen census fix changes any existing Run identity depends on root's choice.",
}
I["M2"] = {
    "consumerSeverity": "MUST", "disposition": "REAL-DESIGN-GAP (wrong record in an identity-bearing annotation) plus a reference validator gap that hid it; MUST confirmed for a conforming literal reader; NOT corrected between 37 and 38",
    "summary": "program-predicate.nodeDigest names workflows/schemas/policy-document.schema.json#/$defs/Predicate (policy major 1) while the node it digests lives in RuleProgramV2. Under the owner's own validator an endpoint atom (source or target) is refused by the v1 selector and admitted by the v2 selector. Identity s3 defines canonical-record as a digest of a NAMED registered record, so a literal reader validates the fragment under the v1 record and cannot close lawful Runs. The reference admits them only because identity-model digest_field returns early for retention=fragment and never applies the named record; the node is validated indirectly through the retained RuleProgramV2 and its digest is recomputed by PROGRAM_PREDICATE_NODE_DIGEST.",
    "ownerSelectors": ["foundation/identity-schemas.v3.json#/$defs/program-predicate/properties/nodeDigest/x-opensip-digest/record",
                       "identity-and-evidence.md s3 representation table canonical-record; retention table fragment (line 450)",
                       "foundation/identity-model.v3.py digest_field `if retention in ('fragment','owner-retained'): return`",
                       "workflows/schemas/policy-document.v2.schema.json#/$defs/Predicate, #/$defs/RuleProgramV2"],
    "probes": {"schemaUnderOwnerValidator": s2["M2-node-against-each-Predicate-selector"]["result"]["rows"],
               "annotation": s1["M2-program-predicate-node-record"]["result"]["nodeDigestAnnotation"],
               "referenceSkipsFragmentRecord": s1["M2-program-predicate-node-record"]["result"]["referenceSkipsFragmentRecordValidation"],
               "closedRunWithEndpointAtom": s1["M2-program-predicate-node-record"]["result"]["closedRunWithEndpointAtom"]},
    "consequence": "Every Run whose program uses a v2-only atom field (endpoint, including every incoming target atom) is unclosable for a reader that honours the annotation; the reference hides this by not validating fragments under their named record.",
    "remedyForRoot": ["Correct the record to workflows/schemas/policy-document.v2.schema.json#/$defs/Predicate.",
                      "State in identity s3 whether a fragment is validated under its named record (and make the reference do exactly that), so the annotation is load-bearing rather than decorative.",
                      "identity-schemas.v3.json is " + ("a registered payload schema document" if "foundation/identity-schemas.v3.json" in registered_docs else "not itself a registered payload schema document") + "; check before editing whether any identity digests its bytes."],
    "limits": "The consumer's failing Run was not rerun; the refusal is reproduced at the schema boundary and the reference acceptance at actual close_run.",
}
I["M3"] = {
    "consumerSeverity": "MUST", "disposition": "REAL-DESIGN-GAP plus EXCLUDED-NORMATIVE-INPUT; MUST confirmed; NOT corrected between 37 and 38",
    "summary": "UnitMembershipV1 units/rows are x-opensip-order sequence, so the schema admits any order, and membershipDigest reaches PlanId. No normative prose states the order. The reference native model sorts units by (rootPath UTF-8 bytes, languageFamily), assigns unitOrdinal = position, and emits rows in path UTF-8 order; the consumer's recorded cb24 choice is byte-identical to that. Reordered memberships are schema-valid with different digests. The optional operational derivation lane of enumeration admission would refuse them, but Run closure (evaluator_input_model -> admit_enumeration) does not pass membership_derivation, so closure never recomputes membership. U-4a points to discovery-defaults.py, which is outside the kit, but that file does not contain the ordering either: it lives only in native_evidence_model.v2.py.",
    "ownerSelectors": ["native/native-evidence.schemas.v2.json#/$defs/UnitMembershipV1 (units, rows: sequence)",
                       "native-evidence.md s1.4 U-1..U-4a (membership without order; U-4a delegates rules to discovery-defaults.py)",
                       "foundation/enumeration-contract.v1.md 'membershipDigest equals C(retained UnitMembershipV1)'",
                       "foundation/evaluator_input_model.v3.py admit_enumeration call (no membership_derivation)",
                       "native/native_evidence_model.v2.py discover_units units.sort / assign_membership sorted(files)"],
    "probes": s1["M3-unit-membership-order"]["result"] | {"schemaValid": {k: v["outcome"] for k, v in s1["M3-unit-membership-order"]["result"]["schemaValid"].items()}},
    "consequence": "Two conforming hosts can mint different PlanIds, and different Run identities, for one repository; the reference Run closure admits either.",
    "includingPythonDecision": "Adding discovery-defaults.py (or the native model) to the kit would make an executable reference the law and still would not publish this order (the order is not in discovery-defaults.py). A normative prose extraction is required: the unit order, unitOrdinal assignment, row, unsupportedFiles and outsideBoundaryFiles order, and memberPackageRoots order, together with the shared pruning and unit-enumeration rules U-4a currently delegates to Python.",
    "remedyForRoot": ["native-evidence.md s1.4: add an ordering law (units by rootPath UTF-8 bytes then languageFamily; unitOrdinal = zero-based position; rows, unsupportedFiles and outsideBoundaryFiles by path UTF-8 bytes; memberPackageRoots by UTF-8 bytes) and replace U-4a's Python delegation with prose.",
                      "Enforce it where Run closure can see it: an explicit order/contiguity check in enumeration admission at closure (no schema-byte change), or an x-opensip-order successor for UnitMembershipV1 in a registered-schema successor (native-evidence.schemas.v2.json is a registered payload schema document).",
                      "Affected: native-evidence.md, foundation/enumeration-contract.v1.md, enumeration_model.v1.py / evaluator_input_model.v3.py, native cases."],
    "limits": "The admit_enumeration full graph was not driven with a reordered membership; closure acceptance is shown by the absence of the derivation argument at the only closure call site and the schema/digest probe.",
}
I["S1"] = {
    "consumerSeverity": "SHOULD", "disposition": "REAL-DESIGN-GAP (unnamed registry) and MISSING VALIDATOR; SHOULD confirmed; NOT corrected between 37 and 38",
    "summary": "Identity s3 and stage-spec.outputSchemaDigest require 'the exact complete registered stage output schema document bytes', but no registry of stage output documents exists and the annotation carries no artifactClass (view.schemaDigests does carry registered-schema-document). The reference's own maintained semantic fixture seals a Run whose stage output schema is a fixture document ($id urn:opensip:fixture:evaluator3-semantic-view) that is not registered, and actual close_run admits it.",
    "ownerSelectors": ["foundation/identity-schemas.v3.json#/$defs/stage-spec/properties/outputSchemaDigest", "identity-and-evidence.md s3 stage-spec paragraph (lines 1201-1214)",
                       "foundation/identity-schemas.v3.json#/x-opensip-payload-registry", "foundation/identity-model.v3.py registered_schema_documents / artifactClass check"],
    "probes": s1["S1-stage-output-schema-registry"]["result"],
    "consequence": "Hosts may name different stage output documents for one Plan; exec-plan2 and therefore seal3/run3 identities diverge while PlanId stays stable.",
    "remedyForRoot": ["Either publish a closed stage-output registry (keyed by producer interface and operation) and annotate outputSchemaDigest with artifactClass registered-schema-document plus a closure membership check, or reword 'registered' to name the producer-interface document the closure actually admits.",
                      "Migrate maintained fixtures that use the fixture stage schema. Affected: identity-schemas.v3.json, identity-and-evidence.md s3, identity-model.v3.py, evaluator_semantic_fixture.v3.py and other fixtures."],
    "limits": "One closed Run was inspected; no second host was simulated.",
}
I["S2"] = {
    "consumerSeverity": "SHOULD", "disposition": "REAL-DESIGN-GAP (unnamed join) with a partial validator; SHOULD confirmed; NOT corrected between 37 and 38",
    "summary": "Closure's body_identity_join requires only that the normalisationVersion blob is retained and equals the frame's raw levelVersion; it never joins that digest to SyntaxGrammarBundleV1.normalizer.specificationDigest. Native context admission does require the syntax normalizer specification to be in the grammar closure tree, but that singular digest is not tied to the per-level versions fact-identity-policy defines, and TypeScript and Rust contexts carry no normalizer record at all. 'The retained specification' is therefore unnamed for every universe.",
    "ownerSelectors": ["native/native-evidence.schemas.v2.json#/$defs/SyntaxGrammarBundleV1/properties/normalizer/properties/specificationDigest",
                       "identity-and-evidence.md s3 bodyIdentity bullets (lines 998-1029) and L1-L3 custody paragraph (1153-1159)",
                       "artifacts/fact-identity-policy.v2.json levelVersionDefinition", "foundation/identity-model.v3.py body_identity_join"],
    "probes": s1["S2-clone-level-specification-join"]["result"],
    "consequence": "A clones fact can name any retained blob as its level specification and close; custody of the normalizer that produced an L1-L3 identity is not bound to the selected grammar/toolchain closure.",
    "remedyForRoot": ["Name the record that carries per-level specification digests for each universe (syntax: a per-level map in the grammar bundle normalizer; TypeScript/Rust: a normalizer record in the native context or the toolchain closure) and add the closure join payload.normalisationVersion ∈ that record.",
                      "Affected: native-evidence.schemas.v2.json (registered payload schema document: successor), native-evidence.md s1.2/s6.3, identity-and-evidence.md s3, identity-model.v3.py, native_evidence_model.v2.py."],
    "limits": "Static source-presence evidence only; no clones Run with a foreign retained level blob was built.",
}
I["S3"] = {
    "consumerSeverity": "SHOULD", "disposition": "REAL-DESIGN-GAP (contradictory owners); SHOULD confirmed, with a possible escalation for root; NOT corrected between 37 and 38",
    "summary": "enumeration-contract s1 promises a default syntax-only unit per directory, and the native mode table says syntax-only serves a repository with no TS or Rust unit. WorkspaceUnitV2 can represent unitKind syntax-only (languageFamily none), and default selection over such a unit requests 10 capability rows. But U-1 mints units only from Cargo.toml/package.json/tsconfig.json/jsconfig.json, discover_units never emits a syntax-only unit, default selection with no units requests zero capabilities, the scope descriptor has no workspace roots, and an explicit '.' without a marker refuses CONFIG.INVALID.",
    "ownerSelectors": ["foundation/enumeration-contract.v1.md s1 'provenance=default-unit' bullet", "native-evidence.md s1.1 mode table syntax-only row and lines 169-179", "native-evidence.md s1.4 U-1 and Config2 join",
                       "native/native-evidence.schemas.v2.json#/$defs/WorkspaceUnitV2/properties/unitKind"],
    "probes": {"attempt1": s1["S3-zero-config-syntax-only"]["result"], "attempt2": s2["S3-default-selection-and-syntax-only-unit"]["result"]},
    "consequence": "A marker-free repository gets an analysis spec with no capability request under zero configuration; syntax-only analysis is reachable only by explicit selection, contrary to the enumeration owner.",
    "severityNoteForRoot": "If an empty default request can seal a successful analysis, this is a silent narrowing and should be re-graded MUST; that depends on host/workflow owners outside this assignment.",
    "remedyForRoot": ["Add a U-1 rule minting one syntax-only unit (languageFamily none, unitKind syntax-only, recognizer and provenance named) for the admitted root when no TS/Rust unit exists (and decide whether directories holding only grammar-readable files inside a TS/Rust repository also get one), or correct enumeration-contract s1 and the mode table to say syntax-only is explicit-only.",
                      "Affected: native-evidence.md s1.1/s1.4, enumeration-contract.v1.md s1, native_evidence_model discover_units/default_capability_selection, security discovery agreement."],
    "limits": "Helper-level only; no marker-free end-to-end analysis was sealed.",
}
I["S4"] = {
    "consumerSeverity": "SHOULD", "disposition": "REAL-DESIGN-GAP (identity-bearing field with no value law); SHOULD confirmed; NOT corrected between 37 and 38",
    "summary": "NativeCoverageAccountV1 requires targetUniverse, and s5 deliberately does not join it, but nothing states the carried value. The owner admission accepts another admitted universe, null or an unbound 64-hex value for every account, and each changes executionInputsDigest; the same mutation of sourceUniverse refuses EXECUTION_INPUTS_COVERAGE_DERIVE. The reference fixture writes the binding universe with a comment that another value is lawful.",
    "ownerSelectors": ["foundation/execution-inputs.schema.v1.json#/$defs/NativeCoverageAccountV1/properties/targetUniverse and x-opensip-external-joins/deliberatelyNotJoined",
                       "foundation/execution-inputs-contract.v1.md s5 'targetUniverse is deliberately not joined' and per-universe attribution clause",
                       "foundation/execution_inputs_model.v1.py sourceUniverse join (no targetUniverse check)"],
    "probes": s1["S4-native-account-target-universe"]["result"],
    "consequence": "Conforming hosts can mint different executionInputsDigest, proof3, seal3 and run3 identities for one Run, with no semantic difference.",
    "remedyForRoot": ["State the carried value (for example the binding universe for same-only relations and one account per admitted target universe, or null meaning 'not constrained') and join it at admission; or drop the field in an execution-inputs schema successor.",
                      "Affected: execution-inputs.schema.v1.json (registered? " + ("yes" if "foundation/execution-inputs.schema.v1.json" in registered_docs else "not in the payload registry") + "), execution-inputs-contract.v1.md s5, execution_inputs_model.v1.py, fixtures."],
    "limits": "The fixture graph's accounts are same-universe; the admission probe is helper-level, not a sealed Run.",
}
I["A1"] = {
    "consumerSeverity": "advisory", "disposition": "CONFIRMED; advisory retained, with S4 as its identity-bearing instance",
    "summary": "execution-inputs.schema.v1.json has 16 and incoming-search.schema.v1.json 3 bare 64-hex positions with no x-opensip-digest annotation and no document-level digest law. The closing digest law explicitly governs identity-schemas.v3 (extended by the native bundle and the relation document). The reference walk passes unannotated hex in these foundation records silently; several are joined by explicit admission code, but the representation of each is not published.",
    "ownerSelectors": ["identity-and-evidence.md s3 'The closing digest law' (lines 405-418) and relation-payload paragraph (lines 858-872)",
                       "foundation/execution-inputs.schema.v1.json", "foundation/incoming-search.schema.v1.json"],
    "probes": s1["A1-unannotated-hex-fields"]["result"],
    "remedyForRoot": ["Extend the closing law (or a document-level x-opensip-digest-law) to these foundation documents and annotate each position, or state per field that admission joins it and which representation applies."],
    "limits": "Static walk; joins in admission code were not enumerated field by field.",
}
I["A2"] = {
    "consumerSeverity": "advisory", "disposition": "CONFIRMED; advisory (no semantic effect today)",
    "summary": "enumeration-plan.schema.v1.json names identity-schemas.v2.json (including the scopeDigest canonical-record `document`, beside bundle `identity`) and subject-inventory.schema.v1.json names it in a description. The referenced $defs scope-descriptor, LogicalPath and Text, and the languageModes map keys, are canonically equal in v2 and v3.",
    "ownerSelectors": ["foundation/enumeration-plan.schema.v1.json#/properties/scopeDigest/x-opensip-digest/record and lines 175, 185, 218", "foundation/subject-inventory.schema.v1.json line 429"],
    "probes": s1["A2-identity-v2-selector-drift"]["result"],
    "remedyForRoot": ["Retarget to identity-schemas.v3.json in the next enumeration-plan/subject-inventory schema successor. enumeration-plan.schema.v1.json's raw bytes enter analysis-spec parameters and PlanId, so a text-only edit is a successor, not a correction in place."],
    "limits": "Equality holds for the three named defs and the language-mode keys only.",
}
I["A4"] = {
    "consumerSeverity": "advisory", "disposition": "CONFIRMED UNDECIDED; recommend re-grading to SHOULD because snapshot2 identity depends on it",
    "summary": "Identity s3 defines snapshot2 over the sorted source inventory and says nothing about pruned trees. Native U-4 lets pruned-tree files appear as host-ignore-convention rows when the inventory holds them, and an inventory without them is equally admissible. U-4a and security S3 A-5 decide only that bytes a program actually reads from a pruned tree enter the snapshot read set. Whether unread node_modules or Cargo target bytes enter sourceInventory is decided nowhere.",
    "ownerSelectors": ["identity-and-evidence.md s3 identity table snapshot row (line 179)", "native-evidence.md s1.4 U-4 and U-4a (lines 637-678)", "security-and-lifecycle.md S3 'Pruned trees and the read set (A-5)' (lines 266-273)"],
    "probes": s1["A4-pruned-tree-inventory"]["result"],
    "remedyForRoot": ["Decide in identity s3 (with security S3): sourceInventory = custody-walked first-party files plus exactly the read-set bytes, excluding unread pruned-tree bytes, or the opposite, and make membership admission refuse the other form."],
    "limits": "No snapshot was minted both ways.",
}
I["A5"] = {
    "consumerSeverity": "advisory", "disposition": "CONFIRMED; recommend re-grading to SHOULD (universe identity keys). The consumer's stated choice diverges from the reference derivation in 4 of 8 probed configurations",
    "summary": "native-evidence.md defines what allowJs and checkJs mean and lists jsAdmittedToProgram/jsDiagnosticsEnabled as universe keys that must agree with the context, but never states their derivation. The reference derives jsAdmittedToProgram = allowJs AND at least one JS root file, and jsDiagnosticsEnabled = checkJs. The consumer chose allowJs, and allowJs AND checkJs, which differ when allowJs is set with no JS roots or checkJs is set without allowJs.",
    "ownerSelectors": ["native-evidence.md s1.2 lines 516-524; s2 universe field list (lines 1208-1213); context agreement (lines 1413-1418)", "native/native_evidence_model.v2.py typescript_mode"],
    "probes": s1["A5-typescript-js-flags"]["result"],
    "consumerHelperNote": "Divergence is recorded against the reference derivation, which is not itself published law; whether the consumer's Runs reach the diverging configurations was not checked.",
    "remedyForRoot": ["Publish the derivation in native-evidence.md s1.2/s2 (and decide the checkJs-without-allowJs case against the pinned compiler's option semantics rather than the model)."],
    "limits": "Helper-level; no universe was bound through bind_typescript_universe with the diverging values.",
}
doc["summaryTable"] = {k: v["disposition"] for k, v in I.items()}
doc["crossOwnerNotes"] = [
    "M1, M3, S2 and A2 remedies touch documents whose raw bytes are identity-bearing (enumeration-plan.schema.v1.json as a parameter schema; native-evidence.schemas.v2.json as a registered payload schema). Prose and admission corrections can land without byte changes; schema-byte corrections are successors that re-mint identities.",
    "M2's fix is a one-selector correction, but the reference validator that skipped fragment records must change with it or the annotation stays unchecked.",
    "S1 and S4 need no new vocabulary, only a named registry or value law plus the closure/admission check the reference currently lacks.",
]
doc["limits"] = [
    "Finite corpus: each probe uses small constructed inputs or the maintained semantic fixture; no claim covers all repositories, universes or relation combinations.",
    "Helper, schema, closure and static standings are kept separate per probe; only M2 and S1 use actual close_run.",
    "The consumer's exported Runs were read for two items only as diagnostics and not rerun; root validates them separately.",
    "No independent source38 review runtime was read or influenced.",
    "Not acceptance, not readiness, and no patch.",
]
text = json.dumps(doc, indent=1, default=str) + "\n"
(HERE / "review.json").write_text(text)
print(json.dumps({"sha256": hashlib.sha256(text.encode()).hexdigest(), "commands": len(doc["commands"]),
                  "probeEquivalence": doc["probeEquivalence37vs38"], "registeredDocs": sorted(registered_docs),
                  "ownerChanged37to38": [r["path"] for r in owner_hashes if r["changed37to38"]]}, indent=1))
