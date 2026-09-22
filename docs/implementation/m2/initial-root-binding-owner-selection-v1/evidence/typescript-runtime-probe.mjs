import assert from 'node:assert/strict';
import {createReportShapeRegistry,parseExact} from './report.js';
const registry=createReportShapeRegistry();
const ids=['urn:opensip:product-v1:workflows:common','urn:opensip:product-v1:workflows:evaluator3:common:3','urn:opensip:product-v1:workflows:evaluator3:common:4'];
let checks=0;
for(const code of ['INSTALLATION.DURABILITY_NOT_CHECKED','INSTALLATION.NOT_INITIALIZED']){
 for(const [index,id] of ids.entries()){
  assert.equal(registry.matches(id+'#/$defs/DomainDetailCode',code),index===2);checks++;
 }
}
for(const id of ids){assert.equal(registry.matches(id+'#/$defs/DomainDetailCode','INSTALLATION.UNREGISTERED'),false);checks++;}
const report={schemaFamily:'opensip.product.envelope',schemaMajor:7,kind:'doctor',requestId:'req1_00000000000000000000000000000001',termination:{class:'success'},exitCode:0,doctor:{kind:'doctor',reportProduced:true,defectsFound:0,defects:[{code:'INSTALLATION.DURABILITY_NOT_CHECKED',remedy:'The complete installation is visible; root durability was not checked by this read-only command.'}]}};
const ref='urn:opensip:product-v1:workflows:evaluator3:command-envelope:7#';
// The real generated registry uses exact integer parsing, not JS floating-number records.
const bytes=new TextEncoder().encode(JSON.stringify(report));
assert.equal(registry.matches(ref,parseExact(bytes)),true);checks++;
report.doctor.defectsFound=false;
assert.equal(registry.matches(ref,parseExact(new TextEncoder().encode(JSON.stringify(report)))),false);checks++;
console.log(JSON.stringify({passed:true,checks,standing:'Actual generated TypeScript shape registry only; no native doctor or product UI rendering.'}));
