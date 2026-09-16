"""P13: (a) MutationReplayScopeV1 id field refs; (b) executable check of the conforming
account/outcome shape for an UNSUPPORTED-TYPED cell, using the frozen owner's derive_outcome."""
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
out = {}

# (a) MutationReplayScopeV1 id refs
rep = json.load(open(os.path.join(ROOT32, 'docs/coop/design-corrections/workflows/schemas/evaluator3/repair.schema.json')))
mrs = (rep.get('$defs') or {}).get('MutationReplayScopeV1')
props = (mrs or {}).get('properties') or {}
ids = {k: props.get(k) for k in ('requestId', 'stepId', 'projectId', 'operation') if k in props}
print('=== MutationReplayScopeV1 id property refs')
print(json.dumps(ids, indent=1)[:1200])
print('required:', (mrs or {}).get('required'))
out['mutationReplayScopeIdProps'] = ids
out['mutationReplayScopeRequired'] = (mrs or {}).get('required')

# (b) derive_outcome for the syntax-data imports cell under each account reading
INV_COMPLETE = [{'digest': 'a' * 64, 'kind': 'symbol', 'state': 'complete',
                 'deficiency': None, 'nativeCause': None}]
ACC_UNSUPPORTED = [{'accountState': 'unsupported', 'coverage': None,
                    'resolutionCompletenessState': None, 'examinedExhaustive': None,
                    'deficiency': 'language-tier-unsupported', 'nativeCause': 'capability-missing',
                    'nativeCauses': ['capability-missing'],
                    'deficiencies': ['language-tier-unsupported'],
                    'scopeIds': [], 'coverageRecords': [], 'inputRefs': [],
                    'relation': 'imports', 'resolution': 'resolved-target'}]
ACC_SUPPORTED_INCOMPLETE = [{'accountState': 'incomplete', 'coverage': 'unknown',
                             'resolutionCompletenessState': 'not-attempted', 'examinedExhaustive': False,
                             'deficiency': 'language-tier-unsupported', 'nativeCause': 'capability-missing',
                             'nativeCauses': ['capability-missing'],
                             'deficiencies': ['language-tier-unsupported'],
                             'scopeIds': ['scope2:' + 'b' * 64],
                             'coverageRecords': [{'coverageId': 'c' * 64,
                                                  'deficiency': 'language-tier-unsupported',
                                                  'nativeCause': 'capability-missing',
                                                  'inputRef': {'domain': 'coverage', 'digest': 'c' * 64},
                                                  'coverage': 'unknown',
                                                  'resolutionCompletenessState': 'not-attempted',
                                                  'examinedExhaustive': False}],
                             'inputRefs': [{'domain': 'coverage', 'digest': 'c' * 64}],
                             'relation': 'imports', 'resolution': 'resolved-target'}]
BINDING = {'ordinal': 0, 'universe': 'f' * 64,
           'enumerator': {'status': 'selected', 'closureId': 'closure2:' + 'd' * 64}}

print('\n=== derive_outcome for the syntax-data imports cell (selected U, symbol inventory complete)')
res = {}
for label, accs in (('account=unsupported-typed (owner reading)', ACC_UNSUPPORTED),
                    ('account=supported-available/incomplete (consumer reading)', ACC_SUPPORTED_INCOMPLETE)):
    d = M.derive_outcome(enumerator_status='selected', universe=BINDING['universe'], required=False,
                         inventories=INV_COMPLETE, account_summaries=accs,
                         candidate_rec=None, candidate_digest=None, candidate_cap=False,
                         binding=BINDING)
    res[label] = {'state': d['state'], 'deficiency': d['deficiency'], 'nativeCause': d['nativeCause'],
                  'sourceCount': len(d['sources'])}
    print('  %-58s -> state=%-9s pair=(%s,%s)' % (label, d['state'], d['deficiency'], d['nativeCause']))
out['deriveOutcomeUnderEachReading'] = res
out['consumerHostRow'] = {'state': 'partial', 'deficiency': 'language-tier-unsupported',
                          'nativeCause': 'capability-missing'}
print('  consumer host row                                          -> state=partial   pair=(language-tier-unsupported,capability-missing)')

print('\n=== conforming shape implied for an UNSUPPORTED-TYPED cell')
print('  account   : applicability=unsupported-typed, coverageIds=[], sourceUniverse=<binding U>')
print('  outcome   : state=%s, deficiency=%s, nativeCause=%s'
      % (res['account=unsupported-typed (owner reading)']['state'],
         res['account=unsupported-typed (owner reading)']['deficiency'],
         res['account=unsupported-typed (owner reading)']['nativeCause']))
print('  consequence: the lawfully minted unknown/language-tier-unsupported Coverage is NOT')
print('               referenced by any account, and the cell outcome discloses no carrier.')

json.dump(out, open(os.path.join(HERE, 'p13-corrective-route.json'), 'w'), indent=2, default=str)
print('\nWROTE p13-corrective-route.json')
