// D2b-0b's pattern differential (the M1 method's pattern-differential.mjs, reading the profile and cases by path):
// every profile row's ECMA-262 Unicode translation is compiled with the `u` flag and must agree with the Python `re`
// reference's recorded result on every value. Usage: node pattern_differential.mjs <profile> <cases> <out>.
import assert from 'node:assert/strict';
import {readFileSync, writeFileSync} from 'node:fs';
const [profilePath, casesPath, outPath] = process.argv.slice(2);
const profile = JSON.parse(readFileSync(profilePath));
const cases = JSON.parse(readFileSync(casesPath));
assert.deepEqual(cases.patterns, profile.patterns.map(row => row.source));
const mismatches = [];
for (let p = 0; p < profile.patterns.length; p++) {
  const regex = new RegExp(profile.patterns[p].ecma262Unicode, 'u');
  for (let i = 0; i < cases.values.length; i++) {
    if (regex.test(cases.values[i]) !== cases.expected[p][i]) mismatches.push({pattern: profile.patterns[p].source, value: cases.values[i]});
  }
}
const result = {patterns: profile.patterns.length, values: cases.values.length, comparisons: profile.patterns.length * cases.values.length, mismatches, productQualification: false};
writeFileSync(outPath, JSON.stringify(result, null, 2) + '\n');
console.log(JSON.stringify({patterns: result.patterns, values: result.values, comparisons: result.comparisons, mismatches: mismatches.length}));
assert.equal(mismatches.length, 0);
