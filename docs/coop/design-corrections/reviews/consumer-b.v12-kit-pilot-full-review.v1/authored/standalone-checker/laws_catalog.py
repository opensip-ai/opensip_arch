"""Applicable structural/identity/retained-closure laws indexed to assertions.

Semantic evaluator replay laws are catalogued as outside this bounded review.
"""

APPLICABLE_LAWS = [
    {
        "id": "L-BLOB-REHASH",
        "citation": "identity-and-evidence.md§3 raw-artifact / H frame store keyed by SHA256 of exact bytes",
        "assertion": "Every blobs[key] base64-decodes; SHA256(bytes)==key; length matches objectTable claim when present",
    },
    {
        "id": "L-H-FRAME",
        "citation": "identity-and-evidence.md§3 H(D,X) framing; closing digest law",
        "assertion": "h-identity blobs start with ASCII(opensip.product.v1)||00||ASCII(D)||00||uint64BE(len(C(X)))||C(X); declared length equals remainder; C(parse)==remainder; SHA256(frame)==digest; domain in the annotation domain or domain set",
    },
    {
        "id": "L-C-LEXICAL",
        "citation": "identity-and-evidence.md§3; admission-and-qualification.md§1",
        "assertion": "Raw C(X) refuses duplicate keys, floating/exponent tokens, -0, nonfinite, malformed UTF-8, non-scalar Unicode; integers [-2^63, 2^64-1]; descriptor <=4MiB; depth<=32",
    },
    {
        "id": "L-C-ENCODE",
        "citation": "identity-and-evidence.md§3 canonical JSON",
        "assertion": "UTF-8 byte-ordered keys, no whitespace/trailing newline, no Unicode normalisation, shortest decimal integers, unescaped scalars, escapes quote/backslash/b/t/n/f/r and lowercase \\u00xx for other C0, slash unescaped; arrays in admitted order",
    },
    {
        "id": "L-SCHEMA-KEYWORDS",
        "citation": "identity-and-evidence.md§3; identity-schemas.v3.json x-opensip-order / x-opensip-digest",
        "assertion": "Every reachable typed record validates against its owning schema including published kit keywords; stock jsonschema pass is not admission",
    },
    {
        "id": "L-DIGEST-CLOSED",
        "citation": "identity-and-evidence.md§3 closing digest law",
        "assertion": "Every 64-hex field in identity-schemas.v3 has x-opensip-digest; representation in {raw-artifact, canonical-record, h-identity, capability-manifest-id}; by-domain is a selector; retention in {preimage, fragment, derived, owner-retained}",
    },
    {
        "id": "L-ORDER",
        "citation": "identity-and-evidence.md§3 x-opensip-order closed vocabulary",
        "assertion": "Registered arrays obey sequence|canonical-set|canonical-order|utf8|path|numeric|ordinal|predicate|ruleId|waiverId|{by:[...]}; unique sort keys except sequence and canonical-order",
    },
    {
        "id": "L-PAYLOAD-REGISTRY",
        "citation": "identity-and-evidence.md§3 payload registry; identity-schemas.v3.json#/x-opensip-payload-registry",
        "assertion": "payloadSchemaDigest is SHA256 of the named full document bytes; payload validates at the row selector; unregistered key refuses; codec C",
    },
    {
        "id": "L-PARAM-SELECTION",
        "citation": "identity-and-evidence.md§3 parameter class selectionCardinality; evaluator3 required rows",
        "assertion": "At most one analysis-spec parameter per registered row; evaluator3 requires enumeration-plan and emission-plan; ScopeDocumentV1 != scope-descriptor",
    },
    {
        "id": "L-PLAN-BUDGET",
        "citation": "identity-and-evidence.md§3 Plan deterministic budget",
        "assertion": "plan.budget equals, exactly and by type, resolved semantic configuration analysis.budget",
    },
    {
        "id": "L-PLAN-CONFIG-SCOPE",
        "citation": "identity-and-evidence.md§3 snapshot/Plan config and scope agreement",
        "assertion": "plan.resolvedConfigDigest==snapshot.resolvedConfigDigest and plan.scopeDigest==snapshot.scopeDigest; every visited record joins the Run snapshot/Plan",
    },
    {
        "id": "L-CTX-SET",
        "citation": "identity-and-evidence.md§3 native context set",
        "assertion": "retained context frames == plan.nativeContextDigests exactly; universe nativeContextId is sha256: plus a Plan member",
    },
    {
        "id": "L-NATIVE-ADMIT",
        "citation": "identity-and-evidence.md§3 re-run admit_native_context / bind_*; native-evidence.md§1.2/§2.3/§2.4/§11/§14",
        "assertion": "Frame retention is not admission; re-run native context admission and universe binding over retained descriptors/trees; typed native refusal is a Run refusal",
    },
    {
        "id": "L-CLOSURE-JOINS",
        "citation": "identity-and-evidence.md§3; identity-schemas.v3.json domainSets closureJoins; closureKinds",
        "assertion": "toolClosure.closureId is retained closure2 kind=toolchain; typescriptStdlibMerkleRoot/rustcDevLlvmDigest are closure2 suffixes of kind stdlib/rust-dev-llvm; grammar closure kind=grammar",
    },
    {
        "id": "L-COMPILER-VERSION",
        "citation": "native-evidence.md§11 and §2.3/§2.4 native.native-context-compiler-version-not-from-manifest",
        "assertion": "compilerVersion/rustcVersion/parserVersion equals the admitted tool/grammar closure semanticVersion; no per-language exception",
    },
    {
        "id": "L-NESTED-PREIMAGES",
        "citation": "identity-and-evidence.md§3 nested native semantic identities; domainSets nestedIdentities/nestedRecords/blobJoins",
        "assertion": "dependency-source-set, file manifests+member bytes at declared length, unified-features, cargo-config-projection+projected file, prepared-output rows, source-unit-ownership are retained frames/records, not opaque strings",
    },
    {
        "id": "L-SNAPSHOT-JOINS-NATIVE",
        "citation": "identity-and-evidence.md§3 native snapshotJoins",
        "assertion": "configGraphPaths, replacedSnapshotConfigs, crateRootPaths are inventoried; lockfile path+contentSha256 match inventory",
    },
    {
        "id": "L-FACT2-C",
        "citation": "identity-and-evidence.md§3 fact2 payload encoding; relation-payload-schemas.v2.json",
        "assertion": "fact2 payloads are C; payloadSchemaDigest is the relation document file digest; resolution is a ladder rung; universeRule same-only requires equal universes; ladder is the explicit array not rungs field-rules",
    },
    {
        "id": "L-ANCHOR-LAW",
        "citation": "identity-and-evidence.md§3 anchorLaw; relation-payload-schemas.v2.json#/x-opensip-relation-registry/anchorLaw",
        "assertion": "source-text >=1 anchors; clones ==1; inventory ==0; anchors name inventoried blobs; source-text UTF-8/range; inventory never vacuously true at zero",
    },
    {
        "id": "L-REL-SNAPSHOT-JOINS",
        "citation": "identity-and-evidence.md§3 relation snapshotJoins",
        "assertion": "file path/digest/length/retained bytes join inventory; package manifestPath inventoried; vcs-change path inventoried unless deleted",
    },
    {
        "id": "L-CLONES-BODY",
        "citation": "identity-and-evidence.md§3 clones body recipe; fact-identity-policy.v2.json#/canonicalisationSchema/byteGrammar",
        "assertion": "bodyIdentity frame retained and rehashed; domainTag, levelId, raw-32 levelVersion, languageId from body not engine, languageVersion=SHA256(C(derived body-language-version)); L0 double length prefix; L1-L3 stream framing",
    },
    {
        "id": "L-BODY-DIALECT",
        "citation": "identity-and-evidence.md§3 languageVersionBinding; native-evidence.md§11",
        "assertion": "TS/syntax closed-suffix-table longest match; Rust ownership selection, no partial-enumeration dialect, no fast path; selected owners' effective editions agree",
    },
    {
        "id": "L-SYNTAX-CAPABILITY",
        "citation": "native-evidence.md§1.2; identity-schemas.v3.json scopeCapabilityLaw",
        "assertion": "syntax facts gated by selected grammar rows except inventory; unsupported scopes coverage=unknown, deficiency=language-tier-unsupported, nativeCause=capability-missing; data-document cannot bear code/clone facts",
    },
    {
        "id": "L-COVERAGE-PARTITION",
        "citation": "identity-and-evidence.md§3; relation-payload-schemas.v2.json coveragePartitionLaw",
        "assertion": "Per view, scopes sharing (snapshotId, relation, resolution, sourceUniverse, targetUniverse) have disjoint subjects; SUBJECT_SCOPE_PARTITION_OVERLAP",
    },
    {
        "id": "L-COVERAGE-TOTALITY",
        "citation": "identity-and-evidence.md§3; relation file coverageTotality; native-evidence.md§1.2",
        "assertion": "complete file@enumerated requires a same-tuple fact for every inventoried subject; matchOn is the full tuple; COVERAGE_INVENTORY_TOTALITY_OMITS_PATH",
    },
    {
        "id": "L-RC6",
        "citation": "native-evidence.md§4.3 RC-6; CoverageResultV3",
        "assertion": "coverage=complete implies resolutionCompleteness.examinedExhaustive=true; not an equality with resolution completeness",
    },
    {
        "id": "L-SSC",
        "citation": "identity-and-evidence.md§3 subjectScopeCommitment; native-evidence.md§4.1a",
        "assertion": "subjectScopeCommitment is sha256: plus the 64-hex suffix of the same admitted scope2 H identity",
    },
    {
        "id": "L-CITATIONS",
        "citation": "identity-and-evidence.md§3 finding citations cannot introduce extra authoritative roots",
        "assertion": "fact/coverage citations in evaluated views; import citations Plan-selected and in evaluationInputRefs; witness citations of this proof; blob citations explicit eval inputs",
    },
    {
        "id": "L-RUST-COMPILER-VER",
        "citation": "native-evidence.md§11 (both languages); §2.3/§2.4 admit_native_context",
        "assertion": "NativeContextV2.toolchain.rustcVersion equals admitted toolchain closure semanticVersion",
    },
    {
        "id": "L-PRED-INPUT-SUBSET",
        "citation": "identity-and-evidence.md§3 Predicate input refs are a subset of evaluationInputRefs",
        "assertion": "Every predicateProofs[].inputRefs member is in evaluationInputRefs; no undocumented per-domain exception",
    },
    {
        "id": "L-IMPORT-SET",
        "citation": "identity-and-evidence.md§3 semantic-evidence.importIds; every evaluated import belongs to Plan",
        "assertion": "evidence.importIds repeats plan.importIds exactly; every Plan import is in evaluationInputRefs",
    },
    {
        "id": "L-CLOSURE-MEMBERSHIP",
        "citation": "identity-schemas.v3.json#/x-opensip-digest-domains/closureMembership and closureKinds",
        "assertion": "Direct closures in plan.semanticClosures; fact.producer=view.producer; proof.evaluator=seal.evaluator; kinds match byField",
    },
    {
        "id": "L-ACYCLIC",
        "citation": "identity-and-evidence.md§3 acyclic graph",
        "assertion": "proof excludes EvidenceId/RunId; evidence may include proof; seal includes both; Run includes seal",
    },
    {
        "id": "L-PROGRAM-PREDICATE",
        "citation": "identity-and-evidence.md§3 program-predicate node addressing",
        "assertion": "Addresses p / a.i / a.0; nodeDigest=SHA256(C(addressed Predicate)); childPredicateIds are operand addresses; ruleProgramDigest equals proof",
    },
    {
        "id": "L-CAP-ID",
        "citation": "identity-and-evidence.md§3; capability-manifest-domains.v2.json recipe; delivery.v4 CAP-MANIFEST-ID-V1",
        "assertion": "capabilityManifestId = SHA256(UTF8(opensip.capability-manifest.v1)||00||committed CVE1 bytes); derived from retained capabilityManifestBytesDigest",
    },
    {
        "id": "L-CAP-GATES",
        "citation": "capability-manifest-domains.v2.json ADM-TYPE/ADM-CLOSED/ADM-DOMAIN/ADM-ORDER",
        "assertion": "Exact JSON type, closed records vs maps, registry membership by exact NFC UTF-8 bytes, ordered collections already canonical; relation domain includes unresolved-edge; ladders drift-checked to relation registry",
    },
    {
        "id": "L-COMPONENT-PROFILE",
        "citation": "security-and-lifecycle.md#S1/#S2; component-manifest-schemas.v11.json manifestSchema (prose field table); security-completion.v1.md§2.1",
        "assertion": "closure.manifestDigest is SHA256 of exact stored manifest bytes (no product-C decoder); metadata profile NFC/i64; required prose fields; no embedded signature; tree projects type=file TreeCommitment rows to Blob path/digest/length",
    },
    {
        "id": "L-PROFILES-NEVER-MIXED",
        "citation": "security-and-lifecycle.md#S2",
        "assertion": "Signed security metadata uses opensip-metadata-canonical.1; product descriptors use identity C; a decoder for one never admits the other",
    },
    {
        "id": "L-EXECUTION-INPUTS",
        "citation": "execution-inputs-contract.v1.md; identity-schemas.v3.json proof.executionInputsDigest",
        "assertion": "ExecutionInputsV1 retained as canonical-record; planId/executionPlanId/analysisSpecDigest join the Run; selectedRefs forbid proof/finding/seal/run/evidence; omitted expected cell outcome is structural",
    },
    {
        "id": "L-VCS-INV",
        "citation": "identity-and-evidence.md§3 vcs-observation.sourceInventoryDigest",
        "assertion": "Equals SHA256(C(snapshot.sourceInventory))",
    },
    {
        "id": "L-PARTIAL-CLONES",
        "citation": "identity-and-evidence.md§3 selected scope vs incomplete enumeration; native-evidence.md§11",
        "assertion": "enumeration=partial admits no body dialect and must not claim complete clones Coverage",
    },
    {
        "id": "L-REPLAY-OUTSIDE",
        "citation": "this bounded review; identity-and-evidence.md§4; charter Phase 9 evaluator replay",
        "assertion": "Full semantic proof replay is outside structural admission; a structurally admitted graph is not a complete accepted Run",
    },
]
