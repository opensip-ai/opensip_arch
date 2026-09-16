"""Profiles, private representation, handwritten admission catalog (with executable parameters), commitment map,
state machines for the native wire-carrier author candidate 03. Rule `params` are READ by tools/admission_ref.py,
tools/representability.py and wirecodec.lexical, so a changed parameter changes executed behaviour. Normative text that
restates a structure (lexical rule text, path-member rule text) is RENDERED from that structure and check.py requires
the published text to equal the rendering (review-02 A-3)."""

from common import NODE, ORDERS

PROFILES = {
    "ts2-cbor": {
        "protocol": "typescript-semantic", "major": "2",
        "source": {"pin": "delivery2", "selector": "$.typescriptSemanticSubstrate.providerProtocol.wireSchema.canonicalCbor"},
        "dataModel": ["null", "false", "true", "uint64", "negative-int64", "UTF-8-NFC-text", "byte-string", "definite-array", "definite-text-keyed-map"],
        "negativeIntegers": "DECODABLE: major type 1 in -2^63..-1 is inside the closed data model; no TS2 carrier member has a negative-integer type, so every negative integer in a TS2 payload refuses as a type mismatch (PROVIDER.PROTOCOL_VIOLATION).",
        "forbidden": ["floating-point", "tags", "indefinite-length items", "non-shortest integer or length arguments", "duplicate map keys", "non-text map keys", "invalid UTF-8", "non-NFC text", "unknown map fields", "simple values other than false/true/null"],
        "mapOrder": "ascending bytewise order of each key's deterministic-CBOR encoding",
        "frameIntegrity": "uint64 big-endian payload length, 32 raw SHA-256 payload bytes, then one canonical-CBOR payload",
        "decodeRule": "decode once under the host-state-selected closed carrier; re-encode and require byte equality",
    },
    "rust3-cbor": {
        "protocol": "rust-semantic", "major": "3",
        "source": {"pin": "rust2", "selector": "$.canonicalCbor"},
        "dataModel": ["null", "false", "true", "uint64", "UTF-8-NFC-text", "byte-string", "definite-array", "definite-text-keyed-map"],
        "negativeIntegers": "FORBIDDEN at decode: any CBOR major type 1 item refuses before carrier typing (rust2 canonicalCbor.forbidden[0]).",
        "forbidden": ["negative integers", "floating point", "tags", "undefined and unassigned simple values", "indefinite-length items", "non-shortest integer or length arguments", "duplicate map keys", "non-text map keys", "invalid UTF-8", "non-NFC text", "unknown map fields"],
        "mapOrder": "length of encoded key first, then bytewise",
        "frameIntegrity": "8-byte big-endian payload length, 32 raw SHA-256 payload bytes, canonical-CBOR payload (40-byte prefix)",
        "decodeRule": "retain payload bytes; decode once under the host-state-selected closed carrier; re-encode and require byte equality",
    },
    "mapOrderEquivalence": "For text keys the two map-order rules select the same order: a deterministic-CBOR text key starts with its length header, so bytewise order of encoded keys is length-first then bytewise. check.py proves it over every carrier member name and random keys.",
    "notProvedByJsonSchema": ["NFC", "UTF-8 byte bounds (maxLength counts scalars)", "shortest encodings", "map order", "duplicate keys", "byte strings", "negative-integer profile", "lexical path and packageKey admission", "domain joins, echoes and commitments"],
}

# ---------------------------------------------------------------- RF-3: executable pattern dialect
PATTERN_DIALECT = {
    "standing": "Normative for every `pattern` in wire-carriers.v1.json and every pattern reachable from an extern it references (the registered schema documents are JSON Schema 2020-12, whose `pattern` keyword is an ECMA-262 regular expression).",
    "engine": "ECMA-262 RegExp",
    "flags": "u",
    "evaluation": "new RegExp(pattern, flags).test(value) over the whole NFC text value; a pattern is not implicitly anchored",
    "lineTerminators": ["U+000A", "U+000D", "U+2028", "U+2029"],
    "semantics": {
        "dot": "any scalar except the four line terminators (the s flag is NOT set)",
        "dollar": "end of input only (the m flag is NOT set); unlike Python re it never matches before a final U+000A",
        "whitespaceClass": "\\s is ECMA-262 WhiteSpace plus LineTerminator: U+0009 U+000A U+000B U+000C U+000D U+0020 U+00A0 U+1680 U+2000-U+200A U+2028 U+2029 U+202F U+205F U+3000 U+FEFF (not U+0085)",
    },
    "referenceEngine": {"path": NODE["path"], "sha256": NODE["sha256"], "bytes": str(NODE["bytes"]), "versions": NODE["versions"],
                        "probe": "tools/ecma_probe.js", "unpinnedDynamicLibraries": NODE["dynamicLibraries"]},
    "referenceTranslation": "tools/wirecodec.py ecma_to_python: finite translation for the construct set in patternSites (literals, escapes, \\uXXXX, classes, [\\s\\S], \\s, \\S, ., ^, $, (?: (?= (?! groups, alternation, quantifiers); any other construct or flag refuses. check.py runs the reference engine and the translation over every patternSites pattern and a newline/terminator corpus and requires identical results, and replays the independent review-02 engine output.",
    "lowering": "The Rust `regex` crate has no lookaround, and its `.` and `\\s` differ from ECMA-262. A generator MUST implement every loweringRequired site as an equivalent handwritten check with the ECMA-262 semantics above (anchored hex/prefix patterns lower to fixed-length ASCII checks); it must not drop a pattern, evaluate it with another dialect, or substitute a different language.",
    "supplementary": "Where a text type carries `lexical`, the lexical rule is normative and any pattern on the same value is supplementary; a value satisfying the pattern but failing the lexical rule refuses.",
    "patternSites": "FILLED BY build.py: the closed list of every reachable pattern site {location{document,pointer}, pattern, negated, constructs, lower}",
    "loweringRequired": "FILLED BY build.py: the closed sublist of patternSites with lower=true",
}

# ---------------------------------------------------------------- A-3: structured lexical rules
LEXICAL_RULES = {
    "logical-path-segments": {"kind": "segments", "separator": "/", "forbiddenScalars": ["\u0000", "\\"], "forbiddenSegments": ["", ".", ".."],
                              "maxSegmentScalars": "255", "owner": "identitySchemas3 #/$defs/LogicalPath (declarative segment grammar)"},
    "canonical-path-segments": {"kind": "segments", "separator": "/", "forbiddenScalars": ["\u0000", "\\"], "forbiddenSegments": ["", ".", ".."],
                                "firstSegmentForbiddenPattern": "^[A-Za-z]:", "owner": "rust2 wireSchema.definitions.CanonicalPath.rule"},
    "package-key": {"kind": "package-key", "separator": " ", "nameVersionForbidAtOrBelow": "32",
                    "owner": "native_evidence_model.v2 dependency_source_set_admit key f'{name} {version} {sourceId}'",
                    "deliberate": "U+007F DEL and the C1 controls U+0080..U+009F are above U+0020 and are deliberately admitted in name and version: they break neither key injectivity nor tuple/key order agreement (review-02 A-4)"},
}


def render_lexical(rule):
    if rule["kind"] == "package-key":
        return (f"exactly name SEP version SEP sourceId with SEP = {rule['separator']!r}; name and version are non-empty and contain no scalar "
                f"<= U+{int(rule['nameVersionForbidAtOrBelow']):04X}; sourceId is the remainder after the second SEP (possibly empty, may contain SEP); "
                + rule["deliberate"])
    parts = [f"split on {rule['separator']!r}", "no segment is one of " + ", ".join(repr(s) for s in rule["forbiddenSegments"]),
             "no scalar anywhere is one of " + ", ".join(f"U+{ord(c):04X}" for c in rule["forbiddenScalars"])]
    if "maxSegmentScalars" in rule:
        parts.append(f"every segment has at most {rule['maxSegmentScalars']} Unicode scalars")
    if "firstSegmentForbiddenPattern" in rule:
        parts.append(f"the first segment does not match the ECMA-262 pattern {rule['firstSegmentForbiddenPattern']} (drive prefix)")
    return "; ".join(parts)


for _r in LEXICAL_RULES.values():
    _r["text"] = render_lexical(_r)

PRIVATE_REPRESENTATION = {
    "standing": "Private carrier choices for one generator recipe; none is a wire change or a wire name.",
    "uint64": {"rust": "u64", "typescript": "bigint", "json-vector": "JSON integer (vectors only)"},
    "text": {"rust": "String (NFC, byte bounds and lexical rules checked by admission)", "typescript": "string"},
    "bytes": {"rust": "protocol::wire::ByteString(Vec<u8>) newtype; codec accepts only CBOR major type 2; length prefix checked against maxBytes before allocation",
              "typescript": "Uint8Array (owned copy, never a view into the frame buffer)",
              "json-vector": "lowercase hex in a member named <member>Hex, JSON vectors only; never a JSON array, base64 or hex on the wire and never a generated JSON carrier"},
    "bool": {"rust": "bool", "typescript": "boolean"},
    "null": {"rust": "unit (only inside nullable or variant-record branches)", "typescript": "null"},
    "nullable": {"rust": "Option<T> serialized as present CBOR null; never skipped", "typescript": "T | null, property required"},
    "optional": {"rust": "Option<T> with skip-when-absent; absent is not null", "typescript": "prop?: T under exactOptionalPropertyTypes; undefined never serialized"},
    "array": {"rust": "Vec<T>", "typescript": "readonly T[]"},
    "enum": {"rust": "enum with exact string renames", "typescript": "string-literal union"},
    "const": {"rust": "validated scalar (const checked at decode)", "typescript": "literal type"},
    "record": {"rust": "struct with deny-unknown-fields", "typescript": "interface; decoder rejects extra keys"},
    "variant-record": {"rust": "enum with one struct per discriminator value; codec writes every memberOrder member including nulls",
                       "typescript": "discriminated union on the discriminator member; every member present"},
    "alias": {"rust": "pub type Alias = Target;", "typescript": "export type Alias = Target;"},
    "extern": {"rust": "generated type from the registered schema (inputs/generator-candidate03-options.json namespace); JSON-vector integers map to u64/bigint because every extern integer has minimum 0",
               "typescript": "same generated type name"},
    "frame-payload": {"rust": "per-protocol enum; decode entry point takes (frameType, HostSelector) and never tries alternatives",
                      "typescript": "per-protocol discriminated union with the same selector-parameterized decoder"},
    "lexical": {"rust": "handwritten function implementing lexicalRules[<id>] exactly as structured, applied after NFC and length checks", "typescript": "same"},
    "selectors": {
        "negotiated-target-attribution-v2": "true iff target-attribution-v2 is in both the admitted Hello and HelloAck token arrays (handshake law factBatch.negotiated)",
        "host-phase": "the host phase in which the Unavailable frame arrives; any other phase has no transition row and faults before payload typing",
    },
    "namespaces": {
        "Ts2": "delivery.v2 typescript-semantic wireSchema successors (this document)",
        "Rust3": "rust-provider-protocol.v2 wireSchema successors and native-evidence §9.2 records (this document)",
        "extern": "Handshake1, Startup1, Native2, Occupancy1 exactly as the frozen subject input inputs/generator-candidate03-options.json names them (checked)",
        "forbidden": "bare CoverageKeyV2, FactCandidateV1, AnchorRefV1, StageResultV1 or FactBatchV3 type names",
    },
    "orders": ORDERS,
    "patternDialect": PATTERN_DIALECT,
    "lexicalRules": LEXICAL_RULES,
}


def rule(id_, applies, text, owner, kind, params=None):
    r = {"id": id_, "appliesTo": applies, "kind": kind, "rule": text, "owner": owner}
    if params is not None:
        r["params"] = params
    return r


def route(key):
    """A refusal is a REFERENCE to a public-route-successor.v1.json key; class, errorCode, exit and envelope detail are
    DERIVED by the pinned owner public_termination_for / failure_envelope_errors / CLASS_TO_EXIT, never restated here."""
    return {"routeKey": key, "successor": "public-route-successor.v1.json#/addKeys/" + key}


def render_path_members(lexical, members, extern_members):
    wire = ", ".join(members)
    ext = ", ".join(f"{m['generatedType']}{m['pointer']}" for m in extern_members)
    return (f"Every member listed in params.members ({wire})" + (f" and params.externMembers ({ext})" if ext else "")
            + f" satisfies lexicalRules[{lexical}]; any pattern on the same value is supplementary.")


# Filled by build.py from the carrier graph; check.py recomputes and requires equality.
PATH_MEMBERS = {"CANONICAL-PATH-ADMISSION": None, "TS2-LOGICAL-PATH-ADMISSION": None}

ADMISSION = [
    rule("FRAME-LIMIT", "both", "Declared payload length <= maxFramePayloadBytes 67108864 before allocation; every array/text/byte length checked before allocation. A member with no maxItems/maxBytes is bounded only by this limit. A host never plans a frame over this limit: REQUEST-WIRE-ACCOUNTING refuses such a request before spawn.", "delivery2 limits.limitRule; rust2 framing.allocationRule", "bound"),
    rule("TS2-ENV-MAJOR", "typescript-semantic", "Envelope protocolMajor == 2 before payload typing.", "handshake x-opensip-wire-law.frameAndMajor", "state"),
    rule("TS2-ENV-DIRECTION-BY-FRAME", "typescript-semantic", "frameType must belong to the direction being read (closedHostToWorkerFrames + closedWorkerToHostFrames + NativeContextVerified).", "delivery2 providerProtocol.closed*Frames; nativeMd §0 line 121", "state"),
    rule("TS2-ENV-SEQUENCE", "typescript-semantic", "Per-direction sequence starts at 0 and increases by exactly 1; overflow refuses.", "delivery2 ordering.sequenceRule", "order"),
    rule("RUST3-FRAME-PRECHECK", "rust-semantic", "Before P3 matching: frameType known, direction equals the frame row direction, sequence equals that direction's counter, counter < 2^64-1, payload decodes under the selected carrier with every join below. Failure is FAULT / PROVIDER.PROTOCOL_VIOLATION (same outcome as P3-34).", "rust2 orderingAndStateMachine.transitionAstV2.framePrecheck (retained)", "state"),
    rule("ECHO-SNAPSHOT2", "both", "Every snapshotId echo (manifest, chunk, seal, accepted, SubjectScopeV1, AnchorRefV1 source-span, SubjectV2.subjectId preimage) is the exact OpenUniverse snapshot2 text.", "startup x-opensip-startup-law.identityMembers + SUCC-ECHO-ENUMERATION", "echo"),
    rule("ECHO-PLAN2", "rust-semantic", "Every PreparedOutput{Manifest,Chunk,Seal,Accepted}.planId is the exact OpenUniverse plan2 text.", "startup identityMembers + SUCC-ECHO-ENUMERATION", "echo"),
    rule("ECHO-OPEN-UNIVERSE", "both", "Analyze executionId/snapshotId/planId (and TS universeKey) equal OpenUniverse.", "delivery2 AnalyzeV1.fields; startup identityMembers", "echo"),
    rule("TS2-MANIFEST-DIGEST", "typescript-semantic", "manifestSha256 = lowercase hex SHA-256(deterministic-CBOR(entries)); no domain, no prefix; Seal and Accepted echo it.", "SUCC-TS2-MANIFEST-DIGEST", "commitment", {"recipe": "raw-sha256-hex-of-cbor-entries"}),
    rule("RAW-MANIFEST-DIGEST", "rust-semantic", "SnapshotManifest, DependencySourceManifest and PreparedOutputManifest manifestSha256 = lowercase hex SHA-256(deterministic-CBOR(entries)); Seal and Accepted echo it.", "rust2 commitments.snapshotManifest/preparedOutputManifest; SUCC-DEPSRC-DIGEST", "commitment", {"recipe": "raw-sha256-hex-of-cbor-entries"}),
    rule("TS2-SNAPSHOT-ORDER", "typescript-semantic", "entries strictly ascending unique by path UTF-8 bytes; kind decides the variant.", "delivery2 SnapshotManifestV1.fields.entries", "order"),
    rule("TS2-LOGICAL-PATH-ADMISSION", "typescript-semantic", "RENDERED BY build.py", "identitySchemas3 #/$defs/LogicalPath (declarative grammar); delivery2 SnapshotEntryV1.fields.path", "shape",
         {"lexical": "logical-path-segments", "members": "FILLED BY build.py", "externMembers": "FILLED BY build.py",
          "notPaths": ["Ts2SnapshotEntryV1.variants.symlink.linkTarget (a link target, not a project path; no lexical rule)"]}),
    rule("CANONICAL-PATH-ADMISSION", "rust-semantic", "RENDERED BY build.py", "rust2 definitions.CanonicalPath rule; SUCC-CANONICAL-PATH", "shape",
         {"lexical": "canonical-path-segments", "members": "FILLED BY build.py", "externMembers": "FILLED BY build.py"}),
    rule("RUST3-SNAPSHOT-ENTRY-TYPES", "rust-semantic", "file: byteLength uint64, contentSha256 DigestHex, executable bool, targetBytes null; symlink: targetBytes non-empty byte string, other variant members null.", "SUCC-RUST3-SNAPSHOT-ENTRY", "shape"),
    rule("CHUNK-CUSTODY", "both", "Chunks follow entry order; chunkIndex contiguous from 0 per entry; byteOffset = checked sum of prior chunk bytes; a zero-length entry has no chunk; SHA-256 of the concatenated bytes equals the entry digest; total length equals the entry length.", "delivery2 snapshotTransport; rust2 SnapshotFileChunkV2.fields.bytes; nativeMd §3.2", "order"),
    rule("SEAL-AGGREGATES", "both", "entryCount = len(entries); total bytes = checked sum of entry lengths (Rust: <= stated limit); totalChunkCount = chunks sent.", "delivery2 SnapshotSealV1.fields; rust2 SnapshotSealV2.fields.all; ProtocolLimitsV3", "join"),
    rule("ACCEPTED-EQUALS-SEAL", "both", "Accepted members are exactly the Seal values, after byte/digest/VFS validation.", "delivery2 SnapshotAcceptedV1; rust2 SnapshotAcceptedV2; nativeMd §9.2 line 2879", "echo"),
    rule("DEPSRC-CUSTODY", "rust-semantic", "DependencySourceManifestV3.entries follow params.entryOrder over the exactly joined package row; the rows of one package are exactly its DependencyFileManifestV1 (H(native.dependency-file-manifest.v1) equals fileManifestSha256; count = fileCount; byte sum = totalBytes); every package of the set appears; entries <= maxDependencySourceEntries; distinct packages <= maxDependencySourcePackages; totalBytes <= maxDependencySourceTotalBytes; chunk bytes <= maxDependencySourceChunkBytes; dependencySourceSetId equals OpenUniverse.repositoryResolution.dependencySourceSetId on every frame. Empty set: entries [], manifestSha256 = hex(SHA-256(0x80)), seal counts 0, no chunk.", "SUCC-DEPSRC-DIGEST; nativeMd §3.1, §3.2, §9.3, §9.7", "join",
         {"entryOrder": ["name", "version", "sourceId", "path"], "orderBytes": "utf-8", "emptyManifestSha256": "sha256(0x80)"}),
    rule("PACKAGE-KEY-JOIN", "rust-semantic", "packageKey (manifest entries and chunks) must byte-equal name + SP + version + SP + sourceId of exactly one DependencySourceSetV1.packages row; join by exact string equality against the constructed keys of the set (injective because name/version contain no SP after DEPSRC-SET-KEY-CONSTRAINTS). A chunk's (packageKey, path) must equal a manifest entry.", "SUCC-DEPSRC-SET-KEY; nativeModel dependency_source_set_admit key", "join",
         {"separator": " ", "join": "exact-constructed-key"}),
    rule("DEPSRC-SET-KEY-CONSTRAINTS", "rust-semantic", "Dependency-source set admission (successor selector wrapping the owner dependency_source_set_admit, before PlanId) refuses an owner-admitted set with a package whose name or version contains a scalar <= U+0020 or whose constructed key exceeds params.maxKeyScalars scalars. The refusal is params.route. Valid empty sourceId and spaces inside sourceId are preserved.", "SUCC-DEPSRC-SET-KEY; SUCC-PUBLIC-ROUTES", "join",
         {"forbidInNameVersionAtOrBelow": "32", "maxKeyScalars": "4096", "route": route("native.dependency-source-not-wire-representable")}),
    rule("DEPSRC-WIRE-REPRESENTABILITY", "rust-semantic", "In the same successor selector and after DEPSRC-SET-KEY-CONSTRAINTS: refuse an owner-admitted set with a package whose name, version or sourceId (params.nfcFields) is not NFC, or a file path that is not NFC, exceeds params.maxPathScalars scalars or fails lexicalRules[params.pathLexical]. Nothing is normalized, truncated or renamed. The refusal is params.route; the owner's own refusals keep precedence.", "SUCC-DEPSRC-REPRESENTABILITY; SUCC-PUBLIC-ROUTES; native-evidence.schemas.v2 DependencyFileManifestV1 path; rust2 canonicalCbor (NFC)", "bound",
         {"nfcFields": ["name", "version", "sourceId"], "pathLexical": "canonical-path-segments", "maxPathScalars": "4096", "route": route("native.dependency-source-not-wire-representable")}),
    rule("PREPARED-V3-ENTRY", "rust-semantic", "entries[i] answers PreparedOutputSetV3.rows[i]: outputOrdinal = i; kind = planRow.kind; planRow = the exact row; logicalPath = '.opensip/prepared/v3/' + i + '-' + planRow.blob.sha256 + '.blob'; blobByteLength/blobSha256 = planRow.blob.byteLength/sha256; contentByteLength/contentSha256 equal the blob values (no V2 wrapper); a generated-file row requires planRow.generated.blob == planRow.blob.", "SUCC-PREPARED-V3", "join"),
    rule("PREPARED-V3-SET-JOIN", "rust-semantic", "Worker: every planRow.inputBinding.dependencySourceSetId equals repositoryResolution.dependencySourceSetId and cfgSetId names a universe.resolvedInputs.cfgSets entry; row kinds inert only. Host (before spawn): H(native.prepared-output-set.v3, {schemaVersion 3, preparation, rows: [entries[*].planRow]}) == repositoryResolution.preparedOutputSetId.", "SUCC-PREPARED-V3", "join"),
    rule("PREPARED-V3-WIRE-LIMIT", "rust-semantic", "Prepared output set admission (successor selector wrapping the owner prepared_output_set_admit, applied only when the owner outcome is admitted, before Plan construction) refuses a selected set whose inert rows exceed params.maxEntries (params.countScope; maxPreparedOutputEntries retained) or whose blob byte total exceeds params.maxTotalBlobBytes. The encoded PreparedOutputManifest frame is bounded by REQUEST-WIRE-ACCOUNTING. maxExpansionRows and maxGeneratedFileRows stay preparation-set limits, never wire widenings. The refusal is params.route.", "provider-handshake ProtocolLimitsV3.maxPreparedOutputEntries; rust2 PreparedOutputManifestV2.fields.entries; nativeMd lines 1855, 2934, 3525; SUCC-PREPARED-V3; SUCC-PUBLIC-ROUTES", "bound",
         {"countScope": "all-inert-rows", "maxEntries": "256", "maxOrdinal": "255", "maxTotalBlobBytes": "1073741824", "route": route("native.prepared-output-exceeds-wire-limit")}),
    rule("REQUEST-WIRE-ACCOUNTING", "both", "At Plan time, after every set admission and before any worker is spawned, the host plans the exact host-to-worker frame sequence (Hello, OpenUniverse, SnapshotManifest, its chunks, SnapshotSeal, then for major 3 DependencySourceManifest, chunks, Seal and, iff preparedOutputSetId is non-null, PreparedOutputManifest, chunks, Seal; then Analyze and one reserved Cancel echoing that execution and analysis) and measures each frame as the exact deterministic-CBOR envelope payload (params.lengthScope; the 40-byte prefix is params.prefixIncluded). Chunks are params.chunking. It refuses a planned frame over maxFramePayloadBytes and, for major 3 only, a request whose summed payload bytes exceed maxRequestPayloadBytesTotal or whose frame count exceeds maxRequestFrames. TypeScript major 2 declares no request totals, so only the frame bound applies. The refusal is params.route.", "rust2 framing.lengthScope/allocationRule; rust2 limitPolicy.aggregateAccounting; provider-handshake ProtocolLimitsV3 and TypeScriptProtocolLimitsV1; nativeMd line 2848 (Plan time, no spawn); SUCC-REQUEST-ACCOUNTING; SUCC-PUBLIC-ROUTES", "bound",
         {"lengthScope": "envelope-payload", "prefixIncluded": False, "prefixBytes": "40", "chunking": "greedy-max-chunk", "reserveCancel": True,
          "totalsApplyTo": ["rust-semantic"], "route": route("native.provider-request-exceeds-wire-limit")}),
    rule("TS2-BUDGET-PROJECTION", "typescript-semantic", "budget is exactly delivery2 stageRequestProjection.budgetProjection output.", "delivery2 stageRequestProjection.budgetProjection", "join"),
    rule("TS2-STAGE-PROJECTION", "typescript-semantic", "stageRequests are all and only selected stages in verified logical order; stageOrdinal contiguous 0..n-1; dependsOn [] when absent.", "delivery2 multiStageAnalyze; stageRequestProjection", "join"),
    rule("DISPATCH-STAGE-CORRELATION", "both", "stageId is C-2 text (StageIdText) and equals DispatchBindingV1.expectedStageId; stageOrdinal = analyzeRequestOrdinal, never retainedStageOrdinal; FactBatch analysisOrdinal/batchIndex/first candidateOrdinal equal the dispatch expectations; batch count 1..cap (rust2 T016 guard retained as pre-match admission).", "dispatch x-opensip-wire.correlation; nativeMd §9.6 lines 3024-3043; rust2 T016", "join"),
    rule("TS2-SUBJECT-SCOPE-RETAINED", "typescript-semantic", "SubjectScopeV1 fully retained: commitment C(opensip.coverage.subject-scope.v1, sorted SnapshotFileSubjectV1[]); subjectCount = kind=file entries; recomputed by host and worker.", "delivery2 definitions.SubjectScopeV1 (retained)", "commitment"),
    rule("PER-KEY-SCOPE2", "both", "Each request key's subjectScopeCommitment = 'sha256:' + hex of scope2 = H('subject-scope', D_key) with D_key members params.descriptorMembers (sourceUniverse/targetUniverse are the key's 64-hex suffixes; relation/resolution the key's; enumeratorClosure the Plan-selected provider closure2 of the stage; subjects the host enumeration). Host mints before spawn; the same descriptor drives admit_coverage_result_v3 and pre-Analyze conversion. Worker checks Sha256Text shape only and echoes: entries[i].key.subjectScopeCommitment and entries[i].entry.examinedUniverse.subjectScopeCommitment equal keys[i]. No equality with TS SubjectScopeV1.subjectScopeCommitment or rust2 commitments.subjectScope is required.", "SUCC-PER-KEY-SCOPE2; nativeMd §4.1a; identityMd §3 lines 287-294", "commitment",
         {"identityDomain": "subject-scope", "textPrefix": "sha256:", "descriptorMembers": ["schemaVersion", "snapshotId", "sourceUniverse", "targetUniverse", "relation", "resolution", "enumeratorClosure", "subjects"]}),
    rule("TS2-DOMAIN-COMMITMENT", "typescript-semantic", "domainCommitment = C(opensip.ts-provider.requested-coverage-domain.v1, {subjectScope, keys}); keys carry per-key scope2 values; worker recomputes.", "delivery2 RequestedCoverageDomainV1.fields.domainCommitment", "commitment"),
    rule("RUST3-DOMAIN-COMMITMENT", "rust-semantic", "domainCommitment = C(opensip.rust-provider.analysis-domain.v2, {subjects, requestedCoverageDomain}); analysisDomain equals a fresh host reconstruction (wireRule) with per-key scope2 values.", "rust2 commitments.analysisDomain; planAndDomainProjection.wireRule", "commitment"),
    rule("RUST3-SUBJECTS", "rust-semantic", "subjectsAlgorithm retained; the snapshotId in the subjectId preimage is the snapshot2 text.", "rust2 planAndDomainProjection.subjectsAlgorithm; SUCC-ECHO-ENUMERATION", "commitment"),
    rule("RUST3-PLAN-STAGE-BYTES", "rust-semantic", "deterministic-CBOR(planStage) equals the selected ExecutionPlan stage bytes; optional members absent exactly when absent.", "rust2 planAndDomainProjection.planStageByteRule", "join"),
    rule("UNIVERSE-NATIVE-IDENTITY", "both", "Universe ids are sha256:hex(H(native.semantic-universe.<language>.v2, universe.resolvedInputs)); CoverageKeyV2 entries carry the 64-hex suffix.", "startup universeIdentity; nativeMd §0 lines 125, 128", "join"),
    rule("FP-CANDIDATE", "both", "fact-plane candidate law: registry relation/rung/layer/schemaId, producer/language constants, producerVersion = verified providerBuildId, target universe in host-admitted target domain.", "factPlane candidateSchema.fields; delivery2 FactCandidateV1.fields", "join"),
    rule("RELATION-PAYLOAD-CBOR", "both", "canonicalRelationPayload decodes once to the registry payload schema and re-encodes byte-equal; <= 1048576 bytes.", "factPlane candidateSchema.transportRepresentation; handshake candidateCborProjection", "shape"),
    rule("ANCHOR-WIRE-SPAN", "both", "Wire anchor rule (retained fact-plane sourceSpanSchema.rule): source-span requires snapshotId = OpenUniverse snapshot2, path = a kind=file manifest path, contentSha256 = that entry digest, startByte < endByte <= entry byteLength (NON-EMPTY). Array order: TS2 cbor-bytes-strict (delivery2 AnchorRefV1.ordering, the more specific TS transport owner, chosen over its 'field-for-field' fact-plane claim), Rust3 cve1-bytes-strict (factPlane anchorSchema.ordering). The two orders differ through map-key order (CVE1 sorts keys bytewise, so contentSha256 compares first; CBOR sorts length-first, so kind/path compare first); anchors differing only in path sort identically. Count 1..100000 (identity-schemas.v3 fact.anchors maxItems; fact-batch.schema.v3 anchors maxItems 4096 is the JSON-vector bound); a refusal above 100000 is outcome-equivalent to the later fact2 mint refusal (nativeMd lines 3838-3843). The shared fact2 rule (identity-model.v3.py line 1892 ANCHOR_RANGE: 0 <= a <= b <= len, plus ANCHOR_UTF8) is NOT narrowed.", "SUCC-ANCHOR-RULES", "join",
         {"nonEmpty": True, "maxCount": "100000", "order": {"typescript-semantic": "cbor-bytes-strict", "rust-semantic": "cve1-bytes-strict"}}),
    rule("ANCHOR-FACT-REF-REFUSED", "both", "kind=fact-ref is PROVIDER.PROTOCOL_VIOLATION at candidate admission before any fact2 mint, because fact-identity-fact2 is a mandatory identity token in both token sets and identity-schemas.v3 fact.anchors has no fact reference.", "SUCC-FACT-REF-REFUSED", "state"),
    rule("OCCUPANCY-JOIN", "both", "occupancyCompanions length <= len(candidates); each candidateOrdinal names a candidate of this batch; targetUniverseId byte-equal to that candidate.", "occupancy x-opensip-order-vocabulary.candidateOrdinal; nativeMd §9.6", "join"),
    rule("RUST3-SPOOL", "rust-semantic", "Candidate spool accounting over deterministic-CBOR({analysisOrdinal, stageId, candidate}) retained; bytes budget increments use candidate encoded length.", "rust2 limitPolicy.candidateSpoolAccounting; deterministicBudget", "bound"),
    rule("COMMIT-MAP", "both", "Every stage/stream/terminal commitment uses exactly the commitmentMap row for its field; the row valueClass must match the domain's owner recipe noun.", "SUCC-COMMIT-MAP", "commitment"),
    rule("COMMIT-TS2-FACT-BATCH", "typescript-semantic", "batchCommitment = C(opensip.ts-provider.fact-batch.v1, facts) over wire candidates; FactBatchV3 carries none.", "handshake x-opensip-wire-law.commitments.typescript-semantic", "commitment"),
    rule("CANCEL-NULLABILITY", "both", "Cancel.executionId is null iff OpenUniverse has not been sent, otherwise its exact value; analysisOrdinal is null iff Analyze has not been sent, otherwise Analyze.analysisOrdinal (TS2: 0). Cancel is host-sent, so the host knows exactly.", "delivery2 CancelV1.fields; SUCC-RUST3-FAULT-CANCEL", "echo"),
    rule("CANCELLED-ECHO", "both", "Cancelled executionId and analysisOrdinal equal the Cancel values.", "delivery2 CancelledV1.fields; rust2 CancelledV2.fields.all", "echo"),
    rule("TS2-OBSERVED-PHASE", "typescript-semantic", "observedPhase is the inherited enum; snapshot for a Cancel in WAIT_NATIVE_CONTEXT_VERIFIED or READY_ANALYZE.", "startup x-opensip-startup-law.cancellation", "state"),
    rule("RUST3-CANCEL-TYPES", "rust-semantic", "Cancel.reason const user-interrupt; Cancelled.observedPhase is the host phase in which the Cancel was sent (one of the 16 *PRE_COMPLETE phases). After P3-29 any in-flight non-Cancelled worker frame is P3-34, so in every admitted trace the send phase equals the worker's receipt phase.", "rust2 CancelledV2.fields.all; P3-29/P3-30; SUCC-RUST3-FAULT-CANCEL", "state"),
    rule("RUST3-PROVIDER-FAULT", "rust-semantic", "ProviderFault is judged by the worker-observed transcript. The worker reads Hello before writing any frame. phase = the P3 phase reached by replaying exactly the frames the worker has read and written; executionId = OpenUniverse.executionId iff the worker has read OpenUniverse, else null; analysisOrdinal = Analyze.analysisOrdinal iff it has read Analyze, else null. Host admission (possible-phase-set): let W be the last admitted worker-to-host frame (Hello if none); the host admits the payload iff (phase, executionId, analysisOrdinal) equals the worker-observed triple after W or after any prefix of the host-to-worker frames sent since W. So an in-flight OpenUniverse/Analyze admits null or the sent value, jointly consistent with phase, and a frame the worker provably read (a later admitted worker frame) requires the value. detailCode IdentityText, diagnostic only, normalizes to provider-protocol. A refused (inconsistent or START-phase) ProviderFault payload turns the owner P3-28 provider-fault terminal into FAULT; params.d9Equivalence records that the pinned owner stage_authority gives both terminal kinds the identical D9 outcome, so no fault outcome is suppressed or changed (review-02 A-5).", "rust2 ProviderFaultV2; P3-28 (*PRE_COMPLETE); SUCC-RUST3-FAULT-CANCEL; nativeModel stage_authority", "state",
         {"phaseSemantics": "worker-observed", "hostAdmission": "possible-phase-set", "anchorFrame": "last-admitted-worker-frame", "nullLaw": {"executionId": "OpenUniverse", "analysisOrdinal": "Analyze"}, "jointConsistency": True, "readHelloFirst": True,
          "d9Equivalence": {"ownerTerminalKind": "provider-fault", "refusedPayloadTerminalKind": "fault"}}),
    rule("RUST3-BUDGET-EXHAUSTED", "rust-semantic", "triggerStageId = current stage; unit/limit = planStage.budget (a stage without budget or with milliseconds cannot BudgetExhausted); observed = limit + 1 (checked).", "rust2 T020 guard (retained pre-match); SUCC-RUST3-OBSERVED", "join", {"observedMinusLimit": "1"}),
]

DOMAIN_RULE = "C(d, v) = 'sha256:' + lowercase hex SHA-256(UTF8(d) || 0x00 || deterministic-CBOR(v))"
COMMITMENT_MAP = {
    "function": DOMAIN_RULE,
    "valueClasses": {
        "stage-entries": "the ordered CoverageResultV3 entries of one stage",
        "stage-major-entries": "the ordered CoverageResultV3 entries of all requested stages, stage-major/key order",
        "stage-candidates": "the ordered wire FactCandidateV1 values of one stage",
        "stage-major-candidates": "the ordered wire FactCandidateV1 values of all stages",
        "batch-facts": "one FactBatchV1 facts array", "request-domain": "the request domain record",
        "file-subjects": "sorted SnapshotFileSubjectV1[]", "key-descriptor": "foundation subject-scope descriptor D_key",
        "manifest-entries": "manifest entries array", "subject-preimage": "SubjectV2 identity preimage",
    },
    "rows": [
        {"protocol": "typescript-semantic", "field": "Startup1TypeScriptCoverageV2.coverageCommitment", "domain": "opensip.ts-provider.stage-coverage.v1", "valueClass": "stage-entries"},
        {"protocol": "typescript-semantic", "field": "Ts2StageResultV1.coverageCommitment", "domain": "opensip.ts-provider.stage-coverage.v1", "valueClass": "stage-entries"},
        {"protocol": "typescript-semantic", "field": "Ts2CompleteV1.coverageStreamCommitment", "domain": "opensip.ts-provider.coverage-stream.v1", "valueClass": "stage-major-entries"},
        {"protocol": "typescript-semantic", "field": "Startup1TypeScriptUnavailableV2.coverageCommitment", "domain": "opensip.ts-provider.coverage-stream.v1", "valueClass": "stage-major-entries"},
        {"protocol": "typescript-semantic", "field": "Startup1TypeScriptBudgetExhaustedV2.coverageCommitment", "domain": "opensip.ts-provider.coverage-stream.v1", "valueClass": "stage-major-entries"},
        {"protocol": "typescript-semantic", "field": "Ts2StageResultV1.factCommitment", "domain": "opensip.ts-provider.stage-facts.v1", "valueClass": "stage-candidates"},
        {"protocol": "typescript-semantic", "field": "Ts2CompleteV1.factStreamCommitment", "domain": "opensip.ts-provider.fact-stream.v1", "valueClass": "stage-major-candidates"},
        {"protocol": "typescript-semantic", "field": "Ts2FactBatchV1.batchCommitment", "domain": "opensip.ts-provider.fact-batch.v1", "valueClass": "batch-facts"},
        {"protocol": "typescript-semantic", "field": "Ts2RequestedCoverageDomainV1.domainCommitment", "domain": "opensip.ts-provider.requested-coverage-domain.v1", "valueClass": "request-domain"},
        {"protocol": "typescript-semantic", "field": "Ts2SubjectScopeV1.subjectScopeCommitment", "domain": "opensip.coverage.subject-scope.v1", "valueClass": "file-subjects"},
        {"protocol": "both", "field": "Ts2CoverageKeyV1.subjectScopeCommitment / Rust3CoverageKeyV2.subjectScopeCommitment / Native2CoverageKeyV2.subjectScopeCommitment / Native2ExaminedUniverseV1.subjectScopeCommitment", "domain": None, "valueClass": "key-descriptor", "recipe": "foundation identity H('subject-scope', D_key), spelled sha256:<scope2 hex>; not DOMAIN_RULE"},
        {"protocol": "typescript-semantic", "field": "Ts2SnapshotManifestV1.manifestSha256 (+ Seal/Accepted echo)", "domain": None, "valueClass": "manifest-entries", "recipe": "lowercase hex SHA-256(deterministic-CBOR(entries)); delivery2 commitments.domains.snapshotManifest not applied"},
        {"protocol": "rust-semantic", "field": "Startup1CoverageV3.coverageCommitment", "domain": "opensip.rust-provider.stage-coverage.v2", "valueClass": "stage-entries"},
        {"protocol": "rust-semantic", "field": "Rust3StageResultV2.coverageCommitment", "domain": "opensip.rust-provider.stage-coverage.v2", "valueClass": "stage-entries"},
        {"protocol": "rust-semantic", "field": "Rust3CompleteV2.coverageStreamCommitment", "domain": "opensip.rust-provider.coverage-stream.v2", "valueClass": "stage-major-entries"},
        {"protocol": "rust-semantic", "field": "Startup1UnavailableV3.coverageCommitment", "domain": "opensip.rust-provider.coverage-stream.v2", "valueClass": "stage-major-entries"},
        {"protocol": "rust-semantic", "field": "Startup1BudgetExhaustedV3.coverageCommitment", "domain": "opensip.rust-provider.coverage-stream.v2", "valueClass": "stage-major-entries"},
        {"protocol": "rust-semantic", "field": "Rust3StageResultV2.factCommitment", "domain": "opensip.rust-provider.stage-facts.v2", "valueClass": "stage-candidates"},
        {"protocol": "rust-semantic", "field": "Rust3CompleteV2.factStreamCommitment", "domain": "opensip.rust-provider.fact-stream.v2", "valueClass": "stage-major-candidates"},
        {"protocol": "rust-semantic", "field": "Rust3StageAnalysisDomainV2.domainCommitment", "domain": "opensip.rust-provider.analysis-domain.v2", "valueClass": "request-domain"},
        {"protocol": "rust-semantic", "field": "Rust3SubjectV2.subjectId", "domain": "opensip.rust-provider.subject.v2", "valueClass": "subject-preimage", "recipe": "'rust-file:sha256:' + hex(...) as rust2 subjectsAlgorithm"},
        {"protocol": "rust-semantic", "field": "Rust3SnapshotManifestV2 / Native2DependencySourceManifestV3 / Rust3PreparedOutputManifestV3 .manifestSha256", "domain": None, "valueClass": "manifest-entries", "recipe": "lowercase hex SHA-256(deterministic-CBOR(entries))"},
    ],
    "basis": "Preimage shape decides the domain. The owner recipe nouns (rust2 commitments: stageCoverage over 'stageCoverageEntries', coverageStream over 'stage-major ... values'; delivery2 field texts 'this stage's ordered ... stream' vs 'every ordered ... from all stages') classify each domain; terminal Unavailable/BudgetExhausted coverage is stage-major (startup coverageFrames.terminals), so it is coverageStream. check.py derives the class from owner text and executes Rust3 and TS2 terminal vectors.",
}

TRANSITIONS = {
    "typescript-semantic": {
        "base": {"pin": "ts2order", "rules": "23"},
        "overlay": "none: T2-14 already guards post-Analyze Unavailable with outputSeen=false; T2-18 keeps Cancel from START (delivery2 cancelTransition).",
        "unavailableSelection": "The carrier selects the Unavailable payload by host phase (WAIT_NATIVE_CONTEXT_VERIFIED or ANALYZING). The TS2 owner table guards T2-10/T2-14 on the payload-derived observation unavailablePayload. Outcomes are equivalent (a phase/payload mismatch faults either way), but trace ids differ: carrier selection refuses in the frame precheck, the owner table reaches T2-23.",
    },
    "rust-semantic": {
        "base": {"pin": "p3", "rules": "34"},
        "precedence": "protocol3-transitions.v1.json plus this overlay (published as p3-guard-successor.v1.json) is the only matching table for major 3; rust2 transitionAstV2 rules are not interpreted. rust2 framePrecheck and the T016/T020 payload guards are retained as pre-match admission (RUST3-FRAME-PRECHECK, DISPATCH-STAGE-CORRELATION, RUST3-BUDGET-EXHAUSTED).",
        "stateAdditions": {"outputSeen": False},
        "stateUpdateAdditions": [{"onFrames": ["Analyze"], "sets": {"outputSeen": False}},
                                 {"onFrames": ["FactBatch", "CoverageV3"], "sets": {"outputSeen": True}}],
        "guardAdditions": {"P3-25": {"outputSeen": False}},
        "equivalence": "rust2 T019 guards stageIndex == 0 AND outputSeen == false; rust2 T017/T018 set outputSeen on every Coverage, so stageIndex > 0 implies outputSeen and the single outputSeen guard is equivalent.",
        "cancel": {"hostMaySendInStart": False, "basis": "P3-29 *PRE_COMPLETE excludes START; Hello is host-to-worker so START is host-controlled. A user interrupt in START terminates the child without a Cancel frame: a resulting P3-33 process observation still reduces to interrupted/130 because the host finalizer combines provider observations with interruption timing (rust2 d9Join.rule) and cancellation is interrupted 130 (nativeMd lines 3838-3843)."},
        "terminalGuards": "Unchanged P3 preMatchLaw: FAULT absorbing; any frame after a terminal in WAIT_ZERO_EXIT/WAIT_EOF/DONE faults; process faults from any phase; unmatched frame P3-34.",
        "custodyOrder": "SnapshotAccepted -> DependencySource custody (always) -> PreparedOutput custody iff preparedOutputSetId != null -> NativeContextVerified or pre-Analyze Unavailable -> Analyze (nativeMd §9.1 step 4 lines 2863-2866; P3-08..P3-22).",
    },
}
