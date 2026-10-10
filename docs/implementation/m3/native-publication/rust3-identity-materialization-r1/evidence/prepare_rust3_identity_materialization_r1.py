"""Prepare an isolated product candidate only after RCA-1 is accepted and bound."""
from pathlib import Path
import json, hashlib, os, subprocess, copy, stat
B=Path('/tmp/opensip-implementation'); A=Path('/Users/sb/code/opensip-ai/opensip_arch'); P=A.parent/'opensip'; W=A.parent/'opensip-rust3-identity'; D=B/'rust3-identity-materialization-r1'; S=D/'architecture'; PRE='docs/implementation/m3/native-publication/rust3-identity-materialization-r1'; C=Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06')
E=dict(os.environ,GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null')
for k in ('GIT_CONFIG_COUNT','GIT_DIR','GIT_WORK_TREE'): E.pop(k,None)
def git(root,*a):return subprocess.check_output(['/usr/bin/git',*a],cwd=root,env=E).decode().strip()
def read(p):return json.loads(p.read_bytes())
def write(p,j):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(j,indent=2)+'\n')
def pin(p,path):
 b=p.read_bytes();return dict(path=path,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
pub=read(C/'CURRENT-STATE.json')['RustCommitAlignmentPublication']; assert pub['rust3LiteralCommitSelected'] and pub['verifyDesignPassed']
assert git(P,'rev-parse','HEAD')==pub['productLock'] and git(A,'rev-parse','HEAD')==pub['architecture'] and git(P,'status','--porcelain')==''
lock=read(P/'design-lock.json'); assert len(lock['contractSuccessors'])==158
assert not W.exists() and not D.exists(); git(P,'worktree','add','--detach',str(W),pub['productLock']);D.mkdir()
selected='docs/implementation/m3/native-successors-fa/rust-commit-alignment-r2/product/schemas/sources/'
changed=['schemas/sources/handshake-v1.schema.json','schemas/sources/startup-v1.schema.json']; associations=[]
for p in changed:
 old=pin(P/p,p); src=A/selected/Path(p).name; (W/p).write_bytes(src.read_bytes()); associations.append(dict(implementationPath=p,before=old,selectedArchitectureSource=pin(src,selected+Path(p).name)))
sm=read(W/'schemas/source-map.json'); am=read(W/'schemas/admission-source-map.json')
for mapping in (sm,am):
 for row in associations:
  matches=[x for x in mapping['sources'] if x['implementationPath']==row['implementationPath']];assert len(matches)==1;matches[0]['architectureSource']=row['selectedArchitectureSource']
write(W/'schemas/source-map.json',sm);write(W/'schemas/admission-source-map.json',am)
ar=read(W/'schemas/admission-registry.json'); before=copy.deepcopy(ar); updates=[]
for group in ('sources','aliases'):
 for row in ar[group]:
  if row['sourcePath'] in changed:
   p=pin(W/row['sourcePath'],row['sourcePath']); row.update(bytes=p['bytes'],sha256=p['sha256']);updates.append(dict(group=group,**row))
 for old,new in zip(before[group],ar[group]):
  assert {k:v for k,v in old.items() if k not in ('bytes','sha256')}=={k:v for k,v in new.items() if k not in ('bytes','sha256')}
  if old['sourcePath'] not in changed:assert old==new
write(W/'schemas/admission-registry.json',ar); target=S/PRE/'admission-registry.json';write(target,ar);am['registryArchitectureSource']=pin(target,PRE+'/admission-registry.json');write(W/'schemas/admission-source-map.json',am)
import re
p=W/'crates/identity/src/schema_registry.rs'; text=p.read_text()
for source in changed:
 raw=(W/source).read_bytes();digest=hashlib.sha256(raw).digest();pattern=r'(SourcePin \{\s*id: "[^\"]+",\s*path: "'+re.escape(source)+r'",\s*bytes: )\d+(,\s*sha256: \[)[\d,\s]+(\],\s*\})'
 text,count=re.subn(pattern,lambda m:m[1]+str(len(raw))+m[2]+', '.join(str(v) for v in digest)+',\n        '+m[3],text);assert count==1
p.write_text(text)
p=W/'crates/host/src/schema_sources.rs'
p.write_text(p.read_text()+'''\n#[cfg(test)]
mod rust3_identity_shape_tests {
    use super::embedded_schema_registry;

    #[test]
    fn current_rust3_commit_is_literal_and_other_digests_stay_sha256() {
        let registry = embedded_schema_registry().unwrap();
        let id = "opensip.product.provider-handshake.1";
        let actual = "59807616e1fa2540724bfbac14d7976d7e4a3860";
        for definition in ["ExpectedRustIdentityV3", "HelloAckV3"] {
            let extra = if definition == "HelloAckV3" {
                r#",\"capabilities\":[\"coverage-v3\",\"fact-identity-fact2\",\"plan-identity-plan2\",\"source-identity-snapshot2\"],\"identityVersions\":{\"snapshot\":2,\"plan\":2,\"fact\":2,\"coverage\":3}"#
            } else { "" };
            for (commit, accepted) in [
                (actual.to_string(), true),
                ("a".repeat(40), true), // Shape alone gives no authenticated identity.
                ("a".repeat(64), false),
                (actual.to_uppercase(), false),
                (format!("{actual}\\\\n"), false),
            ] {
                let raw = format!(r#"{{\"protocolMajor\":3,\"providerBuildId\":\"shape-only-test\",\"rustCommitHash\":\"{commit}\",\"hostTriple\":\"aarch64-apple-darwin\",\"targetTriple\":\"aarch64-apple-darwin\",\"sysrootDigest\":\"{}\"{extra}}}"#, "b".repeat(64));
                let admitted = registry.schema(id, &format!("/$defs/{definition}"))
                    .unwrap().admit_json(raw.as_bytes(), 1_000_000).is_ok();
                assert_eq!(admitted, accepted, "{definition}: {commit}");
            }
        }
        for (digest, accepted) in [("a".repeat(64), true), (actual.to_string(), false)] {
            let raw = format!("\\\"{digest}\\\"");
            assert_eq!(registry.schema(id, "/$defs/DigestHex").unwrap()
                .admit_json(raw.as_bytes(), 100_000).is_ok(), accepted);
        }
    }
}
''')
closure=read(W/'tools/contracts/generator-closure.json'); oldclosure=copy.deepcopy(closure);copied=[];repinned=[]
allowed=set(changed+['schemas/source-map.json','schemas/admission-source-map.json','schemas/admission-registry.json'])
for row in closure['files']:
 p=W/row['path']
 if not p.exists():
  assert row['path'].startswith(('tools/contracts/node_modules/','tools/contracts/python-packages/'));src=P/row['path'];s=src.lstat();assert stat.S_ISREG(s.st_mode)
  fd=os.open(src,os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC)
  with os.fdopen(fd,'rb') as f:
   beforestat=os.fstat(f.fileno());raw=f.read();afterstat=os.fstat(f.fileno());assert (s.st_dev,s.st_ino)==(beforestat.st_dev,beforestat.st_ino);assert (beforestat.st_size,beforestat.st_mtime_ns,beforestat.st_ctime_ns)==(afterstat.st_size,afterstat.st_mtime_ns,afterstat.st_ctime_ns)
  assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw);copied.append(row['path'])
 new=pin(p,row['path'])
 if new!=row:assert row['path'] in allowed;repinned.append(dict(before=dict(row),after=new));row.update(new)
assert [r['path'] for r in closure['files']]==[r['path'] for r in oldclosure['files']];write(W/'tools/contracts/generator-closure.json',closure)
registry=read(W/'schemas/registry.json')
for row in registry['sources']:
 if row['sourcePath'] in changed:row['sourceSha256']=pin(W/row['sourcePath'],row['sourcePath'])['sha256']
registry['recipes'][0]['sourceSha256s']=sorted({r['sourceSha256'] for r in registry['sources']});registry['recipes'][0]['generatorClosureSha256']=pin(W/'tools/contracts/generator-closure.json','tools/contracts/generator-closure.json')['sha256'];write(W/'schemas/registry.json',registry)
write(D/'preparation.json',dict(productBase=pub['productLock'],architectureBase=pub['architecture'],candidateWorktree=str(W),archive=PRE,associations=associations,admissionRepins=updates,generatorRepins=repinned,exactPinnedIgnoredInputsCopied=len(copied),sourceSetAndAliasTopologyUnchanged=True,currentHandshakeIncludesAcceptedRUST3LIM=True,HOMEOverride=False,productConsumerAdmission=False,actualNativeWorker=False,SMComplete=False,effectiveL=False,productQualification=False))
print(json.dumps(dict(worktree=str(W),changed=git(W,'diff','--name-only').splitlines()),indent=2))
