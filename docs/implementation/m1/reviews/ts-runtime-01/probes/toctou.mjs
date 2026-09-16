import { SchemaRegistry } from '../subject/dist/schema.js';
const S='https://json-schema.org/draft/2020-12/schema';
const reg=new SchemaRegistry([{$schema:S,$id:'urn:obj',type:'object',properties:{a:{type:'string'}},required:['a'],additionalProperties:false}]);
const target={a:5n};
const p=new Proxy(target,{get:(o,k)=>k==='a'?'x':Reflect.get(o,k)});
let flip=0;const live={a:5n};
const q=new Proxy(live,{getOwnPropertyDescriptor:(o,k)=>Reflect.getOwnPropertyDescriptor(o,k),get:(o,k)=>{flip++;return k==='a'?'ok':o[k];}});
console.log(JSON.stringify({invalidReportedValid:reg.matches('urn:obj',p),snapshotWouldSee:typeof target.a,getTrapCalls:flip,second:reg.matches('urn:obj',q)}));
