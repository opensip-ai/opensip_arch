import {readFileSync,writeFileSync} from 'node:fs';
import {parseExact} from '../subject/dist/exact-json.js';
import {SchemaRegistry} from '../subject/dist/schema.js';
const arch='/Users/sb/code/opensip-ai/opensip_arch/';
const pins=JSON.parse(readFileSync(arch+'docs/implementation/m1/metadata-v2/sources.json','utf8'));
const reg=new SchemaRegistry(pins.schemas.map(p=>parseExact(readFileSync(arch+p.path))));
const f=parseExact(readFileSync(new URL('harvest-cases.json',import.meta.url)));
const mism=[];let n=0;
for(const [r,i,py] of f.rows){n++;let ts;try{ts=reg.matches(r,f.values[Number(i)]);}catch(e){ts=e.constructor.name+': '+e.message;} if(ts!==py)mism.push({ref:r,index:Number(i),ts,py});}
const out={rows:n,mismatches:mism.length,sample:mism.slice(0,20)};
writeFileSync(new URL('harvest-diff.json',import.meta.url),JSON.stringify(out,(k,v)=>typeof v==='bigint'?v.toString():v,1));console.log(JSON.stringify(out,(k,v)=>typeof v==='bigint'?v.toString():v).slice(0,3000));
