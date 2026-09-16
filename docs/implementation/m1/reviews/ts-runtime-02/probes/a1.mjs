import {readFileSync,writeFileSync} from 'node:fs';
import {parseExact} from '../subject/dist/exact-json.js';
import {SchemaRegistry} from '../subject/dist/schema.js';
const S='https://json-schema.org/draft/2020-12/schema';
const cases=parseExact(readFileSync(new URL('a1-cases.json',import.meta.url)));
const regs=new Map();const reg=o=>{const k=JSON.stringify(o);if(!regs.has(k))regs.set(k,new SchemaRegistry([{$schema:S,$id:'urn:o',"x-opensip-order":o},{$schema:S,$id:'urn:n',not:{"x-opensip-order":o}}]));return regs.get(k);};
const mism=[];
for(const c of cases){for(const [id,exp] of [['urn:o',c.valid],['urn:n',c.notValid]]){let r;try{r=reg(c.order).matches(id,c.value);}catch(e){r=e.constructor.name+': '+e.message;} if(r!==exp)mism.push({id,order:c.order,value:c.value,ts:r,py:exp});}}
const J=x=>JSON.stringify(x,(k,v)=>typeof v==='bigint'?v.toString()+'n':v);
writeFileSync(new URL('a1-diff.json',import.meta.url),J({cases:cases.length,evaluations:cases.length*2,mismatches:mism.length,all:mism}));
console.log(J({cases:cases.length,evaluations:cases.length*2,mismatches:mism.length,sample:mism.slice(0,8)}));
