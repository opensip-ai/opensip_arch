from pathlib import Path
import json,hashlib
A=Path('/Users/sb/code/opensip-ai/opensip_arch');M=A/'docs/implementation/m2';T=Path('/tmp/opensip-implementation');D=T/'typescript-closure408';U=M/'typescript-closure-selection-v1';S=M/'typescript-closure-selection-v1-subject.json';assert not U.exists()and not S.exists();U.mkdir()
def pin(p):
 b=p.read_bytes();return {'path':str(p.relative_to(A)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
for src,rel in [(D/'typescript-lanes.json','product/tools/typescript-lanes.json'),(D/'audit.json','evidence/audit.json'),(D/'preflight.stdout','evidence/preflight.stdout'),(D/'preflight.stderr','evidence/preflight.stderr')]:
 p=U/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(src.read_bytes())
old=A/'docs/implementation/m1/bootstrap-selection-v1/product/tools/typescript-lanes.json';new=U/'product/tools/typescript-lanes.json';a=json.loads(old.read_bytes());b=json.loads(new.read_bytes());before=a['files'];after=b['files'];assert len(before)==len(after)==160;changed=[i for i,(x,y)in enumerate(zip(before,after))if x!=y];assert len(changed)==1;i=changed[0];assert before[i]['path']==after[i]['path']=='tools/verify_design.py';aa=dict(a);bb=dict(b);aa.pop('files');bb.pop('files');assert aa==bb
save(U/'delta.json',{'onlyChangedRowIndex':i,'before':before[i],'after':after[i],'other159RowsUnchanged':True,'nodePinLaneRecordsAndPoliciesUnchanged':True,'productTarget':'tools/typescript-lanes.json','authorTests':'Public entrypoint current failure reproduced before child execution; actual selected lane runs owed after acceptance.','standing':'Exact maintenance-input correction, not broader checker/toolchain qualification.'})
save(U/'materialization-map.json',{'schemaVersion':1,'files':[{'productPath':'tools/typescript-lanes.json','candidatePath':str(new.relative_to(A)),'before':{k:pin(old)[k]for k in ('bytes','sha256')},'after':{k:pin(new)[k]for k in ('bytes','sha256')}}]})
(U/'README.md').write_text('''# TypeScript maintenance checker input binding

Proposed exact correction of a stale maintenance closure row. The public check_typescript.py entrypoint currently refuses tools/verify_design.py before starting a child: its160-file registry pins28690B/76d7f509..., while the separately accepted and live checker is33654B/2764cf7b.... Both files predate current initialization changes. This unit changes only that one row's byte count and SHA-256 to the actual selected admission-runtime checker. The other159 rows, executable pin, lane records, source roots, policies and checker code remain identical. No validation is removed and no local self-hash grants approval.

The registry remains subject to exact accepted-unit membership in check_typescript.py. Actual review/root assent and private selected preflight are required before live replacement. The public maintenance lanes must then run; this unit does not claim they already pass, and any further child failure must be reported and resolved without weakening admission. This is independent of initialization/native creator authority and carries no release/whole-M2 qualification. No package provisioning, tool rebuild, product API, file inventory or dependency change.
''')
(U/'evidence/freeze408.py').write_bytes(Path(__file__).read_bytes())
parents=[pin(old),pin(A/'docs/implementation/m2/admission-runtime-selection-v1/product/tools/verify_design.py'),pin(A/'docs/implementation/m1/bootstrap-selection-v1/successor.json')]
candidates=[pin(p)for p in sorted(U.rglob('*'))if p.is_file()];save(U/'successor.json',{'schemaVersion':1,'standing':'PROPOSED one-row TypeScript maintenance closure correction; no lane success or qualification inferred.','parents':parents,'passageOverrides':[],'candidates':candidates});save(S,{'schemaVersion':1,'files':sorted([*candidates,pin(U/'successor.json')],key=lambda r:r['path'])});print(json.dumps({'subject':pin(S),'members':len(candidates)+1},indent=2))
