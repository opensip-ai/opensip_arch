const fs=require('node:fs');const assert=require('node:assert/strict');
const R=require('/tmp/opensip-implementation/m1-grok-native-integration-review-02/review/results/compiled-g/wire.js');
const registry=R.createReportShapeRegistry();let checks=0;
const cases=JSON.parse(fs.readFileSync('/tmp/opensip-implementation/m1-joint-generation-candidate-02/current-report-cases10.json'));
for(const {ref,raw,label} of cases){const value=R.parseReportExact(new TextEncoder().encode(raw));assert(registry.matches(ref,value),label);checks++;}
const raw=fs.readFileSync('/tmp/opensip-implementation/m1-report-codec-candidate-02/dense-report.json');const value=R.parseReportExact(raw);
assert(registry.matches('urn:opensip:product-v1:workflows:evaluator3:report-projection:1#',value));checks++;
assert.deepEqual(Buffer.from(R.canonicalReport(value)),raw);checks++;
assert.throws(()=>R.parseExact(raw),e=>e instanceof R.JsonError&&e.message==='BYTE_LIMIT');checks++;
assert.throws(()=>registry.matches('urn:opensip:product-v1:workflows:evaluator3:command-envelope:7#',value),e=>e instanceof R.JsonError&&e.message==='BYTE_LIMIT');checks++;
assert.throws(()=>registry.matches('urn:opensip:unselected#',value),e=>e instanceof R.SchemaError&&e.message==='unselected report schema entrypoint');checks++;
const current=cases.find(c=>c.ref.endsWith('report-projection:1#'));
const stale=R.parseReportExact(new TextEncoder().encode(current.raw.replace('renderer-gating-against-inventory6','renderer-gating-against-inventory5')));
assert.equal(registry.matches(current.ref,stale),false);checks++;
const staleProfile=R.parseReportExact(new TextEncoder().encode(current.raw.replace('opensip.report-projection.development-caps.6','opensip.report-projection.development-caps.5')));
assert.equal(registry.matches(current.ref,staleProfile),false);checks++;
fs.writeFileSync('/tmp/opensip-implementation/m1-grok-native-integration-review-02/review/results/combined-consumer-g.json' ,JSON.stringify({passed:true,checks,currentCases:cases.length,denseReportBytes:raw.length,defaultEnvelopeBoundaryPreserved:true,unselectedRootsRefused:true,standing:'Generated report wrapper integration only; no product host, browser or embedded semantic owner qualification'},null,2)+'\n');
