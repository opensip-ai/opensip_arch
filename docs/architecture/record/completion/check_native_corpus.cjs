// Language-native design evidence. This never runs source programs or OpenSIP.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const tsRoot = process.env.OPENSIP_TS_REVIEW_ROOT;
if (!tsRoot) throw new Error('Set OPENSIP_TS_REVIEW_ROOT to the pinned TypeScript package directory');
const tsPath = path.join(tsRoot, 'lib/typescript.js');
const ts = require(tsPath);
const sha = p => crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const folder = __dirname;
const corpusRoot = path.join(folder, 'quality-corpus.v1');
const manifestPath = path.join(folder, 'quality-corpus-manifest.v1.json');
const manifest = JSON.parse(fs.readFileSync(manifestPath));
const prototypeSource = path.join(folder, 'prototype-program-service.pinned.ts');
const prototypeModule = { exports: {} };
const prototypeJs = ts.transpileModule(fs.readFileSync(prototypeSource, 'utf8'), {
  compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2022 }
}).outputText;
new Function('require', 'module', 'exports', prototypeJs)(
  name => name === 'typescript' ? ts : require(name), prototypeModule, prototypeModule.exports);
for (const entry of manifest.files) {
  if (sha(path.resolve(folder, '../../..', entry.path)) !== entry.sha256) throw new Error('Corpus pin mismatch: ' + entry.path);
}
const options = { strict: true, noEmit: true, target: ts.ScriptTarget.ES2022,
  module: ts.ModuleKind.ESNext, moduleResolution: ts.ModuleResolutionKind.Bundler };
function cycles(edges) {
  const nodes = [...new Set(edges.flat())].sort();
  const reaches = (start, target, seen = new Set()) => {
    if (seen.has(start)) return false;
    seen.add(start);
    return edges.some(([a, b]) => a === start && (b === target || reaches(b, target, seen)));
  };
  const groups = [];
  const used = new Set();
  for (const n of nodes) {
    if (used.has(n)) continue;
    const group = nodes.filter(m => m === n || (reaches(n, m) && reaches(m, n)));
    group.forEach(m => used.add(m));
    if (group.length > 1 || edges.some(([a,b]) => a === n && b === n)) groups.push(group);
  }
  return groups.sort((a,b) => a[0].localeCompare(b[0], 'en'));
}
const results = [];
for (const mode of ['native', 'prototype-program-service']) {
for (const [name, fixture] of Object.entries(manifest.projects)) {
  const roots = fixture.files.map(p => path.join(corpusRoot, p));
  const rootSet = new Set(roots);
  const program = mode === 'native' ? ts.createProgram(roots, options) : prototypeModule.exports.createTypeCheckedProgram(roots, { projectRoot: path.join(corpusRoot, name) }).program;
  const checker = program.getTypeChecker();
  const edges = [];
  const calls = [];
  const types = {};
  const bindings = [];
  const callEdges = [];
  let dynamicImport = false;
  const relative = p => path.relative(corpusRoot, p).replaceAll(path.sep, '/');
  for (const file of program.getSourceFiles()) {
    if (!rootSet.has(file.fileName)) continue;
    function visit(node) {
      if (ts.isImportDeclaration(node) && ts.isStringLiteral(node.moduleSpecifier)) {
        const resolved = ts.resolveModuleName(node.moduleSpecifier.text, file.fileName, options, ts.sys).resolvedModule;
        if (resolved && rootSet.has(resolved.resolvedFileName)) edges.push([relative(file.fileName), relative(resolved.resolvedFileName)]);
      }
      if (ts.isCallExpression(node)) {
        if (node.expression.kind === ts.SyntaxKind.ImportKeyword) dynamicImport = true;
        const decl = checker.getResolvedSignature(node)?.declaration;
        if (decl && rootSet.has(decl.getSourceFile().fileName)) {
          let parent = node.parent;
          while (parent && !ts.isFunctionDeclaration(parent)) parent = parent.parent;
          const caller = relative(file.fileName) + ':' + (parent?.name?.text || 'module');
          callEdges.push([caller, relative(decl.getSourceFile().fileName) + ':' + (decl.name?.getText() || '<anonymous>')]);
          calls.push({
          from: relative(file.fileName), target: relative(decl.getSourceFile().fileName),
          name: decl.name?.getText() || '<anonymous>' });
        }
      }
      if (ts.isFunctionDeclaration(node) && node.name) {
        const signature = checker.getSignatureFromDeclaration(node);
        types[relative(file.fileName) + ':' + node.name.text + '.return'] = checker.typeToString(checker.getReturnTypeOfSignature(signature));
      }
      if (ts.isVariableDeclaration(node) && ts.isIdentifier(node.name))
        types[relative(file.fileName) + ':' + node.name.text] = checker.typeToString(checker.getTypeAtLocation(node.name));
      if (ts.isReturnStatement(node) && node.expression && ts.isIdentifier(node.expression)) {
        const declarations = checker.getSymbolAtLocation(node.expression)?.declarations || [];
        bindings.push({ name: node.expression.text,
          kinds: declarations.map(d => ts.SyntaxKind[d.kind]) });
      }
      ts.forEachChild(node, visit);
    }
    visit(file);
  }
  const diagnostics = ts.getPreEmitDiagnostics(program).filter(d => d.category === ts.DiagnosticCategory.Error);
  const coverage = diagnostics.length || dynamicImport ? 'unknown' : 'complete';
  const sortedEdges = [...new Map(edges.map(e => [JSON.stringify(e), e])).values()].sort();
  const actualCycles = coverage === 'complete' ? cycles(sortedEdges) : null;
  let passed = JSON.stringify(sortedEdges) === JSON.stringify(fixture.expectedProjectImportEdges)
    && JSON.stringify(actualCycles) === JSON.stringify(fixture.expectedCycles)
    && coverage === fixture.coverage;
  const reachability = new Set();
  for (const start of new Set(callEdges.map(e => e[0]))) {
    const pending = [start], seen = new Set();
    while (pending.length) {
      const n = pending.pop(); if (seen.has(n)) continue; seen.add(n);
      for (const [from, target] of callEdges) if (from === n) {
        reachability.add(JSON.stringify([start, target])); pending.push(target);
      }
    }
  }
  const observations = fixture.observations || {};
  const queryResults = {};
  if (observations.resolvedCall) {
    const [from, target] = observations.resolvedCall;
    queryResults.resolvedCall = calls.some(c => c.from + ':' + c.name === from && c.target + ':' + c.name === target);
  }
  if (observations.checkedType) {
    const [key, expected] = observations.checkedType;
    queryResults.checkedType = types[key] === expected;
  }
  if (observations.reachable) queryResults.reachable = reachability.has(JSON.stringify(observations.reachable));
  if (observations.returnValueBindsTo) {
    queryResults.returnValueBindsTo = bindings.length === 1 && bindings[0].name === 'value' && JSON.stringify(bindings[0].kinds) === '["Parameter"]';
    queryResults.returnValueDoesNotBindTo = !bindings.some(b => b.kinds.includes('VariableDeclaration'));
  }
  passed &&= Object.values(queryResults).every(Boolean);
  results.push({ mode, project: name, passed, queryResults, callEdges, reachability: [...reachability].map(JSON.parse).sort(), actualProjectImportEdges: sortedEdges, actualCycles,
    coverageObservation: coverage, diagnostics: diagnostics.map(d => d.code), calls, types, bindings });
}
}
const report = {
  kind: 'language-native-design-corpus-check', productQualification: false,
  compilerVersion: ts.version, nodeVersion: process.version,
  pins: { corpusManifest: sha(manifestPath), compiler: sha(tsPath), checker: sha(__filename),
    prototypeSource: sha(prototypeSource), packageLock: sha(path.join(tsRoot, '../../package-lock.json')) },
  interpretation: 'Checks the selected corpus observations with the pinned TypeScript compiler. No OpenSIP provider, D9 mapping, sealed identity, process containment or four-platform gate is executed.',
  count: results.length, passed: results.filter(r => r.passed).length, results
};
const reportIndex = process.argv.indexOf('--report');
if (reportIndex >= 0 && !process.argv[reportIndex + 1]) throw new Error('--report requires a path');
fs.writeFileSync(reportIndex >= 0 ? process.argv[reportIndex + 1] : path.join(folder, 'native-corpus-report.v1.json'), JSON.stringify(report, null, 2) + '\n');
console.log(JSON.stringify({ count: report.count, passed: report.passed, compilerVersion: ts.version, productQualification: false }));
if (report.count !== report.passed) process.exitCode = 1;
