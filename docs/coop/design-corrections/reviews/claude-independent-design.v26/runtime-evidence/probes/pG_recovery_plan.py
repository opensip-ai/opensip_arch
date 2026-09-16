"""PROBE G — complete traversal of commit-recovery-plan.v1.json (the 13-field private
association + the F00-F53 case inventory) with the joins I care about measured rather
than taken from prose."""
import json, os, re, collections

ROOT = '/tmp/opensip-design-corrections/candidate-subject.v26'
p = os.path.join(ROOT, 'docs/v2/architecture/commit-recovery-plan.v1.json')
d = json.load(open(p, encoding='utf-8'))
R = {}
R['standing'] = d['standing']
R['recordName'] = d['recordName']
R['required_fields'] = d['recordSchema']['required']
R['required_count'] = len(d['recordSchema']['required'])
R['properties_count'] = len(d['recordSchema']['properties'])
R['closed'] = d['recordSchema']['additionalProperties'] is False
R['fieldKinds'] = d['fieldKinds']
R['primaryKey'] = d['primaryKey']
R['uniqueKeys'] = d['uniqueKeys']
R['extraAdmissionRules'] = d['extraAdmissionRules']
R['conclusionStanding'] = d['conclusionStanding']
R['storeGenerationBinding_required'] = d['storeGenerationBindingSchema']['required']

cases = d['cases']
R['case_count'] = len(cases)
ids = [c['id'] for c in cases]
R['case_ids'] = ids
R['case_ids_contiguous_F00_F53'] = ids == ['F%02d' % i for i in range(54)]
R['case_row_keys'] = sorted(cases[0].keys())
R['conclusions'] = dict(collections.Counter(c.get('conclusion') for c in cases))
R['executed_values'] = dict(collections.Counter(str(c.get('executed')) for c in cases))
R['any_case_claims_executed'] = [c['id'] for c in cases if c.get('executed') not in (False, 'false', None)]

# journalSeq maximum must exclude the reserved terminal slot
js = d['recordSchema']['properties']['journalSeq']
R['journalSeq_maximum'] = js.get('maximum')
R['journalSeq_excludes_reserved_slot'] = js.get('maximum') == 9007199254740990
R['runId_pattern'] = d['recordSchema']['properties']['runId'].get('pattern')
R['operationRef_pattern'] = d['recordSchema']['properties']['operationRef'].get('pattern')
R['executionId_pattern'] = d['recordSchema']['properties']['executionId'].get('pattern')
R['commitSequence'] = d['recordSchema']['properties']['commitSequence']

# cross-owner: the carrier dispatch's declared owner split must partition the record
disp = json.load(open(os.path.join(
    ROOT, 'docs/coop/design-corrections/security/carrier-dispatch.v3.json'), encoding='utf-8'))
aj = disp['associationJoins']
sec = set(aj['carrierSideValuesOwnedBySecurity'])
sto = set(aj['storageSideValuesOwnedByStorage'])
req = set(d['recordSchema']['required'])
R['owner_split_partitions_record'] = (sec | sto | {'runId'}) == req
R['owner_split_overlap'] = sorted(sec & sto)
R['owner_split_unassigned'] = sorted(req - sec - sto - {'runId'})

print(json.dumps({k: v for k, v in R.items() if k not in ('case_ids',)}, indent=1)[:5200])
json.dump(R, open('/tmp/opensip-design-corrections/claude-independent-design.v26/receipts/probeG.json', 'w'), indent=1)
