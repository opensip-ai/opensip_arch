import assert from 'node:assert/strict';
import {canonical, parseExact, JsonError} from './dist/exact-json.js';
import {SchemaRegistry, SchemaError} from './dist/schema.js';
const base = {$schema:'https://json-schema.org/draft/2020-12/schema', $id:'urn:regression'};
const match = (schema, value) => new SchemaRegistry([{...base, ...schema}]).matches(base.$id, value);
let checks = 0;
const custom = [1n, 2n];
Object.setPrototypeOf(custom, {every(){return true;}});
assert.throws(() => match({type:'array', items:{type:'string'}}, custom), JsonError); checks++;
class OverrideArray extends Array { every(){return true;} }
assert.throws(() => canonical(new OverrideArray(1n, 2n)), JsonError); checks++;
const proxy = new Proxy({a:5n}, {get(_target, key){return key === 'a' ? 'x' : undefined;}});
assert.equal(match({type:'object', properties:{a:{type:'string'}}, required:['a'], additionalProperties:false}, proxy), false); checks++;
let traps = 0;
const effectful = new Proxy({a:5n}, {ownKeys(target){traps++; return Reflect.ownKeys(target);}});
canonical(effectful);
assert.ok(traps > 0); checks++; // Explicitly OUTSIDE the no-Proxy inert-input contract.
assert.throws(() => parseExact(new Uint8Array(new SharedArrayBuffer(1))), JsonError); checks++;
for (const schema of [{enum:'x'}, {enum:[]}, {enum:[1n,1n]}, {required:'x'}, {required:['x','x']},
  {pattern:1n}, {minimum:'1'}, {$ref:1n}, {type:'number'}, {type:[]}, {allOf:[]},
  {minItems:-1n}, {uniqueItems:1n}, {pattern:'unregistered pattern'}, {$ref:'urn:regression#/~3'}]) {
  assert.throws(() => match(schema, {}), SchemaError); checks++;
}
for (const [order, values] of [['utf8',[1n,2n]], ['numeric',['1','2']], ['path',[{path:1n}]],
  ['predicate',[{}]], ['ordinal',[{ordinal:'0'}]], ['candidateOrdinal',[{candidateOrdinal:'0'}]],
  [{by:['x']},[{x:1n}]], [{by:['x']},[{x:[1n]}, {x:[1n,2n]}]]]) {
  assert.equal(match({'x-opensip-order':order}, values), false); checks++;
  assert.equal(match({not:{'x-opensip-order':order}}, values), true); checks++;
}
assert.equal(match({'x-opensip-order':'ordinal'}, [{ordinal:0n},{ordinal:1n}]), true); checks++;
assert.equal(match({'x-opensip-order':'candidateOrdinal'}, [{candidateOrdinal:4n},{candidateOrdinal:9n}]), true); checks++;
console.log(JSON.stringify({checks, passed:true, productQualification:false}));
