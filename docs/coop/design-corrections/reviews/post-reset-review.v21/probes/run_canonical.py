"""Reproduce the six canonical commands on the disposable exact unrepinned copy.
Foundation: outer 3600s (inner 600s per child, owned by the launcher). Others: 600s.
A partial failure record is preserved on ANY orchestration timeout."""
import json,hashlib,os,subprocess,sys,time
COPY='/tmp/opensip-design-corrections/post-reset-review.v21/work/copy'
OUTD='/tmp/opensip-design-corrections/post-reset-review.v21/results/canonical'
os.makedirs(OUTD,exist_ok=True)
PY='/tmp/opensip-architecture-review-env/bin/python'
SPEC=json.load(open(os.path.join(COPY,'docs/coop/design-corrections/reviews/codex-post-reset.v1/final-reference.v21/reference-checks.json')))
def sh(p):
    try: return hashlib.sha256(open(p,'rb').read()).hexdigest()
    except OSError: return None
rec={'standing':'ACTUAL EXECUTION by independent review v21 on a disposable exact unrepinned copy. Not qualification.',
     'copyRoot':COPY,'subjectManifestSha256':'360c2758c0409ebc307966c7a385c385c2d7f580b4623dd760b7ba0e26bf18c1',
     'commands':[],'orchestrationTimeout':False}
def flush():
    json.dump(rec,open(os.path.join(OUTD,'canonical-execution.json'),'w'),indent=1)
for c in SPEC['commands']:
    name=c['name']
    argv=[PY if a.endswith('bin/python') else a for a in c['command']]
    outer=c['outerTimeoutSeconds']
    srcp=os.path.join(COPY,c['source'])
    e={'name':name,'declaredSource':c['source'],'declaredSourceSha256':c['sourceSha256'],
       'observedSourceSha256':sh(srcp),'command':argv,'outerTimeoutSeconds':outer,
       'declaredExitCode':c['exitCode'],'workingDirectory':COPY}
    e['sourceHashAgrees']=(e['observedSourceSha256']==c['sourceSha256'])
    # report path, if the command names one
    rp=None
    if '--report' in argv: rp=os.path.join(COPY,argv[argv.index('--report')+1])
    e['reportPath']=argv[argv.index('--report')+1] if rp else None
    e['reportSha256Before']=sh(rp) if rp else None
    t0=time.time()
    try:
        r=subprocess.run(argv,cwd=COPY,capture_output=True,text=True,timeout=outer)
        e['exitCode']=r.returncode; out,err=r.stdout,r.stderr; e['timedOut']=False
    except subprocess.TimeoutExpired as x:
        e['exitCode']=None; e['timedOut']=True; rec['orchestrationTimeout']=True
        dec=lambda s:'' if s is None else s if isinstance(s,str) else s.decode('utf-8','replace')
        out,err=dec(x.stdout),dec(x.stderr)+'\nORCHESTRATION TIMEOUT after %ds\n'%outer
    e['elapsedSeconds']=round(time.time()-t0,3)
    lg=os.path.join(OUTD,name+'.log')
    open(lg,'w').write('$ '+' '.join(argv)+'\n--- STDOUT ---\n'+out+'\n--- STDERR ---\n'+err)
    e['log']=name+'.log'; e['logSha256']=sh(lg)
    e['stdoutBytes']=len(out); e['stderrBytes']=len(err)
    e['reportSha256After']=sh(rp) if rp else None
    e['reportChanged']=(e['reportSha256Before']!=e['reportSha256After']) if rp else None
    e['exitAgreesWithDeclared']=(e['exitCode']==c['exitCode'])
    rec['commands'].append(e); flush()
    print(name,'exit',e['exitCode'],'declared',c['exitCode'],'elapsed',e['elapsedSeconds'],
          'srcHashOk',e['sourceHashAgrees'],'timedOut',e['timedOut'],flush=True)
rec['allSixExecuted']=len(rec['commands'])==6
rec['allExitAgree']=all(x['exitAgreesWithDeclared'] for x in rec['commands'])
rec['allSourceHashesAgree']=all(x['sourceHashAgrees'] for x in rec['commands'])
flush()
print('SUMMARY allSix',rec['allSixExecuted'],'allExitAgree',rec['allExitAgree'],'allSrcHash',rec['allSourceHashesAgree'])
