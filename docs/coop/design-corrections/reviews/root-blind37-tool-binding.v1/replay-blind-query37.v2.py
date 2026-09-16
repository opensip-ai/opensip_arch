"""Root exact consumer query requests over exact consumer retained export via frozen source37.
Reference output is comparative evidence; opaque-token spelling and diagnostic prose need
semantic assessment rather than blanket byte-equality acceptance. No consumer imports. v2 accepts retained nested outcomes, failure cases and case.host observations.
"""
from pathlib import Path
import argparse,json,hashlib,importlib.util
B=Path('/tmp/opensip-design-corrections')
S=B/'candidate-subject.v37'
MF=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v37.json')
SHA='245ef613243aafeaac2dcdca7f0b398d5a770ec338abbf712039fdfd91676680'
def loadmod(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--export',dest='export',type=Path,required=True);p.add_argument('--vectors',type=Path,required=True);p.add_argument('--host-controls',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();assert not a.out.exists();assert not a.out.resolve().is_relative_to(S.resolve());a.out.mkdir()
 mf=MF.read_bytes();assert sha(mf)==SHA
 for r in json.loads(mf)['files']:
  raw=(S/r['path']).read_bytes();assert len(raw)==r['bytes'] and sha(raw)==r['sha256'],r['path']
 R=loadmod('root_query_transport',B/'check-blind-successor37-export.v1.py');M=loadmod('root_query_identity',S/'docs/coop/design-corrections/foundation/identity-model.v3.py');Q=loadmod('root_query_owner',S/'docs/coop/design-corrections/workflows/query_projection_model.v3.py')
 raw=a.export.read_bytes();vraw=a.vectors.read_bytes();(a.out/'exact-export.json').write_bytes(raw);(a.out/'exact-query-vectors.json').write_bytes(vraw);d=R.parse(raw);j=R.parse(vraw);objects,blobs,_=R.decode(raw,M);rid=d['claim']['runId'];run=objects[rid][1];host_controls=R.parse(a.host_controls.read_bytes()) if a.host_controls else {}
 if a.host_controls:(a.out/'host-controls.json').write_bytes(a.host_controls.read_bytes())
 result={'standing':'Root strong query reference comparison, not blanket response-byte conformance or full charter assent. No consumer source imported and no request/Run repaired.','subjectManifestSha256':SHA,'exportSha256':sha(raw),'vectorSha256':sha(vraw),'runId':rid,'cases':[]}
 try:
  assert M.open_run_closure(run,objects,blobs)[0]==rid;assert M.close_run(run,objects,blobs)==rid;result['retainedRunAdmission']='ADMIT'
 except Exception as e:result['retainedRunAdmission']='REFUSE';result['reason']=str(e);(a.out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));return
 assert isinstance(j.get('operations'),list) and j['operations'], 'No retained operation vectors'
 assert isinstance(j.get('failureCases',[]),list), 'Failure cases must be an array'
 for group in ['operations', 'failureCases']:
  for c in j.get(group, []):
   for reqkey,reskey in [('request','response'),('secondRequest','secondResponse')]:
    if reqkey not in c:continue
    assert isinstance(c[reqkey],dict), 'Retained request must be an object'
    embedded_host = c.get('host', {})
    assert isinstance(embedded_host,dict), 'Retained host observation must be an object'
    external_host = host_controls.get(c['case'])
    if external_host is not None:
     assert isinstance(external_host,dict)
     assert not embedded_host or embedded_host == external_host, 'Conflicting host inputs; do not silently replace retained controls'
    host = embedded_host if external_host is None else external_host
    consumer_outcome = c.get('outcome') if reqkey == 'request' else None
    if consumer_outcome is not None:
     assert isinstance(consumer_outcome,dict)
     assert consumer_outcome.get('kind') in ['response','failure','reference-call-precondition']
     consumer_response = consumer_outcome.get('response')
     if consumer_outcome['kind'] == 'response':assert isinstance(consumer_response,dict)
    else:
     consumer_response = c.get(reskey)
     assert isinstance(consumer_response,dict), 'No retained response/outcome for '+c['case']
    item={'group':group,'case':c['case'],'requestKey':reqkey,'request':c[reqkey],
          'consumerResponse':consumer_response,'consumerOutcome':consumer_outcome,
          'hostControls':host,'hostControlProvenance':('exact vector case.host' if external_host is None else 'explicit captured host-controls input'),
          'scope':'Exact retained request and host observations. No cursor translation, remint, request repair or consumer import. Opaque token spelling and diagnostic prose are not blanket conformance checks.'}
    try:
     item['ownerResponse']=Q.execute_graph_query(c[reqkey],run,objects,blobs,host=host)
     item['ownerOutcome']='RETURNED'
    except Exception as e:
     item['ownerOutcome']='RAISED';item['reason']=str(e);item['exceptionType']=type(e).__name__
    result['cases'].append(item)
 (a.out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'retainedRunAdmission':result['retainedRunAdmission'],'cases':[{k:r.get(k) for k in ['case','requestKey','ownerOutcome','reason']} for r in result['cases']]}))
if __name__=='__main__':main()
