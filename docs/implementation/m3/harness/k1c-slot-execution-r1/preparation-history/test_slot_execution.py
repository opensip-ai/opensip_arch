import os
from pathlib import Path
import signal
import sys
import tempfile
import unittest

from canonical import Refusal
from slot_execution import Invocation, observe_slots


class SlotExecution(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.outputs = []

    def tearDown(self):
        for stream in self.outputs:
            stream.close()
        self.temp.cleanup()

    def invocation(self, ordinal, code, *, timeout=3_000_000_000):
        out = (self.root / f'{ordinal}.stdout').open('wb')
        err = (self.root / f'{ordinal}.stderr').open('wb')
        self.outputs.extend((out, err))
        return Invocation((sys.executable, '-I', '-B', '-c', code),
                          str(self.root), {}, out.fileno(), err.fileno(), timeout)

    def test_ten_actual_roots_and_no_budget_samples(self):
        prepared = []

        def prepare(slot):
            ordinal = len(prepared)
            prepared.append(slot)
            return self.invocation(ordinal, 'import os;print(os.getpid())')

        observations, result = observe_slots('cold', prepare)
        self.assertEqual(prepared, [dict(kind='warmup', index=i) for i in range(3)] +
                         [dict(kind='measured', index=i) for i in range(7)])
        self.assertEqual(len(observations), 10)
        for i, (slot, observed) in enumerate(observations):
            self.assertEqual(slot, prepared[i])
            self.assertEqual(int((self.root / f'{i}.stdout').read_text()), observed.pid)
            self.assertEqual(observed.returncode, 0)
            with self.assertRaises(ChildProcessError):
                os.waitpid(observed.pid, os.WNOHANG)
        self.assertTrue(result['incomplete'])
        self.assertEqual(result['elapsedNanos'], [None] * 7)
        self.assertEqual(result['cgroupMemoryPeakBytes'], [None] * 7)
        self.assertEqual(result['rootReapedElapsedNanos'],
                         [o.root_reaped_elapsed_nanos for _, o in observations[3:]])
        for row in result['slotReasons']:
            self.assertIn('record-missing', row['reasons'])

    def test_warm_priming_is_fresh_and_caller_cache_retained(self):
        prepared = []
        code = "from pathlib import Path;p=Path('cache');n=int(p.read_text()) if p.exists() else 0;print(n);p.write_text(str(n+1))"

        def prepare(slot):
            ordinal = len(prepared)
            prepared.append(slot)
            return self.invocation(ordinal, code)

        observations, result = observe_slots('warm', prepare)
        self.assertEqual(prepared[0], dict(kind='priming', index=0))
        self.assertEqual(len(observations), 11)
        self.assertEqual([int((self.root / f'{i}.stdout').read_text()) for i in range(11)],
                         list(range(11)))
        self.assertEqual((self.root / 'cache').read_text(), '11')
        self.assertEqual(len(result['slotReasons']), 11)
        self.assertEqual(len(result['rootReapedElapsedNanos']), 7)

    def test_caller_cold_reset_occurs_for_warmups_too(self):
        prepared = []
        code = "from pathlib import Path;p=Path('cache');print(int(p.exists()));p.write_text('retained')"

        def prepare(slot):
            ordinal = len(prepared)
            (self.root / 'cache').unlink(missing_ok=True)
            prepared.append(slot)
            return self.invocation(ordinal, code)

        observations, _ = observe_slots('cold', prepare)
        self.assertEqual(len(observations), 10)
        self.assertEqual([int((self.root / f'{i}.stdout').read_text()) for i in range(10)],
                         [0] * 10)

    def test_failed_launch_and_nonzero_slot_retained_without_replacement(self):
        prepared = []

        def prepare(slot):
            ordinal = len(prepared)
            prepared.append(slot)
            launch = self.invocation(ordinal, 'import sys;sys.exit(7)' if ordinal == 5 else '')
            if ordinal == 3:
                return Invocation((str(self.root / 'absent'),), launch.cwd, {},
                                  launch.stdout_fd, launch.stderr_fd, launch.timeout_nanos)
            return launch

        observations, result = observe_slots('cold', prepare)
        self.assertEqual(len(prepared), 10)
        self.assertIsNone(observations[3][1].pid)
        self.assertEqual(observations[5][1].returncode, 7)
        self.assertIsNone(result['rootReapedElapsedNanos'][0])
        self.assertGreater(result['rootReapedElapsedNanos'][2], 0)
        failed = {tuple(r['slot'].values()) for r in result['slotReasons']
                  if 'run-failed' in r['reasons']}
        self.assertEqual(failed, {('measured', 0), ('measured', 2)})

    def test_timeout_slot_not_retried_and_later_slots_execute(self):
        prepared = []

        def prepare(slot):
            ordinal = len(prepared)
            prepared.append(slot)
            return self.invocation(ordinal, 'import time;time.sleep(10)' if ordinal == 0 else '',
                                   timeout=20_000_000 if ordinal == 0 else 3_000_000_000)

        observations, result = observe_slots('cold', prepare)
        self.assertEqual(len(prepared), 10)
        self.assertTrue(observations[0][1].timed_out)
        self.assertEqual(observations[0][1].returncode, -signal.SIGKILL)
        self.assertTrue(all(o.returncode == 0 for _, o in observations[1:]))
        self.assertEqual([r['slot'] for r in result['slotReasons'] if 'timeout' in r['reasons']],
                         [dict(kind='warmup', index=0)])

    def test_preparation_error_aborts_without_fabricating_complete_batch(self):
        prepared = []

        def prepare(slot):
            ordinal = len(prepared)
            prepared.append(slot)
            if ordinal == 2:
                raise RuntimeError('caller preparation failed')
            return self.invocation(ordinal, '')

        with self.assertRaisesRegex(RuntimeError, 'caller preparation failed'):
            observe_slots('cold', prepare)
        self.assertEqual(len(prepared), 3)
        self.assertFalse((self.root / '2.stdout').exists())

    def test_invalid_reset_and_preparation_refused_before_callback(self):
        def fail(slot):
            self.fail('callback invoked for invalid reset')

        for reset in [None, True, 'other']:
            with self.assertRaises(Refusal):
                observe_slots(reset, fail)
        with self.assertRaises(Refusal):
            observe_slots('cold', None)
        with self.assertRaises(Refusal):
            observe_slots('cold', lambda slot: {})
        self.assertEqual(self.outputs, [])


if __name__ == '__main__':
    unittest.main()
