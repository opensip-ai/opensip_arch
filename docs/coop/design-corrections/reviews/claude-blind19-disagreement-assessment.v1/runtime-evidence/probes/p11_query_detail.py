"""P11: resolve root's four query/mutation items against the exact published owners."""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT32 = '/tmp/opensip-design-corrections/candidate-subject.v32'
CB = '/tmp/opensip-design-corrections/consumer-b.v19'
CONTRACT = os.path.join(ROOT32, 'docs/coop/design-corrections/workflows/query-projection-contract.v3.md')
COMMON = os.path.join(ROOT32, 'docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json')

out = {}
text = open(CONTRACT, encoding='utf-8', errors='ignore').read()
lines = text.split('\n')
i = next(i for i, l in enumerate(lines) if l.startswith('## 5. Cursor'))
print('=== query-projection-contract.v3.md section 5 (verbatim)')
sec = '\n'.join(lines[i:i + 16])
print(sec)
out['contractSection5'] = sec

# RequestId / StepId published patterns
common = json.load(open(COMMON))
pats = {}
for k, v in (common.get('$defs') or {}).items():
    if isinstance(v, dict) and v.get('pattern') and ('Request' in k or 'Step' in k or 'Id' == k[-2:]):
        pats[k] = {'pattern': v['pattern'], 'description': (v.get('description') or '')[:200]}
print('\n=== evaluator3 common.schema.json id patterns')
for k, v in sorted(pats.items()):
    print('  %-22s %s' % (k, v['pattern']))
out['commonIdPatterns'] = pats

q = json.load(open(os.path.join(CB, 'output/query/graph-query-reconstruction.json')))
rid = 'req1_abababababababababababababababab'
checks = []
for k, v in sorted(pats.items()):
    if 'Request' in k:
        checks.append({'def': k, 'pattern': v['pattern'], 'value': rid,
                       'matches': bool(re.match(v['pattern'], rid))})
print('\n=== observed requestId vs published patterns')
for c in checks:
    print('   %-22s %-46s -> %s' % (c['def'], c['pattern'][:44], c['matches']))
out['requestIdChecks'] = checks

# stepId presence anywhere in the artifact
print('\n=== stepId present in query artifact:', 'stepId' in json.dumps(q))
out['stepIdPresent'] = 'stepId' in json.dumps(q)

# operations 1/5/6: the truncated ones
print('\n=== truncated operations detail')
tr = []
for idx, op in enumerate(q.get('operations') or []):
    ctx = (op.get('response') or {}).get('context') or {}
    if ctx.get('truncated'):
        row = {'index': idx, 'operation': op.get('operation') or op.get('name'),
               'context': ctx,
               'requestPage': (op.get('request') or {}).get('page'),
               'responseKeys': sorted((op.get('response') or {}).keys())}
        tr.append(row)
        print('  op%d %s' % (idx, row['operation']))
        print('     context:', json.dumps(ctx)[:300])
        print('     request.page:', json.dumps(row['requestPage'])[:200])
out['truncatedOperations'] = tr

# endpoint membership / external vertices
em = q.get('endpointMembership')
print('\n=== endpointMembership')
print(json.dumps(em, indent=1)[:1800])
out['endpointMembership'] = em

# mutation scope artifacts
mk = json.load(open(os.path.join(CB, 'output/vectors/mutation-keys.json')))
print('\n=== mutation-keys.json')
print(json.dumps(mk, indent=1)[:1500])
out['mutationKeys'] = mk

json.dump(out, open(os.path.join(HERE, 'p11-query-detail.json'), 'w'), indent=2, default=str)
print('\nWROTE p11-query-detail.json')
