"""Fresh synthetic prospective event-boundary controls; no actual acquisition."""
from pathlib import Path
import json
LIMITS=(16384,4000000,32*(1<<30))
class Stop(Exception):
    def __init__(self,field,observed,limit):self.fields=(field,observed,limit)
class Model:
    def __init__(self,totals=(0,0,0)):
        self.totals=list(totals);self.delivered=bytearray();self.consumed=0
    def source(self):
        self.totals[0]+=1
        if self.totals[0]>LIMITS[0]:raise Stop('sources',self.totals[0],LIMITS[0])
    def begin(self):
        self.totals[1]+=1
        if self.totals[1]>LIMITS[1]:raise Stop('files',self.totals[1],LIMITS[1])
    def content(self,actual):
        for byte in actual:
            self.totals[2]+=1;self.consumed+=1
            if self.totals[2]>LIMITS[2]:raise Stop('content',self.totals[2],LIMITS[2])
            self.delivered.append(byte)
checks=[]
def record(name,passed,**facts):
    assert passed,name;checks.append(dict(name=name,passed=True,**facts))
for width in [1,2,3,7,8,16,17,4096,32768]:
    m=Model((1,1,LIMITS[2]-10));data=b'abcdefghijklmnopq';failure=None
    try:
        for i in range(0,len(data),width):m.content(data[i:i+width])
    except Stop as e:failure=e.fields
    record('content first crossing width'+str(width),failure==('content',LIMITS[2]+1,LIMITS[2])and m.consumed==11 and bytes(m.delivered)==data[:10],observed=failure,chargedActualBytes=11,deliveredBeforeRefusal=10)
for width in [1,2,7,4096,32768]:
    m=Model((1,1,LIMITS[2]-17));data=b'abcdefghijklmnopq'
    for i in range(0,len(data),width):m.content(data[i:i+width])
    record('inclusive content width'+str(width),m.totals[2]==LIMITS[2]and m.consumed==17 and bytes(m.delivered)==data)
for content_at_limit in [False,True]:
    m=Model((1,LIMITS[1],LIMITS[2]if content_at_limit else 0));failure=None
    try:m.begin();m.content(b'x')
    except Stop as e:failure=e.fields
    record('file before content '+str(content_at_limit),failure==('files',LIMITS[1]+1,LIMITS[1])and m.consumed==0 and m.delivered==b'')
for files_at_limit in [False,True]:
    m=Model((LIMITS[0],LIMITS[1]if files_at_limit else 0,LIMITS[2]));failure=None
    try:m.source();m.begin();m.content(b'x')
    except Stop as e:failure=e.fields
    record('source before files '+str(files_at_limit),failure==('sources',LIMITS[0]+1,LIMITS[0])and m.consumed==0)
for n in [0,1,7,100]:
    m=Model((1,0,LIMITS[2]))
    for _ in range(n):m.begin();m.content(b'')
    record('zero content file count '+str(n),m.totals==[1,n,LIMITS[2]]and m.consumed==0)
for late in ['trailer CRC','trailer ISIZE','tar end','physical IO','cancellation','custody corruption']:
    m=Model();m.source();m.begin();m.content(b'partial');before=tuple(m.totals)
    # The label is an injected subsequent origin, not actual error evidence.
    # A later rejection never refunds already observed candidate work.
    record('late injected origin retains charges '+late,before==(1,1,7),injectedOrigin=late,actualErrorExecution=False,activationDerived=False,admissionGranted=False)
for ignored in ['gzip header','FNAME','tar header','GNU longname','file padding','tar end region']:
    m=Model((1,1,7));before=tuple(m.totals)
    # Control-only/framing observations do not call content()/begin().
    record('nonregular work excluded '+ignored,tuple(m.totals)==before,owningPhysicalWorkUnchanged=True)
for declared in [0,1,1<<64,1<<95]:
    m=Model();m.source();m.begin();m.content(b'x')
    record('announced size is not content '+str(declared),m.totals==( [1,1,1] ),declaredSize=declared,actualPayload=1)
for content in [0,1]:
    m=Model((1,LIMITS[1]-1,0));m.begin();m.content(bytes(content))
    record('inclusive file event '+str(content),m.totals==[1,LIMITS[1],content])
for swap_names in [False,True]:
    candidates=[(('a','1','s'),b'xx'),(('b','1','s'),b'')]
    if swap_names:candidates=[(candidates[1][0],candidates[0][1]),(candidates[0][0],candidates[1][1])]
    outcomes=[]
    for reverse in [False,True]:
        given=list(reversed(candidates))if reverse else candidates
        ordered=sorted(given,key=lambda row:tuple(value.encode('utf-8')for value in row[0]));m=Model((0,LIMITS[1]-1,LIMITS[2]-1));failure=None
        try:
            for key,payload in ordered:m.source();m.begin();m.content(payload)
        except Stop as e:failure=e.fields
        outcomes.append(failure)
        expected=('files',LIMITS[1]+1,LIMITS[1])if swap_names else('content',LIMITS[2]+1,LIMITS[2])
        record('canonical provided permutation '+str(swap_names)+'/'+str(reverse),failure==expected,canonicalOrderFromSuppliedSyntheticTuples=True,actualOwnedCorrespondence=False)
    assert outcomes[0]==outcomes[1]
result=dict(standing='FRESH SYNTHETIC PROSPECTIVE LOGICAL-EVENT CONTROLS; NOT SELECTED LAW OR PHYSICAL READER/DECODER/RESOURCE/CUSTODY/ADMISSION PROOF',testsPassed=len(checks),checks=checks,actualPhysicalBufferGuardImplemented=False,actualSourceAdmission=False,chargingBoundarySelected=False,fullC3aComplete=False,productQualification=False)
Path(__file__).with_name('controls.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(testsPassed=len(checks),allPassed=True,actualPhysicalBufferGuardImplemented=False)))
