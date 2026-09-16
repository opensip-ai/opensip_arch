// Independent Grok counterexamples for typescript-boundary04.
// Uses the private review copy's checker and fixture; does not mutate the frozen subject.
// Not a restatement of harness/review03-regressions.mjs.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const review = path.resolve(here, '..');
const copy = path.join(review, 'copy');
const scratch = path.join(here, 'work');
const tmp = path.join(scratch, 'tmp');
const NODE = '/Users/sb/.nvm/versions/node/v24.16.0/bin/node';
const bin = path.join(copy, 'checker/bin/check-boundary.mjs');
const designLock = path.join(copy, 'inputs/product/design-lock.json');
const architecture = path.join(copy, 'inputs/architecture');
const env = { ...process.env, TMPDIR: tmp };
fs.mkdirSync(tmp, { recursive: true });

const { baseFiles, baseLanes, writeTree } = await import(path.join(copy, 'baseline/subject-02-trial/harness/fixture.mjs'));
const { laneRecordFor } = await import(path.join(copy, 'harness/adapter.mjs'));
const { parse, runtimeUsages } = await import(path.join(copy, 'checker/src/usages.mjs'));

const json = v => JSON.stringify(v, null, 2) + '\n';
const sha = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const base = baseFiles();
const manifest = (file, edit) => { const m = JSON.parse(base[file]); edit(m); return json(m); };
const reportDeps = extra => manifest('apps/report/package.json', m => Object.assign(m.dependencies, extra));
const providerManifest = edit => manifest('providers/typescript/package.json', edit);
const reportTsconfig = edit => manifest('apps/report/tsconfig.json', edit);
const providerTsconfig = edit => manifest('providers/typescript/tsconfig.json', edit);
const pkg = (name, fields) => json({ name, version: '1.0.0', ...fields });
const help = body => ({ 'apps/report/src/help-view.ts': body + '\nexport function help(): string {\n  return "help";\n}\n' });

function loaderRecord(root, file, targets = []) {
  const text = fs.readFileSync(path.join(root, file), 'utf8');
  const loader = runtimeUsages(parse(path.join(root, file), text)).loaders[0];
  if (!loader) throw new Error('no loader in ' + file);
  return { kind: 'dynamic-loader', file, sha256: sha(text), line: loader.line, column: loader.column, text: loader.text, targets, reason: 'independent Grok probe' };
}

const probes = [
  {
    id: 'G4-scoped-versioned-alias-to-local',
    lane: 'report',
    expect: 'refuse',
    refuse: ['local-name-shadow'],
    topic: 'scoped-aliases',
    why: 'versioned npm: alias npm:@opensip/typescript-provider@9.9.9 with a non-local realized manifest name must still refuse on the alias target',
    files: {
      'node_modules/shadow/package.json': json({ name: 'external-package', version: '9.9.9', main: 'index.js', types: 'index.d.ts' }),
      'node_modules/shadow/index.js': 'exports.x = 1;\n',
      'node_modules/shadow/index.d.ts': 'export declare const x: number;\n',
      'apps/report/package.json': reportDeps({ shadow: 'npm:@opensip/typescript-provider@9.9.9' }),
      ...help('import { x } from "shadow";\nexport const s = x;'),
    },
  },
  {
    id: 'G4-baseurl-private-export',
    lane: 'report',
    expect: 'refuse',
    refuse: ['external-by-path'],
    topic: 'paths-baseUrl',
    why: 'baseUrl pointing into a materialized package, without paths, must not make a private file an exported interface',
    files: {
      'apps/report/tsconfig.json': reportTsconfig(m => { m.compilerOptions.baseUrl = '../../node_modules/dep'; delete m.compilerOptions.paths; }),
      ...help('import type { hidden } from "internal.mjs";\nexport type H = typeof hidden;'),
    },
  },
  {
    id: 'G4-paths-exact-private-types',
    lane: 'report',
    expect: 'refuse',
    refuse: ['external-by-path'],
    topic: 'paths-baseUrl',
    why: 'an exact tsconfig paths entry to a non-exported .d.mts must refuse, not only the wildcard dep/* form',
    files: {
      'node_modules/dep/internal.d.mts': 'export declare const hidden: true;\n',
      'apps/report/tsconfig.json': reportTsconfig(m => { m.compilerOptions.paths['dep-hidden'] = ['../../node_modules/dep/internal.d.mts']; }),
      ...help('import type { hidden } from "dep-hidden";\nexport type H = typeof hidden;'),
    },
  },
  {
    id: 'G4-declarationdir-other-lane',
    lane: 'provider',
    expect: 'refuse',
    refuse: ['config-owner'],
    topic: 'tsconfig-output-custody',
    why: 'declarationDir into another package is write custody, independent of the outDir case',
    files: { 'providers/typescript/tsconfig.json': providerTsconfig(m => { m.compilerOptions.declaration = true; m.compilerOptions.declarationDir = '../../apps/report/src/provider-decl'; }) },
  },
  {
    id: 'G4-tsbuildinfo-other-lane',
    lane: 'provider',
    expect: 'refuse',
    refuse: ['config-owner'],
    topic: 'tsconfig-output-custody',
    why: 'tsBuildInfoFile into another package is write custody',
    files: { 'providers/typescript/tsconfig.json': providerTsconfig(m => { m.compilerOptions.incremental = true; m.compilerOptions.tsBuildInfoFile = '../../apps/report/src/provider.tsbuildinfo'; }) },
  },
  {
    id: 'G4-bound-unlisted-input',
    lane: 'report',
    expect: 'refuse',
    refuse: ['inventory-ownership'],
    topic: 'source-inventory',
    why: 'bound report input with no selected inventory row must refuse inventory-ownership',
    files: {
      'apps/report/src/probe-unlisted.ts': 'export const probeUnlisted = 1;\n',
      ...help('import { probeUnlisted } from "./probe-unlisted.js";\nexport const u = probeUnlisted;'),
    },
    lanes: l => {
      const r = l.lanes.report;
      r.inputs.push('apps/report/src/probe-unlisted.ts');
      r.inputs.sort();
      r.runtimeGroups[0].files.push('apps/report/src/probe-unlisted.ts');
    },
  },
  {
    id: 'G4-bound-own-computed-require-exception',
    lane: 'provider',
    expect: 'refuse',
    refuse: ['lane-record-invalid', 'unsupported-loader'],
    topic: 'bound-self-granted-exceptions',
    why: 'a bound product lane cannot authorize its own computed require via trustedUsages',
    files: {
      'providers/typescript/scripts/bundle.cjs': 'const path = require("node:path");\nconst dep = require("dep");\nconst extra = require(process.env.OPENSIP_PROBE_MODULE || "./missing.cjs");\nmodule.exports = path.join("out", dep.parseMode, String(extra));\n',
    },
    edit: (record, root) => record.trustedUsages.push(loaderRecord(root, 'providers/typescript/scripts/bundle.cjs')),
  },
  {
    id: 'G4-named-umd-exports-only',
    lane: 'report',
    expect: 'accept',
    topic: 'amd-umd',
    why: 'named define("id", ["exports"], factory) is still an exports-only UMD branch; factory has no extra module edge',
    files: {
      'node_modules/umd-named/package.json': pkg('umd-named', { main: 'index.js' }),
      'node_modules/umd-named/index.js': '(function (root, factory) {\n  if (typeof define === "function" && define.amd) define("umd-named", ["exports"], factory);\n  else if (typeof exports === "object") factory(exports);\n})(this, function (exports) { exports.u = 1; });\n',
      'apps/report/package.json': reportDeps({ 'umd-named': '1.0.0' }),
      ...help('// @ts-ignore\nimport { u } from "umd-named";\nexport const uu = u;'),
    },
  },
  {
    id: 'G4-factory-only-umd',
    lane: 'report',
    expect: 'accept',
    topic: 'amd-umd',
    why: 'define(factory) with no dependency array is a common UMD AMD branch and creates no extra module edge',
    files: {
      'node_modules/umd-factory/package.json': pkg('umd-factory', { main: 'index.js' }),
      'node_modules/umd-factory/index.js': '(function (root, factory) {\n  if (typeof define === "function" && define.amd) define(factory);\n  else if (typeof exports === "object") factory(exports);\n})(this, function (exports) { exports.u = 1; });\n',
      'apps/report/package.json': reportDeps({ 'umd-factory': '1.0.0' }),
      ...help('// @ts-ignore\nimport { u } from "umd-factory";\nexport const uu = u;'),
    },
  },
  {
    id: 'G4-amd-require-exports-browser',
    lane: 'report',
    expect: 'refuse',
    refuse: ['unsupported-module-format'],
    topic: 'amd-umd',
    why: 'define(["require","exports"], factory) is a real AMD require dependency, not an exports/module-only UMD branch',
    files: {
      'node_modules/amd-req/package.json': pkg('amd-req', { main: 'index.js' }),
      'node_modules/amd-req/index.js': 'define(["require", "exports"], function (require, exports) { exports.u = 1; });\n',
      'apps/report/package.json': reportDeps({ 'amd-req': '1.0.0' }),
      ...help('// @ts-ignore\nimport { u } from "amd-req";\nexport const uu = u;'),
    },
  },
  {
    id: 'G4-real-amd-browser-external',
    lane: 'report',
    expect: 'refuse',
    refuse: ['unsupported-module-format'],
    topic: 'amd-umd',
    why: 'a browser-closure external with define(["other"], factory) remains unsupported AMD',
    files: {
      'node_modules/amd-real/package.json': pkg('amd-real', { main: 'index.js' }),
      'node_modules/amd-real/index.js': 'define(["dep"], function (dep) { return dep; });\n',
      'apps/report/package.json': reportDeps({ 'amd-real': '1.0.0' }),
      ...help('// @ts-ignore\nimport * as amd from "amd-real";\nexport const a = amd;'),
    },
  },
  {
    id: 'G4-umd-factory-still-traversed',
    lane: 'report',
    expect: 'refuse',
    refuse: ['local-name-shadow', 'reentry', 'browser-node'],
    topic: 'amd-umd',
    why: 'exports-only UMD must still traverse factory bodies; requiring a local package name from that factory is not waived',
    files: {
      'node_modules/umd-shadow/package.json': pkg('umd-shadow', { main: 'index.js' }),
      'node_modules/umd-shadow/index.js': '(function (root, factory) {\n  if (typeof define === "function" && define.amd) define(["exports"], factory);\n  else factory(exports);\n})(this, function (exports) { exports.u = require("@opensip/typescript-provider"); });\n',
      'apps/report/package.json': reportDeps({ 'umd-shadow': '1.0.0' }),
      ...help('// @ts-ignore\nimport { u } from "umd-shadow";\nexport const uu = u;'),
    },
  },
  {
    id: 'G4-report-browser-devdependency',
    lane: 'report',
    expect: 'refuse',
    refuse: ['runtime-dev-dependency'],
    topic: 'runtime-dev-dependency',
    why: 'browser-runtime sources may not reach a package declared only in devDependencies',
    files: {
      'node_modules/dev-browser/package.json': pkg('dev-browser', { main: 'index.js', types: 'index.d.ts' }),
      'node_modules/dev-browser/index.js': 'exports.x = 1;\n',
      'node_modules/dev-browser/index.d.ts': 'export declare const x: number;\n',
      'apps/report/package.json': manifest('apps/report/package.json', m => { m.devDependencies = { 'dev-browser': '1.0.0' }; }),
      ...help('import { x } from "dev-browser";\nexport const d = x;'),
    },
  },
  {
    id: 'G4-provider-runtime-peer',
    lane: 'provider',
    expect: 'accept',
    topic: 'runtime-dev-dependency',
    why: 'provider runtime may reach peerDependencies',
    files: {
      'providers/typescript/package.json': providerManifest(m => { m.peerDependencies = { ...(m.peerDependencies || {}), 'compiler-api': '1.0.0' }; delete m.dependencies['compiler-api']; }),
    },
  },
  {
    id: 'G4-provider-runtime-optional',
    lane: 'provider',
    expect: 'accept',
    topic: 'runtime-dev-dependency',
    why: 'provider runtime may reach optionalDependencies',
    files: {
      'providers/typescript/package.json': providerManifest(m => { m.optionalDependencies = { ...(m.optionalDependencies || {}), 'compiler-api': '1.0.0' }; delete m.dependencies['compiler-api']; }),
    },
  },
  {
    id: 'G4-provider-runtime-devdep',
    lane: 'provider',
    expect: 'refuse',
    refuse: ['runtime-dev-dependency'],
    topic: 'runtime-dev-dependency',
    why: 'provider runtime (not scripts/) reaching compiler-api only via devDependencies must refuse; tooling-in-devDep is not a provider runtime exception',
    files: {
      'providers/typescript/package.json': providerManifest(m => { delete m.dependencies['compiler-api']; m.devDependencies['compiler-api'] = '1.0.0'; }),
    },
  },
  {
    id: 'G4-unbound-empty-target-loader',
    lane: 'contracts',
    expect: 'accept',
    topic: 'unbound-tooling-trust',
    why: 'unbound trial may apply an exact empty-target dynamic-loader; this is a disclosed unanalyzed hole, not product policy',
    files: {
      'tools/contracts/generate.cjs': 'const api = require("compiler-api");\nconst { join } = require("node:path");\nconst plugin = require(process.env.OPENSIP_PLUGIN || "./missing.cjs");\nmodule.exports = function outputPath() {\n  return join("generated", api.name, String(plugin));\n};\n',
    },
    edit: (record, root) => record.trustedUsages.push(loaderRecord(root, 'tools/contracts/generate.cjs', [])),
  },
  {
    id: 'G4-unbound-overlap-provider',
    lane: 'custom',
    expect: 'exit2',
    topic: 'unbound-tooling-trust',
    why: 'an unbound tooling trial overlapping the bound typescript-provider package must exit 2',
    files: {},
    record: () => ({
      schemaVersion: 2,
      package: 'tooling',
      packageRoot: 'providers/typescript',
      manifest: 'providers/typescript/package.json',
      tsconfig: 'providers/typescript/tsconfig.json',
      inputs: ['providers/typescript/src/index.ts', 'providers/typescript/src/session.ts', 'providers/typescript/src/generated/protocol.ts', 'providers/typescript/src/compiler-adapter.cts', 'providers/typescript/scripts/bundle.cjs'],
      packageManager: { kind: 'fixture-unlocked', lockfile: null },
      trustedUsages: [],
    }),
    unbound: 'tooling',
  },
  {
    id: 'G4-unbound-under-tools-other',
    lane: 'custom',
    expect: 'accept',
    topic: 'unbound-tooling-trust',
    why: 'generic inventory tools/ grouping permits an unbound trial at tools/other; this is not a bound product package',
    files: {
      'tools/other/package.json': json({ name: 'opensip-other-tools', version: '0.0.0', private: true, dependencies: { 'compiler-api': '1.0.0' } }),
      'tools/other/generate.cjs': 'const api = require("compiler-api");\nmodule.exports = api.name;\n',
    },
    record: () => ({
      schemaVersion: 2,
      package: 'tooling',
      packageRoot: 'tools/other',
      manifest: 'tools/other/package.json',
      tsconfig: null,
      inputs: ['tools/other/generate.cjs'],
      packageManager: { kind: 'fixture-unlocked', lockfile: null },
      trustedUsages: [],
    }),
    unbound: 'tooling',
  },
];

function grade(p, run) {
  const report = run.report;
  if (p.expect === 'exit2') return run.status === 2 ? 'correct' : report?.passed ? 'missed' : 'wrong-reason';
  if (!report) return run.status === 2 ? 'invalid-invocation' : 'tool-error';
  const cats = report.refusals.map(r => r.category);
  if (p.expect === 'accept') return report.passed ? 'correct' : 'false-refusal';
  if (report.passed) return 'missed';
  return cats.some(c => p.refuse.includes(c)) ? 'correct' : 'wrong-reason';
}

fs.rmSync(path.join(scratch, 'cases'), { recursive: true, force: true });
const rows = [];
for (const p of probes) {
  const dir = path.join(scratch, 'cases', p.id);
  const root = path.join(dir, 'root');
  fs.mkdirSync(root, { recursive: true });
  writeTree(root, baseFiles());
  writeTree(root, typeof p.files === 'function' ? p.files() : p.files ?? {});
  let record, unbound;
  if (p.record) { record = p.record(); unbound = p.unbound; }
  else {
    const lanes = baseLanes();
    p.lanes?.(lanes);
    ({ record, unbound } = laneRecordFor(root, lanes, p.lane));
    p.edit?.(record, root);
  }
  const recordFile = path.join(dir, 'lane-record.json');
  fs.writeFileSync(recordFile, json(record));
  const args = [bin, '--root', root, '--lane-record', recordFile, '--design-lock', designLock, '--architecture', architecture, ...(unbound ? ['--unbound-lane', unbound] : [])];
  const c = spawnSync(NODE, args, { encoding: 'utf8', env, cwd: dir, maxBuffer: 64 * 1024 * 1024 });
  let report = null;
  try { report = JSON.parse(c.stdout); } catch { /* exit 2/3 */ }
  const run = { status: c.status, report };
  const row = {
    id: p.id,
    topic: p.topic,
    why: p.why,
    expected: p.expect === 'refuse' ? { refuse: p.refuse } : p.expect,
    status: c.status,
    passed: report?.passed ?? null,
    standing: report?.lane?.standing,
    categories: [...new Set((report?.refusals ?? []).map(r => r.category))],
    refusals: (report?.refusals ?? []).map(r => ({ category: r.category, from: r.from ?? r.file, request: r.request, message: (r.message ?? '').slice(0, 200) })),
    trustedUsagesApplied: (report?.trustedUsagesApplied ?? []).map(u => `${u.kind} ${u.file}:${u.line}`),
    stderr: c.stderr.slice(0, 400),
    grade: grade(p, run),
  };
  rows.push(row);
  process.stdout.write(`${row.id.padEnd(42)} ${row.grade.padEnd(16)} exit=${c.status} ${row.categories.join(',')}${c.status >= 2 && row.stderr ? ' ' + row.stderr.split('\n')[0].slice(0, 80) : ''}\n`);
}

const summary = {};
for (const r of rows) summary[r.grade] = (summary[r.grade] ?? 0) + 1;
const out = {
  schemaVersion: 1,
  standing: 'independent Grok executable counterexamples; not author/root tests and not product selection',
  checker: bin,
  node: spawnSync(NODE, ['-p', 'process.version'], { encoding: 'utf8' }).stdout.trim(),
  summary,
  rows,
};
const outFile = path.join(review, 'results', 'independent-probes.json');
fs.mkdirSync(path.dirname(outFile), { recursive: true });
fs.writeFileSync(outFile, json(out));
process.stdout.write(JSON.stringify(summary) + '\n');
if (rows.some(row => row.grade !== 'correct')) process.exitCode = 1;
