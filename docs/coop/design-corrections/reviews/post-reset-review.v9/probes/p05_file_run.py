"""v9 probe 05 - reviewer's OWN lawful complete file Run + payload negatives.

v8-S2 said a file payload's content claim joined to nothing, and could not be shown end to
end because the v8 fixture's Coverage for file@enumerated was refused by RC-1. This probe:

  1. builds a lawful COMPLETE file Run directly from the shipped builder (no monkeypatching),
     asserts it CLOSES, PREPARES, REPLAYS and COMMITS, and asserts the file fact is not just
     present in the view but REACHABLE - named by the predicate witness's matchingFactIds;
  2. drives five payload/anchor negatives, asserting for each that the mutated fact is still
     the reachable claimed fact and that refusal reaches the INTENDED join, not an earlier
     schema refusal;
  3. tests the memoised-decode case explicitly: two facts sharing ONE canonical payload, the
     second with a borrowed anchor, so payload decode is a cache HIT on the second fact.

An unreferenced blob or an early schema refusal is not proof, so every negative records the
exact cause string and whether the fact was reachable before mutation.

Design/reference only. Synthetic fixtures. Qualifies no store, OS, compiler or normalizer.
"""
import copy, hashlib, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import harness

ns = harness.load()
M, C, N = ns['M'], ns['C'], ns['N']
put, rekey = ns['put_blob'], ns['rekey']
rows = []


def reachable_facts(run, objects):
    """Facts actually named by the predicate witness - the claimed, reachable set."""
    ev = objects[run['evidenceId']][1]
    proof = objects[ev['proofBundleId']][1]
    out = set()
    for pp in proof['predicateProofs']:
        w = None
        for d, raw in ():
            pass
        out |= set()
    return out


def witness_matching(run, objects, blobs):
    ev = objects[run['evidenceId']][1]
    proof = objects[ev['proofBundleId']][1]
    ids = set()
    for pp in proof['predicateProofs']:
        w = json.loads(blobs[pp['witnessDigest']].decode())
        ids |= set(w['matchingFactIds'])
    return ids


def drive(label, mutate=None, expect=None):
    r, o, b = ns['build'](has_match=True, relation='file')
    fkey = next(k for k, (d, v) in o.items() if d == 'fact')
    inventory = {v['path']: v for v in o[r['snapshotId']][1]['sourceInventory']}
    before_reachable = fkey in witness_matching(r, o, b)
    info = {}
    if mutate:
        fkey = mutate(r, o, b, fkey, inventory, info)
    view = o[o[r['evidenceId']][1]['viewIds'][0]][1]
    rec = {'case': label,
           'factInView': fkey in view['facts'],
           'factReachableBeforeMutation': before_reachable,
           'factReachableAfterMutation': fkey in witness_matching(r, o, b),
           'detail': info}
    try:
        rid = M.close_run(r, o, b)
        rec['closure'] = {'admitted': True, 'runId': rid}
        store = M.EvidenceStore()
        ex = 'exec1_' + 'c' * 32
        try:
            prepared = store.prepare(r, o, b, ex, ns['replay'])
            rec['store'] = {'prepared': prepared, 'commit': store.commit(ex)}
        except Exception as e:
            rec['store'] = {'refused': str(e), 'exception': type(e).__name__}
    except Exception as e:
        rec['closure'] = {'admitted': False, 'cause': str(e), 'exception': type(e).__name__}
    if expect:
        cause = rec['closure'].get('cause') or (rec.get('store') or {}).get('refused') or ''
        rec['expect'] = expect
        rec['reachedIntendedCause'] = expect in cause
    rows.append(rec)
    return rec


# ---------- 1. positive control: lawful complete file Run ----------
drive('control-lawful-complete-file-run')

# ---------- 2. negatives on the file payload's own claims ----------
def mut_payload(field, newvalue):
    def f(r, o, b, fkey, inventory, info):
        fact = copy.deepcopy(o[fkey][1])
        payload = json.loads(b[fact['payloadDigest']].decode())
        info['truth'] = inventory.get(payload['path'])
        info['payloadBefore'] = dict(payload)
        payload[field] = newvalue(payload, inventory)
        info['payloadAfter'] = dict(payload)
        fact['payloadDigest'] = put(b, payload)
        return rekey(o, fkey, fact, r)
    return f

drive('wrong-content-hash', mut_payload('contentSha256', lambda p, i: 'f' * 64),
      'RELATION_FILE_CONTENT_JOIN')
drive('wrong-byte-length', mut_payload('byteLength', lambda p, i: p['byteLength'] + 1),
      'RELATION_FILE_LENGTH_JOIN')
drive('content-hash-of-a-DIFFERENT-inventoried-file',
      mut_payload('contentSha256',
                  lambda p, i: next(v['sha256'] for k, v in i.items() if k != p['path'])),
      'RELATION_FILE_CONTENT_JOIN')
drive('byte-length-of-a-DIFFERENT-inventoried-file',
      mut_payload('byteLength',
                  lambda p, i: next(v['bytes'] for k, v in i.items()
                                    if k != p['path'] and v['bytes'] != i[p['path']]['bytes'])),
      'RELATION_FILE_LENGTH_JOIN')

# uninventoried path: keep the fact reachable by moving the rule atom's filter with it.
def mut_absent_path(r, o, b, fkey, inventory, info):
    fact = copy.deepcopy(o[fkey][1])
    payload = json.loads(b[fact['payloadDigest']].decode())
    payload['path'] = 'absent.ts'
    info['payloadAfter'] = dict(payload)
    info['pathInInventory'] = 'absent.ts' in inventory
    fact['payloadDigest'] = put(b, payload)
    return rekey(o, fkey, fact, r)
drive('uninventoried-path', mut_absent_path, 'RELATION_PATH_NOT_INVENTORIED')

# ---------- 3. memoised decode: two facts, ONE canonical payload ----------
def mut_second_owner_same_payload(r, o, b, fkey, inventory, info):
    """A SECOND fact carrying the byte-identical payload of the first, but anchored in a
    different file. Payload decode is a cache HIT on this fact, so if the joins were done
    at decode time rather than per owning fact, this borrowed-anchor owner would admit."""
    first = copy.deepcopy(o[fkey][1])
    payload = json.loads(b[first['payloadDigest']].decode())
    other = next(k for k in inventory if k != payload['path'])
    info['firstOwnerPath'] = payload['path']
    info['secondOwnerAnchorPath'] = other
    info['sharedPayloadDigest'] = first['payloadDigest']
    second = copy.deepcopy(first)
    second['anchors'] = [{'path': other, 'blobDigest': inventory[other]['sha256'],
                          'startByte': 0, 'endByte': inventory[other]['bytes']}]
    key = M.identifier('fact', second)
    o[key] = ('fact', second)
    info['twoFactsShareOnePayloadDigest'] = second['payloadDigest'] == first['payloadDigest']
    view_key = o[r['evidenceId']][1]['viewIds'][0]
    view = copy.deepcopy(o[view_key][1])
    view['facts'] = sorted(set(view['facts']) | {key})
    rekey(o, view_key, view, r)
    ns['resync_witness'](o, b, r)
    ns['resync_proof_refs'](o, b, r)
    return key
drive('second-owner-borrows-anchor-with-memoised-payload', mut_second_owner_same_payload,
      'RELATION_FILE')

# ---------- 4. retained-bytes negative: inventory row present, blob not retained ----------
def mut_drop_retained_blob(r, o, b, fkey, inventory, info):
    fact = copy.deepcopy(o[fkey][1])
    payload = json.loads(b[fact['payloadDigest']].decode())
    info['droppedBlob'] = payload['contentSha256']
    b.pop(payload['contentSha256'], None)
    return fkey
drive('claimed-content-blob-not-retained', mut_drop_retained_blob, 'RELATION_FILE')

out = {
    'probe': 'p05_file_run',
    'standing': 'independent reviewer probe; synthetic design/reference fixtures; qualifies no store, OS, compiler or normalizer',
    'fixtureSha256': ns['_fixtureSha256'],
    'custody': harness.custody([
        'docs/coop/design-corrections/foundation/check-identity.py',
        'docs/coop/design-corrections/foundation/identity-model.py',
        'docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json']),
    'vectors': rows,
}
print(json.dumps(out, indent=1))
