from pathlib import Path
import argparse,json,hashlib,importlib.util,copy
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();dc=a.root/'docs/coop/design-corrections'
s=importlib.util.spec_from_file_location('root_ownership_fixture',dc/'integration-fixtures.py');f=importlib.util.module_from_spec(s);s.loader.exec_module(f)
uid=f.UID('Cargo.toml','lib','fixture-root')
workspace={'edition':{'fixture-root':2021},'enumeration':'partial','units':[f.unit('Cargo.toml','lib','fixture-root','fixture-root')],'selectedUnitIds':[uid],'ownership':[{'path':'src/lib.rs','unitId':uid}]}
rows=[]
for name,change in [('producer-control',{}),('missing-cause-on-input-closure',{'deficiency':'input-closure-incomplete','nativeCause':None}),('unrelated-budget-deficiency',{'deficiency':'budget-exhausted','nativeCause':None}),('false-complete-claim',{'coverage':'complete','deficiency':None,'nativeCause':None})]:
 run,objects,blobs=f.build(resolved=False,has_match=False,relation='clones',universe_language='rust',source_path='src/lib.rs',workspace=copy.deepcopy(workspace))
 key=next(k for k,(d,v) in objects.items() if d=='coverage');coverage=copy.deepcopy(objects[key][1]);payload=f.C.parse(blobs[coverage['payloadDigest']]);original=copy.deepcopy(payload['entry'])
 if change:
  payload['entry'].update(change);coverage['payloadDigest']=f.put_blob(blobs,payload);f.rekey(objects,key,coverage,run);f.resync_witness(objects,blobs,run)
 try:result={'admitted':True,'runId':f.M.close_run(run,objects,blobs)}
 except Exception as exc:result={'admitted':False,'exception':type(exc).__name__,'detail':str(exc)[:400]}
 rows.append({'case':name,'ownershipEnumeration':'partial','sourceControlEntry':original,'entry':payload['entry'],'factCount':sum(d=='fact' for d,v in objects.values()),**result})
report={'standing':'Codex selected actual retained full-Run clone Coverage cause mutations over partial Rust ownership and an empty view. Candidate synthetic builder is construction helper only; expected required disclosure derives from Bv3M5 and owning contract. No native/compiler execution or product measurement. The producer control must close; mutated invalid pairs should refuse in corrected source.','sourceRoot':str(a.root),'sources':[{'path':str(p.relative_to(a.root)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [dc/'integration-fixtures.py',dc/'foundation/identity-model.py',dc/'native/native_evidence_model.v2.py',dc/'native/native-evidence.schemas.v2.json']],'cases':rows}
assert not a.out.exists();a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps([{'case':r['case'],'admitted':r['admitted'],'detail':r.get('detail'),'cause':r['entry']['nativeCause'],'deficiency':r['entry']['deficiency']} for r in rows],indent=2));assert rows[0]['admitted'],'Control did not close: cannot interpret mutations'
