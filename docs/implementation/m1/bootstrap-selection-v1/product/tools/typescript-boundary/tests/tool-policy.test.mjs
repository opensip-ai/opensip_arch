import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import crypto from 'node:crypto';
import { bindToolPolicy } from '../src/tool-policy.mjs';
import { checkBoundary } from '../src/check.mjs';
const json = value => JSON.stringify(value, null, 2) + '\n';
const sha = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
function fixture() {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'opensip-tool-policy07-'));
  const architecture = path.join(temp, 'arch'), root = path.join(temp, 'product');
  fs.mkdirSync(architecture); fs.mkdirSync(root);
  const write = (dir, rel, value) => { const file = path.join(dir, rel); fs.mkdirSync(path.dirname(file), {recursive:true}); fs.writeFileSync(file, typeof value === 'string' ? value : json(value)); };
  const pin = (dir, rel) => { const raw = fs.readFileSync(path.join(dir, rel)); return {path:rel,sha256:sha(raw),bytes:raw.length}; };
  const own = 'tools/demo', external = own + '/node_modules/vendor/index.cjs';
  const record = {schemaVersion:2,package:'tooling',packageRoot:own,manifest:own+'/package.json',tsconfig:null,inputs:[own+'/entry.cjs'],packageManager:{kind:'fixture-unlocked',lockfile:null},trustedUsages:[]};
  write(root,record.manifest,{name:'tool-demo',type:'commonjs',dependencies:{vendor:'1.0.0'}});
  write(root,record.inputs[0],"require('vendor');\n");
  write(root,own+'/node_modules/vendor/package.json',{name:'vendor',version:'1.0.0',main:'index.cjs'});
  write(root,external,'module.exports = name => require(name);\n');
  const usage = {kind:'dynamic-loader',file:external,sha256:pin(root,external).sha256,line:1,column:26,text:'require(name)',targets:[],reason:'Synthetic pinned compiler-style loader: no invocation or runtime completeness claim.'};
  const policy = {schemaVersion:1,kind:'reviewed-developer-tool-loaders',lane:record,files:[...record.inputs,record.manifest,external].sort().map(p=>pin(root,p)),trustedUsages:[usage],unfollowedDynamicLoaders:[{file:external,line:1,column:26,limitation:'reviewed-tool-code-outside-statically-enumerated-closure'}]};
  const inventory = {standing:'synthetic test only; no acceptance',packages:[{id:'tooling',kind:'tooling',path:'tools',dependencies:[]}],files:[{path:record.manifest,package:'tooling',role:'manifest'},{path:record.inputs[0],package:'tooling',role:'entrypoint'}]};
  write(architecture,'parent.json',inventory);write(architecture,'inventory.json',inventory);
  for (const name of ['record','review','assent']) write(architecture,name+'.json',{fixture:true});
  const inventoryBinding = Object.fromEntries([['parent','parent'],['candidate','inventory'],['record','record'],['review','review'],['assent','assent']].map(([k,n])=>[k,pin(architecture,n+'.json')]));
  const designLock = path.join(root,'design-lock.json');
  const select = () => {
    write(architecture,'policy.json',policy);
    write(architecture,'contract-record.json',{candidates:[pin(architecture,'policy.json')]});
    write(architecture,'subject.json',{files:[pin(architecture,'policy.json')]});
    const binding = {record:pin(architecture,'contract-record.json'),subjectManifest:pin(architecture,'subject.json'),review:pin(architecture,'review.json'),assent:pin(architecture,'assent.json')};
    write(root,'design-lock.json',{inputs:[inventoryBinding.parent],inventorySuccessors:[inventoryBinding],contractSuccessors:[binding]});
  };
  select();
  const args = {architecture,designLock,policyPath:'policy.json',root,record,lane:{standing:'bound',policyId:'tooling'}};
  return {temp,architecture,root,record,policy,select,args,write,pin,external,close:()=>fs.rmSync(temp,{recursive:true,force:true})};
}

test('selected tool policy binding refuses altered authority and source inputs', async t => {
  const cases = [
    ['unselected policy',f=>{const x=JSON.parse(fs.readFileSync(f.args.designLock));x.contractSuccessors=[];f.write(f.root,'design-lock.json',x);},/selected exactly once/],
    ['unbound lane',f=>{f.args.lane.standing='unbound-trial';},/only for bound tooling/],
    ['browser package',f=>{f.args.lane.policyId='report';},/only for bound tooling/],
    ['caller exception',f=>{f.args.record.trustedUsages=[f.policy.trustedUsages[0]];},/no caller exceptions/],
    ['changed manifest',f=>f.write(f.root,f.record.manifest,{name:'changed'}),/pinned bytes differ/],
    ['changed local source',f=>f.write(f.root,f.record.inputs[0],'require("other");'),/pinned bytes differ/],
    ['changed loader file',f=>f.write(f.root,f.external,'module.exports = require("other");'),/pinned bytes differ/],
    ['changed lane input list',f=>{f.args.record={...f.record,inputs:[]};},/lane differs/],
    ['undisclosed empty target',f=>{f.policy.unfollowedDynamicLoaders=[];f.select();},/explicitly disclosed/],
    ['invented guarantee',f=>{f.policy.unfollowedDynamicLoaders[0].limitation='proven-never-called';f.select();},/only permitted/],
    ['duplicate exception site',f=>{f.policy.trustedUsages.push(f.policy.trustedUsages[0]);f.select();},/duplicate/],
    ['omitted file pin',f=>{f.policy.files.pop();f.select();},/exact sorted/],
    ['different usage digest',f=>{f.policy.trustedUsages[0].sha256='0'.repeat(64);f.select();},/file pin differs/],
    ['symlink substitution',f=>{const p=path.join(f.root,f.external);fs.renameSync(p,p+'.old');fs.symlinkSync('index.cjs.old',p);},/symlink/],
    ['extra policy field',f=>{f.policy.enabled=true;f.select();},/unexpected fields/],
    ['duplicate policy selection',f=>{const x=JSON.parse(fs.readFileSync(f.args.designLock));x.contractSuccessors.push(x.contractSuccessors[0]);f.write(f.root,'design-lock.json',x);},/selected exactly once/],
    ['candidate member mismatch',f=>{f.write(f.architecture,'contract-record.json',{candidates:[]});const x=JSON.parse(fs.readFileSync(f.args.designLock));x.contractSuccessors[0].record=f.pin(f.architecture,'contract-record.json');f.write(f.root,'design-lock.json',x);},/selected candidate/],
  ];
  for (const [name,mutate,expected] of cases) await t.test(name,()=>{const f=fixture();try{mutate(f);assert.throws(()=>bindToolPolicy(f.args),expected);}finally{f.close();}});
  const f=fixture();try{const result=bindToolPolicy(f.args);assert.equal(result.unfollowedDynamicLoaders.length,1);assert.equal(result.trustedUsages.length,1);}finally{f.close();}
});

test('full checker discloses selected empty-target tool loader and refuses its stale site', async()=>{
  const f=fixture();try {
    const args={...f.args,toolPolicyPath:'policy.json'};
    const noPolicy=await checkBoundary({...args,toolPolicyPath:undefined});
    assert.equal(noPolicy.passed,false);assert.ok(noPolicy.refusals.some(r=>r.category==='unsupported-loader'));
    const yes=await checkBoundary(args);
    assert.equal(yes.passed,true,JSON.stringify(yes.refusals));assert.equal(yes.selectedToolPolicy.unfollowedDynamicLoaders.length,1);assert.equal(yes.dependencyClosureQualified,false);
    f.policy.trustedUsages[0].column=25;f.policy.unfollowedDynamicLoaders[0].column=25;f.select();
    const stale=await checkBoundary(args);assert.equal(stale.passed,false);assert.ok(stale.refusals.some(r=>r.category==='unsupported-loader'));assert.ok(stale.refusals.some(r=>r.category==='lane-record-invalid'));
  } finally {f.close();}
});

test('inventory pins follow every ordered successor, including the adopted product inventory4 shape', async()=>{
  const f=fixture();try {
    const lock=JSON.parse(fs.readFileSync(f.args.designLock));
    const first=lock.inventorySuccessors[0];
    f.write(f.architecture,'inventory2.json',JSON.parse(fs.readFileSync(path.join(f.architecture,'inventory.json'))));
    lock.inventorySuccessors.push({...first,parent:first.candidate,candidate:f.pin(f.architecture,'inventory2.json')});
    f.write(f.root,'design-lock.json',lock);
    const result=await checkBoundary({...f.args,toolPolicyPath:'policy.json'});
    assert.equal(result.passed,true,JSON.stringify(result.refusals));assert.equal(result.inventoryBinding.inventorySuccessorsVerified,2);
    lock.inventorySuccessors[1].parent=first.parent;f.write(f.root,'design-lock.json',lock);
    await assert.rejects(()=>checkBoundary({...f.args,toolPolicyPath:'policy.json'}),/immediate predecessor/);
    lock.inventorySuccessors[1].parent=first.candidate;f.write(f.root,'design-lock.json',lock);
    f.write(f.architecture,'parent.json',{changed:true});
    await assert.rejects(()=>checkBoundary({...f.args,toolPolicyPath:'policy.json'}),/pinned bytes differ/);
  } finally {f.close();}
});

test('finite trusted targets remain subject to ordinary ownership checks', async()=>{
  const f=fixture();try {
    const target='tools/demo/target.cjs';f.write(f.root,target,"require('../../other/private.cjs');\n");f.write(f.root,'tools/other/private.cjs','module.exports=1;\n');
    f.record.inputs.push(target);f.policy.trustedUsages[0].targets=[target];f.policy.unfollowedDynamicLoaders=[];
    f.policy.files=[...f.record.inputs,f.record.manifest,f.external].sort().map(p=>f.pin(f.root,p));
    const inv=JSON.parse(fs.readFileSync(path.join(f.architecture,'inventory.json')));inv.files.push({path:target,package:'tooling',role:'model'});f.write(f.architecture,'inventory.json',inv);
    f.select();const lock=JSON.parse(fs.readFileSync(f.args.designLock));lock.inventorySuccessors[0].candidate=f.pin(f.architecture,'inventory.json');f.write(f.root,'design-lock.json',lock);
    const result=await checkBoundary({...f.args,toolPolicyPath:'policy.json'});
    assert.equal(result.passed,false);assert.ok(result.refusals.some(r=>r.category==='lane-escape'),JSON.stringify(result.refusals));
    assert.equal(result.selectedToolPolicy.unfollowedDynamicLoaders.length,0);
  } finally {f.close();}
});
