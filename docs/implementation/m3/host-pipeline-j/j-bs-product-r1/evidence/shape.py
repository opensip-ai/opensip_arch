import importlib.util,json,pathlib
base=pathlib.Path('/tmp/opensip-implementation/jbs-product-authoring');root=base/'product'
def module(name):
 spec=importlib.util.spec_from_file_location('shape_'+name,root/('tools/contracts/'+name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
admission=module('admission');confine=module('confine');admission.verify_confinement(json.loads((root/'tools/contracts/confinement-profile.json').read_bytes()))
runtime=base/'shape-runtime';runtime.mkdir(exist_ok=True);node=pathlib.Path('/Users/sb/opensip-deps/native-repin-01/runs/check-1/tool-node')
policy=admission.child_profile(node,[root,base/'shape.cjs'],[runtime]);profile=base/'shape-profile.sb';profile.write_text(policy)
status,out,err,failure=confine.capture_child(['/usr/bin/sandbox-exec','-f',str(profile),str(node),str(base/'shape.cjs'),str(root)],cwd=runtime,env={'PATH':'/usr/bin:/bin','LANG':'C','LC_ALL':'C','TZ':'UTC'})
(base/'shape.stdout').write_bytes(out);(base/'shape.stderr').write_bytes(err)
assert status==0 and not failure,(status,failure,err.decode()[-1500:]);result=json.loads(out);assert result['passed'];(base/'shape-checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
