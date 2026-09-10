from pathlib import Path
import json,hashlib,shutil,subprocess
R=Path.cwd();src=Path('/tmp/opensip-design-corrections/v21-evaluator-contract-assessment.v2');dest=R/'docs/coop/design-corrections/reviews'/src.name;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((src/'response.json').read_text());assert r['is_error'] and r['api_error_status']==429 and r['session_id']=='006a1d7b-0dff-4d8b-98ce-a5ba8abf6e1b';assert not dest.exists();dest.mkdir();files=[]
for p in sorted(src.rglob('*')):
 if '.venv' in p.relative_to(src).parts or '__pycache__' in p.parts or not p.is_file():continue
 assert not p.is_symlink();q=dest/p.relative_to(src);q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q);assert sha(q)==sha(p);files.append({'path':str(q.relative_to(dest)),'sha256':sha(q),'bytes':q.stat().st_size})
log=Path('/Users/sb/.claude/projects/-private-tmp-opensip-design-corrections-v21-evaluator-contract-assessment-v1/006a1d7b-0dff-4d8b-98ce-a5ba8abf6e1b.jsonl');blocks=[];active=False;matches=0
for l in log.read_text().split('\n'):
 if not l:continue
 x=json.loads(l);m=x.get('message',{});cs=m.get('content',[])
 if x.get('type')=='user' and isinstance(cs,str) and cs==(src/'prompt.txt').read_text():active=True;matches+=1
 if active:
  for c in cs if isinstance(cs,list) else []:
   if isinstance(c,dict) and c.get('type') in ('tool_use','tool_result'):blocks.append({'timestamp':x.get('timestamp'),'messageUuid':x.get('uuid'),'block':c})
assert matches==1;tool=dest/'tool-calls.json';tool.write_text(json.dumps(blocks,indent=2)+'\n')
envcode="import sys,unicodedata,json,importlib.metadata as m;print(json.dumps({'python':sys.version,'unicode':unicodedata.unidata_version,'packages':{n:m.version(n) for n in ['jsonschema','referencing','attrs','rpds-py','jsonschema-specifications']}},indent=2))"
env=subprocess.run([str(src/'.venv/bin/python'),'-I','-B','-c',envcode],capture_output=True,text=True);(dest/'environment-observed.json').write_text(json.dumps({'standing':'Root read-only observation after interrupted reviewer, not proof every command used this environment.','exitCode':env.returncode,'stdout':env.stdout,'stderr':env.stderr},indent=2)+'\n')
cache=Path('/tmp/opensip-design-corrections/candidate-subject.v21/docs/coop/design-corrections/foundation/__pycache__/canonical.cpython-314.pyc');cust=dest/'additional-custody';cust.mkdir();q=cust/cache.name;shutil.copyfile(cache,q)
missing=[n for n in ['revised-assessment.json','proposal.md','proposal.json','validation-transcript.txt'] if not (src/n).exists()]
(dest/'custody.json').write_text(json.dumps({'standing':'INTERRUPTED actual Claude refinement. 429 weekly quota; not final proposal, not source assent, not independent or blind acceptance.','sessionId':r['session_id'],'actualModel':list(r['modelUsage']),'exactContinuationPromptVerified':True,'files':files,'publicToolBlocks':{'path':tool.name,'sha256':sha(tool),'count':len(blocks)},'missingPromisedArtifacts':missing,'environment':{'path':'environment-observed.json','venvExcludedFromCopy':'Local installed environment binaries/dependencies; observed package versions retained, original remains in tmp.'},'incidentalSnapshotCache':{'actualPath':str(cache),'retainedPath':str(q.relative_to(dest)),'sha256':sha(q),'bytes':q.stat().st_size,'standing':'Added unlisted Python3.14 cache observed after reviewer imported frozen canonical without -B; not a normative source change. Declared file integrity assessed separately.'},'blocker':r['result'],'implementationAuthorized':False},indent=2)+'\n');print(dest,len(files),len(blocks),missing)
