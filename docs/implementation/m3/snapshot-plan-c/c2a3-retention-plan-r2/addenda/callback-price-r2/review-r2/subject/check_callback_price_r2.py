import copy,json
from pathlib import Path
base=Path(__file__).parent
d=json.loads((base/'CALL-TREE.json').read_text());root=d['root']
def transport(width):return (2*width+63)//64

def cost(t):
 if t['kind']=='primitive':return t['visits']
 return transport(t['argumentBytes'])+transport(t['resultBytes'])+sum(cost(c) for c in t['body'])

def calls(t):
 if t['kind']=='primitive':return []
 return [t]+[n for c in t['body'] for n in calls(c)]

expected={
 'Collector::chunk callback entry':(24,0),'Vec::extend_from_slice':(24,0),
 'slice::iter':(16,16),'Iter::new(u8)':(16,16),
 'SpecExtend<u8,slice::Iter>':(24,0),'Iter::as_slice':(8,16),
 'Iter::make_slice':(8,16),'Vec::append_elements':(24,0),
 'Vec::reserve':(16,0),'RawVec::reserve':(24,0),
 'RawVecInner::reserve no-growth':(40,0),'RawVecInner::needs_to_grow':(40,1),
 'RawVecInner::capacity':(16,8),'Vec::as_mut_ptr':(8,8),
 'RawVec::ptr':(8,8),'RawVecInner::ptr':(8,8),'RawVecInner::non_null':(8,8)}

def validate(t):
 nodes=calls(t);assert len(nodes)==len(expected)
 assert {n['name'] for n in nodes}==set(expected)
 for n in nodes:assert (n['argumentBytes'],n['resultBytes'])==expected[n['name']]
 for name,required in [('Vec::append_elements','count > 0 predicate'),('Iter::new(u8)','T::IS_ZST condition'),('Iter::make_slice','T::IS_ZST condition')]:
  n=next(n for n in nodes if n['name']==name)
  assert sum(c.get('name')==required for c in n['body'])==1
validate(root)
assert cost(root)==66 and cost(root)<=128
failure_counts={name:cost(t) for name,t in d['failurePaths'].items()}
assert failure_counts=={'sticky':2,'inactive':6,'overrun':10}
assert all(v<=128 for v in failure_counts.values())
assert transport(40)==2 and transport(0)==0 and transport(24)==1
mutants=[]
for name in ('Vec::extend_from_slice','SpecExtend<u8,slice::Iter>'):
 m=copy.deepcopy(root);next(n for n in calls(m) if n['name']==name)['argumentBytes']=0
 try:validate(m)
 except AssertionError:mutants.append('omit forwarding '+name)
 else:raise AssertionError('forwarding mutation survived')
m=copy.deepcopy(root);a=next(n for n in calls(m) if n['name']=='Vec::append_elements');a['body']=[c for c in a['body'] if c.get('name')!='count > 0 predicate']
try:validate(m)
except AssertionError:mutants.append('omit count predicate')
else:raise AssertionError('predicate mutation survived')
assert (2*40)//64!=transport(40);mutants.append('floor forty-byte tuple transport')
cases=0
for f in (0,1,2,11,12,64,65536):
 h=1+f.bit_length();n=2*f;q=11*f*h
 for e in ((0,) if f==0 else (2*f,4*f,65538*f)):
  map_rows=7*f+83*n+f*h+2*q
  old=128+map_rows+64*f+8*e
  new=128+map_rows+64*f+128*e
  assert new==128+f*(237+23*h)+128*e
  assert new-old==120*e
  assert 64*(new-q)-64*(old-q)==7680*e
  assert new-(128+12*f)>=0
  cases+=1
report={'passed':True,'candidateCallTreeVisits':cost(root),'selectedCallbackVisits':128,
 'nonleafCallsExplicit':len(calls(root)),'candidateFailureVisits':failure_counts,'sourceRowsMatchedToBodiesIndependently':False,
 'uniformTransportRule':'ceil(2*active-width/64), argument and nonunit return separately',
 'mutationsRefused':mutants,'numericCases':cases,'extraProposedCost':['0','120E','7680E'],
 'primitiveContractsEstablished':False,'sourceOperandTotalsEstablished':False,
 'completeMBoundEstablished':False,'nativeEvidenceObserved':False,
 'unitAcceptance':False,'productQualification':False}
(base/'callback-price-report-r2.json').write_text(json.dumps(report,indent=2)+'\n')
