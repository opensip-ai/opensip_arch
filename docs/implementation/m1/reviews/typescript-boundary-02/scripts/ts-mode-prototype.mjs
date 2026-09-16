// Substantiation probe for the "simpler established alternative" question: does
// TypeScript 6.0.3 (already in the closure) give a per-usage-location resolution
// mode without depcruise's request dedup? Resolution-mode selection only; this is
// not a checker and makes no runtime-resolution claim for JS externals.
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const review = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const trial = path.join(review, 'work/copy/trial');
const ts = createRequire(path.join(trial, 'package.json'))('typescript');
const { baseFiles, writeTree } = await import(path.join(trial, 'harness/fixture.mjs'));
const root = path.join(review, 'work/ts-mode-prototype/root');
fs.rmSync(root, { recursive: true, force: true });
writeTree(root, baseFiles());
const api = { 'node_modules/compiler-api/package.json': JSON.stringify({ name: 'compiler-api', version: '1.0.0', main: 'index.js', types: 'index.d.ts', exports: { '.': { types: './index.d.ts', import: './esm.mjs', require: './index.js' } } }),
  'node_modules/compiler-api/esm.mjs': 'export const name = "esm";\n', 'node_modules/compiler-api/index.d.ts': 'export declare const name: string;\nexport interface Named { id: string }\n' };
writeTree(root, {
  ...api,
  'providers/typescript/src/n62.cts': 'import { name } from "compiler-api";\nexport const later = () => import("compiler-api");\nexport const n = name;\n',
  'providers/typescript/src/p07.cts': 'import { Named } from "compiler-api";\nexport type N = Named;\nexport const later = () => import("compiler-api");\n',
  'tools/contracts/p08.cjs': 'const api = require("compiler-api");\nmodule.exports = { name: api.name, later: () => import("compiler-api") };\n',
});
const cases = [
  ['providers/typescript/src/n62.cts', 'providers/typescript/tsconfig.json'],
  ['providers/typescript/src/p07.cts', 'providers/typescript/tsconfig.json'],
  ['tools/contracts/p08.cjs', 'tools/contracts/tsconfig.json'],
];
const rows = [];
for (const [file, config] of cases) {
  const parsed = ts.getParsedCommandLineOfConfigFile(path.join(root, config), {}, { ...ts.sys, onUnRecoverableConfigFileDiagnostic: () => {} });
  const options = { ...parsed.options, noEmit: true, allowJs: true };
  const program = ts.createProgram([path.join(root, file)], options, ts.createCompilerHost(options, true));
  const source = program.getSourceFile(path.join(root, file));
  const usages = [];
  const visit = node => {
    let spec;
    if (ts.isImportDeclaration(node)) spec = node.moduleSpecifier;
    else if (ts.isCallExpression(node) && (node.expression.kind === ts.SyntaxKind.ImportKeyword || (ts.isIdentifier(node.expression) && node.expression.text === 'require')) && node.arguments[0] && ts.isStringLiteralLike(node.arguments[0])) spec = node.arguments[0];
    if (spec) {
      const mode = ts.getModeForUsageLocation(source, spec, options);
      const resolved = ts.resolveModuleName(spec.text, source.fileName, options, ts.sys, undefined, undefined, mode).resolvedModule?.resolvedFileName;
      usages.push({ line: source.getLineAndCharacterOfPosition(spec.getStart()).line + 1, request: spec.text, mode: mode === ts.ModuleKind.ESNext ? 'import' : mode === ts.ModuleKind.CommonJS ? 'require' : String(mode), resolvedDeclaration: resolved && path.relative(root, resolved) });
    }
    ts.forEachChild(node, visit);
  };
  visit(source);
  const emitted = ts.transpileModule(fs.readFileSync(path.join(root, file), 'utf8'), { compilerOptions: { module: options.module, target: options.target }, fileName: file }).outputText;
  rows.push({ file, impliedFormat: source.impliedNodeFormat === ts.ModuleKind.ESNext ? 'esm' : 'commonjs', usages, emittedRequests: [...emitted.matchAll(/(require|import)\(\s*["']([^"']+)["']\s*\)/g)].map(m => `${m[1]}(${m[2]})`) });
}
const out = { typescript: ts.version, standing: 'reviewer substantiation of per-usage mode API; not a checker', rows };
fs.writeFileSync(path.join(review, 'evidence/ts-mode-prototype.json'), JSON.stringify(out, null, 2) + '\n');
console.log(JSON.stringify(out, null, 2));
