from pathlib import Path
import os,json,hashlib,subprocess,datetime
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent;W=Path('/Users/sb/code/opensip-ai/opensip-d4factory-takeover');P=W.parent/'opensip';A=W.parent/'opensip_arch';C=Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06/CURRENT-STATE.json')
def head(p):return subprocess.check_output(['/usr/bin/git','rev-parse','HEAD'],cwd=p,text=True).strip()
assert head(P)==head(W)=='c31809cb4993c5c2bbba3d004d9337f12f18d17b';assert head(A)=='a70566340747162650b863693e1ab3d887845b18'
reports={n:json.loads((F/n/'report.json').read_text()) for n in ['native-adapter-owning-r6','native-route-mutants-r1','core-mutants-r2','native-clippy-r3','host-regressions-r1','lifecycle-regressions-r1','fixture-guards-r1']}
for n in ['native-adapter-owning-r6','native-clippy-r3','host-regressions-r1','lifecycle-regressions-r1','fixture-guards-r1']:assert reports[n]['allPassed'],n
for n in ['native-route-mutants-r1','core-mutants-r2']:assert reports[n]['allKilled'] and reports[n]['sourceRestored'] and reports[n]['restored']['allPassed'],n
pins=reports['native-clippy-r3']['sourcePins']
for pin in pins:
 b=(W/pin['path']).read_bytes();assert len(b)==pin['bytes'] and hashlib.sha256(b).hexdigest()==pin['sha256'],pin['path']
for n in ['native-adapter-owning-r6','native-route-mutants-r1','core-mutants-r2']:assert reports[n]['sourcePins']==pins,n
j=json.loads((F/'CONTINUATION.json').read_text());j.update(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),sourcePins=pins,sourcePaths=len(pins),nativeCIAdapterImplemented=True,operationHeldPinPreserved=True,implementationAccepted=False,productQualification=False,entirePlanComplete=False,currentProcesses=[],
 standing='UNACCEPTED D4-4 factory/core/platform/native CI adapter implemented. Actual native factory routes and both mapping mutants pass; all five current core runtime mutants killed. Full host library and lifecycle regressions passed at documented cutoffs. Provider-spoken spawned fixture controls, complete-unit review, integration and qualification remain owed.',
 nextAction='Implement first-party compiled provider-spoken substitution controls using actual factory-produced closed launch specs and real supervisor/codec participant: control stableId/manifest/tuple mismatches and effectRequest, provider identity/token mismatches, assert own routes, zero source bytes and no Analyze. Cover TS2 native composition. Complete constructor/census/owner gates and final full affected suites; strict inventory239 must preserve161 meanings and fold6 supersessions including a supersession target. Freeze whole unit for CODEX2 plus inventory assessment, root assent, exact integration, descriptions/status and push. Continue entire project afterward.',
 goalTurnClassification='progress',nativeAdapterEvidence={
 'currentOwningReport':'native-adapter-owning-r6/report.json','currentOwningTests':9,'corruptionCasesThroughFactory':['Digest','Length','Mode','Type','Absent'],'actualInjectedReadIoThroughFactory':True,'typedOwnerRoutesAsserted':True,'oneShortBeforeNativeOpenAndReadThroughFactory':True,
 'nativeRouteMutationReport':'native-route-mutants-r1/report.json','nativeRouteMutantsCompiledAndKilled':2,
 'coreMutationReport':'core-mutants-r2/report.json','coreMutantsCompiledAndKilled':5,'restoredCoreTests':6,
 'currentClippyReport':'native-clippy-r3/report.json','allTargetWarningDeniedClippy':True,
 'fullHostReport':'host-regressions-r1/report.json','fullHostPassed':432,'fullHostFailed':0,'fullHostExistingIgnored':4,'fullHostCutoff':'Before test-only expansion of one native factory corruption control to all five corruption kinds plus I/O; production bytes unchanged, current expanded9 controls recompiled and pass.',
 'lifecycleReport':'lifecycle-regressions-r1/report.json','lifecyclePassed':98,'lifecycleCutoff':'Lifecycle source unchanged since this complete suite; later changes only host test composition.',
 'fixtureGuardsReport':'fixture-guards-r1/report.json','featurelessHostNoScenarioHook':True,'releaseFixtureFeatureRejected':True,
 'providerSpokenSpawnControlsComplete':False,'productionCompositionComplete':False})
j['checks'].update(currentNativeComposition='native-adapter-owning-r6/report.json',currentClippy='native-clippy-r3/report.json',currentCoreMutants='core-mutants-r2/report.json',currentNativeRouteMutants='native-route-mutants-r1/report.json',fullHostLibrary='host-regressions-r1/report.json',fullLifecycleLibrary='lifecycle-regressions-r1/report.json',fixtureGuards='fixture-guards-r1/report.json')
j['coreMutationStanding']='All five required core mutations freshly compiled and killed at current source pins, restored six owning tests pass; two additional native adapter mapping mutations freshly compiled and killed through actual store/factory, restored nine native tests pass. Future production source changes require revalidation.'
for name in ['CURRENT.json','CONTINUATION.json']:(F/name).write_text(json.dumps(j,indent=2)+'\n')
c=json.loads(C.read_text());c['currentExecution']=j;c['D4FactoryTakeover']=j;C.write_text(json.dumps(c,indent=2)+'\n')
(F/'native-factory-checkpoint-r2.json').write_text(json.dumps(dict(utc=j['utc'],goalTurnClassification='progress',sourcePins=pins,productHead=head(P),architectureHead=head(A),implementationAccepted=False,productQualification=False,entirePlanComplete=False,continuation=str(F/'CONTINUATION.json'),nextAction=j['nextAction']),indent=2)+'\n')
print(json.dumps(dict(sourcePaths=len(pins),nativeOwning=9,coreMutantsKilled=5,nativeMutantsKilled=2,hostPassed=432,lifecyclePassed=98,independentReviewSubmitted=False,implementationAccepted=False,entirePlanComplete=False)))
