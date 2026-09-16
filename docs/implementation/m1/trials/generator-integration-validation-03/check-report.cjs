const fs=require('node:fs');const R=require('./compiled/report.js');
const options=JSON.parse(fs.readFileSync(process.argv[2]));const registry=R.createReportShapeRegistry();
registry.checkEntryPoints(options.entryPoints.map(row=>row.ref));let refused=0;
for (const base of options.deniedRefs) for (const ref of [base,base+'/properties/protocolMajor']) {
 for (const call of [()=>registry.checkEntryPoints([ref]),()=>registry.matches(ref,{})]) {
  try {call();throw new Error('superseded ref admitted');}catch(e){if (!(e instanceof R.SchemaError) || !e.message.includes('unselected report')) throw e;refused++;}
 }
}
const cases=R.parseExact(fs.readFileSync('./carrier-cases.json'));let matched=0;
for(const [ref,index] of cases.rows){const value=cases.values[Number(index)];if(!registry.matches(ref,value))throw new Error('shape rejected '+ref);matched++;}
console.log(JSON.stringify({selected:options.entryPoints.length,deniedProbes:refused,matched}));
