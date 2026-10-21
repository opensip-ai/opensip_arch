from pathlib import Path
import os,json,hashlib,shutil,subprocess
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;B=F/'fixture-authoring-r1';S=B/'product';P=Path('/Users/sb/code/opensip-ai/opensip');W=P.parent/'opensip-native-owner-patterns-takeover'
baseline=json.loads((F/'baseline-r1/report.json').read_text());assert baseline['mainUnchanged']
full=json.loads((F/'full-r1/report.json').read_text());assert full['sourcePinsUnchanged']
for p,h in full['sourcePins'].items():assert hashlib.sha256((W/p).read_bytes()).hexdigest()==h,p
manifest=json.loads((B/'staged-companions.json').read_text());assert len(manifest['newFiles'])==15
for row in manifest['newFiles']:
 raw=(S/row['path']).read_bytes();assert len(raw)==row['candidate']['bytes'] and hashlib.sha256(raw).hexdigest()==row['candidate']['sha256']
 assert not (W/row['path']).exists() and (W/row['priorPath']).read_bytes()==(P/row['priorPath']).read_bytes()
# Includes are explicit: no resolver/fallback/repair is introduced.
patches={
 'crates/host/src/native_owner_tests.rs':[(Path(r['priorPath']).name,Path(r['path']).name) for r in manifest['newFiles'] if r['path'].startswith('crates/host/')],
 'crates/host/src/fact_admission_tests.rs':[('replay-fixtures.current.json','replay-fixtures.native-owner-r1.json')],
 'crates/host/src/finalization_tests.rs':[('replay-fixtures.current.json','replay-fixtures.native-owner-r1.json')],
 'crates/evaluator/src/coverage.rs':[('coverage-registry.current.json','coverage-registry.native-owner-r1.json')],
 'crates/evaluator/src/import_payloads.rs':[('import-payload-registry.current.json','import-payload-registry.native-owner-r1.json')],
 'crates/evaluator/src/atoms.rs':[('cycle-representative.current.v1.json','cycle-representative.native-owner-r1.v1.json')],
 'crates/security/src/journal_store.rs':[('journal-seal-replay.current.json','journal-seal-replay.native-owner-r1.json')],
 'crates/storage/src/crash_matrix_support/run_candidate.rs':[('journal-seal-cases.json','journal-seal-replay.native-owner-r1.json'),('let f = object(&object(&f)["replay"]);','let f = object(&f);')],
 'crates/storage/src/commit_tests.rs':[('journal-seal-cases.json','journal-seal-replay.native-owner-r1.json'),('let f = object(&object(&f)["replay"]);','let f = object(&f);')],
}
results=[];proposed={}
for p,changes in patches.items():
 original=(W/p).read_text();assert (W/p).read_bytes()==(P/p).read_bytes(),p
 text=original;counts=[]
 for before,after in changes:
  count=text.count(before)
  if p!='crates/host/src/native_owner_tests.rs':assert count>0,(p,before)
  if count:text=text.replace(before,after);counts.append(dict(before=before,after=after,count=count))
 assert text!=original,p;proposed[p]=text;results.append(dict(path=p,replacements=counts))
for row in manifest['newFiles']:
 dst=W/row['path'];dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes((S/row['path']).read_bytes())
for p,text in proposed.items():(W/p).write_text(text)
# Existing style is preserved; format only files whose accepted base was clean.
formatting=[]
for p in patches:
 before=(P/p).read_bytes();r=subprocess.run(['/opt/homebrew/Cellar/rust/1.95.0/bin/rustfmt','--edition','2024','--emit','stdout'],input=before,capture_output=True)
 clean=r.returncode==0 and r.stdout==before
 if clean:subprocess.run(['/opt/homebrew/Cellar/rust/1.95.0/bin/rustfmt','--edition','2024',str(W/p)],check=True)
 formatting.append(dict(path=p,baseFormatClean=clean))
for row in manifest['newFiles']:assert (W/row['priorPath']).read_bytes()==(P/row['priorPath']).read_bytes()
report=dict(standing='UNACCEPTED COMPLETE MATERIALIZATION WITH DISTINCT SYNTHETIC COMPANIONS',newFiles=manifest['newFiles'],includeChanges=results,formatting=formatting,
 originalHistoricalAndCurrentFixturesUnchanged=True,sourceGuardUnchanged=True,noOutcomeOrCauseClassChanged=True,noNewRuntimeMetadataRowsDomainsSelectorsOwners=True,inventorySuccessorRequiredAfterOwnCodeAcceptance=True,
 mandatoryImmediateReviewedBlindRefreshBeforeCensusDependentConsumption=True,testsPassed=False,unitAccepted=False,productQualification=False)
(F/'fixture-companions-applied.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(newFiles=15,existingSourceFiles=len(patches),historicalInputsPreserved=True),indent=2))
