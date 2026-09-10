from pathlib import Path
import sys,json,hashlib,shutil
ROOT=Path(__file__).parent
sys.path.insert(0,str(ROOT/'isolated'))
from helper import query_projection as Q
U='a'*64
EP={'universe':U,'kind':'symbol','nativeSubjectId':'a'}
R={'schemaFamily':'opensip.product.query','schemaMajor':3,'projectId':'prj1-'+U,'view':{'runId':'run3:'+U},'operation':'graph.neighbors','params':{'relation':'calls','minResolution':'resolved-callee','direction':'outgoing','endpoint':EP},'completeness':'best-effort'}
rows=[]
def probe(name, selector, inp, fn, expected):
 try: value=fn(); actual={'kind':'return','value':value}
 except Exception as e:actual={'kind':'exception','type':type(e).__name__,'code':getattr(e,'code',None),'message':str(e)}
 rows.append({'name':name,'normativeSelector':selector,'input':inp,'expected':expected,'observed':actual})
invalid_host={'requestId':'req1_'+'z'*32}
probe('host-request-id-nonhex','query-projection-contract.v3.md §7',invalid_host,lambda:Q._host_request_id(invalid_host),'reference-call precondition refusal')
pkg={'universe':U,'kind':'package','nativeSubjectId':'p'};v={**pkg,'packageManifestPath':'a/Cargo.toml'}
probe('package-missing-manifest-single-match','query-projection-contract.v3.md §2 fault precedence 2',{'endpoint':pkg,'vertices':[v]},lambda:Q.admit_endpoint(pkg,[v]),'QUERY.ENDPOINT_AMBIGUOUS')
extra={**R,'params':{**R['params'],'start':EP}}
probe('operation-specific-extra-param','query-projection-contract.v3.md §4 closed graph.neighbors params',extra,lambda:Q.admit_request(extra),'QUERY.PARAMS_MALFORMED')
missing={**R,'params':{}}
probe('missing-required-params','query-projection-contract.v3.md §§4,8 request admission',missing,lambda:Q.admit_request(missing),'QUERY.PARAMS_MALFORMED')
(ROOT/'results.json').write_text(json.dumps({'standing':'Root independent bounded probes of actual consumer helper against explicit kit laws. No complete Run admission, no peer feedback, no author reference imported. Four probes do not assess all query/workflow behavior.','probes':rows},indent=2)+'\n')
print(json.dumps(rows,indent=2))
