"""R01 — R33-REC-04: audit ALL 107 currentStatusOn33 / currentBasisOn33 fields for source32 prose
appended unqualified into a CURRENT field, using measured facts from frozen33."""
import json, os, re

V33 = '/tmp/opensip-design-corrections/claude-independent-design.v33'
OUT = '/tmp/opensip-design-corrections/claude-independent33-reconciliation.v1/receipts'
V = json.load(open(os.path.join(V33, 'review.json')))
R = {}

# measured current facts
FACTS = {'frozen33Files': 12899, 'frozen32Files': 12898,
         'package10Members': 305, 'package8Members': 277,
         'currentLayer': 'implementation-normative-inputs.v4.json',
         'priorLayer': 'implementation-normative-inputs.v3.json'}
R['measuredCurrentFacts'] = FACTS

STALE = [
    (r'\b277\b', 'package member count 277 is package8; current package10 has 305'),
    (r'\b12,?898\b', 'file count 12898 is source32; frozen33 has 12899'),
    (r'frozen32|source32 manifest|against frozen32', 'binds to source32 rather than 33'),
    (r'snapshot32 owner|snapshot32', 'names the source32 owner'),
    (r'implementation-normative-inputs\.v3', 'names layer3 where layer4 is current'),
    (r'I executed it against frozen32|executed it myself against source32',
     'claims an execution performed against 32 as current evidence'),
]
MAPS = ('fDispositions', 'evaluationResidualDispositions', 'arDispositions', 'fwDispositions',
        'inheritedResidualDispositions', 'scopedReviewOwnerDispositions')
FIELD = {'fDispositions': 'currentBasisOn33'}
hits = []
n = 0
for mp in MAPS:
    fld = FIELD.get(mp, 'currentStatusOn33')
    for rid, row in V[mp].items():
        n += 1
        txt = str(row.get(fld) or '')
        for pat, why in STALE:
            m = re.search(pat, txt, re.I)
            if m:
                hits.append({'map': mp, 'row': rid, 'field': fld, 'pattern': pat, 'why': why,
                             'excerpt': txt[max(0, m.start() - 90):m.start() + 110]})
R['rowsAudited'] = n
R['staleHits'] = hits
print('rows audited: %d | stale-current hits: %d' % (n, len(hits)))
for h in hits:
    print('\n%-34s %-10s %s' % (h['map'] + '/' + h['row'], h['pattern'][:14], h['why']))
    print('    …%s…' % h['excerpt'].replace('\n', ' ')[:180])

# root's named examples, checked individually
print('\n=== root-named examples ===')
named = {}
for mp, rid in (('fDispositions', 'F-01'), ('fDispositions', 'F-03'), ('fDispositions', 'F-05'),
                ('fDispositions', 'F-09'), ('fDispositions', 'F-10'), ('fDispositions', 'F-13'),
                ('evaluationResidualDispositions', 'RES-EP13-05'),
                ('scopedReviewOwnerDispositions', 'DR-204')):
    fld = FIELD.get(mp, 'currentStatusOn33')
    txt = str(V[mp][rid].get(fld) or '')
    named[rid] = txt
    print('\n--- %s.%s ---' % (rid, fld))
    print(txt[:420].replace('\n', ' '))
R['rootNamedExamples'] = named

# F-09: does the delta actually touch its subject?
p01 = json.load(open(os.path.join(V33, 'receipts', 'p01-delta.json')))
CH = {c['path'] for c in p01['changed']} | {a['path'] for a in p01['added']}
R['executionOwnersInDelta'] = sorted(p for p in CH if 'execution' in p)
R['F09SubjectIsExecutionInputs'] = True
print('\nexecution-inputs owners IN the 32->33 delta:', R['executionOwnersInDelta'])
print('F-09 current text claims no 32->33 subject change:',
      'nothing in my derived 32->33 delta touches this row' in named['F-09'])

# F-10 provenance: which package10 groups were reminted on 33 vs carried exact?
R['f10Question'] = ('F-10 needs current mixed provenance: which groups were newly constructed on 33 '
                    'and which are exact earlier bytes re-verified')
json.dump(R, open(os.path.join(OUT, 'r01-fieldaudit.json'), 'w'), indent=1, default=str)
print('\nwrote r01-fieldaudit.json')
