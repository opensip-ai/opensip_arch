import copy
import hashlib
import json
from pathlib import Path
import types
import unittest

from jsonschema import Draft202012Validator, validators

HERE = Path(__file__).resolve().parent
t = types.ModuleType('timing_reference')
exec(compile((HERE / 'timing.py').read_bytes(), str(HERE / 'timing.py'), 'exec'), t.__dict__)
V = validators.extend(Draft202012Validator, type_checker=Draft202012Validator.TYPE_CHECKER.redefine('integer', lambda _, value: type(value) is int))


class TimingTests(unittest.TestCase):
    def test_exact_owner_delta_and_pins(self):
        pins = json.loads((HERE / 'input-pins.json').read_bytes())
        for pin in pins['files']:
            raw = Path(pin['path']).read_bytes()
            self.assertEqual(len(raw), pin['bytes'])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), pin['sha256'])
        old = json.loads(Path(pins['files'][0]['path']).read_bytes())
        new = json.loads((HERE / 'invocation-record.v4.schema.json').read_bytes())
        V.check_schema(new)
        for key in ('$id', 'title', 'description'):
            new[key] = old[key]
        new['properties']['schemaMajor']['const'] = 3
        self.assertEqual(new['$defs']['Attempt']['required'].pop(), 'observedDuration')
        self.assertEqual(new['$defs']['Attempt']['properties'].pop('observedDuration'), {'$ref': '#/$defs/AttemptDurationV1'})
        del new['$defs']['AttemptDurationV1']
        self.assertEqual(new, old)

    def test_closed_duration_shape_and_exact_numbers(self):
        schema = json.loads((HERE / 'invocation-record.v4.schema.json').read_bytes())['$defs']['AttemptDurationV1']
        validator = V(schema)
        valid = [t.observe_terminal('completed', 0, 1), t.observe_terminal('failed', None, None), t.observe_terminal('abandoned', None, None), {'state': 'measured', 'milliseconds': t.U64_MAX}]
        for value in valid:
            self.assertTrue(validator.is_valid(value), value)
        invalid = [{}, {'state': 'measured'}, {'state': 'measured', 'milliseconds': True}, {'state': 'measured', 'milliseconds': 1.0}, {'state': 'measured', 'milliseconds': -1}, {'state': 'measured', 'milliseconds': t.U64_MAX+1}, {'state': 'measured', 'milliseconds': 2, 'reason': 'clock-unavailable'}, {'state': 'unavailable', 'reason': 'not-retained'}, {'state': 'unavailable', 'reason': 'unknown'}, {'state': 'unavailable', 'reason': 'clock-unavailable', 'milliseconds': 0}]
        for value in invalid:
            self.assertFalse(validator.is_valid(value), value)

    def test_zero_fractional_and_exact_boundary(self):
        for delta, expected in [(0, 0), (999999, 0), (1000000, 1), (1999999, 1), (t.U64_MAX*1000000+999999, t.U64_MAX)]:
            self.assertEqual(t.observe_terminal('completed', -42, -42+delta), {'state': 'measured', 'milliseconds': expected})
        self.assertEqual(t.observe_terminal('completed', 0, (t.U64_MAX+1)*1000000), t.unavailable('duration-overflow'))

    def test_clock_failure_has_no_zero_fallback(self):
        for start, end in [(None, 10), (10, None), (None, None)]:
            self.assertEqual(t.observe_terminal('failed', start, end), t.unavailable('clock-unavailable'))
        self.assertEqual(t.observe_terminal('cancelled', 12, 11), t.unavailable('clock-regressed'))
        for start, end in [(True, 3), (0, 4.0), ('0', 4)]:
            with self.assertRaises(t.TimingRefusal):
                t.observe_terminal('completed', start, end)

    def test_recovery_and_outcome_join(self):
        self.assertEqual(t.observe_terminal('abandoned', 1, 3000000), t.unavailable('supervisor-lost'))
        for outcome in ('completed', 'rejected', 'failed', 'cancelled'):
            t.admit_duration(outcome, t.observe_terminal(outcome, 0, 1000000))
            with self.assertRaises(t.TimingRefusal):
                t.admit_duration(outcome, t.unavailable('supervisor-lost'))
        with self.assertRaises(t.TimingRefusal):
            t.admit_duration('abandoned', {'state': 'measured', 'milliseconds': 3})
        with self.assertRaises(t.TimingRefusal):
            t.admit_duration('abandoned', t.unavailable('clock-unavailable'))
        with self.assertRaises(t.TimingRefusal):
            t.observe_terminal('skipped', 0, 0)

    def test_historical_major_is_visible_and_not_rewritten(self):
        old = {'executionId': 'exec1_'+'1'*32, 'outcome': 'completed'}
        before = copy.deepcopy(old)
        projected = t.project_attempt(3, old)
        self.assertEqual(old, before)
        self.assertEqual(projected, {'executionId': old['executionId'], 'sourceSchemaMajor': 3, 'duration': t.unavailable('not-retained')})
        for major in (True, 2, 5, '3'):
            with self.assertRaises(t.TimingRefusal):
                t.project_attempt(major, old)
        with self.assertRaises(t.TimingRefusal):
            t.project_attempt(4, old)
        with self.assertRaises(t.TimingRefusal):
            t.project_attempt(3, dict(old, observedDuration={'state': 'measured', 'milliseconds': 9}))

    def test_current_projection_copies_exact_recorded_value(self):
        current = {'executionId': 'exec1_'+'2'*32, 'outcome': 'cancelled', 'observedDuration': {'state': 'measured', 'milliseconds': 18446744073709550000}}
        before = copy.deepcopy(current)
        p = t.project_attempt(4, current)
        self.assertEqual(p['duration'], current['observedDuration'])
        self.assertEqual(p['executionId'], current['executionId'])
        self.assertEqual(p['sourceSchemaMajor'], 4)
        p['duration']['milliseconds'] = 0
        self.assertEqual(current, before)
        with self.assertRaises(t.TimingRefusal):
            t.project_attempt(4, dict(current, observedDuration=t.unavailable('not-retained')))

    def test_retry_sum_and_missing_are_distinct(self):
        def p(n):
            return {'duration': {'state': 'measured', 'milliseconds': n}}
        self.assertEqual(t.summarize_attempts([]), {'state': 'no-attempts', 'attemptCount': 0})
        self.assertEqual(t.summarize_attempts([p(0)]), {'state': 'measured', 'attemptCount': 1, 'milliseconds': 0})
        self.assertEqual(t.summarize_attempts([p(3), p(8), p(2)]), {'state': 'measured', 'attemptCount': 3, 'milliseconds': 13})
        unknown = {'duration': t.unavailable('not-retained')}
        self.assertEqual(t.summarize_attempts([p(3), unknown]), {'state': 'unavailable', 'attemptCount': 2, 'unavailableAttemptCount': 1, 'reason': 'incomplete-observations'})
        self.assertEqual(t.summarize_attempts([p(t.U64_MAX), p(1)]), {'state': 'unavailable', 'attemptCount': 2, 'unavailableAttemptCount': 0, 'reason': 'duration-overflow'})
        with self.assertRaises(t.TimingRefusal):
            t.summarize_attempts([p(0)]*4)


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TimingTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(json.dumps({'passed': result.wasSuccessful(), 'groups': result.testsRun, 'selected': False, 'productQualification': False,
                      'limits': 'Pure owner/reference checks only. No actual clocks, journal/crash recovery, authority custody, report integration, identity execution or D9 execution qualified.'}, indent=2))
    raise SystemExit(0 if result.wasSuccessful() else 1)
