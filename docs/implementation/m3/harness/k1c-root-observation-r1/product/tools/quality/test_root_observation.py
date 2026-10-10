import errno
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from canonical import Refusal
from measurement import summarize_slots
from root_observation import observe_root


@unittest.skipUnless(sys.platform == 'darwin', 'Darwin informational owner')
class RootObservations(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='opensip-k1-root-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        os.chmod(self.root, 0o700)
        self.output = (self.root / 'out').open('w+b')
        self.addCleanup(self.output.close)
        self.devnull = os.open(os.devnull, os.O_WRONLY)
        self.addCleanup(os.close, self.devnull)

    def run_root(self, code, **kw):
        args = dict(cwd=self.root, environment={},
                    stdout_fd=self.output.fileno(), stderr_fd=self.devnull,
                    timeout_nanos=2_000_000_000)
        args.update(kw)
        return observe_root([sys.executable, '-I', '-B', '-c', code], **args)

    def test_actual_success_reaped_and_q6_quantities_stay_null(self):
        result = self.run_root('pass')
        self.assertEqual(result.returncode, 0)
        self.assertGreater(result.root_reaped_elapsed_nanos, 0)
        self.assertIsInstance(result.rss_native, int)
        self.assertIsNone(result.launch_errno)
        self.assertFalse(result.timed_out)
        with self.assertRaises(ChildProcessError):
            os.waitpid(result.pid, os.WNOHANG)
        row = result.slot_evidence({'kind': 'measured', 'index': 0})
        self.assertIsNone(row['elapsedNanos'])
        self.assertIsNone(row['cgroupMemoryPeakBytes'])
        self.assertEqual(row['rootReapedElapsedNanos'], result.root_reaped_elapsed_nanos)
        self.assertEqual(set(row['reasons']), {'memory-peak-unavailable-platform',
                                              'settlement-unverified-platform'})

    def test_nonzero_exit_keeps_actual_root_information(self):
        result = self.run_root('raise SystemExit(7)')
        self.assertEqual(result.returncode, 7)
        row = result.slot_evidence({'kind': 'measured', 'index': 0})
        self.assertIn('run-failed', row['reasons'])
        self.assertGreater(row['rootReapedElapsedNanos'], 0)
        self.assertIsNone(row['elapsedNanos'])

    def test_signal_exit_is_observed_without_new_public_route(self):
        result = self.run_root('import os, signal; os.kill(os.getpid(), signal.SIGTERM)')
        self.assertEqual(result.returncode, -signal.SIGTERM)
        self.assertIn('run-failed', result.slot_evidence({'kind': 'warmup', 'index': 0})['reasons'])

    def test_deadline_kills_and_reaps_only_owned_root(self):
        result = self.run_root('import time; time.sleep(10)', timeout_nanos=20_000_000)
        self.assertTrue(result.timed_out)
        self.assertEqual(result.returncode, -signal.SIGKILL)
        row = result.slot_evidence({'kind': 'measured', 'index': 0})
        self.assertIn('timeout', row['reasons'])
        self.assertIsNone(row['elapsedNanos'])
        self.assertGreater(row['rootReapedElapsedNanos'], 0)
        with self.assertRaises(ChildProcessError):
            os.waitpid(result.pid, os.WNOHANG)

    def test_failed_launch_retains_errno_and_no_fabricated_sample(self):
        result = observe_root([str(self.root / 'absent')], cwd=self.root,
                              environment={}, stdout_fd=self.output.fileno(),
                              stderr_fd=self.devnull, timeout_nanos=1_000_000)
        self.assertEqual(result.launch_errno, errno.ENOENT)
        self.assertIsNone(result.pid)
        self.assertIsNone(result.rss_native)
        row = result.slot_evidence({'kind': 'measured', 'index': 0})
        self.assertIsNone(row['rootReapedElapsedNanos'])
        self.assertIn('run-failed', row['reasons'])

    def test_real_environment_and_eof_stdin(self):
        result = self.run_root('import os,sys,json; print(json.dumps([dict(os.environ),sys.stdin.read()]))',
                               environment={'K1_TEST_TOKEN': 'public-fixture'})
        self.assertEqual(result.returncode, 0)
        self.output.seek(0)
        env, text = json.loads(self.output.read())
        self.assertEqual(env['K1_TEST_TOKEN'], 'public-fixture')
        self.assertNotIn('HOME', env)
        self.assertNotIn('PATH', env)
        self.assertNotIn('CARGO_HOME', env)
        self.assertEqual(text, '')

    def test_inheritable_extra_descriptor_is_closed(self):
        fd = os.open(self.root / 'descriptor-fixture', os.O_CREAT | os.O_RDWR, 0o600)
        self.addCleanup(os.close, fd)
        os.set_inheritable(fd, True)
        code = ('import os,json; closed=False\n'
                'try: os.fstat(' + str(fd) + ')\n'
                'except OSError: closed=True\n'
                'print(json.dumps(closed))')
        self.assertEqual(self.run_root(code).returncode, 0)
        self.output.seek(0)
        self.assertTrue(json.loads(self.output.read()))

    def test_interrupted_wait_retries_actual_observation(self):
        original = os.wait4
        count = 0
        def wait(pid, options):
            nonlocal count
            count += 1
            if count == 1:
                raise InterruptedError()
            return original(pid, options)
        with patch('root_observation.os.wait4', side_effect=wait):
            result = self.run_root('pass')
        self.assertEqual(result.returncode, 0)
        self.assertGreater(count, 1)

    def test_no_popen_poll_or_wait_can_steal_wait4_counter(self):
        with patch.object(subprocess.Popen, 'poll', side_effect=AssertionError('poll reaps')):
            result = self.run_root('import time; time.sleep(10)', timeout_nanos=20_000_000)
        self.assertTrue(result.timed_out)
        self.assertIsNotNone(result.rss_native)

    def test_slot_accounting_remains_incomplete_with_no_budget_inputs(self):
        result = self.run_root('pass')
        rows = [result.slot_evidence({'kind': k, 'index': i})
                for k, n in [('warmup', 3), ('measured', 7)] for i in range(n)]
        summary = summarize_slots('cold', rows)
        self.assertTrue(summary['incomplete'])
        self.assertIsNone(summary['medianElapsedNanos'])
        self.assertIsNone(summary['maxCgroupMemoryPeakBytes'])

    def test_parent_interruption_reaps_created_root_before_propagating(self):
        original_wait = os.wait4
        original_popen = subprocess.Popen
        children = []
        def spawn(*args, **kw):
            child = original_popen(*args, **kw)
            children.append(child)
            return child
        calls = 0
        def wait(pid, options):
            nonlocal calls
            calls += 1
            if calls == 1:
                raise KeyboardInterrupt()
            return original_wait(pid, options)
        with patch('root_observation.subprocess.Popen', side_effect=spawn), \
                patch('root_observation.os.wait4', side_effect=wait):
            with self.assertRaises(KeyboardInterrupt):
                self.run_root('import time; time.sleep(10)')
        self.assertEqual(len(children), 1)
        self.assertIsNotNone(children[0].returncode)
        with self.assertRaises(ChildProcessError):
            os.waitpid(children[0].pid, os.WNOHANG)

    def test_invalid_boundary_inputs_never_launch(self):
        base = dict(cwd=self.root, environment={}, stdout_fd=self.output.fileno(),
                    stderr_fd=self.devnull, timeout_nanos=1)
        cases = [(['relative'], {}), ([sys.executable], {'timeout_nanos': True}),
                 ([sys.executable], {'environment': {'bad=key': 'value'}}),
                 ([sys.executable], {'stdout_fd': True})]
        with patch('root_observation.subprocess.Popen', side_effect=AssertionError('launched')):
            for argv, extra in cases:
                with self.subTest(argv=argv, extra=extra), self.assertRaises(Refusal):
                    observe_root(argv, **(base | extra))


if __name__ == '__main__':
    unittest.main()
