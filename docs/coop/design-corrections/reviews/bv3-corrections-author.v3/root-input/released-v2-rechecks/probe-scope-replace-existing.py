from pathlib import Path
import argparse,json,hashlib,importlib.util,copy
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();dc=a.root/'docs/coop/design-corrections'
s=importlib.util.spec_from_file_location('root_scope_fixture',dc/'integration-fixtures.py');f=importlib.util.module_from_spec(s);s.loader.exec_module(f)
scope={'schemaFamily':'opensip.product.scope','schemaMajor':1,'include':['**'],'exclude':[]}
rows=[]
for name,value,unknown_schema in [('base-control',None,False),('registered-scope-policy',scope,False),('missing-required-include',{k:v for k,v in scope.items() if k!='include'},False),('wrong-record-selector',{'schemaFamily':'opensip.product.policy','schemaMajor':1,'rules':[]},False),('unregistered-parameter-schema',scope,True)]:
 run,objects,blobs=f.build();before=run['planId']
 if value is not None:
  document=(dc/'workflows/schemas/policy-document.schema.json').read_bytes()
  if unknown_schema:document=b'{}'
  row={'schemaDigest':f.put_blob(blobs,document),'payloadDigest':f.put_blob(blobs,value)}
  plan=copy.deepcopy(objects[run['planId']][1]);spec=f.C.parse(blobs[plan['analysisSpecDigest']]);spec['parameters']=sorted([x for x in spec['parameters'] if x['schemaDigest']!=row['schemaDigest']]+[row],key=f.C.canonical)
  plan['analysisSpecDigest']=f.put_blob(blobs,spec);f.rekey_plan(objects,blobs,run,plan)
 try:result={'admitted':True,'runId':f.M.close_run(run,objects,blobs)}
 except Exception as exc:result={'admitted':False,'exception':type(exc).__name__,'detail':str(exc)[:320]}
 rows.append({'case':name,'planMoved':run['planId']!=before,**result})
report={'standing':'Codex selected retained full-Run parameter admission probes using the exact candidate synthetic fixture builder solely as a construction helper, never an independent oracle. No product measurement. Lawful scope parameter must be representable; malformed, wrong-selector and unregistered controls must refuse. Before v12 legal scope refuses too.','sourceRoot':str(a.root),'sources':[{'path':str(p.relative_to(a.root)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [dc/'integration-fixtures.py',dc/'foundation/identity-model.py',dc/'foundation/identity-schemas.v2.json',dc/'workflows/schemas/policy-document.schema.json']],'cases':rows}
assert not a.out.exists();a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(rows,indent=2))
