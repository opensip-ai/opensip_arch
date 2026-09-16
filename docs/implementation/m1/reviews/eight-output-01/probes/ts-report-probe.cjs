// Review probe: generated report runtime (original schema bytes) admission controls.
const fs = require('node:fs');
const W = __dirname;
const report = require(W + '/subject/compiled-report/apps/report/src/generated/report.js');
const registry = report.createTrialReportShapeRegistry();
const enc = (s) => new TextEncoder().encode(s);
const out = {metadata: {}, controls: []};

// 1. Metadata fixtures versus the retained accepted TS subject02 expectations.
const fixtures = JSON.parse(fs.readFileSync('/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m1/metadata-v2/fixtures.json'));
const expected = JSON.parse(fs.readFileSync('/tmp/opensip-implementation/m1-ts-runtime-subject-02/schema-differential-02.json')).expected;
const envelope = 'urn:opensip:product-v1:workflows:evaluator3:command-envelope:4';
let agree = 0, disagree = [];
fixtures.cases.forEach((c, i) => {
  // Python json.dumps would change nothing relevant: fixture values contain only integers, strings, bools, null.
  const raw = JSON.stringify(c.value);
  const got = registry.matches(envelope, report.parseExact(enc(raw)));
  if (got === expected[i].shape && expected[i].id === c.id) agree++; else disagree.push({id: c.id, got, expected: expected[i]});
});
out.metadata = {cases: fixtures.cases.length, agree, disagree};

// 2. Control cases on original schemas (pattern, if/then, x-opensip-order, not, integer range, duplicates).
for (const c of JSON.parse(fs.readFileSync(W + '/control-cases.json'))) {
  let row = {id: c.id};
  try {
    const value = report.parseExact(enc(c.raw));
    row.ts = registry.matches(c.ref, value) ? 'shape-valid' : 'shape-invalid';
  } catch (e) { row.ts = 'refused:' + (e.message || String(e)); }
  out.controls.push(row);
}
console.log(JSON.stringify(out, null, 1));
