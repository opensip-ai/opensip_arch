from pathlib import Path
import copy,hashlib,importlib.util,json,shutil
root=Path('/tmp/opensip-design-corrections/bv4-final-source-recheck.v2/work')
source=root/'docs/coop/design-corrections/integration-fixtures.py'
s=importlib.util.spec_from_file_location('derivation_fixture',source);f=importlib.util.module_from_spec(s);s.loader.exec_module(f)
rows=[]
for relation in ('references','types'):
 row={'relation':relation,'declaredDeficiency':'derivation-policy-unmet','derivationKinds':['compiler-inferred']}
 try:
  run,objects,blobs=f.build(resolved=False,has_match=True,relation=relation)
  cid=next(k for k,(d,v) in objects.items() if d=='coverage');coverage=copy.deepcopy(objects[cid][1]);payload=f.C.parse(blobs[coverage['payloadDigest']])
  payload['entry'].update(deficiency='derivation-policy-unmet',nativeCause=None,derivationKinds=['compiler-inferred'])
  coverage['payloadDigest']=f.put_blob(blobs,payload);f.rekey(objects,cid,coverage,run)
  f.resync_witness(objects,blobs,run);f.resync_proof_refs(objects,blobs,run)
  row.update(outcome='ADMIT',runId=f.M.close_run(run,objects,blobs))
 except Exception as exc:row.update(outcome='REFUSE_OR_HARNESS_ERROR',error=type(exc).__name__+':'+str(exc))
 rows.append(row)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
report={'standing':'Root full-Run recheck of previously supplied source observation, released final coauthor source. Synthetic author fixtures and root mutation; not evaluation/native execution/independent acceptance. Native section4.7 and sufficiency_v2 restrict derivationPolicy to the types relation. This compares only entry declaration support, not whether a particular policy demands the deficiency.','sourceRoot':str(root),'fixtureSha256':sha(source),'identityModelSha256':sha(source.parent/'foundation/identity-model.py'),'nativeModelSha256':sha(source.parent/'native/native_evidence_model.v2.py'),'cases':rows}
out=Path('/tmp/opensip-design-corrections/bv4-final-source-recheck.v2/derivation');out.mkdir(exist_ok=False)
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');shutil.copyfile(__file__,out/'probe.py');print(json.dumps(report,indent=2))
