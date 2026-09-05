// Reference provider and pure host rule over actual pinned TypeScript corpus.
// No product admission, Plan/Run identity, cache identity, or performance claim.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const args=process.argv.slice(2),arg=k=>args[args.indexOf(k)+1];
const base=__dirname, tsRoot=arg('--typescript-root'),tsPath=path.join(tsRoot,'lib/typescript.js');
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const ts=require(tsPath), prior=JSON.parse(fs.readFileSync(path.join(base,'native-corpus-report.v1.json')));
if(sha(fs.readFileSync(tsPath))!==prior.pins.compiler)throw Error('compiler pin mismatch');
const corpus=JSON.parse(fs.readFileSync(path.join(base,'quality-corpus-manifest.v1.json')));
const root=path.join(base,'quality-corpus.v1'), runs=JSON.parse(fs.readFileSync(arg('--input')));
// Pure host SCC evaluation never consults cache or provider-authored verdicts.
function evaluate(facts,coverage){
 if(coverage!=='complete')return {cycles:null,policyOutcome:null,indeterminate:true};
 const graph=new Map();for(const [a,b] of facts){if(!graph.has(a))graph.set(a,[]);if(!graph.has(b))graph.set(b,[]);graph.get(a).push(b);}
 let clock=0;const ix=new Map(),low=new Map(),stack=[],active=new Set(),groups=[];
 function visit(n){ix.set(n,clock);low.set(n,clock++);stack.push(n);active.add(n);
  for(const m of graph.get(n)){if(!ix.has(m)){visit(m);low.set(n,Math.min(low.get(n),low.get(m)));}else if(active.has(m))low.set(n,Math.min(low.get(n),ix.get(m)));}
  if(low.get(n)===ix.get(n)){const group=[];let m;do{m=stack.pop();active.delete(m);group.push(m);}while(m!==n);group.sort((a,b)=>Buffer.compare(Buffer.from(a),Buffer.from(b)));if(group.length>1||graph.get(n).includes(n))groups.push(group);}}
 for(const n of [...graph.keys()].sort())if(!ix.has(n))visit(n);
 groups.sort((a,b)=>Buffer.compare(Buffer.from(a[0]),Buffer.from(b[0])));
 return {cycles:groups,policyOutcome:groups.length?'fail':'pass',indeterminate:false};
}
const results=[];
for(const run of runs){
 const fixture=corpus.projects[run.project],files=fixture.files.map(p=>path.join(root,p)),allowed=new Set(files);
 const inputBefore=files.map(p=>[path.relative(root,p),sha(fs.readFileSync(p))]);
 const options={strict:true,noEmit:true,target:ts.ScriptTarget.ES2022,module:ts.ModuleKind.ESNext,moduleResolution:ts.ModuleResolutionKind.Bundler};
 // Every invocation gets a new compiler host/program. Its file access path has no
 // connection to durable analysis-cache bytes; cacheRoot is observation only.
 const host=ts.createCompilerHost(options),read=host.readFile.bind(host),reads=[];
 host.readFile=p=>{reads.push(p);return read(p);};
 const program=ts.createProgram(files,options,host),edges=[];let dynamic=false;
 const rel=p=>path.relative(root,p).split(path.sep).join('/');
 for(const file of program.getSourceFiles())if(allowed.has(file.fileName)){
  function visit(node){
   if(ts.isImportDeclaration(node)&&ts.isStringLiteral(node.moduleSpecifier)){
    const resolved=ts.resolveModuleName(node.moduleSpecifier.text,file.fileName,options,host).resolvedModule;
    if(resolved&&allowed.has(resolved.resolvedFileName))edges.push([rel(file.fileName),rel(resolved.resolvedFileName)]);
   }
   if(ts.isCallExpression(node)&&node.expression.kind===ts.SyntaxKind.ImportKeyword)dynamic=true;
   ts.forEachChild(node,visit);
  }visit(file);
 }
 const diagnostics=ts.getPreEmitDiagnostics(program).filter(d=>d.category===ts.DiagnosticCategory.Error).map(d=>d.code).sort((a,b)=>a-b);
 const coverage=dynamic||diagnostics.length?'unknown':'complete';
 const facts=[...new Map(edges.map(e=>[JSON.stringify(e),e])).values()].sort((a,b)=>Buffer.compare(Buffer.from(JSON.stringify(a)),Buffer.from(JSON.stringify(b))));
 const inputAfter=files.map(p=>[path.relative(root,p),sha(fs.readFileSync(p))]);
 if(JSON.stringify(inputBefore)!==JSON.stringify(inputAfter))throw Error('input changed');
 results.push({id:run.id,project:run.project,cacheState:run.cacheState,semantic:{facts,coverage,...evaluate(facts,coverage)},inputFileObservations:inputBefore,trace:{freshCompilerProgram:true,projectFilesRead:[...new Set(reads.filter(p=>allowed.has(p)).map(rel))].sort(),cacheReads:reads.filter(p=>p.startsWith(run.cacheRoot+path.sep)).length,sourceExecutionCount:0,providerFactComputations:1,hostEvaluations:1,durableResultRestores:0},diagnostics});
}
fs.writeFileSync(arg('--report'),JSON.stringify({compilerVersion:ts.version,compilerSha256:sha(fs.readFileSync(tsPath)),productQualification:false,results},null,2)+'\n');
