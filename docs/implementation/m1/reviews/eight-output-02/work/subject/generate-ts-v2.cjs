const fs = require('node:fs');
const path = require('node:path');
const {renderTypes} = require('./render-types.cjs');
const root = __dirname, output = process.argv[2];
if (!output) throw new Error('fresh output root required');
const arch='/Users/sb/code/opensip-ai/opensip_arch';
const schema=JSON.parse(fs.readFileSync(path.join(root,'ts-projection.json')));
const targets=JSON.parse(fs.readFileSync(path.join(root,'targets.json')));
const wireNames=Object.entries(targets).filter(([ref])=>
  /^opensip\.product\.provider-(handshake|startup)\.1#\/\$defs\/TypeScript/.test(ref)
  || ref==='opensip.product.fact-batch.3#').map(([,name])=>name);
const provider=renderTypes(schema,wireNames), report=renderTypes(schema,Object.values(targets));
const header='// Generated candidate: explicit named type renderer; inert carriers, not admission.\n';
const providerFile=path.join(output,'providers/typescript/src/generated/protocol.ts');
fs.mkdirSync(path.dirname(providerFile),{recursive:true});
fs.writeFileSync(providerFile, header+'export type Json = null | boolean | bigint | string | Json[] | {[key:string]:Json};\n'+provider.text);
const runtime='/tmp/opensip-implementation/m1-ts-runtime-subject-02';
const runtimeText=['exact-json.ts','patterns.ts','schema.ts'].map(name=>fs.readFileSync(path.join(runtime,name),'utf8').replace(/^import .*;\n/gm,'')).join('\n');
const pins=JSON.parse(fs.readFileSync(path.join(arch,'docs/implementation/m1/metadata-v2/sources.json')));
const rawSchemas=pins.schemas.map(pin=>{
  const raw=fs.readFileSync(path.join(arch,pin.path));
  if (require('node:crypto').createHash('sha256').update(raw).digest('hex')!==pin.sha256 || raw.length!==pin.bytes) throw new Error('source pin mismatch');
  return raw.toString('utf8');
});
const reportFile=path.join(output,'apps/report/src/generated/report.ts');
fs.mkdirSync(path.dirname(reportFile),{recursive:true});
fs.writeFileSync(reportFile,header+report.text+'\n'+runtimeText+'\nconst selectedSchemaBytes: string[] = '+JSON.stringify(rawSchemas)+';\n'
  +'export function createTrialReportShapeRegistry(): SchemaRegistry { return new SchemaRegistry(selectedSchemaBytes.map(raw=>parseExact(new TextEncoder().encode(raw)))); }\n');
fs.writeFileSync(path.join(root,'ts-exports.json'),JSON.stringify({provider:provider.names,report:report.names},null,2)+'\n');
console.log(JSON.stringify({providerExports:provider.names.length,reportExports:report.names.length,numberTypes:provider.numberTypes+report.numberTypes,anyTypes:provider.anyTypes+report.anyTypes}));
