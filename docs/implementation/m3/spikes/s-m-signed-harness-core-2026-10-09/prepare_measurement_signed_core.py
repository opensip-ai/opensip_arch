from pathlib import Path
import os,json,hashlib,subprocess,importlib.util,sys,copy,datetime,stat
B=Path(__file__).resolve().parent;D=B/'measurement-signed-core';assert not D.exists();D.mkdir(mode=0o700);K=D/'private-test-keys';K.mkdir(mode=0o700);A=Path('/Users/sb/code/opensip-ai/opensip_arch');os.setpriority(os.PRIO_PROCESS,0,10)
os.environ['PATH']='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin'
# This standalone harness explicitly owns its test root. It never opens the
# account installation, a product root or any historical/private fixture.
def load(p,name):
    spec=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
L=load(A/'docs/coop/completion/security_unit_lib_v8.py','harness_metadata_reference')
sys.path.insert(0,'/tmp/opensip-implementation/measurement-jsonschema-4.25.1');import jsonschema
M=load(A/'docs/coop/design-corrections/native/native_evidence_model.v2.py','harness_native_reference')
def h(raw):return hashlib.sha256(raw).hexdigest()
def pin(p):raw=p.read_bytes();return dict(path=str(p),bytes=len(raw),sha256=h(raw))
def write(p,j):p.write_bytes(L.canonical_bytes(json.loads(json.dumps(j))))
def ssl(*args):return subprocess.check_output(['/opt/homebrew/bin/openssl',*args],stderr=subprocess.PIPE)
keys=[];private={}
for i in range(20):
    pem=K/f'fresh-key-{i:02d}.pem';ssl('genpkey','-algorithm','ED25519','-out',str(pem));pem.chmod(0o600)
    der=ssl('pkey','-in',str(pem),'-pubout','-outform','DER');assert der[:12]==bytes.fromhex('302a300506032b6570032100') and len(der)==44
    pub=der[-32:].hex();kid=L.key_id(pub);keys.append(dict(keyId=kid,publicKey=pub,label=f'fresh harness-only key {i}'));private[kid]=pem
now=datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0);stamp=lambda t:t.strftime('%Y-%m-%dT%H:%M:%SZ')
roles={}
for i,name in enumerate(('TR-CORE','TR-INDEX','TR-COMPONENT','TR-BUNDLE')):
    roles[name]=dict(keys=sorted(k['keyId'] for k in keys[8+3*i:11+3*i]),threshold=2,namespaces=['opensip-measurement-harness'],standing='active')
roles['TR-REPAIR']=dict(keys=[],threshold=0,namespaces=[],standing='typed-absence-DR-110')
root=dict(rootSchema=1,rootVersion=1,previousRootVersion=None,issuedAt=stamp(now),expiresAt=stamp(now+datetime.timedelta(days=365)),keys=sorted(keys,key=lambda k:k['keyId']),rootKeys=sorted(k['keyId'] for k in keys[:3]),rootThreshold=2,roles=roles,recoveryAuthority=dict(keys=sorted(k['keyId'] for k in keys[3:8]),threshold=3),kernelAttestationKeys=[],indexOrigin=dict(url='https://opensip-measurement-harness.invalid',spkiSha256=h(ssl('pkey','-in',str(private[keys[0]['keyId']]),'-pubout','-outform','DER'))))
write(D/'explicit-harness-test-root.json',root);admitted,findings=L.admit_root_document(root);assert admitted is not None and findings==[],findings
tree=D/'owned-core-tree';tree.mkdir(mode=0o700);boot=tree/'bootstrap';boot.mkdir(mode=0o700)
profile=dict(standing='UNADMITTED HARNESS-ONLY PROFILE SCAFFOLD; NO PRODUCTION PLATFORM OR LAUNCH SELECTION',platform='macos-aarch64',source='fresh standalone metadata/import harness')
write(D/'harness-platform-profile-scaffold.json',profile)
payload=dict(standing='HARNESS-ONLY INERT EMBEDDED BOOTSTRAP BYTES; NOT PRODUCTION BUNDLE ADMISSION',explicitTestRootSha256=pin(D/'explicit-harness-test-root.json')['sha256'])
write(boot/'payload.json',payload)
def envelope(raw,kind):
    domain,role=L.KIND_ROUTING[kind]
    env=dict(envelopeSchema=2,subject=dict(kind=kind,domain=domain,storedSha256=h(raw),preimageSha256=L.domain_digest(domain,L.load_json_strict(raw))[0]),role=role,namespace='opensip-measurement-harness',signatures=[])
    msg=bytes.fromhex(L.envelope_message_hex(env));message=D/f'{kind}-signature-message.bin';message.write_bytes(msg)
    for kid in root['roles'][role]['keys'][:2]:
        sig=ssl('pkeyutl','-sign','-rawin','-inkey',str(private[kid]),'-in',str(message));assert len(sig)==64
        env['signatures'].append(dict(keyId=kid,alg='ed25519',signature=sig.hex()))
    result=L.verify_envelope(raw,env,admitted,kind,'opensip-measurement-harness');assert result[0]=='VERIFIED',result
    return env,result
payload_env,payload_verified=envelope((boot/'payload.json').read_bytes(),'payload');write(boot/'payload.sig.json',payload_env)
# This actual identity encoder is an inert measured harness tool, not a
# production host entrypoint or a complete native worker/core release.
(tree/'identity-harness').write_bytes((B/'hash_bridge').read_bytes());(tree/'identity-harness').chmod(0o700)
files=[];entries=[dict(path='bootstrap',type='dir',mode='700')]
for p in sorted(tree.rglob('*')):
    st=p.lstat();assert not stat.S_ISLNK(st.st_mode)
    if not stat.S_ISREG(st.st_mode):continue
    raw=p.read_bytes();logical=p.relative_to(tree).as_posix();row=dict(path=logical,type='file',mode='700' if p.name=='identity-harness' else '600',length=len(raw),sha256=h(raw));entries.append(row);files.append(dict(path=logical,sha256=h(raw),bytes=len(raw)));p.chmod(int(row['mode'],8))
entries.sort(key=lambda r:r['path']);files.sort(key=lambda r:r['path']);by_path={r['path']:r for r in files}
inventory=dict(inventorySchema=2,semanticVersion='0.1.0-harness',protocolMajor=1,servedProtocolMajors=[1],platformProfileBinding=dict(schemaVersion=2,platformProfileSetBodyDigest=L.domain_digest('opensip.metadata.platform-profile-set.1',profile)[0]),verifiedInstallRoot='/',platforms=[dict(platform='macos-aarch64',tree=dict(entries=entries),entrypoint='identity-harness',layers=[dict(path=r['path'],layers=['L-DIST','L-HOST'] if r['path']=='identity-harness' else ['L-DIST']) for r in files],requires=[])],embeddedBootstrap=dict(directory='bootstrap',manifest=by_path['bootstrap/payload.json'],envelope=by_path['bootstrap/payload.sig.json']),tcbProfiles=[])
schema=json.loads(Path('/Users/sb/code/opensip-ai/opensip/tools/security/inputs/trust-record-schema.json').read_bytes());jsonschema.Draft202012Validator({'$ref':'#/$defs/CoreInventoryV2','$defs':schema['$defs']}).validate(inventory)
write(D/'inventory.json',inventory);raw=(D/'inventory.json').read_bytes();env,verified=envelope(raw,'inventory');write(D/'inventory.sig.json',env)
base=dict(schemaVersion=2,kind='evaluator',manifestDigest=h(raw),tree=files,semanticVersion=inventory['semanticVersion'],protocolMajor=inventory['protocolMajor'],platform='macos-aarch64')
closures={};bridge=pin(B/'hash_bridge')
for kind in ('evaluator','provider','adapter'):
    descriptor=copy.deepcopy(base);descriptor['kind']=kind;assert {k:v for k,v in descriptor.items() if k!='kind'}=={k:v for k,v in base.items() if k!='kind'}
    identity=M.IM.identifier('closure',descriptor)
    write(D/f'{kind}-descriptor.json',descriptor)
    result=json.loads(subprocess.check_output([str(B/'hash_bridge'),'closure',str(D/f'{kind}-descriptor.json')]))
    assert 'closure2:'+result['identityDigest']==identity
    closures[kind]=identity
controls=[]
def refusal(label,body,carrier,authority=admitted):
    result=L.verify_envelope(body,carrier,authority,'inventory','opensip-measurement-harness');assert result[0]!='VERIFIED',(label,result);controls.append(dict(case=label,outcome=result[0],detail=result[1]))
refusal('stored-byte-change',raw+b' ',env)
single=copy.deepcopy(env);single['signatures']=single['signatures'][:1];refusal('threshold-shortfall',raw,single)
wrong=copy.deepcopy(env);wrong['namespace']='another-harness';refusal('namespace-mismatch',raw,wrong)
refusal('unadmitted-caller-root',raw,env,root)
bad=copy.deepcopy(env);bad['signatures'][0]['signature']='00'*64;bad['signatures'][1]['signature']='00'*64;refusal('invalid-signatures',raw,bad)
assert pin(B/'hash_bridge')==bridge
write(D/'observations.json',dict(standing='UNREVIEWED FRESH SIGNED HARNESS-ONLY INVENTORY AND CORE ROLE PROJECTIONS; NO PRODUCTION TR-CORE/CRC1 ADMISSION',explicitHarnessRoot=pin(D/'explicit-harness-test-root.json'),inventory=pin(D/'inventory.json'),envelope=pin(D/'inventory.sig.json'),verification=verified,bootstrapEnvelopeVerification=payload_verified,rootAdmissionFindings=findings,metadataProfile='opensip.metadata.inventory.1',rawBodyDigestExcludesEnvelope=True,regularFiles=len(files),treeMembers=[pin(tree/r['path']) for r in files],roleClosures=closures,roleDescriptorsDifferOnlyByKind=True,referenceProductIdentityAgrees=True,productBridge=bridge,referenceMetadata=pin(A/'docs/coop/completion/security_unit_lib_v8.py'),referenceNative=pin(A/'docs/coop/design-corrections/native/native_evidence_model.v2.py'),profileScaffold=pin(D/'harness-platform-profile-scaffold.json'),opensslVersion=ssl('version').decode().strip(),controls=controls,privateSigningKeysAreFreshHarnessOnly=True,privateKeysExcludedFromPlanPreimage=True,explicitRootNotProductionTrustAnchor=True,productionTRCORE=False,authenticatedProductionCRC1=False,productionPlatformProfile=False,productionBootstrapBundle=False,selectedEvaluationSeal=False,executionPlanConstructed=False,SMComplete=False,effectiveL=False,qualification=False))
print('Fresh signed harness inventory VERIFIED;3kind-only projections;5signature/root refusal controls; no production admission.')
