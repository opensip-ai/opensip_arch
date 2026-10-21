"""Pure policy-data successor; no product writes or checker/generator execution."""
from pathlib import Path
import json,hashlib,copy,subprocess
F=Path(__file__).parent;B=F/'loader-policy-design-r1';S=B/'architecture';Q=Path('/tmp/opensip-implementation/reviews/codex-native-owner-loader-policy-r1');assert not B.exists() and not Q.exists()
P=Path('/Users/sb/code/opensip-ai/opensip');W=P.parent/'opensip-native-owner-patterns-takeover';A=P.parent/'opensip_arch';PRE='docs/implementation/m3/native-publication/native-owner-generator-loader-policy-r1'
def pin(root,p):
 raw=(root/p).read_bytes();return dict(path=p,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
def git(root,*a):return subprocess.check_output(['/usr/bin/git','-C',str(root),*a],text=True).strip()
L=json.loads((P/'design-lock.json').read_text());assert len(L['contractSuccessors'])==180
accepted={r['path']:r for r in L['inputs']}
for binding in L['contractSuccessors']:
 for row in json.loads((A/binding['record']['path']).read_text())['candidates']:accepted[row['path']]=row
oldpolicy_path='docs/implementation/m1/generator-selection-v2/generator-loader-policy.json';closure_path='docs/implementation/m3/native-publication/native-owner-generator-profile-r1/product/tools/contracts/generator-closure.json';registry_path='docs/implementation/m3/verify-design-vd2/f8c/product/tools/typescript-lanes.json'
parents=[pin(A,p) for p in (oldpolicy_path,closure_path,registry_path)];assert all(accepted[r['path']]==r for r in parents)
policy=json.loads((A/oldpolicy_path).read_text());before=copy.deepcopy(policy);closure=json.loads((A/closure_path).read_text());rows={r['path']:r for r in closure['files']};changes=[]
for row in policy['files']:
 selected=rows[row['path']];assert pin(W,row['path'])==selected
 if row!=selected:changes.append(dict(before=copy.deepcopy(row),after=copy.deepcopy(selected)))
 row.update(bytes=selected['bytes'],sha256=selected['sha256'])
assert [r['before']['path'] for r in changes]==['tools/contracts/package.json','tools/contracts/runtime/patterns.ts','tools/contracts/runtime/schema.ts']
normalized=copy.deepcopy(policy);normalized['files']=before['files'];assert normalized==before
policy_path=PRE+'/generator-loader-policy.json';write(S/policy_path,policy)
registry=json.loads((P/'tools/typescript-lanes.json').read_text());assert pin(P,'tools/typescript-lanes.json')['sha256']==parents[2]['sha256']
prior_registry=copy.deepcopy(registry);generator=next(l for l in registry['lanes'] if l['name']=='generator');assert generator['toolPolicy']==oldpolicy_path;generator['toolPolicy']=policy_path
normalized_registry=copy.deepcopy(registry);next(l for l in normalized_registry['lanes'] if l['name']=='generator')['toolPolicy']=oldpolicy_path;assert normalized_registry==prior_registry
registry_out=PRE+'/product/tools/typescript-lanes.json';write(S/registry_out,registry)
audit=dict(standing='PROPOSED PURE LOADER-POLICY PIN REFRESH; REAL REVIEW/ASSENT/BINDING REQUIRED BEFORE CHECKER CONSUMPTION',productBase=git(P,'rev-parse','HEAD'),architectureBase=git(A,'rev-parse','HEAD'),policyFiles=11,changedPolicyRows=changes,allPolicyInputsEqualAccepted180GeneratorClosure=True,
 trustedUsagesUnchanged=True,unfollowedDynamicLoaderLimitsUnchanged=True,laneRecordUnchanged=True,noNewTargetsExceptionsLoadersPathsOrCapabilities=True,
 typedRegistryChangeOnlyGeneratorToolPolicyPath=True,typedRegistryFilePinsNodeLanesRecordsUnchanged=True,typescriptRegistryInGeneratorClosure=False,ordinaryGenerationInputsOutputsUnchanged=True,discoveryReferenceProductPathsUnchanged=['tools/security/discovery_walk_vectors.py','tools/contracts/generator-closure.json'],
 materializationCodeAccepted=False,generatorExecuted=False,checkerExecuted=False,blindRefreshComplete=False,productQualification=False,
 productMap=[dict(productPath='tools/typescript-lanes.json',candidate=pin(S,registry_out))],
 baselineProof='Actual unchanged main generator boundary lane refuses tools/contracts/package.json pin; candidate report/provider lanes pass. The pure data policy still pins two historical main inputs and lacks the separately accepted180helper byte updates.')
write(S/PRE/'audit.json',audit)
(S/PRE/'README.md').write_text('''# Generator loader policy exact-pin refresh r1

Proposed pure selected policy-data successor; independent ACCEPT-DESIGN-UNIT, root assent, immutable publication and real lock binding precede use. No product implementation, generated output, blind receipt or qualification is accepted here.

The currently selected generator boundary policy has11input rows. Actual unchanged-main checking refuses its stale tools/contracts/package.json pin; the pre-materialization main pattern table also differs, and selected helper design180 supplies the prospective schema/pattern helper bytes. This successor updates exactly3policy size/hash rows, all11now joining the actually accepted180generator closure. No source code is authored or selected beyond the already accepted immutable inputs. The other8rows, lane record, trustedUsages and unfollowedDynamicLoaders are byte/value-equal. Compiler bytes, every dynamic/optional loader spelling, position, hash, target list, reason and limitation stay unchanged. No exception, new target, plugin/config access or trusted-code capability is added.

The prospective product tools/typescript-lanes.json changes only its generator lane toolPolicy path to this immutable new policy. All160checker/dependency file pins, exact Node pin and3lane records/trusted usages remain unchanged. The registry file is outside the generator352-row closure; no generator input/output or discovery reference-loading row changes. The current main may retain its coherent selected ancestor registry until complete code materialization applies the new pointer. No checker is run under a fabricated acceptance/lock or self-hash authority.

Complete materialization still needs full corrected owning/consumer/mutation/feature/Clippy/workspace/source/package/environment/design and all3TypeScript boundary checks, independent complete unit review/root assent/exact integration, its own15new-path inventory binding and immediate independently authorized B2b4c3 one-run unchanged-method/population/disclosure blind refresh before census-dependent consumption. Existing dynamic-loader limitations and all private/owner/production/platform/qualification gates remain open.
''')
candidates=[pin(S,str(p.relative_to(S))) for p in sorted((S/PRE).rglob('*')) if p.is_file()];record_path=PRE+'/successor.json';write(S/record_path,dict(schemaVersion=1,standing='PROPOSED exact loader policy pin selection only; no code/receipt/qualification acceptance',parents=sorted(parents,key=lambda r:r['path']),candidates=candidates,passageOverrides=[]))
manifest=PRE+'-subject.json';write(S/manifest,dict(schemaVersion=1,unit='NATIVE-OWNER-GENERATOR-LOADER-POLICY-r1',files=sorted(candidates+[pin(S,record_path)],key=lambda r:r['path'])))
prepared=dict(unit='NATIVE-OWNER-GENERATOR-LOADER-POLICY-r1',prefix=PRE,stage=str(S),subjectManifest=pin(S,manifest),record=pin(S,record_path),parents=parents,productBase=audit['productBase'],architectureBase=audit['architectureBase'],prospectiveContractSuccessor=181,materializationCodeAccepted=False,checkerExecuted=False,productQualification=False)
write(B/'prepared.json',prepared);Q.mkdir();write(Q/'subject.json',prepared)
for name,src in [('baseline-generator.log',F/'baseline-r1/typescript-generator.log'),('baseline-report.json',F/'baseline-r1/report.json'),('candidate-typescript-lanes.log',F/'full-r1/typescript-lanes.log')]:
 (Q/name).write_bytes(src.read_bytes())
write(Q/'evidence-manifest.json',dict(files=[pin(Q,p.name) for p in sorted(Q.iterdir()) if p.is_file()]))
(Q/'REQUEST.md').write_text(f'''# Native-owner generator loader policy pure data successor

Read subject.json and frozen stage {S}; manifest SHA256 {prepared['subjectManifest']['sha256']}. Rehash all5members,3selectedacceptedparents and frozen evidence-manifest files. Bases product{prepared['productBase']}/ARCH{prepared['architectureBase']} must remainexact. Judge source/policy data independently; ACCEPT-DESIGN-UNIT only, no materialization/checker/qualification grant.

The11-row loader policy is the accepted M1generator-selection-v2 artifact, the parent typedregistry is accepted F8c, and parent generatorclosure is actuallybound180. Rehash acceptance/subject/review/assent joins from real lock. Three size/hash rows change (package.json, runtime/patterns.ts, runtime/schema.ts), everyone of11joins current accepted180closure. No helper code, source/closure/runtime/schema/recipe/output change is included. Allother8rows, lane record,3trustedUsages and unfollowed dynamic loader limitations remain exactlyequal; no new source targets, exceptions, call sites, hashes of loader callers/compiler, positions/spellings or privileges. Compare alltrustedRows, not onlycount. This exact refresh addresses baselineactualmain and candidate failure at package.json; current materialization helper sources are independentlyaccepted180, not authority from unacceptedcode.

Prospective product tools/typescript-lanes.json changes only generator.toolPolicy immutablepath. All160tool/dependency file pins, Node pin and3lane records/trustedusages unchanged. Neither this registry nor loaderpolicy is in generatorclosure352; selected ordinarygeneration/outputs remainunchanged; census reference products are unchangedwalktool+generatorclosure. No freshblind margin/currentqualification inferred. Currentmain retains its selected ancestor registry until complete materialization; designrecord emptyoverrides/no supersession preserves old artifacts.

No fake acceptance/lock or checker execution performed for thisdata proposal. Complete materialization/fullcorrectedowning/all3TSlanes, independentcodeunitreview/rootassent/integration, ownnewpathinventory then immediate reviewedexactmain one-runblindrefresh before anycensus-dependentconsumption remain required. Allowner/privacy/production/platform/dynamicloader/qualification limits remain. Preserve helddrafts. Do notinspect T2/privatefixtures or conflate design acceptance with completeunit/plan closure.

READONLY hashes/JSON/Git/source. No builds/tests/checkers/generators/Cargo/lanes/network/panes/delegation or repository/worktree/stage/control/evidence edits. No private413/keys/installations/heldout/T2/census modes. Write ONLY REVIEW.md and review.json in {Q}. IDs OWNPAT-LOAD-R1-RF-n/NBO-n. JSON verdict ACCEPT-DESIGN-UNIT or REQUIRED-FINDINGS;subjectManifestSha256;requiredFindings;nonBlockingObservations;policyFiles:11;changedPolicyRows:3;trustedUsagesUnchanged:true;materializationCodeAccepted:false;blindRefreshComplete:false;productQualification:false.
''')
print(json.dumps(prepared,indent=2))
