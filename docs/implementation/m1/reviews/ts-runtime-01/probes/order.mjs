import {readFileSync,writeFileSync} from 'node:fs';
import {parseExact} from '../subject/dist/exact-json.js';
import {SchemaRegistry} from '../subject/dist/schema.js';
const arch='/Users/sb/code/opensip-ai/opensip_arch/';
const pins=JSON.parse(readFileSync(arch+'docs/implementation/m1/metadata-v2/sources.json','utf8'));
const reg=new SchemaRegistry(pins.schemas.map(p=>parseExact(readFileSync(arch+p.path))));
const cases=parseExact(readFileSync(new URL('order-cases.json',import.meta.url)));
const mism=[];const kinds={};
for(const c of cases){let r;try{r=reg.matches(c.ref,c.value);}catch(e){r=e.constructor.name+': '+e.message;}
 if(r!==c.valid){const k=String(r)+' vs py '+c.valid;kinds[k]=(kinds[k]||0)+1;mism.push({ref:c.ref,order:c.order,value:c.value,ts:r,py:c.valid});}}
const J=(x)=>JSON.stringify(x,(k,v)=>typeof v==='bigint'?Number(v):v,1);
writeFileSync(new URL('order-diff.json',import.meta.url),J({cases:cases.length,mismatches:mism.length,kinds,all:mism}));
console.log(J({cases:cases.length,mismatches:mism.length,kinds,refs:[...new Set(mism.map(m=>m.ref))].length,sample:mism.slice(0,6)}));
