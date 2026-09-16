// Module-request extraction from TypeScript's parser. Build usages feed the
// TypeScript resolver; runtime usages come from JavaScript text (emitted by
// TypeScript for own TS sources, or materialized files) and feed Node or the
// declared browser resolver. Extraction never resolves or executes anything.
import ts from 'typescript';

const literal = node => !!node && (ts.isStringLiteral(node) || ts.isNoSubstitutionTemplateLiteral(node));
const isIdent = (node, text) => !!node && ts.isIdentifier(node) && node.text === text;
const member = (node, object, name) => !!node && ts.isPropertyAccessExpression(node) && isIdent(node.expression, object) && node.name.text === name;

export const scriptKindFor = file => /\.tsx$/.test(file) ? ts.ScriptKind.TSX
  : /\.(?:d\.)?[cm]?ts$/.test(file) ? ts.ScriptKind.TS
  : /\.jsx$/.test(file) ? ts.ScriptKind.JSX
  : /\.json$/.test(file) ? ts.ScriptKind.JSON : ts.ScriptKind.JS;

export function parse(fileName, text, scriptKind = scriptKindFor(fileName)) {
  return ts.createSourceFile(fileName, text, ts.ScriptTarget.Latest, true, scriptKind);
}

export function where(sf, node) {
  const { line, character } = sf.getLineAndCharacterOfPosition(node.getStart(sf));
  return { line: line + 1, column: character + 1 };
}

function guardedByTry(node) {
  for (let current = node; current.parent; current = current.parent) {
    if (ts.isFunctionLike(current)) return false;
    if (ts.isTryStatement(current.parent) && current.parent.tryBlock === current) return true;
  }
  return false;
}

const hasExportModifier = statement => ts.canHaveModifiers(statement) && (ts.getModifiers(statement) ?? []).some(m => m.kind === ts.SyntaxKind.ExportKeyword);

export function runtimeUsages(sf) {
  const requests = [];
  const loaders = [];
  const unsupported = [];
  const assets = [];
  let esmSyntax = sf.statements.some(s => ts.isImportDeclaration(s) || ts.isExportDeclaration(s) || ts.isExportAssignment(s) || hasExportModifier(s));
  let requireCalls = false;
  let declaresRequire = false;
  const add = (list, node, extra) => list.push({ ...where(sf, node), text: node.getText(sf), guarded: guardedByTry(node), ...extra });
  const callOf = node => node.parent && ts.isCallExpression(node.parent) && node.parent.expression === node;

  const visit = node => {
    if (ts.isImportDeclaration(node)) {
      if (!node.importClause?.isTypeOnly) {
        if (literal(node.moduleSpecifier)) add(requests, node.moduleSpecifier, { kind: 'import', mode: 'import', request: node.moduleSpecifier.text });
        else add(loaders, node, { kind: 'computed-import' });
      }
    } else if (ts.isExportDeclaration(node) && node.moduleSpecifier && !node.isTypeOnly && literal(node.moduleSpecifier)) {
      add(requests, node.moduleSpecifier, { kind: 'export', mode: 'import', request: node.moduleSpecifier.text });
    } else if (ts.isMetaProperty(node) && node.keywordToken === ts.SyntaxKind.ImportKeyword) {
      esmSyntax = true;
    } else if (ts.isAwaitExpression(node) && !ts.findAncestor(node.parent, ts.isFunctionLike)) {
      esmSyntax = true;
    } else if (ts.isCallExpression(node)) {
      const callee = node.expression;
      const [first] = node.arguments;
      if (callee.kind === ts.SyntaxKind.ImportKeyword) {
        if (literal(first)) add(requests, first, { kind: 'dynamic-import', mode: 'import', request: first.text });
        else add(loaders, node, { kind: 'computed-import' });
      } else if (isIdent(callee, 'require') && first && ts.isArrayLiteralExpression(first)) {
        add(unsupported, node, { kind: 'amd-require' });
      } else if (isIdent(callee, 'require')) {
        requireCalls = true;
        if (literal(first)) add(requests, first, { kind: 'require', mode: 'require', request: first.text });
        else add(loaders, node, { kind: 'computed-require' });
      } else if (member(callee, 'require', 'resolve') || member(callee, 'module', 'require')) {
        requireCalls = true;
        const kind = callee.name.text === 'resolve' ? 'require-resolve' : 'module-require';
        if (literal(first)) add(requests, first, { kind, mode: 'require', request: first.text });
        else add(loaders, node, { kind: 'computed-require' });
      } else if (ts.isPropertyAccessExpression(callee) && callee.name.text === 'getBuiltinModule' &&
        (isIdent(callee.expression, 'process') || member(callee.expression, 'globalThis', 'process'))) {
        if (literal(first)) add(requests, first, { kind: 'get-builtin-module', mode: 'require', request: first.text, builtinOnly: true });
        else add(loaders, node, { kind: 'computed-builtin' });
      } else if (isIdent(callee, 'define')) {
        // AMD's omitted dependency array injects require as the first factory
        // argument, regardless of parameter spelling or function syntax. Only
        // the explicit exports/module-only form has no injected loader. A
        // literal module ID does not change the dependency array's meaning.
        const args = literal(node.arguments[0]) ? node.arguments.slice(1) : [...node.arguments];
        const [dependencies, factory] = args;
        const localExportsOnly = args.length === 2 && ts.isArrayLiteralExpression(dependencies) && dependencies.elements.length > 0 && dependencies.elements.every(item => literal(item) && ['exports', 'module'].includes(item.text)) && !!factory && (ts.isIdentifier(factory) || ts.isFunctionExpression(factory) || ts.isArrowFunction(factory));
        add(unsupported, node, { kind: 'amd-define', localExportsOnly });
      } else if (isIdent(callee, 'createRequire') || (ts.isPropertyAccessExpression(callee) && callee.name.text === 'createRequire')) {
        add(loaders, node, { kind: 'create-require' });
      } else if (isIdent(callee, 'eval') || isIdent(callee, 'Function')) {
        add(loaders, node, { kind: 'eval', declaredInputsOnly: true });
      }
    } else if (ts.isNewExpression(node)) {
      const [first, second] = node.arguments ?? [];
      if (isIdent(node.expression, 'Function')) {
        add(loaders, node, { kind: 'eval', declaredInputsOnly: true });
      } else if (isIdent(node.expression, 'URL') && second && ts.isPropertyAccessExpression(second) && ts.isMetaProperty(second.expression) && second.name.text === 'url') {
        if (literal(first)) add(assets, first, { kind: 'asset-url', request: first.text });
        else add(loaders, node, { kind: 'computed-asset-url' });
      } else if ((isIdent(node.expression, 'Worker') || isIdent(node.expression, 'SharedWorker')) && literal(first)) {
        add(assets, first, { kind: 'worker-path', request: first.text });
      }
    } else if (ts.isElementAccessExpression(node) && (isIdent(node.expression, 'require') || isIdent(node.expression, 'module'))) {
      add(loaders, node, { kind: 'computed-member' });
    }

    if (ts.isIdentifier(node) && node.text === 'require') {
      const p = node.parent;
      const declaration = (ts.isVariableDeclaration(p) || ts.isParameter(p) || ts.isFunctionDeclaration(p) || ts.isBindingElement(p)) && p.name === node;
      if (declaration) declaresRequire = true;
      const propertyName = (ts.isPropertyAccessExpression(p) || ts.isPropertyAssignment(p) || ts.isMethodDeclaration(p) || ts.isPropertyDeclaration(p) ||
        ts.isPropertySignature(p) || ts.isMethodSignature(p) || ts.isQualifiedName(p)) && p.name === node;
      const memberRead = ts.isPropertyAccessExpression(p) && p.expression === node &&
        (['main', 'cache', 'extensions'].includes(p.name.text) || (p.name.text === 'resolve' && callOf(p)));
      const allowed = declaration || propertyName || memberRead || callOf(node) || ts.isTypeOfExpression(p) || ts.isArrayLiteralExpression(p) && p.parent && ts.isCallExpression(p.parent) && isIdent(p.parent.expression, 'define');
      const unCalledModuleRequire = ts.isPropertyAccessExpression(p) && p.name === node && isIdent(p.expression, 'module') && !callOf(p);
      if (!allowed || unCalledModuleRequire) add(loaders, node, { kind: 'require-alias' });
    }
    ts.forEachChild(node, visit);
  };
  visit(sf);
  return { requests, loaders, unsupported, assets, esmSyntax, requireCalls, declaresRequire };
}

// Requests TypeScript resolves when building a program for this file.
export function buildUsages(sf) {
  const usages = [];
  const js = /\.[cm]?jsx?$/.test(sf.fileName);
  const isModuleFile = sf.statements.some(s => ts.isImportDeclaration(s) || ts.isExportDeclaration(s) || ts.isExportAssignment(s) || ts.isImportEqualsDeclaration(s) || hasExportModifier(s));
  const add = (node, kind, typeOnly) => usages.push({ node, kind, request: node.text, typeOnly, ...where(sf, node) });
  const visitDoc = node => {
    if (ts.isImportTypeNode(node) && ts.isLiteralTypeNode(node.argument) && literal(node.argument.literal)) add(node.argument.literal, 'jsdoc-import-type', true);
    else if (ts.isJSDocImportTag && ts.isJSDocImportTag(node) && literal(node.moduleSpecifier)) add(node.moduleSpecifier, 'jsdoc-import-tag', true);
    ts.forEachChild(node, visitDoc);
  };
  const visit = node => {
    if (ts.isImportDeclaration(node) && literal(node.moduleSpecifier)) add(node.moduleSpecifier, 'import', !!node.importClause?.isTypeOnly);
    else if (ts.isExportDeclaration(node) && node.moduleSpecifier && literal(node.moduleSpecifier)) add(node.moduleSpecifier, 'export', node.isTypeOnly);
    else if (ts.isImportEqualsDeclaration(node) && ts.isExternalModuleReference(node.moduleReference) && literal(node.moduleReference.expression)) add(node.moduleReference.expression, 'import-equals', node.isTypeOnly);
    else if (ts.isImportTypeNode(node) && ts.isLiteralTypeNode(node.argument) && literal(node.argument.literal)) add(node.argument.literal, 'import-type', true);
    else if (ts.isCallExpression(node) && node.expression.kind === ts.SyntaxKind.ImportKeyword && literal(node.arguments[0])) add(node.arguments[0], 'dynamic-import', false);
    else if (js && ts.isCallExpression(node) && isIdent(node.expression, 'require') && node.arguments.length === 1 && literal(node.arguments[0])) add(node.arguments[0], 'require', false);
    else if (ts.isModuleDeclaration(node) && ts.isStringLiteral(node.name) && isModuleFile) add(node.name, 'augmentation', true);
    if (js) for (const tag of ts.getJSDocTags(node)) visitDoc(tag);
    ts.forEachChild(node, visit);
  };
  visit(sf);
  return usages;
}
