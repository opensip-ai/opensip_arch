from pathlib import Path
import json,hashlib,importlib.util,subprocess
A=Path('/Users/sb/code/opensip-ai/opensip_arch');M=A/'docs/implementation/m2';U=M/'initial-root-binding-owner-selection-v1';T=Path('/tmp/opensip-implementation');P=A.parent/'opensip';G=T/'initial-diagnostics-generation404';subject=M/'initial-root-binding-owner-selection-v1-subject.json'
assert not subject.exists()and not (U/'successor.json').exists()
def dig(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def pin(p):return {'path':str(p.relative_to(A)),**dig(p.read_bytes())}
def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
assert subprocess.check_output(['git','status','--porcelain'],cwd=P)==b''
lock=json.loads((P/'design-lock.json').read_text());accepted={}
for key in ('sourceManifest','applicationManifest'):
 accepted.update({r['path']:r for r in json.loads((A/lock['approvals'][key]['path']).read_text())['files']})
for b in lock['inventorySuccessors']:accepted[b['candidate']['path']]=b['candidate']
previous=[]
for b in lock['contractSuccessors']:
 record=json.loads((A/b['record']['path']).read_text());accepted[b['record']['path']]=b['record'];accepted.update({r['path']:r for r in record['candidates']});previous.extend(record['passageOverrides'])
plan=json.loads((U/'effective-owner-overrides.json').read_text());overrides=plan['passageOverrides'];assert len(overrides)==12
parents={r['parent']['path']:r['parent'] for r in overrides}
for row in json.loads((U/'reference/input-pins.json').read_text())['inputs']:
 if not row['path'].startswith(str(U.relative_to(A))+'/'):parents[row['path']]={k:row[k]for k in ('path','bytes','sha256')}
for name in ['native-runtime-selection-v34/successor.json','project-registry-owner-selection-v2/successor.json','import-totality-reference-selection-v1/successor.json','admission-runtime-selection-v1/schemas/admission-registry.json']:
 p=M/name;parents[str(p.relative_to(A))]=pin(p)
for rel in ['docs/implementation/m1/generator-selection-v2/successor.json','docs/implementation/m1/source-selection-v2/reference/composed-owners/public-detail-registry.proposed.json']:
 parents[rel]=pin(A/rel)
for path,row in parents.items():assert accepted.get(path) is not None and all(accepted[path].get(k)==row[k] for k in ('path','bytes','sha256')),(path,'not exact accepted parent');assert pin(A/path)==row
spec=importlib.util.spec_from_file_location('frozen_owner406_verifier',P/'tools/verify_design.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
oldkeys={(r['parent']['path'],json.dumps(r['selector'],sort_keys=True))for r in previous}
for row in overrides:
 assert v.selected_passage((A/row['parent']['path']).read_bytes(),row['selector'])==row['before'];assert (row['parent']['path'],json.dumps(row['selector'],sort_keys=True))not in oldkeys
# Direct final-inventory override adds a fifth effective description. It does not
# add an inherited row: the existing four lock inheritance rows remain exact.
assert len(lock['inventoryPassageInheritance'])==4
save(U/'evidence/parent-and-passage-verification.json',{'passed':True,'parents':len(parents),'overrides':12,'conflictsWithSelectedOverrides':0,'existingInventoryInheritanceRows':4,'newDirectFinalInventoryOverrides':1,'effectiveInventoryDescriptionsAfterSelection':5,'actualProductHead':subprocess.check_output(['git','rev-parse','HEAD'],cwd=P,text=True).strip(),'sourceApprovalGranted':False})
(U/'evidence/doctor-reference-final-result.json').write_bytes((T/'doctor-reference406-final-result.json').read_bytes())
save(U/'evidence/private-stage.json',{'passed':True,'mapped':12,'unchangedNonLock':579,'trackedFiles':592,'selected':False,'liveProductModified':False,'stageOutput':'/tmp/opensip-implementation/initial-owner406-author-stage','validation':'Every final non-lock staged byte was compared with candidate product below.'})
base=json.loads((U/'baseline.json').read_text());staged=T/'initial-owner406-author-stage'
for r in base['files']:
 if r['path']!='design-lock.json':assert(staged/r['path']).read_bytes()==(G/'product'/r['path']).read_bytes()
origin=M/'trials/initial-root-binding-proposal-402';save(U/'owner-origin.json',{'ownerSource':'owner-draft.md inside archive','ownerBytesIdentical':True,'owner':pin(U/'owner.md'),'frozenArchive':pin(origin/'subject.tar.xz'),'frozenManifest':pin(origin/'subject.json'),'actualReview':pin(M/'reviews/claude-opus5-owner402-20260921-r1/findings.json'),'rootAssessment':pin(M/'reviews/claude-opus5-owner402-20260921-r1/root-assessment.md'),'standing':'Provenance of independently reviewed owner body; this complete formal unit and new native/schema changes require their own review. Historical headings/evidence limits in owner.md are retained.'})
assert (U/'owner.md').read_bytes()==(T/'initial-root-binding402/owner-draft.md').read_bytes()
plan['standing']='Frozen proposed formal passage reconciliation; actual independent review and root assent required before selection.';save(U/'effective-owner-overrides.json',plan)
(U/'README.md').write_text('''# Initial installation, binding and diagnostic contract integration

Frozen proposed formal owner/source/reference successor. No independent review or root selection of this complete unit is claimed. The live product remains883f963,35 inventory/54 contract successors; intended selected chain is35/55.

## Change and source boundaries

owner.md is byte-identical to the body independently accepted through owner402. Its historical proposal401 heading/evidence captions retain provenance; owner-origin.json records exact frozen source/review/assessment. This unit explicitly reconciles12 selected passages for creator delegation, account-derived installation location/disclosure/backup choice, directory durability, endpoint-versus-intermediate lineage, doctor semantics and inventory. Other transition/restore/215/fullS9.3 proposals remain unselected. Four inherited inventory description rows remain unchanged; the new direct final-inventory row104 override yields five effective descriptions without fabricating a fifth inheritance row.

The current unreleased common4 schema retains its ID and317 original enum positions, appending exactly INSTALLATION.DURABILITY_NOT_CHECKED and INSTALLATION.NOT_INITIALIZED. This is an explicit selected-source replacement, not compatibility with old closed-enum decoders. Historical common1/common3 and architecture common4 bytes remain intact. Both generation and admission maps bind the new common4; admission-registry and its source-map registry pin move together. The historical common1 logical alias remains unchanged. Native RegisteredSchemas has a separate compiled length/digest pin: that exact common4 pin is also updated, with a regression covering native schema and generated enum admission/current-versus-historical rejection. No runtime rehash bypass is introduced.

## Reference reconciliation

The workflow successor extends the latest selected import-totality reference, preserving116other top-level statements. doctor computes one actual-defect count excluding only the reserved informational code. terminate's false doctor-report branch adds the pre-existing DOCTOR.REPORT_NOT_PRODUCIBLE detail promised by the selected inventory golden/projection checker; every other terminate AST node is unchanged. This closes an older model/golden mismatch, not new owner law. The helper never appends a notice blindly: reference/doctor_projection.py conditionally assembles complete-root inputs and calls the actual helper/render AST. It is a trusted-premise reference, not native observation or a product renderer.

reference/check_doctor.py and doctor-cases.json are the scoped current replacements for doctor assertions/vectors and the projection-checker golden join. They bind48 dependencies:40 generation schemas plus8 reference inputs. This set differs from the48 admission-registry schemas. Eight doctor cases cover healthy/mixed,255actual+info capacity,256complete overflow/latch, historical two-defect no-note,256partial capacity,257partial overflow and unproducible reports. Five malformed envelope variants refuse. Exact human label/code/remedy/count/list and JSON/agent projections agree. Absence and backup refusals validate in current envelopes. Trustdoctor/storestatus checks preserve their existing field sets without a new diagnostic channel; their synthetic projections are explicitly not native/schema-valid reports. No no-fence internal recovery algorithm changes.

The historical checker/vector/projection files are retained at new reference/historical-source paths for provenance only. They are not current executable entrypoints or a wholesale requalification. Their live newer bytes match the historically reviewed sourceManifest, while overlapping applicationManifest rows win in verify_design's effective accepted-parent map. reference/reconciliation.json records both. This unit does not falsely name mismatching old paths as accepted parents or rewrite the approval chain. Current focused checks use the latest model and current schemas instead of freezing the stale coop model.

## Generation, runtime and staging evidence

Private prospective generation404 passed40schemas857entrypoints8outputs68native types. Exact diff admits only Common4 Rust enum/Display/FromStr additions; the TS current alias and embedded common4 source plus two provenance comments change. All Common1/Common3 and unrelated generated bytes stay unchanged. Both generated TS files typecheck;11checks execute the actual generated TS shape registry, admitting new codes only in common4 and rejecting unknown codes/boolean count.

The349-file generator closure has five explicit replacements, including repair of a stale design-checker pin already present in foundation. The same-source/dependency/compiler/builder generator rebuilt403 offline, with a new observed executable digest; no reproducible-build claim. No public preflight was weakened or bypassed for activation. The private pipeline is explicitly unapproved development generation until this full unit is accepted. Before selection, fresh public-entry-point drift checking remains mandatory using the newly accepted unit.

Original failures remain in evidence: preparation initially omitted ignored pinned generator dependencies and stopped before generation; exact-pin copy completion fixed it. The first wrapper used a wrong registry path and stopped before pipeline entry; corrected wrapper passed. The first native admission run correctly refused22of23 tests with SourceBytes because the Rust SourcePin still named oldcommon4. After exact pin correction and one meaningful regression,24admission tests pass (45filtered), and fresh all-targets workspace compilation passes. Rust compilation before that failure was insufficient runtime evidence and is not presented as admission success.

Twelve existing product files change;579other non-lock files remain exact,592tracked total. stage.py checks the complete baseline and every mapped/unchanged pin before creating a fresh private tree. It leaves the inherited lock unchanged and claims no approval. The author staged and compared every non-lock output; actual independent review, root substantive assent, accepted lock/private validation, public generator drift and live checks remain necessary before materialization.

## Limits

Development macOS arm64 only. No native initial creator, account/core/profile/custody qualification, completeP0 builder, act-wide shared budget, current authority, native doctor assembly/rendering or write route is enabled here. All five disclosed native composition gaps remain. Directory publication/barrier primitives are already accepted in source400/runtime34; this unit does not rerun their qualification. Linux/crash/power-loss/release and wholeM2–M6 remain open. No commits or pushes are authorized to the independent reviewer; root may commit local checkpoints, never push.
''')
(U/'evidence/freeze406.py').write_bytes(Path(__file__).read_bytes())
files=sorted(p for p in U.rglob('*')if p.is_file());assert not any('__pycache__'in p.parts for p in files)
candidates=[pin(p)for p in files];save(U/'successor.json',{'schemaVersion':1,'standing':'PROPOSED complete initial-root owner and diagnostic schema/reference/native-pin/generation integration; exact frozen candidate requires actual substantive review and root assent.','parents':[parents[k]for k in sorted(parents)],'passageOverrides':overrides,'candidates':candidates})
save(subject,{'schemaVersion':1,'files':sorted([*candidates,pin(U/'successor.json')],key=lambda r:r['path'])})
for row in json.loads(subject.read_text())['files']:assert pin(A/row['path'])==row
print(json.dumps({'subject':pin(subject),'members':len(candidates)+1,'parents':len(parents),'overrides':12,'candidateProductFiles':12,'unchangedNonLock':579},indent=2))
