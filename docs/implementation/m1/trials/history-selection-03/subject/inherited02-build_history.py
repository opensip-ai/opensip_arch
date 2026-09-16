"""Root02 proposed typed history/query additions; parent sources stay unchanged."""
import ast,copy,hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
pins=json.loads((HERE/'input-pins.json').read_bytes())['files']
docs={}
for pin in pins:
 raw=Path(pin['path']).read_bytes();assert len(raw)==pin['bytes'] and hashlib.sha256(raw).hexdigest()==pin['sha256']
 if pin['path'].endswith('.json'):docs[pin['role']]=json.loads(raw)
def obj(props):return {'type':'object','additionalProperties':False,'required':list(props),'properties':props}
def ref(uri):return {'$ref':uri}
def write(name,data):(HERE/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
C=docs['common']['$id']+'#/$defs/'
Q=copy.deepcopy(docs['query-schema']);defs=Q['$defs']
item=obj({'runId':ref(C+'RunId'),'projectId':ref(C+'ProjectId'),
          'sealedRun':ref(docs['identity-schema']['$id']+'#/$defs/run'),
          'result':{'allOf':[ref(docs['invocation']['$id']+'#/$defs/AnalysisResult'),{'required':['runId'],'properties':{'authority':{'const':'authoritative'}}}]}})
defs['RunShowItemV1']=item
# This adds constraints to the already closed generic response. It does not
# replace other operation branches or silently claim they were typed already.
defs['RunShowResponseV1']={'properties':{'operation':{'const':'run.show'},'context':{'properties':{
 'resolvedView':ref('#/$defs/ResolvedView'),'availability':{'enum':['retained','expired','purged','corrupt','unavailable']},'truncated':{'const':False},'advisory':{'const':False}},'not':{'required':['nextCursor']}}},
 'allOf':[{'if':{'properties':{'context':{'properties':{'availability':{'const':'retained'}}}}},
 'then':{'properties':{'items':{'type':'array','minItems':1,'maxItems':1,'items':ref('#/$defs/RunShowItemV1')},'context':{'properties':{'coverage':{'const':'complete'},'totalItems':{'const':1}}}}},
 'else':{'properties':{'items':{'type':'array','maxItems':0},'context':{'properties':{'coverage':{'const':'unavailable'},'totalItems':{'const':0}}}}}}]}
defs['GraphQueryResponseV1'].setdefault('allOf',[]).append({'if':{'properties':{'operation':{'const':'run.show'}}},'then':ref('#/$defs/RunShowResponseV1')})
Q['description']+=' Root02 proposed addition: run.show resolves one exact Run and carries one typed RunShowItemV1 when retained, otherwise no items and explicit unavailable context. Other 19 operation response laws remain unchanged. Acceptance and source selection pending.'
write('graph-query.history-candidate.schema.json',Q)
selection=json.loads((HERE/'explicit-history.schema.json').read_bytes())
provenance={'verifiedInDocument':['current-run-equals-envelope-current-run','item-counts-consistent','rows-equal-requested-runs'],
 'hostAsserted':['selected-run-and-project-equal-typed-query-item','findings-belong-to-history-run','retained-read-snapshot-after-invocation-data-commits','typed-query-item-from-close-run-and-retained-receipt','byte-budget-rejected-delta-measurement']}
retained={'allOf':[ref(docs['report-schema']['$id']+'#/$defs/HistoryRunV1')]}
for state,code in [('expired','evidence.expired'),('purged','evidence.purged'),('corrupt','evidence.corrupt'),('unavailable','QUERY.VIEW_UNKNOWN')]:
 retained['allOf'].append({'if':{'required':['availability'],'properties':{'state':{'const':'unavailable'},'availability':{'const':state}}},'then':{'properties':{'detail':{'properties':{'code':{'const':code}}}}}})
slot={'oneOf':[obj({'state':{'const':'current-run'},'runId':ref(C+'RunId')}),ref('#/$defs/RetainedHistorySlotV1')]}
panel={'$schema':'https://json-schema.org/draft/2020-12/schema','$id':'urn:opensip:product-v1:report:explicit-history-panel:1',**obj({'selection':ref(selection['$id']),'runs':{'type':'array','minItems':1,'maxItems':4,'items':slot,'x-opensip-order':'sequence'},'provenance':{'const':provenance}}),'$defs':{'RetainedHistorySlotV1':retained}}
write('explicit-history-panel.schema.json',panel)
flag={'flag':'--history-run','owner':'workflow','class':'selection','join':'Value RUN_ID is exactly one full run3: followed by 64 lowercase hexadecimal digits. Repeatable 1..4 times, preserving argument order; IDs must be distinct. Requires --format html. No comma expansion, prefix, latest, implicit baseline or fallback. Presentation-only input. Help: Include this exact retained Run in the HTML history panel (repeat up to four times).'}
commands=[r['name'] for r in docs['command-inventory']['commands'] if 'html' in r['formats']];assert len(commands)==8
write('history-command-flags.json',{'standing':'root02 proposed exact additive inventory patch; no selected product grammar change','parentSchemaId':docs['command-inventory'].get('$id'),'rows':[{'command':name,'appendFlag':copy.deepcopy(flag)} for name in commands]})
write('history-route-goldens.json',{'standing':'root02 route tuples, not full D9 envelope goldens or CLI qualification','precedence':['command-known-option','format-applicability','lexical-shape-and-uniqueness','selection-count'],
 'cases':[{'case':'non-html','class':'request-rejected','code':'REQUEST.UNKNOWN_OPTION','exitCode':2,'detail':'OUTPUT.FORMAT_NOT_APPLICABLE'},
 {'case':'well-formed-over-four','class':'request-rejected','code':'REQUEST.UNSATISFIABLE','exitCode':2,'detail':'EVALUATION.SELECTION_LIMIT'},
 {'case':'malformed-empty-or-duplicate','class':'request-rejected','code':'REQUEST.UNSATISFIABLE','exitCode':2,'detail':'REPORT.HISTORY_SELECTION_INVALID'}]})

common=copy.deepcopy(docs['common'])
code='REPORT.HISTORY_SELECTION_INVALID'
assert code not in common['$defs']['DomainDetailCode']['enum']
common['$defs']['DomainDetailCode']['enum'].append(code)
write('common.history-candidate.schema.json',common)
detail_registry=copy.deepcopy(docs['detail-registry'])
assert all(row['code']!=code for row in detail_registry['records'])
detail_registry['records'].append({'code':code,'owner':'workflows','selector':'Explicit report history request: empty, malformed or duplicate full Run IDs; request-rejected / REQUEST.UNSATISFIABLE / exit2. This is not the non-applicable-format or selection-count-limit route.'})
detail_registry['records'].sort(key=lambda row:row['code'])
write('public-detail-registry.history-candidate.json',detail_registry)

report_checker=next(row for row in pins if row['role']=='report-admission')
tree=ast.parse(Path(report_checker['path']).read_bytes())
subject_run=next(node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name=='subject_run')
(HERE/'subject_run.py').write_text('# Generated exact AST extraction from pinned report08 subject_run; no semantic change.\n'+ast.unparse(subject_run)+'\n')
