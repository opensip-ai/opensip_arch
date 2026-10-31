// TSR-1 r3 interpretation evidence (TSR1-R2-RF-3): package `exports` into the output directory, with outDir/rootDir
// honored vs stripped, over an in-memory host. Variants: input-only, output-side declaration only, both, neither.
const ts = require(process.argv[2]);
const base = {'/proj/package.json': JSON.stringify({name: 'pkg', exports: {'.': './dist/index.js'}}), '/proj/src/main.ts': 'import "pkg";\n',
  '/proj/tsconfig.json': '{}'};
const variants = {inputAndOutputDecl: {'/proj/src/index.ts': '', '/proj/dist/index.d.ts': ''}, inputOnly: {'/proj/src/index.ts': ''},
  outputDeclOnly: {'/proj/dist/index.d.ts': ''}, neither: {}};
const out = {version: ts.version, results: {}};
for (const [v, extra] of Object.entries(variants)) {
  const files = new Map(Object.entries({...base, ...extra}));
  const host = {fileExists: f => files.has(f), readFile: f => files.get(f), directoryExists: d => [...files.keys()].some(f => f.startsWith(d.replace(/\/$/, '') + '/')),
    realpath: f => f, getCurrentDirectory: () => '/proj', getDirectories: () => []};
  const go = opts => { const r = ts.resolveModuleName('pkg', '/proj/src/main.ts', {module: ts.ModuleKind.ESNext, moduleResolution: ts.ModuleResolutionKind.Bundler, configFilePath: '/proj/tsconfig.json', ...opts}, host).resolvedModule; return r ? r.resolvedFileName : null; };
  out.results[v] = {honored: go({outDir: '/proj/dist', rootDir: '/proj/src'}), stripped: go({})};
}
console.log(JSON.stringify(out, null, 1));
