import pathlib,subprocess,os,tarfile,json,hashlib,shutil,re
p=pathlib.Path('/Users/sb/code/opensip-ai/opensip');b=pathlib.Path('/tmp/opensip-implementation/x4tc-authoring');c=b/'product';d=b/'design';prefix='docs/implementation/m2/continuation-diagnostics-x4tc-r1';assert not c.exists()
e=dict(os.environ,GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null')
for k in ['GIT_CONFIG_COUNT','GIT_DIR','GIT_WORK_TREE']:e.pop(k,None)
assert not subprocess.check_output(['/usr/bin/git','status','--porcelain'],cwd=p,env=e,text=True).strip()
with (b/'product.tar').open('wb') as f:subprocess.run(['/usr/bin/git','archive','HEAD'],cwd=p,env=e,stdout=f,check=True)
c.mkdir()
with tarfile.open(b/'product.tar') as t:t.extractall(c,filter='data')
def dig(x):return dict(bytes=len(x),sha256=hashlib.sha256(x).hexdigest())
def write(rel,x):
 f=c/rel;f.write_text(json.dumps(x,indent=2)+'\n');return f.read_bytes()
source=(d/'schemas/common.v4.schema.json').read_bytes();old=(c/'schemas/sources/common-v4.schema.json').read_bytes();newpin=dict(path=prefix+'/schemas/common.v4.schema.json',**dig(source));(c/'schemas/sources/common-v4.schema.json').write_bytes(source)
sm=json.loads((c/'schemas/source-map.json').read_text());row=next(r for r in sm['sources'] if r['implementationPath']=='schemas/sources/common-v4.schema.json');assert dig(old)=={k:row['architectureSource'][k] for k in ['bytes','sha256']};row['architectureSource']=newpin;write('schemas/source-map.json',sm)
shutil.copyfile(d/'schemas/admission-registry.json',c/'schemas/admission-registry.json')
am=json.loads((c/'schemas/admission-source-map.json').read_text());row=next(r for r in am['sources'] if r['implementationPath']=='schemas/sources/common-v4.schema.json');row['architectureSource']=newpin;am['registryArchitectureSource']=dict(path=prefix+'/schemas/admission-registry.json',**dig((c/'schemas/admission-registry.json').read_bytes()));write('schemas/admission-source-map.json',am)
f=c/'crates/identity/src/schema_registry.rs';raw=f.read_text()
pattern=r'(    SourcePin \{\n        id: "urn:opensip:product-v1:workflows:evaluator3:common:4",\n        path: "schemas/sources/common-v4.schema.json",\n        bytes: )(\d+)(,\n        sha256: \[)([^]]+)(\],\n    \},)'
m=re.search(pattern,raw);assert m and int(m[2])==len(old);assert bytes(int(x.strip()) for x in m[4].split(',') if x.strip())==hashlib.sha256(old).digest()
updated=m[1]+str(len(source))+m[3]+'\n            '+', '.join(map(str,hashlib.sha256(source).digest()))+',\n        '+m[5]
f.write_text(raw[:m.start()]+updated+raw[m.end():])
closure=json.loads((c/'tools/contracts/generator-closure.json').read_text());changed=[]
for row in closure['files']:
 target=c/row['path']
 if not target.exists():
  raw=(p/row['path']).read_bytes();assert dig(raw)=={k:row[k] for k in ['bytes','sha256']},row['path'];target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
for row in closure['files']:
 x=(c/row['path']).read_bytes();h=dig(x)
 if h!={k:row[k] for k in ['bytes','sha256']}:changed.append(row['path']);row.update(h)
assert sorted(changed)==['schemas/source-map.json','schemas/sources/common-v4.schema.json'],changed
cl=write('tools/contracts/generator-closure.json',closure)
registry=json.loads((c/'schemas/registry.json').read_text());rows=[r for r in registry['sources'] if r['sourcePath']=='schemas/sources/common-v4.schema.json'];assert len(rows)==1;rows[0]['sourceSha256']=newpin['sha256'];assert len(registry['recipes'])==1;registry['recipes'][0]['generatorClosureSha256']=dig(cl)['sha256'];registry['recipes'][0]['sourceSha256s']=sorted(r['sourceSha256'] for r in registry['sources']);write('schemas/registry.json',registry)
(b/'materialization-inputs.json').write_text(json.dumps(dict(productBase=subprocess.check_output(['/usr/bin/git','rev-parse','HEAD'],cwd=p,env=e,text=True).strip(),standing='UNFROZEN X4Tc PROSPECTIVE GENERATION INPUTS; NO SELECTION/ACCEPTANCE',generatorClosureChangedPaths=changed,source=newpin,productEdited=False,common1Or3Changed=False),indent=2)+'\n')
print('X4Tc candidate inputs prepared; generator has not run')
