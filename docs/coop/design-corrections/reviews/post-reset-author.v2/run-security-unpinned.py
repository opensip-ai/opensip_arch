"""Run the security checker's cases and sweeps WITHOUT the source-pin gate (pins are Codex's and are expected to fail
until the final re-pin). Writes the report to this directory; nothing in the repository is touched."""
import importlib.util, json, sys
from pathlib import Path
HERE = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/security')
OUT = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location('chk', HERE / 'check-security-lifecycle.v1.py'); chk = importlib.util.module_from_spec(spec); spec.loader.exec_module(chk)
from jsonschema import Draft202012Validator
canonical, model = chk.canonical, chk.model
schemas = canonical.parse((HERE / 'security-lifecycle.schemas.v1.json').read_bytes())
validators = {}
def validator_for(name):
    if name not in validators:
        if name not in schemas['schemas']:
            raise KeyError('UNKNOWN_SCHEMA:' + name)
        s = {'$ref': '#/schemas/' + name, '$defs': schemas['$defs'], 'schemas': schemas['schemas']}
        Draft202012Validator.check_schema(s)
        validators[name] = canonical.ExactValidator(s)
    return validators[name]
report = {'standing': 'post-reset author run with the pin gate bypassed (pins are expected to mismatch until Codex re-pins); design evidence only', 'pinGateBypassed': True}
report['cases'] = chk.run_cases(schemas, validator_for)
report['sweeps'] = []
for sweep in (chk.sweep_clock_monotone, chk.sweep_recovery_replay, chk.sweep_linearization, chk.sweep_profile_separation, chk.sweep_lease_modes,
              chk.sweep_root_schema_readers, chk.sweep_discovery_pruning_and_cap, chk.sweep_platform_vocabulary_join, chk.sweep_boundary_join_native):
    try:
        report['sweeps'].append(sweep())
    except Exception as e:
        import traceback
        report['sweeps'].append({'name': sweep.__name__, 'holds': False, 'detail': ('%s: %s' % (type(e).__name__, e))[:800], 'trace': traceback.format_exc()[-1500:]})
counts = {'total': len(report['cases']), 'pass': sum(c['status'] == 'PASS' for c in report['cases'])}
counts['fail'] = counts['total'] - counts['pass']
report['counts'] = counts
report['passed'] = counts['fail'] == 0 and all(s['holds'] for s in report['sweeps'])
report['schemasValidated'] = sorted(validators)
OUT.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({'passed': report['passed'], 'counts': counts, 'sweeps': [(s['name'], s['holds']) for s in report['sweeps']]}))
for c in report['cases']:
    if c['status'] != 'PASS':
        print('FAIL', c['file'], c['id'], json.dumps(c['failures'])[:700], json.dumps(c['schemaErrors'])[:700])
for s in report['sweeps']:
    if not s['holds']:
        print('SWEEP-FAIL', s['name'], s.get('detail'), s.get('trace'))
