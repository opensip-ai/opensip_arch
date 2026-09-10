from pathlib import Path
import hashlib,importlib.util,json,shutil
root=Path('/tmp/opensip-design-corrections/bv4-totality-recheck.v1/work')
source=root/'docs/coop/design-corrections/integration-fixtures.py'
s=importlib.util.spec_from_file_location('request_fixture',source);f=importlib.util.module_from_spec(s);s.loader.exec_module(f)
rows=[]
for relation in ('references','types','declares','file'):
 row={'relation':relation,'requestedLanguageMode':'syntax-only','sourcePath':'src/lib.rs','hasCompilerUnits':False}
 try:
  run,objects,blobs=f.build(resolved=False,has_match=False,relation=relation,source_path='src/lib.rs',pure_syntax=True,universe_language='syntax')
  row['runId']=f.M.close_run(run,objects,blobs)
  plan=objects[run['planId']][1]
  row['requestedCapabilities']=f.C.parse(blobs[plan['analysisSpecDigest']])['requestedCapabilities']
  row['coverageEntries']=[f.C.parse(blobs[v['payloadDigest']])['entry'] for d,v in objects.values() if d=='coverage']
  row['outcome']='ADMIT'
 except Exception as exc:row.update(outcome='REFUSE_OR_HARNESS_ERROR',error=type(exc).__name__+':'+str(exc))
 rows.append(row)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
report={'standing':'Actual root-selected retained-Run admission controls on captured interim author source. Synthetic compiler-free fixture; no evaluation verdict, native execution, independent acceptance or product qualification inferred. Requested references/syntax-only is intentionally unsupported and must remain representable with unknown Coverage. Other relation cases reuse the same fixture request and do not prove per-capability request/output bijection.','sourceRoot':str(root),'fixtureSha256':sha(source),'identityModelSha256':sha(source.parent/'foundation/identity-model.py'),'nativeModelSha256':sha(source.parent/'native/native_evidence_model.v2.py'),'cases':rows}
out=Path('/tmp/opensip-design-corrections/bv4-request-recheck.v1');out.mkdir(exist_ok=False)
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');shutil.copyfile(__file__,out/'probe.py')
print(json.dumps(report,indent=2))
