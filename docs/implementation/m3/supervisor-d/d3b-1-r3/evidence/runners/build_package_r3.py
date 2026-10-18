from pathlib import Path
import hashlib,json,os,shutil,subprocess
F=Path(__file__).parent;B=Path('/tmp/opensip-implementation');W=Path('/Users/sb/code/opensip-ai/opensip-d3b1-takeover');P=W.parent/'opensip';A=W.parent/'opensip_arch';S=F.parent/'d3b-1-r3/architecture';PRE='docs/implementation/m3/supervisor-d/d3b-1-r3';U=S/PRE;assert not S.exists();U.mkdir(parents=True)
E=dict(os.environ,GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null')
for key in ['GIT_DIR','GIT_WORK_TREE','GIT_CONFIG_COUNT']:E.pop(key,None)
def git(w,*args):return subprocess.check_output(['/usr/bin/git',*args],cwd=w,env=E)
def pinbytes(path,raw):return dict(path=path,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
def pin(root,path):return pinbytes(path,(root/path).read_bytes())
def write(path,data):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(data,indent=2)+'\n')
base=git(P,'rev-parse','HEAD').decode().strip();arch=git(A,'rev-parse','HEAD').decode().strip();assert base=='d154eb002fc536855b9c831d0d6484bfaf5335d3';assert arch=='853d3f08edc90f22abfb11c635eec8b4168094fc';assert git(W,'rev-parse','HEAD').decode().strip()==base
full=json.loads((B/'d3b1-full-takeover-r1/checks.json').read_text());final=json.loads((B/'d3b1-final-candidate-r4/checks.json').read_text());refusal=json.loads((B/'d3b1-refusal-supplement-r1/checks.json').read_text());mutations=json.loads((B/'d3b1-mutations-takeover-r1/controls.json').read_text());inherited=json.loads((B/'d3b1-enforcement-baseline-r1/checks.json').read_text())
proof=json.loads((B/'d3b1-final-proofs-r2/checks.json').read_text());assert proof['allPassed'] and not proof['dependencyManifestsChanged']
assert final['allPassed'] and refusal['allPassed'] and len(refusal['rows'])==2 and mutations['allCaught'] and len(mutations['rows'])==8 and inherited['equalFailureSets']
assert full['suites']['base-opensip_components']['passed']==173 and not full['suites']['base-opensip_components']['failed'];assert final['rows'][0]['passed']==193 and not final['rows'][0]['failed']
assert full['suites']['base-opensip_platform']['failed']==full['suites']['candidate-opensip_platform']['failed']==[]
assert full['suites']['base-opensip_platform']['passed']==full['suites']['candidate-opensip_platform']['passed']==292
assert full['suites']['base-opensip_operability']['passed']==95 and not full['suites']['base-opensip_operability']['failed']
assert 'test result: ok. 95 passed; 0 failed;' in (B/'d3b1-final-candidate-r4/operability-suite.log').read_text()
assert (B/'d3b1-catalog-standalone-r1.log').read_text().rstrip().endswith('OK')
paths=git(W,'diff','--name-only').decode().splitlines();assert len(paths)==15 and git(W,'ls-files','--others','--exclude-standard')==b''
finalpins=json.loads((B/'d3b1-final-candidate-r4/product-pins.json').read_text());assert finalpins==[pin(W,p) for p in paths]
rows=[]
for path in paths:
 raw=(W/path).read_bytes();target=U/'product'/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw);parent=pinbytes(path,git(P,'show',base+':'+path));rows.append(dict(path=path,parent=parent,candidate=pin(W,path),archived=pin(S,PRE+'/product/'+path)))
write(U/'product-map.json',dict(rows=rows))
shutil.copyfile(F/'SCOPE-draft.md',U/'SCOPE.md')
# Pin runners, all owning lane evidence and earlier failed attempts; never binaries/private fixture material.
for name in ['full_lane.py','refusal_supplement.py','enforcement_baseline.py','final_candidate.py','finish_candidate.py','finish_candidate_r3.py','finish_candidate_r4.py','mutations.py','check_no_cgroup.py','repair_preflight.py','provider_bound_control.txt','root_only_control.txt','final_proofs.py','final_proofs_r2.py','build_package_r3.py']:
 target=U/'evidence/runners'/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(F/name,target)
for name in ['d3b1-full-takeover-r1','d3b1-final-candidate-r1','d3b1-final-candidate-r2','d3b1-final-candidate-r4','d3b1-refusal-supplement-r1','d3b1-enforcement-baseline-r1','d3b1-mutations-takeover-r1','d3b1-final-proofs-r2']:
 for p in sorted((B/name).iterdir()):
  if p.is_file() and p.suffix in ['.log','.json','.jsonl','.patch']:
   target=U/'evidence'/name/p.name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,target)
shutil.copyfile(B/'d3b1-catalog-standalone-r1.log',U/'evidence/catalog-standalone.log')
shutil.copytree(F.parent/'d3b1-preflight-r1',U/'evidence/preflight-r1/source')
for name in ['REQUEST.md','REVIEW.md','review.json']:
 target=U/'evidence/preflight-r1/review'/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(B/'reviews/codex-d3b1-takeover-preflight-r1'/name,target)
authorities=['docs/implementation/m3/supervisor-d/PROPOSAL-r5.md','docs/implementation/m3/supervisor-d/d3b/PLAN-r3.md','docs/implementation/m3/reviews/codex-d3b-plan-r3/review.json','docs/implementation/m3/reviews/codex-d3b-plan-r3/lead-assent.json','docs/implementation/m3/supervisor-d/d3b-0-r3-subject.json','docs/implementation/m3/supervisor-d/d3b-0-r3-unit.json','docs/implementation/m3/reviews/codex-d3b-0-r3/review.json','docs/implementation/m3/supervisor-d/d3a-4-r2-subject.json']
write(U/'source.json',dict(productBase=base,architectureBase=arch,productLock=pin(P,'design-lock.json'),inventoryBase=232,contractSuccessors=177,authorities=[pin(A,path) for path in authorities],newPaths=[],publicApiAdded=True,productionCallerAdded=False,productQualification=False,originalDraftPreserved=True))
summary=dict(productBase=base,architectureBase=arch,finalProductPins=finalpins,components=dict(basePassed=173,candidatePassed=193,baseFailed=[],candidateFailed=[],newPassing=20),platform=dict(basePassed=292,candidatePassed=292,baseFailed=[],candidateFailed=[],ignored=1),operability=dict(basePassed=95,candidatePassed=95,baseFailed=[],candidateFailed=[]),compileRefusals=dict(basePassed=3,candidatePassed=3,baseFailed=[],candidateFailed=[]),otherIntegrationTargets={key:val for key,val in full['suites'].items() if not key.endswith(('opensip_components','opensip_platform','opensip_operability','refusal_tests'))},mutations=mutations['rows'],preexistingEnforcementFailure=inherited,overriddenAttempts=['Full r1 compile-refusal setup failures superseded by pinned-CARGO supplement.','Full r1 catalog invocation stopped for nested lock; standalone five controls passed.','Original components two failures resolved by preserving real failed killpg evidence; final full 193 tests pass.','Original registry reference drift resolved by exact generated references; final full 95 operability tests pass.','Early final-candidate r2 compiler failure was test event tuple plumbing. Unit round2 still missed its claimed alive-root assertion/cleanup block; round3 adds it explicitly and final-candidate r4 reruns the owning component suite.'],allRequiredComparisonsAndControlsPassed=True,wholeRepositorySuitePassed=False,qualification=False)
write(U/'checks-summary.json',summary)
write(U/'carried-obligations.json',dict(unit='D3B-1-r3',obligations=[dict(id='D3B-2',owner='lead',scope='Remaining cancellation/revocation/clock code and plan r3 NBO-1; keep production ladder gate closed until accepted.'),dict(id='D5-CODEC-RERUN',owner='lead/D5',scope='Rerun descendant scenarios with real TS2/Rust3 codecs and G21 rows; not qualification.'),dict(id='D3B-L',owner='lead/Linux lane',scope='Subreaper, proc sweep and Linux controls remain not run.'),dict(id='OPERABILITY-OWNER-LABEL-EXPECTATION',owner='lead/operability',scope='Baseline and candidate share one enforcement generated-owner-label expectation failure; no new exception or owner change is selected here.')] ))
# Preserve the exact failed unit round and its independent review as history.
prior=F.parent/'d3b-1-r2/architecture';shutil.copytree(prior,S,dirs_exist_ok=True)
priorreview='docs/implementation/m3/reviews/codex-d3b-1-r2'
for name in ['REQUEST.md','subject.json','REVIEW.md','review.json']:
 target=S/priorreview/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(B/'reviews/codex-d3b-1-r2'/name,target)
priorrecord=dict(subjectManifest=pin(S,'docs/implementation/m3/supervisor-d/d3b-1-r2-subject.json'),review=pin(S,priorreview+'/review.json'),verdict='REQUIRED-FINDINGS',requiredFindings=['D3B1-R2-RF-1'])
source=json.loads((U/'source.json').read_text());source['priorRounds']=[priorrecord];write(U/'source.json',source)
oldrows=json.loads((prior/'docs/implementation/m3/supervisor-d/d3b-1-r2/product-map.json').read_text())['rows'];delta=[r['path'] for r,o in zip(rows,oldrows) if r['candidate']!=o['candidate']];assert delta==['crates/components/src/supervisor_tests.rs'];write(U/'round3-delta.json',dict(changedSinceUnitRound2=delta,productionCodeChanged=False,reusedEvidence='Eight mutations and platform/operability integration baselines remain unchanged; final components193 and Clippy/source/proof evidence rerun after the explicit test correction.'))
# The eight production mutations are reused only across an unchanged
# production source and unchanged failure-observing test bodies. The one
# changed combined test still has the identical first snapshot-failure case.
import importlib.util
spec=importlib.util.spec_from_file_location('owner_blank_for_delta',W/'tools/tests/test_environment_exceptions.py');owner=importlib.util.module_from_spec(spec);spec.loader.exec_module(owner)
oldtext=(prior/'docs/implementation/m3/supervisor-d/d3b-1-r2/product/crates/components/src/supervisor_tests.rs').read_text();newtext=(W/'crates/components/src/supervisor_tests.rs').read_text()
def testbody(text,name):
 code=owner.blank(text);at=code.index('fn '+name+'(');begin=code.index('{',at);depth=1;end=begin+1
 while depth:
  if code[end]=='{':depth+=1
  elif code[end]=='}':depth-=1
  end+=1
 return text[at:end]
selected=['failed_tree_identity_reads_keep_their_step_and_errno','unsent_by_pid_outcomes_are_not_reported_as_kills','an_exceeded_confirm_stays_incomplete_after_a_singleton','an_in_group_descendant_dies_with_the_group','a_snapshot_member_that_changes_group_is_targeted','each_group_kill_failure_keeps_its_original_error','the_provider_snapshot_bound_counts_its_root','the_snapshot_walk_bound_includes_its_root'];equivalent=[]
for name in selected:
 a=testbody(oldtext,name);b=testbody(newtext,name);assert a==b,name;equivalent.append(dict(test=name,unchanged=True,sha256=hashlib.sha256(a.encode()).hexdigest()))
name='a_failed_listing_or_group_kill_leaves_the_tree_incomplete';a=testbody(oldtext,name).split('// All group SIGKILL')[0];b=testbody(newtext,name).split('// All group SIGKILL')[0];assert a==b;equivalent.append(dict(test=name,unchangedFirstSnapshotFailureCase=True,sha256=hashlib.sha256(a.encode()).hexdigest()))
write(U/'mutation-reuse-proof.json',dict(productionSourceUnchanged=True,originalMutationControls=pin(S,'docs/implementation/m3/supervisor-d/d3b-1-r2/evidence/d3b1-mutations-takeover-r1/controls.json'),unchangedFailureObservers=equivalent,onlyChangedRegion='Alive-root assertions and root cleanup in the combined failure control, after the unchanged snapshot-failure case.'))
manifest=PRE+'-subject.json';write(S/manifest,dict(schemaVersion=1,unit='D3B-1-r3',files=[pin(S,p.relative_to(S).as_posix()) for p in sorted(S.rglob('*')) if p.is_file()]))
q=B/'reviews/codex-d3b-1-r3';q.mkdir(exist_ok=False);subject=pin(S,manifest);write(q/'subject.json',dict(stage=str(S),productBase=base,architectureBase=arch,subjectManifest=subject))
(q/'REQUEST.md').write_text(f'''# Independent D3b-1 unit review, corrected takeover round 3

Read frozen stage {S}. Manifest {manifest}, SHA-256 {subject['sha256']}. Rehash every member. Product base {base}; architecture base {arch}. Write ONLY REVIEW.md and review.json in {q}. Read-only source/hash/JSON/Git; no stage/repository/control edits, tests/builds/cargo/lanes, network, panes/delegation, private fixtures/installations/keys/heldout/T2 stores/cache.

Review the exact fifteen parent/candidate product paths, accepted plan and source authority pins, full source/control matrix and self-review/disclosures. Check source and evidence independently. Unit round2 returned D3B1-R2-RF-1 because its asserted alive-root correction was absent. Round3 changes only supervisor_tests.rs: explicitly observes the root alive, kills it out of band and verifies it gone, asserts Unreaped/no ExitObserved/MembersListed, and retains no-root/no-later-call proof. Fresh affected controls and final full193 component tests plus Clippy/proofs must substantiate it. Every byte of round2 and its review is preserved in this manifest. Preflight RF-1/2/3 are archived and corrected: root-only identity/count includes root but no target; actual Provider class 4/5 versus Tool 64/65 controls; native-call recorder and alive-root Unreaped/no ExitObserved versus held-zombie ExitObserved/RootAlone, no by-pid root or later call after settlement/Drop, surviving root cleanup. The real native held-zombie killpg may fail EPERM; older tests now retain that failure as incomplete while checking confirm/reap order separately. Other tests cover escaped descendants, a real fork after snapshot, actual same-pid group change, missed daemon, bounded fork loop, late dedup, typed failure outcomes, original native call/errno evidence and Exceeded latching. The conservative no-cgroup scanner covers all candidate source including tests without guessed exemptions.

Full final components 173 to 193 (20 new) with no failures; platform292 no failures and one inherited ignored; operability95 no failures after exact generated references; compile refusal3 pass each after corrected CARGO environment. One enforcement owner-label expectation fails identically at baseline and candidate; disclose it, do not infer a whole-check pass. Catalog standalone5 pass; earlier nested-lock invocation was stopped and preserved. Eight mutations must fail runtime tests, not compilation. Evidence summary selects final results and preserves invalid/failed attempts; verify every claimed supersession. No new product paths, package edge or mint site; design verification/census closure/format/Clippy checks and final byte pins must be coherent. D3b-2/gate removal, Linux, D5 codec rerun, CF/production wiring and qualification remain outside this unit. Inspect carried obligations; do not accept project completion.

Return JSON {{"verdict":"ACCEPT-UNIT"|"REQUIRED-FINDINGS","subjectManifestSha256":"{subject['sha256']}","requiredFindings":[],"nonBlockingObservations":[]}} with D3B1-R3-RF-n / D3B1-R3-NBO-n ids. Raise any unjustified plan deviation or weak/missing evidence.
''')
print(json.dumps(dict(stage=str(S),reviewDirectory=str(q),subjectManifest=subject,files=len(json.loads((S/manifest).read_text())['files'])),indent=2))
