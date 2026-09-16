import fs from 'node:fs';
import path from 'node:path';
import {isBuiltin} from 'node:module';
import {build} from 'esbuild';
import {browserOptions} from './browser-options.mjs';

// Resolve one edge with esbuild's actual scanner and disabled-module handling.
// The tool-owned onLoad provides all module bodies: dependency bodies are never
// read or executed. Package manifests are resolver inputs. No ambient JS config
// or third-party plugin is loaded. This is not a malicious-tool sandbox.
export async function createBrowserResolver(root) {
 let disposed=false;
 return Object.freeze({
  async resolve(request,baseFile,mode) {
   if(disposed)throw Error('browser resolver disposed');
   if(!['import','require'].includes(mode))throw Error('unselected resolution mode');
   baseFile=path.resolve(baseFile);const loaded=[];
   const body=mode==='require'?`globalThis.__opensip_edge=require(${JSON.stringify(request)});`:`import * as dependency from ${JSON.stringify(request)};globalThis.__opensip_edge=dependency;`;
   let r;
   try{r=await build({...browserOptions(),absWorkingDir:root,entryPoints:[baseFile],outfile:'unused-resolution.js',metafile:true,treeShaking:false,
    plugins:[{name:'opensip-edge-resolution',setup(api){
     api.onResolve({filter:/.*/},a=>a.kind==='entry-point'?{path:baseFile,namespace:'file'}:undefined);
     api.onLoad({filter:/.*/,namespace:'file'},a=>{
      if(a.path===baseFile&&!a.suffix)return {contents:body,loader:'js',resolveDir:path.dirname(baseFile)};
      loaded.push({path:a.path,suffix:a.suffix});return {contents:'export const boundaryPlaceholder=0;',loader:'js',resolveDir:path.dirname(a.path)};
     });
    }}]});}catch(e){return {kind:'refused',detail:isBuiltin(request)?'builtin':'unresolved',errors:e.errors?.map(e=>e.text)??[String(e)]};}
   const entry=Object.entries(r.metafile.inputs).find(([file])=>path.resolve(root,file)===baseFile);
   const edge=entry?.[1].imports[0];
   if(!edge)return {kind:'refused',detail:'missing-scanned-edge'};
   if(edge.external)return {kind:'refused',detail:'external-browser-module',path:edge.path};
   if(loaded.length===0&&path.resolve(root,edge.path)===baseFile&&fs.statSync(baseFile,{throwIfNoEntry:false})?.isFile())return {kind:'resolved',path:fs.realpathSync(baseFile),suffix:''};
   if(loaded.length===0&&edge.path.startsWith('(disabled):'))return {kind:'ignored'};
   if(loaded.length!==1)return {kind:'refused',detail:'unexpected-target-count',count:loaded.length};
   const selected=loaded[0];const st=fs.statSync(selected.path,{throwIfNoEntry:false});
   if(!st?.isFile())return {kind:'refused',detail:'not-regular-file',path:selected.path};
   const physical=fs.realpathSync(selected.path);
   const logical=path.relative(fs.realpathSync(root),physical).split(path.sep).join('/')+selected.suffix;
   // esbuild may invoke file onLoad even for a browser:false module. Its
   // metadata decorates that physical target; a filename prefix alone is not enough.
   if(edge.path==='(disabled):'+logical)return {kind:'ignored'};
   if(edge.path!==logical)return {kind:'refused',detail:'metadata-target-mismatch',path:edge.path};
   return {kind:'resolved',path:physical,suffix:selected.suffix};
  },
  async dispose(){disposed=true;},
 });
}
