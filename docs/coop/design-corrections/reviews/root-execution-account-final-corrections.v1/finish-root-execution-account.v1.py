"""Small root review corrections AFTER actual Claude v2 completes and is retained.
No acceptance, pin change, freeze or product implementation. Preserve exact beforeimages.
"""
from pathlib import Path
import hashlib,json,shutil,difflib
B=Path('/tmp/opensip-design-corrections');S=B/'execution-account-successor.v1/source';A=B/'claude-execution-account-author.v2';O=B/'root-execution-account-final-corrections.v1'
L=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews')
sha=lambda b:hashlib.sha256(b).hexdigest()
assert json.loads((A/'process-completion.json').read_bytes())['exitCode']==0
assert json.loads((A/'result.json').read_bytes()).get('is_error') is not True
assert (L/A.name/'final-public-artifact-manifest.json').is_file(),'Retain the exact completed author evidence first'
assert not O.exists()
for r in json.loads((A/'after-hashes.json').read_bytes()):
 raw=(S/r['path']).read_bytes();assert sha(raw)==r['sha256'] and len(raw)==r['bytes'],r['path']
base='docs/coop/design-corrections/foundation/'
changes={}
def edit(name,old,new):
 p=base+name;s=changes.get(p,(S/p).read_text());assert s.count(old)==1,(name,old[:120],s.count(old));changes[p]=s.replace(old,new)
edit('execution-inputs-contract.v1.md',
 'envelope still makes the row `unavailable` — and the candidate source item and its\n`candidate-producer-result` ref are still retained. Only the invented carrier is gone.',
 'envelope still makes the row `unavailable` — and the candidate source item is retained. An\nexisting envelope keeps its originating `candidate-producer-result` ref; an absent envelope\ncontributes no invented ref. Only the invented carrier is gone.')
edit('execution-inputs.schema.v1.json',
 'Row state and the retained candidate-producer-result ref are unchanged.',
 'Row state is unchanged. An existing envelope keeps its originating candidate-producer-result ref; an absent envelope contributes no invented ref.')
edit('check-execution-inputs.v1.py',
 '        admission = admit(manifest_from_owner(F.build_file_inputs(atom_override=NONE_ATOM, **kwargs)))',
 '        admission_inputs = manifest_from_owner(F.build_file_inputs(atom_override=NONE_ATOM, **kwargs))\n        admission = admit(admission_inputs)\n        admission_digest = M.raw_digest(admission_inputs["execution_inputs"])')
edit('check-execution-inputs.v1.py',
 '    bad = []\n    if result["verdict"] != want_verdict:',
 '    bad = []\n    if admission_digest != proof["executionInputsDigest"]:\n        bad.append({"executionInputsDigestMismatch": {"admission": admission_digest,\n                    "proof": proof["executionInputsDigest"]}})\n    if result["verdict"] != want_verdict:')
edit('check-execution-inputs.v1.py',
 '            "sameGraphAdmissionResult": admission.get("result"),',
 '            "sameGraphAdmissionResult": admission.get("result"),\n            "sameGraphExecutionInputsDigest": admission_digest,\n            "proofExecutionInputsDigest": proof["executionInputsDigest"],')
edit('check-execution-inputs.v1.py',
 '    `bridgedCausesEqualProof` checks the re-run admission really is the Run\'s, by bridging those\n    rows with §9.6 step 3 and comparing to the proof\'s own causes.',
 '    The separately rebuilt reference fixture must produce the exact ExecutionInputs digest\n    named by the closed proof. This byte binding identifies the admission columns with that\n    Run; bridging their causes with §9.6 adds a separate projection check. Both builders reuse\n    the reference model and this remains reference self-consistency, not a blind reconstruction.')
edit('check-execution-inputs.v1.py',
 '    `EXECUTION_INPUTS_CANDIDATE_REQUIRED` before that matters.\n    """\n    kw = copy.deepcopy(owner)',
 '    `EXECUTION_INPUTS_CANDIDATE_REQUIRED` before that matters.\n\n    Bounded ExecutionInputs join fixture only: the changed Plan/analysis-spec is not reminted\n    through structural closure here. This function is not a full-Run reachability control.\n    """\n    kw = copy.deepcopy(owner)')
for rel,s in changes.items():
 if rel.endswith('.py'):compile(s,rel,'exec')
 if rel.endswith('.json'):json.loads(s)
O.mkdir();rows=[]
for rel,s in changes.items():
 p=S/rel;old=p.read_bytes();new=s.encode();q=O/'before'/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(old)
 q=O/'after'/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(new)
 (O/(Path(rel).name+'.diff')).write_text(''.join(difflib.unified_diff(old.decode().splitlines(True),s.splitlines(True),fromfile='claude2/'+rel,tofile='root/'+rel)))
 p.write_bytes(new);rows.append({'path':rel,'beforeSha256':sha(old),'afterSha256':sha(new),'bytes':len(new)})
(O/'changes.json').write_text(json.dumps({'standing':'Root review corrections only; final authoritative checks and independent review pending. No semantic outcome change intended.','changes':['Make candidate ref retention conditional on an actual envelope','Bind full-Run checker admission columns to the exact proof ExecutionInputs digest','Label candidate helper as bounded join rather than full-Run reachability'],'files':rows},indent=2)+'\n')
shutil.copy2(Path(__file__),O/Path(__file__).name)
print('Applied root review corrections',len(rows),'files; final checks required')
