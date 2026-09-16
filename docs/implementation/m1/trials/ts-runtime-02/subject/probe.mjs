import { readFileSync, writeFileSync } from 'node:fs';
import { parseExact, canonical } from './dist/exact-json.js';
const corpus = readFileSync('/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m1/reviews/canonical-02/probes/corpus.hex','utf8').trim().split('\n');
let accepted=0;
const results=corpus.map(hex=>{
 try { const value=parseExact(Buffer.from(hex,'hex'));accepted++;return 'OK '+Buffer.from(canonical(value)).toString('hex'); }
 catch { return 'REFUSE'; }
});
writeFileSync(new URL('ts-outcomes.txt',import.meta.url),results.join('\n')+'\n');
console.log(JSON.stringify({cases:corpus.length,accepted,refused:corpus.length-accepted}));
