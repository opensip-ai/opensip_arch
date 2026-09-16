"""Read-only probe: can the consumer24 M3 real-Run harness close a complete Run whose membership carries a discovered TS/JS
unit, and does a digest-consistent reminted unitKind still close (pre-fix) or refuse (post-fix)?

usage: python -I -B probe_real_run_tsjs.py LABEL
Loads the capture's consumer24 checker as a module (its sections are not run) and reuses its maintained harness pattern:
the membership is built by the fixture's native copy and mutated before it is hashed into membershipDigest, then
EI.full_run closes the Run. Writes receipts/probes/LABEL.json only.
"""
import copy, importlib.util, json, sys, traceback
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-tsjs-unitkind-author.v1')
FOUND = RT / 'work/source/docs/coop/design-corrections/foundation'
label = sys.argv[1]
spec = importlib.util.spec_from_file_location('probe_c24', FOUND / 'check-native-consumer24-corrections.v1.py')
C24 = importlib.util.module_from_spec(spec)
sys.modules['probe_c24'] = C24
spec.loader.exec_module(C24)
EI, _ = C24.owners()
ENUM = C24.load('probe_enum', FOUND / 'enumeration_model.v1.py')
NV = ENUM.NV
real_fixture_helpers = EI.F.fixture_helpers
helpers = real_fixture_helpers()
original = helpers.N.assign_membership
marker = 'd' * 64
results = []


def run_with(units, mutate):
    def patched(u, files, boundaries=None):
        membership = original([dict(x) for x in units], list(files))
        mutate(membership)
        return membership
    helpers.N.assign_membership = patched
    EI.F.fixture_helpers = lambda: helpers
    try:
        graph = EI.F.build_file_inputs()
    finally:
        EI.F.fixture_helpers = real_fixture_helpers
        helpers.N.assign_membership = original
    try:
        got = C24.refusal_any(lambda: EI.full_run(graph))
    except Exception as exc:
        got = 'EXCEPTION ' + type(exc).__name__ + ': ' + str(exc)[:300]
    return graph, got


for name, markers in (('ts-tsconfig', {'tsconfig.json': {'sha256': marker}}),
                      ('js-allowjs-tsconfig', {'tsconfig.json': {'sha256': marker, 'allowJs': True}}),
                      ('js-synthesized', {'package.json': {'sha256': marker}})):
    units = NV.discover_units(markers)['units']
    graph, got = run_with(units, lambda m: None)
    results.append({'case': name + '-canonical', 'closes': got is None, 'refusal': got,
                    'units': graph['membership']['units'] if isinstance(graph, dict) and 'membership' in graph else None})
    wrong = 'js-program' if units[0]['unitKind'] == 'ts-program' else 'ts-program'
    graph, got = run_with(units, lambda m, w=wrong: m['units'][0].update(unitKind=w))
    results.append({'case': name + '-reminted-' + wrong, 'closes': got is None, 'refusal': got})
out = RT / 'receipts/probes'
out.mkdir(parents=True, exist_ok=True)
(out / (label + '.json')).write_text(json.dumps(results, indent=1, default=str) + '\n')
print(json.dumps(results, indent=1, default=str)[:6000])
