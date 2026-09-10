"""v3 boundary probe: the projection join, the per-kind consumer, and the corrected semantics.
Replays root's own final-v2 counterexamples against the corrected bytes."""
import importlib.util, json, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
sp = importlib.util.spec_from_file_location('W', root / 'docs/coop/design-corrections/workflows/workflows_model.v1.py')
W = importlib.util.module_from_spec(sp); sp.loader.exec_module(W)
rows = []
FP1 = 'finding-key2:' + '1' * 64
FP2 = 'finding-key2:' + '2' * 64
FINDINGS = {FP1: {'fingerprint': FP1}, FP2: {'fingerprint': FP2}}
def desc(path, qname):
    return {'schemaVersion': 2, 'ruleStableId': 'r', 'detectorSemanticsMajor': 1,
            'subjectKey': {'language': 'typescript', 'kind': 'function', 'logicalPath': path,
                           'qualifiedName': qname, 'discriminator': 'd'}, 'relatedSubjectKeys': []}
DESCS = {FP1: desc('src/a.ts', 'seen'), FP2: desc('src/b.ts', 'missing')}
def req(rel='runtime-observation', completeness='complete'):
    return {'relation': rel, 'minResolution': 'observed', 'completeness': completeness}
def rec(label, expect, fn):
    try:
        v = fn(); actual = v.get('deficiency') or ('SATISFIED:' + v.get('satisfiedBy', ''))
        rows.append({'case': label, 'expect': expect, 'actual': actual, 'match': actual == expect, 'value': v})
    except Exception as e:
        actual = 'REFUSE:' + getattr(e, 'remedy', str(e)).split(':')[0]
        rows.append({'case': label, 'expect': expect, 'actual': actual, 'match': actual == expect})

def proj(kind, subjects, targets=(FP1, FP2)):
    return W.project_targets_to_imported_subjects(list(targets), kind, FINDINGS, DESCS, subjects)

RT_SUBJ = [{'path': 'src/a.ts', 'symbol': 'seen', 'observability': 'observed-hit'}]
RT_EV = {'available': True, 'consumable': True, 'windowSatisfiesRequirement': True,
         'observationWindow': {'startUtc': '2026-09-01T00:00:00Z', 'endUtc': '2026-09-02T00:00:00Z'},
         'observedPopulation': 'synthetic'}
# ROOT'S final-v2 partial counterexample: one supported, one unobservable, partial-acceptable.
UNOBS = RT_SUBJ + [{'path': 'src/b.ts', 'symbol': 'missing', 'observability': 'unobservable'}]
rec('root-partial-runtime-one-supported-one-unobservable', 'SATISFIED:bounded-observation',
    lambda: W.imported_requirement_outcome(req(completeness='partial-acceptable'),
                                           proj('runtime', UNOBS), RT_EV, True))
rec('complete-runtime-with-an-unobservable-target', 'subject-not-observable',
    lambda: W.imported_requirement_outcome(req(), proj('runtime', UNOBS), RT_EV, True))
rec('complete-runtime-with-a-missing-target', 'import-absent-for-requirement',
    lambda: W.imported_requirement_outcome(req(), proj('runtime', RT_SUBJ), RT_EV, True))
rec('complete-runtime-every-target-supported', 'SATISFIED:bounded-observation',
    lambda: W.imported_requirement_outcome(req(), proj('runtime', RT_SUBJ, (FP1,)), RT_EV, True))
rec('runtime-window-insufficient-still-vetoes-partial', 'observation-window-insufficient',
    lambda: W.imported_requirement_outcome(req(completeness='partial-acceptable'),
                                           proj('runtime', UNOBS),
                                           dict(RT_EV, windowSatisfiesRequirement=False), True))
HS_SUBJ = [{'path': 'src/a.ts'}]
HS_EV = {'available': True, 'consumable': True, 'rangeSatisfiesRequirement': True,
         'revisionRange': {'from': None, 'to': 'a' * 40, 'commitCount': 3, 'truncated': False},
         'covered': {FP1: True, FP2: False}}
rec('root-partial-history-one-supported-one-uncovered', 'SATISFIED:bounded-observation',
    lambda: W.imported_requirement_outcome(req('history-change', 'partial-acceptable'),
                                           proj('history', HS_SUBJ), HS_EV, True))
rec('complete-history-with-an-uncovered-target', 'history-outside-collection-scope',
    lambda: W.imported_requirement_outcome(req('history-change'), proj('history', HS_SUBJ), HS_EV, True))
# typed required boundary: root's None and 0 must now refuse, not become optional success.
for flag, expect in ((True, 'evidence-kind-unavailable'),
                     (False, 'SATISFIED:declared-optional-absence'),
                     (None, 'REFUSE:native.imported-required-declaration-not-boolean'),
                     (0, 'REFUSE:native.imported-required-declaration-not-boolean')):
    rec('required-flag-' + repr(flag), expect,
        lambda f=flag: W.imported_requirement_outcome(req(), proj('runtime', RT_SUBJ, (FP1,)),
                                                      dict(RT_EV, available=False), f))
# projection boundaries
def projrow(label, expect, fn):
    try:
        rows.append({'case': label, 'expect': expect, 'actual': 'OK', 'match': expect == 'OK', 'value': fn()})
    except Exception as e:
        a = 'REFUSE:' + getattr(e, 'remedy', str(e)).split(':')[0]
        rows.append({'case': label, 'expect': expect, 'actual': a, 'match': a == expect})
projrow('projection-refuses-an-ambiguous-target', 'REFUSE:native.imported-projection-ambiguous-target',
        lambda: proj('runtime', RT_SUBJ + [{'path': 'src/a.ts', 'observability': 'observed-hit'}], (FP1,)))
projrow('projection-refuses-a-target-not-in-the-evidence-run',
        'REFUSE:native.imported-projection-target-not-in-evidence-run',
        lambda: W.project_targets_to_imported_subjects(['finding-key2:' + '9' * 64], 'runtime',
                                                       FINDINGS, DESCS, RT_SUBJ))
projrow('projection-refuses-a-missing-fingerprint-preimage',
        'REFUSE:native.imported-projection-fingerprint-preimage-missing',
        lambda: W.project_targets_to_imported_subjects([FP1], 'runtime', FINDINGS, {}, RT_SUBJ))
projrow('runtime-symbol-granularity-is-not-flattened', 'OK',
        lambda: proj('runtime', [{'path': 'src/a.ts', 'symbol': 'other', 'observability': 'observed-hit'}], (FP1,)))
projrow('history-widening-to-file-is-disclosed-per-target', 'OK', lambda: proj('history', HS_SUBJ, (FP1,)))
# per-kind consumer, root's exact cross-kind cases
for rel, cause, expect in (('runtime-observation', 'history-range-insufficient', 'REFUSE'),
                           ('history-change', 'subject-not-observable', 'REFUSE'),
                           ('runtime-observation', 'subject-not-observable', 'ADMIT'),
                           ('history-change', 'history-range-insufficient', 'ADMIT')):
    r = dict(req(rel), satisfied=False, deficiency=cause)
    try:
        v = W.admit_evidence_requirement(r); a = 'ADMIT'
    except Exception as e:
        a = 'REFUSE'; v = getattr(e, 'remedy', str(e))[:80]
    rows.append({'case': 'consumer-%s-%s' % (rel, cause), 'expect': expect, 'actual': a,
                 'match': a == expect, 'value': v})
print(json.dumps({'sourceRoot': str(root), 'allMatch': all(r['match'] for r in rows), 'cases': rows}, indent=1))
