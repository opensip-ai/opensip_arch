import pathlib

P = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v1/work/'
                 'docs/coop/design-corrections/check-integration.py')
s = P.read_text(encoding='utf-8')

ANCHOR = """check('public-detail-registry-schema-parity', details == set(common_schema['$defs']['DomainDetailCode']['enum']))
"""
NEW = '''check('public-detail-registry-schema-parity', details == set(common_schema['$defs']['DomainDetailCode']['enum']))

# CB6-MUST-1. The per-requirement sufficiency OUTCOME crosses a unit boundary: native section 4.6
# `sufficiency_v2` produces it and the workflows repair EvidenceRequirement consumes it. The
# workflows bundle resolves only workflows URNs, so the native vocabulary is MIRRORED there; these
# controls hold the mirror to its authority and hold the three vocabularies apart.
native_schemas = M.C.parse((HERE / 'native/native-evidence.schemas.v2.json').read_bytes())
NATIVE_DEFICIENCY_V2 = native_schemas['$defs']['DeficiencyV2']['enum']
repair_schema = M.C.parse((HERE / 'workflows/schemas/repair.schema.json').read_bytes())
check('native-sufficiency-vocabulary-mirror-is-exact',
      common_schema['$defs']['NativeSufficiencyDeficiency']['enum'] == NATIVE_DEFICIENCY_V2)
check('native-sufficiency-mirror-names-its-authority',
      common_schema['$defs']['NativeSufficiencyDeficiency']['x-opensip-vocabulary']['authority']
      == 'native/native-evidence.schemas.v2.json#/$defs/DeficiencyV2'
      and repair_schema['$defs']['EvidenceRequirement']['properties']['deficiency']
          ['x-opensip-vocabulary']['authority']
      == 'native/native-evidence.schemas.v2.json#/$defs/DeficiencyV2')
check('native-sufficiency-outcome-is-not-the-d9-termination-vocabulary',
      set(NATIVE_DEFICIENCY_V2) - set(common_schema['$defs']['D9Deficiency']['enum'])
      == {'derivation-policy-unmet', 'external-consumers-unknown', 'input-closure-incomplete',
          'resolution-incomplete'})
check('the-native-registry-publishes-the-per-requirement-consumer-boundary',
      native_schemas['x-opensip-deficiency-cause-registry']['perRequirementConsumerBoundary']
      ['consumers'][0]['record']
      == 'workflows/schemas/repair.schema.json#/$defs/EvidenceRequirement')
# The producer really emits one of the four, and the consumer record really carries THAT value: a
# real sufficiency_v2 evaluation, not a hand-written string.
_uni_req = {'relation': 'references', 'minResolution': 'resolved-binding', 'completeness': 'complete',
            'quantifier': 'universal-negative', 'unresolvedEdgePolicy': 'forbid'}
_uni_view = {'references': {'resolution': 'resolved-binding', 'coverage': 'complete',
                            'resolutionCompleteness': {'state': 'partial', 'unresolvedEdgeCount': 2,
                                                       'unresolvedEdgeClasses': ['computed-member-access']}}}
_suff = M.N.sufficiency_v2(_uni_req, _uni_view)
check('sufficiency-v2-emits-resolution-incomplete-for-the-destructive-repair-case',
      _suff['satisfied'] is False and _suff['deficiency'] == 'resolution-incomplete')
_carried = {'relation': _uni_req['relation'], 'minResolution': _uni_req['minResolution'],
            'completeness': 'complete', 'satisfied': _suff['satisfied'],
            'deficiency': _suff['deficiency']}
check('the-repair-record-carries-that-exact-producer-value',
      M.W.admit_evidence_requirement(_carried) == 'resolution-incomplete')
M.W.validate_import_record('workflows/schemas/repair.schema.json',
                           '#/$defs/EvidenceRequirement', _carried)
check('the-carried-producer-value-is-schema-valid-in-the-consumer-record', True)
refuses('the-d9-mapped-value-is-refused-in-the-consumer-record',
        lambda: M.W.validate_import_record('workflows/schemas/repair.schema.json',
                                           '#/$defs/EvidenceRequirement',
                                           dict(_carried, deficiency='verdict-indeterminate')))
'''
assert s.count(ANCHOR) == 1
P.write_text(s.replace(ANCHOR, NEW), encoding='utf-8')
print('ok')
