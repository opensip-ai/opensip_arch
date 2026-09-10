"""Replace the v1 requirement/map controls with corrected ones covering CX-BV6-02/03/04."""
import pathlib

P = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v2/work/'
                 'docs/coop/design-corrections/workflows/check_workflows.v1.py')
s = P.read_text(encoding='utf-8')
lines = s.split('\n')

start = next(i for i, l in enumerate(lines) if l.startswith('# CB6-MUST-1. EvidenceRequirement.deficiency'))
end = next(i for i, l in enumerate(lines) if l.startswith("check('policy.rung-vocabulary-is-exactly-the-ladder-union'"))
NEW = r'''# CB6-MUST-1 / CX-BV6-02 / CX-BV6-03. EvidenceRequirement.deficiency used to name D9Deficiency,
# which cannot express four of the nine native outcomes its producer emits. It now carries the
# vocabulary of its requirement's evidence PLANE, and repair admits BOTH planes, so these controls
# hold four things apart: the native outcome vocabulary, the imported one, the D9 termination
# vocabulary, and the typed presence law that ties a value to `satisfied`.
_NATIVE_DEFICIENCIES = M.NATIVE_SUFFICIENCY_DEFICIENCIES
_IMPORTED_DEFICIENCIES = M.IMPORTED_REQUIREMENT_DEFICIENCIES
_D9_DEFICIENCIES = SCHEMAS[U + 'common']['$defs']['D9Deficiency']['enum']
_IMPORT_LAW = SCHEMAS[U + 'imported-evidence']['x-opensip-imported-requirement-law']
check('repair.sufficiency-vocabulary-mirrors-the-native-authority-exactly',
      SCHEMAS[U + 'common']['$defs']['NativeSufficiencyDeficiency']['enum'] == _NATIVE_DEFICIENCIES)
check('repair.imported-vocabulary-mirrors-its-owning-law-exactly',
      SCHEMAS[U + 'common']['$defs']['ImportedRequirementDeficiency']['enum']
      == _IMPORTED_DEFICIENCIES == list(_IMPORT_LAW['precedence'])
      and set(_IMPORTED_DEFICIENCIES) == set(_IMPORT_LAW['outcomes']))
check('repair.the-two-requirement-planes-are-disjoint-vocabularies',
      not (set(_NATIVE_DEFICIENCIES) & set(_IMPORTED_DEFICIENCIES)))
check('repair.evidence-requirement-carries-both-plane-vocabularies-and-only-those',
      [b['$ref'].rsplit('/', 1)[1] for b in
       SCHEMAS[U + 'repair']['$defs']['EvidenceRequirement']['properties']['deficiency']['oneOf']]
      == ['NativeSufficiencyDeficiency', 'ImportedRequirementDeficiency'])
_FOUR_WITHOUT_A_D9_MEMBER = ['derivation-policy-unmet', 'external-consumers-unknown',
                             'input-closure-incomplete', 'resolution-incomplete']
check('repair.the-four-successor-outcomes-have-no-d9-deficiency-member',
      all(m not in _D9_DEFICIENCIES for m in _FOUR_WITHOUT_A_D9_MEMBER)
      and all(m in _NATIVE_DEFICIENCIES for m in _FOUR_WITHOUT_A_D9_MEMBER))
# DomainDetailCode is a 287-member registry, so this is a statement about the NINE native outcomes
# only: neither vocabulary alone covers them and the union does.
_DDC = set(SCHEMAS[U + 'common']['$defs']['DomainDetailCode']['enum'])
check('repair.neither-single-vocabulary-covers-all-nine-native-outcomes',
      not set(_NATIVE_DEFICIENCIES) <= set(_D9_DEFICIENCIES)
      and not set(_NATIVE_DEFICIENCIES) <= _DDC
      and set(_NATIVE_DEFICIENCIES) <= (set(_D9_DEFICIENCIES) | _DDC))
check('repair.d9-deficiency-enum-was-not-widened-to-carry-per-requirement-outcomes',
      _D9_DEFICIENCIES == ['none', 'required-relation-missing', 'provider-unavailable',
                           'language-tier-unsupported', 'budget-exhausted', 'confidence-floor-unmet',
                           'convergence-exhausted', 'baseline-recipe-unsupported',
                           'verdict-indeterminate', 'query-completeness-unmet'])
_ER_BASE = {'relation': 'imports', 'minResolution': 'resolved-target', 'completeness': 'complete'}
_IMP_BASE = {'relation': 'runtime-observation', 'minResolution': 'observed', 'completeness': 'complete'}
for _m in _NATIVE_DEFICIENCIES:
    must_valid('repair.evidence-requirement-admits-native-outcome.' + _m,
               U + 'repair#/$defs/EvidenceRequirement', dict(_ER_BASE, satisfied=False, deficiency=_m))
for _m in _IMPORTED_DEFICIENCIES:
    must_valid('repair.evidence-requirement-admits-imported-outcome.' + _m,
               U + 'repair#/$defs/EvidenceRequirement', dict(_IMP_BASE, satisfied=False, deficiency=_m))
for _m in ('none', 'verdict-indeterminate', 'convergence-exhausted', 'query-completeness-unmet'):
    must_invalid('repair.evidence-requirement-refuses-d9-only-spelling.' + _m,
                 U + 'repair#/$defs/EvidenceRequirement', dict(_ER_BASE, satisfied=False, deficiency=_m))
# The TYPED presence law, both boundaries. CX-BV6-02: an explicit null is not an absent key and a
# truthy non-boolean is not `true`; the schema always refused both and the boundary now agrees.
must_valid('repair.evidence-requirement-satisfied-omits-the-field',
           U + 'repair#/$defs/EvidenceRequirement', dict(_ER_BASE, satisfied=True))
must_invalid('repair.evidence-requirement-satisfied-must-not-carry-a-deficiency',
             U + 'repair#/$defs/EvidenceRequirement',
             dict(_ER_BASE, satisfied=True, deficiency='resolution-incomplete'))
must_invalid('repair.evidence-requirement-satisfied-must-not-carry-an-explicit-null',
             U + 'repair#/$defs/EvidenceRequirement', dict(_ER_BASE, satisfied=True, deficiency=None))
must_invalid('repair.evidence-requirement-unsatisfied-must-carry-a-deficiency',
             U + 'repair#/$defs/EvidenceRequirement', dict(_ER_BASE, satisfied=False))
must_invalid('repair.evidence-requirement-unsatisfied-must-not-carry-an-explicit-null',
             U + 'repair#/$defs/EvidenceRequirement', dict(_ER_BASE, satisfied=False, deficiency=None))
must_invalid('repair.evidence-requirement-satisfied-must-be-a-boolean',
             U + 'repair#/$defs/EvidenceRequirement', dict(_ER_BASE, satisfied=1))
# The SAME law at the producer/consumer boundary. This is not a claim that the boundary substitutes
# for validating the record: it is the requirement that two boundaries deciding one law AGREE, which
# is exactly what a root probe found they did not. `_boundary_table` below is held equal to the
# schema on every row.
def _requirement_admission(req):
    try:
        return ('ADMIT', M.admit_evidence_requirement(req))
    except M.Refusal as exc:
        return ('REFUSE', exc.error_code + '|' + exc.remedy)
_BOUNDARY_TABLE = [
    (dict(_ER_BASE, satisfied=True), 'ADMIT', ('native', None)),
    (dict(_ER_BASE, satisfied=False, deficiency='resolution-incomplete'), 'ADMIT',
     ('native', 'resolution-incomplete')),
    (dict(_IMP_BASE, satisfied=True), 'ADMIT', ('imported', None)),
    (dict(_IMP_BASE, satisfied=False, deficiency='import-unmapped-only'), 'ADMIT',
     ('imported', 'import-unmapped-only')),
    (dict(_ER_BASE, satisfied=True, deficiency=None), 'REFUSE',
     'native.sufficiency-outcome-on-satisfied-requirement'),
    (dict(_ER_BASE, satisfied=True, deficiency='resolution-incomplete'), 'REFUSE',
     'native.sufficiency-outcome-on-satisfied-requirement'),
    (dict(_ER_BASE, satisfied=1), 'REFUSE', 'native.sufficiency-outcome-satisfied-not-boolean'),
    (dict(_ER_BASE, satisfied=False), 'REFUSE', 'native.sufficiency-outcome-missing'),
    (dict(_ER_BASE, satisfied=False, deficiency=None), 'REFUSE', 'native.sufficiency-outcome-null'),
    (dict(_ER_BASE, satisfied=False, deficiency='verdict-indeterminate'), 'REFUSE',
     'native.sufficiency-outcome-not-a-native-outcome'),
    (dict(_ER_BASE, satisfied=False, deficiency='import-unmapped-only'), 'REFUSE',
     'native.sufficiency-outcome-wrong-plane'),
    (dict(_IMP_BASE, satisfied=False, deficiency='resolution-incomplete'), 'REFUSE',
     'native.sufficiency-outcome-wrong-plane'),
]
for _i, (_req, _expect, _detail) in enumerate(_BOUNDARY_TABLE):
    _outcome, _payload = _requirement_admission(_req)
    if _expect == 'ADMIT':
        check('repair.boundary-admits-and-returns-plane-and-cause.%d' % _i,
              _outcome == 'ADMIT' and _payload == _detail, str(_outcome) + ':' + str(_payload))
    else:
        check('repair.boundary-refuses.%d.%s' % (_i, _detail),
              _outcome == 'REFUSE' and _detail in _payload and _payload.startswith('CONFIG.INVALID|'),
              str(_outcome) + ':' + str(_payload))
    # The owning SCHEMA must reach the same verdict on the same bytes; a disagreement here is the
    # defect CX-BV6-02 named, whichever side is wrong.
    _schema_ok, _ = valid(U + 'repair#/$defs/EvidenceRequirement', _req)
    check('repair.boundary-and-schema-agree.%d' % _i, _schema_ok == (_expect == 'ADMIT'),
          'schema=%s boundary=%s' % (_schema_ok, _expect))
# CX-BV6-03. The IMPORTED plane has its own producer. Its outcomes are decided PER TARGET and each
# names a published import condition; none of them is a native Coverage state.
_IMP_FULL = {'available': True, 'consumable': True, 'windowSatisfiesRequirement': True,
             'observability': {'src/a.ts': 'observed-hit'},
             'observationWindow': {'startUtc': '2026-01-01T00:00:00Z',
                                   'endUtc': '2026-01-02T00:00:00Z'},
             'observedPopulation': 'test-suite'}
def _imported(**delta):
    return M.imported_requirement_outcome(dict(_IMP_BASE, targets=['src/a.ts']),
                                          dict(_IMP_FULL, **delta))
check('repair.imported-observed-hit-satisfies-with-its-observation-bounds',
      _imported()['satisfied'] is True
      and _imported()['disclosures'][0]['observedPopulation'] == 'test-suite'
      and _imported()['disclosures'][0]['observationWindow'] is not None)
check('repair.imported-observable-unhit-is-bounded-evidence-not-a-deficiency',
      _imported(observability={'src/a.ts': 'observable-unhit'})['satisfied'] is True)
for _delta, _want in ((dict(available=False), 'evidence-kind-unavailable'),
                      (dict(consumable=False), 'import-unmapped-only'),
                      (dict(observability={'src/a.ts': 'unobservable'}), 'subject-not-observable'),
                      (dict(observability={'src/a.ts': 'unmapped'}), 'subject-not-observable'),
                      (dict(windowSatisfiesRequirement=False), 'observation-window-insufficient'),
                      (dict(observability={}), 'import-absent-for-requirement')):
    _r = _imported(**_delta)
    check('repair.imported-outcome.' + _want, _r['satisfied'] is False and _r['deficiency'] == _want,
          str(_r))
check('repair.imported-outcome-precedence-reports-the-most-actionable-cause',
      _imported(observability={'src/a.ts': 'unobservable'},
                windowSatisfiesRequirement=False)['deficiency'] == 'subject-not-observable')
# required versus optional is NOT re-invented here: an OPTIONAL absence stays the existing
# IMPORT.ABSENT_FOR_PREDICATE disclosure and is not a gating deficiency.
_OPT = M.imported_requirement_outcome(dict(_IMP_BASE, targets=['src/a.ts']),
                                      dict(_IMP_FULL, available=False), required=False)
check('repair.optional-imported-absence-is-a-disclosure-not-a-deficiency',
      _OPT['satisfied'] is True and 'deficiency' not in _OPT
      and _OPT['disclosures'][0]['code'] == 'IMPORT.ABSENT_FOR_PREDICATE')
def _producer_refusal(fn):
    try:
        fn(); return None
    except M.Refusal as exc:
        return exc.remedy
check('repair.the-imported-producer-refuses-a-native-relation',
      'native.imported-outcome-for-native-relation' in
      (_producer_refusal(lambda: M.imported_requirement_outcome(
          dict(_ER_BASE, targets=['src/a.ts']), _IMP_FULL)) or ''))
check('repair.the-plane-is-read-from-registry-membership-not-from-the-value',
      M.requirement_plane('runtime-observation') == 'imported'
      and M.requirement_plane('history-change') == 'imported'
      and M.requirement_plane('references') == 'native'
      and set(M.EVIDENCE_RELATIONS) == {'runtime-observation', 'history-change'})
check('repair.both-imported-relations-are-still-admissible-requirement-relations',
      all(_repair_requirement_refusal({'relation': _r, 'minResolution': 'observed'}) is None
          for _r in ('runtime-observation', 'history-change')))
check('policy.every-relation-has-a-nonempty-ladder', all(M.RELATION_LADDERS.values()))
# CB6-SHOULD-1 / CX-BV6-04. THREE different things, named for what they are: which operation each
# current command's generic `mutation` step EMITS, the one DEDICATED step operation, and the ACTUAL
# admissible domain of the generic operation field. An earlier revision published command names
# under a key the annotations called the operation domain; the two differ in nine places.
_MAP = SCHEMAS[U + 'repair']['x-opensip-mutation-operation-map']
_BY_COMMAND = _MAP['byCommandGenericMutationStep']
_FIELD_DOMAIN = _MAP['admissibleGenericFieldDomain']['operations']
_OPS = SCHEMAS[U + 'repair']['$defs']['MutationOperation']['enum']
_INV = canonical.parse((HERE / 'command-inventory.v1.json').read_bytes())['commands']
_CMD = {c['name']: c for c in _INV}
# The emission rule is DERIVED, not patched: a command emits a generic operation exactly when it has
# a generic `mutation` step. `analyze` needs no exception - its mutating-family step is `import`,
# whose params carry no operation field at all.
check('workflow.the-generic-map-is-exactly-the-commands-with-a-generic-mutation-step',
      set(_BY_COMMAND) == {c['name'] for c in _INV if 'mutation' in c['steps']},
      str(sorted(set(_BY_COMMAND) ^ {c['name'] for c in _INV if 'mutation' in c['steps']})))
check('workflow.analyze-needs-no-exception-because-import-params-carry-no-operation',
      'import' in _CMD['analyze']['steps'] and 'mutation' not in _CMD['analyze']['steps']
      and 'analyze' not in _BY_COMMAND
      and 'operation' not in SCHEMAS[U + 'invocation-record']['$defs']['ImportParams']['properties']
      and 'mutationClass' not in SCHEMAS[U + 'invocation-record']['$defs']['ImportParams']['properties']
      and 'operation' not in SCHEMAS[U + 'invocation-record']['$defs']['NativePreparationParams']['properties'])
check('workflow.every-generic-row-names-a-real-step-and-class-of-that-command',
      all(r['mintedByStepKind'] == 'mutation' and r['operation'] in _OPS
          and r['mintedByStepKind'] in _CMD[n]['steps'] and r['requestClass'] == _CMD[n]['requestClass']
          for n, r in _BY_COMMAND.items()))
check('workflow.mutation-operation-renames-are-published',
      _MAP['renamedRows'] == {'baseline-upgrade': 'baseline-upgrade-apply',
                              'native-prepare': 'native-preparation',
                              'policy-init': 'policy-write', 'waive': 'waiver-change'})
check('workflow.the-three-mutation-class-renames-are-the-mutation-class-subset',
      {c for c in _MAP['renamedRows'] if _CMD[c]['requestClass'] == 'mutation'}
      == {'baseline-upgrade', 'policy-init', 'waive'}
      and _CMD['native-prepare']['requestClass'] == 'execution')
# The orphan set is RECOMPUTED here, not restated from the document.
check('workflow.operations-with-no-published-emitter-are-recomputed-and-match',
      _MAP['operationsWithNoPublishedEmitter']['operations']
      == sorted(set(_OPS) - {r['operation'] for r in _BY_COMMAND.values()} - {'repair-apply'})
      == ['config-write', 'import', 'native-preparation'])
# THE CORRECTION: the published field domain is the SCHEMA's domain, verified by admitting every
# one of its members at the actual field and refusing the one excluded token. It is deliberately
# WIDER than the emitted set and is not narrowed to current emitters.
check('workflow.the-field-domain-is-every-operation-except-repair-apply',
      _FIELD_DOMAIN == sorted(set(_OPS) - {'repair-apply'}) and len(_FIELD_DOMAIN) == 23)
check('workflow.the-field-domain-is-wider-than-what-current-commands-emit',
      {r['operation'] for r in _BY_COMMAND.values()} < set(_FIELD_DOMAIN)
      and len({r['operation'] for r in _BY_COMMAND.values()}) == 20)
_SCOPE = {'schemaVersion': 1, 'requestId': C['REQ'], 'stepId': 2, 'projectId': C['PRJ']}
for _op in _FIELD_DOMAIN:
    must_valid('workflow.generic-mutation-scope-admits.' + _op,
               U + 'invocation-record#/$defs/MutationReplayScopeV1', dict(_SCOPE, operation=_op))
    must_valid('workflow.generic-mutation-class-admits.' + _op,
               U + 'invocation-record#/$defs/MutationParams/properties/mutationClass', _op)
for _op in _MAP['dedicatedStepOperations']:
    must_invalid('workflow.generic-mutation-scope-refuses.' + _op,
                 U + 'invocation-record#/$defs/MutationReplayScopeV1', dict(_SCOPE, operation=_op))
    must_invalid('workflow.generic-mutation-class-refuses.' + _op,
                 U + 'invocation-record#/$defs/MutationParams/properties/mutationClass', _op)
check('workflow.the-dedicated-operation-cites-its-own-step-and-receipt',
      _MAP['dedicatedStepOperations']['repair-apply']['stepKind'] == 'repair-apply'
      and any('RepairApplyParams' in c for c in
              _MAP['dedicatedStepOperations']['repair-apply']['citations'])
      and SCHEMAS[U + 'repair']['$defs']['MutationReceiptV1']['properties']['operation']['$ref']
          == '#/$defs/MutationOperation')
# Injectivity is an observation about today's inventory, not a law, so it is recorded as one.
check('workflow.the-current-generic-rows-happen-to-be-injective-which-is-not-assumed-as-a-law',
      len({r['operation'] for r in _BY_COMMAND.values()}) == len(_BY_COMMAND)
      and 'injectivityIsNotAssumed' in _MAP)
check('workflow.the-annotations-name-the-field-domain-not-the-command-list',
      all(SCHEMAS[U + 'invocation-record']['$defs'][_d]['properties'][_f]['x-opensip-vocabulary']
          ['fieldDomainAuthority'].endswith('admissibleGenericFieldDomain')
          for _d, _f in (('MutationParams', 'mutationClass'),
                         ('MutationReplayScopeV1', 'operation'))))
check('workflow.publishing-the-map-added-no-operation-and-no-command',
      len(_OPS) == 24 and len(_INV) == 45)
'''
lines[start:end] = NEW.split('\n')
P.write_text('\n'.join(lines), encoding='utf-8')
print('ok')
