"""P03 — verify root's five RR31 review-record findings against my ACTUAL v31 review.json,
rather than accepting them on assertion."""
import json, os

V31 = '/tmp/opensip-design-corrections/claude-independent-design.v31/review.json'
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v32/receipts'
R = json.load(open(V31))
F = {}

# RR31-01
inh = R['inheritedResidualDispositions']
drs = {k: v for k, v in inh.items() if k.startswith('DR-011-R')}
empty = [k for k, v in drs.items() if not v.get('currentOwnerFiles')]
F['RR31_01'] = {'drRowCount': len(drs), 'rowsWithEmptyCurrentOwnerFiles': sorted(empty),
                'count': len(empty),
                'rr27_03ClaimedEveryRowNamesPaths': True,
                'rootIsCorrect': len(empty) == 16}
print('RR31-01: DR-011-R rows=%d with empty currentOwnerFiles=%d -> root correct: %s'
      % (len(drs), len(empty), F['RR31_01']['rootIsCorrect']))

# RR31-02
row = R['evaluationResidualDispositions']['RES-EP13-13']
F['RR31_02'] = {'currentStatusMentionsChange': 'changed at 27->28' in row['currentStatusOn31'],
                'readingStanding': row['readingStanding'],
                'standingSaysSameBytes': 'byte-equal' in row['readingStanding'],
                'rootIsCorrect': ('changed' in row['currentStatusOn31']
                                  and 'byte-equal' in row['readingStanding'])}
print('RR31-02: status notes the change=%s ; standing says byte-equal=%s -> contradiction: %s'
      % (F['RR31_02']['currentStatusMentionsChange'], F['RR31_02']['standingSaysSameBytes'],
         F['RR31_02']['rootIsCorrect']))

# RR31-03
a7 = next(a for a in R['advisories'] if a['id'] == 'A-7')
F['RR31_03'] = {'a7WhyNotAShould': a7['why_not_a_should'],
                'claimsFileNotInDelta': 'not in my 27->31 delta' in a7['why_not_a_should'],
                'nativeSchemaActuallyChanged27to31': None}
delta31 = {c['path'] for c in R['delta27to31']['changedPaths']} if isinstance(
    R['delta27to31']['changedPaths'][0], dict) else set(R['delta27to31']['changedPaths'])
NS = 'docs/coop/design-corrections/native/native-evidence.schemas.v2.json'
F['RR31_03']['nativeSchemaActuallyChanged27to31'] = NS in delta31
F['RR31_03']['rootIsCorrect'] = (F['RR31_03']['claimsFileNotInDelta']
                                 and F['RR31_03']['nativeSchemaActuallyChanged27to31'])
print('RR31-03: A-7 claims file-not-in-delta=%s ; native schema WAS in my 27->31 delta=%s -> root correct: %s'
      % (F['RR31_03']['claimsFileNotInDelta'], F['RR31_03']['nativeSchemaActuallyChanged27to31'],
         F['RR31_03']['rootIsCorrect']))

# RR31-04
a8 = next(a for a in R['advisories'] if a['id'] == 'A-8')
F['RR31_04'] = {'a8Suggestion': a8['suggestion'],
                'suggestsSupplying29or30Manifests': '29/30 manifests' in a8['suggestion']
                or 'manifests' in a8['suggestion'],
                'a8WasAnInputLimitNotSourceDefect': 'not a defect in source31' in a8['why_not_a_should']}
print('RR31-04: A-8 suggestion mentions manifests=%s ; framed as my input limit=%s'
      % (F['RR31_04']['suggestsSupplying29or30Manifests'], F['RR31_04']['a8WasAnInputLimitNotSourceDefect']))

# RR31-05
txt = json.dumps(R)
import re
hits = [m.group(0) for m in re.finditer(r'[^"]{0,160}precede[sd][^"]{0,160}', txt)]
F['RR31_05'] = {'orderingSentences': [h for h in hits if 'custody' in h or 'enumeration' in h][:4]}
print('\nRR31-05: my v31 ordering sentences:')
for h in F['RR31_05']['orderingSentences']:
    print('   ...', h[:230])

json.dump(F, open(os.path.join(OUT, 'p03-v31record.json'), 'w'), indent=1, default=str)
print('\nwrote p03-v31record.json')
