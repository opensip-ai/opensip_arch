"""Prepare, never launch, a normative-only continuation of the original fresh blind origin.
Requires a frozen final manifest and a schema-reference-complete generated subject kit first.
"""
from pathlib import Path
import argparse,json,hashlib
p=argparse.ArgumentParser();p.add_argument('--runtime',type=Path,required=True);p.add_argument('--manifest',type=Path,required=True);p.add_argument('--manifest-sha256',required=True);p.add_argument('--version',type=int,required=True);a=p.parse_args()
R=Path('/tmp/opensip-design-corrections');old=R/'consumer-b.v24-source38.v1';out=a.runtime.resolve()
sha=lambda b:hashlib.sha256(b).hexdigest()
raw=a.manifest.read_bytes();assert sha(raw)==a.manifest_sha256
kit=out/'subject/consumer-input-manifest.json';k=json.loads(kit.read_bytes());assert k['parentSubjectSha256']==a.manifest_sha256
for row in k['files']:
 b=(out/'subject'/row['path']).read_bytes();assert sha(b)==row['sha256'] and len(b)==row['bytes']
assert not any((out/n).exists() for n in ['charter.md','requirements.json','prompt.md','launch.py'])
oldp=json.loads((old/'preparation.json').read_bytes());sub={str(old):str(out),'consumer-b.v24-source38.v1':out.name,'source38':f'source{a.version}',oldp['sourceManifestSha256']:a.manifest_sha256,oldp['kitManifestSha256']:sha(kit.read_bytes())}
def rewrite(t):
 for x,y in sub.items():t=t.replace(x,y)
 return t
charter=rewrite((old/'charter.md').read_text());req=json.loads(rewrite((old/'requirements.json').read_text()));prior=json.loads((old/'requirements.json').read_text())
for group,n in [('requirements',123),('standing',8),('futureQualification',3)]:
 assert len(req[group])==n and [r['id'] for r in req[group]]==[r['id'] for r in prior[group]]
(out/'charter.md').write_text(charter);(out/'requirements.json').write_text(json.dumps(req,indent=2)+'\n');(out/'output').mkdir()
prompt=f"""Continue ONLY your SAME original independently fresh blind origin 9d3dfb70-b2d3-498c-a3c1-f8de9e488514 in this NEW runtime {out}. Your prior completed work in /tmp/opensip-design-corrections/consumer-b.v24 is read-only history and your own work, not current conformance. Preserve it. No other consumer or coauthor inputs are allowed.
Read charter.md and requirements.json fully, verify new normative-only subject/consumer-input-manifest.json SHA {sha(kit.read_bytes())} and every member, parent frozen manifest SHA {a.manifest_sha256}. Current normative owners govern this independent reconstruction; no design acceptance or expected result is supplied. The original123requirements8standing3futurequalification scope remains unchanged. Prior source outputs do not establish current-source conformance. Continue your own helpers from your own previous work as useful, preserving old failures before any corrections. Read ONLY new subject/charter/requirements and your own old/new outputs, plus installed standard library/jsonschema; never read LIVE, author models, fixtures, reports, root results or other runtimes. No subagents.
Independently reconstruct and execute the complete required current-source examples, validate every claimed complete positive through owning schemas INCLUDING published registry keywords, closure joins and full semantic proof replay, export all required records and exact bytes, and complete every original standalone/schema/query requirement. Use /tmp/opensip-architecture-review-env/bin/python -I -B. Missing required normative custody is a specific input-custody finding; report a contradictory or missing law with exact selectors. Correct helper errors only from your own work and normative kit. Do not lower the scope, invent expected outputs, or substitute a summary/count check for the required boundary. Write only this runtime output/. No product, commit/push, activation or root acceptance.
Maintain full-ID checkpoints and retained executions; finish every subprocess before substantive output/blind-review.md/json. ACCEPT-RECONSTRUCTABLE only if all charter conditions actually hold; otherwise give precise CHANGES_REQUIRED or actual blocker. Root separately validates exact exported positives, with no feedback or repaired export supplied to you. No acceptance is implied by the new kit or this continuation.
"""
(out/'prompt.md').write_text(prompt)
launch=(R/'consumer-b.v24/launch.py').read_text().replace("'--session-id'","'--resume'")
(out/'launch.py').write_text(launch)
(out/'preparation.json').write_text(json.dumps({'standing':'PREPARED, UNLAUNCHED; original blind origin, normative-only successor, no oracle or acceptance','version':a.version,'subjectManifestSha256':a.manifest_sha256,'kitManifestSha256':sha(kit.read_bytes()),'kitFiles':len(k['files']),'originalRequirements':123,'standingRules':8,'futureQualification':3,'sessionId':'9d3dfb70-b2d3-498c-a3c1-f8de9e488514','charterSha256':sha((out/'charter.md').read_bytes()),'requirementsSha256':sha((out/'requirements.json').read_bytes())},indent=2)+'\n')
print('Prepared; not launched',out)
