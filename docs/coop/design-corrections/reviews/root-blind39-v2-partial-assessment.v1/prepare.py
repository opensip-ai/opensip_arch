from pathlib import Path
import json,hashlib,shutil,subprocess,ast
B=Path('/tmp/opensip-design-corrections');L=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews');O=Path(__file__).parent
A=B/'consumer-b.v24-source39.v2';N=B/'consumer-b.v24-source39.v3';F=B/'candidate-subject.v39';H=lambda b:hashlib.sha256(b).hexdigest()
assert json.loads((A/'process-completion.json').read_bytes())['exitCode']==0
assert not (A/'output/blind-review.json').exists()
processes=subprocess.run(['ps','-axo','pid,ppid,command'],capture_output=True,text=True).stdout
assert not any(str(A) in line and ('/python' in line or '/claude --' in line) for line in processes.splitlines()),'Prior child still running'
pub=L/A.name/'final-public-artifact-manifest.json';d=json.loads(pub.read_bytes());drift=[]
for r in d['files']:
 q=pub.parent/r['retainedPath'] if 'retainedPath' in r else F/r['sameAsSubjectPath'];raw=q.read_bytes();assert H(raw)==r['sha256'] and len(raw)==r['bytes']
 p=A/r['runtimePath'];b=p.read_bytes()
 if H(b)!=r['sha256'] or len(b)!=r['bytes']:drift.append(r['runtimePath'])
assert not drift,drift
N.mkdir();shutil.copytree(A/'subject',N/'subject');shutil.copytree(A/'output',N/'output')
for name in ['requirements.json','charter.md']:
 raw=(A/name).read_text();(N/name).write_text(raw.replace(str(A),str(N)).replace(A.name,N.name))
req=json.loads((N/'requirements.json').read_bytes());old=json.loads((A/'requirements.json').read_bytes())
for key,count in [('requirements',123),('standing',8),('futureQualification',3)]:
 assert len(req[key])==count and [r['id'] for r in req[key]]==[r['id'] for r in old[key]]
assert (N/'subject/consumer-input-manifest.json').read_bytes()==(A/'subject/consumer-input-manifest.json').read_bytes()
prompt=f'''Continue ONLY your SAME original blind origin 9d3dfb70-b2d3-498c-a3c1-f8de9e488514. Your prior runtime {A} ended with a status response BEFORE its final chain, checkpoints and substantive review were complete. It is now idle, its public artifacts have been preserved and reverified, and there is no quota error. This NEW runtime {N} contains an exact copy of its existing output/ and unchanged subject/ kit. Charter/requirements changed ONLY runtime paths. A copied output is your prior measured work, never a newly executed result.

Finish that outstanding work. This is a bounded COMPLETION continuation, not a new investigation or a new design kit. Read your own final-response in {A}, this charter/requirements and the pending chain's own runtime logs. Adapt only your own helper/output paths to this new runtime, preserving the copies of historical outputs and failed attempts; do not write to old runtimes. Complete the unfinished admission/replay export/termination/negative/provenance/notes/checkpoints/final review obligations you listed, reusing already completed exact-source results honestly. Do not rerun the whole completed investigation without a specific change/failure requiring it. Do not mark unperformed work complete by copying counters. Finish every subprocess, poll only your own public runtime progress in <=60-second intervals, and DO NOT end with a status response while children or required report work remain. CLI process exit 0 alone is not task completion.

Verify unchanged subject/consumer-input-manifest.json SHA c2f2f88d2e3bebfa8fa1b521cb76d2584483eb922973d6e555fe05a15da4ad80 and all104members, parent39 f71a59928d1b6aa84eed81b8cb49fd1fba91c65dd6599c58f99efcdc42569009. Original123requirements8standing3future remain. No source successor, expected answers, root admission result, root diagnostics or other agent work is supplied. Only own old24/source39v1/v2 and new output, current kit, installed standard library/jsonschema allowed. Never LIVE, frozen author source/model/fixtures, root artifacts, other agent results, private logs, web, subagents, product, commit/push or activation. Use /tmp/opensip-architecture-review-env/bin/python -I -B. Write only this runtime output/.

Deliver substantive output/blind-review.md and output/blind-review.json, with exact final export claims and original requirement dispositions, your own completed independent closure/replay results and all actual limitations. Retain the independent retained-graph validator separately from the emitter. Any remaining normative issue on unchanged39 must be reported as such, not assumed fixed. Report actual acceptance standing only after all charter/report conditions hold; partial successful checks do not imply acceptance. No additional full-Run category or scope is introduced by this prompt.
'''
(N/'prompt.md').write_text(prompt)
launcher=(A/'launch.py').read_text();tree=ast.parse(launcher);cmdnode=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='cmd' for t in n.targets));cmd=ast.literal_eval(cmdnode.value)
cmd+=['--add-dir',str(A)];lines=launcher.splitlines(True);lines[cmdnode.lineno-1:cmdnode.end_lineno]=['cmd='+repr(cmd)+'\n'];(N/'launch.py').write_text(''.join(lines))
report={'standing':'INCOMPLETE prior actual Claude review, no substantive final MD/JSON. Retainer was invoked after parent completion but before checking report existence; preserved as partial custody only, never final acceptance. All retained/current files verified stable and no prior child alive before copying. Same original reviewer completion continuation prepared; no root outcome supplied.','publicManifestSha256':H(pub.read_bytes()),'publicFilesVerified':len(d['files']),'runtimeDrift':drift,'priorResultSha256':H((A/'result.json').read_bytes()),'newRuntime':str(N),'kitManifestSha256':H((N/'subject/consumer-input-manifest.json').read_bytes()),'requiredScopeUnchanged':True,'launchPending':True}
(O/'assessment.json').write_text(json.dumps(report,indent=2)+'\n');shutil.copytree(O,L/O.name)
dispatch=L/(N.name+'-dispatch');dispatch.mkdir()
for name in ['prompt.md','launch.py','requirements.json','charter.md']:shutil.copy2(N/name,dispatch/name)
print(json.dumps(report))
