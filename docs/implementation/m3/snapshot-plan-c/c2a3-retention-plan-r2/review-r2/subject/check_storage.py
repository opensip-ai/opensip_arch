"""Source-anchored storage arithmetic only; no native ABI or allocation evidence."""
import hashlib
import json
from pathlib import Path
import re

BASE = Path(__file__).parent
inputs = json.loads((BASE/'INPUTS.json').read_text())
for row in inputs['files']:
    raw = (BASE/'inputs'/row['path']).read_bytes()
    assert len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256']
node = (BASE/'inputs/rust-1.95.0/alloc/btree/node.rs').read_text()
owned = (BASE/'inputs/product/crates/security/src/custody/discovery_walk.rs').read_text()
assert re.search(r'const B: usize = 6;',node)
assert 'const CAPACITY: usize = 2 * B - 1;' in node
assert 'edges: [MaybeUninit<BoxedNode<K, V>>; 2 * B]' in node
overhead = int(re.search(r'const RECORD: usize = (\d+);',owned)[1])
assert overhead == 128 and 'bytes: bytes.saturating_add(RECORD)' in owned


def rounded(value, alignment):
    return ((value + alignment - 1)//alignment)*alignment


def layout(pointer, fat_reference, parent_option, alignment):
    fields = [parent_option,2,2,11*fat_reference,11*fat_reference]
    leaf = rounded(sum(fields)+len(fields)*(alignment-1),alignment)
    internal = rounded(leaf+12*pointer,alignment)
    return {'leafUpperBytes':leaf,'internalUpperBytes':internal}


abi = {'pointer':8,'fat_reference':16,'parent_option':16,'alignment':8}
bound = layout(**abi)
assert bound == {'leafUpperBytes':408,'internalUpperBytes':504}
assert max(bound.values()) <= 512
assert layout(16,32,32,16)['internalUpperBytes'] > 512
assert layout(8,16,32,8)['internalUpperBytes'] > 512
assert 503 < bound['internalUpperBytes']
maximum = (1<<64)-1


def checked(value):
    if value < 0 or value > maximum:
        raise ArithmeticError('WorkBudgetError::Arithmetic (model only)')
    return value


def map_storage(files):
    # Product must use checked arithmetic before shared saturating prices.
    nodes = checked(files*2)
    one_record_bytes = checked(512+overhead)
    return {'objects':nodes,'edges':0,'bytes':checked(nodes*one_record_bytes)}


rows = []
for count in (0,1,2,11,12,127,10000):
    value = map_storage(count)
    assert value['objects'] == 2*count and value['bytes'] == 1280*count
    rows.append({'blobCount':count,'mapStorageOnly':value})
overflow = []
for count in ((1<<63),maximum//1280+1):
    try: map_storage(count)
    except ArithmeticError: overflow.append({'blobCount':count,'refusedArithmetic':True})
    else: raise AssertionError('overflow not refused')
report = {'scope':__doc__,'sourceMembersRehashed':len(inputs['files']),
          'abiAssumptionsNotMeasured':abi,'layoutUpperBoundUnderAssumptions':bound,
          'nodeAllowanceBytes':512,'ownedRecordOverhead':overhead,'cases':rows,
          'overflowControls':overflow,'wrongAbiAndLowerAllowanceRejectedByModel':True,
          'cumulativeNodeCountProof':'source argument in M-STORAGE-PROOF-r1.md, not an executed allocator control',
          'completeMComputed':False,'physicalFixtures':False,'nativeToolsRun':False,
          'nativeAbiMeasured':False,'censusRun':False,'productionFitClaim':False,
          'unitAcceptance':False,'productQualification':False}
(BASE/'storage-arithmetic-report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'storageCases':len(rows),'overflowControls':len(overflow),
                  'sourceMembersRehashed':len(inputs['files']),'completeMComputed':False}))
