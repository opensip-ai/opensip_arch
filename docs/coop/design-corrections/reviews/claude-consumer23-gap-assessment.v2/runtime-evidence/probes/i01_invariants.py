"""I01 — invariants over v1 assessment.json and assessment.md against the receipts they cite: digests, classifications, the reopen
answer, carried obligations, the corrected patch standing, and every numeric or code claim the markdown states."""
import hashlib, json, os, re

V1 = '/tmp/opensip-design-corrections/claude-consumer23-gap-assessment.v1'
V2 = '/tmp/opensip-design-corrections/claude-consumer23-gap-assessment.v2'
ROOT = '/tmp/opensip-design-corrections'
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
A = json.load(open(os.path.join(V1, 'assessment.json')))
MD = open(os.path.join(V1, 'assessment.md'), encoding='utf-8').read() if os.path.isfile(os.path.join(V1, 'assessment.md')) else None
p05 = json.load(open(os.path.join(V2, 'receipts/p05-successor-rehearsal2.json')))
C, bad = {}, []


def chk(name, cond, obs=None):
    C[name] = {'passed': bool(cond), 'observed': obs}
    print('%-92s %s' % (name, 'OK' if cond else 'FAIL'))
    if not cond:
        bad.append(name)


chk('subject manifest sha', A['provenance']['subject']['sha256'] == 'a729406b9de0d865294884f7575ea943c0935437091389e2acebe8e5aedb4235')
chk('consumer report sha equals the pinned final-report digest', A['provenance']['consumerReport']['sha256'] == '77cfab1f6f2cea89a9b8d301e725ec69314e6b94298b0707e565305fd9c66a66'
    == sha(os.path.join(V1, 'consumer23-interim-review.json')))
chk('three findings with the stated classifications', A['findings']['V23-S1']['classification'].startswith('REAL SOURCE INCONSISTENCY')
    and A['findings']['V23-S2']['classification'].startswith('REAL SOURCE INCONSISTENCY') and A['findings']['V23-S3']['classification'].startswith('REAL BUT NARROW NORMATIVE GAP'))
chk('S2 rejects an invented per-requirement distinction', 'NOT a lawful per-requirement' in A['findings']['V23-S2']['classification'])
chk('budget mapping mismatch recorded with measured values', A['findings']['V23-S2']['budgetMappingMismatch']['observed']['modelRunTermination'] == 'VERDICT.INDETERMINATE'
    and A['findings']['V23-S2']['budgetMappingMismatch']['observed']['d9OwnerCode'] == 'COVERAGE.BUDGET_EXHAUSTED')
chk('helper-versus-full-D9 limitations recorded', len(A['findings']['V23-S2']['helperVersusFullD9Limitations']) >= 4)
chk('own v1 patch schema edit corrected, with evidence', 'native-evidence.schemas.v2.json' in A['findings']['V23-S2']['correctionToMyOwnV1Patch']['finding']
    and A['findings']['V23-S2']['correctionToMyOwnV1Patch']['evidence']['variantAReplay']['sameOutcomesAsFrozen36'] == p05['variantA']['sameOutcomesAsFrozen36'])
chk('recommended patch file digest matches', A['recommendedSuccessor']['patch']['sha256'] == sha(os.path.join(V2, A['recommendedSuccessor']['patch']['path'])))
chk('recommended patch leaves native schema bytes unchanged', 'docs/coop/design-corrections/native/native-evidence.schemas.v2.json' not in A['recommendedSuccessor']['patch']['files'])
chk('layer4 not claimed retainable', A['recommendedSuccessor']['layer4InputsTouched'] and any('planning input layer' in x for x in A['recommendedSuccessor']['alsoOwedOutsideThePatch']))
chk('reopen answer YES without MUST', A['doesSource36AcceptanceReopen']['answer'] == 'YES' and 'No MUST' in A['doesSource36AcceptanceReopen']['explanation'])
co = A['carriedObligations']
chk('carried obligations exact', co['productGates'] == {'count': 32, 'performed': 0, 'condition5': 'NOT MET'} and co['plannedRecoveryCases'] == {'count': 54, 'executed': 0}
    and '13' in co['TCB-SCOPE-01'] and co['condition2Obligations'] == 28 and 'no final application' in co['authority'])
chk('standing grants nothing', 'NOT the final application' in A['standing'] and 'Grants no application outcome' in A['standing'])
mism = [k for k, h in A['receipts'].items() if sha(os.path.join(ROOT, k)) != h]
chk('every cited receipt digest still matches', not mism, mism)
chk('rehearsal suite outcomes copied exactly', A['rehearsal']['p05']['variantB']['suites'] == {x['name']: x['returncode'] for x in p05['suites']}
    and A['rehearsal']['p05']['variantB']['planningExitCodes'] == p05['planningExitCodes'])
if MD is not None:
    toks = ['a729406b', '77cfab1f', 'V23-S1', 'V23-S2', 'V23-S3', 'QUERY.PARAMS_MALFORMED', 'QUERY.ENDPOINT_AMBIGUOUS', 'COVERAGE.REQUIRED_RELATION_MISSING',
            'COVERAGE.LANGUAGE_TIER_UNSUPPORTED', 'COVERAGE.CONFIDENCE_FLOOR_UNMET', 'COVERAGE.BUDGET_EXHAUSTED', 'VERDICT.INDETERMINATE', 'evidence.missing',
            'GraphRequestEndpoint', 'publicD9Termination', 'secondaryDeficiencies', 'TCB-SCOPE-01', '32', '54', 'NOT MET', 'reopen', A['recommendedSuccessor']['patch']['sha256'][:8],
            'layer4', 'not the final application review']
    for t in toks:
        chk('md states %r' % t, t.lower() in MD.lower())
    for n in re.findall(r'receipts/([\w.\-]+\.json)', MD):
        if not (os.path.isfile(os.path.join(V1, 'receipts', n)) or os.path.isfile(os.path.join(V2, 'receipts', n))):
            chk('md cites existing receipt %s' % n, False)
    for name, rc in A['rehearsal']['p05']['variantB']['suites'].items():
        if rc != 0:
            chk('md discloses non-zero rehearsal suite %s' % name, name in MD)
C['failed'] = bad
C['assessmentJsonSha256'] = sha(os.path.join(V1, 'assessment.json'))
C['assessmentMdSha256'] = sha(os.path.join(V1, 'assessment.md')) if MD is not None else None
os.makedirs(os.path.join(V2, 'receipts'), exist_ok=True)
json.dump(C, open(os.path.join(V2, 'receipts/i01-invariants.json'), 'w'), indent=1, default=str)
print('\nchecks %d failed %d | assessment.json %s | assessment.md %s' % (len([v for v in C.values() if isinstance(v, dict)]), len(bad), C['assessmentJsonSha256'], C['assessmentMdSha256']))
