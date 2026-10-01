import hashlib, importlib.util, json, sys
from pathlib import Path
W = Path('/Users/sb/code/opensip-ai/opensip'); A = Path('/Users/sb/code/opensip-ai/opensip_arch')
spec = importlib.util.spec_from_file_location('vd', W / 'tools/verify_design.py'); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
M='docs/implementation/m2/'
def pinb(p,b): return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def pin(p): return pinb(p,(A/p).read_bytes())
v80, v81 = pin(M+'repository-file-inventory.v80.json'), pin(M+'repository-file-inventory.v81.json')
inv81 = json.loads((A/v81['path']).read_text()); inv80=json.loads((A/v80['path']).read_text())
NEW='PROBE new read_premise description'
variant = sys.argv[1]
if variant=='v81-direct':
    parent=v81; idx=[i for i,f in enumerate(inv81['files']) if f['path'].endswith('custody/read_premise.rs')][0]; before=inv81['files'][idx]['description']
elif variant=='control':
    parent=v81; idx=[i for i,f in enumerate(inv81['files']) if f['path']=='crates/security/src/custody.rs'][0]; before=inv81['files'][idx]['description']
elif variant=='v80-supersede':
    parent=v80; idx=250; s461=json.loads((A/(M+'stale-descriptions-461b/successor.json')).read_text())
    before=[o for o in s461['passageOverrides'] if o['selector']['jsonPointer']=='/files/250/description'][0]['after']
CAND=b'probe readme\n'; CANDP=pinb('SCRATCH-X1B/README.md',CAND)
rec = json.dumps({'schemaVersion':1,'standing':'PROBE','parents':[parent],'passageOverrides':[{'parent':parent,'selector':{'jsonPointer':f'/files/{idx}/description'},'before':before,'after':NEW}],'candidates':[CANDP]}).encode()
rpin_rec = pinb('SCRATCH-X1B/successor.json', rec)
subj = json.dumps({'schemaVersion':1,'files':[CANDP,rpin_rec]}).encode(); spin=pinb('SCRATCH-X1B-subject.json',subj)
review = json.dumps({'verdict':'ACCEPT-DESIGN-UNIT','requiredFindings':[],'subjectManifestSha256':spin['sha256']}).encode(); rvp=pinb('SCRATCH-X1B/review.json',review)
assent = json.dumps({'status':'ACCEPTED-DESIGN-UNIT','rootSubstantiveAssent':True,'requiredUnitFindings':[],'subjectManifest':spin,'independentReview':rvp,'acceptedSuccessor':rpin_rec}).encode(); ap=pinb('SCRATCH-X1B/assent.json',assent)
synthetic={CANDP['path']:CAND, rpin_rec['path']:rec, spin['path']:subj, rvp['path']:review, ap['path']:assent}
real=m.pinned_bytes
def pinned_bytes(root,row):
    if isinstance(row,dict) and row.get('path') in synthetic: return synthetic[row['path']]
    return real(root,row)
m.pinned_bytes=pinned_bytes
lock=json.loads((W/'design-lock.json').read_text())
lock['contractSuccessors'].append({'record':rpin_rec,'subjectManifest':spin,'review':rvp,'assent':ap})
try:
    r=m.verify(A,lock,W); print(variant,'PASSED', r.get('passed'))
except Exception as e: print(variant,'REFUSED:',type(e).__name__, e)
