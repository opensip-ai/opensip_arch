import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import {fileURLToPath} from 'node:url';
import {parse,runtimeUsages} from '/tmp/opensip-implementation/m1-typescript-boundary-subject-04/checker/src/usages.mjs';
const H=path.dirname(fileURLToPath(import.meta.url));
const cases=[
 ['implicit-function','define(function(load){load("undeclared-package");});'],
 ['implicit-arrow','define((load)=>load("undeclared-package"));'],
 ['named-implicit-arrow','define("named",(load)=>load("undeclared-package"));'],
 ['implicit-identifier','function factory(load){load("undeclared-package");} define(factory);'],
 ['named-explicit-exports','define("named",["exports"],function(exports){exports.ok=true;});'],
];
const rows=[];
for(const [name,source] of cases){
 const usages=runtimeUsages(parse(name+'.js',source));const calls=[];
 // Small specification model only: omitted dependency arguments default to
 // require/exports/module. No external packages are actually loaded.
 const context=vm.createContext({define:(...args)=>{const factory=args.pop();const dependencies=Array.isArray(args.at(-1))?args.at(-1):['require','exports','module'];factory(...dependencies.map(n=>n==='require'?(request)=>calls.push(request):{}));}});
 vm.runInContext(source,context,{timeout:1000});
 rows.push({name,source,modelRequestedModules:calls,actualExtractor:{requests:usages.requests,loaders:usages.loaders,unsupported:usages.unsupported}});
}
const result={standing:'Actual frozen extractor plus small AMD default-argument model derived from specification; not a complete RequireJS implementation or sandbox proof',source:'https://github.com/amdjs/amdjs-api/blob/master/AMD.md#dependencies',rows};fs.writeFileSync(path.join(H,'result.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result,null,2));
