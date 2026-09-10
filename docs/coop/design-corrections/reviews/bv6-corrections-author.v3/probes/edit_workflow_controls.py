"""v3 controls: projection join, per-kind consumer, corrected semantics, receipt key."""
import pathlib

P = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v3/work/'
                 'docs/coop/design-corrections/workflows/check_workflows.v1.py')
s = P.read_text(encoding='utf-8')
start = s.index('# CX-BV6-03. The IMPORTED plane has its own producer,')
end = s.index("check('policy.every-relation-has-a-nonempty-ladder'")
NEW = r'''# CX-BV6-03 / BV6-V3-IMPORT-*. The IMPORTED plane has its own producer, its own per-kind
# projections, and a DETERMINISTIC join from plan target FINGERPRINTS to payload subjects. Targets
# are `finding-key2:` identities; RuntimeSubject keys on {path, symbol?} and HistorySubject on
# {path}. An earlier revision read the payload maps directly by the target string, which equated a
# finding-key identity with a LogicalPath.
_IMP_LAW = SCHEMAS[U + 'imported-evidence']['x-opensip-imported-requirement-law']
_FP1 = 'finding-key2:' + '1' * 64
_FP2 = 'finding-key2:' + '2' * 64
_FINDINGS = {_FP1: {'fingerprint': _FP1}, _FP2: {'fingerprint': _FP2}}
def _fp_descriptor(path, qualified):
    return {'schemaVersion': 2, 'ruleStableId': 'r', 'detectorSemanticsMajor': 1,
            'relatedSubjectKeys': [],
            'subjectKey': {'language': 'typescript', 'kind': 'function', 'logicalPath': path,
                           'qualifiedName': qualified, 'discriminator': 'd'}}
_DESCS = {_FP1: _fp_descriptor('src/a.ts', 'seen'), _FP2: _fp_descriptor('src/b.ts', 'missing')}
_RT_ROWS = [{'path': 'src/a.ts', 'symbol': 'seen', 'observability': 'observed-hit'}]
_RT_UNOBS = _RT_ROWS + [{'path': 'src/b.ts', 'symbol': 'missing', 'observability': 'unobservable'}]
_HS_ROWS = [{'path': 'src/a.ts'}]
_RT_EV = {'available': True, 'consumable': True, 'windowSatisfiesRequirement': True,
          'observationWindow': {'startUtc': '2026-09-01T00:00:00Z', 'endUtc': '2026-09-02T00:00:00Z'},
          'observedPopulation': 'synthetic'}
_HS_EV = {'available': True, 'consumable': True, 'rangeSatisfiesRequirement': True,
          'revisionRange': {'from': None, 'to': 'a' * 40, 'commitCount': 3, 'truncated': False},
          'covered': {_FP1: True, _FP2: False}}
def _imp_req(rel='runtime-observation', completeness='complete'):
    return {'relation': rel, 'minResolution': 'observed', 'completeness': completeness}
def _project(kind, rows, targets=(_FP1, _FP2), descs=None, findings=None):
    return M.project_targets_to_imported_subjects(
        list(targets), kind, _FINDINGS if findings is None else findings,
        _DESCS if descs is None else descs, rows)
def _outcome(rel, completeness, kind, rows, ev, targets=(_FP1, _FP2), required=True):
    try:
        r = M.imported_requirement_outcome(_imp_req(rel, completeness),
                                           _project(kind, rows, targets), ev, required)
        return r.get('deficiency') or ('SATISFIED:' + r.get('satisfiedBy', '')), r
    except M.Refusal as exc:
        return 'REFUSE:' + exc.remedy.split(':')[0], None
def _refusal(fn):
    try:
        fn(); return None
    except M.Refusal as exc:
        return exc.remedy.split(':')[0]
# The join itself: a target is projected through the RETAINED finding-fingerprint subjectKey.
_P = _project('runtime', _RT_ROWS, (_FP1,))
check('repair.the-target-projection-reads-the-retained-fingerprint-subject-key',
      _P[_FP1]['logicalPath'] == 'src/a.ts' and _P[_FP1]['matched'] is True
      and _P[_FP1]['symbolGranularity'] is True)
# SYMBOL granularity is preserved: a symbol-keyed row for a DIFFERENT symbol does not match.
check('repair.a-symbol-keyed-row-for-another-symbol-does-not-match-the-target',
      _project('runtime', [{'path': 'src/a.ts', 'symbol': 'other', 'observability': 'observed-hit'}],
               (_FP1,))[_FP1]['matched'] is False)
# HISTORY has no symbol field, so a symbol target is answered at FILE granularity and that widening
# is disclosed rather than hidden.
check('repair.history-widening-to-file-is-disclosed-per-target',
      _project('history', _HS_ROWS, (_FP1,))[_FP1]['granularityWidenedToFile'] is True
      and _project('runtime', _RT_ROWS, (_FP1,))[_FP1]['granularityWidenedToFile'] is False)
_HW = _outcome('history-change', 'complete', 'history', _HS_ROWS, _HS_EV, (_FP1,))[1]
check('repair.the-widening-reaches-the-outcome-disclosure',
      any(d['kind'] == 'granularity-widened-to-file' and d['targets'] == [_FP1]
          for d in _HW['disclosures']))
# Ambiguity refuses; it is not resolved by choosing one.
check('repair.the-projection-refuses-an-ambiguous-target',
      _refusal(lambda: _project('runtime',
                                _RT_ROWS + [{'path': 'src/a.ts', 'observability': 'observed-hit'}],
                                (_FP1,))) == 'native.imported-projection-ambiguous-target')
check('repair.the-projection-refuses-a-target-not-in-the-evidence-run',
      _refusal(lambda: _project('runtime', _RT_ROWS, ('finding-key2:' + '9' * 64,)))
      == 'native.imported-projection-target-not-in-evidence-run')
check('repair.the-projection-refuses-a-missing-retained-fingerprint-preimage',
      _refusal(lambda: _project('runtime', _RT_ROWS, (_FP1,), descs={}))
      == 'native.imported-projection-fingerprint-preimage-missing')
# ALL versus ANY, and the corrected partial semantics. An earlier revision vetoed on ANY
# unobservable or uncovered target BEFORE the ANY test, so a lawful partial refused.
check('repair.partial-acceptable-is-satisfied-with-one-supported-and-one-unobservable-target',
      _outcome('runtime-observation', 'partial-acceptable', 'runtime', _RT_UNOBS, _RT_EV)[0]
      == 'SATISFIED:bounded-observation')
check('repair.partial-acceptable-is-satisfied-with-one-supported-and-one-uncovered-target',
      _outcome('history-change', 'partial-acceptable', 'history', _HS_ROWS, _HS_EV)[0]
      == 'SATISFIED:bounded-observation')
check('repair.complete-still-names-the-unobservable-target-as-the-cause',
      _outcome('runtime-observation', 'complete', 'runtime', _RT_UNOBS, _RT_EV)[0]
      == 'subject-not-observable')
check('repair.complete-still-names-a-missing-target-as-absent',
      _outcome('runtime-observation', 'complete', 'runtime', _RT_ROWS, _RT_EV)[0]
      == 'import-absent-for-requirement')
check('repair.complete-still-names-an-uncovered-history-target',
      _outcome('history-change', 'complete', 'history', _HS_ROWS, _HS_EV)[0]
      == 'history-outside-collection-scope')
check('repair.complete-is-satisfied-when-every-target-is-supported',
      _outcome('runtime-observation', 'complete', 'runtime', _RT_ROWS, _RT_EV, (_FP1,))[0]
      == 'SATISFIED:bounded-observation')
# BOUNDS are a property of the observation, not of the target count, so they apply in both modes.
check('repair.an-insufficient-window-applies-under-partial-acceptable-too',
      _outcome('runtime-observation', 'partial-acceptable', 'runtime', _RT_UNOBS,
               dict(_RT_EV, windowSatisfiesRequirement=False))[0] == 'observation-window-insufficient')
check('repair.an-insufficient-history-range-applies-under-partial-acceptable-too',
      _outcome('history-change', 'partial-acceptable', 'history', _HS_ROWS,
               dict(_HS_EV, rangeSatisfiesRequirement=False))[0] == 'history-range-insufficient')
# Bounded-negative evidence satisfies and the polarity is disclosed, not collapsed.
_UNHIT = _outcome('runtime-observation', 'complete', 'runtime',
                  [{'path': 'src/a.ts', 'symbol': 'seen', 'observability': 'observable-unhit'}],
                  _RT_EV, (_FP1,))
check('repair.bounded-negative-observable-unhit-satisfies-and-discloses-its-polarity',
      _UNHIT[0] == 'SATISFIED:bounded-observation'
      and _UNHIT[1]['disclosures'][0]['polarity'] == ['observable-unhit']
      and _UNHIT[1]['disclosures'][0]['observedPopulation'] == 'synthetic')
# The evidenceUse declaration reaches this boundary as a TYPED BOOLEAN. There is no `unknown` state
# and no falsy value is read as `optional`; an earlier revision accepted None and 0 as optional.
check('repair.optional-absence-is-satisfied-by-absence-not-by-evidence',
      _outcome('runtime-observation', 'complete', 'runtime', _RT_ROWS,
               dict(_RT_EV, available=False), (_FP1,), required=False)[0]
      == 'SATISFIED:declared-optional-absence')
check('repair.a-required-declaration-still-reports-the-absent-kind',
      _outcome('runtime-observation', 'complete', 'runtime', _RT_ROWS,
               dict(_RT_EV, available=False), (_FP1,), required=True)[0]
      == 'evidence-kind-unavailable')
for _flag in (None, 0, 1, 'yes'):
    check('repair.a-non-boolean-evidence-use-declaration-refuses.' + repr(_flag),
          _outcome('runtime-observation', 'complete', 'runtime', _RT_ROWS,
                   dict(_RT_EV, available=False), (_FP1,), required=_flag)[0]
          == 'REFUSE:native.imported-required-declaration-not-boolean')
# The CONSUMER decides the PER-KIND law, not merely the broad plane. Root's final-v2 controls showed
# a runtime relation admitting a history outcome and the reverse.
for _rel, _cause, _expect in (('runtime-observation', 'history-range-insufficient', 'REFUSE'),
                              ('history-change', 'subject-not-observable', 'REFUSE'),
                              ('runtime-observation', 'subject-not-observable', 'ADMIT'),
                              ('history-change', 'history-range-insufficient', 'ADMIT'),
                              ('runtime-observation', 'import-unmapped-only', 'ADMIT'),
                              ('history-change', 'evidence-kind-unavailable', 'ADMIT')):
    _r = dict(_imp_req(_rel), satisfied=False, deficiency=_cause)
    _got = _refusal(lambda r=_r: M.admit_evidence_requirement(r))
    check('repair.consumer-per-kind.' + _rel + '.' + _cause,
          (_got is None) == (_expect == 'ADMIT')
          and (_got is None or _got == 'native.sufficiency-outcome-not-applicable-to-kind'),
          str(_got))
check('repair.the-two-imported-kinds-report-only-their-own-outcomes',
      set(_IMP_LAW['perKindApplicability']['runtime-observation'])
      & set(_IMP_LAW['perKindApplicability']['history-change'])
      == {'evidence-kind-unavailable', 'import-unmapped-only', 'import-absent-for-requirement'}
      and 'subject-not-observable' not in _IMP_LAW['perKindApplicability']['history-change']
      and 'history-range-insufficient' not in _IMP_LAW['perKindApplicability']['runtime-observation']
      and 'observationWindow' not in SCHEMAS[U + 'imported-evidence']['$defs']['HistoryPayloadV1']['properties']
      and 'collectionScope' in SCHEMAS[U + 'imported-evidence']['$defs']['HistoryPayloadV1']['required'])
check('repair.every-imported-outcome-names-its-owning-payload-field',
      all(r['boundTo'] and r['groundedIn'] and r['appliesTo'] for r in _IMP_LAW['outcomes'].values())
      and set(_IMP_LAW['outcomes']) == set(_IMP_LAW['precedence']))
# The published input bindings name real owners, and the two corrected ones say what they are.
check('repair.the-target-binding-names-the-projection-not-a-payload-key',
      'targetSubjectProjection' in _IMP_LAW
      and 'FINGERPRINTS' in _IMP_LAW['inputBinding']['targets']
      and len(_IMP_LAW['targetSubjectProjection']['deterministicProjection']) == 7)
check('repair.the-window-demand-is-owned-by-the-recipe-closure-not-a-wire-field',
      'closureId' in _IMP_LAW['inputBinding']['windowDemand']
      and 'closureId' in SCHEMAS[U + 'repair']['$defs']['RecipeRef']['required']
      and set(SCHEMAS[U + 'repair']['$defs']['RecipeRef']['properties'])
          == {'contributionId', 'recipeId', 'recipeVersion', 'closureId'})
check('repair.the-all-versus-any-reading-is-recorded-as-a-selected-clarification',
      'SELECTED CLARIFICATION' in _IMP_LAW['inputBinding']['allVersusAny']
      and 'SELECTED CLARIFICATION' in _IMP_LAW['targetSubjectProjection']['standing'])
check('repair.the-imported-producer-refuses-a-native-relation',
      _refusal(lambda: M.imported_requirement_outcome(
          {'relation': 'references', 'minResolution': 'resolved-binding', 'completeness': 'complete'},
          _project('runtime', _RT_ROWS, (_FP1,)), _RT_EV, True))
      == 'native.imported-outcome-for-native-relation')
check('repair.the-plane-is-read-from-registry-membership-not-from-the-value',
      M.requirement_plane('runtime-observation') == 'imported'
      and M.requirement_plane('history-change') == 'imported'
      and M.requirement_plane('references') == 'native'
      and set(M.EVIDENCE_RELATIONS) == {'runtime-observation', 'history-change'})
check('repair.both-imported-relations-are-still-admissible-requirement-relations',
      all(_repair_requirement_refusal({'relation': _r, 'minResolution': 'observed'}) is None
          for _r in ('runtime-observation', 'history-change')))
'''
s = s[:start] + NEW + s[end:]

# ---- receipt key controls, beside the step-kind ones -------------------------------------------
ANCHOR = """check('workflow.the-reference-model-limit-is-stated-not-confused-with-the-design-law',
      'whatIsNotClaimed' in _MAP and 'QUALIFICATION limit' in _MAP['whatIsNotClaimed'])
"""
RECEIPT = '''check('workflow.the-reference-model-limit-is-stated-not-confused-with-the-design-law',
      'whatIsNotClaimed' in _MAP['receiptIdempotencyKeyByStepKind']
      and 'QUALIFICATION limit' in _MAP['receiptIdempotencyKeyByStepKind']['whatIsNotClaimed'])
# BV6-V3-RECEIPT. MutationReceiptV1 requires BOTH operation and idempotencyKey. An earlier revision
# bound only the operation and said the non-generic step kinds mint no H(workflow.mutation-intent)
# key at all, leaving a REQUIRED field underdetermined for import and native-preparation.
_KEYS = _MAP['receiptIdempotencyKeyByStepKind']['recipes']
check('workflow.the-mutation-receipt-requires-both-operation-and-idempotency-key',
      {'operation', 'idempotencyKey'} <= set(SCHEMAS[U + 'repair']['$defs']['MutationReceiptV1']['required']))
check('workflow.every-step-kind-has-a-published-key-recipe-and-lookup-meaning',
      set(_KEYS) == set(_BY_STEP)
      and all(_KEYS[k]['key'] and _KEYS[k]['lookupMeaning'] for k in _KEYS))
# The key recipe for the two non-generic kinds is the EXISTING published one over the EXISTING
# closed scope record, which is admissible precisely because the generic field domain was not
# narrowed to the current emitters.
_SCOPE_KEY = lambda op: M.mutation_replay_key(M.mutation_replay_scope(C['REQ'], 2, C['PRJ'], op))
for _k in ('import', 'native-preparation'):
    must_valid('workflow.the-receipt-key-scope-record-is-schema-valid.' + _k,
               U + 'invocation-record#/$defs/MutationReplayScopeV1',
               dict(_SCOPE, operation=_BY_STEP[_k]['operation']))
    check('workflow.the-published-key-recipe-is-computable-for.' + _k,
          len(_SCOPE_KEY(_BY_STEP[_k]['operation'])) == 64)
check('workflow.the-non-generic-receipt-keys-differ-from-each-other-and-from-a-generic-one',
      len({_SCOPE_KEY(o) for o in ('import', 'native-preparation', 'purge')}) == 3)
check('workflow.native-preparation-lookup-is-not-replay-and-import-is-delivery-only',
      'NOT REPLAY' in _KEYS['native-preparation']['lookupMeaning']
      and 'NEW EXPLICIT AUTHORIZED EXECUTION' in _KEYS['native-preparation']['lookupMeaning']
      and 'DELIVERY ONLY' in _KEYS['import']['lookupMeaning'])
check('workflow.the-owning-mutation-receipt-domain-is-named-without-claiming-it-is-the-only-one',
      'workflow.mutation-receipt' in _MAP['receiptOperationIsRequiredNotOptional']
      and 'workflow.verification-link' in _MAP['receiptOperationIsRequiredNotOptional'])
'''
assert s.count(ANCHOR) == 1
s = s.replace(ANCHOR, RECEIPT)
P.write_text(s, encoding='utf-8')
print('ok')
