from pathlib import Path
import hashlib,json
from registry_model import encode, MAX_ROWS, CAP, I64_MAX
A=Path('/Users/sb/code/opensip-ai/opensip_arch')
p=A/'docs/coop/design-corrections/security/security-lifecycle.schemas.v1.json'
s=json.loads(p.read_text())
names=[f'{i:08x}-0000-4000-8000-000000000000' for i in range(MAX_ROWS)]
j={'journalSchema':1,'kind':'installation-transition','intentDigest':'0'*64,'operation':'store-rollback','fromCoreClosure':'closure2:'+'0'*64,'toCoreClosure':'closure2:'+'1'*64,'fromStateSchema':2,'toStateSchema':1,'fromStoreGeneration':I64_MAX,'toStoreGeneration':I64_MAX-1,'platformProfileSetBodyDigest':'0'*64,'preconditionGeneration':I64_MAX,'rollbackDeadline':'9999-12-31T23:59:59Z','registryDigest':hashlib.sha256(encode(names)).hexdigest(),'registry':names,'affects':'all-registered','leaseSet':names,'state':'LEASED','fenceHeld':True,'writtenAfterAllLeasesHeld':True}
assert set(j)==set(s['schemas']['InstallationTransitionJournalV1']['required'])
rows=[]
for state in s['schemas']['InstallationTransitionJournalV1']['properties']['state']['enum']:
 j['state']=state
 wrapper={'slotSchema':1,'executionId':'exec1_'+'0'*32,'journalRef':'security.installation-transition-journal.v1:'+'0'*64,'journal':j}
 size=len(encode(wrapper));assert size <= CAP
 rows.append({'state':state,'bytes':size,'headroom':CAP-size})
r={'standing':'Representation bound only: fixed-width digest placeholders are not authenticated identity receipts or valid phase-specific journal authorization. No native publication or capacity qualification.', 'source':{'path':str(p.relative_to(A)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()},'nativeNamespaceCap':MAX_ROWS,'namespaceWidth':36,'bothListsFull':True,'longestOperation':'store-rollback','maxNumericDigits':19,'nullableDeadlineNonNullWidth':20,'states':rows,'maximumWrapperBytes':max(r['bytes'] for r in rows)}
o=Path(__file__).with_name('capacity-results.r1.json');assert not o.exists();o.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
