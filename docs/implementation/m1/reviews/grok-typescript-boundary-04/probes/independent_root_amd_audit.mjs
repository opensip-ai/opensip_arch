// Independent reproduction of m1-typescript-umd-audit-01 against the review copy.
// Does not write the frozen subject. Not a new review.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import vm from 'node:vm';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const review = path.resolve(here, '..');
const copy = path.join(review, 'copy');
const frozen = '/tmp/opensip-implementation/m1-typescript-boundary-subject-04';
const scratch = path.join(here, 'work-root-amd-audit');
const tmp = path.join(scratch, 'tmp');
const NODE = '/Users/sb/.nvm/versions/node/v24.16.0/bin/node';
const bin = path.join(copy, 'checker/bin/check-boundary.mjs');
const designLock = path.join(copy, 'inputs/product/design-lock.json');
const architecture = path.join(copy, 'inputs/architecture');
const env = { ...process.env, TMPDIR: tmp };
fs.mkdirSync(tmp, { recursive: true });
fs.rmSync(path.join(scratch, 'cases'), { recursive: true, force: true });

const sha = rel => crypto.createHash('sha256').update(fs.readFileSync(path.join(frozen, rel))).digest('hex');
const shaCopy = rel => crypto.createHash('sha256').update(fs.readFileSync(path.join(copy, rel))).digest('hex');
const byteIdentity = ['checker/src/usages.mjs', 'checker/src/check.mjs', 'checker/bin/check-boundary.mjs'].map(rel => ({
  rel, frozen: sha(rel), copy: shaCopy(rel), identical: sha(rel) === shaCopy(rel),
}));

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

// AMD spec model: omitted dependencies default to ["require","exports","module"].
// First factory argument is require even if the parameter is named load.
// Explicit arrays are used as written. Not a RequireJS implementation.
function amdSpecModel(source) {
  const calls = [];
  const context = vm.createContext({
    define: (...args) => {
      const factory = args.pop();
      const dependencies = Array.isArray(args.at(-1)) ? args.at(-1) : ['require', 'exports', 'module'];
      if (typeof factory !== 'function') return;
      factory(...dependencies.map(n => (n === 'require' ? request => calls.push(request) : {})));
    },
  });
  vm.runInContext(source, context, { timeout: 1000 });
  return calls;
}

const cases = [
  { id: 'root-implicit-function', expect: 'refuse', why: 'function-expression control: implicit require as renamed first parameter', source: 'define(function(load){load("undeclared-package");});' },
  { id: 'root-implicit-arrow', expect: 'refuse', why: 'unnamed arrow factory: omitted deps inject require as first arg', source: 'define((load)=>load("undeclared-package"));' },
  { id: 'root-named-implicit-arrow', expect: 'refuse', why: 'named id plus arrow factory, still omitted deps', source: 'define("named",(load)=>load("undeclared-package"));' },
  { id: 'root-implicit-identifier', expect: 'refuse', why: 'identifier factory, omitted deps', source: 'function factory(load){load("undeclared-package");} define(factory);' },
  { id: 'named-explicit-exports', expect: 'observe', why: 'explicit ["exports"] does not inject require', source: 'define("named",["exports"],function(exports){exports.ok=true;});' },
];

const extraction = [];
for (const c of cases) {
  const usages = runtimeUsages(parse(c.id + '.js', c.source));
  const modelRequestedModules = amdSpecModel(c.source);
  extraction.push({
    id: c.id,
    source: c.source,
    modelRequestedModules,
    actualExtractor: {
      requests: usages.requests.map(r => ({ kind: r.kind, request: r.request, text: r.text })),
      loaders: usages.loaders.map(l => ({ kind: l.kind, text: l.text })),
      unsupported: usages.unsupported.map(u => ({ kind: u.kind, localExportsOnly: !!u.localExportsOnly, text: u.text })),
    },
  });
}

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
  else if (p.expect === 'observe') grade = report.passed ? 'accepted' : (cats.includes('unsupported-module-format') ? 'amd-refused' : 'other-refuse');
  else if (p.expect === 'refuse') grade = report.passed ? 'missed' : (cats.includes('unsupported-module-format') ? 'correct' : 'wrong-reason');
  else grade = 'ungraded';
  return {
    id: p.id, why: p.why, expected: p.expect, status: c.status, passed: report?.passed ?? null,
    categories: cats,
    refusals: (report?.refusals ?? []).map(r => ({ category: r.category, from: r.from, message: (r.message ?? '').slice(0, 160) })),
    grade,
  };
}

const checkerRows = cases.filter(c => c.expect === 'refuse' || c.id === 'named-explicit-exports').map(runChecker);
const refuseRows = checkerRows.filter(r => r.expected === 'refuse');
const out = {
  schemaVersion: 1,
  standing: 'independent Grok reproduction of root umd-audit-01; copy checker bytes; frozen subject not written',
  rootEvidence: {
    fullChecker: '/tmp/opensip-implementation/m1-typescript-umd-audit-01/full-checker.mjs',
    fullCheckerResult: '/tmp/opensip-implementation/m1-typescript-umd-audit-01/full-checker-result.json',
    probe: '/tmp/opensip-implementation/m1-typescript-umd-audit-01/probe.mjs',
    probeResult: '/tmp/opensip-implementation/m1-typescript-umd-audit-01/result.json',
  },
  checkerByteIdentity: byteIdentity,
  amdSpec: 'https://github.com/amdjs/amdjs-api/blob/master/AMD.md#dependencies',
  extraction,
  checker: checkerRows,
  summary: {
    refuseCases: refuseRows.length,
    correct: refuseRows.filter(r => r.grade === 'correct').length,
    missed: refuseRows.filter(r => r.grade === 'missed').map(r => r.id),
    functionExpressionControlRefuses: refuseRows.find(r => r.id === 'root-implicit-function')?.grade === 'correct',
    missedExit0: refuseRows.filter(r => r.grade === 'missed').every(r => r.status === 0 && r.passed === true),
  },
};

const outFile = path.join(review, 'results', 'independent-root-amd-audit.json');
fs.writeFileSync(outFile, json(out));
process.stdout.write(JSON.stringify({
  byteIdentity: byteIdentity.every(r => r.identical),
  summary: out.summary,
  grades: Object.fromEntries(checkerRows.map(r => [r.id, `${r.grade} exit=${r.status}`])),
  extractorUnsupported: Object.fromEntries(extraction.map(e => [e.id, e.actualExtractor.unsupported.map(u => u.kind)])),
  modelLoads: Object.fromEntries(extraction.map(e => [e.id, e.modelRequestedModules])),
}, null, 2) + '\n');
if (!byteIdentity.every(r => r.identical)) process.exitCode = 1;
if (out.summary.missed.length !== 3) process.exitCode = 1;
if (!out.summary.functionExpressionControlRefuses) process.exitCode = 1;
if (!out.summary.missedExit0) process.exitCode = 1;
