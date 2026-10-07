"""Run the unchanged accepted generator pipeline on unfrozen candidate inputs.
This is development generation, not design selection or public drift acceptance.
"""
import pathlib,json,hashlib,importlib.util,types
b=pathlib.Path('/tmp/opensip-implementation/x4tc-authoring');c=b/'product';out=b/'generation-prospective'
def load(path,name):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def dig(raw):return dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
cl=json.loads((c/'tools/contracts/generator-closure.json').read_text());pinned={}
for r in cl['files']:
 raw=(c/r['path']).read_bytes();assert dig(raw)=={k:r[k] for k in ['bytes','sha256']},r['path'];pinned[r['path']]=raw
reg=json.loads((c/'schemas/registry.json').read_text());recipe=reg['recipes'][0];assert recipe['generatorClosureSha256']==dig((c/'tools/contracts/generator-closure.json').read_bytes())['sha256'];assert set(recipe['sourceSha256s'])=={r['sourceSha256'] for r in reg['sources']}
tools=json.loads(pinned['tools/contracts/toolchain.json'])['executables'];assert tools==cl['toolchain'];load(c/'tools/contracts/adapter.py','x4tc_adapter').validate_build_receipt(json.loads(pinned['tools/contracts/build-receipt.json']),pinned,tools['generator'])
args=types.SimpleNamespace(root=c,output=out,node=pathlib.Path('/Users/sb/.nvm/versions/node/v24.16.0/bin/node'),generator=pathlib.Path('/Users/sb/opensip-deps/contracts-generator-rebuild-02/opensip-contract-generator'),python=pathlib.Path('/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/Resources/Python.app/Contents/MacOS/Python'))
result=json.loads((out/'result.json').read_text());assert json.loads((out/'input-closure.json').read_text())['files']==cl['files']
root=out/result['outputRoot'];changed=[]
for row in recipe['outputs']:
 old=(c/row['path']).read_bytes();new=(root/row['path']).read_bytes()
 if old!=new:changed.append(dict(path=row['path'],before=dig(old),after=dig(new)))
assert result['passed'] and sorted(r['path'] for r in changed)==['apps/report/src/generated/report.ts','crates/contracts/src/generated/evidence.rs'],changed
for row in changed:(c/row['path']).write_bytes((root/row['path']).read_bytes())
(b/'generation-summary.json').write_text(json.dumps(dict(passed=True,standing='UNSELECTED PROSPECTIVE DEVELOPMENT GENERATION; NO PUBLIC DRIFT/ACCEPTANCE/QUALIFICATION',changed=changed,totalOutputs=len(recipe['outputs']),productEdited=False,exactPipelineUnchanged=True),indent=2)+'\n');print('prospective generation passed; two generated outputs copied to candidate only')
