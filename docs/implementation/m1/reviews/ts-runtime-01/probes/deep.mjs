import {readFileSync} from 'node:fs';
import {parseExact, canonical} from '../subject/dist/exact-json.js';
import {SchemaRegistry, ShapeLimit} from '../subject/dist/schema.js';
const arch='/Users/sb/code/opensip-ai/opensip_arch/';
const pins=JSON.parse(readFileSync(arch+'docs/implementation/m1/metadata-v2/sources.json','utf8'));
const reg=new SchemaRegistry(pins.schemas.map(p=>parseExact(readFileSync(arch+p.path))));
const out={};
for(const id of ['urn:opensip:product-v1:policy-document:2','urn:opensip:product-v1:workflows:policy-document']){
 const ref=id+'#/$defs/Predicate';
 // not-chain to max data depth; and-trees with arrays
 let v={op:'not',operand:{}};let cur=v;for(let d=1;d<31;d++){cur.operand={op:'not',operand:{}};cur=cur.operand;}
 let w={};for(let d=0;d<15;d++){w={op:'and',operands:[w,w]};}
 for(const [n,val] of [['notChain31',v],['andTree15',w]]){
  let r;const t=performance.now();try{canonical(val);r=reg.matches(ref,val);}catch(e){r=e.constructor.name+': '+e.message;}
  let lim;try{lim=reg.matches(ref,val,1e9);}catch(e){lim=e.constructor.name;}
  out[id.split(':').pop()+' '+n]={defaultLimit:r,bigLimit:lim,ms:Math.round(performance.now()-t)};
 }
}
console.log(JSON.stringify(out,null,1));
