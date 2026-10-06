"""Read-only source/profile preservation checks; does not execute a parser."""
import json,pathlib,re,hashlib,argparse
q=argparse.ArgumentParser();q.add_argument('--product',required=True);q.add_argument('--candidate',required=True);args=q.parse_args();p=pathlib.Path(args.product);c=pathlib.Path(args.candidate)
def raw(root,rel):return (root/rel).read_bytes()
def pin(root,rel):
 x=raw(root,rel);return dict(bytes=len(x),sha256=hashlib.sha256(x).hexdigest())
old=raw(p,'crates/identity/src/toml.rs').decode();new=raw(c,'crates/identity/src/toml.rs').decode();start='/// Development execution profile:';tests='#[cfg(test)]\nmod tests {';assert old[old.index(start):old.index(tests)]==new[new.index(start):new.index(tests)];assert new[new.index(tests):new.index('#[cfg(test)]\nmod view_tests {')].rstrip()==old[old.index(tests):].rstrip()
rel='crates/identity/src/lib.rs';a=raw(p,rel).decode();b=raw(c,rel).decode();pattern=r'pub use toml::\{[^}]+\};';assert re.sub(pattern,'TOML_EXPORTS',a)==re.sub(pattern,'TOML_EXPORTS',b)
policy='tools/identity/dependency-policy.json';a=json.loads(raw(p,policy));b=json.loads(raw(c,policy));changed=[]
for oldrow,newrow in zip(a['localSources'],b['localSources'],strict=True):
 assert oldrow['path']==newrow['path'];assert {k:newrow[k] for k in ('bytes','sha256')}==pin(c,'crates/identity/'+newrow['path'])
 if oldrow!=newrow:changed.append(newrow['path']);newrow.update(oldrow)
assert changed==['src/lib.rs','src/toml.rs'];assert a==b
assert 'pub struct TomlArrayView' in new and 'pub struct TomlIntegerView' in new;assert 'impl ExactSizeIterator<Item = TomlValueView' in new
assert pin(p,'crates/identity/src/schema_registry.rs')==pin(c,'crates/identity/src/schema_registry.rs');assert pin(p,'Cargo.lock')==pin(c,'Cargo.lock');assert pin(p,'crates/identity/Cargo.toml')==pin(c,'crates/identity/Cargo.toml')
print(json.dumps(dict(parserGrammarAndResourceChecksUnchanged=True,oldParserTestsUnchanged=True,onlyTwoExportedViewTypesAdded=True,policyOnlyTwoLocalSourcePinsChanged=changed,dependenciesAndFeaturesUnchanged=True,sourceRegistryUnchanged=True,parserExecuted=False,ownerAdmissionOrQualification=False),indent=2))
