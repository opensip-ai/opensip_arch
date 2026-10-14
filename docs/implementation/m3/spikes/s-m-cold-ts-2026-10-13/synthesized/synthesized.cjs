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

if(input.configurations.length)throw Error('synthesized control requires no tsconfig');
if(input.files.some(r=>/^jsconfig(?:\..*)?\.json$/.test(path.basename(r.path))))throw Error('jsconfig present; synthesized origin not established');
const roots=input.files.filter(r=>!r.path.split('/').some(s=>['node_modules','.git','.hg','.svn','.jj'].includes(s))&&/\.(?:ts|tsx|mts|cts|js|jsx|mjs|cjs)$/.test(r.path)).map(r=>path.join(root,r.path)).sort();
const selected={allowJs:true,checkJs:false,module:'node16',moduleResolution:'node16',target:'es2022',strict:false,skipLibCheck:true,types:[],noEmit:true};
if(roots.some(p=>/\.(jsx|tsx)$/.test(p)))selected.jsx='preserve';
const converted=ts.convertCompilerOptionsFromJson(selected,root);if(converted.errors.length)throw Error('selected synthesized options rejected');
const calls=[],timed=(name,fn)=>{const t=process.hrtime.bigint();const v=fn();calls.push({name,elapsedNanos:Number(process.hrtime.bigint()-t)});return v;};
const options=converted.options,host=ts.createCompilerHost(options);host.readFile=read;host.fileExists=exists;host.directoryExists=p=>directories.has(path.resolve(p));host.getDirectories=p=>getEntries(p).directories.map(n=>path.join(p,n));host.readDirectory=readDirectory;host.realpath=p=>path.resolve(p);host.getCurrentDirectory=()=>root;host.writeFile=()=>{throw Error('emission forbidden');};
const program=timed('createProgram',()=>ts.createProgram({rootNames:roots,options,host}));
const diagnostics=[...timed('getOptionsDiagnostics',()=>program.getOptionsDiagnostics()),...timed('getGlobalDiagnostics',()=>program.getGlobalDiagnostics())];
for(const f of program.getSourceFiles()){diagnostics.push(...timed('getSyntacticDiagnostics',()=>program.getSyntacticDiagnostics(f)),...timed('getSemanticDiagnostics',()=>program.getSemanticDiagnostics(f)));}
const counts={};for(const d of diagnostics)counts[d.code]=(counts[d.code]||0)+1;
const result={origin:'synthesized',synthesizerVersion:1,selectedOptions:selected,standing:diagnostics.length?'synthesized-pass-with-deficiencies':'synthesized-pass-completed',rootFiles:roots.map(p=>path.relative(root,p)),programFiles:program.getSourceFiles().map(f=>f.fileName).sort(),diagnosticCounts:counts,diagnosticsCount:diagnostics.length,calls,maxPublicCompilerCall:calls.reduce((a,b)=>a.elapsedNanos>=b.elapsedNanos?a:b,{name:'none',elapsedNanos:0})};
console.log(JSON.stringify({id:input.id,compilerVersion:ts.version,configurationCount:0,configurations:[result],synthesizedProgramCount:1,readPaths:[...reads].sort(),blockedPaths:[...blocked].sort(),repositoryOnly:true,dependencyTreePinned:false,fullWorkspaceSemanticsClaimed:false,repositoryCodeExecuted:false,emitPerformed:false}));
