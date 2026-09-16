"""For each reminted negative control, diff the claimed proof against the owner's recomputed
proof, so the refusal is shown to be the INTENDED one and not merely the same fault code."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'portable'))
import author_portable as AP  # noqa: E402

R = Path('/private/tmp/opensip-design-corrections/claude-author-remint.v1')


def diff(a, b, path='proof'):
    out = []
    if type(a) is not type(b):
        return [(path, 'TYPE', type(a).__name__, type(b).__name__)]
    if isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a:
                out.append((path + '.' + k, 'ONLY-RECOMPUTED', None, b[k]))
            elif k not in b:
                out.append((path + '.' + k, 'ONLY-CLAIMED', a[k], None))
            else:
                out.extend(diff(a[k], b[k], path + '.' + k))
    elif isinstance(a, list):
        if len(a) != len(b):
            out.append((path, 'LEN', len(a), len(b)))
        for i, (x, y) in enumerate(zip(a, b)):
            out.extend(diff(x, y, path + '[' + str(i) + ']'))
    elif a != b:
        out.append((path, 'VALUE', a, b))
    return out


def main():
    controls = Path(sys.argv[1]).resolve()
    source = Path(sys.argv[2]).resolve()
    package = Path(sys.argv[3]).resolve()
    outfile = sys.argv[4]
    F = AP.foundation(source)
    CK = AP.transport(package, 'chk')
    M = AP.load_module('owner', F / 'identity-model.v3.py')
    RP = AP.load_module('replay', F / 'evaluator_replay_model.v3.py')

    rows = []
    for c in json.loads((controls / 'claims.json').read_text()):
        raw = (controls / c['path']).read_bytes()
        objects, blobs = CK.decode_store(raw, M, [])
        run = objects[c['runId']][1]
        rid, owner = M.open_run_closure(run, objects, blobs)
        seal = objects[run['evaluationSealId']][1]
        claimed = objects[seal['proofBundleId']][1]
        res = RP.derive(run['planId'], seal['executionPlanId'], seal['evaluatorClosure'],
                        claimed['evaluationInputRefs'], objects, blobs, owner)
        d = diff(claimed, res['proof'])
        sel = sorted({s.split('[')[0] for s, *_ in d})
        rows.append({'name': c['name'], 'runId': c['runId'],
                     'structuralOpenRunClosure': 'ADMIT' if rid == c['runId'] else 'REFUSE',
                     'differingSelectorCount': len(d),
                     'differingSelectorRoots': sel,
                     'samples': [{'selector': s, 'kind': k,
                                  'claimed': json.dumps(x)[:120],
                                  'recomputed': json.dumps(y)[:120]} for s, k, x, y in d[:6]]})
        print('==', c['name'])
        print('   structural open_run_closure:', rows[-1]['structuralOpenRunClosure'])
        print('   differing selectors:', len(d), '->', sel)
        for s, k, x, y in d[:4]:
            print('      %-46s %-16s claimed=%s recomputed=%s'
                  % (s, k, json.dumps(x)[:48], json.dumps(y)[:48]))
    json.dump({'standing': 'Claimed-vs-recomputed proof diff for the reminted negative controls.',
               'controls': str(controls), 'rows': rows}, open(outfile, 'w'), indent=1)


if __name__ == '__main__':
    main()
