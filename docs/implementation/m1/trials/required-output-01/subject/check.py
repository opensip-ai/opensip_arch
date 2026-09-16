"""Run in a mutable candidate copy with the pinned reference Python -I -B."""
from pathlib import Path
import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
import unittest

HERE = Path(__file__).resolve().parent
assert sys.flags.isolated == 1 and sys.dont_write_bytecode
PINS = json.loads((HERE / 'input-pins.json').read_text())['files']
for row in PINS:
    for path in (Path(row['path']), HERE / row['copy']):
        raw = path.read_bytes()
        assert len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256'], path


def load(name, path):
    # Compile verified source, ignoring any adjacent Python bytecode cache.
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(path.read_bytes(), str(path), 'exec'), module.__dict__)
    return module


F = load('required_output_reference', HERE / 'output_finalization.py')
R = load('report08_reference', HERE / 'owner/report_model.py')
D = load('d9_required_output_owner', HERE / 'owner/d9/check-d9-v1.14.py')
CONTRACT = json.loads((HERE / 'owner/d9/d9-exit-contract.v1.14.json').read_text())
goldens = next(v for k, v in CONTRACT.items() if isinstance(v, list) and any(isinstance(r, dict) and r.get('id') == 'machine-output-serialization-failed' for r in v))
GOLDEN = next(r for r in goldens if r.get('id') == 'machine-output-serialization-failed')
FAULT = dict({'class': D.derive_class(GOLDEN['scenarioAxes'])}, **D.derive_codes(GOLDEN['scenarioAxes'], CONTRACT['codeMaps']))
assert FAULT == GOLDEN['expectedTermination']
EXITS = CONTRACT['classToExitCode']


class Writer:
    def __init__(self, limit=None, flush_fault=False, max_write=None, progress=None):
        self.data = bytearray()
        self.limit = limit
        self.flush_fault = flush_fault
        self.max_write = max_write
        self.progress = progress
        self.calls = 0
        self.flushes = 0

    def write(self, raw):
        self.calls += 1
        if self.progress is not None:
            return self.progress
        count = len(raw) if self.max_write is None else min(len(raw), self.max_write)
        if self.limit is not None:
            if len(self.data) >= self.limit:
                raise OSError('private path and caller text must never reach diagnostic')
            count = min(count, self.limit - len(self.data))
        self.data.extend(raw[:count])
        return count

    def flush(self):
        self.flushes += 1
        if self.flush_fault:
            raise OSError('private flush diagnostic')


def envelope(aggregate):
    # Minimal stand-in, deliberately not presented as a schema-admitted envelope.
    return {'termination': copy.deepcopy(aggregate), 'exitCode': EXITS[aggregate['class']],
            'availability': {'requiredSelection': ['never-remove-this']}}


AGGREGATES = [{'class': c} for c in EXITS if c != 'interrupted']
AGGREGATES += [{'class': 'interrupted', 'signal': signal} for signal in ['SIGINT', 'SIGTERM', 'SIGHUP']]
AGGREGATES += [dict(a, runId='run3:' + 'a'*64) for a in AGGREGATES if a['class'] == 'interrupted']


class OutputTests(unittest.TestCase):
    def perform(self, aggregate, encoder=R.canonical, writer=None, diag=None, env=None):
        f = F.Finalizer(aggregate, FAULT, EXITS)
        w = Writer() if writer is None else writer
        d = Writer() if diag is None else diag
        source = envelope(aggregate) if env is None else env
        before = copy.deepcopy((aggregate, source))
        result = f.deliver(source, encoder, w, d)
        self.assertEqual(before, (aggregate, source))
        self.assertEqual(f.commit_count, 1)
        return f, result, w, d

    def test_unchanged_d9_full_authority(self):
        proc = subprocess.run([sys.executable, '-I', '-B', str(HERE/'owner/d9/check-d9-v1.14.py')], capture_output=True, text=True)
        (HERE/'d9-base.stdout').write_text(proc.stdout)
        (HERE/'d9-base.stderr').write_text(proc.stderr)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(FAULT, {'class': 'operational-failed', 'errorCode': 'OUTPUT.SERIALIZATION_FAILED'})

    def test_success_preserves_each_aggregate_and_complete_bytes(self):
        for aggregate in AGGREGATES:
            with self.subTest(aggregate=aggregate):
                f, r, w, d = self.perform(aggregate, writer=Writer(max_write=7))
                self.assertEqual(r, {'termination': aggregate, 'exitCode': EXITS[aggregate['class']], 'delivery': 'complete'})
                self.assertEqual(bytes(w.data), R.canonical(envelope(aggregate)))
                self.assertEqual(w.flushes, 1)
                self.assertEqual(d.calls, 0)

    def test_capacity_failure_never_emits_or_truncates(self):
        for aggregate in AGGREGATES:
            with self.subTest(aggregate=aggregate):
                f, r, w, d = self.perform(aggregate, lambda _: b'x' * (F.ENVELOPE_MAX_BYTES + 1))
                self.assertEqual(r, {'termination': FAULT, 'exitCode': 4, 'delivery': 'failed'})
                self.assertEqual(w.calls, 0)
                self.assertEqual(w.flushes, 0)
                self.assertEqual(bytes(d.data), F.DIAGNOSTIC)

    def test_exact_capacity_boundary_standin(self):
        for count in [F.ENVELOPE_MAX_BYTES-1, F.ENVELOPE_MAX_BYTES]:
            _, r, w, _ = self.perform({'class':'success'}, lambda _: b'x'*count)
            self.assertEqual(r['delivery'], 'complete')
            self.assertEqual(len(w.data), count)

    def test_codec_refusal_and_invalid_result_before_write(self):
        def refuse(_):
            raise F.SerializationFailure('secret codec context')
        for encoder in [refuse, lambda _: None, lambda _: '', lambda _: bytearray(b'{}'), lambda _: b'']:
            _, r, w, d = self.perform(AGGREGATES[-1], encoder)
            self.assertEqual(r['termination'], FAULT)
            self.assertEqual(w.calls, 0)
            self.assertEqual(bytes(d.data), F.DIAGNOSTIC)

    def test_aggregate_and_exit_join_failure_before_write(self):
        aggregate = AGGREGATES[-1]
        for field, value in [('termination', {'class':'success'}), ('exitCode', 0)]:
            env = envelope(aggregate); env[field] = value
            _, r, w, _ = self.perform(aggregate, env=env)
            self.assertEqual(r['termination'], FAULT)
            self.assertEqual(w.calls, 0)

    def test_stream_prefix_and_complete_flush_failure(self):
        for aggregate in AGGREGATES:
            raw = R.canonical(envelope(aggregate))
            for prefix in [0, 1, len(raw)//2, len(raw)-1, len(raw)]:
                with self.subTest(aggregate=aggregate, prefix=prefix):
                    writer = Writer(limit=prefix, flush_fault=prefix == len(raw))
                    _, r, w, d = self.perform(aggregate, writer=writer)
                    self.assertEqual(r['termination'], FAULT)
                    self.assertEqual(r['exitCode'], 4)
                    self.assertEqual(bytes(w.data), raw[:prefix])
                    self.assertEqual(bytes(d.data), F.DIAGNOSTIC)

    def test_invalid_writer_progress_is_not_success_or_infinite_retry(self):
        for progress in [0, -1, True, 0.5, 999999]:
            _, r, w, _ = self.perform({'class':'success'}, writer=Writer(progress=progress))
            self.assertEqual(r['termination'], FAULT)
            self.assertEqual(w.calls, 1)

    def test_diagnostic_fault_cannot_change_exit_or_retry_document(self):
        for diag in [Writer(limit=0), Writer(limit=3), Writer(flush_fault=True)]:
            _, r, w, d = self.perform(AGGREGATES[-1], writer=Writer(limit=0), diag=diag)
            self.assertEqual(r['exitCode'], 4)
            self.assertEqual(w.calls, 1)
            self.assertTrue(F.DIAGNOSTIC.startswith(bytes(d.data)))

    def test_after_commit_events_are_byte_identical_and_no_second_delivery(self):
        for writer in [Writer(), Writer(flush_fault=True)]:
            f, r, w, _ = self.perform(AGGREGATES[-1], writer=writer)
            before = bytes(w.data)
            for event in ['user-signal', 'transport-close', 'optional-delivery-failure']:
                self.assertEqual(f.after_commit(event), r['termination'])
            with self.assertRaisesRegex(RuntimeError, 'already-committed'):
                f.deliver(envelope(AGGREGATES[-1]), R.canonical, w, Writer())
            self.assertEqual(f.commit_count, 1)
            self.assertEqual(bytes(w.data), before)

    def test_unknown_reference_exception_is_not_fake_expected_fault(self):
        def bug(_): raise RuntimeError('unclassified programming error')
        with self.assertRaisesRegex(RuntimeError, 'programming error'):
            self.perform({'class':'success'}, bug)

    def test_report_owner_earlier_optional_run_cancellation_composition(self):
        rid = 'run3:'+'b'*64
        for signal in ['SIGINT', 'SIGTERM', 'SIGHUP']:
            for committed in [False, True]:
                steps = ([{'kind':'analysis','requirement':'optional','recorded':True,'outcome':'completed','termination':{'class':'success'},'analysisRunId':rid}] if committed else [])
                steps += [{'kind':'render','requirement':'required','recorded':True,'outcome':'cancelled','termination':{'class':'interrupted','signal':signal}}]
                before = copy.deepcopy(steps)
                aggregate = R.invocation_aggregate(steps, {'requested':True,'phase':'before-settle','signal':signal})
                self.assertEqual(aggregate.get('runId'), rid if committed else None)
                for fail in [False, True]:
                    _, result, _, _ = self.perform(aggregate, writer=Writer(flush_fault=fail))
                    self.assertEqual(result['exitCode'], 4 if fail else 130)
                    self.assertEqual(steps, before)

    def test_report_renderer_failure_keeps_its_original_step_code(self):
        for rid in [None, 'run3:'+'c'*64]:
            render = R.renderer_failure(rid)
            steps = [{'kind':'render','requirement':'required','recorded':True,'outcome':'failed','termination':render}]
            before = copy.deepcopy(steps)
            aggregate = R.invocation_aggregate(steps, None)
            self.assertEqual(aggregate['errorCode'], 'DELIVERY.REQUIRED_FAILED')
            for fail in [False, True]:
                _, result, _, _ = self.perform(aggregate, writer=Writer(flush_fault=fail))
                self.assertEqual(result['termination']['errorCode'], 'OUTPUT.SERIALIZATION_FAILED' if fail else 'DELIVERY.REQUIRED_FAILED')
                self.assertEqual(steps, before)


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(OutputTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    record = {'standing':'Root reference checks, not actual-Claude review or product qualification',
              'groups': result.testsRun, 'passed':result.wasSuccessful(), 'inputPins':len(PINS),
              'd9Fault':FAULT, 'capacityPolicy':'proposed explicit operational failure; no prevention guarantee',
              'limits':['Synthetic codec/writer and step records','No full oversized Run admission','No live signal/process or filesystem atomicity qualification','No source successor selected']}
    (HERE/'result.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(record,indent=2))
    raise SystemExit(0 if result.wasSuccessful() else 1)
