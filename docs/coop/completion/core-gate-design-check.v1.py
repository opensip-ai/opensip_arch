"""Synthetic G01--G05 scoring and exact legacy-state joins; no product execution."""
import argparse, copy, hashlib, importlib.util, json, re, statistics
from pathlib import Path
P=Path(__file__).resolve().parent; ROOT=P.parents[2]
def load(n):return json.loads((P/n).read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def module(n,f):
 s=importlib.util.spec_from_file_location(n,P/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
DIST=module('core_gate_distribution','design_models.py')
DOCTOR=module('core_gate_doctor','doctor-cache-check.v1.py')
FLEETS={'macos-15':'macos-arm64','macos-15-intel':'macos-x86_64','ubuntu-24.04':'linux-x86_64','ubuntu-24.04-arm':'linux-arm64'}
PLATFORMS=set(FLEETS.values())
def need(v):
 if not v:raise ValueError('invalid observation')
def uint(v):return type(v) is int and 0<=v<=2**64-1
def digest(v):return isinstance(v,str) and re.fullmatch('[0-9a-f]{64}',v) is not None
def ints(v,n):return isinstance(v,list) and len(v)==n and all(uint(t) for t in v)
def result(ok,**metrics):return {'status':'PASS' if ok else 'FAIL',**metrics}
def preflight(x):
 need(x['fleet'] in FLEETS and x['platform']==FLEETS[x['fleet']]);need(x['projection']=='thin' and x['translated'] is False and x['timedInstrumentation']==[])
 need(x['preflight']=={'projectionIdentity':'P-test','dependencyIdentity':'D-test','initialStateIdentity':'I-test','outcome':'PASS'})
def download(x):
 wanted={(p,c) for p in PLATFORMS for c in (['pkg','tar.zst'] if p.startswith('macos') else ['tar.zst'])}
 a=x['artifacts'];need(len(a)==len(wanted) and {(t['platform'],t['container']) for t in a}==wanted)
 need(set(x['publication'])=={t['id'] for t in a} and len({t['id'] for t in a})==len(a))
 for t in a:
  need(uint(t['observedBytes']) and uint(t['declaredBytes']) and t['observedBytes']==t['declaredBytes']);need(t['sha256']==x['publication'][t['id']]['sha256'])
  need(digest(t['sha256']) and digest(t['sbomSha256']));need(isinstance(t['signatureRefs'],list) and all(isinstance(r,str) and r for r in t['signatureRefs']) and len(set(t['signatureRefs']))==len(t['signatureRefs']));need(t['signatureRefs'] and t['signatureRefs']==x['publication'][t['id']]['signatureRefs']);need(t['sbomSha256']==x['publication'][t['id']]['sbomSha256'])
  need(not set(t['members']) & {'language-runtime','analyzer','graph-engine','report-generator','evidence-database','telemetry-backend'})
 return result(all(t['observedBytes']<=25_000_000 for t in a),containers=len(a))
def inventory(x):
 nodes=x['nodes'];need(nodes and len({n['path'] for n in nodes})==len(nodes) and len({n['sha256'] for n in nodes})==len(nodes));need(set(x['publishedPaths'])=={n['path'] for n in nodes})
 paths=set(x['publishedPaths']);incoming=set();shared=0
 for n in nodes:
  need(digest(n['sha256']));need(DIST.path_admission([n['path']])=='ACCEPT' and n['type']=='file');ls=set(n['layers']);need(len(ls)==len(n['layers']) and ls)
  if len(ls)>1:need(ls=={'L-DIST','L-HOST'} and n['sharedExecutable'] is True);shared+=1
  else:need(ls<={'L-DIST','L-HOST','L-EVAL','L-COMP','L-TCB'} and n['sharedExecutable'] is False)
  need(len(set(n['requires']))==len(n['requires']) and set(n['requires'])<=paths);incoming|=set(n['requires'])
 need(shared<=1 and set(x['roots'])==paths-incoming and x['roots'])
 edges={n['path']:n['requires'] for n in nodes};seen=set();active=set()
 def walk(n):
  need(n not in active)
  if n in seen:return
  active.add(n)
  for d in edges[n]:walk(d)
  active.remove(n);seen.add(n)
 for n in paths:walk(n)
 return result(True,nodes=len(nodes))
def timing(x):
 preflight(x);need(x['command'] in ['help','version']);need(ints(x['coldMs'],21) and ints(x['warmMs'],21));need(x['jobIds']==list(range(1,22)))
 c=sorted(x['coldMs']);w=sorted(x['warmMs']);r=[c[10],c[19],c[20],w[19],w[20]]
 return result(all(a<=b for a,b in zip(r,[100,150,250,50,100])),operativeMs=r,warmP50Telemetry=w[10])
def no_load(x):
 preflight(x);need(x['command'] in ['help','version']);need(x['observationLaunchId'] not in x['timingLaunchIds'] and x['timingLaunchIds']==list(range(1,22)))
 need(x['observer'] in (['strace-file-process'] if x['platform'].startswith('linux') else ['fs_usage-child','sandbox-deny-fixture-trees']));need(x['killedAndReaped'] is True)
 f=load('core-gate-design-fixtures.v1.json');need(x['fixturePins']==f['pins']);need(x['cwd']=='empty-workdir' and x['cwdEntries']==[] and x['envFixturePointers']==[] and x['pathFixtureExecutables']==[])
 need(isinstance(x['events'],list))
 for e in x['events']:need(set(e)=={'operation','tree'} and e['operation'] in ['open','read','exec','mmap','inventory-name','other'] and e['tree'] in ['component','project','elsewhere'])
 return result(not any(e['operation'] in ['open','read','exec','mmap'] and e['tree'] in ['component','project'] for e in x['events']),observedEvents=len(x['events']))
def rss_trace(t,source):
 need(t['target']=='spawned-measurement-process-T' and uint(t['exitMs']) and t['exitMs']>0)
 s=t['samples'];need(s and all(uint(q['elapsedMs']) and q['elapsedMs']==i*10 for i,q in enumerate(s)) and s[-1]['elapsedMs']<t['exitMs']<=s[-1]['elapsedMs']+10);need(all(uint(q['raw']) for q in s))
 values=[q['raw']*(1024 if source=='linux-VmRSS-kB' else 1) for q in s];need(all(uint(v) for v in values))
 steady=statistics.median([v for q,v in zip(s,values) if q['elapsedMs']>=20] or values);return steady,max(values)
def rss(x):
 if x['command'] in ['analyze','consented-probe']:return {'status':'OUTSIDE-G04','scored':False}
 preflight(x);need(x['command'] in ['help','version']);source='linux-VmRSS-kB' if x['platform'].startswith('linux') else 'macos-resident-size-bytes';need(x['source']==source and len(x['pairs'])==21)
 out=[]
 for i,p in enumerate(x['pairs']):
  need(p['pairId']==i+1 and set(p)=={'pairId','cold','warm'})
  for k in ['cold','warm']:out.append(rss_trace(p[k],source))
 return result(all(s<=40_000_000 and p<=50_000_000 for s,p in out),scored=True,launches=len(out),maxSteadyBytes=max(s for s,p in out),maxPeakBytes=max(p for s,p in out))
def delta(x):
 preflight(x);need(x['command']=='status-inventory' and x['endpoints']=='exec-handshake-to-last-inventory-field' and x['rssQuantity']=='peak');need(x['coreOnlyComponents']==[] and x['enabledComponents']==['typescript-test']);need(x['coreProjection']==x['enabledProjection']=='P-test')
 need(x['pairIds']==list(range(1,22)));need(all(ints(x[k],21) for k in ['coreStart','enabledStart','coreRss','enabledRss']));need(uint(x['downloadBytes']))
 need(isinstance(x['installedNodes'],list) and x['installedNodes']);
 for n in x['installedNodes']:need(n['type'] in ['file','directory','symlink'] and all(uint(n[k]) for k in ['device','inode','blocks']) and ('length' not in n or uint(n['length'])))
 z=DIST.installed_size(x['installedNodes']);need(z['status']!='NON-PASS');d={'download':x['downloadBytes'],'install':z['budgetBytes'],'start':statistics.median(x['enabledStart'])-statistics.median(x['coreStart']),'RSS':statistics.median(x['enabledRss'])-statistics.median(x['coreRss'])};need(x['published']==d)
 return result(d['start']>=0 and d['RSS']>=0,deltas=d)
def evaluate(model,x):
 try:return {'download':download,'inventory':inventory,'timing':timing,'no-load':no_load,'rss':rss,'delta':delta}[model](x)
 except (KeyError,ValueError,TypeError,OverflowError,RecursionError):return {'status':'NON-PASS'}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--report',type=Path,default=P/'core-gate-design-report.v1.json');args=ap.parse_args();c=load('core-gate-design-contract.v1.json');corpus=load('core-gate-design-cases.v1.json');rows=[]
 def check(i,a,e):rows.append({'id':i,'passed':a==e,'actual':a,'expected':e})
 for pin in c['sourcePins']:
  raw=(ROOT/pin['path']).read_bytes()
  if 'startHeading' in pin:
   t=raw.decode();raw=t[t.index(pin['startHeading']):t.index(pin['endHeading'])].encode()
  check('source/'+pin['path']+pin.get('startHeading',''),sha(raw),pin['sha256'])
 check('constants/scorer-law',c['constants'],{'decimalMB':1000000,'downloadBytesInclusive':25000000,'installedBytesInclusive':80000000,'timingN':21,'rank1Based':[11,20,21],'operativeTimingMs':[100,150,250,50,100],'helpVersionRssBytes':[40000000,50000000],'doctorRssBytes':[60000000,100000000],'rssCadenceMs':10,'deltaCaps':None})
 fixture=load('core-gate-design-fixtures.v1.json');observed={}
 for name,tree in fixture['trees'].items():
  entries=[]
  for item in tree:
   p=P/item['path'];check('fixture/'+item['path'],sha(p.read_bytes()),item['sha256']);entries.append([item['path'],item['sha256']])
  observed[name]=sha(json.dumps(entries,separators=(',',':')).encode())
 check('fixture/tree-pins',observed,fixture['pins'])
 before=copy.deepcopy(corpus)
 for case in corpus['cases']:
  value=copy.deepcopy(corpus['bases'][case['base']])
  for patch in case.get('patches',[]):
   at=value;parts=patch['path'].split('/')
   for k in parts[:-1]:at=at[int(k)] if isinstance(at,list) else at[k]
   k=parts[-1];k=int(k) if isinstance(at,list) else k
   if patch.get('remove'):del at[k]
   else:at[k]=patch['value']
  check('case/'+case['id'],evaluate(case['model'],value),case['expected'])
 check('case/input-unchanged',corpus==before,True)
 old=load('distribution-design-cases.v1.json')['cases'];ids=[]
 for case in old:
  if case['id'].startswith('G02.'):
   check('inherited/'+case['id'],DIST.installed_size(case['input']),case['expected']);ids.append('inherited/'+case['id'])
 doctor=load('doctor-cache-cases.v1.json')['cases'];docids=[]
 for case in doctor:
  if case['model']=='rss':
   actual=DOCTOR.rss(case['input']);check('doctor/'+case['id'],DOCTOR.contains(actual,case['expected']),True);docids.append('doctor/'+case['id'])
 all_states=[]
 for pin in c['catalogs']:
  v=json.loads((ROOT/pin).read_text());all_states.extend(s['id'] for s in v['initialStates'])
 mapped=[m['stateId'] for m in c['stateMap']];check('mapping/exact86',sorted(mapped),sorted(all_states));check('mapping/unique86',len(set(mapped)),86)
 result_ids={r['id'] for r in rows};caseids={s['id'] for s in corpus['cases']};check('case/unique-ids',len(caseids),len(corpus['cases']))
 for m in c['stateMap']:
  check('mapping/'+m['stateId'],bool(m['evidence']) and all(e in result_ids for e in m['evidence']) and m['classification'] in ['DESIGN-MAPPED','EXECUTION-OUTPUT'] and bool(m['executionRemainder']),True)
 check('inherited/G02-six',len(ids),6);check('doctor/rss-count',len(docids),c['doctorRssCaseCount'])
 subjects=['core-gate-design-contract.v1.json','core-gate-design-cases.v1.json','core-gate-design-fixtures.v1.json','core-gate-design-check.v1.py']
 report={'standing':'SYNTHETIC-DESIGN-EVIDENCE-NOT-QUALIFICATION','passed':sum(r['passed'] for r in rows),'total':len(rows),'stateCount':len(mapped),'syntheticCaseCount':len(corpus['cases']),'inheritedG02Cases':len(ids),'doctorRssCases':len(docids),'nativeProductRuns':0,'subjectPins':{n:sha((P/n).read_bytes()) for n in subjects},'results':rows}
 args.report.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['passed','total','syntheticCaseCount','stateCount']}));return 0 if report['passed']==report['total'] else 1
if __name__=='__main__':raise SystemExit(main())
