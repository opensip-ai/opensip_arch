import json, hashlib, os
S = '/private/tmp/opensip-design-corrections/application-stage.v45.2/'
C = '/tmp/opensip-design-corrections/candidate-subject.v45/'
m = json.load(open(S + 'application-subject.v45.json'))
staged = {e['path']: e['sha256'] for e in m['files']}
cm = json.load(open('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v45.json'))
snap = {e['path']: e['sha256'] for e in cm['files']}
post = dict(snap); post.update(staged)
def entries(doc):
    for k in ('pins', 'files', 'entries', 'sources'):
        if isinstance(doc.get(k), list): return k, doc[k]
    return None, []
delta = json.load(open(S + 'support/native-recording-delta.v1.json'))
led = ['docs/coop/design-corrections/foundation/source-pins.v1.json', 'docs/coop/design-corrections/security/source-pins.v1.json', 'docs/coop/design-corrections/native/source-pins.v2.json', 'docs/coop/design-corrections/workflows/source-pins.v1.json', 'docs/coop/design-corrections/foundation/evaluator3-source-pins.v1.json']
for L in led:
    sd = json.load(open(S + 'files/' + L)); cd = json.load(open(C + L))
    k, se = entries(sd); _, ce = entries(cd)
    pk = 'path' if 'path' in se[0] else list(se[0].keys())
    changed = [(x['path'], y['sha256'], x['sha256']) for x, y in zip(se, ce) if x != y]
    mism_post = [x['path'] for x in se if post.get(x['path']) != x['sha256']]
    mism_snap_orig = [y['path'] for y in ce if snap.get(y['path']) != y['sha256']]
    print(L, 'key', k, 'entries', len(se), len(ce), 'changed', len(changed), 'staged-ledger mismatches vs post-application tree', len(mism_post), mism_post[:5], 'original-ledger mismatches vs snapshot', len(mism_snap_orig))
    dl = [d for d in delta['pinManifests'] if d['path'] == L][0]
    exp = sorted((e['path'], e['beforeSha256'], e['afterSha256']) for e in dl['entries'])
    print('   delta matches recorded:', sorted(changed) == exp, 'ledger before/after', snap[L] == dl['beforeSha256'], staged[L] == dl['afterSha256'])
    print('   other keys equal:', {kk: sd[kk] == cd[kk] for kk in sd if kk != k})
for sc in delta['sourceChanges']:
    print(sc['path'], 'snap==before', snap[sc['path']] == sc['beforeSha256'], 'staged==after', staged[sc['path']] == sc['afterSha256'])
    a = open(C + sc['path']).read(); b = open(S + 'files/' + sc['path']).read()
    print('   staged == snapshot with only added paragraph:', b.replace(sc['addedOpeningParagraph'], '', 1) == a)
print('native report staged==snapshot', staged.get('docs/coop/design-corrections/native/native-evidence-report.v2.json') == snap.get('docs/coop/design-corrections/native/native-evidence-report.v2.json'), delta['report']['afterSha256'] == staged.get('docs/coop/design-corrections/native/native-evidence-report.v2.json'))
# the other 16 doc changes vs snapshot: are they pinned by any ledger?
pinned = set()
for L in led:
    sd = json.load(open(S + 'files/' + L)); k, se = entries(sd)
    pinned |= {x['path'] for x in se}
d = json.load(open('/private/tmp/opensip-design-corrections/application-review.v45/probes/p03_out.json'))
print('diff-from-snapshot files pinned by any ledger:', [p for p in d['diff'] if p in pinned])
print('absent-from-snapshot files pinned by any ledger:', [p for p in d['absent'] if p in pinned])
