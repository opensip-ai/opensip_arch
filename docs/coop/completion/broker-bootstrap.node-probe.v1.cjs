// Reference child probe only; never shipped provider logic.
'use strict';
const fs = require('node:fs');
const cp = require('node:child_process');
const key = 'OPENSIP_BROKER_CONTEXT';
const before = {...process.env};
const fixed = ['LC_ALL','LANG','TZ','UV_THREADPOOL_SIZE'];
for (const k of Object.keys(process.env)) if (!fixed.includes(k) && k !== key) delete process.env[k];
const sanitized = {...process.env};
const bootstrap = process.env[key];
delete process.env[key];
const child = cp.spawnSync(process.execPath, ['--no-addons', '--no-global-search-paths', '-e',
 'const raw=Object.keys(process.env).sort(); for(const k of Object.keys(process.env)) if(!["LC_ALL","LANG","TZ","UV_THREADPOOL_SIZE"].includes(k)) delete process.env[k]; process.stdout.write(JSON.stringify({rawKeys:raw,keys:Object.keys(process.env).sort(),brokerPresent:Object.hasOwn(process.env,"OPENSIP_BROKER_CONTEXT")}))'],
 {env:Object.fromEntries(fixed.map(k=>[k,process.env[k]])),cwd:process.cwd(),encoding:'utf8'});
const out = {version:process.version,fullICU:process.config.variables.icu_small === false,
 execArgv:process.execArgv,env:before,sanitized,mode:fs.statSync(process.cwd()).mode & 0o777,
 cwd:process.cwd(),bootstrapConsumed:bootstrap !== undefined && !Object.hasOwn(process.env,key),
 childExit:child.status,child:JSON.parse(child.stdout)};
process.stdout.write(JSON.stringify(out));
