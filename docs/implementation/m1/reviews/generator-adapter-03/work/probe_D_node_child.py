"""(D) Real parent + pinned Node step-2 child with probe validate-schemas.cjs (rebound)."""
import json, socket, threading
from rebind import *

victim = WORK / 'victim-node'; victim.mkdir(exist_ok=True)
canary = victim / 'canary.txt'; canary.write_text('node victim canary\n')
listener = socket.socket(); listener.bind(('127.0.0.1', 0)); listener.listen(4)
port = listener.getsockname()[1]; accepted = []
threading.Thread(target=lambda: [accepted.append(listener.accept()) for _ in range(4)], daemon=True).start()

JS = r'''const fs=require('node:fs'),net=require('node:net'),cp=require('node:child_process'),dns=require('node:dns');
const r=[];const t=(n,f)=>{try{const v=f();r.push(n+'='+(v===undefined?'ALLOWED':'ALLOWED:'+JSON.stringify(v).slice(0,60)))}catch(e){r.push(n+'='+(e.code||e.message))}};
const [input,scratch]=process.argv.slice(2);
t('read-outside-canary',()=>fs.readFileSync(OUTSIDE,'utf8'));
t('create-outside',()=>fs.writeFileSync(VICTIM+'/node-written','x'));
t('write-inputs-options',()=>fs.writeFileSync(input+'/options.json','{}'));
t('write-code-generate-ts',()=>fs.writeFileSync(__dirname+'/generate-ts.cjs','//'));
t('read-home-listing',()=>fs.readdirSync('/Users/sb').length);
t('read-parent-work-profile',()=>fs.readFileSync(require('node:path').join(input,'..','child-profile.sb'),'utf8').length);
t('spawnSync-bin-sh',()=>{const x=cp.spawnSync('/bin/sh',['-c','exit 0']);if(x.error)throw x.error;return x.status});
t('spawnSync-self',()=>{const x=cp.spawnSync(process.execPath,['-e','0']);if(x.error)throw x.error;return [x.status,x.signal]});
t('hardlink-input-into-scratch',()=>fs.linkSync(input+'/options.json',scratch+'/hl'));
t('rmdir-scratch-root',()=>{for(const n of fs.readdirSync(scratch))fs.rmSync(scratch+'/'+n,{recursive:true});fs.rmdirSync(scratch)});
t('symlink-at-scratch-root',()=>fs.symlinkSync(VICTIM,scratch));
const s=net.connect({host:'127.0.0.1',port:PORT});
const finish=()=>dns.lookup('example.com',e=>{r.push('dns-lookup='+(e?e.code:'ALLOWED'));process.stderr.write('\n'+r.join('\n')+'\n');process.exit(1)});
s.on('connect',()=>{r.push('tcp-loopback=ALLOWED');finish()});s.on('error',e=>{r.push('tcp-loopback='+e.code);finish()});
'''.replace('OUTSIDE', json.dumps(str(canary.resolve()))).replace('VICTIM', json.dumps(str(victim.resolve()))).replace('PORT', str(port))

c = case('D-node-step2', files={'tools/contracts/validate-schemas.cjs': JS.encode()})
before = snapshot(c)
r = generate(c)
import time; time.sleep(0.3)
print(json.dumps({**r, 'listenerAccepted': len(accepted), 'victimFiles': sorted(p.name for p in victim.iterdir()),
                  'canary': canary.read_text(), 'caseOutputsUnchanged': snapshot(c) == before}, indent=1))
