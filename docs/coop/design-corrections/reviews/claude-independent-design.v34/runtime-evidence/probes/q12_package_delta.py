"""Q12 — the package facts the F rows need on source34: package10 -> package11 member delta (which of
the members I verified before are carried byte-identically), the residual author-assessment binding,
and the construction-account standing. Read-only on both packages."""
import hashlib, json, os

P10 = '/tmp/opensip-design-corrections/claude-author-package-successor.v10'
P11 = '/tmp/opensip-design-corrections/claude-author-package-successor.v11'
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v34/receipts'
REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews'
R = {}


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def rows(pkg):
    am = json.load(open(os.path.join(pkg, 'artifact-manifest.json')))
    return {r['path']: r['sha256'] for r in (am['files'] if isinstance(am, dict) else am)}


m10, m11 = rows(P10), rows(P11)
R['package10ManifestSha256'] = sha(os.path.join(P10, 'artifact-manifest.json'))
R['package11ManifestSha256'] = sha(os.path.join(P11, 'artifact-manifest.json'))
R['members'] = {'package10': len(m10), 'package11': len(m11)}
R['added'] = sorted(p for p in m11 if p not in m10)
R['removed'] = sorted(p for p in m10 if p not in m11)
R['changedCommon'] = sorted(p for p in m11 if p in m10 and m10[p] != m11[p])
R['identicalCommon'] = sum(1 for p in m11 if p in m10 and m10[p] == m11[p])
print('package10 %d -> package11 %d members | added %d removed %d changed-common %d identical-common %d'
      % (len(m10), len(m11), len(R['added']), len(R['removed']), len(R['changedCommon']), R['identicalCommon']))
print('added  :', R['added'])
print('removed:', R['removed'])
print('changed:', R['changedCommon'])
for p in ('README.md', 'verify-package.py', 'author_portable.py', 'evaluator.py.patch', 'check-author-properties.py',
          'author-properties.json', 'query-assessment.json'):
    if p in m11:
        R.setdefault('keyMembers', {})[p] = {'inBoth': p in m10, 'identical': m10.get(p) == m11[p]}
print('key members:', R.get('keyMembers'))

era = json.load(open(os.path.join(P11, 'evaluation-residual-author-assessment.json')))
man34 = sha(os.path.join(REV, 'candidate-subject.v34.json'))
man33 = sha(os.path.join(REV, 'candidate-subject.v33.json'))
verd = {}
for it in era.get('items', []):
    verd[it.get('authorAssessment')] = verd.get(it.get('authorAssessment'), 0) + 1
dep = era.get('sharedReviewDependencies') or []
R['residualAssessment'] = {
    'subjectManifestSha256': era.get('subjectManifestSha256'),
    'bindsFrozen34': era.get('subjectManifestSha256') == man34,
    'bindsFrozen33': era.get('subjectManifestSha256') == man33,
    'rows': len(era.get('items', [])), 'verdicts': verd,
    'independentGrades': sorted({str(it.get('independentGrade')) for it in era.get('items', [])}),
    'tcbDependents': len(dep[0]['dependentResidualIds']) if dep else None,
    'tcbId': dep[0].get('id') if dep else None,
    'identicalToPackage10': m10.get('evaluation-residual-author-assessment.json') == m11.get('evaluation-residual-author-assessment.json'),
    'evidenceResolveAgainst': sorted({e.get('resolveAgainst') for it in era.get('items', []) for e in it.get('evidence', [])})}
print('residual assessment:', json.dumps(R['residualAssessment']))
sb = json.load(open(os.path.join(P11, 'source-binding.v34.json')))
R['binding34'] = sb
for acct in sb.get('constructionAccounts') or []:
    R.setdefault('constructionAccountsIdenticalToPackage10', {})[acct] = m10.get(acct) == m11.get(acct)
print('construction accounts identical to package10:', R.get('constructionAccountsIdenticalToPackage10'))
json.dump(R, open(os.path.join(OUT, 'q12-package-delta.json'), 'w'), indent=1)
print('wrote q12-package-delta.json')
