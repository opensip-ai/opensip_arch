const fs = require('node:fs');
const path = require('node:path');
const {compile} = require('/tmp/opensip-implementation/m1-generator-trial-01/ts/node_modules/json-schema-to-typescript');
const root = __dirname;
const output = process.argv[2];
if (!output) throw new Error('fresh output root required');
const runtime = '/tmp/opensip-implementation/m1-ts-runtime-subject-02';
const arch = '/Users/sb/code/opensip-ai/opensip_arch';
const schema = JSON.parse(fs.readFileSync(path.join(root, 'ts-projection.json')));
const targets = JSON.parse(fs.readFileSync(path.join(root, 'targets.json')));
const bannerComment = '// Generated trial: named28 profile, json-schema-to-typescript16.0.0; inert carriers only.';
async function main() {
  const reportTypes = await compile(schema, 'TrialReportContracts', {
    unreachableDefinitions:true, ignoreMinAndMaxItems:true, enableConstEnums:false, bannerComment});
  const wireRefs = Object.entries(targets).filter(([ref]) =>
    /^opensip\.product\.provider-(handshake|startup)\.1#\/\$defs\/TypeScript/.test(ref)
    || ref === 'opensip.product.fact-batch.3#');
  const providerSchema = {...schema, anyOf: wireRefs.map(([,name])=>({$ref:'#/definitions/'+name}))};
  const providerTypes = await compile(providerSchema, 'TrialSelectedProviderPayload', {
    unreachableDefinitions:false, ignoreMinAndMaxItems:true, enableConstEnums:false, bannerComment});
  const providerPath = path.join(output, 'providers/typescript/src/generated/protocol.ts');
  fs.mkdirSync(path.dirname(providerPath), {recursive:true});
  fs.writeFileSync(providerPath, 'export type Json = null | boolean | bigint | string | Json[] | {[key:string]:Json};\n' + providerTypes);
  const runtimeText = ['exact-json.ts', 'patterns.ts', 'schema.ts'].map(name=>
    fs.readFileSync(path.join(runtime,name),'utf8').replace(/^import .*;\n/gm,'')).join('\n');
  const pins = JSON.parse(fs.readFileSync(path.join(arch, 'docs/implementation/m1/metadata-v2/sources.json')));
  const rawSchemas = pins.schemas.map(pin=>{
    const raw = fs.readFileSync(path.join(arch,pin.path));
    const hash = require('node:crypto').createHash('sha256').update(raw).digest('hex');
    if (hash !== pin.sha256 || raw.length !== pin.bytes) throw new Error('source pin mismatch');
    return raw.toString('utf8');
  });
  const reportPath = path.join(output,'apps/report/src/generated/report.ts');
  fs.mkdirSync(path.dirname(reportPath), {recursive:true});
  const report = reportTypes + '\n' + runtimeText + '\nconst selectedSchemaBytes: string[] = '
    + JSON.stringify(rawSchemas) + ';\n'
    + 'export function createTrialReportShapeRegistry(): SchemaRegistry {\n'
    + '  return new SchemaRegistry(selectedSchemaBytes.map(raw=>parseExact(new TextEncoder().encode(raw))));\n}\n';
  fs.writeFileSync(reportPath, report);
  console.log(JSON.stringify({providerEntryPoints:wireRefs.length, providerBytes:Buffer.byteLength(providerTypes),reportBytes:Buffer.byteLength(report)}));
}
main().catch(error=>{console.error(error);process.exitCode=1;});
