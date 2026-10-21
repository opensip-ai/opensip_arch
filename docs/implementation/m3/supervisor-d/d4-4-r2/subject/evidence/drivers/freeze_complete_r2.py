from pathlib import Path
import os,json,hashlib,subprocess,shutil,re
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;W=Path('/Users/sb/code/opensip-ai/opensip-d4factory-takeover');A=W.parent/'opensip_arch';P=W.parent/'opensip';B=F/'complete-r2';S=B/'subject';R=Path('/tmp/opensip-implementation/reviews/codex-d4-4-r2');R1=Path('/tmp/opensip-implementation/reviews/codex-d4-4-r1');S1=F/'complete-r1/subject';assert not B.exists() and not R.exists()
phase=json.loads((F/'r2-verification-process-r2.json').read_text());assert phase['status']=='complete' and all(x['exitCode']==0 for x in phase['completed'])
m1=json.loads((R1/'subject.json').read_text());v1=json.loads((R1/'review.json').read_text());assert v1['verdict']=='REQUIRED-FINDINGS' and v1['subjectManifestSha256']==hashlib.sha256((R1/'subject.json').read_bytes()).hexdigest()
base=m1['productParent'];abase=m1['architectureParent']
for root,expected in [(W,base),(P,base),(A,abase)]:assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()==expected
host=json.loads((F/'host-regressions-r7/report.json').read_text());pins=host['sourcePins'];assert host['allPassed'] and '436 passed; 0 failed; 4 ignored'in host['summaries'][0] and len(pins)==32
for name in ['native-clippy-r10','repository-r3','component-regressions-r3','doc-controls-r3']:
 j=json.loads((F/name/'report.json').read_text());assert j['allPassed'] and j['sourcePins']==pins,name
for name,count in [('core-mutants-r5',5),('native-route-mutants-r4',4),('identity-version-mutants-r1',3)]:
 j=json.loads((F/name/'report.json').read_text());assert j['allKilled'] and j['sourceRestored'] and j['restored']['allPassed'] and len(j['cases'])==count and all(case['before']==next(p for p in pins if p['path']==case['target']) for case in j['cases']) and [p['path']for p in j['sourcePins']if p!=next(n for n in pins if n['path']==p['path'])]==['crates/host/tests/factory_fixture.rs'],name
assert json.loads((F/'identity-version-mutants-r1/report.json').read_text())['restoredSourcePin']['allPassed']
canonical=json.loads((F/'native-clippy-r10/report.json').read_text())['sourcePins'];assert pins==canonical
for pin in m1['members']:
 raw=(S1/pin['path']).read_bytes();assert len(raw)==pin['bytes'] and hashlib.sha256(raw).hexdigest()==pin['sha256']
shutil.copytree(S1,S);R.mkdir(parents=True)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def out(path,raw):
 p=S/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
def copy(src,path):out(path,src.read_bytes())
def dump(path,value):out(path,(json.dumps(value,indent=2,ensure_ascii=False)+'\n').encode())
def pin(path,logical=None):
 raw=path.read_bytes();return dict(path=logical or path.relative_to(S).as_posix(),bytes=len(raw),sha256=sha(raw))
# All original evidence stays intact in history, never relabelled as current.
shutil.move(str(S/'evidence'),str(S/'history/r1-evidence'))
for name in ['SCOPE.json','product-map.json','REQUIREMENTS.json']:
 copy(S1/name,'history/r1/'+name)
for name in ['successor.json','publication-map.json','meaning-projection.json']:copy(S1/'inventory'/name,'history/r1/inventory/'+name)
for name in ['REQUEST.md','subject.json','REVIEW.md','review.json']:copy(R1/name,'history/r1-review/'+name)
copy(F/'root-peer-audit-publication-finding-r1.json','history/root-peer-audit-publication-finding-r1.json');copy(F/'r2-verification-process.json','history/failed-r2-verification-process.json');
for p in (F/'host-regressions-r6').rglob('*'):
 if p.is_file():copy(p,'history/failed-r2-host-regressions-r6/'+p.relative_to(F/'host-regressions-r6').as_posix())
copy(F/'root-offset-finding-r1.json','history/root-offset-finding-r1.json');copy(F/'r1-review-disposition.json','history/r1-review-disposition.json')
changed=[]
for row in pins:
 path=row['path'];raw=(W/path).read_bytes();assert pin(W/path,path)==row
 previous=(S1/'product'/path).read_bytes()
 if raw!=previous:copy(S1/'product'/path,'history/r1-product/'+path);changed.append(path)
 copy(W/path,'product/'+path)
expected_changes={'crates/components/src/provider_protocol/release_limits.rs','crates/components/src/session_factory/spec.rs','crates/components/src/provider_protocol/ts2/send.rs','crates/components/src/session_factory/tests.rs','crates/host/tests/factory_fixture.rs'};assert set(changed)==expected_changes
pm=json.loads((S1/'product-map.json').read_text());pm['paths']=pins;dump('product-map.json',pm)
req=json.loads((S1/'REQUIREMENTS.json').read_text());req['rows'].append(dict(id='D4F-21',title='Independent exact TS2 identity versions',requirement='Selected IdentityVersionsV1 constants, tied by required TS2 Hello/HelloAck schema refs, independently judge both actual sender Hello and receiver context exact count/keys/values before recheck. Seven unilateral/agreed-wrong value/missing/substituted/extra/empty-map controls and three compiled mutants; no new profile or producer authority.',navigation='crates/components/src/provider_protocol/release_limits.rs and session_factory/spec.rs'));dump('REQUIREMENTS.json',req)
current=['host-regressions-r7','component-regressions-r3','platform-regressions-r1','lifecycle-regressions-r1','fixture-conversion-owning-r2','doc-controls-r3','native-clippy-r10','fixture-guards-r2','core-mutants-r5','native-route-mutants-r4','identity-version-owning-r1','identity-version-mutants-r1','native-adapter-owning-r12','repository-r3','source-census-r1','source-census-audit-r1','constructor-pin-r3','host-base-r1']
for name in current:
 for p in (F/name).rglob('*'):
  if p.is_file():copy(p,'evidence/'+name+'/'+p.relative_to(F/name).as_posix())
for name in ['r2-verification-process-r2.json','r2-mutation-applicability.json']:copy(F/name,'evidence/'+name)
for p in F.glob('*.py'):copy(p,'evidence/drivers/'+p.name)
# Offset metadata correction is exact and validated against original bytes.
constructor=json.loads((S/'evidence/constructor-pin-r3/report.json').read_text());assert constructor['allRawByteOffsetsValidated']
for row in constructor['allIdentifierOccurrences']:
 raw=(W/row['path']).read_bytes();assert raw[row['byteOffset']:].startswith(b'from_recheck');assert raw.decode()[row['characterOffset']:].startswith('from_recheck')
archive='docs/implementation/m3/supervisor-d/d4-4-r2/subject';idir='docs/implementation/m3/supervisor-d/d4-4-inventory-v239-r2';candidate=pin(S/'inventory/preview/repository-file-inventory.v239.json','docs/implementation/m2/repository-file-inventory.v239.json');assert candidate==m1['inventoryCandidate']
record=json.loads((S1/'inventory/successor.json').read_text());record['unit']='D4-4-inventory-v239-r2';record['codeProductMap']=pin(S/'product-map.json',archive+'/product-map.json');record['integrationCensus']=pin(S/'evidence/repository-r3/report.json',archive+'/evidence/repository-r3/report.json');dump('inventory/successor.json',record);recordpin=pin(S/'inventory/successor.json',idir+'/successor.json')
projection=json.loads((S1/'inventory/meaning-projection.json').read_text());dump('inventory/meaning-projection.json',projection)
pub=json.loads((S1/'inventory/publication-map.json').read_text());pub.update(successorRecord=recordpin,meaningProjection=idir+'/meaning-projection.json',codeArchivePrefix=archive);dump('inventory/publication-map.json',pub)
for k in ['codeProductMap','integrationCensus']:
 r=record[k];assert pin(S/r['path'].removeprefix(archive+'/'),r['path'])==r
# Retain prior test identities, with exactly one new component drift control.
reg=[]
for name,old,now in [('host',F/'host-base-r1/host.log',F/'host-regressions-r7/owning.log'),('components',Path('/tmp/opensip-implementation/rust3-successor-takeover-2026-10-21/candidate-suites-r3/opensip_components.log'),F/'component-regressions-r3/owning.log')]:
 def tests(p):return dict(re.findall(r'^test (.+) \.\.\. (ok|ignored|FAILED).*$',p.read_text(),re.M))
 before=tests(old);after=tests(now);assert before and set(before)<=set(after) and all(after[k]==v for k,v in before.items());reg.append(dict(suite=name,parentCount=len(before),currentCount=len(after),removed=[],existingOutcomesUnchanged=True,added=sorted(set(after)-set(before))))
dump('evidence/regression-identity-comparison.json',dict(suites=reg,productQualification=False))
scope=json.loads((S1/'SCOPE.json').read_text());scope.update(unit='D4-4-r2',standing='COMPLETE corrected D4-4 library unit and exact inventory239 successor; R1 REQUIRED-FINDINGS preserved; UNACCEPTED pending fresh independent review.',componentTests=419,compiledRuntimeMutants=12,coreFactoryControls=7,identityVersionDriftCases=7,independentIdentityVersions='Four selected protocol constants independently compare both actual TS2 outputs; exact source refs and complete required/closed key set pinned. No caller/codec map supplies expected values.',sourcePaths=32,codeArchivePrefix=archive,currentRuntimeCutoff='Fresh32-path full host436/components419/doc16, native13, all-target Clippy and repository/public-binding evidence after atomic peer audit fix. Core5/native4/identity3 compiled mutation target bytes remain exact; only host-only peer audit source differs globally from mutant cutoff, with fresh atomic-peer native13 controls. No mutated-target behavior changed or control waived. Platform301/lifecycle98 and fixture guards have unchanged owned inputs.',requiredFindingDispositions=[dict(id='D4F-R1-RF-1',status='fixed-proposed',correction='Pinned constant authority and both-output exact count/key/value validation before recheck; agreed-wrong and unilateral controls plus3compiled mutants.')],rootRequiredCorrections=[dict(id='LEAD-D4F-R1-OFFSET-1',status='fixed-proposed',correction='Current constructor report explicitly separates characterOffset and UTF-8 byteOffset; all15raw-byte positions validated. R1 report retained as historical.')],atomicPeerAuditCorrection='Observed host-r6 JSON truncation failure preserved. Peer now publishes complete pending sibling by atomic rename under existing audit mutex; no production code, test class, signal, timing or dependency policy changed.',mutationApplicability='evidence/r2-mutation-applicability.json',changesFromR1=changed,inventory=dict(parent=record['parent'],candidate=candidate,record=recordpin,parentRows=1422,candidateRows=1432,addedRows=10,realizedPriorPlannedRows=1,inheritedMeanings=150,directMeanings=11,totalMeanings=161,currentSupersessionsFolded=6))
dump('SCOPE.json',scope)
members=[pin(p)for p in sorted(S.rglob('*'))if p.is_file()];manifest=dict(schemaVersion=1,unit='D4-4-r2',productParent=base,architectureParent=abase,candidatePaths=m1['candidatePaths'],subjectRoot=str(S),members=members,inventoryCandidate=candidate,inventorySuccessor=recordpin,previousManifestSha256=v1['subjectManifestSha256'],productQualification=False);raw=(json.dumps(manifest,indent=2)+'\n').encode();(R/'subject.json').write_bytes(raw)
result=dict(subjectManifestSha256=sha(raw),members=len(members),reviewDirectory=str(R),subjectRoot=str(S),candidatePaths=m1['candidatePaths'],inventory=candidate,inventorySuccessor=recordpin,sourceChangedFromR1=changed,implementationAccepted=False,productQualification=False);(B/'freeze.json').write_text(json.dumps(result,indent=2)+'\n')
for row in pins:assert pin(W/row['path'],row['path'])==row
print(json.dumps(result))
