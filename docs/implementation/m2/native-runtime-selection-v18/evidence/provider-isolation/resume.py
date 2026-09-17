from pathlib import Path
import json,subprocess,hashlib,tomllib
T=Path('/tmp/opensip-implementation');B=T/'m2-native-provider-isolation-18';P=T/'m2-package-parser-trial-38/product';E=B/'export';A=Path('/Users/sb/code/opensip-ai/opensip_arch');cargo='/opt/homebrew/Cellar/rust/1.95.0/bin/cargo';rustc='/opt/homebrew/Cellar/rust/1.95.0/bin/rustc';py='/tmp/opensip-implementation/metadata-reference-env/bin/python'
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
assert not(B/'receipt.json').exists(); prior=B/'initial-feature-profile-refusal';prior.mkdir()
for n in ['commands.json','dependencies.stdout','dependencies.stderr']:(prior/n).write_bytes((B/n).read_bytes())
commands=json.loads((B/'commands.json').read_bytes());assert [r['exitCode']for r in commands]==[0,0,0,0,1];commands=commands[:4]
source=[]
for p in sorted(E.rglob('*')):
 if p.is_file():
  rel=str(p.relative_to(E));assert p.read_bytes()==(P/rel).read_bytes();source.append({'path':rel,**pin(p.read_bytes())})
assert len(source)==26
vendor=B/'vendor';archives=Path('/Users/sb/.cargo/registry/cache/index.crates.io-1949cf8c6b5b557f');deps=[]
for row in tomllib.loads((E/'providers/rust/Cargo.lock').read_text())['package']:
 if 'source' not in row:continue
 name=row['name']+'-'+row['version'];raw=(archives/(name+'.crate')).read_bytes();assert hashlib.sha256(raw).hexdigest()==row['checksum'];checks=json.loads((vendor/name/'.cargo-checksum.json').read_bytes());assert checks['package']==row['checksum']
 for n,h in checks['files'].items():assert hashlib.sha256((vendor/name/n).read_bytes()).hexdigest()==h
 deps.append({'name':row['name'],'version':row['version'],**pin(raw),'fileCount':len(checks['files'])})
assert len(deps)==19
env={'PATH':'/usr/bin:/bin','HOME':str(B/'empty-home'),'CARGO_HOME':str(B/'cargo-home'),'RUSTC':rustc,'CARGO_TARGET_DIR':str(B/'target'),'LANG':'C','LC_ALL':'C','TZ':'UTC','CARGO_INCREMENTAL':'0'}
def run(name,cmd,expected=0,**kwargs):
 r=subprocess.run(cmd,cwd=E/'providers/rust',env=env,capture_output=True,timeout=300,**kwargs);(B/(name+'.stdout')).write_bytes(r.stdout);(B/(name+'.stderr')).write_bytes(r.stderr);commands.append({'name':name,'command':cmd,'exitCode':r.returncode,'expected':expected});(B/'commands.json').write_text(json.dumps(commands,indent=2)+'\n');assert r.returncode==expected,(name,r.stderr.decode());print(name+' passed',flush=True);return r
run('dependencies',[py,'-I','-B',str(P/'tools/check_dependencies.py'),'--manifest',str(E/'providers/rust/Cargo.toml'),'--target','aarch64-apple-darwin','--cargo',cargo,'--feature-profile','toml-workspace'])
run('edges',[py,'-I','-B',str(P/'tools/check_package_edges.py'),'--repository',str(E),'--metadata',str(B/'metadata.stdout'),'--inventory',str(A/'docs/implementation/m2/repository-file-inventory.v26.json'),'--lane','rust-provider'])
exe=B/'target/aarch64-apple-darwin/debug/opensip-rust-provider'
for i,data in enumerate([b'',b'{"kind":"hello"}\n',b'not a protocol frame\x00']):
 r=run('unavailable-'+str(i),[str(exe)],1,input=data);assert r.stdout==b'' and r.stderr==b'opensip Rust provider: native analysis is not implemented in this development build\n'
for row in source:assert pin((E/row['path']).read_bytes())=={k:row[k]for k in ['bytes','sha256']}
(B/'receipt.json').write_text(json.dumps({'standing':'Candidate M2 parser provider boundary proof; intentional unavailable exit, not a semantic provider or analysis success','sources':source,'sharedOwnerFiles':len([r for r in source if r['path'].startswith('crates/')]),'providerOwnedFiles':len([r for r in source if r['path'].startswith('providers/')]),'dependencies':deps,'environment':env,'commands':commands,'sourceAndProviderLockUnchanged':True,'noHostRootManifestAppsToolsNode':True,'rustc':pin(Path(rustc).read_bytes()),'cargo':pin(Path(cargo).read_bytes()),'executable':pin(exe.read_bytes()),'nativeCompilerIntegrationImplemented':False,'fullM1Complete':False,'releaseQualification':False,'featureProfile':'toml-workspace; proposed exact metadata profile, source/runtime acceptance pending','resumption':'Original build and metadata succeeded; original dependency guard refusal preserved. Resumed with exact explicit contracts feature profile and unchanged compiled source/export bytes. No rebuild claimed.','trustedHostLimit':'Native linker/SDK/loader/compiler libs and dependency build/procmacro remain TCB; no malicious process network confinement or complete compiler closure attestation'},indent=2)+'\n');print('receipt written',len(source),len(deps))
