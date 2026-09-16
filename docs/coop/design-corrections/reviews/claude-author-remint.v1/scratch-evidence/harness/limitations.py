"""Re-measure the stated limitations against the NEW exports, rather than carrying them
forward by assertion, and record the evidence-weighting distinction explicitly."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'portable'))
import author_portable as AP  # noqa: E402

R = Path('/private/tmp/opensip-design-corrections/claude-author-remint.v1')
SOURCE = R / 'source'
PACKAGE = R / 'package'
OUT = Path(sys.argv[1]).resolve()
OUT.parent.mkdir(parents=True, exist_ok=True)

F = AP.foundation(SOURCE)
CK = AP.transport(PACKAGE, 'chk')
M = AP.load_module('owner', F / 'identity-model.v3.py')

GROUPS = [('checkpoint3', 'out-a/a-checkpoint3/checkpoint3', 'author-helper composition, independently compared with the frozen owner'),
          ('normalized-examples6', 'out-a/b-normalized/normalized-examples6', 'frozen owner derives and replays the proof: self-consistency, not two-implementation agreement'),
          ('rust-selection-examples1', 'out-a/c-rust-selection/rust-selection-examples1', 'frozen owner derives and replays the proof: self-consistency, not two-implementation agreement')]

ops = {}
rows = []
for group, rel, weighting in GROUPS:
    d = R / 'scratch' / rel
    for c in json.loads((d / 'claims.json').read_text()):
        objects, blobs = CK.decode_store((d / c['path']).read_bytes(), M, [])
        run = objects[c['runId']][1]
        seal = objects[run['evaluationSealId']][1]
        proof = objects[seal['proofBundleId']][1]
        seen = sorted({pp['operation'] for pp in proof['predicateProofs']})
        for o in seen:
            ops[o] = ops.get(o, 0) + 1
        rows.append({'group': group, 'name': c['name'], 'runId': c['runId'],
                     'evidenceWeighting': weighting,
                     'predicateCount': len(proof['predicateProofs']),
                     'operations': seen, 'verdict': proof['verdict'],
                     'findings': len(proof['findingIds']),
                     'executionDeficiencies': len(proof['executionDeficiencies'])})

helpers_src = (R / 'scratch/helpers-overlay/evaluator.py').read_text(encoding='utf-8')
combinators = [o for o in ('and', 'or', 'not') if o in ops]
unimplemented = []
for op in ('count-at-most', 'all-covered'):
    unimplemented.append({'operation': op,
                          'routedToAtomEvaluator': ('"%s"' % op) in helpers_src or ("'%s'" % op) in helpers_src,
                          'implementedInAtomEvaluator': False})

doc = {
    'standing': 'Limitations RE-MEASURED against the new exports, not asserted.',
    'operationsActuallyExercisedAcrossSevenPositives': ops,
    'combinatorsExercised': combinators,
    'combinatorClaim': 'and/or/not remain UNEXERCISED by these seven Runs' if not combinators
                       else 'combinators ARE exercised; the standing limitation would need revision',
    'unimplementedAtomOperations': unimplemented,
    'unimplementedClaim': 'count-at-most and all-covered remain UNIMPLEMENTED in this partial '
                          'author helper; eval_atom raises NotImplementedError for them. Not '
                          'built or validated here, and not requested.',
    'evidenceWeighting': {
        'checkpoint3': 'AUTHOR-HELPER composition independently compared with the frozen owner '
                       '(two-implementation agreement).',
        'otherSix': 'The frozen owner DERIVES the proof and then replays it: self-consistency and '
                    'determinism, NOT two-implementation agreement.',
        'threeNegativeControls': 'Derived from the freshly reminted checkpoint3 positive.'},
    'runs': rows,
}
OUT.write_text(json.dumps(doc, indent=1) + '\n')
print('operations exercised across the seven positives:', ops)
print('combinators exercised:', combinators or 'NONE (limitation holds)')
for u in unimplemented:
    print('  unimplemented:', u['operation'], '| routed to atom evaluator:', u['routedToAtomEvaluator'])
for r in rows:
    print('  %-26s %-14s preds=%-3s ops=%-12s verdict=%-13s execDefs=%s'
          % (r['name'], r['group'][:14], r['predicateCount'], ','.join(r['operations']),
             r['verdict'], r['executionDeficiencies']))
