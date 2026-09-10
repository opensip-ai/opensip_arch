import pathlib

P = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v1/work/'
                 'docs/coop/design-corrections/check-integration.py')
s = P.read_text(encoding='utf-8')

ANCHOR = """refuses('the-d9-mapped-value-is-refused-in-the-consumer-record',
        lambda: M.W.validate_import_record('workflows/schemas/repair.schema.json',
                                           '#/$defs/EvidenceRequirement',
                                           dict(_carried, deficiency='verdict-indeterminate')))
"""
NEW = '''refuses('the-d9-mapped-value-is-refused-in-the-consumer-record',
        lambda: M.W.validate_import_record('workflows/schemas/repair.schema.json',
                                           '#/$defs/EvidenceRequirement',
                                           dict(_carried, deficiency='verdict-indeterminate')))

# CB6-ADV-3. The successor D9 artifact is a LIVE, MANDATORY cross-unit obligation, and the correct
# handling of it is to carry the obligation rather than repin the historical evidence. These
# controls hold all three halves at once: the inherited artifact keeps its exact bytes and still
# omits the cause; the selected successor composition DOES carry it and is what the product source
# runs on; and the mismatch is disclosed and attributed rather than silently reconciled.
INHERITED_D9 = M.C.parse((HERE.parent / 'artifacts/d9-exit-contract.v1.14.json').read_bytes())
_inherited_causes = INHERITED_D9['scenarioAxesSchema']['properties']['faultCause']['enum']
check('the-inherited-d9-artifact-still-omits-the-host-invariant-cause',
      'host-invariant' not in _inherited_causes
      and 'host-invariant' not in INHERITED_D9['codeMaps']['faultCauseToErrorCode'])
check('the-inherited-artifact-already-published-the-error-code-with-no-preimage',
      'SYSTEM.OUTCOME.ILLEGAL_STATE' in INHERITED_D9['codeVocabulary']['errorCodes']
      and 'SYSTEM.OUTCOME.ILLEGAL_STATE' not in INHERITED_D9['codeMaps']['faultCauseToErrorCode'].values())
check('the-selected-successor-composition-carries-the-cause-the-inherited-artifact-cannot',
      'host-invariant' in common_schema['$defs']['D9FaultCause']['enum']
      and set(_inherited_causes) | {'host-invariant'}
          == set(common_schema['$defs']['D9FaultCause']['enum']))
check('the-successor-map-stays-injective-and-adds-no-error-code',
      len(set(INHERITED_D9['codeMaps']['faultCauseToErrorCode'].values()))
      == len(INHERITED_D9['codeMaps']['faultCauseToErrorCode'])
      and 'SYSTEM.OUTCOME.ILLEGAL_STATE' in INHERITED_D9['codeVocabulary']['errorCodes'])
check('the-cross-unit-obligation-is-disclosed-and-attributed-not-reconciled-by-repinning',
      'publishing the successor D9 artifact belongs to that unit'
      in native_schemas['x-opensip-public-route-registry']['hostInvariantSuccessor']
      and 'HISTORICAL and unchanged'
      in common_schema['$defs']['D9FaultCause']['description'])
'''
assert s.count(ANCHOR) == 1
P.write_text(s.replace(ANCHOR, NEW), encoding='utf-8')
print('ok')
