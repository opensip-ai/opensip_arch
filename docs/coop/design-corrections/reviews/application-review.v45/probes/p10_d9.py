import json, hashlib
S = '/private/tmp/opensip-design-corrections/application-stage.v45.2/files/'
C = '/tmp/opensip-design-corrections/candidate-subject.v45/'
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def ptr(doc, pointer):
    if pointer in ('', '/'): return doc
    for part in pointer.lstrip('/').split('/'):
        part = part.replace('~1', '/').replace('~0', '~')
        doc = doc[int(part)] if isinstance(doc, list) else doc[part]
    return doc
ns = json.load(open(C + 'docs/coop/design-corrections/native/native-evidence.schemas.v2.json'))
reg = ns['x-opensip-public-route-registry']
print('successorArtifactObligation:', json.dumps(reg.get('successorArtifactObligation'), indent=1)[:4000])
cs = json.load(open(C + 'docs/coop/design-corrections/workflows/schemas/common.schema.json'))
fc = cs['$defs']['D9FaultCause']
print('common D9FaultCause', json.dumps(fc)[:800])
d9 = json.load(open(C + 'docs/coop/artifacts/d9-exit-contract.v1.14.json'))
en = d9['scenarioAxesSchema']['properties']['faultCause']['enum']
print('v1.14 faultCause enum', len(en), en)
print('v1.14 has host-invariant', 'host-invariant' in en, 'map key', 'host-invariant' in d9['codeMaps']['faultCauseToErrorCode'])
ec = d9['codeVocabulary']['errorCodes']
print('ILLEGAL_STATE in vocabulary', any('SYSTEM.OUTCOME.ILLEGAL_STATE' in json.dumps(x) for x in (ec if isinstance(ec, list) else [ec])))
print('ILLEGAL_STATE preimage', [k for k, v in d9['codeMaps']['faultCauseToErrorCode'].items() if v == 'SYSTEM.OUTCOME.ILLEGAL_STATE'])
fcenum = fc.get('enum') or []
print('selected set == inherited + host-invariant:', set(fcenum) == set(en) | {'host-invariant'}, len(fcenum))
print('d9 artifact sha', sha(C + 'docs/coop/artifacts/d9-exit-contract.v1.14.json'))
ir = json.load(open(S + 'docs/coop/design-corrections/inherited-residuals.applied.v1.json'))
k = [kk for kk, v in ir.items() if isinstance(v, list)][0]
print('inherited list key', k, len(ir[k]), [r.get('id') for r in ir[k]])
carriers = [r for r in ir[k] if 'carriedCrossUnitObligation' in r]
print('rows with carried obligation', [r['id'] for r in carriers])
for r in carriers:
    ob = r['carriedCrossUnitObligation']
    print('=====', r['id']); print(json.dumps(ob, indent=1))
    def walk(o):
        if isinstance(o, dict):
            if 'path' in o and 'sha256' in o:
                p = o['path']; src = C + p
                try:
                    ok = sha(src) == o['sha256']
                    val = ptr(json.load(open(src)), o['selector']) if o.get('selector', '').startswith('/') and p.endswith('.json') else None
                    print('   REF', p, 'sha ok', ok, 'selector', o.get('selector'), 'resolves' if val is not None else '', json.dumps(val)[:300] if val is not None else '')
                except Exception as ex:
                    print('   REF', p, 'ERROR', ex)
            for v in o.values(): walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    walk(ob)
ar = json.load(open(S + 'docs/coop/design-corrections/accepted-review-advisories.v1.json'))
txt = json.dumps(ar)
i = txt.find('CB-ADV-4')
print('CB-ADV-4 occurrences', txt.count('CB-ADV-4'))
print(txt[max(0, i - 200): i + 2500])
