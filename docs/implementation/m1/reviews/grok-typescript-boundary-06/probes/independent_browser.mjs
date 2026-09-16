/** Independent esbuild scanner attacks. Not a restatement of root06-browser.mjs. */
import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const COPY = '/tmp/opensip-implementation/m1-grok-typescript-boundary-review-06/review/copy';
const RESULTS = '/tmp/opensip-implementation/m1-grok-typescript-boundary-review-06/review/results';
const WORK = path.join(COPY, 'work/independent-browser');
const { createBrowserResolver: current } = await import(pathToFileURL(path.join(COPY, 'checker/src/browser-scanner.mjs')).href);
const { build } = await import(pathToFileURL(path.join(COPY, 'checker/node_modules/esbuild/lib/main.js')).href);
const { browserOptions } = await import(pathToFileURL(path.join(COPY, 'checker/src/browser-options.mjs')).href);

fs.mkdirSync(WORK, { recursive: true });
fs.mkdirSync(RESULTS, { recursive: true });

const rows = [];
function rec(name, passed, observed) {
  rows.push({ name, passed: !!passed, observed });
  console.log(passed ? 'PASS' : 'FAIL', name, observed ?? '');
}

async function firstFixResolve(root, request, baseFile, mode) {
  // Replica of root06-browser-scanner-before-fix.mjs classification.
  const loaded = [];
  const body = mode === 'require'
    ? `globalThis.__opensip_edge=require(${JSON.stringify(request)});`
    : `import * as dependency from ${JSON.stringify(request)};globalThis.__opensip_edge=dependency;`;
  let r;
  try {
    r = await build({
      ...browserOptions(), absWorkingDir: root, entryPoints: [baseFile], outfile: 'unused-resolution.js',
      metafile: true, treeShaking: false,
      plugins: [{
        name: 'opensip-edge-resolution',
        setup(api) {
          api.onResolve({ filter: /.*/ }, a => a.kind === 'entry-point' ? { path: baseFile, namespace: 'file' } : undefined);
          api.onLoad({ filter: /.*/, namespace: 'file' }, a => {
            if (a.path === baseFile && !a.suffix) return { contents: body, loader: 'js', resolveDir: path.dirname(baseFile) };
            loaded.push({ path: a.path, suffix: a.suffix });
            return { contents: 'export const boundaryPlaceholder=0;', loader: 'js', resolveDir: path.dirname(a.path) };
          });
        },
      }],
    });
  } catch {
    return { kind: 'refused' };
  }
  const entry = Object.entries(r.metafile.inputs).find(([file]) => path.resolve(root, file) === baseFile);
  const edge = entry?.[1].imports[0];
  if (!edge) return { kind: 'refused', detail: 'missing-scanned-edge' };
  if (edge.path.startsWith('(disabled):')) return { kind: 'ignored', firstFix: true, edge: edge.path };
  return { kind: 'other', edge: edge.path };
}

function writePkg(dir, files) {
  fs.mkdirSync(dir, { recursive: true });
  for (const [name, text] of Object.entries(files)) {
    const p = path.join(dir, name);
    fs.mkdirSync(path.dirname(p), { recursive: true });
    fs.writeFileSync(p, text);
  }
}

async function scan(id, files, request, mode = 'import', from = 'entry.mjs') {
  const dir = path.join(WORK, id);
  writePkg(dir, files);
  const r = await current(dir);
  const result = await r.resolve(request, path.join(dir, from), mode);
  await r.dispose();
  return result;
}

// 1. literal (disabled): filename must resolve, not ignore
{
  const cur = await scan('literal-disabled', {
    'entry.mjs': '',
    '(disabled):target.js': 'export const x = 1; throw new Error("must-not-evaluate");',
  }, './(disabled):target.js');
  rec('literal-disabled-filename-resolved', cur.kind === 'resolved' && cur.path.endsWith('(disabled):target.js'), cur);
  const first = await firstFixResolve(
    path.join(WORK, 'literal-disabled'),
    './(disabled):target.js',
    path.join(WORK, 'literal-disabled/entry.mjs'),
    'import',
  );
  rec('first-fix-wrongly-ignored-literal-disabled-filename', first.kind === 'ignored', first);
}

// 2. browser:false is ignored even if the physical file would throw / import missing
{
  writePkg(path.join(WORK, 'browser-false'), {
    'package.json': JSON.stringify({ name: 't', version: '1.0.0', browser: { './dep.js': false } }),
    'entry.mjs': '',
    'dep.js': 'import "definitely-missing-pkg"; throw new Error("must-not-evaluate");',
  });
  const r = await current(path.join(WORK, 'browser-false'));
  const result = await r.resolve('./dep.js', path.join(WORK, 'browser-false/entry.mjs'), 'import');
  await r.dispose();
  rec('browser-false-ignored-and-not-evaluated', result.kind === 'ignored', result);
}

// 3. live node builtin without browser:false
{
  const result = await scan('builtin-live', { 'entry.mjs': '' }, 'node:fs');
  rec('node-fs-without-disable-refused', result.kind === 'refused' && result.detail === 'builtin', result);
}

// 4. query suffix recorded
{
  const result = await scan('query', {
    'entry.mjs': '',
    'dep.js': 'export const x=1;',
  }, './dep.js?one');
  rec('query-suffix-recorded', result.kind === 'resolved' && result.suffix === '?one', result);
}

// 5. fragment suffix
{
  const result = await scan('frag', {
    'entry.mjs': '',
    'dep.js': 'export const x=1;',
  }, './dep.js#one');
  rec('fragment-suffix-recorded', result.kind === 'resolved' && result.suffix === '#one', result);
}

// 6. missing target
{
  const result = await scan('missing', { 'entry.mjs': '' }, './nope.js');
  rec('missing-target-unresolved', result.kind === 'refused' && result.detail === 'unresolved', result);
}

// 7. symlink physical path
{
  const dir = path.join(WORK, 'symlink');
  writePkg(dir, { 'entry.mjs': '', 'real.js': 'export const x=1;' });
  fs.symlinkSync('real.js', path.join(dir, 'link.js'));
  const r = await current(dir);
  const result = await r.resolve('./link.js', path.join(dir, 'entry.mjs'), 'import');
  await r.dispose();
  rec('symlink-uses-realpath', result.kind === 'resolved' && result.path === fs.realpathSync(path.join(dir, 'real.js')), result);
}

// 8. repository body not evaluated
{
  const result = await scan('no-eval', {
    'entry.mjs': '',
    'dep.js': 'process.exit(99);\nthrow new Error("evaluated");\n',
  }, './dep.js');
  rec('repository-js-not-evaluated', result.kind === 'resolved' && process.exitCode !== 99, result);
}

// 9. import vs require mainFields (module vs main)
{
  const dir = path.join(WORK, 'fields');
  writePkg(dir, {
    'package.json': JSON.stringify({
      name: 'fields', version: '1.0.0',
      main: './cjs.js',
      module: './esm.js',
    }),
    'entry.mjs': '',
    'entry.cjs': '',
    'cjs.js': 'module.exports = { kind: "cjs" };',
    'esm.js': 'export const kind = "esm";',
  });
  const r = await current(dir);
  const imp = await r.resolve('.', path.join(dir, 'entry.mjs'), 'import');
  const req = await r.resolve('.', path.join(dir, 'entry.cjs'), 'require');
  await r.dispose();
  rec('import-prefers-module-field', imp.kind === 'resolved' && imp.path.endsWith('esm.js'), imp);
  rec('require-observed-main-or-module', req.kind === 'resolved', { req, note: 'record which field require selected' });
}

// 10. package exports + conditions:['module']
{
  const dir = path.join(WORK, 'exports');
  writePkg(dir, {
    'package.json': JSON.stringify({
      name: 'ex', version: '1.0.0',
      exports: { '.': { import: './esm.js', require: './cjs.js', default: './cjs.js' } },
    }),
    'entry.mjs': '',
    'entry.cjs': '',
    'esm.js': 'export const k="esm";',
    'cjs.js': 'module.exports={k:"cjs"};',
  });
  const r = await current(dir);
  const imp = await r.resolve('.', path.join(dir, 'entry.mjs'), 'import');
  const req = await r.resolve('.', path.join(dir, 'entry.cjs'), 'require');
  await r.dispose();
  rec('exports-import-condition', imp.kind === 'resolved' && imp.path.endsWith('esm.js'), imp);
  rec('exports-require-observed', req.kind === 'resolved', req);
}

// 11. https / data refuse
{
  const https = await scan('https', { 'entry.mjs': '' }, 'https://example.invalid/a.js');
  const data = await scan('data', { 'entry.mjs': '' }, 'data:text/javascript,export default 1');
  rec('https-and-data-refused', https.kind === 'refused' && data.kind === 'refused', { https, data });
}

// 12. browserOptions shared recipe
{
  rec('browser-options-recipe',
    JSON.stringify(browserOptions().mainFields) === JSON.stringify(['browser', 'module', 'main'])
    && JSON.stringify(browserOptions().conditions) === JSON.stringify(['module'])
    && browserOptions().preserveSymlinks === false
    && browserOptions().platform === 'browser');
}

const failed = rows.filter(r => !r.passed);
const out = {
  standing: 'independent Grok TS06 browser-scanner probes; not product bundler selection',
  passed: failed.length === 0,
  caseCount: rows.length,
  failedCount: failed.length,
  failed: failed.map(r => r.name),
  checks: rows,
};
fs.writeFileSync(path.join(RESULTS, 'independent-browser.json'), JSON.stringify(out, null, 2) + '\n');
console.log(JSON.stringify({ passed: out.passed, caseCount: out.caseCount, failed: out.failed }));
if (failed.length) process.exit(1);
