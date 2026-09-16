from pathlib import Path
import json,hashlib,shutil
B=Path('/tmp/opensip-design-corrections');R=Path('/Users/sb/code/opensip-ai/opensip_arch');old=B/'claude-author-package-successor.v6';out=B/'claude-author-package-successor.v7';mf=R/'docs/coop/design-corrections/reviews/candidate-subject.v31.json';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert not out.exists();h=sha(mf);m=json.loads(mf.read_text());source=Path(m['snapshotRoot']);members={r['path']:r for r in m['files']};prior=json.loads((old/'artifact-manifest.json').read_text())
for r in prior['files']:assert sha(old/r['path'])==r['sha256'] and (old/r['path']).stat().st_size==r['bytes']
assert sha(source/'docs/coop/design-corrections/native/native-evidence.schemas.v2.json')==json.loads((old/'source-rebuild.v1.json').read_text())['nativeSchemaSha256']
shutil.copytree(old,out,ignore=shutil.ignore_patterns('__pycache__'));hist=out/'historical-source30-preparation';hist.mkdir()
for n in ['source-manifest.json','artifact-manifest.json','README.md','verify-package.py','evaluation-residual-author-assessment.json','source-rebuild.v1.json']:shutil.copy2(out/n,hist/n)
(out/'source-manifest.json').write_bytes(mf.read_bytes());s=(out/'verify-package.py').read_text();oldh=sha(old/'source-manifest.json');assert s.count(oldh)==1;s=s.replace(oldh,h);needle="result={'standing':";assert s.count(needle)==1;idx=s.index(needle)
addition='''# Query reproduction is a separate measured boundary, now part of package verification.
query_commands = [
 [sys.executable,'-I','-B',str(ROOT/'check-author-query.py'),'--source',str(a.source),
  '--package',str(ROOT),'--out',str(a.out/'query-checks')],
 [sys.executable,'-I','-B',str(ROOT/'assess-author-query.py'),'--input',str(a.out/'query-checks'),
  '--out',str(a.out/'query-assessment.json')],
]
for index,cmd in enumerate(query_commands):
 proc=subprocess.run(cmd,capture_output=True,text=True,timeout=600)
 (a.out/('query-step-%d.stdout' % index)).write_text(proc.stdout)
 (a.out/('query-step-%d.stderr' % index)).write_text(proc.stderr)
 assert proc.returncode==0,{'command':cmd,'exitCode':proc.returncode}
query=json.loads((a.out/'query-assessment.json').read_text())
assert query['passed'] is True and len(query['checks'])==7
results.append({'group':'query','negativeControls':None,'passed':True,'count':len(query['checks']),
                'reportSha256':sha(a.out/'query-assessment.json')})
print('query',True,flush=True)
'''
s=s[:idx]+addition+s[idx:];(out/'verify-package.py').write_text(s)
j=json.loads((out/'evaluation-residual-author-assessment.json').read_text());j['subjectManifestSha256']=h;j['standing']='Root source31-bound author proposal only. All independent grades PENDING; no historical repair, application or qualification.'
for row in j['items']:
 assert row['independentGrade']=='PENDING'
 for r in row['evidence']:
  before=r['sha256'];r.update(previousSha256=before,sha256=members[r['path']]['sha256'],resolveAgainst='frozen candidate31',currentIndependentAssessment='PENDING');r['sourceBytesChanged']=before!=r['sha256']
j['sourceSha256']=members[j['source']]['sha256'];(out/'evaluation-residual-author-assessment.json').write_text(json.dumps(j,indent=2)+'\n')
# Preserve the exact source30 construction account in place AND in the historical directory.
# Current binding is separate: it does not pretend those historical commands used source31.
(out/'source-binding.v31.json').write_text(json.dumps({'standing':'Current source31 binding. Exact Runs were freshly constructed against30 and are byte-identical here; native schema and selected semantic constructor inputs did not change31. Full source31 replay/query verification and actual independent assessment remain required.','sourceManifestSha256':h,'parentPackageManifestSha256':sha(old/'artifact-manifest.json'),'constructionAccount':'source-rebuild.v1.json','constructionSourceVersion':30,'currentVerificationSourceVersion':31,'exportsChanged':False,'queryVerificationChange':'verify-package now executes query reproduction plus all seven query assertions after the thirteen Run/control outcomes; no consumer code is imported.','productQualification':False},indent=2)+'\n')
readme=(old/'README.md').read_text();readme=readme.replace('# Source30 rebuilt author reference package — review pending','# Source31 author reference package — review pending');readme=readme.replace('against frozen source30.', 'against frozen source30, then preserved byte-identically for current frozen source31 verification.');readme=readme.replace('Fresh verification must separately execute both structural closure and complete semantic replay;', 'verify-package.py executes structural closure and complete semantic replay for all thirteen outcomes, then regenerates and asserts all seven query checks;');readme+='''\nCurrent source binding is source-binding.v31.json. source-rebuild.v1.json is the original source30 construction receipt, not a claim that its commands ran against31. Historical source30 preparation is preserved unchanged. Run `python -I -B verify-package.py --source <frozen-source31> --out <fresh-outside-package-and-source>` to repeat the thirteen Run/control outcomes and all seven query checks. The separate check-author-properties.py and probe-mixed-universe-view.py commands take --source/--package/--out; their exact prior measured invocations are retained in source-rebuild.v1.json. Query reproduction is now automatic; properties and mixed-universe checks remain explicitly separate. These are author-assisted reference checks, not independent or blind acceptance.\n''';(out/'README.md').write_text(readme)
for group in ['checkpoint3','normalized-examples6','rust-selection-examples1','semantic-controls1','binding-controls']:
 for p in (old/group).glob('*.store.json'):assert (out/group/p.name).read_bytes()==p.read_bytes()
rows=[{'path':str(p.relative_to(out)),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(out.rglob('*')) if p.is_file() and p!=out/'artifact-manifest.json'];(out/'artifact-manifest.json').write_text(json.dumps({'standing':'Source31-bound author package with automatic query reproduction; actual independent review pending.','sourceManifestSha256':h,'files':rows},indent=2)+'\n');print(json.dumps({'package':str(out),'files':len(rows),'artifactManifestSha256':sha(out/'artifact-manifest.json'),'sourceManifestSha256':h},indent=2))
