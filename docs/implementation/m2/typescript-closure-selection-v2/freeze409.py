from pathlib import Path
import json,hashlib
A=Path('/Users/sb/code/opensip-ai/opensip_arch');M=A/'docs/implementation/m2';OLD=M/'typescript-closure-selection-v1';U=M/'typescript-closure-selection-v2';S=M/'typescript-closure-selection-v2-subject.json';assert not U.exists()and not S.exists();U.mkdir()
def pin(p):
 b=p.read_bytes();return {'path':str(p.relative_to(A)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
old=json.loads((OLD/'successor.json').read_text());assert [r['path']for r in old['parents']]!=sorted(r['path']for r in old['parents'])
(U/'README.md').write_text('''# TypeScript closure successor ordering correction409

The actual408 review accepted the one-row repair, but root's fresh private design verifier correctly refused the successor because its three parent pins were not sorted by path. This occurred before dependency materialization, lane execution or any live write. Product remains clean7e1e18b35/55. Preserve original408 candidate/review/root assessment and failed staging evidence;408was not selected.

This corrected successor sorts the exact same three parent records and preserves all eight original408 candidate bytes at their original immutable paths. Its subject additionally includes this correction README and freeze script. Cross-directory candidate paths are intentional immutable reuse, not edits or evidence that408was selected. No checker, lane registry, map, policy, dependency or executable bytes change relative to408. The original one-row registry correction remains the entire prospective product change.

Actual independent review/root assent and private selected-design/public-lane execution still precede live materialization. The reference checker explicitly requires sorted unique parent paths, as well as candidate and subject paths. This package claims no lane execution or product qualification. Root and actual408 review both missed this mechanical ordering requirement; the verifier caught it without permitting live changes.
''')
(U/'freeze409.py').write_bytes(Path(__file__).read_bytes())
parents=sorted(old['parents'],key=lambda r:r['path']);assert len({r['path']for r in parents})==3
candidates=sorted([*old['candidates'],pin(U/'README.md'),pin(U/'freeze409.py')],key=lambda r:r['path']);save(U/'successor.json',{'schemaVersion':1,'standing':'PROPOSED corrected parent ordering for exact TypeScript closure repair; original408unselected.','parents':parents,'passageOverrides':[],'candidates':candidates});save(S,{'schemaVersion':1,'files':sorted([*candidates,pin(U/'successor.json')],key=lambda r:r['path'])});print(json.dumps({'subject':pin(S),'members':len(candidates)+1,'reusedOriginalCandidates':8,'sortedParents':3},indent=2))
