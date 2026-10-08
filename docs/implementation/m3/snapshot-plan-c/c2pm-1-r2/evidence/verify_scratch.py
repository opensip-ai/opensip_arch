"""Read-only in-memory binding-structure diagnostic, not independent assent.

Run after the exact successor and subject are frozen. Synthetic review/assent
exist in memory at SCRATCH-C2PM1 paths ONLY; never write them to either repo or
use them in a committed lock. This checks the actual current verify_design
against the real baseline and one proposed successor. No Cargo or product
runtime is executed.
"""
from pathlib import Path
import json,hashlib,copy,importlib.util
D=Path(__file__).resolve().parents[1]; STAGE=D.parents[4]; A=Path('/Users/sb/code/opensip-ai/opensip_arch'); P=A.parent/'opensip'; REL='docs/implementation/m3/snapshot-plan-c/c2pm-1-r2'
spec=importlib.util.spec_from_file_location('verify_design',P/'tools/verify_design.py'); vd=importlib.util.module_from_spec(spec);spec.loader.exec_module(vd)
lock=json.loads((P/'design-lock.json').read_text()); base=vd.verify(A,lock,P)
memory={}
def row(rel,b):return {'path':rel,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
for file in STAGE.rglob('*'):
 if file.is_file():memory[file.relative_to(STAGE).as_posix()]=file.read_bytes()
def pin(rel):return row(rel,memory[rel])
subject=pin(REL+'-subject.json');record=pin(REL+'/successor.json');document=json.loads(memory[record['path']]);named=[e['supersedes'] for e in document['passageSupersessions']]
review={'verdict':'ACCEPT-DESIGN-UNIT','requiredFindings':[],'subjectManifestSha256':subject['sha256'],'supersededPassages':named,'standing':'SYNTHETIC IN-MEMORY STRUCTURE CHECK ONLY; NO ACTUAL REVIEW OR ASSENT'}
memory['SCRATCH-C2PM1/review.json']=json.dumps(review).encode();rp=pin('SCRATCH-C2PM1/review.json')
assent={'status':'ACCEPTED-DESIGN-UNIT','rootSubstantiveAssent':True,'requiredUnitFindings':[],'subjectManifest':subject,'independentReview':rp,'acceptedSuccessor':record,'standing':'SYNTHETIC IN-MEMORY STRUCTURE CHECK ONLY'}
memory['SCRATCH-C2PM1/assent.json']=json.dumps(assent).encode();ap=pin('SCRATCH-C2PM1/assent.json')
real=vd.pinned_bytes
def overlay(root,r):
 if r.get('path') in memory:
  b=memory[r['path']];assert row(r['path'],b)==r;return b
 return real(root,r)
vd.pinned_bytes=overlay
future=copy.deepcopy(lock);future['contractSuccessors'].append({'record':record,'subjectManifest':subject,'review':rp,'assent':ap});result=vd.verify(A,future,P)
assert result['passed'] and base['passed'];assert len(result['contractSuccessors'])==133 and len(base['contractSuccessors'])==132
assert result['selectedInventory']==base['selectedInventory'] and result['inventoryPassageInheritance']==base['inventoryPassageInheritance']
mine=result['contractSuccessors'][-1];assert len(mine['passageOverrides'])==7 and len(mine['passageSupersessions'])==1
print(json.dumps({'standing':'IN-MEMORY STRUCTURE CHECK; ACTUAL REVIEW/ASSENT STILL REQUIRED','passed':True,'baseContractSuccessors':132,'proposedContractSuccessors':133,'inventoryUnchanged':167,'passageOverrides':7,'contractPassageSupersessions':1,'subjectManifestSha256':subject['sha256'],'productRuntimeExecuted':False,'productQualification':False},indent=2))
