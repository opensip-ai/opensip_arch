"""Use genuine accepted architecture bindings on a disposable product copy."""
from pathlib import Path
import json,subprocess,hashlib
B=Path(__file__).resolve().parent
ROOT=B/'product'
PY='/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/Resources/Python.app/Contents/MacOS/Python'
NODE='/Users/sb/.nvm/versions/node/v24.16.0/bin/node'
GEN='/tmp/opensip-implementation/m1-generator-build-05/opensip-contract-generator'
ARCH='/Users/sb/code/opensip-ai/opensip_arch'
changed='crates/contracts/src/generated/output.rs'
missing='providers/typescript/src/generated/protocol.ts'
(ROOT/changed).write_bytes((ROOT/changed).read_bytes()+b'\n// private drift control\n')
(ROOT/missing).unlink()
rows=[]
for name,write,expect in [('drift',False,1),('repair',True,0),('clean',False,0),('extra-refusal',True,1)]:
    extra=ROOT/'crates/contracts/src/generated/unselected.rs'
    if name=='extra-refusal':extra.write_text('// preserve unexpected private fixture\n')
    work=B/('public-'+name)
    command=[PY,'-I','-B',str(ROOT/'tools/generate_contracts.py'),'--root',str(ROOT),'--architecture',ARCH,'--output',str(work),'--node',NODE,'--generator',GEN]
    if write:command.append('--write')
    with (B/(name+'.stdout')).open('w') as out,(B/(name+'.stderr')).open('w') as err:
        p=subprocess.run(command,stdout=out,stderr=err,timeout=600)
    result={'case':name,'command':command,'exitCode':p.returncode,'expectedExitCode':expect}
    if name=='extra-refusal':
        result['unexpectedPreserved']=extra.read_text()=='// preserve unexpected private fixture\n'
        result['reason']='undeclared generated output present' in (B/(name+'.stderr')).read_text()
        assert result['unexpectedPreserved'] and result['reason'],result
        extra.unlink() # Remove only the fixture created above, after proving refusal preserves it.
    elif (work/'selection-result.json').exists():
        v=json.loads((work/'selection-result.json').read_text());result['selection']=v
        assert v['generatorClosureSelected'] is True and v['sourceSchemasVerified']==40
        if name in ['drift','repair']:assert set(v['changed'])=={changed,missing,'apps/report/src/generated/report.ts'},v
        else:assert v['changed']==[] and v['passed'] is True,v
    else:raise AssertionError(result)
    rows.append(result);(B/'public-results.json').write_text(json.dumps(rows,indent=2)+'\n')
    print(name,p.returncode,flush=True);assert p.returncode==expect,result
reference=Path('/tmp/opensip-implementation/m1-root-generator04-reproduction/generation-internal-01/assembly/output')
outputs=json.loads((B/'public-clean/result.json').read_text())['outputs'] if (B/'public-clean/result.json').exists() else json.loads((ROOT/'schemas/registry.json').read_text())['recipes'][0]['outputs']
for row in outputs:
    path=row['path'];assert (ROOT/path).read_bytes()==(reference/path).read_bytes(),path
(B/'output-comparison.json').write_text(json.dumps({'generatedOutputsExactReviewed04':8,'privateChangedMissingExtraControls':True,'actualDesignChainUsed':True,'liveProductModified':False},indent=2)+'\n')
