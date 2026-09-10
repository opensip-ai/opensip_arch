"""v9 probe 06 - stricter file-Run negatives, corrected expectations, RC-1 preservation.

Corrects two reviewer harness assumptions from p05 (NOT product defects):
  (a) the borrowed-anchor second owner refuses at RELATION_ANCHOR_FOREIGN_PATH, which IS the
      anchorPathField join; p05 expected a 'RELATION_FILE*' token.
  (b) dropping the retained blob refuses earlier at EVIDENCE_UNAVAILABLE, which is correct
      (required evidence is missing before any relation join runs); p05 expected a relation token.

Strengthens p05: every payload negative now RESYNCS the witness and proof refs after mutation,
so the mutated fact is the reachable claimed fact BOTH before and after, and the refusal cannot
be an artifact of a stale witness reference.

Adds: RC-1 preservation evidence, a lawful SECOND owner positive control (so the anchor rule is
not merely refusing all second owners), and reverse-order construction.
"""
import copy, hashlib, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import harness

ns = harness.load()
M, C, N = ns['M'], ns['C'], ns['N']
put, rekey = ns['put_blob'], ns['rekey']
rows = []


def witness_matching(run, objects, blobs):
    ev = objects[run['evidenceId']][1]
    proof = objects[ev['proofBundleId']][1]
    ids = set()
    for pp in proof['predicateProofs']:
        ids |= set(json.loads(blobs[pp['witnessDigest']].decode())['matchingFactIds'])
    return ids


def drive(label, mutate, expect, resync=True):
    r, o, b = ns['build'](has_match=True, relation='file')
    fkey = next(k for k, (d, v) in o.items() if d == 'fact')
    inventory = {v['path']: v for v in o[r['snapshotId']][1]['sourceInventory']}
    before = fkey in witness_matching(r, o, b)
    info = {}
    fkey = mutate(r, o, b, fkey, inventory, info) if mutate else fkey
    if resync:
        # re-point the witness/proof at the mutated fact so it is the CLAIMED reachable fact
        view = o[o[r['evidenceId']][1]['viewIds'][0]][1]
        ns['resync_witness'](o, b, r)
        ns['resync_proof_refs'](o, b, r)
    after = fkey in witness_matching(r, o, b)
    view = o[o[r['evidenceId']][1]['viewIds'][0]][1]
    rec = {'case': label, 'detail': info,
           'factInView': fkey in view['facts'],
           'reachableBefore': before, 'reachableAfter': after}
    try:
        rid = M.close_run(r, o, b)
        rec['closure'] = {'admitted': True, 'runId': rid}
        store = M.EvidenceStore(); ex = 'exec1_' + 'c' * 32
        try:
            rec['store'] = {'prepared': store.prepare(r, o, b, ex, ns['replay']),
                            'commit': store.commit(ex)}
        except Exception as e:
            rec['store'] = {'refused': str(e), 'exception': type(e).__name__}
    except Exception as e:
        rec['closure'] = {'admitted': False, 'cause': str(e), 'exception': type(e).__name__}
    cause = rec['closure'].get('cause') or (rec.get('store') or {}).get('refused') or ''
    rec['expect'] = expect
    rec['reachedIntendedCause'] = (expect is None) if expect is None else (expect in cause)
    rows.append(rec)
    return rec


def mut_payload(field, newvalue):
    def f(r, o, b, fkey, inventory, info):
        fact = copy.deepcopy(o[fkey][1])
        payload = json.loads(b[fact['payloadDigest']].decode())
        info['inventoryTruth'] = inventory.get(payload['path'])
        info['before'] = dict(payload)
        payload[field] = newvalue(payload, inventory)
        info['after'] = dict(payload)
        fact['payloadDigest'] = put(b, payload)
        return rekey(o, fkey, fact, r)
    return f


# --- positive control
drive('control-lawful-complete-file-run', None, None)

# --- payload claim negatives, now with the mutated fact reachable after mutation
drive('wrong-content-hash', mut_payload('contentSha256', lambda p, i: 'f' * 64),
      'RELATION_FILE_CONTENT_JOIN')
drive('wrong-byte-length', mut_payload('byteLength', lambda p, i: p['byteLength'] + 1),
      'RELATION_FILE_LENGTH_JOIN')
drive('content-hash-of-another-inventoried-file',
      mut_payload('contentSha256', lambda p, i: next(v['sha256'] for k, v in i.items() if k != p['path'])),
      'RELATION_FILE_CONTENT_JOIN')
drive('byte-length-of-another-inventoried-file',
      mut_payload('byteLength', lambda p, i: next(
          v['bytes'] for k, v in i.items() if k != p['path'] and v['bytes'] != i[p['path']]['bytes'])),
      'RELATION_FILE_LENGTH_JOIN')
drive('uninventoried-path', mut_payload('path', lambda p, i: 'absent.ts'),
      'RELATION_PATH_NOT_INVENTORIED')

# --- corrected expectations
def mut_second_owner(lawful):
    def f(r, o, b, fkey, inventory, info):
        first = copy.deepcopy(o[fkey][1])
        payload = json.loads(b[first['payloadDigest']].decode())
        claimed = payload['path']
        if lawful:
            # a second fact in the SAME file: a legitimate second owner of one payload
            anchor_path = claimed
        else:
            anchor_path = next(k for k in inventory if k != claimed)
        second = copy.deepcopy(first)
        second['anchors'] = [{'path': anchor_path, 'blobDigest': inventory[anchor_path]['sha256'],
                              'startByte': 0, 'endByte': max(0, inventory[anchor_path]['bytes'] - 1)}]
        second['confidenceMillionths'] = 999999  # make it a distinct fact
        key = M.identifier('fact', second)
        o[key] = ('fact', second)
        info['claimedPath'] = claimed
        info['secondOwnerAnchorPath'] = anchor_path
        info['payloadDigestShared'] = second['payloadDigest'] == first['payloadDigest']
        info['payloadDecodeIsCacheHitOnSecondFact'] = info['payloadDigestShared']
        vk = o[r['evidenceId']][1]['viewIds'][0]
        view = copy.deepcopy(o[vk][1]); view['facts'] = sorted(set(view['facts']) | {key})
        rekey(o, vk, view, r)
        return key
    return f

drive('second-owner-borrows-foreign-anchor-memoised-payload', mut_second_owner(False),
      'RELATION_ANCHOR_FOREIGN_PATH')
drive('POSITIVE-second-owner-same-file-memoised-payload', mut_second_owner(True), None)

def mut_drop_blob(r, o, b, fkey, inventory, info):
    payload = json.loads(b[o[fkey][1]['payloadDigest']].decode())
    info['droppedContentBlob'] = payload['contentSha256']
    b.pop(payload['contentSha256'], None)
    return fkey
drive('claimed-content-blob-not-retained', mut_drop_blob, 'EVIDENCE_UNAVAILABLE')

# --- RC-1 preservation: no rung invented, no completeness claim asserted for file@enumerated
r, o, b = ns['build'](has_match=True, relation='file')
skey = next(k for k, (d, v) in o.items() if d == 'subject-scope')
sc = o[skey][1]
ckey = next(k for k, (d, v) in o.items() if d == 'coverage')
cov_payload = json.loads(b[o[ckey][1]['payloadDigest']].decode())
rc1 = {
    'scopeRelation': sc['relation'], 'scopeResolution': sc['resolution'],
    'enumeratedIsAResolvedRung': 'enumerated' in getattr(N, 'RESOLVED_RUNGS', []),
    'resolvedRungs': sorted(getattr(N, 'RESOLVED_RUNGS', [])),
    'resolutionCompleteness': cov_payload['entry']['resolutionCompleteness'],
    'examinedPartitionCoverage': cov_payload['entry']['coverage'],
    'deficiency': cov_payload['entry']['deficiency'],
}

out = {'probe': 'p06_file_run_strict',
       'standing': 'independent reviewer probe; synthetic design/reference fixtures; qualifies no store, OS or compiler',
       'fixtureSha256': ns['_fixtureSha256'],
       'harnessCorrections': [
           'p05 expected a RELATION_FILE* token for the borrowed-anchor owner; the intended join is RELATION_ANCHOR_FOREIGN_PATH (anchorPathField). Reviewer error.',
           'p05 expected a RELATION_FILE* token for the dropped retained blob; EVIDENCE_UNAVAILABLE is correct and earlier. Reviewer error.'],
       'rc1Preservation': rc1,
       'vectors': rows}
print(json.dumps(out, indent=1))
