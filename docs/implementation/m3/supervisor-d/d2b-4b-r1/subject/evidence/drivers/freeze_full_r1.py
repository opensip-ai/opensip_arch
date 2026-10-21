from pathlib import Path
import json,hashlib,subprocess,shutil,os
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;P=Path('/Users/sb/code/opensip-ai/opensip');A=P.parent/'opensip_arch';W=P.parent/'opensip-rust3-send-takeover'
Q=Path('/tmp/opensip-implementation/reviews/codex-d2b4b-r1');S=Q/'subject';OLD=Path('/tmp/opensip-implementation/reviews/codex-d2b4a-r2/subject')
assert not Q.exists()
def git(root,*args):return subprocess.check_output(['git','-C',str(root),*args],text=True).strip()
def pin(root,path):
 raw=(root/path).read_bytes();return dict(path=path,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
def put(path,value):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def copy(root,path,target):
 assert not Path(path).is_absolute()and '..'not in Path(path).parts
 dest=S/target/path;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(root/path,dest)
ph=git(P,'rev-parse','HEAD');ah=git(A,'rev-parse','HEAD')
assert ph=='594a9ddddc7a830605b9ce750d6ddb800f0ba234'and ah=='8a3a9ef7c8ec25ac5cab5308efe11ded1a74a71b'
assert not git(P,'status','--porcelain')and not git(A,'status','--porcelain','--untracked-files=no')
repo=json.loads((F/'repository-r1/report.json').read_text());assert repo['allPassed'];pins=repo['sourcePins'];assert len(pins)==24
for row in pins:assert pin(W,row['path'])==row
paths=[r['path']for r in pins];new=sorted(git(W,'ls-files','-o','--exclude-standard').splitlines());existing=sorted(set(paths)-set(new));assert len(new)==18 and len(existing)==6
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
for path in sorted(context-set(paths)):copy(W,path,'context')
# Public current authorities used by the accepted predecessor, plus current
# split acceptance, inventory parent, and all current meaning records.
authority={str(p.relative_to(OLD/'authority/architecture'))for p in (OLD/'authority/architecture').rglob('*')if p.is_file()}
authority|={'docs/implementation/m3/supervisor-d/PROPOSAL-r5.md','docs/implementation/m3/supervisor-d/d2b/PLAN-r3.md','docs/implementation/m3/supervisor-d/d2b/PLAN-r3-A1.md','docs/implementation/m3/supervisor-d/d2b/PLAN-r3-A2.md','docs/implementation/m3/supervisor-d/d2b-3a-r1-unit.json','docs/implementation/m3/supervisor-d/d2b-4a-r2-unit.json','docs/implementation/m3/reviews/codex-d2b-3a-r1/review.json','docs/implementation/m3/reviews/codex-d2b4a-r2/review.json','docs/implementation/m2/repository-file-inventory.v236.json'}
lock=json.loads((P/'design-lock.json').read_text())
for binding in lock['contractSuccessors']:authority.add(binding['record']['path'])
for binding in lock['inventorySuccessors'][-1:]:
 for key in ['record','review','assent']:authority.add(binding[key]['path'])
for path in sorted(authority):copy(A,path,'authority/architecture')
put(S/'authority/live-pins.json',dict(productParent=ph,architectureParent=ah,files=[pin(A,path)for path in sorted(authority)],qualification=False))
# Retain complete relevant run artifacts and failed-source histories. Targets,
# binaries, temporary/private fixtures and stores are deliberately not members.
evidence=['base-r1','handoff-r1','handoff-r2','schedule-r1','domain-r1','domain-r2','domain-r3','domain-r4','domain-r5','domain-r6','policy-r1','snapshot-r1','snapshot-r2','dependency-r1','dependency-r2','prepared-r1','prepared-r2','request-r1','request-r2','request-r3','sender-r1','sender-r2','participant-r1','participant-r2','participant-r3','public-api-r1','public-api-r2','public-api-r3','mutation-owning-r1','mutation-owning-r2','mutants-r1','candidate-suites-r1','candidate-suites-r2','source-census-r1','source-census-r2','repository-r1']
for name in evidence:
 if (F/name).exists():shutil.copytree(F/name,S/'evidence'/name)
for p in sorted(F.iterdir()):
 if p.is_dir()and p.name.startswith('preserved-'):shutil.copytree(p,S/'history'/p.name)
 elif p.is_file()and(p.suffix=='.py'or p.name.endswith('-driver.log')):copy(F,p.name,'evidence/drivers')
for name in ['SCOPE-CLARIFICATION.json','REQUEST-ASSEMBLY-NOTES.json','REVIEW-PACKAGING-NOTE.json']:copy(F,name,'evidence')
preview=F/'inventory237-preview';projection=json.loads((preview/'meaning-projection-preview.json').read_text());assert projection['totalMeanings']==145
IP='docs/implementation/m2/repository-file-inventory.v237.json';INV='docs/implementation/m3/supervisor-d/d2b4b-inventory-v237-r1'
copy(preview,'repository-file-inventory.v237.json','inventory/preview')
candidate=pin(preview,'repository-file-inventory.v237.json');candidate['path']=IP
parent=projection['parent'];inherited=[dict(parent=candidate,selector=e['selector'],before=e['before'],after=e['after'])for e in projection['projections']]
projection.update(candidate=candidate,proposedInventoryPassageInheritance=inherited,codeUnitAccepted=False,inventoryBound=False)
put(S/'inventory/meaning-projection.json',projection)
record=dict(schemaVersion=1,unit='D2B4B-inventory-v237-r1',standing='PROPOSED with full4b code, independently assessed together; no integration/acceptance inferred',parent=parent,candidate=candidate,parentArtifactBytesUnchanged=True,inheritedRowsEqualByValue=True,packagesUnchanged=True,pendingDecisionsUnchanged=True,addedFiles=new,changedFiles=existing,realizedPlannedFiles=[],productParent=ph,codeProductMap=pin(S,'product-map.json'),integrationCensus=pin(S,'evidence/repository-r1/report.json'),productQualification=False)
put(S/'inventory/successor.json',record);successor=pin(S,'inventory/successor.json');successor['path']=INV+'/successor.json'
put(S/'inventory/publication-map.json',dict(candidate=candidate,successorRecord=successor,meaningProjection=INV+'/meaning-projection.json',candidateFrozenMember='inventory/preview/repository-file-inventory.v237.json',successorFrozenMember='inventory/successor.json',bindingRequiresIndependentAssessmentAndRootAssent=True))
scope=dict(unit='D2B-4b-r1',standing='FULL SEND/REQUEST/SCHEDULE/PARTICIPANT CODE + OWN STRICT INVENTORY237; UNACCEPTED',sourcePaths=24,newPaths=18,existingPaths=6,componentsTests=362,identityTests=86,rust3Tests=87,newTestsSinceAccepted4a=44,compiledRuntimeMutants=21,allSourcesRestored=True,baseComponents=318,baseIdentity=86,baseCandidateFailureSetsEqual=True,componentAllTargetClippyPassed=True,operabilityRows=115,mintRowsBefore=453,mintRowsAfter=462,inventory=dict(parent=parent,candidate=candidate,record=successor,parentRows=1392,candidateRows=1410,inheritedMeanings=138,directCurrentMeanings=7,projectedMeanings=145),scope='Complete host builders for all ordinary frame families; inline/ref host variants; immutable canonical schedule and independent sender; base D3a participant, bounded acquisition, zero-copy original candidate handoff and cleanup. Supplied C4/native projections are trusted inputs, never Plan/set/source admission. Reference worker/census admission and FA2 hosts/replays remain4c under A2. Standalone reference sender tested for1/257, participant rejects those sessions until4c; exact offered arrays are never stripped.',runtimeScope='Current23Rust source pins tested. Subsequent24thpath only lexical census JSON, consumed by Python source checks, not Rust; all24verified in repository-r1. Full workspace, feature/platform, child/provider, production/source39 and project qualification are not established by component suites.',binaryCustody='Mutants freshly compiled and executed one at a time, artifact fresh=false and SHA/runtime logs/source retained. Executables reused the dedicated target path; past binary bytes are not frozen members or claimed live rehashable.',carried=['No production session factory/caller or C4/H completion.','FA2 host/worker successors and reference worker admission/reconstruction/faults, trial07Rust3 raw0.0 and successor replays remain4c.','Current six old raw descriptions retained unchanged by strictinventory; separate accepted description successor185 required.','All other project owner/privacy/platform/Linux/toolchain/source39/clock/T2/production/qualification gates remain open.'],productQualification=False,entireProjectComplete=False)
put(S/'SCOPE.json',scope)
members=[pin(S,str(p.relative_to(S)))for p in sorted(S.rglob('*'))if p.is_file()]
manifest=dict(schemaVersion=1,unit='D2B-4b-r1',productParent=ph,architectureParent=ah,candidatePaths=paths,members=members)
put(Q/'subject.json',manifest);subject=pin(Q,'subject.json')
expected=dict(verdict='ACCEPT-UNIT',subjectManifestSha256=subject['sha256'],requiredFindings=[],nonBlockingObservations=[],inventoryCandidateAssessment=dict(verdict='ACCEPT',requiredFindings=[],**candidate,parent=parent,successorRecord=successor),productQualification=False)
(Q/'REQUEST.md').write_text(f'''# D2b-4b r1: complete Rust3 host codec/participant and own inventory237

Read subject.json SHA256 {subject['sha256']} and the complete frozen subject/ tree. Rehash all {len(members)} members and actual24candidate files at {W}, comparing six parent versions and18newpaths to product main {ph}; architecture main {ah}. Full ACCEPT-UNIT or REQUIRED-FINDINGS for the COMPLETE unit is requested, plus a separate explicit substantive inventoryCandidateAssessment within the same review. This is not a helper preflight and no acceptance/integration is presumed.

Authorities: accepted M3-D r5, D2b PLAN-r3/A1/A2 and accepted3a A2 assent; current exact schemas/carriers/RPP/P3T and guard overlay; RUST3-LIM host builder LD17 belongs4b. Inspect all55 duty IDs (23builder/sender locations are an index, not semantic proof). Judge whether existing accepted law suffices or identify a concrete design selection required. In particular judge the A2 staging boundary: complete by-reference StageRequestV3 host builder/sender at ALL counts is implemented and tested; current accepted4a receiver deliberately refuses reference/census sessions, so base Participant preserves that gate until4c. No token is stripped and no V2 is substituted under an offered reference token. FA2 host/worker variants, reference worker reconstruction/admission/faults, successor/trial07Rust3raw0.0 replays stay4c. Do not infer their completion or silently shrink4b scope.

Inspect complete implementation: source-derived exact32limits and signed token order, native identity/set joins, snapshot/dependency/prepared manifests/chunks/seals, complete native H versus raw wire digest recipes, all per-key C4scope2 joins and unchanged subject/domain commitments, exact C2 literal/optional absence and stage ordinals. Prepared selected set carries EVERY inert row including failed rows with exact setH, raw blob fields and generated equality; no row filtering, stale/fallback selection or execution authority. C4 already owns native/set/Plan/freshness/representability admissions; these JSON/Value projections do not establish them.

Verify REQUEST-WIRE-ACCOUNTING full envelopes and greedy chunks,9GiB request/1M frames and one exact maximal Cancel reserve at actual final sequence; independent sender walk from Plan (not slots/context), actual slot/frame/digest/coordinate/final-entry/zero-entry/seal/total guards before sent state, typed actual consumed Open/Analyze Cancel echoes, latched refusals. Full inline envelope sizing refuses F1 even at256subjects, before repeated subject materialization; no dummy big chunk buffers or invented caps. The Participant gates source on actual table acknowledgments, finishes each pending physical frame beforeCancel, does at most one pipe IO per step, classifies host vs provider faults, precharges transport frames before prefix/payload allocation even for coalesced reads, preserves supervisor-owned ZeroExit-beforeEOF, and moves original candidate buffers once only atDONE. Check pointer-identity control, all terminals including pre/postUnavailable, no output after earlyEOF/latefault/discard/cancelled candidates. It grants no H fact admission.

Evidence: fresh accepted base318components/86identity and exact candidate362/86 have equal empty failure sets;87focused owning checks and components alltargetClippy-Dwarnings pass. All21mutants were freshly compiled, each killed by its named runtime witness (not compile failure), then all23Rust pins restored and freshly recompiled87positive; sources/logs/compiler artifacts and recorded executable SHA are frozen. Past mutant executables reused a target path and are NOT retained binary members. Current24thpath is only lexical census JSON; Python repository checks validate all24. Code/test history failures are preserved: domain compile/missing-root failures, snapshot API compile correction, dependency fixture map-order equality corrected to deterministic bytes, prepared fixture parse failure, request fixed-slot bug10->9 caught by full prepared positive, participant fixture AsRef compile failure, publicAPI lints/metadata-position correction. These are historical failed attempts, not passing or mutation proof. No full workspace/feature/platform/provider qualification claim.

Source/duty/repository gates: package edges, source115events/462constructor rows, tenenvironment checks, selecteddesign/generation/admission sources, diff, public19file census closure and both recomputed current public receipt bindings pass with ZERO blind/tree/private invocations. All115accepted owner annotations/rows and all453parentmintrows, owner definitions/member list/other census fields stay exact; nine new from/into lexical rows are ordinary conversions/container construction, not identity mint authority. The first census script wrongly assumed historical114 and generator owner equality; it stopped before writing. Corrected census preserves accepted invocation_mode owner annotation verbatim.

Inventory assessment: exact candidate {candidate}, successor record {successor}; see inventory/publication-map.json. Strict18newpaths =>1410rows, all1392parentrows equal by value, allotherfields/20packages/9pending/91plannedabsences unchanged, covers parenttracked paths plus18new. Independently reconstruct/project ALL138inherited current236meanings PLUS7DIRECT current236overrides from current contract records =>145, preserving before/after meanings and reindexing by path. No new meaning/supersession or description contract acceptance. Combined code+inventory assessment uses the existing verifier profile unchanged; binding/integration/root assent remain lead work only after exact acceptance. Separate description185/status/push remain owed. Root and review acceptance, not this manifest, establish any accepted state.

Read-only source/JSON/hashes/Git only. NO builds/tests/Cargo/generation/lanes/network/panes/delegation; no private corpus413/T2/store/cache/overlay/keys/real installation/held trees or census modes. Do not edit either repository, worktree, subject, controls or evidence. Write ONLY REVIEW.md and review.json in {Q}. IDs D2B4B-R1-RF-n/NBO-n. Required JSON shape (use REQUIRED-FINDINGS with actual findings when warranted):

{json.dumps(expected,indent=2)}
''')
prepared=dict(unit='D2B-4b-r1',reviewDirectory=str(Q),stage=str(S),subject=subject,members=len(members),productParent=ph,architectureParent=ah,sourcePins=pins,candidate=candidate,inventoryRecord=successor,inventoryPrefix=INV,productQualification=False,reviewSubmitted=False)
put(F/'full-r1-prepared.json',prepared)
for row in members:assert pin(S,row['path'])==row
for row in pins:assert pin(W,row['path'])==row
assert git(P,'rev-parse','HEAD')==ph and git(A,'rev-parse','HEAD')==ah
print(json.dumps(dict(subject=subject,members=len(members),reviewDirectory=str(Q),candidate=candidate,record=successor),indent=2))
