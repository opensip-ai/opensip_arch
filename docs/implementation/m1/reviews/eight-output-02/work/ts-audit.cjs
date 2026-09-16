// Review02 AST audit of the two rendered TS outputs (TypeScript 6.0.3 API, same as renderer).
const fs = require('node:fs');
const ts = require('/tmp/opensip-implementation/m1-typescript-api-trial-01/node_modules/typescript');
const W = __dirname, S = W + '/subject';
const targets = JSON.parse(fs.readFileSync(S + '/targets.json'));
const exportsJson = JSON.parse(fs.readFileSync(S + '/ts-exports.json'));
const projection = JSON.parse(fs.readFileSync(S + '/ts-projection.json'));
const tableNames = new Set(Object.values(targets));
const result = {};

function audit(label, file) {
  const text = fs.readFileSync(file, 'utf8');
  const sf = ts.createSourceFile(file, text, ts.ScriptTarget.ES2022, true, ts.ScriptKind.TS);
  const aliases = [], otherExports = [];
  const counts = {number: 0, any: 0, unknown: 0, object: 0, never: 0, numericLiteralType: 0, emptyTypeLiteral: 0, bigintLiteralType: 0, typeReferencesOutsideTable: new Set()};
  const neverSites = [];
  for (const st of sf.statements) {
    const exported = st.modifiers?.some(m => m.kind === ts.SyntaxKind.ExportKeyword);
    if (!exported) continue;
    if (ts.isTypeAliasDeclaration(st)) {
      const name = st.name.text;
      if (tableNames.has(name)) aliases.push(name); else otherExports.push('type ' + name);
      if (!tableNames.has(name)) continue;
      const visit = node => {
        switch (node.kind) {
          case ts.SyntaxKind.NumberKeyword: counts.number++; break;
          case ts.SyntaxKind.AnyKeyword: counts.any++; break;
          case ts.SyntaxKind.UnknownKeyword: counts.unknown++; break;
          case ts.SyntaxKind.ObjectKeyword: counts.object++; break;
          case ts.SyntaxKind.NeverKeyword: counts.never++; neverSites.push(name); break;
        }
        if (ts.isLiteralTypeNode(node)) {
          const lit = node.literal;
          if (ts.isNumericLiteral(lit) || (ts.isPrefixUnaryExpression(lit) && ts.isNumericLiteral(lit.operand))) counts.numericLiteralType++;
          if (ts.isBigIntLiteral(lit) || (ts.isPrefixUnaryExpression(lit) && ts.isBigIntLiteral(lit.operand))) counts.bigintLiteralType++;
        }
        if (ts.isTypeLiteralNode(node) && node.members.length === 0) counts.emptyTypeLiteral++;
        if (ts.isTypeReferenceNode(node)) {
          const ref = node.typeName.getText(sf);
          if (!tableNames.has(ref) && ref !== 'Json') counts.typeReferencesOutsideTable.add(ref);
        }
        ts.forEachChild(node, visit);
      };
      visit(st.type);
    } else {
      const kind = ts.SyntaxKind[st.kind];
      const name = st.name?.text ?? (st.declarationList?.declarations.map(d => d.name.getText(sf)).join(','));
      otherExports.push(kind + ' ' + name);
    }
  }
  counts.typeReferencesOutsideTable = [...counts.typeReferencesOutsideTable];
  const sorted = [...aliases].sort();
  return {aliases: aliases.length, aliasesSortedEqualDeclared: JSON.stringify(sorted) === JSON.stringify(aliases),
    duplicates: aliases.length - new Set(aliases).size, otherExports, counts, neverSites: [...new Set(neverSites)].slice(0, 20), names: aliases};
}

// Independent provider closure: every $ref anywhere in the projection node (not only renderer-visible refs).
function closure(roots, respectTsType) {
  const seen = new Set();
  const stack = [...roots];
  const refsIn = (node, out) => {
    if (node === null || typeof node !== 'object') return;
    if (respectTsType && !Array.isArray(node) && Object.hasOwn(node, 'tsType')) return;
    if (typeof node.$ref === 'string') out.push(node.$ref.slice('#/definitions/'.length));
    for (const [key, value] of Object.entries(node)) if (!key.startsWith('x-')) refsIn(value, out);
  };
  while (stack.length) {
    const name = stack.pop();
    if (seen.has(name)) continue;
    seen.add(name);
    const out = [];
    refsIn(projection.definitions[name], out);
    stack.push(...out);
  }
  return [...seen].sort();
}

const report = audit('report', S + '/output-e/apps/report/src/generated/report.ts');
const prov = audit('provider', S + '/output-e/providers/typescript/src/generated/protocol.ts');
const providerRoots = Object.entries(targets).filter(([ref]) => /^opensip\.product\.provider-(handshake|startup)\.1#\/\$defs\/TypeScript/.test(ref) || ref === 'opensip.product.fact-batch.3#').map(([, n]) => n);
const fullClosure = closure(providerRoots, false), visibleClosure = closure(providerRoots, true);
const provSet = new Set(prov.names);
result.report = {...report, names: undefined, equalsTable: JSON.stringify([...report.names].sort()) === JSON.stringify([...tableNames].sort()), equalsTsExports: JSON.stringify(report.names) === JSON.stringify(exportsJson.report)};
result.provider = {...prov, names: undefined, roots: providerRoots.length, rootsExported: providerRoots.every(n => provSet.has(n)),
  equalsTsExports: JSON.stringify(prov.names) === JSON.stringify(exportsJson.provider),
  allNamesInTable: prov.names.every(n => tableNames.has(n)),
  equalsVisibleRefClosure: JSON.stringify(visibleClosure) === JSON.stringify([...prov.names].sort()),
  fullRefClosureMinusExports: fullClosure.filter(n => !provSet.has(n)), exportsMinusFullClosure: prov.names.filter(n => !fullClosure.includes(n))};
// Runtime block and header checks.
const rt = '/tmp/opensip-implementation/m1-ts-runtime-subject-02/';
const runtimeText = ['exact-json.ts', 'patterns.ts', 'schema.ts'].map(n => fs.readFileSync(rt + n, 'utf8').replace(/^import .*;\n/gm, '')).join('\n');
const reportText = fs.readFileSync(S + '/output-e/apps/report/src/generated/report.ts', 'utf8');
result.report.runtimeBlockVerbatim = reportText.includes(runtimeText);
const providerText = fs.readFileSync(S + '/output-e/providers/typescript/src/generated/protocol.ts', 'utf8');
result.provider.jsonHeader = providerText.split('\n')[1];
// Projection-side exactness: every integer-bearing node the renderer can see carries a tsType; numbers never parsed by JS.
let intNoTs = [], floatLiterals = 0;
(function scan(node, path) {
  if (node === null || typeof node !== 'object') { if (typeof node === 'number' && !Number.isInteger(node)) floatLiterals++; return; }
  if (Array.isArray(node)) return node.forEach((x, i) => scan(x, path + '/' + i));
  const types = Array.isArray(node.type) ? node.type : [node.type];
  if (types.includes('integer') && !Object.hasOwn(node, 'tsType')) intNoTs.push(path);
  if ((Object.hasOwn(node, 'const') && typeof node.const !== 'string' && node.const !== null && typeof node.const !== 'boolean' || (node.enum || []).some(v => typeof v === 'number' || (v && typeof v === 'object'))) && !Object.hasOwn(node, 'tsType')) intNoTs.push('literal:' + path);
  for (const [k, v] of Object.entries(node)) if (!k.startsWith('x-') && k !== 'tsType') scan(v, path + '/' + k);
})(projection.definitions, '#/definitions');
result.projection = {integerOrNumericLiteralNodesWithoutTsType: intNoTs.slice(0, 20), count: intNoTs.length, nonIntegerNumbers: floatLiterals};
fs.writeFileSync(W + '/logs/ts-audit.json', JSON.stringify(result, null, 1) + '\n');
console.log(JSON.stringify(result, null, 1));
