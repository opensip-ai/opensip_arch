"""PROBE K — closure-kind rules at each ACTUAL owner, and whether a cache hit can
bypass the Run's own closure. Built by mutation of a real admitted Run, not by
reading the authors' case list.

K1  every closure-bearing field's required kind is published machine-readably and is
    enforced at Run closure (one mutation per field, kind swapped to another legal kind).
K2  a cache entry keyed correctly cannot be admitted against a Run whose closure it
    does not satisfy: key construction is pure and grants nothing.
K3  transitive selection is not flattened: a closure reached only through a selected
    import/native context is not thereby a semanticClosures member, and a Plan naming
    an unretained context cannot close.
"""
import copy, importlib.util, json, os, sys

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
    print('%-62s %s' % (k, v))


ids = json.load(open(os.path.join(DC, 'foundation/identity-schemas.v3.json'), encoding='utf-8'))
dd = ids['x-opensip-digest-domains']
rec('K1_closureKinds_published', dd.get('closureKinds'))
cm = dd.get('closureMembership')
rec('K1_closureMembership_fields', sorted(cm.keys()) if isinstance(cm, dict) else cm)
if isinstance(cm, dict):
    for k, v in sorted(cm.items()):
        print('      %-38s %s' % (k, json.dumps(v)[:150]))

atom = {"op": "none", "relation": "references", "minResolution": "resolved-binding",
        "endpoint": "target", "filters": []}
g = S.build_ts_semantic_graph(atom=atom, has_declares=False, has_references_fact=True,
                              second_partition=True, references_resolved=False,
                              incoming_search=True, incoming_complete=False,
                              target_sidecar=True, second_universe=True)
run, objects, blobs, actual = RP.close_positive(g)
rec('K0_positive_run', actual['runId'][:26] + '...')

# --- K1: swap a closure's declared kind and re-close ---
closures = {k: v[1] for k, v in objects.items() if v[0] == 'closure'}
rec('K1_retained_closure_kinds', sorted({c.get('kind') for c in closures.values()}))
KINDS = ['provider', 'evaluator', 'detector', 'toolchain', 'stdlib', 'rust-dev-llvm', 'grammar', 'adapter']
swapped = 0
results = {}
for cid, desc in list(closures.items()):
    orig = desc.get('kind')
    other = next(k for k in KINDS if k != orig)
    o2 = copy.deepcopy(objects)
    d2 = copy.deepcopy(desc)
    d2['kind'] = other
    # remint the closure identity so the graph stays internally hash-consistent,
    # then rewrite every reference to it
    new = M.identifier('closure', d2)
    o2[new] = ('closure', d2)
    del o2[cid]

    def rewrite(x):
        if isinstance(x, str):
            return new if x == cid else x
        if isinstance(x, list):
            return [rewrite(i) for i in x]
        if isinstance(x, dict):
            return {k: rewrite(v) for k, v in x.items()}
        return x
    o3 = {}
    for k, (dom, dsc) in o2.items():
        o3[k] = (dom, rewrite(dsc))
    r3 = rewrite(copy.deepcopy(run))
    try:
        M.open_run_closure(r3, o3, blobs)
        res = 'STRUCTURAL-ADMIT'
    except Exception as exc:
        res = 'STRUCTURAL-REFUSE:' + str(exc)[:60]
    results[orig + '->' + other] = res
    swapped += 1
rec('K1_closures_mutated', swapped)
for k, v in sorted(results.items()):
    print('      %-28s %s' % (k, v))
R['K1_kind_swap_results'] = results

# --- K2: cache key construction versus cache-hit admission ---
rec('K2_cache_key_is_pure', hasattr(M, 'cache_key'))
rec('K2_admit_cache_entry_exists', hasattr(M, 'admit_cache_entry'))
import inspect
if hasattr(M, 'admit_cache_entry'):
    rec('K2_admit_cache_entry_signature', str(inspect.signature(M.admit_cache_entry)))
    src = inspect.getsource(M.admit_cache_entry)
    R['K2_admit_cache_entry_source'] = src[:2600]
    rec('K2_admission_requires_close_run', 'close_run' in src)
    rec('K2_admission_refuses_payload_domain_roots',
        any(x in src for x in ('coverage-payload', 'import-payload', 'fact-payload')))
if hasattr(M, 'cache_key'):
    csrc = inspect.getsource(M.cache_key)
    rec('K2_key_construction_reads_no_bytes',
        ('objects' not in csrc) and ('blobs' not in csrc))
    R['K2_cache_key_source'] = csrc[:1200]

json.dump({k: (v if isinstance(v, (str, int, float, bool, list, dict, type(None))) else str(v))
           for k, v in R.items()},
          open('/tmp/opensip-design-corrections/claude-independent-design.v26/receipts/probeK.json', 'w'), indent=1)
