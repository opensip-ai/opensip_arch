import assert from 'node:assert/strict';
import {readFileSync, writeFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {parseExact} from './dist/exact-json.js';
import {SchemaRegistry} from './dist/schema.js';
const arch = '/Users/sb/code/opensip-ai/opensip_arch/';
const pins = JSON.parse(readFileSync(arch+'docs/implementation/m1/metadata-v2/sources.json','utf8'));
const registry = new SchemaRegistry(pins.schemas.map(pin=>parseExact(readFileSync(arch+pin.path))));
const entrypoints = Object.keys(JSON.parse(readFileSync('/tmp/opensip-implementation/m1-full-generator-trial-01/source-map.json','utf8')).selectedTargets);
registry.checkEntryPoints(entrypoints);
const fixtures = parseExact(readFileSync(arch+'docs/implementation/m1/metadata-v2/fixtures.json'));
const actual = fixtures.cases.map(c=>({id:c.id, shape:registry.matches('urn:opensip:product-v1:workflows:evaluator3:command-envelope:4',c.value)}));
const expected = JSON.parse(execFileSync('/tmp/opensip-implementation/metadata-reference-env/bin/python',
  ['-I', '-B', fileURLToPath(new URL('metadata-reference.py', import.meta.url))], {encoding:'utf8'}));
const result = {entrypoints:entrypoints.length, cases:actual.length, expected, actual,
  mismatches:actual.filter((value,i)=>JSON.stringify(value)!==JSON.stringify(expected[i])).length, productQualification:false};
writeFileSync(new URL('schema-differential-02.json',import.meta.url),JSON.stringify(result,null,2)+'\n');
assert.deepEqual(actual, expected);
console.log(JSON.stringify({entrypoints:entrypoints.length,cases:actual.length,mismatches:result.mismatches}));
