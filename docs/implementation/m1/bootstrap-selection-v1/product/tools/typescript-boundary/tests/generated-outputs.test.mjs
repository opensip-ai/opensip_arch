// Synthetic inventory pins exercise checker mechanics only. They are never
// semantic approval, a product design lock, or public-wrapper activation.
import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import crypto from 'node:crypto';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {checkBoundary} from '../src/check.mjs';
const json=value=>JSON.stringify(value,null,2)+'\n';
const tsc=fileURLToPath(new URL('../bin/tsc',import.meta.resolve('typescript')));
function fixture(t,browser=false,bom=false){
 const temp=fs.realpathSync(fs.mkdtempSync(path.join(os.tmpdir(),'opensip-generated-output09-')));
 t.after(()=>fs.rmSync(temp,{recursive:true,force:true}));
 const root=path.join(temp,'product'),architecture=path.join(temp,'architecture');fs.mkdirSync(root);fs.mkdirSync(architecture);
 const own=browser?'apps/report':'providers/typescript',id=browser?'report':'typescript-provider';
 const write=(base,name,value)=>{const p=path.join(base,name);fs.mkdirSync(path.dirname(p),{recursive:true});fs.writeFileSync(p,typeof value==='string'?value:json(value));};
 const inputs=[own+'/src/helper.ts',own+'/src/index.ts'];
 const record={schemaVersion:2,package:id,packageRoot:own,manifest:own+'/package.json',tsconfig:own+'/tsconfig.json',inputs,packageManager:{kind:'fixture-unlocked',lockfile:null},trustedUsages:[]};
 write(root,record.manifest,{name:browser?'@fixture/report':'@fixture/provider',private:true,type:'module'});
 write(root,record.tsconfig,{compilerOptions:{strict:true,target:'ES2022',module:browser?'ESNext':'NodeNext',moduleResolution:browser?'Bundler':'NodeNext',types:[],lib:['ES2022','DOM'],rootDir:'src',outDir:'dist',emitBOM:bom},include:['src/**/*.ts']});
 write(root,inputs[0],'export const value:number = 42;\n');
 write(root,inputs[1],'import {value} from "./helper.js";\nexport const answer=value;\nexport const url=new URL("./helper.js",import.meta.url);\n');
 const inventory={standing:'synthetic mechanics only; no acceptance',packages:[{id,path:own,kind:'typescript-package',dependencies:[]}],files:[...inputs,record.manifest,record.tsconfig].map(p=>({path:p,package:id,role:p.endsWith('.ts')?'model':'configuration'}))};
 write(architecture,'parent.json',inventory);write(architecture,'inventory.json',inventory);
 for(const name of ['record','review','assent'])write(architecture,name+'.json',{fixture:true});
 const pin=name=>{const raw=fs.readFileSync(path.join(architecture,name));return {path:name,bytes:raw.length,sha256:crypto.createHash('sha256').update(raw).digest('hex')}};
 const binding=Object.fromEntries([['parent','parent'],['candidate','inventory'],['record','record'],['review','review'],['assent','assent']].map(([key,name])=>[key,pin(name+'.json')]));
 const designLock=path.join(root,'design-lock.json');write(root,'design-lock.json',{inputs:[binding.parent],inventorySuccessors:[binding],contractSuccessors:[]});
 return {root,own,record,write,args:{root,architecture,designLock,record},output:path.join(root,own,'dist/helper.js'),
  compile(allowErrors=false){const p=spawnSync(process.execPath,[tsc,'--project',path.join(root,record.tsconfig)],{encoding:'utf8'});if(!allowErrors)assert.equal(p.status,0,p.stdout+p.stderr);assert.ok(fs.existsSync(this.output));return p;}};
}
function hasOutputRefusal(result,file){return result.refusals.some(r=>r.category==='undeclared-local'&&r.file===file);}
for(const browser of [false,true])test(`${browser?'browser':'Node'} clean and built lanes have the same source edges`,async t=>{
 const f=fixture(t,browser);const clean=await checkBoundary(f.args);assert.equal(clean.passed,true,json(clean.refusals));assert.equal(clean.stats.verifiedGeneratedFiles,0);
 f.compile();const built=await checkBoundary(f.args);assert.equal(built.passed,true,json(built.refusals));assert.equal(built.stats.verifiedGeneratedFiles,2);
 assert.ok(built.edges.some(e=>e.graph==='runtime'&&e.kind==='import'&&e.resolved===f.own+'/src/helper.ts'&&e.emittedOutput===f.own+'/dist/helper.js'));
 assert.ok(built.edges.some(e=>e.kind==='asset-url'&&e.resolved===f.own+'/src/helper.ts'&&e.emittedOutput===f.own+'/dist/helper.js'));
});
test('exact byte-order-mark output is recognized',async t=>{const f=fixture(t,false,true);f.compile();assert.equal(fs.readFileSync(f.output).subarray(0,3).toString('hex'),'efbbbf');const r=await checkBoundary(f.args);assert.equal(r.passed,true,json(r.refusals));assert.equal(r.stats.verifiedGeneratedFiles,2);});
for (const browser of [false,true]) test(`${browser?'browser':'Node'} changed generated output refuses and is neither scanned nor executed`,async t=>{
 const f=fixture(t,browser);f.compile();const marker=path.join(f.root,'executed');fs.appendFileSync(f.output,`\nimport fs from 'node:fs';fs.writeFileSync(${JSON.stringify(marker)},'bad');\n`);
 const r=await checkBoundary(f.args);assert.equal(r.passed,false);assert.ok(hasOutputRefusal(r,f.own+'/dist/helper.js'));assert.equal(fs.existsSync(marker),false);assert.ok(!r.edges.some(e=>e.from===f.own+'/dist/helper.js'),json(r.edges.filter(e=>e.from===f.own+'/dist/helper.js')));
});
test('extra output is refused even when its bytes equal a valid output',async t=>{const f=fixture(t);f.compile();fs.copyFileSync(f.output,path.join(f.root,f.own,'dist/extra.js'));const r=await checkBoundary(f.args);assert.equal(r.passed,false);assert.ok(hasOutputRefusal(r,f.own+'/dist/extra.js'));});
test('symlinked output is refused despite matching target bytes',async t=>{const f=fixture(t);f.compile();const outside=path.join(f.root,'same.js');fs.copyFileSync(f.output,outside);fs.unlinkSync(f.output);fs.symlinkSync(outside,f.output);const r=await checkBoundary(f.args);assert.equal(r.passed,false);assert.ok(hasOutputRefusal(r,f.own+'/dist/helper.js'));});
test('partial build retains clean-source analysis without inventing a runtime-ready claim',async t=>{const f=fixture(t);f.compile();fs.unlinkSync(f.output);const r=await checkBoundary(f.args);assert.equal(r.passed,true,json(r.refusals));assert.equal(r.stats.verifiedGeneratedFiles,1);assert.equal(r.dependencyClosureQualified,false);});
test('stale output after source change refuses until rebuilt',async t=>{const f=fixture(t);f.compile();f.write(f.root,f.own+'/src/helper.ts','export const value:number = 43;\n');let r=await checkBoundary(f.args);assert.equal(r.passed,false);assert.ok(hasOutputRefusal(r,f.own+'/dist/helper.js'));f.compile();r=await checkBoundary(f.args);assert.equal(r.passed,true,json(r.refusals));});
test('exact compiled browser output still cannot admit Node builtins',async t=>{const f=fixture(t,true);f.write(f.root,f.own+'/src/helper.ts','import "node:fs";\nexport const value:number=42;\n');f.compile(true);const r=await checkBoundary(f.args);assert.equal(r.passed,false);assert.ok(r.refusals.some(x=>x.category==='browser-node'),json(r.refusals));});
