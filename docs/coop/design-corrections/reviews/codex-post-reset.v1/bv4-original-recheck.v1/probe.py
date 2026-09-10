"""Root diagnostic recheck against exact frozen v13; no accepted files edited."""
from pathlib import Path
import hashlib,importlib.util,json,shutil
root=Path('/tmp/opensip-design-corrections/candidate-subject.v13');dc=root/'docs/coop/design-corrections'
out=Path('/tmp/opensip-design-corrections/bv4-original-recheck.v1');out.mkdir(exist_ok=False)
def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
f=load('bv4_original_fixtures',dc/'integration-fixtures.py')
cases=[]
for path in ['tool/main.py','LICENSE','README.md','src/plain.rs']:
 r={'path':path,'relation':'file','source':'existing author fixture construction, root-selected path'}
 try:
  run,objects,blobs=f.build(resolved=False,has_match=True,universe_language='syntax',relation='file',source_path=path)
  r['runId']=f.M.close_run(run,objects,blobs);r['outcome']='ADMIT'
  r['fileFacts']=[v for domain,v in objects.values() if domain=='fact' and v['relation']=='file']
 except Exception as e:r.update(outcome='REFUSE',cause=type(e).__name__+':'+str(e))
 cases.append(r)
n=load('bv4_original_native',dc/'native/native_evidence_model.v2.py')
helper=[]
for relation,rung in [('file','enumerated'),('package','enumerated'),('vcs-change','enumerated'),('declares','syntactic')]:
 helper.append({'relation':relation,'rung':rung,'noSelectedGrammars':True,'path':'tool/main.py','requireAll':True,'result':n.syntax_capability_support([],relation,rung,['tool/main.py'],True)})
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
report={'standing':'Actual Codex diagnostic on original frozen v13. Existing author reference/fixtures plus root-selected paths; NOT independent blind evidence or product qualification. Read the actual outcomes; constructor errors are not admission refusals.','sourceRoot':str(root),'sources':[{'path':str(p.relative_to(root)),'sha256':sha(p)} for p in [dc/'integration-fixtures.py',dc/'foundation/identity-model.py',dc/'native/native_evidence_model.v2.py']],'cases':cases,'helperCases':helper,'limitation':'Fixture uses a broader synthetic snapshot. This probes actual reference inventory exemption; it does not resolve the contradictory normative wording or decide canonical anchor policy.'}
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');shutil.copyfile(__file__,out/'probe.py')
print(json.dumps(report,indent=2))
