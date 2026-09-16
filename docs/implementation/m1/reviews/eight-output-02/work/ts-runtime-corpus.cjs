// Cross-validate corpus values with the accepted TS02 original-schema registry embedded in report.ts.
const fs = require('node:fs');
const W = __dirname;
const report = require(W + '/subject/compiled-report/apps/report/src/generated/report.js');
const registry = report.createTrialReportShapeRegistry();
const out = {};
for (const label of ['witnesses', 'mutants']) {
  const rows = JSON.parse(fs.readFileSync(W + '/raw-' + label + '.json'));
  let valid = 0; const bad = [];
  for (const [i, r] of rows.entries()) {
    try { if (registry.matches(r.ref, report.parseExact(new TextEncoder().encode(r.raw)))) valid++; else bad.push({i, ref: r.ref, kind: r.kind}); }
    catch (e) { bad.push({i, ref: r.ref, kind: r.kind, error: String(e.message || e)}); }
  }
  out[label] = {rows: rows.length, tsRuntimeValid: valid, disagreements: bad.slice(0, 20), disagreementCount: bad.length};
}
fs.writeFileSync(W + '/logs/ts-runtime-corpus.json', JSON.stringify(out, null, 1));
console.log(JSON.stringify(out, null, 1));
