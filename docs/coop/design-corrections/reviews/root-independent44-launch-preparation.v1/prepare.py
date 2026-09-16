"""Prepare exact44 continuation of the independent non-author origin; never accept or launch."""
from pathlib import Path
import json,hashlib,subprocess,ast,shutil
B=Path('/tmp/opensip-design-corrections');L=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews');P=Path(__file__).parent
A=B/'claude-independent-design.v43';N=B/'claude-independent-design.v44';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();J=lambda p:json.loads(p.read_bytes())
SID='85a08aec-9d22-4ac6-8ec2-c10170e727d7'
assert J(A/'process-completion.json')['exitCode']==0 and J(A/'review.json')['verdict']=='ACCEPT'
ps=subprocess.run(['ps','-axo','comm=,args='],capture_output=True,text=True,check=True).stdout
assert not any(r.strip().split()[0].endswith('/claude') and '--resume '+SID in r for r in ps.splitlines() if r.strip())
mf=L/'candidate-subject.v44.json';src=B/'candidate-subject.v44';archive=L/'candidate-source.v44.tar.gz';pkg=B/'claude-author-package-successor.v21';rebuild=B/'root-author-package-final44-rebuild.v1';ref=L/'codex-post-reset.v1/final-reference.v44/reference-checks.json'
c=J(B/'root-final44-resume-custody.v1/verification.json');m=J(mf);binding=J(pkg/'source-binding.v44.json')
assert H(mf)==c['manifestSha256']==binding['formalSubjectManifestSha256']=='e873c8db7b50f8d4bc4c6b1754239fb200b11f4e5d0f23b1ceaa6ea17297a32b'
assert H(archive)==c['archiveSha256'] and c['allMembersAndPinsVerified']
assert m['parentManifestSha256']==H(L/'candidate-subject.v43.json')=='db43ee76f91b08dc5076d152761ddef795a3645fafa690a3974d693bedaf897d'
assert J(rebuild/'rebuild-report.json')['passed'] and J(ref)['passed']
for row in J(pkg/'artifact-manifest.json')['files']:
 p=pkg/row['path'];assert H(p)==row['sha256'] and p.stat().st_size==row['bytes']
assert not N.exists();N.mkdir()
inputs=[mf,archive,L/'candidate-subject.v43.json',pkg/'artifact-manifest.json',pkg/'source-binding.v44.json',rebuild/'rebuild-report.json',ref,L/'root-source44-companion-checks.v1/checks.json',src/'docs/v2/architecture/implementation-normative-inputs.v12.json',A/'review.json',L/'claude-provider-wire43-correction.v1/review.md',L/'claude-provider-wire43-correction.v1/review.json',L/'claude-provider-startup43-correction.v1/review.md',L/'claude-provider-startup43-correction.v1/review.json',L/'root-startup43-scope-clarification.v1/clarification.json']
header=f'''Exact source44 binding, parent43. Source {src}; {m['fileCount']} members, {m['totalBytes']} bytes.24 modified/6 added/0 removed parent43 files. The changes are provider wire/startup normative publication and references, root scope clarification, source pins, current planning layer12 and generated reports. Actual root six groups/seventeen evaluator children PASS. Package21 was rebuilt from package15+native-v2 overlay, then metadata-bound; all17exports/seven queries/nine membership probes passed. Derive Run-ID continuity yourself. No acceptance prescribed. Only source-author reports supplied; do not read broader author runtime histories or any blind material/root blind results. Source schema/order additions are normative; Python helpers are reference evidence, never blind input.

The inherited scope text below calls for package21 verification: its actual current evidence is rebuild-report.json and work/verification/verification.json in the listed rebuild directory, plus source-binding.v44.json, rather than a separate redundantly rerun verification directory. Final metadata binding preserves every export and replay helper byte. Assess it substantively; do not infer acceptance from metadata.

'''
for p in inputs:header+=str(p)+' SHA256 '+H(p)+'\n'
(N/'prompt.md').write_text(header+'\n'+(P/'review-scope.md').read_text())
text=(A/'launch.py').read_text();node=next(n for n in ast.parse(text).body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='cmd' for x in n.targets))
cmd=['/Users/sb/.local/bin/claude','--safe-mode','--strict-mcp-config','--model','opus','--resume',SID,'--permission-mode','dontAsk','--tools','Read,Glob,Grep,Bash,Write,Edit','--allowedTools','Read','Glob','Grep','Write','Edit','Bash(python3 *)','Bash(/tmp/opensip-architecture-review-env/bin/python *)','--output-format','stream-json','--verbose','-p']
for p in [src,B/'candidate-subject.v43',B/'candidate-subject.v42',B/'candidate-subject.v40',L,Path('/tmp/opensip-architecture-review-env'),A,B/'claude-independent-design.v42',B/'claude-independent-design.v40',pkg,rebuild,B/'root-source44-final-reference.v1']:
 cmd+=['--add-dir',str(p)]
lines=text.splitlines(True);lines[node.lineno-1:node.end_lineno]=['cmd='+repr(cmd)+'\n'];(N/'launch.py').write_text(''.join(lines))
d={'standing':'PREPARED UNLAUNCHED independent non-author85 current44 review; prior43 complete/idle; no blind inputs or acceptance prescribed.','sourceManifestSha256':H(mf),'parentReviewSha256':H(A/'review.json'),'packageManifestSha256':H(pkg/'artifact-manifest.json'),'promptSha256':H(N/'prompt.md'),'launcherSha256':H(N/'launch.py'),'runtime':str(N),'actualSessionId':SID}
(N/'preparation.json').write_text(json.dumps(d,indent=2)+'\n');D=L/(N.name+'-dispatch');D.mkdir()
for name in ['prompt.md','launch.py','preparation.json']:shutil.copyfile(N/name,D/name)
print(json.dumps(d))
