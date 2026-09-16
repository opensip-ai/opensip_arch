"""P14 — bind the 30 residual rows to frozen32 and re-decide the TCB dependent set."""
import hashlib, json, os

SRC = '/tmp/opensip-design-corrections/candidate-subject.v32'
PKG = '/tmp/opensip-design-corrections/claude-author-package-successor.v8'
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v32/receipts'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v32.json'
man = {f['path']: f for f in json.load(open(MAN))['files']}
delta = json.load(open(os.path.join(OUT, 'p01-delta.json')))
CH = {c['path'] for c in delta['changed']} | {a['path'] for a in delta['added']}
PP = 'docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json'
prop = json.load(open(os.path.join(SRC, PP)))
era = json.load(open(os.path.join(PKG, 'evaluation-residual-author-assessment.json')))
R = {'proposalSha256': hashlib.sha256(open(os.path.join(SRC, PP), 'rb').read()).hexdigest(),
     'proposalChangedIn31to32': PP in CH,
     'ids': [i['id'] for i in prop['items']],
     'idsMatchAuthorAssessment': [i['id'] for i in prop['items']] == [i['id'] for i in era['items']],
     'rowCount': len(prop['items'])}
print('proposal unchanged 31->32 :', not R['proposalChangedIn31to32'])
print('30 ids identical           :', R['idsMatchAuthorAssessment'], R['rowCount'])
R['authorBindsFrozen32'] = era.get('subjectManifestSha256') == hashlib.sha256(
    open(MAN, 'rb').read()).hexdigest()
print('author assessment binds frozen32 manifest:', R['authorBindsFrozen32'])

bad_sha, unresolved, changed_ev, notpend = [], [], [], []
docs = {}
for p, a in zip(prop['items'], era['items']):
    for ev in a.get('evidence', []):
        rel = ev['path']
        docs.setdefault(rel, []).append(p['id'])
        rec = man.get(rel)
        if rec is None:
            unresolved.append((p['id'], rel))
        elif rec['sha256'] != ev.get('sha256'):
            bad_sha.append((p['id'], rel))
        if rel in CH:
            changed_ev.append((p['id'], rel))
    if a.get('independentGrade') != 'PENDING' or p.get('reviewStatus') != 'PENDING':
        notpend.append(p['id'])
R.update(evidenceUnresolved=unresolved, evidenceShaMismatches=bad_sha,
         evidenceFilesChangedIn31to32=changed_ev, rowsNotPending=notpend,
         citedDocuments={k: {'rows': len(v), 'changed31to32': k in CH} for k, v in sorted(docs.items())})
print('\nevidence unresolved:', unresolved)
print('evidence sha mismatches:', bad_sha)
print('rows whose cited evidence FILE changed 31->32:', changed_ev)
print('rows not PENDING:', notpend)
print('\ncited documents:')
for k, v in R['citedDocuments'].items():
    print('   %-72s rows=%-3d changed=%s' % (k[-72:], v['rows'], v['changed31to32']))

dep = era.get('sharedReviewDependencies')
R['tcb'] = dep[0] if dep else None
if dep:
    R['tcbDependents'] = dep[0]['dependentResidualIds']
    print('\nTCB-SCOPE-01 dependents (%d): %s' % (len(R['tcbDependents']), R['tcbDependents']))
verd = {}
for i in era['items']:
    verd[i.get('authorAssessment')] = verd.get(i.get('authorAssessment'), 0) + 1
R['authorVerdictCounts'] = verd
print('author self-assessment verdicts:', verd)
json.dump(R, open(os.path.join(OUT, 'p14-residuals32.json'), 'w'), indent=1, default=str)
print('\nwrote p14-residuals32.json')
