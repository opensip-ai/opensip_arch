import {readFileSync,writeFileSync} from 'node:fs';
import {parseExact} from './dist/exact-json.js';
import {SchemaRegistry} from './dist/schema.js';
const arch='/Users/sb/code/opensip-ai/opensip_arch/';
const pins=JSON.parse(readFileSync(arch+'docs/implementation/m1/metadata-v2/sources.json','utf8'));
const registry=new SchemaRegistry(pins.schemas.map(p=>parseExact(readFileSync(arch+p.path))));
const fixture=parseExact(readFileSync(new URL('reference-shapes.json',import.meta.url)));
const errors=[];
for(const c of fixture.cases){let result;try{result=registry.matches(c.ref,fixture.values[Number(c.valueIndex)]);}catch(error){result=error.name+': '+error.message;}
 if(result!==c.valid)errors.push({ref:c.ref,index:Number(c.valueIndex),expected:c.valid,actual:result});}
const result={passed:errors.length===0,cases:fixture.cases.length,mismatches:errors,productQualification:false};
writeFileSync(new URL('shape-differential.json',import.meta.url),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify({cases:result.cases,mismatches:errors.length,sample:errors.slice(0,5)}));
