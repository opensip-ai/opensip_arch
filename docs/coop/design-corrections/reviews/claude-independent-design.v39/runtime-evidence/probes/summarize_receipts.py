"""Print a structural summary of this runtime's receipts and the source38 review keys (stdout only; writes nothing)."""
import collections, json, os
RT = '/private/tmp/opensip-design-corrections/claude-independent-design.v39'
REC = RT + '/receipts'


def J(p):
    with open(p, encoding='utf-8') as fh:
        return json.load(fh)


def shape(x, depth=0):
    if isinstance(x, dict):
        if depth >= 2:
            return '{%d keys}' % len(x)
        return {k: shape(v, depth + 1) for k, v in list(x.items())[:40]}
    if isinstance(x, list):
        return '[%d]' % len(x) + ('' if not x or depth >= 2 else ' first=' + json.dumps(shape(x[0], depth + 1), default=str)[:300])
    if isinstance(x, str):
        return x[:160]
    return x


for name in ('subject-verification.json', 'planning-checks.json', 'archive-verification.source39.json', 'archive-verification.source39-pkg.json'):
    print('==', name)
    print(json.dumps(shape(J(REC + '/' + name)), indent=1, default=str)[:5000])
print('== delta-diff-summary')
print(json.dumps(shape(J(REC + '/delta-diff-summary.json')), indent=1)[:1500])
for f in sorted(os.listdir(REC + '/reference')):
    print('== reference/', f)
g = J(REC + '/reference/groups-report.all.json')
print(json.dumps(shape(g), indent=1, default=str)[:3000])
for r in g.get('rows', []):
    print({k: (v[-400:] if isinstance(v, str) else v) for k, v in r.items() if k not in ('copyBefore',)})
for f in sorted(os.listdir(REC + '/probes')):
    d = J(REC + '/probes/' + f)
    rows = d.get('rows')
    print('== probes/', f, 'rows', len(rows) if isinstance(rows, list) else None, 'failed', [x.get('case') for x in d.get('failed', [])] if isinstance(d.get('failed'), list) else d.get('failed'),
          'observations', [x['case'] for x in rows if isinstance(x, dict) and x.get('kind') == 'observation'] if isinstance(rows, list) else None, 'keys', list(d)[:20])
for f in sorted(os.listdir(REC + '/runs')):
    if f.endswith('.run.json'):
        print('== runs/', f, json.dumps(J(REC + '/runs/' + f))[:700])
kinds = collections.Counter()
for line in open(REC + '/read-ledger.jsonl'):
    kinds[json.loads(line)['kind']] += 1
print('== ledger kinds', dict(kinds))
pv = RT + '/work/package-v16-verify/verification.json'
if os.path.exists(pv):
    print('== package verify', json.dumps(shape(J(pv)), indent=1, default=str)[:3000])
v38 = J('/private/tmp/opensip-design-corrections/claude-independent-design.v38/review.json')
print('== v38 keys', list(v38))
print('== v38 readScope', {k: (len(v) if isinstance(v, list) else v) for k, v in v38['readScope'].items()})
for k in ('fDispositions', 'evaluationResidualDispositions', 'arDispositions', 'fwDispositions', 'inheritedResidualDispositions', 'scopedReviewOwnerDispositions'):
    print('== v38', k, len(v38[k]), json.dumps(v38[k][0])[:700])
print('== v38 TCB', json.dumps(v38['sharedAssumptionTCBSCOPE01'])[:1500])
print('== v38 advisories ids', [a['id'] for a in v38['advisories']], 'verdict', v38['verdict'])
