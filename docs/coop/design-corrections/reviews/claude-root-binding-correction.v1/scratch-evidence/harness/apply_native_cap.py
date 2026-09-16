import hashlib
S='/private/tmp/opensip-design-corrections/claude-root-binding-correction.v1/scratch'
np=S+'/src25/docs/coop/design-corrections/native/native_evidence_model.v2.py'
nsrc=open(np,encoding='utf-8').read()
before=hashlib.sha256(nsrc.encode()).hexdigest()
old='    admit_release_capability_registry(registry)' + chr(10) + '    available = {(r[' + chr(34) + 'capabilityId' + chr(34) + '], mode) for r in registry for mode in r[' + chr(34) + 'languageModes' + chr(34) + ']}' + chr(10)
guard='    admit_unit_roots(units)   # decided BEFORE the outward \"or .\" spelling makes a wrong root indistinguishable' + chr(10)
assert nsrc.count(old)==1, nsrc.count(old)
nsrc=nsrc.replace(old, guard+old, 1)
open(np,'w',encoding='utf-8').write(nsrc)
print('before',before)
print('after ',hashlib.sha256(nsrc.encode()).hexdigest())
