"""(B2) Does the step-3 output-root symlink widen the step-4 child's grants?

Control: real generator + probe TS child. Escape: symlinking generator stub + same probe TS child.
The probe TS child only attempts effects and reports on stderr (exit 1), so nothing is published.
"""
import json
from rebind import *

victim = WORK / 'victim'   # compiled into bin/probe-escape
canary = victim / 'canary.txt'

def reset():
    victim.mkdir(exist_ok=True)
    for p in victim.rglob('*'):
        if p.is_file() and p.name != 'canary.txt': p.unlink()
    canary.write_text('victim canary\n')

TS = r'''const fs=require('node:fs');const r=[];
const t=(n,f)=>{try{const v=f();r.push(n+'='+(v===undefined?'ALLOWED':'ALLOWED:'+JSON.stringify(v)))}catch(e){r.push(n+'='+(e.code||e.message))}};
const out=process.argv[3];
t('lstat-output-root-is-symlink',()=>fs.lstatSync(out).isSymbolicLink());
t('write-via-output-path',()=>fs.writeFileSync(out+'/via-output-path.txt','x'));
t('read-victim-canary-direct',()=>fs.readFileSync(VICTIM+'/canary.txt','utf8'));
t('write-victim-direct',()=>fs.writeFileSync(VICTIM+'/written-by-ts-child.txt','escaped\n'));
t('overwrite-victim-canary-direct',()=>fs.appendFileSync(VICTIM+'/canary.txt','tampered\n'));
process.stderr.write('\n'+r.join('\n')+'\n');process.exit(1);
'''.replace('VICTIM', json.dumps(str(victim.resolve())))

report = {}
for label, gen in [('control-real-generator', GEN), ('escape-symlinking-generator', str(WORK / 'bin/probe-escape'))]:
    reset()
    c = case('b2-' + label, files={'tools/contracts/generate-ts.cjs': TS.encode()}, generator=gen)
    before = snapshot(c)
    r = generate(c, generator=gen)
    report[label] = {**r, 'victimFiles': sorted(p.name for p in victim.iterdir()),
                     'canary': canary.read_text(), 'caseOutputsUnchanged': snapshot(c) == before}
print(json.dumps(report, indent=1))
