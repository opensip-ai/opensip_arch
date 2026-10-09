from pathlib import Path
import json,hashlib,statistics
B=Path(__file__).resolve().parent;R=Path('/tmp/opensip-implementation/sm-replay-2026-10-09');reports=[]
for root,name,pattern in [(R,'results.json','replay-193-{}.stdout'),(B,'results.json','native-193-{}.stdout'),(B,'release-results.json','release-native-193-{}.stdout')]:
 report=json.loads((root/name).read_text());assert len(report['runs'])==10;values=[];shape=None
 for n,row in enumerate(report['runs']):
  assert row['ordinal']==n and row['warmup']==(n<3)and row['exitCode']==0 and row['findings']==193 and row['rssUnit']=='bytes'and row['rssBytes']==row['rssNative'];raw=json.loads((root/pattern.format(n)).read_text());assert raw['completeReplayNanos']==row['completeReplayNanos']and raw['findings']==row['findings']and raw['objects']==row['objects']and raw['blobs']==row['blobs'];assert (root/pattern.format(n).replace('.stdout','.stderr')).read_bytes()==b'';current=(row['objects'],row['blobs'],row['findings']);shape=current if shape is None else shape;assert current==shape
  if n>=3:values.append(row['completeReplayNanos'])
 assert statistics.median(values)==report['medianReplayNanos']and max(values)==report['maxReplayNanos'];reports.append(dict(path=str(root/name),runs=10,measured=7,medianReplayNanos=statistics.median(values),maxReplayNanos=max(values),objects=shape[0],blobs=shape[1],findings=shape[2],allPass=True))
native=json.loads((B/'packet-193-selected.json').read_text());assert native['syntheticSourceFiles']==native['syntheticFindings']==193;assert len({r['id']for r in native['objects']})==len(native['objects']);assert len({r['sha256']for r in native['blobs']})==len(native['blobs']);assert any(r['id']==native['runId']and r['domain']=='run'for r in native['objects'])
for row in native['blobs']:assert hashlib.sha256(bytes.fromhex(row['hex'])).hexdigest()==row['sha256']
assert len([r for r in native['objects']if r['domain']=='fact'])==193;assert len([r for r in native['objects']if r['domain']=='finding'])==193
for name in ['build.json','build-release.json']:
 pin=json.loads((B/name).read_text());raw=Path(pin['executable']).read_bytes();assert len(raw)==pin['bytes']and hashlib.sha256(raw).hexdigest()==pin['sha256']
controls=json.loads((B/'release-controls.json').read_text())['controls'];assert len(controls)==5 and [c['exitCode']for c in controls]==[0,0,101,101,101]
for c in controls:
 if c['expectedNativeDiagnostic']:assert c['expectedNativeDiagnostic']in Path(c['stderr']).read_text()
 else:assert json.loads(Path(c['stdout']).read_text())['fullReplayPassed']is True
size=json.loads((R/'size-source.json').read_text());assert size['distinctConfiguredFiles']==193 and len(set(size['sourcePaths']))==193
result=dict(standing='UNREVIEWED READONLY STATISTICAL/HASH/GRAPH/CONTROL AUDIT,NOT ACCEPTANCE',reports=reports,exactSyntheticSourceAndFactAndFindingCount=193,controls=5,nativeBuildPinsUnchanged=True,allNativeGraphBlobHashesMatched=True,SM9FigureComplete=False,SM9PlaceholderFilled=False,SMComplete=False,LG1Met=False,effectiveL=False,productQualification=False)
(B/'checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
