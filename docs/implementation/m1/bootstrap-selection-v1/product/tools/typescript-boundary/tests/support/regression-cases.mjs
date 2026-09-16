// Author-03 regression cases: review-02 required findings not already isolated by
// the reviewer probes, positive counterparts so fixes do not refuse valid code,
// and checks for the new design's own claims (inventory binding, topology,
// exact trusted usages, emitted-output mapping). Expectations are fixed from the
// build-plan boundary or from the Node oracle, before running either candidate.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const top = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const { baseFiles } = await import(path.join(top, 'baseline/subject-02-trial/harness/fixture.mjs'));
const { parse, runtimeUsages } = await import(path.join(top, 'checker/src/usages.mjs'));
const ts = createRequire(path.join(top, 'checker/package.json'))('typescript');

const json = value => JSON.stringify(value, null, 2) + '\n';
const base = baseFiles();
const manifest = (file, edit) => { const m = JSON.parse(base[file]); edit(m); return json(m); };
const help = body => ({ 'apps/report/src/help-view.ts': body + '\nexport function help(): string {\n  return "help";\n}\n' });
const legacyInput = (laneId, file, groupIndex = 0) => lanes => {
  const lane = lanes.lanes[laneId];
  lane.inputs.push(file); lane.inputs.sort();
  lane.runtimeGroups[groupIndex].files.push(file);
};
const compilerApi = branches => ({
  'node_modules/compiler-api/package.json': json({ name: 'compiler-api', version: '1.0.0', main: 'index.js', types: 'index.d.ts', exports: { '.': { types: './index.d.ts', ...branches } } }),
});

function exactUsage(root, file, predicate) {
  const text = fs.readFileSync(path.join(root, file), 'utf8');
  const usages = runtimeUsages(parse(file, text));
  const found = [...usages.loaders, ...usages.requests].find(predicate);
  if (!found) throw new Error(`fixture usage not found in ${file}`);
  return { sha256: crypto.createHash('sha256').update(text).digest('hex'), line: found.line, column: found.column, text: found.text };
}

const COMPUTED_GENERATE = 'const { join } = require("node:path");\nconst target = join(__dirname, "target.cjs");\nconst loaded = require(target);\nmodule.exports = function outputPath() {\n  return loaded.name;\n};\n';
const TARGET = { 'tools/contracts/target.cjs': 'module.exports = { name: "target" };\n' };
const loaderRecord = (sha, targets) => (record, root) => {
  const usage = exactUsage(root, 'tools/contracts/generate.cjs', u => u.kind === 'computed-require');
  record.trustedUsages.push({ kind: 'dynamic-loader', file: 'tools/contracts/generate.cjs', ...usage, sha256: sha ?? usage.sha256, targets, reason: 'regression fixture: computed require of a declared sibling' });
};

export const regressionCases = [
  // TypeScript emit paths: .js output paths resolve authored .ts sources.
  { id: 'A3-P01-provider-outdir-emitted-output', lane: 'provider', expect: 'accept',
    why: 'with outDir, runtime requests are resolved from emitted locations and ./session.js maps to the planned output of session.ts',
    files: { 'providers/typescript/tsconfig.json': manifest('providers/typescript/tsconfig.json', m => { m.compilerOptions.outDir = 'dist'; }) } },
  { id: 'A3-N01-emitted-relative-output-missing', lane: 'provider', refuse: ['unresolved'],
    why: 'a .js request with neither a file nor a planned TypeScript output must not be treated as no edge',
    files: { 'providers/typescript/src/session.ts': 'import type { Frame } from "#generated/protocol.js";\nimport { later } from "./missing-output.js";\nexport function createSession(_read: unknown, frame: Frame): string {\n  return frame.kind + String(later);\n}\n' } },
  { id: 'A3-P05-ts-nodenext-commonjs-scope', lane: 'contracts', expect: 'accept',
    why: 'counterpart to RV-N19: NodeNext in a CommonJS scope emits require, so the valid require branch is used although the import branch is missing',
    files: { ...compilerApi({ import: './missing.mjs', require: './index.js' }),
      'tools/contracts/tsconfig.json': json({ compilerOptions: { target: 'ES2022', module: 'NodeNext', moduleResolution: 'NodeNext', types: [], allowJs: true, checkJs: false, noEmit: true }, include: ['*.cjs', '*.ts'] }),
      'tools/contracts/gen.ts': 'import { name } from "compiler-api";\nexport const n = name;\n' },
    lanes: legacyInput('contracts', 'tools/contracts/gen.ts'),
    oracle: [{ from: 'tools/contracts/gen.ts', emit: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2022 } }] },

  // Node 24 runtime resolution counterparts.
  { id: 'A3-P02-node-require-esm-mjs', lane: 'contracts', expect: 'accept',
    why: 'Node 24 require() of an explicit .mjs without top-level await loads',
    files: { 'tools/contracts/esm-helper.mjs': 'export const helper = "esm";\n',
      'tools/contracts/generate.cjs': 'const api = require("compiler-api");\nconst { helper } = require("./esm-helper.mjs");\nmodule.exports = function outputPath() {\n  return api.name + helper;\n};\n' },
    lanes: legacyInput('contracts', 'tools/contracts/esm-helper.mjs'),
    oracle: [{ from: 'tools/contracts/generate.cjs', request: './esm-helper.mjs', mode: 'require' }] },
  { id: 'A3-N02-hash-import-maps-to-external', lane: 'provider', refuse: ['external-by-path'],
    why: 'a package imports (#) mapping into node_modules bypasses the declared-dependency request name (fail-closed, R5 family)',
    files: { 'providers/typescript/package.json': manifest('providers/typescript/package.json', m => { m.imports['#dep'] = 'dep'; }),
      'providers/typescript/scripts/bundle.cjs': 'const path = require("node:path");\nconst dep = require("#dep");\nmodule.exports = path.join("out", dep.parseMode);\n' } },

  // AMD (R3 family): declared inputs are covered by RV-F01.
  { id: 'A3-N03-browser-external-amd-define', lane: 'report', refuse: ['unsupported-module-format'],
    why: 'bundlers follow AMD define dependencies; an AMD request in the browser runtime closure must not be silently absent',
    files: { 'node_modules/dep/browser.mjs': 'export const parseMode = "browser";\nif (typeof define === "function") define(["node-only"], function () { return 1; });\n' } },
  { id: 'A3-P03-node-external-umd-inert', lane: 'contracts', expect: 'accept',
    why: 'a UMD wrapper in a Node-group dependency takes the CommonJS branch; its AMD branch is inert without an AMD loader',
    files: { 'node_modules/compiler-api/index.js': '(function (factory) {\n  if (typeof define === "function" && define.amd) define([], factory);\n  else module.exports = factory();\n})(function () { return { name: "compiler-api" }; });\n' },
    oracle: [{ from: 'tools/contracts/generate.cjs', request: 'compiler-api', mode: 'require' }] },
  { id: 'A3-N09-computed-loader-in-external', lane: 'contracts', refuse: ['unsupported-loader'],
    why: 'a computed require inside a reached dependency is not treated as no edge',
    files: { 'node_modules/compiler-api/index.js': 'const name = "./impl.js";\nexports.name = require(name).name;\n', 'node_modules/compiler-api/impl.js': 'exports.name = "impl";\n' } },

  // Exact trusted usages (dynamic loaders and optional unresolved requests).
  { id: 'A3-P04-trusted-loader-exact', lane: 'contracts', expect: 'accept', newOnly: true,
    why: 'an exact reviewed dynamic-loader record with declared targets is analyzed, not waived',
    files: { 'tools/contracts/generate.cjs': COMPUTED_GENERATE, ...TARGET }, lanes: legacyInput('contracts', 'tools/contracts/target.cjs'),
    recordEdit: loaderRecord(undefined, ['tools/contracts/target.cjs']) },
  { id: 'A3-N04-trusted-loader-wrong-sha', lane: 'contracts', refuse: ['unsupported-loader', 'lane-record-invalid'], newOnly: true,
    why: 'a record bound to other bytes must not cover the loader',
    files: { 'tools/contracts/generate.cjs': COMPUTED_GENERATE, ...TARGET }, lanes: legacyInput('contracts', 'tools/contracts/target.cjs'),
    recordEdit: loaderRecord('0'.repeat(64), ['tools/contracts/target.cjs']) },
  { id: 'A3-N05-trusted-loader-undeclared-target', lane: 'contracts', refuse: ['lane-record-invalid'], newOnly: true,
    why: 'a trusted loader cannot introduce an undeclared target',
    files: { 'tools/contracts/generate.cjs': COMPUTED_GENERATE, ...TARGET, 'tools/contracts/other.cjs': 'module.exports = {};\n' }, lanes: lanes => { legacyInput('contracts', 'tools/contracts/target.cjs')(lanes); legacyInput('contracts', 'tools/contracts/other.cjs')(lanes); },
    recordEdit: loaderRecord(undefined, ['tools/contracts/undeclared.cjs']) },
  { id: 'A3-N06-optional-unresolved-unguarded', lane: 'provider', refuse: ['unresolved', 'lane-record-invalid'], newOnly: true,
    why: 'an optional-unresolved record only covers a request guarded by try',
    files: { 'node_modules/compiler-api/index.js': 'require("optional-peer");\nexports.name = "compiler-api";\n' },
    recordEdit: (record, root) => {
      const usage = exactUsage(root, 'node_modules/compiler-api/index.js', u => u.request === 'optional-peer');
      record.trustedUsages.push({ kind: 'optional-unresolved', file: 'node_modules/compiler-api/index.js', ...usage, request: 'optional-peer', mode: 'require', reason: 'regression fixture' });
    } },

  // Inventory binding, invocation and topology.
  { id: 'A3-X01-package-not-typescript-inventory-package', lane: 'report', expect: 'exit2', newOnly: true,
    why: 'a lane record naming a non-TypeScript inventory package is invalid input', recordEdit: record => { record.package = 'opensip-host'; } },
  { id: 'A3-X02-unbound-flag-on-bound-package', lane: 'report', expect: 'exit2', newOnly: true,
    why: 'an inventory-bound lane cannot be downgraded to an unbound trial', args: ['--unbound-lane', 'tooling'] },
  { id: 'A3-X03-inventory-pin-tamper', lane: 'report', expect: 'exit2', newOnly: true,
    why: 'selected inventory bytes that differ from the design-lock pin must refuse',
    architectureEdit: dir => { fs.appendFileSync(path.join(dir, 'fixture-boundary-inventory.v1.json'), ' '); } },
  { id: 'A3-N07-pnpm-lane-without-materialization-record', lane: 'contracts', refuse: ['topology'], newOnly: true,
    why: 'a pnpm lane must be checked against a pnpm-materialized node_modules, not an npm or hand-made tree',
    files: { 'tools/contracts/pnpm-lock.yaml': "lockfileVersion: '9.0'\n" },
    recordEdit: record => { record.packageManager = { kind: 'pnpm', lockfile: 'tools/contracts/pnpm-lock.yaml' }; } },
  { id: 'A3-N08-undeclared-unreached-source', lane: 'report', refuse: ['undeclared-local'],
    why: 'a caller cannot hide lane sources by omitting them from both inputs and imports',
    files: { 'apps/report/tools/orphan.mjs': 'export const orphan = 1;\n' } },

  // Browser worker/asset URLs (A4).
  { id: 'A3-P06-browser-worker-url-own-output', lane: 'report', expect: 'accept',
    why: 'a worker URL to ./worker.js maps to the planned output of a declared worker.ts and is followed',
    files: { 'apps/report/src/worker.ts': 'export const work = 1;\n', ...help('export const start = () => new Worker(new URL("./worker.js", import.meta.url), { type: "module" });') },
    lanes: legacyInput('report', 'apps/report/src/worker.ts') },
  { id: 'A3-N10-browser-worker-url-missing', lane: 'report', refuse: ['unresolved'],
    why: 'a worker URL with no file and no planned output is not treated as no edge',
    files: help('export const start = () => new Worker(new URL("./absent-worker.js", import.meta.url), { type: "module" });') },

  // Added after the first mutation run to isolate checks that other rules masked.
  { id: 'A3-N11-npm-alias-targets-local-name', lane: 'report', refuse: ['local-name-shadow'],
    why: 'npm layout: an npm: alias whose target is a local package name lives under the alias directory, so only the manifest alias check sees the local name',
    files: {
      'node_modules/helper/package.json': json({ name: '@opensip/typescript-provider', version: '0.1.0', main: 'index.js', module: 'index.mjs' }),
      'node_modules/helper/index.mjs': 'export const x = 1;\n', 'node_modules/helper/index.js': 'exports.x = 1;\n',
      'apps/report/package.json': manifest('apps/report/package.json', m => { m.dependencies.helper = 'npm:@opensip/typescript-provider@0.1.0'; }),
      ...help('import { x } from "helper";\nexport const h = x;'),
    } },
  { id: 'A3-N12-optional-record-wrong-mode', lane: 'provider', refuse: ['unresolved', 'lane-record-invalid'], newOnly: true,
    why: 'an optional-unresolved record is bound to the usage mode; a record claiming import mode does not cover a guarded require',
    files: { 'node_modules/compiler-api/index.js': 'try { require("optional-peer"); } catch {}\nexports.name = "compiler-api";\n' },
    recordEdit: (record, root) => {
      const usage = exactUsage(root, 'node_modules/compiler-api/index.js', u => u.request === 'optional-peer');
      record.trustedUsages.push({ kind: 'optional-unresolved', file: 'node_modules/compiler-api/index.js', ...usage, request: 'optional-peer', mode: 'import', reason: 'regression fixture: wrong mode' });
    } },
  { id: 'A3-N13-external-request-realizes-local-package-directory', lane: 'report', refuse: ['local-name-shadow'],
    why: 'a dependency requests a non-local name that pnpm realizes into a store directory of a local package name',
    files: {
      'node_modules/shadow-alias': { symlink: '.pnpm/@opensip+typescript-provider@0.1.0/node_modules/@opensip/typescript-provider' },
      'node_modules/.pnpm/@opensip+typescript-provider@0.1.0/node_modules/@opensip/typescript-provider/package.json': json({ name: '@opensip/typescript-provider', version: '0.1.0', main: 'index.js', module: 'index.mjs' }),
      'node_modules/.pnpm/@opensip+typescript-provider@0.1.0/node_modules/@opensip/typescript-provider/index.mjs': 'export const x = 1;\n',
      'node_modules/.pnpm/@opensip+typescript-provider@0.1.0/node_modules/@opensip/typescript-provider/index.js': 'exports.x = 1;\n',
      'node_modules/dep/browser.mjs': 'import { x } from "shadow-alias";\nexport const parseMode = String(x);\n',
    } },
  { id: 'A3-N14-jsx-implicit-runtime-import-unmodelled', lane: 'report', refuse: ['compiler-unexplained-input'],
    why: 'react-jsx makes TypeScript load an implicit react/jsx-runtime import that the extractor does not model; the completeness cross-check refuses instead of omitting the build edge',
    files: {
      'apps/report/tsconfig.json': manifest('apps/report/tsconfig.json', m => { m.compilerOptions.jsx = 'react-jsx'; m.include = [...m.include, 'src/**/*.tsx']; }),
      'apps/report/package.json': manifest('apps/report/package.json', m => { m.dependencies.react = '19.0.0'; }),
      'node_modules/react/package.json': json({ name: 'react', version: '19.0.0', exports: { './jsx-runtime': { types: './jsx-runtime.d.ts', default: './jsx-runtime.js' } } }),
      'node_modules/react/jsx-runtime.d.ts': 'export declare function jsx(type: unknown, props: unknown): unknown;\nexport declare namespace JSX { interface IntrinsicElements { [name: string]: unknown } }\n',
      'node_modules/react/jsx-runtime.js': 'export function jsx() { return null; }\n',
      'apps/report/src/badge.tsx': 'export const Badge = () => <span>badge</span>;\n',
    },
    lanes: legacyInput('report', 'apps/report/src/badge.tsx') },

  // Dependency class policy positive control (A5 proposal).
  { id: 'A3-P07-provider-build-script-dev-dependency', lane: 'provider', expect: 'accept',
    why: 'build scripts may use devDependencies; only provider runtime groups are restricted',
    files: { 'providers/typescript/package.json': manifest('providers/typescript/package.json', m => { m.devDependencies['dev-only'] = '1.0.0'; }),
      'node_modules/dev-only/package.json': json({ name: 'dev-only', version: '1.0.0', main: 'index.js' }), 'node_modules/dev-only/index.js': 'exports.devValue = 1;\n',
      'providers/typescript/scripts/bundle.cjs': 'const path = require("node:path");\nconst dep = require("dep");\nconst dev = require("dev-only");\nmodule.exports = path.join("out", dep.parseMode, String(dev.devValue));\n' } },
];

// Root04: isolate guards masked by the stricter bound-lane policy or the new
// realized-manifest identity check. Original cases above remain intact.
const rootCase = id => regressionCases.find(row => row.id === id);
for (const [id, source] of [['ROOT04-N01-unbound-optional-unguarded', 'A3-N06-optional-unresolved-unguarded'], ['ROOT04-N02-unbound-optional-wrong-mode', 'A3-N12-optional-record-wrong-mode']]) {
  regressionCases.push({ ...rootCase(source), id, lane: 'contracts', why: 'unbound tooling trial isolates the optional exception guard; it cannot grant exceptions to bound product lanes' });
}
regressionCases.push({ id: 'ROOT04-P01-unbound-optional-guarded', lane: 'contracts', expect: 'accept', newOnly: true,
  files: { 'node_modules/compiler-api/index.js': 'try { require("optional-peer"); } catch {}\nexports.name = "compiler-api";\n' },
  recordEdit: (record, root) => {
    const usage = exactUsage(root, 'node_modules/compiler-api/index.js', u => u.request === 'optional-peer');
    record.trustedUsages.push({ kind: 'optional-unresolved', file: 'node_modules/compiler-api/index.js', ...usage, request: 'optional-peer', mode: 'require', reason: 'root04 positive unbound trial control' });
  } });
regressionCases.push({ id: 'ROOT04-N03-unbound-stale-record', lane: 'contracts', refuse: ['lane-record-invalid'], newOnly: true,
  files: { 'node_modules/compiler-api/index.js': 'const optional = require("node:path");\nexports.name = optional.sep;\n' },
  recordEdit: (record, root) => {
    const usage = exactUsage(root, 'node_modules/compiler-api/index.js', u => u.request === 'node:path');
    record.trustedUsages.push({ kind: 'optional-unresolved', file: 'node_modules/compiler-api/index.js', ...usage, request: 'node:path', mode: 'require', reason: 'root04 stale record for a resolved built-in' });
  } });
for (const [id, source, file] of [
  ['ROOT04-N04-alias-identity-independent', 'A3-N11-npm-alias-targets-local-name', 'node_modules/helper/package.json'],
  ['ROOT04-N05-directory-identity-independent', 'A3-N13-external-request-realizes-local-package-directory', 'node_modules/.pnpm/@opensip+typescript-provider@0.1.0/node_modules/@opensip/typescript-provider/package.json'],
]) {
  const original = rootCase(source);
  const materialized = JSON.parse(original.files[file]); materialized.name = 'external-package';
  regressionCases.push({ ...original, id, newOnly: true, files: { ...original.files, [file]: json(materialized) }, why: 'isolate name check from the independent realized manifest-name refusal' });
}
