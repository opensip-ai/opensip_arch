from pathlib import Path
import copy, importlib.util, json

HERE = Path(__file__).parent
spec = importlib.util.spec_from_file_location('root_query_reader', HERE/'replay-query.py')
R = importlib.util.module_from_spec(spec)
spec.loader.exec_module(R)

row = {'vector':'control', 'run':'explicit', 'request':{'page':{'cursor':'opaque-unchanged'}},
       'hostObservations':{'requestId':'host-supplied'}, 'response':{'items':[]}}
class Owner:
    def __init__(self, structural=True, semantic=True):
        self.structural, self.semantic, self.semantic_calls = structural, semantic, 0
    def open_run_closure(self, *args):
        if not self.structural: raise ValueError('structural control')
        return 'run', {}
    def close_run(self, *args):
        self.semantic_calls += 1
        if not self.semantic: raise ValueError('semantic control')
        return 'run'
class Query:
    def __init__(self): self.calls=[]
    def execute_graph_query(self, request, run, objects, blobs, host):
        self.calls.append(copy.deepcopy((request,host)))
        request['mutation']='probe';host['mutation']='probe'
        return {'items':[]}
checks=[]
for structural,semantic in [(False,True),(True,False),(True,True)]:
    owner,query=Owner(structural,semantic),Query()
    before=copy.deepcopy(row)
    report={'cases':[],'structuralAdmission':'NOT-REACHED','semanticAdmission':'NOT-REACHED'}
    completed=R.execute_selected(owner,query,'run',{'run':('run',{})},{},[row],report)
    assert completed == (structural and semantic)
    assert owner.semantic_calls == int(structural)
    assert len(query.calls) == int(structural and semantic)
    assert row == before
    if query.calls:assert query.calls[0] == (row['request'],row['hostObservations'])
    checks.append({'structuralAdmitted':structural,'semanticAdmitted':semantic,
                   'queryCalls':len(query.calls),'passed':True})
real=json.loads(Path('/tmp/opensip-design-corrections/consumer-b.v24/output/vectors/graph-query.json').read_text())
labels=sorted({r['run'] for r in real['vectors']})
selected={label:len(R.selected_cases(real,label)) for label in labels}
assert sum(selected.values())==53
print(json.dumps({'standing':'Three synthetic admission-barrier/unchanged-input controls; actual53 vector rows parsed only. No product or consumer conformance.','passed':True,'controls':checks,'observedVectorPartitions':selected},indent=2))
