"""Root comparison of exact final consumer outputs; no consumer code imports or repairs."""
from pathlib import Path
import copy, hashlib, importlib.util, json, shutil
B=Path('/tmp/opensip-design-corrections')
L=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews')
O=Path(__file__).parent
V=B/'consumer-b.v24-source45.v1/output/vectors/graph-query.json'
v=json.loads(V.read_text()); rows={r['vector']:r for r in v['vectors']}
def load(name,p):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
S=load('root45surface',B/'candidate-subject.v45/docs/coop/design-corrections/workflows/query_surface_projection.v3.py')
def eq(a,b):return S.canonical.equal_typed(a,b)
def response_projection(a):
 a=copy.deepcopy(a)
 # Only non-semantic optional fields; record exact original differences separately.
 a.setdefault('termination',{'class':'success'})
 if 'nextCursor' in a['context']:a['context']['nextCursor']='<HOST-OPAQUE-TOKEN-PRESENT>'
 for r in a['context']['evidence']['resolutionLimitations']:r.pop('note',None)
 for r in a['context']['evidence']['deficiencyCitations']:
  if r.get('nativeCause','absent') is None:r.pop('nativeCause')
 return a
def failure_projection(a):
 a=copy.deepcopy(a)
 for d in a.get('errors',[]):
  d.pop('remedy',None);d.pop('subject',None)
 d=a.get('termination',{}).get('domainDetail',{})
 d.pop('remedy',None);d.pop('subject',None)
 return a
out=[]
foreign={'page2-after-newer-latest-bound-run','page2-with-host-cache-present'}
for name in ['cmp-base','cmp-code','syntax-mixed-disclosed']:
 p=B/'root-blind45-query-envelope-capture.v1'/name/'report.json';j=json.loads(p.read_text())
 assert j['semanticAdmission']=='ADMIT'
 for r in j['cases']:
  key=r['vector'];c=r['consumerResponse'];o=r.get('ownerResponse'); cf=r['consumerFailureEnvelope'];of=r.get('ownerFailureEnvelope')
  if key in foreign:
   assert c and of and of['termination']['domainDetail']['code']=='QUERY.CURSOR_MISMATCH'
   category='consumer-host opaque continuation; root token refusal expected; consumer page examined separately'
  elif c:
   assert o and eq(response_projection(c),response_projection(o)),key
   category='all required structured response fields agree; optional success termination, diagnostic notes, null nativeCause and token bytes accounted'
  else:
   assert cf and of and eq(failure_projection(cf),failure_projection(of)),key
   category='all structured failure fields agree; diagnostic remedy/subject wording differs where recorded'
  out.append({'vector':key,'comparison':category,'passed':True,'captureSha256':hashlib.sha256(p.read_bytes()).hexdigest()})
assert len(out)==63
parity=[]
for key,r in rows.items():
 if 'response' in r:
  env=r['envelope'];S._admit(S.ENVELOPE_REF,env,'ROOT_ENVELOPE')
  projected=S.project_query_surface(r['response'],r['termination'],envelope=env)['parity']
  assert set(r['renderings'])=={'human','json','agent'}
  for fmt,body in r['renderings'].items():
   if fmt=='human':
    recovered={}
    for line in body.splitlines():
     k,sep,val=line.partition(': ');assert sep and k not in recovered
     recovered[k]=S.canonical.parse(val.encode())
   else:
    decoded=S.canonical.parse(body.encode())
    recovered=S.project_query_surface(decoded['queryResponse'],decoded['termination'],envelope=decoded)['parity']
   assert eq(projected,recovered),(key,fmt)
  parity.append({'vector':key,'carrier':'ADMIT','summaryJoins':'PASS','threeRenderedParityProjections':'PASS'})
 else:
  S._admit(S.ENVELOPE_REF,r['failureEnvelope'],'ROOT_FAILURE_ENVELOPE')
  parity.append({'vector':key,'failureCarrier':'ADMIT','noSuccessRenderingsClaimed':True})
# Consumer-host continuation uses its exact page-one token; verify exact ordered
# concatenation against the independently matched unpaged reference and unchanged cache page.
p1=rows['page1-latest-size1'];p2=rows['page2-after-newer-latest-bound-run'];pc=rows['page2-with-host-cache-present'];allp=rows['single-page-reference']
assert p2['request']['page']['cursor']==p1['response']['context']['nextCursor']
assert pc['request']['page']['cursor']==p1['response']['context']['nextCursor']
assert eq(p1['response']['items']+p2['response']['items'],allp['response']['items'])
assert eq(p2['response'],pc['response'])
assert p2['response']['context']['resolvedView']==p1['response']['context']['resolvedView']
report={'standing':'Scoped root semantic query comparison and exact carrier/parity validation, not provider/product qualification. No consumer code imported, graph repaired, reminted or token translated.',
 'sourceManifestSha256':'8b4efbb04d9e25126ec7955931cf364f7013b3710a45c48bae8bc563a0c82155','vectorsSha256':hashlib.sha256(V.read_bytes()).hexdigest(),
 'strongCaptureCases':out,'carrierAndParity':parity,'consumerHostPagination':'PASS: exact supplied token binding, fixed old Run, ordered page union matches root-validated single-page result; cache page unchanged',
 'negativeScope':'Two declared retained-blob loss/corruption cases checked separately by root-blind45-negative-query.v1. Third tampered-verdict query is a consumer in-memory measurement; root does not claim exact exported negative replay.',
 'result':'PASS'}
(O/'assessment.json').write_text(json.dumps(report,indent=2)+'\n')
shutil.copytree(O,L/O.name)
print(json.dumps({'result':'PASS','strongCaptureCases':len(out),'carriers':len(parity),'successRenderings':sum('threeRenderedParityProjections' in r for r in parity),'opaqueContinuationCases':2}))
