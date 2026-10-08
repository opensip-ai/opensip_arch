from pathlib import Path
import json,sys,copy
sys.path.insert(0,'/tmp/opensip-implementation/c2a-protocol-major-panel/audit-deps')
from jsonschema import Draft202012Validator
from referencing import Registry,Resource
D=Path(__file__).resolve().parents[1];P=Path('/Users/sb/code/opensip-ai/opensip');A=P.parent/'opensip_arch';routes=json.loads((D/'native-import-routes.json').read_text());extension=json.loads((D/'public-detail-extension.json').read_text());code=extension['newPublicCode'];commons={}
for c in extension['copies']:
 b=json.loads((A/c['source']['path']).read_text());n=json.loads((D.parents[4]/c['candidate']['path']).read_text());assert n['$defs']['DomainDetailCode']['enum']==b['$defs']['DomainDetailCode']['enum']+[code];restored=copy.deepcopy(n);restored['$defs']['DomainDetailCode']=b['$defs']['DomainDetailCode'];assert restored==b
 if '/product/' in c['candidate']['path']:commons[n['$id']]=n
schemas={}
for p in (P/'schemas/sources').glob('*.json'):
 s=json.loads(p.read_text())
 if '$id' in s:schemas[s['$id']]=s
schemas.update(commons);registry=Registry().with_resources((k,Resource.from_contents(s)) for k,s in schemas.items());ev=Draft202012Validator(json.loads((P/'schemas/sources/command-envelope-v7.schema.json').read_text()),registry=registry)
rows=[]
for key,r in routes['keys'].items():
 assert set(r['possibleOrigins'])==set(r['byOriginatingBoundary'])
 for origin,v in r['byOriginatingBoundary'].items():
  detail=dict(code=v['envelopeDetail'],remedy=routes['publicRemedies'][v['envelopeDetail']],subject=key);term={k:v[k] for k in ['class','errorCode','faultCause'] if k in v}
  if v['domainDetail'] is not None:term['domainDetail']=detail
  envelope=dict(schemaFamily='opensip.product.envelope',schemaMajor=7,kind='failure',requestId='req1_'+'0'*32,termination=term,exitCode=4 if origin=='host-generated-internal-layer' else 2,errors=[detail]);assert ev.is_valid(envelope),(key,origin,list(ev.iter_errors(envelope)))
  for label,change in [('missing-errors',lambda e:e.pop('errors')),('empty-errors',lambda e:e.update(errors=[])),('internal-key-public',lambda e:e['errors'][0].update(code=key)),('null-termination-detail',lambda e:e['termination'].update(domainDetail=None))]:
   bad=copy.deepcopy(envelope);change(bad);assert not ev.is_valid(bad),(key,origin,label)
  rows.append(dict(key=key,origin=origin,envelopeValid=True,negativeControls=4))
(D/'evidence/carriers.json').write_text(json.dumps(dict(completeFailureEnvelopes=len(rows),newPublicDetails=1,commonCopies=4,controls=rows,productExecution=False,productQualification=False),indent=2)+'\n');print(json.dumps(dict(completeFailureEnvelopes=len(rows),negativeControls=len(rows)*4)))
