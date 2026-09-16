"""Prepare a NEW actual Claude blind origin with unchanged complete charter. No launch."""
from pathlib import Path
import argparse,ast,hashlib,json,subprocess,sys,uuid
P=argparse.ArgumentParser();P.add_argument('--manifest-sha256',required=True);A=P.parse_args()
B=Path('/tmp/opensip-design-corrections');L=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews')
O=B/'consumer-b.v24';MF=L/'candidate-subject.v37.json';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert not O.exists();assert H(MF)==A.manifest_sha256
M=json.loads(MF.read_bytes());S=Path(M['snapshotRoot']);assert M['parentManifestSha256']=='a729406b9de0d865294884f7575ea943c0935437091389e2acebe8e5aedb4235'
# Previous kit is ONLY a normative path inventory. No previous consumer work is copied.
command=[sys.executable,'-I','-B',str(B/'final-claude-source-preparation.v5/prepare-blind-kit.py'),'--snapshot',str(S),'--origin-standing','fresh','--manifest',str(MF),'--manifest-sha256',H(MF),'--previous-kit-manifest',str(B/'consumer-b.v23/subject/consumer-input-manifest.json'),'--out',str(O/'subject')]
result=subprocess.run(command,capture_output=True,text=True);assert result.returncode==0,(result.stdout,result.stderr)
KIT=O/'subject/consumer-input-manifest.json';(O/'output').mkdir()
original_req=B/'consumer-b.v23/requirements.json';original_charter=B/'consumer-b.v23/original-charter-prompt.source26.md'
req=json.loads(original_req.read_bytes())
def relocate(v):
 if isinstance(v,str):return v.replace('/tmp/opensip-design-corrections/consumer-b.v13/output','/tmp/opensip-design-corrections/consumer-b.v24/output').replace('/tmp/opensip-design-corrections/consumer-b.v14/output','/tmp/opensip-design-corrections/consumer-b.v24/output')
 if isinstance(v,list):return [relocate(x) for x in v]
 if isinstance(v,dict):return {k:relocate(x) for k,x in v.items()}
 return v
current=relocate(req);current['inputKit']={'manifestSha256':H(KIT),'parentSubjectSha256':H(MF)}
current['templateStanding']='Original complete requirements for a NEW independent origin, bound to the current frozen normative-only kit. Source review remains separate. No author oracle, prior finding or expected output is supplied.'
assert current['requirements']==relocate(req['requirements']) and len(current['requirements'])==123
assert current['standing']==relocate(req['standing']) and len(current['standing'])==8
assert current['futureQualification']==relocate(req['futureQualification']) and len(current['futureQualification'])==3
(O/'requirements.json').write_text(json.dumps(current,indent=2)+'\n')
charter=original_charter.read_text().replace('consumer-b.v14','consumer-b.v24').replace('/tmp/opensip-design-corrections/consumer-b.v13/output','/tmp/opensip-design-corrections/consumer-b.v24/output')
for before,after in [('c9a6c26a82dbe24acfbba423360be54e45f11325576b172d75a005ec35d0ffb2',H(MF)),('f8aec9c5469573568fe6f57f14429b739cf7f9707c08a26b72d0c48e71c43f3c',H(KIT))]:
 assert charter.count(before)==1;charter=charter.replace(before,after)
(O/'charter.md').write_text(charter)
prompt=f'''You are actual Claude in a NEW fresh independent blind consumer origin for OpenSIP. No prior session is resumed. Your entire work starts here; no predecessor implementation, outputs, reviews, or expected answers are provided.

Read charter.md and requirements.json in this runtime in full, then verify subject/consumer-input-manifest.json and every member. These specify the SAME original complete123 requirements,8standing rules and3future-qualification limits. Current source37 manifest SHA {H(MF)}; normative kit SHA {H(KIT)}. Source review is separate and pending; no architecture/application acceptance is implied. Historical labels in embedded normative descriptions are provenance only. Apply exact current kit owners and profile; report missing input custody rather than silently inventing a rule.

Read ONLY this runtime's subject/charter/requirements and your own output/, plus installed standard library/jsonschema. Never read the live repository, other /tmp/opensip-design-corrections directories, author models/fixtures/reports, other consumer code or prior reviews. Independently choose and compute all required examples. Do not spawn agents. Write only output/. No product implementation, commits/pushes or acceptance on root's behalf.

Reference interpreter /tmp/opensip-architecture-review-env/bin/python -I -B is available directly, as is python3. Use direct Write/Edit for authored code. Complete the full required work, retained exports, independent schema/closure/semantic replay and measured original standalone examples; no reduced schema-only or count-only substitution. A command finishing successfully is not evidence of a law the command did not check. Retain exact inputs, derived outputs and executed checks so each required claim can be independently assessed. Stock JSON Schema does not execute the published registry/join keywords; implement their selected normative laws too. Raw-input canonicalization and complete proof replay are distinct required boundaries. Keep future real OS/compiler/crypto/SQLite/host enforcement explicitly unperformed, not a current design omission.

Keep checkpoints with the full required ID set and actual standing after each phase, preserve failed attempts before corrections, and use unique receipts. Wait for your own background work to finish and inspect results before writing a final response; a progress-only response while required children run does not complete the review. If interrupted, this new origin may resume its own checkpoints without dropping any requirement. Final output/blind-review.md/json must give substantive ACCEPT-RECONSTRUCTABLE, CHANGES_REQUIRED or an actual BLOCKED result as the charter permits. Root separately verifies exact final exports; no root result or oracle is supplied here.
'''
(O/'prompt.md').write_text(prompt)
# Public-filtered launcher body only; NEVER reuse the historical session id or resume flag.
t=(B/'consumer-b.v14/launch.py').read_text();start=t.index('cmd=');end=t.index('\nstart=time.time()',start);sid=str(uuid.uuid4())
cmd=['/Users/sb/.local/bin/claude','--safe-mode','--strict-mcp-config','--model','opus','--session-id',sid,'--permission-mode','dontAsk','--tools','Read,Glob,Grep,Bash,Write,Edit','--allowedTools','Read','Glob','Grep','Write','Edit','Bash(python3 *)','Bash(/tmp/opensip-architecture-review-env/bin/python *)','--add-dir',str(O),'--add-dir','/tmp/opensip-architecture-review-env','--output-format','stream-json','--verbose','-p']
assert '--resume' not in cmd
launch=t[:start]+'cmd='+repr(cmd)+t[end:];ast.parse(launch);(O/'launch.py').write_text(launch)
dispatch={'standing':'PREPARED NEW fresh actual Claude origin, no execution or acceptance. Same full charter; no prior consumer implementation or outcomes supplied.','plannedNewSessionId':sid,'sourceManifestSha256':H(MF),'kitManifestSha256':H(KIT),'promptSha256':H(O/'prompt.md'),'charterSha256':H(O/'charter.md'),'requirementsSha256':H(O/'requirements.json'),'originalCharterSha256':H(original_charter),'originalRequirementsSha256':H(original_req),'substantiveRequirementSemanticsUnchanged':True,'requirements':123,'standingRules':8,'futureQualificationItems':3,'copiedPriorConsumerArtifacts':False,'kitPreparationCommand':command,'kitPreparationStdout':result.stdout,'expectedFreshActualInitRequired':True}
(O/'dispatch.json').write_text(json.dumps(dispatch,indent=2)+'\n');print(json.dumps(dispatch,indent=2))
