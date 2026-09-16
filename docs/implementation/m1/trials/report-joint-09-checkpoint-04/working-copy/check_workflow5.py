"""Joint reference replay: full invocation5 shape and finalized report ledger."""
from pathlib import Path
import copy
import json
import types
import unittest
HERE=Path(__file__).resolve().parent

def load(path,name):
    module=types.ModuleType(name);module.__file__=str(path)
    exec(compile(path.read_bytes(),str(path),'exec'),module.__dict__)
    return module

V=load(HERE/'check_model_carriers.py','carriers')
W=load(HERE/'workflow5_replay.py','workflow5')
M=load(HERE/'models/report_model.py','report5')
F=load(HERE/'models/fit_output.py','fit5')
J=load(HERE/'fit_join.py','fit_join')
INV='urn:opensip:product-v1:workflows:evaluator3:invocation:5'
fixture=json.loads(V.read_unit('report-projection','fixtures.json'))
GOLDENS=[g for g in fixture['interruptionGoldens']['scenarios'] if g['command']=='fit']

def validate(kind,value):
    suffix={'planned-steps':'#/properties/orderedSteps','step-params':'#/$defs/FitQueryFromAnalysisParams','invocation':''}[kind]
    V.validate(INV+suffix,value)

def base(golden):
    record=copy.deepcopy(golden['invocationRecord'])
    for k in ['stepResults','termination','terminationEmitted','cancellation']:record.pop(k,None)
    record['schemaMajor']=5
    record['orderedSteps'][1]['params']={'kind':'query','operation':'candidate.list','sourceStep':0}
    return record

def project_ledger(record,golden):
    roles={0:'primary-analysis',1:'query',2:'render'}
    if len(record['orderedSteps'])>3:roles[3]='optional-export'
    shape=V.report['$defs']['InvocationLedgerV1']
    value=W.ledger(record,roles,golden['variant'],V.T,M,shape)
    V.validate(V.report['$id']+'#/$defs/InvocationLedgerV1',value)
    return value

class WorkflowTests(unittest.TestCase):
    def test_fresh_fit_replay_preserves_interruption_and_projects_timing(self):
        self.assertGreaterEqual(len(GOLDENS),3)
        for golden in GOLDENS:
            with self.subTest(golden=golden['id']):
                b=base(golden);script=copy.deepcopy(golden['ownerScript']);before=copy.deepcopy((b,script))
                record,code,_=W.replay(b,script,V.C.canonical,V.T,validate)
                self.assertEqual((b,script),before)
                self.assertEqual(code,golden['exitCode'])
                self.assertEqual(record['termination'],golden['invocationRecord']['termination'])
                ledger=project_ledger(record,golden)
                self.assertEqual(M.invocation_aggregate(ledger['steps'],ledger['cancellation']),record['termination'])
                for step in ledger['steps']:
                    for attempt in step['attempts']:
                        self.assertEqual(attempt['sourceSchemaMajor'],5)
                        self.assertEqual(attempt['duration'],{'state':'unavailable','reason':'clock-unavailable'})

    def test_private_observations_produce_measured_service_time(self):
        g=next(g for g in GOLDENS if g['scenario']=='signal-before-required-render')
        script=copy.deepcopy(g['ownerScript'])
        script['0'][0]['clockSamples']={'startNs':1000000,'endNs':5000000}
        script['1'][0]['clockSamples']={'startNs':100,'endNs':2000100}
        record,_,_=W.replay(base(g),script,V.C.canonical,V.T,validate)
        ledger=project_ledger(record,g)
        self.assertEqual(ledger['steps'][0]['attemptServiceTime'],{'state':'measured','attemptCount':1,'milliseconds':4})
        self.assertEqual(ledger['steps'][1]['attemptServiceTime'],{'state':'measured','attemptCount':1,'milliseconds':2})
        self.assertEqual(ledger['steps'][2]['attemptServiceTime'],{'state':'no-attempts','attemptCount':0})

    def test_source_binding_refuses_wrong_workflow_dependency_and_source(self):
        g=GOLDENS[0]
        for change in ['workflow','dependency','source','kind','boolean','legacy-request']:
            b=base(g)
            if change=='workflow':b['workflow']['name']='analyze'
            elif change=='dependency':b['orderedSteps'][1]['dependsOn']=[]
            elif change=='source':b['orderedSteps'][1]['params']['sourceStep']=1
            elif change=='kind':b['orderedSteps'][0]['kind']='query'
            elif change=='boolean':b['orderedSteps'][1]['params']['sourceStep']=False
            else:
                b['orderedSteps'][1]['params']=copy.deepcopy(g['invocationRecord']['orderedSteps'][1]['params'])
                b['orderedSteps'][1]['params']['request']['schemaMajor']=4
            with self.subTest(change=change),self.assertRaises((ValueError,V.C.ValidationError)):
                W.replay(b,g['ownerScript'],V.C.canonical,V.T,validate)

    def test_actual_query_request_binds_replayed_run_and_project(self):
        g=next(g for g in GOLDENS if g['scenario']=='signal-before-required-render')
        record,_,_=W.replay(base(g),g['ownerScript'],V.C.canonical,V.T,validate)
        request=F.resolved_request(record)
        V.validate(V.query_schema['$id']+'#/$defs/GraphQueryRequestV1',request)
        self.assertEqual(request['view'],{'runId':record['stepResults'][0]['result']['runId']})
        self.assertEqual(request['projectId'],record['projectId'])
        self.assertNotEqual(request['view'],g['invocationRecord']['orderedSteps'][1]['params']['request']['view'])

    def test_full_envelope_retains_completed_query_and_executes_static_parity(self):
        g=next(g for g in GOLDENS if g['scenario']=='signal-before-required-render')
        record,_,availability=W.replay(base(g),g['ownerScript'],V.C.canonical,V.T,validate)
        page=copy.deepcopy(fixture['bases']['fit-sealed']['envelope']['advisoryReport'])
        # Fresh synthetic response envelope for the freshly resolved query4.
        # Candidate rows remain existing synthetic owner test inputs.
        page['request']=F.resolved_request(record)
        admit=lambda r,pid,rid:J.admit_page(r,pid,rid,V.C,M,V.validate)
        handle=F.capture_completed(record,page,admit,V.C.equal_typed)
        envelope=J.interrupted(record,g['selectionContext'],handle,V.C,M,F,availability,V.validate)
        self.assertEqual(envelope['advisoryReport'],page)
        self.assertEqual(envelope['run'],g['envelope']['run'])
        pins=json.loads(V.read_unit('fit-interruption','input-pins.json'))['files']
        pin=next(r for r in pins if r['role']=='inventory')
        raw=Path(pin['path']).read_bytes()
        import hashlib
        self.assertEqual(hashlib.sha256(raw).hexdigest(),pin['sha256'])
        command=next(r for r in json.loads(raw)['commands'] if r['name']=='fit')
        text=M.static_parity_text(envelope,command,M.document_disclosures({}))
        self.assertIn('candidates-availability: "sealed-run-first-page"\n',text)
        self.assertIn('termination-class: "interrupted"\n',text)
        self.assertIn('envelope: '+M.canonical(envelope).decode()+'\n',text)
        with self.assertRaises(F.RequiredProjectionFailure):
            J.interrupted(record,g['selectionContext'],None,V.C,M,F,availability,V.validate)
        for change in ['summary','parity','run','selection','unstarted-selection','duplicate-selection']:
            bad=copy.deepcopy(handle);sel=copy.deepcopy(g['selectionContext']);rec=copy.deepcopy(record)
            if change=='summary':rec['stepResults'][1]['result']['items']=0
            elif change=='parity':bad['report']['parity']['candidatesTotalItems']=100
            elif change=='run':bad['report']['request']['view']['runId']='run3:'+'0'*64
            elif change=='selection':sel['requestId']='req1_'+'0'*32
            elif change=='unstarted-selection':sel['perStep'][0]['stepId']=2
            else:sel['perStep'].append(copy.deepcopy(sel['perStep'][0]))
            with self.subTest(change=change),self.assertRaises((ValueError,V.C.ValidationError)):
                J.interrupted(rec,sel,bad,V.C,M,F,availability,V.validate)

    def test_real_noncompleted_query_replays_get_explicit_unavailable_parity(self):
        g=next(g for g in GOLDENS if g['scenario']=='signal-before-required-render')
        for event in ['cancel-before-query','operational-fault','rejected']:
            script=copy.deepcopy(g['ownerScript'])
            if event=='cancel-before-query':script['cancelAt']['stepId']=1
            elif event=='operational-fault':script['1']=[{'event':event,'faultCause':'host-io'}]
            else:script['1']=[{'event':event,'errorCode':'REQUEST.PRECONDITION_FAILED','detail':'CONFIG.INVALID'}]
            with self.subTest(event=event):
                record,code,availability=W.replay(base(g),script,V.C.canonical,V.T,validate)
                self.assertEqual(code,130)
                envelope=J.interrupted(record,g['selectionContext'],None,V.C,M,F,availability,V.validate)
                report=envelope['advisoryReport']
                self.assertEqual(report['state'],'unavailable-query-result')
                self.assertEqual(report['queryOutcome'],record['stepResults'][1]['outcome'])
                self.assertIsNone(report['parity']['candidates'])
                self.assertIsNone(report['parity']['candidatesTotalItems'])
                self.assertEqual(envelope['run'],record['stepResults'][0]['result'])
                project_ledger(record,g)

if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(WorkflowTests))
    out={'standing':'Root invocation5 reference replay and finalized ledger shape; no live host or source custody qualification',
         'groups':result.testsRun,'fitGoldens':len(GOLDENS),'passed':result.wasSuccessful()}
    (HERE/'workflow5-result.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2));raise SystemExit(not result.wasSuccessful())
