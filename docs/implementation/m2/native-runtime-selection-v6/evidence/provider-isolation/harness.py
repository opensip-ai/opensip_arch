from pathlib import Path
import json,shutil,subprocess,hashlib,tomllib,importlib.util
B=Path('/tmp/opensip-implementation/m2-native-provider-isolation-06'); B.mkdir(); P=Path('/tmp/opensip-implementation/m2-native-runtime-candidate-06/product'); E=B/'export'; E.mkdir(); A=Path('/Users/sb/code/opensip-ai/opensip_arch'); cargo='/opt/homebrew/Cellar/rust/1.95.0/bin/cargo'; rustc='/opt/homebrew/Cellar/rust/1.95.0/bin/rustc'; py='/tmp/opensip-implementation/metadata-reference-env/bin/python'
def pin(b): return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
source=[]
for name in ['crates/contracts','crates/identity','providers/rust']:
 for p in sorted((P/name).rglob('*')):
  if p.is_file():
   assert p.name in ['Cargo.toml','Cargo.lock','rust-toolchain.toml'] or p.suffix=='.rs'
   rel=str(p.relative_to(P)); raw=p.read_bytes(); out=E/rel; out.parent.mkdir(parents=True,exist_ok=True); out.write_bytes(raw); out.chmod(0o444); source.append({'path':rel,**pin(raw)})
for p in sorted(E.rglob('*'),reverse=True):
 if p.is_dir() and p.is_relative_to(E/'crates'): p.chmod(0o555)
ch=B/'cargo-home'; ch.mkdir(); home=B/'empty-home'; home.mkdir(); vendor=B/'vendor'; vendor.mkdir()
spec=importlib.util.spec_from_file_location('archive_helper',P/'tools/build_contracts.py'); helper=importlib.util.module_from_spec(spec); spec.loader.exec_module(helper)
archives=Path('/Users/sb/.cargo/registry/cache/index.crates.io-1949cf8c6b5b557f'); deps=[]
for row in tomllib.loads((E/'providers/rust/Cargo.lock').read_text())['package']:
 if 'source' not in row: continue
 assert row['source']=='registry+https://github.com/rust-lang/crates.io-index'; name=row['name']+'-'+row['version']; raw=(archives/(name+'.crate')).read_bytes(); deps.append(helper.unpack_archive(raw,row['name'],row['version'],row['checksum'],vendor/name))
config='[source.crates-io]\nreplace-with = "verified-vendor"\n[source.verified-vendor]\ndirectory = '+json.dumps(str(vendor))+'\n'; (ch/'config.toml').write_text(config)
for parent in (E/'providers/rust',*(E/'providers/rust').parents): assert not any((parent/'.cargo'/n).exists() for n in ['config','config.toml'])
env={'PATH':'/usr/bin:/bin','HOME':str(home),'CARGO_HOME':str(ch),'RUSTC':rustc,'CARGO_TARGET_DIR':str(B/'target'),'LANG':'C','LC_ALL':'C','TZ':'UTC','CARGO_INCREMENTAL':'0'}; commands=[]
def run(name,cmd,expected=0,**kwargs):
 r=subprocess.run(cmd,cwd=E/'providers/rust',env=env,capture_output=True,timeout=300,**kwargs); (B/(name+'.stdout')).write_bytes(r.stdout); (B/(name+'.stderr')).write_bytes(r.stderr); commands.append({'name':name,'command':cmd,'exitCode':r.returncode,'expected':expected}); (B/'commands.json').write_text(json.dumps(commands,indent=2)+'\n'); assert r.returncode==expected,(name,r.returncode,r.stderr.decode()); print(name+' passed',flush=True); return r
run('cargo-version',[cargo,'-vV']); run('rustc-version',[rustc,'-vV'])
run('build',[cargo,'build','--locked','--offline','--target','aarch64-apple-darwin'])
run('metadata',[cargo,'metadata','--locked','--offline','--format-version','1','--filter-platform','aarch64-apple-darwin'])
run('dependencies',[py,'-I','-B',str(P/'tools/check_dependencies.py'),'--manifest',str(E/'providers/rust/Cargo.toml'),'--target','aarch64-apple-darwin','--cargo',cargo])
run('edges',[py,'-I','-B',str(P/'tools/check_package_edges.py'),'--repository',str(E),'--metadata',str(B/'metadata.stdout'),'--inventory',str(A/'docs/implementation/m2/repository-file-inventory.v16.json'),'--lane','rust-provider'])
exe=B/'target/aarch64-apple-darwin/debug/opensip-rust-provider'
for i,data in enumerate([b'',b'{"kind":"hello"}\n',b'not a protocol frame\x00']):
 r=run('unavailable-'+str(i),[str(exe)],1,input=data); assert r.stdout==b'' and r.stderr==b'opensip Rust provider: native analysis is not implemented in this development build\n'
for row in source: assert pin((E/row['path']).read_bytes())=={k:row[k] for k in ['bytes','sha256']}
(B/'receipt.json').write_text(json.dumps({'standing':'Candidate M2 shared admission module provider boundary proof; intentional unavailable exit, not a semantic provider or analysis success','sources':source,'sharedOwnerFiles':len([r for r in source if r['path'].startswith('crates/')]),'providerOwnedFiles':len([r for r in source if r['path'].startswith('providers/')]),'dependencies':deps,'environment':env,'commands':commands,'sourceAndProviderLockUnchanged':True,'noHostRootManifestAppsToolsNode':True,'rustc':pin(Path(rustc).read_bytes()),'cargo':pin(Path(cargo).read_bytes()),'executable':pin(exe.read_bytes()),'nativeCompilerIntegrationImplemented':False,'fullM1Complete':False,'releaseQualification':False,'trustedHostLimit':'Native linker/SDK/loader/compiler libs and reviewed dependency build/procmacro remain TCB; no malicious process network confinement or complete compiler closure attestation'},indent=2)+'\n')
