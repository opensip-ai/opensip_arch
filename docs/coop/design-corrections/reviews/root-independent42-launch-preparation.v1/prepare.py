from pathlib import Path
import json,hashlib,subprocess,ast,shutil
B=Path('/tmp/opensip-design-corrections');L=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews');P=Path(__file__).parent;A=B/'claude-independent-design.v40';N=B/'claude-independent-design.v42';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert json.loads((A/'process-completion.json').read_bytes())['exitCode']==0 and (A/'review.md').is_file() and (A/'review.json').is_file()
assert (L/A.name/'final-public-artifact-manifest.json').is_file()
ps=subprocess.run(['ps','-axo','comm=,args='],capture_output=True,text=True).stdout
assert not any(r.strip().split()[0].endswith('/claude') and '--resume 85a08aec-9d22-4ac6-8ec2-c10170e727d7' in r for r in ps.splitlines() if r.strip())
mf=L/'candidate-subject.v42.json';s=B/'candidate-subject.v42';archive=L/'candidate-source.v42.tar.gz';pkg=B/'claude-author-package-successor.v19';v=B/'author-package-final42-verification.v1/verification.json';ref=L/'codex-post-reset.v1/final-reference.v42/reference-checks.json';custody=json.loads((B/'root-final42-custody.v1/verification.json').read_bytes());m=json.loads(mf.read_bytes());binding=json.loads((pkg/'source-binding.v42.json').read_bytes())
assert H(mf)==custody['manifestSha256']==binding['formalSubjectManifestSha256'] and H(archive)==custody['archiveSha256'] and custody['allMembersAndPinsVerified']
assert json.loads(v.read_bytes())['passed'] and json.loads(ref.read_bytes())['passed']
assert m['parentManifestSha256']==H(L/'candidate-subject.v41.json')=='eb7a4c48d86c844914ffc0ef70743752655a411e453bbaa066cfaee572312236'
assert H(L/'candidate-subject.v40.json')=='3be452843acb6f5f234dfc1826b627a234d81e5a45edd70715a03715d7467072'
assert not N.exists();N.mkdir()
inputs=[mf,archive,pkg/'artifact-manifest.json',pkg/'source-binding.v42.json',v,ref,B/'root-author-package-final42-rebuild.v1/rebuild-report.json',s/'docs/v2/architecture/implementation-normative-inputs.v11.json',A/'review.json']
authors=['claude-view-attribution-assessment.v1','claude-attribution-capture-assessment.v1','claude-program-entry-clarification.v1','claude-program-entry-enforcement.v1']
roots=['root-view-attribution-integration.v1','root-capture-integration.v1','root-program-entry-clarification-integration.v1','root-program-entry-enforcement-integration.v1','root-planning-layer-history-clarification.v1']
header='Current exact source42 binding. Source '+str(s)+f'; {m["fileCount"]} members {m["totalBytes"]} bytes. Immediate parent41 preserved, last independently reviewed40 preserved. Actual final reference execution is root-source42-final-reference.v3; v2 was an environment launch failure and v1 predates the final programEntry correction. Package19 rebuilt from package15 plus native-v2 overlay. All inputs below are source or author review material; no blind outputs. Hash binding is custody, not an acceptance direction.\n\n'
for p in inputs:header+=str(p)+' SHA256 '+H(p)+'\n'
for name in authors:
 p=B/name/'review.json';header+=str(p)+' SHA256 '+H(p)+' (bounded author proposal, not independent acceptance)\n'
header+='Root integration records: '+', '.join(str(B/n) for n in roots)+'. Read their actual evidence as appropriate.\n\n'
(N/'prompt.md').write_text(header+(P/'review-scope.v2.md').read_text())
text=(A/'launch.py').read_text();tree=ast.parse(text);node=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='cmd' for x in n.targets));cmd=ast.literal_eval(node.value)
for path in [s,pkg,v.parent,B/'root-author-package-final42-rebuild.v1',A,B/'root-source42-final-reference.v3']+[B/n for n in authors+roots]:
 if str(path) not in cmd:cmd+=['--add-dir',str(path)]
lines=text.splitlines(True);lines[node.lineno-1:node.end_lineno]=['cmd='+repr(cmd)+'\n'];(N/'launch.py').write_text(''.join(lines))
d={'standing':'PREPARED UNLAUNCHED original non-author85 current42 review. Prior40 complete and idle; no blind inputs or acceptance prescribed.','sourceManifestSha256':H(mf),'parentReviewSha256':H(A/'review.json'),'promptSha256':H(N/'prompt.md'),'launcherSha256':H(N/'launch.py'),'runtime':str(N)};(N/'preparation.json').write_text(json.dumps(d,indent=2)+'\n');D=L/(N.name+'-dispatch');D.mkdir()
for name in ['prompt.md','launch.py','preparation.json']:shutil.copy2(N/name,D/name)
print(json.dumps(d))
