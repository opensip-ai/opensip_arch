from pathlib import Path
import json,hashlib,shutil,uuid,argparse,ast
p=argparse.ArgumentParser();p.add_argument('--manifest-sha256',required=True);a=p.parse_args()
B=Path('/tmp/opensip-design-corrections');L=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews');O=B/'claude-independent-design.v37';h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
mf=L/'candidate-subject.v37.json';assert h(mf)==a.manifest_sha256;m=json.loads(mf.read_bytes());assert m['parentManifestSha256']=='a729406b9de0d865294884f7575ea943c0935437091389e2acebe8e5aedb4235'
c=json.loads((B/'root-final37-custody.v1/verification.json').read_bytes());assert c['manifestSha256']==h(mf) and c['archiveEveryMemberVerified']
pkg=B/'claude-author-package-successor.v14';vr=B/'author-package-final37-verification.v1/verification.json';v=json.loads(vr.read_bytes());assert v['passed'] and v['sourceManifestSha256']==h(mf) and v['packageManifestSha256']==h(pkg/'artifact-manifest.json')
assert not O.exists();O.mkdir();sid=str(uuid.uuid4())
text=(B/'root-source37-preparation.v1/fresh-independent37.prompt.template.md').read_text()
for old,new in {'@SUBJECT_SHA256@':h(mf),'@AUTHOR_PACKAGE@':str(pkg),'@PACKAGE_SHA256@':h(pkg/'artifact-manifest.json')}.items():assert old in text;text=text.replace(old,new)
assert '@SUBJECT' not in text and '@PACKAGE' not in text and '@AUTHOR' not in text
text+=f'\nExact current archive SHA256 {h(L/"candidate-source.v37.tar.gz")}; manifest fileCount {m["fileCount"]}, totalBytes {m["totalBytes"]}. Root current reference receipts: {L/"codex-post-reset.v1/final-reference.v37"}; root package revalidation {vr}. These are source-bound nonblind evidence, not your acceptance. Write only {O}. Actual new origin expected {sid}.\n'
(O/'prompt.md').write_text(text)
t=(B/'claude-independent-design.v26/launch.py').read_text();start=t.index('cmd=');end=t.index('\nstart=time.time()',start)
cmd=['/Users/sb/.local/bin/claude','--safe-mode','--strict-mcp-config','--model','opus','--session-id',sid,'--permission-mode','dontAsk','--tools','Read,Glob,Grep,Bash,Write,Edit','--allowedTools','Read','Glob','Grep','Write','Edit','Bash(python3 *)','Bash(/tmp/opensip-architecture-review-env/bin/python *)']
for d in [Path(m['snapshotRoot']),B/'candidate-subject.v36',pkg,vr.parent,L,Path('/tmp/opensip-architecture-review-env')]:cmd+=['--add-dir',str(d)]
cmd+=['--output-format','stream-json','--verbose','-p'];launch=t[:start]+'cmd='+repr(cmd)+t[end:];ast.parse(launch);assert '--resume' not in launch;(O/'launch.py').write_text(launch)
(O/'dispatch.json').write_text(json.dumps({'standing':'Prepared fresh origin only; actual init and substantive review required','sessionId':sid,'manifestSha256':h(mf),'promptSha256':h(O/'prompt.md'),'packageManifestSha256':h(pkg/'artifact-manifest.json'),'packageVerificationSha256':h(vr),'freshOrigin':True,'originalCharterPreserved':'Full original26 fresh-design charter, updated current binding and explicit current107 obligations. No prior read/verdict inheritance.'},indent=2)+'\n')
shutil.copytree(O,L/(O.name+'-dispatch'));print(json.dumps({'prepared':str(O),'sessionId':sid,'promptSha256':h(O/'prompt.md')}))
