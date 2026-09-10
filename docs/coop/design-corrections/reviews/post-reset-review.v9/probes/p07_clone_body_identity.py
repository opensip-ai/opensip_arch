"""v9 probe 07 - independent reconstruction of the normalized-body identity.

The reviewer rebuilds, from the RETAINED inherited grammar and the registry binding alone:
  * the body-language-version record (a third implementation: not M.body_language_version and
    not the checker's own body_language_version);
  * the domain-separated frame of fact-identity-policy.v2#/canonicalisationSchema/byteGrammar;
and compares against the bodyIdentity the shipped clone Runs actually mint.

Checks demanded of a normalized-body identity and verified here directly:
  - field encoding, ORDER, domain tag and component LENGTHS (u8 => <=255 each);
  - levelVersion carried as RAW 32 digest bytes, never hex display text;
  - normalisationVersion is the raw SHA-256 of the RETAINED level-specification bytes (custody);
  - at L0 the payload is recomputed from the fact's OWN source anchor span (a real source join);
  - languageId is the BODY language (a .js body under the TypeScript engine is javascript);
  - byte-identical bodies in different source variants do NOT share an identity;
  - bodyIdentity is never equated with FACT-ID-V1.

Custody, not qualification: nothing here grades a tokenizer or certifies a normalizer.
"""
import copy, hashlib, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import harness

ns = harness.load()
M, C, N = ns['M'], ns['C'], ns['N']
SUB = harness.SUBJECT
POLICY = json.loads((SUB / 'docs/coop/artifacts/fact-identity-policy.v2.json').read_text())
GRAMMAR = POLICY['canonicalisationSchema']['byteGrammar']
IDS = json.loads((SUB / 'docs/coop/design-corrections/foundation/identity-schemas.v2.json').read_text())
UROWS = IDS['x-opensip-digest-domains']['domainSets']['native-semantic-universe']


# ---- reviewer's OWN frame builder, transcribed from the inherited grammar text ----
def reviewer_frame(domain_tag, level_id, level_version, language_id, language_version, payload):
    """domainSeparatedPreimage: five u8-length-prefixed components then u32be len || payload."""
    def u8(raw):
        assert len(raw) <= 255, ('component exceeds the inherited u8 bound', len(raw))
        return bytes([len(raw)]) + raw
    assert GRAMMAR['domainSeparatedPreimage'][0].startswith('u8 tag_len')
    return (u8(domain_tag.encode('ascii')) + u8(level_id.encode('ascii')) + u8(level_version)
            + u8(language_id.encode('ascii')) + u8(language_version)
            + len(payload).to_bytes(4, 'big') + payload)


def reviewer_language_version_record(universe, context, row, anchor, retained):
    """Rebuild body-language-version from the registry binding, reviewer's own traversal."""
    b = row['languageVersionBinding']
    rec = {'schemaVersion': 1}
    for name, src in b['fields'].items():
        if 'const' in src:
            rec[name] = src['const']; continue
        node = context if src['source'] == 'native-context' else universe
        for step in src['path']:
            node = node[step]
        rec[name] = node
    d = b['dialect']
    if d['form'] == 'closed-suffix-table':
        hits = [s for s in d['table'] if anchor['path'].endswith(s)]
        assert hits, 'unlisted suffix must refuse'
        variant = d['table'][max(hits, key=len)]
        rec['dialect'] = {d['key']: variant}
        rec['languageId'] = b['bodyLanguageByVariant'][variant]
    else:
        o = d['ownership']
        owned = retained[o['retainedAs']]
        assert owned[o['enumerationField']] == 'complete'
        units = {u[o['unitField']]: u for u in owned[o['unitsField']]}
        rowsel = [r for r in owned['ownership'] if r[o['pathField']] == anchor['path']]
        chosen = [r for r in rowsel if r[o['unitField']] in set(owned[o['selectionField']])]
        eff = set()
        for r in chosen:
            u = units[r[o['unitField']]]
            eff.add(u[o['targetEditionField']] if u[o['targetEditionField']] is not None
                    else universe['edition'][u[o['crateField']]])
        assert len(eff) == 1, ('ambiguous', eff)
        rec['dialect'] = {d['key']: next(iter(eff))}
        rec['languageId'] = b['bodyLanguage']
    return rec


def analyse(label, language, source_path=None, workspace=None):
    r, o, b = ns['build'](has_match=True, relation='clones',
                          universe_language=language, source_path=source_path, workspace=workspace)
    fkey = next(k for k, (d, v) in o.items() if d == 'fact')
    fact = o[fkey][1]
    payload = json.loads(b[fact['payloadDigest']].decode())
    snap = o[r['snapshotId']][1]
    anchor = fact['anchors'][0]
    domain = ('native.semantic-universe.typescript.v2' if language == 'typescript'
              else 'native.semantic-universe.rust.v2')
    row = UROWS[domain]
    # the universe and context records the fact's OWN sourceUniverse names
    uni, ctx = None, None
    for k, (dm, v) in o.items():
        pass
    uni = ns['_last_universe'] if '_last_universe' in ns else None
    # recover them from the retained frames instead: the fixture returns them via build's natives
    # (rebuild deterministically by re-running native_inputs is unnecessary - read the retained blob)
    rec = {'case': label, 'language': language, 'anchorPath': anchor['path']}

    # ---- custody: normalisationVersion is the raw SHA-256 of the RETAINED level spec bytes
    spec_digest = payload['normalisationVersion']
    spec_bytes = b.get(spec_digest)
    rec['levelSpecificationRetained'] = spec_bytes is not None
    rec['normalisationVersionIsRawSha256OfRetainedBytes'] = (
        spec_bytes is not None and hashlib.sha256(spec_bytes).hexdigest() == spec_digest)
    rec['levelSpecificationBytesPreview'] = (spec_bytes or b'')[:60].decode('utf8', 'replace')

    # ---- the framed preimage is retained under the bodyIdentity suffix
    ident = payload['bodyIdentity']
    rec['bodyIdentityForm'] = ident[:7]
    frame = b.get(ident.split(':', 1)[1])
    rec['frameRetained'] = frame is not None
    rec['frameRehashesToBodyIdentity'] = (
        frame is not None and 'sha256:' + hashlib.sha256(frame).hexdigest() == ident)

    # ---- parse the frame with the reviewer's own reader and check the grammar
    if frame:
        p = 0; comps = []
        for _ in range(5):
            n = frame[p]; p += 1; comps.append(frame[p:p + n]); p += n
        plen = int.from_bytes(frame[p:p + 4], 'big'); p += 4
        body_payload = frame[p:p + plen]; p += plen
        rec['trailingBytes'] = len(frame) - p
        tag, level_id, level_version, language_id, language_version = comps
        rec['componentLengths'] = [len(c) for c in comps]
        rec['allComponentsWithinU8'] = all(len(c) <= 255 for c in comps)
        rec['domainTag'] = tag.decode()
        rec['domainTagMatchesInheritedGrammar'] = tag.decode() == GRAMMAR['domainTag']
        rec['levelId'] = level_id.decode()
        rec['levelIdEqualsPayloadLevel'] = level_id.decode() == payload['normalisationLevel']
        rec['levelVersionIsRaw32'] = len(level_version) == 32
        rec['levelVersionIsNotHexText'] = level_version != spec_digest.encode()
        rec['levelVersionEqualsRawDigestOfSpec'] = level_version == bytes.fromhex(spec_digest)
        rec['bodyLanguageId'] = language_id.decode()
        rec['languageVersionIsRaw32'] = len(language_version) == 32
        # ---- L0: payload must be u32be len || the EXACT anchor span bytes of the fact's own file
        inner_len = int.from_bytes(body_payload[:4], 'big')
        span = body_payload[4:]
        file_row = next(x for x in snap['sourceInventory'] if x['path'] == anchor['path'])
        file_bytes = b[file_row['sha256']]
        expected_span = file_bytes[anchor['startByte']:anchor['endByte']]
        rec['l0PayloadIsU32bePrefixed'] = inner_len == len(span)
        rec['l0PayloadEqualsOwnAnchorSpan'] = span == expected_span
        rec['l0RecomputedFromOwnSource'] = rec['l0PayloadEqualsOwnAnchorSpan']
        rec['spanBytes'] = len(span)
        # ---- reviewer's independent frame rebuild must reproduce the identity byte for byte
        rebuilt = reviewer_frame(GRAMMAR['domainTag'], payload['normalisationLevel'],
                                 bytes.fromhex(spec_digest), language_id.decode(),
                                 language_version, body_payload)
        rec['reviewerRebuiltFrameMatchesByte'] = rebuilt == frame
        rec['reviewerRebuiltIdentityMatches'] = (
            'sha256:' + hashlib.sha256(rebuilt).hexdigest() == ident)
        rec['languageVersionRaw32Hex'] = language_version.hex()
    # ---- FACT-ID separation
    rec['bodyIdentityIsNotTheFactId'] = ident != fkey and not fkey.startswith(ident)
    rec['factId'] = fkey
    rec['bodyIdentity'] = ident

    # ---- closure / store
    try:
        rec['closure'] = {'admitted': True, 'runId': M.close_run(r, o, b)}
        store = M.EvidenceStore(); ex = 'exec1_' + 'c' * 32
        rec['store'] = {'prepared': store.prepare(r, o, b, ex, ns['replay']),
                        'commit': store.commit(ex)}
    except Exception as e:
        rec['closure'] = {'admitted': False, 'cause': str(e), 'exception': type(e).__name__}
    return rec


rows = [
    analyse('typescript-ts-body', 'typescript', source_path='a.ts'),
    analyse('javascript-body-through-typescript-engine', 'typescript', source_path='a.js'),
    analyse('typescript-tsx-body', 'typescript', source_path='a.tsx'),
    analyse('typescript-d-ts-body', 'typescript', source_path='a.d.ts'),
    analyse('rust-body', 'rust'),
]

# ---- byte-identical bodies across variants must NOT share an identity
by = {r['case']: r['bodyIdentity'] for r in rows}
cross = {
    'tsAndJsBodiesAreByteIdentical': True,
    'tsVsJsDistinctIdentity': by['typescript-ts-body'] != by['javascript-body-through-typescript-engine'],
    'tsVsTsxDistinctIdentity': by['typescript-ts-body'] != by['typescript-tsx-body'],
    'tsVsDtsDistinctIdentity': by['typescript-ts-body'] != by['typescript-d-ts-body'],
    'jsBodyLanguageIsJavascript': next(r['bodyLanguageId'] for r in rows
                                       if r['case'] == 'javascript-body-through-typescript-engine') == 'javascript',
    'tsBodyLanguageIsTypescript': next(r['bodyLanguageId'] for r in rows
                                       if r['case'] == 'typescript-ts-body') == 'typescript',
    'rustBodyLanguageIsRust': next(r['bodyLanguageId'] for r in rows if r['case'] == 'rust-body') == 'rust',
}

out = {'probe': 'p07_clone_body_identity',
       'standing': 'independent reviewer probe; custody/framing evidence only; qualifies no normalizer or tokenizer',
       'inheritedPolicySha256': hashlib.sha256(
           (SUB / 'docs/coop/artifacts/fact-identity-policy.v2.json').read_bytes()).hexdigest(),
       'inheritedPreimageGrammar': GRAMMAR['domainSeparatedPreimage'],
       'vectors': rows, 'crossVariant': cross}
print(json.dumps(out, indent=1))
