import hashlib, importlib.util, json, pathlib, types
base=pathlib.Path('/tmp/opensip-implementation/jbs-product-authoring')
root=base/'product';trusted=pathlib.Path('/Users/sb/code/opensip-ai/opensip/tools/contracts/pipeline.py')
spec=importlib.util.spec_from_file_location('candidate_pipeline',trusted)
pipeline=importlib.util.module_from_spec(spec);spec.loader.exec_module(pipeline)
sha=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
closure=json.loads((root/'tools/contracts/generator-closure.json').read_bytes())
args=types.SimpleNamespace(root=root,output=base/'generate-candidate-1',node=pathlib.Path('/Users/sb/opensip-deps/native-repin-01/runs/check-1/tool-node'),generator=pathlib.Path('/Users/sb/opensip-deps/contracts-generator-rebuild-02/opensip-contract-generator'),python=pathlib.Path('/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/Resources/Python.app/Contents/MacOS/Python'))
result=pipeline.run(args,selected_closure=closure['files'],provenance={'registrySha256':sha(root/'schemas/registry.json'),'generatorClosureSha256':sha(root/'tools/contracts/generator-closure.json')})
changed=[]
for row in result['outputs']:
 target=root/row['path'];source=args.output/result['outputRoot']/row['path']
 if target.read_bytes()!=source.read_bytes():changed.append(row['path']);target.write_bytes(source.read_bytes())
policy_path=root/'tools/contracts/dependency-policy.json';policy=json.loads(policy_path.read_bytes());policy_changed=[]
for row in policy['localSources']:
 p=root/'crates/contracts'/row['path'];current={'path':row['path'],'bytes':len(p.read_bytes()),'sha256':sha(p)}
 if current!=row:policy_changed.append(row['path']);row.update(current)
assert policy_changed==['src/generated/invocation.rs'],policy_changed
policy_path.write_text(json.dumps(policy,indent=2)+'\n')
(base/'generation.json').write_text(json.dumps({'candidateOnly':True,'repositoryEdited':False,'passed':True,'changedGenerated':changed,'changedDependencyPolicyMembers':policy_changed,'result':result},indent=2)+'\n')
print(json.dumps({'passed':True,'changedGenerated':changed,'changedDependencyPolicyMembers':policy_changed}))
