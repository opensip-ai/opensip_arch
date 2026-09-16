"""PROBE K2 — refined. Distinguish an unreferenced retained object (lawfully ignorable)
from a genuinely enforced closure-kind field, and test at close_run, not only at the
structural owner primitive."""
import copy, importlib.util, json, os, sys, inspect

DC = '/tmp/opensip-design-corrections/candidate-subject.v26/docs/coop/design-corrections'
sys.path.insert(0, os.path.join(DC, 'foundation'))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


S = load('sf3', os.path.join(DC, 'foundation/evaluator_semantic_fixture.v3.py'))
RP = load('csr3', os.path.join(DC, 'foundation/check-semantic-replay.v3.py'))
M = RP.M
R = {}


def rec(k, v):
    R[k] = v
    print('%-58s %s' % (k, v))


atom = {"op": "none", "relation": "references", "minResolution": "resolved-binding",
        "endpoint": "target", "filters": []}
g = S.build_ts_semantic_graph(atom=atom, has_declares=False, has_references_fact=True,
                              second_partition=True, references_resolved=False,
                              incoming_search=True, incoming_complete=False,
                              target_sidecar=True, second_universe=True)
run, objects, blobs, actual = RP.close_positive(g)

blob = json.dumps({k: v[1] for k, v in objects.items()}, default=str) + json.dumps(run)
closures = {k: v[1] for k, v in objects.items() if v[0] == 'closure'}
ref = {cid: blob.count(cid) - 1 for cid in closures}   # minus its own object key
rec('closures_and_reference_counts', {closures[c]['kind']: n for c, n in ref.items()})

KINDS = ['provider', 'evaluator', 'detector', 'toolchain', 'stdlib', 'rust-dev-llvm', 'grammar', 'adapter']
out = {}
for cid, desc in closures.items():
    orig = desc.get('kind')
    other = next(k for k in KINDS if k != orig)
    d2 = copy.deepcopy(desc)
    d2['kind'] = other
    new = M.identifier('closure', d2)
    o2 = {k: (dom, copy.deepcopy(dsc)) for k, (dom, dsc) in objects.items()}
    o2[new] = ('closure', d2)
    del o2[cid]

    def rw(x):
        if isinstance(x, str):
            return new if x == cid else x
        if isinstance(x, list):
            return [rw(i) for i in x]
        if isinstance(x, dict):
            return {k: rw(v) for k, v in x.items()}
        return x
    o3 = {k: (dom, rw(dsc)) for k, (dom, dsc) in o2.items()}
    r3 = rw(copy.deepcopy(run))
    b3 = dict(blobs)
    try:
        M.open_run_closure(r3, o3, b3)
        struct = 'ADMIT'
    except Exception as exc:
        struct = 'REFUSE:' + str(exc)[:42]
    try:
        M.close_run(r3, o3, b3)
        full = 'ADMIT'
    except Exception as exc:
        full = 'REFUSE:' + str(exc)[:42]
    out['%s->%s (refs=%d)' % (orig, other, ref[cid])] = {'structural': struct, 'completeReplay': full}

R['kind_swap'] = out
for k in sorted(out):
    print('   %-36s structural=%-24s replay=%s' % (k, out[k]['structural'], out[k]['completeReplay']))

src = inspect.getsource(M.admit_cache_entry)
R['admit_cache_entry_source'] = src
rec('cache_admission_calls_close_run', 'close_run' in src)
rec('cache_admission_length', len(src))
print('\n--- admit_cache_entry ---')
print(src[:2400])

json.dump({k: v for k, v in R.items() if k != 'admit_cache_entry_source'},
          open('/tmp/opensip-design-corrections/claude-independent-design.v26/receipts/probeK2.json', 'w'), indent=1)
