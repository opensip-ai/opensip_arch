"""Rebuild author reference exports from portable constructors against a frozen successor."""
from pathlib import Path
import argparse,json,hashlib,shutil,subprocess,concurrent.futures
p=argparse.ArgumentParser();p.add_argument('--old',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--work',type=Path,required=True);p.add_argument('--manifest',type=Path,required=True);p.add_argument('--version',type=int,required=True);a=p.parse_args();old=a.old.resolve();out=a.out.resolve();work=a.work.resolve();sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert not out.exists() and not work.exists();work.mkdir();raw=a.manifest.read_bytes();h=hashlib.sha256(raw).hexdigest();mf=json.loads(raw);source=Path(mf['snapshotRoot']);members={r['path']:r for r in mf['files']};prior=json.loads((old/'artifact-manifest.json').read_text())
for r in prior['files']:assert sha(old/r['path'])==r['sha256'] and (old/r['path']).stat().st_size==r['bytes']
for r in mf['files']:assert sha(source/r['path'])==r['sha256'] and (source/r['path']).stat().st_size==r['bytes']
PYTHON='/tmp/opensip-architecture-review-env/bin/python';commands=[]
def execute(name,args):
 cmd=[PYTHON,'-I','-B',str(old/name)]+[str(x) for x in args];proc=subprocess.run(cmd,capture_output=True,text=True,timeout=600);tag=name.removesuffix('.py');(work/(tag+'.stdout')).write_text(proc.stdout);(work/(tag+'.stderr')).write_text(proc.stderr);row={'name':name,'command':cmd,'exitCode':proc.returncode,'scriptSha256':sha(old/name)};(work/(tag+'.execution.json')).write_text(json.dumps(row,indent=2)+'\n');print(name,proc.returncode,flush=True);assert proc.returncode==0,row;return row
jobs=[('build-checkpoint3.py','checkpoint'),('build-normalized-examples6.py','normalized'),('build-rust-selection-examples.py','selection'),('build-binding-controls.py','binding')]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 futures=[pool.submit(execute,n,['--source',source,'--package',old,'--out',work/label]) for n,label in jobs]
 for f in futures:commands.append(f.result())
commands.append(execute('build-semantic-controls.py',['--source',source,'--package',old,'--out',work/'semantic','--positive',work/'checkpoint/checkpoint3']))
shutil.copytree(old,out,ignore=shutil.ignore_patterns('__pycache__'));hist=out/'historical-source28-preparation';hist.mkdir()
selected=['source-manifest.json','artifact-manifest.json','evaluation-residual-author-assessment.json','README.md','verify-package.py','checkpoint3','normalized-examples6','rust-selection-examples1','semantic-controls1','binding-controls','query-checks1','query-assessment.json','author-properties.json','mixed-universe-view.probe.json','root-replay-verification']+[q.name for q in out.glob('source-rebinding.v*.json')]
for n in selected:shutil.move(str(out/n),str(hist/n))
for n,rel in [('checkpoint3','checkpoint/checkpoint3'),('normalized-examples6','normalized/normalized-examples6'),('rust-selection-examples1','selection/rust-selection-examples1'),('semantic-controls1','semantic/semantic-controls1'),('binding-controls','binding')]:shutil.copytree(work/rel,out/n,ignore=shutil.ignore_patterns('__pycache__'))
(out/'source-manifest.json').write_bytes(raw);oldh=sha(old/'source-manifest.json');s=(old/'verify-package.py').read_text();assert s.count(oldh)==1;(out/'verify-package.py').write_text(s.replace(oldh,h))
j=json.loads((old/'evaluation-residual-author-assessment.json').read_text());j['subjectManifestSha256']=h;j['standing']=f'Root source{a.version}-bound author proposal only; prior packages preserved. All independent grades PENDING; no historical repair, application or qualification.';changes=[]
for row in j['items']:
 assert row['independentGrade']=='PENDING'
 for r in row['evidence']:
  before=r['sha256'];r.update(previousSha256=before,sha256=members[r['path']]['sha256'],resolveAgainst=f'frozen candidate{a.version}',currentIndependentAssessment='PENDING');r['sourceBytesChanged']=before!=r['sha256']
  if r['sourceBytesChanged']:changes.append({'id':row['id'],'path':r['path'],'previousSha256':before,'currentSha256':r['sha256']})
j['sourceSha256']=members[j['source']]['sha256'];(out/'evaluation-residual-author-assessment.json').write_text(json.dumps(j,indent=2)+'\n')
# Query/property probes consume this newly constructed package, not the old stored Runs.
def probe(name,args):
 cmd=[PYTHON,'-I','-B',str(out/name)]+[str(x) for x in args];proc=subprocess.run(cmd,capture_output=True,text=True,timeout=600);tag=name.removesuffix('.py');(work/(tag+'.stdout')).write_text(proc.stdout);(work/(tag+'.stderr')).write_text(proc.stderr);row={'name':name,'command':cmd,'exitCode':proc.returncode,'scriptSha256':sha(out/name)};commands.append(row);assert proc.returncode==0,row;print(name,proc.returncode,flush=True)
probe('check-author-query.py',['--source',source,'--package',out,'--out',work/'query-checks'])
probe('assess-author-query.py',['--input',work/'query-checks','--out',work/'query-assessment.json'])
probe('check-author-properties.py',['--source',source,'--package',out,'--out',work/'author-properties.json'])
probe('probe-mixed-universe-view.py',['--source',source,'--package',out,'--out',work/'mixed-universe-view.probe.json'])
shutil.copytree(work/'query-checks',out/'query-checks1')
for n in ['query-assessment.json','author-properties.json','mixed-universe-view.probe.json']:shutil.copy2(work/n,out/n)
comparison=[]
for group in ['checkpoint3','normalized-examples6','rust-selection-examples1','semantic-controls1','binding-controls']:
 for claim in json.loads((out/group/'claims.json').read_text()):
  path=claim['path'];oldclaims=json.loads((old/group/'claims.json').read_text());previous=next(r for r in oldclaims if r['name']==claim['name']);comparison.append({'group':group,'name':claim['name'],'previousRunId':previous['runId'],'runId':claim['runId'],'previousExportSha256':sha(old/group/path),'exportSha256':sha(out/group/path),'exportChanged':sha(old/group/path)!=sha(out/group/path)})
(out/'source-rebuild.v1.json').write_text(json.dumps({'standing':'Fresh portable author reconstruction, not label-only rebind. No independent acceptance or product qualification. Complete selected-owner replay required separately.','sourceManifestSha256':h,'parentPackageManifestSha256':sha(old/'artifact-manifest.json'),'nativeSchemaSha256':sha(source/'docs/coop/design-corrections/native/native-evidence.schemas.v2.json'),'commands':commands,'changedResidualSourceReferences':changes,'exportComparisons':comparison},indent=2)+'\n')
(out/'README.md').write_text(f'''# Source{a.version} rebuilt author reference package — review pending

This package contains seven positive synthetic Runs, three reminted semantic refusal controls, and three binding controls reconstructed from the bundled portable author constructors against frozen source{a.version}. The native schema digest changed, so the exports and query/property receipts were rebuilt. Source28 preparation and its exact previous exports are retained under historical-source28-preparation. The source manifest and artifact manifest bind current inputs. Fresh verification must separately execute both structural closure and complete semantic replay; no independent agreement is inferred from construction.

Only the TS checkpoint compares the partial author helper with the reference owner. The other six positive examples use the owner to derive and replay proof, establishing self-consistency. These examples exercise exists/none only. and/or/not remain unexercised; count-at-most/all-covered remain unimplemented in the partial helper. The attempted two-binding construction is incomplete and demonstrates no owner defect; the explicit-selection control is single-binding only. Shared TCB assumptions remain explicit on the thirteen attributed residual rows. None of this qualifies extraction by a compiler, hostile in-process code containment, storage performance, or product behavior.

The portable constructors take --source, --package and a fresh --out outside every input. build-semantic-controls additionally requires --positive pointing at freshly built checkpoint3. The complete construction commands and export changes are in source-rebuild.v1.json. Query/property receipts were measured using these new exact exports. Whole transport equality with historical packages is not claimed; unreferenced blobs grant no input authority. The current thirty-row author assessment has final-source rationale pins and PENDING independent grades. Earlier review and custody records describe their historical subjects, not acceptance of this package.

The original 123/8/3 blind charter remains unchanged. Never supply this author package or its outputs to a consumer described as blind. Independent design review, blind reconstruction, final application review and readiness reconciliation remain required. No product implementation, commit or push is authorized by this package.
''')
rows=[{'path':str(p.relative_to(out)),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(out.rglob('*')) if p.is_file() and p!=out/'artifact-manifest.json'];(out/'artifact-manifest.json').write_text(json.dumps({'standing':f'Source{a.version} freshly reconstructed author reference package; independent review pending.','sourceManifestSha256':h,'files':rows},indent=2)+'\n');(work/'preparation.json').write_text(json.dumps({'package':str(out),'manifestSha256':sha(out/'artifact-manifest.json'),'files':len(rows),'sourceManifestSha256':h,'exports':len(comparison)},indent=2)+'\n');print((work/'preparation.json').read_text())
