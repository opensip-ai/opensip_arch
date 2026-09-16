"""S00 — copy the COMPLETE v1 reports into this runtime, then verify the two claimed leftovers
against the exact v31/v32 manifest rows. No suites, no source reads, no archive scan."""
import hashlib, json, os, shutil

V1 = '/tmp/opensip-design-corrections/claude-independent32-reconciliation.v1'
V2 = '/tmp/opensip-design-corrections/claude-independent32-reconciliation.v2'
REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews'
M31, M32 = os.path.join(REV, 'candidate-subject.v31.json'), os.path.join(REV, 'candidate-subject.v32.json')
OUT = os.path.join(V2, 'receipts')
os.makedirs(OUT, exist_ok=True)


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


R = {}
for n in ('review.json', 'review.md'):
    shutil.copy2(os.path.join(V1, n), os.path.join(V2, n))
R['inputV1ReviewJsonSha256'] = sha(os.path.join(V1, 'review.json'))
R['inputV1ReviewMdSha256'] = sha(os.path.join(V1, 'review.md'))
R['copiedByteIdentical'] = (sha(os.path.join(V2, 'review.json')) == R['inputV1ReviewJsonSha256']
                            and sha(os.path.join(V2, 'review.md')) == R['inputV1ReviewMdSha256'])
print('copied v1 -> v2 byte-identical:', R['copiedByteIdentical'])
print('input v1 review.json sha:', R['inputV1ReviewJsonSha256'])
print('input v1 review.md   sha:', R['inputV1ReviewMdSha256'])

R['manifest32Sha256'] = sha(M32)
R['manifest32MatchesRequired'] = (
    R['manifest32Sha256'] == '3897e8d1bb389f3d39669997d3078d5a44fa024f29d97bd17854a48916610bf2')
R['manifest31Sha256'] = sha(M31)
print('manifest32 sha matches required:', R['manifest32MatchesRequired'])

m31 = {f['path']: f['sha256'] for f in json.load(open(M31))['files']}
m32 = {f['path']: f['sha256'] for f in json.load(open(M32))['files']}
R['manifestRowCounts'] = {'v31': len(m31), 'v32': len(m32)}

# ---- leftover 1: the three DR-007 owners ----
DR7 = ['docs/v2/contracts/product-v1/workflows-and-surfaces.md',
       'docs/v2/contracts/product-v1/native-evidence.md',
       'docs/coop/design-corrections/foundation/evaluator-fault-contract.v3.md']
rows = {}
for p in DR7:
    rows[p] = {'inV31': p in m31, 'inV32': p in m32,
               'sha31': m31.get(p), 'sha32': m32.get(p),
               'changed31to32': m31.get(p) != m32.get(p)}
R['dr007OwnerRows'] = rows
print('\n--- DR-007 owners, compared on the two manifest rows ---')
for p, v in rows.items():
    print('   %-62s changed31->32=%s' % (p[-62:], v['changed31to32']))
    print('       31: %s' % v['sha31'])
    print('       32: %s' % v['sha32'])
R['dr007Changed'] = sorted(p for p, v in rows.items() if v['changed31to32'])
R['dr007Unchanged'] = sorted(p for p, v in rows.items() if not v['changed31to32'])
print('   -> changed  :', R['dr007Changed'])
print('   -> unchanged:', R['dr007Unchanged'])

V = json.load(open(os.path.join(V2, 'review.json')))
cur = V['inheritedResidualDispositions']['DR-007']
R['dr007AsRecordedInV1'] = {'changed': cur['ownerFilesChangedIn31to32'],
                            'unchanged': cur['ownerFilesUnchangedIn31to32'],
                            'readingStanding': cur['readingStanding']}
R['leftover1Substantiated'] = (cur['ownerFilesChangedIn31to32'] == []
                               and set(R['dr007Changed']) and
                               set(R['dr007Changed']) <= set(cur['ownerFilesUnchangedIn31to32']))
print('\nv1 recorded changed=%s' % cur['ownerFilesChangedIn31to32'])
print('v1 recorded unchanged includes the two changed chapters:',
      set(R['dr007Changed']) <= set(cur['ownerFilesUnchangedIn31to32']))
print('leftover 1 substantiated:', R['leftover1Substantiated'])

# ---- leftover 2 ----
res = V['evaluationResidualDispositions']['RES-EP13-13']
R['res13StatusTail'] = res['currentStatusOn32'][-220:]
R['leftover2Substantiated'] = 'which I reviewed then' in res['currentStatusOn32']
print('\nRES-EP13-13 currentStatusOn32 tail:', R['res13StatusTail'][-180:])
print('leftover 2 substantiated:', R['leftover2Substantiated'])

json.dump(R, open(os.path.join(OUT, 's00-copy-verify.json'), 'w'), indent=1)
print('\nwrote s00-copy-verify.json')
