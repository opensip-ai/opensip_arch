import {readFileSync,writeFileSync} from 'node:fs';
const prof=JSON.parse(readFileSync('/tmp/opensip-implementation/m1-ts-runtime-subject-02/pattern-profile.json','utf8')).patterns;
const {values,expected}=JSON.parse(readFileSync(new URL('exhaust-cases.json',import.meta.url),'utf8'));
const mism=[];
prof.forEach((r,p)=>{const re=new RegExp(r.ecma262Unicode,'u');const e=expected[p];for(let i=0;i<values.length;i++){if((re.test(values[i])?'1':'0')!==e[i])mism.push({pattern:r.source,value:values[i]});}});
const out={patterns:prof.length,values:values.length,comparisons:prof.length*values.length,mismatches:mism.length,sample:mism.slice(0,10)};
writeFileSync(new URL('exhaust-diff.json',import.meta.url),JSON.stringify(out,null,1));console.log(JSON.stringify(out));
