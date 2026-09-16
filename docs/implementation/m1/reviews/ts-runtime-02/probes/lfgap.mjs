import {readFileSync} from 'node:fs';
import {parseExact} from '../subject/dist/exact-json.js';
import {SchemaRegistry} from '../subject/dist/schema.js';
const arch='/Users/sb/code/opensip-ai/opensip_arch/';
const pins=JSON.parse(readFileSync(arch+'docs/implementation/m1/metadata-v2/sources.json','utf8'));
const reg=new SchemaRegistry(pins.schemas.map(p=>parseExact(readFileSync(arch+p.path))));
const py=JSON.parse(readFileSync(new URL('lfgap-py.json',import.meta.url),'utf8'));
console.log(JSON.stringify({rows:py.length,mismatch:py.filter(([r,v,e])=>reg.matches(r,v)!==e).length,tsAcceptsLfTraversal:py.filter(([r,v])=>/\n\/\.\./.test(v)&&reg.matches(r,v)).map(([r,v])=>[r.split('#')[1]+' '+r.split(':').slice(-1)[0],JSON.stringify(v)])}));
