"""Author audit probes against frozen candidate25; never edits the candidate."""
import argparse, copy, importlib.util, json
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('--source',type=Path,required=True); p.add_argument('--out',type=Path,required=True); p.add_argument('--expect-corrected',action='store_true'); a=p.parse_args()
def load(name,path):
 s=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
D=a.source/'docs/coop/design-corrections'
K=load('audit_security_checks',D/'security/check-security-lifecycle.v1.py'); S=K.model
N=load('audit_native',D/'native/native_evidence_model.v2.py')
rows=[]
def observe(name,ctx,expected):
 result=S.discovery(ctx); row={'name':name,'expectedFromContract':expected,'status':result['status'],'refusal':result.get('refusal'),'detail':result.get('detail'),'units':len(result['provenance']['units']),'nestedRepositories':result['provenance']['nestedRepositories'],'nestedProjects':result['provenance']['nestedProjects']}; rows.append(row); return result
base=K._synthetic_repo(0,0); root=base['cwd']
observe('single-root-control',base,'ACCEPT: one first-party root')
observe('4200-first-party-control',K._synthetic_repo(4200,0),'REFUSE: 4201 selected first-party directories exceeds 4096')
observe('4200-installed-control',K._synthetic_repo(0,4200),'ACCEPT: dependency tree excluded')
for boundary in ['nested-repository','nested-project']:
 ctx=copy.deepcopy(base); sub=root+'/separate'; ctx['fs'][sub]={'kind':'dir','uid':1000,'mode':'0755','dev':1}
 if boundary=='nested-repository': ctx['fs'][sub]['vcs']=True
 else: ctx['fs'][sub+'/opensip.json']={'kind':'file','uid':1000,'mode':'0644','nlink':1,'size':100}
 for i in range(4200):
  d=sub+f'/pkg{i:04d}';ctx['fs'][d]={'kind':'dir','uid':1000,'mode':'0755','dev':1};ctx['fs'][d+'/package.json']={'kind':'file','uid':1000,'mode':'0644','nlink':1,'size':100}
 observe(boundary+'-4200',ctx,'ACCEPT: one first-party root; nested authority tree is excluded')
ctx=K._synthetic_repo(4200,0);ctx['configWorkspaceRoots']=['.']
security=observe('explicit-root-security-control',ctx,'ACCEPT: explicit root suppresses automatic selection')
markers={k[len(root)+1:]:{'sha256':'a'*64} for k,v in ctx['fs'].items() if k.startswith(root+'/') and k.endswith('/package.json')}
boundaries=S.boundary_inventory(security)
native=N.discover_units(markers,['.'],boundaries)
rows.append({'name':'same-explicit-root-native','expectedFromContract':'ACCEPT: same single selected root as security','units':len(native['units']),'refused':native['refused']})
assert rows[0]['status']=='ACCEPT' and rows[1]['status']=='REFUSE' and rows[2]['status']=='ACCEPT'
if a.expect_corrected:
 assert rows[3]['status']==rows[4]['status']=='ACCEPT'
 assert rows[3]['units']==rows[4]['units']==1
 assert rows[5]['status']=='ACCEPT' and rows[6]['refused'] is None and rows[6]['units']==1
else:
 assert rows[3]['refusal']==rows[4]['refusal']=='PROJECT.WORKSPACE_UNIT_LIMIT'
 assert rows[5]['status']=='ACCEPT' and rows[6]['refused']['detail']=='native.too-many-units'
a.out.write_text(json.dumps({'standing':'AUTHOR CORRECTION CHECK; not independent acceptance' if a.expect_corrected else 'AUTHOR REPRODUCTION; confirms discrepancies, not a passing conformance suite','source':str(a.source),'observations':rows},indent=2)+'\n')
print('PASS author corrected expectations' if a.expect_corrected else 'Reproduced candidate25 discrepancies; controls behaved as specified.')
