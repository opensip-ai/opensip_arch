"""Unit C1a4-blind's companion blind held-out census controls (C1a plan r6 RF-3; B2-b4 plan r6 section 2.5; Codex
C1A4-R1-NBO-1): a canary in a held-out tree's names and content never reaches the receipt, stdout or stderr; each error
class is reduced to its class, and an over-item-5 entry to its closed row; an invalid receipt refuses; a blind receipt
survives ordinary regeneration, returns the caps on a failure and goes stale on drift in each binding; the ordinary
mode never touches a held-out store, and the held-out join refuses outside the blind mode; and the census reads no
product source its receipt does not bind. Synthetic stores, receipts and rule; the product sources are copied into a
scratch product holding exactly the bound set. No T2 cache, network or environment input.
"""
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
import copy
import importlib.util
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_discovery_census import ROOT, census as dc_root, entry, make_store, unlock  # noqa: E402

CANARY = 'zq-canary-5d1b'
TOOL = 'tools/security/snapshot_ledger_census.py'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


slc = load('snapshot_ledger_census_under_test', ROOT / TOOL)


class Rule:
    """A synthetic discovery rule: nothing is pruned, and the reference's markers."""
    WORKSPACE_MARKERS = ('Cargo.toml', 'package.json', 'tsconfig.json', 'jsconfig.json')

    class RootGrammarError(ValueError):
        pass

    @staticmethod
    def classify_path(rel, cargo_roots, member_roots=()):
        return None

    @staticmethod
    def normalize_explicit_root(spec):
        raise Rule.RootGrammarError('ROOT_GRAMMAR')


def bound_product(tmp):
    """A product copy holding exactly the census's bound inputs: the four tools, discovery's reference-loading
    product files, discovery's cost closure, and every snapshot source the receipt binds."""
    model = load('snapshot_ledger_model_bound', ROOT / slc.MODEL)
    paths = {slc.TOOL, slc.MODEL, slc.DISCOVERY, slc.MEMBER_MODEL} | set(dc_root.REFERENCE_PRODUCT) | {p for p, _, _ in dc_root.CLOSURE}
    paths |= set(model.SNAPSHOT_FILES) | {p for _, p, _ in model.SNAPSHOT_ANCHORS} | {p for _, p, _, _ in model.SESSION_ANCHORS}
    paths |= {p for _, p, _ in model.VCS_ANCHORS}
    paths |= set(model.SESSION_FILES) | {model.WORK_LEDGER} | set(slc.ANCHORED)
    for rel in sorted(paths):
        (Path(tmp) / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / rel, Path(tmp) / rel)
    return Path(tmp)


class Fixture(unittest.TestCase):
    """A bound product copy, an architecture copy holding a synthetic manifest and reference inputs, and a cache whose
    store holds one lead-readable and two held-out trees, each held-out tree carrying the canary in its names and its
    content."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.product = bound_product(os.path.join(self.tmp, 'product'))
        (self.product / slc.OUTPUT_RECEIPT).parent.mkdir(parents=True, exist_ok=True)
        self.arch = Path(self.tmp, 'arch')
        for rel in dc_root.REFERENCE_ARCH:
            (self.arch / rel).parent.mkdir(parents=True, exist_ok=True)
            (self.arch / rel).write_bytes(b'# synthetic ' + rel.encode() + b'\n')
        self.cache = os.path.join(self.tmp, 'cache')
        self.store = os.path.join(self.cache, 'store')
        os.makedirs(self.store)
        self.files = {'readable': {'Cargo.toml': b'[package]\n', 'src/lib.rs': b''},
                      'held-a': {CANARY + '/Cargo.toml': b'[package]\nname = "' + CANARY.encode() + b'"\n',
                                 CANARY + '/' + CANARY + '.rs': CANARY.encode()},
                      'held-b': {'package.json': b'{"name": "' + CANARY.encode() + b'"}', CANARY + '.txt': CANARY.encode()}}
        self.entries = [entry('readable', self.files['readable']), entry('held-a', self.files['held-a'], held_out=True),
                        entry('held-b', self.files['held-b'], held_out=True)]
        for e in self.entries:
            make_store(os.path.join(self.store, e['treeDigest']['value']), self.files[e['id']])
        self.write_manifest(dict(repositories=self.entries, workspaces=[]))
        self.census = self.make()

    def tearDown(self):
        unlock(self.tmp)
        shutil.rmtree(self.tmp)

    def make(self):
        c = slc.Census(self.product, self.arch, reference=(Rule, None))
        dc = c.dc
        c.population = lambda tree: dc.model(c.c, Rule, tree).observed
        return c

    def write_manifest(self, manifest):
        self.manifest = manifest
        path = self.arch / dc_root.MANIFEST
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(json.dumps(manifest, indent=1).encode())

    def held(self, id_):
        return next(e for e in self.entries if e['id'] == id_)

    def blind(self, census=None):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            slc.run_blind(census or self.census, self.cache)
        raw = (self.product / slc.OUTPUT_RECEIPT).read_bytes()
        return raw, json.loads(raw), out.getvalue(), err.getvalue()

    def record(self, census=None):
        return json.loads((census or self.census).record(self.cache, log=False))

    def check_silent(self, raw, out, err):
        for text in (raw.decode(), out, err):
            self.assertNotIn(CANARY, text)
            self.assertNotIn(self.tmp, text)
        self.assertEqual(err, '')
        self.assertRegex(out, r'^Blind held-out snapshot census: \d+ entries, \d+ measured, \d+ passing, \d+ over item 5, \d+ errors\.\n$')

    def assert_closed(self, receipt):
        self.assertEqual(set(receipt), slc.RECEIPT_KEYS)
        self.assertEqual(receipt['bindings'], self.census.bindings())
        for r in receipt['rows']:
            self.assertIn(r['id'], ('held-a', 'held-b'))
            keys = {'measured': slc.MEASURED_KEYS, 'over-item-5': slc.OVER_KEYS, 'error': slc.ERROR_KEYS}[r['status']]
            self.assertEqual(set(r), keys)
            if r['status'] == 'measured':
                self.assertEqual(set(r['marginPermille']), {'objects', 'edges', 'bytes'})
                self.assertTrue(all(type(v) is int for v in r['marginPermille'].values()))
                self.assertIs(type(r['passes2x']), bool)
            if r['status'] == 'error':
                self.assertIn(r['errorClass'], slc.ERROR_CLASSES)


class Canary(Fixture):
    def test_a_measured_run_emits_only_the_closed_rows(self):
        raw, receipt, out, err = self.blind()
        self.check_silent(raw, out, err)
        self.assert_closed(receipt)
        self.assertEqual([r['status'] for r in receipt['rows']], ['measured', 'measured'])
        self.assertEqual(receipt['state'], 'holds (blind census)')

    def test_the_blind_margins_are_the_lead_readable_measure(self):
        """One computation path: a held-out tree's margins equal the lead-readable row's for the same tree."""
        _, receipt, _, _ = self.blind()
        dc = self.census.dc
        for r in receipt['rows']:
            e = self.held(r['id'])
            tree = dc.verified_tree(os.path.join(self.store, e['treeDigest']['value']), e)
            row = self.census.price(tree, r['id'])
            margin = row['margins'][slc.PROFILE]
            self.assertEqual(r['marginPermille'], {k: margin[k]['marginPermille'] for k in slc.KEYS})
            self.assertEqual(r['passes2x'], margin['passes2x'])

    def test_each_error_class_is_reduced_to_its_class(self):
        cases = {}
        census = self.make()
        census.measure = lambda tree: (_ for _ in ()).throw(ValueError(CANARY))
        cases['MODEL'] = census
        census = self.make()
        census.population = lambda tree: {CANARY}
        cases['POPULATION'] = census
        census = self.make()
        census.measure = lambda tree: (_ for _ in ()).throw(SystemExit(CANARY))
        cases['MODEL-exit'] = census
        for kind, census in cases.items():
            raw, receipt, out, err = self.blind(census)
            self.check_silent(raw, out, err)
            self.assert_closed(receipt)
            self.assertEqual({r['errorClass'] for r in receipt['rows']}, {kind.split('-')[0]}, kind)
            self.assertEqual(receipt['state'], 'incomplete (blind census)')

    def test_a_tampered_store_is_integrity_and_a_missing_one_is_io(self):
        a = os.path.join(self.store, self.held('held-a')['treeDigest']['value'])
        unlock(a)
        os.chmod(Path(a, CANARY + '/Cargo.toml'), 0o644)
        Path(a, CANARY + '/Cargo.toml').write_bytes(b'[package]\n' + CANARY.encode())
        b = os.path.join(self.store, self.held('held-b')['treeDigest']['value'])
        unlock(b)
        shutil.rmtree(b)
        raw, receipt, out, err = self.blind()
        self.check_silent(raw, out, err)
        self.assertEqual({r['id']: r['errorClass'] for r in receipt['rows']}, {'held-a': 'INTEGRITY', 'held-b': 'IO'})

    def test_an_over_item_5_entry_is_its_closed_row(self):
        census = self.make()
        census.limits = (0,) + census.limits[1:]
        raw, receipt, out, err = self.blind(census)
        self.check_silent(raw, out, err)
        self.assertEqual({r['status'] for r in receipt['rows']}, {'over-item-5'})
        self.assertEqual({frozenset(r) for r in receipt['rows']}, {frozenset(slc.OVER_KEYS)})
        self.assertEqual(receipt['state'], 'holds (blind census)')

    def test_a_held_out_member_is_a_model_error(self):
        census = self.make()
        measure = census.measure
        census.measure = lambda tree: dict(measure(tree), members=(CANARY,))
        raw, receipt, out, err = self.blind(census)
        self.check_silent(raw, out, err)
        self.assertEqual({r['errorClass'] for r in receipt['rows']}, {'MODEL'})

    def test_the_command_line_prints_only_the_generic_line_in_the_blind_mode(self):
        missing = os.path.join(self.tmp, CANARY)
        r = subprocess.run([sys.executable, '-I', '-B', str(self.product / TOOL), '--held-out-blind', '--architecture', str(self.arch),
                            '--packages-root', missing, '--t2-cache', self.cache], capture_output=True, text=True)
        self.assertEqual((r.returncode, r.stdout, r.stderr), (1, '', 'Snapshot ledger census blind run failed.\n'))

    def test_an_abbreviated_option_is_refused_before_any_run(self):
        r = subprocess.run([sys.executable, '-I', '-B', str(self.product / TOOL), '--held-out', '--architecture', str(self.arch),
                            '--packages-root', self.tmp, '--t2-cache', self.cache], capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)
        self.assertFalse((self.product / slc.OUTPUT_RECEIPT).exists())


class Receipts(Fixture):
    def setUp(self):
        super().setUp()
        _, self.receipt, _, _ = self.blind()
        self.ids = ['held-a', 'held-b']

    def compose(self, receipt):
        return slc.compose_held_out(self.ids, receipt, self.census.bindings())

    def test_the_valid_receipt_composes(self):
        rows, state = self.compose(self.receipt)
        self.assertEqual(state, 'holds (blind census)')
        self.assertEqual([r['status'] for r in rows], ['blind-census', 'blind-census'])

    def test_missing_duplicate_or_unknown_ids_refuse(self):
        for rows in (self.receipt['rows'][:1], self.receipt['rows'] + self.receipt['rows'][:1],
                     self.receipt['rows'][:1] + [dict(self.receipt['rows'][1], id='unknown')]):
            bad = dict(self.receipt, rows=rows)
            with self.assertRaises(ValueError):
                self.compose(bad)

    def test_malformed_rows_refuse(self):
        measured = self.receipt['rows'][0]
        for row in (dict(measured, passes2x=not measured['passes2x']),
                    {k: v for k, v in measured.items() if k != 'marginPermille'},
                    dict(id='held-a', status='error', errorClass='MODEL', marginPermille=measured['marginPermille']),
                    dict(id='held-a', status='error', errorClass=CANARY),
                    dict(id='held-a', status='over-item-5', integrity=True, population=True, marginPermille=measured['marginPermille']),
                    dict(measured, marginPermille=dict(measured['marginPermille'], objects=-1)),
                    dict(measured, status='passed')):
            bad = dict(self.receipt, rows=[row, self.receipt['rows'][1]])
            with self.assertRaises(ValueError):
                self.compose(bad)

    def test_a_state_disagreeing_with_the_rows_or_an_open_shape_refuses(self):
        for bad in (dict(self.receipt, state='fails (blind census)'), dict(self.receipt, extra=1), dict(self.receipt, schemaVersion=2)):
            with self.assertRaises(ValueError):
                self.compose(bad)


class Lifecycle(Fixture):
    def test_a_blind_result_survives_ordinary_regeneration(self):
        self.blind()
        first = self.record()
        self.assertEqual(first['heldOutMargin'], 'holds (blind census)')
        self.assertEqual([r['status'] for r in first['heldOutEntries']], ['blind-census', 'blind-census'])
        self.assertEqual(first, self.record())
        self.assertEqual(first['capsStatus'], 'recorded-margin-holds')

    def test_a_failing_blind_result_returns_the_caps(self):
        census = self.make()
        census.caps = {slc.PROFILE: (1, 1, 1)}
        self.blind(census)
        record = self.record(census)
        self.assertEqual(record['heldOutMargin'], 'fails (blind census)')
        self.assertIn('held-a', record['failing2x'][slc.PROFILE])
        self.assertEqual(record['capsStatus'], 'returned-to-law')

    def test_an_incomplete_blind_result_keeps_the_gate_open(self):
        census = self.make()
        census.population = lambda tree: set()
        self.blind(census)
        self.assertEqual(self.record()['heldOutMargin'], 'incomplete (blind census)')

    def test_no_receipt_leaves_the_held_out_rows_outstanding(self):
        record = self.record()
        self.assertEqual(record['heldOutMargin'], 'outstanding')
        self.assertEqual([r['status'] for r in record['heldOutEntries']], ['outstanding: held-out'] * 2)

    def assert_stale(self, census):
        record = self.record(census)
        self.assertEqual(record['heldOutMargin'], 'outstanding')
        self.assertEqual([r['status'] for r in record['heldOutEntries']], ['outstanding: held-out (blind receipt stale)'] * 2)

    def test_drift_in_each_binding_makes_the_receipt_stale(self):
        self.blind()
        receipt = json.loads((self.product / slc.OUTPUT_RECEIPT).read_bytes())
        self.assertEqual(set(receipt['bindings']), {'discovery', 'tools', 'snapshotSources', 'caps', 'item5', 'maxUnitDepth', 'afterWalk'})
        # Each binding drifted alone, in the current inputs, makes the bound receipt stale.
        for key in receipt['bindings']:
            census = self.make()
            current = copy.deepcopy(census.bindings())
            if isinstance(current[key], list):
                current[key][0] = dict(current[key][0], sha256='0' * 64)
            elif isinstance(current[key], dict):
                first = sorted(current[key])[0]
                current[key][first] = 'drift'
            else:
                current[key] = current[key] + 1
            census.bindings = lambda current=current: current
            self.assert_stale(census)
        # And by real bytes: a bound snapshot source, the companion tool and discovery's member model.
        for rel in (slc.SEAL, slc.TOOL, slc.MEMBER_MODEL):
            path = self.product / rel
            original = path.read_bytes()
            path.write_bytes(original + (b'\n// drift\n' if rel.endswith('.rs') else b'\n# drift\n'))
            try:
                self.assert_stale(self.make())
            finally:
                path.write_bytes(original)


class Access(Fixture):
    def test_the_ordinary_census_touches_no_held_out_store(self):
        held = [os.path.join(self.store, self.held(i)['treeDigest']['value']) for i in ('held-a', 'held-b')]
        touched = []
        real = {name: getattr(os, name) for name in ('lstat', 'stat', 'scandir', 'listdir', 'open', 'readlink')}

        def spy(name):
            def call(path, *args, **kwargs):
                touched.append(os.fspath(path) if not isinstance(path, int) else '')
                return real[name](path, *args, **kwargs)
            return call
        for name in real:
            setattr(os, name, spy(name))
        try:
            self.record()
        finally:
            for name, fn in real.items():
                setattr(os, name, fn)
        self.assertTrue(touched)
        self.assertFalse([p for p in touched if any(p.startswith(h) for h in held)])

    def test_the_held_out_join_refuses_outside_the_mode(self):
        with self.assertRaises(ValueError):
            self.census.dc.held_out_store_path(self.store, self.held('held-a'), object())
        with self.assertRaises(ValueError):
            self.census.dc.store_path(self.store, self.held('held-a'))

    def test_a_held_out_workspace_refuses_the_blind_mode(self):
        self.write_manifest(dict(self.manifest, workspaces=[dict(id='ws', heldOut=True)]))
        with self.assertRaises(ValueError):
            self.census.blind(self.cache, self.census.dc._BLIND)


class Completeness(Fixture):
    def test_the_census_reads_no_product_source_its_receipt_leaves_unbound(self):
        """The fixture's product holds only the bound inputs; the census builds and runs there. And every product path
        the tool and the model name is bound, by the companion's own bindings or by discovery's closure and tools."""
        _, receipt, _, _ = self.blind()
        b = receipt['bindings']
        bound = {r['path'] for r in b['tools'] + b['snapshotSources'] + b['discovery']['closure']}
        bound |= {b['discovery']['tool']['path'], b['discovery']['memberModel']['path']}
        bound |= {r['path'] for r in b['discovery']['reference'] if not r['path'].startswith('docs/')}
        named = set()
        for rel in (slc.TOOL, slc.MODEL):
            named |= set(re.findall(r"'((?:crates|tools)/[^']+\.(?:rs|py|json))'", (ROOT / rel).read_text()))
        unbound = sorted(n for n in named if n not in bound and not n.endswith('.json'))
        self.assertEqual(unbound, [])


if __name__ == '__main__':
    unittest.main()
