// Shared complete positive payload for both tools. Every case starts from these
// exact bytes (verified by tree digest) before its edge mutation is applied.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const json = value => JSON.stringify(value, null, 2) + '\n';

export function baseFiles() {
  return {
    'package.json': json({ name: 'opensip-fixture-root', private: true, workspaces: ['apps/report', 'providers/typescript'] }),

    // Browser report lane: DOM compiler settings, browser runtime conditions,
    // one Node build script that is an explicit lane input.
    'apps/report/package.json': json({ name: '@opensip/report', version: '0.0.0', private: true, type: 'module', dependencies: { dep: '1.0.0' } }),
    'apps/report/tsconfig.json': json({
      compilerOptions: {
        target: 'ES2022', module: 'ESNext', moduleResolution: 'Bundler', customConditions: ['browser'],
        lib: ['ES2022', 'DOM'], types: [], strict: true, noEmit: true, allowJs: true,
        paths: { '@report/*': ['./src/*'] },
      },
      include: ['src/**/*.ts', 'build.mjs'],
    }),
    'apps/report/build.mjs': 'import { existsSync } from "node:fs";\nimport { parseMode } from "dep";\nexport const ready = existsSync("dist") ? parseMode : "";\n',
    'apps/report/src/index.ts': [
      'import { renderReport } from "./report-view.js";',
      'import type { ReportProjection } from "./generated/report.js";',
      'import { parseMode } from "dep";',
      'export async function start(projection: ReportProjection): Promise<string> {',
      '  const helpView = await import("./help-view.js");',
      '  return renderReport(projection) + helpView.help() + parseMode;',
      '}',
      '',
    ].join('\n'),
    'apps/report/src/report-view.ts': [
      'import type { ReportProjection } from "@report/generated/report.js";',
      'export * from "./view-state.js";',
      'export function renderReport(projection: ReportProjection): string {',
      '  return String(projection.version);',
      '}',
      '',
    ].join('\n'),
    'apps/report/src/view-state.ts': 'export type ViewState = { selected?: string };\nexport const initial: ViewState = {};\n',
    'apps/report/src/help-view.ts': 'export function help(): string {\n  return "help";\n}\n',
    'apps/report/src/generated/report.ts': '// Generated fixture binding; owner: schemas/registry.json (fixture only).\nexport interface ReportProjection { version: number }\n',

    // Node provider lane: NodeNext, package subpath imports, CJS adapter and script.
    'providers/typescript/package.json': json({
      name: '@opensip/typescript-provider', version: '0.0.0', private: true, type: 'module',
      exports: './src/index.ts', imports: { '#generated/*': './src/generated/*' },
      dependencies: { dep: '1.0.0', 'compiler-api': '1.0.0' }, devDependencies: { '@types/node': '24.0.0' },
    }),
    'providers/typescript/tsconfig.json': json({
      compilerOptions: {
        target: 'ES2022', module: 'NodeNext', moduleResolution: 'NodeNext', lib: ['ES2022'],
        types: ['node'], strict: true, noEmit: true, allowJs: true,
      },
      include: ['src/**/*.ts', 'src/**/*.cts', 'scripts/**/*.cjs'],
    }),
    'providers/typescript/src/index.ts': [
      'import { readFileSync } from "node:fs";',
      'import { createSession } from "./session.js";',
      'import type { Frame } from "./generated/protocol.js";',
      'import { parseMode } from "dep";',
      'import { adapt } from "./compiler-adapter.cjs";',
      'export function main(frame: Frame): string {',
      '  return createSession(readFileSync, frame) + parseMode + adapt();',
      '}',
      '',
    ].join('\n'),
    'providers/typescript/src/session.ts': 'import type { Frame } from "#generated/protocol.js";\nexport function createSession(_read: unknown, frame: Frame): string {\n  return frame.kind;\n}\n',
    'providers/typescript/src/generated/protocol.ts': '// Generated fixture binding; owner: schemas/registry.json (fixture only).\nexport interface Frame { kind: string }\n',
    'providers/typescript/src/compiler-adapter.cts': 'import api = require("compiler-api");\nexport function adapt(): string {\n  return api.name;\n}\n',
    'providers/typescript/scripts/bundle.cjs': 'const path = require("node:path");\nconst dep = require("dep");\nmodule.exports = path.join("out", dep.parseMode);\n',

    // Contract tooling lane at its current real location (tools/contracts).
    'tools/contracts/package.json': json({ name: 'opensip-contract-tools', version: '0.0.0', private: true, dependencies: { 'compiler-api': '1.0.0' } }),
    'tools/contracts/tsconfig.json': json({ compilerOptions: { target: 'ES2022', module: 'NodeNext', moduleResolution: 'NodeNext', types: [], allowJs: true, checkJs: false, noEmit: true }, include: ['*.cjs'] }),
    'tools/contracts/generate.cjs': 'const api = require("compiler-api");\nconst { join } = require("node:path");\nmodule.exports = function outputPath() {\n  return join("generated", api.name);\n};\n',

    // Materialized dependency tree (fixture-only stand-ins, no install scripts).
    'node_modules/@opensip/report': { symlink: '../../apps/report' },
    'node_modules/@opensip/typescript-provider': { symlink: '../../providers/typescript' },
    'node_modules/dep/package.json': json({
      name: 'dep', version: '1.0.0',
      exports: { '.': {
        types: { import: './types/import.d.mts', require: './types/require.d.cts' },
        browser: './browser.mjs', import: './import.mjs', require: './require.cjs', default: './import.mjs',
      } },
    }),
    'node_modules/dep/import.mjs': 'export const parseMode = "import";\n',
    'node_modules/dep/browser.mjs': 'export const parseMode = "browser";\n',
    'node_modules/dep/require.cjs': 'exports.parseMode = "require";\n',
    'node_modules/dep/internal.mjs': 'export const hidden = true;\n',
    'node_modules/dep/types/import.d.mts': 'export declare const parseMode: "import";\n',
    'node_modules/dep/types/require.d.cts': 'export declare const parseMode: "require";\n',
    'node_modules/compiler-api/package.json': json({ name: 'compiler-api', version: '1.0.0', main: 'index.js', types: 'index.d.ts' }),
    'node_modules/compiler-api/index.js': 'exports.name = "compiler-api";\n',
    'node_modules/compiler-api/index.d.ts': 'export declare const name: string;\n',
    'node_modules/@types/node/package.json': json({ name: '@types/node', version: '24.0.0', types: 'index.d.ts' }),
    'node_modules/@types/node/index.d.ts': 'declare module "node:fs" {\n  export function readFileSync(p: unknown): string;\n  export function existsSync(p: string): boolean;\n}\ndeclare module "node:path" {\n  export function join(...p: string[]): string;\n}\ndeclare var require: any;\ndeclare var module: any;\n',
  };
}

// Trial-owned lane declaration. It is not the product inventory and is not promoted.
export function baseLanes() {
  const reportInputs = ['apps/report/build.mjs', 'apps/report/src/generated/report.ts', 'apps/report/src/help-view.ts',
    'apps/report/src/index.ts', 'apps/report/src/report-view.ts', 'apps/report/src/view-state.ts'];
  const providerInputs = ['providers/typescript/scripts/bundle.cjs', 'providers/typescript/src/compiler-adapter.cts',
    'providers/typescript/src/generated/protocol.ts', 'providers/typescript/src/index.ts', 'providers/typescript/src/session.ts'];
  return {
    schemaVersion: 1,
    standing: 'trial fixture lane declaration; not the product inventory',
    localPackageNames: ['@opensip/report', '@opensip/typescript-provider', 'opensip-contract-tools'],
    lanes: {
      report: {
        referenceInventoryId: 'report', packageRoot: 'apps/report', manifest: 'apps/report/package.json', tsconfig: 'apps/report/tsconfig.json',
        inputs: reportInputs, browserRoots: ['apps/report/src/'],
        runtimeGroups: [
          { name: 'browser-esm', conditions: ['browser', 'import', 'default'], files: reportInputs.filter(f => f.startsWith('apps/report/src/')) },
          { name: 'node-esm-script', conditions: ['node', 'import', 'default'], files: ['apps/report/build.mjs'] },
        ],
        typeConditions: ['types', 'browser', 'import', 'default'],
      },
      provider: {
        referenceInventoryId: 'typescript-provider', packageRoot: 'providers/typescript', manifest: 'providers/typescript/package.json', tsconfig: 'providers/typescript/tsconfig.json',
        inputs: providerInputs, browserRoots: [],
        runtimeGroups: [
          { name: 'node-esm', conditions: ['node', 'import', 'default'], files: ['providers/typescript/src/generated/protocol.ts', 'providers/typescript/src/index.ts', 'providers/typescript/src/session.ts'] },
          { name: 'node-cjs', conditions: ['node', 'require', 'default'], files: ['providers/typescript/scripts/bundle.cjs', 'providers/typescript/src/compiler-adapter.cts'] },
        ],
        typeConditions: ['types', 'node', 'import', 'default'],
      },
      contracts: {
        referenceInventoryId: 'tooling', packageRoot: 'tools/contracts', manifest: 'tools/contracts/package.json', tsconfig: 'tools/contracts/tsconfig.json',
        inputs: ['tools/contracts/generate.cjs'], browserRoots: [],
        runtimeGroups: [{ name: 'node-cjs', conditions: ['node', 'require', 'default'], files: ['tools/contracts/generate.cjs'] }],
        typeConditions: ['types', 'node', 'require', 'default'],
      },
    },
  };
}

export function writeTree(root, files) {
  for (const [name, value] of Object.entries(files)) {
    const file = path.join(root, name);
    if (value === null) { fs.rmSync(file, { recursive: true, force: true }); continue; }
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.rmSync(file, { recursive: true, force: true });
    if (typeof value === 'object') fs.symlinkSync(value.symlink, file);
    else fs.writeFileSync(file, value);
  }
}

export function treeDigest(root) {
  const hash = crypto.createHash('sha256');
  const walk = relative => {
    const entries = fs.readdirSync(path.join(root, relative), { withFileTypes: true }).map(e => e.name).sort();
    for (const name of entries) {
      const rel = relative ? relative + '/' + name : name;
      const stat = fs.lstatSync(path.join(root, rel));
      if (stat.isSymbolicLink()) hash.update('L\0' + rel + '\0' + fs.readlinkSync(path.join(root, rel)) + '\0');
      else if (stat.isDirectory()) walk(rel);
      else hash.update('F\0' + rel + '\0').update(fs.readFileSync(path.join(root, rel))).update('\0');
    }
  };
  walk('');
  return hash.digest('hex');
}
