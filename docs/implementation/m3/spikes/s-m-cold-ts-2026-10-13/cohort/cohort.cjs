'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const ts=require(process.argv[2]), input=JSON.parse(fs.readFileSync(process.argv[3],'utf8'));
if(ts.version!=='6.0.3')throw Error('compiler version');
const root=input.virtualRoot,libs=path.dirname(process.argv[2]),data=new Map(),directories=new Map(),reads=new Set(),blocked=new Set();
function put(name,text){name=path.resolve(name);data.set(name,text);let cursor=name;while(cursor!==path.dirname(cursor)){let parent=path.dirname(cursor);if(!directories.has(parent))directories.set(parent,{files:new Set(),directories:new Set()});const bucket=directories.get(parent);if(cursor===name)bucket.files.add(path.basename(cursor));else bucket.directories.add(path.basename(cursor));cursor=parent;}}
for(const row of input.files){const raw=fs.readFileSync(row.sealed);if(raw.length!==row.bytes||crypto.createHash('sha256').update(raw).digest('hex')!==row.sha256)throw Error('sealed content differs');put(path.join(root,row.path),raw.toString('utf8'));}
for(const row of input.libraries){const raw=fs.readFileSync(row.path);if(raw.length!==row.bytes||crypto.createHash('sha256').update(raw).digest('hex')!==row.sha256)throw Error('library content differs');put(row.path,raw.toString('utf8'));}
const exists=p=>data.has(path.resolve(p));
const read=p=>{p=path.resolve(p);if(!data.has(p)){blocked.add(p);return undefined;}reads.add(p);return data.get(p);};
const getEntries=p=>{const d=directories.get(path.resolve(p));return d?{files:[...d.files].sort(),directories:[...d.directories].sort()}:{files:[],directories:[]};};
const readDirectory=(p,ext,excludes,includes,depth)=>ts.matchFiles(path.resolve(p),ext,excludes,includes,true,root,depth,getEntries,p=>path.resolve(p));
const configHost={useCaseSensitiveFileNames:true,fileExists:exists,readFile:read,readDirectory};
const results=[];
for(const rel of input.configurations){const calls=[];const timed=(name,fn)=>{const start=process.hrtime.bigint();const value=fn();calls.push({name,elapsedNanos:Number(process.hrtime.bigint()-start)});return value;};const config=path.join(root,rel);const started=process.hrtime.bigint();const configRead=timed('readConfigFile',()=>ts.readConfigFile(config,read));
 if(configRead.error){results.push({config:rel,standing:'incomplete',reason:'config-read-diagnostic',diagnosticCodes:[configRead.error.code],calls});continue;}
 const parsed=timed('parseJsonConfigFileContent',()=>ts.parseJsonConfigFileContent(configRead.config,configHost,path.dirname(config),{noEmit:true},config));
 if(!parsed.fileNames.length){results.push({config:rel,standing:'incomplete',reason:'no-configured-source-files',diagnosticCodes:parsed.errors.map(d=>d.code),projectReferences:parsed.projectReferences?.map(r=>r.path)||[],calls});continue;}
 const host=ts.createCompilerHost(parsed.options);host.readFile=read;host.fileExists=exists;host.directoryExists=p=>directories.has(path.resolve(p));host.getDirectories=p=>getEntries(p).directories.map(n=>path.join(p,n));host.readDirectory=readDirectory;host.realpath=p=>path.resolve(p);host.getCurrentDirectory=()=>root;host.writeFile=()=>{throw Error('emission forbidden');};
 const program=timed('createProgram',()=>ts.createProgram({rootNames:parsed.fileNames,options:parsed.options,projectReferences:parsed.projectReferences,host}));const diagnostics=[...parsed.errors,...timed('getOptionsDiagnostics',()=>program.getOptionsDiagnostics()),...timed('getGlobalDiagnostics',()=>program.getGlobalDiagnostics())];
 for(const file of program.getSourceFiles()){diagnostics.push(...timed('getSyntacticDiagnostics',()=>program.getSyntacticDiagnostics(file)),...timed('getSemanticDiagnostics',()=>program.getSemanticDiagnostics(file)));}
 const counts={};for(const d of diagnostics)counts[d.code]=(counts[d.code]||0)+1;
 results.push({config:rel,standing:diagnostics.length?'configured-pass-with-deficiencies':'configured-pass-completed',configuredFiles:parsed.fileNames.map(p=>path.relative(root,p)).sort(),programFiles:program.getSourceFiles().map(f=>f.fileName).sort(),projectReferences:parsed.projectReferences?.map(r=>r.path)||[],diagnosticCounts:counts,diagnosticsCount:diagnostics.length,calls,maxPublicCompilerCall:calls.reduce((a,b)=>a.elapsedNanos>=b.elapsedNanos?a:b,{name:'none',elapsedNanos:0}),elapsedNanos:Number(process.hrtime.bigint()-started)});
}
console.log(JSON.stringify({id:input.id,compilerVersion:ts.version,cohortSelection:'every retained regular basename matching /^tsconfig(?:\\..*)?\\.json$/',configurationCount:input.configurations.length,configurations:results,readPaths:[...reads].sort(),blockedPaths:[...blocked].sort(),repositoryOnly:true,dependencyTreePinned:false,fullWorkspaceSemanticsClaimed:false,nonregularSnapshotPolicySelected:false,repositoryCodeExecuted:false,emitPerformed:false}));
