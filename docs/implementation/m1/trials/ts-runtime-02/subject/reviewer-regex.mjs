import {readFileSync,writeFileSync} from 'node:fs';
import {parseExact} from './dist/exact-json.js';
import {SchemaRegistry} from './dist/schema.js';
import {selectedPattern} from './dist/patterns.js';
const {rows}=JSON.parse(readFileSync(new URL('regex-py.json',import.meta.url)));
const diff=[];const byPat={};
for(const [p,s,py] of rows){const js=new RegExp(selectedPattern(p),'u').test(s); if(js!==py){diff.push({p,s:JSON.stringify(s),py,js});byPat[p]=(byPat[p]||0)+1;}}
writeFileSync(new URL('regex-diff.json',import.meta.url),JSON.stringify({rows:rows.length,mismatches:diff.length,byPattern:byPat,sample:diff},null,1));
console.log(JSON.stringify({rows:rows.length,mismatches:diff.length,byPat},null,1));
for(const d of diff.filter(d=>/\\.\\.\?/.test(d.p)).slice(0,10))console.log(JSON.stringify(d));
// end-to-end on real registry
const arch='/Users/sb/code/opensip-ai/opensip_arch/';
const pins=JSON.parse(readFileSync(arch+'docs/implementation/m1/metadata-v2/sources.json','utf8'));
const reg=new SchemaRegistry(pins.schemas.map(p=>parseExact(readFileSync(arch+p.path))));
const cr=String.fromCharCode(13), ls=String.fromCharCode(0x2028), lf=String.fromCharCode(10);
const e2e={};
for(const s of ['a/../x','a'+cr+'/../../etc/passwd','a'+ls+'/../../x','..'+lf,'a/..'+lf,'ok/path'])
 for(const r of ['urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/CanonicalPath','urn:opensip:product-v1:workflows:common#/$defs/LogicalPath','urn:opensip:product-v1:identity:v3#/$defs/LogicalPath'])
  { try{e2e[r.split(':').slice(-1)[0]+' '+JSON.stringify(s)]=reg.matches(r,s);}catch(e){e2e[r+' '+JSON.stringify(s)]=e.constructor.name;} }
writeFileSync(new URL('regex-e2e-ts.json',import.meta.url),JSON.stringify(e2e,null,1));console.log(JSON.stringify(e2e,null,1));
