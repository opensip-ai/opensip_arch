const fs=require('node:fs');const R=require('./report.cjs');const reg=R.createReportShapeRegistry();
const ID='urn:opensip:design:control-schema:3#';const out={};
for(const file of process.argv.slice(2)){
 const cases=JSON.parse(fs.readFileSync(file,'utf8'));const mism=[];const counts={};
 for(const c of cases){const bytes=c.rawHex!==undefined?Buffer.from(c.rawHex,'hex'):new TextEncoder().encode(c.raw);let got=false,err=null;
  try{got=reg.matches(ID,R.parseExact(new Uint8Array(bytes)));}catch(e){err=(e.message||e.constructor.name);}
  const k=(c.kind||'corpus')+':'+c.valid+':'+got;counts[k]=(counts[k]||0)+1;
  if(got!==c.valid)mism.push({id:c.id,expected:c.valid,got,err});
  if(c.kind==='lexical')(out.lexical??=[]).push({id:c.id,err});}
 out[file]={cases:cases.length,counts,mismatches:mism};}
const mal=[];for(const b of [-1n,true,'128',null,{},[],1.5,0.0,-0n]){let ok=true;try{new R.SchemaRegistry([{$id:'urn:u',type:'string','x-maxUtf8Bytes':b}]).checkEntryPoints(['urn:u#'])}catch{ok=false}mal.push({bound:String(b),type:typeof b,accepted:ok});}
let zero;try{const r=new R.SchemaRegistry([{$id:'urn:z',type:'string','x-maxUtf8Bytes':0n}]);r.checkEntryPoints(['urn:z#']);zero={empty:r.matches('urn:z#',''),one:r.matches('urn:z#','a')}}catch(e){zero=String(e)}
// non-parser inputs: lone surrogate string handed directly to matches (bypassing parseExact)
let direct;try{const r=new R.SchemaRegistry([{$id:'urn:s',type:'string','x-maxUtf8Bytes':3n}]);r.checkEntryPoints(['urn:s#']);direct={loneSurrogate:r.matches('urn:s#','\ud800'),fourBytes:r.matches('urn:s#','\u{1F980}'),threeBytes:r.matches('urn:s#','界')}}catch(e){direct=String(e)}
out.malformed=mal;out.zero=zero;out.direct=direct;fs.writeFileSync('ts-probe-result.json',JSON.stringify(out,null,1));
for(const [k,v] of Object.entries(out))console.log(k,JSON.stringify(v.mismatches?{cases:v.cases,counts:v.counts,mismatches:v.mismatches.slice(0,10)}:v).slice(0,1500));
