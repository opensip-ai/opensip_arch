from pathlib import Path
import subprocess,json,hashlib,concurrent.futures
R=Path('/tmp/opensip-design-corrections/claude-author-remint.v1');O=Path(__file__).parent;P=R/'package';S=R/'source';PY='/tmp/opensip-architecture-review-env/bin/python'
manifest=R/'scratch/artifact-manifest.json';assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='b4f90d217d30085c77bacbe57429d3acc9ff60144216dce73101f372ac235cfc'
d=json.loads(manifest.read_text());print('delivery keys',list(d),flush=True)
for r in d['artifacts']:
 p=R/'scratch'/r['path'];raw=p.read_bytes();assert hashlib.sha256(raw).hexdigest()==r['sha256'];assert len(raw)==r['bytes']
jobs=[('ts','a-checkpoint3/checkpoint3',False),('normalized','b-normalized/normalized-examples6',False),('rust-selections','c-rust-selection/rust-selection-examples1',False),('semantic-negatives','d-controls/semantic-controls1',True),('binding-controls','e-binding-controls',None)]
def run(job):
 name,rel,negative=job; inp=R/'scratch/out-a'/rel;out=O/name;assert not out.exists()
 cmd=[PY,'-I','-B',str(P/'check-export.v4.py'),'--input',str(inp),'--claims',str(inp/'claims.json'),'--source',str(S),'--out',str(out)]
 p=subprocess.run(cmd,capture_output=True,text=True);(O/(name+'.stdout')).write_text(p.stdout);(O/(name+'.stderr')).write_text(p.stderr)
 report=json.loads((out/'report.json').read_text());checks=report['checks'];assert all(c['ownerAdmission']=='ADMIT' for c in checks),report
 if negative is False:assert p.returncode==0 and report['passed'] and all(c['semanticAdmission']=='ADMIT' for c in checks),report
 elif negative is True:assert p.returncode==1 and all(c['semanticAdmission']=='REFUSE' for c in checks),report
 else:
  assert p.returncode==1
  for c in checks:
   wanted='REFUSE' if c['name']=='ts-invalid-default-entry' else 'ADMIT';assert c['semanticAdmission']==wanted,c
   if wanted=='REFUSE':assert 'ENUMERATION_BINDING_PROGRAM_ENTRY' in c['reason'],c
 result={'group':name,'expectedControlOutcome':True,'exitCode':p.returncode,'reportSha256':hashlib.sha256((out/'report.json').read_bytes()).hexdigest(),'checks':[{'name':c['name'],'runId':c['claimedRunId'],'ownerAdmission':c['ownerAdmission'],'semanticAdmission':c['semanticAdmission'],'reason':c.get('reason')} for c in checks]};print(name,'PASS',len(checks),flush=True);return result
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(run,jobs))
(O/'verification.json').write_text(json.dumps({'standing':'Root replay of exact actual Claude author exports through selected owner; not blind reconstruction or product qualification','sourceManifestSha256':hashlib.sha256((R/'source-manifest.json').read_bytes()).hexdigest(),'authorArtifactManifestSha256':hashlib.sha256(manifest.read_bytes()).hexdigest(),'groups':results,'passed':True},indent=2)+'\n')
