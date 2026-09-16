import json
S = '/private/tmp/opensip-design-corrections/application-stage.v45.2/files/docs/coop/design-corrections/'
rm = json.load(open(S + 'readiness-row-map.v1.json'))
keys = set()
for r in rm['rows']:
    keys |= set(r)
print('row keys union', sorted(keys))
for r in rm['rows']:
    print('=' * 20, r['id'])
    for k in ['sourceObligation', 'sourceRequiredEvidence', 'disposition']:
        print(k + ':', r.get(k))
    for s in r['productSuccessors']:
        print('  succ', s['path'].split('/')[-1], s['sha256'][:12], s.get('sections'))
    print('  gates', r['releaseGates'])
    print('  grade', r.get('independentGrade'), r.get('designGrade'), 'qualified', r.get('productQualified'))
    ia = r.get('compatibleInheritedAccount')
    if ia: print('  inherited', ia.get('path'), ia.get('selector'), ia.get('sha256', '')[:12])
    for k in sorted(set(r) - {'id', 'sourceObligation', 'sourceRequiredEvidence', 'disposition', 'productSuccessors', 'releaseGates', 'independentGrade', 'designGrade', 'productQualified', 'compatibleInheritedAccount', 'effectiveWhen', 'independentDesignReview', 'independentApplicationGradeBinding', 'resolveInheritedSourcesAgainst'}):
        print('  EXTRA', k, json.dumps(r[k])[:3000])
print({k: v for k, v in rm.items() if k != 'rows'})
