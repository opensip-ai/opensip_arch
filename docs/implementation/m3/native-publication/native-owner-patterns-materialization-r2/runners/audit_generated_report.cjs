// Actual generated public report registry and exact output-delta controls.
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict'),crypto=require('node:crypto');
const tempRoot=require('node:child_process').execFileSync('/usr/bin/getconf',['DARWIN_USER_TEMP_DIR'],{encoding:'utf8'}).trim();
const privateTMPDIR=fs.mkdtempSync(path.join(tempRoot,'opensip-report-audit-'));fs.chmodSync(privateTMPDIR,0o700);process.env.TMPDIR=privateTMPDIR;
const F=__dirname,P='/Users/sb/code/opensip-ai/opensip',W=P+'-native-owner-patterns-takeover';
// The real isolated worktree has its own name rather than P's lexical suffix.
const candidate='/Users/sb/code/opensip-ai/opensip-native-owner-patterns-takeover';
const ts=require(path.join(P,'tools/contracts/node_modules/typescript'));
const rel='apps/report/src/generated/report.ts',before=fs.readFileSync(path.join(P,rel),'utf8'),after=fs.readFileSync(path.join(candidate,rel),'utf8');
function load(text){const c=ts.transpileModule(text,{compilerOptions:{target:ts.ScriptTarget.ES2022,module:ts.ModuleKind.CommonJS},reportDiagnostics:true});assert.equal(c.diagnostics.filter(d=>d.category===ts.DiagnosticCategory.Error).length,0);const m={exports:{}};new Function('exports','module',c.outputText)(m.exports,m);return m.exports;}
const old=load(before),now=load(after),reg=now.createReportShapeRegistry(),prior=old.createReportShapeRegistry();
const options=JSON.parse(fs.readFileSync(path.join(candidate,'tools/contracts/options.json'))),refs=options.entryPoints.map(r=>r.ref);
reg.checkEntryPoints(refs);assert.equal(refs.length,886);
let checks=0;
for(const ref of ['urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/CanonicalPath','opensip.product.occupancy-companion.1#/$defs/LogicalPath']){
 for(const value of ['a/..\n','a/..\r','a/..\u2028','a/..\u2029','src/a.ts','a\n/ok']){assert.equal(reg.matches(ref,value),true);checks++;}
 for(const value of ['.','..','a/.','a/..','a/../b','a\n/../b','a\r/../b','a\u2028/../b','a\u2029/../b']){assert.equal(reg.matches(ref,value),false);checks++;}
}
for(const ref of refs.filter(r=>r.endsWith('/LogicalPath')&&!r.startsWith('opensip.product.occupancy-companion.1#'))){
 for(const value of ['a/..\n','a/..\r','a/..\u2028','a/..\u2029','a\n/../b','src/a.ts','..']){assert.equal(reg.matches(ref,value),prior.matches(ref,value),ref+' '+JSON.stringify(value));checks++;}
}
assert.throws(()=>reg.matches('urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/TypeScriptUniverseV2ResolvedInputs/properties/jsRootFiles','a/..\n'),/unselected report schema entrypoint/);checks++;
const embedded=text=>text.match(/^const selectedSchemaBytes: string\[\] = (.*);$/m);
const raw=JSON.parse(embedded(after)[1]),map=JSON.parse(fs.readFileSync(path.join(candidate,'schemas/source-map.json')));
assert.equal(raw.length,43);
for(let i=0;i<raw.length;i++){assert.equal(raw[i],fs.readFileSync(path.join(candidate,map.sources[i].implementationPath),'utf8'));}
const runtime=root=>['exact-json.ts','patterns.ts','schema.ts'].map(n=>fs.readFileSync(path.join(root,'tools/contracts/runtime',n),'utf8').replace(/^import .*;\n/gm,'')).join('\n');
assert(after.includes(runtime(candidate)));assert(before.includes(runtime(P)));
let normalized=after.replace(runtime(candidate),runtime(P)).replace(embedded(after)[0],embedded(before)[0]);
normalized=normalized.replace(/^\/\/ Registry SHA-256: .*$/m,before.match(/^\/\/ Registry SHA-256: .*$/m)[0]).replace(/^\/\/ Generator closure SHA-256: .*$/m,before.match(/^\/\/ Generator closure SHA-256: .*$/m)[0]);
assert.equal(normalized,before,'unrelated generated report bytes changed');
const recipe=JSON.parse(fs.readFileSync(path.join(candidate,'schemas/registry.json'))).recipes[0],outputs=[];
for(const row of recipe.outputs){const a=fs.readFileSync(path.join(candidate,row.path)),b=fs.readFileSync(path.join(P,row.path));outputs.push({path:row.path,bytes:a.length,sha256:crypto.createHash('sha256').update(a).digest('hex'),changed:!a.equals(b)});}
assert.deepEqual(outputs.filter(r=>r.changed).map(r=>r.path),[rel]);
const report={standing:'EXACT GENERATED OUTPUT AUDIT AND ACTUAL PUBLIC REPORT SHAPE REGISTRY; NOT UNIT ACCEPTANCE',privateTMPDIR,TMPDIRMode:'0700',entrypoints:refs.length,registryChecks:checks,embeddedDocuments:raw.length,embeddedSourceBytesExact:true,exactHelperEmbedding:true,onlyReportChanges:['registry/closure provenance headers','exact selected runtime helpers','exact selected raw native schema bytes'],allUnrelatedReportBytesEqual:true,outputs,productQualification:false};
fs.writeFileSync(path.join(F,'generated-output-audit.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));
