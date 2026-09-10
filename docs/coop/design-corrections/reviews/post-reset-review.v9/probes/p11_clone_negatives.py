"""v9 probe 11 - Coverage boundary (corrected), a complete '#' marker-path Run, clone negatives.

Corrects one reviewer harness error from p10 (NOT a product defect): the "healthy universe,
honest empty view" case owned 'src/other.rs', which is not in the fixture snapshot inventory, so
it refused at NATIVE_NESTED_PATH_NOT_INVENTORIED before the Coverage question was ever reached.
It is repeated here owning an INVENTORIED path that is simply not the anchor.

Then: a complete clone Run whose owning unit marker path contains '#', and a set of clone
negatives - wrong framing, wrong level version, missing retained inputs, foreign language and
foreign anchor - each asserted to reach its own intended cause.
"""
import copy, hashlib, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import harness

ns = harness.load()
M, C, N = ns['M'], ns['C'], ns['N']
UID, unit = ns['UID'], ns['unit']
put, rekey = ns['put_blob'], ns['rekey']
out = {'probe': 'p11_clone_negatives',
       'standing': 'independent reviewer probe; synthetic fixtures; qualifies no normalizer or store',
       'harnessCorrection': "p10's healthy-empty-view case owned an UNINVENTORIED path and refused "
                            "earlier at NATIVE_NESTED_PATH_NOT_INVENTORIED. Reviewer error, not a product defect."}

def run_case(label, **kw):
    try:
        r, o, b = ns['build'](relation='clones', universe_language='rust', **kw)
    except Exception as e:
        return {'case': label, 'outcome': 'build-refused', 'cause': str(e)}
    ckey = next(k for k, (d, v) in o.items() if d == 'coverage')
    cov = json.loads(b[o[ckey][1]['payloadDigest']].decode())
    view = o[o[r['evidenceId']][1]['viewIds'][0]][1]
    rec = {'case': label, 'coverageClaim': cov['entry']['coverage'],
           'deficiency': cov['entry']['deficiency'], 'factCount': len(view['facts']),
           'sealVerdict': o[r['evaluationSealId']][1]['verdict']}
    try:
        rec['closure'] = {'admitted': True, 'runId': M.close_run(r, o, b)}
        store = M.EvidenceStore(); ex = 'exec1_' + 'c' * 32
        rec['store'] = {'prepared': store.prepare(r, o, b, ex, ns['replay']), 'commit': store.commit(ex)}
    except Exception as e:
        rec['closure'] = {'admitted': False, 'cause': str(e), 'exception': type(e).__name__}
    return rec

# ---- A. per-body refusal inside a HEALTHY universe is compatible with complete Coverage ----
inventoried_other = 'crates/c#interop/src/lib.rs'
unowned_ws = {'edition': {'fixture-root': 2021, 'interop': 2021}, 'enumeration': 'complete',
              'units': [unit('crates/c#interop/Cargo.toml', 'lib', 'interop', 'interop')],
              'selectedUnitIds': [UID('crates/c#interop/Cargo.toml', 'lib', 'interop')],
              'ownership': [{'path': inventoried_other,
                             'unitId': UID('crates/c#interop/Cargo.toml', 'lib', 'interop')}]}
out['healthyUniverseHonestEmptyView'] = run_case(
    'POSITIVE-healthy-universe-anchor-unowned-empty-view-claims-complete',
    has_match=False, workspace=unowned_ws, resolved=True)

# ---- B. a COMPLETE Run whose owning unit marker path contains '#' ----
hash_ws = {'edition': {'interop': 2021}, 'enumeration': 'complete',
           'units': [unit('crates/c#interop/Cargo.toml', 'lib', 'interop', 'interop')],
           'selectedUnitIds': [UID('crates/c#interop/Cargo.toml', 'lib', 'interop')],
           'ownership': [{'path': inventoried_other,
                          'unitId': UID('crates/c#interop/Cargo.toml', 'lib', 'interop')}]}
r = run_case('POSITIVE-complete-run-with-hash-marker-path', has_match=True,
             source_path=inventoried_other, workspace=hash_ws)
r['markerPathContainsHash'] = True
r['unitId'] = UID('crates/c#interop/Cargo.toml', 'lib', 'interop')
out['hashMarkerPathCompleteRun'] = r

# ---- C. clone negatives, each asserted against its own intended cause ----
def clone_negative(label, mutate, expect):
    r, o, b = ns['build'](has_match=True, relation='clones', universe_language='rust')
    fkey = next(k for k, (d, v) in o.items() if d == 'fact')
    info = {}
    fkey = mutate(r, o, b, fkey, info) or fkey
    ns['resync_witness'](o, b, r); ns['resync_proof_refs'](o, b, r)
    try:
        M.close_run(r, o, b)
        rec = {'case': label, 'outcome': 'ADMITTED', 'detail': info}
    except Exception as e:
        rec = {'case': label, 'outcome': 'refused', 'cause': str(e),
               'exception': type(e).__name__, 'detail': info}
    rec['expect'] = expect
    rec['reachedIntendedCause'] = expect in rec.get('cause', '')
    return rec

def repayload(fn):
    def m(r, o, b, fkey, info):
        fact = copy.deepcopy(o[fkey][1])
        payload = json.loads(b[fact['payloadDigest']].decode())
        info['before'] = dict(payload)
        fn(payload, b, o, r, fact, info)
        info['after'] = dict(payload)
        fact['payloadDigest'] = put(b, payload)
        return rekey(o, fkey, fact, r)
    return m

def unframed(payload, b, o, r, fact, info):
    """Unframed concatenation is explicitly FORBIDDEN by the inherited grammar."""
    frame = b[payload['bodyIdentity'].split(':', 1)[1]]
    p = 0; comps = []
    for _ in range(5):
        n = frame[p]; p += 1; comps.append(frame[p:p + n]); p += n
    plen = int.from_bytes(frame[p:p + 4], 'big'); p += 4
    body = frame[p:p + plen]
    bad = b''.join(comps) + body            # no length prefixes at all
    payload['bodyIdentity'] = 'sha256:' + put(b, bad)
    info['forbiddenForm'] = 'unframed concatenation'

def wrong_level_version(payload, b, o, r, fact, info):
    payload['normalisationVersion'] = 'a' * 64
    info['note'] = 'names a level specification that is not retained'

def wrong_level_id(payload, b, o, r, fact, info):
    payload['normalisationLevel'] = 'L1-lexical'
    info['note'] = 'frame levelId says L0-verbatim'

def foreign_body_identity(payload, b, o, r, fact, info):
    payload['bodyIdentity'] = 'sha256:' + 'd' * 64
    info['note'] = 'names no retained frame'

out['cloneNegatives'] = [
    clone_negative('unframed-concatenation-forbidden-by-inherited-grammar',
                   repayload(unframed), 'BODY'),
    clone_negative('level-version-names-unretained-specification',
                   repayload(wrong_level_version), 'BODY'),
    clone_negative('level-id-disagrees-with-the-frame', repayload(wrong_level_id), 'BODY'),
    clone_negative('body-identity-names-no-retained-frame',
                   repayload(foreign_body_identity), 'BODY'),
]

# anchor moved out of the body the identity was minted over
def move_anchor(r, o, b, fkey, info):
    fact = copy.deepcopy(o[fkey][1])
    a = dict(fact['anchors'][0]); a['endByte'] = max(0, a['endByte'] - 1)
    fact['anchors'] = [a]
    info['note'] = 'L0 payload no longer equals the anchor span'
    return rekey(o, fkey, fact, r)
out['cloneNegatives'].append(clone_negative('anchor-span-no-longer-matches-l0-payload',
                                            move_anchor, 'BODY'))

def two_anchors(r, o, b, fkey, info):
    fact = copy.deepcopy(o[fkey][1])
    fact['anchors'] = fact['anchors'] + [dict(fact['anchors'][0], startByte=0, endByte=1)]
    info['note'] = 'anchorCardinality for clones is exactly 1'
    return rekey(o, fkey, fact, r)
out['cloneNegatives'].append(clone_negative('clones-fact-with-two-anchors', two_anchors, 'ANCHOR'))

print(json.dumps(out, indent=1, default=str))
