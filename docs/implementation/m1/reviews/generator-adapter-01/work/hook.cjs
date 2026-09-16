const M=require('module'),fs=require('fs');const log=[];const orig=M._resolveFilename;
M._resolveFilename=function(r,p,...a){const x=orig.call(this,r,p,...a);log.push('resolve '+r+' -> '+x);return x};
for(const f of ['readFileSync','openSync','statSync','existsSync','readdirSync','realpathSync']){const o=fs[f];fs[f]=function(p,...a){if(typeof p==='string'||p instanceof URL)log.push(f+' '+p);return o.call(this,p,...a)}}
process.on('exit',()=>{const u=[...new Set(log)];require('fs').writeFileSync(process.env.TRACE_OUT||'/dev/stderr',u.join('\n')+'\n')});
