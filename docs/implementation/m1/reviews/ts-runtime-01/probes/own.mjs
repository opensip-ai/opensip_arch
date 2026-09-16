import { parseExact, canonical, JsonError } from '../subject/dist/exact-json.js';
import { SchemaRegistry, SchemaError, ShapeLimit } from '../subject/dist/schema.js';
const S='https://json-schema.org/draft/2020-12/schema';
const out={};
const run=(name,f)=>{try{out[name]=f();}catch(e){out[name]='THROW '+e.constructor.name+': '+e.message;}};
const reg=new SchemaRegistry([
 {$schema:S,$id:'urn:items',type:'array',items:{type:'string'}},
 {$schema:S,$id:'urn:obj',type:'object',properties:{a:{type:'string'}},required:['a'],additionalProperties:false},
 {$schema:S,$id:'urn:utf8',type:'array','x-opensip-order':'utf8'},
 {$schema:S,$id:'urn:notutf8',not:{'x-opensip-order':'utf8'}},
 {$schema:S,$id:'urn:anyutf8',anyOf:[{'x-opensip-order':'utf8'},{type:'array'}]},
 {$schema:S,$id:'urn:by',type:'array','x-opensip-order':{by:['k']}},
 {$schema:S,$id:'urn:enumobj',enum:[1n]},
 {$schema:S,$id:'urn:enumbad',enum:1n},
 {$schema:S,$id:'urn:reqbad',type:'object',required:'a'},
 {$schema:S,$id:'urn:typenum',type:'number'},
 {$schema:S,$id:'urn:patbad',pattern:1n},
 {$schema:S,$id:'urn:minbad',minimum:'5'},
 {$schema:S,$id:'urn:refbad',$ref:1n},
 {$schema:S,$id:'urn:cyc2',allOf:[{$ref:'urn:cyc2'}]},
 {$schema:S,$id:'urn:ordinal',type:'array','x-opensip-order':'ordinal'},
]);
// 1. custom Array prototype passes canonical, overrides every/some
run('arrayProtoBypass',()=>{const a=[1n,2n];Object.setPrototypeOf(a,Object.create(Array.prototype,{every:{value:()=>true}}));canonical(a);return reg.matches('urn:items',a);});
run('arraySubclass',()=>{class X extends Array{every(){return true}};const a=X.from([1n]);return reg.matches('urn:items',a);});
// 2. Proxy TOCTOU: data descriptors during canonical, different values on get
run('proxyToctou',()=>{let n=0;const t={a:'x'};const p=new Proxy(t,{get(o,k){n++;return k==='a'?5n:o[k];}});const r=reg.matches('urn:obj',p);return {result:r,getTraps:n};});
run('proxyArrayToctou',()=>{const t=['x'];const p=new Proxy(t,{get(o,k){ if(k==='every')return ()=>true; return o[k];}});return reg.matches('urn:items',p);});
run('proxyCanonicalEffects',()=>{let n=0;const p=new Proxy({a:1n},{ownKeys(o){n++;return Reflect.ownKeys(o);}});canonical(p);return n;});
// 3. order data errors
run('utf8IntsAscending',()=>reg.matches('urn:utf8',[1n,2n]));
run('utf8Objects',()=>reg.matches('urn:utf8',[{},{}]));
run('utf8Mixed',()=>reg.matches('urn:utf8',['a',1n]));
run('notUtf8Objects',()=>reg.matches('urn:notutf8',[{},{}]));
run('anyUtf8Objects',()=>reg.matches('urn:anyutf8',[{},{}]));
run('byMissing',()=>reg.matches('urn:by',[{},{}]));
run('byInts',()=>reg.matches('urn:by',[{k:1n},{k:2n}]));
run('byNested',()=>reg.matches('urn:by',[{k:['a']},{k:['b']}]));
run('byArrayPrefix',()=>reg.matches('urn:by',[{k:['a','b']},{k:['a']}]));
run('ordinalOk',()=>reg.matches('urn:ordinal',[{ordinal:0n},{ordinal:1n}]));
run('single utf8 object',()=>reg.matches('urn:utf8',[{}]));
// 4. malformed keywords (checkEntryPoints does not type keyword values)
run('enumNonArrayFailOpen',()=>reg.matches('urn:enumbad',2n));
run('requiredNonArrayFailOpen',()=>reg.matches('urn:reqbad',{}));
run('typeNumberInt',()=>reg.matches('urn:typenum',1n));
run('patternBigint',()=>reg.matches('urn:patbad','x1'));
run('minimumString',()=>reg.matches('urn:minbad',3n));
run('refNonString',()=>reg.matches('urn:refbad',0n));
run('cycleViaAllOf',()=>reg.matches('urn:cyc2',0n));
// 5. lexical extras
const bad=['','-','+1','1.','.1','0x1','NaN','Infinity','[1 2]','{"a" 1}','{a:1}',"'a'",'"\\x"','"\\u12"','"a\tb"','"\u0000"','tru','nul','[]]','{"a":1}}','\u00a0 1','1\u2028','"\\uDC00\\uD800"','[' ,'"\\ud800\\u0061"'];
out.lexicalRefused=bad.filter(t=>{try{parseExact(new TextEncoder().encode(t));return false;}catch(e){return e instanceof JsonError;}}).length+'/'+bad.length;
out.lexicalAccepted=bad.filter(t=>{try{parseExact(new TextEncoder().encode(t));return true;}catch(e){return false;}});
out.bytesSurrogateUtf8=(()=>{try{parseExact(new Uint8Array([0x22,0xed,0xa0,0x80,0x22]));return 'ACCEPT'}catch(e){return e.constructor.name}})();
out.pairOk=new TextDecoder().decode(canonical(parseExact(new TextEncoder().encode('"\\ud83d\\ude00\\u007f\\u2028\\/\\u001f"'))));
out.keyOrder=new TextDecoder().decode(canonical(parseExact(new TextEncoder().encode('{"\\ud83d\\ude00":1,"\\uffff":2,"10":3,"9":4,"":5,"a":6,"B":7}'))));
out.foreignU8=(()=>{try{return parseExact(new DataView(new ArrayBuffer(2)))}catch(e){return e.constructor.name}})();
out.shared=(()=>{try{const s=new Uint8Array(new SharedArrayBuffer(2));s.set([49,50]);return String(parseExact(s))}catch(e){return e.constructor.name+':'+e.message}})();
run('canonicalNumber',()=>canonical(1));
run('canonicalBoxed',()=>canonical(Object(1n)));
run('canonicalCycle',()=>{const a={};a.a=a;return canonical(a);});
run('matchesNonInertFirst',()=>reg.matches('urn:items',[1]));
run('limitZeroAfterCanonical',()=>reg.matches('urn:items',[1],0));
console.log(JSON.stringify(out,(k,v)=>typeof v==='bigint'?v.toString()+'n':v,1));
