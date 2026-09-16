import {readFileSync,writeFileSync} from 'node:fs';
import {parseExact} from '../subject/dist/exact-json.js';
import {SchemaRegistry} from '../subject/dist/schema.js';
const arch='/Users/sb/code/opensip-ai/opensip_arch/';
const pins=JSON.parse(readFileSync(arch+'docs/implementation/m1/metadata-v2/sources.json','utf8'));
const reg=new SchemaRegistry(pins.schemas.map(p=>parseExact(readFileSync(arch+p.path))));
const values=readFileSync(new URL('harvest-values.jsonl',import.meta.url),'utf8').split('\n').slice(0,-1).map(l=>parseExact(new TextEncoder().encode(l)));
const rows=JSON.parse(readFileSync(new URL('harvest-rows.json',import.meta.url),'utf8'));
const mism=[];let valid=0,limits=0;
for(const [r,i,py] of rows){let ts;try{ts=reg.matches(r,values[i]);}catch(e){ts=e.constructor.name+': '+e.message;if(e.constructor.name==='ShapeLimit')limits++;} if(ts===true)valid++; if(ts!==py)mism.push({ref:r,index:i,ts,py});}
const out={values:values.length,rows:rows.length,tsValid:valid,shapeLimits:limits,mismatches:mism.length,sample:mism.slice(0,20)};
writeFileSync(new URL('harvest-diff.json',import.meta.url),JSON.stringify(out,null,1));console.log(JSON.stringify(out).slice(0,3000));
