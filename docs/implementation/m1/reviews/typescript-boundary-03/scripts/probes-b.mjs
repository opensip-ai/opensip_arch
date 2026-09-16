// Independent review-03 probes against author-03 candidate B (and, where it
// applies, frozen candidate A). Expectations are fixed here before execution and
// come from the build-plan boundary policy or from Node 24 itself. The checker is
// run only from the reviewer's mutable copy. Node oracles run AFTER the checker
// and load only reviewer-authored fixture stubs; no-execution probes are never
// oracled. usage: node probes-b.mjs [--only REGEX] [--out FILE] [--checker BIN]
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { spawnSync } from 'node:child_process';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const review = fs.realpathSync(path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..'));
const copy = path.join(review, 'work/copy');
const argv = process.argv.slice(2);
const opt = n => { const i = argv.indexOf(n); return i >= 0 ? argv[i + 1] : undefined; };
const only = opt('--only') ? new RegExp(opt('--only')) : null;
const out = path.resolve(opt('--out') ?? path.join(review, 'evidence/probes-b.json'));
const bin = fs.realpathSync(opt('--checker') ?? path.join(copy, 'checker/bin/check-boundary.mjs'));
const label = path.basename(out, '.json');
const scratch = path.join(review, 'work/probes-b', label);
const tmp = path.join(review, 'work/tmp');
fs.mkdirSync(tmp, { recursive: true });
const env = { ...process.env, TMPDIR: tmp };
const NODE = process.execPath;

const { baseFiles, baseLanes, writeTree } = await import(path.join(copy, 'baseline/subject-02-trial/harness/fixture.mjs'));
const { laneRecordFor } = await import(path.join(copy, 'harness/adapter.mjs'));
const { parse, runtimeUsages } = await import(path.join(copy, 'checker/src/usages.mjs'));
const ts = createRequire(path.join(copy, 'checker/package.json'))('typescript');

const json = v => JSON.stringify(v, null, 2) + '\n';
const base = baseFiles();
const manifest = (file, edit) => { const m = JSON.parse(base[file]); edit(m); return json(m); };
const reportDeps = extra => manifest('apps/report/package.json', m => Object.assign(m.dependencies, extra));
const providerManifest = edit => manifest('providers/typescript/package.json', edit);
const contractsDeps = extra => manifest('tools/contracts/package.json', m => Object.assign(m.dependencies, extra));
const help = body => ({ 'apps/report/src/help-view.ts': body + '\nexport function help(): string {\n  return "help";\n}\n' });
const pkg = (name, fields) => json({ name, version: '1.0.0', ...fields });
const GENERATE = extra => `const api = require("compiler-api");\nconst { join } = require("node:path");\nconst extra = require("${extra}");\nmodule.exports = function outputPath() {\n  return join("generated", api.name, String(extra.name));\n};\n`;
const BUNDLE = extra => `const path = require("node:path");\nconst dep = require("dep");\nconst extra = require(${JSON.stringify(extra)});\nmodule.exports = path.join("out", dep.parseMode, String(extra));\n`;
const compilerApi = branches => ({
  'node_modules/compiler-api/package.json': json({ name: 'compiler-api', version: '1.0.0', main: 'index.js', types: 'index.d.ts', exports: { '.': { types: './index.d.ts', ...branches } } }),
  'node_modules/compiler-api/esm.mjs': 'export const name = "compiler-api-esm";\n',
});
const depFiles = () => Object.fromEntries(Object.entries(base).filter(([n]) => n.startsWith('node_modules/dep/')).map(([n, v]) => [n.slice('node_modules/dep/'.length), v]));
const reportTsconfig = edit => manifest('apps/report/tsconfig.json', edit);
const providerTsconfig = edit => manifest('providers/typescript/tsconfig.json', edit);

// Exact trusted-usage record for a computed loader in a materialized file, as a caller could write it.
function loaderRecord(root, file, targets = []) {
  const text = fs.readFileSync(path.join(root, file), 'utf8');
  const loader = runtimeUsages(parse(path.join(root, file), text)).loaders[0];
  if (!loader) throw new Error('no loader in ' + file);
  return { kind: 'dynamic-loader', file, sha256: crypto.createHash('sha256').update(text).digest('hex'), line: loader.line, column: loader.column, text: loader.text, targets, reason: 'caller-written exemption (reviewer probe)' };
}

const MARK = name => path.join(scratch, 'markers', name);
const probes = [
  // ---------- positive controls ----------
  { id: 'RV3-C00-report', lane: 'report', expect: 'accept', why: 'unchanged payload' },
  { id: 'RV3-C00-provider', lane: 'provider', expect: 'accept', why: 'unchanged payload' },
  { id: 'RV3-C00-contracts', lane: 'contracts', expect: 'accept', why: 'unchanged payload (unbound tooling trial)' },

  // ---------- review-02 R2..R7 reproduced ----------
  { id: 'RV3-R2-browser-elided-static-plus-import', lane: 'report', expect: 'refuse', refuse: ['browser-node'], finding: 'R2',
    files: { 'node_modules/node-only/package.json': pkg('node-only', { main: 'index.js', types: 'index.d.ts' }), 'node_modules/node-only/index.js': 'const fs = require("node:fs");\nexports.read = fs.readFileSync;\n',
      'node_modules/node-only/index.d.ts': 'export declare type Reader = (path: string) => string;\n', 'apps/report/package.json': reportDeps({ 'node-only': '1.0.0' }),
      ...help('import { Reader } from "node-only";\nexport type R = Reader;\nexport const load = () => import("node-only");') } },
  { id: 'RV3-R3a-amd-define-cross-lane-cjs', lane: 'provider', expect: 'refuse', refuse: ['unsupported-module-format', 'lane-escape'], finding: 'R3',
    files: { 'providers/typescript/scripts/bundle.cjs': 'define(["../../../apps/report/src/view-state.ts"], function (view) {\n  return String(view);\n});\n' } },
  { id: 'RV3-R3b-amd-require-array-cross-lane-ts', lane: 'report', expect: 'refuse', refuse: ['unsupported-module-format', 'lane-escape'], finding: 'R3',
    files: help('declare const require: (deps: string[], cb: () => void) => void;\nrequire(["../../../providers/typescript/src/index.js"], () => {});') },
  { id: 'RV3-R4a-module-sync-require-missing', lane: 'contracts', expect: 'refuse', refuse: ['unresolved'], finding: 'R4',
    files: { 'node_modules/sync/package.json': pkg('sync', { exports: { '.': { 'module-sync': './missing.mjs', default: './index.js' } } }), 'node_modules/sync/index.js': 'exports.name = "cjs";\n',
      'tools/contracts/package.json': contractsDeps({ sync: '1.0.0' }), 'tools/contracts/generate.cjs': GENERATE('sync') },
    oracle: [{ from: 'tools/contracts/generate.cjs', request: 'sync', mode: 'require' }] },
  { id: 'RV3-R4b-module-sync-require-selected', lane: 'contracts', expect: 'accept', finding: 'R4',
    files: { 'node_modules/sync/package.json': pkg('sync', { exports: { '.': { 'module-sync': './ok.mjs', require: './missing.cjs', default: './missing.cjs' } } }), 'node_modules/sync/ok.mjs': 'export const name = "ok";\n',
      'tools/contracts/package.json': contractsDeps({ sync: '1.0.0' }), 'tools/contracts/generate.cjs': GENERATE('sync') },
    oracle: [{ from: 'tools/contracts/generate.cjs', request: 'sync', mode: 'require' }] },
  { id: 'RV3-R4c-module-sync-import-mode-missing', lane: 'report', expect: 'refuse', refuse: ['unresolved'], finding: 'R4 (new: import mode)',
    files: { 'node_modules/sync/package.json': pkg('sync', { exports: { '.': { 'module-sync': './missing.mjs', import: './ok.mjs', default: './ok.mjs' } } }), 'node_modules/sync/ok.mjs': 'export const name = "ok";\n',
      'apps/report/package.json': reportDeps({ sync: '1.0.0' }),
      'apps/report/build.mjs': 'import { existsSync } from "node:fs";\nimport { parseMode } from "dep";\nimport { name } from "sync";\nexport const ready = existsSync("dist") ? parseMode + name : "";\n' },
    oracle: [{ from: 'apps/report/build.mjs', request: 'sync', mode: 'import' }] },
  { id: 'RV3-R4d-esm-extensionless', lane: 'report', expect: 'refuse', refuse: ['unresolved'], finding: 'R4',
    files: { 'node_modules/dep/import.mjs': 'export { parseMode } from "./helper";\n', 'node_modules/dep/helper.mjs': 'export const parseMode = "import";\n' },
    oracle: [{ from: 'apps/report/build.mjs', request: 'dep', mode: 'import' }] },
  { id: 'RV3-R4e-require-mjs-extensionless', lane: 'contracts', expect: 'refuse', refuse: ['unresolved'], finding: 'R4',
    files: { 'node_modules/compiler-api/index.js': 'const impl = require("./impl");\nexports.name = impl.name;\n', 'node_modules/compiler-api/impl.mjs': 'export const name = "impl";\n' },
    oracle: [{ from: 'tools/contracts/generate.cjs', request: 'compiler-api', mode: 'require' }] },
  { id: 'RV3-R4f-esm-directory-import', lane: 'report', expect: 'refuse', refuse: ['unresolved'], finding: 'R4',
    files: { 'node_modules/dep/import.mjs': 'export { parseMode } from "./lib";\n', 'node_modules/dep/lib/index.mjs': 'export const parseMode = "import";\n' },
    oracle: [{ from: 'apps/report/build.mjs', request: 'dep', mode: 'import' }] },
  { id: 'RV3-R5a-relative-node_modules-undeclared', lane: 'report', expect: 'refuse', refuse: ['external-by-path', 'undeclared-external', 'lane-escape'], finding: 'R5',
    files: help('import { name } from "../../../node_modules/compiler-api/index.js";\nexport const n = name;') },
  { id: 'RV3-R5b-bare-dotdot-traversal-undeclared', lane: 'provider', expect: 'refuse', refuse: ['undeclared-external', 'external-by-path', 'unresolved'], finding: 'R5 (new: bare specifier with ..)',
    why: 'Node require("compiler-api/../undeclared-pkg/index.js") loads a package the lane never declared',
    files: { 'node_modules/undeclared-pkg/package.json': pkg('undeclared-pkg', { main: 'index.js' }), 'node_modules/undeclared-pkg/index.js': 'module.exports = "undeclared";\n',
      'providers/typescript/scripts/bundle.cjs': BUNDLE('compiler-api/../undeclared-pkg/index.js') },
    oracle: [{ from: 'providers/typescript/scripts/bundle.cjs', request: 'compiler-api/../undeclared-pkg/index.js', mode: 'require' }] },
  { id: 'RV3-R5c-bare-dotdot-traversal-browser', lane: 'report', expect: 'refuse', refuse: ['undeclared-external', 'external-by-path', 'unresolved'], finding: 'R5 (new)',
    files: { 'node_modules/legacy/package.json': pkg('legacy', { main: 'index.js' }), 'node_modules/legacy/index.js': 'exports.x = 1;\n',
      'node_modules/undeclared-pkg/package.json': pkg('undeclared-pkg', { main: 'index.js' }), 'node_modules/undeclared-pkg/index.js': 'exports.u = 1;\n',
      'apps/report/package.json': reportDeps({ legacy: '1.0.0' }),
      ...help('// @ts-ignore\nimport { u } from "legacy/../undeclared-pkg/index.js";\nexport const uu = u;') } },
  { id: 'RV3-R6a-pnpm-alias-shadow', lane: 'report', expect: 'refuse', refuse: ['local-name-shadow'], finding: 'R6',
    files: { 'node_modules/@opensip/typescript-provider': { symlink: '../.pnpm/evil@0.1.0/node_modules/evil' },
      'node_modules/.pnpm/evil@0.1.0/node_modules/evil/package.json': json({ name: 'evil', version: '0.1.0', main: 'index.js', types: 'index.d.ts' }),
      'node_modules/.pnpm/evil@0.1.0/node_modules/evil/index.js': 'exports.x = 1;\n', 'node_modules/.pnpm/evil@0.1.0/node_modules/evil/index.d.ts': 'export declare const x: number;\n',
      'apps/report/package.json': reportDeps({ '@opensip/typescript-provider': 'npm:evil@0.1.0' }), ...help('import { x } from "@opensip/typescript-provider";\nexport const shadow = x;') } },
  { id: 'RV3-R6b-versionless-scoped-alias-to-local', lane: 'report', expect: 'refuse', refuse: ['local-name-shadow'], finding: 'R6 (new: version-less scoped alias)',
    why: '"shadow": "npm:@opensip/typescript-provider" (no version) aliases a local package name; npm layout directory is node_modules/shadow',
    files: { 'node_modules/shadow/package.json': json({ name: '@opensip/typescript-provider', version: '0.1.0', main: 'index.js', types: 'index.d.ts' }),
      'node_modules/shadow/index.js': 'exports.x = 1;\n', 'node_modules/shadow/index.d.ts': 'export declare const x: number;\n',
      'apps/report/package.json': reportDeps({ shadow: 'npm:@opensip/typescript-provider' }), ...help('import { x } from "shadow";\nexport const s = x;') } },
  { id: 'RV3-R6c-realized-manifest-name-local', lane: 'report', expect: 'refuse', refuse: ['local-name-shadow'], finding: 'R6 (new: realized package name)',
    why: 'non-alias dependency whose materialized package.json name is a local package name',
    files: { 'node_modules/shadow2/package.json': json({ name: '@opensip/typescript-provider', version: '0.1.0', main: 'index.js', types: 'index.d.ts' }),
      'node_modules/shadow2/index.js': 'exports.x = 1;\n', 'node_modules/shadow2/index.d.ts': 'export declare const x: number;\n',
      'apps/report/package.json': reportDeps({ shadow2: '0.1.0' }), ...help('import { x } from "shadow2";\nexport const s = x;') } },
  { id: 'RV3-R7a-esnext-emit-commonjs-scope', lane: 'contracts', expect: 'refuse', refuse: ['unresolved', 'unsupported-module-format'], finding: 'R7',
    files: { ...compilerApi({ import: './missing.mjs', require: './index.js' }),
      'tools/contracts/tsconfig.json': json({ compilerOptions: { target: 'ES2022', module: 'ESNext', moduleResolution: 'Bundler', types: [], allowJs: true, checkJs: false, noEmit: true }, include: ['*.cjs', '*.ts'] }),
      'tools/contracts/gen.ts': 'import { name } from "compiler-api";\nexport const n = name;\n' },
    lanes: l => { const c = l.lanes.contracts; c.inputs.push('tools/contracts/gen.ts'); c.inputs.sort(); c.runtimeGroups[0].files.push('tools/contracts/gen.ts'); },
    oracle: [{ from: 'tools/contracts/gen.ts', emit: { module: ts.ModuleKind.ESNext, target: ts.ScriptTarget.ES2022 } }] },
  { id: 'RV3-R7b-preserve-emit-commonjs-scope', lane: 'contracts', expect: 'refuse', refuse: ['unresolved', 'unsupported-module-format'], finding: 'R7 (new: module preserve)',
    files: { ...compilerApi({ import: './missing.mjs', require: './index.js' }),
      'tools/contracts/tsconfig.json': json({ compilerOptions: { target: 'ES2022', module: 'Preserve', moduleResolution: 'Bundler', types: [], allowJs: true, checkJs: false, noEmit: true }, include: ['*.cjs', '*.ts'] }),
      'tools/contracts/gen.ts': 'import { name } from "compiler-api";\nexport const n = name;\n' },
    lanes: l => { const c = l.lanes.contracts; c.inputs.push('tools/contracts/gen.ts'); c.inputs.sort(); c.runtimeGroups[0].files.push('tools/contracts/gen.ts'); },
    oracle: [{ from: 'tools/contracts/gen.ts', emit: { module: ts.ModuleKind.Preserve, target: ts.ScriptTarget.ES2022 } }] },
  { id: 'RV3-R7c-commonjs-emit-in-module-scope', lane: 'provider', expect: 'refuse', refuse: ['unsupported-module-format', 'config-invalid'], finding: 'R7 (new control)',
    why: 'module CommonJS emits require into .js inside a type:module package; Node cannot load it',
    files: { 'providers/typescript/tsconfig.json': providerTsconfig(m => { m.compilerOptions.module = 'CommonJS'; m.compilerOptions.moduleResolution = 'Node10'; }) } },

  // ---------- new counterexamples: authority, ownership, config, execution ----------
  { id: 'RV3-X01-unbound-lane-inside-bound-package', lane: 'custom', expect: 'exit2', finding: 'unbound overlap',
    why: 'a caller runs a subtree of the bound report package as an unbound tooling lane, getting Node policy for browser sources',
    files: { ...help('import { existsSync } from "node:fs";\nexport const e = existsSync;'),
      'apps/report/src/package.json': json({ name: 'sub', private: true, type: 'module', dependencies: { dep: '1.0.0' } }),
      'apps/report/src/tsconfig.json': json({ compilerOptions: { target: 'ES2022', module: 'ESNext', moduleResolution: 'Bundler', lib: ['ES2022', 'DOM'], types: [], strict: true, noEmit: true, allowJs: true, paths: { '@report/*': ['./*'] } }, include: ['**/*.ts'] }) },
    record: () => ({ schemaVersion: 2, package: 'tooling', packageRoot: 'apps/report/src', manifest: 'apps/report/src/package.json', tsconfig: 'apps/report/src/tsconfig.json',
      inputs: ['apps/report/src/generated/report.ts', 'apps/report/src/help-view.ts', 'apps/report/src/index.ts', 'apps/report/src/report-view.ts', 'apps/report/src/view-state.ts'],
      packageManager: { kind: 'fixture-unlocked', lockfile: null }, trustedUsages: [] }), unbound: 'tooling' },
  { id: 'RV3-X02-caller-exempts-dependency-loader-bound-provider', lane: 'provider', expect: 'refuse', refuse: ['unsupported-loader', 'lane-record-invalid'], finding: 'exception authority',
    why: 'a bound provider runtime lane record exempts an arbitrary dependency computed require with no targets',
    files: { 'node_modules/evil/package.json': pkg('evil', { main: 'index.js' }), 'node_modules/evil/index.js': 'module.exports = require(process.env.OPENSIP_EVIL_MODULE || "./payload.js");\n',
      'node_modules/evil/payload.js': 'module.exports = 1;\n', 'providers/typescript/package.json': providerManifest(m => { m.dependencies.evil = '1.0.0'; }),
      'providers/typescript/scripts/bundle.cjs': BUNDLE('evil') },
    edit: (record, root) => record.trustedUsages.push(loaderRecord(root, 'node_modules/evil/index.js')) },
  { id: 'RV3-X03-caller-exempts-dependency-loader-bound-browser', lane: 'report', expect: 'refuse', refuse: ['unsupported-loader', 'lane-record-invalid'], finding: 'exception authority',
    why: 'a bound browser lane record exempts a dependency computed import() with no targets',
    files: { 'node_modules/evilb/package.json': pkg('evilb', { module: 'index.mjs', main: 'index.mjs' }), 'node_modules/evilb/index.mjs': 'export const load = () => import(globalThis.location.hash.slice(1));\n',
      'apps/report/package.json': reportDeps({ evilb: '1.0.0' }), ...help('// @ts-ignore\nimport { load } from "evilb";\nexport const l = load;') },
    edit: (record, root) => record.trustedUsages.push(loaderRecord(root, 'node_modules/evilb/index.mjs')) },
  { id: 'RV3-X04-tsconfig-extends-other-lane-node_modules', lane: 'report', expect: 'refuse', refuse: ['config-owner'], finding: 'config boundary',
    files: { 'providers/typescript/node_modules/shared-config/tsconfig.json': json({ compilerOptions: { strict: true } }),
      'apps/report/tsconfig.json': reportTsconfig(m => { m.extends = '../../providers/typescript/node_modules/shared-config/tsconfig.json'; }) } },
  { id: 'RV3-X05-outdir-into-other-lane', lane: 'provider', expect: 'refuse', refuse: ['config-owner', 'config-invalid'], finding: 'config boundary (advisory)',
    files: { 'providers/typescript/tsconfig.json': providerTsconfig(m => { m.compilerOptions.outDir = '../../apps/report/src/provider-out'; }) } },
  { id: 'RV3-X06a-no-execution-node', lane: 'provider', expect: 'no-execution', markers: ['boom-cjs', 'boom-esm', 'boom-plugin'], finding: 'non-executing resolution',
    files: () => ({ 'node_modules/boom/package.json': pkg('boom', { main: 'index.js', exports: { '.': { import: './esm.mjs', require: './index.js' } } }),
      'node_modules/boom/index.js': `require("node:fs").mkdirSync(${JSON.stringify(path.dirname(MARK('x')))}, { recursive: true });\nrequire("node:fs").writeFileSync(${JSON.stringify(MARK('boom-cjs'))}, "cjs");\n`,
      'node_modules/boom/esm.mjs': `import fs from "node:fs";\nfs.mkdirSync(${JSON.stringify(path.dirname(MARK('x')))}, { recursive: true });\nfs.writeFileSync(${JSON.stringify(MARK('boom-esm'))}, "esm");\n`,
      'node_modules/boom-plugin/package.json': pkg('boom-plugin', { main: 'index.js' }),
      'node_modules/boom-plugin/index.js': `require("node:fs").mkdirSync(${JSON.stringify(path.dirname(MARK('x')))}, { recursive: true });\nrequire("node:fs").writeFileSync(${JSON.stringify(MARK('boom-plugin'))}, "plugin");\nmodule.exports = () => ({ create: i => i.languageService });\n`,
      'providers/typescript/package.json': providerManifest(m => { m.dependencies.boom = '1.0.0'; m.dependencies['boom-plugin'] = '1.0.0'; }),
      'providers/typescript/tsconfig.json': providerTsconfig(m => { m.compilerOptions.plugins = [{ name: 'boom-plugin' }]; }),
      'providers/typescript/scripts/bundle.cjs': BUNDLE('boom'),
      'providers/typescript/src/session.ts': 'import type { Frame } from "#generated/protocol.js";\n// @ts-ignore\nimport "boom";\nexport function createSession(_read: unknown, frame: Frame): string {\n  return frame.kind;\n}\n' }) },
  { id: 'RV3-X06b-no-execution-browser', lane: 'report', expect: 'no-execution', markers: ['boomb-browser', 'boomb-main'], finding: 'non-executing resolution',
    files: () => ({ 'node_modules/boomb/package.json': pkg('boomb', { main: 'main.js', browser: 'browser.js' }),
      'node_modules/boomb/browser.js': `require("node:fs").mkdirSync(${JSON.stringify(path.dirname(MARK('x')))}, { recursive: true });\nrequire("node:fs").writeFileSync(${JSON.stringify(MARK('boomb-browser'))}, "b");\n`,
      'node_modules/boomb/main.js': `require("node:fs").mkdirSync(${JSON.stringify(path.dirname(MARK('x')))}, { recursive: true });\nrequire("node:fs").writeFileSync(${JSON.stringify(MARK('boomb-main'))}, "m");\n`,
      'apps/report/package.json': reportDeps({ boomb: '1.0.0' }), ...help('// @ts-ignore\nimport "boomb";') }) },
  { id: 'RV3-X07-bound-input-without-inventory-row', lane: 'report', expect: 'refuse', refuse: ['inventory-ownership', 'undeclared-local'], finding: 'inventory file ownership (advisory)',
    why: 'a bound report lane input that the selected inventory has no row for',
    files: { 'apps/report/src/unlisted-view.ts': 'export const unlisted = 1;\n', ...help('import { unlisted } from "./unlisted-view.js";\nexport const u = unlisted;') },
    lanes: l => { const r = l.lanes.report; r.inputs.push('apps/report/src/unlisted-view.ts'); r.inputs.sort(); r.runtimeGroups[0].files.push('apps/report/src/unlisted-view.ts'); } },
  { id: 'RV3-X08-type-only-paths-bypass-exports', lane: 'report', expect: 'refuse', refuse: ['external-by-path', 'unresolved'], finding: 'type-only exports bypass (advisory)',
    files: { 'node_modules/dep/internal.d.mts': 'export declare const hidden: true;\n',
      'apps/report/tsconfig.json': reportTsconfig(m => { m.compilerOptions.paths['dep/*'] = ['../../node_modules/dep/*']; }),
      ...help('import type { hidden } from "dep/internal.mjs";\nexport type H = typeof hidden;') } },
  { id: 'RV3-X09-provider-runtime-compiler-as-devdependency', lane: 'provider', expect: 'policy', finding: 'devDependency proposal vs approved ownership',
    why: 'the only real TS manifest (tools/contracts) keeps typescript in devDependencies; a provider that analyzes TS at runtime written the same way',
    files: { 'providers/typescript/package.json': providerManifest(m => { delete m.dependencies['compiler-api']; m.devDependencies['compiler-api'] = '1.0.0'; }) } },
  { id: 'RV3-X10-browser-umd-dependency', lane: 'report', expect: 'accept', finding: 'AMD over-refusal (advisory)',
    why: 'common UMD wrapper; bundlers take the CommonJS branch',
    files: { 'node_modules/umd/package.json': pkg('umd', { main: 'index.js' }),
      'node_modules/umd/index.js': '(function (root, factory) {\n  if (typeof define === "function" && define.amd) define(["exports"], factory);\n  else if (typeof exports === "object") factory(exports);\n})(this, function (exports) { exports.u = 1; });\n',
      'apps/report/package.json': reportDeps({ umd: '1.0.0' }), ...help('// @ts-ignore\nimport { u } from "umd";\nexport const uu = u;') } },
];

function oracle(root, o) {
  const from = path.join(root, o.from);
  if (o.emit) {
    const emitted = from.replace(/\.ts$/, '.oracle-emit.js');
    fs.writeFileSync(emitted, ts.transpileModule(fs.readFileSync(from, 'utf8'), { compilerOptions: o.emit }).outputText);
    const r = spawnSync(NODE, ['--no-warnings', emitted], { encoding: 'utf8', env, cwd: path.dirname(emitted) });
    return { ...o, status: r.status, error: r.status === 0 ? undefined : (r.stderr.match(/code: '([A-Z_]+)'/) ?? r.stderr.match(/(ERR_[A-Z_]+)/))?.[1] ?? 'exit ' + r.status };
  }
  const req = `const { createRequire } = require('node:module'); const r = createRequire(process.argv[1]); const out = {};
try { out.resolved = r.resolve(process.argv[2]); } catch (e) { out.error = e.code || e.message; }
if (out.resolved) { try { r(process.argv[2]); out.loaded = true; } catch (e) { out.error = e.code || String(e.message).slice(0, 160); } }
console.log(JSON.stringify(out));`;
  const imp = `import { pathToFileURL, fileURLToPath } from 'node:url'; import fs from 'node:fs'; const out = {};
try { const u = import.meta.resolve(process.argv[2], pathToFileURL(process.argv[1]).href); out.resolved = u.startsWith('file:') ? fileURLToPath(u) : u;
  if (u.startsWith('file:') && !(fs.existsSync(out.resolved) && fs.statSync(out.resolved).isFile())) out.error = 'ERR_MODULE_NOT_FOUND (not a file)'; } catch (e) { out.error = e.code || e.message; }
if (out.resolved && !out.error) { try { await import(pathToFileURL(out.resolved).href); out.loaded = true; } catch (e) { out.error = e.code || String(e.message).slice(0, 160); } }
console.log(JSON.stringify(out));`;
  const flags = o.mode === 'require' ? ['--no-deprecation', '-e', req] : ['--experimental-import-meta-resolve', '--no-warnings', '--input-type=module', '-e', imp];
  const r = spawnSync(NODE, [...flags, from, o.request], { encoding: 'utf8', env, cwd: path.dirname(from) });
  let res; try { res = JSON.parse(r.stdout); } catch { res = { error: 'harness: ' + r.stderr.slice(0, 200) }; }
  if (res.resolved && !res.resolved.startsWith('node:')) res.resolved = path.relative(root, res.resolved);
  return { ...o, ...res };
}

function grade(p, run) {
  const report = run.report;
  if (p.expect === 'exit2') return run.status === 2 ? 'correct' : report?.passed ? 'missed' : 'wrong-reason';
  if (p.expect === 'policy') return report ? (report.passed ? 'accepted' : 'refused:' + [...new Set(report.refusals.map(r => r.category))].join(',')) : 'exit' + run.status;
  if (p.expect === 'no-execution') return run.markersPresent.length ? 'EXECUTED' : 'correct';
  if (!report) return run.status === 2 ? 'invalid-invocation' : 'tool-error';
  const cats = report.refusals.map(r => r.category);
  if (p.expect === 'accept') return report.passed ? 'correct' : 'false-refusal';
  if (report.passed) return 'missed';
  return cats.some(c => p.refuse.includes(c)) ? 'correct' : 'wrong-reason';
}

fs.rmSync(scratch, { recursive: true, force: true });
const rows = [];
for (const p of probes.filter(p => !only || only.test(p.id))) {
  const dir = path.join(scratch, p.id);
  const root = path.join(dir, 'root');
  writeTree(root, baseFiles());
  writeTree(root, typeof p.files === 'function' ? p.files() : p.files ?? {});
  let record, unbound;
  if (p.record) { record = p.record(); unbound = p.unbound; }
  else {
    const lanes = baseLanes(); p.lanes?.(lanes);
    ({ record, unbound } = laneRecordFor(root, lanes, p.lane));
    p.edit?.(record, root);
  }
  const recordFile = path.join(dir, 'lane-record.json');
  fs.writeFileSync(recordFile, json(record));
  const args = [bin, '--root', root, '--lane-record', recordFile, '--design-lock', path.join(copy, 'inputs/product/design-lock.json'), '--architecture', path.join(copy, 'inputs/architecture'), ...(unbound ? ['--unbound-lane', unbound] : [])];
  const c = spawnSync(NODE, args, { encoding: 'utf8', env, cwd: dir, maxBuffer: 256 * 1024 * 1024 });
  let report = null; try { report = JSON.parse(c.stdout); } catch { /* exit 2/3 */ }
  const run = { status: c.status, report, markersPresent: (p.markers ?? []).filter(m => fs.existsSync(MARK(m))) };
  const row = { id: p.id, finding: p.finding, lane: p.lane, why: p.why, expected: p.expect === 'refuse' ? { refuse: p.refuse } : p.expect,
    status: c.status, passed: report?.passed ?? null, standing: report?.lane?.standing, categories: [...new Set((report?.refusals ?? []).map(r => r.category))],
    refusals: (report?.refusals ?? []).map(r => ({ category: r.category, from: r.from ?? r.file, request: r.request, message: (r.message ?? '').slice(0, 160) })),
    trustedUsagesApplied: (report?.trustedUsagesApplied ?? []).map(u => `${u.kind} ${u.file}:${u.line}`),
    inventoryBinding: report ? { inputsWithoutInventoryRow: report.inventoryBinding?.inputsWithoutInventoryRow, inventoryStanding: report.inventoryBinding?.inventoryStanding } : undefined,
    stderr: c.stderr.slice(0, 300), markersPresent: run.markersPresent, grade: grade(p, run) };
  if (p.oracle && p.expect !== 'no-execution') {
    row.oracle = p.oracle.map(o => oracle(root, o));
    row.nodeVerdict = row.oracle.some(o => o.error) ? 'node-fails' : 'node-loads';
    row.oracleAgrees = (row.nodeVerdict === 'node-loads') === (report?.passed === true);
  }
  rows.push(row);
  process.stdout.write(`${row.id.padEnd(58)} exit=${c.status} ${row.grade.padEnd(22)} ${row.categories.join(',')}${row.oracle ? '  node:' + row.nodeVerdict + (row.oracleAgrees ? '' : ' DISAGREES') : ''}${row.stderr && c.status >= 2 ? '  stderr:' + row.stderr.split('\n')[0].slice(0, 90) : ''}\n`);
}
const summary = {};
for (const r of rows) summary[r.grade] = (summary[r.grade] ?? 0) + 1;
fs.mkdirSync(path.dirname(out), { recursive: true });
fs.writeFileSync(out, json({ schemaVersion: 1, standing: 'independent review-03 probes against author-03 candidate B; not qualification', checker: path.relative(review, bin), node: process.version, summary, rows }));
process.stdout.write(JSON.stringify(summary) + '\n');
