"""Measured residuals that this correction does not close (reported as integration needs, not hidden).

usage: python -I -B probe_residuals.py LABEL
R1 S7: a matched baseline subject that becomes unmatched (signature collision) under COMPLETE current enumeration.
R2 M5: parity fields of the other query-class commands have no CommandEnvelope major 3 carrier.
"""
import importlib.util, json, sys
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-consumer24-workflow-author.v1')
DC = RT / 'work/source38-work/docs/coop/design-corrections'
LABEL = sys.argv[1]
sys.path.insert(0, str(DC / 'foundation'))


def load(name, path):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


P = load('resid_proj', DC / 'workflows/workflow_projection_model.v3.py')
RC = load('resid_rc', DC / 'foundation/check-replay.v3.py')
SCOPE_ALL = {'schemaFamily': 'opensip.product.scope', 'schemaMajor': 1, 'include': ['**'], 'exclude': []}
CUSTODY = {'exportedAtUtc': '2026-09-08T00:00:00Z', 'exportedByHostRelease': '1.0.0'}
out = {'label': LABEL, 'standing': 'measured residuals over owner fixtures; not corrected here'}


def host_from_graph(run_id, objects):
    closures, majors, platform = {}, set(), None
    for key, (dom, val) in objects.items():
        if dom != 'closure':
            continue
        closures[key] = {'bytes': 'ok', 'trust': 'admitted', 'protocolMajor': val['protocolMajor'], 'platform': val['platform']}
        majors.add(val['protocolMajor'])
        if val['kind'] == 'evaluator':
            platform = val['platform']
        elif platform is None and val['kind'] == 'detector' and val['platform'] != 'any':
            platform = val['platform']
    return {'closures': closures, 'protocolMajors': sorted(majors), 'platform': platform or 'linux', 'pivotRunId': run_id, 'recipeMajors': [2]}


X1 = {'nativeSubjectId': 'symbol:x1'}
X2 = {'nativeSubjectId': 'symbol:x2', 'signatureTokens': ['function', 'x', '(', 'number', ')']}
X3 = {'nativeSubjectId': 'symbol:x3'}
r1 = {}
for gate in (True, False):
    base = RC.positive(symbol_rows=[X1, X2], scope_document=SCOPE_ALL, gate=gate)
    art = P.adopt_admitted_baseline_v3(*base, CUSTODY)
    cur = RC.positive(symbol_rows=[X1, X2, X3], scope_document=SCOPE_ALL, gate=gate)
    view = P.project_admitted_run_v3(*cur)
    res = P.compare_admitted_v3(baseline_artifact=art, current_run=cur[0], current_objects=cur[1], current_blobs=cur[2],
                                host=host_from_graph(art['descriptor']['runId'], base[1]), profile_name='code-regression')
    d = res['descriptor']
    r1['gate-' + str(gate).lower()] = {
        'currentEnumeration': view['ruleResults'][0]['enumeration']['state'],
        'currentUnmatched': [(o['finding']['subject']['qualifiedName'], o['finding']['correspondence']['reason']) for o in view['occurrences'] if not o['finding']['fingerprint']],
        'entries': [(e['classification'], e.get('indeterminateReason'), e['presence']['E4']) for e in d['entries']],
        'ruleDeficiencies': d['ruleDeficiencies'], 'verdict': d['verdict']}
out['R1-S7-unmatched-after-collision-under-complete-enumeration'] = r1

inv = json.loads((DC / 'workflows/command-inventory.v3.json').read_text())
env = json.loads((DC / 'workflows/schemas/evaluator3/command-envelope.schema.json').read_text())
props = sorted(env['properties'])
r2 = {}
for c in inv['commands']:
    if c['requestClass'] != 'query':
        continue
    r2[c['name']] = {'steps': c['steps'], 'parityFields': c['parityFields'],
                     'fieldsWithoutAnEnvelopeProperty': [f for f in c['parityFields'] if f not in ('termination-class', 'query-response')]}
out['R2-M5-query-class-parity-carriers'] = {'envelopeProperties': props, 'commands': r2}
dest = RT / 'receipts/probes'
dest.mkdir(parents=True, exist_ok=True)
(dest / ('probe-residuals.' + LABEL + '.json')).write_text(json.dumps(out, indent=1, default=str) + '\n')
print(json.dumps(out, indent=1, default=str))
