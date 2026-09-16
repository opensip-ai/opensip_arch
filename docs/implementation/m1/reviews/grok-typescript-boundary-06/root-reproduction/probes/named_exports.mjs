import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
import {createBrowserResolver} from '../copy/checker/src/browser-scanner.mjs';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../copy/work/named-exports');
const pkg=path.join(root,'node_modules/ex');fs.mkdirSync(pkg,{recursive:true});
fs.writeFileSync(path.join(pkg,'package.json'),JSON.stringify({name:'ex',version:'1.0.0',exports:{'.':{import:'./esm.js',require:'./cjs.js',default:'./cjs.js'}}}));
fs.writeFileSync(path.join(pkg,'esm.js'),'export const k="esm";');fs.writeFileSync(path.join(pkg,'cjs.js'),'module.exports={k:"cjs"};');
fs.writeFileSync(path.join(root,'entry.mjs'),'');fs.writeFileSync(path.join(root,'entry.cjs'),'');
const resolver=await createBrowserResolver(root);
let results;
try {
 const imp=await resolver.resolve('ex',path.join(root,'entry.mjs'),'import');
 const req=await resolver.resolve('ex',path.join(root,'entry.cjs'),'require');
 assert.equal(imp.kind,'resolved');assert.equal(imp.path,fs.realpathSync(path.join(pkg,'esm.js')));
 assert.equal(req.kind,'resolved');assert.equal(req.path,fs.realpathSync(path.join(pkg,'cjs.js')));
 results={passed:true,checks:2,imp,req,standing:'Root named-package reproduction; the original two dot-request expectation failures remain preserved.'};
}finally {await resolver.dispose();}
fs.writeFileSync(path.resolve(root,'../../../results/named-exports.json'),JSON.stringify(results,null,2)+'\n');console.log(JSON.stringify(results));
