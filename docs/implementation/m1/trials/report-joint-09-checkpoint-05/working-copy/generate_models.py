"""Rebase only declared owner model version support; no host implementation."""
from pathlib import Path
import hashlib
import json

HERE=Path(__file__).resolve().parent
subjects=json.loads((HERE/'input-subjects.json').read_text())['subjects']
rows={}
for s in subjects:
    raw=Path(s['manifest']).read_bytes();assert hashlib.sha256(raw).hexdigest()==s['manifestSha256']
    rows[s['unit']]=(Path(s['subject']),{r['path']:r for r in json.loads(raw)['files']})


def read(unit,name):
    base,manifest=rows[unit];pin=manifest[name];raw=(base/name).read_bytes()
    assert len(raw)==pin['bytes'] and hashlib.sha256(raw).hexdigest()==pin['sha256']
    return raw


timing=json.loads(read('workflow-timing','invocation-record.v4.schema.json'))
joint=json.loads((HERE/'composed-sources/invocation-record.proposed.schema.json').read_text())
def timing_common_successor(value):
    if isinstance(value,list):return [timing_common_successor(v) for v in value]
    if not isinstance(value,dict):return value
    out={k:timing_common_successor(v) for k,v in value.items()}
    if isinstance(out.get('$ref'),str):
        old='urn:opensip:product-v1:workflows:evaluator3:common:3'
        if out['$ref']==old or out['$ref'].startswith(old+'#'):out['$ref']=old[:-1]+'4'+out['$ref'][len(old):]
    return out
for name in ['Attempt','AttemptDurationV1','StepOutcome']:
    assert timing_common_successor(timing['$defs'][name])==joint['$defs'][name],name
assert joint['properties']['schemaMajor']['const']==5
assert json.loads((HERE/'composed-sources/graph-query.proposed.schema.json').read_text())['$defs']['GraphQueryResponseV1']['properties']['schemaMajor']['const']==4
specs=[
 ('report-projection','report_model.py','report_model.py','report-producer-majors'),
 ('report-evidence-design','reference_model.py','feature_model.py','feature-query-major4'),
 ('presentation-catalog','catalog.py','catalog.py',None),
 ('config-disclosure','disclosure.py','disclosure.py',None),
 ('workflow-timing','timing.py','timing.py','timing-major5'),
 ('history-selection','history.py','history/history.py',None),
 ('history-selection','query_history.py','history/query_history.py','query-major4'),
 ('history-selection','subject_run.py','history/subject_run.py',None),
 ('fit-interruption','fit_output.py','fit_output.py','fit-request-major4'),
 ('required-output','output_finalization.py','output_finalization.py',None),
]
outputs=[]
for unit,source,target,transform in specs:
    raw=read(unit,source);text=raw.decode()
    if transform=='timing-major5':
        assert text.count('(3, 4)')==2
        text=text.replace('(3, 4)','(3, 4, 5)')
        text=text.replace('v4 missing observed duration','selected timing source missing observed duration')
    elif transform=='query-major4':
        assert text.count("'schemaMajor':3")==2
        text=text.replace("'schemaMajor':3","'schemaMajor':4")
    elif transform=='report-producer-majors':
        assert text.count('"schemaMajor": 3')==2 and text.count('"schemaMajor": 6')==2
        text=text.replace('"schemaMajor": 3','"schemaMajor": 4').replace('"schemaMajor": 6','"schemaMajor": 7')
    elif transform=='feature-query-major4':
        assert text.count('"schemaMajor": 3')==1
        text=text.replace('"schemaMajor": 3','"schemaMajor": 4')
    elif transform=='fit-request-major4':
        assert text.count("'schemaMajor':3")==1
        text=text.replace("'schemaMajor':3","'schemaMajor':4")
    output=text.encode();compile(output,str(HERE/'models'/target),'exec')
    dest=HERE/'models'/target;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(output)
    outputs.append({'path':str(dest.relative_to(HERE)),'sourceUnit':unit,'source':source,'sourceSha256':hashlib.sha256(raw).hexdigest(),
                    'sha256':hashlib.sha256(output).hexdigest(),'bytes':len(output),'transform':transform or 'byte-identical'})
result={'standing':'Generated reference model proposals; not product/host custody or selected source closure',
        'timingCompatibility':'Invocation5 Attempt, AttemptDurationV1 and StepOutcome equal proposed timing invocation4 definitions after the explicit common3-to-common4 reference succession; timing projection laws and duration shapes remain unchanged. Unknown source majors remain incompatible.',
        'queryCompatibility':'New typed run.show, fit request and mock report graph producers emit query major4 directly; interruption constructors emit envelope7. Existing stored responses/envelopes are not relabeled, decoded or admitted through this transform. Actual public query owner/runtime rebinding remains required.',
        'outputs':outputs,
        'pending':['Joint model adapters for report construction/admission','Retained-source and full schema/Run joins','Fit planning/custody integration','Budget, whole report fixture and real renderer checks','Actual independent review and final generated source binding']}
(HERE/'model-generation-result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'generated':len(outputs),'transformed':sum(r['transform']!='byte-identical' for r in outputs)}))
