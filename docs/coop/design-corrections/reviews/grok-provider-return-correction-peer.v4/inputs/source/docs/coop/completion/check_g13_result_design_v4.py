"""Reference result validator against explicit matrix and trusted baseline context.
Synthetic report cases test validation rules; none is a measured product result.
"""
import argparse,copy,hashlib,json,re
from pathlib import Path
import platform
import importlib.metadata
try:
    from jsonschema import Draft202012Validator
except ModuleNotFoundError:
    raise SystemExit('DEPENDENCY-MISSING: install docs/coop/completion/review-dependencies/requirements.txt into the review environment')
B=Path(__file__).resolve().parent
SHA=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
M=json.loads((B/'language-quality-matrix.completed.v2.json').read_text())
S=json.loads((B/'g13-result-schema.v4.json').read_text())
V=Draft202012Validator(S)

CLASSES={"macos-arm64":("macos-15",3),"macos-x86_64":("macos-15-intel",4),"linux-x86_64":("ubuntu-24.04",4),"linux-arm64":("ubuntu-24.04-arm",4)}
RAM_GIB={"macos-arm64":7,"macos-x86_64":14,"linux-x86_64":16,"linux-arm64":16}
HARDWARE=("runnerClass","vcpu","ramBytes","cpuModel","osVersion","osBuild","kernel","filesystem","measurementToolDigest")

def valid(x, baseline=None, trusted_runners=None):
    if not V.is_valid(x) or trusted_runners is None or set(trusted_runners)!=set(M['platforms']):return False
    if x['matrixDigest']!=SHA(B/'language-quality-matrix.completed.v2.json') or x['corpusDigest']!=SHA(B/'quality-corpus-manifest.v1.json'):return False
    first=baseline is None
    if (x['baselineStatus']=='FIRST-BASELINE')!=first or x['baselineArtifactDigest']!=(None if first else baseline['digest']):return False
    cells={c['cellId']:c for c in x['cells']};perfs={p['platform']:p for p in x['performance']}
    if len(cells)!=24 or len(perfs)!=4 or set(cells)!={r['id'] for r in M['rows']} or set(perfs)!=set(M['platforms']):return False
    ids=[p['observationId'] for p in x['performance']]
    if len(ids)!=len(set(ids)):return False
    all_pass=True
    for platform,p in perfs.items():
        m=p['measurements'];runner=p['runner'];ok=m is not None and runner is not None
        if ok:
            ok=runner['hostDigest']==x['hostDigest'] and runner['providerClosureDigest']==x['providerClosureDigest']
            ok &= (runner['runnerClass'],runner['vcpu'])==CLASSES[platform]
            ok &= all(runner[k]==trusted_runners[platform].get(k) for k in HARDWARE)
            # D-102 preflight belongs to class admission, even for true observations.
            ok &= abs(runner['ramBytes']-RAM_GIB[platform]*2**30)<=3*2**28
            ok &= (re.fullmatch(r'15(?:\.[0-9]+)*',runner['osVersion']) is not None if platform.startswith('macos-') else runner['osVersion']=='24.04')
            cold=sorted(m['coldDurationNs'])[28];warm=sorted(m['warmDurationNs'])[28]
            rss=max(m['observedTreePeakRssBytes'],m['sumIndividualHighWaterRssBytes'])
            ok &= cold<=10_000_000_000 and warm<=5_000_000_000 and rss<=1_073_741_824
            if first:
                ok &= all(m[k] is None for k in ['baselineColdP95Ns','baselineWarmP95Ns','baselineRssBytes'])
            else:
                expected=baseline['platforms'][platform]
                ok &= expected.get('runnerInventory')==trusted_runners[platform]
                for field,quantity in [('baselineColdP95Ns',cold),('baselineWarmP95Ns',warm),('baselineRssBytes',rss)]:
                    ok &= m[field]==expected[field] and quantity*10<=expected[field]*11
        if (p['result']=='PASS')!=ok:return False
        all_pass &= ok
    for row in M['rows']:
        c=cells[row['id']];fs=c['fixtureResults'];named={f['fixtureId'] for f in fs}
        if named!=set(row['projects']) or len(fs)!=len(named) or c['performanceObservationId']!=perfs[row['platform']]['observationId']:return False
        ok=all(f['expectationMatched'] and f['missingCount']==f['extraCount']==f['duplicateCount']==0 and f['expectedCount']==f['actualCount'] and f['differenceArtifactDigest'] is None for f in fs)
        ok &= perfs[row['platform']]['result']=='PASS'
        if (c['result']=='PASS')!=ok:return False
        all_pass &= ok
    return (x['result']=='PASS')==all_pass

def reference():
    h='a'*64
    p=[]
    for platform in M['platforms']:
        runner={k:('fixture-runner' if k not in ['vcpu','ramBytes','concurrency'] and not k.endswith('Digest') else h) for k in S['properties']['performance']['items']['properties']['runner']['oneOf'][1]['properties']}
        runner.update(runnerClass=CLASSES[platform][0],vcpu=CLASSES[platform][1],ramBytes=RAM_GIB[platform]*2**30,osVersion='15.6' if platform.startswith('macos-') else '24.04',concurrency=1)
        p.append({'observationId':platform,'platform':platform,'profileId':'whole-analyze-1000modules.v1','runner':runner,'measurements':{'coldDurationNs':[1_000_000_000]*30,'warmDurationNs':[500_000_000]*30,'warmups':5,'observedTreePeakRssBytes':1000000,'sumIndividualHighWaterRssBytes':2000000,'baselineColdP95Ns':None,'baselineWarmP95Ns':None,'baselineRssBytes':None},'result':'PASS','reason':'SYNTHETIC VALIDATOR INPUT, NOT MEASURED'})
    return {'schemaMajor':1,'gate':M['gate'],'matrixDigest':SHA(B/'language-quality-matrix.completed.v2.json'),'corpusDigest':SHA(B/'quality-corpus-manifest.v1.json'),'hostDigest':h,'providerClosureDigest':h,'baselineStatus':'FIRST-BASELINE','baselineArtifactDigest':None,'performance':p,'cells':[{'cellId':r['id'],'fixtureResults':[{'fixtureId':f,'expectedCount':1,'actualCount':1,'missingCount':0,'extraCount':0,'duplicateCount':0,'expectationMatched':True,'differenceArtifactDigest':None} for f in r['projects']],'result':'PASS','performanceObservationId':r['platform']} for r in M['rows']],'result':'PASS'}

def main(args):
    Draft202012Validator.check_schema(S)
    base=reference();trusted={p['platform']:{k:p['runner'][k] for k in HARDWARE} for p in base['performance']};cases=[('reference-structure',base,None,True)]
    changes=[('missing-cell',lambda x:x['cells'].pop()),('duplicate-cell',lambda x:x['cells'].__setitem__(1,copy.deepcopy(x['cells'][0]))),('missing-fixture',lambda x:x['cells'][0]['fixtureResults'].pop()),('false-match',lambda x:x['cells'][0]['fixtureResults'][0].update(expectationMatched=False)),('cold-over-ceiling',lambda x:x['performance'][0]['measurements'].update(coldDurationNs=[10000000001]*30)),('rss-over-ceiling',lambda x:x['performance'][0]['measurements'].update(sumIndividualHighWaterRssBytes=1073741825)),('missing-runner',lambda x:x['performance'][0].update(runner=None)),('cross-platform-link',lambda x:x['cells'][0].update(performanceObservationId=M['platforms'][1])),('wrong-subject',lambda x:x.update(hostDigest='b'*64)),('forged-baseline',lambda x:x.update(baselineStatus='ESTABLISHED',baselineArtifactDigest='b'*64))]
    for name,change in changes:
        x=copy.deepcopy(base);change(x);cases.append((name,x,None,False))
    baseline={'digest':'b'*64,'platforms':{p:{'baselineColdP95Ns':900000000,'baselineWarmP95Ns':500000000,'baselineRssBytes':2000000,'runnerInventory':trusted[p]} for p in M['platforms']}}
    x=copy.deepcopy(base);x.update(baselineStatus='ESTABLISHED',baselineArtifactDigest=baseline['digest'])
    for p in x['performance']:p['measurements'].update({k:v for k,v in baseline['platforms'][p['platform']].items() if k!='runnerInventory'})
    cases.append(('regression-over-10percent',x,baseline,False))
    for p in x['performance']:p['measurements']['coldDurationNs']=[990000000]*30
    cases.append(('regression-exact-10percent',copy.deepcopy(x),baseline,True))
    cases[-2]=(cases[-2][0],copy.deepcopy(cases[-2][1]),baseline,False)
    # Preserve the independent over-boundary case, rather than sharing mutable input.
    for p in cases[-2][1]['performance']:p['measurements']['coldDurationNs']=[1000000000]*30
    for name,change in [('wrong-class',lambda x:x['performance'][0]['runner'].update(runnerClass='ubuntu-24.04')),('wrong-vcpu',lambda x:x['performance'][0]['runner'].update(vcpu=99)),('forged-ram',lambda x:x['performance'][0]['runner'].update(ramBytes=1)),('forged-image',lambda x:x['performance'][0]['runner'].update(osBuild='forged')),('warm-over-ceiling',lambda x:x['performance'][0]['measurements'].update(warmDurationNs=[5000000001]*30))]:
        changed=copy.deepcopy(base);change(changed);cases.append((name,changed,None,False))
    bad_baseline=copy.deepcopy(baseline);bad_baseline['platforms'][M['platforms'][0]]['runnerInventory']['osBuild']='older-image'
    cases.append(('baseline-environment-mismatch',copy.deepcopy(x),bad_baseline,False))
    results=[{'id':'missing-trusted-inventory','expected':False,'actual':valid(base)}]
    assert results[0]['actual'] is False
    for name,x,context,expected in cases:
        actual=valid(x,context,trusted);assert actual==expected,(name,actual,expected);results.append({'id':name,'expected':expected,'actual':actual})
    for p in M['platforms']:
        center=RAM_GIB[p]*2**30;tol=3*2**28
        for suffix,value,expected in [('lower-edge',center-tol,True),('upper-edge',center+tol,True),('below-class',center-tol-1,False),('above-class',center+tol+1,False),('one-byte',1,False),('one-tebibyte',2**40,False)]:
            changed=copy.deepcopy(base);inventory=copy.deepcopy(trusted)
            next(r for r in changed['performance'] if r['platform']==p)['runner']['ramBytes']=value;inventory[p]['ramBytes']=value
            actual=valid(changed,None,inventory);assert actual==expected,(p,suffix,actual)
            results.append({'id':p+'-ram-'+suffix,'expected':expected,'actual':actual})
        for osversion in (['26.0','150.0','15x','15.6\n'] if p.startswith('macos-') else ['22.04','24.040','24.04\n']):
            changed=copy.deepcopy(base);inventory=copy.deepcopy(trusted)
            next(r for r in changed['performance'] if r['platform']==p)['runner']['osVersion']=osversion;inventory[p]['osVersion']=osversion
            actual=valid(changed,None,inventory);assert actual is False,(p,osversion)
            results.append({'id':p+'-wrong-os-'+repr(osversion),'expected':False,'actual':actual})
    report={'kind':'G13-result-validator-design-cases','trustedRunnerInventory':trusted,'inventoryStanding':'SYNTHETIC-NOT-MEASURED','productQualification':False,'environment':{'python':platform.python_version(),'jsonschema':importlib.metadata.version('jsonschema')},'count':len(results),'passed':len(results),'results':results,'pins':{p.name:SHA(p) for p in [Path(__file__),B/'g13-result-schema.v4.json',B/'language-quality-matrix.completed.v2.json']}}
    Path(args.report).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'count':len(results),'passed':len(results)}))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--report',default=str(B/'g13-result-design-report.v4.json'));main(p.parse_args())
