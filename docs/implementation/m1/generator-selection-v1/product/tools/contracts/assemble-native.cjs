// Integration adapter: inert native types in the existing two TS output files.
const fs = require('node:fs');
const path = require('node:path');
const H = __dirname;
const GEN = H;
const ts = require('./node_modules/typescript');
const {renderTypes} = require('./render-types.cjs');
const [base, native, output, prepared] = process.argv.slice(2);
if (!base || !native || !output || !prepared || process.argv.length!==6) throw Error('four roots required');
const raw=fs.readFileSync(path.join(native,'wire.ts'),'utf8');
const ast=ts.createSourceFile('native.ts',raw,ts.ScriptTarget.ES2022,true,ts.ScriptKind.TS);
if(ast.parseDiagnostics.length)throw Error('native syntax');
const declarations=new Map();
for(const s of ast.statements){
 if(ts.isImportDeclaration(s))continue;
 if(!(ts.isTypeAliasDeclaration(s)||ts.isInterfaceDeclaration(s)))throw Error('native executable or unselected declaration');
 if(declarations.has(s.name.text))throw Error('duplicate native declaration');
 declarations.set(s.name.text,s);
}
const externs=new Set(Object.values(JSON.parse(fs.readFileSync(path.join(native,'render-result.json'))).externalTypes));
const builtins=new Set(['ReadonlyArray','Uint8Array']);
function closure(seeds){
 const selected=new Set(), external=new Set();
 function visit(name){
  if(selected.has(name)||builtins.has(name))return;
  if(externs.has(name)){external.add(name);return;}
  const s=declarations.get(name);if(!s)throw Error('unresolved native type '+name);
  selected.add(name);
  function walk(n){if(ts.isTypeReferenceNode(n)){if(!ts.isIdentifier(n.typeName))throw Error('qualified native type');visit(n.typeName.text);}ts.forEachChild(n,walk);}
  walk(s);
 }
 seeds.forEach(visit);
 return {selected,external};
}
const printer=ts.createPrinter({newLine:ts.NewLineKind.LineFeed});
function textOf(c){return [...declarations].filter(([n])=>c.selected.has(n)).map(([,s])=>printer.printNode(ts.EmitHint.Unspecified,s,ast)).join('\n')+'\n';}
function topNames(text){const parsed=ts.createSourceFile('prior.ts',text,ts.ScriptTarget.ES2022,true,ts.ScriptKind.TS);if(parsed.parseDiagnostics.length)throw Error('prior syntax');return new Set(parsed.statements.filter(s=>s.name&&ts.isIdentifier(s.name)).map(s=>s.name.text));}
function disjoint(text,names){const old=topNames(text);for(const n of names)if(old.has(n))throw Error('native name collision '+n);}
const options=JSON.parse(fs.readFileSync(path.join(prepared,'options.json')));
const projection=JSON.parse(fs.readFileSync(path.join(prepared,'ts-projection.json')));
const names=new Map(options.entryPoints.map(r=>[r.ref,r.typeName]));
const provider=closure([...declarations.keys()].filter(n=>n.startsWith('Ts2')));
const providerBase=renderTypes(projection,[...options.providerEntryPoints.map(r=>names.get(r)),...provider.external]);
const providerText='export type Json = null | boolean | bigint | string | Json[] | {[key:string]:Json};\n'+providerBase.text;
disjoint(providerText,provider.selected);
const all=closure([...declarations.keys()]);
const reportPath='apps/report/src/generated/report.ts', providerPath='providers/typescript/src/generated/protocol.ts';
const reportText=fs.readFileSync(path.join(base,reportPath),'utf8');
disjoint(reportText,all.selected);
const reportNames=topNames(reportText);for(const n of all.external)if(!reportNames.has(n))throw Error('report extern absent '+n);
const header='// Native integration reference; exact source pins in assembly receipt. Inert types only.\n';
for(const [rel,text] of [[providerPath,header+providerText+textOf(provider)],[reportPath,reportText+'\n'+header+textOf(all)]]){
 const p=path.join(output,rel);fs.mkdirSync(path.dirname(p),{recursive:true});fs.writeFileSync(p,text);
}
fs.writeFileSync(path.join(output,'../typescript-assembly.json'),JSON.stringify({providerNative:[...provider.selected].sort(),providerExternal:[...provider.external].sort(),providerSchemaTypes:providerBase.names.length,reportNative:[...all.selected].sort(),reportExternal:[...all.external].sort(),standing:'Inert types and closed generated external closure only'},null,2)+'\n');
console.log(JSON.stringify({providerNative:provider.selected.size,providerExternal:provider.external.size,reportNative:all.selected.size}));
