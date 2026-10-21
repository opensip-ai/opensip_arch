"""Freeze complete materialization only after the owning lane is terminal/pass.

This prepares a review subject; it grants no acceptance or integration.
"""
from pathlib import Path
import hashlib,json,shutil,subprocess

F=Path(__file__).parent
W=Path('/Users/sb/code/opensip-ai/opensip-native-owner-patterns-takeover')
P=W.parent/'opensip';A=W.parent/'opensip_arch'
S=F/'unit-r1/architecture'
PRE='docs/implementation/m3/native-publication/native-owner-patterns-materialization-r1'
D=S/PRE
Q=Path('/tmp/opensip-implementation/reviews/codex-native-owner-materialization-r1')

def git(root,*args):
    return subprocess.check_output(['/usr/bin/git','-C',str(root),*args],text=True).strip()
def pin(root,path):
    raw=(root/path).read_bytes()
    return dict(path=path,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
def write(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,indent=2)+'\n')
def copy(src,dst):
    dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)

checks=json.loads((F/'full-r4/report.json').read_text())
assert checks['allPassed'] and checks['sourcePinsUnchanged']
release=json.loads((F/'storage-release-boundary-r1/report.json').read_text())
assert release['allPassed'] and release['sourcePinsUnchanged']
assert checks['selectedGenerationInputsStillExact']==352
assert checks['selectedGeneratedOutputsStillExact']==8
assert git(P,'rev-parse','HEAD')==git(W,'rev-parse','HEAD')==checks['productBase']
assert not git(P,'status','--porcelain') and not git(A,'diff','--name-only','HEAD')
paths=sorted(git(W,'diff','--name-only').splitlines()+git(W,'ls-files','--others','--exclude-standard').splitlines())
assert len(paths)==42 and set(paths)==set(checks['sourcePins'])
for p in paths:assert pin(W,p)['sha256']==checks['sourcePins'][p]
mut=json.loads((F/'mutations-r1/report.json').read_text())
extra=json.loads((F/'companion-mutations-r1/report.json').read_text())
assert mut['allCaught'] and mut['allRestored'] and mut['restoredPositiveControlsPassed']
assert extra['all4Caught'] and extra['restored'] and extra['restoredPositiveControlsPassed']
for report in [mut,extra]:
    for p,h in report['originalPins'].items():assert pin(W,p)['sha256']==h
    assert all(not r['compileFailure'] and r['failedTests'] for r in report['mutations'])
pre=F/'companion-preflight-r1'
preq=Path('/tmp/opensip-implementation/reviews/codex-native-owner-companions-preflight-r1')
verdict=json.loads((preq/'review.json').read_text())
assert verdict['verdict']=='PREFLIGHT-CLEAR' and not verdict['requiredFindings']
assert verdict['subjectManifestSha256']==pin(pre,'subject-manifest.json')['sha256']
for row in json.loads((pre/'subject-manifest.json').read_text())['files']:assert pin(pre,row['path'])==row
assert not S.exists() and not Q.exists()
D.mkdir(parents=True)
rows=[]
for p in paths:
    copy(W/p,D/'product'/p)
    result=subprocess.run(['/usr/bin/git','-C',str(P),'show','HEAD:'+p],capture_output=True)
    parent=None
    if result.returncode==0:
        target=D/'parents'/p;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(result.stdout)
        parent=dict(path=p,bytes=len(result.stdout),sha256=hashlib.sha256(result.stdout).hexdigest())
    rows.append(dict(path=p,parent=parent,candidate=pin(W,p),archived=pin(S,PRE+'/product/'+p)))
assert sum(r['parent'] is None for r in rows)==15
write(D/'product-map.json',dict(rows=rows))
(D/'tracked-product.diff').write_bytes(subprocess.check_output(['/usr/bin/git','-C',str(W),'diff','--binary']))
# Preserve the exact independently reviewed companion construction and authorities.
for folder in ['authorities','evidence']:
    shutil.copytree(pre/folder,D/'source-preflight'/folder)
for n in ['product-map.json','source.json','subject-manifest.json']:
    copy(pre/n,D/'source-preflight'/n)
for n in ['REQUEST.md','subject.json','REVIEW.md','review.json']:
    copy(preq/n,D/'history/companion-preflight-r1'/n)
for n in ['PLAN-r3.md','PREFLIGHT-R3-LEAD-NOTE.json','COMPANION-PREFLIGHT-R1-LEAD-NOTE.json','generation-report-r3.json','generated-output-audit.json','generator-input-provisioning.json','typescript-input-provisioning.json','inventory-readiness.json','host-integration-consumer-correction.json']:
    copy(F/n,D/'evidence'/n)
for folder in ['full-r1','full-r2','full-r3','full-r4','host-format-r1','baseline-r1','registered-initial-r1','companion-focused-r1','companion-focused-r2','companion-focused-r3','companion-focused-r4','companion-focused-r5','mutations-r1','companion-mutations-r1','full-walk-all-cases-diagnostic-r1','storage-release-boundary-r1']:
    for p in sorted((F/folder).iterdir()):
        if p.is_file():copy(p,D/'evidence'/folder/p.name)
for p in sorted((F/'ecma-full-differential-r3').iterdir()):
    if p.is_file() and p.name!='probe':copy(p,D/'evidence/ecma-full-differential-r3'/p.name)
for p in sorted(F.glob('*.py')):copy(p,D/'runners'/p.name)
copy(F/'audit_generated_report.cjs',D/'runners/audit_generated_report.cjs')
authorities=[]
for folder in ['source-design-r1','generator-profile-design-r1','loader-policy-design-r1']:
    integration=json.loads((F/folder/'integration.json').read_text())
    for key in ['subjectManifest','record','review']:
        row=integration[key];assert pin(A,row['path'])==row
        copy(A/row['path'],D/'authorities'/row['path']);authorities.append(row)
    for n in ['integration.json','lead-assent.json']:
        copy(F/folder/n,D/'history'/folder/n)
for p in ['docs/implementation/m3/component-install/PLAN-r3.md','docs/implementation/m3/component-install/plan-r3-subject.json','docs/implementation/m3/component-install/ci2-inventory-v230-unit.json','docs/implementation/m3/component-install/ci-3l-takeover-r1-unit.json']:
    copy(A/p,D/'authorities'/p);authorities.append(pin(A,p))
lock=json.loads((P/'design-lock.json').read_text())
assert len(lock['contractSuccessors'])==181 and len(lock['inventorySuccessors'])==193
source=dict(productBase=git(P,'rev-parse','HEAD'),architectureBase=git(A,'rev-parse','HEAD'),productLock=pin(P,'design-lock.json'),selectedInventory=lock['inventorySuccessors'][-1]['candidate'],authorities=authorities,existingPaths=27,newPaths=[r['path'] for r in rows if r['parent'] is None],newDependencies=False,sourceCount=43,admissionSources=52,aliases=15,selectedNativeDocumentIds=3,patternForms=26,sourceDesignsBound=[179,180,181],blindRefreshComplete=False,productQualification=False,entireProjectComplete=False)
write(D/'source.json',source)
write(D/'checks-summary.json',dict(completeOwning=checks,storageReleaseBoundary=release,compiledMutants=14,originalMutants=mut,companionMutants=extra,finiteDifferential=json.loads((F/'ecma-full-differential-r3/report.json').read_text()),blindReceiptStanding=checks['blindReceiptStanding'],unitAccepted=False,productQualification=False))
write(D/'carried-obligations.json',dict(obligations=[
 dict(id='OWNPAT-INVENTORY',scope='After exact independently accepted code integration, add the 15 real new paths through additive inventory successor; all inherited rows by value, 113 inheritance records preserved.'),
 dict(id='OWNPAT-DESCRIPTIONS',scope='Qualify descriptions of the 15 physically retained predecessor .current fixture/metadata files through existing description contract passage mechanism, without rewriting inherited raw inventory rows.'),
 dict(id='OWNPAT-BLIND-REFRESH',scope='Immediately after own metadata binding and before D2b3c or other census-dependent consumption, obtain independent exact-main pre-run approval and runAuthorized for the unchanged reviewed blind tool/method/population/allowlist. One authorized blind run, ordinary write/check, only allowed summaries; independent post-run acceptance and root assent before receipt commit. On difference/error commit nothing, do not inspect private content or tune/retry.'),
 dict(id='PROJECT-QUALIFICATION',scope='This unit supplies no new real worker/compiler/semantic source registration, installation/signing/custody/privacy/H-C4/Linux qualification or D4/CI4/project closure. Existing ignored and deferred controls remain scoped obligations.')]))
(D/'SCOPE.md').write_text('''# Native-owner complete materialization unit r1

Complete 42-path candidate over actually accepted/bound source designs179,180,181: 27 existing paths and 15 new public synthetic companions/metadata files. No dependency, entrypoint, source set, alias, package owner or parser limit is added. Three resolved document identities delimit the closed26-form pattern keyword profile; full52-source raw length/hash/$id guards stay exact. Foreign references and patternProperties retain inherited semantics. Corrected complete-input paths, occupancy exact segments and grant newline atoms match the selected ECMA-u owner semantics. Unknown native forms fail closed.

Ordinary selected offline generation and zero-drift check pass on43sources/eight outputs. Only report.ts changes: exact helpers, selected raw native document and closure/registry provenance; all other report bytes and seven outputs are exact. Actual generated registry checks73controls/886entrypoints. The exact accepted loader policy updates three source pins and no authority/callsite; TypeScript owning lanes must pass the final complete lane. Finite Rust/Node controls compare3,100,500native cases and8,586,000inherited cases with zero differences; these finite controls do not prove qualification.

Fifteen fresh companions preserve every predecessor physically. Eleven host corpora, one evaluator cycle, one exact23-object/46-blob security subset and two runtime registry companions use current selected schema documents and rebuilt dependent identities. Ten fixture/include readers select these companions; runtime metadata changes only three native digest occurrences. Independent inverse correspondence covers9,127object and4,580blob occurrences, preserving deliberate invalidity and opaque bytes. 116indexed native selections map exactly. Carrier ordering follows the published canonical/encounter laws.

Exactly12single semantic mutation requests retain14already-existing base facts selected by unchanged observation matchingFactIds; allother514request selections remain exact. Intended mutants remain reachable. Exactly two current negative outcomes change unavailable to invalid because newly bound identity ordering reaches a source-derived refusal earlier: unchanged malformed FilePayloadV1 requires exact typed schema mismatch; foreign-view/missing-child requires exact typed REFERENCE_PLAN_JOIN. All other524verdicts remain equal. The earlier arbitrary foreign-FACT proposal is rejected/restored, never selected. No success population is enlarged. Original source assertions are restored after diagnostic aggregation; final526-case fullwalk runs original assertions plus these stronger typed checks.

Initial failed candidate lane and unchanged-main baseline remain preserved. The33storage baseline failures and old generator-policy mismatch are evidence of prior state, not waivers. The final host integration reader also selects the rebuilt replay corpus. The source manifest guard adds only lifecycle's already accepted CI PLAN-r3 LD-CIP-3 fixture forwards; default/dependency routes stay rejected. R2 completes every owning check with only three host integration failures. R3 reruns full host and all-target Clippy after the one test-only path correction; all41prior paths remain exact and the other R2 checks carry explicit evidence correspondence. R3 passes all tests and checks but records formatting drift in two host test files; R4 runs full host and Clippy again after exact rustfmt-only correction, with allother40paths byte-exact. Final complete owning composition, Clippy/workspace/features, all TypeScript lanes, environment/source/package/design and clean-base formatting classification must pass on exact42pins. Fourteen fresh compiled runtime/provenance regressions fail intended controls and restore exact source pins; compile failures are not counted as catches. Independent source preflight is clear but not this unit's acceptance.

Complete code-unit review and substantive root assent must precede exact integration. Own additive inventory and retained-predecessor description qualification remain required. Blind receipt is explicitly STALE/PENDING until independently reviewed exact-main pre-run gate, one authorized refresh and accepted post-run evidence; no census-dependent continuation occurs before that. No actual heldout/private/key/installation content is inspected here. No current blind margin, product/platform qualification or project completion follows from this unit.
''')
manifest=PRE+'-subject.json'
write(S/manifest,dict(schemaVersion=1,unit='NATIVE-OWNER-MATERIALIZATION-r1',files=[pin(S,str(p.relative_to(S))) for p in sorted(S.rglob('*')) if p.is_file()]))
Q.mkdir(parents=True)
subject=dict(unit='NATIVE-OWNER-MATERIALIZATION-r1',architectureStage=str(S),subjectManifest=pin(S,manifest),productBase=source['productBase'],architectureBase=source['architectureBase'])
write(Q/'subject.json',subject)
(Q/'REQUEST.md').write_text(f'''# Complete native-owner materialization unit review r1

Read subject.json, frozen architecture stage {S} and its complete manifest SHA256 {subject['subjectManifest']['sha256']}. Rehash every member and exact42-row product-map (27parents/15new), verify live pinned bases and actually bound designs179/180/181. This requests complete ACCEPT-UNIT, not another source preflight. Judge the accepted PLAN-r3 sequence and all earlier source findings; no guard weakening, extra source/alias/entrypoint, dependency or semantic source registration. Check closed3resolved-document/26-form scope, foreign/reference/patternProperties isolation and strict full52source construction. Check all selected source/map/recipe/compiled/provenance joins and generated eight-output audit, ordinary generation+zero drift, actual report73controls/886entrypoints and all three final TypeScript lanes under bound181.

Judge complete final owning/check evidence and14compiled mutants/restoration, preserving earlier failures and actual baseline distinctions. Validate every public synthetic identity/canonical/opaque correspondence, malformed status and indexed selection. Specifically scrutinize12single semantic mutant requests retaining14existing base facts; all514others exact, mutants remain selected. Exactlytwo expected negative outcomes change through documented FILEschema/foreignVIEWcurrent refusal precedence and require exact typed assertions; allother524verdicts equal. Earlier arbitrary foreign-FACT change is rejected/restored. Existing original/current files remain byte-exact, final fullwalk original assertions restored. No test adaptation is accepted merely because totals pass. Source-preflight findings are empty and root assent remains preflight-only until this review. New runtime metadata changes only3native SHA occurrences. Debug/test storage helpers select the exact flat current security subset with production admission unchanged. The additional host integration test reader selects this same rebuilt replay corpus. Its manifest guard explicitly adds only lifecycle as already permitted by accepted CI PLAN-r3 LD-CIP-3, preserving all default/dependency rejection checks. Source preflight covered the preceding41-path image; final owning R3 reruns host and Clippy after this42nd test-only path, with every41prior path byte-exact and all other complete R2 checks retained under explicit correspondence. Then R4 reruns full host/Clippy after rustfmt-only changes to native_owner_tests.rs and admission_tests.rs; allother40paths remain exact. R3 test passes are preserved alongside its formatting refusal, and final R4 formatting classification must pass. No claim that a preflight approved the later path is made.

Review own mandatory15path additive inventory plus retained-predecessor descriptive qualifications as carried obligations after exact code integration. Blind receipt remains STALE/PENDING: independently reviewed exact-main pre-run gate/one authorized run/post-run review+assent remain mandatory before census-dependent consumption. No private413/heldout/T2/key/installation content or blind mode is used here. No unit review itself establishes integration, inventory, current blind margin, D4/CI4 or whole-project qualification.

Read-only hashes/JSON/Git/source queries only. No builds/tests/Cargo/generation/lanes/network/panes/delegation or repository/worktree/stage/control/evidence edits. Write ONLY REVIEW.md and review.json in {Q}. JSON verdict ACCEPT-UNIT or REQUIRED-FINDINGS; subjectManifestSha256; requiredFindings; nonBlockingObservations; blindRefreshComplete:false; productQualification:false. Finding IDs OWNPAT-UNIT-R1-RF-n/NBO-n.
''')
print(json.dumps(subject,indent=2))
