"""A complete mixed-result rule can prove absence for its non-emitted fingerprints.

The two fully replayed Runs differ only in policy. A known finding on one file
must not make a different, fully evaluated file's result indeterminate.
Synthetic retained native evidence; no compiler or host qualification.
"""
from pathlib import Path
import importlib.util,json
HERE=Path(__file__).resolve().parent
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
R=load('knowledge_graph3',HERE.parent/'foundation/check-replay.v3.py')
P=load('knowledge_projection3',HERE/'workflow_projection_model.v3.py')
scope={'schemaFamily':'opensip.product.scope','schemaMajor':1,'include':['**'],'exclude':[]}
def build(pattern):
 graph=R.positive(scope_document=scope,atom_override={'op':'exists','relation':'file','minResolution':'enumerated',
                  'filters':[{'field':'subject','cmp':'glob','value':pattern}]})
 R.M.close_run(*graph)
 return graph
baseline=build('README.md');current=build('src/**')
bv=P.project_admitted_run_v3(*baseline);cv=P.project_admitted_run_v3(*current)
assert bv['snapshotId']==cv['snapshotId']
for view in (bv,cv):
 roots=P.admitted_root_predicate_values(view,view['policy']['rules'][0]['ruleId'])
 assert set(roots.values())=={'true','false'}
 assert not view['executionDeficiencies']
art=P.adopt_admitted_baseline_v3(*baseline,{'exportedAtUtc':'2026-09-08T00:00:00Z','exportedByHostRelease':'1.0.0'})
closures={k:{'bytes':'ok','trust':'admitted','trustOrigin':'retained-generation','protocolMajor':v['protocolMajor'],'platform':v['platform']}
          for k,(d,v) in baseline[1].items() if d=='closure'}
host={'closures':closures,'protocolMajors':sorted({v['protocolMajor'] for v in closures.values()}),
      'platform':'macos-aarch64','pivotRunId':bv['runId'],'recipeMajors':[2]}
comparison=P.compare_admitted_v3(baseline_artifact=art,current_run=current[0],current_objects=current[1],current_blobs=current[2],
                               host=host,profile_name='code-regression',pivot_runs={'E1':baseline})
d=comparison['descriptor'];entries=d['entries']
assert len(entries)==2 and all(e['classification']=='POLICY-DELTA' for e in entries),entries
assert {e['direction'] for e in entries}=={'appeared','vanished'},entries
appeared=next(e for e in entries if e['direction']=='appeared')
assert appeared['presence']['E1'] is False and appeared['presence']['E4'] is True
assert d['pivotsAvailable']['E1']=='available' and d['verdict']=='pass',d
print(json.dumps({'standing':'Reference regression over two complete owner-admitted and semantically replayed Runs; trust observations synthetic',
 'passed':True,'count':1,'results':[{'case':'mixed-determinate-rule-preserves-policy-attribution','baselineRunId':bv['runId'],
 'currentRunId':cv['runId'],'comparison':comparison}],'productQualification':False},indent=2))
