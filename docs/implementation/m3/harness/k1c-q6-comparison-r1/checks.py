import datetime,hashlib,json,pathlib,subprocess
product=pathlib.Path('/Users/sb/code/opensip-ai/opensip-k1c-q6-comparison')
evidence=pathlib.Path('/tmp/opensip-implementation/k1c-q6-comparison-authoring')
commands=[]
for name in ('test_q6_comparison.py','test_measurement.py'):
    command=['/usr/bin/nice','-n','10','/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14','-I','-B',str(product/'tools/quality'/name)]
    result=subprocess.run(command,cwd=product,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    (evidence/(name+'.log')).write_text(result.stdout)
    assert result.returncode==0,result.stdout
    commands.append({'command':command,'exitCode':result.returncode})
assert not pathlib.Path('/Users/sb/Library/Application Support/OpenSIP').exists()
report={'standing':'K1c Q6 CORE BUDGET ARITHMETIC ONLY','commands':commands,'completedAt':datetime.datetime.now(datetime.UTC).isoformat(),'sourcePins':[],'repositoryCodeExecuted':False,'measurementRan':False,'baselineAdmitted':False,'runnerEligible':False,'D13EquivalenceDecided':False,'fullK1cComplete':False,'productQualification':False}
for name in ('canonical.py','measurement.py','q6_comparison.py','test_q6_comparison.py'):
    raw=(product/'tools/quality'/name).read_bytes()
    report['sourcePins'].append({'path':'tools/quality/'+name,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
(evidence/'checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'commands':len(commands),'measurementRan':False}))
