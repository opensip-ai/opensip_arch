"""Exercise actual packaged runner refusal and child failure, in private copies."""
from pathlib import Path
import json,hashlib,shutil,subprocess
ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'copy/tools/typescript-boundary'
NODE='/Users/sb/.nvm/versions/node/v24.16.0/bin/node'
rows=[]
for case in ['wrong-hash','wrong-length','escaping-source','escaping-target','duplicate-target','failing-test','passing-test']:
    dest=ROOT/'controls'/case
    shutil.copytree(SOURCE,dest,ignore=shutil.ignore_patterns('node_modules'))
    (dest/'node_modules').symlink_to(SOURCE/'node_modules',target_is_directory=True)
    map_path=dest/'tests/fixtures/staging-map.json';value=json.loads(map_path.read_text());row=value['files'][0]
    if case=='wrong-hash':row['sha256']='0'*64
    elif case=='wrong-length':row['bytes']+=1
    elif case=='escaping-source':row['path']='../escape.mjs'
    elif case=='escaping-target':row['stagePath']='../escape.mjs'
    elif case=='duplicate-target':value['files'].append(row.copy())
    else:
        row=next(r for r in value['files'] if r['stagePath'].startswith('checker/test/'))
        raw=("import test from 'node:test';\nimport assert from 'node:assert/strict';\ntest('root actual packaged runner child',()=>assert.equal(1,"+('2' if case=='failing-test' else '1')+"));\n").encode()
        (dest/row['path']).write_bytes(raw);row['bytes']=len(raw);row['sha256']=hashlib.sha256(raw).hexdigest();value['files']=[row]
    map_path.write_text(json.dumps(value))
    before={p.resolve() for p in Path('/tmp').glob('opensip-boundary-tests-*')}
    result=subprocess.run([NODE,str(dest/'tests/run.mjs')],capture_output=True,text=True,timeout=30)
    after={p.resolve() for p in Path('/tmp').glob('opensip-boundary-tests-*')}
    # Another full-suite reproduction may concurrently own a stage; only new leftover dirs matter.
    clean=not(after-before)
    expected=0 if case=='passing-test' else 1
    passed=(result.returncode==expected and clean)
    if case in ['wrong-hash','wrong-length']:passed &= 'Fixture source differs' in result.stderr
    if case in ['escaping-source','escaping-target']:passed &= 'Invalid fixture path' in result.stderr
    if case=='duplicate-target':passed &= 'Duplicate fixture target' in result.stderr
    if case=='failing-test':passed &= 'root actual packaged runner child' in result.stdout and 'fail 1' in result.stdout
    rows.append({'case':case,'passed':bool(passed),'exitCode':result.returncode,'noNewStageLeft':clean})
    (ROOT/'results'/f'{case}.stdout').write_text(result.stdout);(ROOT/'results'/f'{case}.stderr').write_text(result.stderr)
(ROOT/'results/runner-controls.json').write_text(json.dumps({'cases':rows,'passed':all(r['passed'] for r in rows)},indent=2)+'\n')
print(json.dumps(rows,indent=2));assert all(r['passed'] for r in rows)
