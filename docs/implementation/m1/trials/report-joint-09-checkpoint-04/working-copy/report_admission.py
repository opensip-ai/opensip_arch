"""Joint report consumer candidate, retaining the original report admission laws.

The old automatic-history block is used only for automatic selection. Explicit
history uses its own exact selection/slot joins. New owner source admission and
product/browser implementation remain separate duties; internal joins are not
proof that the host supplied every retained input.
"""
from pathlib import Path
import ast,copy,hashlib,json,types
HERE=Path(__file__).resolve().parent
PLANNING={'__file__':str(HERE/'planning_owner.py')}
exec(compile((HERE/'planning_owner.py').read_bytes(),str(HERE/'planning_owner.py'),'exec'),PLANNING)
METADATA={'__file__':str(HERE/'metadata_owner.py')}
exec(compile((HERE/'metadata_owner.py').read_bytes(),str(HERE/'metadata_owner.py'),'exec'),METADATA)


def compiled_parent(read_unit):
    source=read_unit('report-projection','check.py')
    names={'Refused','need','sha','pointer_get','scan_depth','parse_report','embedded_owner_records',
           'admit_envelope','subject_run','check_projection','admit_ledger','admit_document'}
    nodes=[n for n in ast.parse(source).body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in names]
    assert {n.name for n in nodes}==names
    function=next(n for n in nodes if n.name=='admit_document');count=0
    for n in ast.walk(function):
        if isinstance(n,ast.If) and ast.unparse(n.test)=='present(history)':
            n.test=ast.parse("present(history) and history['data']['selection'].get('policy') != 'explicit-run-ids.1'",mode='eval').body
            count+=1
    assert count==1
    return compile(ast.fix_missing_locations(ast.Module(body=nodes,type_ignores=[])),'pinned-report08-admission#explicit-history-branch','exec')


def admit(raw,validation,model,joins,catalog,query_summary,feature=None):
    # Parse with the same codec before deriving any selection-sensitive joins.
    namespace={'copy':copy,'json':json,'hashlib':hashlib,'EXIT':model.EXIT,
               'ENV6':'urn:opensip:product-v1:workflows:evaluator3:command-envelope:7'}
    exec(compiled_parent(validation.read_unit),namespace)
    budget={k:copy.deepcopy(v['const']) for k,v in validation.report['$defs']['BudgetProfileV1']['properties'].items()}
    ctx=types.SimpleNamespace(reference=validation.C,M=model,budget=budget,schema=validation.report,registry=validation.registry,
        documents=validation.schemas,inventory5=METADATA['read']('inventory'),
        planning=PLANNING['read'](),
        derivations=json.loads((HERE/'joint-budget-derivation.json').read_bytes()),
        qsp=types.SimpleNamespace(command_surface_summary=query_summary,QuerySurfaceProjectionError=query_summary.__globals__['QuerySurfaceProjectionError']))
    parsed=namespace['parse_report'](ctx,raw)
    try:validation.validate(validation.report['$id'],parsed)
    except validation.C.ValidationError as error:raise namespace['Refused']('SCHEMA',error.message[:120]) from error
    current=namespace['subject_run'](parsed['envelope'],parsed['command'])
    selected=parsed['disclosures']['explicitHistorySelection']
    model_view=types.SimpleNamespace(**{k:v for k,v in vars(model).items() if not k.startswith('__')})
    model_view.document_disclosures=lambda panels:joins.disclosures(panels,selected,model,validation.H,current,lambda v:validation.validate(validation.history_schema['$id'],v))
    ctx.M=model_view
    doc=namespace['admit_document'](ctx,raw)
    run=doc['envelope'].get('run')
    preview=doc['envelope'].get('queryRecord',{}).get('plan') if doc['command']=='repair-preview' else None
    joins.additions(doc,current,run,preview,model,validation.H,validation.T,catalog,validation.C,lambda v:validation.validate(validation.history_schema['$id'],v))
    # Feature panels embed complete query4 request/response records. Apply
    # their original standalone codec boundary too; a larger enclosing report
    # profile never permits a deeper or oversized public query document.
    pending=[doc['panels'].get(name) for name in ['symbolEvidence','coupling']]
    while pending:
        value=pending.pop()
        if isinstance(value,dict):
            if value.get('schemaFamily')=='opensip.product.query':
                validation.C.typed(value)
                if len(model.canonical(value))>budget['embeddedPanelOwnerMaxCanonicalBytes']:
                    raise ValueError('FEATURE-QUERY-CODEC-BYTES')
            pending.extend(value.values())
        elif isinstance(value,list):pending.extend(value)
    panels=doc['panels'];present=lambda v:v.get('state')=='present'
    if any(present(panels.get(k,{})) for k in ['symbolEvidence','coupling']):
        if feature is None:raise ValueError('feature owner required for present evidence panels')
        feature.admit_panel_prerequisites(panels)
        feature.admit_successor_placement(panels,budget['explorationMaxCanonicalBytes'])
        placement={}
        exec(compile((HERE/'joint_placement.py').read_bytes(),str(HERE/'joint_placement.py'),'exec'),placement)
        cap=model.effective_exploration_budget(budget,doc['envelope'],doc['invocationLedger'],validation.report['required'])
        def allowed(name):
            return placement['allocation'](panels,name,budget['projectionPriority'],cap,model)
        if present(panels.get('symbolEvidence',{})):
            data=panels['symbolEvidence']['data'];resolution=panels['graph']['data']['subjectResolution']
            feature.admit_symbol_evidence(data,{'projectId':doc['envelope']['projectId'],'runId':current,'resolution':resolution,'graphResolution':resolution,'bounds':feature.PUBLIC_BOUNDS,'budget':allowed('symbolEvidence')})
            placement['check_feature_deltas'](data,allowed('symbolEvidence'),model)
        if present(panels.get('coupling',{})):
            data=panels['coupling']['data'];feature.admit_coupling(data,current,allowed('coupling'))
            placement['check_feature_deltas'](data,allowed('coupling'),model)
    return doc
