from pathlib import Path
import ast, copy, hashlib, importlib.util, json, sqlite3

SOURCE=Path('/tmp/opensip-design-corrections/claude-source38-advisory-author.v1/work/edited')
OUT=Path(__file__).parent
F=SOURCE/'docs/coop/design-corrections/foundation'
W=SOURCE/'docs/coop/design-corrections/workflows'
SEC=SOURCE/'docs/coop/design-corrections/security'
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
K=load('root_advisory_semantic',F/'check-semantic-replay.v3.py')
T=load('root_advisory_termination',F/'run_termination_model.v1.py')
WP=load('root_advisory_workflow',W/'workflow_projection_model.v3.py')
g,(run,objects,blobs),actual=K.case_declares_exists()
M=K.M
rid=M.close_run(run,objects,blobs)
derived=T.finalize(run,objects,blobs)['termination']
execution_plan_id=objects[run['evaluationSealId']][1]['executionPlanId']
stage_count=len(objects[execution_plan_id][1]['stages'])
eid='exec1_'+'a'*32
_,inventory=M.commit_inventory(rid,objects,blobs)
receipt={'schemaVersion':2,'runId':rid,'executionId':eid,'namespaceId':'root-reference',
    'commitSequence':1,'inventoryDigest':inventory,'sealedAssurance':'replayable','signerKeyId':'reference-host'}
attempt={'executionId':eid,'outcome':'completed','derivation':{'planId':run['planId'],
    'executionPlanId':execution_plan_id,'stageCount':stage_count,'stagesCompleted':stage_count}}
obs={'stepId':0,'durability':'authoritative','attempts':[attempt],'commitReceipt':receipt,'requiredClosureNotInstalled':False}
def vshape(value):WP.validate_profile('urn:opensip:product-v1:workflows:evaluator3:common:3#/$defs/StepTermination',value)
def vattempt(value):WP.validate_profile('urn:opensip:product-v1:workflows:evaluator3:invocation:3#/$defs/Attempt',value)
receipt_schema=copy.deepcopy(M.SCHEMA);receipt_schema['$ref']='#/$defs/commit-receipt'
def vreceipt(value):M.C.validate(receipt_schema,value)
rows=[]
for name in ['baseline','wrong-execution-plan','wrong-inventory-digest']:
    changed=copy.deepcopy(obs)
    if name=='wrong-execution-plan':changed['attempts'][0]['derivation']['executionPlanId']='exec-plan2:'+'e'*64
    if name=='wrong-inventory-digest':changed['commitReceipt']['inventoryDigest']='f'*64
    try:
        got=T.admit_analysis_step_termination(derived,run,objects,blobs,changed,vshape,vattempt,vreceipt)
        rows.append({'case':name,'outcome':'RETURNED','result':got})
    except Exception as exc:rows.append({'case':name,'outcome':'REFUSE','exceptionType':type(exc).__name__,'reason':str(exc)})
# Execute the exact owner dispatch function, with its exact constants/DDL and no rewritten branch.
# This is a bounded extraction, not an execution of the whole carrier checker.
cp=SEC/'check-carrier-v3.py';text=cp.read_text();tree=ast.parse(text)
fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_s37_open')
dispatch=json.loads((SEC/'carrier-dispatch.v3.json').read_text())
seven=dispatch['openDispatch']['sevenCarrierFormat3Objects']
query='SELECT name, sql FROM sqlite_master WHERE name IN (%s)'%','.join('?'*7)
ref=sqlite3.connect(':memory:');ref.executescript((SEC/'grant-journal.carrier.v3.sql').read_text())
env={'_S37_ADMITTED':'e'*64,'_S37_SEVEN':seven,'_S37_Q7':query,
    '_S37_REF_DEFS':dict(ref.execute(query,seven).fetchall())}
exec(compile(ast.Module(body=[fn],type_ignores=[]),str(cp),'exec'),env)
empty=sqlite3.connect(':memory:');association={'journalCarrierDigest':'e'*64,'grantGeneration':7}
before=list(empty.execute('SELECT type,name,sql FROM sqlite_master'))
route=env['_s37_open'](empty,'readOnlyRecovery',assoc=association)
after=list(empty.execute('SELECT type,name,sql FROM sqlite_master'))
report={'standing':'Root focused review of completed ce3 author bytes. Full admitted synthetic Run for composition probes; exact-function extraction on real empty SQLite for missing-carrier dispatch. No product qualification or integrated acceptance.',
    'source':str(SOURCE),'runId':rid,'actualRunExecutionPlanId':execution_plan_id,
    'actualInventoryDigest':inventory,'runAdmission':'ADMIT','terminationCases':rows,
    'noJournalCarrier':{'dispatch':route,'readOnlyStanding':dispatch['publicProjectionByPhase']['readOnlyStandingOfDispatchResult'].get(route),'sqliteUnchanged':before==after},
    'inputHashes':{str(p.relative_to(SOURCE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [F/'run_termination_model.v1.py',cp,SEC/'carrier-dispatch.v3.json']}}
(OUT/'probes.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
