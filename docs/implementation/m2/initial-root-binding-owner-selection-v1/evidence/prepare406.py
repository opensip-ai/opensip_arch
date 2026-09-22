"""Prepare mutable formal integration candidate; do not freeze or select."""
from pathlib import Path
import json,hashlib,shutil,subprocess
A=Path('/Users/sb/code/opensip-ai/opensip_arch');M=A/'docs/implementation/m2';T=Path('/tmp/opensip-implementation');D=M/'initial-root-binding-owner-selection-v1';G=T/'initial-diagnostics-generation404';P=G/'product';L=A.parent/'opensip';O=T/'initial-root-binding402';assert not D.exists()
def dig(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def save(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
def copy(src,dst):dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(src.read_bytes())
assert subprocess.check_output(['git','status','--porcelain'],cwd=L)==b''
assert json.loads((G/'compile-result.json').read_text())['exitCode']==0
D.mkdir();copy(O/'owner-draft.md',D/'owner.md');copy(O/'diagnostic-draft/common.schema.json',D/'schemas/common.v4.schema.json');copy(O/'diagnostic-draft/workflows_model.v1.py',D/'reference/workflows_model.v1.py')
r=json.loads((O/'diagnostic-draft/public-detail-registry.json').read_text())
r['standing']='Proposed current closed public domain-detail registry for initial-root binding; existing D9 class/code/exit unchanged. Historical correction fields retain their original provenance and do not enumerate this successor.'
r['initialRootBindingCorrection']={'codes':['INSTALLATION.DURABILITY_NOT_CHECKED','INSTALLATION.NOT_INITIALIZED'],'owner':'docs/implementation/m2/initial-root-binding-owner-selection-v1/owner.md','historicalMetadata':'newInThisCorrection and scopeBindingDetailsRegistered describe inherited earlier corrections, not this successor.','activation':'Current common4, generation/admission maps and generated bindings must be selected together before emission; no native emission is enabled by this unit.'}
for row in r['records']:
 if row['code']=='INSTALLATION.DURABILITY_NOT_CHECKED':row['selector']='docs/implementation/m2/initial-root-binding-owner-selection-v1/owner.md section5; doctor complete-root informational notice excluded from defectsFound'
 if row['code']=='INSTALLATION.NOT_INITIALIZED':row['selector']='docs/implementation/m2/initial-root-binding-owner-selection-v1/owner.md section6; noncreator authoritative-root absence'
save(D/'reference/public-detail-registry.json',r)
# Admission-only references are a separate selected registry and source map.
common={'path':str((D/'schemas/common.v4.schema.json').relative_to(A)),**dig((D/'schemas/common.v4.schema.json').read_bytes())}
ar=json.loads((P/'schemas/admission-registry.json').read_text());found=0
for row in ar['sources']:
 if row['sourcePath']=='schemas/sources/common-v4.schema.json':row.update(dig((D/'schemas/common.v4.schema.json').read_bytes()));found+=1
assert found==1
assert not any(x['sourcePath']=='schemas/sources/common-v4.schema.json'for x in ar['aliases'])
save(D/'schemas/admission-registry.json',ar);save(P/'schemas/admission-registry.json',ar)
am=json.loads((P/'schemas/admission-source-map.json').read_text());found=0
for row in am['sources']:
 if row['implementationPath']=='schemas/sources/common-v4.schema.json':row['architectureSource']=common;found+=1
assert found==1
am['registryArchitectureSource']={'path':str((D/'schemas/admission-registry.json').relative_to(A)),**dig((D/'schemas/admission-registry.json').read_bytes())};save(P/'schemas/admission-source-map.json',am)
# These two maps are not in the generator closure: changing them does not invalidate404 output provenance.
closure=json.loads((P/'tools/contracts/generator-closure.json').read_text());assert not {'schemas/admission-registry.json','schemas/admission-source-map.json'}&{x['path']for x in closure['files']}
for row in closure['files']:assert dig((P/row['path']).read_bytes())=={k:row[k]for k in ('bytes','sha256')}
base=json.loads((G/'baseline.json').read_text());mapping=[];unchanged=[]
for row in base['files']:
 assert dig((L/row['path']).read_bytes())=={k:row[k]for k in ('bytes','sha256')}
 raw=(P/row['path']).read_bytes()
 if dig(raw)!={k:row[k]for k in ('bytes','sha256')}:
  assert row['path']!='design-lock.json'
  target=D/'product'/row['path'];copy(P/row['path'],target)
  mapping.append({'productPath':row['path'],'candidatePath':str(target.relative_to(A)),'before':{k:row[k]for k in ('bytes','sha256')},'after':dig(raw)})
 elif row['path']!='design-lock.json':unchanged.append(row)
save(D/'baseline.json',base);save(D/'materialization-map.json',{'schemaVersion':1,'standing':'Mutable proposal; root selection and fresh private/live validation still required. No selected product changes.','baseProductHead':base['productHead'],'files':mapping,'unchanged':unchanged})
plan=json.loads((M/'initial-root-binding-reconciliation/passage-plan.json').read_text());plan['standing']='Mutable formal integration proposal; no freeze, review, assent or selection yet.';plan['ownerCandidateSubject']='docs/implementation/m2/trials/initial-root-binding-proposal-402/subject.json'
for row in plan['passageOverrides']:row['after']=row['after'].replace(' | \n',' |\n')
save(D/'effective-owner-overrides.json',plan)
for name in ['preparation.json','ignored-generator-dependencies.json','output-materialization.json','compile-result.json','compile-environment.json','pipeline.stderr','pipeline-r2.stdout','pipeline-r2.stderr','workspace.stdout','workspace.stderr']:
 copy(G/name,D/'evidence'/name)
copy(G/'generation/result.json',D/'evidence/generation404-result.json');copy(T/'generation-closure-audit/rebuild-preconditions.json',D/'evidence/rebuild403-preconditions.json');copy(T/'contracts-generator-rebuild-403/receipt.json',D/'evidence/rebuild403-receipt.json')
copy(Path(__file__),D/'evidence/prepare406.py')
(D/'README.md').write_text('''# Initial installation, binding and diagnostic contract integration

MUTABLE FORMAL CANDIDATE. Not frozen, reviewed, selected or a product implementation approval.

The owner.md body is byte-identical to owner402's inherited owner401 body. Its historical heading and evidence statements retain provenance. This unit proposes explicit passage reconciliation, current schema/registry/source-map replacement, the doctor count helper and generated artifacts together. The native creator, actual account/core/profile/custody admission, act-wide budget composition, P0 construction and current authority remain implementation obligations.

The current development common4 schema retains its unreleased ID and all317 existing enum positions, adding exactly two domain-detail codes. It is an explicit selected-source replacement, not compatibility with old closed-enum decoders. Historical common1/common3 and historical architecture common4 bytes are preserved. No envelope fields, record identity or signature domain changes. Both generation and admission-only source maps must bind the new common4 bytes; the historical common1 logical-document alias remains common1.

Private prospective generation404 ran all40 sources and857 entry points, produced8 artifacts (only Rust evidence.rs and report.ts differ), and passed a fresh workspace all-targets compilation. The349-file closure has five explicitly pinned replacements, including correction of the already-stale design checker hash. The generator was rebuilt offline from identical sources/dependencies/compiler/builder; its new executable hash is an observed development pin, not a reproducible-build claim. The live product is unchanged. The initial preparation missed ignored generator dependencies and stopped; a follow-up copied exact pinned bytes. The first wrapper used a wrong registry path and stopped before pipeline entry; corrected wrapper passed. Evidence retains these limits and failures.

The admission registry/source map changes follow generation404 and are outside its349-file closure. Reverification confirms the generated input pins remain unchanged. Product activation requires actual independent review, root substantive assent, private selection checks and fresh public-entry-point drift verification. Merely supplying a matching local hash never grants source selection.

Doctor checker/vectors/rendering reconciliation and the formal subject/successor are still being prepared; do not treat this working directory as a complete formal unit. No production doctor assembler or renderer is claimed by a reference projection test.
''')
print(json.dumps({'mutableCandidate':str(D),'mappedFiles':len(mapping),'unchangedNonLockFiles':len(unchanged),'mappedPaths':[r['productPath']for r in mapping]},indent=2))
