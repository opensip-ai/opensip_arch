// Independent AMD simplified-CommonJS counterexample for TS04 UMD S1.
// Does not mutate the frozen subject or interrupt fullcheck. Uses review/copy checker bytes.
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const review = path.resolve(here, '..');
const copy = path.join(review, 'copy');
const scratch = path.join(here, 'work-amd-cjs');
const tmp = path.join(scratch, 'tmp');
const NODE = '/Users/sb/.nvm/versions/node/v24.16.0/bin/node';
const bin = path.join(copy, 'checker/bin/check-boundary.mjs');
const designLock = path.join(copy, 'inputs/product/design-lock.json');
const architecture = path.join(copy, 'inputs/architecture');
const env = { ...process.env, TMPDIR: tmp };
fs.mkdirSync(tmp, { recursive: true });
fs.rmSync(path.join(scratch, 'cases'), { recursive: true, force: true });

const { baseFiles, baseLanes, writeTree } = await import(path.join(copy, 'baseline/subject-02-trial/harness/fixture.mjs'));
const { laneRecordFor } = await import(path.join(copy, 'harness/adapter.mjs'));
const { parse, runtimeUsages } = await import(path.join(copy, 'checker/src/usages.mjs'));

const json = v => JSON.stringify(v, null, 2) + '\n';
const pkg = (name, fields) => json({ name, version: '1.0.0', ...fields });
const help = body => ({ 'apps/report/src/help-view.ts': body + '\nexport function help(): string {\n  return "help";\n}\n' });
const reportDeps = extra => {
  const m = JSON.parse(baseFiles()['apps/report/package.json']);
  Object.assign(m.dependencies, extra);
  return json(m);
};

// Primary AMD/RequireJS semantics (amdjs-api AMD.md; RequireJS simplified CJS wrapper):
// If dependencies are omitted, they default to ["require","exports","module"].
// The factory is invoked as factory(require, exports, module). Parameter spelling
// does not rename those values. RequireJS CJS scan looks for literal require("id")
// in Function#toString; a first-parameter alias used as a call is still require
// at runtime and is not that scan's require("id") form.
function amdSimplifiedCjs(factory) {
  const loaded = [];
  const localRequire = id => {
    loaded.push(id);
    return { id, ok: true };
  };
  const exp = {};
  const mod = { exports: exp };
  const arity = factory.length;
  const args = [localRequire, exp, mod].slice(0, arity || 3);
  let threw = null;
  try { factory(...args); } catch (error) { threw = String(error && error.message || error); }
  return { loaded, expKeys: Object.keys(exp), threw, arity };
}

function amdExplicitDeps(deps, factory) {
  const loaded = [];
  const localRequire = id => {
    loaded.push(id);
    return { id, ok: true };
  };
  const exp = {};
  const mod = { exports: exp };
  const map = { require: localRequire, exports: exp, module: mod };
  let threw = null;
  try { factory(...deps.map(d => map[d])); } catch (error) { threw = String(error && error.message || error); }
  return { loaded, expKeys: Object.keys(exp), threw };
}

const noArrayHidden = function (exports) {
  const hidden = exports('undeclared-hidden');
  return hidden;
};
const namedExportsOnly = function (exports) {
  exports.u = 1;
};
const namedExportsCall = function (exports) {
  exports('undeclared-hidden');
};

const semantics = {
  spec: {
    amdjs: 'https://github.com/amdjs/amdjs-api/blob/master/AMD.md',
    rule: 'If the dependencies argument is omitted, it should default to ["require", "exports", "module"]. The loader may pass only factory.length arguments. Simplified CJS scan, if used, looks for literal require("module-id") and requires the first argument to be named require for that scan.',
    requirejs: 'https://requirejs.org/docs/whyamd.html and wiki Differences-between-the-simplified-CommonJS-wrapper-and-standard-AMD-define: no dependency array and factory.length >= 1 is treated as CJS; factory is called with require, exports, module in that order. Explicit dependency arrays are not scanned for extra require() calls.',
  },
  noArrayFirstParamIsRequire: amdSimplifiedCjs(noArrayHidden),
  explicitExportsArrayAssignment: amdExplicitDeps(['exports'], namedExportsOnly),
  explicitExportsArrayCallIsNotRequire: amdExplicitDeps(['exports'], namedExportsCall),
};

function extract(text, file = 'index.js') {
  const usages = runtimeUsages(parse(file, text));
  return {
    requests: usages.requests.map(r => ({ kind: r.kind, request: r.request, text: r.text })),
    loaders: usages.loaders.map(l => ({ kind: l.kind, text: l.text })),
    unsupported: usages.unsupported.map(u => ({ kind: u.kind, localExportsOnly: !!u.localExportsOnly, text: u.text })),
  };
}

const hiddenBody = 'define(function (exports) {\n  var hidden = exports("undeclared-hidden");\n  return hidden;\n});\n';
const namedBody = '(function (root, factory) {\n  if (typeof define === "function" && define.amd) define("umd-named", ["exports"], factory);\n  else if (typeof exports === "object") factory(exports);\n})(this, function (exports) { exports.u = 1; });\n';
const iifeBody = '(function (root, factory) {\n  if (typeof define === "function" && define.amd) define(factory);\n  else if (typeof exports === "object") factory(exports);\n})(this, function (exports) { var hidden = exports("undeclared-hidden"); return hidden; });\n';

const extraction = {
  noArrayHiddenCall: extract(hiddenBody),
  namedExportsOnly: extract(namedBody),
  iifeDefineIdentifierHiddenCall: extract(iifeBody),
};

function runChecker(id, indexJs, checkerBin) {
  const dir = path.join(scratch, 'cases', id);
  const root = path.join(dir, 'root');
  fs.mkdirSync(root, { recursive: true });
  writeTree(root, baseFiles());
  writeTree(root, {
    [`node_modules/${id}/package.json`]: pkg(id, { main: 'index.js' }),
    [`node_modules/${id}/index.js`]: indexJs,
    'node_modules/undeclared-hidden/package.json': pkg('undeclared-hidden', { main: 'index.js' }),
    'node_modules/undeclared-hidden/index.js': 'exports.hidden = true;\n',
    'apps/report/package.json': reportDeps({ [id]: '1.0.0' }),
    ...help(`// @ts-ignore\nimport * as m from "${id}";\nexport const mm = m;`),
  });
  const { record } = laneRecordFor(root, baseLanes(), 'report');
  const recordFile = path.join(dir, 'lane-record.json');
  fs.writeFileSync(recordFile, json(record));
  const c = spawnSync(NODE, [checkerBin, '--root', root, '--lane-record', recordFile, '--design-lock', designLock, '--architecture', architecture], { encoding: 'utf8', env, cwd: dir, maxBuffer: 32 * 1024 * 1024 });
  let report = null;
  try { report = JSON.parse(c.stdout); } catch { /* */ }
  return {
    id,
    status: c.status,
    passed: report?.passed ?? null,
    categories: [...new Set((report?.refusals ?? []).map(r => r.category))],
    refusals: (report?.refusals ?? []).map(r => ({ category: r.category, from: r.from, request: r.request, message: (r.message ?? '').slice(0, 200) })),
    stderr: (c.stderr || '').slice(0, 300),
  };
}

const current = {
  noArrayHiddenCall: runChecker('amd-cjs-noarray-hidden', hiddenBody, bin),
  namedExportsOnly: runChecker('amd-named-exports-only', namedBody, bin),
  iifeDefineIdentifierHiddenCall: runChecker('amd-iife-define-id-hidden', iifeBody, bin),
};

const widenedDir = path.join(scratch, 'widened-checker');
fs.rmSync(widenedDir, { recursive: true, force: true });
fs.mkdirSync(widenedDir, { recursive: true });
for (const item of ['src', 'bin', 'package.json']) {
  fs.cpSync(path.join(copy, 'checker', item), path.join(widenedDir, item), { recursive: true });
}
fs.symlinkSync(path.join(copy, 'checker/node_modules'), path.join(widenedDir, 'node_modules'));
const usagesPath = path.join(widenedDir, 'src/usages.mjs');
const before = fs.readFileSync(usagesPath, 'utf8');
const needle = 'const localExportsOnly = node.arguments.length === 2 && ts.isArrayLiteralExpression(dependencies) && dependencies.elements.length > 0 && dependencies.elements.every(item => literal(item) && [\'exports\', \'module\'].includes(item.text)) && !!factory && (ts.isIdentifier(factory) || ts.isFunctionExpression(factory) || ts.isArrowFunction(factory));';
const widened = 'const localExportsOnly = (node.arguments.length === 1 && ts.isFunctionExpression(node.arguments[0])) || (node.arguments.length === 2 && ts.isArrayLiteralExpression(dependencies) && dependencies.elements.length > 0 && dependencies.elements.every(item => literal(item) && [\'exports\', \'module\'].includes(item.text)) && !!factory && (ts.isIdentifier(factory) || ts.isFunctionExpression(factory) || ts.isArrowFunction(factory)));';
if (before.split(needle).length !== 2) throw new Error('widening site not unique');
fs.writeFileSync(usagesPath, before.replace(needle, widened));
const widenedBin = path.join(widenedDir, 'bin/check-boundary.mjs');
const widenedRun = {
  noArrayHiddenCall: runChecker('widened-amd-cjs-noarray-hidden', hiddenBody, widenedBin),
};

function gradeCurrent(row, expect) {
  if (expect === 'refuse-amd') return row.categories.includes('unsupported-module-format') && row.passed === false ? 'correct-conservative-amd-refuse' : 'unexpected';
  if (expect === 'accept') return row.passed === true ? 'accept' : 'false-refusal';
  if (expect === 'refuse-undeclared') return row.categories.includes('undeclared-external') ? 'caught-undeclared' : (row.passed ? 'missed-undeclared' : 'other-refuse');
  return 'ungraded';
}

const out = {
  schemaVersion: 1,
  standing: 'independent AMD simplified-CJS counterexample against widening no-array define(function(){}); not a new review and not product selection',
  semantics,
  extraction,
  currentChecker: {
    noArrayHiddenCall: { ...current.noArrayHiddenCall, grade: gradeCurrent(current.noArrayHiddenCall, 'refuse-amd') },
    namedExportsOnly: { ...current.namedExportsOnly, grade: gradeCurrent(current.namedExportsOnly, 'accept') },
    iifeDefineIdentifierHiddenCall: { ...current.iifeDefineIdentifierHiddenCall, grade: gradeCurrent(current.iifeDefineIdentifierHiddenCall, 'refuse-amd') },
  },
  widenedNoArrayAsLocalExportsOnly: {
    site: 'usages.mjs localExportsOnly also true for define(function(){})',
    noArrayHiddenCall: { ...widenedRun.noArrayHiddenCall, grade: gradeCurrent(widenedRun.noArrayHiddenCall, 'refuse-undeclared') },
  },
  conclusions: {
    omittedDependencyArrayInjectsRequireFirst: semantics.noArrayFirstParamIsRequire.loaded.includes('undeclared-hidden'),
    extractorDoesNotSeeExportsCallAsRequire: extraction.noArrayHiddenCall.requests.length === 0,
    currentCheckerRefusesNoArrayFunctionDefine: current.noArrayHiddenCall.categories.includes('unsupported-module-format'),
    wideningNoArrayWouldMissHiddenRequire: widenedRun.noArrayHiddenCall.passed === true,
    namedExplicitExportsArrayDoesNotInjectRequire: semantics.explicitExportsArrayCallIsNotRequire.loaded.length === 0,
  },
};

const outFile = path.join(review, 'results', 'independent-amd-cjs.json');
fs.writeFileSync(outFile, json(out));
process.stdout.write(JSON.stringify({
  semanticsLoaded: out.conclusions.omittedDependencyArrayInjectsRequireFirst,
  extractorBlind: out.conclusions.extractorDoesNotSeeExportsCallAsRequire,
  currentNoArray: out.currentChecker.noArrayHiddenCall.grade,
  currentNamed: out.currentChecker.namedExportsOnly.grade,
  currentIife: out.currentChecker.iifeDefineIdentifierHiddenCall.grade,
  widened: out.widenedNoArrayAsLocalExportsOnly.noArrayHiddenCall.grade,
  conclusions: out.conclusions,
}, null, 2) + '\n');
if (!out.conclusions.omittedDependencyArrayInjectsRequireFirst) process.exitCode = 1;
if (!out.conclusions.extractorDoesNotSeeExportsCallAsRequire) process.exitCode = 1;
if (!out.conclusions.currentCheckerRefusesNoArrayFunctionDefine) process.exitCode = 1;
if (!out.conclusions.wideningNoArrayWouldMissHiddenRequire) process.exitCode = 1;
