"""P2 (INVOCATION + CLOSURE probe) for V20-ROOT-4 / DUPLICATE_REQUESTED_CAPABILITY.

Kind, stated explicitly:
  - REACHABILITY leg  : INVOCATION probe. It runs the ACTUAL discovery instrument
    `discover_units` over marker inventories and asks whether its OUTPUT can carry two units
    sharing (rootPath, languageMode) - the exact condition `default_capability_selection`
    refuses. It does not run a product host and proves no product qualification.
  - ROUTE leg         : CLOSURE probe over `public_termination_for` / `failure_envelope_errors`.
  - EQUIVALENCE leg   : INVOCATION probe showing which refusal the SAME rows meet at
    `admit_requested_capabilities`, and what the schema alone would say.

Failed assertions are reported as failures; nothing is swallowed.
"""
import importlib.util, json, sys, traceback
from pathlib import Path

ROOT = Path(sys.argv[1])


def load(name, rel):
    s = importlib.util.spec_from_file_location(name, ROOT / rel)
    m = importlib.util.module_from_spec(s)
    sys.modules[name] = m
    s.loader.exec_module(m)
    return m


N = load('native_evidence_model_v2', 'native/native_evidence_model.v2.py')

out = {'kind': 'invocation (discovery) + closure (route) + invocation (equivalence)'}


def attempt(fn):
    try:
        return {'outcome': 'returned', 'value': fn()}
    except Exception as exc:
        return {'outcome': 'raised', 'type': type(exc).__name__, 'str': str(exc)[:400]}


# ---- ROUTE leg -------------------------------------------------------------------------
out['route'] = {
    'public_termination_for("DUPLICATE_REQUESTED_CAPABILITY")':
        attempt(lambda: N.public_termination_for('DUPLICATE_REQUESTED_CAPABILITY')),
    'public_termination_for(...,host-generated-internal-layer)':
        attempt(lambda: N.public_termination_for('DUPLICATE_REQUESTED_CAPABILITY',
                                                 'host-generated-internal-layer')),
    'failure_envelope_errors("DUPLICATE_REQUESTED_CAPABILITY")':
        attempt(lambda: N.failure_envelope_errors('DUPLICATE_REQUESTED_CAPABILITY')),
    'inRouteRegistryKeys': 'DUPLICATE_REQUESTED_CAPABILITY' in N.PUBLIC_ROUTE_REGISTRY['keys'],
    'registeredTupleKeyPresent':
        'native.requested-capability-duplicate-ownership-tuple' in N.PUBLIC_ROUTE_REGISTRY['keys'],
}
_TUPLE = 'native.requested-capability-duplicate-ownership-tuple'
if out['route']['registeredTupleKeyPresent']:
    row = N.PUBLIC_ROUTE_REGISTRY['keys'][_TUPLE]
    out['route']['tupleKeyRow'] = {'originDependent': row['originDependent'],
                                   'possibleOrigins': row['possibleOrigins']}
    out['route']['tupleKeyTerminations'] = {
        o: attempt(lambda o=o: N.public_termination_for(_TUPLE + ':inventory:ts-tsconfig:.', o))
        for o in row['possibleOrigins']}

# ---- REACHABILITY leg: the ACTUAL discovery instrument ---------------------------------
MARKERS = {
    # one directory holding BOTH a Cargo.toml and a package.json -> two co-located units
    'Cargo.toml': {'sha256': 'a' * 64},
    'package.json': {'sha256': 'b' * 64},
    # a directory with several tsjs markers at once -> marker precedence must pick ONE
    'apps/x/tsconfig.json': {'sha256': 'c' * 64},
    'apps/x/jsconfig.json': {'sha256': 'd' * 64},
    'apps/x/package.json': {'sha256': 'e' * 64},
    # a tsconfig with allowJs, whose MODE collides with a jsconfig elsewhere
    'apps/y/tsconfig.json': {'sha256': 'f' * 64, 'allowJs': True},
    'apps/z/jsconfig.json': {'sha256': '0' * 64},
}
disc = attempt(lambda: N.discover_units(MARKERS))
out['discovery'] = {'input': sorted(MARKERS), 'result': disc['outcome']}
if disc['outcome'] == 'returned':
    units = disc['value']['units']
    keys = [(u['rootPath'], u['languageMode']) for u in units]
    out['discovery']['units'] = [{'rootPath': u['rootPath'], 'languageFamily': u['languageFamily'],
                                  'languageMode': u['languageMode']} for u in units]
    out['discovery']['duplicateRootModePairs'] = sorted({k for k in keys if keys.count(k) > 1})
    out['discovery']['discoveryOutputHasDuplicateRootMode'] = len(set(keys)) != len(keys)
    # feed the ACTUAL discovery output straight into the default selection
    reg = sorted(({'capabilityId': c['id'],
                   'languageModes': sorted(m for m in N.CAPABILITY_MATRIX['languageModes']
                                           if (c['id'], m) not in
                                           {(x['capability'], x['mode']) for x in
                                            N.CAPABILITY_MATRIX['cells'] if x['state'] == 'NOT-SELECTED'})}
                  for c in N.CAPABILITY_MATRIX['capabilities']),
                 key=lambda r: r['capabilityId'].encode())
    sel = attempt(lambda: N.default_capability_selection(units, reg))
    out['discovery']['defaultSelectionOnRealDiscoveryOutput'] = (
        {'outcome': sel['outcome'], 'rows': len(sel['value']['analysisSpec']['requestedCapabilities'])}
        if sel['outcome'] == 'returned' else sel)
else:
    out['discovery']['error'] = disc

# ---- EQUIVALENCE leg -------------------------------------------------------------------
_U = {'rootPath': '.', 'languageMode': 'ts-tsconfig', 'languageFamily': 'typescript'}
_REG = sorted(({'capabilityId': c['id'],
                'languageModes': sorted(m for m in N.CAPABILITY_MATRIX['languageModes']
                                        if (c['id'], m) not in
                                        {(x['capability'], x['mode']) for x in
                                         N.CAPABILITY_MATRIX['cells'] if x['state'] == 'NOT-SELECTED'})}
               for c in N.CAPABILITY_MATRIX['capabilities']),
              key=lambda r: r['capabilityId'].encode())
out['handBuiltDuplicateUnits'] = attempt(lambda: N.default_capability_selection([_U, dict(_U)], _REG))

_ROWS = [{'capabilityId': 'inventory', 'languageMode': 'ts-tsconfig', 'workspaceRoot': '.',
          'required': True}]
out['sameRowsAtVocabularyHelper'] = {
    'twoIdenticalRows': attempt(lambda: N.admit_requested_capabilities(_ROWS + [dict(_ROWS[0])])),
    'twoRowsSameTupleDifferentRequired':
        attempt(lambda: N.admit_requested_capabilities(
            _ROWS + [{**_ROWS[0], 'required': False}])),
}
out['sameRowsAtWholeSpecBoundary'] = attempt(
    lambda: N.admit_analysis_spec({'schemaVersion': 2, 'policyPackIds': [], 'parameters': [],
                                   'requestedCapabilities': _ROWS + [dict(_ROWS[0])]}))

print(json.dumps(out, indent=1, default=str))
