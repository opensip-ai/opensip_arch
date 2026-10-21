from pathlib import Path
import json,hashlib,copy,shutil,subprocess
F=Path(__file__).parent;B=F/'generator-profile-design-r1';S=B/'architecture';P=Path('/Users/sb/code/opensip-ai/opensip');A=P.parent/'opensip_arch'
PRE='docs/implementation/m3/native-publication/native-owner-generator-profile-r1';SP='docs/implementation/m3/native-publication/native-owner-patterns-source-r1'
Q=Path('/tmp/opensip-implementation/reviews/codex-native-owner-generator-profile-r1');assert not Q.exists()
def pin(root,path):
 raw=(root/path).read_bytes();return dict(path=path,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
def write(path,data):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(data,indent=2)+'\n')
def git(root,*args):return subprocess.check_output(['/usr/bin/git','-C',str(root),*args],text=True).strip()
prepared=json.loads((B/'prepared-initial.json').read_text());assert git(P,'rev-parse','HEAD')==prepared['productBase'] and git(A,'rev-parse','HEAD')==prepared['architectureBase']
report=json.loads((B/'controls-report.json').read_text());assert report['nativeComparisons']==3100500 and report['inheritedComparisons']==8347500 and report['realSelectedEntrypointsChecked']==886
parents=[pin(A,SP+'/product/tools/contracts/generator-closure.json'),pin(A,SP+'/product/schemas/registry.json'),pin(A,'docs/implementation/m1/source-selection-v2/owners/native/owner-pattern-successor.v1.json')]
L=json.loads((P/'design-lock.json').read_text());accepted={r['path']:r for r in L['inputs']}
for binding in L['contractSuccessors']:
 for row in json.loads((A/binding['record']['path']).read_text())['candidates']:accepted[row['path']]=row
assert all(accepted[r['path']]==r for r in parents)
oldclosure=json.loads((A/SP/'product/tools/contracts/generator-closure.json').read_text());newclosure=json.loads((S/PRE/'product/tools/contracts/generator-closure.json').read_text())
changed=[dict(before=a,after=b) for a,b in zip(oldclosure['files'],newclosure['files']) if a!=b];assert len(changed)==2
assert len(newclosure['files'])==len(oldclosure['files'])==352
assert all(a==b for a,b in zip(oldclosure['files'],newclosure['files']) if a['path'].startswith('tools/contracts/python-packages/'))
oldregistry=json.loads((A/SP/'product/schemas/registry.json').read_text());newregistry=json.loads((S/PRE/'product/schemas/registry.json').read_text());normalized=copy.deepcopy(newregistry);normalized['recipes'][0]['generatorClosureSha256']=oldregistry['recipes'][0]['generatorClosureSha256'];assert normalized==oldregistry
productmap=[dict(productPath=p,candidate=pin(S,PRE+'/product/'+p)) for p in prepared['helperPaths']+['tools/contracts/generator-closure.json','schemas/registry.json']]
audit=dict(standing='PROPOSED EXACT GENERATOR HELPER/PROFILE SELECTION; NO GENERATION OR COMPLETE PRODUCT UNIT ACCEPTANCE',productBase=prepared['productBase'],architectureBase=prepared['architectureBase'],helperProductMap=productmap,
 closedDocumentIds=json.loads((B/'profile-nodes.json').read_text())['owners'],nativeForms=26,nativePatternNodes=137,inheritedTypeScriptForms=70,inheritedRustFormsSeparately=72,
 newlyRecognizedNativeOnlyForms=report['newForms'],closureRows=352,closureChangedRows=changed,pythonPackageClosureRowsUnchanged=True,toolchainUnchanged=True,
 registryChangeOnlyGeneratorClosureSha256=True,sourceSchemasUnchangedFromAccepted179=True,sourceMapUnchangedFromAccepted179=True,admissionMapUnchangedFromAccepted179=True,
 noSourceSetNamespaceOwnerRootOutputPathChanges=True,generatorSources=43,admissionSources=52,aliases=15,realSelectedGeneratorEntryPoints=886,
 exactInterpreterScope='pattern keyword only; three closed resolved target document identities; foreign targets and patternProperties retain inherited table; admission before cache lookup; cache by translated admitted expression',
 boundedAuthoringControls={k:report[k] for k in ('registryControls','nativeComparisons','inheritedComparisons','realSourceDocuments','realSelectedEntrypointsChecked')},
 generatorFailure='Exact accepted source closure admitted; prepare succeeded; validate refused corrected patterns outside inherited selected table. No product generated outputs were written.',
 candidateGenerationRequiresThisRealAcceptedBinding=True,materializationCodeAccepted=False,derivedOutputsAccepted=False,blindRefreshComplete=False,mandatoryImmediateReviewedBlindRefreshAfterCodeIntegration=True,productQualification=False)
write(S/PRE/'audit.json',audit)
(S/PRE/'README.md').write_text('''# Native-owner generator profile r1

Proposed helper-source design selection. Independent ACCEPT-DESIGN-UNIT, root assent, immutable publication and real product-lock binding are required before selected generation uses these bytes. This does not accept the complete materialization, derived outputs, a current blind margin or qualification.

Contract179 selects the35current native-owner source corrections. On the isolated candidate the ordinary selected entrypoint admitted the real design and all352closure rows, prepared inputs, then refused the corrected pattern at runtime vocabulary validation. No generated product output was written. This successor selects exactly two helper files plus the full prospective generator closure and registry: runtime/patterns.ts and runtime/schema.ts. All70inherited TypeScript map rows remain byte-equal. A separate closed26-form native keyword table recognizes the actual137nodes across exactly3document IDs; it returns the raw selected ECMA-u expression, including occupancy's exact end semantics and the security grant's unescaped wildcard dots. Four forms were absent from the inherited TypeScript table (the2corrected relative paths and2C0/DEL/C1 text forms); they are recognized only in the selected native keyword scope. The Rust inherited table has72forms and is separate.

Only `pattern` compilation/evaluation passes the actual resolved document ID. Existing reference resolution carries that ID through both directions. `patternProperties` retains the inherited table; an unknown native keyword fails closed even if the inherited table recognizes it. No public owner/profile flag, entrypoint, source-set bypass or source authority is added. RegExp cache keys are admitted translated expressions; admission occurs before lookup so cache order cannot leak foreign/native semantics or admit an unknown form. The generic inert interpreter remains inert; the generator's parent verifies the exact full input/architecture closure before the child runs.

Of352closure rows only these2helper rows change against contract179. AllPython-package rows, tools, options, source schemas/maps/sets, source/admission registries except the generator closure digest, namespaces, owners, roots and8declared output paths are unchanged. The registry changes only its one recipe closure digest. The helpers are included in generated report code by the unchanged renderer, so complete materialization review must inspect all actual generated output changes and report-runtime behavior; this source selection does not substitute for that review.

Bounded authoring evidence includes141synthetic registry checks,3,100,500native comparisons against the independently established Rust/Node corpus,8,347,500comparisons preserving the70inherited TypeScript forms, and runtime entrypoint closure checking on43actualdocuments/886entrypoints. These controls do not invoke the selected generator, write product outputs or establish full owning/confinement/qualification success. Earlier authoring-harness errors and generation refusals are preserved. All complete code-unit owning/registered-consumer/mutation/provenance/Clippy/feature/source/package/environment/design checks remain owed.

After complete materialization independent acceptance/root assent/exact integration, immediately complete the standing B2-b4c3 exact-main pre-run review, one unchanged-method/population/allowlist blind run on a clean detached checkout, ordinarywrite/check and independent post-run review/root assent before receipt commit. No census-dependent lane or D2b3c consumes changed reference bindings before that sequence. On changed rows/errors commit nothing, peek/tune/retry nothing and report through the existing owner protocol. The original owner decisions, privacy/production gates, H/C4semantic duties and every remaining project/qualification requirement remain unchanged.
''')
candidates=[pin(S,str(p.relative_to(S))) for p in sorted((S/PRE).rglob('*')) if p.is_file()]
record_path=PRE+'/successor.json';write(S/record_path,dict(schemaVersion=1,standing='PROPOSED exact helper/profile source selection only; complete materialization and qualification separate',parents=sorted(parents,key=lambda r:r['path']),candidates=candidates,passageOverrides=[]))
manifest_path=PRE+'-subject.json';write(S/manifest_path,dict(schemaVersion=1,unit='NATIVE-OWNER-GENERATOR-PROFILE-r1',files=sorted(candidates+[pin(S,record_path)],key=lambda r:r['path'])))
E=B/'evidence';E.mkdir()
evidence_files=[(F/'generator_profile_controls.cjs','controls.cjs'),(F/'prepare_generator_profile.py','prepare.py'),(B/'controls-report.json','controls-report.json'),(B/'profile-nodes.json','profile-nodes.json'),(F/'ecma-full-differential-r3/inputs.json','inputs.json'),(F/'ecma-full-differential-r3/matrix.bin','matrix.bin'),(F/'ecma-full-differential-r3/report.json','rust-node-differential-report.json'),(F/'generation-r2/validate.stderr','selected-generation-validate.stderr'),(F/'generation-r2.log','selected-generation.log'),(F/'generation-report-r2.json','selected-generation-report.json')]
evidence_files += [(p,p.name) for p in sorted(F.glob('generator-profile-controls*-lane.log'))]
evidence_files += [(P/'tools/contracts/runtime'/name,'baseline/'+name) for name in ('exact-json.ts','patterns.ts','schema.ts')]
for src,rel in evidence_files:
 dst=E/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
write(B/'evidence-manifest.json',dict(files=[pin(B,str(p.relative_to(B))) for p in sorted(E.rglob('*')) if p.is_file()]))
prepared.update(unit='NATIVE-OWNER-GENERATOR-PROFILE-r1',subjectManifest=pin(S,manifest_path),record=pin(S,record_path),parents=parents,evidenceManifest=pin(B,'evidence-manifest.json'),members=len(candidates)+1,materializationCodeAccepted=False,generatorRun=False,blindRefreshComplete=False,productQualification=False)
write(B/'prepared.json',prepared)
Q.mkdir();write(Q/'subject.json',prepared)
request=f'''# Native-owner generator helper/profile source selection r1

Read subject.json, frozen design stage {S}, and {B}/evidence-manifest.json. Rehash all{prepared['members']}design members and frozen evidence pins. Design manifest SHA256 {prepared['subjectManifest']['sha256']}. Verify the3parents are selected exact accepted current inputs, product base{prepared['productBase']}, architecture base{prepared['architectureBase']}; these bases remain unchanged. Judge this source-helper design independently from contract179 and source-preflightR3.

Contract179 selected35corrected native/relation source patterns, source/admission joins and prospective closure. The isolated ordinary selected generator actually admitted that exact real design/full352inputs and prepared, then validate refused corrected patterns outside its inherited table. Read preserved refusal; no product output writes. This new pure source design selects exactly2TSruntime helpers, full prospective closure and registry, audit/README. No schema/source-map/admission-map/pin/source set/namespace/root/owner/output-path/toolchain/Python-package change follows. Compare against contract179: closure only2helper rows change and registry only its one recipe closure hash; all other352rows/fields/recipe/source metadata unchanged.

Review exact owner-scoped behavior across3closed resolved documentIDs and26forms/137actualnodes: only `pattern` keyword uses rawselectedECMA-u form, foreign schemas and `patternProperties` preserve inherited70-row table. Four forms absent from this TS table are native-only (2newrelative paths +2existingC0/DEL/C1text); do not conflate with the72-form Rust baseline. Unknown native pattern must failclosed even if inherited-known; no source guard or caller-selected profile. Resolve transitive startup/native and native/foreign references with targetidentity. Check cache keyed by admitted expression with admissionbeforecache; same rawliteral/profile order must not leak. Regex flags/end/dot/linebreak/scalar semantics must match selected owner, especially a/..<LF> and full-length grant wildcard CR/LS/PS.

Read bounded controls141registry checks,3,100,500native matrix comparisons and8,347,500inheritedTS comparisons,43real documents/886entrypoint closure. These are helper authoring evidence, no selected generation/fullunit/qualification. Earlier harness errors are preserved; inspect finalscript/report/bytes independently. The unchanged renderer embeds helpers in report output: complete later materialization review must inspect real output changes and owning/consumer/mutation/provenance checks. This design selection authorizes exact helper inputs only after realacceptance/rootassent/publication/binding; no generator bypass or selfhashauthority. Empty overrides/no supersession.

Complete code review/integration then immediate B2b4c3 exact-main reviewed one-run blindrefresh is mandatory before D2b3c/census-dependentconsumption. Preserve unchangedmethod/population/allowlist, cleancheckout/private0700/exclusivelane/nice10, no contentpeeks/tuning/ad-hocretry, ordinarywrite/check then independentpostrunreview/rootassent before receiptcommit. No private/production/H/C4semantic/qualification/project completion grant.

READONLY hashes/JSON/Git/source only. No tests/builds/generators/Cargo/lanes/network/panes/delegation or edits to repositories/worktrees/stage/control/evidence. No private413/keys/installations/heldout/T2/census modes. Write ONLY REVIEW.md and review.json in {Q}. Use required findings OWNPAT-GEN-R1-RF-n and NBO-n if needed. Verdict ACCEPT-DESIGN-UNIT only if exactsubject clears. JSON fields: verdict,subjectManifestSha256,requiredFindings,nonBlockingObservations,helperFiles:2,nativeForms:26,inheritedTypeScriptForms:70,generatorSources:43,admissionSources:52,aliases:15,materializationCodeAccepted:false,blindRefreshComplete:false,productQualification:false.
'''
(Q/'REQUEST.md').write_text(request);print(json.dumps(prepared,indent=2))
