"""Compare the conversion before/after and challenge its newly pinned exact value.
No product execution; mutation controls affect in-memory reference inputs only.
"""
from pathlib import Path
import copy
import hashlib
import importlib.util
import json

B = Path('/tmp/opensip-design-corrections')
O = B / 'root-source45-correction.v1'
OLD = B / 'candidate-subject.v44'
NEW = B / 'source44-closed-world-successor.v1/source'
NAT = 'docs/coop/design-corrections/native/'


def load(name, p):
    s = importlib.util.spec_from_file_location(name, p)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


checker = load('closed_world_successor_checker', NEW / NAT / 'check_native_evidence.v2.py')
before = load('closed_world_before', OLD / NAT / 'native_evidence_model.v2.py')
after = load('closed_world_after', NEW / NAT / 'native_evidence_model.v2.py')
cases = json.loads((NEW / NAT / 'native-cases.v2.json').read_bytes())
record = json.loads((O / 'correction.json').read_bytes())
value = record['closedWorld']
assert before.closed_world_v2(None, {'source': 'none', 'state': 'none'}, [], 'unknown') == value
selected = [c for c in cases['cases'] if c['id'] in record['strengthenedCases']]
assert len(selected) == 2
rows = []
for c in selected:
    a = checker.resolve(c['steps'][0]['args'], {'fixtures': cases['fixtures']})
    old = before.provider_startup_exchange(**copy.deepcopy(a))
    new = after.provider_startup_exchange(**copy.deepcopy(a))
    assert old == new
    e = [x['payload']['entry']['closedWorld'] for s in new['hostConversion']['stages'] for x in s['coverage']]
    assert e and all(x == value for x in e)
    result = checker.run_case(c, after, cases['fixtures'])
    assert result['passed'], result
    rows.append({'case': c['id'], 'kind': 'positive-before-after', 'passed': True,
                 'sameCompleteReferenceResult': True, 'entriesPinned': len(e),
                 'resultBytesSha256': hashlib.sha256(json.dumps(new, sort_keys=True, separators=(',', ':')).encode()).hexdigest()})

alternatives = json.loads((B / 'consumer-b.v24-source44.v1/output/traces/startup-vectors.json').read_bytes())['conversion']['candidates']
law = after.STARTUP.LAW['preAnalyzeUnavailable']
for name, alternate in alternatives.items():
    assert alternate != value
    law['hostConversionClosedWorld'] = copy.deepcopy(alternate)
    for c in selected:
        r = checker.run_case(c, after, cases['fixtures'])
        assert not r['passed'], (name, r)
        rows.append({'case': name + ':' + c['id'], 'kind': 'in-memory-law-mutation',
                     'passed': True, 'observed': 'REFUSED-BY-CASE', 'faults': r['faults']})
law['hostConversionClosedWorld'] = copy.deepcopy(value)
assert all(checker.run_case(c, after, cases['fixtures'])['passed'] for c in selected)
out = O / 'focused-verification.json'
assert not out.exists()
out.write_text(json.dumps({'standing': 'Actual reference before/after comparison and mutation controls; not full Run, provider, process or product qualification.',
                          'source44ModelSha256': hashlib.sha256((OLD / NAT / 'native_evidence_model.v2.py').read_bytes()).hexdigest(),
                          'source45ModelSha256': hashlib.sha256((NEW / NAT / 'native_evidence_model.v2.py').read_bytes()).hexdigest(),
                          'allPassed': True, 'positiveCases': 2, 'negativeControls': 8, 'rows': rows}, indent=2) + '\n')
print(json.dumps({'allPassed': True, 'positiveCases': 2, 'negativeControls': 8}))
