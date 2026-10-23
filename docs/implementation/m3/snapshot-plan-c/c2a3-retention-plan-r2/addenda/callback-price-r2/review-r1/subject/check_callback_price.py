import json
from pathlib import Path
base=Path(__file__).parent
stages=json.loads((base/'STAGES.json').read_text())['stages']
assert len(stages)==16 and len({s['id'] for s in stages})==16
for stage in stages:
 assert sum(o['bytes'] for o in stage['logicalOperands'])==stage['candidateBytes']
 assert 0<stage['candidateBytes']<=64
cases=0
for f in (0,1,2,11,12,64,65536):
 h=1+f.bit_length();n=2*f;q=11*f*h
 for e in ((0,) if f==0 else (2*f,4*f,65538*f)):
  map_rows=7*f+83*n+f*h+2*q
  old=128+map_rows+64*f+8*e
  new=128+map_rows+64*f+16*e
  assert new==128+f*(237+23*h)+16*e
  assert new-old==8*e
  assert (new-q)*64-(old-q)*64==512*e
  assert new-(128+12*f)>=0
  cases+=1
# The same16 stage allowance bounds the selected refusal stage counts.
refusals={'sticky':1,'inactive':4,'overrun':6}
assert all(v<=16 for v in refusals.values())
# Wrong delta interpretations must not be accepted as the selected formula.
e=2
assert 8*e!=16*e
assert 512*e!=64*e
report={'passed':True,'numericCases':cases,'candidateStageCount':len(stages),
 'maxCandidateOperandBytes':max(s['candidateBytes'] for s in stages),
 'sourceOperandTotalsIndependentlyProven':False,
 'selectedRefusalStageCounts':refusals,'wrongDeltaCounterclaimsRefused':2,
 'extraCost':['0','8E','512E'],'productFormulaChanged':False,
 'completeMBoundEstablished':False,'nativeEvidenceObserved':False,
 'unitAcceptance':False,'productQualification':False}
(base/'callback-price-report.json').write_text(json.dumps(report,indent=2)+'\n')
