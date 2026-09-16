"""First joint source composition pass. Not a complete report or selected closure."""
from pathlib import Path
import ast
import copy
import hashlib
import json

HERE=Path(__file__).resolve().parent
ARCH=Path('/Users/sb/code/opensip-ai/opensip_arch')
SUBJECTS=json.loads((HERE/'input-subjects.json').read_text())['subjects']
MANIFESTS={}
READS={}
for row in SUBJECTS:
    raw=Path(row['manifest']).read_bytes()
    assert hashlib.sha256(raw).hexdigest()==row['manifestSha256']
    MANIFESTS[row['unit']]=(Path(row['subject']),{r['path']:r for r in json.loads(raw)['files']})


def read(unit,relative):
    base,entries=MANIFESTS[unit];row=entries[relative];path=base/relative
    raw=path.read_bytes()
    assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],path
    READS[str(path)]={'path':str(path),'sha256':row['sha256'],'bytes':len(raw)}
    return raw


def document(unit,relative):
    return json.loads(read(unit,relative))


def external(row):
    raw=Path(row['path']).read_bytes()
    assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],row['path']
    READS[row['path']]={'path':row['path'],'sha256':row['sha256'],'bytes':row['bytes']}
    return raw


def remap_refs(value,mapping):
    if isinstance(value,list):return [remap_refs(v,mapping) for v in value]
    if not isinstance(value,dict):return value
    out={k:remap_refs(v,mapping) for k,v in value.items()}
    if '$ref' in out:
        uri,sep,fragment=out['$ref'].partition('#')
        if uri in mapping:out['$ref']=mapping[uri]+(sep+fragment if sep else '')
    return out


report=document('report-projection','report-projection.schema.json')
patch=document('report-evidence-design','owner/report-projection-successor-patch.v2.json')
old_report=json.loads(external(patch['parent']))
# Check the actual parent delta rather than assuming any report07 patch applies.
restored=copy.deepcopy(report)
assert restored['properties']['envelope']['$ref'].endswith(':6')
restored['properties']['envelope']=copy.deepcopy(old_report['properties']['envelope'])
assert report['description']==old_report['description'].replace('envelope (command-envelope:5)','envelope (command-envelope:6, jointly selected with its envelope5 parent)')
restored['description']=old_report['description']
assert restored==old_report,'unaccounted report07-to08 delta'

tree=ast.parse(read('report-evidence-design','check.py'))
names={'unescape','pointer_parent','resolve_pointer','PatchRefused','apply_semantic'}
nodes=[n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in names]
assert {n.name for n in nodes}==names
ops={'copy':copy}
exec(compile(ast.Module(body=nodes,type_ignores=[]),'pinned-feature02-patch-owner','exec'),ops)
report=ops['apply_semantic'](report,patch['ops'])

fit=document('fit-interruption','successor-fragments.json')
invocation=document('workflow-timing','invocation-record.v4.schema.json')
old_invocation=invocation['$id'];new_invocation=old_invocation.rsplit(':',1)[0]+':5'
for name,value in fit['invocation']['addDef'].items():
    assert name not in invocation['$defs'];invocation['$defs'][name]=copy.deepcopy(value)
assert fit['invocation']['appendQueryParamsOneOf'] not in invocation['$defs']['QueryParams']['oneOf']
invocation['$defs']['QueryParams']['oneOf'].append(copy.deepcopy(fit['invocation']['appendQueryParamsOneOf']))
invocation['$id']=new_invocation;invocation['properties']['schemaMajor']['const']=5
invocation['title']='Proposed invocation5: timing observations and fit query source-step binding'
invocation['description']+=' Joint unaccepted successor5 adds only the closed FitQueryFromAnalysisParams alternative. Host source-step, completion and private response joins are separate mandatory laws.'

pins=document('report-projection','source-pins.json')['files']
path=str(ARCH/'docs/implementation/m1/trials/interruption-envelope-07/subject/command-envelope.v6.schema.json')
envelope=json.loads(external(next(r for r in pins if r['path']==path)))
old_envelope=envelope['$id'];new_envelope=old_envelope.rsplit(':',1)[0]+':7'
envelope['$defs']['FitAdvisoryReportV1']['oneOf'].append(copy.deepcopy(fit['envelope']['appendFitAdvisoryReportOneOf']))
envelope['allOf'].append(copy.deepcopy(fit['envelope']['appendRootAllOf']))
envelope['$id']=new_envelope;envelope['properties']['schemaMajor']['const']=7
envelope['title']='Proposed envelope7: total interrupted-fit advisory parity'
envelope['description']+=' Joint unaccepted successor7 adds explicit unavailable-query-result parity for an interrupted authoritative fit carrier. Completed query responses are preserved by private host completion custody.'

query=document('history-selection','graph-query.history-candidate.schema.json')
old_query=query['$id'];new_query=old_query.rsplit(':',1)[0]+':4'
query['$id']=new_query
changed=[]
for name,value in query['$defs'].items():
    major=value.get('properties',{}).get('schemaMajor',{})
    if major.get('const')==3:
        major['const']=4;changed.append(name)
assert set(changed)=={'GraphQueryRequestV1','GraphQueryResponseV1'},changed
query['title']='Proposed graph query4 with typed run.show response'
query['description']=query.get('description','')+' Joint integration proposes major4 for the refined run.show response. All existing v3 documents remain historical; typed authority cannot be obtained by relabeling a legacy cached item.'

policy_path=str(ARCH/'docs/coop/design-corrections/workflows/schemas/policy-document.v2.schema.json')
policy=json.loads(external(next(r for r in pins if r['path']==policy_path)))
orphan='AtomSuccessorV1';orphan_ref=policy['$id']+'#/$defs/'+orphan
assert policy['$defs'][orphan]['description'].startswith('Proposed Atom extension:')
assert policy['$defs'][orphan]['properties']['filters']['items']['$ref']=='#/$defs/FieldFilterSuccessorV1'
assert 'FieldFilterSuccessorV1' not in policy['$defs']
encoded=json.dumps(policy)
assert encoded.count('"$ref": "#/$defs/'+orphan+'"')==0
supplement=json.loads((HERE/'supplemental-inputs.json').read_text())['files']
options=json.loads(external(next(r for r in supplement if r['role']=='prior-generator-options')))
assert len(options['entryPoints'])==587 and not any(r['ref']==orphan_ref for r in options['entryPoints'])
removed_policy_definition=policy['$defs'].pop(orphan)

sources={'report-projection.proposed.schema.json':report,'invocation-record.proposed.schema.json':invocation,
         'command-envelope.proposed.schema.json':envelope,'graph-query.proposed.schema.json':query,
         'common.proposed.schema.json':document('history-selection','common.history-candidate.schema.json'),
         'configuration-disclosure.schema.json':document('config-disclosure','configuration-disclosure.schema.json'),
         'presentation-catalog.schema.json':document('presentation-catalog','presentation-catalog.schema.json'),
         'explicit-history.schema.json':document('history-selection','explicit-history.schema.json'),
         'explicit-history-panel.schema.json':document('history-selection','explicit-history-panel.schema.json'),
         'policy.proposed.schema.json':policy}
mapping={old_invocation:new_invocation,old_invocation.rsplit(':',1)[0]+':3':new_invocation,old_envelope:new_envelope,old_query:new_query}
# Keep fragment-local references intact. Full selected registry closure and all
# producer/consumer rebindings are still required in subsequent integration work.
sources={name:remap_refs(value,mapping) for name,value in sources.items()}
carrier_scope={}
exec(compile((HERE/'report_carriers.py').read_bytes(),str(HERE/'report_carriers.py'),'exec'),carrier_scope)
sources['report-projection.proposed.schema.json']=carrier_scope['integrate'](
    sources['report-projection.proposed.schema.json'],sources['invocation-record.proposed.schema.json'],
    sources['configuration-disclosure.schema.json']['$id'],sources['explicit-history.schema.json']['$id'],
    sources['explicit-history-panel.schema.json']['$id'])
catalog_scope={}
exec(compile((HERE/'catalog_carrier.py').read_bytes(),str(HERE/'catalog_carrier.py'),'exec'),catalog_scope)
sources['report-projection.proposed.schema.json']=catalog_scope['integrate'](
    sources['report-projection.proposed.schema.json'],sources['presentation-catalog.schema.json'])
out=HERE/'composed-sources';out.mkdir(exist_ok=True)
for name,value in sources.items():(out/name).write_text(json.dumps(value,indent=2)+'\n')
result={'standing':'First joint schema composition only; not full report integration, selected majors, independent approval or product qualification',
        'accountedParentChange':'report07 envelope reference5 to report08 reference6 and its exact descriptive phrase, with no other schema delta',
        'featureOpsApplied':len(patch['ops']),'queryMajorFieldsChanged':changed,
        'proposedMajors':{'invocation':5,'envelope':7,'graphQuery':4,'report':1},
        'majorDecision':'Breaking query refinement gets a proposed new major; actual review and complete caller/generated/source closure remain required',
        'policyCleanup':{'parent':policy_path,'removed':'/$defs/'+orphan,'removedValue':removed_policy_definition,
                         'reason':'Unreferenced stale proposal has a dangling FieldFilterSuccessorV1 reference; absent from all587 prior accepted generator entry points',
                         'preserved':'Every other policy schema JSON value and all selected policy definitions; accepted original file unchanged',
                         'requires':'Explicit source successor selection and actual independent review; final generator root list must preserve exclusion'},
        'outputs':[{'path':'composed-sources/'+name,'sha256':hashlib.sha256((out/name).read_bytes()).hexdigest(),'bytes':(out/name).stat().st_size} for name in sources],
        'reads':list(READS.values()),
        'pending':['Semantic fixture integration for new catalogue/configuration/timing/history carriers','Full selected registry and reference rebinding','Fit builtin planning and completion response model integration','Whole-document budget and all parent tests','Required output policy/source succession','Actual independent review']}
(HERE/'composition-result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['standing','featureOpsApplied','proposedMajors']}))
