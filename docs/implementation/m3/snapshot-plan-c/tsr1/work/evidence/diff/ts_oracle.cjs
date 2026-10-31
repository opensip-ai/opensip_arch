// TSR-1 r2 interpretation evidence: TypeScript 6.0.3's own config parse over an IN-MEMORY, case-sensitive host.
// Usage: node ts_oracle.cjs <typescript.js> <cases.json> <ts package lib dir>   (no filesystem access for case files)
const ts = require(process.argv[2]);
const cases = JSON.parse(require('fs').readFileSync(process.argv[3], 'utf8'));
const libdir = process.argv[4];
const ROOT = '/proj';
const inv = (decl, canon) => { const m = new Map(); for (const [k, v] of decl.type) if (!m.has(v) || canon.includes(k)) m.set(v, k); return m; };
const T = inv(ts.targetOptionDeclaration.type ? ts.targetOptionDeclaration : null, ['es2015']);
const M = inv(ts.moduleOptionDeclaration, ['es2015']);
const MR = new Map([[1, 'classic'], [2, 'node10'], [3, 'node16'], [99, 'nodenext'], [100, 'bundler']]);
const JSX = new Map([[1, 'preserve'], [2, 'react'], [3, 'react-native'], [4, 'react-jsx'], [5, 'react-jsxdev']]);
const rel = p => p === ROOT ? '' : p.startsWith(ROOT + '/') ? p.slice(ROOT.length + 1) : '<outside>' + p;
const refs = f => require('fs').readFileSync(libdir + '/' + f, 'utf8').split('\n').filter(l => l.startsWith('/// <reference lib=')).map(l => l.match(/lib="([^"]+)"/)[1]);
const out = {version: ts.version, cases: {}};
for (const c of cases) {
  const files = new Map(Object.entries(c.files).map(([p, t]) => [ROOT + '/' + p, t]));
  const dirs = new Set([ROOT]); for (const p of files.keys()) { let d = p; while ((d = d.slice(0, d.lastIndexOf('/'))) && d.length >= ROOT.length) dirs.add(d); }
  const entries = dir => { const fl = [], ds = []; const pre = dir.endsWith('/') ? dir : dir + '/';
    for (const p of files.keys()) if (p.startsWith(pre) && !p.slice(pre.length).includes('/')) fl.push(p.slice(pre.length));
    for (const d of dirs) if (d.startsWith(pre) && d !== dir && !d.slice(pre.length).includes('/')) ds.push(d.slice(pre.length));
    return {files: fl, directories: ds}; };
  const host = {useCaseSensitiveFileNames: true, getCurrentDirectory: () => ROOT,
    fileExists: p => files.has(p), readFile: p => files.get(p), directoryExists: d => dirs.has(d.replace(/\/$/, '')),
    readDirectory: (root, ext, exc, inc, depth) => ts.matchFiles(root, ext, exc, inc, true, ROOT, depth, entries, p => p),
    onUnRecoverableConfigFileDiagnostic: () => {}};
  const parsed = ts.getParsedCommandLineOfConfigFile(ROOT + '/' + c.entry, {}, host);
  const o = parsed.options;
  const target = ts.getEmitScriptTarget(o);
  const lib = o.lib ? o.lib.map(f => f.slice(4, -5)) : refs(ts.getDefaultLibFileName(o));
  let paths = [];
  if (o.paths) { const base = o.baseUrl ?? o.pathsBasePath; paths = Object.keys(o.paths).map(k => ({pattern: k, substitutions: o.paths[k].map(s => rel(ts.getNormalizedAbsolutePath(s, base)))})); }
  out.cases[c.name] = {
    target: T.get(target), module: M.get(ts.getEmitModuleKind(o)), moduleResolution: MR.get(ts.getEmitModuleResolutionKind(o)),
    jsx: o.jsx === undefined ? null : JSX.get(o.jsx), strict: o.strict !== false, esModuleInterop: ts.getESModuleInterop(o),
    allowSyntheticDefaultImports: ts.getAllowSyntheticDefaultImports(o), resolveJsonModule: ts.getResolveJsonModule(o),
    allowJs: ts.getAllowJSCompilerOption(o), checkJs: !!o.checkJs, skipLibCheck: !!o.skipLibCheck, types: o.types ?? [],
    customConditions: o.customConditions ?? [], lib, baseUrl: o.baseUrl === undefined ? null : rel(o.baseUrl),
    rootDirs: (o.rootDirs ?? []).map(rel), paths, programRootFiles: parsed.fileNames.map(rel),
    errors: [...new Set(parsed.errors.map(e => e.code))].sort((a, b) => a - b)};
}
console.log(JSON.stringify(out, null, 1));
