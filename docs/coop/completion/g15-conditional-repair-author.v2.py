#!/usr/bin/env python3
"""Retain narrowly scoped signed freshness cases; all seed material is PUBLIC TEST."""
import copy,datetime,hashlib,importlib.util,json
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
P=Path(__file__).resolve().parent;ROOT=P.parents[2]
s=importlib.util.spec_from_file_location('g15_repair_author',P/'compatibility-selection-model.v5.py');M=importlib.util.module_from_spec(s);s.loader.exec_module(M)
def load(name):return json.loads((P/name).read_text())
def raw(value):return (json.dumps(value,indent=2,ensure_ascii=False)+'\n').encode()
def write(name,value):(P/name).write_bytes(raw(value))
def sha(value):return hashlib.sha256(value).hexdigest()
bundle=load('g15-conditional-bundle.v1.json');host=load('g15-conditional-host.v1.json');host['now']='2027-03-01T00:00:00Z';root=json.loads(bytes.fromhex(bundle['documents']['root']));rev=json.loads(bytes.fromhex(bundle['documents']['revocation']));keys=load('g15-conditional-test-keys.v1.json')['keys'];x=load('g15-conditional-cases.v1.json')['cases'][0]['resolutionInputs'];now=datetime.datetime(2027,3,1,tzinfo=datetime.timezone.utc)
def variant(issued):
 r=copy.deepcopy(rev);r['issuedAt']=issued;data=raw(r);env=json.loads(bytes.fromhex(bundle['documents']['revocation.envelope']));env['subject'].update({'storedSha256':sha(data),'preimageSha256':M.digest(M.SEC.DOMAIN_TAGS['revocation'],r)});env['signatures']=[];msg=bytes.fromhex(M.SEC.envelope_message_hex(env))
 for kid in root['rootKeys'][:2]:
  key=next(k for k in keys if k['keyId']==kid);private=Ed25519PrivateKey.from_private_bytes(bytes.fromhex(key['PUBLIC_TEST_SEED_HEX']));env['signatures'].append({'keyId':kid,'alg':'ed25519','signature':private.sign(msg).hex()})
 env['signatures'].sort(key=lambda q:q['keyId']);return data.hex(),raw(env).hex()
cases=[]
for label,seconds,status,reason in [('just-inside',90*86400-1,'ACCEPT',None),('equality',90*86400,'ACCEPT',None),('just-outside',90*86400+1,'REFUSE','REVOCATION-STALE'),('review-150-days',150*86400,'REFUSE','REVOCATION-STALE')]:
 issued=(now-datetime.timedelta(seconds=seconds)).strftime('%Y-%m-%dT%H:%M:%SZ');r,e=variant(issued);cases.append({'id':label,'issuedAt':issued,'ageSeconds':seconds,'host':host,'resolutionInputs':x,'revocationHex':r,'envelopeHex':e,'expectedStatus':status,'expectedReason':reason})
for label,issued,reason in [('invalid-calendar','2027-02-30T00:00:00Z','REVOCATION-TIMESTAMP'),('invalid-spelling','not-a-UTC-timestamp','SCHEMA-revocation')]:
 r,e=variant(issued);cases.append({'id':label,'issuedAt':issued,'ageSeconds':None,'host':host,'resolutionInputs':x,'revocationHex':r,'envelopeHex':e,'expectedStatus':'REFUSE','expectedReason':reason})
# Keep malformed trusted evaluation input controlled too; it is never interpreted
# as permission to relax freshness.
r,e=variant('2026-12-20T00:00:00Z');bad_host=copy.deepcopy(host);bad_host['now']='2027-02-30T00:00:00Z';cases.append({'id':'invalid-evaluation-calendar','issuedAt':'2026-12-20T00:00:00Z','ageSeconds':None,'host':bad_host,'resolutionInputs':x,'revocationHex':r,'envelopeHex':e,'expectedStatus':'REFUSE','expectedReason':'HOST-EVALUATION-TIMESTAMP'})
write('g15-revocation-freshness-cases.v2.json',{'status':'PROPOSED-G15-M1-REPAIR','rule':'0 <= trusted evaluation time - issuedAt <= 90 days; equality remains fresh, greater age refuses. Existing version and future-time checks remain.','cases':cases})
# The independent probe is already retained as an immutable input; regeneration
# does not depend on the reviewer's temporary filesystem.
assert (P/'g15-stale-revocation-probe.v2.json').is_file(), 'retained independent probe required'
corpus=load('g15-conditional-cases.v1.json');corpus['repair']='G15-M1 revocation freshness only; original60conditional cases unchanged.'
for name in ['security-completion.v2.md','security-behavior-model.v2.py','g15-conditional-cases.v1.json','g15-conditional-freeze.v1.json','g15-stale-revocation-probe.v2.json']:
 q=P/name;corpus['sourcePins'][str(q.relative_to(ROOT))]=sha(q.read_bytes())
write('g15-conditional-cases.v2.json',corpus)
matrix=load('g15-conditional-matrix.v1.json')
for unit in matrix['matrix']:
 for member in unit['members'].values():
  if member['designInput']['path'].endswith('g15-conditional-cases.v1.json'):member['designInput']['path']='docs/coop/completion/g15-conditional-cases.v2.json'
write('g15-conditional-matrix.v2.json',matrix)
print('Authored',len(cases),'signed freshness/malformed-time cases; retained60conditional cases')
