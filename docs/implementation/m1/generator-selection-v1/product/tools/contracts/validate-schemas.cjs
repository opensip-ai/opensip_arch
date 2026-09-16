// Use the exact selected runtime's vocabulary and operand checks before any
// carrier projection. No duplicate keyword list can silently diverge.
const fs=require('node:fs');
const path=require('node:path');
const ts=require('typescript');
const [input,scratch]=process.argv.slice(2);
if (!input || !scratch || process.argv.length!==4) throw new Error('input and scratch roots required');
fs.mkdirSync(scratch,{recursive:true});
const source=['exact-json.ts','patterns.ts','schema.ts'].map(name=>fs.readFileSync(path.join(__dirname,'runtime',name),'utf8').replace(/^import .*;\n/gm,'')).join('\n');
const compilation=ts.transpileModule(source,{compilerOptions:{target:ts.ScriptTarget.ES2022,module:ts.ModuleKind.CommonJS},reportDiagnostics:true});
if (compilation.diagnostics?.some(d=>d.category===ts.DiagnosticCategory.Error)) throw new Error('selected runtime compilation failed');
const file=path.join(scratch,'schema-runtime.cjs');fs.writeFileSync(file,compilation.outputText);
const runtime=require(file);
const originals=JSON.parse(fs.readFileSync(path.join(input,'raw-schemas.json'),'utf8'));
const options=JSON.parse(fs.readFileSync(path.join(input,'options.json'),'utf8'));
const registry=new runtime.SchemaRegistry(originals.map(raw=>runtime.parseExact(new TextEncoder().encode(raw))));
registry.checkEntryPoints(options.entryPoints.map(row=>row.ref));
console.log(JSON.stringify({checkedOriginalSchemaEntryPoints:options.entryPoints.length}));
