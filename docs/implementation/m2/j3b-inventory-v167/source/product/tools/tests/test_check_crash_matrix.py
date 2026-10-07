"""Regression controls for tools/check_crash_matrix.py (law X9 r1 item 7, r2 item 3).

Builds a small synthetic run set in a disposable directory against the
repository's real scope registry, checks that it passes, then that each
single corruption refuses. Nothing outside the temporary directory is read
except the registry source; nothing is written outside it.
"""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

REPOSITORY = Path(__file__).resolve().parents[2]
FILE = REPOSITORY / 'tools/check_crash_matrix.py'
spec = importlib.util.spec_from_file_location('crash_matrix', FILE)
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)

COMMIT = 'a' * 40
EPOCH = 1791072000
KILLED = 'x3b.append.seal.witness-pending/rename.after'
REPEATED = 'x3c.object/write.before'
HOST_POINT = 'x3b.append.terminal.commit.after'


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()


def required_rows():
    rows = [{
        'case': 'F07', 'variant': 'kill-witness-pending-rename-after', 'units': ['X3b'],
        'labels': ['process-death', 'scripted-clock', 'synthetic'],
        'script': [{'await': KILLED + '#1', 'then': 'kill'}],
        'expected': {'R1': 'unknown-attempt-open', 'R2': 'Committed'},
    }]
    # The repeated object point is killed at its first, middle and last occurrence.
    for k in (1, 3, 5):
        rows.append({
            'case': 'F02', 'variant': f'torn-object-{k}', 'units': ['X3c'],
            'labels': ['injected', 'process-death', 'scripted-clock', 'synthetic'],
            'script': [{'arm': f'{REPEATED}#{k}=torn'}, {'await': f'{REPEATED}#{k}', 'then': 'kill'}],
            'expected': {'R1': 'unknown-attempt-open'},
        })
    rows.append({
        'case': 'F09', 'variant': 'fail-after-seal-commit', 'units': ['X3b'],
        'labels': ['injected', 'scripted-clock', 'synthetic'],
        'script': [{'arm': 'x3b.append.seal.commit.after#1=fail-after'}],
        'expected': {'outcome': 'CommitUndetermined'},
    })
    return rows


def host_row(point):
    """A host required run that kills at `point` (law X9 r10: the host's own
    required-runs file)."""
    return {
        'case': 'F32', 'variant': 'kill-' + point.replace('.', '-').replace('#', '-'), 'units': ['X3b-4', 'X7b'],
        'labels': ['process-death', 'scripted-clock', 'synthetic'],
        'script': [{'arm': f'{point}=hold'}, {'await': point, 'then': 'kill'}],
        'expected': {'scripted': 'killed'},
    }


def run_record(row, normalized='1' * 64, trace='2' * 64):
    row = copy.deepcopy(row)
    killed = [s['await'] for s in row['script'] if s.get('then') == 'kill']
    return {
        'schema': 'opensip.x9.run.v1', 'case': row['case'], 'variant': row['variant'], 'units': row['units'],
        'labels': row['labels'],
        'product': {'commit': COMMIT, 'worktreeClean': True, 'toolchain': 'rustc 1.95.0', 'profile': 'dev', 'features': ['crash-matrix']},
        'host': {'os': 'macOS 27.0', 'arch': 'arm64', 'filesystem': 'apfs', 'profileStanding': 'BASELINE-ATTESTED', 'fixture': 'synthetic-signed-v2'},
        'clock': {'epoch': EPOCH, 'script': 'x9-ordinal-3600'},
        'script': row['script'],
        'children': [{'role': 'commit', 'ordinal': 1, 'exit': {'signal': 9} if killed else {'code': 0}, 'lastHeld': killed[0] if killed else None,
                      'trace': {'records': 41, 'sha256': trace}, 'outcome': None}],
        'postState': {'raw': [{'path': 'ledger.sqlite', 'bytes': 4096, 'sha256': '3' * 64}], 'logical': {'ledger': {}}, 'normalizedSha256': normalized},
        'ladder': [{'step': 'R1-recover', 'standing': 'unknown-attempt-open', 'stateUnchanged': True}],
        'expected': row['expected'], 'verdict': 'PASS',
    }


def matrix_record(runs, scopes):
    return {
        'schema': 'opensip.x9.matrix.v1',
        'product': {'commit': COMMIT, 'worktreeClean': True},
        'runs': runs,
        'census': {'points': [
            {'name': KILLED, 'occurrences': 1, 'durability': True},
            {'name': REPEATED, 'occurrences': 5, 'durability': True},
            {'name': 'x6.recover.after-lease', 'occurrences': 1, 'durability': False},
        ], 'trace': {'records': 120, 'sha256': '4' * 64}},
        'killSet': [KILLED + '#1', REPEATED + '#1', REPEATED + '#3', REPEATED + '#5'],
        'releaseAbsence': {'binary': {'path': 'target/release/opensip', 'bytes': 1, 'sha256': '5' * 64}, 'profile': 'release', 'features': [],
                           'strings': ['OPENSIP_X9_', *sorted(scopes)], 'found': [], 'featureBuildRefused': True, 'passed': True},
        'limits': [{'id': f'L{n}', 'reason': 'recorded, not tested', 'owner': 'M6'} for n in range(1, 12)],
    }


class CrashMatrixCheckTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name).resolve()
        self.scopes = M.registry(REPOSITORY)
        self.rows = required_rows()
        self.required = self.root / 'required-runs.v1.json'
        self.required.write_bytes(canonical({'schema': 'opensip.x9.required-runs.v1', 'clockEpoch': EPOCH, 'runs': self.rows}))
        self.first = self.write_set('first', {})
        self.second = self.write_set('second', {})

    def write_set(self, name, runs_override, matrix_change=None):
        directory = self.root / name
        (directory / 'runs').mkdir(parents=True)
        listed = []
        for row in self.rows:
            record = runs_override.get((row['case'], row['variant']), run_record(row))
            path = f"runs/{row['case']}-{row['variant']}.json"
            raw = record if isinstance(record, bytes) else canonical(record)
            (directory / path).write_bytes(raw)
            listed.append({'path': path, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()})
        listed.sort(key=lambda e: e['path'])
        matrix = matrix_record(listed, self.scopes)
        if matrix_change:
            matrix_change(matrix)
        (directory / 'matrix.json').write_bytes(canonical(matrix))
        return directory

    def check(self, first=None, second=None):
        return M.check(REPOSITORY, first or self.first, second or self.second, self.required, COMMIT)

    def refuses(self, message, **kwargs):
        with self.assertRaises(M.MatrixError) as caught:
            self.check(**kwargs)
        self.assertIn(message, str(caught.exception))

    def test_registry_is_read_from_the_barrier_source(self):
        self.assertTrue(self.scopes['x3c.object'])
        self.assertFalse(self.scopes['x6.recover'])
        self.assertFalse(self.scopes['x4.observer'])
        self.assertEqual(len(self.scopes), 25)
        self.assertNotIn('x9.selftest', self.scopes)

    def test_a_complete_agreeing_pair_passes(self):
        result = self.check()
        self.assertEqual(result['runs'], 5)
        self.assertEqual(result['killSet'], 4)
        self.assertTrue(result['repetitionsAgree'])

    def test_kill_set_derivation_and_grammar(self):
        points = [{'name': 'a', 'occurrences': 1, 'durability': True}, {'name': 'b', 'occurrences': 2, 'durability': True},
                  {'name': 'c', 'occurrences': 4, 'durability': True}, {'name': 'd', 'occurrences': 9, 'durability': False}]
        self.assertEqual(M.kill_set(points), ['a#1', 'b#1', 'b#2', 'c#1', 'c#2', 'c#4'])
        for good in (KILLED, 'x3d.publish.commit-returned', 'x3c.evidence.stage-run_records', 'x3b.end.floor/directory-barrier.before'):
            self.assertTrue(M.point_valid(good, self.scopes), good)
        for bad in ('x3c.attempt', 'x9.selftest.step', 'x3c.object/fsync.before', 'x3c.object/write', 'X3c.attempt.commit', 'x3c..attempt.commit'):
            self.assertFalse(M.point_valid(bad, self.scopes), bad)

    def test_missing_and_extra_runs_refuse(self):
        rows = self.rows
        self.rows = rows[:-1]
        short = self.write_set('short', {})
        self.rows = rows
        self.refuses('missing runs', first=short)
        extra = self.write_set('extra', {})
        (extra / 'runs/F99-stray.json').write_bytes(b'{}')
        self.refuses('run files differ', first=extra)

    def test_each_run_field_corruption_refuses(self):
        target = (self.rows[0]['case'], self.rows[0]['variant'])
        cases = [
            ('verdict FAIL', lambda r: r.update(verdict='FAIL')),
            ('verdict HARNESS-ERROR', lambda r: r.update(verdict='HARNESS-ERROR')),
            ('labels differ', lambda r: r.update(labels=['process-death'])),
            ('labels differ', lambda r: r.update(labels=['process-death', 'synthetic'])),
            ("clock is not the run set's script", lambda r: r['clock'].update(epoch=EPOCH + 1)),
            ("clock is not the run set's script", lambda r: r['clock'].update(script='os')),
            ('keys differ', lambda r: r.pop('clock')),
            ('child ordinals', lambda r: r['children'].append(dict(r['children'][0]))),
            ('child ordinals', lambda r: r['children'][0].pop('ordinal')),
            ('expected differs', lambda r: r['expected'].update(R2='Refused')),
            ('script differs', lambda r: r.update(script=[{'await': KILLED + '#2', 'then': 'kill'}])),
            ('not the reviewed commit', lambda r: r['product'].update(commit='b' * 40)),
            ('dirty worktree', lambda r: r['product'].update(worktreeClean=False)),
            ('profile or features', lambda r: r['product'].update(features=[])),
            ('fixture labels', lambda r: r['host'].update(fixture='real')),
            ('not verified by signal 9', lambda r: r['children'][0].update(exit={'code': 0})),
            ('not verified by signal 9', lambda r: r['children'][0].update(lastHeld=KILLED + '#2')),
            ('keys differ', lambda r: r.update(extra=1)),
            ('postState', lambda r: r['postState'].update(normalizedSha256='x')),
        ]
        for n, (message, change) in enumerate(cases):
            record = run_record(self.rows[0])
            change(record)
            broken = self.write_set(f'run-{n}', {target: record})
            with self.subTest(message=message):
                self.refuses(message, first=broken)

    def test_injected_label_cannot_hide_a_kill_or_claim_one(self):
        row = self.rows[4]
        record = run_record(row)
        record['labels'] = ['process-death', 'scripted-clock', 'synthetic']
        self.refuses('labels differ', first=self.write_set('claimed', {(row['case'], row['variant']): record}))

    def test_noncanonical_float_and_duplicate_key_refuse(self):
        target = (self.rows[0]['case'], self.rows[0]['variant'])
        record = run_record(self.rows[0])
        pretty = json.dumps(record, sort_keys=True, indent=1).encode()
        self.refuses('noncanonical', first=self.write_set('pretty', {target: pretty}))
        floated = canonical(record).replace(b'"bytes":4096', b'"bytes":4096.0')
        self.refuses('float', first=self.write_set('float', {target: floated}))
        duplicated = canonical(record).replace(b'{"case":', b'{"case":"F07","case":', 1)
        self.refuses('duplicate key', first=self.write_set('dup', {target: duplicated}))

    def test_matrix_corruptions_refuse(self):
        cases = [
            ('run bytes differ', lambda m: m['runs'][0].update(sha256='0' * 64)),
            ('kill set differs', lambda m: m.update(killSet=m['killSet'][:-1])),
            ('census durability differs', lambda m: m['census']['points'][2].update(durability=True)),
            ('outside the registry', lambda m: m['census']['points'].append({'name': 'x9.selftest.step', 'occurrences': 1, 'durability': True})),
            ('release absence did not pass', lambda m: m['releaseAbsence'].update(found=['OPENSIP_X9_'])),
            ('release absence did not pass', lambda m: m['releaseAbsence'].update(featureBuildRefused=False)),
            ('release absence did not pass', lambda m: m['releaseAbsence'].update(strings=['OPENSIP_X9_'])),
            ('exactly L1..L11', lambda m: m.update(limits=m['limits'][:-1])),
            ('reviewed clean commit', lambda m: m['product'].update(worktreeClean=False)),
        ]
        for n, (message, change) in enumerate(cases):
            with self.subTest(message=message):
                self.refuses(message, first=self.write_set(f'matrix-{n}', {}, change))

    def test_a_new_census_durability_point_without_a_kill_refuses(self):
        def grow(matrix):
            matrix['census']['points'].insert(0, {'name': 'x3b.append.seal.insert.before', 'occurrences': 1, 'durability': True})
            matrix['killSet'] = M.kill_set(matrix['census']['points'])
        self.refuses('without a process-death run', first=self.write_set('uncovered', {}, grow))

    def test_repetitions_must_agree(self):
        target = (self.rows[0]['case'], self.rows[0]['variant'])
        normalized = self.write_set('normalized', {target: run_record(self.rows[0], normalized='9' * 64)})
        self.refuses('normalizedSha256', second=normalized)
        traced = self.write_set('traced', {target: run_record(self.rows[0], trace='8' * 64)})
        self.refuses('trace digest', second=traced)

    def test_required_runs_need_the_clock_and_its_label(self):
        rows = copy.deepcopy(self.rows)
        self.required.write_bytes(canonical({'schema': 'opensip.x9.required-runs.v1', 'runs': rows}))
        self.refuses('keys differ')
        rows[0]['labels'] = ['process-death', 'synthetic']
        self.required.write_bytes(canonical({'schema': 'opensip.x9.required-runs.v1', 'clockEpoch': EPOCH, 'runs': rows}))
        self.refuses('invalid required labels')

    # ------------------------------------------------ check-unit (X9 r4 item 7)

    def unit_set(self, name, change=None, matrix_change=None, rows=None):
        """A unit's run set: uncommitted (worktreeClean false) by default."""
        rows = rows or self.rows
        overrides = {}
        for row in rows:
            record = run_record(row)
            record['product']['worktreeClean'] = False
            if change:
                change(row, record)
            overrides[(row['case'], row['variant'])] = record

        def dirty(matrix):
            matrix['product']['worktreeClean'] = False
            if matrix_change:
                matrix_change(matrix)
        return self.write_set(name, overrides, dirty)

    def check_unit(self, first, second, unit='X9-2'):
        return M.check(REPOSITORY, first, second, self.required, COMMIT, unit)

    def test_check_unit_passes_an_uncommitted_unit_and_check_does_not(self):
        first, second = self.unit_set('unit-a'), self.unit_set('unit-b')
        result = self.check_unit(first, second)
        self.assertEqual((result['unit'], result['runs'], result['matrixPass']), ('X9-2', 5, False))
        self.assertTrue(result['repetitionsAgree'])
        self.refuses('not the reviewed clean commit', first=first, second=second)

    def test_check_unit_takes_only_its_cases_and_needs_no_full_coverage(self):
        other = {'case': 'F11', 'variant': 'kill-evidence-stage', 'units': ['X3c'],
                 'labels': ['process-death', 'scripted-clock', 'synthetic'],
                 'script': [{'await': 'x3c.evidence.stage-pins#1', 'then': 'kill'}], 'expected': {}}
        self.required.write_bytes(canonical({'schema': 'opensip.x9.required-runs.v1', 'clockEpoch': EPOCH,
                                             'runs': self.rows + [other]}))

        def grow(matrix):
            matrix['census']['points'].insert(0, {'name': 'x3b.append.seal.insert.before', 'occurrences': 1, 'durability': True})
            matrix['killSet'] = M.kill_set(matrix['census']['points'])
        first, second = self.unit_set('grown-a', matrix_change=grow), self.unit_set('grown-b', matrix_change=grow)
        self.assertEqual(self.check_unit(first, second)['runs'], 5)
        with self.assertRaises(M.MatrixError):
            self.check_unit(first, second, unit='X9-3')

    def test_check_unit_refuses_a_kill_outside_the_kill_set(self):
        def shrink(matrix):
            matrix['census']['points'] = [p for p in matrix['census']['points'] if p['name'] != KILLED]
            matrix['killSet'] = M.kill_set(matrix['census']['points'])
        first = self.unit_set('outside-a', matrix_change=shrink)
        with self.assertRaises(M.MatrixError) as caught:
            self.check_unit(first, self.unit_set('outside-b', matrix_change=shrink))
        self.assertIn('outside the kill set', str(caught.exception))

    def test_check_unit_keeps_the_per_run_check_and_the_repetition_agreement(self):
        def other_commit(row, record):
            record['product']['commit'] = 'b' * 40
        for change, message in ((other_commit, 'not the reviewed commit'),):
            with self.assertRaises(M.MatrixError) as caught:
                self.check_unit(self.unit_set('commit-a', change), self.unit_set('commit-b'))
            self.assertIn(message, str(caught.exception))

        def renormalized(row, record):
            record['postState']['normalizedSha256'] = '9' * 64
        with self.assertRaises(M.MatrixError) as caught:
            self.check_unit(self.unit_set('rep-a'), self.unit_set('rep-b', renormalized))
        self.assertIn('normalizedSha256', str(caught.exception))
        with self.assertRaises(M.MatrixError):
            self.check_unit(self.unit_set('unknown-a'), self.unit_set('unknown-b'), unit='X9-9')

    def test_a_row_with_a_unit_member_is_in_that_units_subset_only(self):
        # Law X9 r15: F14's moved kill row is X9-4's, although F14 is in
        # X9-3's case list; `check` admits the member and still needs its run.
        moved = {'case': 'F14', 'variant': 'kill-settle-before-after-latch', 'units': ['X3d', 'X6'],
                 'labels': ['process-death', 'scripted-clock', 'synthetic'],
                 'script': [{'await': KILLED + '#1', 'then': 'kill'}], 'expected': {}, 'unit': 'X9-4'}
        plain = {'case': 'F13', 'variant': 'kill-commit-returned', 'units': ['X3c', 'X3d'],
                 'labels': ['process-death', 'scripted-clock', 'synthetic'],
                 'script': [{'await': KILLED + '#1', 'then': 'kill'}], 'expected': {}}
        self.required.write_bytes(canonical({'schema': 'opensip.x9.required-runs.v1', 'clockEpoch': EPOCH,
                                             'runs': self.rows + [moved, plain]}))
        original = self.rows
        self.rows = [moved]
        x94 = self.check_unit(self.unit_set('x94-a'), self.unit_set('x94-b'), unit='X9-4')
        self.assertEqual(x94['runs'], 1)
        self.rows = [plain]
        x93 = self.check_unit(self.unit_set('x93-a'), self.unit_set('x93-b'), unit='X9-3')
        self.assertEqual(x93['runs'], 1)
        # X9-3's set with the moved row in it is an extra run.
        self.rows = [moved, plain]
        with self.assertRaises(M.MatrixError) as caught:
            self.check_unit(self.unit_set('x93-extra-a'), self.unit_set('x93-extra-b'), unit='X9-3')
        self.assertIn('extra run', str(caught.exception))
        # `check` takes every row, the moved one included.
        self.rows = original + [moved, plain]
        first, second = self.write_set('all-a', {}), self.write_set('all-b', {})
        self.assertEqual(self.check(first, second)['runs'], len(self.rows))
        self.rows = original + [plain]
        self.refuses('missing runs', first=self.write_set('short-a', {}), second=self.write_set('short-b', {}))
        self.rows = original
        for unit in ('X9-9', 4):
            bad = dict(moved, unit=unit)
            self.required.write_bytes(canonical({'schema': 'opensip.x9.required-runs.v1', 'clockEpoch': EPOCH,
                                                 'runs': self.rows + [bad]}))
            self.refuses('invalid required unit')

    def test_an_x9_6_row_is_in_no_units_subset_and_check_needs_it(self):
        # Law X9 r16: the coverage rows carry "unit": "X9-6".
        cover = {'case': 'F11', 'variant': 'kill-x4-checkpoint-before-admit-2', 'units': ['X3c', 'X3d'],
                 'labels': ['process-death', 'scripted-clock', 'synthetic'],
                 'script': [{'await': KILLED + '#1', 'then': 'kill'}], 'expected': {}, 'unit': 'X9-6'}
        self.required.write_bytes(canonical({'schema': 'opensip.x9.required-runs.v1', 'clockEpoch': EPOCH,
                                             'runs': self.rows + [cover]}))
        for unit in M.UNIT_CASES:
            self.assertFalse(M.in_unit(('F11', cover['variant']), cover, unit))
        # X9-2's sets need no X9-6 row (its case F11 is X9-3's, and the
        # member takes it out of every subset); a set with it holds an extra run.
        self.assertEqual(self.check_unit(self.unit_set('x92-a'), self.unit_set('x92-b'))['runs'], 5)
        original = self.rows
        self.rows = original + [cover]
        with self.assertRaises(M.MatrixError) as caught:
            self.check_unit(self.unit_set('x92-extra-a'), self.unit_set('x92-extra-b'))
        self.assertIn('extra run', str(caught.exception))
        # `check` needs it.
        self.assertEqual(self.check(self.write_set('all-a', {}), self.write_set('all-b', {}))['runs'], 6)
        self.rows = original
        self.refuses('missing runs')
        with self.assertRaises(SystemExit):
            # check-unit admits no X9-6.
            import contextlib, io, sys as _sys
            argv = _sys.argv
            _sys.argv = ['check_crash_matrix.py', 'check-unit', '--repository', str(REPOSITORY), '--unit', 'X9-6',
                         '--run-set', '.', '--repeat', '.', '--required', str(self.required), '--commit', COMMIT]
            try:
                with contextlib.redirect_stderr(io.StringIO()):
                    M.main()
            finally:
                _sys.argv = argv

    def test_an_x3c_3_row_is_in_no_units_subset_and_check_needs_it(self):
        # Law X9 r17 frame rule 3 and LD-RC-3: X3c-3's RC rows carry
        # "unit": "X3c-3", read as r16 reads "X9-6".
        rc = {'case': 'F04', 'variant': 'recommit-kill-x3c-object-reopen-confirm-before-1', 'units': ['X3c'],
              'labels': ['process-death', 'scripted-clock', 'synthetic'],
              'script': [{'await': KILLED + '#1', 'then': 'kill'}], 'expected': {}, 'unit': 'X3c-3'}
        self.assertIn('X3c-3', M.UNIT_VALUES)
        self.required.write_bytes(canonical({'schema': 'opensip.x9.required-runs.v1', 'clockEpoch': EPOCH,
                                             'runs': self.rows + [rc]}))
        for unit in M.UNIT_CASES:
            self.assertFalse(M.in_unit(('F04', rc['variant']), rc, unit))
        # X9-2's sets need no X3c-3 row, though F04 is X9-2's case; a set
        # with it holds an extra run.
        self.assertEqual(self.check_unit(self.unit_set('x92-a'), self.unit_set('x92-b'))['runs'], 5)
        original = self.rows
        self.rows = original + [rc]
        with self.assertRaises(M.MatrixError) as caught:
            self.check_unit(self.unit_set('x92-extra-a'), self.unit_set('x92-extra-b'))
        self.assertIn('extra run', str(caught.exception))
        # `check` needs it.
        self.assertEqual(self.check(self.write_set('all-a', {}), self.write_set('all-b', {}))['runs'], 6)
        self.rows = original
        self.refuses('missing runs')
        # check-unit admits no X3c-3.
        self.assertNotIn('X3c-3', M.UNIT_CASES)
        with self.assertRaises(SystemExit):
            import contextlib, io, sys as _sys
            argv = _sys.argv
            _sys.argv = ['check_crash_matrix.py', 'check-unit', '--repository', str(REPOSITORY), '--unit', 'X3c-3',
                         '--run-set', '.', '--repeat', '.', '--required', str(self.required), '--commit', COMMIT]
            try:
                with contextlib.redirect_stderr(io.StringIO()):
                    M.main()
            finally:
                _sys.argv = argv

    def test_j3b_and_j3d_rows_require_whole_check_and_never_check_unit(self):
        for unit in ('J3b', 'J3d'):
            original = self.rows
            row = {'case': 'F04', 'variant': 'signal-row-control', 'units': ['J1'],
                   'labels': ['scripted-clock', 'synthetic'], 'script': [], 'expected': {}, 'unit': unit}
            self.assertIn(unit, M.UNIT_VALUES)
            self.assertNotIn(unit, M.UNIT_CASES)
            self.required.write_bytes(canonical({'schema': 'opensip.x9.required-runs.v1', 'clockEpoch': EPOCH,
                                                 'runs': original + [row]}))
            for old_unit in M.UNIT_CASES:
                self.assertFalse(M.in_unit(('F04', row['variant']), row, old_unit))
            self.assertEqual(self.check_unit(self.unit_set(unit + '-subset-a'), self.unit_set(unit + '-subset-b'))['runs'], 5)
            self.refuses('missing runs')
            self.rows = original + [row]
            self.assertEqual(self.check(self.write_set(unit + '-whole-a', {}), self.write_set(unit + '-whole-b', {}))['runs'], 6)
            self.rows = original
            import contextlib, io, sys as _sys
            argv = _sys.argv
            _sys.argv = ['check_crash_matrix.py', 'check-unit', '--repository', str(REPOSITORY), '--unit', unit,
                         '--run-set', '.', '--repeat', '.', '--required', str(self.required), '--commit', COMMIT]
            try:
                with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
                    M.main()
            finally:
                _sys.argv = argv

    def test_the_timing_guard_is_required_where_the_tick_is_armed_and_bounded(self):
        # Law X9 r12 and r13: item 11's timing guard (5,000 ms).
        armed = {'case': 'F44', 'variant': 'reader-at-rev', 'units': ['X6'], 'labels': ['scripted-clock', 'synthetic'],
                 'script': [{'spawn': 'commit', 'name': 'writer', 'arm': 'x4.observer.tick#*=hold,x3c.evidence.commit.before#1=hold'}],
                 'expected': {}}
        original = self.rows
        self.rows = [armed]
        self.required.write_bytes(canonical({'schema': 'opensip.x9.required-runs.v1', 'clockEpoch': EPOCH, 'runs': original + [armed]}))

        def guarded(ms):
            def change(row, record):
                if row['case'] == 'F44':
                    record['children'][0]['exit'] = {'code': 0}
                    record['children'][0]['lastHeld'] = None
                    if ms is not None:
                        record['timingGuard'] = {'monotonicMs': ms, 'limitMs': 5000}
            return change
        result = self.check_unit(self.unit_set('guard-a', guarded(17)), self.unit_set('guard-b', guarded(4999)), unit='X9-3')
        self.assertEqual(result['runs'], 1)
        for ms, message in ((None, 'timingGuard'), (5001, 'over its limit')):
            with self.assertRaises(M.MatrixError) as caught:
                self.check_unit(self.unit_set(f'bad-{ms}-a', guarded(ms)), self.unit_set(f'bad-{ms}-b', guarded(17)), unit='X9-3')
            self.assertIn(message, str(caught.exception))

        self.rows = original

        def stray(row, record):
            record['timingGuard'] = {'monotonicMs': 1, 'limitMs': 5000}
        with self.assertRaises(M.MatrixError) as caught:
            self.check_unit(self.unit_set('stray-a', stray), self.unit_set('stray-b'))
        self.assertIn('arms no observer tick', str(caught.exception))

    def test_release_absence_scan(self):
        clean = self.root / 'clean.bin'
        clean.write_bytes(b'\x00binary without barrier strings\x00')
        result = M.release_absence(REPOSITORY, clean)
        self.assertTrue(result['passed'])
        self.assertEqual(result['found'], [])
        self.assertIn('x3d.session', result['strings'])
        for needle in (b'OPENSIP_X9_ARMS', b'x3d.publish'):
            dirty = self.root / 'dirty.bin'
            dirty.write_bytes(b'\x00' + needle + b'\x00')
            self.assertFalse(M.release_absence(REPOSITORY, dirty)['passed'], needle)

    # ----------------------------------- the two-target gate (X9 r10, X9-6)

    def host_target(self, name, census_points, rows, epoch=EPOCH):
        """A host target: its own required runs and one run set whose census
        is `census_points`."""
        original = self.rows
        self.rows = rows
        required = self.root / f'{name}-required.json'
        required.write_bytes(canonical({'schema': 'opensip.x9.required-runs.v1', 'clockEpoch': epoch, 'runs': rows}))

        def census(matrix):
            matrix['census']['points'] = census_points
            matrix['killSet'] = M.kill_set(census_points)
        first, second = self.write_set(name + '-a', {}, census), self.write_set(name + '-b', {}, census)
        self.rows = original
        return ('host', required, first, second)

    def storage_target(self):
        return ('storage', self.required, self.first, self.second)

    def two(self, host):
        return M.check_targets(REPOSITORY, [self.storage_target(), host], COMMIT)

    def two_refuses(self, message, host):
        with self.assertRaises(M.MatrixError) as caught:
            self.two(host)
        self.assertIn(message, str(caught.exception))

    def test_the_two_target_gate_covers_the_union_kill_set_from_either_target(self):
        # The host kills its own point; the storage kill of KILLED covers the
        # host census's KILLED too. Neither target alone kills the other's.
        host = self.host_target('host', [
            {'name': KILLED, 'occurrences': 1, 'durability': True},
            {'name': HOST_POINT, 'occurrences': 1, 'durability': True},
        ], [host_row(HOST_POINT + '#1')])
        result = self.two(host)
        self.assertTrue(result['matrixPass'])
        self.assertFalse(result['productQualification'])
        self.assertEqual((result['runs'], result['unionCensusPoints'], result['killSet'], result['killedPoints']), (6, 4, 5, 5))
        self.assertEqual(sorted(result['targets']), ['host', 'storage'])
        self.assertEqual(result['killedOutsideKillSet'], [])
        # Storage alone is not a matrix pass, though its own kill set is covered.
        alone = M.check_targets(REPOSITORY, [self.storage_target()], COMMIT)
        self.assertFalse(alone['matrixPass'])

    def test_a_union_kill_set_point_no_target_kills_refuses(self):
        host = self.host_target('host-uncovered', [
            {'name': HOST_POINT, 'occurrences': 1, 'durability': True},
            {'name': 'x7.delivery.required.before', 'occurrences': 1, 'durability': True},
        ], [host_row(HOST_POINT + '#1')])
        self.two_refuses('union kill-set points without a process-death run: x7.delivery.required.before#1', host)

    def test_a_larger_occurrence_count_in_the_other_target_moves_the_union_kill_set(self):
        # The host census reaches the repeated object point 7 times: the
        # union's middle and last occurrences are #4 and #7, which storage's
        # kills at #3 and #5 do not cover.
        host = self.host_target('host-occurrences', [
            {'name': HOST_POINT, 'occurrences': 1, 'durability': True},
            {'name': REPEATED, 'occurrences': 7, 'durability': True},
        ], [host_row(HOST_POINT + '#1')])
        self.two_refuses(REPEATED + '#4, ' + REPEATED + '#7', host)

    def test_the_two_targets_share_one_clock_epoch_and_a_name_each(self):
        host = self.host_target('host-epoch', [{'name': HOST_POINT, 'occurrences': 1, 'durability': True}],
                                [host_row(HOST_POINT + '#1')], epoch=EPOCH + 1)
        with self.assertRaises(M.MatrixError) as caught:
            M.check_targets(REPOSITORY, [self.storage_target(), host], COMMIT)
        self.assertIn('clock', str(caught.exception))
        with self.assertRaises(M.MatrixError) as caught:
            M.check_targets(REPOSITORY, [self.storage_target(), self.storage_target()], COMMIT)
        self.assertIn('named once', str(caught.exception))

    def test_each_target_keeps_the_per_run_check_and_the_repetition_agreement(self):
        rows = [host_row(HOST_POINT + '#1')]
        points = [{'name': HOST_POINT, 'occurrences': 1, 'durability': True}]
        name, required, first, _ = self.host_target('host-rep', points, rows)
        original = self.rows
        self.rows = rows
        target = (rows[0]['case'], rows[0]['variant'])

        def census(matrix):
            matrix['census']['points'] = points
            matrix['killSet'] = M.kill_set(points)
        other = self.write_set('host-rep-other', {target: run_record(rows[0], normalized='9' * 64)}, census)
        dirty_record = run_record(rows[0])
        dirty_record['product']['worktreeClean'] = False
        dirty = self.write_set('host-rep-dirty', {target: dirty_record}, census)
        self.rows = original
        self.two_refuses('host: ' + '-'.join(target) + ': repetitions disagree on normalizedSha256', (name, required, first, other))
        self.two_refuses('host: ' + '-'.join(target) + ': dirty worktree', (name, required, first, dirty))

    def test_the_command_line_gate_needs_both_targets(self):
        command = [sys.executable, str(FILE), 'check', '--repository', str(REPOSITORY), '--commit', COMMIT,
                   '--target', 'storage', str(self.required), str(self.first), str(self.second)]
        out = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(out.returncode, 1)
        self.assertIn('exactly the targets host and storage', out.stderr)
        _, required, first, second = self.host_target('host-cli', [
            {'name': KILLED, 'occurrences': 1, 'durability': True},
            {'name': HOST_POINT, 'occurrences': 1, 'durability': True},
        ], [host_row(HOST_POINT + '#1')])
        out = subprocess.run(command + ['--target', 'host', str(required), str(first), str(second)], capture_output=True, text=True)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertTrue(json.loads(out.stdout)['matrixPass'])

    def test_coverage_reports_the_uncovered_union_points_before_any_run(self):
        storage_census = self.root / 'storage-census.json'
        storage_census.write_bytes(canonical(matrix_record([], self.scopes)['census']))
        host_required = self.root / 'host-coverage-required.json'
        host_required.write_bytes(canonical({'schema': 'opensip.x9.required-runs.v1', 'clockEpoch': EPOCH,
                                             'runs': [host_row(HOST_POINT + '#1')]}))
        host_census = self.root / 'host-census.json'
        host_census.write_bytes(canonical({'points': [
            {'name': HOST_POINT, 'occurrences': 1, 'durability': True},
            {'name': 'x4.checkpoint.before-observation', 'occurrences': 3, 'durability': True},
        ], 'trace': {'records': 1, 'sha256': '4' * 64}}))
        result = M.coverage(REPOSITORY, [('storage', storage_census, self.required), ('host', host_census, host_required)])
        self.assertFalse(result['passed'])
        self.assertEqual(result['uncovered'], ['x4.checkpoint.before-observation#1', 'x4.checkpoint.before-observation#2',
                                               'x4.checkpoint.before-observation#3'])
        self.assertEqual(result['killSet'], 8)
        self.assertFalse(result['matrixPass'])
        # A storage matrix.json carries its census too.
        host_census.write_bytes(canonical({'points': [{'name': HOST_POINT, 'occurrences': 1, 'durability': True}],
                                           'trace': {'records': 1, 'sha256': '4' * 64}}))
        result = M.coverage(REPOSITORY, [('storage', self.first / 'matrix.json', self.required), ('host', host_census, host_required)])
        self.assertTrue(result['passed'])
        self.assertEqual(result['uncovered'], [])


if __name__ == '__main__':
    unittest.main()
