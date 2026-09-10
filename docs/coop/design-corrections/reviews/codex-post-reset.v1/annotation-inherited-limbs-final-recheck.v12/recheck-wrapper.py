from pathlib import Path
import hashlib,json
root=Path.cwd();dc=root/'docs/coop/design-corrections';retained=dc/'reviews/digest-corrections-author.v10';assert (retained/'custody.json').exists();h=json.loads((retained/'handoff.json').read_text())
for row in h['ownedFilesChanged']:assert hashlib.sha256((root/row['path']).read_bytes()).hexdigest()==row['sha256']
p=dc/'reviews/codex-post-reset.v1/annotation-inherited-limbs-draft-counterexample.v10/probe.py';s=p.read_text().replace('annotation-inherited-limbs-draft-counterexample.v10','annotation-inherited-limbs-final-recheck.v12').replace('draft schema/reference inherited-annotation consistency counterexample','final-source schema/reference inherited-annotation consistency recheck').replace('identity-model.draft.py','identity-model.final.py')
launch=Path('/tmp/opensip-design-corrections/annotation-inherited-limbs-final-launch.v12');launch.mkdir(exist_ok=False);adapted=launch/'adapted-probe.py';adapted.write_text(s);exec(compile(s,str(adapted),'exec'),{'__file__':str(adapted),'__name__':'codex_final_inherited_limbs'})
out=dc/'reviews/codex-post-reset.v1/annotation-inherited-limbs-final-recheck.v12';d=json.loads((out/'result.json').read_text());checks=[]
for row in d['vectors']:
 result=row['admission'];token={'preimage':'RELATION_DIGEST_LAW_RESIDUE','invented-retention':'RELATION_DIGEST_RETENTION','not-joined':None}[row['retention']]
 ok=result['admitted'] if token is None else not result['admitted'] and token in result.get('cause','');checks.append({'id':row['id'],'expectedCause':token,'passed':ok})
passed=all(c['passed'] for c in checks);(out/'recheck-wrapper.py').write_bytes(Path(__file__).read_bytes());(out/'recheck-assessment.json').write_text(json.dumps({'standing':'Codex rerun of own nine schema/reference coherence controls on captured final source; not a Run attack or independent acceptance','checks':checks,'passed':passed},indent=2)+'\n');assert passed,'Final-source inherited-limb recheck failed; results retained, do not overwrite';print('All nine field/alias/branch coherence cases match intended retention/join refusals and lawful exemptions.')
