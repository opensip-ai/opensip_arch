"""Update the cross-unit controls for the two-plane requirement and the corrected map."""
import pathlib

P = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v2/work/'
                 'docs/coop/design-corrections/check-integration.py')
s = P.read_text(encoding='utf-8')

OLD = """check('native-sufficiency-mirror-names-its-authority',
      common_schema['$defs']['NativeSufficiencyDeficiency']['x-opensip-vocabulary']['authority']
      == 'native/native-evidence.schemas.v2.json#/$defs/DeficiencyV2'
      and repair_schema['$defs']['EvidenceRequirement']['properties']['deficiency']
          ['x-opensip-vocabulary']['authority']
      == 'native/native-evidence.schemas.v2.json#/$defs/DeficiencyV2')
"""
NEW = """check('native-sufficiency-mirror-names-its-authority',
      common_schema['$defs']['NativeSufficiencyDeficiency']['x-opensip-vocabulary']['authority']
      == 'native/native-evidence.schemas.v2.json#/$defs/DeficiencyV2'
      and repair_schema['$defs']['EvidenceRequirement']['properties']['deficiency']
          ['x-opensip-vocabulary']['nativePlaneAuthority']
      == 'native/native-evidence.schemas.v2.json#/$defs/DeficiencyV2')
# CX-BV6-03. Repair admits requirements over BOTH evidence planes, and the imported plane is owned
# by the imported-evidence document, not by native section 4.6. These controls hold the two
# vocabularies disjoint, hold each mirror to its own authority, and hold the boundary to deciding
# the plane from REGISTRY MEMBERSHIP rather than from the value.
imported_schema = M.C.parse((HERE / 'workflows/schemas/imported-evidence.schema.json').read_bytes())
IMPORTED_LAW = imported_schema['x-opensip-imported-requirement-law']
check('imported-requirement-mirror-is-exact-and-names-its-own-authority',
      common_schema['$defs']['ImportedRequirementDeficiency']['enum']
      == list(IMPORTED_LAW['precedence'])
      and set(IMPORTED_LAW['precedence']) == set(IMPORTED_LAW['outcomes'])
      and common_schema['$defs']['ImportedRequirementDeficiency']['x-opensip-vocabulary']['authority']
          .endswith('x-opensip-imported-requirement-law/outcomes'))
check('the-two-requirement-planes-are-disjoint-vocabularies',
      not (set(NATIVE_DEFICIENCY_V2) & set(IMPORTED_LAW['precedence'])))
check('the-repair-field-admits-both-plane-vocabularies-and-only-those',
      [b['$ref'].rsplit('/', 1)[1] for b in
       repair_schema['$defs']['EvidenceRequirement']['properties']['deficiency']['oneOf']]
      == ['NativeSufficiencyDeficiency', 'ImportedRequirementDeficiency'])
check('the-imported-plane-relations-are-exactly-the-imported-registry',
      set(imported_schema['x-opensip-evidence-relation-registry']['relations'])
      == {'runtime-observation', 'history-change'}
      and all(M.W.requirement_plane(r) == 'imported'
              for r in imported_schema['x-opensip-evidence-relation-registry']['relations'])
      and M.W.requirement_plane('references') == 'native')
# The producers really are different functions over different domains, and neither answers for the
# other. Root's contrast established the domains differ; these controls establish the ROUTING.
_imp_req = {'relation': 'runtime-observation', 'minResolution': 'observed',
            'completeness': 'complete', 'targets': ['src/a.ts']}
_imp_out = M.W.imported_requirement_outcome(
    _imp_req, {'available': True, 'consumable': False, 'windowSatisfiesRequirement': True,
               'observability': {'src/a.ts': 'observed-hit'}})
check('the-imported-producer-emits-an-imported-outcome-for-an-imported-relation',
      _imp_out['satisfied'] is False and _imp_out['deficiency'] == 'import-unmapped-only')
check('the-repair-record-carries-that-exact-imported-value-on-its-own-plane',
      M.W.admit_evidence_requirement(dict(_imp_req, satisfied=False,
                                          deficiency=_imp_out['deficiency']))
      == ('imported', 'import-unmapped-only'))
refuses('a-native-relation-cannot-carry-an-imported-outcome',
        lambda: M.W.admit_evidence_requirement(
            {'relation': 'references', 'minResolution': 'resolved-binding',
             'completeness': 'complete', 'satisfied': False, 'deficiency': 'import-unmapped-only'}))
refuses('an-imported-relation-cannot-carry-a-native-outcome',
        lambda: M.W.admit_evidence_requirement(
            dict(_imp_req, satisfied=False, deficiency='resolution-incomplete')))
refuses('the-imported-producer-refuses-a-native-relation',
        lambda: M.W.imported_requirement_outcome(
            {'relation': 'references', 'minResolution': 'resolved-binding',
             'completeness': 'complete', 'targets': ['src/a.ts']}, {'available': True}))
"""
assert s.count(OLD) == 1
s = s.replace(OLD, NEW)

OLD2 = """check('the-repair-record-carries-that-exact-producer-value',
      M.W.admit_evidence_requirement(_carried) == 'resolution-incomplete')
"""
NEW2 = """check('the-repair-record-carries-that-exact-producer-value',
      M.W.admit_evidence_requirement(_carried) == ('native', 'resolution-incomplete'))
"""
assert s.count(OLD2) == 1
s = s.replace(OLD2, NEW2)
P.write_text(s, encoding='utf-8')
print('ok')
