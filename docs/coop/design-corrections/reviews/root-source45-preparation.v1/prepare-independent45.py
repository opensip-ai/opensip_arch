"""Prepare exact44 continuation of the independent non-author origin; never accept or launch."""
from pathlib import Path
import json,hashlib,subprocess,ast,shutil
B=Path('/tmp/opensip-design-corrections');L=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews');P=Path(__file__).parent
A=B/'claude-independent-design.v44';N=B/'claude-independent-design.v45';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();J=lambda p:json.loads(p.read_bytes())
SID='85a08aec-9d22-4ac6-8ec2-c10170e727d7'
assert J(A/'process-completion.json')['exitCode']==0 and J(A/'review.json')['verdict']=='ACCEPT'
ps=subprocess.run(['ps','-axo','comm=,args='],capture_output=True,text=True,check=True).stdout
assert not any(r.strip().split()[0].endswith('/claude') and '--resume '+SID in r for r in ps.splitlines() if r.strip())
mf=L/'candidate-subject.v45.json';src=B/'candidate-subject.v45';archive=L/'candidate-source.v45.tar.gz';pkg=B/'claude-author-package-successor.v22';rebuild=B/'root-author-package-final45-rebuild.v1';ref=L/'codex-post-reset.v1/final-reference.v45/reference-checks.json'
c=J(B/'root-final45-custody.v1/verification.json');m=J(mf);binding=J(pkg/'source-binding.v45.json')
assert H(mf)==c['manifestSha256']==binding['formalSubjectManifestSha256']=='8b4efbb04d9e25126ec7955931cf364f7013b3710a45c48bae8bc563a0c82155'
assert H(archive)==c['archiveSha256'] and c['allMembersAndPinsVerified']
assert m['parentManifestSha256']==H(L/'candidate-subject.v44.json')=='e873c8db7b50f8d4bc4c6b1754239fb200b11f4e5d0f23b1ceaa6ea17297a32b'
assert J(rebuild/'rebuild-report.json')['passed'] and J(ref)['passed']
for row in J(pkg/'artifact-manifest.json')['files']:
 p=pkg/row['path'];assert H(p)==row['sha256'] and p.stat().st_size==row['bytes']
assert not N.exists();N.mkdir()
inputs=[mf,archive,L/'candidate-subject.v44.json',pkg/'artifact-manifest.json',pkg/'source-binding.v45.json',rebuild/'rebuild-report.json',ref,L/'root-source45-companion-checks.v2/checks.json',src/'docs/v2/architecture/implementation-normative-inputs.v13.json',A/'review.json']
header=f"""Exact source45, parent44. Source {src}; {m['fileCount']} members, {m['totalBytes']} bytes.14 modified/1 added/0 removed. Current custody validates snapshot/archive/parent/all6264 pins. All six root groups/seventeen evaluator children and both companion checks PASS. Package22 rebuilt FROM package15+native-v2 overlay, then formally bound45. No acceptance prescribed. Assess exact source delta independently; no blind material or expected blind results supplied.

Source-only correction rationale: section9.7's pre-Analyze Unavailable conversion previously invoked closed_world_v2 by name without publishing its complete output. Knowing the Python implementation could hide a missing normative recipe. The new law publishes the complete hostConversionClosedWorld value, with conversion-only scope and no claim that dynamic loading is absent. Native reference uses the law, two existing cases pin all fields, and the checker binds prose/machine law/helper consistency. Generic TS/Rust historical batch prose is clarified in three places; public registered-schema shapes stay unchanged. The native-cases JSON was reindented; compare its parsed structure to distinguish the two semantic case additions from whitespace. Planning13 binds current inputs and preserves12. No other product feature or architecture change is intended; verify rather than assume.

Your source44 OBS44-05..07 limitations remain material: reference checks do not validate all provider-authored descriptors, all cancellation correlations, all commitments or full process/compiler behavior. Keep measured subset claims precise; normative requirements are not executed proof. ADV44-01 optional direct planning input coverage and ADV42-01 implementation verification remain to be accounted; do not invent product qualification or newly require optional features.

"""
for p in inputs:header+=str(p)+' SHA256 '+H(p)+'\n'
(N/'prompt.md').write_text(header+'\n'+(P/'review-scope.md').read_text())
text=(A/'launch.py').read_text();node=next(n for n in ast.parse(text).body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='cmd' for x in n.targets))
cmd=['/Users/sb/.local/bin/claude','--safe-mode','--strict-mcp-config','--model','opus','--resume',SID,'--permission-mode','dontAsk','--tools','Read,Glob,Grep,Bash,Write,Edit','--allowedTools','Read','Glob','Grep','Write','Edit','Bash(python3 *)','Bash(/tmp/opensip-architecture-review-env/bin/python *)','--output-format','stream-json','--verbose','-p']
for p in [src,B/'candidate-subject.v44',B/'candidate-subject.v42',B/'candidate-subject.v40',L,Path('/tmp/opensip-architecture-review-env'),A,B/'claude-independent-design.v42',B/'claude-independent-design.v40',pkg,rebuild,B/'root-source45-final-reference.v1']:
 cmd+=['--add-dir',str(p)]
lines=text.splitlines(True);lines[node.lineno-1:node.end_lineno]=['cmd='+repr(cmd)+'\n'];(N/'launch.py').write_text(''.join(lines))
d={'standing':'PREPARED UNLAUNCHED independent non-author85 current45 review; prior44 complete/idle; no blind inputs or acceptance prescribed.','sourceManifestSha256':H(mf),'parentReviewSha256':H(A/'review.json'),'packageManifestSha256':H(pkg/'artifact-manifest.json'),'promptSha256':H(N/'prompt.md'),'launcherSha256':H(N/'launch.py'),'runtime':str(N),'actualSessionId':SID}
(N/'preparation.json').write_text(json.dumps(d,indent=2)+'\n');D=L/(N.name+'-dispatch');D.mkdir()
for name in ['prompt.md','launch.py','preparation.json']:shutil.copyfile(N/name,D/name)
print(json.dumps(d))
