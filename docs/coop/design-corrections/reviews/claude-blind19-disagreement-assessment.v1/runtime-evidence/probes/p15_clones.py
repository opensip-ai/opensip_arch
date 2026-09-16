"""P15: what the owner actually derives for the clones-fact cells (root's 'class C')."""
import importlib.util, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT32 = '/tmp/opensip-design-corrections/candidate-subject.v32'
FOUND = os.path.join(ROOT32, 'docs/coop/design-corrections/foundation')


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


M = load('owner', os.path.join(FOUND, 'execution_inputs_model.v1.py'))
print('CANDIDATE_CAPS      :', sorted(M.CANDIDATE_CAPS))
print('clones-fact is cand :', 'clones-fact' in M.CANDIDATE_CAPS)
print('_matrix_pairs(clones-fact):', M._matrix_pairs('clones-fact'))

# Reproduce the syntax-code / typescript / rust clones-fact cell:
# selected binding with U, file inventory complete, clones account complete, NO candidate record.
INV = [{'digest': 'a' * 64, 'kind': 'file', 'state': 'complete', 'deficiency': None, 'nativeCause': None}]
ACC = [{'accountState': 'complete', 'coverage': 'complete',
        'resolutionCompletenessState': 'not-applicable', 'examinedExhaustive': True,
        'deficiency': None, 'nativeCause': None, 'nativeCauses': [], 'deficiencies': [],
        'scopeIds': ['scope2:' + 'b' * 64], 'coverageRecords': [],
        'inputRefs': [], 'relation': 'clones', 'resolution': 'normalized-body-hash'}]
BINDING = {'ordinal': 0, 'universe': 'f' * 64,
           'enumerator': {'status': 'selected', 'closureId': 'closure2:' + 'd' * 64}}

out = {'candidateCaps': sorted(M.CANDIDATE_CAPS),
       'clonesFactIsCandidateCap': 'clones-fact' in M.CANDIDATE_CAPS,
       'matrixPairsClonesFact': M._matrix_pairs('clones-fact')}

for cand_cap in (True, False):
    d = M.derive_outcome(enumerator_status='selected', universe=BINDING['universe'], required=True,
                         inventories=INV, account_summaries=ACC,
                         candidate_rec=None, candidate_digest=None, candidate_cap=cand_cap,
                         binding=BINDING)
    print('\ncandidate_cap=%-5s -> state=%-9s pair=(%s,%s) sources=%s' % (
        cand_cap, d['state'], d['deficiency'], d['nativeCause'],
        [(s.get('source'), s.get('deficiency'), s.get('nativeCause')) for s in d['sources']]))
    out['deriveOutcome_candidateCap_%s' % cand_cap] = {
        'state': d['state'], 'deficiency': d['deficiency'], 'nativeCause': d['nativeCause'],
        'sources': [{'source': s.get('source'), 'deficiency': s.get('deficiency'),
                     'nativeCause': s.get('nativeCause')} for s in d['sources']]}

print('\nconsumer host rows for clones-fact: state=partial, pair=(None,None)  [syntax-code/typescript/rust]')
print('owner line 1413 compares row.state vs derived state; line 1424 compares the pairs.')

# is a candidate owed for clones-fact per the enumeration contract?
ec = open(os.path.join(FOUND, 'enumeration-contract.v1.md'), encoding='utf-8', errors='ignore').read()
import re
print('\n=== enumeration-contract lines naming candidate capabilities')
for l in ec.split('\n'):
    if 'clones-near' in l or 'clones-cross' in l or 'CANDIDATE_CAPS' in l:
        print('   ', l.strip()[:260])
        out.setdefault('enumerationCandidateLines', []).append(l.strip()[:400])

mx = json.load(open(os.path.join(ROOT32, 'docs/coop/design-corrections/native/native-capability-matrix.v2.json')))
caps = {c['id'] if 'id' in c else c.get('capabilityId'): c for c in mx.get('capabilities', [])}
print('\n=== matrix capability rows: relations per capability')
for k in ('clones-fact', 'clones-near', 'clones-cross-tsjs'):
    c = caps.get(k)
    print('  %-18s relations=%s' % (k, json.dumps((c or {}).get('relations'))))
    out.setdefault('matrixCapabilityRelations', {})[k] = (c or {}).get('relations')

json.dump(out, open(os.path.join(HERE, 'p15-clones.json'), 'w'), indent=2, default=str)
print('\nWROTE p15-clones.json')
