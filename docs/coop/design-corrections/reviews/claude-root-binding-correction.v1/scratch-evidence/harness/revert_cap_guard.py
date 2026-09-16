import hashlib
S='/private/tmp/opensip-design-corrections/claude-root-binding-correction.v1/scratch'
np=S+'/src25/docs/coop/design-corrections/native/native_evidence_model.v2.py'
s=open(np,encoding='utf-8').read()
before=hashlib.sha256(s.encode()).hexdigest()
guard='    admit_unit_roots(units)   # decided BEFORE the outward \"or .\" spelling makes a wrong root indistinguishable'+chr(10)
assert s.count(guard)==1, s.count(guard)
s=s.replace(guard,'',1)
open(np,'w',encoding='utf-8').write(s)
print('before',before)
print('after ',hashlib.sha256(s.encode()).hexdigest())
