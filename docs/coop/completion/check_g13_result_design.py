"""Reference result validator against explicit matrix and trusted baseline context.
Synthetic report cases test validation rules; none is a measured product result.
"""
import argparse,copy,hashlib,json
from pathlib import Path
from jsonschema import Draft202012Validator
B=Path(__file__).resolve().parent
SHA=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
M=json.loads((B/'language-quality-matrix.completed.v1.json').read_text())
S=json.loads((B/'g13-result-schema.v1.json').read_text())
V=Draft202012Validator(S)

def valid(x, baseline=None):
    if not V.is_valid(x):return False
    if x['matrixDigest']!=SHA(B/'language-quality-matrix.completed.v1.json') or x['corpusDigest']!=SHA(B/'quality-corpus-manifest.v1.json'):return False
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
            cold=sorted(m['coldDurationNs'])[28];warm=sorted(m['warmDurationNs'])[28]
            rss=max(m['observedTreePeakRssBytes'],m['sumIndividualHighWaterRssBytes'])
            ok &= cold<=10_000_000_000 and warm<=5_000_000_000 and rss<=1_073_741_824
            if first:
                ok &= all(m[k] is None for k in ['baselineColdP95Ns','baselineWarmP95Ns','baselineRssBytes'])
            else:
                expected=baseline['platforms'][platform]
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
        runner.update(vcpu=4,ramBytes=8589934592,concurrency=1)
        p.append({'observationId':platform,'platform':platform,'profileId':'whole-analyze-1000modules.v1','runner':runner,'measurements':{'coldDurationNs':[1_000_000_000]*30,'warmDurationNs':[500_000_000]*30,'warmups':5,'observedTreePeakRssBytes':1000000,'sumIndividualHighWaterRssBytes':2000000,'baselineColdP95Ns':None,'baselineWarmP95Ns':None,'baselineRssBytes':None},'result':'PASS','reason':'SYNTHETIC VALIDATOR INPUT, NOT MEASURED'})
    return {'schemaMajor':1,'gate':M['gate'],'matrixDigest':SHA(B/'language-quality-matrix.completed.v1.json'),'corpusDigest':SHA(B/'quality-corpus-manifest.v1.json'),'hostDigest':h,'providerClosureDigest':h,'baselineStatus':'FIRST-BASELINE','baselineArtifactDigest':None,'performance':p,'cells':[{'cellId':r['id'],'fixtureResults':[{'fixtureId':f,'expectedCount':1,'actualCount':1,'missingCount':0,'extraCount':0,'duplicateCount':0,'expectationMatched':True,'differenceArtifactDigest':None} for f in r['projects']],'result':'PASS','performanceObservationId':r['platform']} for r in M['rows']],'result':'PASS'}

def main(args):
    Draft202012Validator.check_schema(S)
    base=reference();cases=[('reference-structure',base,None,True)]
    changes=[('missing-cell',lambda x:x['cells'].pop()),('duplicate-cell',lambda x:x['cells'].__setitem__(1,copy.deepcopy(x['cells'][0]))),('missing-fixture',lambda x:x['cells'][0]['fixtureResults'].pop()),('false-match',lambda x:x['cells'][0]['fixtureResults'][0].update(expectationMatched=False)),('cold-over-ceiling',lambda x:x['performance'][0]['measurements'].update(coldDurationNs=[10000000001]*30)),('rss-over-ceiling',lambda x:x['performance'][0]['measurements'].update(sumIndividualHighWaterRssBytes=1073741825)),('missing-runner',lambda x:x['performance'][0].update(runner=None)),('cross-platform-link',lambda x:x['cells'][0].update(performanceObservationId=M['platforms'][1])),('wrong-subject',lambda x:x.update(hostDigest='b'*64)),('forged-baseline',lambda x:x.update(baselineStatus='ESTABLISHED',baselineArtifactDigest='b'*64))]
    for name,change in changes:
        x=copy.deepcopy(base);change(x);cases.append((name,x,None,False))
    baseline={'digest':'b'*64,'platforms':{p:{'baselineColdP95Ns':900000000,'baselineWarmP95Ns':500000000,'baselineRssBytes':2000000} for p in M['platforms']}}
    x=copy.deepcopy(base);x.update(baselineStatus='ESTABLISHED',baselineArtifactDigest=baseline['digest'])
    for p in x['performance']:p['measurements'].update(baseline['platforms'][p['platform']])
    cases.append(('regression-over-10percent',x,baseline,False))
    for p in x['performance']:p['measurements']['coldDurationNs']=[990000000]*30
    cases.append(('regression-exact-10percent',copy.deepcopy(x),baseline,True))
    cases[-2]=(cases[-2][0],copy.deepcopy(cases[-2][1]),baseline,False)
    # Preserve the independent over-boundary case, rather than sharing mutable input.
    for p in cases[-2][1]['performance']:p['measurements']['coldDurationNs']=[1000000000]*30
    results=[]
    for name,x,context,expected in cases:
        actual=valid(x,context);assert actual==expected,(name,actual,expected);results.append({'id':name,'expected':expected,'actual':actual})
    report={'kind':'G13-result-validator-design-cases','productQualification':False,'count':len(results),'passed':len(results),'results':results,'pins':{p.name:SHA(p) for p in [Path(__file__),B/'g13-result-schema.v1.json',B/'language-quality-matrix.completed.v1.json']}}
    Path(args.report).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'count':len(results),'passed':len(results)}))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--report',default=str(B/'g13-result-design-report.v1.json'));main(p.parse_args())
