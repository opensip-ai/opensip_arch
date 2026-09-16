'use strict';
const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { check } = require('./check-typescript-edges.cjs');
const compiler = process.env.OPENSIP_TEST_TYPESCRIPT;
assert(compiler, 'OPENSIP_TEST_TYPESCRIPT must name the pinned TypeScript 6.0.3 package');

function fixture(t) {
  const root = fs.realpathSync(fs.mkdtempSync(path.join(os.tmpdir(), 'opensip-ts-edges-')));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  const write = (name, value) => { const file = path.join(root, name); fs.mkdirSync(path.dirname(file), { recursive: true }); fs.writeFileSync(file, typeof value === 'string' ? value : JSON.stringify(value)); };
  const inventory = { packages: [
    { id: 'report', path: 'apps/report', kind: 'typescript-package', dependencies: [] },
    { id: 'typescript-provider', path: 'providers/typescript', kind: 'typescript-package', dependencies: [] },
    { id: 'tooling', path: 'tools', kind: 'tooling', dependencies: [] },
  ] };
  for (const pkg of inventory.packages) {
    write(pkg.path + '/package.json', { name: '@opensip/' + pkg.id, version: '0.1.0', type: 'module' });
    write(pkg.path + '/tsconfig.json', { compilerOptions: { target: 'ES2022', module: 'NodeNext', moduleResolution: 'NodeNext', strict: true }, include: ['src/**/*'] });
  }
  write('apps/report/src/main.ts', 'export const value = 1;');
  write('providers/typescript/src/main.ts', 'export const secret = 1;');
  const run = (files = ['apps/report/src/main.ts'], lane = 'report') => check({ root, inventory, lane,
    config: inventory.packages.find(p => p.id === lane).path + '/tsconfig.json', files, compiler });
  return { root, write, run, inventory };
}

test('own relative import, generated module and deterministic UTF8 input order', t => {
  const f = fixture(t);
  f.write('apps/report/src/main.ts', 'import type { Report } from "./generated/report.js"; export const n: Report = { value: 1n };');
  f.write('apps/report/src/generated/report.ts', 'export interface Report { value: bigint }');
  const files = ['apps/report/src/main.ts', 'apps/report/src/generated/report.ts'];
  const a = f.run(files), b = f.run([...files].reverse());
  assert.deepEqual(a, b);
  assert.equal(a.edges[0].kind, 'type-import');
  assert.equal(a.edges[0].owner, 'report');
  assert.equal(a.sourcePurityQualified, false);
});

test('runtime, type-only, export, import-type, dynamic and import-equals edges cannot cross owners', t => {
  const f = fixture(t);
  const spec = '../../../providers/typescript/src/main.js';
  for (const text of [
    `import { secret } from '${spec}';`, `import type { secret } from '${spec}';`,
    `export * from '${spec}';`, `export type { secret } from '${spec}';`,
    `type X = typeof import('${spec}');`, `const p = import('${spec}');`,
    `import worker = require('${spec}');`, `const w = require('${spec}');`,
    `const p = require.resolve('${spec}');`, `module.require('${spec}');`,
  ]) {
    f.write('apps/report/src/main.ts', text);
    assert.throws(() => f.run(), /forbidden internal TS edge|undeclared local input/, text);
  }
});

test('missing source and unresolvable imports never mean no edge', t => {
  const f = fixture(t);
  f.write('apps/report/src/main.ts', 'import "./missing.js";');
  assert.throws(() => f.run(), /unresolved module request/);
  f.write('apps/report/src/extra.ts', 'export const x = 1;');
  assert.throws(() => f.run(), /config source missing from declared inputs/);
});

test('computed imports and loaders refuse', t => {
  const f = fixture(t);
  for (const text of [
    'const name="a"; import(name);', 'const name="a"; require(name);',
    'const load=require; load("x");', 'const r=require.resolve; r("x");',
    'module["require"]("x");', 'eval("x");', 'new Function("x")();',
  ]) {
    f.write('apps/report/src/main.ts', text);
    assert.throws(() => f.run(), /nonliteral|alias|computed/, text);
  }
});

test('browser Node imports refuse while explicit report build script may use them', t => {
  const f = fixture(t);
  f.write('apps/report/src/main.ts', 'import fs from "node:fs";');
  assert.throws(() => f.run(), /browser source imports Node builtin/);
  f.write('apps/report/src/main.ts', 'export const x = 1;');
  f.write('apps/report/build.cjs', 'const fs = require("node:fs");');
  const result = f.run(['apps/report/src/main.ts', 'apps/report/build.cjs']);
  assert.equal(result.edges[0].destination, 'node-builtin');
});

test('provider build is independent of report files and permits Node', t => {
  const f = fixture(t);
  fs.rmSync(path.join(f.root, 'apps'), { recursive: true });
  f.write('providers/typescript/src/main.ts', 'import fs from "node:fs";');
  const result = f.run(['providers/typescript/src/main.ts'], 'typescript-provider');
  assert.equal(result.edges[0].destination, 'node-builtin');
});

test('path aliases resolve actual owners', t => {
  const f = fixture(t);
  f.write('apps/report/tsconfig.json', { compilerOptions: { target: 'ES2022', module: 'NodeNext', moduleResolution: 'NodeNext', paths: {
    '@self/*': ['./src/*'], '@worker/*': ['../../providers/typescript/src/*'],
  } }, include: ['src/**/*'] });
  f.write('apps/report/src/helper.ts', 'export const x=1;');
  f.write('apps/report/src/main.ts', 'import {x} from "@self/helper.js";');
  assert.equal(f.run(['apps/report/src/main.ts', 'apps/report/src/helper.ts']).edges[0].owner, 'report');
  f.write('apps/report/src/main.ts', 'import {secret} from "@worker/main.js";');
  assert.throws(() => f.run(['apps/report/src/main.ts', 'apps/report/src/helper.ts']), /forbidden internal TS edge|undeclared local input/);
});

test('source symlinks and cross-package TS config extends refuse', t => {
  const f = fixture(t);
  fs.unlinkSync(path.join(f.root, 'apps/report/src/main.ts'));
  fs.symlinkSync(path.join(f.root, 'providers/typescript/src/main.ts'), path.join(f.root, 'apps/report/src/main.ts'));
  assert.throws(() => f.run(), /symlink in local source/);
  fs.unlinkSync(path.join(f.root, 'apps/report/src/main.ts'));
  f.write('apps/report/src/main.ts', 'export {};');
  f.write('apps/report/tsconfig.json', { extends: '../../providers/typescript/tsconfig.json', include: ['src/**/*'] });
  assert.throws(() => f.run(), /configuration reads another package/);
});

test('triple slash path and type-reference directives are checked', t => {
  const f = fixture(t);
  f.write('apps/report/src/main.ts', '/// <reference path="../../../providers/typescript/src/main.ts"/>\nexport {};');
  assert.throws(() => f.run(), /triple-slash reference crosses/);
  f.write('apps/report/src/main.ts', '/// <reference types="node"/>\nexport {};');
  assert.throws(() => f.run(), /browser source requests Node ambient types/);
});

test('external dependency must be declared and resolved through package export mode', t => {
  const f = fixture(t);
  f.write('node_modules/dep/package.json', { name: 'dep', version: '1.0.0', exports: {
    import: { types: './import.d.mts' }, require: { types: './require.d.cts' },
  } });
  f.write('node_modules/dep/import.d.mts', 'export const mode: "import";');
  f.write('node_modules/dep/require.d.cts', 'export const mode: "require";');
  f.write('apps/report/src/main.ts', 'import {mode} from "dep";');
  assert.throws(() => f.run(), /external module is not declared/);
  f.write('apps/report/package.json', { name: '@opensip/report', version: '0.1.0', type: 'module', dependencies: { dep: '1.0.0' } });
  assert.match(f.run().edges[0].destination, /import\.d\.mts$/);
  f.write('apps/report/build.cjs', 'const d = require("dep");');
  const result = f.run(['apps/report/src/main.ts', 'apps/report/build.cjs']);
  assert(result.edges.some(e => /require\.d\.cts$/.test(e.destination)));
});

test('materialized dependency cannot shadow another local package name', t => {
  const f = fixture(t);
  f.write('node_modules/@opensip/typescript-provider/package.json', { name: '@opensip/typescript-provider', version: '0.1.0', types: 'index.d.ts' });
  f.write('node_modules/@opensip/typescript-provider/index.d.ts', 'export const x: number;');
  f.write('apps/report/package.json', { name: '@opensip/report', type: 'module', dependencies: { '@opensip/typescript-provider': '0.1.0' } });
  f.write('apps/report/src/main.ts', 'import {x} from "@opensip/typescript-provider";');
  assert.throws(() => f.run(), /shadows a local package/);
});
