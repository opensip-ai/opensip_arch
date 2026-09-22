from pathlib import Path
import subprocess,json,hashlib,difflib
T=Path('/tmp/opensip-implementation');D=T/'initial-diagnostics-generation404';P=D/'product';L=Path('/Users/sb/code/opensip-ai/opensip');A=L.parent/'opensip_arch';U=A/'docs/implementation/m2/initial-root-binding-owner-selection-v1'
node='/Users/sb/.nvm/versions/node/v24.16.0/bin/node';out=D/'typescript-runtime406';out.mkdir()
cmd=[node,str(P/'tools/contracts/node_modules/typescript/bin/tsc'),'--ignoreConfig','--strict','--target','ES2022','--module','ESNext','--moduleResolution','Bundler','--outDir',str(out),str(P/'apps/report/src/generated/report.ts')]
env={'PATH':'/usr/bin:/bin','LANG':'C','LC_ALL':'C','TZ':'UTC'}
r=subprocess.run(cmd,cwd=D,env=env,capture_output=True);(D/'typescript-emit.stdout').write_bytes(r.stdout);(D/'typescript-emit.stderr').write_bytes(r.stderr);assert r.returncode==0
(out/'package.json').write_text('{"type":"module"}\n')
(out/'probe.mjs').write_text('''import assert from 'node:assert/strict';
import {createReportShapeRegistry,parseExact} from './report.js';
const registry=createReportShapeRegistry();
const ids=['urn:opensip:product-v1:workflows:common','urn:opensip:product-v1:workflows:evaluator3:common:3','urn:opensip:product-v1:workflows:evaluator3:common:4'];
let checks=0;
for(const code of ['INSTALLATION.DURABILITY_NOT_CHECKED','INSTALLATION.NOT_INITIALIZED']){
 for(const [index,id] of ids.entries()){
  assert.equal(registry.matches(id+'#/$defs/DomainDetailCode',code),index===2);checks++;
 }
}
for(const id of ids){assert.equal(registry.matches(id+'#/$defs/DomainDetailCode','INSTALLATION.UNREGISTERED'),false);checks++;}
const report={schemaFamily:'opensip.product.envelope',schemaMajor:7,kind:'doctor',requestId:'req1_00000000000000000000000000000001',termination:{class:'success'},exitCode:0,doctor:{kind:'doctor',reportProduced:true,defectsFound:0,defects:[{code:'INSTALLATION.DURABILITY_NOT_CHECKED',remedy:'The complete installation is visible; root durability was not checked by this read-only command.'}]}};
const ref='urn:opensip:product-v1:workflows:evaluator3:command-envelope:7#';
// The real generated registry uses exact integer parsing, not JS floating-number records.
const bytes=new TextEncoder().encode(JSON.stringify(report));
assert.equal(registry.matches(ref,parseExact(bytes)),true);checks++;
report.doctor.defectsFound=false;
assert.equal(registry.matches(ref,parseExact(new TextEncoder().encode(JSON.stringify(report)))),false);checks++;
console.log(JSON.stringify({passed:true,checks,standing:'Actual generated TypeScript shape registry only; no native doctor or product UI rendering.'}));
''')
# Resolve the real selected ID rather than assuming a schema spelling.
schema=json.loads((P/'schemas/sources/command-envelope-v7.schema.json').read_text());probe=out/'probe.mjs';probe.write_text(probe.read_text().replace('urn:opensip:product-v1:workflows:evaluator3:command-envelope:7#',schema['$id']+'#'))
r=subprocess.run([node,str(probe)],cwd=out,env=env,capture_output=True);(D/'typescript-runtime.stdout').write_bytes(r.stdout);(D/'typescript-runtime.stderr').write_bytes(r.stderr);print(r.stdout.decode());print(r.stderr.decode()[:1500]);assert r.returncode==0
# All changed lines are narrowly enumerated; old Common1/Common3 and everything else are byte preserved.
name='crates/contracts/src/generated/evidence.rs';old=(L/name).read_text();new=(P/name).read_text();delta=list(difflib.unified_diff(old.splitlines(),new.splitlines(),fromfile='baseline/'+name,tofile='candidate/'+name));(U/'evidence/generated-rust.diff').write_text('\n'.join(delta)+'\n')
allowed=['Common4DomainDetailCode enum, Display and FromStr only']
for block in ['''    #[serde(rename = "INSTALLATION.DURABILITY_NOT_CHECKED")]
    InstallationDurabilityNotChecked,
    #[serde(rename = "INSTALLATION.NOT_INITIALIZED")]
    InstallationNotInitialized,
''','''            Self::InstallationDurabilityNotChecked => {
                f.write_str("INSTALLATION.DURABILITY_NOT_CHECKED")
            }
            Self::InstallationNotInitialized => {
                f.write_str("INSTALLATION.NOT_INITIALIZED")
            }
''','''            "INSTALLATION.DURABILITY_NOT_CHECKED" => {
                Ok(Self::InstallationDurabilityNotChecked)
            }
            "INSTALLATION.NOT_INITIALIZED" => Ok(Self::InstallationNotInitialized),
''']:
 assert new.count(block)==1;new=new.replace(block,'')
assert new==old
name='apps/report/src/generated/report.ts';old=(L/name).read_text().splitlines();new=(P/name).read_text().splitlines();assert len(old)==len(new);changed=[]
for a,b in zip(old,new):
 if a==b:continue
 if a.startswith('// Registry SHA-256:')or a.startswith('// Generator closure SHA-256:'):changed.append(a.split(':')[0]);continue
 if a.startswith('export type Common4DomainDetailCode = '):
  assert b.replace(' | "INSTALLATION.DURABILITY_NOT_CHECKED" | "INSTALLATION.NOT_INITIALIZED"','')==a;changed.append('Common4DomainDetailCode');continue
 if a.startswith('const selectedSchemaBytes: string[] = '):
  prefix='const selectedSchemaBytes: string[] = ';aa=json.loads(a[len(prefix):-1]);bb=json.loads(b[len(prefix):-1]);assert len(aa)==len(bb)==40
  differs=[i for i,(x,y)in enumerate(zip(aa,bb))if x!=y];assert len(differs)==1;i=differs[0];assert aa[i]==(L/'schemas/sources/common-v4.schema.json').read_text()and bb[i]==(P/'schemas/sources/common-v4.schema.json').read_text();changed.append('selectedSchemaBytes: common4 only');continue
 raise AssertionError('unexpected generated TS change '+a[:120])
(U/'evidence/generated-delta.json').write_text(json.dumps({'passed':True,'rust':allowed,'typescriptChangedLines':changed,'allOtherGeneratedBytesUnchanged':True,'common1Common3Unchanged':True,'generatedRuntimeChecks':json.loads(r.stdout)},indent=2)+'\n')
print('PASS exact generated delta and TypeScript runtime')
