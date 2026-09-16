import assert from 'node:assert/strict';
import { parseExact, canonical, MAX_BYTES, MAX_DEPTH, JsonError } from './dist/exact-json.js';
import { SchemaRegistry, ShapeLimit, SchemaError } from './dist/schema.js';
const encode=s=>new TextEncoder().encode(s),decode=b=>new TextDecoder().decode(b);
let checks=0;
for(const text of ['9007199254740991','9007199254740992','9007199254740993','18446744073709551615','-9223372036854775808']) {
 const value=parseExact(encode(text));assert.equal(typeof value,'bigint');assert.equal(decode(canonical(value)),text);checks++;
}
for(const text of ['18446744073709551616','-9223372036854775809','-0','1e0','1.0','01','-01','\ufeff{}','{"a":0,"\\u0061":1}','"\\ud800"','"\\udfff"','[1,]','{"a":1,}']) {assert.throws(()=>parseExact(encode(text)),JsonError);checks++;}
assert.throws(()=>parseExact(new Uint8Array([0xc0,0xaf])),JsonError);checks++;
assert.throws(()=>parseExact(new ArrayBuffer(0)),JsonError);checks++;
assert.equal(parseExact(encode('['.repeat(MAX_DEPTH)+'0'+']'.repeat(MAX_DEPTH))).length,1);checks++;
assert.throws(()=>parseExact(encode('['.repeat(MAX_DEPTH+1)+'0'+']'.repeat(MAX_DEPTH+1))),JsonError);checks++;
const max='"'+'x'.repeat(MAX_BYTES-2)+'"';assert.equal(canonical(parseExact(encode(max))).length,MAX_BYTES);checks++;
assert.throws(()=>parseExact(encode(' '+max)),JsonError);checks++;
assert.throws(()=>canonical('x'.repeat(MAX_BYTES-1)),JsonError);checks++;
let effects=0;const accessor={get x(){effects++;return 1n;}};assert.throws(()=>canonical(accessor),JsonError);assert.equal(effects,0);checks++;
const array=[];Object.defineProperty(array,'0',{get(){effects++;return 1n;}});assert.throws(()=>canonical(array),JsonError);assert.equal(effects,0);checks++;
const hidden={};Object.defineProperty(hidden,'x',{value:1n});assert.throws(()=>canonical(hidden),JsonError);checks++;
assert.equal(decode(canonical(parseExact(encode('{"__proto__":1,"constructor":2}')))),'{"__proto__":1,"constructor":2}');checks++;
const document={$schema:'https://json-schema.org/draft/2020-12/schema',$id:'urn:trial',type:'integer',minimum:0n,maximum:18446744073709551615n};
const registry=new SchemaRegistry([document]);document.maximum=0n;
assert.equal(registry.matches('urn:trial',18446744073709551615n),true);checks++;
assert.throws(()=>registry.matches('https://example.invalid/schema',0n),SchemaError);checks++;
assert.throws(()=>registry.matches('urn:trial',0n,0),SchemaError);checks++;
const cycle=new SchemaRegistry([{$schema:document.$schema,$id:'urn:cycle',$ref:'urn:cycle'}]);assert.throws(()=>cycle.matches('urn:cycle',0n),ShapeLimit);checks++;
const unsupported=new SchemaRegistry([{$schema:document.$schema,$id:'urn:unsupported',unevaluatedProperties:false}]);assert.throws(()=>unsupported.matches('urn:unsupported',{}),SchemaError);checks++;
console.log(JSON.stringify({passed:true,checks,productQualification:false}));
