from pathlib import Path
import os,json,subprocess,datetime
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK')=='1'
F=Path(__file__).parent; C=Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06')
P=Path('/Users/sb/code/opensip-ai/opensip');A=P.parent/'opensip_arch'
integration=json.loads((F/'source-design-r1/integration.json').read_text())
env=dict(os.environ,GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null')
for key in ('GIT_DIR','GIT_WORK_TREE','GIT_CONFIG_COUNT'):env.pop(key,None)
def git(root,*args):return subprocess.check_output(['/usr/bin/git','-C',str(root),*args],text=True,env=env).strip()
assert git(P,'rev-parse','HEAD')==integration['productLock'] and git(A,'rev-parse','HEAD')==integration['architecture']
assert not git(P,'status','--porcelain') and not git(A,'diff','--name-only','HEAD')
push=[]
for root,key in ((A,'architecture'),(P,'productLock')):
 subprocess.run(['/usr/bin/git','-C',str(root),'push','origin','main'],env=env,check=True)
 remote=git(root,'ls-remote','origin','refs/heads/main').split()[0];assert remote==integration[key]
 push.append(dict(repository=str(root),head=remote,remoteVerified=True))
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
(F/'source-design-r1/push.json').write_text(json.dumps(dict(utc=now,repositories=push),indent=2)+'\n')
next_work=[
 'Prepare separately selected generator runtime/profile correction: exact current validate-schemas helper refuses new owner patterns outside its selected table. Do not weaken guard or rerun generator before independent design acceptance, root assent and real closure binding.',
 'After binding helper design, apply accepted helper/closure/registry bytes in isolated candidate, run selected offline generation and drift check, inspect every output delta; complete actual registered consumer, owning, feature, Clippy, meaningful mutation and source/package/environment/design controls.',
 'Obtain full code-unit review and root assent, integrate exact accepted bytes, immediately complete exact-main independently authorized B2-b4c3 blind-refresh sequence before any census-dependent consumption.',
 'Only then resume held D2b-3c; continue all remaining written project and qualification requirements.'
]
checkpoint=dict(utc=now,standing='ENTIRE PROJECT ACTIVE; SOURCE DESIGN ACCEPTED/BOUND/PUSHED; MATERIALIZATION UNACCEPTED',product=integration['productLock'],architecture=integration['architecture'],contractSuccessors=179,inventory=233,inventorySuccessors=193,
 acceptedSourceDesign=integration,sourceDesignPushed=True,sourcePreflight='r3 PREFLIGHT-CLEAR; all prior RFs closed',
 isolatedCandidate=str(P.parent/'opensip-native-owner-patterns-takeover'),candidateBase=integration['productLock'],candidateModifiedExistingPaths=11,compiledPinsUpdated=2,
 generatorAttempts=[dict(name='generation-r1',result='admission refusal: absent selected package inputs; no generation or output writes'),dict(name='generation-r2',result='352 selected inputs admitted; prepare passed; validate failed: pattern outside selected profile; no generation or output writes')],
 selectedGeneratorInputsProvisionedFromExistingCheckout=True,networkUsed=False,unitAccepted=False,blindRefreshComplete=False,reviewerPane='w8:p1',activeReview=None,nextWork=next_work,originalDraftsPreserved=True,productQualification=False,entirePlanComplete=False)
(F/'CHECKPOINT.json').write_text(json.dumps(checkpoint,indent=2)+'\n')
(C/'CONTINUATION-2026-10-21-NATIVE-OWNER.json').write_text(json.dumps(checkpoint,indent=2)+'\n')
statepath=C/'CURRENT-STATE.json';state=json.loads(statepath.read_text());state['currentExecution'].update(productHead=integration['productLock'],architectureHead=integration['architecture'],contractSuccessors=179,activeReview=None,activeReviewStatus='No active review. Source design ACCEPT-DESIGN-UNIT bound/pushed; generator helper profile successor required before next selected generation.',currentCandidate=checkpoint['isolatedCandidate'],candidateStanding=checkpoint['standing'],pushed=True,nextWork=next_work,integrationSession=None,activeRecoverySession=None)
state['NativeOwnerSourceSelectionBound']=dict(integration,pushed=True);state['NativeOwnerMaterializationProgress']=checkpoint
statepath.write_text(json.dumps(state,indent=2)+'\n')
plan=C/'ACTIVE-PLAN.md';prefix='2026-10-21 CURRENT: Native-owner source design ACCEPT-DESIGN-UNIT/root assent/bound contract179/PUSHED product'+integration['productLock'][:8]+'/ARCH'+integration['architecture'][:8]+'. Inventory233/193successors unchanged; r116 published status remains historical. Source preflightR3 CLEAR after2RF rounds; 3.1M native and8.586M inherited finite comparisons pass. Isolated materialization11existing paths includes2compiled whole-source pins+5accepted metadata; no unit acceptance. First selected generation refused absent cached packages; exact352closure inputs now verified/provisioned offline. Second admitted real design/closure and prepared, then selected runtime validation refused corrected patterns outside selected profile. No generated output writes. Next separately review/bind scoped generator helper/profile successor BEFORE rerun, then full materialization owning/actual-consumer/mutation/unitreview/integration and immediate mandatory independently authorized blind refresh; D2b3c remains held until refresh. No private contents accessed. Detailed CONTINUATION-2026-10-21-NATIVE-OWNER.json. Entire project goal ACTIVE.\n\n'
plan.write_text(prefix+plan.read_text())
print(json.dumps(dict(checkpoint=str(C/'CONTINUATION-2026-10-21-NATIVE-OWNER.json'),push=push,next=next_work[0]),indent=2))
