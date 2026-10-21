from pathlib import Path
import os,json,hashlib,subprocess,shutil,re
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;W=Path('/Users/sb/code/opensip-ai/opensip-d4factory-takeover');P=W.parent/'opensip';A=W.parent/'opensip_arch';B=F/'complete-r1';S=B/'subject';R=Path('/tmp/opensip-implementation/reviews/codex-d4-4-r1');assert not B.exists() and not R.exists()
base='c31809cb4993c5c2bbba3d004d9337f12f18d17b';abase='a70566340747162650b863693e1ab3d887845b18'
def head(p):return subprocess.check_output(['git','rev-parse','HEAD'],cwd=p,text=True).strip()
assert head(W)==head(P)==base and head(A)==abase
report=json.loads((F/'host-regressions-r5/report.json').read_text());assert report['allPassed'] and '436 passed; 0 failed; 4 ignored'in report['summaries'][0];pins=report['sourcePins'];assert len(pins)==32
for name in ['native-clippy-r8','repository-r1']:
 j=json.loads((F/name/'report.json').read_text());assert j['allPassed'] and j['sourcePins']==pins
for name in ['core-mutants-r4','native-route-mutants-r3']:
 j=json.loads((F/name/'report.json').read_text());assert j['allKilled'] and j['sourceRestored'] and j['restored']['allPassed'] and j['sourcePins']==pins
paths=sorted(subprocess.check_output(['git','ls-files','-m','-o','--exclude-standard'],cwd=W,text=True).splitlines());assert paths==[p['path']for p in pins]
def sha(b):return hashlib.sha256(b).hexdigest()
def out(path,data):
 p=S/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
def copy(src,path):out(path,src.read_bytes())
def dump(path,j):out(path,(json.dumps(j,indent=2,ensure_ascii=False)+'\n').encode())
def pin(path,logical=None):
 b=path.read_bytes();return dict(path=logical or str(path.relative_to(S)),bytes=len(b),sha256=sha(b))
S.mkdir(parents=True);R.mkdir(parents=True);new=[];existing=[]
for p in pins:
 src=W/p['path'];assert pin(src,p['path'])==p;copy(src,'product/'+p['path']);old=subprocess.run(['git','show',base+':'+p['path']],cwd=W,capture_output=True)
 if old.returncode==0:out('parent/'+p['path'],old.stdout);existing.append(p['path'])
 else:new.append(p['path'])
assert len(new)==11 and len(existing)==21
product_map=dict(productParent=base,paths=pins,newPaths=new,existingPaths=existing,productionCallerAdded=False,newRuntimeDependencies=False,newTestOnlyDevFeature='opensip-host -> opensip-platform/test-fixture',productQualification=False)
dump('product-map.json',product_map)
copy(F/'REQUIREMENTS.json','REQUIREMENTS.json');copy(F/'parent-refresh-r1.json','history/parent-refresh-r1.json')
# Scope-relevant accepted public authorities and exact locked records. No
# private corpus, live installation, keys, target cache or blind content.
lock=json.loads((P/'design-lock.json').read_text());copy(P/'design-lock.json','authority/product/design-lock.json');copy(P/'Cargo.lock','authority/product/Cargo.lock')
authorities=['docs/implementation/m3/supervisor-d/PROPOSAL-r5.md','docs/implementation/m3/supervisor-d/d4/PLAN-r1.md','docs/implementation/m3/supervisor-d/d4/PLAN-r2.md','docs/implementation/m3/component-install/CI-A3-r4.md','docs/implementation/m3/component-install/PLAN-r3.md','docs/implementation/m3/supervisor-d/d2b/PLAN-r3.md','docs/implementation/m2/repository-file-inventory.v238.json','docs/implementation/m2/repository-file-inventory.v237.json']
for path in authorities:copy(A/path,'authority/architecture/'+path)
for binding in lock['contractSuccessors']:
 p=binding['record'];assert pin(A/p['path'],p['path'])==p;copy(A/p['path'],'authority/architecture/'+p['path'])
# Unchanged source context is separately pinned, never counted as a change.
context=['crates/components/Cargo.toml','crates/components/src/supervisor.rs','crates/components/src/supervisor_records.rs','crates/components/src/provider_protocol/rust3/receive.rs','crates/components/src/provider_protocol/rust3/receive_tests.rs','crates/components/src/provider_protocol/ts2/carrier.rs','crates/components/src/provider_protocol/ts2_tests.rs','crates/platform/Cargo.toml','crates/platform/src/lib.rs','crates/platform/src/work_ledger.rs','crates/platform/src/process_tests.rs','crates/lifecycle/Cargo.toml','crates/security/src/archive_profile.rs','crates/security/src/trust_admitted_components.rs','crates/security/src/component_manifest.rs','tools/check_operability.py','tools/check_package_edges.py','tools/verify_design.py','schemas/sources/handshake-v1.schema.json','crates/components/tests/data/rust3-startup-shape.v1.json','crates/security/tests/fixtures/manifest268-semantic.ndjson']
for path in context:
 if path not in paths:copy(W/path,'context/product/'+path)
# Current evidence plus explicit historical cutoffs and failures. Executable
# hashes identify past runs; mutable target binaries are intentionally absent.
current=['host-regressions-r5','component-regressions-r1','platform-regressions-r1','lifecycle-regressions-r1','fixture-conversion-owning-r2','doc-controls-r1','native-clippy-r8','fixture-guards-r2','core-mutants-r4','native-route-mutants-r3','repository-r1','source-census-r1','source-census-audit-r1','constructor-pin-r2','host-base-r1']
history=['native-adapter-owning-r1','native-adapter-owning-r2','provider-spoken-r1','provider-spoken-r2','provider-spoken-r3','native-adapter-owning-r7','host-regressions-r2','native-clippy-r4','fixture-conversion-owning-r1','ts2-provider-spoken-r1']
for category,names in [('evidence',current),('history',history)]:
 for name in names:
  source=F/name;assert source.is_dir(),name
  for p in source.rglob('*'):
   if p.is_file():copy(p,category+'/'+name+'/'+p.relative_to(source).as_posix())
for p in F.glob('*.py'):copy(p,'evidence/drivers/'+p.name)
for p in F.glob('*lane.log'):copy(p,'history/lane-logs/'+p.name)
# Preserve all inventory rows and all current meanings by physical path.
preview=json.loads((F/'inventory239-preview/meaning-projection-preview.json').read_text());assert preview['newRows']==1432 and preview['totalMeanings']==161 and len(preview['foldedCurrentSupersessions'])==6
copy(F/'inventory239-preview/repository-file-inventory.v239.json','inventory/preview/repository-file-inventory.v239.json')
candidate=pin(S/'inventory/preview/repository-file-inventory.v239.json','docs/implementation/m2/repository-file-inventory.v239.json')
archive='docs/implementation/m3/supervisor-d/d4-4-r1/subject';idir='docs/implementation/m3/supervisor-d/d4-4-inventory-v239-r1'
projection=dict(preview);projection['candidate']=candidate;projection['inheritance']=[dict(parent=candidate,selector=r['selector'],before=r['before'],after=r['after'])for r in preview['projections']];projection['codeUnitAccepted']=False;dump('inventory/meaning-projection.json',projection)
record=dict(schemaVersion=1,unit='D4-4-inventory-v239-r1',standing='PROPOSED with complete D4-4 library unit; independent complete-unit/inventory assessment and root assent required',parent=preview['parent'],candidate=candidate,parentArtifactBytesUnchanged=True,inheritedRowsEqualByValue=True,packagesUnchanged=True,pendingDecisionsUnchanged=True,addedFiles=[r['path']for r in preview['addedRows']],changedFiles=existing,realizedPlannedFiles=['crates/components/src/session_factory.rs'],productParent=base,codeProductMap=pin(S/'product-map.json',archive+'/product-map.json'),integrationCensus=pin(S/'evidence/repository-r1/report.json',archive+'/evidence/repository-r1/report.json'),productQualification=False)
assert len(record['addedFiles'])==10 and len(set(record['addedFiles']+existing+record['realizedPlannedFiles']))==32
dump('inventory/successor.json',record);recordpin=pin(S/'inventory/successor.json',idir+'/successor.json')
dump('inventory/publication-map.json',dict(candidate=candidate,successorRecord=recordpin,meaningProjection=idir+'/meaning-projection.json',candidateFrozenMember='inventory/preview/repository-file-inventory.v239.json',successorFrozenMember='inventory/successor.json',bindingRequiresIndependentAssessmentAndRootAssent=True,codeArchivePrefix=archive))
# Prove every future archive-qualified reference resolves to these bytes.
for key in ['codeProductMap','integrationCensus']:
 ref=record[key];rel=ref['path'].removeprefix(archive+'/');assert pin(S/rel,ref['path'])==ref
# Baseline test identities remain present, not merely equal totals.
regressions=[]
for name,old,now in [('host',F/'host-base-r1/host.log',F/'host-regressions-r5/owning.log'),('components',Path('/tmp/opensip-implementation/rust3-successor-takeover-2026-10-21/candidate-suites-r3/opensip_components.log'),F/'component-regressions-r1/owning.log')]:
 def tests(p):return {m[0]:m[1]for m in re.findall(r'^test (.+) \.\.\. (ok|ignored|FAILED).*$',p.read_text(),re.M)}
 before=tests(old);after=tests(now);assert before and set(before)<=set(after) and all(after[k]==v for k,v in before.items())
 regressions.append(dict(suite=name,parentCount=len(before),currentCount=len(after),removed=[],existingOutcomesUnchanged=True,added=sorted(set(after)-set(before))))
dump('evidence/regression-identity-comparison.json',dict(suites=regressions,productQualification=False))
scope=dict(unit='D4-4-r1',standing='COMPLETE D4-4 library session factory and host native adapter + strict own inventory239; UNACCEPTED',sourcePaths=32,newCodePaths=11,existingCodePaths=21,hostTests=436,hostExistingIgnored=4,componentTests=418,componentIgnored=0,platformTests=301,platformExistingIgnored=1,lifecycleTests=98,docControls=16,nativeFactoryControls=13,rust3SpokenSubstitutions=6,ts2SpokenSubstitutions=8,matchingAckBaselines=2,compiledRuntimeMutants=9,allMutationTargetsRestored=True,sourceOwnerRows=115,lexicalRowsBefore=463,lexicalRowsAfter=470,allOwnerAnnotationsAnd463ParentRowsUnchanged=True,inventory=dict(parent=preview['parent'],candidate=candidate,record=recordpin,parentRows=1422,candidateRows=1432,addedRows=10,realizedPriorPlannedRows=1,inheritedMeanings=150,directMeanings=11,totalMeanings=161,currentSupersessionsFolded=6),codeArchivePrefix=archive,currentRuntimeCutoff='host/core/native mutation/Clippy/repository evidence at exact32paths; component418 and doc16 at preceding31path cutoff before metadata and host-only CMS guard, unchanged compiled component/platform/lifecycle owner inputs; earlier platform301/lifecycle98 and feature guards explicitly pinned.',nativeRepresentation='Later CI-A3-r4 permits owned/clonable path result and optional file digest; directories supply None. Operation retains capability through settlement; factory does not forge directory digest or infer lifetime from owned carrier.',leadFix='Final source audit enforced actual CI CMS Entrypoint operation: generic same-file/alias/directory requests refuse before reads, with a freshly compiled omission mutant killed.',testFixtureClass='Only first-party compiled binary from registered harness-free target. Consuming release-refused dev-only VerifiedLaunch conversion changes class alone; exact carrier invariant passes.',failedAttempts='History preserves wrong fixture/control inputs, buffered stdout/EOF false-positive invalidation, wrong launch-class invalidation, source privacy compile failure, and style/import fixes; none count as acceptance or qualification.',D5GeneralStructuralGateComplete=False,productionCallerAdded=False,C4AdmissionClaimed=False,HSettlementClaimed=False,linuxClaimed=False,productQualification=False,entireProjectComplete=False)
dump('SCOPE.json',scope)
members=[pin(p)for p in sorted(S.rglob('*'))if p.is_file()]
manifest=dict(schemaVersion=1,unit='D4-4-r1',productParent=base,architectureParent=abase,candidatePaths=paths,subjectRoot=str(S),members=members,inventoryCandidate=candidate,inventorySuccessor=recordpin,productQualification=False)
manifestbytes=(json.dumps(manifest,indent=2)+'\n').encode();(R/'subject.json').write_bytes(manifestbytes);copy_path=B/'freeze.json';copy_path.write_text(json.dumps(dict(subjectManifestSha256=sha(manifestbytes),members=len(members),reviewDirectory=str(R),subjectRoot=str(S),candidatePaths=paths,inventory=candidate,inventorySuccessor=recordpin,implementationAccepted=False,productQualification=False),indent=2)+'\n')
for p in pins:assert pin(W/p['path'],p['path'])==p
print(json.dumps(dict(subjectManifestSha256=sha(manifestbytes),members=len(members),sourcePaths=len(paths),inventory=candidate,successor=recordpin,subjectRoot=str(S))))
