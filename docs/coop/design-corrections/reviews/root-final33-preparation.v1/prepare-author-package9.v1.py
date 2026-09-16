from pathlib import Path
import json,hashlib,shutil
B=Path('/tmp/opensip-design-corrections');L=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews');old=B/'claude-author-package-successor.v8';out=B/'claude-author-package-successor.v9';mf=L/'candidate-subject.v33.json';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert not out.exists();m=json.loads(mf.read_bytes());h=sha(mf);S=Path(m['snapshotRoot']);members={r['path']:r for r in m['files']}
for row in json.loads((old/'artifact-manifest.json').read_bytes())['files']:assert sha(old/row['path'])==row['sha256'] and (old/row['path']).stat().st_size==row['bytes']
assert sha(S/'docs/coop/design-corrections/native/native-evidence.schemas.v2.json')==json.loads((old/'source-rebuild.v1.json').read_bytes())['nativeSchemaSha256']
shutil.copytree(old,out,ignore=shutil.ignore_patterns('__pycache__'));H=out/'historical-source32-preparation';H.mkdir()
for n in ['source-manifest.json','artifact-manifest.json','README.md','verify-package.py','evaluation-residual-author-assessment.json','source-binding.v32.json']:shutil.copy2(out/n,H/n)
(out/'source-manifest.json').write_bytes(mf.read_bytes());p=out/'verify-package.py';s=p.read_text();assert s.count(sha(old/'source-manifest.json'))==1;p.write_text(s.replace(sha(old/'source-manifest.json'),h))
p=out/'evaluation-residual-author-assessment.json';j=json.loads(p.read_bytes());j['subjectManifestSha256']=h;j['standing']='Source33-bound author proposal only; all independent grades PENDING. No historical repair, application or qualification.'
for row in j['items']:
 assert row['independentGrade']=='PENDING'
 for r in row['evidence']:
  before=r['sha256'];r.update(previousSha256=before,sha256=members[r['path']]['sha256'],resolveAgainst='frozen candidate33',currentIndependentAssessment='PENDING',sourceBytesChanged=before!=members[r['path']]['sha256'])
j['sourceSha256']=members[j['source']]['sha256'];p.write_text(json.dumps(j,indent=2)+'\n')
(out/'source-binding.v33.json').write_text(json.dumps({'standing':'Current source33 binding of exact historical source30-constructed exports. Native schema unchanged. New current-source complete replay/query verification and independent assessment are required; no old execution is relabelled.','sourceManifestSha256':h,'parentPackageManifestSha256':sha(old/'artifact-manifest.json'),'constructionAccount':'source-rebuild.v1.json','constructionSourceVersion':30,'currentVerificationSourceVersion':33,'exportsChanged':False,'productQualification':False},indent=2)+'\n')
(out/'README.md').write_text('''# Source33 author reference package — review pending

The seven synthetic positives, three reminted semantic negatives and three binding controls retain their exact source30 construction bytes. source-rebuild.v1.json is the historical construction receipt; source-binding.v33.json is the separate current binding. Earlier preparation and assessments are preserved unchanged under their historical paths. Current source verification remains required.

Run the reference interpreter with `-I -B verify-package.py --source <frozen-source33> --out <new-external-output>`. It verifies exact source/package hashes, executes structural and full semantic closure on all thirteen cases, then reproduces and asserts seven query checks. Property and mixed-universe probes remain separate: check-author-properties.py and probe-mixed-universe-view.py take --source/--package/--out. Prior execution does not imply current execution.

Evidence limits remain: only the TypeScript checkpoint compares a consumer helper with the owner; six other positives are owner-derived/replayed self-consistency. The helper exercises exists/none; and/or/not are unexercised and count-at-most/all-covered are unimplemented. The two-binding construction is incomplete and retains a single explicit binding. Synthetic records qualify no compiler/provider/OS/process-isolation boundary. This package contains author-assisted reference evidence, never blind acceptance or final application approval. All thirty independent residual grades remain PENDING.
''')
for group in ['checkpoint3','normalized-examples6','rust-selection-examples1','semantic-controls1','binding-controls']:
 for p in (old/group).glob('*.store.json'):assert (out/group/p.name).read_bytes()==p.read_bytes()
rows=[{'path':p.relative_to(out).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(out.rglob('*')) if p.is_file() and p!=out/'artifact-manifest.json'];(out/'artifact-manifest.json').write_text(json.dumps({'standing':'Source33-bound author reference evidence, independent review pending.','sourceManifestSha256':h,'files':rows},indent=2)+'\n');print(json.dumps({'files':len(rows),'artifactManifestSha256':sha(out/'artifact-manifest.json'),'sourceManifestSha256':h}))
