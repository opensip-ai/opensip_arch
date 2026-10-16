"""Unit B2-b4c1's blind held-out census controls (B2-b4 plan r6 section 2.5): a canary in a held-out tree's names and
content never reaches the receipt, stdout or stderr; each error class is reduced to its class; an invalid receipt
refuses; a blind receipt survives ordinary regeneration and goes stale on drift in each binding; and the ordinary mode
never touches a held-out store. Synthetic stores, receipts and models only; no T2 cache, network or environment input.
"""
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
import copy
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_discovery_census import ROOT, census, closure_copy, entry, make_store, unlock  # noqa: E402

CANARY = 'zq-canary-7f3e'
C = census.costs(census.Path(census.__file__).resolve().parents[2])
LIMITS = C['LIMITS']


class Fake:
    """A model result with the fields the blind row reads."""

    def __init__(self, objects, edges, bytes_, observed):
        self.objects, self.edges, self._bytes, self.observed = objects, edges, bytes_, observed

    def bytes_at(self, length):
        return self._bytes


def fits(tree):
    return Fake(LIMITS[0] // 4, LIMITS[1] // 4, LIMITS[2] // 4, set(tree.nodes)), set(tree.nodes)


def over(tree):
    return Fake(LIMITS[0] // 2 + 1, LIMITS[1] // 4, LIMITS[2] // 4, set(tree.nodes)), set(tree.nodes)


class Fixture(unittest.TestCase):
    """A product copy (the cost closure and this tool), an architecture copy holding a synthetic manifest, and a cache
    whose store holds one lead-readable and two held-out trees, each held-out tree carrying the canary in its names and
    its content."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.product = closure_copy(os.path.join(self.tmp, 'product'))
        for rel in (census.TOOL,) + census.REFERENCE_PRODUCT:
            (self.product / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / rel, self.product / rel)
        (self.product / census.OUTPUT_RECEIPT).parent.mkdir(parents=True, exist_ok=True)
        self.arch = Path(self.tmp, 'arch')
        # The reference-loading inputs the receipt binds (r2, Codex B2B4C1-R1-RF-3): synthetic bytes here.
        for rel in census.REFERENCE_ARCH:
            (self.arch / rel).parent.mkdir(parents=True, exist_ok=True)
            (self.arch / rel).write_bytes(b'# synthetic ' + rel.encode() + b'\n')
        self.cache = os.path.join(self.tmp, 'cache')
        self.store = os.path.join(self.cache, 'store')
        os.makedirs(self.store)
        self.files = {'readable': {'Cargo.toml': b'[package]\n'},
                      'held-a': {CANARY + '/Cargo.toml': b'[package]\nname = "' + CANARY.encode() + b'"\n'},
                      'held-b': {'package.json': b'{"name": "' + CANARY.encode() + b'"}', CANARY + '.txt': b''}}
        self.entries = [entry('readable', self.files['readable']), entry('held-a', self.files['held-a'], held_out=True),
                        entry('held-b', self.files['held-b'], held_out=True)]
        for e in self.entries:
            make_store(os.path.join(self.store, e['treeDigest']['value']), self.files[e['id']])
        self.write_manifest(dict(repositories=self.entries, workspaces=[]))

    def tearDown(self):
        unlock(self.tmp)
        shutil.rmtree(self.tmp)

    def write_manifest(self, manifest):
        self.manifest = manifest
        path = self.arch / census.MANIFEST
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(json.dumps(manifest, indent=1).encode())

    def held(self, id_):
        return next(e for e in self.entries if e['id'] == id_)

    def blind(self, measure=fits, c=C):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            census.run_blind(self.product, self.arch, self.cache, c, measure)
        raw = (self.product / census.OUTPUT_RECEIPT).read_bytes()
        return raw, json.loads(raw), out.getvalue(), err.getvalue()

    def compose(self, c=C):
        receipt_path = self.product / census.OUTPUT_RECEIPT
        receipt = json.loads(receipt_path.read_bytes()) if receipt_path.is_file() else None
        return census.compose_held_out(self.manifest, receipt, census.receipt_bindings(self.product, self.arch, c))

    def assert_closed(self, receipt):
        """The allow-list: the closed top level, public bindings only, and rows in exactly the two closed formats."""
        self.assertEqual(set(receipt), census.RECEIPT_KEYS)
        self.assertEqual(receipt['bindings'], census.receipt_bindings(self.product, self.arch, C))
        self.assertIn(receipt['state'], ('holds (blind census)', 'fails (blind census)', 'incomplete (blind census)'))
        for r in receipt['rows']:
            self.assertIn(r['id'], ('held-a', 'held-b'))
            if r['status'] == 'measured':
                self.assertEqual(set(r), census.MEASURED_KEYS)
                self.assertEqual(set(r['marginPermille']), {'objects', 'edges', 'bytes'})
                self.assertTrue(all(type(v) is int for v in r['marginPermille'].values()))
                self.assertIs(type(r['passes2x']), bool)
            else:
                self.assertEqual(r['status'], 'error')
                self.assertEqual(set(r), census.ERROR_KEYS)
                self.assertIn(r['errorClass'], census.ERROR_CLASSES)


class Canary(Fixture):
    def check_silent(self, raw, out, err):
        for text in (raw.decode(), out, err):
            self.assertNotIn(CANARY, text)
            self.assertNotIn(self.tmp, text)
        self.assertEqual(err, '')
        self.assertRegex(out, r'^Blind held-out census: \d+ entries, \d+ measured, \d+ passing, \d+ errors\.\n$')

    def test_a_measured_run_emits_only_the_closed_rows(self):
        raw, receipt, out, err = self.blind()
        self.check_silent(raw, out, err)
        self.assert_closed(receipt)
        self.assertEqual([r['id'] for r in receipt['rows']], ['held-a', 'held-b'])
        self.assertEqual(receipt['rows'][0]['marginPermille'], dict(objects=4000, edges=4000, bytes=4000))
        self.assertEqual(receipt['state'], 'holds (blind census)')
        self.assertEqual(out, 'Blind held-out census: 2 entries, 2 measured, 2 passing, 0 errors.\n')

    def test_each_error_class_is_reduced_to_its_class(self):
        def model_error(tree):
            raise ValueError('model failed at ' + CANARY)

        def io_error(tree):
            raise PermissionError(13, 'denied', os.path.join(self.store, CANARY))

        def population(tree):
            m, expected = fits(tree)
            return m, expected | {CANARY + '/extra'}

        def unknown(tree):
            raise RuntimeError(CANARY)

        def exit_(tree):
            raise SystemExit(os.path.join(self.store, CANARY))
        for measure, kind in ((model_error, 'MODEL'), (io_error, 'IO'), (population, 'POPULATION'), (unknown, 'MODEL'), (exit_, 'MODEL')):
            raw, receipt, out, err = self.blind(measure)
            self.check_silent(raw, out, err)
            self.assert_closed(receipt)
            self.assertEqual([r.get('errorClass') for r in receipt['rows']], [kind, kind], kind)
            self.assertEqual(receipt['state'], 'incomplete (blind census)')

    def test_a_tampered_store_is_integrity_and_a_missing_or_unreadable_one_is_io(self):
        a = os.path.join(self.store, self.held('held-a')['treeDigest']['value'])
        os.chmod(a, 0o755)
        Path(a, CANARY + '-planted').write_bytes(CANARY.encode())
        os.chmod(a, 0o555)
        b = os.path.join(self.store, self.held('held-b')['treeDigest']['value'])
        unlock(b)
        shutil.rmtree(b)
        raw, receipt, out, err = self.blind()
        self.check_silent(raw, out, err)
        self.assert_closed(receipt)
        self.assertEqual([r.get('errorClass') for r in receipt['rows']], ['INTEGRITY', 'IO'])
        os.chmod(self.store, 0)
        try:
            raw, receipt, out, err = self.blind()
        finally:
            os.chmod(self.store, 0o755)
        self.check_silent(raw, out, err)
        self.assertEqual([r.get('errorClass') for r in receipt['rows']], ['IO', 'IO'])

    def test_a_failing_margin_is_measured_and_fails(self):
        raw, receipt, out, err = self.blind(over)
        self.check_silent(raw, out, err)
        self.assert_closed(receipt)
        self.assertEqual(receipt['rows'][0]['marginPermille']['objects'], LIMITS[0] * 1000 // (LIMITS[0] // 2 + 1))
        self.assertEqual([r['passes2x'] for r in receipt['rows']], [False, False])
        self.assertEqual(receipt['state'], 'fails (blind census)')

    def test_the_command_line_prints_no_exception_text_in_the_blind_mode(self):
        missing = os.path.join(self.tmp, CANARY)
        result = subprocess.run([sys.executable, '-I', '-B', census.__file__, '--held-out-blind', '--architecture', missing,
                                 '--packages-root', missing, '--t2-cache', missing], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, '')
        self.assertEqual(result.stderr, 'Discovery census blind run failed.\n')
        ordinary = subprocess.run([sys.executable, '-I', '-B', census.__file__, '--check', '--architecture', missing,
                                   '--packages-root', missing], capture_output=True, text=True)
        self.assertEqual(ordinary.returncode, 1)
        self.assertIn(CANARY, ordinary.stderr)

    def test_an_abbreviated_option_is_refused_before_any_run(self):
        # r2 (Codex B2B4C1-R1-RF-2): abbreviations are not accepted, so no spelling reaches a run; the parser's refusal
        # echoes no input path.
        missing = os.path.join(self.tmp, CANARY)
        full = ['--architecture', missing, '--packages-root', missing, '--t2-cache', missing]
        # The repository's own receipt (absent before the B2-b4c2 run, present after) is left exactly as it was.
        receipt = ROOT / census.OUTPUT_RECEIPT
        before = receipt.read_bytes() if receipt.is_file() else None
        for args in (['--held-out-bl'] + full, ['--held'] + full,
                     ['--held-out-blind', '--arch', self.tmp, '--packages-root', missing, '--t2-cache', missing]):
            result = subprocess.run([sys.executable, '-I', '-B', census.__file__, *args], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2, args)
            self.assertEqual(result.stdout, '')
            self.assertNotIn(CANARY, result.stderr)
            self.assertEqual(receipt.read_bytes() if receipt.is_file() else None, before)

    def test_an_exit_or_interrupt_in_a_blind_run_prints_only_the_generic_line(self):
        # r2 (Codex B2B4C1-R1-RF-2): the redaction boundary covers SystemExit and KeyboardInterrupt, chosen from the
        # parsed arguments.
        argv, costs = sys.argv, census.costs
        for raised in (SystemExit(os.path.join(self.store, CANARY)), KeyboardInterrupt(CANARY), ValueError(CANARY)):
            def boom(product, sizes=None, raised=raised):
                raise raised
            out, err = io.StringIO(), io.StringIO()
            sys.argv = ['discovery_census.py', '--held-out-blind', '--architecture', str(self.arch), '--packages-root', self.tmp,
                        '--t2-cache', self.cache]
            census.costs = boom
            try:
                with redirect_stdout(out), redirect_stderr(err), self.assertRaises(SystemExit) as caught:
                    census.main()
            finally:
                sys.argv, census.costs = argv, costs
            self.assertEqual(caught.exception.code, 1)
            self.assertEqual(out.getvalue(), '')
            self.assertEqual(err.getvalue(), 'Discovery census blind run failed.\n')


class Receipts(Fixture):
    def setUp(self):
        super().setUp()
        _, self.receipt, _, _ = self.blind()

    def refuses(self, receipt, message):
        (self.product / census.OUTPUT_RECEIPT).write_bytes(json.dumps(receipt).encode())
        with self.assertRaisesRegex(ValueError, message):
            self.compose()

    def test_the_valid_receipt_composes(self):
        rows, state = self.compose()
        self.assertEqual(state, 'holds (blind census)')
        self.assertEqual([(r['id'], r['status'], r['result']['passes2x']) for r in rows],
                         [('held-a', 'blind-census', True), ('held-b', 'blind-census', True)])

    def test_missing_duplicate_or_unknown_ids_refuse(self):
        for rows in (self.receipt['rows'][:1], self.receipt['rows'] + [dict(self.receipt['rows'][0], id='readable')],
                     [self.receipt['rows'][0], dict(self.receipt['rows'][1], id='unknown')]):
            self.refuses(dict(self.receipt, rows=rows), 'receipt coverage differs')
        # A duplicate refuses as a format error, whether or not the receipt is stale.
        self.refuses(dict(self.receipt, rows=self.receipt['rows'] + self.receipt['rows'][:1]), 'a receipt id is duplicated')
        self.refuses(dict(self.receipt, rows=self.receipt['rows'] + self.receipt['rows'][:1], bindings={}), 'a receipt id is duplicated')

    def test_malformed_rows_refuse(self):
        measured = self.receipt['rows'][0]
        error = dict(id='held-b', status='error', errorClass='MODEL')
        cases = [(dict(error, marginPermille=measured['marginPermille']), 'error row shape'),
                 (dict(error, errorClass='Traceback'), 'error row shape'),
                 ({k: v for k, v in measured.items() if k != 'marginPermille'}, 'measured row shape'),
                 (dict(measured, marginPermille=dict(objects=1999, edges=4000, bytes=4000)), 'passes2x disagrees'),
                 (dict(measured, passes2x=False), 'passes2x disagrees'),
                 (dict(measured, marginPermille=dict(objects='4000', edges=4000, bytes=4000)), 'margins'),
                 (dict(measured, integrity=False), 'measured row shape'),
                 (dict(measured, note=CANARY), 'measured row shape'),
                 (dict(measured, status='skipped'), 'receipt row status')]
        for bad, message in cases:
            # Rows are checked before the state, so the state is left as recorded.
            self.refuses(dict(self.receipt, rows=[dict(bad, id='held-a'), self.receipt['rows'][1]]), message)

    def test_a_state_disagreeing_with_the_rows_or_an_open_shape_refuses(self):
        self.refuses(dict(self.receipt, state='fails (blind census)'), 'receipt state differs')
        self.refuses(dict(self.receipt, extra=CANARY), 'receipt shape')
        self.refuses(dict(self.receipt, rows=[]), 'receipt rows')


class Lifecycle(Fixture):
    def census_record(self):
        return census.census_output(self.product, self.arch, self.cache, C, None, None, None, None)

    def setUp(self):
        super().setUp()
        # Only the held-out rows are under test: the lead-readable entry is dropped from the manifest here.
        self.write_manifest(dict(repositories=self.entries[1:], workspaces=[]))

    def test_a_blind_result_survives_ordinary_regeneration(self):
        self.blind()
        first = self.census_record()
        self.assertEqual(self.census_record(), first)  # --check after --write compares equal
        body = json.loads(first)
        self.assertEqual(body['heldOutMargin'], 'holds (blind census)')
        self.assertEqual([e['status'] for e in body['entries']], ['blind-census', 'blind-census'])
        self.assertEqual(body['failingEntries'], [])
        self.assertEqual(body['caps'], 'recorded-margin-holds')

    def test_a_failing_blind_result_returns_the_caps(self):
        self.blind(over)
        body = json.loads(self.census_record())
        self.assertEqual(body['heldOutMargin'], 'fails (blind census)')
        self.assertEqual(body['failingEntries'], ['held-a', 'held-b'])
        self.assertEqual(body['caps'], 'returned-to-law')

    def test_an_incomplete_blind_result_keeps_the_gate_open(self):
        def model_error(tree):
            raise ValueError('x')
        self.blind(model_error)
        body = json.loads(self.census_record())
        self.assertEqual(body['heldOutMargin'], 'incomplete (blind census)')
        self.assertEqual(body['failingEntries'], [])

    def test_no_receipt_leaves_the_held_out_rows_outstanding(self):
        body = json.loads(self.census_record())
        self.assertEqual(body['heldOutMargin'], 'outstanding')
        self.assertEqual([e['status'] for e in body['entries']], ['outstanding: held-out'] * 2)

    def test_drift_in_each_binding_makes_the_receipt_stale(self):
        self.blind()
        tool = self.product / census.TOOL
        closure = self.product / census.CLOSURE[0][0]
        sizes = copy.deepcopy(C)
        name = sorted(sizes['SIZES'])[0]
        sizes['SIZES'] = dict(sizes['SIZES'], **{name: sizes['SIZES'][name] + 8})
        limits = dict(C, LIMITS=(LIMITS[0] - 1,) + tuple(LIMITS[1:]))
        manifest = copy.deepcopy(self.manifest)
        manifest['note'] = 'drift'

        def drifted(c=C):
            rows, state = self.compose(c)
            self.assertEqual(state, 'outstanding')
            self.assertEqual({r['status'] for r in rows}, {'outstanding: held-out (blind receipt stale)'})
        reference = [self.product / p for p in census.REFERENCE_PRODUCT] + [self.arch / p for p in census.REFERENCE_ARCH]
        for path in [tool, closure] + reference:
            original = path.read_bytes()
            path.write_bytes(original + b'\n')
            drifted()
            path.write_bytes(original)
        drifted(sizes)
        drifted(limits)
        original_lengths = census.ROOT_LENGTHS
        census.ROOT_LENGTHS = original_lengths[:-1] + (original_lengths[-1] + 1,)
        try:
            drifted()
        finally:
            census.ROOT_LENGTHS = original_lengths
        self.write_manifest(manifest)
        drifted()
        # A drifted manifest that changes the held-out set is stale too, never a coverage refusal.
        self.write_manifest(dict(repositories=self.entries, workspaces=[]))
        drifted()
        self.write_manifest(dict(repositories=self.entries[1:], workspaces=[]))
        self.assertEqual(self.compose()[1], 'holds (blind census)')


class Access(Fixture):
    def test_the_ordinary_census_touches_no_held_out_store(self):
        self.blind()
        seen = []
        real = (os.lstat, os.stat, os.scandir, os.listdir, os.readlink, open)

        def spy(fn):
            def call(path, *a, **k):
                seen.append(os.fspath(path))
                return fn(path, *a, **k)
            return call

        def stub(c, wv, ref, slm, rule, tree, label, source='automatic', roots=()):
            # The lead-readable entry's model is stubbed: only store access is under test.
            return type('M', (), dict(counts={}, objects=1, edges=1, bytes=1, per_root_byte=1, bytes_at=lambda self, r: 1 + r))()
        original = census.checked_model
        census.checked_model = stub
        os.lstat, os.stat, os.scandir, os.listdir, os.readlink = (spy(f) for f in real[:5])
        census.open = spy(open)
        try:
            body = json.loads(census.census_output(self.product, self.arch, self.cache, C, None, None, None, None))
        finally:
            os.lstat, os.stat, os.scandir, os.listdir, os.readlink = real[:5]
            del census.open
            census.checked_model = original
        self.assertEqual([e.get('status') for e in body['entries']], [None, 'blind-census', 'blind-census'])
        self.assertTrue([p for p in seen if self.held('readable')['treeDigest']['value'] in p])
        for id_ in ('held-a', 'held-b'):
            self.assertFalse([p for p in seen if self.held(id_)['treeDigest']['value'] in p], id_)

    def test_the_blind_join_refuses_outside_the_mode(self):
        with self.assertRaisesRegex(ValueError, 'for the blind mode only'):
            census.held_out_store_path(self.store, self.held('held-a'), object())
        with self.assertRaisesRegex(ValueError, 'for the blind mode only'):
            census.held_out_store_path(self.store, self.held('held-a'), None)
        with self.assertRaisesRegex(ValueError, 'takes held-out entries only'):
            census.held_out_store_path(self.store, self.held('readable'), census._BLIND)
        with self.assertRaisesRegex(ValueError, 'held-out entries are never opened'):
            census.store_path(self.store, self.held('held-a'))

    def test_a_held_out_workspace_refuses_the_blind_mode(self):
        self.write_manifest(dict(repositories=self.entries, workspaces=[dict(id='ws', heldOut=True)]))
        with self.assertRaisesRegex(ValueError, 'a held-out workspace'):
            self.blind()


if __name__ == '__main__':
    unittest.main()
