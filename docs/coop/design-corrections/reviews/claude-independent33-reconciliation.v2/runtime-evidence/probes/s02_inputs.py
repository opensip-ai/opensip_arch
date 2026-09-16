"""S02 — gather the measured records this correction needs: my v1 full-Run evidence rows, the three
residual rows root names, and the composition-delta facts already measured. No new suites."""
import json, os

V1 = '/tmp/opensip-design-corrections/claude-independent33-reconciliation.v1'
V33 = '/tmp/opensip-design-corrections/claude-independent-design.v33'
PKG = '/tmp/opensip-design-corrections/claude-author-package-successor.v10'
OUT = '/tmp/opensip-design-corrections/claude-independent33-reconciliation.v2/receipts'
R = {}
V = json.load(open(os.path.join(V1, 'review.json')))


def walk(o, path=''):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from walk(v, path + '.' + k)
    elif isinstance(o, list):
        if o and isinstance(o[0], dict) and 'case' in o[0] and 'runId' in o[0]:
            yield path, o
        else:
            for i, v in enumerate(o):
                yield from walk(v, '%s[%d]' % (path, i))


print('=== full-Run evidence arrays in my v1 record ===')
R['fullRunArrays'] = {}
for p, arr in walk(V):
    R['fullRunArrays'][p] = arr
    print('--- %s (%d rows)' % (p, len(arr)))
    for r in arr:
        print('   %-62s %-14s %s' % (r['case'][:62], r.get('verdict'),
                                     json.dumps(r.get('causePairs') or r.get('executionCausePairs'), default=str)[:90]))

print('\n=== the three residual rows root names ===')
R['residualRows'] = {}
for rid in ('RES-EP13-01', 'RES-EP13-07', 'RES-EP13-15'):
    row = V['evaluationResidualDispositions'][rid]
    R['residualRows'][rid] = row
    print('\n--- %s' % rid)
    for k in ('disposition', 'currentOwnerSelectors', 'ownerSelectorsChangedIn32to33',
              'ownerSelectorsResolveInFrozen33', 'reviewStatus', 'independentGradeAwardedHere',
              'sharedAssumption', 'limits', 'currentStatusOn33', 'priorStatusOn32'):
        if k in row:
            print('   %-32s %s' % (k, str(row[k])[:340].replace('\n', ' ')))

print('\n=== composition-contract delta facts already measured ===')
p01 = json.load(open(os.path.join(V33, 'receipts', 'p01-delta.json')))
comp = [c for c in p01['changed'] if 'evaluator-composition-contract' in c['path']]
nat = [c for c in p01['changed'] if 'native-evidence.md' in c['path']]
R['compositionDeltaRow'] = comp
R['nativeDeltaRow'] = nat
print('composition:', json.dumps(comp, default=str)[:400])
print('native     :', json.dumps(nat, default=str)[:400])
R['compositionAssessedInV1'] = {
    'parentCompositionProviderFallback':
        V['sourceChangeAssessment']['executionInputsLaw'].get('parentCompositionProviderFallback'),
}
print('\nmy v1 assessment of the composition change:')
print(json.dumps(R['compositionAssessedInV1'], default=str, indent=1)[:1600])

# package10 residual assessment rows for these three ids (already measured in v1/r02)
era = os.path.join(PKG, 'evaluation-residual-author-assessment.json')
d = json.load(open(era))
R['packageResidualRows'] = {}
for it in d.get('items', []):
    if it.get('id') in ('RES-EP13-01', 'RES-EP13-07', 'RES-EP13-15'):
        R['packageResidualRows'][it['id']] = it
        print('\n--- package10 assessment row %s' % it['id'])
        for k, v in it.items():
            print('   %-26s %s' % (k, str(v)[:300].replace('\n', ' ')))
json.dump(R, open(os.path.join(OUT, 's02-inputs.json'), 'w'), indent=1, default=str)
print('\nwrote s02-inputs.json')
