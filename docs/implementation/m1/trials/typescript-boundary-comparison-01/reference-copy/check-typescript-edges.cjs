'use strict';
// Developer input-graph check. It neither executes package scripts nor attests
// runtime purity. The selected compiler is an explicit trusted tool input.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const { isBuiltin } = require('node:module');

class BoundaryError extends Error {}
function need(value, message) { if (!value) throw new BoundaryError(message); }
function within(child, parent) {
  const relative = path.relative(parent, child);
  return relative === '' || (!relative.startsWith('..' + path.sep) && relative !== '..' && !path.isAbsolute(relative));
}
function relativePath(value) {
  need(typeof value === 'string' && value.length > 0 && !value.includes('\\') && !value.includes('\0') &&
    !path.posix.isAbsolute(value) && !value.split('/').some(p => p === '' || p === '.' || p === '..'), 'noncanonical input path');
  return value;
}
function pin(file) {
  const raw = fs.readFileSync(file);
  return { sha256: crypto.createHash('sha256').update(raw).digest('hex'), bytes: raw.length };
}
function regularSource(root, relative) {
  let current = root;
  for (const part of relativePath(relative).split('/')) {
    current = path.join(current, part);
    need(!fs.lstatSync(current).isSymbolicLink(), 'symlink in local source: ' + relative);
  }
  need(fs.statSync(current).isFile(), 'local source is not a regular file: ' + relative);
  return current;
}
function packageName(specifier) {
  return specifier.startsWith('@') ? specifier.split('/').slice(0, 2).join('/') : specifier.split('/')[0];
}
function diagnostic(ts, items) {
  return items.map(d => (d.file ? d.file.fileName + ': ' : '') + ts.flattenDiagnosticMessageText(d.messageText, '\n')).join('\n');
}

function check({ root, inventory, lane, config, files, compiler }) {
  root = fs.realpathSync(root);
  const ts = require(compiler);
  need(ts.version === '6.0.3', 'unselected compiler API version');
  need(Array.isArray(inventory.packages), 'missing package inventory');
  const packages = inventory.packages.filter(p => p.path).map(p => ({ ...p, absolute: path.join(root, relativePath(p.path)) }));
  need(new Set(packages.map(p => p.path)).size === packages.length, 'duplicate inventory package path');
  need(new Set(packages.map(p => p.id)).size === packages.length, 'duplicate inventory package id');
  packages.sort((a, b) => b.absolute.length - a.absolute.length);
  const selected = packages.find(p => p.id === lane);
  need(selected && (selected.kind === 'typescript-package' || selected.kind === 'tooling'), 'lane is not a TS or tooling package');
  const owner = file => packages.find(p => within(file, p.absolute));
  need(Array.isArray(files) && files.length > 0, 'explicit source input list is required');
  const inputPaths = files.map(f => regularSource(root, f));
  need(new Set(inputPaths).size === inputPaths.length, 'duplicate source input');
  const inputs = new Set(inputPaths);
  for (const file of inputs) {
    need(owner(file)?.id === selected.id, 'input crosses selected package owner: ' + file);
    need(/\.(?:[cm]?[jt]sx?)$/.test(file), 'unsupported source extension: ' + file);
    need(!file.split(path.sep).includes('node_modules'), 'dependency files cannot be declared local inputs');
  }

  const configPath = regularSource(root, config);
  need(owner(configPath)?.id === selected.id, 'config crosses package owner');
  const observedConfigReads = new Map();
  const configHost = {
    ...ts.sys,
    readFile(file) {
      const raw = ts.sys.readFile(file);
      if (raw !== undefined) observedConfigReads.set(path.resolve(file), pin(file));
      return raw;
    },
    onUnRecoverableConfigFileDiagnostic(d) { throw new BoundaryError(diagnostic(ts, [d])); },
  };
  const parsed = ts.getParsedCommandLineOfConfigFile(configPath, {}, configHost);
  need(parsed && parsed.errors.length === 0, 'invalid TS config: ' + diagnostic(ts, parsed?.errors ?? []));
  need(!parsed.projectReferences?.length, 'project references require a separately selected build graph');
  need(!parsed.options.plugins?.length, 'compiler plugins are not selected by this checker');
  for (const file of observedConfigReads.keys()) {
    const physical = fs.realpathSync(file);
    need(physical.split(path.sep).includes('node_modules') || owner(physical)?.id === selected.id,
      'configuration reads another package or undeclared external input: ' + file);
  }
  for (const file of parsed.fileNames) need(inputs.has(path.resolve(file)), 'config source missing from declared inputs: ' + file);
  // Build scripts may be explicit additional roots outside tsconfig include.
  const options = { ...parsed.options, noEmit: true, allowJs: true, checkJs: false };
  const host = ts.createCompilerHost(options, true);
  const program = ts.createProgram(inputPaths, options, host);
  const syntactic = program.getSyntacticDiagnostics();
  need(syntactic.length === 0, 'source syntax is not supported: ' + diagnostic(ts, syntactic));

  const manifests = new Map();
  const localNames = new Map();
  for (const pkg of packages.filter(p => p.kind === 'typescript-package' || p.id === selected.id)) {
    const manifestPath = path.join(pkg.absolute, 'package.json');
    if (!fs.existsSync(manifestPath)) continue;
    const doc = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
    if (typeof doc.name === 'string') {
      need(!localNames.has(doc.name), 'duplicate local package name: ' + doc.name);
      localNames.set(doc.name, pkg.id);
    }
    manifests.set(pkg.id, { document: doc, path: manifestPath, ...pin(manifestPath) });
  }
  const manifest = manifests.get(selected.id);
  need(manifest, 'selected package manifest is required');
  const declaredExternal = new Set(['dependencies', 'devDependencies', 'peerDependencies', 'optionalDependencies']
    .flatMap(key => Object.keys(manifest.document[key] ?? {})));
  const edges = [];
  const refs = [];
  const relative = file => path.relative(root, file).split(path.sep).join('/');
  const runtimeBrowser = file => lane === 'report' && within(file, path.join(selected.absolute, 'src'));
  const importEdge = (source, literal, kind, forcedMode) => {
    need(literal && ts.isStringLiteralLike(literal), 'nonliteral module request in ' + relative(source.fileName));
    const specifier = literal.text;
    need(specifier.length > 0 && !specifier.includes('\0'), 'invalid module specifier');
    if (isBuiltin(specifier)) {
      need(!runtimeBrowser(source.fileName), 'browser source imports Node builtin: ' + specifier);
      edges.push({ from: relative(source.fileName), specifier, kind, destination: 'node-builtin' });
      return;
    }
    const mode = forcedMode ?? program.getModeForUsageLocation(source, literal);
    const resolved = ts.resolveModuleName(specifier, source.fileName, options, host, undefined, undefined, mode).resolvedModule;
    need(resolved, 'unresolved module request: ' + specifier + ' from ' + relative(source.fileName));
    const physical = fs.realpathSync(resolved.resolvedFileName);
    const local = within(physical, root) && !physical.split(path.sep).includes('node_modules');
    if (local) {
      const destination = owner(physical);
      need(destination, 'resolved local module has no owner: ' + physical);
      need(destination.id === selected.id || selected.dependencies.includes(destination.id), 'forbidden internal TS edge: ' + selected.id + ' -> ' + destination.id);
      need(destination.id === selected.id, 'cross-package source requires a separately selected immutable export');
      need(inputs.has(physical), 'resolved local module missing from declared inputs: ' + relative(physical));
      regularSource(root, relative(physical));
      edges.push({ from: relative(source.fileName), specifier, kind, destination: relative(physical), owner: destination.id });
    } else {
      need(!specifier.startsWith('.') && !path.isAbsolute(specifier), 'relative module escapes declared local sources');
      const name = packageName(specifier);
      need(!localNames.has(name), 'external dependency shadows a local package: ' + name);
      need(declaredExternal.has(name), 'external module is not declared by package: ' + name);
      need(physical.split(path.sep).includes('node_modules'), 'external module is outside materialized dependency tree');
      edges.push({ from: relative(source.fileName), specifier, kind, destination: physical, externalPackage: name, ...pin(physical) });
    }
  };

  for (const file of inputPaths) {
    const source = program.getSourceFile(file);
    need(source, 'compiler did not parse declared source: ' + file);
    for (const ref of source.referencedFiles) {
      const target = fs.realpathSync(path.resolve(path.dirname(file), ref.fileName));
      need(inputs.has(target) && owner(target)?.id === selected.id, 'triple-slash reference crosses declared source boundary');
      refs.push({ from: relative(file), kind: 'path-reference', destination: relative(target) });
    }
    for (const ref of source.typeReferenceDirectives) {
      need(!(runtimeBrowser(file) && ref.fileName === 'node'), 'browser source requests Node ambient types');
      const target = ts.resolveTypeReferenceDirective(ref.fileName, file, options, host).resolvedTypeReferenceDirective;
      need(target, 'unresolved type-reference: ' + ref.fileName);
      const physical = fs.realpathSync(target.resolvedFileName);
      need(physical.split(path.sep).includes('node_modules'), 'type-reference resolves to undeclared local source');
      const name = '@types/' + ref.fileName.replace(/^@/, '').replace('/', '__');
      need(declaredExternal.has(name) || declaredExternal.has(ref.fileName), 'ambient type dependency is not declared');
      refs.push({ from: relative(file), kind: 'type-reference', specifier: ref.fileName, destination: physical, ...pin(physical) });
    }
    for (const ref of source.libReferenceDirectives) refs.push({ from: relative(file), kind: 'compiler-library', specifier: ref.fileName });
    const visit = node => {
      if (ts.isImportDeclaration(node)) importEdge(source, node.moduleSpecifier, node.importClause?.isTypeOnly ? 'type-import' : 'import');
      else if (ts.isExportDeclaration(node) && node.moduleSpecifier) importEdge(source, node.moduleSpecifier, node.isTypeOnly ? 'type-export' : 'export');
      else if (ts.isImportEqualsDeclaration(node) && ts.isExternalModuleReference(node.moduleReference)) importEdge(source, node.moduleReference.expression, 'import-equals', ts.ModuleKind.CommonJS);
      else if (ts.isImportTypeNode(node)) {
        need(ts.isLiteralTypeNode(node.argument), 'nonliteral import type');
        importEdge(source, node.argument.literal, 'import-type');
      } else if (ts.isCallExpression(node)) {
        const callee = node.expression;
        if (callee.kind === ts.SyntaxKind.ImportKeyword) importEdge(source, node.arguments[0], 'dynamic-import', ts.ModuleKind.ESNext);
        else if (ts.isIdentifier(callee) && callee.text === 'require') importEdge(source, node.arguments[0], 'require', ts.ModuleKind.CommonJS);
        else if (ts.isPropertyAccessExpression(callee) && ts.isIdentifier(callee.expression) && callee.expression.text === 'require' && callee.name.text === 'resolve') importEdge(source, node.arguments[0], 'require-resolve', ts.ModuleKind.CommonJS);
        else if (ts.isPropertyAccessExpression(callee) && ts.isIdentifier(callee.expression) && callee.expression.text === 'module' && callee.name.text === 'require') importEdge(source, node.arguments[0], 'module-require', ts.ModuleKind.CommonJS);
        else if ((ts.isIdentifier(callee) && ['eval', 'Function'].includes(callee.text)) || (ts.isPropertyAccessExpression(callee) && callee.name.text === 'createRequire')) throw new BoundaryError('computed code/module loader requires explicit supported analysis');
      } else if (ts.isNewExpression(node) && ts.isIdentifier(node.expression) && node.expression.text === 'Function') {
        throw new BoundaryError('computed code requires explicit supported analysis');
      }
      if (ts.isElementAccessExpression(node) && ts.isIdentifier(node.expression) && ['module', 'require'].includes(node.expression.text)) {
        throw new BoundaryError('computed module loader access is not supported');
      }
      if ((ts.isImportSpecifier(node) && (node.propertyName ?? node.name).text === 'createRequire') ||
          (ts.isBindingElement(node) && (node.propertyName ?? node.name).text === 'createRequire') ||
          (ts.isPropertyAccessExpression(node) && node.name.text === 'createRequire')) {
        throw new BoundaryError('createRequire loader analysis is not selected');
      }
      if (ts.isIdentifier(node) && node.text === 'require') {
        const parent = node.parent;
        const direct = ts.isCallExpression(parent) && parent.expression === node;
        const calledProperty = ts.isPropertyAccessExpression(parent) && ts.isCallExpression(parent.parent) && parent.parent.expression === parent;
        const resolver = calledProperty && parent.expression === node && parent.name.text === 'resolve';
        const moduleMember = calledProperty && parent.name === node && ts.isIdentifier(parent.expression) && parent.expression.text === 'module';
        need(direct || resolver || moduleMember, 'require alias or computed loader is not supported');
      }
      ts.forEachChild(node, visit);
    };
    visit(source);
  }
  // Compiler-discovered local declarations/imports cannot hide outside the
  // explicit input list, even if a source-level edge spelling was overlooked.
  for (const source of program.getSourceFiles()) {
    const physical = fs.realpathSync(source.fileName);
    if (within(physical, root) && !physical.split(path.sep).includes('node_modules')) {
      need(inputs.has(physical), 'compiler discovered undeclared local input: ' + relative(physical));
    }
  }
  const order = (a, b) => Buffer.compare(Buffer.from(JSON.stringify(a)), Buffer.from(JSON.stringify(b)));
  return {
    schemaVersion: 1, passed: true, lane, compilerVersion: ts.version,
    inputs: inputPaths.map(file => ({ path: relative(file), ...pin(file) })).sort((a, b) => Buffer.compare(Buffer.from(a.path), Buffer.from(b.path))),
    configInputs: [...observedConfigReads].map(([file, value]) => ({ path: file, ...value })).sort(order),
    packageManifest: { path: relative(manifest.path), sha256: manifest.sha256, bytes: manifest.bytes },
    edges: edges.sort(order), references: refs.sort(order),
    sourcePurityQualified: false, dependencyClosureQualified: false,
    limits: ['Static declared-input graph, not runtime sandbox or arbitrary JavaScript effect analysis.',
      'External transitive dependency/script effects, asset reads and exact package closure are separate build-lane checks.',
      'No semantic type-check, compilation, browser or provider qualification.'],
  };
}

function main() {
  const values = {};
  for (let i = 2; i < process.argv.length; i += 2) {
    const key = process.argv[i];
    need(['--root', '--inventory', '--lane', '--config', '--files', '--typescript'].includes(key) && !Object.hasOwn(values, key) && process.argv[i + 1], 'invalid command arguments');
    values[key] = process.argv[i + 1];
  }
  for (const key of ['--root', '--inventory', '--lane', '--config', '--files', '--typescript']) need(values[key], 'missing ' + key);
  const result = check({ root: values['--root'], inventory: JSON.parse(fs.readFileSync(values['--inventory'], 'utf8')),
    lane: values['--lane'], config: values['--config'], files: JSON.parse(fs.readFileSync(values['--files'], 'utf8')), compiler: path.resolve(values['--typescript']) });
  process.stdout.write(JSON.stringify(result, null, 2) + '\n');
}
module.exports = { check, BoundaryError };
if (require.main === module) {
  try { main(); } catch (error) { process.stderr.write('TS boundary refused: ' + error.message + '\n'); process.exitCode = 1; }
}
