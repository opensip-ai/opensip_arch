import { parseExact, canonical, MAX_BYTES } from '../subject/dist/exact-json.js';
import { SchemaRegistry, ShapeLimit } from '../subject/dist/schema.js';
const enc=s=>new TextEncoder().encode(s);const t=(n,f)=>{const s=performance.now();let r;try{r=f();}catch(e){r=e.constructor.name+':'+e.message;}return [n,Math.round(performance.now()-s)+'ms',typeof r==='object'?'ok':String(r)];};
const res=[];
// wide object with many keys near 4MiB
let parts=[],len=2,i=0;while(true){const p=`"k${i}":0`;if(len+p.length+1>MAX_BYTES)break;parts.push(p);len+=p.length+1;i++;}
const wide=enc('{'+parts.join(',')+'}');res.push(['wideKeys',i]);
let v;res.push(t('parseWide',()=>v=parseExact(wide)));res.push(t('canonicalWide',()=>canonical(v)));
const nums=enc('['+Array(Math.floor((MAX_BYTES-2)/2)).fill('0').join(',')+']');let a;res.push(t('parseNums',()=>a=parseExact(nums)),t('canonicalNums',()=>canonical(a)));
const bigstr=enc('['+Array(Math.floor((MAX_BYTES-2)/13)).fill('"\\u00e9\\u00e9"').join(',')+']');res.push(t('parseEscStr',()=>parseExact(bigstr)));
const longnum=enc('1'.repeat(MAX_BYTES));res.push(t('parseLongNum',()=>parseExact(longnum)));
const S='https://json-schema.org/draft/2020-12/schema';
const reg=new SchemaRegistry([{$schema:S,$id:'urn:a',type:'array',items:{type:'integer'},uniqueItems:false},{$schema:S,$id:'urn:o',type:'object',additionalProperties:{type:'integer'}},
 {$schema:S,$id:'urn:u',type:'array',items:{type:'integer'},uniqueItems:true},
 {$schema:S,$id:'urn:exp',$defs:{n:{anyOf:[{type:'string'},{type:'array',items:{$ref:'#/$defs/n'}}]}},$ref:'#/$defs/n'}]);
res.push(t('matchNumsDefault',()=>reg.matches('urn:a',a)));res.push(t('matchWideDefault',()=>reg.matches('urn:o',v)));
res.push(t('matchNumsBigLimit',()=>reg.matches('urn:a',a,1e8)));
const u=Array.from({length:300000},(_, k)=>BigInt(k));res.push(t('unique300k',()=>reg.matches('urn:u',u)));
res.push(['arrayLenAtDefaultLimitRejected', (()=>{for(const n of [400000,499999,500000,600000]){try{reg.matches('urn:a',Array(n).fill(0n));}catch(e){return 'ShapeLimit at n='+n;}}return 'none';})()]);
console.log(JSON.stringify(res));
