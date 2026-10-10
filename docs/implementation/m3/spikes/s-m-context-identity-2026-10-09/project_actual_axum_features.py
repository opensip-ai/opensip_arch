from pathlib import Path
import importlib.util,json,hashlib,tomllib,os,subprocess,sys
sys.path.insert(0,"/tmp/opensip-implementation/measurement-jsonschema-4.25.1")
B=Path(__file__).resolve().parent;A=Path('/Users/sb/code/opensip-ai/opensip_arch');D=B/'actual-feature-projection';D.mkdir(exist_ok=False);os.setpriority(os.PRIO_PROCESS,0,10)
def pin(p):b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
model=A/'docs/coop/design-corrections/native/native_evidence_model.v2.py';spec=importlib.util.spec_from_file_location('native_model',model);M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
meta=B/'axum-resolved-metadata.json';attempt=json.loads((B/'axum-resolved-metadata-attempt.json').read_text());assert pin(meta)==attempt['metadata'];j=json.loads(meta.read_text());root=Path(j['workspace_root']);manifest=root/'Cargo.toml';root_toml=tomllib.loads(manifest.read_text());resolver=int(root_toml['workspace']['resolver']);assert resolver in [1,2,3]
lock=Path(attempt['originalLock']['path']);assert pin(lock)=={k:v for k,v in attempt['originalLock'].items() if k!='version'};lock_packages=tomllib.loads(lock.read_text())['package'];lookup={};tuple_rows=[];seen=set()
for p in j['packages']:
 tuple_=[p['name'],p['version'],p['source'] or ''];matches=[r for r in lock_packages if [r['name'],r['version'],r.get('source','')]==tuple_];assert len(matches)==1,tuple_
 encoded=M.C.canonical(tuple_);key='pkg1-'+hashlib.sha256(encoded).hexdigest();assert key not in seen and p['id'] not in lookup;seen.add(key);lookup[p['id']]=key;tuple_rows.append(dict(metadataId=p['id'],tuple=tuple_,canonicalTupleUtf8=encoded.decode(),packageKey=key))
assert len(lookup)==191;rows=[]
for node in j['resolve']['nodes']:
 features=node['features'];assert features==sorted(set(features));assert all(e['pkg'] in lookup for e in node['deps']);rows.append(dict(packageKey=lookup[node['id']],features=features))
assert len(rows)==len(lookup);rows.sort(key=lambda r:r['packageKey'])
features=dict(schemaVersion=1,resolverVersion=resolver,targetTriple=attempt['filterPlatform'],activated=rows,computedBy=dict(producer='opensip-cargo-adapter',producerBuildId='measurement-cargo-'+attempt['runtime']['sha256']))
# This producer label identifies the outside-product first-party adapter. It grants no bundled Tool or carrier admission.
identity=M.unified_features_identity(features);write(D/'unified-features.json',features);write(D/'package-keys.json',dict(standing='ACTUAL ORIGINAL LOCK TUPLE / ONE METADATA CONTEXT UNIQUE JOIN; NOT SOURCE ADMISSION',packages=sorted(tuple_rows,key=lambda r:r['packageKey'])))
bridge=B/'hash_bridge';before=pin(bridge);child=subprocess.Popen([str(bridge),'native.unified-features.rust.v1',str(D/'unified-features.json')],stdout=subprocess.PIPE,stderr=subprocess.PIPE);priority=os.getpriority(os.PRIO_PROCESS,child.pid);raw,err=child.communicate();assert priority==10 and child.returncode==0,err;bridge_result=json.loads(raw);assert identity=='sha256:'+bridge_result['identityDigest'];assert pin(bridge)==before
(D/'bridge.stdout').write_bytes(raw);(D/'bridge.stderr').write_bytes(err)
write(D/'observations.json',dict(standing='UNREVIEWED ACTUAL AXUM ACTIVATION DATA/HASH SUPPORT ONLY; NO BUNDLED CARGO/TOOL/CARRIER/CONTEXT ADMISSION',metadata=pin(meta),lockfile=pin(lock),workspaceManifest=pin(manifest),referenceModel=pin(model),foundationCanonical=pin(A/'docs/coop/design-corrections/foundation/canonical.py'),runtime=attempt['runtime'],bridge=before,bridgeSource=pin(B/'hash_bridge.rs'),actualPackages=191,activatedPackages=len(rows),resolverVersion=resolver,targetTriple=attempt['filterPlatform'],unifiedFeatures=pin(D/'unified-features.json'),unifiedFeaturesId=identity,productIdentityAgrees=True,observedBridgeNiceness=priority,sourceAdmission=False,contextAdmitted=False,ToolAdmitted=False,actualC2PlanOrKeys=False,fullSM=False))
print(identity,len(rows),'actual activations: schema/reference/product identity agree')
