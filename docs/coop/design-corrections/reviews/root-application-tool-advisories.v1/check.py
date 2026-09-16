from pathlib import Path
import json,hashlib,shutil,subprocess,importlib.util,ast,copy
O=Path(__file__).parent;T=O.parent/'application-successor-root.v2';stage=O/'synthetic-stage';stage.mkdir();support=stage/'support';support.mkdir();py='/tmp/opensip-architecture-review-env/bin/python';sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(n,d):(support/n).write_text(json.dumps(d,indent=2)+'\n')
s=(T/'prepare-validation.py').read_text();start=s.index('# Historical copied reports are provenance only.');end=s.index("save('staged-reference-checks.v1.json'",start)
ctx=dict(Path=Path,json=json,shutil=shutil,subprocess=subprocess,stage=stage,support=support,py=py,sha=sha,save=save,__file__=str(T/'prepare-validation.py'))
exec(compile(s[start:end],str(T/'prepare-validation.py'),'exec'),ctx)
receipt=json.loads((support/'current-application-tool-checks.v1.json').read_text());work=stage.parent/(stage.name+'-tool-validation')
for row in receipt['sourceFiles']:
 q=support/row['path'];q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(work/row['path'],q)
checks=[]
def check(n,ok):assert ok,n;checks.append({'id':n,'passed':True})
f=T/'retain_public.py';sp=importlib.util.spec_from_file_location('P',f);P=importlib.util.module_from_spec(sp);sp.loader.exec_module(P)
for name in ['summary.json','plan.json']:
 check('claude-authored-'+name,not P.grok_source_is_private(name,'raw.json','claude'))
 check('grok-private-'+name,P.grok_source_is_private(name,'raw.json','grok'))
 check('named-stdout-'+name,P.grok_source_is_private(name,name,'claude'))
 check('nested-private-'+name,P.grok_source_is_private('scratch/compaction/'+name,'raw.json','claude'))
# Exact freeze guard, bounded before-image/preparation scope; no actual freeze/application.
s=(T/'freeze-application.py').read_text();start=s.index('# Bind the newly executed');end=s.index("before = stage / 'before'",start);guard=compile(s[start:end],str(T/'freeze-application.py'),'exec')
def safe(r):
 q=Path(r);assert not q.is_absolute() and '..' not in q.parts;return q
def validate():exec(guard,{'load':lambda p:json.loads(p.read_text()),'support':support,'safe':safe,'sha':sha,'Path':Path})
validate();check('freeze-current-receipt-positive',True)
q=support/receipt['sourceFiles'][0]['path'];before=q.read_bytes();q.write_bytes(before+b'\n')
try:validate()
except AssertionError:check('freeze-tool-drift-refused',True)
else:raise AssertionError('tool drift admitted')
q.write_bytes(before)
q=support/receipt['runs'][0]['report'];before=q.read_bytes();q.write_bytes(before+b'\n')
try:validate()
except AssertionError:check('freeze-receipt-drift-refused',True)
else:raise AssertionError('receipt drift admitted')
q.write_bytes(before)
# The corrected retain suite must refuse missing arguments, same paths and overwrite before executing.
script=work/'check-retain-public.v1.py';prior=work/'prior.json';prior.write_text('prior evidence');new=work/'never-created.json'
for name,args in [('missing-report-args',[]),('same-report-paths',['--report',str(new),'--envelope-report',str(new)]),('existing-report',['--report',str(prior),'--envelope-report',str(new)])]:
 r=subprocess.run([py,'-I','-B',str(script)]+args,capture_output=True,text=True);(O/(name+'.stderr.txt')).write_text(r.stderr);check(name,r.returncode!=0 and prior.read_text()=='prior evidence' and not new.exists())
# Explicit live-root assent recheck avoids accepted_files-based ref selection.
s=(T/'assemble-records.successor.v1.py').read_text();line=next(x for x in s.splitlines() if "'Root design assent changed during assembly'" in x)
root=O/'assent-root';root.mkdir();q=root/'assent.json';q.write_text('bound');assent_ref={'path':'assent.json','sha256':sha(q)};q.write_text('drift')
try:exec(line,{'digest':sha,'root':root,'assent_ref':assent_ref})
except AssertionError:check('explicit-live-assent-drift-refused',True)
else:raise AssertionError('assent drift admitted')
(O/'verification.json').write_text(json.dumps({'standing':'Root bounded tooling probes and freshly executed suites; no actual application or freeze.','checks':checks,'toolReceipt':receipt,'passed':True},indent=2)+'\n');print('PASS',len(checks),'focused checks plus current suites')
