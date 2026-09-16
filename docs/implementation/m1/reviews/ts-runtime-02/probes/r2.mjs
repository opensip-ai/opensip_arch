import vm from 'node:vm';
import {readFileSync} from 'node:fs';
import { parseExact, canonical, JsonError, MAX_BYTES } from '../subject/dist/exact-json.js';
import { SchemaRegistry, SchemaError, ShapeLimit } from '../subject/dist/schema.js';
const S='https://json-schema.org/draft/2020-12/schema';
const out={};const run=(n,f)=>{try{out[n]=f();}catch(e){out[n]='THROW '+e.constructor.name+': '+e.message;}};
const reg=new SchemaRegistry([
 {$schema:S,$id:'urn:items',type:'array',items:{type:'string'}},
 {$schema:S,$id:'urn:obj',type:'object',properties:{a:{type:'string'}},required:['a'],additionalProperties:false},
 {$schema:S,$id:'urn:any',type:['array','object','string','integer','null','boolean']},
]);
// review-01 bypasses
run('arrayProtoBypass',()=>{const a=[1n,2n];Object.setPrototypeOf(a,Object.create(Array.prototype,{every:{value:()=>true}}));return reg.matches('urn:items',a);});
run('arraySubclass',()=>{class X extends Array{every(){return true}};return reg.matches('urn:items',X.from([1n]));});
run('proxyGetInvalidToValid',()=>reg.matches('urn:obj',new Proxy({a:5n},{get:(o,k)=>k==='a'?'x':Reflect.get(o,k)})));
run('proxyArrayEvery',()=>reg.matches('urn:items',new Proxy([1n],{get:(o,k)=>k==='every'?()=>true:Reflect.get(o,k)})));
// descriptor-lying Proxy (outside contract): snapshot is still self-consistent
run('proxyDescriptorLie',()=>reg.matches('urn:obj',new Proxy({a:5n},{getOwnPropertyDescriptor:(o,k)=>k==='a'?{value:'x',writable:true,enumerable:true,configurable:true}:Reflect.getOwnPropertyDescriptor(o,k)})));
run('proxyArrayProtoTrap',()=>reg.matches('urn:items',new Proxy(['x'],{getPrototypeOf:()=>Array.prototype})));
// mutation after snapshot cannot matter: mutate inside a schema? n/a; mutate during canonical via proxy
run('mutateDuringCanonical',()=>{const t={a:'x'};const p=new Proxy(t,{ownKeys(o){o.a=5n;return Reflect.ownKeys(o);}});return reg.matches('urn:obj',p);});
// cross-realm
const ctx=vm.createContext({});
run('crossRealmArray',()=>reg.matches('urn:any',vm.runInContext('["x"]',ctx)));
run('crossRealmObject',()=>reg.matches('urn:any',vm.runInContext('({a:"x"})',ctx)));
run('crossRealmU8',()=>parseExact(vm.runInContext('new Uint8Array([49])',ctx)));
run('crossRealmSABinLocalU8',()=>String(parseExact(new Uint8Array(vm.runInContext('(()=>{const s=new SharedArrayBuffer(1);new Uint8Array(s)[0]=49;return s})()',ctx)))));
run('localSAB',()=>parseExact(new Uint8Array(new SharedArrayBuffer(1))));
run('growableSAB',()=>parseExact(new Uint8Array(new SharedArrayBuffer(1,{maxByteLength:4}))));
run('resizableAB',()=>{const b=new ArrayBuffer(1,{maxByteLength:4});new Uint8Array(b)[0]=49;return String(parseExact(new Uint8Array(b)));});
run('bufferSubclass',()=>String(parseExact(Buffer.from('12'))));
run('nullProtoArray',()=>{const a=['x'];Object.setPrototypeOf(a,null);return reg.matches('urn:items',a);});
run('frozenValue',()=>reg.matches('urn:obj',Object.freeze({a:'x'})));
run('nullProtoObj',()=>{const o=Object.create(null);o.a='x';return reg.matches('urn:obj',o);});
// A2 extras
const bad=(n,s)=>run(n,()=>new SchemaRegistry([{$schema:S,$id:'urn:b',...s}]).matches('urn:b',{}));
bad('typeArrayDup',{type:['string','string']});bad('nestedIdOther',{properties:{a:{$id:'urn:other'}}});bad('nestedSchemaOther',{properties:{a:{$schema:'x'}}});
bad('patternPropsUnknown',{patternProperties:{'^z':true}});bad('propertiesNonObject',{properties:[]});bad('byExtraKey',{'x-opensip-order':{by:['a'],x:1n}});
bad('maxLengthHuge',{maxLength:18446744073709551615n});bad('minimumNeg',{minimum:-9223372036854775808n});bad('enumNestedDup',{enum:[{a:1n,b:2n},{b:2n,a:1n}]});
bad('defsBadUnreferenced',{$defs:{x:{pattern:1n}}});bad('constAny',{const:{pattern:1n}});bad('refNoHash',{$ref:'urn:b'});
// 4MiB snapshot cost
let parts=[],len=2,i=0;while(true){const p=`"k${i}":"v"`;if(len+p.length+1>MAX_BYTES)break;parts.push(p);len+=p.length+1;i++;}
const big=parseExact(new TextEncoder().encode('{'+parts.join(',')+'}'));
const t=performance.now();run('big4MiB',()=>reg.matches('urn:any',big));out.big4MiBms=Math.round(performance.now()-t);
console.log(JSON.stringify(out,(k,v)=>typeof v==='bigint'?v+'n':v,1));
