"""Proposed additive schema fragments; final major/source selection remains pending."""
from pathlib import Path
import copy
import hashlib
import json

HERE=Path(__file__).resolve().parent
pins=json.loads((HERE/'input-pins.json').read_text())['files']
sources={}
for row in pins:
    raw=Path(row['path']).read_bytes()
    assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
    sources[row['role']]=raw
common=json.loads(sources['common3'])
params={'type':'object','additionalProperties':False,'required':['kind','operation','sourceStep'],
        'properties':{'kind':{'const':'query'},'operation':{'const':'candidate.list'},'sourceStep':copy.deepcopy(common['$defs']['StepId'])}}
nulls={k:{'type':'null'} for k in ['candidates','evidenceLevels','candidatesTruncated','candidatesTotalItems','candidatesNextCursor']}
parity={'type':'object','additionalProperties':False,'required':['runId',*nulls,'candidatesAvailability'],
        'properties':{'runId':copy.deepcopy(common['$defs']['RunId']),**nulls,'candidatesAvailability':{'const':'unavailable-query-result'}}}
report={'type':'object','additionalProperties':False,'required':['state','queryOutcome','parity'],
        'properties':{'state':{'const':'unavailable-query-result'},'queryOutcome':{'enum':['cancelled','skipped','failed','rejected']},'parity':parity}}
guard={'if':{'required':['advisoryReport'],'properties':{'advisoryReport':{'properties':{'state':{'const':'unavailable-query-result'}}}}},
       'then':{'properties':{'kind':{'const':'run'},'termination':{'properties':{'class':{'const':'interrupted'}}},'run':{'required':['runId'],'properties':{'authority':{'const':'authoritative'}}}}}}
patch={'standing':'Unaccepted owner fragments, not a selected schema major or complete report integration',
       'invocation':{'addDef':{'FitQueryFromAnalysisParams':params},'appendQueryParamsOneOf':{'$ref':'#/$defs/FitQueryFromAnalysisParams'}},
       'envelope':{'appendFitAdvisoryReportOneOf':report,'appendRootAllOf':guard},
       'semanticJoins':['source step is earlier analysis and explicit completed dependency','resolve project from invocation and exact Run from source result','completed response binds request/step/attempt and exact query summary','unavailable query outcome matches actual noncompleted query','RunId and all null parity fields match interrupted run carrier'],
       'finalSourceDuties':['Choose and bind invocation/envelope successor majors','Compose timing and interruption successors','Update builtin planning grammar, query dispatcher and inventory descriptions','Update report builder, admission and every parity rendering','Implement private completion response custody']}
for name,value in [('fit-query-from-analysis.schema.json',params),('fit-query-unavailable.schema.json',report),('successor-fragments.json',patch)]:
    (HERE/name).write_text(json.dumps(value,indent=2)+'\n')
