"""Derive exact frozen reference proof on captured consumer inputs; never change or remint them."""
from pathlib import Path
import json,hashlib,importlib.util
B=Path('/tmp/opensip-design-corrections');S=B/'candidate-subject.v33';IN=B/'root-blind20-final33-replay.v1';OUT=B/'root-blind20-proof-differences33.v1'
def load(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def sha(b):return hashlib.sha256(b).hexdigest()
T=load('root_transport20',B/'check-blind-successor33-export.v1.py')
R=load('root_replay20',S/'docs/coop/design-corrections/foundation/evaluator_replay_model.v3.py');M=R.M
def diff(a,b,path=''):
    if type(a)!=type(b):return [{'path':path,'consumer':a,'reference':b}]
    if isinstance(a,dict):
        out=[]
        for k in sorted(set(a)|set(b)):
            if k not in a or k not in b:out.append({'path':path+'/'+k,'consumer':a.get(k),'reference':b.get(k),'missingFrom':'consumer' if k not in a else 'reference'})
            else:out.extend(diff(a[k],b[k],path+'/'+k))
        return out
    if isinstance(a,list):
        if len(a)!=len(b):return [{'path':path,'consumer':a,'reference':b,'lengths':[len(a),len(b)]}]
        return [d for i,(x,y) in enumerate(zip(a,b)) for d in diff(x,y,path+'/'+str(i))]
    return [] if a==b else [{'path':path,'consumer':a,'reference':b}]
assert not OUT.exists();OUT.mkdir();rows=[]
for n in ['syntax-code','typescript','rust','rust-partial','syntax-data']:
    raw=(IN/'captured'/(n+'.store.json')).read_bytes();prior=json.loads((IN/n/'report.json').read_text());assert sha(raw)==prior['exportSha256'];assert prior['structuralAdmission']=='ADMIT'
    d=T.parse(raw);o,b,_=T.decode(raw,M);rid=d['claim']['runId'];run=o[rid][1];_,owner=M.open_run_closure(run,o,b);seal=o[run['evaluationSealId']][1];proof=o[seal['proofBundleId']][1]
    r=R.derive(run['planId'],seal['executionPlanId'],seal['evaluatorClosure'],proof['evaluationInputRefs'],o,b,owner)
    ds=diff(proof,r['proof']);out=OUT/n;out.mkdir()
    for name,v in [('consumer-proof.json',proof),('reference-proof.json',r['proof']),('differences.json',ds)]: (out/name).write_text(json.dumps(v,indent=2)+'\n')
    row={'name':n,'runId':rid,'exportSha256':sha(raw),'differenceCount':len(ds),'paths':[x['path'] for x in ds]};rows.append(row);print(json.dumps(row),flush=True)
(OUT/'report.json').write_text(json.dumps({'standing':'Frozen full reference derivation on exact structurally admitted consumer inputs. Comparison only; no remint, consumer imports, substituted acceptance or independent charter acceptance.','sourceManifestSha256':'1cf3db70d4b73b0c42f1393331e6a874ee26f7ddf67aa05c6ac15a5753069299','rows':rows},indent=2)+'\n')
