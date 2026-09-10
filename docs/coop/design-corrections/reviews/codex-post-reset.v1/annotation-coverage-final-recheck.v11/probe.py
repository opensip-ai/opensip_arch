from pathlib import Path
import argparse,copy,hashlib,importlib.util,json,shutil
p=argparse.ArgumentParser();p.add_argument('--cause',required=True);a=p.parse_args();root=Path.cwd();dc=root/'docs/coop/design-corrections';out=dc/'reviews/codex-post-reset.v1/annotation-coverage-final-recheck.v11';assert not out.exists()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();h=json.loads((dc/'reviews/digest-corrections-author.v9/handoff.json').read_text());owned=h['ownedFilesChanged'];assert (dc/'reviews/digest-corrections-author.v9/custody.json').exists()
for row in owned:assert sha(root/row['path'])==row['sha256']
source=dc/'foundation/identity-model.py';spec=importlib.util.spec_from_file_location('codex_annotation_final',source);M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)
def trial(name,doc=None):
 try:M.relation_annotation_closure(name,doc);return {'admitted':True}
 except Exception as exc:return {'admitted':False,'exception':type(exc).__name__,'cause':str(exc)}
controls={name:trial(name) for name in sorted(M.RELATIONS)};vectors=[]
for name in sorted(M.RELATIONS):
 for kind in ('DigestHex','CanonicalPath','Sha256Text'):
  doc=copy.deepcopy(M.RELATION_DOCUMENT);sel=doc['x-opensip-relation-registry']['relations'][name]['selector'].split('/')[-1]
  doc['$defs'][sel]['properties']['strayUnannotated']={'$ref':'#/$defs/'+kind}
  result=trial(name,doc);result.update(id=name+'-'+kind,intendedCause=a.cause,reachedIntendedCause=not result['admitted'] and a.cause in result.get('cause',''));vectors.append(result)
removed=copy.deepcopy(M.RELATION_DOCUMENT);removed['$defs']['ClonesPayloadV1']['properties']['bodyIdentity'].pop('x-opensip-digest');r=trial('clones',removed);r.update(id='removed-existing-bodyIdentity-annotation',intendedCause=a.cause,reachedIntendedCause=not r['admitted'] and a.cause in r.get('cause',''));vectors.append(r)
doc=copy.deepcopy(M.RELATION_DOCUMENT);doc['$defs']['FilePayloadV1']['properties']['byteLength']['x-opensip-digest']={'representation':'raw-artifact','retention':'preimage'};doc['x-opensip-relation-registry']['relations']['file']['snapshotJoins'][0].pop('lengthField');limb1=trial('file',doc)
doc=copy.deepcopy(M.RELATION_DOCUMENT);doc['x-opensip-relation-registry']['relations']['file']['snapshotJoins'][0]['anchorPathField']='inventedField';limb2=trial('file',doc)
passed=all(x['admitted'] for x in controls.values()) and all(x['reachedIntendedCause'] for x in vectors) and 'RELATION_DIGEST_LAW_RESIDUE' in limb1.get('cause','') and 'RELATION_JOIN_FIELD_UNKNOWN' in limb2.get('cause','')
out.mkdir();captured=[]
for row in owned:
 q=out/'source-delta'/row['path'];q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(root/row['path'],q);captured.append(dict(row,capturedPath=str(q.relative_to(out))))
shutil.copyfile(__file__,out/'probe.py');(out/'result.json').write_text(json.dumps({'standing':'Codex final-source verification of the independent v9-S1 construction; schema/reference validator evidence, not a complete Run or independent acceptance or product qualification.','baseManifestSha256':'288ac21453b635115b833935386ca5d65dbb6f482f51e078b118ffefb3ac1249','sourceDelta':captured,'originalReview':'reviews/post-reset-review.v9/review.json#/newShouldIssues/0','originalProbe':'reviews/post-reset-review.v9/probes/p04_third_limb.py','controls':controls,'vectors':vectors,'preservedLimb1':limb1,'preservedLimb2':limb2,'passed':passed},indent=2)+'\n')
assert passed,'Final source recheck failed; exact source/results retained, do not overwrite'
print('13 real-selector controls pass; 39 injected fields and one removed annotation reject at intended cause; both existing residue limbs preserved.')
