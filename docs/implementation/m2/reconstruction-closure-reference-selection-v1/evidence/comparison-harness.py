from pathlib import Path
import json,hashlib,shutil,copy,importlib.util,lzma
T=Path('/tmp/opensip-implementation');S=T/'m2-input-structure-subject-47';B=T/'m2-reconstruction-reference-candidate-49';assert not B.exists();B.mkdir();refs=json.loads((S/'reference-inputs.json').read_bytes())
for row in refs['files']:
 p=S/row['path'];raw=p.read_bytes();assert(len(raw),hashlib.sha256(raw).hexdigest())==(row['bytes'],row['sha256']);dst=B/row['path'];dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(raw)
F=B/'reference/archroot/docs/coop/design-corrections/foundation';p=F/'evaluator_input_model.v3.py';old=p.read_text();needle="closures={key:value for key,(domain,value) in objects.items() if domain=='closure'}";replacement="closures={key:objects[key][1] for key in plan['semanticClosures']}";assert old.count(needle)==1;(B/'predecessor.py').write_text(old);p.write_text(old.replace(needle,replacement));(B/'candidate.py').write_bytes(p.read_bytes())
# Reuse only fixture construction from the prior independent reference harness;
# no assertions or expected values from Rust are imported.
script=(T/'resume_reconstruction48_v2.py').read_text();a=script.index("I=load('reconstruction48_i'");z=script.index('for name,plan,execution,closure,refs,run,obs,blobs in packets:');F_old=S/'reference/archroot/docs/coop/design-corrections/foundation'
def load(name,file):
 sp=importlib.util.spec_from_file_location(name,F_old/file);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
ctx={'T':T,'load':load,'json':json};exec(script[a:z],ctx);I=ctx['I'];M=ctx['M'];packets=ctx['packets'];sp=importlib.util.spec_from_file_location('reconstruction49_new',p);N=importlib.util.module_from_spec(sp);sp.loader.exec_module(N)
rows=[];diffs=[];n_ok=0;n_refused=0
for name,plan,execution,closure,rf,run,obs,blobs in packets:
 _,owner=M.open_run_closure(obs[run][1]if isinstance(run,str)else run,obs,blobs);owner={k:owner[k]for k in ['plan','snapshot','analysisSpec','nativeUniverses','nativeContexts']};json.dumps(owner)
 selected=owner['plan']['semanticClosures'];named={k:v for k,v in obs.items()if v[0]!='closure'or k in selected};extra=copy.deepcopy(obs[selected[0]][1]);extra['semanticVersion']='99.0.0';extraid=M.identifier('closure',extra);augmented={**obs,extraid:('closure',extra)}
 variants=[('original',obs,rf),('named-only',named,rf),('ambient-extra',augmented,rf)]
 inv=next((r for r in rf if r['domain']=='subject-inventory'),None)
 if inv:variants.append(('duplicate-inventory',obs,rf+[copy.deepcopy(inv)]))
 incoming=next((r for r in rf if r['domain']=='incoming-search'),None)
 if incoming:variants.append(('duplicate-incoming',obs,rf+[copy.deepcopy(incoming)]))
 for variant,objects,inputrefs in variants:
  def derive(mod):
   try:
    normal,evidence=mod.reconstruct(plan,execution,closure,inputrefs,objects,blobs,owner,M);evidence.pop('blobs');return {'normalized':normal,'evidence':evidence}
   except Exception as exc:
    if exc.__class__.__name__!='AdmissionError':raise
    return {'refused':str(exc)}
  before=derive(I);after=derive(N);label=name+'-'+variant
  if 'refused'in after:assert before==after;n_refused+=1
  else:
   n_ok+=1
   for section in ['normalized','evidence']:
    assert set(after[section]['closures'])==set(selected)
    expect=copy.deepcopy(before[section]);expect['closures']={k:objects[k][1]for k in selected};assert after[section]==expect,(label,section)
   if variant=='named-only':assert before==after
  if before!=after:diffs.append(label)
  rows.append({'label':label,'planId':plan,'executionId':execution,'evaluatorClosure':closure,'inputRefs':inputrefs,'objects':[{'id':k,'domain':d,'descriptor':v}for k,(d,v)in objects.items()],'blobs':[{'digest':k,'hex':v.hex()}for k,v in blobs.items()],'owner':owner,'before':before,'expected':after})
raw=(''.join(json.dumps(r,separators=(',',':'))+'\n'for r in rows)).encode();(B/'cases.ndjson.xz').write_bytes(lzma.compress(raw));(B/'cases-pin.json').write_text(json.dumps({'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()},indent=2)+'\n');report={'cases':len(rows),'admitted':n_ok,'refused':n_refused,'onlyChangedMaps':'normalized.closures and evidence.closures restricted to Plan semanticClosures','changedCases':diffs,'unchangedCases':len(rows)-len(diffs),'predecessorSha256':hashlib.sha256(old.encode()).hexdigest(),'candidateSha256':hashlib.sha256(p.read_bytes()).hexdigest(),'standing':'Proposed reference correction, not selected. Preserves inventory/incoming occurrences; no other reconstruction field differs.'};(B/'comparison.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k!='changedCases'}));print('changed',len(diffs))
