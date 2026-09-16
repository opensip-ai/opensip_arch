import json, hashlib, os, collections
R = '/Users/sb/code/opensip-ai/opensip_arch/'
S = '/private/tmp/opensip-design-corrections/application-stage.v45.2/'
app = json.load(open(S + 'files/docs/coop/design-corrections/application.v1.json'))
def sha(p): return hashlib.sha256(open(R + p, 'rb').read()).hexdigest()
for k in ['codexCoauthorAssent', 'codexBlindAssessment', 'blindInputManifest', 'blindInputCustody', 'designSourceArchive', 'currentSourceMap', 'reviewedProposedAct']:
    v = app[k]; p = v['path']
    print(k, p, 'exists', os.path.exists(R + p), 'sha ok', os.path.exists(R + p) and sha(p) == v['sha256'])
km = json.load(open(R + app['blindInputManifest']['path']))
print('kit manifest keys', list(km.keys()))
ents = None
for k, v in km.items():
    if isinstance(v, list) and v and isinstance(v[0], dict) and 'sha256' in v[0]: ents = v; print('kit entries key', k, len(v))
paths = [e['path'] for e in ents]
print('kit parent', km.get('parentSubjectSha256') or km.get('parent'))
cm = json.load(open(R + 'docs/coop/design-corrections/reviews/candidate-subject.v45.json'))
snap = {e['path']: e['sha256'] for e in cm['files']}
insnap = sum(1 for e in ents if snap.get(e['path']) == e['sha256'])
print('kit entries byte-equal to snapshot', insnap, 'of', len(ents))
print('kit not equal snapshot', [e['path'] for e in ents if snap.get(e['path']) != e['sha256']])
print('kit by dir', collections.Counter(os.path.dirname(p) for p in paths).most_common(40))
print('kit python files', [p for p in paths if p.endswith('.py')])
print('kit reports/cases', [p for p in paths if 'report' in p or 'cases' in p or 'fixture' in p or 'check' in p])
B = R + 'docs/coop/design-corrections/reviews/consumer-b.v24-source45.v1/'
print('blind runtime top', sorted(os.listdir(B)))
fam = json.load(open(R + app['blindInputCustody']['path']))
print('final public artifact manifest keys', list(fam.keys()), json.dumps(fam)[:1200])
br = json.load(open(B + 'blind-review.json'))
print('blind standing', br['standing'][:2500])
print('verdictBasis', br['verdictBasis'])
print('source45Continuation executedFresh', br['source45Continuation'].get('executedFresh'))
print('reusedExactPriorMeasurements', br['source45Continuation'].get('reusedExactPriorMeasurements'))
print('claimedCompletePositives', len(br['claimedCompletePositives']))
ev = [k for k in br.keys()]
print('blind review keys', ev)
