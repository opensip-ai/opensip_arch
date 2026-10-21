from pathlib import Path
import json,hashlib,subprocess,datetime
F=Path(__file__).parent;Q=Path('/tmp/opensip-implementation/reviews/codex-native-owner-materialization-r2');sub=json.loads((Q/'subject.json').read_text());assert sub['unit']=='NATIVE-OWNER-MATERIALIZATION-r2';S=Path(sub['architectureStage']);PRE='docs/implementation/m3/native-publication/native-owner-patterns-materialization-r2';P=Path('/Users/sb/code/opensip-ai/opensip');A=P.parent/'opensip_arch';W=P.parent/'opensip-native-owner-patterns-takeover'
def pin(root,p):
 b=(root/p).read_bytes();return dict(path=p,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def git(root,*args):return subprocess.check_output(['/usr/bin/git','-C',str(root),*args],text=True).strip()
assert git(P,'rev-parse','HEAD')==git(W,'rev-parse','HEAD')==sub['productBase'] and git(A,'rev-parse','HEAD')==sub['architectureBase']
assert not git(P,'status','--porcelain') and not git(A,'diff','--name-only','HEAD')
assert pin(S,sub['subjectManifest']['path'])==sub['subjectManifest'];m=json.loads((S/sub['subjectManifest']['path']).read_text());assert len({r['path'] for r in m['files']})==len(m['files'])
for r in m['files']:assert pin(S,r['path'])==r
rows=json.loads((S/PRE/'product-map.json').read_text())['rows'];assert len(rows)==42 and len({r['path'] for r in rows})==42 and sum(r['parent'] is None for r in rows)==15
for r in rows:
 assert pin(W,r['path'])==r['candidate'] and pin(S,r['archived']['path'])==r['archived'];assert all(r['candidate'][k]==r['archived'][k] for k in ['bytes','sha256'])
 if r['parent'] is None:assert not (P/r['path']).exists()
 else:assert pin(P,r['path'])==r['parent']
checks=json.loads((S/PRE/'checks-summary.json').read_text());final=checks['completeOwning'];assert final['allPassed'] and final['sourcePinsUnchanged'] and final['formatPassed'];assert len(final['runs'])==21 and all(r['exitCode']==0 for r in final['runs']);assert final['sourcePins']=={r['path']:r['candidate']['sha256'] for r in rows}
assert checks['compiledMutants']==17 and checks['storageReleaseBoundary']['allPassed']
finite=checks['finiteDifferential'];assert finite['inheritedFormSetEqual'] and finite['candidateInheritedForms']==72 and finite['newSharedForms']==0 and finite['nativeOnlyFormsRefusedByInherited'] and finite['mismatchCount']==0
closure=json.loads((W/'tools/contracts/generator-closure.json').read_text());assert len(closure['files'])==352
for r in closure['files']:assert pin(W,r['path'])==r
outputs=json.loads((F/'generated-output-audit.json').read_text())['outputs'];assert len(outputs)==8
for r in outputs:
 a=pin(W,r['path']);assert all(a[k]==r[k] for k in a)
for key,restored,caught,count in [('originalMutants','allRestored','allCaught',13),('companionMutants','restored','all4Caught',4)]:
 report=checks[key];assert report[restored] and report[caught] and report['restoredPositiveControlsPassed'] and len(report['mutations'])==count
 for p,h in report['originalPins'].items():assert pin(W,p)['sha256']==h
 assert all(not r['compileFailure'] and r['failedTests'] for r in report['mutations'])
legacy=(P/'crates/identity/src/schema_patterns.rs').read_text();candidate=(W/'crates/identity/src/schema_patterns.rs').read_text();assert candidate.split('/// Closed selected native-owner ECMA-u pattern forms.')[0].rstrip()==legacy.rstrip()
assert json.loads((F/'public-combined-binding-readiness.json').read_text())['cumulativeUnionMatches']
audit=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),standing='ROOT INDEPENDENT LIVE COMPLETE R2 REHASH/CHECK AUDIT; NOT ACCEPTANCE BEFORE INDEPENDENT VERDICT',subjectManifest=sub['subjectManifest'],manifestMembers=len(m['files']),productPaths=42,existingParents=27,newPaths=15,sourcePinsMatchFinalOwning=True,completeChecks=21,allChecksPassed=True,generatorInputsRehashed=352,outputsRehashed=8,compiledMutantsCaught=17,mutationRestorationExact=True,inheritedInterpreterPrefixExactPredecessor=True,inheritedForms=72,newSharedForms=0,storageReleaseBoundaryPassed=True,publicCombinedBindingDeltaUnionMatches=True,blindRefreshComplete=False,unitAccepted=False,productQualification=False)
(F/'root-complete-unit-r2-audit.json').write_text(json.dumps(audit,indent=2)+'\n');print(json.dumps(audit,indent=2))
