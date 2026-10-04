"""Build contract successor FA-2 deterministically, and check it without the product's tools.

FA-2 gives a TypeScript or Rust provider's symbol census a lawful carrier (M3-H r1, X-H1). It writes,
under docs/implementation/m3/native-successors-fa/:
  fa-2/design/native/provider-handshake.schemas.v1.json      (successor copy: the symbol-census-v1 token)
  fa-2/product/schemas/sources/handshake-v1.schema.json      (product source copy, the same edits)
  fa-2/design/native/symbol-census.schemas.v1.json           (new document: the census payloads)
  fa-2/product/schemas/sources/symbol-census-v1.schema.json  (product source copy of it)
  fa-2/materialization-map.json, fa-2/evidence/copies-report.json, fa-2/evidence/vectors.json,
  fa-2/successor.json and fa-2-subject.json.
It reads fa-2/section-9-8.md and fa-2/README.md as written by the lead.

Each handshake copy is its parent's raw bytes with exactly FA-2's edits, in place: the token appended
last to both language token enums (no existing member moves), the two token-array maxItems raised by
one, the two token descriptions and the document description extended, one supersedes entry and one
symbolCensus law entry added. The parents carry no bound passage override (asserted), so nothing is
carried.

The checks restate tools/verify_design.py's contract_successor and successor_chain rules for this record,
against the product lock at every commit in LOCK_COMMITS: accepted parents at their pinned bytes, exact
before texts, line selectors on the Markdown parent only, no selector already bound, candidates equal to
the subject minus the record, and fresh candidate paths. The vectors are computed with an independent
two-line implementation of the foundation encoder C and the H frame, checked first against native-evidence's
own scope2 oracle case.

Usage (read-only on the product; git is used only to read the lock and one base blob):
    python3.14 -I -B evidence/build_fa2.py --product /path/to/opensip [--deps DIR] [--check] [--lock-commit SHA]
--check rebuilds in memory and compares with the files on disk instead of writing.
--deps names a directory holding jsonschema 4.25.1; with it the census vectors are also validated with the
design encoder's ExactValidator (foundation/canonical.py), and the projected record against SIS.
"""
from __future__ import annotations

import argparse
import copy
import difflib
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ARCH = HERE.parents[5]
BASE = 'docs/implementation/m3/native-successors-fa'
UNIT = f'{BASE}/fa-2'
SUBJECT = f'{BASE}/fa-2-subject.json'
# The instructed base (main when FA-2 was assigned), main when r1 was written, and main at r2 (I1-P, lock only).
# --lock-commit adds more.
LOCK_COMMITS = ['e093e908dd7fe735356a896f3cf4b97e1d93198e', '15c077935a9fdd9d2550726922669d576e7f6c4b',
                'cd5958b3608f44a0035566c9d4500e5005c62e91']
BASE_PRODUCT_HEAD = LOCK_COMMITS[0]

NE = 'docs/v2/contracts/product-v1/native-evidence.md'
HS = 'docs/coop/design-corrections/native/provider-handshake.schemas.v1.json'
ST = 'docs/coop/design-corrections/native/provider-startup.schemas.v1.json'
PHS = 'docs/implementation/m1/source-selection-v2/schemas/sources/handshake.v1.schema.json'
PST = 'docs/implementation/m1/source-selection-v2/schemas/sources/startup.v1.schema.json'
SIS = 'docs/coop/design-corrections/foundation/subject-inventory.schema.v1.json'
CASES = 'docs/coop/design-corrections/native/native-cases.v2.json'
ORACLE_CASE = 'subject-scope-commitment-is-the-scope2-identity-in-native-sha256-text-form'

TOKEN = 'symbol-census-v1'
HS_COPY = f'{UNIT}/design/native/provider-handshake.schemas.v1.json'
PHS_COPY = f'{UNIT}/product/schemas/sources/handshake-v1.schema.json'
CENSUS_DOC = f'{UNIT}/design/native/symbol-census.schemas.v1.json'
CENSUS_PRODUCT = f'{UNIT}/product/schemas/sources/symbol-census-v1.schema.json'
SECTION = f'{UNIT}/section-9-8.md'
README = f'{UNIT}/README.md'
BUILD = f'{UNIT}/evidence/build_fa2.py'
VECTORS = f'{UNIT}/evidence/vectors.json'
COPIES_REPORT = f'{UNIT}/evidence/copies-report.json'
MAP = f'{UNIT}/materialization-map.json'
SUCCESSOR = f'{UNIT}/successor.json'

COPIES = {HS: (HS_COPY, 'schemas/sources/handshake-v1.schema.json'),
          PHS: (PHS_COPY, 'schemas/sources/handshake-v1.schema.json')}

# ---------------------------------------------------------------------------------------------------
# Text passage overrides of native-evidence.md: (line, anchor or None, inserted text, source).
# Every override is insert-only: after = before[:i] + inserted + before[i:], where i is the end of the
# anchor (which occurs exactly once in the line), or the end of the line when anchor is None.
# ---------------------------------------------------------------------------------------------------

ROW_A = ("| `docs/coop/artifacts/delivery.v2.json` | "
         "`$.typescriptSemanticSubstrate.providerProtocol.wireSchema.payloadSchemas.AnalyzeV1`, "
         "`$.typescriptSemanticSubstrate.providerProtocol.wireSchema.payloadSchemas.CompleteV1`, "
         "`$.typescriptSemanticSubstrate.providerProtocol.wireSchema.frameSchemas.Analyze.payloadType`, "
         "`$.typescriptSemanticSubstrate.providerProtocol.wireSchema.frameSchemas.Complete.payloadType` | "
         "**Retained** when `symbol-census-v1` is not negotiated; **replaced** by `TypeScriptAnalyzeV2` / "
         "`TypeScriptCompleteV2` (§9.8) when it is. Each keeps every inherited member and adds only "
         "`symbolCensus`. |")
ROW_B = ("| `docs/coop/artifacts/rust-provider-protocol.v2.json` | "
         "`$.wireSchema.payloadSchemas.AnalyzeV2`, `$.wireSchema.payloadSchemas.CompleteV2`, "
         "`$.wireSchema.frameSchemas.Analyze.payloadType`, `$.wireSchema.frameSchemas.Complete.payloadType` | "
         "**Retained** when `symbol-census-v1` is not negotiated; **replaced** by `AnalyzeV3` / `CompleteV3` "
         "(§9.8) when it is. Each keeps every inherited member and adds only `symbolCensus`. |")
ROW_C = ("| `docs/coop/artifacts/delivery.v2.json`; `docs/coop/artifacts/rust-provider-protocol.v2.json` | "
         "`$.typescriptSemanticSubstrate.providerProtocol.wireSchema.coverageDomain.keyConstruction.subjectScopeCommitment`; "
         "`$.typescriptSemanticSubstrate.providerProtocol.wireSchema.definitions.RequestedCoverageDomainV1.workerRule`, "
         "only its requirement that every `key.subjectScopeCommitment` equal `subjectScope.subjectScopeCommitment`; "
         "`$.typescriptSemanticSubstrate.providerProtocol.wireSchema.coverageDomain.cardinality.normalSuccess`, "
         "only its \"each entry repeats the identical full key\"; "
         "`$.planAndDomainProjection.coverageDomainAlgorithm[3]`, only its `subjectScopeCommitment` member | "
         "**Superseded** in both languages, whether or not `symbol-census-v1` is negotiated. A requested key's "
         "`subjectScopeCommitment` is §4.1a's commitment over the host's `D` for that key; for a `symbol`-kind key "
         "it is §9.8's census-free D∅. The returned entry answers it as §9.7 states, with §9.8's census exception. "
         "`SubjectScopeV1`, `subjects`, `analysisDomain`, `domainCommitment` and `commitments.subjectScope` are "
         "**retained** as the inherited proofs of the sealed file set and of the requested domain; none of them is "
         "a key commitment, and the worker still recomputes them. |")
ROW_D = ("| `docs/coop/design-corrections/native/native-evidence.schemas.v2.json` (registered bytes kept) | "
         "`#/$defs/CapabilityToken` | **Extended** for the Hello and HelloAck token arrays by `symbol-census-v1` "
         "(§9.1, §9.8), through FA-2's successor copy of `native/provider-handshake.schemas.v1.json`, whose "
         "`TypeScriptCapabilityToken` and `RustCapabilityToken` carry it. The registered document is not edited: "
         "its raw SHA-256 is a registered `payloadSchemaDigest` (§10). |")

TOKEN_PARAGRAPH = (
    "`symbol-census-v1` is a second additional optional capability of the same kind. It is not an\n"
    "identity token and does not enlarge the identity token set. It is required to spawn only where the\n"
    "Plan owes the worker a symbol census, as a token the Plan needs (step 1 below; §9.8). When present on\n"
    "both Hello and HelloAck, the Analyze and Complete payloads are §9.8's `TypeScriptAnalyzeV2` /\n"
    "`TypeScriptCompleteV2` or `AnalyzeV3` / `CompleteV3`; when absent, the inherited payloads remain. A\n"
    "census-bearing payload without the token, or an inherited payload with it, is\n"
    "`PROVIDER.PROTOCOL_VIOLATION`. The two optional tokens are independent. Protocol major stays 3 /\n"
    "TypeScript major 2, and the token adds no frame, phase, terminal, limit member or identity version.")

RUST_ROWS = (
    "| `Analyze` | host→worker | Historical `rust-provider-protocol.v2` `AnalyzeV2` when `symbol-census-v1` is "
    "absent; `AnalyzeV3` (§9.8) when it is negotiated: `AnalyzeV2`'s members plus `symbolCensus`, the census "
    "request | no |\n"
    "| `Complete` | worker→host | Historical `CompleteV2` when `symbol-census-v1` is absent; `CompleteV3` (§9.8) "
    "when it is negotiated: `CompleteV2`'s members plus `symbolCensus`, the census | yes |")

TS_PARAGRAPH = (
    "**Analyze and Complete.** Negotiated `symbol-census-v1`: `TypeScriptAnalyzeV2` and\n"
    "`TypeScriptCompleteV2` (§9.8), the inherited `delivery.v2` `AnalyzeV1` and `CompleteV1` members plus\n"
    "`symbolCensus`. Not negotiated: `AnalyzeV1` and `CompleteV1` unchanged.")

H9 = (
    "- **H-9 (enumeration and execution inputs; FA-2) — closed.** A TypeScript or Rust provider's\n"
    "  symbol census reaches the host only on §9.8's negotiated `Complete` payload. The host projects it,\n"
    "  field by field, into one `SubjectInventoryV1` per owed `(cellOrdinal, programOrdinal, symbol)`\n"
    "  locator of the enumeration contract (§§1-4), filling only the locator, `kind`, the state carrier,\n"
    "  `subjectLanguage` and `projections`. Those records are host-derived typed inputs under the\n"
    "  execution-inputs contract's ownership law (§§6-7): captured into `hostCapture.hostDerivedRefs`,\n"
    "  never stage outputs, never a new frame name. Owner admission is the enumeration contract's (its §8:\n"
    "  \"Caller maps must already be owner-admitted\"). No foundation document changes.")


def ne_overrides(section_text):
    return [
        (93, None, " A TypeScript or Rust provider's census reaches the host only on the negotiated "
                   "`symbol-census-v1` payloads of §9.8, which the host projects into `SubjectInventoryV1` "
                   "records; it is never inferred.", 'header: where the census comes from'),
        (138, None, '\n' + '\n'.join([ROW_A, ROW_B, ROW_C, ROW_D]), '§0: four superseded or extended selectors'),
        (1913, 'rather than dedupe).', " For a `symbol`-kind relation of a TypeScript or Rust universe it is "
                                       "that provider's admitted census (§9.8); before any census is admitted it "
                                       "is empty (§9.8's census-free D∅).", '§4.1a inputs: subjects of a symbol scope'),
        (1927, '**its own** enumeration', ' (for a `symbol`-kind key in a TypeScript or Rust universe, the census admitted under §9.8)',
         '§4.1a step 1'),
        (2791, '`target-attribution-v2`', ' and `symbol-census-v1` (§9.8)', '§9.1 token list'),
        (2814, None, '\n' + TOKEN_PARAGRAPH, '§9.1 the token'),
        (2884, None, '\n' + RUST_ROWS, '§9.2 Rust frame table'),
        (2990, None, '\n\n' + TS_PARAGRAPH, '§9.4 TypeScript payloads'),
        (3235, 'the host subject scope', " (for a `symbol`-kind key, §9.8's census-free D∅: no census exists "
                                         "before Analyze)", '§9.7 pre-Analyze conversion key'),
        (3279, 'equal the requested key', ', except that under negotiated `symbol-census-v1` a `symbol`-kind '
                                          "entry's `subjectScopeCommitment` is the census commitment of §9.8, "
                                          'checked when the census is admitted', '§9.7 entry attribution'),
        (3292, None, ' Under negotiated `symbol-census-v1` no census rides on these terminals: each '
                     '`symbol`-kind entry keeps its requested census-free commitment with `subjectCount` 0 (§9.8).',
         '§9.7 terminal coverage'),
        (3313, None, '\n\n' + section_text, '§9.8 appended (section-9-8.md)'),
        (4195, None, '\n' + H9, '§13 join H-9'),
    ]


# JSON Pointer overrides of the two provider-startup copies (the same three on each).
STARTUP_OVERRIDES = [
    ('/x-opensip-startup-law/coverageFrames/entries',
     'entries[i].key.relation, resolution and subjectScopeCommitment equal keys[i]',
     " (except that under negotiated symbol-census-v1 a symbol-kind entry's subjectScopeCommitment is the "
     'census commitment of native-evidence section 9.8, checked when the census is admitted)'),
    ('/x-opensip-startup-law/coverageFrames/terminals', None,
     ' Under negotiated symbol-census-v1 these terminals carry no census, so each symbol-kind entry keeps its '
     'requested census-free commitment (the D∅ of native-evidence section 9.8) with subjectCount 0.'),
    ('/x-opensip-startup-law/preAnalyzeUnavailable/hostConversion',
     "key = that key's subject-scope coordinates",
     ' (for a symbol-kind key, the census-free scope D∅ of native-evidence section 9.8, with subjects [], '
     'since no census exists before Analyze)'),
]

# ---------------------------------------------------------------------------------------------------
# The handshake copies.
# ---------------------------------------------------------------------------------------------------

DESCRIPTION_ANCHOR = '9.4 and 9.6'
DESCRIPTION_INSERT = ', and of the symbol-census-v1 token of section 9.8'
TOKEN_DESC_APPEND = (' symbol-census-v1 (section 9.8; contract successor FA-2) is also a member, although the '
                     'registered native-evidence.schemas.v2.json CapabilityToken does not list it.')
SUPERSEDES_ADD = ('native/native-evidence.schemas.v2.json#/$defs/CapabilityToken (the Hello and HelloAck token '
                  'arrays only: TypeScriptCapabilityToken and RustCapabilityToken here add symbol-census-v1, '
                  'native-evidence section 9.8)')
SYMBOL_CENSUS_LAW = {
    'negotiated': ('TypeScriptAnalyzeV2 and TypeScriptCompleteV2 (typescript-semantic), or AnalyzeV3 and CompleteV3 '
                   '(rust-semantic), as published in FA-2\'s symbol-census.schemas.v1.json, iff symbol-census-v1 is '
                   'in both the Hello and the HelloAck token arrays. Each is the inherited Analyze or Complete payload '
                   'with every inherited member unchanged, plus symbolCensus.'),
    'notNegotiated': ('delivery.v2 AnalyzeV1 and CompleteV1 (typescript-semantic) and rust-provider-protocol.v2 '
                      'AnalyzeV2 and CompleteV2 (rust-semantic), unchanged.'),
    'violation': ('A census-bearing payload without the token, or the inherited payload with the token, is '
                  'PROVIDER.PROTOCOL_VIOLATION.'),
    'planNeed': ('symbol-census-v1 is not an identity token and does not enlarge the identity token set. It is a '
                 'token the Plan needs (native-evidence section 9.1, step 1) for every worker the Plan owes a symbol '
                 'census (section 9.8), and for no other.'),
    'majors': ('Protocol major stays 3 / TypeScript major 2. The token adds no frame, phase, terminal, limit member '
               'or identity version, and it is independent of target-attribution-v2.'),
}
MAX_ITEMS = {'TypeScriptCapabilitiesV2': (11, 12), 'RustCapabilitiesV3': (13, 14)}
TOKEN_ENUMS = ['TypeScriptCapabilityToken', 'RustCapabilityToken']

# ---------------------------------------------------------------------------------------------------
# The census schema (new document).
# ---------------------------------------------------------------------------------------------------

LAW_TEXT = {
    'standing': ('NORMATIVE field-level restatement of native-evidence section 9.8 (contract successor FA-2). '
                 'Section 9.8 is the prose owner; where they differ, that is a defect in whichever moved.'),
    'negotiation': ('Capability token symbol-census-v1 (native-evidence 9.1). When it is in both the Hello and the '
                    'HelloAck token arrays, the Analyze payload is TypeScriptAnalyzeV2 or AnalyzeV3 and the Complete '
                    'payload is TypeScriptCompleteV2 or CompleteV3. When it is absent, delivery.v2 AnalyzeV1 and '
                    'CompleteV1 and rust-provider-protocol.v2 AnalyzeV2 and CompleteV2 remain. Any other combination '
                    'is PROVIDER.PROTOCOL_VIOLATION. Frame names, phases, terminals, limits, commitments and identity '
                    'versions are unchanged.'),
    'planNeed': ('The host owes a worker a census exactly when the Plan\'s EnumerationPlanV1 expects at least one '
                 '(cellOrdinal, programOrdinal, symbol) inventory whose available binding\'s universe is that '
                 'worker\'s universe. Every such binding names one enumerator.closureId, the worker\'s provider '
                 'closure, which is also the producerClosure of every stage the worker serves. The host requests a '
                 'census from every worker it asks for a symbol-kind key, and from no other. Any other Plan is a '
                 'host invariant refused before spawn.'),
    'request': ('Analyze.symbolCensus is SymbolCensusRequestV1 {enumeratorClosure} when a census is owed, and null '
                'otherwise.'),
    'requestCommitment': ('Every requested key whose relation\'s registry subjectKind is symbol carries, as '
                          'subjectScopeCommitment, the native-evidence 4.1a commitment ("sha256:" + the 64-hex suffix '
                          'of H("subject-scope", D)) of the census-free descriptor D∅ = {schemaVersion: 2, '
                          'snapshotId, sourceUniverse, targetUniverse, relation, resolution, enumeratorClosure, '
                          'subjects: []}. Before analysis the worker recomputes it and rejects a mismatch as '
                          'provider-protocol.'),
    'return': ('Complete.symbolCensus is SymbolCensusV1, null exactly when the request\'s was. The complete variant '
               'carries examinedPaths and rows; the over-bound variant replaces it exactly when the complete census '
               'would exceed 100000 rows, 100000 examined paths or 4194304 bytes of deterministic CBOR. There is no '
               'partial and no unavailable variant.'),
    'returnCommitment': ('Every symbol-kind entry of that Analyze\'s Coverage or CoverageV3 frames carries, as '
                         'key.subjectScopeCommitment and examinedUniverse.subjectScopeCommitment, the 4.1a commitment '
                         'of D∅ with subjects set to the rows\' nativeSubjectIds in canonical-set order (not row '
                         'order), and examinedUniverse.subjectCount equal to the row count. Under an over-bound census '
                         'these entries keep their requested commitment with subjectCount 0.'),
    'otherTerminals': ('BudgetExhausted, post-Analyze and pre-Analyze Unavailable, Cancelled, ProviderFault and every '
                       'fault carry no census. On the two clean terminals each symbol-kind entry keeps its requested '
                       'D∅ commitment with subjectCount 0, and the owed inventories are host-derived outcomes of '
                       'the terminal (partial with budget-exhausted, null cause, no rows, no examined paths; or '
                       'unavailable with provider-unavailable).'),
    'hostProjection': ('At the clean settlement of Complete only, and atomically with that Analyze\'s candidates and '
                       'Coverage, the host projects the census once per owed locator into SubjectInventoryV1: '
                       'schemaVersion 1, planId from the retained Plan, parameterDigest = raw SHA-256 of '
                       'C(EnumerationPlanV1), the locator\'s cellOrdinal and programOrdinal, kind symbol, state '
                       'complete, deficiency null, nativeCause null, examinedPaths as carried, and each row with kind '
                       'symbol, subjectLanguage from subject-inventory.schema.v1.json x-opensip-subject-language-table '
                       'on its path, and projections [] (projection unavailable). Rows are byte-equal across '
                       'locators. Identity: raw SHA-256 of C(record); custody: hostCapture.hostDerivedRefs, origin '
                       'provider-return.'),
    'admission': ('The enumeration owner admits each projected record (schema, locator, state law: examinedPaths '
                  'equals the binding\'s symbol extent) before the full enumeration join. The host then builds D for '
                  'every symbol-kind key from the admitted census and admits each entry through '
                  'admit_coverage_result_v3, unchanged. A projected record or a D above its 4 MiB C ceiling takes the '
                  'over-bound census\'s route, the subject-scope bound\'s scope-limit route, which this document does '
                  'not own. Nothing truncates, shards or rewrites a census.'),
    'refusals': ('Wire: a malformed, misordered, out-of-bound, wrongly null or token-mismatched census payload is '
                 'PROVIDER.PROTOCOL_VIOLATION under the native-evidence section 10 fault law. Admission: locator, '
                 'state, extent and row refusals are the enumeration owner\'s, origin provider-return; an entry\'s '
                 'commitment or count mismatch is 4.1a\'s existing refusal. No public code is added.'),
    'internalKeys': ['native.symbol-census-payload-without-token', 'native.symbol-census-token-without-payload',
                     'native.symbol-census-null-mismatch', 'native.symbol-census-row-order',
                     'native.symbol-census-path-not-examined', 'native.symbol-census-bound',
                     'native.symbol-census-over-bound-within-bounds', 'native.symbol-census-request-commitment-mismatch',
                     'native.symbol-census-enumerator-not-the-worker'],
    'internalKeysStanding': 'Diagnostic keys kept in the operational record. Not DomainDetailCode members.',
}


def census_schema():
    ref = lambda name: {'$ref': f'#/$defs/{name}'}
    nullable = lambda name: {'oneOf': [ref(name), {'type': 'null'}]}
    sha = {'$ref': '#/$defs/Sha256Text'}
    u64 = {'$ref': '#/$defs/Uint64'}
    return {
        '$schema': 'https://json-schema.org/draft/2020-12/schema',
        '$id': 'opensip.product.symbol-census.1',
        'title': 'Symbol census on negotiated Analyze and Complete (capability token symbol-census-v1)',
        'description': ('NORMATIVE field-level publication for native-evidence section 9.8 (contract successor FA-2). '
                        'Closed JSON-vector forms of deterministic-CBOR wire maps: the census request carried on '
                        'Analyze, the census carried on Complete, and the four payload versions that carry them when '
                        'symbol-census-v1 is in both the Hello and the HelloAck token arrays. Inherited members keep '
                        'their names, types and laws. TypeScriptCompleteV2 and CompleteV3 restate their inherited '
                        'members exactly; TypeScriptAnalyzeV2 and AnalyzeV3 name their inherited stage-request '
                        'arrays by selector and do not restate them. Cross-record joins a schema cannot express (the '
                        'census-free and census commitments, the locator projection, the extent and the byte bound) '
                        'are stated in x-opensip-symbol-census-law.'),
        'x-opensip-symbol-census-law': LAW_TEXT,
        '$defs': {
            'Uint64': {'type': 'integer', 'minimum': 0, 'maximum': 18446744073709551615},
            'Sha256Text': {'type': 'string', 'pattern': '^sha256:[0-9a-f]{64}(?![\\s\\S])'},
            'ExecutionIdText': {'type': 'string', 'minLength': 1,
                                'description': 'The inherited ExecutionId text, exact OpenUniverse value '
                                               '(provider-startup.schemas.v1.json ExecutionIdText).'},
            'SnapshotId2': {'type': 'string', 'pattern': '^snapshot2:[0-9a-f]{64}(?![\\s\\S])'},
            'PlanId2': {'type': 'string', 'pattern': '^plan2:[0-9a-f]{64}(?![\\s\\S])'},
            'StageIdText': {'type': 'string', 'minLength': 1, 'maxLength': 255, 'description': 'C-2 stageId text'},
            'ClosureId': {'type': 'string', 'pattern': '^closure2:[0-9a-f]{64}(?![\\s\\S])',
                          'description': 'A Plan-selected closure2 identity text (identity-schemas.v3 closure).'},
            'LogicalPath': {'type': 'string', 'minLength': 1, 'maxLength': 4096,
                            'pattern': '^[^/\\\\\\u0000]{1,255}(/[^/\\\\\\u0000]{1,255})*(?![\\s\\S])',
                            'not': {'pattern': '(^|/)\\.\\.?(/|$)'},
                            'description': 'Byte-identical constraint to subject-inventory.schema.v1.json#/$defs/LogicalPath.'},
            'SubjectIdV1': {'type': 'string', 'minLength': 3, 'maxLength': 4096,
                            'pattern': '^[a-z][a-z0-9-]*:[^\\u0000-\\u001f\\u007f-\\u009f]+(?![\\s\\S])',
                            'description': ('relation-payload-schemas.v2.json#/$defs/SubjectIdV1, as '
                                            'subject-inventory.schema.v1.json requires of a symbol nativeSubjectId.')},
            'SymbolCensusRequestV1': {
                'type': 'object', 'additionalProperties': False, 'required': ['enumeratorClosure'],
                'properties': {'enumeratorClosure': ref('ClosureId')},
                'description': ('The census request on Analyze. enumeratorClosure is the one enumerator.closureId of '
                                'every owed symbol binding at this worker\'s universe: the worker\'s provider closure. '
                                'It is the D∅ field the worker cannot otherwise know.')},
            'SymbolCensusRowV1': {
                'type': 'object', 'additionalProperties': False,
                'required': ['nativeSubjectId', 'path', 'qualifiedName', 'exported', 'signatureTokens'],
                'properties': {
                    'nativeSubjectId': ref('SubjectIdV1'),
                    'path': {'$ref': '#/$defs/LogicalPath',
                             'description': ('The trusted attributed first-party snapshot path, a member of '
                                             'examinedPaths. Never an external or node_modules path.')},
                    'qualifiedName': {'type': 'string', 'minLength': 1, 'maxLength': 4096},
                    'exported': {'type': 'string', 'enum': ['exported', 'not-exported', 'unknown']},
                    'signatureTokens': {'type': 'array', 'maxItems': 256,
                                        'items': {'type': 'string', 'minLength': 0, 'maxLength': 4096},
                                        'x-opensip-order': 'sequence',
                                        'description': 'Enumerator-native tokens, grammar order, repeats retained.'}},
                'description': ('One first-party symbol. It carries no planId, parameterDigest, cellOrdinal, '
                                'programOrdinal, kind, state carrier, subjectLanguage or projections: the host fills '
                                'them (x-opensip-symbol-census-law hostProjection).')},
            'CompleteSymbolCensusV1': {
                'type': 'object', 'additionalProperties': False, 'required': ['state', 'examinedPaths', 'rows'],
                'properties': {
                    'state': {'const': 'complete'},
                    'examinedPaths': {'type': 'array', 'maxItems': 100000, 'uniqueItems': True,
                                      'items': ref('LogicalPath'), 'x-opensip-order': 'canonical-set',
                                      'description': 'The examined logical paths; admission requires set equality '
                                                     'with the binding\'s symbol extent.'},
                    'rows': {'type': 'array', 'maxItems': 100000, 'uniqueItems': True,
                             'items': ref('SymbolCensusRowV1'), 'x-opensip-order': {'by': ['nativeSubjectId']},
                             'description': 'Strictly ascending and unique by the UTF-8 bytes of nativeSubjectId.'}},
                'description': ('The complete census. Its deterministic CBOR is at most 4194304 bytes; a larger census '
                                'is sent as OverBoundSymbolCensusV1 instead.')},
            'OverBoundSymbolCensusV1': {
                'type': 'object', 'additionalProperties': False,
                'required': ['state', 'rowCount', 'examinedPathCount'],
                'properties': {'state': {'const': 'over-bound'}, 'rowCount': u64, 'examinedPathCount': u64},
                'description': ('Sent instead of the complete census exactly when rowCount > 100000, '
                                'examinedPathCount > 100000, or the complete variant\'s deterministic CBOR would '
                                'exceed 4194304 bytes (checked by admission). No rows; never truncated.')},
            'SymbolCensusV1': {'oneOf': [ref('CompleteSymbolCensusV1'), ref('OverBoundSymbolCensusV1')],
                               'description': 'The census on Complete. No partial and no unavailable variant.'},
            'TypeScriptAnalyzeV2': {
                'type': 'object', 'additionalProperties': False,
                'required': ['analysisOrdinal', 'executionId', 'snapshotId', 'planId', 'universeKey',
                             'stageRequests', 'symbolCensus'],
                'properties': {
                    'analysisOrdinal': {'const': 0},
                    'executionId': ref('ExecutionIdText'),
                    'snapshotId': ref('SnapshotId2'),
                    'planId': ref('PlanId2'),
                    'universeKey': {'$ref': '#/$defs/Sha256Text',
                                    'description': 'The native semantic-universe identity, exact OpenUniverse value.'},
                    'stageRequests': {'type': 'array', 'minItems': 1, 'maxItems': 1024, 'items': {'type': 'object'},
                                      'x-opensip-order': 'sequence',
                                      'description': ('delivery.v2 typescriptSemanticSubstrate.providerProtocol.'
                                                      'wireSchema.definitions.StageRequestV1, unchanged in members and '
                                                      'law; its requested keys\' subjectScopeCommitment values follow '
                                                      'native-evidence 4.1a and 9.8. Not restated here.')},
                    'symbolCensus': nullable('SymbolCensusRequestV1')},
                'description': 'typescript-semantic Analyze when symbol-census-v1 is negotiated: AnalyzeV1 plus symbolCensus.'},
            'AnalyzeV3': {
                'type': 'object', 'additionalProperties': False,
                'required': ['analysisOrdinal', 'executionId', 'snapshotId', 'planId', 'stages', 'symbolCensus'],
                'properties': {
                    'analysisOrdinal': {'$ref': '#/$defs/Uint64',
                                        'description': 'The inherited AnalyzeV2 value, unchanged.'},
                    'executionId': ref('ExecutionIdText'),
                    'snapshotId': ref('SnapshotId2'),
                    'planId': ref('PlanId2'),
                    'stages': {'type': 'array', 'minItems': 1, 'maxItems': 256, 'items': {'type': 'object'},
                               'x-opensip-order': 'sequence',
                               'description': ('rust-provider-protocol.v2 wireSchema.definitions.StageRequestV2, '
                                               'unchanged in members and law; its analysisDomain keys\' '
                                               'subjectScopeCommitment values follow native-evidence 4.1a and 9.8. '
                                               'Not restated here.')},
                    'symbolCensus': nullable('SymbolCensusRequestV1')},
                'description': 'rust-semantic Analyze when symbol-census-v1 is negotiated: AnalyzeV2 plus symbolCensus.'},
            'TypeScriptStageResultV1': {
                'type': 'object', 'additionalProperties': False,
                'required': ['stageId', 'stageOrdinal', 'factBatchCount', 'factCount', 'coverageEntryCount',
                             'factCommitment', 'coverageCommitment'],
                'properties': {'stageId': ref('StageIdText'), 'stageOrdinal': u64, 'factBatchCount': u64,
                               'factCount': u64, 'coverageEntryCount': u64, 'factCommitment': sha,
                               'coverageCommitment': sha},
                'description': 'delivery.v2 StageResultV1, unchanged.'},
            'RustStageResultV2': {
                'type': 'object', 'additionalProperties': False,
                'required': ['stageId', 'factCount', 'coverageEntryCount', 'factCommitment', 'coverageCommitment'],
                'properties': {'stageId': ref('StageIdText'), 'factCount': u64, 'coverageEntryCount': u64,
                               'factCommitment': sha, 'coverageCommitment': sha},
                'description': 'rust-provider-protocol.v2 StageResultV2, unchanged.'},
            'TypeScriptCompleteV2': {
                'type': 'object', 'additionalProperties': False,
                'required': ['analysisOrdinal', 'stageResults', 'factStreamCommitment', 'coverageStreamCommitment',
                             'symbolCensus'],
                'properties': {
                    'analysisOrdinal': {'const': 0},
                    'stageResults': {'type': 'array', 'minItems': 1, 'maxItems': 1024,
                                     'items': ref('TypeScriptStageResultV1'), 'x-opensip-order': 'sequence'},
                    'factStreamCommitment': sha, 'coverageStreamCommitment': sha,
                    'symbolCensus': nullable('SymbolCensusV1')},
                'description': 'typescript-semantic Complete when symbol-census-v1 is negotiated: CompleteV1 plus symbolCensus.'},
            'CompleteV3': {
                'type': 'object', 'additionalProperties': False,
                'required': ['analysisOrdinal', 'stageResults', 'factStreamCommitment', 'coverageStreamCommitment',
                             'symbolCensus'],
                'properties': {
                    'analysisOrdinal': {'$ref': '#/$defs/Uint64',
                                        'description': 'The inherited CompleteV2 value, unchanged.'},
                    'stageResults': {'type': 'array', 'minItems': 1, 'maxItems': 256,
                                     'items': ref('RustStageResultV2'), 'x-opensip-order': 'sequence'},
                    'factStreamCommitment': sha, 'coverageStreamCommitment': sha,
                    'symbolCensus': nullable('SymbolCensusV1')},
                'description': 'rust-semantic Complete when symbol-census-v1 is negotiated: CompleteV2 plus symbolCensus.'},
        },
    }


# ---------------------------------------------------------------------------------------------------
# Helpers.
# ---------------------------------------------------------------------------------------------------

def read(path):
    return (ARCH / path).read_bytes()


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def pin(path, raw):
    return {'path': path, 'bytes': len(raw), 'sha256': sha(raw)}


def dump(value):
    return (json.dumps(value, indent=2, ensure_ascii=True) + '\n').encode('ascii')


def git_show(product, commit, path):
    return subprocess.run(['git', '-C', str(product), 'show', f'{commit}:{path}'], check=True,
                          capture_output=True).stdout


def pointer_get(value, pointer):
    for token in pointer[1:].split('/'):
        value = value[token.replace('~1', '/').replace('~0', '~')]
    return value


def pointer_set(value, pointer, new):
    tokens = [t.replace('~1', '/').replace('~0', '~') for t in pointer[1:].split('/')]
    for token in tokens[:-1]:
        value = value[token]
    value[tokens[-1]] = new


def insert(before, anchor, text):
    if anchor is None:
        return before + text
    if before.count(anchor) != 1:
        raise SystemExit(f'anchor not unique: {anchor!r}')
    i = before.index(anchor) + len(anchor)
    return before[:i] + text + before[i:]


def C(value):
    """Foundation canonical JSON (identity section 3; foundation/canonical.py canonical)."""
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')


def H(domain, value):
    raw = C(value)
    return hashlib.sha256(b'opensip.product.v1\0' + domain.encode('ascii') + b'\0'
                          + len(raw).to_bytes(8, 'big') + raw).hexdigest()


def scope(descriptor):
    hexdigest = H('subject-scope', descriptor)
    return {'scopeId': 'scope2:' + hexdigest, 'subjectScopeCommitment': 'sha256:' + hexdigest,
            'subjectCount': len(descriptor['subjects'])}


def canonical_set(items):
    ordered = sorted(items, key=C)
    if len(set(ordered)) != len(ordered):
        raise SystemExit('duplicate subject')
    return ordered


# ---------------------------------------------------------------------------------------------------
# Lock checks (verify_design's contract_successor and successor_chain rules, restated).
# ---------------------------------------------------------------------------------------------------

def lock_state(product, commit):
    lock = json.loads(git_show(product, commit, 'design-lock.json'))
    accepted = {row['path']: row for row in lock['inputs']}
    bound = {}
    for binding in lock['contractSuccessors']:
        raw = read(binding['record']['path'])
        if sha(raw) != binding['record']['sha256']:
            raise SystemExit(f'arch record differs from the lock: {binding["record"]["path"]}')
        record = json.loads(raw)
        for row in record.get('candidates', []):
            accepted[row['path']] = row
        accepted[binding['record']['path']] = binding['record']
        for entry in record.get('passageOverrides', []) + record.get('passageSupersessions', []):
            key = (entry['parent']['path'], json.dumps(entry['selector'], sort_keys=True))
            bound[key] = binding['record']['path']
    for binding in lock['inventorySuccessors']:
        accepted[binding['candidate']['path']] = binding['candidate']
        accepted[binding['parent']['path']] = binding['parent']
    return accepted, bound, len(lock['contractSuccessors'])


def check_lock(product, parents, overrides, candidates, subject_rows):
    results = []
    for commit in LOCK_COMMITS:
        accepted, bound, count = lock_state(product, commit)
        for row in parents:
            have = accepted.get(row['path'])
            if have is None or have['sha256'] != row['sha256'] or have['bytes'] != row['bytes']:
                raise SystemExit(f'{commit[:7]}: parent is not an accepted base: {row["path"]}')
        # A copied JSON parent must carry no bound override (its copy would otherwise have to carry it).
        # The text and pointer parents may carry other units' overrides; only selector equality conflicts.
        bound_copied = sorted({path for (path, _), _ in bound.items()} & set(COPIES))
        if bound_copied:
            raise SystemExit(f'{commit[:7]}: a copied parent carries a bound override: {bound_copied}')
        bound_elsewhere = sorted({f'{path}:{json.loads(sel).get("line", json.loads(sel).get("jsonPointer"))}'
                                  for (path, sel), _ in bound.items() if path in {row['path'] for row in parents}})
        for entry in overrides:
            key = (entry['parent']['path'], json.dumps(entry['selector'], sort_keys=True))
            if key in bound:
                raise SystemExit(f'{commit[:7]}: selector already bound by {bound[key]}: {key}')
        for row in subject_rows:
            if row['path'] in accepted:
                raise SystemExit(f'{commit[:7]}: candidate reuses an accepted path: {row["path"]}')
        results.append({'commit': commit, 'contractSuccessors': count, 'parentsAccepted': True,
                        'copiedParentsWithBoundOverrides': 0, 'otherUnitsBoundSelectorsOnParents': bound_elsewhere,
                        'fa2SelectorsAlreadyBound': 0, 'candidatePathsFresh': True})
    seen = set()
    for entry in overrides:
        key = (entry['parent']['path'], json.dumps(entry['selector'], sort_keys=True))
        if key in seen:
            raise SystemExit('duplicate override')
        seen.add(key)
        parent_raw = read(entry['parent']['path'])
        if 'line' in entry['selector']:
            try:
                json.loads(parent_raw)
            except ValueError:
                pass
            else:
                raise SystemExit('line selector on a JSON parent')
            current = parent_raw.decode('utf-8').splitlines()[entry['selector']['line'] - 1]
        else:
            current = pointer_get(json.loads(parent_raw), entry['selector']['jsonPointer'])
        if current != entry['before'] or not entry['after'] or entry['after'] == entry['before']:
            raise SystemExit(f'override before text differs: {entry["selector"]}')
    if {row['path'] for row in candidates} != {row['path'] for row in subject_rows} - {SUCCESSOR}:
        raise SystemExit('candidates do not cover the subject')
    return results


# ---------------------------------------------------------------------------------------------------
# Builders.
# ---------------------------------------------------------------------------------------------------

def handshake_copy(parent):
    raw = read(parent)
    text = raw.decode('ascii')
    expected = json.loads(raw)
    edits = []

    def replace_string(pointer, new):
        old = pointer_get(expected, pointer)
        if text.count(json.dumps(old)) != 1:
            raise SystemExit(f'cannot place {pointer}')
        edits.append({'jsonPointer': pointer, 'edit': 'string extended (insert-only)'})
        pointer_set(expected, pointer, new)
        return text.replace(json.dumps(old), json.dumps(new))

    text = replace_string('/description', insert(expected['description'], DESCRIPTION_ANCHOR, DESCRIPTION_INSERT))
    for name in TOKEN_ENUMS:
        pointer = f'/$defs/{name}/description'
        text = replace_string(pointer, pointer_get(expected, pointer) + TOKEN_DESC_APPEND)
    lines = text.split('\n')
    for name in TOKEN_ENUMS:
        members = expected['$defs'][name]['enum']
        want = [json.dumps(m) for m in members]
        hits = [i for i, line in enumerate(lines) if line.strip() == '"enum": ['
                and [l.strip().rstrip(',') for l in lines[i + 1:i + 1 + len(members)]] == want
                and lines[i + 1 + len(members)].strip().startswith(']')]
        if len(hits) != 1:
            raise SystemExit(f'cannot place the {name} enum')
        last = hits[0] + len(members)
        indent = lines[last][:len(lines[last]) - len(lines[last].lstrip())]
        lines[last] += ','
        lines.insert(last + 1, indent + json.dumps(TOKEN))
        members.append(TOKEN)
        edits.append({'jsonPointer': f'/$defs/{name}/enum', 'edit': f'{TOKEN} appended last', 'copyLine': last + 2})
    for name, (old, new) in MAX_ITEMS.items():
        start = [i for i, line in enumerate(lines) if line.strip() == json.dumps(name) + ': {']
        if len(start) != 1:
            raise SystemExit(f'cannot find {name}')
        hit = next(i for i in range(start[0], len(lines)) if lines[i].strip() == f'"maxItems": {old},')
        lines[hit] = lines[hit].replace(f'"maxItems": {old},', f'"maxItems": {new},')
        if expected['$defs'][name]['maxItems'] != old:
            raise SystemExit(f'{name} maxItems is not {old}')
        expected['$defs'][name]['maxItems'] = new
        edits.append({'jsonPointer': f'/$defs/{name}/maxItems', 'edit': f'{old} -> {new}', 'copyLine': hit + 1})
    sup = [i for i, line in enumerate(lines) if line.strip() == '"supersedes": [']
    if len(sup) != 1:
        raise SystemExit('cannot find supersedes')
    members = expected['x-opensip-wire-law']['supersedes']
    last = sup[0] + len(members)
    if lines[last].strip() != json.dumps(members[-1]) or lines[last + 1].strip() != '],':
        raise SystemExit('supersedes is not where expected')
    indent = lines[last][:len(lines[last]) - len(lines[last].lstrip())]
    lines[last] += ','
    lines.insert(last + 1, indent + json.dumps(SUPERSEDES_ADD))
    members.append(SUPERSEDES_ADD)
    edits.append({'jsonPointer': '/x-opensip-wire-law/supersedes', 'edit': 'one entry appended', 'copyLine': last + 2})
    anchor = [i for i, line in enumerate(lines) if line == '    "commitments": {']
    if len(anchor) != 1:
        raise SystemExit('cannot find the wire-law commitments entry')
    block = ['    "symbolCensus": {']
    items = list(SYMBOL_CENSUS_LAW.items())
    for n, (key, value) in enumerate(items):
        block.append('      ' + json.dumps(key) + ': ' + json.dumps(value) + (',' if n < len(items) - 1 else ''))
    block.append('    },')
    lines[anchor[0]:anchor[0]] = block
    expected['x-opensip-wire-law']['symbolCensus'] = dict(SYMBOL_CENSUS_LAW)
    edits.append({'jsonPointer': '/x-opensip-wire-law/symbolCensus', 'edit': 'entry added before commitments',
                  'copyLines': [anchor[0] + 1, anchor[0] + len(block)]})
    out = '\n'.join(lines).encode('ascii')
    if json.loads(out) != expected:
        raise SystemExit(f'{parent}: copy does not parse to the expected document')
    hunks = [{'parentLines': [i1 + 1, i2], 'copyLines': [j1 + 1, j2]} for tag, i1, i2, j1, j2 in
             difflib.SequenceMatcher(None, raw.decode().split('\n'), out.decode().split('\n'),
                                     autojunk=False).get_opcodes() if tag != 'equal']
    return out, {'parent': pin(parent, raw), 'copy': pin(COPIES[parent][0], out), 'boundOverridesCarried': [],
                 'fa2Edits': edits, 'hunks': hunks}


def build_overrides(section_text):
    ne_raw = read(NE)
    ne_text = ne_raw.decode('utf-8')
    by_newline, by_splitlines = ne_text.split('\n'), ne_text.splitlines()
    parent_pins = {path: pin(path, read(path)) for path in (NE, ST, PST)}
    out = []
    for line, anchor, text, _ in ne_overrides(section_text):
        before = by_splitlines[line - 1]
        if by_newline[line - 1] != before:
            raise SystemExit(f'line numbering differs at NE:{line}')
        out.append({'parent': parent_pins[NE], 'selector': {'line': line}, 'before': before,
                    'after': insert(before, anchor, text)})
    for parent in (ST, PST):
        document = json.loads(read(parent))
        for pointer, anchor, text in STARTUP_OVERRIDES:
            before = pointer_get(document, pointer)
            out.append({'parent': parent_pins[parent], 'selector': {'jsonPointer': pointer}, 'before': before,
                        'after': insert(before, anchor, text)})
    return out


def vectors():
    cases = json.loads(read(CASES))
    case = next(c for c in cases['cases'] if c['id'] == ORACLE_CASE)
    utf8 = case['steps'][0]['args']['canonicalUtf8']
    descriptor = json.loads(utf8)
    if C(descriptor) != utf8.encode('utf-8'):
        raise SystemExit('the encoder does not reproduce the oracle canonical bytes')
    oracle = scope(descriptor)
    if oracle['scopeId'] != case['expect']['$c.scopeId']:
        raise SystemExit('the encoder does not reproduce the oracle scope2')
    empty = scope(dict(descriptor, subjects=[]))
    # A TypeScript example. Identities are synthetic and labelled; only the recipes are claimed.
    snapshot = 'snapshot2:' + '1' * 64
    universe = '2' * 64
    closure = 'closure2:' + '3' * 64
    rows = [
        {'nativeSubjectId': 'ts:src/a.ts#a"b', 'path': 'src/a.ts', 'qualifiedName': 'a"b', 'exported': 'unknown',
         'signatureTokens': []},
        {'nativeSubjectId': 'ts:src/a.ts#a#b', 'path': 'src/a.ts', 'qualifiedName': 'a#b', 'exported': 'exported',
         'signatureTokens': ['function']},
        {'nativeSubjectId': 'ts:src/view.tsx#View', 'path': 'src/view.tsx', 'qualifiedName': 'View',
         'exported': 'exported', 'signatureTokens': ['function', 'View']},
    ]
    if [r['nativeSubjectId'].encode() for r in rows] != sorted(r['nativeSubjectId'].encode() for r in rows):
        raise SystemExit('example rows are not in nativeSubjectId order')
    census = {'state': 'complete', 'examinedPaths': canonical_set(['src/a.ts', 'src/util.js', 'src/view.tsx']),
              'rows': rows}
    subjects = canonical_set([r['nativeSubjectId'] for r in rows])
    keys = []
    for relation, rung in (('imports', 'resolved-target'), ('references', 'resolved-binding')):
        d_empty = {'schemaVersion': 2, 'snapshotId': snapshot, 'sourceUniverse': universe, 'targetUniverse': universe,
                   'relation': relation, 'resolution': rung, 'enumeratorClosure': closure, 'subjects': []}
        d_census = dict(d_empty, subjects=subjects)
        keys.append({'relation': relation, 'resolution': rung,
                     'requestCommitment': scope(d_empty)['subjectScopeCommitment'],
                     'returnCommitment': scope(d_census)['subjectScopeCommitment'],
                     'returnSubjectCount': len(subjects), 'canonicalDescriptorUtf8': C(d_census).decode('utf-8')})
    language = json.loads(read(SIS))['x-opensip-subject-language-table']['members']

    def subject_language(path):
        best = ('unspecified', 0)
        for member in language:
            for suffix in member['suffixes']:
                if path.endswith(suffix) and len(suffix) > best[1]:
                    best = (member['languageId'], len(suffix))
        return best[0]

    record = {'schemaVersion': 1, 'planId': 'plan2:' + '4' * 64, 'parameterDigest': '5' * 64, 'cellOrdinal': 0,
              'programOrdinal': 0, 'kind': 'symbol', 'state': 'complete', 'deficiency': None, 'nativeCause': None,
              'examinedPaths': census['examinedPaths'],
              'rows': [dict(r, kind='symbol', subjectLanguage=subject_language(r['path']), projections=[])
                       for r in rows]}
    return {
        'standing': ('Synthetic, labelled vectors for native-evidence 9.8 (FA-2). They fix recipes and orders, not '
                     'any real identity. Encoder: an independent two-line implementation of identity section 3 C '
                     'and H, checked first against native-evidence\'s own oracle case.'),
        'oracle': {'case': ORACLE_CASE, 'canonicalUtf8': utf8, 'expectedScopeId': case['expect']['$c.scopeId'],
                   'computed': oracle},
        'censusFreeOfOracleDescriptor': {'descriptor': dict(descriptor, subjects=[]), 'computed': empty},
        'typescriptExample': {
            'snapshotId': snapshot, 'universe': universe, 'enumeratorClosure': closure,
            'analyzeSymbolCensus': {'enumeratorClosure': closure},
            'completeSymbolCensus': census,
            'rowOrder': [r['nativeSubjectId'] for r in rows],
            'canonicalSetSubjectOrder': subjects,
            'orderNote': ('Rows are ordered by the UTF-8 bytes of nativeSubjectId; D.subjects is a canonical set, '
                          'ordered by canonical item bytes. \'"\' (0x22) precedes \'#\' (0x23) in UTF-8, but its '
                          'canonical spelling begins with a backslash (0x5c), so the two orders differ here.'),
            'keys': keys,
            'terminalSymbolEntry': {'subjectScopeCommitment': keys[0]['requestCommitment'], 'subjectCount': 0},
            'projectedInventory': record,
            'projectedInventoryDigest': sha(C(record)),
            'overBound': {'state': 'over-bound', 'rowCount': 100001, 'examinedPathCount': 2400},
        },
    }


def validate(deps, built):
    sys.path.insert(0, str(deps))
    sys.path.insert(0, str(ARCH / 'docs/coop/design-corrections/foundation'))
    import canonical  # noqa: E402  (the design encoder; needs jsonschema)
    schema = json.loads(built[CENSUS_DOC])
    sis = json.loads(read(SIS))

    def errors(doc, instance, ref):
        # The whole document is the root, so its own '#/$defs/...' references resolve; a root '$ref'
        # selects the record under test. SIS is validated as itself.
        wrapper = doc if ref is None else dict(doc, **{'$ref': ref})
        return [e.message for e in canonical.ExactValidator(wrapper).iter_errors(instance)]

    vec = json.loads(built[VECTORS])['typescriptExample']
    root = '#/$defs/'
    checks = []

    def expect(label, instance, ref, ok, doc=schema):
        found = errors(doc, instance, ref)
        if bool(found) == ok:
            raise SystemExit(f'validation {label}: expected {"valid" if ok else "invalid"}, got {found[:2]}')
        checks.append({'case': label, 'expected': 'valid' if ok else 'refused'})

    complete = vec['completeSymbolCensus']
    expect('complete census', complete, root + 'SymbolCensusV1', True)
    expect('over-bound census', vec['overBound'], root + 'SymbolCensusV1', True)
    expect('rows out of nativeSubjectId order', dict(complete, rows=list(reversed(complete['rows']))),
           root + 'SymbolCensusV1', False)
    expect('a host-filled member on a row', dict(complete, rows=[dict(complete['rows'][0], kind='symbol')]),
           root + 'SymbolCensusV1', False)
    expect('a partial census', dict(complete, state='partial'), root + 'SymbolCensusV1', False)
    expect('examinedPaths not a canonical set', dict(complete, examinedPaths=list(reversed(complete['examinedPaths']))),
           root + 'SymbolCensusV1', False)
    sha_text = 'sha256:' + '6' * 64
    ts_complete = {'analysisOrdinal': 0, 'stageResults': [{'stageId': 's', 'stageOrdinal': 0, 'factBatchCount': 0,
                   'factCount': 0, 'coverageEntryCount': 2, 'factCommitment': sha_text,
                   'coverageCommitment': sha_text}], 'factStreamCommitment': sha_text,
                   'coverageStreamCommitment': sha_text, 'symbolCensus': complete}
    expect('TypeScriptCompleteV2', ts_complete, root + 'TypeScriptCompleteV2', True)
    expect('TypeScriptCompleteV2 with null census', dict(ts_complete, symbolCensus=None), root + 'TypeScriptCompleteV2', True)
    expect('CompleteV1 without symbolCensus', {k: v for k, v in ts_complete.items() if k != 'symbolCensus'},
           root + 'TypeScriptCompleteV2', False)
    ts_analyze = {'analysisOrdinal': 0, 'executionId': 'exec', 'snapshotId': vec['snapshotId'],
                  'planId': 'plan2:' + '4' * 64, 'universeKey': 'sha256:' + vec['universe'],
                  'stageRequests': [{}], 'symbolCensus': vec['analyzeSymbolCensus']}
    expect('TypeScriptAnalyzeV2', ts_analyze, root + 'TypeScriptAnalyzeV2', True)
    rust_complete = {'analysisOrdinal': 0, 'stageResults': [{'stageId': 's', 'factCount': 0, 'coverageEntryCount': 2,
                     'factCommitment': sha_text, 'coverageCommitment': sha_text}], 'factStreamCommitment': sha_text,
                     'coverageStreamCommitment': sha_text, 'symbolCensus': vec['overBound']}
    expect('CompleteV3 (over-bound)', rust_complete, root + 'CompleteV3', True)
    expect('AnalyzeV3', {'analysisOrdinal': 0, 'executionId': 'exec', 'snapshotId': vec['snapshotId'],
                         'planId': 'plan2:' + '4' * 64, 'stages': [{}], 'symbolCensus': None}, root + 'AnalyzeV3', True)
    expect('projected SubjectInventoryV1 against SIS', vec['projectedInventory'], None, True, doc=sis)
    expect('projected record with a provider-side state carrier', dict(vec['projectedInventory'],
           deficiency='budget-exhausted'), None, False, doc=sis)
    return checks


def build(product, deps):
    section_text = read(SECTION).decode('utf-8').rstrip('\n')
    built, reports = {}, []
    for parent in (HS, PHS):
        out, report = handshake_copy(parent)
        built[COPIES[parent][0]] = out
        reports.append(report)
    if built[HS_COPY] != built[PHS_COPY]:
        raise SystemExit('the two handshake copies differ although their parents are identical')
    schema = dump(census_schema())
    built[CENSUS_DOC] = schema
    built[CENSUS_PRODUCT] = schema
    built[VECTORS] = dump(vectors())
    built[COPIES_REPORT] = dump({'standing': 'FA-2 JSON successor copies: every edit and every changed hunk.',
                                 'copies': reports})
    base = git_show(product, BASE_PRODUCT_HEAD, 'schemas/sources/handshake-v1.schema.json')
    if base != read(PHS):
        raise SystemExit('the product handshake source differs from its selected arch copy')
    built[MAP] = dump({
        'schemaVersion': 1,
        'standing': ('Exact schema source bytes for FA-2\'s implementing units: D2b copies each candidate to its '
                     'product path. Those units also add the census schema\'s source-map and admission rows, re-pin '
                     'the registries and regenerate carriers, which this map does not fix. Independent review and '
                     'root assent are required before selection.'),
        'baseProductHead': BASE_PRODUCT_HEAD,
        'files': [
            {'productPath': 'schemas/sources/handshake-v1.schema.json', 'candidatePath': PHS_COPY,
             'before': {'bytes': len(base), 'sha256': sha(base)},
             'after': {'bytes': len(built[PHS_COPY]), 'sha256': sha(built[PHS_COPY])}},
            {'productPath': 'schemas/sources/symbol-census-v1.schema.json', 'candidatePath': CENSUS_PRODUCT,
             'before': None, 'after': {'bytes': len(schema), 'sha256': sha(schema)}},
        ],
    })
    overrides = build_overrides(section_text)
    parents = sorted([pin(p, read(p)) for p in (NE, HS, ST, PHS, PST)], key=lambda r: r['path'])
    disk = {path: read(path) for path in (README, SECTION, BUILD)}
    candidate_bytes = dict(built, **disk)
    candidates = sorted([pin(p, b) for p, b in candidate_bytes.items()], key=lambda r: r['path'])
    successor = dump({
        'schemaVersion': 1,
        'standing': ('PROPOSED FA-2 r2 native contract successor (M3-H r1 X-H1; joined by M3-L r4): the provider symbol '
                     'census carrier. A new optional capability token symbol-census-v1 negotiates one added member, '
                     'symbolCensus, on the existing Analyze and Complete payloads of typescript-semantic major 2 and '
                     'rust-semantic major 3; symbol-kind keys commit to the census rule before spawn (the census-free '
                     'scope) and to its values on return. Text passage overrides of native-evidence (thirteen, '
                     'insert-only, one of them appending section 9.8), JSON Pointer overrides of the two '
                     'provider-startup copies (three each), complete successor copies of the two provider-handshake '
                     'copies, and a new census schema document with its product copy. No frame, phase, terminal, '
                     'limit member, identity version or major changes.'),
        'parents': parents,
        'passageOverrides': overrides,
        'candidates': candidates,
    })
    built[SUCCESSOR] = successor
    subject_rows = sorted(candidates + [pin(SUCCESSOR, successor)], key=lambda r: r['path'])
    built[SUBJECT] = dump({'schemaVersion': 1, 'files': subject_rows})
    lock_results = check_lock(product, parents, overrides, candidates, subject_rows)
    checks = validate(deps, built) if deps else None
    return built, lock_results, checks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--product', required=True)
    parser.add_argument('--deps')
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--lock-commit', action='append', default=[],
                        help='also check the product lock at this commit (repeatable)')
    args = parser.parse_args()
    LOCK_COMMITS.extend(c for c in args.lock_commit if c not in LOCK_COMMITS)
    built, lock_results, checks = build(Path(args.product), Path(args.deps) if args.deps else None)
    if args.check:
        bad = [p for p, b in built.items() if not (ARCH / p).is_file() or read(p) != b]
        if bad:
            raise SystemExit('differs from disk: ' + ', '.join(bad))
    else:
        for path, raw in built.items():
            (ARCH / path).parent.mkdir(parents=True, exist_ok=True)
            (ARCH / path).write_bytes(raw)
    print(json.dumps({'checked' if args.check else 'written': sorted(built), 'lock': lock_results,
                      'schemaValidation': checks}, indent=2))
    for path in sorted(built):
        print(sha(built[path]), len(built[path]), path)


if __name__ == '__main__':
    main()
