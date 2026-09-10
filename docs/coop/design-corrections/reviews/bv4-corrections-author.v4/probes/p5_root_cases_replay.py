"""p5 - replay of ROOT's 17 pre-Plan boundary cases against the corrected bytes.

The case list, ids and expectations are taken verbatim from root's own probe
/tmp/opensip-design-corrections/bv4-v4-checkpoint2-preflight.v1/probe.py
(sha256 ae9fc7ae5394edac0a42e89120704c37c9c6d962172f69048dbd3be8b21d10c5), which reported 12 hold and 5
fail on the checkpoint-2 bytes. That probe binds itself to a checkpoint's changedFiles hashes and
therefore refuses to run on moved source; this replay exists so the same 17 cases can be reported here
without editing root's file or its retained failing report, both of which are preserved untouched.

Reference-model probe: synthetic requests and schema-admitted envelopes. No actual host, renderer,
invocation execution or retained Run closure. The raw-retained-schema case demonstrates schema
behaviour only. No product qualification.

Usage: p5_root_cases_replay.py <root-of-a-source-copy>
"""
import importlib.util, json, sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
DC = ROOT / 'docs/coop/design-corrections'
spec_ = importlib.util.spec_from_file_location('native_p5', DC / 'native/native_evidence_model.v2.py')
N = importlib.util.module_from_spec(spec_)
spec_.loader.exec_module(N)
W = N.IM.workflow_admission()

explicit = lambda n: {'schemaVersion': 2, 'policyPackIds': [], 'parameters': [],
                      'requestedCapabilities': [
                          {'capabilityId': 'inventory', 'languageMode': 'ts-tsconfig',
                           'workspaceRoot': 'apps/u%04d' % i, 'required': True} for i in range(n)]}
units = lambda n: [{'rootPath': 'apps/u%03d' % i, 'languageMode': 'ts-tsconfig',
                    'languageFamily': 'tsjs'} for i in range(n)]
results = []


def run(name, fn, expected):
    try:
        fn()
        actual, detail = 'ADMIT', None
    except N.ScopeRefusal as exc:
        actual = 'ScopeRefusal'
        t = N.scope_refusal_termination(exc)
        env = {'schemaFamily': 'opensip.product.envelope', 'schemaMajor': 2, 'kind': 'failure',
               'requestId': 'req1_' + 'c' * 32, 'termination': t, 'exitCode': W.EXIT[t['class']],
               'errors': [t['domainDetail']]}
        W.validate_import_record('workflows/schemas/common.schema.json', '#/$defs/StepTermination', t)
        W.validate_import_record('workflows/schemas/command-envelope.schema.json', '', env)
        detail = {'observed': exc.subject, 'termination': t, 'failureEnvelopeSchema': 'ADMIT'}
    except Exception as exc:
        actual = type(exc).__name__
        detail = {'messagePrefix': str(exc)[:180], 'messageScalars': len(str(exc))}
    results.append({'id': name, 'expected': expected, 'actual': actual,
                    'holds': actual == expected, 'evidence': detail})


for n in (0, 1, 1024):
    run('complete-explicit-%d' % n, lambda n=n: N.admit_analysis_spec(explicit(n)), 'ADMIT')
run('complete-explicit-1025', lambda: N.admit_analysis_spec(explicit(1025)), 'ScopeRefusal')
for n in (1, 93):
    run('default-ts-%d' % n, lambda n=n: N.default_capability_selection(units(n), []), 'ADMIT')
run('default-ts-94', lambda: N.default_capability_selection(units(94), []), 'ScopeRefusal')
run('raw-retained-schema-1025-is-still-schema-validation',
    lambda: N.validate_foundation('analysis-spec', explicit(1025)), 'ValidationError')

malformed = {}
s = explicit(1); del s['requestedCapabilities']; malformed['missing-requested-capabilities'] = s
for label, value in [('null', None), ('boolean', True), ('integer', 7), ('short-string', 'bad'),
                     ('oversized-string', 'x' * 1025), ('object', {})]:
    s = explicit(1); s['requestedCapabilities'] = value; malformed['wrong-array-type-' + label] = s
s = explicit(1); del s['schemaVersion']; malformed['missing-schema-version'] = s
s = explicit(1); s['unexpected'] = True; malformed['unknown-property'] = s
snapshot = json.loads(json.dumps(malformed))
for label, s in malformed.items():
    run(label, lambda s=s: N.admit_analysis_spec(s), 'ValidationError')

print(json.dumps({'sourceRoot': str(ROOT), 'caseListFrom': 'root probe ae9fc7ae5394edac0a42e89120704c37c9c6d962172f69048dbd3be8b21d10c5',
                  'cases': len(results), 'hold': sum(r['holds'] for r in results),
                  'fail': sum(not r['holds'] for r in results),
                  'allHold': all(r['holds'] for r in results),
                  'noMalformedInputWasCoercedOrRepaired': malformed == snapshot,
                  'results': results}, indent=2))
