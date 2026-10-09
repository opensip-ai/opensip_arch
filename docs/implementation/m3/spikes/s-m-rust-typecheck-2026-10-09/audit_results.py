from pathlib import Path
import json,hashlib,statistics,re,sys
B=Path(__file__).resolve().parent;P=Path('/Users/sb/code/opensip-ai/opensip');sys.path.insert(0,str(P/'tools/quality'));from canonical import digest
r=json.loads((B/'results.json').read_text());checks=[]
for w in r['workloads']:
 inv=w['inventory'];assert json.loads((B/(w['id']+'-inventory.json')).read_text())==inv
 if inv['overlay']is not None:assert digest(inv['overlay'])==inv['overlayDigest']
 assert len(w['runs'])==10 and [q['warmup']for q in w['runs']]==[True]*3+[False]*7;times=[q['totalRootSetNanos']for q in w['runs']if not q['warmup']];assert statistics.median(times)==w['medianRootSetNanos']and max(times)==w['maxRootSetNanos'];summary=[]
 for idx,root in enumerate(inv['libraryRoots']):
  allRows=[run['libraryRoots'][idx]for run in w['runs']];codes=set();markers=[]
  for q in allRows:
   assert q['manifest']==root['manifest']and q['rootOrdinal']==idx;events=[json.loads(line)for line in Path(q['stdout']).read_text().splitlines()if line.startswith('{')];assert events==q['events'];assert q['afterExpansionReached']==any(e['event']=='after_expansion'for e in events);assert q['afterAnalysisReachedSuccessfully']==any(e['event']=='after_analysis'for e in events);assert q['rssNative']>=0;assert not q['afterAnalysisReachedSuccessfully']or q['exitCode']==0;err=Path(q['stderr']).read_text();codes.update(re.findall(r'error\[(E\d{4})\]',err));markers.append(dict(exit=q['exitCode'],afterExpansion=q['afterExpansionReached'],afterAnalysis=q['afterAnalysisReachedSuccessfully'],events=events))
  assert all(x==markers[0]for x in markers);summary.append(dict(manifest=root['manifest'],root=root['root'],exitCode=allRows[0]['exitCode'],afterAnalysisReachedSuccessfully=allRows[0]['afterAnalysisReachedSuccessfully'],observedErrorCodes=sorted(codes),successfulAfterAnalysisIn10Runs=sum(q['afterAnalysisReachedSuccessfully']for q in allRows),noNativeFailureRouteInferred=True))
 checks.append(dict(id=w['id'],roots=len(summary),successfulRoots=sum(q['afterAnalysisReachedSuccessfully']for q in summary),allTenPhaseAndExitShapesMatch=True,exactWarmupStatisticsMatch=True,rootSummary=summary))
assert len(checks)==8 and sum(w['roots']for w in checks)==48 and sum(w['successfulRoots']for w in checks)==7
(B/'checks.json').write_text(json.dumps(dict(standing='UNREVIEWED ACTUAL ROOT/PHASE/STATISTICAL AUDIT; NO FULLSM OR SOURCE ADMISSION',workloads=checks,totalCompilerChildren=480,successfulAfterAnalysisChildren=70,syntheticControls=6,SM4PlaceholderFilled=False,SM11PlaceholderFilled=False,SMComplete=False,LG1Met=False),indent=2)+'\n');print('480 actual roots/70 successful after-analysis children; all phase shapes and3warmup7statistics match.')
