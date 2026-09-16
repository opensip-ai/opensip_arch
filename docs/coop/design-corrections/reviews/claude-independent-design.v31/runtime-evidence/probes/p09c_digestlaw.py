"""PROBE 09c (v31) — corrects p09 AND p09b.

p09 read rc=2 from mutated runs as digest-law enforcement. p09b showed the real cause: the native
checker is SOURCE-PINNED and answers PIN-MISMATCH, because native-evidence.schemas.v2.json is a
pinned file. The pin gate fires FIRST. That is correct source behaviour and I do not bypass it, so
mutation of a pinned file can never test this law.

Two honest routes are used instead:
  (a) read the checker's OWN frozen report (a frozen member) for its measured digestLaw block;
  (b) exercise the checker's exact enforcement predicate in-memory over a mutated PARSED copy,
      which decides the law without altering any pinned byte.
"""
import hashlib, json, os, re

SRC = '/tmp/opensip-design-corrections/candidate-subject.v31'
N = os.path.join(SRC, 'docs/coop/design-corrections/native')
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v31/receipts'
R = {'corrects': ['p09 treated PIN-MISMATCH (rc=2) as digest-law enforcement',
                  'p09b confirmed the real cause but still could not test the law by mutation']}

# ---- (a) the checker's own frozen report ----
rep = json.load(open(os.path.join(N, 'native-evidence-report.v2.json')))
R['frozenReportResult'] = rep.get('result')
R['frozenReportDigestLaw'] = rep.get('digestLaw')
print('frozen native-evidence-report.v2.json:')
print('   result   :', rep.get('result'))
print('   digestLaw:', json.dumps(rep.get('digestLaw'))[:400])
dl = rep.get('digestLaw') or {}
R['reportedAnnotationSites'] = dl.get('annotationSites')
R['reportedSitesEqualMyMeasured76'] = dl.get('annotationSites') == 76
R['reportedNoUndeclared'] = (not dl.get('undeclaredRetentionSites')
                             and not dl.get('undeclaredRepresentationSites'))
print('   checker-measured sites == my independent 76 :', R['reportedSitesEqualMyMeasured76'])
print('   checker reports zero undeclared sites       :', R['reportedNoUndeclared'])

# is the schema really pinned? (explains PIN-MISMATCH, and shows the gate's scope)
pins = json.load(open(os.path.join(N, 'source-pins.v2.json')))
def pinned_paths(o, acc):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ('path', 'file') and isinstance(v, str):
                acc.add(v)
            pinned_paths(v, acc)
    elif isinstance(o, list):
        for v in o:
            pinned_paths(v, acc)
    return acc
P = pinned_paths(pins, set())
R['nativePinLedgerEntries'] = len(P)
R['schemaIsPinned'] = any(p.endswith('native-evidence.schemas.v2.json') for p in P)
R['checkerIsPinned'] = any(p.endswith('check_native_evidence.v2.py') for p in P)
print('\nnative pin ledger entries: %d | schema pinned: %s | checker pinned: %s'
      % (len(P), R['schemaIsPinned'], R['checkerIsPinned']))

# ---- (b) the checker's exact predicate, in memory ----
src = open(os.path.join(N, 'check_native_evidence.v2.py'), encoding='utf-8').read()
R['enforcementSource'] = [l.strip() for l in src.splitlines()
                          if 'undeclared_retention' in l or 'undeclared_representation' in l]
print('\nenforcement lines in the checker:')
for l in R['enforcementSource']:
    print('   ', l[:150])

sch = json.load(open(os.path.join(N, 'native-evidence.schemas.v2.json')))
law = sch['x-opensip-digest-law']


def sites_of(s):
    out = []
    def walk(x, p):
        if isinstance(x, dict):
            if 'x-opensip-digest' in x:
                out.append({'path': p, **x['x-opensip-digest']})
            for k, v in x.items():
                walk(v, p + '/' + k)
        elif isinstance(x, list):
            for i, v in enumerate(x):
                walk(v, p + '/' + str(i))
    walk(s, '')
    return out


def decide(s, l):
    ds = sites_of(s)
    return ([x['path'] for x in ds if x.get('retention') not in l['retention']],
            [x['path'] for x in ds if x.get('representation') not in l['representations']],
            len(ds))


ret, rep2, n = decide(sch, law)
R['inMemoryBaseline'] = {'sites': n, 'undeclaredRetention': ret, 'undeclaredRepresentation': rep2}
print('\nin-memory baseline: %d sites, undeclared retention=%d representation=%d' % (n, len(ret), len(rep2)))

import copy
# mutation 1: an undeclared retention value
m1 = copy.deepcopy(sch)
m1['$defs']['SourceUnitOwnershipV1']['properties']['units']['items']['properties']['unitId'][
    'x-opensip-digest']['retention'] = 'conjured-from-nowhere'
r1 = decide(m1, law)
R['inMemory_undeclaredRetention'] = {'named': r1[0], 'wouldFailOkConjunct': bool(r1[0])}
print('mutation: undeclared retention -> named sites %s | checker ok-conjunct would be False: %s'
      % (r1[0], bool(r1[0])))

# mutation 2: an undeclared representation value
m2 = copy.deepcopy(sch)
m2['$defs']['SourceUnitOwnershipV1']['properties']['selectedUnitIds']['items'][
    'x-opensip-digest']['representation'] = 'invented-rep'
r2 = decide(m2, law)
R['inMemory_undeclaredRepresentation'] = {'named': r2[1], 'wouldFailOkConjunct': bool(r2[1])}
print('mutation: undeclared representation -> named sites %s | ok-conjunct False: %s'
      % (r2[1], bool(r2[1])))

# mutation 3: catalog entry removed while its 3 uses remain
l3 = copy.deepcopy(law)
del l3['retention']['derived']
r3 = decide(sch, l3)
R['inMemory_catalogRemoval'] = {'named': r3[0], 'count': len(r3[0]), 'wouldFailOkConjunct': bool(r3[0])}
print('mutation: `derived` removed from catalog -> %d sites named: %s' % (len(r3[0]), r3[0]))

R['lawIsDecidableAndLoadBearing'] = bool(r1[0]) and bool(r2[1]) and len(r3[0]) == 3 and not ret and not rep2
print('\nlaw decidable, baseline clean, every mutation named:', R['lawIsDecidableAndLoadBearing'])
json.dump(R, open(os.path.join(OUT, 'p09c-digestlaw.json'), 'w'), indent=1, default=str)
print('wrote p09c-digestlaw.json')
