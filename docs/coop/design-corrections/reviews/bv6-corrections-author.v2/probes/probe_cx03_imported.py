"""Develop CX-BV6-03 controls: the imported plane's producer, the plane separation, and the
safety invariant that an imported requirement never authorizes an unsafe repair."""
import importlib.util, json, sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
sp = importlib.util.spec_from_file_location('W', ROOT / 'docs/coop/design-corrections/workflows/workflows_model.v1.py')
W = importlib.util.module_from_spec(sp); sp.loader.exec_module(W)
rows = []

def req(relation='runtime-observation', targets=('src/a.ts',), **kw):
    return {'relation': relation, 'minResolution': 'observed', 'completeness': 'complete',
            'targets': list(targets), **kw}

FULL = {'available': True, 'consumable': True, 'windowSatisfiesRequirement': True,
        'observability': {'src/a.ts': 'observed-hit'},
        'observationWindow': {'startUtc': '2026-01-01T00:00:00Z', 'endUtc': '2026-01-02T00:00:00Z'},
        'observedPopulation': 'test-suite'}

def out(label, evidence, expect, **kw):
    r = W.imported_requirement_outcome(req(), evidence, **kw)
    rows.append({'case': label, 'expect': expect, 'actual': r.get('deficiency') or 'SATISFIED',
                 'satisfied': r['satisfied'], 'disclosures': r['disclosures']})

out('satisfied-observed-hit', FULL, 'SATISFIED')
out('satisfied-observable-unhit', {**FULL, 'observability': {'src/a.ts': 'observable-unhit'}}, 'SATISFIED')
out('kind-unavailable-required', {**FULL, 'available': False}, 'evidence-kind-unavailable')
out('kind-unavailable-optional', {**FULL, 'available': False}, 'SATISFIED', required=False)
out('unmapped-only-import', {**FULL, 'consumable': False}, 'import-unmapped-only')
out('target-unobservable', {**FULL, 'observability': {'src/a.ts': 'unobservable'}}, 'subject-not-observable')
out('target-unmapped', {**FULL, 'observability': {'src/a.ts': 'unmapped'}}, 'subject-not-observable')
out('window-insufficient', {**FULL, 'windowSatisfiesRequirement': False}, 'observation-window-insufficient')
out('no-observation-for-target', {**FULL, 'observability': {}}, 'import-absent-for-requirement')
out('precedence-unobservable-beats-window',
    {**FULL, 'observability': {'src/a.ts': 'unobservable'}, 'windowSatisfiesRequirement': False},
    'subject-not-observable')

# plane separation, both directions
def refusal(fn):
    try:
        return {'result': 'ADMIT', 'return': fn()}
    except Exception as e:
        return {'result': 'REFUSE', 'detail': getattr(e, 'remedy', str(e))[:120]}

rows.append({'case': 'native-relation-refused-by-imported-producer',
             'expect': 'REFUSE',
             **refusal(lambda: W.imported_requirement_outcome(req(relation='references'), FULL))})
rows.append({'case': 'imported-requirement-carrying-a-native-outcome',
             'expect': 'REFUSE',
             **refusal(lambda: W.admit_evidence_requirement(
                 req(satisfied=False, deficiency='resolution-incomplete')))})
rows.append({'case': 'native-requirement-carrying-an-imported-outcome',
             'expect': 'REFUSE',
             **refusal(lambda: W.admit_evidence_requirement(
                 {'relation': 'references', 'minResolution': 'resolved-binding',
                  'completeness': 'complete', 'satisfied': False,
                  'deficiency': 'import-unmapped-only'}))})
rows.append({'case': 'imported-requirement-carrying-its-own-outcome',
             'expect': 'ADMIT',
             **refusal(lambda: W.admit_evidence_requirement(
                 req(satisfied=False, deficiency='import-unmapped-only')))})

print(json.dumps({'sourceRoot': str(ROOT), 'cases': rows}, indent=1))
