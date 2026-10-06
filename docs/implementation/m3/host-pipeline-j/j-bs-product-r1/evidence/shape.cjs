const fs = require('node:fs');
const Module = require('node:module');
const path = require('node:path');
const root = process.argv[2];
const ts = require(path.join(root, 'tools/contracts/node_modules/typescript'));
const source = fs.readFileSync(path.join(root, 'apps/report/src/generated/report.ts'), 'utf8');
const code = ts.transpileModule(source, {compilerOptions: {module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2022}}).outputText;
const generated = new Module(path.join(process.cwd(), 'generated-report.cjs'));
generated.filename = path.join(process.cwd(), 'generated-report.cjs');
generated._compile(code, generated.filename);
const registry = generated.exports.createReportShapeRegistry();
const ref = 'urn:opensip:product-v1:workflows:evaluator3:invocation:5#/$defs/RetentionDisclosure';
const envRef = 'urn:opensip:product-v1:workflows:evaluator3:command-envelope:7#';
function check(ref, value, expected) {
  const actual = registry.matches(ref, value);
  if (actual !== expected) throw new Error(JSON.stringify({ref, value, expected, actual}));
}
let presence = 0;
for (const policy of ['durable-unbounded','durable-bounded','ephemeral'])
for (const provenance of ['DEFAULTED','CONFIGURED','EXPLICIT-FLAG'])
for (const firstUse of [false,true])
for (const backupStatus of [undefined,'backed-up','not-backed-up','unknown']) {
  const value = {policy,provenance,firstUse,storageRoot:'/tmp/jbs-synthetic-path-only'};
  if (backupStatus !== undefined) value.backupStatus = backupStatus;
  check(ref,value,firstUse ? backupStatus !== undefined : backupStatus === undefined);presence++;
}
const baseline = {policy:'durable-unbounded',provenance:'DEFAULTED',firstUse:true,storageRoot:'/tmp/jbs-synthetic-path-only',backupStatus:'unknown'};
let malformed=0;
for (const backupStatus of [null,true,false,1n,0n,{},[],'UNKNOWN','unknown\n','not backed up','']) {check(ref,{...baseline,backupStatus},false);malformed++;}
for (const firstUse of [null,1n,0n,'true',{},[]]) {check(ref,{...baseline,firstUse},false);malformed++;}
for (const key of ['policy','provenance','firstUse','storageRoot']) {const value={...baseline};delete value[key];check(ref,value,false);malformed++;}
check(ref,{...baseline,extra:true},false);malformed++;
let interrupted=0;
for (const signal of ['SIGINT','SIGTERM','SIGHUP']) {
  const envelope={schemaFamily:'opensip.product.envelope',schemaMajor:7n,kind:'failure',requestId:'req1_'+'0'.repeat(32),termination:{class:'interrupted',signal},exitCode:130n,errors:[]};
  check(envRef,envelope,true);interrupted++;
  for (const firstUse of [false,true]) {const retentionDisclosure={...baseline,firstUse};if (!firstUse) delete retentionDisclosure.backupStatus;check(envRef,{...envelope,retentionDisclosure},false);interrupted++;}
}
process.stdout.write(JSON.stringify({passed:true,presenceCases:presence,malformedCases:malformed,interruptedCases:interrupted,actualGeneratedReportValidator:true,emitterRan:false,productQualification:false})+'\n');
