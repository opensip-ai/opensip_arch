from pathlib import Path
import json,hashlib,re,copy
B=Path(__file__).parent
D=json.loads((B/'CALL-TREE.json').read_text())['definitions']; L=json.loads((B/'LEDGER.json').read_text())
def cost(node,defs=D,stack=()):
 if node['kind']=='primitive':return node['visits']
 if node['kind']=='ref':
  name=node['name'];assert name not in stack
  return cost(defs[name],defs,stack+(name,))
 assert node['kind']=='call'
 return sum((2*node[k]+63)//64 for k in ('argumentBytes','resultBytes'))+sum(cost(x,defs,stack) for x in node['body'])
def total(rows,defs=D):return sum(cost(defs[x['node']],defs)*x['times'] if 'node'in x else x['visits'] for x in rows)
fixed=total(L['fixed']);scan=total(L['perBlob']);assert fixed==768<=1024 and scan==163<=256
assert 1<<(fixed-1).bit_length()==1024 and 1<<(scan-1).bit_length()==256

# Explicit one-time post-bootstrap failure substitution and borrowed cleanup.
error_defs=json.loads((B/'ERROR-CALL-TREE.json').read_text())
assert error_defs['baseCallTreeSha256']==hashlib.sha256((B/'CALL-TREE.json').read_bytes()).hexdigest()
expanded={**D,**error_defs['definitions']}
error_visits={k:cost(v,expanded) for k,v in error_defs['definitions'].items()}
assert error_visits['helper_error']==12 and error_visits['try_error']==24
error_ceiling=max(error_visits[k]for k in ['helper_question_error','sub_question_error','charge_question_error'])+16
assert error_ceiling==52<=64<128
assert 1024-(fixed-128+error_ceiling)==332 and 256-scan==93

source=(B/'product/crates/lifecycle/src/component_admission.rs').read_text();assert hashlib.sha256(source.encode()).hexdigest()=='12d82483517c7bb2da9d6bd485566a36000c6bdca0a41ce182d5fe5dc7ada996'
part=source.split('fn fund_representation(',1)[1].split('\n}\n',1)[0];loop=part.split('    for blob in candidate.blobs() {',1)[1].split('\n    }',1)[0];allcalls=len(re.findall(r'\b(?:add|mul)\(',part));scancalls=len(re.findall(r'\b(?:add|mul)\(',loop));assert allcalls-scancalls==32 and scancalls==5
proposed=(B/'proposed-component_admission.rs').read_text();expected=source.replace('const FIXED: usize = 128;','const FIXED: usize = 1024;').replace('let scan = mul(12, count)?;','let scan = mul(256, count)?;').replace('mul(count, add(237, mul(23, height)?)?)?','mul(count, add(481, mul(23, height)?)?)?');assert proposed==expected
cases=[]
for f in [0,1,2,5,11,12,64,1024,65536]:
 for b in [0,1,65536]:
  for p in [0,9,4096]:
   h=1+f.bit_length();e=f*(2*((b+65535)//65536)+2);q=11*f*h
   old=128+f*(237+23*h)+128*e;new=1024+f*(481+23*h)+128*e;pre=1024+256*f
   assert new-old==896+244*f and 64*(new-old)==57344+15616*f
   assert new-pre==f*(225+23*h)+128*e>=0
   assert (new-q)-pre==f*(225+12*h)+128*e>=0
   assert fixed+scan*f<=pre
   cases.append({'F':f,'perBlobBytes':b,'P':p,'proposedEdges':new,'prepaidEdges':pre})
# These counterclaims are arithmetic controls, not executed Rust mutants.
refused=[]
assert fixed>128;refused.append('reuse fixed128')
assert scan>12;refused.append('reuse scan12F')
assert 481-256==237-12==225;assert 237-256!=225;refused.append('raise scan without total coefficient')
assert (896+244)>0;refused.append('omit extra scalar byte streams')
for name in ['vec_deref','fn_forward','try_success']:
 assert cost(D[name])>0;refused.append('erase nonleaf '+name)
report={'passed':True,'definitionVisits':{k:cost(v)for k,v in D.items()},'fixedCandidateVisitsIncluding128ErrorReserve':fixed,'scanCandidateVisitsPerBlob':scan,'selectedFixed':1024,'selectedScan':256,'postBootstrapErrorSubgraphVisits':error_ceiling,'trustedBootstrapExplicitlyExcluded':True,'sourceHelperCalls':{'fixed':32,'perBlob':5},'formulaCases':len(cases),'refusedCounterclaims':refused,'checkedCases':cases,'nativeExecution':False,'actualRustExecuted':False,'primitiveContractsEstablished':False,'trustedMeterBodyExcludedByProposedBoundary':True,'completeMBoundEstablished':False,'unitAcceptance':False,'productQualification':False}
(B/'funding-price-report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items()if k not in ['definitionVisits','checkedCases']}))
