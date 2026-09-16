import ast
import copy
import hashlib
import json
from pathlib import Path
import types
import unittest
from contextlib import contextmanager
from jsonschema import Draft202012Validator, validators, ValidationError
from referencing import Registry,Resource
from referencing.jsonschema import DRAFT202012

HERE = Path(__file__).resolve().parent
module = types.ModuleType('history_reference');module.__file__=str(HERE/'history.py')
exec(compile((HERE/'history.py').read_bytes(), str(HERE/'history.py'), 'exec'), module.__dict__)
pins = json.loads((HERE/'input-pins.json').read_bytes())['files']
for pin in pins:
    raw = Path(pin['path']).read_bytes()
    assert len(raw) == pin['bytes'] and hashlib.sha256(raw).hexdigest() == pin['sha256']
paths = {r['role']: Path(r['path']) for r in pins}
schema = json.loads((HERE/'explicit-history.schema.json').read_bytes())
validator = validators.extend(Draft202012Validator, type_checker=Draft202012Validator.TYPE_CHECKER.redefine('integer', lambda _, v: type(v) is int))


def rid(n):
    return 'run3:'+format(n, '064x')


# Synthetic receipt/query shapes for isolated selection tests. Actual close_run
# admission runs separately in check_query.py; these dictionaries prove no custody.
PID='prj1-'+'2'*64
query=json.loads((HERE/'graph-query.history-candidate.schema.json').read_bytes())
panel=json.loads((HERE/'explicit-history-panel.schema.json').read_bytes())
report=json.loads(paths['report-schema'].read_bytes())
resources=[query,panel,report,schema,*[json.loads(paths[k].read_bytes()) for k in ['common','identity-schema','invocation']]]
registry=Registry().with_resources((d['$id'],Resource(contents={k:v for k,v in d.items() if k!='$schema'},specification=DRAFT202012)) for d in resources)
def validate_query(v):validator({'$ref':query['$id']+'#/$defs/GraphQueryResponseV1'},registry=registry).validate(v)
def validate_history(v):validator({'$ref':panel['$id']+'#/$defs/RetainedHistorySlotV1'},registry=registry).validate(v)
def typed_value(value):
    if type(value) is not dict or value.get('state') not in ['present','unavailable']:return value
    value=copy.deepcopy(value);run_id=value.get('runId')
    if value['state']=='unavailable':
        if value.get('availability') not in ['expired','purged','corrupt','unavailable']:return value
        response=module.QUERY.unavailable(PID,run_id,value['availability'])
    else:
        result={'kind':'analysis','authority':'authoritative','runId':run_id,'planId':'plan2:'+'3'*64,'verdict':'pass','requiredCoverage':'satisfied','durability':'committed','deficiency':'none','secondaryDeficiencies':[]}
        sealed={'schemaVersion':3,'projectId':PID,'snapshotId':'snapshot2:'+'4'*64,'planId':result['planId'],'evidenceId':'evidence3:'+'5'*64,'evaluationSealId':'seal3:'+'6'*64,'capabilityManifestId':'7'*64}
        response={'schemaFamily':'opensip.product.query','schemaMajor':3,'operation':'run.show','context':{'projectId':PID,'resolvedView':{'runId':run_id},'coverage':'complete','availability':'retained','truncated':False,'totalItems':1,'advisory':False},'items':[{'projectId':PID,'runId':run_id,'sealedRun':sealed,'result':result}]}
        value.setdefault('run',copy.deepcopy(result));value.setdefault('commitSequence',None);value.setdefault('findings',[]);value.setdefault('findingsProjection',{'total':len(value['findings']),'omitted':0,'omissionCause':'none'})
    return {'query':response,'history':value}
def resolve(selection,lookup):
    return module.resolve_slots(selection,PID,lambda run_id:typed_value(lookup(run_id)),validate_query,validate_history)

class HistoryTests(unittest.TestCase):
    def test_owner_limit_types_and_eight_command_scope(self):
        common = json.loads(paths['common'].read_bytes())
        report = json.loads(paths['report-schema'].read_bytes())
        inventory = json.loads(paths['command-inventory'].read_bytes())
        limits = [v['properties']['maxHistoryRuns'] for v in report['$defs'].values() if 'maxHistoryRuns' in v.get('properties', {})]
        self.assertEqual(limits, [{'const': 4}])
        self.assertEqual(module.MAX_RUNS, 4)
        self.assertEqual(schema['properties']['requestedRunIds']['items'], common['$defs']['RunId'])
        self.assertEqual(len([c for c in inventory['commands'] if 'html' in c['formats']]), 8)
        validator.check_schema(schema)

    def test_exact_order_and_four_slots(self):
        ids = [rid(70), rid(1), rid(40), rid(8)]
        request = module.admit_request(ids, 'html')
        validator(schema['$defs']['Request']).validate(request)
        selected = module.plan_selection(request, rid(20))
        validator(schema).validate(selected)
        self.assertEqual(selected['requestedRunIds'], ids)
        self.assertEqual([s['runId'] for s in selected['slots']], ids)
        self.assertNotIn('baselineSourceRunId', selected)

    def test_invalid_requests_refuse_before_lookup_without_token_disclosure(self):
        for ids in ([], [rid(1)]*2, [rid(i) for i in range(5)], ['latest'], ['secret-invalid-token'],
                    [rid(1)+','+rid(2)], [rid(1)+'\n'], [rid(1).upper()], [True], (rid(1),)):
            with self.assertRaises(module.HistoryRefusal) as error:
                module.admit_request(ids, 'html')
            self.assertEqual(str(error.exception), 'EVALUATION.SELECTION_LIMIT' if type(ids) is list and len(ids)>4 else 'REPORT.HISTORY_SELECTION_INVALID')
        for fmt in ('human', 'json', 'sarif', 'agent', None, True):
            with self.assertRaises(module.HistoryRefusal) as error:
                module.admit_request([rid(1)], fmt)
            self.assertEqual(error.exception.route, {'class':'request-rejected','code':'REQUEST.UNKNOWN_OPTION','exitCode':2,'detail':'OUTPUT.FORMAT_NOT_APPLICABLE'})

    def test_current_run_is_explicit_and_uses_no_lookup(self):
        selection = module.plan_selection(module.admit_request([rid(1), rid(2)], 'html'), rid(1))
        calls = []
        def lookup(run_id):
            calls.append(run_id)
            return {'state': 'unavailable', 'runId': run_id, 'availability': 'purged'}
        result = resolve(selection, lookup)
        self.assertEqual(result[0], {'state': 'current-run', 'runId': rid(1)})
        self.assertEqual(calls, [rid(2)])

    def test_missing_history_preserves_every_requested_slot_without_fallback(self):
        ids = [rid(i) for i in range(4)]
        states = dict(zip(ids, ('expired', 'purged', 'corrupt', 'unavailable')))
        calls = []
        def lookup(run_id):
            calls.append(run_id)
            return {'state': 'unavailable', 'runId': run_id, 'availability': states[run_id]}
        result = resolve(module.plan_selection(module.admit_request(ids, 'html'), None), lookup)
        self.assertEqual(calls, ids)
        self.assertEqual([row['runId'] for row in result], ids)
        self.assertEqual([row['availability'] for row in result], list(states.values()))

    def test_wrong_lookup_result_is_internal_source_failure(self):
        selection = module.plan_selection(module.admit_request([rid(1)], 'html'), None)
        for value in (None, {}, {'state': 'present', 'runId': rid(2)},
                      {'state': 'current-run', 'runId': rid(1)},
                      {'state': 'unavailable', 'runId': rid(1), 'availability': 'latest'}):
            with self.assertRaises(module.HistorySourceRefusal):
                resolve(selection, lambda _: value)

    def test_selection_mutations_do_not_redirect_lookup(self):
        good = module.plan_selection(module.admit_request([rid(1), rid(2)], 'html'), None)
        edits = []
        bad = copy.deepcopy(good); bad['slots'].reverse(); edits.append(bad)
        bad = copy.deepcopy(good); bad['slots'][0]['source'] = 'current-run'; edits.append(bad)
        bad = copy.deepcopy(good); bad['requestedRunIds'].pop(); edits.append(bad)
        bad = copy.deepcopy(good); bad['fallback'] = 'latest'; edits.append(bad)
        edits.extend([None, {}])
        for selected in edits:
            calls = []
            with self.assertRaises(module.HistorySourceRefusal):
                resolve(selected, lambda value: calls.append(value))
            self.assertEqual(calls, [])

    def test_output_copy_does_not_mutate_admitted_sources(self):
        source = {'state': 'present', 'runId': rid(1), 'findings': []}
        ids = [rid(1)]
        request = module.admit_request(ids, 'html')
        ids.clear()
        selection = module.plan_selection(request, None)
        result = resolve(selection, lambda _: source)
        result[0]['findings'].append('new')
        self.assertEqual(source['findings'], [])
        self.assertEqual(request['runIds'], [rid(1)])

    def test_current_run_malformed_is_internal(self):
        for value in ['latest',True,{},'run3:bad']:
            with self.assertRaises(ValueError) as error:
                module.plan_selection(module.admit_request([rid(1)],'html'),value)
            self.assertIs(type(error.exception),module.HistorySourceRefusal)

    def test_exact_route_precedence(self):
        fixtures = [
            (['private-invalid'], 'json', 'REQUEST.UNKNOWN_OPTION', 'OUTPUT.FORMAT_NOT_APPLICABLE'),
            ([rid(i) for i in range(5)], 'html', 'REQUEST.UNSATISFIABLE', 'EVALUATION.SELECTION_LIMIT'),
            (['private-invalid']+[rid(i) for i in range(4)], 'html', 'REQUEST.UNSATISFIABLE', 'REPORT.HISTORY_SELECTION_INVALID'),
            ([rid(1),rid(1)], 'html', 'REQUEST.UNSATISFIABLE', 'REPORT.HISTORY_SELECTION_INVALID')]
        for ids,fmt,code,detail in fixtures:
            with self.assertRaises(module.HistoryRefusal) as error: module.admit_request(ids,fmt)
            self.assertEqual(error.exception.route,{'class':'request-rejected','code':code,'exitCode':2,'detail':detail})
            self.assertNotIn('private-invalid',str(error.exception))

    def test_typed_query_project_and_receipt_joins(self):
        selection=module.plan_selection(module.admit_request([rid(1)],'html'),None)
        good=typed_value({'state':'present','runId':rid(1),'findings':[]})
        mutations=[]
        bad=copy.deepcopy(good);bad['query']['items'][0]['projectId']='prj1-'+'f'*64;mutations.append(bad)
        bad=copy.deepcopy(good);bad['history']['run']['verdict']='fail';mutations.append(bad)
        bad=copy.deepcopy(good);bad['history']['findingsProjection']['total']=1;mutations.append(bad)
        for value in mutations:
            with self.assertRaises(module.HistorySourceRefusal):
                module.resolve_slots(selection,PID,lambda _:value,validate_query,validate_history)

    def test_one_read_snapshot_includes_committed_pivot_and_is_released(self):
        # Synthetic lease acquired after the caller commits primary + pivot.
        live={rid(1):{'state':'unavailable','runId':rid(1),'availability':'expired'},rid(3):{'state':'present','runId':rid(3),'findings':[]}}
        events=['primary-committed','pivot-committed']
        @contextmanager
        def acquire():
            events.append('acquire');snap=copy.deepcopy(live)
            try:yield snap
            finally:events.append('release')
        def lookup(snap,run_id):
            events.append(run_id);live[rid(3)]={'state':'unavailable','runId':rid(3),'availability':'purged'}
            return typed_value(snap[run_id])
        request=module.admit_request([rid(1),rid(2),rid(3)],'html')
        selection,rows=module.resolve_in_snapshot(request,rid(2),PID,acquire,lookup,validate_query,validate_history)
        self.assertEqual(events,['primary-committed','pivot-committed','acquire',rid(1),rid(3),'release'])
        self.assertEqual([r['state'] for r in rows],['unavailable','current-run','present'])
        events.clear()
        with self.assertRaises(module.HistorySourceRefusal):
            module.resolve_in_snapshot(request,rid(2),PID,acquire,lambda *_:{},validate_query,validate_history)
        self.assertEqual(events,['acquire','release'])

    def test_explicit_panel_union_current_identity_and_provenance(self):
        selection=module.plan_selection(module.admit_request([rid(1),rid(2)],'html'),rid(1))
        rows=resolve(selection,lambda run_id:{'state':'unavailable','runId':run_id,'availability':'purged'})
        value={'selection':selection,'runs':rows,'provenance':copy.deepcopy(panel['properties']['provenance']['const'])}
        shape=lambda value:validator(panel,registry=registry).validate(value)
        module.validate_panel(value,rid(1),shape)
        self.assertNotIn('not-current-run',value['provenance']['verifiedInDocument'])
        self.assertIn('selected-run-and-project-equal-typed-query-item',value['provenance']['hostAsserted'])
        for edit in [lambda x:x['runs'].reverse(),lambda x:x['selection'].update(currentRunId=rid(2))]:
            bad=copy.deepcopy(value);edit(bad)
            with self.assertRaises(module.HistorySourceRefusal):module.validate_panel(bad,rid(1),shape)
        bad=copy.deepcopy(value);bad['runs'][0]={'state':'unavailable','runId':rid(1),'availability':'purged'}
        with self.assertRaises(module.HistorySourceRefusal):module.validate_panel(bad,rid(1),shape)

    def test_eight_exact_flag_records_and_closed_availability_details(self):
        patch=json.loads((HERE/'history-command-flags.json').read_bytes())
        inv=json.loads(paths['command-inventory'].read_bytes())
        self.assertEqual([r['command'] for r in patch['rows']],[r['name'] for r in inv['commands'] if 'html' in r['formats']])
        flags=[r['appendFlag'] for r in patch['rows']];self.assertTrue(all(f==flags[0] for f in flags))
        self.assertEqual(set(flags[0]),{'flag','owner','class','join'})
        self.assertEqual(flags[0]['flag'],'--history-run')
        self.assertIn('Repeatable 1..4',flags[0]['join']);self.assertIn('Requires --format html',flags[0]['join'])
        for availability,code in [('expired','evidence.expired'),('purged','evidence.purged'),('corrupt','evidence.corrupt'),('unavailable','QUERY.VIEW_UNKNOWN')]:
            row={'state':'unavailable','runId':rid(1),'availability':availability,'detail':{'code':code,'remedy':'Read retained evidence'}}
            validate_history(row);row['detail']['code']='CONFIG.INVALID'
            with self.assertRaises(ValidationError):validate_history(row)

    def test_owned_subject_run_mapping_is_preserved(self):
        parent=ast.parse(paths['report-admission'].read_bytes())
        selected=next(n for n in parent.body if isinstance(n,ast.FunctionDef) and n.name=='subject_run')
        generated=next(n for n in ast.parse((HERE/'subject_run.py').read_bytes()).body if isinstance(n,ast.FunctionDef))
        self.assertEqual(ast.dump(selected,include_attributes=False),ast.dump(generated,include_attributes=False))
        for command in ['default','analyze','audit','fit']:
            self.assertEqual(module.current_run_from_envelope({'kind':'run','run':{'authority':'authoritative','runId':rid(1)}},command),rid(1))
            self.assertIsNone(module.current_run_from_envelope({'kind':'run','run':{'authority':'ephemeral'}},command))
        for command,record in [('candidates',{'context':{'resolvedView':{'runId':rid(1)}}}),('inspect',{'inspection':{'runId':rid(1)}}),('review-brief',{'brief':{'runId':rid(1)}})]:
            self.assertEqual(module.current_run_from_envelope({'kind':'query','queryRecord':record},command),rid(1))
        self.assertIsNone(module.current_run_from_envelope({'kind':'query','queryRecord':{'preview':{}}},'repair-preview'))
        for kind in ['failure','invocation']:self.assertIsNone(module.current_run_from_envelope({'kind':kind},'audit'))

    def test_query_successor_changes_only_the_run_show_response(self):
        parent=json.loads(paths['query-schema'].read_bytes())
        self.assertEqual(set(query['$defs'])-set(parent['$defs']),{'RunShowItemV1','RunShowResponseV1'})
        for key,value in parent['$defs'].items():
            if key=='GraphQueryResponseV1':
                changed=copy.deepcopy(query['$defs'][key]);changed['allOf'].pop();self.assertEqual(changed,value)
            else:self.assertEqual(query['$defs'][key],value,key)
        self.assertEqual(query['$defs']['Operation'],parent['$defs']['Operation'])

    def test_one_new_history_detail_is_registered_without_replacing_routes(self):
        parent=json.loads(paths['common'].read_bytes());changed=json.loads((HERE/'common.history-candidate.schema.json').read_bytes())
        code='REPORT.HISTORY_SELECTION_INVALID'
        expected=copy.deepcopy(parent);expected['$defs']['DomainDetailCode']['enum'].append(code);self.assertEqual(changed,expected)
        validator(changed['$defs']['DomainDetailCode']).validate(code)
        with self.assertRaises(ValidationError):validator(parent['$defs']['DomainDetailCode']).validate(code)
        old=json.loads(paths['detail-registry'].read_bytes());new=json.loads((HERE/'public-detail-registry.history-candidate.json').read_bytes())
        old_by={r['code']:r for r in old['records']};new_by={r['code']:r for r in new['records']}
        self.assertEqual(set(new_by)-set(old_by),{code})
        self.assertTrue(all(new_by[k]==v for k,v in old_by.items()))
        goldens=json.loads((HERE/'history-route-goldens.json').read_bytes())['cases']
        self.assertEqual({r['detail'] for r in goldens},{code,'OUTPUT.FORMAT_NOT_APPLICABLE','EVALUATION.SELECTION_LIMIT'})

    def test_automatic_owner_remains_separate_and_unchanged(self):
        tree = ast.parse(paths['report-model'].read_bytes())
        nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'history_selection']
        self.assertEqual(len(nodes), 1)
        owner = {}
        exec(compile(ast.Module(body=nodes, type_ignores=[]), 'pinned-report-history-owner', 'exec'), owner)
        receipts = [{'runId': rid(i), 'commitSequence': i} for i in range(1, 11)]
        automatic = owner['history_selection'](10, receipts, rid(1), 'baseline2:'+'a'*64, 4)
        self.assertEqual(automatic['requestedRunIds'], [rid(1), rid(9), rid(8), rid(7)])
        explicit = module.plan_selection(module.admit_request([rid(2), rid(3)], 'html'), rid(10))
        self.assertEqual(explicit['requestedRunIds'], [rid(2), rid(3)])
        self.assertNotIn(rid(1), explicit['requestedRunIds'])


if __name__ == '__main__':
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(HistoryTests))
    print(json.dumps({'passed': result.wasSuccessful(), 'groups': result.testsRun, 'externalPins': len(pins),
                      'selected': False, 'productQualification': False,
                      'limits': 'Explicit selection owner/reference only. Store callbacks are synthetic admitted-source stand-ins; actual route/grammar/report schema integration, identity/custody and browser checks remain required.'}, indent=2))
    raise SystemExit(0 if result.wasSuccessful() else 1)
