import pathlib

P = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v1/work/'
                 'docs/coop/design-corrections/workflows/check_workflows.v1.py')
s = P.read_text(encoding='utf-8')

# --- runner: per-case evidence requirements + remedy discrimination -------------------------
OLD = """    try:
        plan = M.repair_preview(C['PRJ'], tree, run, RS['recipe'], RS['targets'], edits, RS['evidenceRequirements'], scope, trust, ephemeral=case.get('ephemeral', False))
    except M.Refusal as r:
        check(cid, case['expect'].get('refusal') == r.detail, r.detail); continue
"""
NEW = """    # CB6-MUST-1: a case may supply its own evidence requirements so that FAILING requirements and
    # the (satisfied, deficiency) pair law are exercised, not only the admitted positive.
    requirements = case.get('evidenceRequirements', RS['evidenceRequirements'])
    try:
        plan = M.repair_preview(C['PRJ'], tree, run, RS['recipe'], RS['targets'], edits, requirements, scope, trust, ephemeral=case.get('ephemeral', False))
    except M.Refusal as r:
        check(cid, case['expect'].get('refusal') == r.detail, r.detail)
        # A detail-free refusal is not self-identifying, so the case names the internal decision key
        # it expects and the control fails if a DIFFERENT refusal happened to fire.
        if 'expectRemedyContains' in case:
            check(cid + '.refusal-reason', case['expectRemedyContains'] in r.remedy, r.remedy)
        continue
"""
assert s.count(OLD) == 1
s = s.replace(OLD, NEW)

OLD2 = """        check(cid + '.applicable', plan['descriptor']['applicable'] == exp['applicable'] and (exp['applicable'] or plan['descriptor']['unmetPreconditions'][0]['code'] == exp['unmet']))
"""
NEW2 = """        check(cid + '.applicable', plan['descriptor']['applicable'] == exp['applicable'] and (exp['applicable'] or plan['descriptor']['unmetPreconditions'][0]['code'] == exp['unmet']))
        if 'unmetRemedyContains' in exp:
            # The EXACT native cause must reach the public unmet precondition. Two of these cases
            # differ only in that value, so a remedy that dropped or collapsed it fails here.
            check(cid + '.unmet-remedy-carries-the-native-cause',
                  any(exp['unmetRemedyContains'] in u['remedy'] for u in plan['descriptor']['unmetPreconditions']),
                  str([u['remedy'] for u in plan['descriptor']['unmetPreconditions']]))
"""
assert s.count(OLD2) == 1
s = s.replace(OLD2, NEW2)

# --- new controls, beside the existing repair requirement controls --------------------------
ANCHOR = """check('repair.evidence-requirement-unregistered-relation-refused',
      _repair_requirement_refusal({'relation': 'not-a-relation', 'minResolution': 'resolved-target'}) is not None)
"""
CONTROLS = '''check('repair.evidence-requirement-unregistered-relation-refused',
      _repair_requirement_refusal({'relation': 'not-a-relation', 'minResolution': 'resolved-target'}) is not None)
# CB6-MUST-1. EvidenceRequirement.deficiency used to name D9Deficiency, which cannot express four of
# the nine outcomes its only producer (native section 4.6 sufficiency_v2) emits. These controls hold
# the three things the repair must keep separate: the NATIVE per-requirement outcome vocabulary, the
# D9 termination vocabulary, and the presence law that ties the value to `satisfied`.
_NATIVE_DEFICIENCIES = M.NATIVE_SUFFICIENCY_DEFICIENCIES
_D9_DEFICIENCIES = SCHEMAS[U + 'common']['$defs']['D9Deficiency']['enum']
_MIRROR = SCHEMAS[U + 'common']['$defs']['NativeSufficiencyDeficiency']['enum']
check('repair.sufficiency-vocabulary-mirrors-the-native-authority-exactly',
      _MIRROR == _NATIVE_DEFICIENCIES, str(_MIRROR) + ' != ' + str(_NATIVE_DEFICIENCIES))
check('repair.evidence-requirement-names-the-native-vocabulary-not-d9',
      SCHEMAS[U + 'repair']['$defs']['EvidenceRequirement']['properties']['deficiency']['$ref']
      == U + 'common#/$defs/NativeSufficiencyDeficiency')
check('repair.evidence-requirement-deficiency-names-its-vocabulary-authority',
      SCHEMAS[U + 'repair']['$defs']['EvidenceRequirement']['properties']['deficiency']
      ['x-opensip-vocabulary']['authority'] == 'native/native-evidence.schemas.v2.json#/$defs/DeficiencyV2')
# The four members that made the former typing unrepresentable, named one by one rather than counted.
_FOUR_WITHOUT_A_D9_MEMBER = ['derivation-policy-unmet', 'external-consumers-unknown',
                             'input-closure-incomplete', 'resolution-incomplete']
check('repair.the-four-successor-outcomes-have-no-d9-deficiency-member',
      all(m not in _D9_DEFICIENCIES for m in _FOUR_WITHOUT_A_D9_MEMBER)
      and all(m in _NATIVE_DEFICIENCIES for m in _FOUR_WITHOUT_A_D9_MEMBER))
check('repair.neither-single-vocabulary-covers-all-nine-native-outcomes',
      not set(_NATIVE_DEFICIENCIES) <= set(_D9_DEFICIENCIES)
      and not set(_NATIVE_DEFICIENCIES) <= set(SCHEMAS[U + 'common']['$defs']['DomainDetailCode']['enum'])
      and set(_NATIVE_DEFICIENCIES) <= (set(_D9_DEFICIENCIES)
                                        | set(SCHEMAS[U + 'common']['$defs']['DomainDetailCode']['enum'])))
check('repair.d9-deficiency-was-not-widened-to-carry-per-requirement-outcomes',
      _D9_DEFICIENCIES == ['none', 'required-relation-missing', 'provider-unavailable',
                           'language-tier-unsupported', 'budget-exhausted', 'confidence-floor-unmet',
                           'convergence-exhausted', 'baseline-recipe-unsupported',
                           'verdict-indeterminate', 'query-completeness-unmet'])
_ER_BASE = {'relation': 'imports', 'minResolution': 'resolved-target', 'completeness': 'complete'}
for _m in _NATIVE_DEFICIENCIES:
    must_valid('repair.evidence-requirement-admits-native-outcome.' + _m,
               U + 'repair#/$defs/EvidenceRequirement', dict(_ER_BASE, satisfied=False, deficiency=_m))
for _m in ('none', 'verdict-indeterminate', 'convergence-exhausted', 'query-completeness-unmet'):
    must_invalid('repair.evidence-requirement-refuses-d9-only-spelling.' + _m,
                 U + 'repair#/$defs/EvidenceRequirement', dict(_ER_BASE, satisfied=False, deficiency=_m))
must_valid('repair.evidence-requirement-satisfied-omits-the-field',
           U + 'repair#/$defs/EvidenceRequirement', dict(_ER_BASE, satisfied=True))
must_invalid('repair.evidence-requirement-satisfied-must-not-carry-a-deficiency',
             U + 'repair#/$defs/EvidenceRequirement',
             dict(_ER_BASE, satisfied=True, deficiency='resolution-incomplete'))
must_invalid('repair.evidence-requirement-unsatisfied-must-carry-a-deficiency',
             U + 'repair#/$defs/EvidenceRequirement', dict(_ER_BASE, satisfied=False))
# The same law again at the producer/consumer BOUNDARY, so a host that skips schema validation is
# still held to it. `admit_evidence_requirement` returns the exact cause, never a boolean.
def _requirement_admission(req):
    try:
        return ('ADMIT', M.admit_evidence_requirement(req))
    except M.Refusal as exc:
        return ('REFUSE', exc.remedy)
check('repair.boundary-returns-the-exact-cause-not-a-boolean',
      _requirement_admission(dict(_ER_BASE, satisfied=False, deficiency='resolution-incomplete'))
      == ('ADMIT', 'resolution-incomplete'))
check('repair.boundary-returns-none-for-a-satisfied-requirement',
      _requirement_admission(dict(_ER_BASE, satisfied=True)) == ('ADMIT', None))
for _bad, _key in ((dict(_ER_BASE, satisfied=True, deficiency='resolution-incomplete'),
                    'native.sufficiency-outcome-on-satisfied-requirement'),
                   (dict(_ER_BASE, satisfied=False), 'native.sufficiency-outcome-missing'),
                   (dict(_ER_BASE, satisfied=False, deficiency='verdict-indeterminate'),
                    'native.sufficiency-outcome-not-a-native-outcome'),
                   (dict(_ER_BASE, satisfied=False, deficiency='none'),
                    'native.sufficiency-outcome-not-a-native-outcome')):
    _outcome, _reason = _requirement_admission(_bad)
    check('repair.boundary-refuses.' + _key + '.' + str(_bad.get('deficiency')),
          _outcome == 'REFUSE' and _key in _reason, str(_outcome) + ':' + str(_reason))
'''
assert s.count(ANCHOR) == 1
s = s.replace(ANCHOR, CONTROLS)
P.write_text(s, encoding='utf-8')
print('ok')
