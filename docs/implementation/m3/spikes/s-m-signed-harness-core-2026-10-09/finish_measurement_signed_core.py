from pathlib import Path
import json,hashlib,subprocess,importlib.util,sys,os,copy
B=Path(__file__).resolve().parent;D=B/'measurement-signed-core';A=Path('/Users/sb/code/opensip-ai/opensip_arch');os.setpriority(os.PRIO_PROCESS,0,10);os.environ['PATH']='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin';sys.path.insert(0,'/tmp/opensip-implementation/measurement-jsonschema-4.25.1')
def load(p,name):s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
L=load(A/'docs/coop/completion/security_unit_lib_v8.py','metadata_reference');M=load(A/'docs/coop/design-corrections/native/native_evidence_model.v2.py','native_reference')
def pin(p):raw=p.read_bytes();return dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
root=json.loads((D/'explicit-harness-test-root.json').read_bytes());admitted,findings=L.admit_root_document(root);assert admitted and findings==[]
raw=(D/'inventory.json').read_bytes();inventory=L.load_json_strict(raw);env=L.load_json_strict((D/'inventory.sig.json').read_bytes());verified=L.verify_envelope(raw,env,admitted,'inventory','opensip-measurement-harness');assert verified[0]=='VERIFIED'
tree=D/'owned-core-tree';payload_raw=(tree/'bootstrap/payload.json').read_bytes();payload_env=L.load_json_strict((tree/'bootstrap/payload.sig.json').read_bytes());payload_verified=L.verify_envelope(payload_raw,payload_env,admitted,'payload','opensip-measurement-harness');assert payload_verified[0]=='VERIFIED'
base=json.loads((D/'evaluator-descriptor.json').read_bytes());assert base['manifestDigest']==hashlib.sha256(raw).hexdigest();closures={};tree_members=[]
for row in base['tree']:
    p=tree/row['path'];observed=pin(p);assert observed['bytes']==row['bytes'] and observed['sha256']==row['sha256'];tree_members.append(observed)
for kind in ('evaluator','provider','adapter'):
    descriptor=json.loads((D/f'{kind}-descriptor.json').read_bytes());assert descriptor['kind']==kind and {k:v for k,v in descriptor.items() if k!='kind'}=={k:v for k,v in base.items() if k!='kind'}
    identity=M.IM.identifier('closure',descriptor);out=subprocess.check_output([str(B/'hash_bridge'),'closure',str(D/f'{kind}-descriptor.json')]);(D/f'{kind}-bridge.stdout').write_bytes(out);assert identity=='closure2:'+json.loads(out)['identityDigest'];closures[kind]=identity
controls=[]
def refusal(label,body,carrier,authority=admitted):
    result=L.verify_envelope(body,carrier,authority,'inventory','opensip-measurement-harness');assert result[0]!='VERIFIED';controls.append(dict(case=label,outcome=result[0],detail=result[1]))
refusal('stored-byte-change',raw+b' ',env)
single=copy.deepcopy(env);single['signatures']=single['signatures'][:1];refusal('threshold-shortfall',raw,single)
wrong=copy.deepcopy(env);wrong['namespace']='another-harness';refusal('namespace-mismatch',raw,wrong)
refusal('unadmitted-caller-root',raw,env,root)
bad=copy.deepcopy(env)
for row in bad['signatures']:row['signature']='00'*64
refusal('invalid-signatures',raw,bad)
result=dict(standing='UNREVIEWED FRESH SIGNED HARNESS-ONLY INVENTORY AND CORE ROLE PROJECTIONS; NO PRODUCTION TR-CORE/CRC1 ADMISSION',explicitHarnessRoot=pin(D/'explicit-harness-test-root.json'),inventory=pin(D/'inventory.json'),envelope=pin(D/'inventory.sig.json'),verification=list(verified),bootstrapEnvelopeVerification=list(payload_verified),rootAdmissionFindings=findings,metadataProfile='opensip.metadata.inventory.1',rawBodyDigestExcludesEnvelope=True,regularFiles=len(base['tree']),treeMembers=tree_members,roleClosures=closures,roleDescriptorsDifferOnlyByKind=True,referenceProductIdentityAgrees=True,productBridge=pin(B/'hash_bridge'),referenceMetadata=pin(A/'docs/coop/completion/security_unit_lib_v8.py'),referenceNative=pin(A/'docs/coop/design-corrections/native/native_evidence_model.v2.py'),profileScaffold=pin(D/'harness-platform-profile-scaffold.json'),opensslVersion=subprocess.check_output(['/opt/homebrew/bin/openssl','version']).decode().strip(),controls=controls,privateSigningKeysAreFreshHarnessOnly=True,privateKeysExcludedFromPlanPreimage=True,explicitRootNotProductionTrustAnchor=True,productionTRCORE=False,authenticatedProductionCRC1=False,productionPlatformProfile=False,productionBootstrapBundle=False,selectedEvaluationSeal=False,executionPlanConstructed=False,SMComplete=False,effectiveL=False,qualification=False)
assert not (D/'observations.json').exists();(D/'observations.json').write_text(json.dumps(result,indent=2)+'\n');print('Fresh harness inventory VERIFIED under explicit admitted test root;3core role IDs/reference-product agree;5refusal controls. No production admission.')
