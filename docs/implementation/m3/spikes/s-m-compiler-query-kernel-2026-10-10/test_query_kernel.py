"""Small actual controls, outside product and outside complete S-M figures."""
import ast
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, '/Users/sb/code/opensip-ai/opensip/tools/quality')
sys.path.insert(0, str(HERE))
from query_kernel import HEAD, TAIL, Query, file_pin, run_query
from selected_projection import rustflags_projection

RUSTC = Path('/Users/sb/code/.opensip-implementation-cache/g2-rust-1.95/sysroot/bin/rustc')
RUSTC_PIN = {'bytes': 412504, 'sha256': 'b829b733131d4e1673eeebd1f34d06ae1e9ff4977b051313cf42e2a9e79ecf1c'}
NATIVE_TMP = Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T')
ROOT = Path(tempfile.mkdtemp(prefix='opensip-sm-query-controls-', dir=NATIVE_TMP))
ROOT.chmod(0o700)
OBSERVATIONS = []


class QueryControls(unittest.TestCase):
    def run_control(self, query, *, executable=RUSTC, expected_pin=RUSTC_PIN):
        n = len(OBSERVATIONS)
        result = run_query(query, executable=executable, expected_pin=expected_pin,
                           attempt_label='experimental-small-controls', cwd=ROOT,
                           output_directory=ROOT, ordinal=n,
                           experimental_targets=('aarch64-apple-darwin',),
                           timeout_nanos=30_000_000_000)
        OBSERVATIONS.append(result)
        self.assertFalse(result['retry'])
        self.assertFalse(result['cacheReuse'])
        self.assertFalse(result['nativeAdmission'])
        self.assertFalse(result['SMComplete'])
        return result

    def test_actual_empty_environment_cwd_stdin_and_closed_extra_fd(self):
        probe = HERE / 'probe'
        fd = os.open(ROOT / 'sentinel', os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        os.set_inheritable(fd, True)
        try:
            q = Query('host-info', original_flags=(f'--cfg=probe_fd_{fd}',))
            r = self.run_control(q, executable=probe, expected_pin=file_pin(probe))
        finally:
            os.close(fd)
        self.assertEqual(r['rootObservation']['returncode'], 0)
        out = Path(r['stdout']['path']).read_text()
        self.assertIn('ENV_COUNT=0\n', out)
        actual_cwd = Path(next(line[4:] for line in out.splitlines() if line.startswith('CWD=')))
        self.assertTrue(actual_cwd.samefile(ROOT))
        self.assertIn('STDIN_BYTES=0\n', out)
        self.assertIn('EXTRA_FD_RESULT=-1\n', out)
        actual_args = json.loads(next(line[5:] for line in out.splitlines() if line.startswith('ARGS=')))
        self.assertEqual(actual_args, r['argv'][1:])

    def test_actual_version_probe_and_no_stdout_identity_mint(self):
        r = self.run_control(Query('version'))
        self.assertEqual(r['argv'][1:], ['-vV'])
        self.assertEqual(r['rootObservation']['returncode'], 0)
        out = Path(r['stdout']['path']).read_text()
        self.assertIn('host: aarch64-apple-darwin', out)
        self.assertNotIn('semanticVersion', r)
        self.assertNotIn('baseCfg', r)

    def test_actual_host_info_with_projection(self):
        q = Query('host-info', original_flags=('--cfg=experimental_marker', '-C', 'opt-level=1', '@ambient', '--sysroot', '/ambient'))
        r = self.run_control(q)
        self.assertEqual(r['rootObservation']['returncode'], 0)
        self.assertEqual(r['argv'][1:], list(HEAD + ('--cfg=experimental_marker', '-C', 'opt-level=1') + TAIL))
        self.assertIn('experimental_marker\n', Path(r['stdout']['path']).read_text())
        self.assertEqual(len(r['projection']['stripped']), 3)

    def test_actual_requested_target_and_fresh_repeat(self):
        q = Query('target-info', target='aarch64-apple-darwin')
        a = self.run_control(q)
        b = self.run_control(q)
        self.assertEqual(a['argv'][1:], list(HEAD + ('--target', q.target) + TAIL))
        self.assertEqual(a['rootObservation']['returncode'], 0)
        self.assertEqual(b['rootObservation']['returncode'], 0)
        self.assertNotEqual(a['stdout']['path'], b['stdout']['path'])
        self.assertEqual(a['stdout']['sha256'], b['stdout']['sha256'])
        for r in (a, b):
            with self.assertRaises(ChildProcessError):
                os.waitpid(r['rootObservation']['pid'], os.WNOHANG)

    def test_actual_compiler_refusal_keeps_outputs_no_retry(self):
        # The selected reference honors this joined spelling unconditionally.
        # Its invalid value belongs to the compiler; do not silently narrow it.
        r = self.run_control(Query('host-info', original_flags=('--cap-lints=invalid',)))
        self.assertNotEqual(r['rootObservation']['returncode'], 0)
        self.assertGreater(r['stderr']['bytes'], 0)
        self.assertEqual(r['projection']['honored'], ['--cap-lints=invalid'])
        self.assertNotIn('missingInput', r)

    def test_non_information_commands_and_json_targets_refused_before_outputs(self):
        queries = [Query('compile'), Query('lazy-crate-type'), Query('target-spec-json'),
                   Query('version', original_flags=('--sysroot', '/tmp')),
                   Query('host-info', target='aarch64-apple-darwin'),
                   Query('target-info', target='custom.json'),
                   Query('target-info', target='/tmp/custom.json'),
                   Query('target-info', target='unknown-target')]
        before = sorted(p.name for p in ROOT.iterdir())
        for q in queries:
            with self.assertRaises(ValueError):
                self.run_control(q)
        self.assertEqual(before, sorted(p.name for p in ROOT.iterdir()))

    def test_mismatched_executable_pin_and_symlink_refused_before_outputs(self):
        before = sorted(p.name for p in ROOT.iterdir())
        with self.assertRaises(ValueError):
            self.run_control(Query('version'), expected_pin={'bytes': RUSTC_PIN['bytes'], 'sha256': '0' * 64})
        self.assertEqual(before, sorted(p.name for p in ROOT.iterdir()))
        alias = ROOT / 'compiler-alias'
        alias.symlink_to(RUSTC)
        with self.assertRaises(OSError):
            self.run_control(Query('version'), executable=alias)

    def test_exact_selected_projection_source_and_edge_cases(self):
        p = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/native/native_evidence_model.v2.py')
        tree = ast.parse(p.read_text())
        target = ast.parse((HERE / 'selected_projection.py').read_text())
        selected_names = {'_CFG_RE', '_LINT_RE', '_ALLOWED_C', '_ALLOWED_C_VALUES', 'rustflags_projection'}
        def selected(t):
            return [ast.dump(n, include_attributes=False) for n in t.body if
                    (isinstance(n, ast.FunctionDef) and n.name in selected_names) or
                    (isinstance(n, ast.Assign) and any(isinstance(x, ast.Name) and x.id in selected_names for x in n.targets))]
        self.assertEqual(selected(tree), selected(target))
        projection = rustflags_projection(['-C', 'linker=evil', '-Cllvm-args=evil', '@response', '--cfg', 'a',
                                          '-Dwarnings', '--remap-path-prefix=/owned=/virtual',
                                          '--remap-path-prefix=/foreign=/virtual', '--cfg'], {'/owned'}, set())
        self.assertEqual(projection['honored'], ['--cfg', 'a', '-Dwarnings', '--remap-path-prefix=/owned=/virtual'])
        self.assertEqual(len(projection['stripped']), 5)
        self.assertEqual(projection['stripped'][-1]['reason'], 'dangling')

    def test_no_output_overwrite(self):
        n = len(OBSERVATIONS)
        p = ROOT / f'query-{n}.stdout'
        p.write_bytes(b'original retained bytes')
        with self.assertRaises(FileExistsError):
            self.run_control(Query('version'))
        self.assertEqual(p.read_bytes(), b'original retained bytes')


if __name__ == '__main__':
    original_home = os.environ.get('HOME')
    os.setpriority(os.PRIO_PROCESS, 0, 10)
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(QueryControls)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    assert os.environ.get('HOME') == original_home
    assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
    (HERE / 'controls.json').write_text(json.dumps({'testsRun': result.testsRun,
        'failures': len(result.failures), 'errors': len(result.errors),
        'passed': result.wasSuccessful(), 'actualQueries': OBSERVATIONS,
        'retainedPrivateTMPDIR': str(ROOT), 'niceness': os.getpriority(os.PRIO_PROCESS, 0),
        'HOMEUnchanged': True, 'fullSM': False, 'nativeAdmission': False}, indent=2) + '\n')
    sys.exit(0 if result.wasSuccessful() else 1)
