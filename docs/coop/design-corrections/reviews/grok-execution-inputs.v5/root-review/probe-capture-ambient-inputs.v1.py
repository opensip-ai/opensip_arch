from pathlib import Path
import importlib.util,copy,json,hashlib
p=Path('/tmp/opensip-design-corrections/evaluator-successor.v1/docs/coop/design-corrections/foundation')
def load(n,f):
    s=importlib.util.spec_from_file_location(n,p/f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
F=load('ambient_F','evaluator_graph_fixture.v3.py');H=load('ambient_H','execution_inputs_fixture.v3.py')
g=F.build_file_inputs(complete_required_native=True);m1,d1=H.build_manifest(g)
g2=copy.deepcopy(g);raw=b'unrelated cached bytes, never selected'
g2['blobs'][hashlib.sha256(raw).hexdigest()]=raw;m2,d2=H.build_manifest(g2)
print(json.dumps({'standing':'bounded host-capture input identity probe; no full Run claim',
    'samePlan':g['inputs']['planId']==g2['inputs']['planId'],
    'sameSelectedRefs':m1['selectedRefs']==m2['selectedRefs'],
    'digestWithoutAmbient':d1,'digestWithAmbient':d2,
    'changedFields':[k for k in m1 if m1[k]!=m2[k]]},indent=2))
