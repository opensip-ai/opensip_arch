"""Final reverification after review files are written: full subject, live before-state, activation absence, snapshot sample-free full hash, prerequisites, review shape; records result into review.json#/finalReverification."""
import json, hashlib, os
RT = '/private/tmp/opensip-design-corrections/application-review.v46/'
PK = '/private/tmp/opensip-design-corrections/application-stage.v46/'
R = '/Users/sb/code/opensip-ai/opensip_arch/'
SNAP = '/tmp/opensip-design-corrections/candidate-subject.v45/'
MS = 'dab6e00fc3ccf82f015941bc767a10b18be9e6ca5f1c8598fa1fe9a4d05743f7'
def h(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
res = {}
res['manifestSha256'] = h(PK + 'application-subject.v46.json'); res['manifestMatches'] = res['manifestSha256'] == MS
m = json.load(open(PK + 'application-subject.v46.json'))
bad = []
for k, base in [('files', PK + 'files/'), ('beforeImages', PK + 'before/'), ('support', PK)]:
    for e in m[k]:
        p = base + e['path']
        if not os.path.isfile(p) or os.path.getsize(p) != e['bytes'] or h(p) != e['sha256']: bad.append((k, e['path']))
res['entriesChecked'] = sum(len(m[k]) for k in ('files', 'beforeImages', 'support')); res['entryMismatches'] = bad
listed = {'files/' + e['path'] for e in m['files']} | {'before/' + e['path'] for e in m['beforeImages']} | {e['path'] for e in m['support']} | {'application-subject.v46.json'}
disk = {os.path.relpath(os.path.join(r, f), PK) for r, d, fs in os.walk(PK) for f in fs}
res['unlisted'] = sorted(disk - listed); res['missing'] = sorted(listed - disk)
live_bad = []
for e in m['files']:
    p = R + e['path']
    if e['beforeSha256'] is None:
        if os.path.exists(p): live_bad.append((e['path'], 'new path exists'))
    elif not os.path.isfile(p) or h(p) != e['beforeSha256']: live_bad.append((e['path'], 'live differs from before-image'))
res['liveBeforeStateViolations'] = live_bad
res['activationAbsent'] = not os.path.exists(R + 'docs/coop/design-corrections/application-activation.v1.json')
sm = json.load(open(R + 'docs/coop/design-corrections/reviews/candidate-subject.v45.json'))
res['snapshotEntries'] = len(sm['files']); res['snapshotMismatches'] = sum(1 for e in sm['files'] if h(SNAP + e['path']) != e['sha256'])
pre = {'docs/coop/design-corrections/reviews/candidate-subject.v45.json': '8b4efbb04d9e25126ec7955931cf364f7013b3710a45c48bae8bc563a0c82155',
       'docs/coop/design-corrections/reviews/claude-independent-design.v45/review.json': '427ae73e715799a5a1375d231d8d5e1022c7eb11c95555b4cf9fd93f79af1f6c',
       'docs/coop/design-corrections/reviews/consumer-b.v24-source45.v1/blind-review.json': '7ee66bb559488109a51d2c64eca8e48c93db7b830a071947e1eaf695c79ac2f1',
       'docs/coop/design-corrections/reviews/codex-post-reset.v1/design-assent.v45.json': '36830f6e4fac4d21e78949ee578930b2e1e95fc87c1289cf67690dee7bb10eef',
       'docs/coop/design-corrections/reviews/application-review.v45/review.json': '6ff6e1858dd3b606a638b7c780ac2b9c4dce146799786849653831ea8040812f',
       'docs/coop/design-corrections/reviews/application-subject.v46.json': MS}
res['prerequisiteHashesMatch'] = {k: h(R + k) == v for k, v in pre.items()}
rv = json.load(open(RT + 'review.json'))
res['reviewShape'] = {'verdict': rv.get('verdict'), 'subjectManifestSha256Matches': rv.get('subjectManifestSha256') == MS,
                      'newMustIssuesEmptyList': isinstance(rv.get('newMustIssues'), list) and not rv['newMustIssues'],
                      'newShouldIssuesEmptyList': isinstance(rv.get('newShouldIssues'), list) and not rv['newShouldIssues']}
res['reviewMdPresent'] = os.path.isfile(RT + 'review.md')
res['passed'] = res['manifestMatches'] and not bad and not res['unlisted'] and not res['missing'] and not live_bad and res['activationAbsent'] and res['snapshotMismatches'] == 0 and all(res['prerequisiteHashesMatch'].values()) and all(v for k, v in res['reviewShape'].items() if k != 'verdict')
rv['finalReverification'] = {**res, 'note': 'Executed after review.md and review.json were written; this field is the only post-check addition to review.json.'}
json.dump(rv, open(RT + 'review.json', 'w'), indent=1, ensure_ascii=False)
print(json.dumps(res, indent=1))
