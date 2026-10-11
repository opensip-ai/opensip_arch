from pathlib import Path
import json,hashlib,statistics
B=Path(__file__).resolve().parent;j=json.loads((B/'results.json').read_text());assert j['children']==10 and len(j['workloads'])==1 and j['observedParentNiceness']==10
for row in [j['runtimePin'],j['modulePin']]:
 p=Path(row['path']);raw=p.read_bytes();assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
reference={w['id']:w for w in json.loads((B.parent/'results.json').read_text())['workloads']}
for w in j['workloads']:
 p=B/w['inputPin']['path'];raw=p.read_bytes();assert len(raw)==w['inputPin']['bytes'] and hashlib.sha256(raw).hexdigest()==w['inputPin']['sha256'];assert json.loads(raw)['heldOut']is False
 assert len(w['runs'])==10
 for n,r in enumerate(w['runs']):
  assert r['ordinal']==n and r['warmup']==(n<3) and r['observedChildNiceness']==10 and r['exitCode']==0 and r['rssBytes']==r['rssNative'] and r['rssUnit']=='bytes' and r['rssBytes']>0
  observed=json.loads((B/f'{w["id"]}-{n}.stdout').read_text());assert observed.pop('elapsedNanos')==r['elapsedNanos'];assert observed==w['shape'];assert (B/f'{w["id"]}-{n}.stderr').read_bytes()==b''
  for a in reference[w['id']]['actors']:assert all(observed[k]==a['shape'][k]for k in observed)
 vals=[r['elapsedNanos']for r in w['runs'][3:]];assert statistics.median(vals)==w['medianNanos'] and max(vals)==w['maxNanos'];assert max(r['rssBytes']for r in w['runs'][3:])==w['measuredPeakProcessRssBytes']
report=dict(standing='UNREVIEWED READONLY10CHILD ACTUALPRIVATE RUST HELPER AUDIT',children=10,workloads=1,allRawOutputsAndStatisticsChecked=True,allFieldsMatchBothIndependentPythonImplementations=True,actualNativeWorker=False,actualAcceptedTransportManifest=False,coverageKeysValidatedC2Values=False,SM12FigureComplete=False,SMComplete=False,LG1Met=False,effectiveL=False,productQualification=False);(B/'checks.json').write_text(json.dumps(report,indent=2)+'\n');print('10Rusthelper rawoutputs/priorities/statistics/runtimepins agree; no operationalworker/admission inferred.')
