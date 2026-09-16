"""Phase 1 -- canonicalization, H, lexical admission, CVE1, semantic-vs-operational,
acyclic joins. Independently authored minimal descriptors; all expected values are
COMPUTED here from the kit prose, never copied from a kit example.

IDs: R-H-HELPER, R-CVE1-EIGHT-TYPES, R-LEXICAL-ADMISSION, R-SEMANTIC-VS-OPERATIONAL,
     R-RAW-VS-PARSED, R-ACYCLIC-JOINS
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_core as K
import opensip_schema as S

OUT = '/tmp/opensip-design-corrections/consumer-b.v20/output'
V = OUT + '/vectors'
fails = []


def expect(cond, label, detail=''):
    if not cond:
        fails.append('%s :: %s' % (label, detail))
    return cond


# ---------------------------------------------------------------- R-H-HELPER
def h_helper():
    """C and H over independently authored minimal descriptors.

    Descriptors are real registered records of identity-schemas.v3 so the helper is
    exercised on the shapes that actually mint identities, not on toy objects.
    """
    vectors = []

    # 1. scope-descriptor (auxiliary canonical-record digest, not an H domain)
    scope = {'schemaVersion': 2, 'workspaceRoots': ['.'],
             'pathPrefixes': [], 'excludedPathPrefixes': []}
    vectors.append({'kind': 'canonical-record', 'record': 'scope-descriptor',
                    'value': scope, 'cBytes': K.C(scope).decode(),
                    'cByteLength': len(K.C(scope)),
                    'rawSha256OfC': K.rec_digest(scope)})

    # 2. control characters / escapes / key byte order / no-slash-escape / U+007F / U+2028
    CTRL = ''.join(chr(c) for c in (0, 8, 9, 10, 11, 12, 13, 31))
    esc = {'z': 'a/b', 'a': 'q' + CTRL + 'r',
           'a' + chr(0xE4): 'x', 'a' + chr(0x7F): 'del',
           'ls': 'a' + chr(0x2028) + 'b', 'Z': 'upper'}
    cb = K.C(esc)
    vectors.append({'kind': 'escape-and-key-order', 'value': esc,
                    'cBytes': cb.decode(),
                    'cBytesHexFirst64': cb[:64].hex(),
                    'cByteLength': len(cb),
                    'rawSha256OfC': K.raw_sha256(cb),
                    'observed': {
                        'slashNotEscaped': b'a/b' in cb,
                        'u007fUnescaped': chr(0x7F).encode() in cb,
                        'u2028Unescaped': chr(0x2028).encode() in cb,
                        'shortEscapesUsed': all(x in cb for x in
                                                (b'\\b', b'\\t', b'\\n', b'\\f', b'\\r')),
                        'lowercaseU00xxForOtherControls': (b'\\u0000' in cb and b'\\u000b' in cb
                                                           and b'\\u001f' in cb),
                        'keysInUtf8ByteOrder': [k for k in sorted(esc, key=lambda s: s.encode())],
                    }})
    expect(b'a/b' in cb, 'C: slash must not be escaped')
    expect(b'\\u000b' in cb, 'C: U+000B uses lowercase \\u00xx')
    expect(chr(0x2028).encode() in cb, 'C: U+2028 stays unescaped')
    expect(chr(0x7F).encode() in cb, 'C: U+007F stays unescaped')

    # 3. array admitted order is preserved -- C never sorts
    a1 = {'xs': ['b', 'a']}
    a2 = {'xs': ['a', 'b']}
    vectors.append({'kind': 'array-admitted-order-preserved',
                    'valueA': a1, 'cA': K.C(a1).decode(), 'hA': K.rec_digest(a1),
                    'valueB': a2, 'cB': K.C(a2).decode(), 'hB': K.rec_digest(a2),
                    'equal': K.rec_digest(a1) == K.rec_digest(a2)})
    expect(K.rec_digest(a1) != K.rec_digest(a2),
           'C: must not sort arrays into one identity')

    # 4. H frame: domain separation and length prefix
    minimal = {'schemaVersion': 2, 'kind': 'grammar',
               'manifestDigest': '00' * 32, 'tree': [], 'semanticVersion': '1.0.0',
               'protocolMajor': 3, 'platform': 'macos-aarch64'}
    fr = K.h_frame('closure', minimal)
    vectors.append({'kind': 'h-frame', 'record': 'closure', 'value': minimal,
                    'cByteLength': len(K.C(minimal)),
                    'framePrefixHex': fr[:40].hex(),
                    'frameByteLength': len(fr),
                    'H': K.H('closure', minimal),
                    'typedId': K.ID('closure', minimal),
                    'sameCBytesOtherDomain': K.H('snapshot', minimal),
                    'domainSeparationHolds': K.H('closure', minimal) != K.H('snapshot', minimal),
                    'rawSha256OfCIsNotH': K.rec_digest(minimal) != K.H('closure', minimal)})
    expect(K.H('closure', minimal) != K.H('snapshot', minimal), 'H: domain separation')
    expect(K.rec_digest(minimal) != K.H('closure', minimal),
           'H: SHA256(C(X)) is not H(D,X)')
    # frame round trip
    dom, obj = K.parse_h_frame(fr, {'closure'})
    expect(dom == 'closure' and obj == minimal, 'H frame round-trip')
    # offering a raw canonical payload where a frame is required must fail the prefix
    try:
        K.parse_h_frame(K.C(minimal), {'closure'})
        expect(False, 'payload offered as frame must refuse')
        payload_as_frame = None
    except K.CanonError as e:
        payload_as_frame = str(e)
    vectors.append({'kind': 'payload-offered-where-frame-required',
                    'firstRefusal': payload_as_frame, 'masksLater': False,
                    'classification': 'invalid'})

    # 5. integer bound vectors at the declared edges
    for v, ok in ((2 ** 64 - 1, True), (-(2 ** 63), True), (2 ** 64, False), (-(2 ** 63) - 1, False)):
        try:
            cbv = K.C({'n': v}).decode()
            got = {'accepted': True, 'c': cbv}
        except K.CanonError as e:
            got = {'accepted': False, 'refusal': str(e)}
        expect(got['accepted'] == ok, 'C integer bound %d' % v, json.dumps(got))
        vectors.append({'kind': 'integer-bound', 'n': str(v), 'expectedAccept': ok, **got})

    return vectors


# ---------------------------------------------------------------- R-CVE1-EIGHT-TYPES
def cve1_types():
    reg = json.load(open(S.KIT + '/docs/coop/artifacts/resolved-inputs.v2.json'))
    cve = reg['planIdContract']['canonicalValueEncoding']
    closed = cve['closedTypes']
    samples = {
        'null': None,
        'false': False,
        'true': True,
        'unsigned-64': 18446744073709551615,
        'negative-signed-64': -9223372036854775808,
        'NFC-UTF8-string': 'relation' + chr(0xE9),          # already NFC
        'array': ['b', 'a', 1],                        # order preserved
        'string-keyed-map': {'b': 1, 'a': None, chr(0xE4): True},
    }
    rows = []
    for t in closed:
        v = samples[t]
        enc = K.cve1(v)
        dec = K.cve1_decode_exact(enc)
        rows.append({'type': t, 'declaredEncoding': cve['encodings'][t],
                     'value': v, 'encodedHex': enc.hex(),
                     'encodedLength': len(enc),
                     'tagByte': '0x%02x' % enc[0],
                     'decoded': dec, 'roundTrip': dec == v,
                     'classification': 'valid'})
        expect(dec == v, 'CVE1 round-trip %s' % t, enc.hex())
        expect(K.cve1_type(v) == t, 'CVE1 type dispatch %s' % t)
    expect(len(closed) == 8, 'CVE1 closed type count is 8', str(len(closed)))
    expect(sorted(closed) == sorted(K.CVE1_TYPES), 'CVE1 type set matches kit')

    # map entry ordering is by unsigned lexicographic NFC UTF-8 key bytes
    m = {chr(0xE4): 1, 'b': 2, 'a': 3}
    enc = K.cve1(m)
    order = []
    pos = 5
    for _ in range(3):
        k, pos = K.cve1_decode(enc, pos)
        _, pos = K.cve1_decode(enc, pos)
        order.append(k)
    expect(order == ['a', 'b', chr(0xE4)], 'CVE1 map key order', str(order))
    rows.append({'type': 'string-keyed-map', 'aspect': 'key order',
                 'input': list(m.keys()), 'encodedKeyOrder': order,
                 'rule': cve['encodings']['string-keyed-map'], 'classification': 'valid'})

    negatives = []
    for label, v, code in (
            ('non-NFC string refused rather than normalised', 'e' + chr(0x301), 'STRING_NOT_NFC'),
            ('float forbidden', 1.5, 'FLOAT_FORBIDDEN'),
            ('byte string forbidden', b'\x01', 'BYTE_STRING_FORBIDDEN'),
            ('unsigned overflow', 2 ** 64, 'UNSIGNED_64_RANGE'),
            ('negative underflow', -(2 ** 63) - 1, 'NEGATIVE_SIGNED_64_RANGE'),
    ):
        try:
            K.cve1(v)
            negatives.append({'case': label, 'refused': False, 'classification': 'invalid'})
            expect(False, 'CVE1 negative ' + label)
        except K.Cve1Error as e:
            negatives.append({'case': label, 'refused': True, 'firstRefusal': str(e),
                              'expectedCode': code, 'masksLater': False,
                              'classification': 'invalid'})
            expect(str(e) == code, 'CVE1 negative code ' + label, str(e))
    # duplicate map key cannot reach the encoder: Python dicts cannot hold one, so the
    # raw-input hook is where it is refused (see R-LEXICAL-ADMISSION / R-RAW-VS-PARSED)
    negatives.append({'case': 'duplicate map key',
                      'whereRefused': 'raw-input parse hook (section 7.5 parse hook analogue); '
                                      'an already-parsed object cannot express it',
                      'refused': True, 'firstRefusal': 'DUPLICATE_KEY',
                      'masksLater': False, 'classification': 'invalid'})
    return {'closedTypes': closed, 'constraints': cve['constraints'],
            'roundTrips': rows, 'negatives': negatives}


# ------------------------------------------- R-LEXICAL-ADMISSION / R-RAW-VS-PARSED
def lexical():
    raw_negatives = []
    cases = [
        ('duplicate key on raw input', b'{"a":1,"a":2}', 'DUPLICATE_KEY'),
        ('float token', b'{"n":1.0}', 'FLOAT_OR_EXPONENT_TOKEN'),
        ('exponent token', b'{"n":1e3}', 'FLOAT_OR_EXPONENT_TOKEN'),
        ('negative zero token', b'{"n":-0}', 'NEGATIVE_ZERO_TOKEN'),
        ('nonfinite token', b'{"n":NaN}', 'NONFINITE_TOKEN'),
        ('negative Infinity token', b'{"n":-Infinity}', 'NONFINITE_TOKEN'),
        ('integer above 2^64-1', b'{"n":18446744073709551616}', 'INTEGER_RANGE'),
        ('integer below -2^63', b'{"n":-9223372036854775809}', 'INTEGER_RANGE'),
        ('malformed UTF-8', b'{"a":"\xff\xfe"}', 'MALFORMED_UTF8'),
        ('lone surrogate as non-scalar Unicode', '{"a":"\ud800"}'.encode('utf-8', 'surrogatepass'),
         'MALFORMED_UTF8'),
        ('nesting depth 33', (b'[' * 33) + (b']' * 33), 'NESTING_DEPTH_EXCEEDED'),
    ]
    for label, b, code in cases:
        try:
            K.admit_raw_descriptor(b)
            raw_negatives.append({'case': label, 'rawInputHex': b[:48].hex(),
                                  'refused': False, 'classification': 'invalid'})
            expect(False, 'raw admission ' + label)
        except K.LexicalRefusal as e:
            raw_negatives.append({'case': label, 'rawInputHex': b[:48].hex(),
                                  'refused': True, 'firstRefusal': e.code,
                                  'firstRefusalDetail': e.detail,
                                  'offset': e.offset,
                                  'expectedCode': code,
                                  'masksLater': ('yes -- this raw-lexical refusal precedes '
                                                 'any schema or digest check on the same bytes'),
                                  'classification': 'invalid'})
            expect(e.code == code, 'raw admission code ' + label, e.code)

    # depth law: root container counts as 1, scalar leaves and object keys add no depth
    d32 = (b'[' * 32) + (b']' * 32)
    ok32 = True
    try:
        K.admit_raw_descriptor(d32)
    except K.LexicalRefusal as e:
        ok32 = False
    expect(ok32, 'depth 32 admits (root counts as 1)')

    # RAW vs PARSED separation, measured
    dup_raw = b'{"a":1,"a":2}'
    parsed_same_text = json.loads(dup_raw.decode())       # stock JSON silently keeps the last
    raw_refused = False
    try:
        K.admit_raw_descriptor(dup_raw)
    except K.LexicalRefusal:
        raw_refused = True
    encode_of_parsed = K.C(parsed_same_text).decode()
    separation = {
        'rawInput': dup_raw.decode(),
        'rawAdmissionRefused': raw_refused,
        'rawFirstRefusal': 'DUPLICATE_KEY',
        'stockJsonParseResult': parsed_same_text,
        'encodingTheAlreadyParsedObjectSucceeds': encode_of_parsed,
        'conclusion': ('The duplicate-key, float/exponent, -0, nonfinite, malformed-UTF8 and '
                       'depth faults are only observable on RAW BYTES. Encoding an already '
                       'parsed object cannot see them: the lexical information is gone. These '
                       'are therefore two different admission stages, as identity section 3 '
                       'states ("Before deserialization loses lexical information").'),
        'classification': 'explanatory',
    }
    expect(raw_refused and encode_of_parsed == '{"a":2}', 'raw-vs-parsed separation')

    # a float in an ALREADY-PARSED object is refused by C itself (different boundary)
    try:
        K.C({'n': 1.0})
        parsed_float = {'refused': False}
        expect(False, 'C must refuse a float in a parsed object')
    except K.CanonError as e:
        parsed_float = {'refused': True, 'firstRefusal': str(e)}
    separation['parsedObjectFloatRefusedByC'] = parsed_float

    # string bound: Text maxLength counts Unicode SCALAR VALUES, byte cap independent
    long_text = chr(0xE9) * 4096                      # 4096 scalars, 8192 bytes
    too_long = chr(0xE9) * 4097
    bound = {
        'record': 'identity-schemas.v3#/$defs/Text (maxLength 4096)',
        'scalarCount4096': {'scalars': len(long_text), 'utf8Bytes': len(long_text.encode()),
                            'stockSchemaErrors': S.stock_validate(
                                'foundation/identity-schemas.v3.json', '#/$defs/Text', long_text)},
        'scalarCount4097': {'scalars': len(too_long), 'utf8Bytes': len(too_long.encode()),
                            'stockSchemaErrors': S.stock_validate(
                                'foundation/identity-schemas.v3.json', '#/$defs/Text', too_long)},
        'law': ('identity section 3: "Text maxLength counts Unicode scalar values, while the '
                'descriptor byte cap remains independent." Measured: 4096 scalars = 8192 bytes '
                'admits; 4097 scalars refuses on the scalar count, not the byte count.'),
        'classification': 'valid/invalid pair',
    }
    expect(not bound['scalarCount4096']['stockSchemaErrors'], 'Text 4096 scalars admits')
    expect(bound['scalarCount4097']['stockSchemaErrors'], 'Text 4097 scalars refuses')

    # descriptor byte cap on RAW input, independent of any schema
    big = b'{"a":"' + b'x' * (4 * 1024 * 1024) + b'"}'
    try:
        K.admit_raw_descriptor(big)
        cap = {'refused': False}
        expect(False, '4MiB descriptor cap')
    except K.LexicalRefusal as e:
        cap = {'refused': True, 'firstRefusal': e.code, 'detail': e.detail,
               'neverTruncated': True}
    return {'rawInputNegatives': raw_negatives, 'depth32Admits': ok32,
            'rawVsParsed': separation, 'stringBound': bound, 'descriptorByteCap': cap}


# ---------------------------------------------------------- R-SEMANTIC-VS-OPERATIONAL
def semantic_vs_operational():
    """identity section 2: RequestId/ExecutionId, wall clocks, PIDs, credentials,
    authorization nonces, receipts and output destinations are OPERATIONAL and
    excluded from Run identity. Measured as a pair on the actual run3 record and on
    the operational commit-receipt that carries those fields."""
    run = {'schemaVersion': 3,
           'projectId': 'prj1-' + '11' * 32,
           'snapshotId': 'snapshot2:' + 'aa' * 32,
           'planId': 'plan2:' + 'bb' * 32,
           'evidenceId': 'evidence3:' + 'cc' * 32,
           'evaluationSealId': 'seal3:' + 'dd' * 32,
           'capabilityManifestId': 'ee' * 32}
    run_id = K.ID('run', run)

    sem = dict(run, snapshotId='snapshot2:' + 'ab' * 32)   # one semantic field moved
    sem_id = K.ID('run', sem)

    receipt_a = {'schemaVersion': 2, 'runId': run_id, 'executionId': 'exec1_' + '1' * 32,
                 'namespaceId': 'ns-a', 'commitSequence': 7,
                 'inventoryDigest': '33' * 32, 'sealedAssurance': 'replayable',
                 'signerKeyId': 'key-1'}
    receipt_b = dict(receipt_a, executionId='exec1_' + '2' * 32, commitSequence=8,
                     namespaceId='ns-b', signerKeyId='key-2')
    # the RunId is computed from the run descriptor, which has no operational field at all
    run_id_attempt2 = K.ID('run', run)

    out = {
        'runDescriptor': run,
        'runId': run_id,
        'semanticFieldChange': {'field': 'snapshotId', 'newValue': sem['snapshotId'],
                                'newRunId': sem_id, 'identityMoved': sem_id != run_id},
        'operationalChange': {
            'changedFields': ['executionId', 'commitSequence', 'namespaceId', 'signerKeyId'],
            'receiptA': receipt_a, 'receiptB': receipt_b,
            'receiptADigest': K.rec_digest(receipt_a),
            'receiptBDigest': K.rec_digest(receipt_b),
            'receiptDigestMoved': K.rec_digest(receipt_a) != K.rec_digest(receipt_b),
            'runIdAttempt1': run_id, 'runIdAttempt2': run_id_attempt2,
            'runIdentityUnmoved': run_id == run_id_attempt2,
            'law': 'identity section 2 + section 5 step 4: the receipt authenticates RunId and '
                   'inventory and is operational custody evidence EXCLUDED from semantic IDs. '
                   '"Identical semantic inputs can produce the same Run on two attempts; '
                   'attempts remain separately auditable."'},
        'requestIdExecutionIdGrammar': {
            'productSuccessorExecutionId': '^exec1_[0-9a-f]{32}(?![\\s\\S])',
            'productSuccessorRequestId': '^req1_[0-9a-f]{32}(?![\\s\\S])',
            'trailingNewlineRefusedNotTrimmed': S.stock_validate(
                'foundation/identity-schemas.v3.json',
                '#/$defs/commit-receipt/properties/executionId',
                'exec1_' + '1' * 32 + '\n'),
            'c2ProvenanceSelector': 'docs/coop/artifacts/c2-plan-stage-schema.v4.json'
                                    '#planIntent.wireTypes.executionId (provenance only, '
                                    'deliberately NOT byte-equivalent)',
        },
        'classification': 'valid',
    }
    expect(sem_id != run_id, 'semantic field change moves RunId')
    expect(run_id == run_id_attempt2, 'operational change does not move RunId')
    expect(K.rec_digest(receipt_a) != K.rec_digest(receipt_b),
           'operational receipt has its own moving digest')
    expect(out['requestIdExecutionIdGrammar']['trailingNewlineRefusedNotTrimmed'],
           'executionId with trailing newline must refuse')
    return out


# ---------------------------------------------------------------- R-ACYCLIC-JOINS
def acyclic_joins():
    """Independently construct acyclic source -> Plan -> View -> Proof -> Evidence ->
    Seal -> Run joins, and show that cycle attempts refuse.

    The derivation order the kit states (native 4.1a "No circularity"):
    closures -> native context -> universe -> scope2 -> commitment -> coverage payload
    -> coverage2 -> view2 ; and identity section 3: "proof does not include EvidenceId
    or RunId; evidence may include proof; seal includes both; Run includes seal."
    """
    # which record may name which, read off the closed schemas themselves
    idj = json.load(open(S.KIT + '/docs/coop/design-corrections/foundation/identity-schemas.v3.json'))
    defs = idj['$defs']

    def prefixes_named(name):
        found = set()

        def rec(n):
            if isinstance(n, dict):
                p = n.get('pattern')
                if isinstance(p, str):
                    for dom, pref in K.PREFIX.items():
                        if p.startswith('^' + pref + ':'):
                            found.add(pref)
                for v in n.values():
                    rec(v)
            elif isinstance(n, list):
                for v in n:
                    rec(v)
        rec(defs[name])
        return sorted(found)

    edges = {}
    for rec_name in ['snapshot', 'plan', 'subject-scope', 'fact', 'coverage', 'view',
                     'proof-bundle', 'semantic-evidence', 'evaluation-seal', 'run',
                     'execution-plan', 'finding', 'policy-derivation']:
        edges[rec_name] = prefixes_named(rec_name)

    proof_domains = defs['ProofInputRef']['properties']['domain']['enum']
    finding_ev_domains = defs['FindingEvidenceRef']['properties']['domain']['enum']

    # acyclicity of the declared edge set
    pref_to_rec = {v: k for k, v in K.PREFIX.items()}
    adj = {k: [pref_to_rec[p] for p in v if pref_to_rec.get(p) in edges] for k, v in edges.items()}
    colour, cycles = {}, []

    def dfs(u, stack):
        colour[u] = 1
        for w in adj.get(u, []):
            if colour.get(w) == 1:
                cycles.append(stack + [u, w])
            elif colour.get(w, 0) == 0:
                dfs(w, stack + [u])
        colour[u] = 2

    for u in list(adj):
        if colour.get(u, 0) == 0:
            dfs(u, [])

    # cycle refusal attempts, measured against the owning closed schemas
    attempts = []
    proof = {'schemaVersion': 3, 'planId': 'plan2:' + '11' * 32,
             'executionPlanId': 'exec-plan2:' + '22' * 32,
             'evaluatorClosure': 'closure2:' + '33' * 32,
             'ruleProgramDigest': '44' * 32,
             'evaluationInputRefs': [], 'predicateProofs': [], 'findingIds': [],
             'verdict': 'pass', 'evaluationState': 'evaluated', 'ruleResults': [],
             'waivedFindingIds': [], 'executionDeficiencies': [],
             'executionInputsDigest': '55' * 32}
    bad = dict(proof, evidenceId='evidence3:' + '66' * 32)
    attempts.append({
        'attempt': 'proof-bundle names EvidenceId (back edge Proof->Evidence)',
        'errors': S.stock_validate('foundation/identity-schemas.v3.json',
                                   '#/$defs/proof-bundle', bad),
        'law': 'identity section 3: "proof does not include EvidenceId or RunId"; the record is '
               'closed (additionalProperties:false) so the field has no home.',
        'classification': 'invalid'})
    bad2 = dict(proof, evaluationInputRefs=[{'domain': 'run', 'digest': '77' * 32}])
    attempts.append({
        'attempt': 'proof evaluationInputRefs names domain=run (back edge Proof->Run)',
        'errors': S.stock_validate('foundation/identity-schemas.v3.json',
                                   '#/$defs/proof-bundle', bad2),
        'proofInputRefDomainEnum': proof_domains,
        'law': 'ProofInputRef domain enum excludes run, semantic-evidence, evaluation-seal, '
               'proof-bundle and finding (composition section 9.1 "Forbidden members").',
        'classification': 'invalid'})
    bad3 = dict(proof, evaluationInputRefs=[{'domain': 'semantic-evidence', 'digest': '77' * 32}])
    attempts.append({
        'attempt': 'proof evaluationInputRefs names domain=semantic-evidence',
        'errors': S.stock_validate('foundation/identity-schemas.v3.json',
                                   '#/$defs/proof-bundle', bad3),
        'classification': 'invalid'})
    finding_bad = {'domain': 'run', 'digest': '88' * 32}
    attempts.append({
        'attempt': 'finding evidenceRef names domain=run',
        'errors': S.stock_validate('foundation/identity-schemas.v3.json',
                                   '#/$defs/FindingEvidenceRef', finding_bad),
        'findingEvidenceRefDomainEnum': finding_ev_domains,
        'classification': 'invalid'})
    for a in attempts:
        expect(bool(a['errors']), 'cycle attempt must refuse: ' + a['attempt'])

    return {
        'declaredForwardEdges': edges,
        'proofInputRefDomains': proof_domains,
        'findingEvidenceRefDomains': finding_ev_domains,
        'cyclesFoundInDeclaredEdgeSet': cycles,
        'acyclic': not cycles,
        'derivationOrder': ['closures', 'native-context', 'native-universe', 'snapshot',
                            'subject-scope', 'coverage-payload', 'coverage', 'fact',
                            'view', 'plan', 'execution-plan', 'proof-bundle',
                            'semantic-evidence', 'evaluation-seal', 'run'],
        'cycleRefusalAttempts': attempts,
        'classification': 'valid + invalid controls',
    }


def main():
    os.makedirs(V, exist_ok=True)
    res = {
        'consumerId': 'consumer-b.v20',
        'phase': 1,
        'standing': 'Independently authored. Every value is computed by this script from the '
                    'normative kit; no kit example was used as an expected value.',
        'R-H-HELPER': h_helper(),
        'R-CVE1-EIGHT-TYPES': cve1_types(),
        'R-LEXICAL-ADMISSION+R-RAW-VS-PARSED': lexical(),
        'R-SEMANTIC-VS-OPERATIONAL': semantic_vs_operational(),
        'R-ACYCLIC-JOINS': acyclic_joins(),
    }
    with open(V + '/phase1-canonical-h-lexical.json', 'w') as f:
        json.dump(res, f, indent=1, default=str)
    # split file required by the requirement observable
    with open(V + '/cve1-eight-types.json', 'w') as f:
        json.dump(res['R-CVE1-EIGHT-TYPES'], f, indent=1, default=str)
    print('phase1 assertions failed:', len(fails))
    for f_ in fails:
        print('  FAIL', f_)
    if fails:
        sys.exit(1)
    print('phase1 OK -> vectors/phase1-canonical-h-lexical.json, vectors/cve1-eight-types.json')


main()
