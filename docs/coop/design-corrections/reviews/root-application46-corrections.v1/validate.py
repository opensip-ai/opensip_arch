from pathlib import Path
import hashlib,json,shutil,subprocess
B=Path('/tmp/opensip-design-corrections');S=B/'application-stage.v46';F=S/'files';R=Path(__file__).parent;C=B/'candidate-subject.v45';V=B/'application-stage.v46-validation';L=Path('/Users/sb/code/opensip-ai/opensip_arch');dc='docs/coop/design-corrections/';py='/tmp/opensip-architecture-review-env/bin/python'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((L/dc/'reviews/candidate-subject.v45.json').read_text());assert all(sha(C/r['path'])==r['sha256'] for r in m['files']);shutil.copytree(C,V)
for p in F.rglob('*'):
 if p.is_file():q=V/p.relative_to(F);q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
out=S/'support/reference-rerun.v46';runner=S/'support/run-application-reference-suites.py'
r=subprocess.run([py,'-I','-B',str(runner),'--root',str(V),'--out',str(out)],capture_output=True,text=True);(R/'reference-rerun.log').write_text(r.stdout+r.stderr);assert r.returncode==0,r.stderr
measured=json.loads((out/'reference-checks.json').read_text());assert measured['passed'] and len(measured['commands'])==7
changed=[]
for p in F.rglob('*'):
 if p.is_file() and sha(p)!=sha(V/p.relative_to(F)):changed.append(str(p.relative_to(F)))
assert changed==[],changed
old=S/'support/staged-reference-checks.v1.json';shutil.copyfile(old,R/'prior-staged-reference-checks.v1.json')
record={'scratchRoot':str(V),'commands':measured['commands'],'acceptedDesignFileCount':len(m['files']),'implementationQualification':False,'standing':'Fresh application46 reference rerun on a disposable full accepted-source copy overlaid with the46 application files. All staged after-images remained byte-identical after execution; accepted source45 remains immutable. Earlier support/reference-rerun receipts retain their original45.2 execution scope.'}
old.write_text(json.dumps(record,indent=2)+'\n');(R/'validation.json').write_text(json.dumps({'freshReferenceCommandsPassed':7,'sourceFilesVerified':len(m['files']),'stagedAfterImagesChangedByExecution':changed,'passed':True},indent=2)+'\n');print((R/'validation.json').read_text())
