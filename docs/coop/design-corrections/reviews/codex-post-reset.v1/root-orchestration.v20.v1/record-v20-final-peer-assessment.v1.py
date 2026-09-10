from pathlib import Path
import json,hashlib,shutil,datetime
R=Path('/Users/sb/code/opensip-ai/opensip_arch');E=R/'docs/coop/design-corrections/reviews';O=E/'codex-post-reset.v1';B=Path('/tmp/opensip-design-corrections');P=B/'v20-final-delta-peer.v1';F=B/'v20-final-source.v2';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();load=lambda p:json.loads(p.read_text());ref=lambda p:{'path':str(p.relative_to(R)),'sha256':sha(p)}
r=load(P/'assessment.json');assert sha(P/'assessment.json')=='52bbc64b9ab734e2c055792baae2abf44a2644c108d712ac065ad4cb55297654';assert len(r['requiredChanges'])==1 and r['requiredChanges'][0]['id']==1
receipt=load(P/'response.json');assert receipt['is_error'] is False and receipt['session_id']=='6d2c5d9d-e2c8-454c-bf51-0a7e0cf7e27b' and receipt['num_turns']==63 and not receipt['permission_denials']
assert sha(P/'work/probe/patched-check-identity.py')==sha(F/'work/docs/coop/design-corrections/foundation/check-identity.py')=='d60afe7a8f1f8e45da1a3ae35247f9f3a77fc4e481f198fcb332515894d80fcd'
assert sha(F/'proposal.json')=='7843e3cc7ba8a21ba12d9ca17c816ce8b680e4fa5b208f055d34f6ce7e66f96e'
old=load(B/'v20-final-source.v1/proposal.json');new=load(F/'proposal.json');by={x['path']:x for x in old['files']}
for x in new['files']:
 assert sha(F/'work'/x['path'])==x['afterSha256']
 if x['path'].endswith('/check-identity.py'):assert x['beforeFinalPeerCorrectionSha256']==by[x['path']]['afterSha256']
 else:assert x==by[x['path']]
# Full source copy check, beyond the12file proposal inventory. The one staging root record is
# preserved as-of and never integrated as a current source file.
parent=load(E/'candidate-subject.v19.json');expected={x['path']:x['sha256'] for x in parent['files']};expected.update({x['path']:x['afterSha256'] for x in new['files']});expected['v20-root-augmentation.json']=sha(B/'v20-combined-source.v1/work/v20-root-augmentation.json')
actual={str(p.relative_to(F/'work')) for p in (F/'work').rglob('*') if p.is_file() and '__pycache__' not in p.parts};assert actual==set(expected)
for rel,digest in expected.items():assert sha(F/'work'/rel)==digest,rel
assert load(F/'root-identity.v1.json')['passed']==1592 and load(F/'root-identity.v1.json')['failed']==0
assert load(F/'root-sentinel.v1.json')['passed']==7
rows=[]
for p in sorted((P/'work/probe').rglob('*')):
 if p.is_file():
  q=E/'v20-final-delta-peer.v1/retained-probe'/p.relative_to(P/'work/probe');q.parent.mkdir(parents=True,exist_ok=True);assert not q.exists();shutil.copyfile(p,q);rows.append(ref(q))
q=E/'v20-final-delta-peer.v1/additional-probe-custody.json';q.write_text(json.dumps({'standing':'Exact standalone probes/variants/outputs retained; full unchanged baseline/finaltree copies omitted and reconstructible from recorded source.','files':rows},indent=2)+'\n')
qual=[
'Root read the complete final JSON/Markdown/receipt, exact supplied patch, probe source and instrumented delta, invalid post-suite output, at-point output and new exact sentinel file. Root original4diffs were authored/read; all12source hashes and complete8654file copy independently checked.',
'Peer v1 subject manifest cec321... has one required correction. Root did not accept the uncorrected predicate: final proposal v2 applies the EXACT Claude-authored/tested patched file d60afe..., with the other11manifest files unchanged. This is transparent composition of substantively reviewed bytes, not a claim peer reviewed a different manifest or a new independent review.',
'Root final1592identity checks pass and7 targeted exact-helper AST tests distinguish successful returns from actual W.Refusal objects with None or named detail, while unexpected errors propagate. The7controls inject helper behavior; they are not actual adopt_baseline invocations or complete Run tests.',
'The shipped positive already succeeded at its execution point. Required precision correction concerns distinguishing detail-less refusal, not a demonstrated false pass of that exact empty-entry fixture. Peer initial post-suite replay was invalid because globals rebound; only its at-point observations support baseline behavior.',
'Initial system Python probe failed missing jsonschema. zsh PIPESTATUS output was blank; pipeline wrapper exit0 did not authenticate the Python result. Correct interpreter and instrumented/patched runs are separately preserved, and root finalcheck exit0/report corroborate the exact final file.',
'Peer membership mutation is an in-memory reevaluation of the guard expression, not a whole-checker mutation run. Its baseline guard-fails claim means that expression against stale parent data, not the baseline1591suite failing (which passed). Whole suite guard neutralization for runtime schema registration is separately evidenced by the earlier combined peer.',
'Native schema digest has ONE replaced literal fixture declaration in this delta, but MANY dynamic schema-identity consumers and possible transitive identity changes. Peer carryForwardComposition phrase consumed in exactly one place must not be read as a global identity-stability claim.',
'Parent manifest was unresolved in the peer narrow lookup. Root explicitly verified its exact312db9...manifest and all8653frozenfiles; originalv1e7403...1192files also verified. No missing design dependency is inferred from that bounded lookup.',
'Whole-tree source comparison here verifies all8654copy files, not just12deltas. Root-level v20-root-augmentation.json remains an as-of staging record and is not integrated among the12source paths; retained historical copies remain historical. No semantic correction is required for that advisory.',
'Optional cosmetic wrapping remains unchanged, with no violated width law. Positive informational observation requires no further action; all original observations remain in retained peer evidence.',
'Root terminated ONLY the peer-owned broad grep process group after it stalled for over3minutes; actual Claude session remained alive and completed successfully. Exact stall cause is not established; root-search-recovery.v1.json preserves action. No source or Claude process was terminated.',
'The peer permits freeze before its minor correction, but root resolved it first under the authorized completion task. One-suite/four-variant reference results are not six canonical commands, source-pin acceptance, semantic proof replay or product qualification.',
'Finalsource coauthor alignment is not fresh independent20/NEWblind9/fullapplication. Those remain mandatory; implementation/readiness/qualification not granted.'
]
d={'standing':'Root substantive assessment of final bounded actualClaude peer plus exact application of its authored sentinel correction. Independent acceptance pending.','sessionId':receipt['session_id'],'fullRead':True,'boundedFinalDeltaAssent':True,'requiredChanges':[],'originalPeerRequiredChanges':r['requiredChanges'],'resolution':{'id':1,'action':'Applied exact actual-Claude authored sentinel patch, fully read and byte-verified; root1592identitychecks/7targetedhelperchecks pass.','reviewedSubjectManifestSha256':r['exactManifest']['proposalSha256'],'patch':ref(E/'v20-final-delta-peer.v1/required-change-1.patch'),'patchedFileSha256':sha(P/'work/probe/patched-check-identity.py')},'subjectManifestSha256':sha(F/'proposal.json'),'subject':ref(E/'v20-final-source.v2/proposal.json'),'actualAssessment':ref(E/'v20-final-delta-peer.v1/assessment.json'),'receipt':ref(E/'v20-final-delta-peer.v1/response.json'),'independentAcceptance':False,'completeFileCopyVerified':len(actual),'qualifications':qual,'observationsDisposition':['Historical staging record not integrated as current source; preserve as-of metadata.','Optional wrapping left unchanged.','Positive informational observation retained; no further action required.'],'implementationAuthorized':False,'readinessChanged':False}
p=O/'coauthor-assessment.v20-final-delta-peer.v1.json';assert not p.exists();p.write_text(json.dumps(d,indent=2)+'\n');print('Root finalpeer assessment retained; resolved original required correction with exact authored bytes')
