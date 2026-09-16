// Independent reviewer probes (review-02). Not author-tuned: expectations come
// from the build plan's boundary policy or from Node 24 itself (oracle), and are
// fixed before running the candidate. Uses the author's shared positive payload
// from the MUTABLE copy only; the frozen subject is never executed.
//
// usage: node probes.mjs [--checker PATH] [--out FILE] [--no-oracle] [--only REGEX]
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const review = path.resolve(here, '..');
const copyTrial = path.join(review, 'work/copy/trial');
const { baseFiles, baseLanes, writeTree } = await import(path.join(copyTrial, 'harness/fixture.mjs'));
const ts = createRequire(path.join(copyTrial, 'package.json'))('typescript');

const args = process.argv.slice(2);
const opt = name => { const i = args.indexOf(name); return i >= 0 ? args[i + 1] : undefined; };
const checker = path.resolve(opt('--checker') ?? path.join(copyTrial, 'candidate/check-lane.mjs'));
const out = path.resolve(opt('--out') ?? path.join(review, 'evidence/probes.json'));
const withOracle = !args.includes('--no-oracle');
const only = opt('--only') ? new RegExp(opt('--only')) : null;
const label = path.basename(out, '.json');
const scratch = path.join(review, 'work', 'probes', label);
const tmp = path.join(review, 'work', 'tmp');
fs.mkdirSync(tmp, { recursive: true });
const env = { ...process.env, TMPDIR: tmp };

const json = v => JSON.stringify(v, null, 2) + '\n';
const base = baseFiles();
const manifest = (file, edit) => { const m = JSON.parse(base[file]); edit(m); return json(m); };
const reportDeps = extra => manifest('apps/report/package.json', m => Object.assign(m.dependencies, extra));
const contractsDeps = extra => manifest('tools/contracts/package.json', m => Object.assign(m.dependencies, extra));
const help = (body, name = 'apps/report/src/help-view.ts') => ({ [name]: body + '\nexport function help(): string {\n  return "help";\n}\n' });
const depFiles = () => Object.fromEntries(Object.entries(base).filter(([n]) => n.startsWith('node_modules/dep/')).map(([n, v]) => [n.slice('node_modules/dep/'.length), v]));
const pkg = (name, fields) => json({ name, version: '1.0.0', ...fields });
const compilerApi = branches => ({
  'node_modules/compiler-api/package.json': json({ name: 'compiler-api', version: '1.0.0', main: 'index.js', types: 'index.d.ts', exports: { '.': { types: './index.d.ts', ...branches } } }),
  'node_modules/compiler-api/esm.mjs': 'export const name = "compiler-api-esm";\n',
});
const GENERATE = extra => `const api = require("compiler-api");\nconst { join } = require("node:path");\nconst extra = require("${extra}");\nmodule.exports = function outputPath() {\n  return join("generated", api.name, String(extra.name));\n};\n`;
const NODE_ONLY = {
  'node_modules/node-only/package.json': pkg('node-only', { main: 'index.js', types: 'index.d.ts' }),
  'node_modules/node-only/index.js': 'const fs = require("node:fs");\nexports.read = fs.readFileSync;\n',
  'node_modules/node-only/index.d.ts': 'export declare type Reader = (path: string) => string;\n',
};

// kind: "boundary" (build-plan policy), "node" (Node 24 oracle is the authority),
// "trust" (demonstrates a trusted-input assumption; no pass/fail expectation).
export const probes = [
  // ---- positive controls (valid code that must be accepted) ----
  { id: 'RV-C00-report', kind: 'boundary', lane: 'report', expect: 'accept', why: 'unchanged payload' },
  { id: 'RV-C00-provider', kind: 'boundary', lane: 'provider', expect: 'accept', why: 'unchanged payload',
    variants: ['cwd-root', 'relative-root', 'symlinked-root'] },
  { id: 'RV-C00-contracts', kind: 'boundary', lane: 'contracts', expect: 'accept', why: 'unchanged payload' },
  { id: 'RV-P01-browser-wrong-condition-only-node', kind: 'boundary', lane: 'report', expect: 'accept',
    why: 'require branch (node builtin + unresolved request) is reachable only through the wrong condition for a browser static import',
    files: {
      'node_modules/iso/package.json': pkg('iso', { exports: { '.': { import: './esm.mjs', require: './cjs.cjs' } } }),
      'node_modules/iso/esm.mjs': 'export const v = 1;\n',
      'node_modules/iso/cjs.cjs': 'const fs = require("node:fs");\nrequire("./missing.cjs");\nexports.v = fs;\n',
      'apps/report/package.json': reportDeps({ iso: '1.0.0' }),
      ...help('import { v } from "iso";\nexport const iv = v;'),
    } },
  { id: 'RV-P02-cjs-wrong-condition-only-node', kind: 'node', lane: 'contracts', expect: 'accept',
    why: 'import branch has an unresolved request but a CJS require never reaches it',
    files: {
      'node_modules/iso2/package.json': pkg('iso2', { exports: { '.': { import: './esm.mjs', require: './cjs.cjs' } } }),
      'node_modules/iso2/esm.mjs': 'import "./missing.mjs";\nexport const name = 1;\n',
      'node_modules/iso2/cjs.cjs': 'exports.name = 1;\n',
      'tools/contracts/package.json': contractsDeps({ iso2: '1.0.0' }),
      'tools/contracts/generate.cjs': GENERATE('iso2'),
    },
    oracle: [{ from: 'tools/contracts/generate.cjs', request: 'iso2', mode: 'require' }] },
  { id: 'RV-P03-jsdoc-import-types-only-package', kind: 'boundary', lane: 'report', expect: 'accept',
    why: 'JSDoc @import is type-only; a declarations-only package has no runtime target (JS analogue of author P19)',
    files: {
      'node_modules/types-only/package.json': pkg('types-only', { types: 'index.d.ts' }),
      'node_modules/types-only/index.d.ts': 'export interface Shape { id: string }\n',
      'apps/report/package.json': reportDeps({ 'types-only': '1.0.0' }),
      'apps/report/build.mjs': '/** @import { Shape } from "types-only" */\nimport { existsSync } from "node:fs";\nimport { parseMode } from "dep";\n/** @type {Shape | undefined} */\nexport const ready = existsSync("dist") ? { id: parseMode } : undefined;\n',
    } },
  { id: 'RV-P05-pnpm-alias-valid', kind: 'boundary', lane: 'report', expect: 'accept',
    why: 'pnpm npm: alias to a differently named package in an in-root store',
    files: {
      'node_modules/dep': { symlink: '.pnpm/real-dep@1.0.0/node_modules/real-dep' },
      ...Object.fromEntries(Object.entries(depFiles()).map(([n, v]) => ['node_modules/.pnpm/real-dep@1.0.0/node_modules/real-dep/' + n, n === 'package.json' ? v.replace('"name": "dep"', '"name": "real-dep"') : v])),
      'apps/report/package.json': reportDeps({ dep: 'npm:real-dep@1.0.0' }),
    } },
  { id: 'RV-P06-node-module-sync-selected', kind: 'node', lane: 'contracts', expect: 'accept',
    why: 'Node 24 require conditions include module-sync, listed before require in the exports object',
    files: {
      'node_modules/sync/package.json': pkg('sync', { exports: { '.': { 'module-sync': './ok.mjs', require: './missing.cjs', default: './missing.cjs' } } }),
      'node_modules/sync/ok.mjs': 'export const name = "ok";\n',
      'tools/contracts/package.json': contractsDeps({ sync: '1.0.0' }),
      'tools/contracts/generate.cjs': GENERATE('sync'),
    },
    oracle: [{ from: 'tools/contracts/generate.cjs', request: 'sync', mode: 'require' }] },
  { id: 'RV-P07-cts-elided-static-plus-dynamic', kind: 'boundary', lane: 'provider', expect: 'accept',
    why: 'static import used only as a type is elided by TypeScript, so only import() remains at runtime',
    files: {
      ...compilerApi({ import: './esm.mjs', require: './index.js' }),
      'node_modules/compiler-api/index.d.ts': 'export declare const name: string;\nexport interface Named { id: string }\n',
      'providers/typescript/src/compiler-adapter.cts': 'import api = require("compiler-api");\nimport { Named } from "compiler-api";\nexport type N = Named;\nexport const later = () => import("compiler-api");\nexport function adapt(): string {\n  return api.name;\n}\n',
    } },

  // ---- negatives ----
  { id: 'RV-N01-relative-path-undeclared-external', kind: 'boundary', lane: 'report', expect: 'refuse', refuse: ['undeclared-external', 'lane-escape', 'unresolved'],
    why: 'report does not declare compiler-api; a relative node_modules path must not bypass the declared-external check (cf. N16)',
    files: help('import { name } from "../../../node_modules/compiler-api/index.js";\nexport const n = name;') },
  { id: 'RV-N02-relative-path-bypasses-exports', kind: 'boundary', lane: 'report', expect: 'refuse', refuse: ['unresolved', 'undeclared-external', 'lane-escape'],
    why: 'a relative path must not bypass package exports encapsulation (cf. N17)',
    files: help('import { hidden } from "../../../node_modules/dep/internal.mjs";\nexport const h = hidden;') },
  { id: 'RV-N03-pnpm-alias-shadows-local-name', kind: 'boundary', lane: 'report', expect: 'refuse', refuse: ['local-name-shadow'],
    why: 'npm: alias materializes a registry package under a local workspace name (cf. N15 in npm layout)',
    files: {
      'node_modules/@opensip/typescript-provider': { symlink: '../.pnpm/evil@0.1.0/node_modules/evil' },
      'node_modules/.pnpm/evil@0.1.0/node_modules/evil/package.json': json({ name: 'evil', version: '0.1.0', main: 'index.js', types: 'index.d.ts' }),
      'node_modules/.pnpm/evil@0.1.0/node_modules/evil/index.js': 'exports.x = 1;\n',
      'node_modules/.pnpm/evil@0.1.0/node_modules/evil/index.d.ts': 'export declare const x: number;\n',
      'apps/report/package.json': reportDeps({ '@opensip/typescript-provider': 'npm:evil@0.1.0' }),
      ...help('import { x } from "@opensip/typescript-provider";\nexport const shadow = x;'),
    } },
  { id: 'RV-N04-pnpm-store-shadows-local-name', kind: 'boundary', lane: 'report', expect: 'refuse', refuse: ['local-name-shadow'],
    why: 'control for N03: same shadow without an alias, in a pnpm store',
    files: {
      'node_modules/@opensip/typescript-provider': { symlink: '../.pnpm/@opensip+typescript-provider@0.1.0/node_modules/@opensip/typescript-provider' },
      'node_modules/.pnpm/@opensip+typescript-provider@0.1.0/node_modules/@opensip/typescript-provider/package.json': json({ name: '@opensip/typescript-provider', version: '0.1.0', main: 'index.js', types: 'index.d.ts' }),
      'node_modules/.pnpm/@opensip+typescript-provider@0.1.0/node_modules/@opensip/typescript-provider/index.js': 'exports.x = 1;\n',
      'node_modules/.pnpm/@opensip+typescript-provider@0.1.0/node_modules/@opensip/typescript-provider/index.d.ts': 'export declare const x: number;\n',
      'apps/report/package.json': reportDeps({ '@opensip/typescript-provider': '0.1.0' }),
      ...help('import { x } from "@opensip/typescript-provider";\nexport const shadow = x;'),
    } },
  { id: 'RV-N05-node-module-sync-missing', kind: 'node', lane: 'contracts', expect: 'refuse', refuse: ['unresolved'],
    why: 'Node 24 selects module-sync for require; its target is missing',
    files: {
      'node_modules/sync/package.json': pkg('sync', { exports: { '.': { 'module-sync': './missing.mjs', default: './index.js' } } }),
      'node_modules/sync/index.js': 'exports.name = "cjs";\n',
      'tools/contracts/package.json': contractsDeps({ sync: '1.0.0' }),
      'tools/contracts/generate.cjs': GENERATE('sync'),
    },
    oracle: [{ from: 'tools/contracts/generate.cjs', request: 'sync', mode: 'require' }] },
  { id: 'RV-N06-esm-extensionless-relative', kind: 'node', lane: 'report', expect: 'refuse', refuse: ['unresolved'],
    why: 'Node ESM does not probe extensions; the node build script reaches dep/import.mjs',
    files: { 'node_modules/dep/import.mjs': 'export { parseMode } from "./helper";\n', 'node_modules/dep/helper.mjs': 'export const parseMode = "import";\n' },
    oracle: [{ from: 'apps/report/build.mjs', request: 'dep', mode: 'import' }] },
  { id: 'RV-N07-cjs-require-mjs-extensionless', kind: 'node', lane: 'contracts', expect: 'refuse', refuse: ['unresolved'],
    why: 'CommonJS require probes .js/.json/.node only, not .mjs',
    files: { 'node_modules/compiler-api/index.js': 'const impl = require("./impl");\nexports.name = impl.name;\n', 'node_modules/compiler-api/impl.mjs': 'export const name = "impl";\n' },
    oracle: [{ from: 'tools/contracts/generate.cjs', request: 'compiler-api', mode: 'require' }] },
  { id: 'RV-N08-cjs-require-ts-extensionless', kind: 'node', lane: 'contracts', expect: 'refuse', refuse: ['unresolved'],
    why: 'CommonJS require does not probe .ts in node_modules',
    files: { 'node_modules/compiler-api/index.js': 'const impl = require("./impl");\nexports.name = impl.name;\n', 'node_modules/compiler-api/impl.ts': 'export const name: string = "impl";\n' },
    oracle: [{ from: 'tools/contracts/generate.cjs', request: 'compiler-api', mode: 'require' }] },
  { id: 'RV-N09-esm-directory-import', kind: 'node', lane: 'report', expect: 'refuse', refuse: ['unresolved'],
    why: 'Node ESM refuses directory imports',
    files: { 'node_modules/dep/import.mjs': 'export { parseMode } from "./lib";\n', 'node_modules/dep/lib/index.mjs': 'export const parseMode = "import";\n' },
    oracle: [{ from: 'apps/report/build.mjs', request: 'dep', mode: 'import' }] },
  { id: 'RV-N10-elided-static-plus-dynamic-browser', kind: 'boundary', lane: 'report', expect: 'refuse', refuse: ['browser-node'],
    why: 'a type-used static import is elided but import() of the same Node-only package remains in the browser runtime closure',
    files: { ...NODE_ONLY, 'apps/report/package.json': reportDeps({ 'node-only': '1.0.0' }),
      ...help('import { Reader } from "node-only";\nexport type R = Reader;\nexport const load = () => import("node-only");') } },
  { id: 'RV-N11-worker-url-cross-lane', kind: 'boundary', lane: 'report', expect: 'refuse', refuse: ['lane-escape', 'unsupported-loader', 'undeclared-local'],
    why: 'new URL(literal, import.meta.url) worker/asset entry is followed by common bundlers; bundler unselected',
    files: help('export const worker = () => new Worker(new URL("../../../providers/typescript/src/index.js", import.meta.url), { type: "module" });') },
  { id: 'RV-N12-accepted-record-covers-other-request-kind', kind: 'boundary', lane: 'provider', expect: 'refuse', refuse: ['unresolved'],
    why: 'record meant for a try/catch require probe also silences an unguarded import() of the same specifier',
    files: { 'node_modules/compiler-api/index.js': 'try { require("optional-peer"); } catch {}\nexports.name = "compiler-api";\nexports.load = () => import("optional-peer");\n' },
    lanes: l => { l.lanes.provider.acceptedUnresolved = [{ from: 'node_modules/compiler-api/index.js', module: 'optional-peer', reason: 'optional require probe in try/catch' }]; } },
  { id: 'RV-N13-external-realpath-into-own-lane', kind: 'boundary', lane: 'report', expect: 'refuse', refuse: ['undeclared-local', 'reentry', 'lane-escape'],
    why: 'materialized dependency symlink realizes to undeclared files inside the lane package',
    files: { 'node_modules/dep': { symlink: '../apps/report/vendor/dep' },
      ...Object.fromEntries(Object.entries(depFiles()).map(([n, v]) => ['apps/report/vendor/dep/' + n, v])) } },
  { id: 'RV-N14-type-only-workspace-name-cross', kind: 'boundary', lane: 'report', expect: 'refuse', refuse: ['lane-escape', 'undeclared-external', 'local-name-shadow', 'undeclared-local'],
    why: 'type-only import of the provider package by workspace name (type-only cannot hide cross-lane ownership)',
    files: help('import type { main } from "@opensip/typescript-provider";\nexport type M = typeof main;') },
  { id: 'RV-N15-unresolved-require-resolve', kind: 'boundary', lane: 'provider', expect: 'refuse', refuse: ['unresolved'],
    why: 'unresolved exotic require keeps its kind and is refused',
    files: { 'providers/typescript/scripts/bundle.cjs': 'const path = require("node:path");\nconst dep = require("dep");\nmodule.exports = path.join("out", dep.parseMode, require.resolve("missing-tool"));\n' } },
  { id: 'RV-N16-cts-import-equals-plus-dynamic-import-missing', kind: 'boundary', lane: 'provider', expect: 'refuse', refuse: ['unresolved'],
    why: 'import = require (cjs) and import() of one package; import branch missing',
    files: { ...compilerApi({ import: './missing.mjs', require: './index.js' }),
      'providers/typescript/src/compiler-adapter.cts': 'import api = require("compiler-api");\nexport const later = () => import("compiler-api");\nexport function adapt(): string {\n  return api.name;\n}\n' } },
  { id: 'RV-N17-esm-external-imports-require-only', kind: 'node', lane: 'provider', expect: 'refuse', refuse: ['unresolved'],
    why: 'transitive ESM import of a require-only exports map',
    files: { 'node_modules/dep/import.mjs': 'import "cjs-only";\nexport const parseMode = "import";\n',
      'node_modules/cjs-only/package.json': pkg('cjs-only', { exports: { '.': { require: './index.cjs' } } }), 'node_modules/cjs-only/index.cjs': 'exports.x = 1;\n' },
    oracle: [{ from: 'node_modules/dep/import.mjs', request: 'cjs-only', mode: 'import' }] },
  { id: 'RV-N18-cjs-external-requires-import-only', kind: 'node', lane: 'contracts', expect: 'refuse', refuse: ['unresolved'],
    why: 'transitive CJS require of an import-only exports map',
    files: { 'node_modules/compiler-api/index.js': 'require("esm-only");\nexports.name = "compiler-api";\n',
      'node_modules/esm-only/package.json': pkg('esm-only', { exports: { '.': { import: './index.mjs' } } }), 'node_modules/esm-only/index.mjs': 'export const x = 1;\n' },
    oracle: [{ from: 'tools/contracts/generate.cjs', request: 'compiler-api', mode: 'require' }] },
  { id: 'RV-N19-ts-esnext-emit-in-commonjs-scope', kind: 'node', lane: 'contracts', expect: 'refuse', refuse: ['unresolved', 'unsupported-module-format'],
    why: 'module ESNext emits ESM syntax into a commonjs-scope .js; Node detection loads it as ESM (import condition)',
    files: {
      ...compilerApi({ import: './missing.mjs', require: './index.js' }),
      'tools/contracts/tsconfig.json': json({ compilerOptions: { target: 'ES2022', module: 'ESNext', moduleResolution: 'Bundler', types: [], allowJs: true, checkJs: false, noEmit: true }, include: ['*.cjs', '*.ts'] }),
      'tools/contracts/gen.ts': 'import { name } from "compiler-api";\nexport const n = name;\n',
    },
    lanes: l => { const c = l.lanes.contracts; c.inputs.push('tools/contracts/gen.ts'); c.inputs.sort(); c.runtimeGroups[0].files.push('tools/contracts/gen.ts'); },
    oracle: [{ from: 'tools/contracts/gen.ts', emit: { module: ts.ModuleKind.ESNext, target: ts.ScriptTarget.ES2022 } }] },
  // ---- second set: written after reviewer mutant batch A, to distinguish surviving mutants ----
  { id: 'RV-P08-type-only-import-runtime-unresolvable', kind: 'boundary', lane: 'report', expect: 'accept',
    why: 'import type from a package whose declarations are not runtime-resolvable (types in a subdirectory, no main/index)',
    files: {
      'node_modules/typesdir/package.json': pkg('typesdir', { types: 'types/index.d.ts' }),
      'node_modules/typesdir/types/index.d.ts': 'export interface Shape { id: string }\n',
      'apps/report/package.json': reportDeps({ typesdir: '1.0.0' }),
      ...help('import type { Shape } from "typesdir";\nexport type S = Shape;'),
    } },
  { id: 'RV-P09-untyped-js-esm-detection-import-condition', kind: 'node', lane: 'report', expect: 'accept',
    why: 'Node detects ESM syntax in an untyped .js and uses the import condition for its static import',
    files: {
      'node_modules/esmjs/package.json': pkg('esmjs', { main: 'index.js' }),
      'node_modules/esmjs/index.js': 'import { name } from "cond";\nexport const v = name;\n',
      'node_modules/cond/package.json': pkg('cond', { exports: { '.': { import: './ok.mjs', require: './missing.cjs' } } }),
      'node_modules/cond/ok.mjs': 'export const name = "ok";\n',
      'apps/report/package.json': reportDeps({ esmjs: '1.0.0' }),
      'apps/report/build.mjs': 'import { existsSync } from "node:fs";\nimport { parseMode } from "dep";\nimport { v } from "esmjs";\nexport const ready = existsSync("dist") ? parseMode + v : "";\n',
    },
    oracle: [{ from: 'apps/report/build.mjs', request: 'esmjs', mode: 'import' }] },
  { id: 'RV-P10-browser-declaration-in-commonjs-scope-uses-import', kind: 'boundary', lane: 'report', expect: 'accept',
    why: 'bundler policy (TS moduleResolution Bundler) uses import conditions for declarations in commonjs-scope packages',
    files: {
      'node_modules/cjsdts/package.json': pkg('cjsdts', { main: 'index.js', types: 'index.d.ts' }),
      'node_modules/cjsdts/index.js': 'exports.z = 1;\n',
      'node_modules/cjsdts/index.d.ts': 'export * from "cond2";\n',
      'node_modules/cond2/package.json': pkg('cond2', { exports: { '.': { import: { types: './ok.d.mts', default: './ok.mjs' }, require: { types: './missing.d.cts', default: './missing.cjs' } } } }),
      'node_modules/cond2/ok.d.mts': 'export interface Z { z: number }\n',
      'node_modules/cond2/ok.mjs': 'export const z = 1;\n',
      'apps/report/package.json': reportDeps({ cjsdts: '1.0.0' }),
      ...help('import type { Z } from "cjsdts";\nexport type ZZ = Z;'),
    } },
  { id: 'RV-N20-accepted-record-does-not-cover-other-external', kind: 'boundary', lane: 'provider', expect: 'refuse', refuse: ['unresolved'],
    why: 'a record for compiler-api must not silence the same unresolved module requested by another external',
    files: { 'node_modules/compiler-api/index.js': 'try { require("optional-peer"); } catch {}\nexports.name = "compiler-api";\n',
      'node_modules/dep/import.mjs': 'import "optional-peer";\nexport const parseMode = "import";\n' },
    lanes: l => { l.lanes.provider.acceptedUnresolved = [{ from: 'node_modules/compiler-api/index.js', module: 'optional-peer', reason: 'optional require probe in try/catch' }]; } },
  { id: 'RV-N21-accepted-record-cannot-silence-browser-node', kind: 'boundary', lane: 'report', expect: 'refuse', refuse: ['browser-node', 'lane-record-invalid'],
    why: 'an acceptedUnresolved record naming a core module must not silence a browser-node refusal',
    files: { 'node_modules/dep/browser.mjs': 'import {readFileSync} from "node:fs"; export const parseMode=typeof readFileSync;\n' },
    lanes: l => { l.lanes.report.acceptedUnresolved = [{ from: 'node_modules/dep/browser.mjs', module: 'fs', reason: 'not an unresolved request' }]; } },
  { id: 'RV-N22-external-imports-shadowing-copy', kind: 'boundary', lane: 'report', expect: 'refuse', refuse: ['local-name-shadow'],
    why: 'an external (not own source) resolves a materialized copy under a local package name',
    files: {
      'node_modules/@opensip/typescript-provider': null,
      'node_modules/@opensip/typescript-provider/package.json': json({ name: '@opensip/typescript-provider', version: '0.1.0', main: 'index.js', module: 'index.js' }),
      'node_modules/@opensip/typescript-provider/index.js': 'export const x = 1;\n',
      'node_modules/dep/browser.mjs': 'import { x } from "@opensip/typescript-provider";\nexport const parseMode = String(x);\n',
    } },
  { id: 'RV-N23-provider-runtime-imports-devdependency', kind: 'boundary', lane: 'provider', expect: 'refuse', refuse: ['undeclared-external'],
    why: 'sealed provider runtime closure: a devDependency reached at runtime (policy question; advisory)',
    files: {
      'providers/typescript/package.json': manifest('providers/typescript/package.json', m => { m.devDependencies['dev-only'] = '1.0.0'; }),
      'node_modules/dev-only/package.json': pkg('dev-only', { main: 'index.js' }),
      'node_modules/dev-only/index.js': 'exports.devValue = 1;\n',
      'providers/typescript/src/session.ts': 'import type { Frame } from "#generated/protocol.js";\nimport { devValue } from "dev-only";\nexport function createSession(_read: unknown, frame: Frame): string {\n  return frame.kind + String(devValue);\n}\n',
    } },
  { id: 'RV-T01-lane-record-declares-browser-src-as-node', kind: 'trust', lane: 'report', expect: 'accept',
    why: 'lane records are trusted: declaring browser sources as a node group disables browser-node checks',
    files: help('import { existsSync } from "node:fs";\nexport const e = existsSync;'),
    lanes: l => { const r = l.lanes.report; r.browserRoots = []; r.runtimeGroups[0].platform = 'node'; r.runtimeGroups[0].conditions = ['node']; } },
];

function nodeOracle(root, o) {
  const from = path.join(root, o.from);
  if (o.emit) {
    const emitted = from.replace(/\.ts$/, '.oracle-emit.js');
    fs.writeFileSync(emitted, ts.transpileModule(fs.readFileSync(from, 'utf8'), { compilerOptions: o.emit }).outputText);
    const r = spawnSync(process.execPath, ['--no-warnings', emitted], { encoding: 'utf8', env, cwd: path.dirname(emitted) });
    const code = (r.stderr.match(/code: '([A-Z_]+)'/) ?? r.stderr.match(/(ERR_[A-Z_]+)/))?.[1];
    return { ...o, emittedFile: path.relative(root, emitted), status: r.status, error: r.status === 0 ? undefined : code ?? r.stderr.split('\n').find(Boolean) };
  }
  const requireScript = `const { createRequire } = require('node:module'); const r = createRequire(process.argv[1]); const out = {};
try { out.resolved = r.resolve(process.argv[2]); } catch (e) { out.resolveError = e.code || e.message; }
if (out.resolved) { try { r(process.argv[2]); out.loaded = true; } catch (e) { out.loadError = e.code || String(e.message).slice(0, 200); } }
console.log(JSON.stringify(out));`;
  const importScript = `import { pathToFileURL, fileURLToPath } from 'node:url'; import fs from 'node:fs'; const out = {};
try { const u = import.meta.resolve(process.argv[2], pathToFileURL(process.argv[1]).href); out.resolved = u.startsWith('file:') ? fileURLToPath(u) : u;
  if (u.startsWith('file:') && !(fs.existsSync(out.resolved) && fs.statSync(out.resolved).isFile())) out.resolveError = 'ERR_MODULE_NOT_FOUND (target is not a file)';
} catch (e) { out.resolveError = e.code || e.message; }
if (out.resolved && !out.resolveError) { try { await import(pathToFileURL(out.resolved).href); out.loaded = true; } catch (e) { out.loadError = e.code || String(e.message).slice(0, 200); } }
console.log(JSON.stringify(out));`;
  const flags = o.mode === 'require' ? ['--no-deprecation', '-e', requireScript] : ['--experimental-import-meta-resolve', '--no-warnings', '--input-type=module', '-e', importScript];
  const r = spawnSync(process.execPath, [...flags, from, o.request], { encoding: 'utf8', env, cwd: path.dirname(from) });
  let res;
  try { res = JSON.parse(r.stdout); } catch { res = { harnessError: r.stderr.slice(0, 300) }; }
  if (res.resolved && !res.resolved.startsWith('node:')) res.resolved = path.relative(root, res.resolved);
  return { ...o, ...res, error: res.resolveError ?? res.loadError ?? res.harnessError };
}

function runChecker(root, lanesFile, lane, { cwd, rootArg } = {}) {
  const c = spawnSync(process.execPath, [checker, '--root', rootArg ?? root, '--lanes', lanesFile, '--lane', lane], { encoding: 'utf8', env, cwd: cwd ?? path.dirname(root) });
  let report;
  try { report = JSON.parse(c.stdout); } catch { report = null; }
  return { status: c.status, stderr: c.stderr.slice(0, 600), stdout: c.stdout, report };
}

// ---- third set: the author's declared fail-closed refusals and lane validation, which no
// author test isolates (their removal survived the author suite in reviewer mutants) ----
const reportTsconfig = edit => manifest('apps/report/tsconfig.json', edit);
probes.push(
  { id: 'RV-F01-amd-request-in-declared-input', kind: 'boundary', lane: 'provider', expect: 'refuse', refuse: ['unsupported-module-format'],
    why: 'declared fail-closed: AMD requests are not selected',
    files: { 'providers/typescript/scripts/bundle.cjs': 'define(["dep"], function (dep) {\n  return dep.parseMode;\n});\n' } },
  { id: 'RV-F02-invalid-package-json-scope', kind: 'node', lane: 'contracts', expect: 'refuse', refuse: ['unsupported-module-format', 'unresolved'],
    why: 'declared fail-closed: nearest package.json of a reached external is invalid JSON',
    files: {
      'node_modules/scoped/package.json': pkg('scoped', { main: 'lib/index.js' }),
      'node_modules/scoped/lib/package.json': '{ "type": \n',
      'node_modules/scoped/lib/index.js': 'const b = require("./b.js");\nexports.name = b;\n',
      'node_modules/scoped/lib/b.js': 'module.exports = "b";\n',
      'tools/contracts/package.json': contractsDeps({ scoped: '1.0.0' }),
      'tools/contracts/generate.cjs': GENERATE('scoped'),
    },
    oracle: [{ from: 'tools/contracts/generate.cjs', request: 'scoped', mode: 'require' }] },
  { id: 'RV-F03-external-cts-static-plus-dynamic', kind: 'boundary', lane: 'provider', expect: 'refuse', refuse: ['unsupported-mixed-mode'],
    why: 'declared fail-closed mixed-mode check claimed for reached externals too',
    files: {
      'node_modules/tsdep/package.json': pkg('tsdep', { exports: { '.': { require: './index.cts' } } }),
      'node_modules/tsdep/index.cts': 'import { name } from "compiler-api";\nexport const later = () => import("compiler-api");\nexport const n = name;\n',
      'providers/typescript/package.json': manifest('providers/typescript/package.json', m => { m.dependencies.tsdep = '1.0.0'; }),
      'providers/typescript/scripts/bundle.cjs': 'const path = require("node:path");\nconst dep = require("dep");\nconst ts = require("tsdep");\nmodule.exports = path.join("out", dep.parseMode, String(ts.n));\n',
    } },
  { id: 'RV-F04-own-lane-symlink-input', kind: 'boundary', lane: 'report', expect: 'refuse', refuse: ['symlink'],
    why: 'declared input is a symlink to a file in the same lane (no cross-lane escape to mask it)',
    files: { 'apps/report/src/help-view.ts': { symlink: '../lib/help-real.ts' }, 'apps/report/lib/help-real.ts': 'export function help(): string {\n  return "help";\n}\n' } },
  { id: 'RV-F05-tsconfig-project-references', kind: 'boundary', lane: 'report', expect: 'refuse', refuse: ['config-invalid', 'config-owner'],
    why: 'declared: project references are not selected',
    files: { 'apps/report/tsconfig.json': reportTsconfig(m => { m.references = [{ path: '../../tools/contracts' }]; }) } },
  { id: 'RV-F06-tsconfig-compiler-plugins', kind: 'boundary', lane: 'report', expect: 'refuse', refuse: ['config-invalid'],
    why: 'declared: compiler plugins are not selected',
    files: { 'apps/report/tsconfig.json': reportTsconfig(m => { m.compilerOptions.plugins = [{ name: 'some-plugin' }]; }) } },
  { id: 'RV-F07-tsconfig-typeRoots', kind: 'boundary', lane: 'report', expect: 'refuse', refuse: ['ambient-types'],
    why: 'declared: typeRoots is not selected',
    files: { 'apps/report/tsconfig.json': reportTsconfig(m => { m.compilerOptions.typeRoots = ['./types']; }) } },
  { id: 'RV-F08-ambient-types-undeclared', kind: 'boundary', lane: 'report', expect: 'refuse', refuse: ['ambient-types'],
    why: 'explicit ambient type package not declared by the lane manifest',
    files: { 'node_modules/@types/ambient-x/package.json': pkg('@types/ambient-x', { types: 'index.d.ts' }), 'node_modules/@types/ambient-x/index.d.ts': 'declare const ambientX: number;\n',
      'apps/report/tsconfig.json': reportTsconfig(m => { m.compilerOptions.types = ['ambient-x']; }) } },
  { id: 'RV-F09-lane-platform-inconsistent', kind: 'boundary', lane: 'report', expect: 'exit2',
    why: 'lane record: node build script declared as a browser group must be a LaneError (exit 2)',
    lanes: l => { l.lanes.report.runtimeGroups[1].platform = 'browser'; l.lanes.report.runtimeGroups[1].conditions = ['browser']; } },
  { id: 'RV-P11-typed-untyped-js-esm-detection', kind: 'node', lane: 'report', expect: 'accept',
    why: 'as RV-P09 but the package ships declarations, so only runtime ESM detection decides the condition',
    files: {
      'node_modules/esmjs/package.json': pkg('esmjs', { main: 'index.js', types: 'index.d.ts' }),
      'node_modules/esmjs/index.d.ts': 'export declare const v: string;\n',
      'node_modules/esmjs/index.js': 'import { name } from "cond";\nexport const v = name;\n',
      'node_modules/cond/package.json': pkg('cond', { exports: { '.': { import: './ok.mjs', require: './missing.cjs' } } }),
      'node_modules/cond/ok.mjs': 'export const name = "ok";\n',
      'apps/report/package.json': reportDeps({ esmjs: '1.0.0' }),
      'apps/report/build.mjs': 'import { existsSync } from "node:fs";\nimport { parseMode } from "dep";\nimport { v } from "esmjs";\nexport const ready = existsSync("dist") ? parseMode + v : "";\n',
    },
    oracle: [{ from: 'apps/report/build.mjs', request: 'esmjs', mode: 'import' }] },
);

function grade(p, report, status) {
  if (p.expect === 'exit2') return status === 2 ? 'correct' : 'missed';
  if (!report || status === 3) return 'tool-error';
  const cats = report.refusals.map(r => r.category);
  if (cats.includes('tool-error')) return 'tool-error';
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
  writeTree(root, p.files ?? {});
  const lanes = baseLanes();
  p.lanes?.(lanes);
  const lanesFile = path.join(dir, 'lanes.json');
  fs.writeFileSync(lanesFile, json(lanes));
  const run = runChecker(root, lanesFile, p.lane);
  const row = { id: p.id, kind: p.kind, lane: p.lane, why: p.why, expected: p.expect === 'accept' ? 'accept' : { refuse: p.refuse },
    status: run.status, passed: run.report?.passed ?? null, categories: [...new Set((run.report?.refusals ?? []).map(r => r.category))],
    refusals: run.report?.refusals ?? [], accepted: run.report?.accepted ?? [], stderr: run.stderr, grade: grade(p, run.report, run.status) };
  if (p.kind === 'trust') row.grade = run.report?.passed ? 'trusted-input-accepted' : 'refused';
  if (p.variants) {
    row.variants = {};
    const link = path.join(dir, 'root-link');
    fs.rmSync(link, { force: true });
    fs.symlinkSync('root', link);
    const v = {
      'cwd-root': runChecker(root, lanesFile, p.lane, { cwd: '/' }),
      'relative-root': runChecker(root, lanesFile, p.lane, { cwd: path.dirname(dir), rootArg: path.join(path.basename(dir), 'root') }),
      'symlinked-root': runChecker(root, lanesFile, p.lane, { rootArg: link }),
    };
    for (const [name, r] of Object.entries(v)) row.variants[name] = { status: r.status, identicalReport: r.stdout === run.stdout, stderr: r.stderr };
  }
  if (withOracle && p.oracle) {
    row.oracle = p.oracle.map(o => nodeOracle(root, o));
    row.oracleVerdict = row.oracle.some(o => o.error) ? 'node-fails' : 'node-loads';
    row.oracleAgreesWithCandidate = (row.oracleVerdict === 'node-loads') === (run.report?.passed === true);
  }
  row.edges = (run.report?.graphs ?? []).map(g => ({ group: g.name, rounds: g.rounds, edges: g.edges.map(e => `${e.from} -${e.mode}-> ${e.module} => ${e.resolved}`) }));
  rows.push(row);
  process.stdout.write(`${row.id.padEnd(56)} ${row.grade.padEnd(24)} ${row.categories.join(',')}${row.oracle ? '  oracle:' + row.oracleVerdict + (row.oracleAgreesWithCandidate ? '' : ' DISAGREES') : ''}${row.variants ? '  variants:' + JSON.stringify(Object.fromEntries(Object.entries(row.variants).map(([k, x]) => [k, x.identicalReport]))) : ''}\n`);
}
const summary = {};
for (const r of rows) summary[r.grade] = (summary[r.grade] ?? 0) + 1;
fs.mkdirSync(path.dirname(out), { recursive: true });
fs.writeFileSync(out, json({ schemaVersion: 1, standing: 'independent reviewer probes; not qualification', checker: path.relative(review, checker), node: process.version, summary, rows }));
process.stdout.write(JSON.stringify(summary) + '\n');
