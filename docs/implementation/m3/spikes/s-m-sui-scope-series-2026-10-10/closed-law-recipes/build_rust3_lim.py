"""Build contract successor RUST3-LIM deterministically, and check it without the product's tools.

RUST3-LIM answers M3-L r3's X13 / R12: Rust3 caps a request's subject list at maxSubjectsPerStage (256), so a
Rust provider cannot be spawned for a repository with more than 256 non-empty .rs files. Under a new optional
rust-semantic capability token, subject-scope-reference-v1, each Analyze stage names its subject array by count
and commitment (RustSubjectScopeV1) instead of carrying it inline; both sides rebuild the array from the
SnapshotManifest the worker has already accepted. It writes, under docs/implementation/m3/native-successors-fa/:
  rust3-lim/design/native/provider-handshake.schemas.v1.json      (successor copy of FA-2's design copy)
  rust3-lim/product/schemas/sources/handshake-v1.schema.json      (successor copy of FA-2's product copy)
  rust3-lim/design/native/rust-subject-scope.schemas.v1.json      (new document: the stage records)
  rust3-lim/product/schemas/sources/rust-subject-scope-v1.schema.json  (product source copy of it)
  rust3-lim/materialization-map.json, rust3-lim/evidence/copies-report.json, rust3-lim/evidence/vectors.json,
  rust3-lim/successor.json and rust3-lim-subject.json.
It reads rust3-lim/section-9-3a.md and rust3-lim/README.md as written by the lead, and pins as candidates
evidence/count_rust_subjects.py, evidence/rust-subject-counts.json and evidence/verify_scratch.py as on disk.

Order. The two handshake copies take FA-2's candidates as parents, so this unit binds after FA-2. The lock
checks below therefore emulate FA-2 bound next, as its record and subject currently are on disk: FA-2's candidates
join the accepted set and its passage overrides join the bound selectors. This unit depends only on FA-2's two
handshake copies (FA2_COPY_PIN). If a later FA-2 round changes either copy, this build refuses and this unit needs
a parent-only rebuild; any other FA-2 change needs nothing here.

Each handshake copy is its parent's raw bytes with exactly these edits, in place: the token appended last to
RustCapabilityToken (no member moves), RustCapabilitiesV3.maxItems 14 -> 15, the document description, the
RustCapabilityToken description and FA-2's CapabilityToken supersedes entry extended (insert-only), and one
subjectScope wire-law entry added after FA-2's symbolCensus entry. TypeScript records are untouched.

The checks restate tools/verify_design.py's contract_successor and successor_chain rules for this record against
the product lock at every commit in LOCK_COMMITS: accepted parents at their pinned bytes, exact before texts, line
selectors on the Markdown parent only, no selector already bound (FA-2's included), candidates equal to the
subject minus the record, and fresh candidate paths. The vectors use an independent deterministic-CBOR encoder
(rust-provider-protocol.v2 canonicalCbor: length-first map-key order) and show that the by-reference domain
commits to the same domainCommitment as the inline one.

Usage (read-only on the product; git is used only to read the lock and one base blob):
    python3.14 -I -B evidence/build_rust3_lim.py --product /path/to/opensip [--deps DIR] [--check] [--lock-commit SHA]
--check rebuilds in memory and compares with the files on disk instead of writing.
--deps names a directory holding jsonschema 4.25.1; with it the vectors are also validated against the new schema
with the design encoder's ExactValidator (foundation/canonical.py).
"""
from __future__ import annotations

import argparse
import copy
import difflib
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ARCH = HERE.parents[5]
BASE = 'docs/implementation/m3/native-successors-fa'
UNIT = f'{BASE}/rust3-lim'
SUBJECT = f'{BASE}/rust3-lim-subject.json'
# Product main when this unit was assigned (I1-P bound; 82 contract successors). --lock-commit adds more.
LOCK_COMMITS = ['cd5958b3608f44a0035566c9d4500e5005c62e91']
BASE_PRODUCT_HEAD = LOCK_COMMITS[0]

NE = 'docs/v2/contracts/product-v1/native-evidence.md'
PHS_BASE = 'docs/implementation/m1/source-selection-v2/schemas/sources/handshake.v1.schema.json'
FA2_HS = f'{BASE}/fa-2/design/native/provider-handshake.schemas.v1.json'
FA2_PHS = f'{BASE}/fa-2/product/schemas/sources/handshake-v1.schema.json'
# FA-2, in review with Codex. This unit binds after it and depends only on FA-2's two handshake copies, whose
# bytes are pinned here and in successor.json's parents. FA-2's record and subject are read from disk as they
# currently are (they move between FA-2's review rounds); a change to either copy refuses this build.
FA2_RECORD_PATH = f'{BASE}/fa-2/successor.json'
FA2_SUBJECT_PATH = f'{BASE}/fa-2-subject.json'
FA2_COPY_PIN = {'bytes': 33812, 'sha256': '32aeec8c687639fd5633b37bce3c1873cf991eba70f3b08207fa6d47177658fd'}

TOKEN = 'subject-scope-reference-v1'
HS_COPY = f'{UNIT}/design/native/provider-handshake.schemas.v1.json'
PHS_COPY = f'{UNIT}/product/schemas/sources/handshake-v1.schema.json'
SCOPE_DOC = f'{UNIT}/design/native/rust-subject-scope.schemas.v1.json'
SCOPE_PRODUCT = f'{UNIT}/product/schemas/sources/rust-subject-scope-v1.schema.json'
SECTION = f'{UNIT}/section-9-3a.md'
README = f'{UNIT}/README.md'
BUILD = f'{UNIT}/evidence/build_rust3_lim.py'
COUNT = f'{UNIT}/evidence/count_rust_subjects.py'
COUNTS = f'{UNIT}/evidence/rust-subject-counts.json'
VERIFY = f'{UNIT}/evidence/verify_scratch.py'
VECTORS = f'{UNIT}/evidence/vectors.json'
COPIES_REPORT = f'{UNIT}/evidence/copies-report.json'
MAP = f'{UNIT}/materialization-map.json'
SUCCESSOR = f'{UNIT}/successor.json'

COPIES = {FA2_HS: HS_COPY, FA2_PHS: PHS_COPY}
MAX_SNAPSHOT_ENTRIES = 200000
MAX_SUBJECTS_PER_STAGE = 256
FRAME = 67108864

# ---------------------------------------------------------------------------------------------------
# Text passage overrides of native-evidence.md: (line, anchor or None, inserted text).
# Every override is insert-only: after = before[:i] + inserted + before[i:], where i is the end of the
# anchor (which occurs exactly once in the line), or the end of the line when anchor is None.
# None of these lines is bound by any successor at the lock commits or overridden by FA-2.
# ---------------------------------------------------------------------------------------------------

ROW_E = ("| `docs/coop/artifacts/rust-provider-protocol.v2.json` | "
         "`$.wireSchema.payloadSchemas.AnalyzeV2.fields.stages`, `$.wireSchema.definitions.StageRequestV2`, "
         "`$.wireSchema.definitions.StageAnalysisDomainV2`, "
         "`$.planAndDomainProjection.subjectsAlgorithm[2]`, only its comparison with `maxSubjectsPerStage` | "
         "**Retained** when `subject-scope-reference-v1` is not negotiated; **replaced** by `StageRequestV3` / "
         "`StageAnalysisDomainV3` / `RustSubjectScopeV1` (§9.3a) when it is, in `AnalyzeV2` and §9.8's "
         "`AnalyzeV3` alike. The subjects array is then rebuilt by host and worker from the accepted manifest and "
         "named by count and commitment, never sent, and `maxSubjectsPerStage` does not bound it. "
         "`subjectsAlgorithm` steps 1, 2, 4 and 5, step 3's sort, duplicate and empty rules, "
         "`commitments.subjectScope`, `commitments.analysisDomain`, `sameInputsRule`, `wireRule`, "
         "`independentDerivationRequirement` and `deterministicBudget` are **retained** in both cases, and "
         "`ProtocolLimitsV3` is unchanged. |")
ROW_F = ("| `docs/coop/design-corrections/native/native-evidence.schemas.v2.json` (registered bytes kept) | "
         "`#/$defs/CapabilityToken` | **Extended** for the `rust-semantic` Hello and HelloAck token arrays by "
         "`subject-scope-reference-v1` (§9.1, §9.3a), through RUST3-LIM's successor copy of "
         "`native/provider-handshake.schemas.v1.json`, whose `RustCapabilityToken` carries it. The registered "
         "document is not edited: its raw SHA-256 is a registered `payloadSchemaDigest` (§10). |")
TOKEN_LIST = " optional negotiated `subject-scope-reference-v1` (Rust; §9.3a),"
FRAME_ROW = ("| `Analyze` `stages` | host→worker | Historical `rust-provider-protocol.v2` `StageRequestV2`, with "
             "the inline `analysisDomain.subjects` array of at most `maxSubjectsPerStage`, when "
             "`subject-scope-reference-v1` is absent; `StageRequestV3` (§9.3a) when it is negotiated, in either "
             "`Analyze` payload: `analysisDomain.subjectScope` is `RustSubjectScopeV1` `{scopeKind, subjectCount, "
             "subjectScopeCommitment}`, and host and worker rebuild the array from the accepted manifest | no |")
STAGE_CORRELATION = (" (under negotiated `subject-scope-reference-v1`, §9.3a's `StageRequestV3`, which keeps "
                     "both members unchanged)")
STAGE_ECHO = " (`StageRequestV3.planStage.stageId` under negotiated `subject-scope-reference-v1`, §9.3a)"


def ne_overrides(section_text):
    return [
        (123, None, '\n' + ROW_E + '\n' + ROW_F),
        (2790, '`native-context-v2`,', TOKEN_LIST),
        (2883, None, '\n' + FRAME_ROW),
        (2942, None, '\n\n' + section_text),
        (3028, '`StageRequestV2`', STAGE_CORRELATION),
        (3070, '`StageRequestV2.planStage.stageId`', STAGE_ECHO),
    ]


# ---------------------------------------------------------------------------------------------------
# Handshake copy edits (on FA-2's copies).
# ---------------------------------------------------------------------------------------------------

DESCRIPTION_ANCHOR = 'and of the symbol-census-v1 token of section 9.8'
DESCRIPTION_INSERT = ', and of the rust-semantic subject-scope-reference-v1 token of section 9.3a'
SUPERSEDES_ANCHOR = 'add symbol-census-v1, native-evidence section 9.8'
SUPERSEDES_INSERT = '; RustCapabilityToken also adds subject-scope-reference-v1, native-evidence section 9.3a'
RUST_TOKEN_DESC_APPEND = (' subject-scope-reference-v1 (section 9.3a; contract successor RUST3-LIM) is also a '
                          'member, although the registered native-evidence.schemas.v2.json CapabilityToken does '
                          'not list it.')
MAX_ITEMS = {'RustCapabilitiesV3': (14, 15)}
SUBJECT_SCOPE_LAW = {
    'negotiated': ('rust-semantic only. Every member of the Analyze stages array (rust-provider-protocol.v2 AnalyzeV2, '
                   'or FA-2\'s AnalyzeV3 when symbol-census-v1 is also negotiated) is StageRequestV3, as published in '
                   'RUST3-LIM\'s rust-subject-scope.schemas.v1.json, iff subject-scope-reference-v1 is in both the '
                   'Hello and the HelloAck token arrays, whatever the subject count.'),
    'notNegotiated': 'rust-provider-protocol.v2 StageRequestV2 with its inline analysisDomain.subjects array, unchanged.',
    'violation': 'A StageRequestV3 without the token, or a StageRequestV2 with it, is PROVIDER.PROTOCOL_VIOLATION.',
    'limits': ('ProtocolLimitsV3 is unchanged and still checked by exact equality in Hello. Under the token '
               'maxSubjectsPerStage bounds only the historical inline array, which is not sent; the subject scope is '
               'bounded by the accepted manifest (1..SnapshotSeal.entryCount, at most maxSnapshotEntries).'),
    'planNeed': ('subject-scope-reference-v1 is not an identity token and does not enlarge the identity token set. It '
                 'is a token the Plan needs (native-evidence section 9.1, step 1) for a rust-semantic worker exactly '
                 'when the snapshot\'s subjects array is longer than maxSubjectsPerStage, and for no other.'),
    'majors': ('Protocol major stays 3. The token adds no frame, phase, terminal, limit member or identity version, '
               'and it is independent of target-attribution-v2 and symbol-census-v1. typescript-semantic is '
               'unaffected: delivery.v2 SubjectScopeV1 already names its file set by reference.'),
}
SUBJECT_SCOPE_ENTRY_AFTER = '    "symbolCensus": {'

# ---------------------------------------------------------------------------------------------------
# The new schema document.
# ---------------------------------------------------------------------------------------------------

LAW = {
    'standing': ('NORMATIVE field-level restatement of native-evidence section 9.3a (contract successor RUST3-LIM). '
                 'Section 9.3a is the prose owner; where they differ, that is a defect in whichever moved.'),
    'negotiation': ('Capability token subject-scope-reference-v1 (native-evidence 9.1), rust-semantic only. When it is '
                    'in both the Hello and the HelloAck token arrays, every member of the Analyze stages array '
                    '(rust-provider-protocol.v2 AnalyzeV2, or FA-2\'s AnalyzeV3 when symbol-census-v1 is also '
                    'negotiated) is StageRequestV3, whatever the subject count. When it is absent, StageRequestV2 '
                    'remains. Any other combination is PROVIDER.PROTOCOL_VIOLATION. The token is independent of '
                    'target-attribution-v2 and symbol-census-v1.'),
    'subjects': ('The subjects array is rust-provider-protocol.v2 planAndDomainProjection.subjectsAlgorithm steps 1, 2, '
                 '4 and 5 over the accepted SnapshotManifest entries, with step 3\'s (subjectsAlgorithm[2]) sort, '
                 'duplicate and empty rules and without its comparison with maxSubjectsPerStage. It is never sent.'),
    'commitments': ('RustSubjectScopeV1.subjectScopeCommitment is commitments.subjectScope over that array. '
                    'StageAnalysisDomainV3.domainCommitment is commitments.analysisDomain over {subjects: that array, '
                    'requestedCoverageDomain}. Both recipes are unchanged, so for equal inputs domainCommitment equals '
                    'the StageAnalysisDomainV2 value.'),
    'host': ('The host analysis-domain constructor builds the array before spawn from the sealed snapshot. sameInputsRule, '
             'wireRule and independentDerivationRequirement apply to StageAnalysisDomainV3 unchanged.'),
    'worker': ('After SnapshotAccepted the worker rebuilds the array from the manifest it accepted. Before any analysis '
               'it requires subjectCount, subjectScopeCommitment and domainCommitment of every stage to equal its own '
               'recomputation. On any difference it ends with ProviderFault input-rejected: PROVIDER.PROTOCOL_VIOLATION, '
               'with no facts, no Coverage and no Run (native-evidence section 10).'),
    'bounds': ('ProtocolLimitsV3 is unchanged in members and values and is still checked by exact equality in Hello. '
               'Under the token maxSubjectsPerStage bounds only the historical inline array. subjectCount is at least 1 '
               'and at most the accepted SnapshotSeal.entryCount, which is at most maxSnapshotEntries (200000). The '
               'sealed snapshot\'s 100000 inventory rows, 4 MiB descriptor and 8 GiB total apply first. No response '
               'bound is lifted, and limitPolicy semanticBudgetSeparation applies unchanged.'),
    'workUnits': ('rust-provider-protocol.v2 deterministicBudget is unchanged: one checked work-units increment before '
                  'each canonical (stage, subjectOrdinal, Coverage entryOrdinal) tuple, over the reconstructed ordinals.'),
    'planNeed': ('subject-scope-reference-v1 is a token the Plan needs (native-evidence 9.1, step 1) for a rust-semantic '
                 'worker exactly when the subjects array is longer than maxSubjectsPerStage. A signed row without it is '
                 'then never spawned (unknown / provider-unavailable, cause capability-missing). Otherwise it is '
                 'optional, and used when negotiated. Nothing splits, truncates or samples the array.'),
    'readingRule': ('Some texts name StageRequestV2 or StageAnalysisDomainV2 as the source of a Rust stage\'s '
                    'stageOrdinal, planStage or requestedCoverageDomain: native-evidence 9.6, the execution-inputs '
                    'contract\'s stage-id echo, provider-startup preAnalyzeUnavailable hostConversion and FA-2\'s '
                    'AnalyzeV3.stages. Under the token each reads the same member of StageRequestV3 or '
                    'StageAnalysisDomainV3.'),
    'unchanged': ('Protocol major 3. No frame, phase, terminal, limit member, identity version, commitment recipe or H '
                  'domain is added. expectedProtocolContractSha256 and protocol3-transitions.v1.json are unchanged. '
                  'typescript-semantic already names its file set by reference (delivery.v2 SubjectScopeV1) and is '
                  'unaffected.'),
    'internalKeys': [
        'native.subject-scope-stage-without-token',
        'native.subject-scope-token-without-stage',
        'native.subject-scope-count-mismatch',
        'native.subject-scope-commitment-mismatch',
        'native.subject-scope-domain-commitment-mismatch',
        'native.subject-scope-plan-need-unmet',
    ],
    'internalKeysStanding': ('Operational-record diagnostic keys only. None is a DomainDetailCode member, a D9 code, a '
                             'deficiency or a cause.'),
}


def scope_schema():
    sha_text = {'type': 'string', 'pattern': '^sha256:[0-9a-f]{64}(?![\\s\\S])'}
    return {
        '$schema': 'https://json-schema.org/draft/2020-12/schema',
        '$id': 'opensip.product.rust-subject-scope.1',
        'title': ('Rust subject scope by reference on negotiated Analyze stages (capability token '
                  'subject-scope-reference-v1)'),
        'description': ('NORMATIVE field-level publication for native-evidence section 9.3a (contract successor '
                        'RUST3-LIM). Closed JSON-vector forms of deterministic-CBOR wire maps: the rust-semantic stage '
                        'request, analysis domain and subject scope that replace StageRequestV2 and '
                        'StageAnalysisDomainV2 inside the Analyze stages array when subject-scope-reference-v1 is in '
                        'both the Hello and the HelloAck token arrays. Inherited members keep their names, types and '
                        'laws; planStage and requestedCoverageDomain are named by selector and not restated. Joins a '
                        'schema cannot express (the reconstruction from the accepted manifest, the commitments, the '
                        'Plan-time need) are stated in x-opensip-subject-scope-law.'),
        'x-opensip-subject-scope-law': LAW,
        '$defs': {
            'Uint64': {'type': 'integer', 'minimum': 0, 'maximum': 18446744073709551615},
            'Sha256Text': sha_text,
            'RustSubjectScopeV1': {
                'type': 'object',
                'additionalProperties': False,
                'required': ['scopeKind', 'subjectCount', 'subjectScopeCommitment'],
                'properties': {
                    'scopeKind': {'const': 'nonempty-rs-files',
                                  'description': ('rust-provider-protocol.v2 subjectsAlgorithm: every file-kind '
                                                  'SnapshotManifest entry whose path ends in .rs and whose byteLength '
                                                  'is greater than zero.')},
                    'subjectCount': {'type': 'integer', 'minimum': 1, 'maximum': MAX_SNAPSHOT_ENTRIES,
                                     'description': ('Length of the reconstructed subjects array; at most the accepted '
                                                     'SnapshotSeal.entryCount, which is at most maxSnapshotEntries.')},
                    'subjectScopeCommitment': {'$ref': '#/$defs/Sha256Text',
                                               'description': ('rust-provider-protocol.v2 commitments.subjectScope over '
                                                               'the reconstructed subjects array.')},
                },
                'description': ('The Rust subject array named by count and commitment. No snapshotId: Analyze carries '
                                'it, and every subjectId hashes it.'),
            },
            'StageAnalysisDomainV3': {
                'type': 'object',
                'additionalProperties': False,
                'required': ['subjectScope', 'requestedCoverageDomain', 'domainCommitment'],
                'properties': {
                    'subjectScope': {'$ref': '#/$defs/RustSubjectScopeV1'},
                    'requestedCoverageDomain': {
                        'type': 'array', 'minItems': 1, 'maxItems': 256, 'items': {'type': 'object'},
                        'x-opensip-order': 'sequence',
                        'description': ('rust-provider-protocol.v2 StageAnalysisDomainV2.requestedCoverageDomain, '
                                        'unchanged in members and law (coverageDomainAlgorithm, at most '
                                        'maxRequestedCoverageKeysPerStage; each key\'s subjectScopeCommitment per '
                                        'native-evidence section 0 and 4.1a). Not restated here.')},
                    'domainCommitment': {'$ref': '#/$defs/Sha256Text',
                                         'description': ('rust-provider-protocol.v2 commitments.analysisDomain over '
                                                         '{subjects: the reconstructed array, requestedCoverageDomain}; '
                                                         'equal to the StageAnalysisDomainV2 value for equal inputs.')},
                },
                'description': 'StageAnalysisDomainV2 with its inline subjects array replaced by subjectScope.',
            },
            'StageRequestV3': {
                'type': 'object',
                'additionalProperties': False,
                'required': ['stageOrdinal', 'planStage', 'analysisDomain'],
                'properties': {
                    'stageOrdinal': {'$ref': '#/$defs/Uint64',
                                     'description': 'StageRequestV2.stageOrdinal, unchanged: contiguous Analyze order.'},
                    'planStage': {'type': 'object',
                                  'description': ('StageRequestV2.planStage, unchanged: the exact nested C-2 stage '
                                                  'value (planStageByteRule). Not restated here.')},
                    'analysisDomain': {'$ref': '#/$defs/StageAnalysisDomainV3'},
                },
                'description': ('rust-semantic Analyze stages member when subject-scope-reference-v1 is negotiated, in '
                                'AnalyzeV2 or FA-2\'s AnalyzeV3 alike.'),
            },
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
        token = token.replace('~1', '/').replace('~0', '~')
        value = value[int(token)] if isinstance(value, list) else value[token]
    return value


def insert(before, anchor, text):
    if anchor is None:
        return before + text
    if before.count(anchor) != 1:
        raise SystemExit(f'anchor not unique: {anchor!r}')
    i = before.index(anchor) + len(anchor)
    return before[:i] + text + before[i:]


def insert_only(before, after):
    """True when after is before with exactly one contiguous insertion."""
    extra = len(after) - len(before)
    return extra > 0 and any(after[:i] == before[:i] and after[i + extra:] == before[i:]
                             for i in range(len(before) + 1))


def head(major, n):
    if n < 24:
        return bytes([major << 5 | n])
    for extra, width in ((24, 1), (25, 2), (26, 4), (27, 8)):
        if n < 1 << (8 * width):
            return bytes([major << 5 | extra]) + n.to_bytes(width, 'big')
    raise SystemExit('integer out of uint64 range')


def cbor(value):
    """rust-provider-protocol.v2 canonicalCbor: RFC 8949 core deterministic, length-first map-key order."""
    if value is None:
        return b'\xf6'
    if value is True:
        return b'\xf5'
    if value is False:
        return b'\xf4'
    if isinstance(value, int):
        if value < 0:
            raise SystemExit('negative integer')
        return head(0, value)
    if isinstance(value, str):
        raw = value.encode('utf-8')
        return head(3, len(raw)) + raw
    if isinstance(value, bytes):
        return head(2, len(value)) + value
    if isinstance(value, list):
        return head(4, len(value)) + b''.join(cbor(v) for v in value)
    if isinstance(value, dict):
        items = sorted(((cbor(k), cbor(v)) for k, v in value.items()), key=lambda kv: (len(kv[0]), kv[0]))
        if len({k for k, _ in items}) != len(items):
            raise SystemExit('duplicate map key')
        return head(5, len(items)) + b''.join(k + v for k, v in items)
    raise SystemExit(f'unsupported value {type(value)}')


def domain_hash(domain, value):
    return 'sha256:' + hashlib.sha256(domain.encode('ascii') + b'\0' + cbor(value)).hexdigest()


def subjects_from(snapshot_id, entries, cap=None):
    """subjectsAlgorithm steps 1-5; cap=None is RUST3-LIM's reconstruction (step 3 without the cap)."""
    chosen = sorted((e for e in entries if e['kind'] == 'file' and e['path'].endswith('.rs') and e['byteLength'] > 0),
                    key=lambda e: e['path'].encode('utf-8'))
    paths = [e['path'] for e in chosen]
    if len(set(paths)) != len(paths):
        raise SystemExit('duplicate path')
    if not chosen:
        raise SystemExit('empty subject set: refused before spawn')
    if cap is not None and len(chosen) > cap:
        raise SystemExit('over maxSubjectsPerStage: refused before spawn')
    return [{'subjectOrdinal': i,
             'subjectId': 'rust-file:sha256:' + hashlib.sha256(
                 b'opensip.rust-provider.subject.v2\0' + cbor({'snapshotId': snapshot_id, 'path': e['path'],
                                                               'contentSha256': e['contentSha256'],
                                                               'byteLength': e['byteLength']})).hexdigest(),
             'path': e['path'], 'startByte': 0, 'endByte': e['byteLength']} for i, e in enumerate(chosen)]


# ---------------------------------------------------------------------------------------------------
# Lock checks (verify_design's contract_successor and successor_chain rules, restated), with FA-2 bound first.
# ---------------------------------------------------------------------------------------------------

def check_pin(row):
    raw = read(row['path'])
    if len(raw) != row['bytes'] or sha(raw) != row['sha256']:
        raise SystemExit(f'pin differs: {row["path"]}')
    return raw


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
            bound[(entry['parent']['path'], json.dumps(entry['selector'], sort_keys=True))] = binding['record']['path']
    for binding in lock['inventorySuccessors']:
        accepted[binding['candidate']['path']] = binding['candidate']
        accepted[binding['parent']['path']] = binding['parent']
    return accepted, bound, len(lock['contractSuccessors'])


def bind_fa2(accepted, bound):
    """Emulate FA-2 bound next in the chain, as its record and subject currently are on disk."""
    subject_raw = read(FA2_SUBJECT_PATH)
    subject = json.loads(subject_raw)
    record_raw = read(FA2_RECORD_PATH)
    record = json.loads(record_raw)
    members = {row['path']: row for row in subject['files']}
    if members.get(FA2_RECORD_PATH) != pin(FA2_RECORD_PATH, record_raw):
        raise SystemExit('FA-2 record is not in its subject')
    for path in COPIES:
        row = members.get(path)
        if row is None or {k: row[k] for k in ('bytes', 'sha256')} != FA2_COPY_PIN:
            raise SystemExit(f'FA-2 handshake copy changed: {path}; rebuild this unit on it')
    for row in subject['files']:
        check_pin(row)
        if row['path'] in accepted:
            raise SystemExit(f'FA-2 candidate reuses an accepted path: {row["path"]}')
    for row in record['parents']:
        have = accepted.get(row['path'])
        if have is None or have['sha256'] != row['sha256']:
            raise SystemExit(f'FA-2 parent is not accepted: {row["path"]}')
    for entry in record['passageOverrides']:
        key = (entry['parent']['path'], json.dumps(entry['selector'], sort_keys=True))
        if key in bound:
            raise SystemExit(f'FA-2 selector already bound: {key}')
        bound[key] = FA2_RECORD_PATH
    for row in subject['files']:
        accepted[row['path']] = row
    return {'record': pin(FA2_RECORD_PATH, record_raw), 'subject': pin(FA2_SUBJECT_PATH, subject_raw),
            'passageOverrides': len(record['passageOverrides'])}


def check_lock(product, parents, overrides, candidates, subject_rows):
    results = []
    for commit in LOCK_COMMITS:
        accepted, bound, count = lock_state(product, commit)
        before_fa2 = sorted(p['path'] for p in parents if p['path'] not in accepted)
        fa2 = bind_fa2(accepted, bound)
        for row in parents:
            have = accepted.get(row['path'])
            if have is None or have['sha256'] != row['sha256'] or have['bytes'] != row['bytes']:
                raise SystemExit(f'{commit[:7]}: parent is not an accepted base: {row["path"]}')
        bound_copied = sorted({path for (path, _) in bound} & set(COPIES))
        if bound_copied:
            raise SystemExit(f'{commit[:7]}: a copied parent carries a bound override: {bound_copied}')
        for entry in overrides:
            key = (entry['parent']['path'], json.dumps(entry['selector'], sort_keys=True))
            if key in bound:
                raise SystemExit(f'{commit[:7]}: selector already bound by {bound[key]}: {key}')
        for row in subject_rows:
            if row['path'] in accepted:
                raise SystemExit(f'{commit[:7]}: candidate reuses an accepted path: {row["path"]}')
        ne_bound = sorted(json.loads(sel)['line'] for (path, sel) in bound if path == NE)
        results.append({'commit': commit, 'contractSuccessors': count, 'fa2BoundNext': fa2,
                        'parentsNotAcceptedWithoutFa2': before_fa2,
                        'parentsAccepted': True, 'copiedParentsWithBoundOverrides': 0,
                        'neLinesBoundIncludingFa2': ne_bound, 'rust3LimSelectorsAlreadyBound': 0,
                        'candidatePathsFresh': True})
    seen = set()
    for entry in overrides:
        key = (entry['parent']['path'], json.dumps(entry['selector'], sort_keys=True))
        if key in seen:
            raise SystemExit('duplicate override')
        seen.add(key)
        parent_raw = read(entry['parent']['path'])
        try:
            json.loads(parent_raw)
        except ValueError:
            pass
        else:
            raise SystemExit('line selector on a JSON parent')
        current = parent_raw.decode('utf-8').splitlines()[entry['selector']['line'] - 1]
        if current != entry['before'] or not entry['after'] or entry['after'] == entry['before']:
            raise SystemExit(f'override before text differs: {entry["selector"]}')
        if not insert_only(entry['before'], entry['after']):
            raise SystemExit(f'override is not insert-only: {entry["selector"]}')
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
        nonlocal text
        old = pointer_get(expected, pointer)
        if text.count(json.dumps(old)) != 1:
            raise SystemExit(f'cannot place {pointer}')
        text = text.replace(json.dumps(old), json.dumps(new))
        tokens = pointer[1:].split('/')
        target = expected
        for token in tokens[:-1]:
            target = target[int(token)] if isinstance(target, list) else target[token]
        target[int(tokens[-1]) if isinstance(target, list) else tokens[-1]] = new
        edits.append({'jsonPointer': pointer, 'edit': 'string extended (insert-only)'})

    replace_string('/description', insert(expected['description'], DESCRIPTION_ANCHOR, DESCRIPTION_INSERT))
    sup = expected['x-opensip-wire-law']['supersedes']
    hits = [i for i, s in enumerate(sup) if SUPERSEDES_ANCHOR in s]
    if len(hits) != 1:
        raise SystemExit('cannot find FA-2\'s CapabilityToken supersedes entry')
    replace_string(f'/x-opensip-wire-law/supersedes/{hits[0]}',
                   insert(sup[hits[0]], SUPERSEDES_ANCHOR, SUPERSEDES_INSERT))
    replace_string('/$defs/RustCapabilityToken/description',
                   expected['$defs']['RustCapabilityToken']['description'] + RUST_TOKEN_DESC_APPEND)
    lines = text.split('\n')
    members = expected['$defs']['RustCapabilityToken']['enum']
    if TOKEN in members:
        raise SystemExit('token already present')
    want = [json.dumps(m) for m in members]
    hits = [i for i, line in enumerate(lines) if line.strip() == '"enum": ['
            and [l.strip().rstrip(',') for l in lines[i + 1:i + 1 + len(members)]] == want
            and lines[i + 1 + len(members)].strip().startswith(']')]
    if len(hits) != 1:
        raise SystemExit('cannot place the RustCapabilityToken enum')
    last = hits[0] + len(members)
    indent = lines[last][:len(lines[last]) - len(lines[last].lstrip())]
    lines[last] += ','
    lines.insert(last + 1, indent + json.dumps(TOKEN))
    members.append(TOKEN)
    edits.append({'jsonPointer': '/$defs/RustCapabilityToken/enum', 'edit': f'{TOKEN} appended last',
                  'copyLine': last + 2})
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
    start = [i for i, line in enumerate(lines) if line == SUBJECT_SCOPE_ENTRY_AFTER]
    if len(start) != 1:
        raise SystemExit('cannot find FA-2\'s symbolCensus wire-law entry')
    end = next(i for i in range(start[0], len(lines)) if lines[i] == '    },')
    block = ['    "subjectScope": {']
    items = list(SUBJECT_SCOPE_LAW.items())
    for n, (key, value) in enumerate(items):
        block.append('      ' + json.dumps(key) + ': ' + json.dumps(value) + (',' if n < len(items) - 1 else ''))
    block.append('    },')
    lines[end + 1:end + 1] = block
    law = expected['x-opensip-wire-law']
    reordered = {}
    for key, value in law.items():
        reordered[key] = value
        if key == 'symbolCensus':
            reordered['subjectScope'] = dict(SUBJECT_SCOPE_LAW)
    expected['x-opensip-wire-law'] = reordered
    edits.append({'jsonPointer': '/x-opensip-wire-law/subjectScope', 'edit': 'entry added after symbolCensus',
                  'copyLines': [end + 2, end + 1 + len(block)]})
    out = '\n'.join(lines).encode('ascii')
    if json.loads(out) != expected or list(json.loads(out)['x-opensip-wire-law']) != list(reordered):
        raise SystemExit(f'{parent}: copy does not parse to the expected document')
    for name in ('TypeScriptCapabilityToken', 'TypeScriptCapabilitiesV2', 'ProtocolLimitsV3', 'HelloV3', 'HelloAckV3',
                 'TypeScriptHelloV2', 'TypeScriptHelloAckV2', 'TypeScriptProtocolLimitsV1'):
        if json.loads(out)['$defs'][name] != json.loads(raw)['$defs'][name]:
            raise SystemExit(f'{name} changed')
    hunks = [{'parentLines': [i1 + 1, i2], 'copyLines': [j1 + 1, j2]} for tag, i1, i2, j1, j2 in
             difflib.SequenceMatcher(None, raw.decode().split('\n'), out.decode().split('\n'),
                                     autojunk=False).get_opcodes() if tag != 'equal']
    return out, {'parent': pin(parent, raw), 'copy': pin(COPIES[parent], out), 'boundOverridesCarried': [],
                 'unchangedDefs': ['TypeScriptCapabilityToken', 'TypeScriptCapabilitiesV2', 'ProtocolLimitsV3',
                                   'HelloV3', 'HelloAckV3', 'TypeScriptHelloV2', 'TypeScriptHelloAckV2',
                                   'TypeScriptProtocolLimitsV1'],
                 'rust3LimEdits': edits, 'hunks': hunks}


def build_overrides(section_text):
    ne_raw = read(NE)
    ne_text = ne_raw.decode('utf-8')
    by_newline, by_splitlines = ne_text.split('\n'), ne_text.splitlines()
    ne_pin = pin(NE, ne_raw)
    out = []
    for line, anchor, text in ne_overrides(section_text):
        before = by_splitlines[line - 1]
        if by_newline[line - 1] != before:
            raise SystemExit(f'line numbering differs at NE:{line}')
        out.append({'parent': ne_pin, 'selector': {'line': line}, 'before': before, 'after': insert(before, anchor, text)})
    return out


def vectors():
    snapshot = 'snapshot2:' + '1' * 64
    universe = 'sha256:' + '2' * 64

    def entry(path, length, digit, kind='file'):
        if kind == 'symlink':
            return {'path': path, 'kind': 'symlink', 'byteLength': None, 'contentSha256': None, 'executable': None,
                    'targetBytesHex': b'lib.rs'.hex()}
        return {'path': path, 'kind': 'file', 'byteLength': length, 'contentSha256': digit * 64, 'executable': False,
                'targetBytesHex': None}
    entries = [entry('Cargo.toml', 120, 'a'), entry('build.rs', 0, 'b'), entry('src/lib.rs', 2048, 'c'),
               entry('src/link.rs', None, None, 'symlink'), entry('src/main.rs', 512, 'd'),
               entry('tests/it.rs', 300, 'e')]
    if [e['path'].encode() for e in entries] != sorted(e['path'].encode() for e in entries):
        raise SystemExit('manifest entries are not path-sorted')
    subjects = subjects_from(snapshot, entries)
    if subjects_from(snapshot, entries, cap=MAX_SUBJECTS_PER_STAGE) != subjects:
        raise SystemExit('reconstruction differs from the inline algorithm under the cap')
    key = {'relation': 'references', 'resolution': 'resolved-binding', 'sourceUniverseId': universe,
           'targetUniverseId': universe, 'subjectScopeCommitment': 'sha256:' + '7' * 64,
           'producer': 'rust-semantic', 'producerVersion': 'synthetic-provider-build', 'schemaVersion': 1}
    plan_stage = {'kind': 'fact-derivation', 'stageId': 'rust-references', 'operator': 'semantic-provider',
                  'providerId': 'rust-semantic', 'relations': ['references']}
    scope_commitment = domain_hash('opensip.rust-provider.subject-scope.v2', subjects)
    domain_commitment = domain_hash('opensip.rust-provider.analysis-domain.v2',
                                    {'subjects': subjects, 'requestedCoverageDomain': [key]})
    inline = {'stageOrdinal': 0, 'planStage': plan_stage,
              'analysisDomain': {'subjects': subjects, 'requestedCoverageDomain': [key],
                                 'domainCommitment': domain_commitment}}
    reference = {'stageOrdinal': 0, 'planStage': plan_stage,
                 'analysisDomain': {'subjectScope': {'scopeKind': 'nonempty-rs-files', 'subjectCount': len(subjects),
                                                     'subjectScopeCommitment': scope_commitment},
                                    'requestedCoverageDomain': [key], 'domainCommitment': domain_commitment}}
    # Worker side: rebuild from the accepted manifest and compare.
    rebuilt = subjects_from(snapshot, entries)
    worker_ok = (len(rebuilt) == reference['analysisDomain']['subjectScope']['subjectCount']
                 and domain_hash('opensip.rust-provider.subject-scope.v2', rebuilt) == scope_commitment
                 and domain_hash('opensip.rust-provider.analysis-domain.v2',
                                 {'subjects': rebuilt, 'requestedCoverageDomain': [key]}) == domain_commitment)
    if not worker_ok:
        raise SystemExit('worker reconstruction does not reproduce the by-reference domain')
    reversed_commitment = domain_hash('opensip.rust-provider.subject-scope.v2', list(reversed(subjects)))

    def projection(count, path_bytes=60):
        rows = [{'subjectOrdinal': i, 'subjectId': 'rust-file:sha256:' + 'f' * 64,
                 'path': ('p' * (path_bytes - 3 - len(str(i)))) + str(i) + '.rs', 'startByte': 0, 'endByte': 4096}
                for i in range(count)]
        inline_bytes = len(cbor(rows))
        ref_bytes = len(cbor({'scopeKind': 'nonempty-rs-files', 'subjectCount': count,
                              'subjectScopeCommitment': 'sha256:' + '0' * 64}))
        return {'subjects': count, 'pathBytes': path_bytes, 'inlineSubjectsArrayBytes': inline_bytes,
                'stagesFittingOneAnalyzeFrameInline': FRAME // inline_bytes, 'subjectScopeBytes': ref_bytes}
    return {
        'standing': ('Synthetic, labelled vectors for native-evidence 9.3a (RUST3-LIM). They fix recipes and orders, not '
                     'any real identity; planStage and the Coverage key are illustrative shapes, not validated C-2 '
                     'values. Encoder: an independent implementation of rust-provider-protocol.v2 canonicalCbor '
                     '(length-first map-key order).'),
        'snapshotId': snapshot,
        'manifestEntries': entries,
        'excluded': {'Cargo.toml': 'not .rs', 'build.rs': 'byteLength 0', 'src/link.rs': 'symlink'},
        'subjects': subjects,
        'subjectScopeCommitment': scope_commitment,
        'domainCommitment': domain_commitment,
        'stageRequestV2Inline': inline,
        'stageRequestV3ByReference': reference,
        'equalities': {
            'domainCommitmentEqualAcrossV2AndV3': True,
            'workerRebuildReproducesCountAndCommitments': True,
            'reconstructionEqualsInlineAlgorithmUnderCap': True,
        },
        'cborBytes': {'stageRequestV2Inline': len(cbor(inline)), 'stageRequestV3ByReference': len(cbor(reference)),
                      'subjectsArray': len(cbor(subjects))},
        'refusals': [
            {'case': 'subjectCount one too high', 'value': len(subjects) + 1,
             'expected': 'worker ProviderFault input-rejected -> PROVIDER.PROTOCOL_VIOLATION'},
            {'case': 'commitment over the array in reverse order', 'value': reversed_commitment,
             'expected': 'worker ProviderFault input-rejected -> PROVIDER.PROTOCOL_VIOLATION'},
            {'case': 'StageRequestV3 when the token was not negotiated',
             'expected': 'PROVIDER.PROTOCOL_VIOLATION'},
            {'case': 'StageRequestV2 when the token was negotiated', 'expected': 'PROVIDER.PROTOCOL_VIOLATION'},
            {'case': 'subjectCount 0 or above 200000', 'expected': 'schema refusal: PROVIDER.PROTOCOL_VIOLATION'},
            {'case': 'token absent and more than 256 subjects',
             'expected': 'Plan time: never spawned; unknown / provider-unavailable, cause capability-missing'},
        ],
        'sizeProjection': {
            'standing': ('Synthetic 60-byte paths and 4096-byte files; subjectId fixed at 81 characters. Inline bytes '
                         'are what each stage of one Analyze frame carries today; the by-reference scope is constant.'),
            'maxFramePayloadBytes': FRAME,
            'rows': [projection(n) for n in (256, 27000, 100000, 200000)],
        },
    }


def validate(deps, built):
    sys.path.insert(0, str(deps))
    sys.path.insert(0, str(ARCH / 'docs/coop/design-corrections/foundation'))
    import canonical  # noqa: E402  (the design encoder; needs jsonschema)
    schema = json.loads(built[SCOPE_DOC])
    vec = json.loads(built[VECTORS])
    checks = []

    def expect(label, instance, name, ok):
        wrapper = dict(schema, **{'$ref': '#/$defs/' + name})
        found = [e.message for e in canonical.ExactValidator(wrapper).iter_errors(instance)]
        if bool(found) == ok:
            raise SystemExit(f'validation {label}: expected {"valid" if ok else "invalid"}, got {found[:2]}')
        checks.append({'case': label, 'expected': 'valid' if ok else 'refused'})
    ref = vec['stageRequestV3ByReference']
    scope = ref['analysisDomain']['subjectScope']
    expect('StageRequestV3', ref, 'StageRequestV3', True)
    expect('RustSubjectScopeV1', scope, 'RustSubjectScopeV1', True)
    expect('subjectCount 0', dict(scope, subjectCount=0), 'RustSubjectScopeV1', False)
    expect('subjectCount 200000', dict(scope, subjectCount=MAX_SNAPSHOT_ENTRIES), 'RustSubjectScopeV1', True)
    expect('subjectCount 200001', dict(scope, subjectCount=MAX_SNAPSHOT_ENTRIES + 1), 'RustSubjectScopeV1', False)
    expect('another scopeKind', dict(scope, scopeKind='all-snapshot-files'), 'RustSubjectScopeV1', False)
    expect('a snapshotId member', dict(scope, snapshotId=vec['snapshotId']), 'RustSubjectScopeV1', False)
    expect('a boolean subjectCount', dict(scope, subjectCount=True), 'RustSubjectScopeV1', False)
    expect('inline subjects inside StageAnalysisDomainV3',
           dict(ref['analysisDomain'], subjects=vec['subjects']), 'StageAnalysisDomainV3', False)
    expect('the inline V2 stage request as a StageRequestV3', vec['stageRequestV2Inline'], 'StageRequestV3', False)
    expect('no requested keys', dict(ref['analysisDomain'], requestedCoverageDomain=[]), 'StageAnalysisDomainV3', False)
    return checks


def counts_check():
    spec = importlib.util.spec_from_file_location('count_rust_subjects', ARCH / COUNT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    e0, t2b = module.SCRATCH / 'e0/t2a/git', module.SCRATCH / 't2b/results'
    if not (e0.is_dir() and t2b.is_dir()):
        return 'not re-derived: the scratch sources are absent on this machine'
    out = (json.dumps(module.build(e0, t2b), indent=2) + '\n').encode('ascii')
    if out != read(COUNTS):
        raise SystemExit('rust-subject-counts.json does not reproduce')
    return 'reproduced from the E0 trees and the T2b listings'


def build(product, deps):
    section_text = read(SECTION).decode('utf-8').rstrip('\n')
    built, reports = {}, []
    for parent in (FA2_HS, FA2_PHS):
        out, report = handshake_copy(parent)
        built[COPIES[parent]] = out
        reports.append(report)
    if built[HS_COPY] != built[PHS_COPY]:
        raise SystemExit('the two handshake copies differ although their parents are identical')
    schema = dump(scope_schema())
    built[SCOPE_DOC] = schema
    built[SCOPE_PRODUCT] = schema
    built[VECTORS] = dump(vectors())
    built[COPIES_REPORT] = dump({'standing': ('RUST3-LIM JSON successor copies of FA-2\'s two handshake copies: every '
                                              'edit and every changed hunk.'), 'copies': reports})
    base = git_show(product, BASE_PRODUCT_HEAD, 'schemas/sources/handshake-v1.schema.json')
    if base != read(PHS_BASE):
        raise SystemExit('the product handshake source differs from its selected arch copy')
    fa2_after = read(FA2_PHS)
    built[MAP] = dump({
        'schemaVersion': 1,
        'standing': ('Exact schema source bytes for RUST3-LIM\'s implementing units: D2b copies each candidate to its '
                     'product path. The handshake candidate already contains FA-2\'s edits, so it replaces FA-2\'s '
                     'handshake candidate as the materialization source; FA-2 binds first. Those units also add the new '
                     'schema\'s source-map and admission rows, re-pin the registries and regenerate carriers, which this '
                     'map does not fix. Independent review and root assent are required before selection.'),
        'baseProductHead': BASE_PRODUCT_HEAD,
        'files': [
            {'productPath': 'schemas/sources/handshake-v1.schema.json', 'candidatePath': PHS_COPY,
             'before': {'bytes': len(base), 'sha256': sha(base)},
             'afterFa2': {'bytes': len(fa2_after), 'sha256': sha(fa2_after)},
             'after': {'bytes': len(built[PHS_COPY]), 'sha256': sha(built[PHS_COPY])}},
            {'productPath': 'schemas/sources/rust-subject-scope-v1.schema.json', 'candidatePath': SCOPE_PRODUCT,
             'before': None, 'after': {'bytes': len(schema), 'sha256': sha(schema)}},
        ],
    })
    overrides = build_overrides(section_text)
    parents = sorted([pin(p, read(p)) for p in (NE, FA2_HS, FA2_PHS)], key=lambda r: r['path'])
    disk = {path: read(path) for path in (README, SECTION, BUILD, COUNT, COUNTS, VERIFY)}
    candidate_bytes = dict(built, **disk)
    candidates = sorted([pin(p, b) for p, b in candidate_bytes.items()], key=lambda r: r['path'])
    successor = dump({
        'schemaVersion': 1,
        'standing': ('PROPOSED RUST3-LIM native contract successor (M3-L r3 X13 / R12): the Rust3 request subject list '
                     'by reference. A new optional rust-semantic capability token subject-scope-reference-v1 replaces '
                     'each Analyze stage\'s inline subjects array (at most maxSubjectsPerStage, 256) with '
                     'RustSubjectScopeV1 {scopeKind, subjectCount, subjectScopeCommitment}; host and worker rebuild the '
                     'array from the accepted SnapshotManifest, the commitment recipes are unchanged, and the scope is '
                     'bounded by the manifest (maxSnapshotEntries) and the sealed snapshot. The token is needed exactly '
                     'when a snapshot has more than 256 subjects. Text passage overrides of native-evidence (six, '
                     'insert-only, one of them appending section 9.3a), complete successor copies of FA-2\'s two '
                     'provider-handshake copies (binds after FA-2), and a new stage-record schema document with its '
                     'product copy. No frame, phase, terminal, limit member or value, identity version or major '
                     'changes.'),
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
                      'counts': counts_check(), 'schemaValidation': checks}, indent=2))
    for path in sorted(built):
        print(sha(built[path]), len(built[path]), path)


if __name__ == '__main__':
    main()
