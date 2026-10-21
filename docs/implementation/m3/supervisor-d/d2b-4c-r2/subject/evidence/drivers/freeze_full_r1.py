from pathlib import Path
import json,hashlib,subprocess,shutil,os
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;P=Path('/Users/sb/code/opensip-ai/opensip');A=P.parent/'opensip_arch';W=P.parent/'opensip-rust3-successor-takeover'
Q=Path('/tmp/opensip-implementation/reviews/codex-d2b4c-r1');S=Q/'subject';OLD=Path('/tmp/opensip-implementation/reviews/codex-d2b4b-r1/subject')
assert not Q.exists()
def git(root,*args):return subprocess.check_output(['git','-C',str(root),*args],text=True).strip()
def pin(root,path):
 raw=(root/path).read_bytes();return dict(path=path,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
def put(path,value):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def copy(root,path,target):
 assert not Path(path).is_absolute()and '..'not in Path(path).parts
 dest=S/target/path;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(root/path,dest)
ph=git(P,'rev-parse','HEAD');ah=git(A,'rev-parse','HEAD')
assert ph=='0f5bbe492a40ff03c18262536f58c86e5af64be0'and ah=='fee2bce708521b653f37a324d03330c7edddde2a'
assert not git(P,'status','--porcelain')and not git(A,'status','--porcelain','--untracked-files=no')
repo=json.loads((F/'repository-r2/report.json').read_text());assert repo['allPassed'];pins=repo['sourcePins'];assert len(pins)>24
for row in pins:assert pin(W,row['path'])==row
paths=[r['path']for r in pins];new=sorted(git(W,'ls-files','-o','--exclude-standard').splitlines());existing=sorted(set(paths)-set(new));assert len(new)==12 and len(existing)+len(new)==len(paths)
Q.mkdir();S.mkdir()
for row in pins:copy(W,row['path'],'product')
for path in existing:
 dest=S/'parent'/path;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(subprocess.check_output(['git','show',f'{ph}:{path}'],cwd=P))
put(S/'product-map.json',dict(productParent=ph,paths=pins,newPaths=new,existingPaths=existing,productionCallerAdded=False,newDependencies=False,productQualification=False))
# Complete current public codec/schema/identity context, overlaid by product/.
context={'Cargo.toml','Cargo.lock','design-lock.json','crates/components/Cargo.toml','crates/components/src/lib.rs','crates/components/src/supervisor.rs','crates/contracts/Cargo.toml','crates/contracts/src/lib.rs','crates/contracts/src/generated/protocol.rs','crates/identity/Cargo.toml','tools/check_operability.py','tools/check_package_edges.py','tools/verify_design.py','crates/host/src/native_file_manifest.rs','crates/host/src/dependency_transport_digest.rs'}
for directory in ['crates/components/src/provider_protocol','crates/identity/src','schemas','crates/components/data']:
 for p in (W/directory).rglob('*'):
  if p.is_file():context.add(str(p.relative_to(W)))
context.update(git(W,'ls-files','crates/components/tests/data').splitlines())
for path in sorted(context-set(paths)):copy(W,path,'context')
# Public current authorities used by the accepted predecessor, plus current
# split acceptance, inventory parent, and all current meaning records.
authority={str(p.relative_to(OLD/'authority/architecture'))for p in (OLD/'authority/architecture').rglob('*')if p.is_file()}
authority|={'docs/implementation/m3/supervisor-d/PROPOSAL-r5.md','docs/implementation/m3/supervisor-d/d2b/PLAN-r3.md','docs/implementation/m3/supervisor-d/d2b/PLAN-r3-A1.md','docs/implementation/m3/supervisor-d/d2b/PLAN-r3-A2.md','docs/implementation/m3/supervisor-d/d2b-3a-r1-unit.json','docs/implementation/m3/supervisor-d/d2b-4a-r2-unit.json','docs/implementation/m3/reviews/codex-d2b-3a-r1/review.json','docs/implementation/m3/reviews/codex-d2b4a-r2/review.json','docs/implementation/m2/repository-file-inventory.v237.json'}
lock=json.loads((P/'design-lock.json').read_text())
for binding in lock['contractSuccessors']:
 authority.add(binding['record']['path'])
 if 'rust3-identity-materialization-r1' in binding['record']['path']:
  for key in ['subjectManifest','review','assent']:authority.add(binding[key]['path'])
authority.update(['docs/implementation/m3/supervisor-d/d2b-4b-r1-unit.json','docs/implementation/m3/reviews/codex-d2b4b-r1/review.json','docs/coop/design-corrections/native/native-cases.v2.json','docs/implementation/m3/native-successors-fa/fa-2/evidence/vectors.json','docs/implementation/m3/native-successors-fa/rust3-lim/evidence/vectors.json'])
for binding in lock['inventorySuccessors'][-1:]:
 for key in ['record','review','assent']:authority.add(binding[key]['path'])
for path in sorted(authority):copy(A,path,'authority/architecture')
put(S/'authority/live-pins.json',dict(productParent=ph,architectureParent=ah,files=[pin(A,path)for path in sorted(authority)],qualification=False))
# Retain complete relevant run artifacts and failed-source histories. Targets,
# binaries, temporary/private fixtures and stores are deliberately not members.
import re
for p in sorted(F.iterdir()):
 if p.is_dir() and re.fullmatch(r'(base|reference|census|replay|send-replay|accounting|successor-owning|participant-successor|successor-mutations|candidate-suites|source-census|repository)-r[0-9]+',p.name):shutil.copytree(p,S/'evidence'/p.name)
 elif p.is_dir() and p.name.startswith('preserved-'):shutil.copytree(p,S/'history'/p.name)
 elif p.is_file() and (p.suffix=='.py' or p.name.endswith('-lane.log')):copy(F,p.name,'evidence/drivers')
for name in ['replay-progress-r3.json','native-full-scope-audit-r2.json','requirements-final-preflight-r1.json','PREPARED.json']:
 copy(F,name,'evidence')
preview=F/'inventory238-preview';projection=json.loads((preview/'meaning-projection-preview.json').read_text());assert projection['totalMeanings']==150 and projection['foldedCurrentSupersessions']==['crates/components/src/provider_protocol.rs']
IP='docs/implementation/m2/repository-file-inventory.v238.json';INV='docs/implementation/m3/supervisor-d/d2b4c-inventory-v238-r1'
copy(preview,'repository-file-inventory.v238.json','inventory/preview')
candidate=pin(preview,'repository-file-inventory.v238.json');candidate['path']=IP
parent=projection['parent'];inherited=[dict(parent=candidate,selector=e['selector'],before=e['before'],after=e['after'])for e in projection['projections']]
projection.update(candidate=candidate,proposedInventoryPassageInheritance=inherited,codeUnitAccepted=False,inventoryBound=False)
put(S/'inventory/meaning-projection.json',projection)
record=dict(schemaVersion=1,unit='D2B4C-inventory-v238-r1',standing='PROPOSED with full4c code, independently assessed together; no integration/acceptance inferred',parent=parent,candidate=candidate,parentArtifactBytesUnchanged=True,inheritedRowsEqualByValue=True,packagesUnchanged=True,pendingDecisionsUnchanged=True,addedFiles=new,changedFiles=existing,realizedPlannedFiles=[],productParent=ph,codeProductMap=pin(S,'product-map.json'),integrationCensus=pin(S,'evidence/repository-r2/report.json'),productQualification=False)
put(S/'inventory/successor.json',record);successor=pin(S,'inventory/successor.json');successor['path']=INV+'/successor.json'
put(S/'inventory/publication-map.json',dict(candidate=candidate,successorRecord=successor,meaningProjection=INV+'/meaning-projection.json',candidateFrozenMember='inventory/preview/repository-file-inventory.v238.json',successorFrozenMember='inventory/successor.json',bindingRequiresIndependentAssessmentAndRootAssent=True))
mut=json.loads((F/'successor-mutations-r2/report.json').read_text());extra=json.loads((F/'successor-mutations-r3/report.json').read_text());assert mut['allKilled']and extra['allKilled']and mut['sourceRestored']and extra['sourceRestored']
full=json.loads((F/'candidate-suites-r3/report.json').read_text());assert full['allPassed']and full['clippyExitCode']==0
scope=dict(unit='D2B-4c-r1',standing='COMPLETE RUST3 SUCCESSOR ADMISSION/REPLAY CODE + STRICT INVENTORY238; UNACCEPTED',sourcePaths=len(paths),newPaths=len(new),existingPaths=len(existing),componentsTests=411,identityTests=86,rust3Tests=136,baseComponents=362,baseIdentity=86,baseCandidateFailureSetsEqual=True,compiledRuntimeMutants=8,allMutatedSourceTargetsRestored=True,componentAllTargetClippyPassed=True,operabilityRows=115,mintRowsBefore=462,mintRowsAfter=463,inventory=dict(parent=parent,candidate=candidate,record=successor,parentRows=1410,candidateRows=1422,inheritedMeanings=145,directCurrentMeanings=5,projectedMeanings=150,explicitDispatchSupersession185Folded=True),historicalTrial07=dict(originalCases=353,integerRust3ScopedPredicates=194,separateRawFloatRefusal=1,ts2Separate=48,c4hExternal=110,wholeReferenceConformanceClaimed=False),nativeCases=dict(entirePinnedSourceCasesAudited=477,inheritedTableCases=6,currentLiteralProfileRefusalSteps=34,sharedSchemaBoolRefusalSteps=2,rustLimitAndEmptyDependencyPredicateSteps=3,originalWholeExecutorOutcomeReproductionClaimed=False),runtimeScope='Exact current source pins tested; subsequent source census verification made no further source/census mutation. Full workspace, feature/platform, provider execution, production/source39 and project qualification are not established by component suites.',binaryCustody='Mutants freshly compiled individually and killed by named runtime witnesses, then exact target sources restored and current full suites recompiled. Recorded executable hashes identify observed runs; old mutable target-path binaries are not frozen executable members.',carried=['C4 owns Plan/native/set/snapshot/freshness/selection/representability authority. H owns returned symbol-census settlement, scope commitments and fact admission.','No production factory/caller/source39, qualification or other project completion inferred.','Historical compiler64character inputs are never truncated/relabelled to satisfy current RCA-1 literal40. Shape refusals are NOT historical later-diagnostic or whole-executor conformance witnesses.','Raw inventory238 preserves every old description; separate accepted description successor186 and status/push remain owed after exact code/inventory acceptance.'],productQualification=False,entireProjectComplete=False)
put(S/'SCOPE.json',scope)
members=[pin(S,str(p.relative_to(S)))for p in sorted(S.rglob('*'))if p.is_file()]
manifest=dict(schemaVersion=1,unit='D2B-4c-r1',productParent=ph,architectureParent=ah,candidatePaths=paths,members=members);put(Q/'subject.json',manifest);subject=pin(Q,'subject.json')
expected=dict(verdict='ACCEPT-UNIT',subjectManifestSha256=subject['sha256'],requiredFindings=[],nonBlockingObservations=[],inventoryCandidateAssessment=dict(verdict='ACCEPT',requiredFindings=[],**candidate,parent=parent,successorRecord=successor),productQualification=False)
(Q/'REQUEST.md').write_text(f'''# D2b-4c r1: full Rust3 successor admission/replays and own inventory238

Read subject.json SHA256 {subject['sha256']} and all {len(members)} frozen members under subject/. Rehash them and all {len(paths)} actual candidate files at {W}; compare {len(existing)} parent versions and12new paths to product {ph}, architecture {ah}. Assess COMPLETE4c, not helper preflight. Return ACCEPT-UNIT or REQUIRED-FINDINGS, with separate substantive inventoryCandidateAssessment. Nothing is accepted/integrated by this request.

Authorities: accepted M3-D r5, D2b PLAN-r3/A1/A2 and predecessor4a/4b exact acceptances; selected schemas, carriers,52source registry, raw RPP, P3T and overlay; accepted FA2/RUST3-LIM. PLAN LD13 explicitly makes RCA-1 current product handshake the base; LD14 remains historical scope. Inspect requirements-final-preflight and SCOPE. Check all55 duty IDs;36source-location entries are a navigation index, not semantic proof. Identify any missing required behavior or unjustified authority/profile choice rather than accepting a narrowed unit.

Inspect all8token combinations and both omission/addition mismatch directions for every optional token before OpenUniverse/source; no token stripping or inherited payload substitution. FA2 derives only required D-empty expected values against supplied C4cells, not native authority. Request/independentSender choose exact Analyze variant and nullable census. Reference context independently reconstructs full nonempty.rs subject/scope/domain recipes from the sealed manifest;1/256/257/513 controls, no-token257 and oversized-inline256 refusals remain. No new caps, generated carrier/schema owner, Plan selection, producer/native authority or production caller is introduced.

Selected CompleteV3 uses existing generated census carrier and same selected schema evaluator with source-checked metadata/item decomposition. Judge closed members, exact item refs and array keyword proof, nativeSubjectId strict order/uniqueness, canonical examined-path order/uniqueness, row-path membership, all counts/nullability and exact original-node4MiB bound. A legal row can be much larger when JSON-escaped, so no unrelated JSON cap is introduced. Exact4MiB/+1 and100000/+1path/row predicates are separate; row shape cardinality is not full received-byte admission. Complete and typed over-bound move original census and Coverage buffers once only after valid terminal/ZeroExit/EOF. No manufactured protocol fault or H settlement. Only returned symbol scopes/counts defer to H; nonsymbol count/scope tampering is refused. Clean BudgetExhausted/postUnavailable keep requested D-empty count0. Participant all8combinations, null4pairs, one-shot pointer/raw handoff, partialAnalyze-beforeCancel and input-rejected typed-fault normalization controls are included. Existing4a/4b RF1/RF2, T4/T5 and provenance duties still apply; source-derived depth recomputation covers both successors and all8combinations.

Historical replay scope is explicit, not hidden skips. Original353trial07bytes stay pinned, including exact raw analysisOrdinal0.0 and genuine CBORfloat0 refusal. All31rules/cases are partitioned:194integer Rust3scoped predicates,1rawfloat refusal,48TS2 and110C4/H cases not credited. Full20Rust3 accounting quantities use actual production Recorder/sizers and cardinality predicate, exact64MiB/+1frame and9GiB/+1request without dummyGiBbuffers.39small sends use actual independent sender over explicitly supplied synthetic current projections;1original24byte override exercises actual greedy constructor (it is not a legal current Hello),2symbolicGiB cases use actual charging/greedy predicates. Originalabc fragments establish custody bytes; canonical host greedy schedule remains independently enforced. Source/Dempty/commitment/vector adapters and illustrative Plan values establish no C4/current whole-request admission. Critically assess these boundaries against LD14; do not credit a current-context projection as byte-for-byte original whole-frame conformance.

Native-case audit covers ALL477cases of the exact source pinned by historical trial07 common.py, avoiding an invented count-matching101subset. Six original table cases are present by exact ID in current table replay and passed in full suite. Exact Rust limit map and empty dependency shapes are replayed;2shared schema bool values refuse without integer coercion.34original literal Rust wire/startup views are rejected by current schemas: old64compiler commits conflict with accepted RCA-1 literal40, and private fact-vector JSON/aliases are not current wire carriers. Inputs are NOT padded, truncated, hashed or relabelled. These current-profile refusals are explicitly NOT historical whole-executor passes or witnesses for later historical diagnostics/host conversion. Judge whether LD13/LD14 and current accepted authority justify each disposition, or identify missing actual owning-wire replay/controls. Other-owner/TS2 outcomes are not Rust3passes or fullproject completion.

Evidence: accepted base362components/86identity vs exact current411/86 have equal empty failure sets;136focused Rust3checks and warning-denied component alltargetClippy pass.8freshcompiled runtime mutants were killed by named failing tests: reference reconstruction, token mismatch, exact census bytes, nullability, H returned-symbol boundary, clean-terminal zero count, pendingAnalyze/Cancel, and inappropriate deferral of nonsymbol scopes/counts. Compile failure never counts as kill. Exact mutated source targets restored; subsequent current full411/86/Clippy pass. Past executables reused one dedicated target and are not frozen binaries; recorded runtime binary SHA/log/compiler artifacts are evidence. Earlier failed fixture/compile/style attempts are preserved as failures, not pass evidence. No private/blind/provider/feature/platform/fullworkspace qualification is claimed.

Repository/source gates pass at current cutoff: package edges,115owner rows and463lexical constructor rows, environment tests, design/generation/source/admission pins, diff, public19file census closure and both current receipt bindings. No blind/tree/private invocation. All115accepted annotations and462parent lexical rows/member lists/owner definitions/census standing are preserved; only an ordinary census-code into-call row was added, not mint authority. Verify current code/public sources and pinned logs; no rerunning lanes is authorized.

Inventory: candidate {candidate}, successor {successor}; publication-map and meaning-projection include strict12newpaths =>1422rows, every1410parentrow unchanged by value, all other fields/20packages/9pending/91plannedabsences unchanged. Reconstruct ALL145inherited current237meanings +5DIRECT current237overrides =>150 distinct paths, then fold the explicit current237 dispatch supersession from contract185 over inherited184 meaning, keeping original raw before and replacing after with185after. Reindex by physical path. No old description is silently changed by raw additive inventory; separate description186 stillowed. Independently assess this complete exact projection with unchanged verifier profile. Acceptance, root assent, binding, integration, descriptions/status/push and project qualification remain distinct.

Read-only source/JSON/hashes/Git. NO builds/tests/Cargo/generation/lanes/network/panes/delegation. No private corpus413/T2/store/cache/overlay/keys/real installation/held trees, census modes or real-home changes. Do not edit either repository, worktree, subject, controls or evidence. Write ONLY REVIEW.md and review.json in {Q}. IDs D2B4C-R1-RF-n/NBO-n. Required JSON shape (substitute actual REQUIRED-FINDINGS/findings if warranted):

{json.dumps(expected,indent=2)}
''')
prepared=dict(unit='D2B-4c-r1',reviewDirectory=str(Q),stage=str(S),subject=subject,members=len(members),productParent=ph,architectureParent=ah,sourcePins=pins,candidate=candidate,inventoryRecord=successor,inventoryPrefix=INV,productQualification=False,reviewSubmitted=False);put(F/'full-r1-prepared.json',prepared)
for row in members:assert pin(S,row['path'])==row
for row in pins:assert pin(W,row['path'])==row
assert git(P,'rev-parse','HEAD')==ph and git(A,'rev-parse','HEAD')==ah
print(json.dumps(dict(subject=subject,members=len(members),reviewDirectory=str(Q),candidate=candidate,record=successor),indent=2))
