"""P10: bounded substantive review of the final19 query artifact and mutation scope against
their published owners in frozen v32. Confirms or refutes root's four preliminary items."""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT32 = '/tmp/opensip-design-corrections/candidate-subject.v32'
CB = '/tmp/opensip-design-corrections/consumer-b.v19'
Q = os.path.join(CB, 'output/query/graph-query-reconstruction.json')
SCHEMA = os.path.join(ROOT32, 'docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json')
CONTRACT = os.path.join(ROOT32, 'docs/coop/design-corrections/workflows/query-projection-contract.v3.md')
ENVELOPE = os.path.join(ROOT32, 'docs/coop/design-corrections/workflows/schemas/evaluator3/command-envelope.schema.json')

q = json.load(open(Q))
schema = json.load(open(SCHEMA))
contract = open(CONTRACT, encoding='utf-8', errors='ignore').read()

print('=== final19 query artifact top keys')
print(sorted(q.keys())[:40])
out = {'queryArtifactKeys': sorted(q.keys())}


def walk(o, path=''):
    if isinstance(o, dict):
        yield path, o
        for k, v in o.items():
            yield from walk(v, path + '/' + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, path + '/' + str(i))


nodes = list(walk(q))

# --- root item 1: truncated page / truncated=true
trunc = [(p, {k: v for k, v in o.items() if k in ('truncated', 'nextCursor', 'items', 'pageSize')})
         for p, o in nodes if isinstance(o, dict) and 'truncated' in o]
print('\n=== truncated occurrences:', len(trunc))
for p, o in trunc[:10]:
    print('  ', p, json.dumps(o)[:220])
out['truncated'] = [{'path': p, 'value': o} for p, o in trunc]

# --- root item 2: cursor ord:1 lacking selection binding
cursors = [(p, o.get('cursor') or o.get('nextCursor'))
           for p, o in nodes if isinstance(o, dict) and (o.get('cursor') or o.get('nextCursor'))]
print('\n=== cursors:', len(cursors))
for p, c in cursors[:12]:
    print('  ', p, repr(c)[:160])
out['cursors'] = [{'path': p, 'cursor': c} for p, c in cursors]
cursor_law = [l.strip() for l in contract.split('\n') if 'cursor' in l.lower()]
print('\n=== contract lines mentioning cursor:', len(cursor_law))
for l in cursor_law[:12]:
    print('   ', l[:230])
out['contractCursorLines'] = cursor_law[:30]

# schema cursor definition
cur_defs = {}
for p, o in walk(schema):
    if isinstance(o, dict) and 'cursor' in (o.get('properties') or {}):
        cur_defs[p] = json.dumps(o['properties']['cursor'])[:700]
for p, v in list(cur_defs.items())[:6]:
    print('\n--- schema cursor at', p)
    print('   ', v)
out['schemaCursorDefs'] = cur_defs

# --- root item 3: external-import omission
imp = [(p, o) for p, o in nodes if isinstance(o, dict)
       and any(k for k in o if 'import' in k.lower())]
print('\n=== nodes with import-ish keys:', len(imp))
for p, o in imp[:8]:
    print('  ', p, sorted(k for k in o if 'import' in k.lower()))
out['importNodes'] = [{'path': p, 'keys': sorted(k for k in o if 'import' in k.lower())} for p, o in imp[:40]]
ext = [l.strip() for l in contract.split('\n') if 'external' in l.lower()]
print('\n=== contract lines mentioning external:', len(ext))
for l in ext[:10]:
    print('   ', l[:230])
out['contractExternalLines'] = ext[:20]

# --- root item 4: invalid request/step IDs
ids = {}
for p, o in nodes:
    if not isinstance(o, dict):
        continue
    for k in ('requestId', 'stepId', 'executionId'):
        if k in o:
            ids.setdefault(k, []).append((p, o[k]))
print('\n=== id fields found')
for k, vs in ids.items():
    uniq = sorted({repr(v) for _p, v in vs})
    print('  %-12s count=%d distinct=%s' % (k, len(vs), uniq[:6]))
out['idFields'] = {k: sorted({str(v) for _p, v in vs}) for k, vs in ids.items()}

# schema patterns for those ids
pats = {}
for p, o in walk(schema):
    if isinstance(o, dict) and o.get('pattern') and p.split('/')[-1] in ('RequestId', 'StepId', 'requestId', 'stepId'):
        pats[p] = o['pattern']
for p, o in walk(json.load(open(ENVELOPE))):
    if isinstance(o, dict) and o.get('pattern') and p.split('/')[-1] in ('RequestId', 'StepId', 'requestId', 'stepId'):
        pats['envelope' + p] = o['pattern']
print('\n=== published id patterns')
for p, v in pats.items():
    print('   %s  ->  %s' % (p, v))
out['idPatterns'] = pats

# validate the observed ids against the patterns
checks = []
for k, vs in ids.items():
    for p, v in vs:
        for pp, rx in pats.items():
            if k.lower() in pp.lower():
                ok = bool(re.match(rx, str(v))) if isinstance(v, str) else False
                checks.append({'idField': k, 'value': v, 'pattern': rx, 'patternAt': pp, 'matches': ok})
print('\n=== id conformance checks:', len(checks))
for c in checks[:20]:
    print('   %-10s %-28s vs %-40s -> %s' % (c['idField'], str(c['value'])[:26], c['pattern'][:38], c['matches']))
out['idConformance'] = checks

json.dump(out, open(os.path.join(HERE, 'p10-query-mutation.json'), 'w'), indent=2, default=str)
print('\nWROTE p10-query-mutation.json')
