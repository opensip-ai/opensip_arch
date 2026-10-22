"""Draft M arithmetic and staged-fee consistency; no implemented/native fit evidence."""
import hashlib
import json
from pathlib import Path
import re

BASE = Path(__file__).parent
inputs = json.loads((BASE/'INPUTS.json').read_text())
for row in inputs['files']:
    raw = (BASE/'inputs'/row['path']).read_bytes()
    assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
owned = (BASE/'inputs/product/crates/security/src/custody/discovery_walk.rs').read_text()
ci = (BASE/'inputs/product/crates/lifecycle/src/installation.rs').read_text()
assert re.search(r'const RECORD: usize = 128;',owned)
assert 'bytes: bytes.saturating_add(RECORD)' in owned
assert 'const READ_CHUNK: usize = 65_536;' in ci
MAXIMUM = (1<<64)-1


def checked(value):
    if type(value) is not int or value<0 or value>MAXIMUM:
        raise ArithmeticError('Budget/Arithmetic model')
    return value


def add(*costs):
    return tuple(checked(sum(c[i] for c in costs)) for i in range(3))


def subtract(a,b):
    return tuple(checked(a[i]-b[i]) for i in range(3))


def record(size):
    return (1,0,checked(checked(size)+128))


def multiply(cost,times):
    return tuple(checked(value*times) for value in cost)


def representation(lengths,path_bytes):
    f = checked(len(lengths)); p = checked(path_bytes)
    lengths = [checked(n) for n in lengths]
    b = checked(sum(lengths)); h = 1+f.bit_length()
    envelope = checked(sum(checked(2*((n+65535)//65536)+2) for n in lengths))
    nodes = checked(2*f); q = checked(11*f*h)
    # Expanded category table; every non-path edge gets the metadata allowance.
    map_edges = checked(2*nodes+6*f+8*nodes+22*(2*nodes)+20*nodes+8*nodes
                        +(f+nodes)+f*h+2*q)
    edges = checked(128+64*f+8*envelope+map_edges)
    assert edges == 128+f*(237+23*h)+8*envelope
    scalar = checked(edges-q)
    bulk = checked(768*f+704*nodes+1024*(2*nodes)+1024*nodes+1024*nodes)
    assert bulk == 10368*f
    storage = add(record(checked(24*f)) if f else (0,0,0),
                  *(record(n) for n in lengths),multiply(record(512),nodes))
    total = add(storage,(0,edges,checked(2*b+48*f+2*p*q+64*scalar+bulk)))
    fixed = (0,128,8192)
    scan = (0,checked(12*f),checked(64*12*f))
    remaining = subtract(subtract(total,fixed),scan)
    assert add(fixed,scan,remaining) == total
    return {'blobCount':f,'bytes':b,'maxPathBytes':p,'heightBound':h,'readAttemptEnvelopeSum':envelope,
            'mapNodesBound':nodes,'keyComparisonsBound':q,'proposedM':total,
            'fixedCharge':fixed,'metadataScanCharge':scan,'remainingCharge':remaining}


def slots(count,candidate_size,result_size):
    if not count:
        return (0,0,0),(0,0,0)
    actual = add(record(checked(count*candidate_size)),record(checked(count*result_size)),
                 (0,checked(8*count),checked(4*count*candidate_size+2*count*result_size)))
    per_component = add(record(candidate_size),record(result_size),
                        (0,8,checked(4*candidate_size+2*result_size)))
    bound = multiply(per_component,count)
    assert all(actual[i]<=bound[i] for i in range(3))
    return actual,bound


cases = [representation(lengths,path) for lengths,path in (
    ([],0),([0],0),([1,5],12),([65536],32),([65537,200],400),([123]*128,25),([123]*10000,25))]
shared = [{'components':n,'actualSharedFee':slots(n,128,384)[0],
           'conservativeSumOfSlotBounds':slots(n,128,384)[1],
           'sizesSyntheticNotNative':True} for n in (0,1,2,10)]
overflow = []
for label,lengths,path in [('record-overflow',[MAXIMUM],1),('sum-overflow',[MAXIMUM//2+1]*2,1),
                           ('comparison-overflow',[1],MAXIMUM)]:
    try: representation(lengths,path)
    except ArithmeticError: overflow.append(label)
    else: raise AssertionError(('overflow accepted',label))
core = add(multiply(record(73),5),(0,128,2*5*73+2*16+128*32))
assert core == (5,128,5863)
result = {'scope':__doc__,'sourceMembersRehashed':len(inputs['files']),
          'abiAssumptionsNotMeasured':{'usizeBits':64,'vecHeaderBytes':24,'nodeAllowanceBytes':512},
          'cases':cases,'sharedSlotCases':shared,'overflowControls':overflow,
          'proposedReceiptOwnerCoreFee':core,'coreFeeNotAdmissionLedgerWork':True,
          'feeComputationStagedWithoutDoubleCharge':True,
          'completeProposedRepresentationMComputed':True,'implementedM':False,
          'nativeAbiMeasured':False,'completeAdmissionAComputed':False,'censusRun':False,
          'productionFitClaim':False,'nativeToolsRun':False,'unitAcceptance':False,'productQualification':False}
(BASE/'m-bound-arithmetic-report.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'M_cases':len(cases),'slotCases':len(shared),'overflowControls':len(overflow),
                  'coreFee':core,'implementedM':False,'completeAdmissionAComputed':False}))
