// Deterministic inert type renderer. Full admission uses the original schemas.
// Every exported carrier name comes from the explicit selected target table.
const ts = require('typescript');
const json = JSON.stringify;

function renderTypes(schema, selectedNames) {
  const definitions = schema.definitions;
  const selected = new Set();
  const scalar = {null:'null', boolean:'boolean', integer:'bigint', string:'string'};
  function visit(name) {
    if (selected.has(name)) return;
    if (!Object.hasOwn(definitions, name)) throw new Error('missing named schema: '+name);
    selected.add(name);
    expression(definitions[name]);
  }
  function expression(node) {
    if (node === true) return 'Json';
    if (node === false) return 'never';
    // Exact literals and integer unions are produced by the Python projection,
    // before any JS number parsing. Never reconstruct numeric literals here.
    if (Object.hasOwn(node, 'tsType')) return '('+node.tsType+')';
    const constraints = [];
    if (node.$ref !== undefined) {
      const prefix = '#/definitions/';
      if (typeof node.$ref !== 'string' || !node.$ref.startsWith(prefix)) throw new Error('unflattened reference');
      const name = node.$ref.slice(prefix.length);
      visit(name);
      constraints.push(name);
    }
    if (node.enum !== undefined) {
      if (node.enum.some(v=>typeof v==='number')) throw new Error('numeric enum without exact literal projection');
      constraints.push('('+node.enum.map(v=>json(v)).join(' | ')+')');
    }
    if (node.const !== undefined) throw new Error('const without exact literal projection');
    if (node.type !== undefined) {
      const types = Array.isArray(node.type) ? node.type : [node.type];
      constraints.push('('+types.map(kind=>{
        if (Object.hasOwn(scalar,kind)) return scalar[kind];
        if (kind==='array') return '('+expression(node.items === undefined ? true : node.items)+')[]';
        if (kind!=='object') throw new Error('unsupported carrier type: '+kind);
        const fields = [];
        const properties = node.properties || {};
        const required = new Set(node.required || []);
        for (const key of Object.keys(properties).sort()) {
          fields.push(json(key)+(required.has(key)?'':'?')+': '+expression(properties[key])+';');
        }
        for (const key of [...required].sort()) {
          if (!Object.hasOwn(properties,key)) fields.push(json(key)+': Json;');
        }
        // Pattern/extra-key restrictions remain runtime constraints. Combining
        // a typed index with fixed fields can wrongly narrow those fixed fields;
        // use Json for the index when both coexist, retaining each named field.
        const patterns = Object.values(node.patternProperties || {});
        let index;
        if (node.additionalProperties !== false) index = node.additionalProperties === undefined ? 'Json' : expression(node.additionalProperties);
        if (patterns.length) index = [index, ...patterns.map(expression)].filter(Boolean).join(' | ');
        if (index) fields.push('[key: string]: '+(fields.length?'Json | undefined':index)+';');
        return '{'+fields.join('\n')+'}';
      }).join(' | ')+')');
    }
    for (const keyword of ['allOf','anyOf','oneOf']) {
      if (node[keyword] !== undefined) {
        const parts = node[keyword].map(expression);
        constraints.push('('+parts.join(keyword==='allOf'?' & ':' | ')+')');
      }
    }
    // Implicit-type constraint nodes (contains/pattern/if/not/required, etc.)
    // may also admit values of other JSON types. They cannot narrow the inert
    // type by inference. Explicit type/ref/applicator constraints above suffice.
    return constraints.length ? constraints.join(' & ') : 'Json';
  }
  for (const name of selectedNames) visit(name);
  const names = [...selected].sort();
  const source = names.map(name=>'export type '+name+' = '+expression(definitions[name])+';').join('\n');
  if (selected.size !== names.length) throw new Error('late reference discovery');
  const ast = ts.createSourceFile('carriers.ts', source, ts.ScriptTarget.ES2022, true, ts.ScriptKind.TS);
  if (ast.parseDiagnostics.length) throw new Error('generated type syntax refused');
  let numberTypes = 0, anyTypes = 0;
  function audit(node) {
    if (node.kind === ts.SyntaxKind.NumberKeyword) numberTypes++;
    if (node.kind === ts.SyntaxKind.AnyKeyword) anyTypes++;
    ts.forEachChild(node, audit);
  }
  audit(ast);
  if (numberTypes || anyTypes) throw new Error('inexact numeric or any carrier type');
  const exports = ast.statements.map(item=>{
    if (!ts.isTypeAliasDeclaration(item) || !item.modifiers?.some(m=>m.kind===ts.SyntaxKind.ExportKeyword)) throw new Error('unexpected generated declaration');
    return item.name.text;
  });
  if (json(exports)!==json(names)) throw new Error('carrier export set differs from selected name table');
  const text = ts.createPrinter({newLine:ts.NewLineKind.LineFeed}).printFile(ast);
  return {text, names, numberTypes, anyTypes};
}
module.exports = {renderTypes};
