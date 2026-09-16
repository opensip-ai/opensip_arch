/** Independent S1-guard challenges for checker10. */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import crypto from 'node:crypto';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {checkBoundary} from '../copy/tools/typescript-boundary/src/check.mjs';

const json = value => JSON.stringify(value, null, 2) + '\n';
const pkgRoot = fileURLToPath(new URL('../copy/tools/typescript-boundary/', import.meta.url));
const tsc = path.join(pkgRoot, 'node_modules/typescript/bin/tsc');
const rows = [];
const check = (name, passed, detail = '') => {
  rows.push({name, passed: Boolean(passed), detail: String(detail).slice(0, 900)});
  console.log(passed ? 'PASS' : 'FAIL', name, String(detail).slice(0, 240));
};

function fixture({browser = false, declaredJs = false, external = false, outDir = 'dist'} = {}) {
  const temp = fs.realpathSync(fs.mkdtempSync(path.join(os.tmpdir(), 'opensip-generated-challenge10-')));
  const root = path.join(temp, 'product');
  const architecture = path.join(temp, 'architecture');
  fs.mkdirSync(root);
  fs.mkdirSync(architecture);
  const own = browser ? 'apps/report' : 'providers/typescript';
  const id = browser ? 'report' : 'typescript-provider';
  const write = (base, name, value) => {
    const p = path.join(base, name);
    fs.mkdirSync(path.dirname(p), {recursive: true});
    fs.writeFileSync(p, typeof value === 'string' ? value : json(value));
  };
  const inputs = [own + '/src/helper.ts', own + '/src/index.ts'];
  if (declaredJs) inputs.push(own + '/src/leaf.js');
  const record = {
    schemaVersion: 2, package: id, packageRoot: own, manifest: own + '/package.json', tsconfig: own + '/tsconfig.json',
    inputs, packageManager: {kind: 'fixture-unlocked', lockfile: null}, trustedUsages: [],
  };
  const manifest = {name: browser ? '@fixture/report' : '@fixture/provider', private: true, type: 'module'};
  if (external) manifest.dependencies = {ext: '1.0.0'};
  write(root, record.manifest, manifest);
  const compilerOptions = {
    strict: true, noImplicitAny: false, allowJs: true, checkJs: false,
    target: 'ES2022', module: browser ? 'ESNext' : 'NodeNext',
    moduleResolution: browser ? 'Bundler' : 'NodeNext', types: [], lib: ['ES2022', 'DOM'],
    rootDir: 'src',
  };
  if (outDir) compilerOptions.outDir = outDir;
  write(root, record.tsconfig, {
    compilerOptions,
    include: declaredJs || external ? ['src/**/*.ts', 'src/**/*.js'] : ['src/**/*.ts'],
  });
  write(root, own + '/src/helper.ts', 'export const value:number = 42;\n');
  let index = 'import {value} from "./helper.js";\nexport const answer=value;\nexport const url=new URL("./helper.js",import.meta.url);\n';
  if (declaredJs) {
    write(root, own + '/src/leaf.js', 'export const leaf = 7;\nexport const marker = "declared-js";\n');
    index += 'import {leaf} from "./leaf.js";\nexport const used=leaf;\n';
  }
  if (external) {
    write(root, own + '/node_modules/ext/package.json', {name: 'ext', version: '1.0.0', type: 'module', exports: './index.js'});
    write(root, own + '/node_modules/ext/index.js', 'export const ext = "external-js";\n');
    index += 'import {ext} from "ext";\nexport const usedExt=ext;\n';
  }
  write(root, own + '/src/index.ts', index);
  const files = [...record.inputs, record.manifest, record.tsconfig];
  const inventory = {
    standing: 'synthetic mechanics only; no acceptance',
    packages: [{id, path: own, kind: 'typescript-package', dependencies: []}],
    files: files.map(p => ({path: p, package: id, role: p.endsWith('.ts') || p.endsWith('.js') ? 'model' : 'configuration'})),
  };
  write(architecture, 'parent.json', inventory);
  write(architecture, 'inventory.json', inventory);
  for (const name of ['record', 'review', 'assent']) write(architecture, name + '.json', {fixture: true});
  const pin = name => {
    const raw = fs.readFileSync(path.join(architecture, name));
    return {path: name, bytes: raw.length, sha256: crypto.createHash('sha256').update(raw).digest('hex')};
  };
  const binding = Object.fromEntries([['parent', 'parent'], ['candidate', 'inventory'], ['record', 'record'], ['review', 'review'], ['assent', 'assent']].map(([key, name]) => [key, pin(name + '.json')]));
  const designLock = path.join(root, 'design-lock.json');
  write(root, 'design-lock.json', {inputs: [binding.parent], inventorySuccessors: [binding], contractSuccessors: []});
  return {
    temp, root, own, record, write,
    output: path.join(root, own, 'dist/helper.js'),
    args: {root, architecture, designLock, record},
    compile(allowErrors = false) {
      const p = spawnSync(process.execPath, [tsc, '--project', path.join(root, record.tsconfig)], {encoding: 'utf8'});
      if (!allowErrors && p.status !== 0) {
        const err = new Error(p.stdout + p.stderr);
        err.compileFailed = true;
        throw err;
      }
      return p;
    },
    cleanup() { fs.rmSync(temp, {recursive: true, force: true}); },
  };
}

const distFrom = (r, own) => r.edges.filter(e => String(e.from || '').startsWith(own + '/dist/'));

{
  const f = fixture({});
  try {
    const clean = await checkBoundary(f.args);
    check('clean-pass-zero-generated', clean.passed === true && clean.stats.verifiedGeneratedFiles === 0, json(clean.refusals));
    f.compile();
    const built = await checkBoundary(f.args);
    check('verified-maps-to-ts', built.passed === true && built.stats.verifiedGeneratedFiles === 2
      && built.edges.some(e => e.graph === 'runtime' && e.resolved === f.own + '/src/helper.ts' && e.emittedOutput === f.own + '/dist/helper.js'));
    check('verified-no-dist-from', distFrom(built, f.own).length === 0, json(distFrom(built, f.own)));
  } finally { f.cleanup(); }
}

for (const browser of [false, true]) {
  const f = fixture({browser});
  try {
    f.compile();
    const marker = path.join(f.root, 'executed');
    fs.appendFileSync(f.output, `\nimport fs from 'node:fs'; fs.writeFileSync(${JSON.stringify(marker)}, 'bad');\n`);
    const r = await checkBoundary(f.args);
    const fromDist = distFrom(r, f.own);
    check(`${browser ? 'browser' : 'node'}-changed-refuses-census`, r.passed === false && r.refusals.some(x => x.category === 'undeclared-local' && x.file === f.own + '/dist/helper.js'));
    check(`${browser ? 'browser' : 'node'}-changed-not-executed`, fs.existsSync(marker) === false);
    check(`${browser ? 'browser' : 'node'}-changed-no-dist-from`, fromDist.length === 0, json(fromDist.slice(0, 4)));
    check(`${browser ? 'browser' : 'node'}-changed-runtime-unit-refusal`, r.refusals.some(x => x.category === 'unsupported-runtime-target' && x.from === f.own + '/dist/helper.js'), json(r.refusals));
  } finally { f.cleanup(); }
}

{
  const f = fixture({});
  try {
    f.compile();
    fs.copyFileSync(f.output, path.join(f.root, f.own, 'dist/extra.js'));
    const r = await checkBoundary(f.args);
    check('extra-census-refused', r.passed === false && r.refusals.some(x => x.file === f.own + '/dist/extra.js' && x.category === 'undeclared-local'));
    check('extra-no-from-node', !r.edges.some(e => e.from === f.own + '/dist/extra.js'), json(r.edges.filter(e => String(e.from || '').includes('extra')).slice(0, 3)));
  } finally { f.cleanup(); }
}

{
  const f = fixture({});
  try {
    f.compile();
    const outside = path.join(f.root, 'same.js');
    fs.copyFileSync(f.output, outside);
    fs.unlinkSync(f.output);
    fs.symlinkSync(outside, f.output);
    const r = await checkBoundary(f.args);
    check('symlink-census-refused', r.passed === false && r.refusals.some(x => x.file === f.own + '/dist/helper.js' && x.category === 'undeclared-local'));
    check('symlink-no-dist-or-outside-from', !r.edges.some(e => e.from === f.own + '/dist/helper.js' || e.from === 'same.js'), json(r.edges.filter(e => String(e.from || '').includes('helper.js') || e.from === 'same.js').slice(0, 4)));
  } finally { f.cleanup(); }
}

{
  const f = fixture({declaredJs: true, outDir: null});
  try {
    const r = await checkBoundary(f.args);
    const leafHits = r.edges.filter(e => e.from === f.own + '/src/leaf.js' || e.resolved === f.own + '/src/leaf.js');
    check('declared-local-js-still-scanned', r.passed === true && leafHits.length > 0 && !r.refusals.some(x => x.from === f.own + '/src/leaf.js' || x.file === f.own + '/src/leaf.js'), json({passed: r.passed, refusals: r.refusals, leafHits, stats: r.stats}));
    check('declared-local-js-not-treated-as-dist', !r.edges.some(e => String(e.from || '').includes('/dist/leaf.js')));
  } catch (err) {
    if (!rows.some(r => r.name.startsWith('declared-local-js'))) check('declared-local-js-still-scanned', false, String(err));
  } finally { f.cleanup(); }
}

{
  const f = fixture({external: true});
  try {
    try { f.compile(); } catch (err) { check('external-js-compile', false, String(err)); throw err; }
    const r = await checkBoundary(f.args);
    const extEdges = r.edges.filter(e => e.request === 'ext' || String(e.from || '').includes('node_modules/ext/'));
    check('external-js-still-resolved', r.passed === true && r.edges.some(e => e.request === 'ext' && String(e.resolved || '').includes('node_modules/ext')), json({passed: r.passed, refusals: r.refusals, extEdges: extEdges.slice(0, 6)}));
  } catch (err) {
    if (!rows.some(r => r.name.startsWith('external-js'))) check('external-js-still-resolved', false, String(err));
  } finally { f.cleanup(); }
}

{
  const leftover = fs.readdirSync(os.tmpdir()).filter(n => n.startsWith('opensip-generated-challenge10-'));
  check('challenge-temps-cleaned', leftover.length === 0, leftover.join(','));
}

const failed = rows.filter(r => !r.passed).map(r => r.name);
const out = path.join(path.dirname(fileURLToPath(import.meta.url)), '../results/challenge.json');
fs.writeFileSync(out, json({caseCount: rows.length, failedCount: failed.length, failed, cases: rows}));
console.log(json({caseCount: rows.length, failedCount: failed.length, failed}));
if (failed.length) process.exitCode = 1;
