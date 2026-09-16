import assert from 'node:assert/strict';
import {readFileSync, writeFileSync} from 'node:fs';
import {selectedPattern} from './dist/patterns.js';
const profile = JSON.parse(readFileSync(new URL('pattern-profile.json', import.meta.url)));
const cases = JSON.parse(readFileSync(new URL('pattern-cases.json', import.meta.url)));
const mismatches = [];
for (let p = 0; p < profile.patterns.length; p++) {
  const row = profile.patterns[p];
  assert.equal(selectedPattern(row.source), row.ecma262Unicode);
  const regex = new RegExp(row.ecma262Unicode, 'u');
  for (let i = 0; i < cases.values.length; i++) {
    if (regex.test(cases.values[i]) !== cases.expected[p][i]) mismatches.push({pattern: row.source, value: cases.values[i]});
  }
}
assert.equal(selectedPattern('unregistered pattern'), undefined);
const result = {patterns: profile.patterns.length, values: cases.values.length,
  comparisons: profile.patterns.length * cases.values.length, mismatches, productQualification: false};
writeFileSync(new URL('pattern-differential.json', import.meta.url), JSON.stringify(result, null, 2) + '\n');
console.log(JSON.stringify(result));
assert.equal(mismatches.length, 0);
