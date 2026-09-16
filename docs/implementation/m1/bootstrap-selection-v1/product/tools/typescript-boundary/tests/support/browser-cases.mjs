// Extra independent UMD shapes. Isolated from the main 19-probe run.
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const review = path.resolve(here, '..');
const copy = review;
const scratch = path.join(review, 'work/root06-browser');
const tmp = path.join(scratch, 'tmp');
const NODE = process.execPath;
const bin = process.env.OPENSIP_BOUNDARY_CHECKER ?? path.join(copy, 'checker/bin/check-boundary.mjs');
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
 {id:'suffix-reentry',expect:'refuse',category:'reentry',indexJs:'import "../../apps/report/src/help-view.ts?one";export const u=1;'},
 {id:'suffix-query',expect:'accept',indexJs:'import "./dep.js?one";export const u=1;',files:{'dep.js':'export const x=1;'}},
 {id:'suffix-fragment',expect:'accept',indexJs:'import "./dep.js#one";export const u=1;',files:{'dep.js':'export const x=1;'}},
 {id:'suffix-transitive-unresolved',expect:'refuse',category:'unresolved',indexJs:'import "./dep.js?one";export const u=1;',files:{'dep.js':'import "undeclared-package";'}},
 {id:'suffix-cross-package',expect:'accept',indexJs:'import "../dep/internal.mjs?one";export const u=1;'},
 {id:'disabled-prefix-real-file',expect:'accept',indexJs:'import "./(disabled):target.js";export const u=1;',files:{'(disabled):target.js':'export const x=1;'}},
 {id:'disabled-prefix-transitive-unresolved',expect:'refuse',category:'unresolved',indexJs:'import "./(disabled):target.js";export const u=1;',files:{'(disabled):target.js':'import "undeclared-package";'}},
 {id:'disabled-edge',expect:'accept',indexJs:'import "./dep.js";export const u=1;',fields:{browser:{'./dep.js':false}},files:{'dep.js':'import "undeclared-package";'}},
 {id:'browser-builtin-disabled',expect:'accept',indexJs:'import "node:fs";export const u=1;',fields:{browser:{'node:fs':false}}},
 {id:'browser-builtin-live',expect:'refuse',category:'browser-node',indexJs:'import "node:fs";export const u=1;'},
 {id:'browser-alias-transitive',expect:'refuse',category:'unresolved',indexJs:'import "./dep.js";export const u=1;',fields:{browser:{'./dep.js':'./browser.js'}},files:{'dep.js':'export const x=1;','browser.js':'import "undeclared-package";'}},
 {id:'module-main-import',expect:'accept',indexJs:'export const u=1;',fields:{module:'./module.mjs'},files:{'module.mjs':'export const u=1;'}},
 {id:'module-main-hidden-edge',expect:'refuse',category:'unresolved',indexJs:'export const u=1;',fields:{module:'./module.mjs'},files:{'module.mjs':'import "undeclared-package";export const u=1;'}},
 {id:'external-url-refuses',expect:'refuse',category:'unresolved',indexJs:'import "https://example.invalid/a.js";export const u=1;'},
 {id:'inline-url-refuses',expect:'refuse',category:'unresolved',indexJs:'import "data:text/javascript,export default 1";export const u=1;'},
];

const rows = [];
for (const p of probes) {
  const dir = path.join(scratch, p.id);
  const root = path.join(dir, 'root');
  fs.mkdirSync(root, { recursive: true });
  writeTree(root, baseFiles());
  writeTree(root, {
    [`node_modules/${p.id}/package.json`]: pkg(p.id, { main: 'index.js', ...p.fields }),
    [`node_modules/${p.id}/index.js`]: p.indexJs,
    ...Object.fromEntries(Object.entries(p.files??{}).map(([name,text])=>[`node_modules/${p.id}/${name}`,text])),
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
  else grade = report.passed ? 'missed' : (cats.includes(p.category??'unresolved') ? 'correct' : 'wrong-reason');
  const row = { id: p.id, why: p.why, expected: p.expect, status: c.status, passed: report?.passed ?? null, categories: cats, refusals: (report?.refusals ?? []).map(r => ({ category: r.category, from: r.from, message: (r.message ?? '').slice(0, 160) })), grade };
  rows.push(row);
  process.stdout.write(`${row.id.padEnd(42)} ${row.grade.padEnd(16)} exit=${c.status} ${cats.join(',')}\n`);
}
const outFile = path.join(review, 'results/root06-browser04.json');
fs.writeFileSync(outFile, json({ schemaVersion: 1, standing: 'Root full-checker browser resolver integration probes; adapted fixture setup', summary: rows.reduce((a, r) => (a[r.grade] = (a[r.grade] || 0) + 1, a), {}), rows }));
if (rows.some(r => r.grade !== 'correct')) process.exitCode = 1;
