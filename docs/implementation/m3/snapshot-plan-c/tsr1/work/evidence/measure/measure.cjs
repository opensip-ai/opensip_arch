// TSR-1 interpretation evidence (not a product run): TypeScript 6.0.3's own parse of synthetic configs.
const ts = require(process.argv[2]);
const fs = require('fs'), path = require('path');
const root = process.argv[3];
const out = {version: ts.version, cases: {}};
for (const name of fs.readdirSync(root).sort()) {
  const dir = path.join(root, name);
  if (!fs.statSync(dir).isDirectory()) continue;
  const entry = fs.existsSync(path.join(dir, 'tsconfig.json')) ? 'tsconfig.json' : 'jsconfig.json';
  const cfgPath = path.join(dir, entry);
  const host = {...ts.sys, useCaseSensitiveFileNames: true};
  const parsed = ts.getParsedCommandLineOfConfigFile(cfgPath, {}, {...host, onUnRecoverableConfigFileDiagnostic: d => {}});
  const o = parsed.options;
  const rel = p => path.relative(dir, p).split(path.sep).join('/');
  out.cases[name] = {
    target: ts.getEmitScriptTarget(o), module: ts.getEmitModuleKind(o), moduleResolution: ts.getEmitModuleResolutionKind(o),
    strict: ts.getStrictOptionValue(o, 'noImplicitAny'), esModuleInterop: ts.getESModuleInterop(o),
    allowSyntheticDefaultImports: ts.getAllowSyntheticDefaultImports(o), resolveJsonModule: ts.getResolveJsonModule(o),
    allowJs: ts.getAllowJSCompilerOption(o), skipLibCheck: !!o.skipLibCheck, maxNodeModuleJsDepth: o.maxNodeModuleJsDepth ?? 0,
    defaultLib: ts.getDefaultLibFileName(o), lib: o.lib, types: ts.getAutomaticTypeDirectiveNames(o, host),
    baseUrl: o.baseUrl && rel(o.baseUrl), paths: o.paths, pathsBasePath: o.pathsBasePath && rel(o.pathsBasePath),
    rootDirs: o.rootDirs && o.rootDirs.map(rel),
    fileNames: parsed.fileNames.map(rel),
    errors: parsed.errors.map(e => e.code).sort((a,b)=>a-b),
  };
}
console.log(JSON.stringify(out, null, 1));
