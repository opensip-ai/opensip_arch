import ast
import copy
import hashlib
import json
from pathlib import Path
import types
import unittest
from jsonschema import Draft202012Validator, validators, ValidationError

HERE = Path(__file__).resolve().parent
module = types.ModuleType('history_reference')
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
            self.assertEqual(str(error.exception), 'REPORT.HISTORY_SELECTION_INVALID')
        for fmt in ('human', 'json', 'sarif', 'agent', None, True):
            with self.assertRaises(module.HistoryRefusal):
                module.admit_request([rid(1)], fmt)

    def test_current_run_is_explicit_and_uses_no_lookup(self):
        selection = module.plan_selection(module.admit_request([rid(1), rid(2)], 'html'), rid(1))
        calls = []
        def lookup(run_id):
            calls.append(run_id)
            return {'state': 'unavailable', 'runId': run_id, 'availability': 'purged'}
        result = module.resolve_slots(selection, lookup)
        self.assertEqual(result[0], {'state': 'current-run', 'runId': rid(1)})
        self.assertEqual(calls, [rid(2)])

    def test_missing_history_preserves_every_requested_slot_without_fallback(self):
        ids = [rid(i) for i in range(4)]
        states = dict(zip(ids, ('expired', 'purged', 'corrupt', 'unavailable')))
        calls = []
        def lookup(run_id):
            calls.append(run_id)
            return {'state': 'unavailable', 'runId': run_id, 'availability': states[run_id]}
        result = module.resolve_slots(module.plan_selection(module.admit_request(ids, 'html'), None), lookup)
        self.assertEqual(calls, ids)
        self.assertEqual([row['runId'] for row in result], ids)
        self.assertEqual([row['availability'] for row in result], list(states.values()))

    def test_wrong_lookup_result_is_internal_source_failure(self):
        selection = module.plan_selection(module.admit_request([rid(1)], 'html'), None)
        for value in (None, {}, {'state': 'present', 'runId': rid(2)},
                      {'state': 'current-run', 'runId': rid(1)},
                      {'state': 'unavailable', 'runId': rid(1), 'availability': 'latest'}):
            with self.assertRaises(module.HistorySourceRefusal):
                module.resolve_slots(selection, lambda _: value)

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
                module.resolve_slots(selected, lambda value: calls.append(value))
            self.assertEqual(calls, [])

    def test_output_copy_does_not_mutate_admitted_sources(self):
        source = {'state': 'present', 'runId': rid(1), 'findings': []}
        ids = [rid(1)]
        request = module.admit_request(ids, 'html')
        ids.clear()
        selection = module.plan_selection(request, None)
        result = module.resolve_slots(selection, lambda _: source)
        result[0]['findings'].append('new')
        self.assertEqual(source['findings'], [])
        self.assertEqual(request['runIds'], [rid(1)])

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
