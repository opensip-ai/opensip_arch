// Independent TS05 delta probes. Reproduces TS04 RF-1/S1 and nearby shapes
// not in root's 9 controls. Uses review/copy checker only.
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const review = path.resolve(here, '..');
const copy = '/tmp/opensip-implementation/m1-typescript-boundary-subject-05';
const scratch = path.join(here, 'work-delta');
const tmp = path.join(scratch, 'tmp');
const NODE = '/Users/sb/.nvm/versions/node/v24.16.0/bin/node';
const bin = path.join(copy, 'checker/bin/check-boundary.mjs');
const designLock = path.join(copy, 'inputs/product/design-lock.json');
const architecture = path.join(copy, 'inputs/architecture');
const env = { ...process.env, TMPDIR: tmp };
fs.mkdirSync(tmp, { recursive: true });
fs.rmSync(path.join(scratch, 'cases'), { recursive: true, force: true });

const { parse, runtimeUsages } = await import(path.join(copy, 'checker/src/usages.mjs'));
const { baseFiles, baseLanes, writeTree } = await import(path.join(copy, 'baseline/subject-02-trial/harness/fixture.mjs'));
const { laneRecordFor } = await import(path.join(copy, 'harness/adapter.mjs'));
const json = v => JSON.stringify(v, null, 2) + '\n';
const pkg = (name, fields) => json({ name, version: '1.0.0', ...fields });
const help = body => ({ 'apps/report/src/help-view.ts': body + '\nexport function help(): string {\n  return "help";\n}\n' });
const reportDeps = extra => {
  const m = JSON.parse(baseFiles()['apps/report/package.json']);
  Object.assign(m.dependencies, extra);
  return json(m);
};

function extract(source) {
  const usages = runtimeUsages(parse('probe.js', source));
  return {
    requests: usages.requests.map(r => ({ kind: r.kind, request: r.request })),
    unsupported: usages.unsupported.map(u => ({ kind: u.kind, localExportsOnly: !!u.localExportsOnly })),
  };
}

const probes = [
  // TS04 RF-1 reproductions
  { id: 'G5-implicit-arrow', expect: 'refuse', topic: 'rf1', why: 'unnamed arrow omitted-array injects require', source: 'define((load)=>load("undeclared-package"));' },
  { id: 'G5-named-implicit-arrow', expect: 'refuse', topic: 'rf1', why: 'named id plus arrow omitted-array still injects require', source: 'define("named",(load)=>load("undeclared-package"));' },
  { id: 'G5-implicit-identifier', expect: 'refuse', topic: 'rf1', why: 'identifier factory omitted-array injects require', source: 'function factory(load){load("undeclared-package");} define(factory);' },
  { id: 'G5-implicit-function-control', expect: 'refuse', topic: 'rf1', why: 'function-expression control still refuses', source: 'define(function(load){load("undeclared-package");});' },
  { id: 'G5-noarray-exports-spelling', expect: 'refuse', topic: 'rf1', why: 'first injected argument is require despite spelling exports', source: 'define(function(exports){exports("undeclared-package");});' },
  // TS04 S1 reproductions
  { id: 'G5-named-explicit-exports', expect: 'accept', topic: 's1', why: 'named define(id, ["exports"], factory) has no injected require', source: 'define("named",["exports"],function(exports){exports.u=1;});' },
  { id: 'G5-named-explicit-exports-module', expect: 'accept', topic: 's1', why: 'named define(id, ["exports","module"], factory)', source: 'define("named",["exports","module"],function(exports,module){exports.u=1;});' },
  { id: 'G5-unnamed-explicit-exports', expect: 'accept', topic: 's1', why: 'unnamed two-arg exports-only still accepted', source: 'define(["exports"],function(exports){exports.u=1;});' },
  // Nearby independent, not in root 9
  { id: 'G5-named-exports-arrow-factory', expect: 'accept', topic: 'nearby', why: 'named id + explicit exports array + arrow factory is still exports-only', source: 'define("named",["exports"],(exports)=>{exports.u=1;});' },
  { id: 'G5-unnamed-exports-arrow-factory', expect: 'accept', topic: 'nearby', why: 'unnamed explicit exports array + arrow factory', source: 'define(["exports"],(exports)=>{exports.u=1;});' },
  { id: 'G5-named-module-only-array', expect: 'accept', topic: 'nearby', why: 'explicit ["module"] only is still no injected require', source: 'define("named",["module"],function(module){module.exports.u=1;});' },
  { id: 'G5-named-omitted-function', expect: 'refuse', topic: 'nearby', why: 'literal id does not make omitted array exports-only', source: 'define("named",function(load){load("undeclared-package");});' },
  { id: 'G5-explicit-require-exports', expect: 'refuse', topic: 'nearby', why: 'explicit require in array must not be waived', source: 'define("named",["require","exports"],function(load,exports){load("undeclared-package");});' },
  { id: 'G5-explicit-ordinary-package', expect: 'refuse', topic: 'nearby', why: 'explicit ordinary package must not be waived', source: 'define("named",["undeclared-package"],function(dep){return dep;});' },
  { id: 'G5-factory-body-still-traversed', expect: 'refuse', topic: 'nearby', refuseAny: ['local-name-shadow', 'reentry', 'unsupported-module-format'], why: 'exports-only UMD factory body is still walked; require of a local name is not waived', source: '(function(root,factory){if(typeof define==="function"&&define.amd)define("umd-shadow",["exports"],factory);else factory(exports);})(this,function(exports){exports.u=require("@opensip/typescript-provider");});' },
  { id: 'G5-empty-array-conservative', expect: 'observe', topic: 'cost', why: 'explicit empty dependency array is not omitted-deps; conservative AMD refuse expected', source: 'define([],function(){return 1;});' },
  { id: 'G5-object-form-conservative', expect: 'observe', topic: 'cost', why: 'AMD object-literal sugar has no factory/require; conservative AMD refuse expected', source: 'define({u:1});' },
  { id: 'G5-computed-id-explicit-exports', expect: 'observe', topic: 'cost', why: 'non-literal leading id is not normalized; explicit exports array may still refuse', source: 'var id="named"; define(id,["exports"],function(exports){exports.u=1;});' },
  { id: 'G5-template-id-explicit-exports', expect: 'accept', topic: 'nearby', why: 'no-substitution template module id is a literal and should normalize', source: 'define(`named`,["exports"],function(exports){exports.u=1;});' },
];

function runChecker(p) {
  const dir = path.join(scratch, 'cases', p.id);
  const root = path.join(dir, 'root');
  fs.mkdirSync(root, { recursive: true });
  writeTree(root, baseFiles());
  writeTree(root, {
    [`node_modules/${p.id}/package.json`]: pkg(p.id, { main: 'index.js' }),
    [`node_modules/${p.id}/index.js`]: p.source,
    'apps/report/package.json': reportDeps({ [p.id]: '1.0.0' }),
    ...help(`// @ts-ignore\nimport * as m from "${p.id}";\nexport const mm = m;`),
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
  else if (p.expect === 'observe') grade = report.passed ? 'accepted' : (cats.includes('unsupported-module-format') ? 'conservative-amd-refuse' : 'other-refuse:' + cats.join(','));
  else if (p.expect === 'accept') grade = report.passed ? 'correct' : 'false-refusal';
  else if (p.refuseAny) grade = report.passed ? 'missed' : (p.refuseAny.some(x => cats.includes(x)) ? 'correct' : 'wrong-reason');
  else grade = report.passed ? 'missed' : (cats.includes('unsupported-module-format') ? 'correct' : 'wrong-reason');
  return {
    id: p.id, topic: p.topic, why: p.why, expected: p.expect, source: p.source,
    extraction: extract(p.source),
    status: c.status, passed: report?.passed ?? null, categories: cats,
    refusals: (report?.refusals ?? []).map(r => ({ category: r.category, from: r.from, request: r.request, message: (r.message ?? '').slice(0, 160) })),
    grade,
  };
}

const rows = probes.map(runChecker);
for (const row of rows) process.stdout.write(`${row.id.padEnd(38)} ${String(row.grade).padEnd(24)} exit=${row.status} ${row.categories.join(',')}\n`);
const scored = rows.filter(r => r.expected !== 'observe');
const summary = {};
for (const r of rows) summary[r.grade] = (summary[r.grade] ?? 0) + 1;
const out = {
  schemaVersion: 1,
  standing: 'independent Grok TS05 delta probes; not root9 restatement; not product selection',
  checker: bin,
  summary,
  scored: { total: scored.length, correct: scored.filter(r => r.grade === 'correct').length, failed: scored.filter(r => r.grade !== 'correct').map(r => r.id) },
  rows,
};
fs.writeFileSync(path.join(review, 'results', 'independent-delta.json'), json(out));
process.stdout.write(JSON.stringify({ summary, scored: out.scored }, null, 2) + '\n');
if (out.scored.failed.length) process.exitCode = 1;
