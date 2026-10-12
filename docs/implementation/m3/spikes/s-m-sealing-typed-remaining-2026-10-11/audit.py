from pathlib import Path
import json,hashlib,statistics,struct,sys
B=Path(__file__).resolve().parent;P=Path('/Users/sb/code/opensip-ai/opensip');sys.path.insert(0,str(P/'tools/contracts/python-packages'));from jsonschema import Draft202012Validator
j=json.loads((B/'results.json').read_text());template=json.loads((B/'control-template.json').read_text());fixture_path=P/'crates/host/tests/fixtures/replay-fixtures.json';raw=fixture_path.read_bytes();assert hashlib.sha256(raw).hexdigest()=='4004eb2a751eb5d55a0dd8170d1ff81545282ca27a863215763e8b7c4393d163';fixture=json.loads(raw);schema=json.loads((P/'schemas/sources/identity-v3.schema.json').read_text())
def C(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def identity(kind,v):r=C(v);return ('snapshot2:'if kind=='snapshot'else'plan2:')+hashlib.sha256(b'opensip.product.v1\0'+kind.encode()+b'\0'+struct.pack('>Q',len(r))+r).hexdigest()
controls=[]
for kind in ['snapshot','plan']:
 matches=[v for v in fixture['objectPool'].values()if v['domain']==kind and v['descriptor']==template[kind]];assert len(matches)==1;assert identity(kind,template[kind])==matches[0]['id'];Draft202012Validator(dict(schema,**{'$ref':'#/$defs/'+kind})).validate(template[kind]);controls.append(dict(domain=kind,id=matches[0]['id'],publicFixturePreimageAndIdentityMatched=True))
assert len(j['workloads'])==13 and j['observedParentNiceness']==10 and j['snapshotPlanIdentitiesAdmitted']is False
rows=[]
for w in j['workloads']:
 assert w['heldOut']is False and len(w['runs'])==10;sh=w['shape'];observations=[]
 for n,r in enumerate(w['runs']):
  raw=json.loads((B/f'{w["id"]}-{n}.stdout').read_text());elapsed=raw.pop('elapsedNanos');assert raw==sh;assert elapsed==r['elapsedNanos'];assert (B/f'{w["id"]}-{n}.stderr').read_bytes()==b'';assert r['ordinal']==n and r['warmup']==(n<3)and r['observedChildNiceness']==10 and r['exitCode']==0 and r['rssUnit']=='bytes'and r['rssNative']==r['rssBytes']and 0<=r['rssBytes']<2**64
  if n>=3:observations.append(elapsed)
 assert statistics.median(observations)==w['medianNanos']and max(observations)==w['maxNanos'];inv=sh['regularRows'];assert inv==sorted(inv,key=lambda r:r['path'].encode())and len({r['path']for r in inv})==len(inv)and sh['rows']==len(inv)and sh['bytes']==sum(r['bytes']for r in inv)
 snapshot=dict(template['snapshot'],sourceInventory=inv);plan=dict(template['plan'],snapshotId=identity('snapshot',snapshot));assert identity('snapshot',snapshot)==sh['snapshotEquivalentDigest']and identity('plan',plan)==sh['planEquivalentDigest'];assert len(C(snapshot))==sh['snapshotEquivalentDescriptorBytes']and len(C(plan))==sh['planEquivalentDescriptorBytes']and len(C(inv))==sh['inventoryCanonicalBytes']
 for kind,v in [('snapshot',snapshot),('plan',plan)]:Draft202012Validator(dict(schema,**{'$ref':'#/$defs/'+kind})).validate(v)
 bounds=dict(rows100000=sh['rows']<=100000,descriptor4MiB=len(C(snapshot))<=4*1024*1024,total8GiB=sh['bytes']<=8*1024**3);assert all(bounds.values());rows.append(dict(id=w['id'],regularRows=sh['rows'],bytes=sh['bytes'],nonregularExcluded=len(sh['nonregularExcluded']),snapshotDescriptorBytes=len(C(snapshot)),planDescriptorBytes=len(C(plan)),medianNanos=w['medianNanos'],maxNanos=w['maxNanos'],measuredPeakRssBytes=max(r['rssBytes']for r in w['runs'][3:]),bounds=bounds,overlayConfigurationNotCaptured=w['overlayConfigurationNotCaptured']))
result=dict(standing='UNREVIEWED READONLY TYPED SEALING STATISTICAL/IDENTITY/REGISTERED SHAPE AUDIT',publicControlIdentityMatches=controls,fixturePin=dict(path=str(fixture_path),bytes=len(fixture_path.read_bytes()),sha256=hashlib.sha256(fixture_path.read_bytes()).hexdigest()),workloads=rows,all130ChildPrioritiesObserved10=True,SM5FigureComplete=False,SM5PlaceholderFilled=False,SMComplete=False,LG1Met=False,snapshotPlanIdentitiesAdmitted=False,dependencySourceSetsIncluded=False,effectiveL=False,productQualification=False);(B/'checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(workloads=len(rows),children=130,allPass=True),indent=2))
