import {readFileSync} from 'node:fs';
const prof=JSON.parse(readFileSync('/tmp/opensip-implementation/m1-ts-runtime-subject-02/pattern-profile.json','utf8')).patterns;
const {values,expected}=JSON.parse(readFileSync(new URL('exhaust-cases.json',import.meta.url),'utf8'));
let positives=0,mapped=0,unmapped=0;const byPat={};
prof.forEach((r,p)=>{const m=new RegExp(r.ecma262Unicode,'u'),u=new RegExp(r.source,'u');const e=expected[p];
 for(let i=0;i<values.length;i++){if(e[i]==='1')positives++; const x=e[i]==='1'; if(m.test(values[i])!==x)mapped++; if(u.test(values[i])!==x){unmapped++;byPat[r.source]=(byPat[r.source]||0)+1;}}});
console.log(JSON.stringify({values:values.length,expectedLen:expected[0].length,positives,mappedMismatch:mapped,unmappedSourceMismatch:unmapped,byPat}));
