"""Narrow binding/projection tests; does not claim full invocation/page admission."""
from pathlib import Path
import ast
import copy
import hashlib
import json
import sys
import types
import unittest
from jsonschema import Draft202012Validator, ValidationError

HERE=Path(__file__).resolve().parent
assert sys.flags.isolated and sys.dont_write_bytecode
sources={}
pins=json.loads((HERE/'input-pins.json').read_text())['files']
for row in pins:
    raw=Path(row['path']).read_bytes()
    assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
    sources[row['role']]=(row['path'],raw)


def source_module(name,path,raw):
    m=types.ModuleType(name);m.__file__=str(path)
    exec(compile(raw,str(path),'exec'),m.__dict__)
    return m


F=source_module('fit_proposal',HERE/'fit_output.py',(HERE/'fit_output.py').read_bytes())
M=source_module('report08',*sources['report-model'])
C=source_module('canonical',*sources['canonical'])
query_tree=ast.parse(sources['query-projection'][1])
names={'QuerySurfaceProjectionError','_equal','_join','_summary','command_surface_summary'}
query_nodes=[n for n in query_tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in names]
assert {n.name for n in query_nodes}==names
Q={'canonical':C}
exec(compile(ast.Module(body=query_nodes,type_ignores=[]),sources['query-projection'][0],'exec'),Q)
fixture=json.loads(sources['report-fixtures'][1])
golden=next(r for r in fixture['interruptionGoldens']['scenarios'] if r['id']=='fit/primary/signal-before-required-render')
COMMAND=next(r for r in json.loads(sources['inventory'][1])['commands'] if r['name']=='fit')
PAGE=fixture['bases']['fit-sealed']['envelope']['advisoryReport']
PARAM_SCHEMA=json.loads((HERE/'fit-query-from-analysis.schema.json').read_text())
ABSENT_SCHEMA=json.loads((HERE/'fit-query-unavailable.schema.json').read_text())


def record_and_envelope():
    record=copy.deepcopy(golden['invocationRecord'])
    record['orderedSteps'][1]['params']={'kind':'query','operation':'candidate.list','sourceStep':0}
    return record,copy.deepcopy(golden['envelope'])


def admit_page(report,project_id,run_id):
    # The reference exercises the actual extracted query summary owner and
    # existing fit-specific joins. Full schema/native admission remains an
    # upstream precondition, not a claim made by this helper.
    if set(report)!={'state','request','candidateList','parity'}:
        raise F.BindingRefusal('page-fields')
    page=report['candidateList'];ctx=page['context']
    if ctx['resolvedView']!={'runId':run_id}:
        raise F.BindingRefusal('page-run')
    summary=Q['command_surface_summary']('candidate-list',page,{'projectId':project_id})
    listed=len(page['candidates'])
    if listed>100 or ctx['truncated']!=(ctx['totalItems']>listed):
        raise F.BindingRefusal('page-size')
    if ctx['truncated']:
        if listed!=100 or ctx.get('nextCursor')!=M.fit_cursor(project_id,run_id,100):
            raise F.BindingRefusal('page-cursor')
    elif 'nextCursor' in ctx:
        raise F.BindingRefusal('unexpected-cursor')
    parity={'runId':run_id,'candidates':page['candidates'],'evidenceLevels':page['evidenceLevels'],
            'candidatesTruncated':ctx['truncated'],'candidatesTotalItems':ctx['totalItems'],
            'candidatesNextCursor':ctx.get('nextCursor'),'candidatesAvailability':'sealed-run-first-page'}
    if not C.equal_typed(parity,report['parity']):
        raise F.BindingRefusal('page-parity')
    return summary


def capture(record,page=PAGE):
    return F.capture_completed(record,page,admit_page,C.equal_typed)


def project(record,env,handle):
    return F.project_interrupted(record,env,handle,admit_page,C.equal_typed)


class FitTests(unittest.TestCase):
    def test_original_frozen_counterexample_and_placeholder_request(self):
        with self.assertRaisesRegex(KeyError,'advisoryReport'):
            M.static_parity_text(golden['envelope'],COMMAND,M.document_disclosures({}))
        request=golden['invocationRecord']['orderedSteps'][1]['params']['request']
        self.assertNotEqual(request['view']['runId'],golden['envelope']['run']['runId'])
        self.assertNotEqual(request['projectId'],golden['envelope']['projectId'])

    def test_completed_page_survives_cancellation_and_actual_static_render(self):
        record,env=record_and_envelope();before=copy.deepcopy((record,env,PAGE))
        out=project(record,env,capture(record))
        self.assertEqual(out['advisoryReport'],PAGE)
        self.assertEqual(out['run'],env['run']);self.assertEqual(out['termination'],env['termination'])
        text=M.static_parity_text(out,COMMAND,M.document_disclosures({}))
        self.assertIn('candidates-availability: "sealed-run-first-page"\n',text)
        self.assertIn('termination-class: "interrupted"\n',text)
        self.assertEqual(before,(record,env,PAGE))

    def test_source_step_binds_actual_run_and_project_without_plan_mutation(self):
        record,env=record_and_envelope();before=copy.deepcopy(record)
        request=F.resolved_request(record)
        self.assertEqual(request,PAGE['request'])
        self.assertEqual(record,before)
        self.assertNotIn('request',record['orderedSteps'][1]['params'])

    def test_closed_parameter_schema_and_relation_checks(self):
        record,_=record_and_envelope();valid=record['orderedSteps'][1]['params']
        Draft202012Validator(PARAM_SCHEMA).validate(valid)
        for field,value in [('sourceStep',True),('sourceStep',-1),('sourceStep',64),('operation','graph.path'),('request',{})]:
            bad=dict(valid);bad[field]=value
            with self.assertRaises(ValidationError):Draft202012Validator(PARAM_SCHEMA).validate(bad)
        for source in [False,0.0,1,2,63,-1]:
            bad=copy.deepcopy(record);bad['orderedSteps'][1]['params']['sourceStep']=source
            with self.assertRaises(F.BindingRefusal):F.resolved_request(bad)
        for change in ['dependency','gate','kind','extra-query','duplicate-result']:
            bad=copy.deepcopy(record)
            if change=='dependency':bad['orderedSteps'][1]['dependsOn']=[]
            elif change=='gate':bad['orderedSteps'][1]['dependencyGate']='terminal'
            elif change=='kind':bad['orderedSteps'][0]['kind']='verify'
            elif change=='extra-query':bad['orderedSteps'].append(copy.deepcopy(bad['orderedSteps'][1]))
            else:bad['stepResults'].append(copy.deepcopy(bad['stepResults'][0]))
            with self.assertRaises(F.BindingRefusal):F.resolved_request(bad)

    def test_uncompleted_source_cannot_bind_query(self):
        for outcome in ['failed','rejected','skipped','cancelled']:
            record,_=record_and_envelope();record['stepResults'][0]['outcome']=outcome
            with self.assertRaises(F.BindingRefusal):F.resolved_request(record)

    def test_ephemeral_has_no_public_query_or_authoritative_candidate_parity(self):
        record,_=record_and_envelope()
        record['stepResults'][0]['result']={'kind':'analysis','authority':'ephemeral'}
        record['stepResults'][1]['result']={'kind':'query','items':0,'truncated':False,'completenessMet':False,'advisory':True}
        self.assertIsNone(F.resolved_request(record))
        handle=capture(record,F.ephemeral_report())
        self.assertIsNone(handle['report']['parity']['candidates'])
        with self.assertRaises(F.BindingRefusal):capture(record,PAGE)

    def test_exact_completed_summary_and_request_are_required(self):
        record,_=record_and_envelope()
        for field,value in [('items',0),('truncated',True),('advisory',False),('completenessMet',False)]:
            bad=copy.deepcopy(record);bad['stepResults'][1]['result'][field]=value
            with self.assertRaises(F.BindingRefusal):capture(bad)
        for key,value in [('view',{'runId':'run3:'+'a'*64}),('projectId','prj1-'+'a'*64),('page',{'size':50}),('params',{'includeSuppressed':True})]:
            page=copy.deepcopy(PAGE);page['request'][key]=value
            with self.assertRaises(F.BindingRefusal):capture(record,page)

    def test_private_handle_joins_request_step_and_completed_attempt(self):
        record,env=record_and_envelope();handle=capture(record)
        for field,value in [('requestId','req1_'+'0'*32),('stepId',0),('executionId','exec1_'+'0'*32),('extra',True)]:
            bad=copy.deepcopy(handle);bad[field]=value
            with self.assertRaises(F.BindingRefusal):project(record,env,bad)
        bad=copy.deepcopy(record);bad['stepResults'][1]['attempts']=[]
        with self.assertRaises(F.BindingRefusal):capture(bad)

    def test_missing_completed_response_is_explicit_projection_fault(self):
        record,env=record_and_envelope()
        with self.assertRaisesRegex(F.RequiredProjectionFailure,'not-retained'):project(record,env,None)
        self.assertEqual(record['stepResults'][1]['outcome'],'completed')
        self.assertEqual(env['termination']['class'],'interrupted')

    def test_noncompleted_query_has_total_null_parity_and_actual_outcome(self):
        for outcome in ['cancelled','skipped','failed','rejected']:
            record,env=record_and_envelope();record['stepResults'][1]['outcome']=outcome
            record['stepResults'][1].pop('result')
            out=project(record,env,None);report=out['advisoryReport']
            Draft202012Validator(ABSENT_SCHEMA).validate(report)
            self.assertEqual(report['queryOutcome'],outcome)
            self.assertIsNone(report['parity']['candidates'])
            self.assertIsNone(report['parity']['candidatesTotalItems'])
            self.assertEqual(report['parity']['runId'],out['run']['runId'])
            text=M.static_parity_text(out,COMMAND,M.document_disclosures({}))
            self.assertIn('candidates: null\n',text)
            self.assertIn('candidates-availability: "unavailable-query-result"\n',text)
            with self.assertRaises(F.BindingRefusal):project(record,env,{'report':PAGE})

    def test_absence_is_not_an_empty_successful_page(self):
        record,env=record_and_envelope();record['stepResults'][1]['outcome']='cancelled'
        report=project(record,env,None)['advisoryReport']
        for field,value in [('candidates',[]),('candidatesTotalItems',0),('candidatesTruncated',False)]:
            bad=copy.deepcopy(report);bad['parity'][field]=value
            with self.assertRaises(ValidationError):Draft202012Validator(ABSENT_SCHEMA).validate(bad)
        bad=copy.deepcopy(report);bad['queryOutcome']='completed'
        with self.assertRaises(ValidationError):Draft202012Validator(ABSENT_SCHEMA).validate(bad)

    def test_changed_page_parity_and_other_source_run_are_refused(self):
        record,env=record_and_envelope();page=copy.deepcopy(PAGE);page['parity']['candidates']=[]
        with self.assertRaises(F.BindingRefusal):capture(record,page)
        handle=capture(record);bad=copy.deepcopy(env);bad['run']['runId']='run3:'+'f'*64
        with self.assertRaises(F.BindingRefusal):project(record,bad,handle)
        bad=copy.deepcopy(env);bad['advisoryReport']=F.ephemeral_report()
        with self.assertRaises(F.BindingRefusal):project(record,bad,handle)

    def test_no_run_failure_carriers_and_other_interruption_static_functions(self):
        rows=[]
        for g in fixture['interruptionGoldens']['scenarios']:
            row=next(r for r in json.loads(sources['inventory'][1])['commands'] if r['name']==g['command'])
            env=g['envelope']
            if g['id']==golden['id']:
                record,env=record_and_envelope();env=project(record,env,capture(record))
            elif g['command']=='fit':
                self.assertEqual(project(g['invocationRecord'],env,None),env)
            text=M.static_parity_text(env,row,M.document_disclosures({}))
            self.assertIn('envelope: ',text)
            rows.append({'id':g['id'],'bytes':len(text.encode()),'sha256':hashlib.sha256(text.encode()).hexdigest()})
        self.assertEqual(len(rows),36)
        (HERE/'static-parity-execution.json').write_text(json.dumps({'standing':'Actual reference static parity calls, not browser or all-format execution','rows':rows},indent=2)+'\n')


if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(FitTests))
    out={'standing':'Root proposed binding/custody reference checks; not full parent integration, actual-Claude approval or product qualification',
         'groups':result.testsRun,'passed':result.wasSuccessful(),'pins':len(pins),
         'limits':['Full invocation/page/native schema admission delegated, not reproduced','AST-extracted unchanged candidate summary owner only','Private host handle is a dictionary stand-in','Noncompleted-outcome test records are focused synthetic join inputs, not full re-admitted invocations','36 static parity calls do not qualify all formats or browser rendering','Final schema majors, whole parent closure and live request binding remain pending']}
    (HERE/'result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
    raise SystemExit(0 if result.wasSuccessful() else 1)
