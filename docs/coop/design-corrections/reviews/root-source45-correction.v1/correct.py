"""Publish the exact pre-analysis closedWorld value; preserve frozen source44.
Architecture/reference correction only. No acceptance, activation or product code.
"""
from pathlib import Path
import copy
import hashlib
import json

B = Path('/tmp/opensip-design-corrections')
T = B / 'source44-closed-world-successor.v1/source'
O = B / 'root-source45-correction.v1'
DC = 'docs/coop/design-corrections/'
BT = chr(96)
VALUE = {'exportsClosed': 'unknown', 'entryPointsRecognized': 'none',
         'nonliteralLoading': 'none', 'externalConsumers': 'unknown',
         'dynamicDispatch': 'not-applicable', 'reasons': ['no-manifest'],
         'deadCodeRepairEligible': False}
ROWS = []


def save(rel, raw):
    p = T / rel
    old = p.read_bytes()
    assert old != raw
    q = O / 'before' / rel
    assert not q.exists()
    q.parent.mkdir(parents=True, exist_ok=True)
    q.write_bytes(old)
    p.write_bytes(raw)
    ROWS.append({'path': rel, 'beforeSha256': hashlib.sha256(old).hexdigest(),
                 'afterSha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)})


def dump(j):
    return (json.dumps(j, indent=2) + '\n').encode()


rel = 'docs/v2/contracts/product-v1/native-evidence.md'
s = (T / rel).read_text()
old = f'    - {BT}closedWorld{BT}: {BT}closed_world_v2{BT} over no manifest, no recognized entry points and no edges,\n      with external consumers {BT}unknown{BT};'
new = f'''    - {BT}closedWorld{BT}: exactly the complete value below, for both languages. Its machine-readable
      owner is {BT}provider-startup.schemas.v1.json#/x-opensip-startup-law/preAnalyzeUnavailable/hostConversionClosedWorld{BT};
      no call to an unpublished helper or choice of reason strings is required:

      {BT * 3}json
'''
new += '\n'.join('      ' + line for line in json.dumps(VALUE, indent=2).splitlines())
new += f'''
      {BT * 3}

      This fixed value applies only to this pre-analysis host conversion. It records absent manifest
      and analysis observations; it does not prove that the repository has no dynamic loading or
      dispatch. Coverage remains {BT}unknown{BT}, and dead-code repair remains ineligible.
'''.rstrip()
assert s.count(old) == 1
save(rel, s.replace(old, new).encode())

rel = DC + 'native/provider-startup.schemas.v1.json'
j = json.loads((T / rel).read_bytes())
law = j['x-opensip-startup-law']['preAnalyzeUnavailable']
old = 'closedWorld = closed_world_v2(no manifest, entry points none, no edges, externalConsumers unknown)'
assert law['hostConversion'].count(old) == 1
law['hostConversion'] = law['hostConversion'].replace(old, 'closedWorld = exactly the complete hostConversionClosedWorld value published alongside this law (native-evidence section 9.7), identically for both languages')
assert 'hostConversionClosedWorld' not in law
law['hostConversionClosedWorld'] = VALUE
save(rel, dump(j))

rel = DC + 'native/native_evidence_model.v2.py'
s = (T / rel).read_text()
old = '"closedWorld": closed_world_v2(None, {"source": "none", "state": "none"}, [], "unknown"),'
new = '"closedWorld": copy.deepcopy(STARTUP.LAW["preAnalyzeUnavailable"]["hostConversionClosedWorld"]),'
assert s.count(old) == 1
s = s.replace(old, new)
s = s.replace('# completeness_from_stage, closed_world_v2, admit_coverage_result_v3, stage_authority and run_termination - and reads',
              '# completeness_from_stage, admit_coverage_result_v3, stage_authority and run_termination - with the published\n# exact hostConversionClosedWorld record, and reads')
save(rel, s.encode())

rel = DC + 'native/native-cases.v2.json'
j = json.loads((T / rel).read_bytes())
changed_cases = []
for c in j['cases']:
    if c['id'] not in ('startup-ts2-pre-analyze-unavailable-host-derives-provider-unavailable-coverage',
                       'startup-rust3-pre-analyze-unavailable-host-derives-provider-unavailable-coverage'):
        continue
    args = c['steps'][0]['args']
    inp = j['fixtures'][args['inputs'].removeprefix('$fixtures.')]
    for si, stage in enumerate(inp['plannedStages']):
        for ki, _ in enumerate(stage['scopeDescriptors']):
            c['expect'][f'$r.hostConversion.stages.{si}.coverage.{ki}.payload.entry.closedWorld'] = copy.deepcopy(VALUE)
    changed_cases.append(c['id'])
assert len(changed_cases) == 2, changed_cases
save(rel, dump(j))

rel = DC + 'native/check_native_evidence.v2.py'
s = (T / rel).read_text()
old = '    startup_law = startup_doc["x-opensip-startup-law"]\n'
new = old + '''    # M-s44-1: the pre-analysis conversion commits this exact complete record. This is
    # a conversion-specific law, not a restriction on other lawful ClosedWorldV2 records.
    conversion_closed_world = {"exportsClosed": "unknown", "entryPointsRecognized": "none",
                              "nonliteralLoading": "none", "externalConsumers": "unknown",
                              "dynamicDispatch": "not-applicable", "reasons": ["no-manifest"],
                              "deadCodeRepairEligible": False}
    if startup_law["preAnalyzeUnavailable"].get("hostConversionClosedWorld") != conversion_closed_world:
        startup_faults.append("pre-analysis closedWorld differs from the exact section 9.7 record")
    if model.closed_world_v2(None, {"source": "none", "state": "none"}, [], "unknown") != conversion_closed_world:
        startup_faults.append("pre-analysis closedWorld differs from the retained helper's no-observation result")
    marker = "hostConversionClosedWorld"
    section97 = contract_text[contract_text.index("### 9.7"):contract_text.index("## 10.")]
    fence = chr(96) * 3
    block = re.search(fence + r"json\\s*(\\{.*?\\})\\s*" + fence, section97, re.S)
    if marker not in section97 or block is None or json.loads(block.group(1)) != conversion_closed_world:
        startup_faults.append("section 9.7 does not publish the exact complete pre-analysis closedWorld record")
'''
assert s.count(old) == 1
save(rel, s.replace(old, new).encode())

# A-s44-1: retain the shared capture law while naming each historical language payload.
rel = DC + 'foundation/provider-target-attribution-return.schema.v2.json'
j = json.loads((T / rel).read_bytes())
law = j['x-opensip-return-law']
old = 'Historical FactBatchV2/FactCandidateV1 stay closed when the token is absent.'
assert old in law['standing']
law['standing'] = law['standing'].replace(old, 'With the token absent, the historical per-language payload remains closed: delivery.v2 FactBatchV1 for typescript-semantic, rust-provider-protocol.v2 FactBatchV2 for rust-semantic, each with unchanged FactCandidateV1.')
old = 'When the token is absent, FactBatchV2 remains and occupancy is unknown except exact-id ephemeral.'
assert old in law['boundary']['compilerWorkerTransport']
law['boundary']['compilerWorkerTransport'] = law['boundary']['compilerWorkerTransport'].replace(old, 'When the token is absent, delivery.v2 FactBatchV1 remains for typescript-semantic and rust-provider-protocol.v2 FactBatchV2 for rust-semantic; occupancy is unknown except exact-id ephemeral.')
old = law['missingAndIncomplete']['missingToken']
assert 'FactBatchV2' in old
law['missingAndIncomplete']['missingToken'] = old.replace('FactBatchV2', 'the historical per-language payload (delivery.v2 FactBatchV1 for typescript-semantic; rust-provider-protocol.v2 FactBatchV2 for rust-semantic)')
save(rel, dump(j))

(O / 'correction.json').write_bytes(dump({'standing': 'Authored source successor only; current source44 remains frozen. Independent review and reference verification pending.',
    'issues': ['M-s44-1', 'A-s44-1'], 'files': ROWS, 'closedWorld': VALUE,
    'caseCountChanged': False, 'strengthenedCases': changed_cases,
    'registeredSchemaChanged': False, 'productImplementation': False,
    'scope': 'Fixed pre-analysis conversion value, published in prose and machine-readable law; reference reads it. General closed-world law and other CoverageResultV3 values are unchanged.'}))
print(json.dumps({'files': len(ROWS), 'strengthenedCases': changed_cases, 'reviewPending': True}))
