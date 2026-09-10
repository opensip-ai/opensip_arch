import json,hashlib,os,subprocess,sys,time
ROOT='/tmp/opensip-design-corrections/post-reset-review.v19/copies/repro-v19'
REF='/tmp/opensip-design-corrections/candidate-subject.v19/docs/coop/design-corrections/reviews/codex-post-reset.v1/final-reference.v19/reference-checks.json'
ref=json.load(open(REF))
def sh(p):
    return hashlib.sha256(open(p,'rb').read()).hexdigest() if os.path.isfile(p) else None
out=[]
for c in ref['commands']:
    src=os.path.join(ROOT,c['source'])
    pre=sh(src)
    rep=None
    for i,a in enumerate(c['command']):
        if a=='--report': rep=c['command'][i+1]
    repbefore=sh(os.path.join(ROOT,rep)) if rep else None
    t=time.time()
    r=subprocess.run(c['command'],cwd=ROOT,capture_output=True,text=True)
    out.append({'name':c['name'],'declaredSourceSha256':c['sourceSha256'],'observedSourceSha256':pre,
      'sourceMatches':pre==c['sourceSha256'],'declaredExit':c['exitCode'],'observedExit':r.returncode,
      'exitMatches':r.returncode==c['exitCode'],'seconds':round(time.time()-t,2),
      'stdoutSha256':hashlib.sha256(r.stdout.encode()).hexdigest(),'stdoutBytes':len(r.stdout),
      'stderrSha256':hashlib.sha256(r.stderr.encode()).hexdigest(),'stderrBytes':len(r.stderr),
      'stdoutTail':r.stdout[-1200:],'stderrTail':r.stderr[-1200:],
      'reportPath':rep,'reportShaBefore':repbefore,'reportShaAfter':sh(os.path.join(ROOT,rep)) if rep else None})
    print(c['name'],r.returncode,flush=True)
json.dump(out,open('/tmp/opensip-design-corrections/post-reset-review.v19/results/canonical-six.json','w'),indent=1)
print('ALLEXIT',[ (o['name'],o['observedExit'],o['sourceMatches']) for o in out])
