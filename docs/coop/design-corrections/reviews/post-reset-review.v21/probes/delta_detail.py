import json,os,hashlib
A='/tmp/opensip-design-corrections/candidate-subject.v20'
B='/tmp/opensip-design-corrections/candidate-subject.v21'
LED=['docs/coop/design-corrections/foundation/source-pins.v1.json',
     'docs/coop/design-corrections/native/source-pins.v2.json',
     'docs/coop/design-corrections/security/source-pins.v1.json',
     'docs/coop/design-corrections/workflows/source-pins.v1.json']
CH3={'docs/coop/design-corrections/foundation/run-reference-checks.py',
     'docs/coop/design-corrections/foundation/check-identity.py',
     'docs/coop/design-corrections/workflows/workflows_model.v1.py'}
def pins(p):
    j=json.load(open(p))
    for k in ('pins','files'):
        if isinstance(j.get(k),list): return {e.get('path') or e.get('file'):e['sha256'] for e in j[k]}
    return {}
print('=== LEDGER REPIN DELTA (v20 -> v21) ===')
for L in LED:
    a=pins(os.path.join(A,L)); b=pins(os.path.join(B,L))
    added=set(b)-set(a); removed=set(a)-set(b)
    moved={p for p in set(a)&set(b) if a[p]!=b[p]}
    print(f'{L}: n {len(a)}->{len(b)} added {sorted(added)} removed {sorted(removed)}')
    for p in sorted(moved):
        print(f'    REPIN {p}  in3changed={p in CH3}')
    if not moved: print('    (no repins)')
print()
print('=== CONTRACT BYTES v20 vs v21 ===')
for n in ['README.md','admission-and-qualification.md','identity-and-evidence.md','native-evidence.md','security-and-lifecycle.md','workflows-and-surfaces.md']:
    rel='docs/v2/contracts/product-v1/'+n
    ha=hashlib.sha256(open(os.path.join(A,rel),'rb').read()).hexdigest()
    hb=hashlib.sha256(open(os.path.join(B,rel),'rb').read()).hexdigest()
    print(f'{n}: {"UNCHANGED" if ha==hb else "CHANGED"}')
print()
print('=== SCHEMAS / OTHER .json .py CHANGED? ===')
m20={f['path']:f['sha256'] for f in json.load(open('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v20.json'))['files']}
m21={f['path']:f['sha256'] for f in json.load(open('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v21.json'))['files']}
ch=[p for p in set(m20)&set(m21) if m20[p]!=m21[p]]
schema=[p for p in ch if p.endswith('.json') and 'schema' in p.lower()]
print('changed schema documents:',schema or 'NONE')
py=[p for p in ch if p.endswith('.py')]
print('changed .py:',sorted(py))
