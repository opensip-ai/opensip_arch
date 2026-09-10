from pathlib import Path
import argparse,json,hashlib,importlib.util,copy
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();dc=a.root/'docs/coop/design-corrections'
s=importlib.util.spec_from_file_location('root_mirror_identity',dc/'foundation/identity-model.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);w=m.workflow_admission()
blob=lambda i:{'path':f'src/f{i:05d}.txt','sha256':'a'*64,'bytes':1}
wrapper={'schemaVersion':2,'kind':'dependency',**{k:'a'*64 for k in ['payloadSchemaDigest','payloadDigest','sourceCorrespondenceDigest','buildDigest','scopeDigest','observationDigest']},'producerClosure':'closure2:'+'b'*64,'adapterClosure':'closure2:'+'c'*64,'blobs':[blob(0)],'completeness':'complete','omissions':[]}
scope={'schemaVersion':2,'workspaceRoots':['a','b'],'pathPrefixes':['a','b'],'excludedPathPrefixes':['x','z']}
cases=[]
for name,v in [('valid-one',wrapper),('valid-sorted-omissions',dict(wrapper,omissions=['a','b'])),('reversed-omissions',dict(wrapper,omissions=['b','a'])),('duplicate-omissions',dict(wrapper,omissions=['a','a'])),('zero-blobs',dict(wrapper,blobs=[])),('4097-blobs',dict(wrapper,blobs=[blob(i) for i in range(4097)]))]:cases.append((name,'import','ImportWrapperV2',v))
cases.append(('valid-scope','scope-descriptor','ImportScopeDescriptor',scope))
for key in ['workspaceRoots','pathPrefixes','excludedPathPrefixes']:
 for label,values in [('reverse',['b','a']),('duplicate',['a','a'])]:cases.append((key+'-'+label,'scope-descriptor','ImportScopeDescriptor',dict(scope,**{key:values})))
rows=[]
for name,fdef,wdef,v in cases:
 def foundation():
  if fdef=='import':return m.identifier('import',v)
  m.validate_registered_record('foundation/identity-schemas.v2.json','#/$defs/'+fdef,v);m.ordered(v)
 def workflow():return w.validate_import_record('workflows/schemas/imported-evidence.schema.json','#/$defs/'+wdef,v)
 results={}
 for label,fn in [('foundation',foundation),('workflow',workflow)]:
  try:fn();results[label]={'admitted':True}
  except Exception as exc:results[label]={'admitted':False,'exception':type(exc).__name__,'detail':str(exc)[:180]}
 rows.append({'case':name,'sameAdmission':results['foundation']['admitted']==results['workflow']['admitted'],**results})
report={'standing':'Codex independently selected mirror admission cases; synthetic digest values test descriptor admission/order only, not retained Run closure. Foundation import uses its real identifier gate; scope uses registered validation plus owning order gate. Workflow uses actual registered validator.','sourceRoot':str(a.root),'sources':[{'path':str(p.relative_to(a.root)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [dc/'foundation/identity-model.py',dc/'foundation/identity-schemas.v2.json',dc/'workflows/workflows_model.v1.py',dc/'workflows/schemas/imported-evidence.schema.json']],'cases':rows,'mismatches':[r['case'] for r in rows if not r['sameAdmission']]}
assert not a.out.exists();a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'cases':len(rows),'mismatches':report['mismatches']}))
