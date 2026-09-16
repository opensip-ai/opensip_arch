/** Independent generated-output recognition/mapping challenges. */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import crypto from 'node:crypto';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {checkBoundary} from '../tools/typescript-boundary/src/check.mjs';

const json = value => JSON.stringify(value, null, 2) + '\n';
const pkgRoot = fileURLToPath(new URL('../tools/typescript-boundary/', import.meta.url));
const tsc = path.join(pkgRoot, 'node_modules/typescript/bin/tsc');
const rows = [];
const check = (name, passed, detail = '') => {
  rows.push({name, passed: Boolean(passed), detail: String(detail).slice(0, 800)});
  console.log(passed ? 'PASS' : 'FAIL', name, String(detail).slice(0, 220));
};

function fixture({browser = false, bom = false, outDir = 'dist', sourceMap = false, declaration = false, extraTs = false} = {}) {
  const temp = fs.realpathSync(fs.mkdtempSync(path.join(os.tmpdir(), 'opensip-generated-challenge09-')));
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
  if (extraTs) inputs.push(own + '/src/unused.ts');
  const record = {
    schemaVersion: 2, package: id, packageRoot: own, manifest: own + '/package.json', tsconfig: own + '/tsconfig.json',
    inputs: extraTs ? inputs.slice(0, 2) : inputs,
    packageManager: {kind: 'fixture-unlocked', lockfile: null}, trustedUsages: [],
  };
  write(root, record.manifest, {name: browser ? '@fixture/report' : '@fixture/provider', private: true, type: 'module'});
  write(root, record.tsconfig, {
    compilerOptions: {
      strict: true, target: 'ES2022', module: browser ? 'ESNext' : 'NodeNext',
      moduleResolution: browser ? 'Bundler' : 'NodeNext', types: [], lib: ['ES2022', 'DOM'],
      rootDir: 'src', outDir, emitBOM: bom, sourceMap, declaration,
    },
    include: ['src/**/*.ts'],
  });
  write(root, own + '/src/helper.ts', 'export const value:number = 42;\n');
  write(root, own + '/src/index.ts', 'import {value} from "./helper.js";\nexport const answer=value;\nexport const url=new URL("./helper.js",import.meta.url);\n');
  if (extraTs) write(root, own + '/src/unused.ts', 'export const leftover:number = 1;\n');
  const files = [...record.inputs, record.manifest, record.tsconfig];
  if (extraTs) files.push(own + '/src/unused.ts');
  const inventory = {
    standing: 'synthetic mechanics only; no acceptance',
    packages: [{id, path: own, kind: 'typescript-package', dependencies: []}],
    files: files.map(p => ({path: p, package: id, role: p.endsWith('.ts') ? 'model' : 'configuration'})),
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
  const output = path.join(root, own, outDir, 'helper.js');
  return {
    temp, root, own, record, write, output, outDir,
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

const fromDist = r => r.edges.filter(e => String(e.from || '').includes('/dist/') || String(e.from || '').includes('/src/helper.js') || String(e.from || '').endsWith('/helper.js') && String(e.from || '').includes('dist'));

{
  const f = fixture({});
  try {
    const clean = await checkBoundary(f.args);
    check('clean-pass-zero-generated', clean.passed === true && clean.stats.verifiedGeneratedFiles === 0, json(clean.refusals));
    f.compile();
    const built = await checkBoundary(f.args);
    check('built-pass-two-generated', built.passed === true && built.stats.verifiedGeneratedFiles === 2, json({refusals: built.refusals, stats: built.stats}));
    check('built-runtime-maps-to-source', built.edges.some(e => e.graph === 'runtime' && e.kind === 'import' && e.resolved === f.own + '/src/helper.ts' && e.emittedOutput === f.own + '/dist/helper.js'));
    check('built-no-from-dist', fromDist(built).length === 0, json(fromDist(built).slice(0, 3)));
  } finally { f.cleanup(); }
}

{
  const f = fixture({});
  try {
    f.compile();
    const marker = path.join(f.root, 'executed');
    fs.appendFileSync(f.output, `\nimport fs from 'node:fs'; fs.writeFileSync(${JSON.stringify(marker)}, 'bad');\n`);
    const r = await checkBoundary(f.args);
    const distFrom = r.edges.filter(e => e.from === f.own + '/dist/helper.js' || e.from === f.own + '/dist/index.js');
    check('changed-refuses-undeclared', r.passed === false && r.refusals.some(x => x.category === 'undeclared-local' && x.file === f.own + '/dist/helper.js'));
    check('changed-not-executed', fs.existsSync(marker) === false);
    check('changed-does-not-scan-unverified-js-as-from', distFrom.length === 0, json(distFrom.slice(0, 5)));
  } finally { f.cleanup(); }
}

{
  const f = fixture({browser: true});
  try {
    f.compile();
    fs.appendFileSync(f.output, '\nimport "node:fs";\n');
    const r = await checkBoundary(f.args);
    const browserNode = r.refusals.filter(x => x.category === 'browser-node');
    const distFrom = r.edges.filter(e => String(e.from || '').startsWith(f.own + '/dist/'));
    check('browser-tampered-dist-still-fails-census', r.passed === false && r.refusals.some(x => x.category === 'undeclared-local'));
    check('browser-tampered-dist-not-admitted-as-node-group-from', distFrom.length === 0, json({distFrom: distFrom.slice(0, 3), browserNode}));
  } finally { f.cleanup(); }
}

{
  const f = fixture({});
  try {
    f.compile();
    fs.copyFileSync(f.output, path.join(f.root, f.own, 'dist/extra.js'));
    const r = await checkBoundary(f.args);
    check('extra-refused', r.passed === false && r.refusals.some(x => x.file === f.own + '/dist/extra.js'));
  } finally { f.cleanup(); }
}

{
  const f = fixture({extraTs: true});
  try {
    const r = await checkBoundary(f.args);
    check('undeclared-ts-refused', r.passed === false && r.refusals.some(x => x.category === 'undeclared-local' && x.file === f.own + '/src/unused.ts'), json(r.refusals));
  } finally { f.cleanup(); }
}

{
  const f = fixture({});
  try {
    f.write(f.root, f.record.tsconfig, {
      compilerOptions: {
        strict: true, target: 'ES2022', module: 'NodeNext', moduleResolution: 'NodeNext',
        types: [], lib: ['ES2022', 'DOM'], rootDir: 'src',
      },
      include: ['src/**/*.ts'],
    });
    f.compile();
    const beside = f.own + '/src/helper.js';
    const r = await checkBoundary(f.args);
    const mapped = r.edges.some(e => e.graph === 'runtime' && e.resolved === f.own + '/src/helper.ts' && e.emittedOutput === beside);
    check('emit-beside-source-admits-exact-js-as-generated', r.passed === true && r.stats.verifiedGeneratedFiles === 2 && mapped && fs.existsSync(path.join(f.root, beside)), json({passed: r.passed, stats: r.stats, refusals: r.refusals, mapped}));
    check('emit-beside-source-does-not-treat-js-as-declared-from', !r.edges.some(e => e.from === beside), json(r.edges.filter(e => e.from && e.from.endsWith('.js')).slice(0, 4)));
  } finally { f.cleanup(); }
}

{
  const f = fixture({declaration: true});
  try {
    f.compile();
    const dts = f.own + '/dist/helper.d.ts';
    const r = await checkBoundary(f.args);
    const dtsRefusal = r.refusals.find(x => x.file === dts);
    check('declaration-emit-not-blanket-ignored', Boolean(dtsRefusal) && dtsRefusal.category === 'undeclared-local', json({passed: r.passed, refusals: r.refusals, stats: r.stats}));
  } finally { f.cleanup(); }
}

{
  const f = fixture({sourceMap: true});
  try {
    f.compile();
    const r = await checkBoundary(f.args);
    check('sourcemap-disk-mismatch-refuses-generated-js', r.passed === false && r.refusals.some(x => x.category === 'undeclared-local' && x.file === f.own + '/dist/helper.js'), json({passed: r.passed, refusals: r.refusals, stats: r.stats}));
  } finally { f.cleanup(); }
}

{
  const f = fixture({});
  try {
    f.compile();
    f.write(f.root, f.record.tsconfig, '{ not json');
    let threw = false;
    let r;
    try { r = await checkBoundary(f.args); } catch (err) { threw = true; r = {error: String(err)}; }
    check('config-error-does-not-throw', threw === false, json(r));
    check('config-error-does-not-admit-stale-dist', r && r.passed === false && (r.refusals || []).some(x => x.category === 'config-invalid' || (x.category === 'undeclared-local' && String(x.file || '').includes('/dist/'))), json(r?.refusals));
  } finally { f.cleanup(); }
}

{
  const f = fixture({browser: true});
  try {
    f.write(f.root, f.own + '/src/helper.ts', 'import "node:fs";\nexport const value:number=42;\n');
    f.compile(true);
    const r = await checkBoundary(f.args);
    check('browser-source-node-builtin-refused', r.passed === false && r.refusals.some(x => x.category === 'browser-node'), json(r.refusals));
    check('browser-source-not-accepted-as-dist-js-route', !r.passed, 'failed check');
  } finally { f.cleanup(); }
}

{
  const leftover = fs.readdirSync(os.tmpdir()).filter(n => n.startsWith('opensip-generated-challenge09-'));
  check('challenge-temps-cleaned', leftover.length === 0, leftover.join(','));
}

const failed = rows.filter(r => !r.passed).map(r => r.name);
const out = path.join(path.dirname(fileURLToPath(import.meta.url)), '../results/challenge.json');
fs.writeFileSync(out, json({caseCount: rows.length, failedCount: failed.length, failed, cases: rows}));
console.log(json({caseCount: rows.length, failedCount: failed.length, failed}));
if (failed.length) process.exitCode = 1;
