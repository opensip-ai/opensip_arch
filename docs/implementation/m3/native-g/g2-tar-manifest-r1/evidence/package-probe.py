import pathlib,os,subprocess,tempfile,time,json,hashlib,gzip
b=pathlib.Path('/tmp/opensip-implementation/g2-tar-manifest-authoring');d=b/'cargo-profile-probe';assert not d.exists();f=d/'fixture';(f/'src').mkdir(parents=True)
name='opensip-profile-fixture';version='0.1.0';root=f'{name}-{version}/'
(f/'Cargo.toml').write_text('[workspace]\n\n[package]\nname="opensip-profile-fixture"\nversion="0.1.0"\nedition="2024"\npublish=false\nlicense="Apache-2.0"\ninclude=["Cargo.toml", "src/**"]\n')
(f/'Cargo.lock').write_text('version = 4\n\n[[package]]\nname = "opensip-profile-fixture"\nversion = "0.1.0"\n')
(f/'src/lib.rs').write_text('pub fn declared_fixture() -> u8 { 7 }\n')
for path in ['src/'+('a'*120)+'.rs','src/'+('b'*(99-len(root)-4))+'é.rs']:(f/path).write_text('// packaging input only; never compiled or executed\n')
base=pathlib.Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR'],text=True).strip());lock=base/'opensip-lanes.lock';e=dict(os.environ,PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo',CARGO_TARGET_DIR=str(d/'target'),TMPDIR=tempfile.mkdtemp(prefix='opensip-package-profile-',dir=base),GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null');os.chmod(e['TMPDIR'],0o700)
for k in ['GIT_CONFIG_COUNT','GIT_DIR','GIT_WORK_TREE']:e.pop(k,None)
while True:
 try:lock.mkdir();break
 except FileExistsError:time.sleep(5)
try:
 with (d/'package.log').open('w') as log:r=subprocess.run(['/usr/bin/nice','-n','10','/opt/homebrew/Cellar/rust/1.95.0/bin/cargo','package','--locked','--offline','--no-verify','--allow-dirty'],cwd=f,env=e,stdout=log,stderr=subprocess.STDOUT)
 assert r.returncode==0,(d/'package.log').read_text()
finally:lock.rmdir()
archive=d/'target/package'/f'{name}-{version}.crate';raw=archive.read_bytes();inflated=gzip.decompress(raw);(d/'declared-inflated.tar').write_bytes(inflated)
headers=[];offset=0
while any(inflated[offset:offset+512]):
 h=inflated[offset:offset+512];size=int(h[124:136].strip(b'\0 '),8);headers.append({'nameHex':h[:100].hex(),'type':chr(h[156]),'size':size});offset+=512+((size+511)//512)*512
result={'standing':'Harness-only pinned Cargo writer probe, no crate compile/verify/repository code/provider/qualification. Python stdlib gzip used only to supply declared inflated observation, not selected product inflater.', 'command':['cargo','package','--locked','--offline','--no-verify','--allow-dirty'],'packageName':name,'packageVersion':version,'rawBytes':len(raw),'rawSha256':hashlib.sha256(raw).hexdigest(),'inflatedBytes':len(inflated),'inflatedSha256':hashlib.sha256(inflated).hexdigest(),'gzipFlags':raw[3],'headers':headers,'endRegionBytes':len(inflated)-offset,'nativeProducerExecuted':False,'qualification':False}
(d/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='headers'}))
