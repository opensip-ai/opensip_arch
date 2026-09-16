from pathlib import Path
import json,hashlib,shutil,subprocess,os
r=Path(__file__).parent; original=r/'repository'; export=r/'source-export';export.mkdir()
for name in ['crates/contracts','crates/identity','providers/rust']:
 shutil.copytree(original/name,export/name)
assert not (export/'Cargo.toml').exists()
assert not (export/'apps').exists()
assert not (export/'providers/typescript').exists()
assert not (export/'tools').exists()
for path in export.rglob('*'):
 if path.is_file():path.chmod(0o444)
for path in sorted(export.rglob('*'),reverse=True):
 if path.is_dir():path.chmod(0o555)
export.chmod(0o555)
home=r/'home';home.mkdir()
env={'PATH':'/usr/bin:/bin','HOME':str(home),'CARGO_HOME':'/Users/sb/.cargo','RUSTC':'/opt/homebrew/bin/rustc','CARGO_TARGET_DIR':str(r/'target'),'LANG':'C','LC_ALL':'C','TZ':'UTC'}
configs=[Path('/Users/sb/.cargo')/n for n in ('config','config.toml')]
configs += [ancestor/'.cargo'/n for ancestor in [export,*export.parents] for n in ('config','config.toml')]
assert not any(x.exists() for x in configs), 'unexpected Cargo configuration'
manifest=export/'providers/rust/Cargo.toml';commands=[]
def run(args,name):
 p=subprocess.run(args,env=env,cwd=export/'providers/rust',capture_output=True,text=True)
 (r/(name+'.stdout')).write_text(p.stdout);(r/(name+'.stderr')).write_text(p.stderr)
 commands.append({'command':args,'exitCode':p.returncode,'stdout':name+'.stdout','stderr':name+'.stderr'})
 if p.returncode:raise RuntimeError(p.stderr)
 return p.stdout
cargo='/opt/homebrew/bin/cargo'
meta=json.loads(run([cargo,'metadata','--locked','--offline','--format-version','1','--filter-platform','aarch64-apple-darwin','--manifest-path',str(manifest)],'provider-metadata'))
(r/'provider-metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
run([cargo,'build','--locked','--offline','--manifest-path',str(manifest)],'build')
run([str(r/'target/debug/opensip-rust-provider')],'probe')
for row in json.loads((r/'shared-sources-before.json').read_bytes()):
 for root in [original,export]:
  raw=(root/row['path']).read_bytes();assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
assert (original/'Cargo.lock').read_bytes()==(r/'root-lock-before').read_bytes()
record={'schemaVersion':1,'passed':True,'scope':'actual separate provider Cargo workspace/lock and immutable pure-source export trial; disposable executable is not a provider implementation','sourceExport':str(export),'hostManifestAbsent':True,'hostAppsAbsent':True,'nodeAndGeneratorAbsent':True,'workspaceMembers':meta['workspace_members'],'rootLockUnchanged':True,'sharedSourcesUnchanged':True,'commands':commands,'environment':env,'compilerIntegrationQualified':False,'productQualification':False}
(r/'result.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record,indent=2))
