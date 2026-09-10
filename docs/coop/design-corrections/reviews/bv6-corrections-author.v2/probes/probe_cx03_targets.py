"""Root's imported-target counterexample (root-input/imported-target-draft.v1.json) replayed against
the corrected producer, plus the all-versus-any and per-kind boundaries it asked me to publish."""
import importlib.util, json, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
sp = importlib.util.spec_from_file_location('W', root / 'docs/coop/design-corrections/workflows/workflows_model.v1.py')
W = importlib.util.module_from_spec(sp); sp.loader.exec_module(W)
rows = []
RT = {'available': True, 'consumable': True, 'windowSatisfiesRequirement': True,
      'observationWindow': {'startUtc': '2026-09-01T00:00:00Z', 'endUtc': '2026-09-02T00:00:00Z'},
      'observedPopulation': 'synthetic', 'observability': {'seen': 'observed-hit'}}
def req(rel='runtime-observation', completeness='complete'):
    return {'relation': rel, 'minResolution': 'observed', 'completeness': completeness}
def run(label, r, targets, ev, expect, **kw):
    try:
        out = W.imported_requirement_outcome(r, targets, ev, **kw)
        actual = out.get('deficiency') or ('SATISFIED:' + out.get('satisfiedBy', ''))
    except Exception as e:
        actual = 'REFUSE:' + getattr(e, 'remedy', str(e)).split(':')[0]
    rows.append({'case': label, 'expect': expect, 'actual': actual, 'match': actual == expect})

# ROOT'S EXACT COUNTEREXAMPLE: complete over [seen, missing], only `seen` observed.
run('root-counterexample-complete-with-a-missing-target', req(), ['seen', 'missing'], RT,
    'import-absent-for-requirement')
run('same-inputs-under-partial-acceptable', req(completeness='partial-acceptable'),
    ['seen', 'missing'], RT, 'SATISFIED:bounded-observation')
run('complete-with-every-target-observed', req(), ['seen'], RT, 'SATISFIED:bounded-observation')
run('bounded-negative-observable-unhit-satisfies', req(), ['seen'],
    {**RT, 'observability': {'seen': 'observable-unhit'}}, 'SATISFIED:bounded-observation')
run('optional-absence-is-satisfied-by-absence', req(), ['seen'], {**RT, 'available': False},
    'SATISFIED:declared-optional-absence', required=False)
run('required-is-never-defaulted-to-optional', req(), ['seen'], {**RT, 'available': False},
    'evidence-kind-unavailable')
run('no-targets-refuses-rather-than-vacuously-satisfying', req(), [], RT, 'REFUSE:native.imported-outcome-without-targets')
# HISTORY uses its OWN projection and never the runtime one.
HS = {'available': True, 'consumable': True, 'rangeSatisfiesRequirement': True,
      'covered': {'seen': True}, 'present': {'seen': True},
      'revisionRange': {'from': None, 'to': 'a' * 40, 'commitCount': 3, 'truncated': False}}
run('history-satisfied-by-its-own-projection', req('history-change'), ['seen'], HS,
    'SATISFIED:bounded-observation')
run('history-outside-collection-scope', req('history-change'), ['seen', 'other'],
    {**HS, 'covered': {'seen': True}}, 'history-outside-collection-scope')
run('history-truncated-range', req('history-change'), ['seen'],
    {**HS, 'rangeSatisfiesRequirement': False}, 'history-range-insufficient')
run('history-never-reports-a-runtime-outcome', req('history-change'), ['seen'],
    {**HS, 'covered': {}, 'present': {}}, 'history-outside-collection-scope')
run('runtime-never-reports-a-history-outcome', req(), ['seen'],
    {**RT, 'observability': {'seen': 'unobservable'}}, 'subject-not-observable')
print(json.dumps({'sourceRoot': str(root), 'allMatch': all(r['match'] for r in rows),
                  'cases': rows}, indent=1))
