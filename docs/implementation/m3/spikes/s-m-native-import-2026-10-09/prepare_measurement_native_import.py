from pathlib import Path
import json,hashlib,importlib.util,sys,os,subprocess,copy
sys.path.insert(0,'/tmp/opensip-implementation/measurement-jsonschema-4.25.1')
import jsonschema
from referencing import Registry,Resource
B=Path(__file__).resolve().parent;D=B/'measurement-native-import';assert not D.exists();D.mkdir();A=Path('/Users/sb/code/opensip-ai/opensip_arch');P=A.parent/'opensip';os.setpriority(os.PRIO_PROCESS,0,10)
def load(p,name):s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
M=load(A/'docs/coop/design-corrections/native/native_evidence_model.v2.py','native_import_measurement_reference');L=load(A/'docs/coop/completion/security_unit_lib_v8.py','metadata_import_measurement_reference')
def read(p):return json.loads(p.read_bytes())
def rawsha(raw):return hashlib.sha256(raw).hexdigest()
def pin(p):raw=p.read_bytes();return dict(path=str(p),bytes=len(raw),sha256=rawsha(raw))
def write(p,j):p.write_bytes(M.C.canonical(j))
def digest(j):return rawsha(M.C.canonical(j))
def bridge(domain,p):
    out=subprocess.check_output([str(B/'hash_bridge'),domain,str(p)]);return json.loads(out)
E=dict(os.environ,GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null')
for k in ('GIT_CONFIG_COUNT','GIT_DIR','GIT_WORK_TREE'):E.pop(k,None)
actual=subprocess.check_output(['/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14','-I','-B','tools/verify_design.py','--architecture',str(A),'--implementation',str(P)],cwd=P,env=E);assert json.loads(actual)['passed'];(D/'actual-selected-design.json').write_bytes(actual)
mapping=read(P/'schemas/source-map.json');native_pin=next(r['architectureSource'] for r in mapping['sources'] if r['implementationPath']=='schemas/sources/native-v2.schema.json');assert pin(A/native_pin['path'])==native_pin|dict(path=str(A/native_pin['path']))
native_raw=(P/'schemas/sources/native-v2.schema.json').read_bytes();assert native_raw==(A/native_pin['path']).read_bytes();native=read(P/'schemas/sources/native-v2.schema.json')
assert 'native.input-import-self-reference' in native['x-opensip-public-route-registry']['keys'] and 'oneOf' in native['$defs']['DependencySourcePayloadV1']['properties']['acquisitionSourcePath']
documents={}
for row in read(P/'schemas/admission-registry.json')['sources']:
    raw=(P/row['sourcePath']).read_bytes();assert len(raw)==row['bytes'] and rawsha(raw)==row['sha256'];doc=json.loads(raw);documents[doc['$id']]=doc
registry=Registry().with_resources([(k,Resource.from_contents(v)) for k,v in documents.items()])
foundation=read(A/'docs/coop/design-corrections/foundation/identity-schemas.v3.json')
def validate(doc,name,value):
    jsonschema.Draft202012Validator({'$ref':'#/$defs/'+name,'$defs':doc['$defs']},registry=registry).validate(value)
def foundation_validate(name,value):validate(foundation,name,value)
scope=dict(schemaVersion=2,workspaceRoots=['.'],pathPrefixes=['.'],excludedPathPrefixes=[]);foundation_validate('scope-descriptor',scope);write(D/'analysis-scope-descriptor.json',scope)
config=dict(analysis=dict(profileId='measurement.axum',capabilities=['imports','syntax'],budget=dict(unit='work-units',limit=1000000)),components={},discovery=dict(workspaceRoots=['.']),policy={},evidence=dict(importIds=[]));foundation_validate('semantic-configuration',config);write(D/'semantic-configuration-scaffold.json',config)
old_snapshot=read(B/'manifest-scope/rs-medium-axum-snapshot-fixture.json');snapshot=copy.deepcopy(old_snapshot['descriptor']);inventory=snapshot['sourceInventory'];foundation_validate('source-inventory',inventory)
vcs=dict(schemaVersion=2,kind='none',commitId=None,dirty=False,sourceInventoryDigest=digest(inventory));foundation_validate('vcs-observation',vcs);write(D/'vcs-observation-scaffold.json',vcs)
snapshot.update(scopeDigest=digest(scope),resolvedConfigDigest=digest(config),vcsDigest=digest(vcs));foundation_validate('snapshot',snapshot);write(D/'fresh-snapshot-descriptor.json',snapshot)
snapshot_id=M.IM.identifier('snapshot',snapshot);assert snapshot_id=='snapshot2:'+bridge('snapshot',D/'fresh-snapshot-descriptor.json')['identityDigest'];assert snapshot_id!=old_snapshot['snapshotId']
dep=read(B/'actual-dependency-source-set/descriptor.json');dep_obs=read(B/'actual-dependency-source-set/observations.json');context=read(B/'measurement-native-context/descriptor.json');expected=M.dependency_source_set_identity(dep);assert expected==context['dependencySourceSetId']==dep_obs['dependencySourceSetId'];assert all(row['acquisition']['descriptorId'] is None for row in dep['packages'])
tarballs=[dict(packageKey=row['packageKey'],crateTarballSha256=row['archive']['sha256']) for row in dep_obs['witnesses']];assert len(tarballs)==187 and len({r['packageKey'] for r in tarballs})==187
payload=dict(schemaVersion=1,payloadDomain='native.import-payload.dependency-source.v1',set=dep,acquisitionSourcePath=None,tarballDigests=tarballs);validate(native,'DependencySourcePayloadV1',payload)
correspondence=dict(kind='exact-snapshot',snapshotId=snapshot_id);build=dict(schemaVersion=1,buildIdentity=None);observation=dict(schemaVersion=1,kind='dependency',window=None,population=None,selection=None,revisionRange=None)
common=documents['urn:opensip:product-v1:workflows:common'];imported=documents['urn:opensip:product-v1:workflows:imported-evidence'];validate(common,'SourceCorrespondence',correspondence);validate(imported,'BuildIdentityV1',build);validate(imported,'ImportObservationV1',observation)
core=read(B/'measurement-signed-core/observations.json');root=read(B/'measurement-signed-core/explicit-harness-test-root.json');admitted,findings=L.admit_root_document(root);assert admitted and findings==[]
core_raw=(B/'measurement-signed-core/inventory.json').read_bytes();core_env=read(B/'measurement-signed-core/inventory.sig.json');assert L.verify_envelope(core_raw,core_env,admitted,'inventory','opensip-measurement-harness')[0]=='VERIFIED'
roles={kind:read(B/f'measurement-signed-core/{kind}-descriptor.json') for kind in ('evaluator','provider','adapter')}
for kind,descriptor in roles.items():
    assert descriptor['kind']==kind and descriptor['manifestDigest']==rawsha(core_raw)
    assert {k:v for k,v in descriptor.items() if k!='kind'}=={k:v for k,v in roles['evaluator'].items() if k!='kind'}
    assert M.IM.identifier('closure',descriptor)==core['roleClosures'][kind]
wrapper=dict(schemaVersion=2,kind='dependency',payloadSchemaDigest=rawsha(native_raw),payloadDigest=digest(payload),sourceCorrespondenceDigest=digest(correspondence),buildDigest=digest(build),producerClosure=core['roleClosures']['provider'],adapterClosure=core['roleClosures']['adapter'],blobs=[],scopeDigest=digest(scope),observationDigest=digest(observation),completeness='complete',omissions=[])
validate(imported,'ImportWrapperV2',wrapper);foundation_validate('import',wrapper)
for name,value in [('payload',payload),('source-correspondence',correspondence),('build',build),('observation',observation),('wrapper',wrapper)]:write(D/(name+'.json'),value)
(D/'selected-full-native-schema.json').write_bytes(native_raw)
import_id=M.IM.identifier('import',wrapper);assert import_id=='import2:'+bridge('import',D/'wrapper.json')['identityDigest']
def check_candidate(candidate,candidate_payload):
    validate(imported,'ImportWrapperV2',candidate);validate(native,'DependencySourcePayloadV1',candidate_payload)
    assert candidate['kind']=='dependency' and candidate['payloadSchemaDigest']==rawsha(native_raw) and candidate['payloadDigest']==digest(candidate_payload)
    assert candidate_payload['acquisitionSourcePath'] is None,'native.input-import-acquisition-path'
    assert all(r['acquisition']['descriptorId'] is None for r in candidate_payload['set']['packages']),'native.input-import-self-reference'
    assert sorted(candidate_payload['tarballDigests'],key=lambda r:r['packageKey'])==sorted(tarballs,key=lambda r:r['packageKey']),'actual tarball membership differs'
    assert candidate['producerClosure']==core['roleClosures']['provider'] and candidate['adapterClosure']==core['roleClosures']['adapter']
    assert candidate['sourceCorrespondenceDigest']==digest(correspondence) and candidate['buildDigest']==digest(build) and candidate['scopeDigest']==digest(scope) and candidate['observationDigest']==digest(observation)
    return M.IM.identifier('import',candidate),M.dependency_source_set_identity(candidate_payload['set'])
def resolve(candidates,selected):
    assert selected==sorted(set(selected)), 'noncanonical selected import union'
    matches=set()
    for candidate,candidate_payload in candidates:
        candidate_id,set_id=check_candidate(candidate,candidate_payload)
        if candidate_id in selected and set_id==expected:matches.add(candidate_id)
    assert len(matches)==1,'native.input-import-join-missing' if not matches else 'native.input-import-join-ambiguous'
    return next(iter(matches))
assert resolve([(wrapper,payload)],[import_id])==import_id
controls=[]
def refuse(label,action):
    try:action()
    except (AssertionError,jsonschema.ValidationError,ValueError) as err:controls.append(dict(case=label,refused=True,detail=str(err)[:256]));return
    raise AssertionError('accepted control '+label)
refuse('missing-selected-import',lambda:resolve([(wrapper,payload)],[]));refuse('duplicate-selected-import-id',lambda:resolve([(wrapper,payload)],[import_id,import_id]))
bad=copy.deepcopy(payload);bad['acquisitionSourcePath']='explicit-refusal-path';bad_wrapper=copy.deepcopy(wrapper);bad_wrapper['payloadDigest']=digest(bad);refuse('non-null-acquisition-path',lambda:check_candidate(bad_wrapper,bad))
bad=copy.deepcopy(payload);bad['set']['packages'][0]['acquisition']['descriptorId']=import_id;bad_wrapper=copy.deepcopy(wrapper);bad_wrapper['payloadDigest']=digest(bad);refuse('non-null-payload-self-reference',lambda:check_candidate(bad_wrapper,bad))
bad=copy.deepcopy(wrapper);bad['payloadSchemaDigest']=dep_obs['descriptor']['sha256'];refuse('selected-definition-instead-of-full-document-digest',lambda:check_candidate(bad,payload))
bad=copy.deepcopy(wrapper);bad['producerClosure']=read(B/'measurement-provider-closure-v2/observations.json')['closureId'];refuse('component-provider-substituted-for-core',lambda:check_candidate(bad,payload))
# tarballDigests is a published sequence, not a canonical set. Two exact
# validated byte sequences can carry the same set while minting distinct imports.
other_payload=copy.deepcopy(payload);other_payload['tarballDigests'].reverse();other_wrapper=copy.deepcopy(wrapper);other_wrapper['payloadDigest']=digest(other_payload);other_id,_=check_candidate(other_wrapper,other_payload);assert other_id!=import_id
refuse('two-distinct-matching-imports',lambda:resolve([(wrapper,payload),(other_wrapper,other_payload)],sorted([import_id,other_id])))
assert config['evidence']['importIds']==[]
def configuration_guard(ids):
    assert import_id not in ids,'native.input-import-configured'
configuration_guard(config['evidence']['importIds'])
refuse('native-import-in-configuration-even-when-context-selected',lambda:configuration_guard([import_id]))
bad=copy.deepcopy(payload);bad['tarballDigests']=bad['tarballDigests'][:-1];bad_wrapper=copy.deepcopy(wrapper);bad_wrapper['payloadDigest']=digest(bad);refuse('omitted-actual-package-tarball',lambda:check_candidate(bad_wrapper,bad))
write(D/'observations.json',dict(standing='UNREVIEWED COMPLETE PRELIMINARY IMPORT/SNAPSHOT DATA; NO PRODUCTION ADMISSION',importId=import_id,dependencySourceSetId=expected,freshSnapshotId=snapshot_id,previousSnapshotId=old_snapshot['snapshotId'],freshSnapshotHasClosedScaffoldPreimages=True,originalSnapshotPreserved=True,snapshotRegularFiles=len(inventory),contextId=read(B/'measurement-native-context/observations.json')['nativeContextId'],selectedFullSchemaDocument=pin(D/'selected-full-native-schema.json'),selectedArchitectureSource=native_pin,payload=pin(D/'payload.json'),wrapper=pin(D/'wrapper.json'),auxiliaryDigestsAreRawCanonicalSha256=True,payloadSelfReferencesAndPathNull=True,coreTestRootVerification='VERIFIED',coreProjectionKindsOnly=True,coreProviderNotInRustSemanticClosures=True,exactlyOnePlanSelectedMatchingImport=True,nativeConfigurationImportsEmpty=True,referenceProductImportIdentityAgrees=True,referenceProductSnapshotIdentityAgrees=True,controls=controls,scopeAndConfigurationScaffoldsInsidePreimages=True,productionTRCORE=False,authenticatedProductionCRC1=False,productionImportAdmission=False,productionSnapshotAdmission=False,executionPlanConstructed=False,actualC2Keys=False,actualNativeWorker=False,SMComplete=False,effectiveL=False,qualification=False))
print('Complete fresh import2/snapshot2 data/reference-product agree;187packages/498snapshotrows;9refusal controls including exact semantic guards; no production admission.')
