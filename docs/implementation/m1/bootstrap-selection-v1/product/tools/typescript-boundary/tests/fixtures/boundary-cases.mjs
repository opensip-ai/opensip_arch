import { baseFiles } from './fixture.mjs';
// Case matrix. Expectations come from the build-plan boundary policy, not from
// either tool's behavior. `refuse` lists acceptable diagnostic categories; a
// refusal for any other category is graded wrong-reason.
const X = '../../../providers/typescript/src/index.js';            // from apps/report/src/*.ts
const XTYPE = '../../../providers/typescript/src/generated/protocol.js';
const XB = '../../providers/typescript/src/index.js';              // from apps/report/build.mjs
const CROSS = ['lane-escape', 'undeclared-local'];
const LOADER = ['unsupported-loader'];
const src = (body, name = 'apps/report/src/help-view.ts') => ({ [name]: body + '\nexport function help(): string {\n  return "help";\n}\n' });
// author02 fixture helpers.
const MIXED_CJS = 'const api = require("compiler-api");\nmodule.exports = { name: api.name, later: () => import("compiler-api") };\n';
const compilerApi = branches => ({
  'node_modules/compiler-api/package.json': JSON.stringify({ name: 'compiler-api', version: '1.0.0', main: 'index.js', types: 'index.d.ts', exports: { '.': { types: './index.d.ts', ...branches } } }) + '\n',
  'node_modules/compiler-api/esm.mjs': 'export const name = "compiler-api-esm";\n',
});
const providerManifest = extra => JSON.stringify({
  name: '@opensip/typescript-provider', version: '0.0.0', private: true, type: 'module',
  exports: './src/index.ts', imports: { '#generated/*': './src/generated/*' },
  dependencies: { dep: '1.0.0', 'compiler-api': '1.0.0', ...extra }, devDependencies: { '@types/node': '24.0.0' },
}, null, 2) + '\n';
const BUNDLE_REQUIRING = name => `const path = require("node:path");\nconst dep = require("dep");\nconst extra = require("${name}");\nmodule.exports = path.join("out", dep.parseMode, String(extra));\n`;
const LOADER_PACKAGE = {
  'node_modules/loader/package.json': '{"name":"loader","version":"1.0.0","main":"index.cjs"}\n',
  'node_modules/loader/index.cjs': 'module.exports = () => import("compiler-api");\n',
  'providers/typescript/package.json': providerManifest({ loader: '1.0.0' }),
  'providers/typescript/scripts/bundle.cjs': BUNDLE_REQUIRING('loader'),
};
const OPTIONAL_PEER = { 'node_modules/compiler-api/index.js': 'try { require("optional-peer"); } catch {}\nexports.name = "compiler-api";\n' };
const legacy = fields => ({
  'node_modules/legacy/package.json': JSON.stringify({ name: 'legacy', version: '1.0.0', ...fields }) + '\n',
  'node_modules/legacy/index.js': 'exports.x = 1;\n', 'node_modules/legacy/esm.mjs': 'export const x = 1;\n',
});
const depFiles = () => Object.fromEntries(Object.entries(baseFiles()).filter(([n]) => n.startsWith('node_modules/dep/')).map(([n, v]) => [n.slice('node_modules/dep/'.length), v]));
const pnpm = (overrides = {}) => {
  const store = 'node_modules/.pnpm/dep@1.0.0/node_modules/dep/';
  return {
    'node_modules/dep': { symlink: '.pnpm/dep@1.0.0/node_modules/dep' },
    ...Object.fromEntries(Object.entries({ ...depFiles(), ...overrides }).map(([n, v]) => [store + n, v])),
    'apps/report/node_modules/dep': { symlink: '../../../node_modules/.pnpm/dep@1.0.0/node_modules/dep' },
    'providers/typescript/node_modules/dep': { symlink: '../../../node_modules/.pnpm/dep@1.0.0/node_modules/dep' },
  };
};
const nested = () => ({ 'node_modules/dep': null, ...Object.fromEntries(Object.entries(depFiles()).map(([n, v]) => ['apps/report/node_modules/dep/' + n, v])) });
const outsideStore = () => ({
  'node_modules/dep': { symlink: '../../outside-store/dep' },
  ...Object.fromEntries(Object.entries(depFiles()).map(([n, v]) => ['../outside-store/dep/' + n, v])),
});
const addInput = (lane, file, group) => lanes => {
  const l = lanes.lanes[lane];
  l.inputs.push(file); l.inputs.sort();
  l.runtimeGroups.find(g => g.name === group).files.push(file);
};

export const cases = [
  // Complete positive payload controls.
  { id: 'P00-report', requirement: 'positive control', lane: 'report', expect: 'accept' },
  { id: 'P00-provider', requirement: 'positive control', lane: 'provider', expect: 'accept' },
  { id: 'P00-contracts', requirement: 'positive control; tools/contracts lane', lane: 'contracts', expect: 'accept' },
  { id: 'P01-provider-only', requirement: 'independent lane: report/tooling sources absent', lane: 'provider', expect: 'accept', files: { 'apps': null, 'tools': null } },
  { id: 'P02-report-only', requirement: 'independent lane: provider/tooling sources absent', lane: 'report', expect: 'accept', files: { 'providers': null, 'tools': null } },
  { id: 'P03-jsdoc-own', requirement: 'JSDoc type import of own generated binding in script', lane: 'report', expect: 'accept',
    files: { 'apps/report/build.mjs': '/** @import { ReportProjection } from "./src/generated/report.js" */\nimport { existsSync } from "node:fs";\n/** @type {ReportProjection | undefined} */\nexport const sample = existsSync("dist") ? { version: 1 } : undefined;\n' } },
  { id: 'P04-self-reference', requirement: 'package self-reference through own exports', lane: 'provider', expect: 'accept',
    files: { 'providers/typescript/scripts/bundle.cjs': 'const path = require("node:path");\nconst dep = require("dep");\nmodule.exports = path.join("out", dep.parseMode);\nmodule.exports.self = () => import("@opensip/typescript-provider");\n' } },
  { id: 'P05-literal-template-import', requirement: 'no-substitution template literal is a literal edge', lane: 'report', expect: 'accept',
    files: src('export const later = () => import(`./view-state.js`);') },
  { id: 'P06-loader-named-members', requirement: 'members named require/eval are not loaders', lane: 'report', expect: 'accept',
    files: src('export class Store {\n  require(key: string): string { return key; }\n  eval(): number { return 1; }\n}\nexport const value = new Store().require("x");') },

  // Runtime/type-only/dynamic/export edge spellings across lanes.
  { id: 'N01-runtime-import', requirement: 'runtime import', lane: 'report', refuse: CROSS, files: src(`import { main } from "${X}";\nexport const m = main;`) },
  { id: 'N02-type-only-import', requirement: 'type-only import (duplicate schema owner)', lane: 'report', refuse: CROSS, files: src(`import type { Frame } from "${XTYPE}";\nexport type F = Frame;`) },
  { id: 'N03-export-star', requirement: 'export * from', lane: 'report', refuse: CROSS, files: src(`export * from "${X}";`) },
  { id: 'N04-export-type', requirement: 'export type from', lane: 'report', refuse: CROSS, files: src(`export type { Frame } from "${XTYPE}";`) },
  { id: 'N05-import-type-node', requirement: 'typeof import() type', lane: 'report', refuse: CROSS, files: src(`export type M = typeof import("${X}");`) },
  { id: 'N06-dynamic-import', requirement: 'literal dynamic import', lane: 'report', refuse: CROSS, files: src(`export const load = () => import("${X}");`) },
  { id: 'N07-import-equals', requirement: 'import = require', lane: 'provider', refuse: CROSS,
    files: { 'providers/typescript/src/compiler-adapter.cts': 'import api = require("compiler-api");\nimport view = require("../../../apps/report/src/view-state.js");\nexport function adapt(): string {\n  return api.name + String(view);\n}\n' } },
  { id: 'N08-require', requirement: 'literal require', lane: 'provider', refuse: CROSS,
    files: { 'providers/typescript/scripts/bundle.cjs': 'const path = require("node:path");\nconst dep = require("dep");\nconst view = require("../../../apps/report/src/view-state.ts");\nmodule.exports = path.join("out", dep.parseMode, String(view));\n' } },
  { id: 'N09-require-resolve', requirement: 'require.resolve', lane: 'provider', refuse: CROSS,
    files: { 'providers/typescript/scripts/bundle.cjs': 'const path = require("node:path");\nconst dep = require("dep");\nmodule.exports = path.join(require.resolve("../../../apps/report/src/view-state.ts"), dep.parseMode);\n' } },
  { id: 'N10-module-require', requirement: 'module.require', lane: 'provider', refuse: CROSS,
    files: { 'providers/typescript/scripts/bundle.cjs': 'const path = require("node:path");\nconst dep = require("dep");\nmodule.exports = path.join("out", dep.parseMode, String(module.require("../../../apps/report/src/view-state.ts")));\n' } },
  { id: 'N11-reverse-direction', requirement: 'provider imports report source', lane: 'provider', refuse: CROSS,
    files: { 'providers/typescript/src/session.ts': 'import type { Frame } from "#generated/protocol.js";\nimport { initial } from "../../../apps/report/src/view-state.js";\nexport function createSession(_read: unknown, frame: Frame): string {\n  return frame.kind + String(initial);\n}\n' } },
  { id: 'N12-contracts-cross', requirement: 'tooling script requires provider source', lane: 'contracts', refuse: CROSS,
    files: { 'tools/contracts/generate.cjs': 'const api = require("compiler-api");\nconst { join } = require("node:path");\nconst bundle = require("../../providers/typescript/scripts/bundle.cjs");\nmodule.exports = function outputPath() {\n  return join("generated", api.name, bundle);\n};\n' } },

  // Aliases, package exports and names.
  { id: 'N13-paths-alias', requirement: 'tsconfig paths alias crossing', lane: 'report', refuse: CROSS,
    files: {
      'apps/report/tsconfig.json': JSON.stringify({ compilerOptions: { target: 'ES2022', module: 'ESNext', moduleResolution: 'Bundler', customConditions: ['browser'], lib: ['ES2022', 'DOM'], types: [], strict: true, noEmit: true, allowJs: true, paths: { '@report/*': ['./src/*'], '@worker/*': ['../../providers/typescript/src/*'] } }, include: ['src/**/*.ts', 'build.mjs'] }, null, 2) + '\n',
      ...src('import { main } from "@worker/index.js";\nexport const m = main;'),
    } },
  { id: 'N14-workspace-name', requirement: 'workspace package name resolves to other lane', lane: 'report', refuse: [...CROSS, 'undeclared-external', 'local-name-shadow'],
    files: src('import { main } from "@opensip/typescript-provider";\nexport const m = main;') },
  { id: 'N15-materialized-shadow', requirement: 'materialized dependency shadows local package name', lane: 'report', refuse: ['local-name-shadow'],
    files: {
      'node_modules/@opensip/typescript-provider': null,
      'node_modules/@opensip/typescript-provider/package.json': '{"name":"@opensip/typescript-provider","version":"0.1.0","types":"index.d.ts","main":"index.js"}\n',
      'node_modules/@opensip/typescript-provider/index.d.ts': 'export declare const x: number;\n',
      'node_modules/@opensip/typescript-provider/index.js': 'exports.x = 1;\n',
      'apps/report/package.json': '{"name":"@opensip/report","version":"0.0.0","private":true,"type":"module","dependencies":{"dep":"1.0.0","@opensip/typescript-provider":"0.1.0"}}\n',
      ...src('import { x } from "@opensip/typescript-provider";\nexport const shadow = x;'),
    } },
  { id: 'N16-undeclared-external', requirement: 'external package not declared by lane manifest', lane: 'report', refuse: ['undeclared-external'],
    files: src('import { name } from "compiler-api";\nexport const n = name;') },
  { id: 'N17-unexported-subpath', requirement: 'package exports encapsulation', lane: 'report', refuse: ['unresolved'],
    files: src('import { hidden } from "dep/internal.mjs";\nexport const h = hidden;') },
  { id: 'N18-imports-outside-package', requirement: 'package.json imports target outside package', lane: 'report', refuse: [...CROSS, 'unresolved'],
    files: {
      'apps/report/package.json': '{"name":"@opensip/report","version":"0.0.0","private":true,"type":"module","imports":{"#provider/*":"../../providers/typescript/src/*"},"dependencies":{"dep":"1.0.0"}}\n',
      ...src('import { main } from "#provider/index.js";\nexport const m = main;'),
    } },

  // Unknown resolution and generated/declared inputs.
  { id: 'N19-missing-module', requirement: 'unresolvable relative request', lane: 'report', refuse: ['unresolved'], files: src('import "./missing.js";') },
  { id: 'N20-missing-generated', requirement: 'generated binding absent', lane: 'report', refuse: ['unresolved'], files: { 'apps/report/src/generated/report.ts': null },
    lanes: lanes => { const l = lanes.lanes.report; l.inputs = l.inputs.filter(f => !f.includes('generated')); l.runtimeGroups[0].files = l.runtimeGroups[0].files.filter(f => !f.includes('generated')); } },
  { id: 'N21-undeclared-local-import', requirement: 'imported own file not declared', lane: 'report', refuse: ['undeclared-local', 'config-include'],
    files: { 'apps/report/src/extra.ts': 'export const extra = 1;\n', ...src('import { extra } from "./extra.js";\nexport const e = extra;') } },
  { id: 'N22-undeclared-generated-type', requirement: 'type-only import of undeclared generated file', lane: 'report', refuse: ['undeclared-local', 'config-include'],
    files: { 'apps/report/src/generated/extra.ts': 'export interface Extra { a: 1 }\n', ...src('import type { Extra } from "./generated/extra.js";\nexport type E = Extra;') } },
  { id: 'N47-undeclared-local-outside-include', requirement: 'imported own file outside tsconfig include and declared inputs', lane: 'report', refuse: ['undeclared-local'],
    files: { 'apps/report/lib/extra.ts': 'export const extra = 1;\n', ...src('import { extra } from "../lib/extra.js";\nexport const e = extra;') } },
  { id: 'N23-config-include-stray', requirement: 'tsconfig include selects undeclared file', lane: 'report', refuse: ['config-include'], files: { 'apps/report/src/stray.ts': 'export const stray = 1;\n' } },

  // Node/browser environment.
  { id: 'N24-browser-node-builtin', requirement: 'browser source imports Node builtin', lane: 'report', refuse: ['browser-node'], files: src('import { existsSync } from "node:fs";\nexport const e = existsSync;') },
  { id: 'N25-browser-node-types-directive', requirement: 'browser source requests Node ambient types', lane: 'report', refuse: ['browser-node', 'undeclared-external'],
    files: { 'apps/report/src/help-view.ts': '/// <reference types="node" />\nexport function help(): string {\n  return "help";\n}\n' } },
  { id: 'N26-browser-getbuiltin-literal', requirement: 'browser process.getBuiltinModule literal', lane: 'report', refuse: ['browser-node', 'unsupported-loader'],
    files: src('declare const process: { getBuiltinModule(id: string): unknown };\nexport const fsModule = process.getBuiltinModule("node:fs");') },
  { id: 'N27-ambient-auto-types', requirement: 'automatic @types inclusion is an unrecorded ambient input', lane: 'report', refuse: ['ambient-types', 'browser-node'],
    files: { 'apps/report/tsconfig.json': JSON.stringify({ compilerOptions: { target: 'ES2022', module: 'ESNext', moduleResolution: 'Bundler', customConditions: ['browser'], lib: ['ES2022', 'DOM'], strict: true, noEmit: true, allowJs: true, paths: { '@report/*': ['./src/*'] } }, include: ['src/**/*.ts', 'build.mjs'] }, null, 2) + '\n' } },
  { id: 'N28-triple-slash-path', requirement: 'triple-slash path reference crossing', lane: 'report', refuse: CROSS,
    files: { 'apps/report/src/help-view.ts': '/// <reference path="../../../providers/typescript/src/generated/protocol.ts" />\nexport function help(): string {\n  return "help";\n}\n' } },
  { id: 'N29-jsdoc-import-tag-cross', requirement: 'JSDoc @import crossing in script', lane: 'report', refuse: CROSS,
    files: { 'apps/report/build.mjs': '/** @import { Frame } from "../../providers/typescript/src/generated/protocol.js" */\nimport { existsSync } from "node:fs";\n/** @type {Frame | undefined} */\nexport const frame = existsSync("dist") ? { kind: "x" } : undefined;\n' } },
  { id: 'N30-jsdoc-bracket-cross', requirement: 'JSDoc bracket import crossing in script', lane: 'report', refuse: CROSS,
    files: { 'apps/report/build.mjs': 'import { existsSync } from "node:fs";\n/** @type {import("../../providers/typescript/src/generated/protocol.js").Frame | undefined} */\nexport const frame = existsSync("dist") ? { kind: "x" } : undefined;\n' } },

  // Unsupported computed modules must refuse rather than mean "no edge".
  { id: 'N31-computed-import', requirement: 'computed dynamic import', lane: 'report', refuse: LOADER, files: src(`const target = "${X}";\nexport const load = () => import(target);`) },
  { id: 'N32-computed-require', requirement: 'computed require', lane: 'provider', refuse: LOADER,
    files: { 'providers/typescript/scripts/bundle.cjs': 'const path = require("node:path");\nconst dep = require("dep");\nconst target = "../../../apps/report/src/view-state.ts";\nmodule.exports = path.join("out", dep.parseMode, String(require(target)));\n' } },
  { id: 'N33-template-substitution', requirement: 'template literal with substitution', lane: 'report', refuse: LOADER, files: src('const lane = "typescript";\nexport const load = () => import(`../../../providers/${lane}/src/index.js`);') },
  { id: 'N34-require-alias', requirement: 'require alias', lane: 'provider', refuse: LOADER,
    files: { 'providers/typescript/scripts/bundle.cjs': 'const path = require("node:path");\nconst dep = require("dep");\nconst load = require;\nmodule.exports = path.join("out", dep.parseMode, String(load("../../../apps/report/src/view-state.ts")));\n' } },
  { id: 'N35-create-require', requirement: 'createRequire loader', lane: 'report', refuse: LOADER,
    files: { 'apps/report/build.mjs': `import { createRequire } from "node:module";\nimport { parseMode } from "dep";\nconst load = createRequire(import.meta.url);\nexport const ready = String(load("${XB}")) + parseMode;\n` } },
  { id: 'N36-eval', requirement: 'eval code loader', lane: 'report', refuse: LOADER, files: src(`export const load = () => eval("import('${X}')");`) },
  { id: 'N37-new-function', requirement: 'Function constructor loader', lane: 'report', refuse: LOADER, files: src(`export const load = new Function("return import('${X}')");`) },
  { id: 'N38-computed-member-loader', requirement: 'computed member loader access', lane: 'provider', refuse: LOADER,
    files: { 'providers/typescript/scripts/bundle.cjs': 'const path = require("node:path");\nconst dep = require("dep");\nconst key = "require";\nmodule.exports = path.join("out", dep.parseMode, String(module[key]("../../../apps/report/src/view-state.ts")));\n' } },
  { id: 'N39-computed-getbuiltin', requirement: 'computed process.getBuiltinModule', lane: 'provider', refuse: LOADER,
    files: { 'providers/typescript/scripts/bundle.cjs': 'const path = require("node:path");\nconst dep = require("dep");\nconst id = "node:" + "child_process";\nmodule.exports = path.join("out", dep.parseMode, String(process.getBuiltinModule(id)));\n' } },

  // Source/config integrity.
  { id: 'N40-parse-failure', requirement: 'syntax error must refuse, not partially extract', lane: 'report', refuse: ['parse-failure'], expectSyntaxError: true,
    files: src('export const broken = ;') },
  { id: 'N41-source-symlink', requirement: 'declared input is a symlink to another lane', lane: 'report', refuse: ['symlink', 'lane-escape'],
    files: { 'apps/report/src/help-view.ts': { symlink: '../../../providers/typescript/src/session.ts' } } },
  { id: 'N42-config-extends-other-lane', requirement: 'tsconfig extends another lane config', lane: 'report', refuse: ['config-owner'],
    files: { 'apps/report/tsconfig.json': JSON.stringify({ extends: '../../providers/typescript/tsconfig.json', compilerOptions: { moduleResolution: 'Bundler', module: 'ESNext', customConditions: ['browser'], types: [], lib: ['ES2022', 'DOM'], paths: { '@report/*': ['./src/*'] } }, include: ['src/**/*.ts', 'build.mjs'] }, null, 2) + '\n' } },

  // Declarations versus runtime conditional exports; external re-entry.
  { id: 'N43-runtime-browser-target-missing', requirement: 'type graph resolves but browser runtime target is absent', lane: 'report', refuse: ['unresolved'],
    files: { 'node_modules/dep/browser.mjs': null } },
  { id: 'N44-runtime-require-target-missing', requirement: 'CJS require condition target absent while require types exist', lane: 'provider', refuse: ['unresolved'],
    files: { 'node_modules/dep/require.cjs': null }, nodeOracle: [{ from: 'providers/typescript/scripts/bundle.cjs', request: 'dep' }] },
  { id: 'N45-runtime-reenters-other-lane', requirement: 'external runtime file imports another lane', lane: 'report', refuse: ['reentry', ...CROSS],
    files: { 'node_modules/dep/browser.mjs': 'export { main } from "../../providers/typescript/src/index.ts";\nexport const parseMode = "browser";\n' } },
  { id: 'N46-types-reenter-declared-local', requirement: 'external declarations import an already declared lane input', lane: 'report', refuse: ['reentry'],
    files: { 'node_modules/dep/types/import.d.mts': 'export type { ViewState } from "../../../apps/report/src/view-state.js";\nexport declare const parseMode: "import";\n' } },

  // ---- author02 additions (after root probes found three misses in the 56-case matrix) ----
  // Root probe bytes, reproduced exactly.
  { id: 'R01-root-external-browser-node', requirement: 'root probe: external runtime file in browser closure imports node:fs', lane: 'report', refuse: ['browser-node'],
    files: { 'node_modules/dep/browser.mjs': 'import {readFileSync} from "node:fs"; export const parseMode=typeof readFileSync;\n' } },
  { id: 'R02-root-external-unresolved', requirement: 'root probe: external runtime file has an unresolvable request', lane: 'report', refuse: ['unresolved'],
    files: { 'node_modules/dep/browser.mjs': 'import "./missing.mjs"; export const parseMode="browser";\n' } },
  { id: 'R03-root-cjs-dynamic-import-condition', requirement: 'root probe: import() in CJS uses the import condition (branch missing)', lane: 'contracts', refuse: ['unresolved'],
    files: {
      'tools/contracts/generate.cjs': 'module.exports = async () => import("compiler-api");\n',
      'node_modules/compiler-api/package.json': '{"name":"compiler-api","version":"1.0.0","main":"index.js","types":"index.d.ts","exports":{".":{"types":"./index.d.ts","import":"./missing.mjs","require":"./index.js"}}}',
    },
    nodeOracle: [{ from: 'tools/contracts/generate.cjs', request: 'compiler-api', mode: 'import' }] },

  // Per-edge conditions: own CJS file, mixed same-file requests, own .cts static imports, external CJS.
  { id: 'P07-cjs-dynamic-import-valid', requirement: 'import() in CJS with a valid import branch', lane: 'contracts', expect: 'accept',
    files: { 'tools/contracts/generate.cjs': 'module.exports = async () => import("compiler-api");\n', ...compilerApi({ import: './esm.mjs', require: './index.js' }) },
    nodeOracle: [{ from: 'tools/contracts/generate.cjs', request: 'compiler-api', mode: 'import' }] },
  { id: 'P08-cjs-mixed-same-file-valid', requirement: 'require and import() of one package in one CJS file, both branches valid', lane: 'contracts', expect: 'accept',
    files: { 'tools/contracts/generate.cjs': MIXED_CJS, ...compilerApi({ import: './esm.mjs', require: './index.js' }) },
    nodeOracle: [{ from: 'tools/contracts/generate.cjs', request: 'compiler-api', mode: 'require' }, { from: 'tools/contracts/generate.cjs', request: 'compiler-api', mode: 'import' }] },
  { id: 'N48-cjs-mixed-require-branch-missing', requirement: 'mixed CJS file: require branch missing, import branch valid', lane: 'contracts', refuse: ['unresolved'],
    files: { 'tools/contracts/generate.cjs': MIXED_CJS, ...compilerApi({ import: './esm.mjs', require: './missing.cjs' }) },
    nodeOracle: [{ from: 'tools/contracts/generate.cjs', request: 'compiler-api', mode: 'require' }, { from: 'tools/contracts/generate.cjs', request: 'compiler-api', mode: 'import' }] },
  { id: 'N49-cjs-mixed-import-branch-missing', requirement: 'mixed CJS file: import branch missing, require branch valid', lane: 'contracts', refuse: ['unresolved'],
    files: { 'tools/contracts/generate.cjs': MIXED_CJS, ...compilerApi({ import: './missing.mjs', require: './index.js' }) },
    nodeOracle: [{ from: 'tools/contracts/generate.cjs', request: 'compiler-api', mode: 'require' }, { from: 'tools/contracts/generate.cjs', request: 'compiler-api', mode: 'import' }] },
  { id: 'P10-cts-static-import-uses-require', requirement: '.cts static import is emitted as require (import branch absent)', lane: 'provider', expect: 'accept',
    files: { 'providers/typescript/src/compiler-adapter.cts': 'import { name } from "compiler-api";\nexport function adapt(): string {\n  return name;\n}\n', ...compilerApi({ import: './missing.mjs', require: './index.js' }) },
    nodeOracle: [{ from: 'providers/typescript/src/compiler-adapter.cts', request: 'compiler-api', mode: 'require' }] },
  { id: 'N51-cts-static-import-require-branch-missing', requirement: '.cts static import with require branch missing', lane: 'provider', refuse: ['unresolved'],
    files: { 'providers/typescript/src/compiler-adapter.cts': 'import { name } from "compiler-api";\nexport function adapt(): string {\n  return name;\n}\n', ...compilerApi({ import: './esm.mjs', require: './missing.cjs' }) },
    nodeOracle: [{ from: 'providers/typescript/src/compiler-adapter.cts', request: 'compiler-api', mode: 'require' }] },
  { id: 'N62-cts-static-and-dynamic-same-specifier', requirement: 'depcruise dedups static+dynamic same specifier in CJS TS: fail closed', lane: 'provider', refuse: ['unsupported-mixed-mode'],
    files: { 'providers/typescript/src/compiler-adapter.cts': 'import { name } from "compiler-api";\nexport const later = () => import("compiler-api");\nexport function adapt(): string {\n  return name;\n}\n', ...compilerApi({ import: './esm.mjs', require: './index.js' }) } },
  { id: 'P09-external-cjs-dynamic-import-valid', requirement: 'external CJS file import() with a valid import branch', lane: 'provider', expect: 'accept',
    files: { ...LOADER_PACKAGE, ...compilerApi({ import: './esm.mjs', require: './index.js' }) },
    nodeOracle: [{ from: 'node_modules/loader/index.cjs', request: 'compiler-api', mode: 'import' }] },
  { id: 'N50-external-cjs-dynamic-import-branch-missing', requirement: 'external CJS file import() whose import branch is missing', lane: 'provider', refuse: ['unresolved'],
    files: { ...LOADER_PACKAGE, ...compilerApi({ import: './missing.mjs', require: './index.js' }) },
    nodeOracle: [{ from: 'node_modules/loader/index.cjs', request: 'compiler-api', mode: 'import' }] },

  // Transitive browser runtime closure versus Node scripts and declarations.
  { id: 'N52-browser-external-two-hops-node', requirement: 'Node builtin two hops inside the browser runtime closure', lane: 'report', refuse: ['browser-node'],
    files: { 'node_modules/dep/browser.mjs': 'export { parseMode } from "./helper.mjs";\n', 'node_modules/dep/helper.mjs': 'import { join } from "node:path";\nexport const parseMode = typeof join;\n' } },
  { id: 'P11-node-script-external-uses-node', requirement: 'Node build-script branch of a shared dependency may use Node builtins', lane: 'report', expect: 'accept',
    files: { 'node_modules/dep/import.mjs': 'import { existsSync } from "node:fs";\nexport const parseMode = typeof existsSync;\n' } },
  { id: 'P12-browser-external-type-only-node', requirement: 'type-only Node reference in external declarations is not runtime browser closure', lane: 'report', expect: 'accept',
    files: { 'node_modules/dep/types/import.d.mts': 'import type { Stats } from "node:fs";\nexport declare const parseMode: "import";\nexport type S = Stats;\n' } },
  { id: 'P18-browser-type-only-import-of-node-package', requirement: 'type-only import of a package whose runtime entry uses Node is erased from the browser runtime closure', lane: 'report', expect: 'accept',
    files: {
      'node_modules/node-only/package.json': '{"name":"node-only","version":"1.0.0","main":"index.js","types":"index.d.ts"}\n',
      'node_modules/node-only/index.js': 'const fs = require("node:fs");\nexports.read = fs.readFileSync;\n',
      'node_modules/node-only/index.d.ts': 'export declare type Reader = (path: string) => string;\n',
      'apps/report/package.json': '{"name":"@opensip/report","version":"0.0.0","private":true,"type":"module","dependencies":{"dep":"1.0.0","node-only":"1.0.0"}}\n',
      ...src('import type { Reader } from "node-only";\nexport type R = Reader;'),
    } },
  { id: 'P19-browser-type-only-import-of-types-only-package', requirement: 'type-only import of a declarations-only package needs no runtime target', lane: 'report', expect: 'accept',
    files: {
      'node_modules/types-only/package.json': '{"name":"types-only","version":"1.0.0","types":"index.d.ts"}\n',
      'node_modules/types-only/index.d.ts': 'export interface Shape { id: string }\n',
      'apps/report/package.json': '{"name":"@opensip/report","version":"0.0.0","private":true,"type":"module","dependencies":{"dep":"1.0.0","types-only":"1.0.0"}}\n',
      ...src('import type { Shape } from "types-only";\nexport type S = Shape;'),
    } },
  { id: 'N53-external-declaration-unresolved', requirement: 'external declaration request unresolvable in the type graph', lane: 'report', refuse: ['unresolved'],
    files: { 'node_modules/dep/types/import.d.mts': 'export type { Missing } from "./missing-types.js";\nexport declare const parseMode: "import";\n' } },

  // Explicitly accepted unresolved external requests.
  { id: 'P13-accepted-unresolved-external', requirement: 'recorded optional external request is accepted, not treated as no edge', lane: 'provider', expect: 'accept',
    files: OPTIONAL_PEER, lanes: lanes => { lanes.lanes.provider.acceptedUnresolved = [{ from: 'node_modules/compiler-api/index.js', module: 'optional-peer', reason: 'fixture optional peer probe in try/catch' }]; } },
  { id: 'N54-unaccepted-unresolved-external', requirement: 'same optional external request without a record', lane: 'provider', refuse: ['unresolved'], files: OPTIONAL_PEER },
  { id: 'N55-stale-accepted-unresolved', requirement: 'accepted record that matches nothing', lane: 'provider', refuse: ['lane-record-invalid'],
    lanes: lanes => { lanes.lanes.provider.acceptedUnresolved = [{ from: 'node_modules/compiler-api/index.js', module: 'optional-peer', reason: 'stale' }]; } },

  { id: 'N64-external-parse-failure', requirement: 'syntax error in a reached external must refuse, not partially extract', lane: 'report', refuse: ['external-parse-failure'], expectSyntaxError: true,
    files: { 'node_modules/dep/browser.mjs': 'export const parseMode = ;\nimport "../../providers/typescript/src/index.ts";\n' } },

  // Materialization topologies.
  { id: 'P14-pnpm-in-root-layout', requirement: 'in-root pnpm-style .pnpm store with per-package symlinks', lane: 'report', expect: 'accept', files: pnpm() },
  { id: 'N56-pnpm-external-browser-node', requirement: 'pnpm layout: browser runtime external imports node:fs', lane: 'report', refuse: ['browser-node'],
    files: pnpm({ 'browser.mjs': 'import { readFileSync } from "node:fs";\nexport const parseMode = typeof readFileSync;\n' }) },
  { id: 'N57-pnpm-external-reentry', requirement: 'pnpm layout: external re-enters another lane', lane: 'report', refuse: ['reentry'],
    files: pnpm({ 'browser.mjs': 'export { main } from "../../../../../providers/typescript/src/index.ts";\nexport const parseMode = "browser";\n' }) },
  { id: 'P15-nested-own-node_modules', requirement: 'dependency materialized under the lane package node_modules', lane: 'report', expect: 'accept', files: nested() },
  { id: 'N58-other-lane-nested-node_modules', requirement: 'import from another lane package node_modules', lane: 'report', refuse: ['lane-escape'],
    files: { 'providers/typescript/node_modules/leak/index.js': 'export const leak = 1;\n', ...src('import { leak } from "../../../providers/typescript/node_modules/leak/index.js";\nexport const l = leak;') } },
  { id: 'N59-store-outside-root', requirement: 'dependency symlinked to a store outside the materialized root', lane: 'report', refuse: ['outside-root', 'lane-escape'], files: outsideStore() },

  // Node module format and main fields.
  { id: 'N60-ambiguous-js-format', requirement: '.js without type mixing import and require: fail closed', lane: 'provider', refuse: ['unsupported-module-format'],
    files: {
      'node_modules/ambig/package.json': '{"name":"ambig","version":"1.0.0","main":"index.js"}\n',
      'node_modules/ambig/index.js': 'import { name } from "./a.js";\nconst b = require("./b.js");\nmodule.exports = name + b;\n',
      'node_modules/ambig/a.js': 'export const name = "a";\n', 'node_modules/ambig/b.js': 'module.exports = "b";\n',
      'providers/typescript/package.json': providerManifest({ ambig: '1.0.0' }), 'providers/typescript/scripts/bundle.cjs': BUNDLE_REQUIRING('ambig'),
    } },
  { id: 'P16-node-ignores-module-field', requirement: 'Node require uses main even when module points nowhere', lane: 'provider', expect: 'accept',
    files: { ...legacy({ main: './index.js', module: './missing-esm.mjs' }), 'providers/typescript/package.json': providerManifest({ legacy: '1.0.0' }), 'providers/typescript/scripts/bundle.cjs': BUNDLE_REQUIRING('legacy') },
    nodeOracle: [{ from: 'providers/typescript/scripts/bundle.cjs', request: 'legacy', mode: 'require' }] },
  // Authored as negative N61; the Node oracle showed Node's legacy main fallback to index.js (DEP0128), so it is a positive control.
  { id: 'P17-node-legacy-main-fallback', requirement: 'missing main falls back to index.js as in Node (module field ignored)', lane: 'provider', expect: 'accept',
    files: { ...legacy({ main: './missing.js', module: './esm.mjs' }), 'providers/typescript/package.json': providerManifest({ legacy: '1.0.0' }), 'providers/typescript/scripts/bundle.cjs': BUNDLE_REQUIRING('legacy') },
    nodeOracle: [{ from: 'providers/typescript/scripts/bundle.cjs', request: 'legacy', mode: 'require' }] },
  { id: 'N63-node-main-and-index-missing-module-present', requirement: 'Node require with missing main and index but present module field', lane: 'provider', refuse: ['unresolved'],
    files: { ...legacy({ main: './missing.js', module: './esm.mjs' }), 'node_modules/legacy/index.js': null, 'providers/typescript/package.json': providerManifest({ legacy: '1.0.0' }), 'providers/typescript/scripts/bundle.cjs': BUNDLE_REQUIRING('legacy') },
    nodeOracle: [{ from: 'providers/typescript/scripts/bundle.cjs', request: 'legacy', mode: 'require' }] },
];

export { addInput };
