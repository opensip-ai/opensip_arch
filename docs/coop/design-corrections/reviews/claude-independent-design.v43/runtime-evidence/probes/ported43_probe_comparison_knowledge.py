"""Independent pure-function probe of the source39 comparison presence-knowledge helpers (workflows-and-surfaces section 3).

Calls workflow_projection_model.v3 first_attribution_unknown, baseline_presence_knowledge, correspondence_barrier,
selection_excludes and fingerprint_absence_known with reviewer-authored synthetic records. Expected values are the
reviewer's reading of section 3; full-Run comparison controls are the author's check-workflow-projection /
check-comparison-knowledge (reference group evidence). Writes only receipts/probes/comparison-knowledge.json."""
import importlib.util, json, sys, traceback
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v43')
WF = RT / 'work/source43-pkg/docs/coop/design-corrections/workflows'
spec = importlib.util.spec_from_file_location('p40_wpm3', WF / 'workflow_projection_model.v3.py')
P = importlib.util.module_from_spec(spec)
sys.modules['p40_wpm3'] = P
spec.loader.exec_module(P)
ROWS = []


def row(case, got, want):
    ROWS.append({'case': case, 'ok': got == want, 'observed': got, 'expected': want})


def pres(B, E0, E1, E2, E3, E4):
    return {'B': B, 'E0': E0, 'E1': E1, 'E2': E2, 'E3': E3, 'E4': E4}


def main():
    f = P.first_attribution_unknown
    row('known-code-net-new-before-null-keeps-classification', f(pres(False, None, True, True, True, None)), None)
    row('unknown-baseline-first-change-rests-on-B', f(pres(None, None, True, True, True, True)), 'baseline-absence-unknown')
    row('unknown-current-with-known-baseline', f(pres(True, None, True, True, True, None)), 'current-absence-unknown')
    row('both-unknown-selects-baseline-first', f(pres(None, None, None, None, None, None)), 'baseline-absence-unknown')
    row('all-known-unchanged-is-not-unknown', f(pres(True, None, True, True, True, True)), None)
    row('known-policy-hidden-code-net-new', f(pres(False, None, True, False, False, False)), None)
    row('known-fixed-then-unknown-current-keeps-known-change', f(pres(True, None, False, False, False, None)), None)

    rows = [{'ruleId': 'r', 'subjectPath': 'src/a.ts', 'kind': 'symbol', 'language': 'typescript', 'qualifiedName': 'f'}]
    cb = P.correspondence_barrier
    row('same-rule-same-path-no-subject-key-is-a-barrier', cb(rows, 'r', 'src/a.ts'), True)
    row('different-path-is-not-a-barrier', cb(rows, 'r', 'src/b.ts'), False)
    row('different-rule-is-not-a-barrier', cb(rows, 'other', 'src/a.ts'), False)
    row('provably-different-subject-identity-is-not-a-barrier', cb(rows, 'r', 'src/a.ts', {'kind': 'symbol', 'language': 'typescript', 'qualifiedName': 'g'}), False)
    row('same-subject-identity-is-a-barrier', cb(rows, 'r', 'src/a.ts', {'kind': 'symbol', 'language': 'typescript', 'qualifiedName': 'f'}), True)
    row('baseline-row-without-identity-keeps-the-same-rule-same-path-barrier',
        cb([{'ruleId': 'r', 'subjectPath': 'src/a.ts'}], 'r', 'src/a.ts', {'kind': 'symbol', 'language': 'typescript', 'qualifiedName': 'g'}), True)
    row('row-without-a-path-is-conservatively-a-barrier', cb([{'ruleId': 'r'}], 'r', 'src/a.ts'), True)

    policy_on = {'rules': [{'ruleId': 'r', 'enabled': True}]}
    policy_off = {'rules': [{'ruleId': 'r', 'enabled': False}]}
    scope_src = {'schemaFamily': 'opensip.product.scope', 'schemaMajor': 1, 'include': ['src/**'], 'exclude': []}
    se = P.selection_excludes
    row('disabled-rule-is-non-selection', se(policy_off, None, 'r', 'src/a.ts'), True)
    row('missing-rule-is-non-selection', se({'rules': []}, None, 'r', 'src/a.ts'), True)
    row('scope-not-selecting-path-is-non-selection', se(policy_on, scope_src, 'r', 'README.md'), True)
    row('enabled-and-selected-is-not-non-selection', se(policy_on, scope_src, 'r', 'src/a.ts'), False)

    bp = P.baseline_presence_knowledge
    b_rules_complete = {'r': {'absenceKnowledge': 'complete-hit-set'}}
    b_rules_unknown = {'r': {'absenceKnowledge': 'unknown'}}
    base = {'contextDocuments': {'policy': policy_on, 'scope': {'schemaFamily': 'opensip.product.scope', 'schemaMajor': 1, 'include': ['**'], 'exclude': []}},
            'unmatchedOccurrences': []}
    row('baseline-entry-is-known-presence', bp('fp', 'r', {'fp': {'waived': False}}, b_rules_complete, base, 'src/a.ts'), True)
    row('complete-hit-set-without-barrier-is-known-absence', bp('fp', 'r', {}, b_rules_complete, base, 'src/a.ts'), False)
    row('unknown-absence-knowledge-is-null-not-false', bp('fp', 'r', {}, b_rules_unknown, base, 'src/a.ts'), None)
    with_unmatched = dict(base, unmatchedOccurrences=[{'ruleId': 'r', 'subjectPath': 'src/a.ts'}])
    row('baseline-unmatched-same-rule-same-path-is-null', bp('fp', 'r', {}, b_rules_complete, with_unmatched, 'src/a.ts'), None)
    row('baseline-unmatched-other-path-does-not-block-absence', bp('fp', 'r', {}, b_rules_complete, with_unmatched, 'src/b.ts'), False)
    disabled_base = dict(base, contextDocuments={'policy': policy_off, 'scope': base['contextDocuments']['scope']})
    row('baseline-non-selection-is-false-even-with-unknown-knowledge', bp('fp', 'r', {}, b_rules_unknown, disabled_base, 'src/a.ts'), False)
    row('empty-entries-never-coerce-missing-rule-coverage-to-false', bp('fp', 'r', {}, {}, base, 'src/a.ts'), None)

    fa = P.fingerprint_absence_known
    view = {'policy': policy_on, 'evaluationState': 'evaluated', 'ruleResults': [], 'proof': {'predicateProofs': None}, 'occurrences': []}
    row('missing-extent-is-unknown-never-false', fa(view, None, 'r', 'src/a.ts'), False)
    row('missing-rule-id-is-unknown', fa(view, {'examinedPaths': ['src/a.ts'], 'scopeDocument': None, 'foundationScope': None, 'extractionComplete': True}, None, 'src/a.ts'), False)
    row('non-selection-short-circuits-to-known-absence', fa({'policy': policy_off, 'occurrences': []}, None, 'r', 'src/a.ts'), True)


try:
    main()
except Exception:  # noqa: BLE001
    ROWS.append({'case': 'probe-crashed', 'ok': False, 'observed': traceback.format_exc()[-1500:]})
out = RT / 'receipts/probes/comparison-knowledge.json'
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps({'standing': 'independent reviewer pure-function probe; not full-Run comparison', 'rows': ROWS,
                           'failed': [r for r in ROWS if not r['ok']]}, indent=1, default=str))
print(json.dumps({'total': len(ROWS), 'failed': [(r['case'], r['observed'], r.get('expected')) for r in ROWS if not r['ok']]}, indent=1, default=str))
