// Narrow supplements for gaps dependency-cruiser options cannot express:
// declared-input census, config reads/include, explicit ambient types, parse
// failures and unsupported computed loaders. Uses TypeScript parse/config APIs
// only; module resolution stays with dependency-cruiser.
import fs from 'node:fs';
import path from 'node:path';
import ts from 'typescript';

export const typescriptVersion = ts.version;

function canonical(value) {
  return typeof value === 'string' && value.length > 0 && !value.includes('\\') && !value.includes('\0') &&
    !path.posix.isAbsolute(value) && !value.split('/').some(p => p === '' || p === '.' || p === '..');
}

function inputPathFindings(root, lane) {
  const findings = [];
  const seen = new Set();
  const grouped = lane.runtimeGroups.flatMap(g => g.files);
  for (const file of [...lane.inputs, lane.tsconfig, lane.manifest]) {
    if (!canonical(file)) { findings.push({ category: 'input-path', message: 'noncanonical path ' + file }); continue; }
    if (!file.startsWith(lane.packageRoot + '/') || file.split('/').includes('node_modules')) findings.push({ category: 'input-path', message: 'input outside lane package ' + file });
    let current = root;
    for (const part of file.split('/')) {
      current = path.join(current, part);
      const stat = fs.lstatSync(current, { throwIfNoEntry: false });
      if (!stat) { findings.push({ category: 'unresolved', message: 'declared input missing ' + file }); break; }
      if (stat.isSymbolicLink()) { findings.push({ category: 'symlink', message: 'symlink in declared input ' + file }); break; }
    }
  }
  for (const file of lane.inputs) {
    if (seen.has(file)) findings.push({ category: 'input-path', message: 'duplicate input ' + file });
    seen.add(file);
  }
  if (grouped.length !== seen.size || grouped.some(f => !seen.has(f))) findings.push({ category: 'input-path', message: 'runtime groups must partition declared inputs exactly' });
  return findings;
}

function configFindings(root, lane) {
  const findings = [];
  const packageDir = path.join(root, lane.packageRoot);
  const reads = new Set();
  const host = {
    ...ts.sys,
    readFile(file) { const raw = ts.sys.readFile(file); if (raw !== undefined) reads.add(path.resolve(file)); return raw; },
    onUnRecoverableConfigFileDiagnostic(d) { findings.push({ category: 'config-invalid', message: ts.flattenDiagnosticMessageText(d.messageText, '\n') }); },
  };
  const parsed = ts.getParsedCommandLineOfConfigFile(path.join(root, lane.tsconfig), {}, host);
  if (!parsed) return { findings, parsed };
  for (const d of parsed.errors) findings.push({ category: 'config-invalid', message: ts.flattenDiagnosticMessageText(d.messageText, '\n') });
  if (parsed.projectReferences?.length) findings.push({ category: 'config-invalid', message: 'project references are not selected' });
  if (parsed.options.plugins?.length) findings.push({ category: 'config-invalid', message: 'compiler plugins are not selected' });
  for (const file of reads) {
    const physical = fs.realpathSync(file);
    const relative = path.relative(packageDir, physical);
    if (!physical.split(path.sep).includes('node_modules') && (relative.startsWith('..') || path.isAbsolute(relative))) {
      findings.push({ category: 'config-owner', message: 'configuration reads outside lane package ' + path.relative(root, physical) });
    }
  }
  const inputs = new Set(lane.inputs.map(f => path.join(root, f)));
  for (const file of parsed.fileNames) if (!inputs.has(path.resolve(file))) findings.push({ category: 'config-include', message: 'tsconfig selects undeclared input ' + path.relative(root, file) });
  return { findings, parsed };
}

function ambientFindings(root, lane, parsed) {
  const findings = [];
  if (!parsed) return findings;
  const manifest = JSON.parse(fs.readFileSync(path.join(root, lane.manifest), 'utf8'));
  const declared = new Set(['dependencies', 'devDependencies', 'peerDependencies', 'optionalDependencies'].flatMap(k => Object.keys(manifest[k] ?? {})));
  const { types, typeRoots } = parsed.options;
  if (!Array.isArray(types)) findings.push({ category: 'ambient-types', message: 'compilerOptions.types must be explicit; automatic @types inclusion is an unrecorded input' });
  if (typeRoots !== undefined) findings.push({ category: 'ambient-types', message: 'compilerOptions.typeRoots is not selected' });
  for (const name of types ?? []) {
    const packageName = name.startsWith('@types/') ? name : '@types/' + name.replace(/^@/, '').replace('/', '__');
    if (!declared.has(packageName) && !declared.has(name)) findings.push({ category: 'ambient-types', message: 'ambient type package not declared ' + name });
    if (lane.browserRoots.length && (name === 'node' || name === '@types/node')) findings.push({ category: 'browser-node', message: 'browser lane selects Node ambient types' });
  }
  return findings;
}

const literal = node => !!node && (ts.isStringLiteral(node) || ts.isNoSubstitutionTemplateLiteral(node));
const calledWithLiteral = call => ts.isCallExpression(call) && call.arguments.length >= 1 && literal(call.arguments[0]);
const LOADER_OBJECTS = new Set(['require', 'module', 'globalThis', 'window', 'self', 'process']);

function loaderFindings(program, root, lane) {
  const findings = [];
  for (const file of lane.inputs) {
    const source = program.getSourceFile(path.join(root, file));
    if (!source) { findings.push({ category: 'parse-failure', message: 'not parsed ' + file }); continue; }
    const syntax = program.getSyntacticDiagnostics(source);
    if (syntax.length) findings.push({ category: 'parse-failure', message: file + ': ' + ts.flattenDiagnosticMessageText(syntax[0].messageText, '\n') });
    const refuse = (node, why) => findings.push({ category: 'unsupported-loader', message: `${file}:${source.getLineAndCharacterOfPosition(node.getStart(source)).line + 1} ${why}` });
    const visit = node => {
      if (ts.isCallExpression(node) && node.expression.kind === ts.SyntaxKind.ImportKeyword && !literal(node.arguments[0])) refuse(node, 'computed dynamic import');
      // Declaration/member names (e.g. a method called `require`) are not loader references.
      // So are member names on objects other than the known loader globals.
      const declarationName = ts.isIdentifier(node) && node.parent && !ts.isPropertyAccessExpression(node.parent) && node.parent.name === node;
      const ordinaryMember = ts.isIdentifier(node) && node.parent && ts.isPropertyAccessExpression(node.parent) && node.parent.name === node &&
        !(ts.isIdentifier(node.parent.expression) && LOADER_OBJECTS.has(node.parent.expression.text));
      if (ts.isIdentifier(node) && !declarationName && !ordinaryMember) {
        const parent = node.parent;
        if (node.text === 'require') {
          const direct = ts.isCallExpression(parent) && parent.expression === node && calledWithLiteral(parent);
          const member = ts.isPropertyAccessExpression(parent) && ts.isCallExpression(parent.parent) && parent.parent.expression === parent && calledWithLiteral(parent.parent);
          const resolve = member && parent.expression === node && parent.name.text === 'resolve';
          const moduleRequire = member && parent.name === node && ts.isIdentifier(parent.expression) && parent.expression.text === 'module';
          if (!(direct || resolve || moduleRequire)) refuse(node, 'require used as a value or with a computed request');
        } else if (['createRequire', 'eval'].includes(node.text) || (node.text === 'Function' && !ts.isTypeReferenceNode(parent))) {
          refuse(node, node.text + ' is an unsupported code/module loader');
        } else if (node.text === 'getBuiltinModule') {
          const member = ts.isPropertyAccessExpression(parent) && parent.name === node && ts.isCallExpression(parent.parent) && parent.parent.expression === parent;
          if (!member || !calledWithLiteral(parent.parent)) refuse(node, 'computed getBuiltinModule request');
        }
      }
      if (ts.isElementAccessExpression(node) && ts.isIdentifier(node.expression) && LOADER_OBJECTS.has(node.expression.text)) {
        refuse(node, 'computed member access on loader object ' + node.expression.text);
      }
      ts.forEachChild(node, visit);
    };
    visit(source);
  }
  return findings;
}

function censusFindings(lane, modules) {
  const inputs = new Set(lane.inputs);
  const findings = [];
  const seen = new Set();
  for (const m of modules) {
    const local = [m.source, ...m.dependencies.filter(d => !d.couldNotResolve && !d.coreModule).map(d => d.resolved)];
    for (const file of local) {
      if (file.startsWith('node_modules/') || inputs.has(file) || seen.has(file)) continue;
      seen.add(file);
      if (file.startsWith(lane.packageRoot + '/')) findings.push({ category: 'undeclared-local', message: 'graph reaches undeclared lane input ' + file });
    }
  }
  return findings;
}

export function supplementalFindings({ root, lane, modules }) {
  const findings = inputPathFindings(root, lane);
  if (findings.some(f => f.category === 'unresolved' || f.category === 'input-path')) return findings;
  const { findings: config, parsed } = configFindings(root, lane);
  findings.push(...config, ...ambientFindings(root, lane, parsed));
  const options = { ...(parsed?.options ?? {}), noResolve: true, noLib: true, types: [], allowJs: true, noEmit: true };
  // setParentNodes: the loader guard inspects parents of require/eval identifiers.
  const program = ts.createProgram(lane.inputs.map(f => path.join(root, f)), options, ts.createCompilerHost(options, true));
  findings.push(...loaderFindings(program, root, lane), ...censusFindings(lane, modules));
  return findings;
}
