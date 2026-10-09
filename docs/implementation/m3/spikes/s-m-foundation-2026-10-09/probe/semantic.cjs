'use strict';
const fs=require('node:fs'), path=require('node:path');
const ts=require(process.argv[2]);
const root=fs.realpathSync(process.argv[3]), libs=fs.realpathSync(path.dirname(process.argv[2]));
const readPaths=new Set(), blockedPaths=new Set(), calls=[];
const under=(p,r)=>p===r||p.startsWith(r+path.sep);
function permitted(p){
 const absolute=path.resolve(p);
 if (!under(absolute,root)&&!under(absolute,libs)) return false;
 try {const real=fs.realpathSync(absolute);return under(real,root)||under(real,libs);} catch {return false;}
}
const readFile=p=>{if(!permitted(p)){blockedPaths.add(path.resolve(p));return undefined;}readPaths.add(path.resolve(p));return ts.sys.readFile(p);};
const fileExists=p=>permitted(p)&&ts.sys.fileExists(p);
function timed(label,fn){const start=process.hrtime.bigint();const value=fn();calls.push({label,elapsedNanos:Number(process.hrtime.bigint()-start)});return value;}
const config=path.join(root,'tsconfig.json');
if(!fileExists(config)) {console.log(JSON.stringify({standing:'incomplete',reason:'root-tsconfig-absent',root,compilerVersion:ts.version}));process.exit(2);}
const configRead=timed('readConfigFile',()=>ts.readConfigFile(config,readFile));
if(configRead.error){console.log(JSON.stringify({standing:'incomplete',reason:'root-tsconfig-unreadable',code:configRead.error.code}));process.exit(2);}
const configHost={useCaseSensitiveFileNames:true,fileExists,readFile,readDirectory:(dir,extensions,excludes,includes,depth)=>{
 if(!permitted(dir)) return [];
 return ts.sys.readDirectory(dir,extensions,excludes,includes,depth).filter(permitted);
 }};
const parsed=timed('parseJsonConfigFileContent',()=>ts.parseJsonConfigFileContent(configRead.config,configHost,root,{noEmit:true},config));
if(!parsed.fileNames.length){console.log(JSON.stringify({standing:'incomplete',reason:'no-configured-source-files',configDiagnostics:parsed.errors.map(d=>d.code)}));process.exit(2);}
const host=ts.createCompilerHost(parsed.options);
host.readFile=readFile;host.fileExists=fileExists;host.directoryExists=p=>permitted(p)&&ts.sys.directoryExists(p);
host.realpath=p=>permitted(p)?fs.realpathSync(p):p;
host.writeFile=()=>{throw new Error('emission-forbidden');};
const program=timed('createProgram',()=>ts.createProgram({rootNames:parsed.fileNames,options:parsed.options,projectReferences:parsed.projectReferences,host}));
const diagnostics=[...parsed.errors];
diagnostics.push(...timed('getOptionsDiagnostics',()=>program.getOptionsDiagnostics()));
diagnostics.push(...timed('getGlobalDiagnostics',()=>program.getGlobalDiagnostics()));
for(const file of program.getSourceFiles()){
 diagnostics.push(...timed('getSyntacticDiagnostics:'+file.fileName,()=>program.getSyntacticDiagnostics(file)));
 diagnostics.push(...timed('getSemanticDiagnostics:'+file.fileName,()=>program.getSemanticDiagnostics(file)));
}
const counts={};for(const d of diagnostics)counts[d.code]=(counts[d.code]||0)+1;
const maxCall=calls.reduce((a,b)=>a.elapsedNanos>b.elapsedNanos?a:b,{label:'none',elapsedNanos:0});
console.log(JSON.stringify({standing:diagnostics.length||blockedPaths.size?'semantic-pass-with-deficiencies':'semantic-pass-completed',compilerVersion:ts.version,root,config,configuredFiles:parsed.fileNames.length,programFiles:program.getSourceFiles().length,projectReferences:parsed.projectReferences?.length||0,diagnosticCounts:counts,diagnosticsCount:diagnostics.length,repositoryOnly:true,nodeModulesPinned:false,readPaths:[...readPaths].sort(),blockedPaths:[...blockedPaths].sort(),calls,maxPublicCompilerCall:maxCall,totalInstrumentedNanos:calls.reduce((s,c)=>s+c.elapsedNanos,0),fullWorkspaceSemanticsClaimed:false,emitPerformed:false,repositoryCodeExecuted:false}));
