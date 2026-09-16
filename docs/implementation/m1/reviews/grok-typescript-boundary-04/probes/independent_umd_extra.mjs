// Extra independent UMD shapes. Isolated from the main 19-probe run.
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const review = path.resolve(here, '..');
const copy = path.join(review, 'copy');
const scratch = path.join(here, 'work-umd');
const tmp = path.join(scratch, 'tmp');
const NODE = '/Users/sb/.nvm/versions/node/v24.16.0/bin/node';
const bin = path.join(copy, 'checker/bin/check-boundary.mjs');
const designLock = path.join(copy, 'inputs/product/design-lock.json');
const architecture = path.join(copy, 'inputs/architecture');
const env = { ...process.env, TMPDIR: tmp };
fs.mkdirSync(tmp, { recursive: true });

const { baseFiles, baseLanes, writeTree } = await import(path.join(copy, 'baseline/subject-02-trial/harness/fixture.mjs'));
const { laneRecordFor } = await import(path.join(copy, 'harness/adapter.mjs'));
const json = v => JSON.stringify(v, null, 2) + '\n';
const reportDeps = extra => {
  const m = JSON.parse(baseFiles()['apps/report/package.json']);
  Object.assign(m.dependencies, extra);
  return json(m);
};
const pkg = (name, fields) => json({ name, version: '1.0.0', ...fields });
const help = body => ({ 'apps/report/src/help-view.ts': body + '\nexport function help(): string {\n  return "help";\n}\n' });

const probes = [
  {
    id: 'G4-umd-define-function-expression-only',
    expect: 'accept',
    why: 'define(function(exports){...}) with no dependency array: common UMD; no extra module edge',
    indexJs: 'if (typeof define === "function" && define.amd) define(function (exports) { exports.u = 1; }); else exports.u = 1;\n',
  },
  {
    id: 'G4-umd-exports-module-two-arg',
    expect: 'accept',
    why: 'define(["exports","module"], factory) is the documented localExportsOnly shape',
    indexJs: '(function (root, factory) {\n  if (typeof define === "function" && define.amd) define(["exports", "module"], factory);\n  else factory(exports, module);\n})(this, function (exports, module) { exports.u = 1; });\n',
  },
  {
    id: 'G4-named-umd-exports-module',
    expect: 'accept',
    why: 'named define("id", ["exports","module"], factory) is still exports/module-only',
    indexJs: '(function (root, factory) {\n  if (typeof define === "function" && define.amd) define("umd-nm", ["exports", "module"], factory);\n  else factory(exports, module);\n})(this, function (exports, module) { exports.u = 1; });\n',
  },
];

const rows = [];
for (const p of probes) {
  const dir = path.join(scratch, p.id);
  const root = path.join(dir, 'root');
  fs.mkdirSync(root, { recursive: true });
  writeTree(root, baseFiles());
  writeTree(root, {
    [`node_modules/${p.id}/package.json`]: pkg(p.id, { main: 'index.js' }),
    [`node_modules/${p.id}/index.js`]: p.indexJs,
    'apps/report/package.json': reportDeps({ [p.id]: '1.0.0' }),
    ...help(`// @ts-ignore\nimport { u } from "${p.id}";\nexport const uu = u;`),
  });
  const { record } = laneRecordFor(root, baseLanes(), 'report');
  const recordFile = path.join(dir, 'lane-record.json');
  fs.writeFileSync(recordFile, json(record));
  const c = spawnSync(NODE, [bin, '--root', root, '--lane-record', recordFile, '--design-lock', designLock, '--architecture', architecture], { encoding: 'utf8', env, cwd: dir, maxBuffer: 32 * 1024 * 1024 });
  let report = null;
  try { report = JSON.parse(c.stdout); } catch { /* */ }
  const cats = [...new Set((report?.refusals ?? []).map(r => r.category))];
  let grade;
  if (!report) grade = 'tool-error';
  else if (p.expect === 'accept') grade = report.passed ? 'correct' : 'false-refusal';
  else grade = report.passed ? 'missed' : (cats.includes('unsupported-module-format') ? 'correct' : 'wrong-reason');
  const row = { id: p.id, why: p.why, expected: p.expect, status: c.status, passed: report?.passed ?? null, categories: cats, refusals: (report?.refusals ?? []).map(r => ({ category: r.category, from: r.from, message: (r.message ?? '').slice(0, 160) })), grade };
  rows.push(row);
  process.stdout.write(`${row.id.padEnd(42)} ${row.grade.padEnd(16)} exit=${c.status} ${cats.join(',')}\n`);
}
const outFile = path.join(review, 'results', 'independent-probes-umd-extra.json');
fs.writeFileSync(outFile, json({ schemaVersion: 1, standing: 'independent extra UMD shapes', summary: rows.reduce((a, r) => (a[r.grade] = (a[r.grade] || 0) + 1, a), {}), rows }));
if (rows.some(r => r.grade !== 'correct')) process.exitCode = 1;
