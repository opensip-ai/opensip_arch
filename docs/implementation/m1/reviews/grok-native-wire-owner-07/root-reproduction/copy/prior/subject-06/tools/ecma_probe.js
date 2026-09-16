'use strict';
// Execute the declared ECMA-262 pattern dialect (candidate 03, RF-3). Reads one JSON object from stdin:
//   {"flags": "u", "cases": [{"pattern": "...", "strings": ["...", ...]}, ...]}
// and writes {"engine": {...}, "results": [[bool, ...], ...]} where results[i][j] = new RegExp(pattern_i, flags).test(strings_i[j]).
// No file, network or environment access beyond stdin/stdout.
const fs = require('fs');
const input = JSON.parse(fs.readFileSync(0, 'utf8'));
const out = {
  engine: {node: process.versions.node, v8: process.versions.v8, icu: process.versions.icu, unicode: process.versions.unicode},
  flags: input.flags,
  results: [],
};
for (const c of input.cases) {
  let re;
  try {
    re = new RegExp(c.pattern, input.flags);
  } catch (e) {
    out.results.push({error: String(e)});
    continue;
  }
  out.results.push(c.strings.map((s) => re.test(s)));
}
process.stdout.write(JSON.stringify(out));
