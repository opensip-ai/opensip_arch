import json, hashlib, os, sys
S = '/private/tmp/opensip-design-corrections/application-stage.v45.2/'
R = '/Users/sb/code/opensip-ai/opensip_arch/'
C = '/tmp/opensip-design-corrections/candidate-subject.v45/'
EXPECT = '948d9bdd50169ad54871b6816d7f970a2f203fd9b1e84b7bea87dcc5c9ca6757'
def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()
out = {}
mb = open(S + 'application-subject.v45.json', 'rb').read()
out['manifestSha256'] = hashlib.sha256(mb).hexdigest()
out['manifestMatches'] = out['manifestSha256'] == EXPECT
m = json.loads(mb)
base = {'files': S + 'files/', 'beforeImages': S + 'before/', 'support': S}
bad = []
for k in base:
    for e in m[k]:
        p = base[k] + e['path']
        if not os.path.isfile(p) or os.path.getsize(p) != e['bytes'] or sha(p) != e['sha256']: bad.append((k, e['path']))
out['entries'] = sum(len(m[k]) for k in base); out['entryMismatches'] = bad
disk = set()
for r, ds, fs in os.walk(S):
    for f in fs: disk.add(os.path.relpath(os.path.join(r, f), S))
listed = {('files/' + e['path']) for e in m['files']} | {('before/' + e['path']) for e in m['beforeImages']} | {e['path'] for e in m['support']} | {'application-subject.v45.json'}
out['unlistedStageFiles'] = sorted(disk - listed)
live = []
for e in m['files']:
    fp = R + e['path']; cur = sha(fp) if os.path.isfile(fp) else None
    if cur != e['beforeSha256']: live.append((e['path'], cur))
out['liveNotEqualBefore'] = live
out['activationExists'] = os.path.exists(R + 'docs/coop/design-corrections/application-activation.v1.json')
out['retainedManifestEqualsStage'] = open(R + m['retainedManifestPath'], 'rb').read() == mb
for k in ['designSubject', 'independentDesignReview', 'freshBlindConsumerReview']:
    out[k + 'Matches'] = sha(R + m[k]['path']) == m[k]['sha256']
if '--snapshot' in sys.argv:
    cm = json.load(open(R + 'docs/coop/design-corrections/reviews/candidate-subject.v45.json'))
    sb = [e['path'] for e in cm['files'] if not os.path.isfile(C + e['path']) or sha(C + e['path']) != e['sha256']]
    n = sum(len(fs) for _, _, fs in os.walk(C))
    out['snapshotEntries'] = len(cm['files']); out['snapshotMismatches'] = sb; out['snapshotDiskFiles'] = n
print(json.dumps(out, indent=1))
