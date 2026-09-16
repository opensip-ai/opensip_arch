"""Discriminate the proposal: the same boundaries over the EDITED copy, compared with BASELINE.

Narrow only: the shared boundary probe, the exact new control lines replicated, the termination vectors,
schema metaschema validity, the array-order law for the two edited documents, and every termination-shaped
fixture object whose admission changes between baseline and edited. No group or global suite is run.
"""
import importlib.util, json
from pathlib import Path
from jsonschema import Draft202012Validator

HERE = Path('/tmp/opensip-design-corrections/claude-source37-termination-boundary-assessment.v1/probes')
spec = importlib.util.spec_from_file_location('boundaries', HERE / 'boundaries.py')
B = importlib.util.module_from_spec(spec)
spec.loader.exec_module(B)

edited = B.run('edited', 'p03-edited-boundaries.json')
baseline = json.loads((HERE / 'p01-baseline-boundaries.json').read_text())
mb, me = B.modules('baseline'), B.modules('edited')
gates = {}

# 1. Every retained-law-illegal case refuses at every schema boundary; every lawful control still admits.
s = edited['summary']
gates['required-illegal-refused-everywhere'] = all(not v['admittedAt'] for v in s['illegalAdmittedAt'].values() if v['required'])
gates['lawful-controls-admitted-everywhere'] = not s['lawfulRefusedAt']
gates['existing-refusals-still-refuse'] = not s['existingRefusalAdmittedAt']
advisory_only = {k: v for k, v in s['illegalAdmittedAt'].items() if not v['required']}

# 2. Producers: identical emissions before and after, and none illegal.
def emissions(rec):
    return [(r['producer'], r['key'], r['outcome'], json.dumps(r.get('termination'), sort_keys=True)) for r in rec['producers']['rows']]
gates['producer-emissions-identical'] = emissions(edited) == emissions(baseline)
gates['producer-emissions-lawful'] = all(c['emittedRequiredIllegal'] == 0 for c in edited['producers']['counts'].values())

# 3. Replicated new control lines (check_workflows) and the termination/envelope vectors, narrow.
cases = json.loads((me.dc / 'workflows/workflow-cases.v1.json').read_text())
schema = json.loads((me.dc / 'workflows/schemas/common.schema.json').read_text())
operational = next(b['then'] for b in schema['$defs']['StepTermination']['allOf']
                   if b['if'].get('properties', {}).get('class', {}).get('const') == 'operational-failed')
gates['control.fault-pairs-equal-host-fault-map'] = (
    [(r['properties']['faultCause']['const'], r['properties']['errorCode']['const']) for r in operational['anyOf']]
    == list(me.W.FAULT_TO_ERROR.items()))
constants = cases['constants']


def sub(o):
    if isinstance(o, str) and o.startswith('$') and o[1:] in constants:
        return constants[o[1:]]
    if isinstance(o, dict):
        return {k: sub(v) for k, v in o.items()}
    if isinstance(o, list):
        return [sub(v) for v in o]
    return o


def admits(m, t):
    return B.outcome(lambda: m.W.validate_import_record('workflows/schemas/common.schema.json', '#/$defs/StepTermination', sub(t)))['observed'] == 'ADMIT'


vectors = {'accept': [admits(me, t) for t in cases['terminationVectors']['accept']],
           'reject': [not admits(me, t) for t in cases['terminationVectors']['reject']]}
gates['termination-vectors'] = all(vectors['accept']) and all(vectors['reject'])
baseline_new_rejects = [admits(mb, t) for t in cases['terminationVectors']['reject'][12:]]
gates['new-reject-vectors-were-admitted-by-baseline'] = len(baseline_new_rejects) == 12 and all(baseline_new_rejects)
envelopes = {'accept': [], 'reject': []}
for side in ('accept', 'reject'):
    for e in cases['envelopeVectors'][side]:
        try:
            value = sub(e)
        except Exception as exc:
            envelopes[side].append('SUB-ERROR ' + type(exc).__name__)
            continue
        base = B.outcome(lambda: mb.W.validate_import_record('workflows/schemas/command-envelope.schema.json', '', value))['observed']
        new = B.outcome(lambda: me.W.validate_import_record('workflows/schemas/command-envelope.schema.json', '', value))['observed']
        envelopes[side].append(base + '->' + new)
gates['envelope-vectors-unchanged'] = all(x.split('->')[0] == x.split('->')[1] for side in envelopes.values() for x in side if '->' in x)

# 4. Metaschema and array-order law for the edited documents.
for rel in ('workflows/schemas/common.schema.json', 'workflows/schemas/evaluator3/common.schema.json'):
    doc = json.loads((me.dc / rel).read_text())
    Draft202012Validator.check_schema(doc)
    arrays = []

    def walk(node, path=''):
        if isinstance(node, dict):
            t = node.get('type')
            if t == 'array' or isinstance(t, list) and 'array' in t:
                arrays.append((path, 'x-opensip-order' in node))
            for k, v in node.items():
                walk(v, path + '/' + k)
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, path + '/' + str(i))

    walk(doc)
    gates['array-order-laws-declared:' + rel] = all(ok for _, ok in arrays)

# 5. Positive fixture consequence: any termination-shaped object in the copy whose admission changes.
props = set(json.loads((me.dc / 'workflows/schemas/evaluator3/common.schema.json').read_text())['$defs']['StepTermination']['properties'])
changed, examined = [], 0
for path in sorted(mb.dc.rglob('*.json')):
    rel = path.relative_to(mb.dc)
    if str(rel) == 'workflows/workflow-cases.v1.json':
        pass
    try:
        doc = json.loads(path.read_text())
    except Exception:
        continue

    def walk(o, ptr):
        global examined
        if isinstance(o, dict):
            if isinstance(o.get('class'), str) and o['class'] in mb.W.EXIT and set(o) <= props:
                examined += 1
                value = sub(o)
                row = {}
                for label, m in (('baseline', mb), ('edited', me)):
                    row[label + '.workflows'] = B.outcome(lambda: m.W.validate_import_record('workflows/schemas/common.schema.json', '#/$defs/StepTermination', value))['observed']
                    row[label + '.evaluator3'] = B.outcome(lambda: m.P.validate_profile(B.E3 + 'common:3#/$defs/StepTermination', value))['observed']
                if row['baseline.workflows'] != row['edited.workflows'] or row['baseline.evaluator3'] != row['edited.evaluator3']:
                    changed.append({'file': str(rel), 'pointer': ptr, 'value': o, 'outcomes': row})
            for k, v in o.items():
                walk(v, ptr + '/' + str(k))
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, ptr + '/' + str(i))

    walk(doc, '')
gates['no-baseline-fixture-changes-admission'] = not changed

record = {'gates': gates, 'advisoryStillAdmitted': advisory_only, 'terminationVectors': vectors,
          'baselineAdmittedNewRejectVectors': baseline_new_rejects, 'envelopeVectors': envelopes,
          'fixtureObjectsExamined': examined, 'fixtureAdmissionChanges': changed,
          'editedProducerCounts': edited['producers']['counts'],
          'editedDigestConsequence': edited['digestConsequence']['commonSchemaSha256']}
(HERE / 'p03-edited-discrimination.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record, indent=2))
if not all(gates.values()):
    raise SystemExit(1)
