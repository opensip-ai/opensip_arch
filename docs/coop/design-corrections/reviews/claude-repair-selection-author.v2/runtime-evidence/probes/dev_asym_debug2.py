"""Compare proof.evaluationInputRefs view roots with evidence.viewIds on both shapes."""
import importlib.util
from pathlib import Path

SRC = Path('/tmp/opensip-design-corrections/repair-selection-successor.v2/source')
FOUND = SRC / 'docs/coop/design-corrections/foundation'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


P = load('dev_replay', FOUND / 'check-replay.v3.py')
F, M = P.F, P.M
SYMBOL_ROWS = [{'nativeSubjectId': 'ts-symbol:src/index.ts#x', 'qualifiedName': 'x'}]

for label, kw in [('control', dict(multiple_universes=True, symbol_rows=SYMBOL_ROWS)),
                  ('asymmetric', dict(multiple_universes=True, symbol_rows=SYMBOL_ROWS,
                                      symbol_only_second_program=True))]:
    g = F.build_file_inputs(**kw)
    seed, objects, blobs, out = F.seal_fixture(g)
    proof = out['proof']
    proof_views = {'view2:' + r['digest'] for r in proof['evaluationInputRefs'] if r['domain'] == 'view'}
    ev = objects[seed['evidenceId']][1]
    print('===', label)
    print('  evidence viewIds  ', len(ev['viewIds']))
    print('  proof view refs   ', len(proof_views))
    print('  evidence - proof  ', sorted(set(ev['viewIds']) - proof_views))
    print('  proof - evidence  ', sorted(proof_views - set(ev['viewIds'])))
    print('  proof ref domains ', sorted({r['domain'] for r in proof['evaluationInputRefs']}))
    print('  input ref domains ', sorted({r['domain'] for r in g['inputs']['evaluationInputRefs']}))
    print('  inputs view refs  ', len([r for r in g['inputs']['evaluationInputRefs'] if r['domain'] == 'view']))
    print('  verdict           ', proof['verdict'], '| findings', len(proof['findingIds']))
