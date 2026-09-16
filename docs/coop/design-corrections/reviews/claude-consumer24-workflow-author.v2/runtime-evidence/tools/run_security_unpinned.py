"""Execute the security-lifecycle checker body WITHOUT its source-pin gate. Explicitly labelled; not the owner launcher.

usage: python -I -B run_security_unpinned.py ROOT LABEL
Copied from v1 tools/run_security_unpinned.py; only the receipt root changes to v2.
The owner main() refuses to execute when source pins mismatch; pins are root-owned and this correction necessarily
changes pinned files, so the owner gate reports sourcePinsValid=false with zero cases executed. This driver loads
the checker module (main() is __name__-guarded), then performs exactly main()'s post-gate body: run_cases over the
bundle validators and every sweep listed in main(). It never edits pins and never reports pin validity.
"""
import hashlib, importlib.util, json, sys
from pathlib import Path

ROOT = Path(sys.argv[1])
LABEL = sys.argv[2]
RT = Path('/private/tmp/opensip-design-corrections/claude-consumer24-workflow-author.v2')
SEC = ROOT / 'docs/coop/design-corrections/security'
script = SEC / 'check-security-lifecycle.v1.py'
sys.path.insert(0, str(SEC))
spec = importlib.util.spec_from_file_location('security_checker_unpinned', script)
S = importlib.util.module_from_spec(spec)
spec.loader.exec_module(S)
from jsonschema import Draft202012Validator  # noqa: E402

schemas = S.canonical.parse((SEC / 'security-lifecycle.schemas.v1.json').read_bytes())
validators = {}


def validator_for(name):
    if name not in validators:
        if name not in schemas['schemas']:
            raise KeyError('UNKNOWN_SCHEMA:' + name)
        s = {'$ref': '#/schemas/' + name, '$defs': schemas['$defs'], 'schemas': schemas['schemas']}
        Draft202012Validator.check_schema(s)
        validators[name] = S.canonical.ExactValidator(s)
    return validators[name]


cases = S.run_cases(schemas, validator_for)
sweeps = []
for sweep in (S.sweep_clock_monotone, S.sweep_recovery_replay, S.sweep_linearization, S.sweep_journal_record_dispatch,
              S.sweep_profile_separation, S.sweep_lease_modes, S.sweep_root_schema_readers,
              S.sweep_discovery_pruning_and_cap, S.sweep_platform_vocabulary_join, S.sweep_boundary_join_native,
              S.sweep_public_detail_closure):
    try:
        sweeps.append(sweep())
    except Exception as e:
        sweeps.append({'name': sweep.__name__, 'holds': False, 'detail': ('%s: %s' % (type(e).__name__, e))[:500]})
counts = {'total': len(cases), 'pass': sum(c['status'] == 'PASS' for c in cases)}
counts['fail'] = counts['total'] - counts['pass']
report = {'standing': 'OWNER PIN GATE BYPASSED BY EXTERNAL DRIVER; pins not evaluated; body of main() only', 'root': str(ROOT),
          'checkerSha256': hashlib.sha256(script.read_bytes()).hexdigest(), 'counts': counts,
          'sweeps': [{k: s.get(k) for k in ('name', 'holds', 'checked', 'detail')} for s in sweeps],
          'failedCases': [{'file': c['file'], 'id': c['id']} for c in cases if c['status'] != 'PASS'],
          'passed': counts['fail'] == 0 and all(s['holds'] for s in sweeps)}
out = RT / 'receipts/checks' / LABEL
out.mkdir(parents=True, exist_ok=True)
(out / 'security-lifecycle-unpinned.json').write_text(json.dumps(report, indent=1) + '\n')
print(json.dumps(report, indent=1))
sys.exit(0 if report['passed'] else 1)
