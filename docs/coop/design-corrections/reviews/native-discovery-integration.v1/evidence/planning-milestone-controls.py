import importlib.util,json,copy
from pathlib import Path
R=Path('/Users/sb/code/opensip-ai/opensip_arch');S=Path('/tmp/opensip-design-corrections/candidate-subject.v25');O=Path(__file__).parent
s=importlib.util.spec_from_file_location('planning_check',R/'docs/operations/check_implementation_planning.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
data=m.load(R/'docs/v2/architecture/implementation-coverage.v1.json');inventory=m.load(R/'docs/v2/architecture/repository-file-inventory.v1.json')
sources={}
for k,r in data['sources'].items():
 raw=((R if r.get('location')=='working-tree' else S)/r['path']).read_bytes();assert m.sha(raw)==r['sha256'];sources[k]=json.loads(raw) if r['path'].endswith('.json') else raw.decode()
m.validate_coverage(data,sources,inventory)
rows=[]
for kind in ['advertised-renderer','command-golden']:
 d=copy.deepcopy(data)
 if kind=='advertised-renderer':
  row=next(r for r in d['groups']['commands'] if r['id']=='analyze');row['milestone']='M3';wanted='Command delivery precedes an advertised renderer'
 else:
  row=d['groups']['workflowGoldens'][0];row['milestone']='M3';wanted='Golden delivery precedes its command'
 try:m.validate_coverage(d,sources,inventory);raise AssertionError('Mutation admitted')
 except ValueError as e:assert wanted in str(e),str(e);rows.append({'mutation':kind,'refused':True,'reason':str(e)})
(O/'planning-milestone-controls.json').write_text(json.dumps({'standing':'Documentation invariant controls only','baseline':'PASS','controls':rows},indent=2)+'\n');print(rows)
