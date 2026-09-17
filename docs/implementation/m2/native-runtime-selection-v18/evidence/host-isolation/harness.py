from pathlib import Path
import json,hashlib,shutil,subprocess,os,sys,tomllib,importlib.util
A=Path('/Users/sb/code/opensip-ai/opensip_arch'); L=Path('/tmp/opensip-implementation/m2-package-parser-trial-38/product'); B=Path('/tmp/opensip-implementation/m2-native-host-isolation-18'); assert not B.exists(); B.mkdir()
py='/tmp/opensip-implementation/metadata-reference-env/bin/python'; cargo=Path('/opt/homebrew/Cellar/rust/1.95.0/bin/cargo'); rustc=cargo.parent/'rustc'
# Base24/35 design/source preflight only. New runtime source unit is unselected.
# Proposed admission source binding is checked separately; exact build source pins follow.
r=subprocess.run([py,'-I','-B',str(L/'tools/verify_design.py'),'--architecture',str(A),'--implementation',str(L)],capture_output=True,timeout=120)
(B/'design.stdout').write_bytes(r.stdout); (B/'design.stderr').write_bytes(r.stderr); assert r.returncode==0
spec=importlib.util.spec_from_file_location('selected_builder',L/'tools/build_contracts.py'); helper=importlib.util.module_from_spec(spec); spec.loader.exec_module(helper)
def pin(b): return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def filepin(p): return {'path':str(p),**pin(p.read_bytes())}
rootdoc=tomllib.loads((L/'Cargo.toml').read_text()); selected=['Cargo.toml','Cargo.lock','rust-toolchain.toml']
for name in rootdoc['workspace']['members']:
 for p in sorted((L/name).rglob('*')):
  if p.is_symlink(): raise ValueError('linked input')
  if p.is_file():
   assert p.name=='Cargo.toml' or p.suffix in ['.rs','.json','.cve1'],str(p)
   selected.append(str(p.relative_to(L)))
# Only explicitly indexed raw documents needed by host include_bytes! are added.
registry=json.loads((L/'schemas/admission-registry.json').read_bytes())
for row in registry['sources']:
 raw=(L/row['sourcePath']).read_bytes()
 assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
 selected.append(row['sourcePath'])
selected.append('schemas/admission-registry.json')
assert len(registry['sources'])==48
selected=sorted(selected); sources=[{'path':s,**pin((L/s).read_bytes())} for s in selected]
project=B/'project'; project.mkdir(); vendor=B/'vendor'; vendor.mkdir()
for s in selected:
 p=project/s; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes((L/s).read_bytes())
lock=tomllib.loads((project/'Cargo.lock').read_text()); deps=[]; archives=Path('/Users/sb/.cargo/registry/cache/index.crates.io-1949cf8c6b5b557f')
for p in lock['package']:
 if 'source' not in p: continue
 assert p['source']=='registry+https://github.com/rust-lang/crates.io-index'
 name=p['name']+'-'+p['version']; raw=(archives/(name+'.crate')).read_bytes()
 deps.append(helper.unpack_archive(raw,p['name'],p['version'],p['checksum'],vendor/name))
ch=B/'cargo-home'; ch.mkdir(); home=B/'empty-home'; home.mkdir()
config='[source.crates-io]\nreplace-with = "verified-vendor"\n[source.verified-vendor]\ndirectory = '+json.dumps(str(vendor))+'\n'
(ch/'config.toml').write_text(config)
for parent in (project,*project.parents):
 assert not any((parent/'.cargo'/name).exists() for name in ['config','config.toml'])
env={'PATH':'/usr/bin:/bin','HOME':str(home),'CARGO_HOME':str(ch),'CARGO_TARGET_DIR':str(B/'target'),'RUSTC':str(rustc),'RUSTDOC':str(cargo.parent/'rustdoc'),'LANG':'C','LC_ALL':'C','TZ':'UTC','CARGO_INCREMENTAL':'0'}
tools={n:filepin(p) for n,p in [('cargo',cargo),('rustc',rustc),('rustdoc',cargo.parent/'rustdoc')]}; cmds=[]
def run(name,cmd):
 with (B/(name+'.stdout')).open('wb') as out,(B/(name+'.stderr')).open('wb') as err: r=subprocess.run(cmd,cwd=project,env=env,stdout=out,stderr=err,timeout=600)
 cmds.append({'name':name,'command':cmd,'exitCode':r.returncode}); (B/'commands.json').write_text(json.dumps(cmds,indent=2)+'\n'); assert r.returncode==0,name
 print(name+' passed',flush=True)
run('cargo-version',[str(cargo),'-vV']); run('rustc-version',[str(rustc),'-vV'])
target='aarch64-apple-darwin'; assert 'host: '+target in (B/'rustc-version.stdout').read_text()
run('build',[str(cargo),'build','--locked','--offline','--workspace','--target',target,'--message-format=json'])
run('tests',[str(cargo),'test','--locked','--offline','--workspace','--all-targets','--target',target])
run('doctests',[str(cargo),'test','--locked','--offline','--doc','-p','opensip-evaluator','--target',target])
run('metadata',[str(cargo),'metadata','--locked','--offline','--format-version','1','--filter-platform',target])
exe=B/'target'/target/'debug/opensip'
run('version',[str(exe),'version','--format','json']); run('help',[str(exe),'help','--format','json'])
for row in sources:
 assert pin((project/row['path']).read_bytes())=={k:row[k] for k in ['bytes','sha256']}
for n,row in tools.items(): assert filepin(Path(row['path']))==row
receipt={'schemaVersion':1,'standing':'Observed private native-owner candidate host development lane from exact source snapshot and checksum-verified supplied archives. Not reproducible-build, malicious-native-tool confinement or release qualification.','sources':sources,'archiveMaterializer':filepin(L/'tools/build_contracts.py'),'harness':filepin(Path(__file__)),'tools':tools,'python':filepin(Path(sys.executable)),'dependencies':deps,'environment':env,'vendorConfig':config,'commands':cmds,'target':target,'profile':'dev','executable':filepin(exe),'sourceAndLockUnchanged':True,'noNodeProviderUiOrToolSourcesInProject':True,'embeddedSchemaDocuments':48,'designPreflightScope':'Base24/35 only; proposed runtime unit not yet independently accepted','fullM1Complete':False,'limits':['System linker/SDK/loader/native compiler libraries remain trusted host inputs; compiler executable pins are not full transitive toolchain authentication.','Dependency build scripts and procedural macros are selected native TCB; --offline disables Cargo fetching, not arbitrary process networking.','No signed release closure, size/startup gates, cross-target or full provider/report implementation.']}
(B/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n'); print('receipt written',len(sources),len(deps))
