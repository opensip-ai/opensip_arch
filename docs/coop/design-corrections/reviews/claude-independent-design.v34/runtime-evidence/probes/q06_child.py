"""Q06 child — one fresh interpreter. Builds the E2 multi-scope fixture with maps in SET iteration order
(hash-seeded per process because -I ignores PYTHONHASHSEED) and prints the atom result digest.
argv[1] = '34' or '33' selects which atom_model evaluates; the fixture builders are always frozen34's."""
import copy, hashlib, importlib.util, json, sys

PROBES = '/tmp/opensip-design-corrections/claude-independent-design.v34/probes'
sys.path.insert(0, PROBES)
F34 = '/tmp/opensip-design-corrections/candidate-subject.v34/docs/coop/design-corrections/foundation'
F33 = '/tmp/opensip-design-corrections/candidate-subject.v33/docs/coop/design-corrections/foundation'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


K = load('chk34', F34 + '/check-atoms.v1.py')
AMX = K.AM if sys.argv[1] == '34' else load('am33', F33 + '/atom_model.v1.py')
from q05_fixtures import e2_inputs  # noqa: E402

inputs = e2_inputs(K, AMX, hash_order=True)
outs = {}
for ep in ('source', 'target'):
    atom = {'op': 'all-covered', 'relation': 'reachability', 'minResolution': 'from-resolved-calls',
            'endpoint': ep, 'filters': []}
    r = AMX.evaluate_atom(copy.deepcopy(atom), copy.deepcopy(K.F_SUBJ), copy.deepcopy(inputs))
    outs[ep] = {'value': r['value'], 'causes': r['causes'], 'coverageIds': r['coverageIds']}
print(json.dumps({'model': sys.argv[1], 'coverageInsertionOrder': list(inputs['coverages']),
                  'digest': hashlib.sha256(json.dumps(outs, sort_keys=True).encode()).hexdigest(),
                  'carriers': [c.get('nativeCause') for ep in outs for c in outs[ep]['causes']
                               if c['code'] == 'coverage-unknown']}))
