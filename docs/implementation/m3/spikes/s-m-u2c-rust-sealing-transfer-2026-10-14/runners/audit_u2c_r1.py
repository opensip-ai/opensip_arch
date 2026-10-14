from pathlib import Path
import json,hashlib,statistics
# U-2c audit (read-only): recomputes every r2 statistic from the raw child records, rechecks exits/stderr, the accepted
# repository controls, part split, bounds, per-entry identities against U-2b, and forms the D-3 R8 "two entry children" sums.
# The r1 series (superseded, retained as history) are summarised the same way.
W=Path(__file__).resolve().parent;A=Path('/Users/sb/code/opensip-ai/opensip_arch');SP=A/'docs/implementation/m3/spikes'
inputs={e['slug']:e for e in json.loads((W/'u2c-inputs.json').read_text())['entries']}
typed={w['id']:w for w in json.loads((SP/'s-m-sealing-typed-2026-10-09/results.json').read_text())['workloads']}
acct={w['id']:w for w in json.loads((SP/'s-m-transfer-2026-10-09/results.json').read_text())['workloads']}
u2b={s['entry']:s for s in json.loads((SP/'s-m-u2b-dependency-source-sets-2026-10-14/u2b-sets.json').read_text())['sets'] if s['built']}
u2b.update({s['entry']:s for s in json.loads((SP/'s-m-u2b-overlay-entry-2026-10-14/u2b-sets-entry8.json').read_text())['sets']})
def ms(v):return round(v/1e6,6)
def stats(xs):return dict(medianNanos=statistics.median(xs),maxNanos=max(xs))
out=dict(standing='U-2c AUDIT (READ-ONLY RECOMPUTATION FROM RAW CHILD RECORDS)',sm5=[],sm7=[],sm5r1=[],sm7r1=[])
s5=json.loads((W/'sm5-two-part-results-r2.json').read_text());assert s5['laneHeldForEntireSet'] and s5['observedParentNiceness']==10
for w in s5['workloads']:
 e=inputs[w['id']];E=W/'sm5-two-part-evidence';kids=[]
 for n in range(10):
  assert (E/f"{w['id']}-{n}.stderr").read_bytes()==b'';r=json.loads((E/f"{w['id']}-{n}.stdout").read_text());kids.append(r)
  assert r['elapsedNanos']==r['repositoryPartNanos']+r['dependencyPartNanos'] and r['elapsedNanos']==w['runs'][n]['elapsedNanos'] and w['runs'][n]['observedChildNiceness']==10 and w['runs'][n]['exitCode']==0
 shapes={json.dumps({k:v for k,v in r.items() if not k.endswith('Nanos')},sort_keys=True) for r in kids};assert len(shapes)==1
 meas=kids[3:];rp=kids[0]['repository'];dp=kids[0]['dependency'];acc=typed[w['repositoryWorkload']]['shape']
 assert all(rp[k]==acc[k] for k in ['rows','bytes','snapshotEquivalentDigest','planEquivalentDigest','snapshotEquivalentDescriptorBytes','inventoryCanonicalBytes','nonregularExcluded'])
 assert dp['dependencySourceSetId']==e['dependencySourceSetId']==u2b[e['entry']]['dependencySourceSetId'] and dp['packages']==u2b[e['entry']]['registryPackages'] and dp['entries']==u2b[e['entry']]['regularFiles'] and dp['bytes']==u2b[e['entry']]['totalBytes']
 row=dict(id=w['id'],entry=e['entry'],repositoryWorkload=w['repositoryWorkload'],elapsed=stats([r['elapsedNanos']for r in meas]),repositoryPart=stats([r['repositoryPartNanos']for r in meas]),dependencyPart=stats([r['dependencyPartNanos']for r in meas]),
  acceptedTypedRepositoryMedianNanos=typed[w['repositoryWorkload']]['medianNanos'],repository=dict((k,rp[k])for k in ['rows','bytes','snapshotEquivalentDescriptorBytes','snapshotEquivalentDigest']),dependency=dp,
  boundsMet=dict(repositoryRows=rp['rows']<=100000,repositoryDescriptor=rp['snapshotEquivalentDescriptorBytes']<=4194304,repositoryBytes=rp['bytes']<=8589934592,dependencyPackages=dp['packages']<=4096,dependencyEntries=dp['entries']<=1000000,dependencyBytes=dp['bytes']<=8589934592),
  rssMaxBytes=max(x['rssNative']for x in w['runs'][3:]))
 assert all([row[k]['medianNanos'],row[k]['maxNanos']]==[w[k]['median'],w[k]['max']] for k in ['elapsed','repositoryPart','dependencyPart']) and all(row['boundsMet'].values());out['sm5'].append(row)
s7=json.loads((W/'sm7-results-r2.json').read_text());assert s7['laneHeldForEntireSet'] and s7['positiveControl']['exitCode']==0 and len(s7['controls'])==9 and all(c['exitCode']!=0 for c in s7['controls'])
for w in s7['results']:
 e=inputs[w['slug']];E=W/'sm7-r2-evidence';kids=[json.loads((E/f"{w['slug']}-{n}.stdout.json").read_text()) for n in range(10)]
 for n,k in enumerate(kids):assert k['allDigestsVerified'] and k['accepted']==w['dependencySeal'] and k['frames']==w['runs'][n]['frames'] and k['rows']==w['snapshotRows'] and k['contentBytes']==w['snapshotBytes']
 seal=w['dependencySeal'];assert seal['dependencySourceSetId']==e['dependencySourceSetId'] and seal['entryCount']==e['files'] and seal['totalBytes']==e['bytes']
 acc=acct.get(e['entry']);
 if acc:assert w['manifestSha256']==acc['manifestSha256'] and w['snapshotRows']==acc['rows']
 else:assert e['entry'].startswith('mr-rs-medium-serde-json/') and w['snapshotRows']==typed['mr-rs-medium-serde-json']['shape']['rows']
 meas=w['runs'][3:];row=dict(id=w['slug'],entry=e['entry'],transfer=stats([r['transferNanos']for r in meas]),receiver=stats([r['receiverNanos']for r in meas]),snapshotRows=w['snapshotRows'],snapshotBytes=w['snapshotBytes'],dependencyEntries=seal['entryCount'],dependencyBytes=seal['totalBytes'],dependencyChunks=seal['totalChunkCount'],dependencyManifestBytes=w['dependencyManifestBytes'],frames=meas[0]['frames'],
  acceptedRepositoryOnlyMedianNanos=acc['medianTransferNanos'] if acc else None,rssMaxBytes=max(r['rssNative']for r in meas))
 assert row['transfer']['medianNanos']==w['medianTransferNanos'] and row['transfer']['maxNanos']==w['maxTransferNanos'];out['sm7'].append(row)
for name,key,res in [('sm5r1','results','sm5-ds-results-r1.json'),('sm7r1','results','sm7-results-r1.json')]:
 d=json.loads((W/res).read_text())
 for w in d[key]:
  m=[r.get('elapsedNanos',r.get('transferNanos'))for r in w['runs']if not r['warmup']];out[name].append(dict(entry=w['entry'],medianNanos=statistics.median(m),maxNanos=max(m)))
r8={};
for part,rows,keys in [('sm5',out['sm5'],['elapsed','repositoryPart','dependencyPart']),('sm7',out['sm7'],['transfer'])]:
 pair=[r for r in rows if r['entry'].startswith('mr-rs-medium-serde-json/')];assert len(pair)==2
 r8[part]={k:dict(medianSumNanos=sum(r[k]['medianNanos']for r in pair),maxSumNanos=sum(r[k]['maxNanos']for r in pair))for k in keys}
out['R8TwoEntryChildren']=dict(label='two entry children (PLAN-r3 D-3): sums of the two entries\' medians and of their maxima',**r8)
(W/'u2c-audit.json').write_text(json.dumps(out,indent=1)+'\n')
for r in out['sm5']:print('SM5',r['entry'],ms(r['elapsed']['medianNanos']),ms(r['elapsed']['maxNanos']),ms(r['repositoryPart']['medianNanos']),ms(r['dependencyPart']['medianNanos']),ms(r['acceptedTypedRepositoryMedianNanos']))
for r in out['sm7']:print('SM7',r['entry'],ms(r['transfer']['medianNanos']),ms(r['transfer']['maxNanos']),r['acceptedRepositoryOnlyMedianNanos'] and ms(r['acceptedRepositoryOnlyMedianNanos']),r['frames'],r['dependencyManifestBytes'])
print(json.dumps(out['R8TwoEntryChildren']))
