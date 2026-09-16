"""Full adapter refusal/write behavior with explicit test-only child stubs.

Fixtures rebind synthetic build receipts; these are not build attestations.
Real generator/schema algorithms are exercised by separate frozen-unit evidence.
"""
import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

REAL_RUN = subprocess.run

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('generation_execution', ROOT / 'tools/generate_contracts.py')
G = importlib.util.module_from_spec(spec); spec.loader.exec_module(G)


def pin(raw):
    return {'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}


class ExecutionTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(); self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        shutil.copytree(ROOT / 'schemas', self.root / 'schemas')
        self.closure = json.loads((ROOT / 'tools/contracts/generator-closure.json').read_text())
        for row in self.closure['files']:
            target = self.root / row['path']; target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / row['path'], target)
        shutil.copyfile(ROOT / 'tools/contracts/options.json', self.root / 'tools/contracts/options.json')
        self.registry = json.loads((self.root / 'schemas/registry.json').read_text())
        self.paths = [row['path'] for row in self.registry['recipes'][0]['outputs']]
        for relative in self.paths:
            path = self.root / relative; path.parent.mkdir(parents=True, exist_ok=True); path.write_text('original\n')
        package = self.root / 'tools/contracts/node_modules/typescript'; package.mkdir(parents=True)
        (package / 'package.json').write_text('{"name":"typescript","version":"6.0.3"}\n')
        raw = (package / 'package.json').read_bytes()
        self.closure['typescriptPackageFiles'] = [{'path': 'package.json', **pin(raw)}]
        self.generator = self.root / 'generator-stub'; self.node = self.root / 'node-stub'
        self.generator.write_text('#!/bin/sh\nexit 0\n'); self.node.write_text('#!/bin/sh\nexit 0\n')
        self.generator.chmod(0o700); self.node.chmod(0o700)
        self.closure['toolchain'] = {'generator': pin(self.generator.read_bytes()), 'node': pin(self.node.read_bytes()), 'python': pin(Path(sys.executable).read_bytes())}
        self.seal()

    def seal(self):
        self.closure['toolchain']['generator'] = pin(self.generator.read_bytes())
        self.closure['toolchain']['node'] = pin(self.node.read_bytes())
        receipt_path = self.root / 'tools/contracts/build-receipt.json'
        receipt = json.loads(receipt_path.read_text()); receipt['executable'] = self.closure['toolchain']['generator']
        receipt['standing'] = 'synthetic test fixture; never a build attestation'
        receipt_path.write_text(json.dumps(receipt))
        for row in self.closure['files']: row.update(pin((self.root / row['path']).read_bytes()))
        path = self.root / 'tools/contracts/generator-closure.json'; path.write_text(json.dumps(self.closure))
        self.registry['recipes'][0]['generatorClosureSha256'] = pin(path.read_bytes())['sha256']
        (self.root / 'schemas/registry.json').write_text(json.dumps(self.registry))

    def run_generation(self, write=False):
        output = io.StringIO()
        # Adapter-output tests use shell stubs. Sandbox effects have separate
        # real native/Node positive and denial controls, never these stubs.
        def stub_run(command, **kwargs):
            self.assertEqual(command[:2], ['/usr/bin/sandbox-exec', '-f'])
            return REAL_RUN(command[3:], **kwargs)
        with contextlib.redirect_stdout(output), mock.patch.object(G.subprocess, 'run', side_effect=stub_run):
            G.generate(self.root, generator=str(self.generator), node=str(self.node), write=write)
        return json.loads(output.getvalue())

    def assert_original(self):
        for relative in self.paths: self.assertEqual((self.root / relative).read_text(), 'original\n')

    def emit(self, extra=False):
        lines = ['#!/bin/sh']
        for relative in self.paths + (['extra.txt'] if extra else []):
            lines += ['mkdir -p "$2/' + str(Path(relative).parent) + '"', 'printf "stub\\n" > "$2/' + relative + '"']
        self.generator.write_text('\n'.join(lines) + '\n'); self.seal()

    def test_child_failure_does_not_publish(self):
        self.node.write_text('#!/bin/sh\necho child-noise\necho deliberate-failure >&2\nexit 7\n'); self.seal()
        with self.assertRaisesRegex(G.GenerationError, 'child failed: deliberate-failure'): self.run_generation(write=True)
        self.assert_original()

    def test_missing_and_extra_outputs_do_not_publish(self):
        with self.assertRaisesRegex(G.GenerationError, 'different output set'): self.run_generation(write=True)
        self.emit(extra=True)
        with self.assertRaisesRegex(G.GenerationError, 'undeclared, linked'): self.run_generation(write=True)
        self.assert_original()

    def test_executable_and_closure_changes_refuse(self):
        self.node.write_text('#!/bin/sh\nexit 3\n')
        with self.assertRaisesRegex(G.GenerationError, 'executable differs'): self.run_generation(write=True)
        self.assert_original()
        self.seal(); (self.root / 'tools/contracts/prepare.py').write_text('unexpected')
        with self.assertRaisesRegex(G.GenerationError, 'digest mismatch'): self.run_generation(write=True)
        self.assert_original()

    def test_prepared_owners_cannot_override_parent_options(self):
        source = self.root / 'tools/contracts/prepare.py'
        text = source.read_text()
        old = "json.dumps(options['owners'], indent=2)"
        self.assertEqual(text.count(old), 1)
        source.write_text(text.replace(old, "json.dumps([], indent=2)"))
        self.seal()
        with self.assertRaisesRegex(G.GenerationError, 'prepared owner mapping differs'):
            self.run_generation(write=True)
        self.assert_original()

    def test_materialized_package_change_refuses(self):
        (self.root / 'tools/contracts/node_modules/typescript/package.json').write_text('{}')
        with self.assertRaisesRegex(ValueError, 'TypeScript'): self.run_generation(write=True)
        self.assert_original()

    def test_drift_then_write_then_clean_with_one_summary(self):
        self.emit()
        with self.assertRaisesRegex(G.GenerationError, 'output drift'): self.run_generation()
        self.assert_original()
        written = self.run_generation(write=True)
        self.assertEqual(written['outputs'], 8); self.assertEqual(len(written['changed']), 8)
        clean = self.run_generation(); self.assertEqual(clean['changed'], [])

    def test_undeclared_checked_in_output_refuses_before_write(self):
        self.emit(); (self.root / 'apps/report/src/generated/extra.ts').write_text('unexpected')
        with self.assertRaisesRegex(G.GenerationError, 'undeclared checked-in'): self.run_generation(write=True)
        self.assert_original()

    def test_symlink_destination_refuses_before_any_write(self):
        self.emit(); relative = self.paths[-1]; path = self.root / relative
        outside = self.root / 'outside'; outside.write_text('preserved'); path.unlink(); path.symlink_to(outside)
        with self.assertRaisesRegex(G.GenerationError, 'symlink in generation'): self.run_generation(write=True)
        self.assertEqual(outside.read_text(), 'preserved')
        for name in self.paths[:-1]: self.assertEqual((self.root / name).read_text(), 'original\n')

    def test_collector_refuses_child_links_and_special_files(self):
        outside = self.root / 'outside-secret'; outside.write_bytes(b'not generator output')
        output = self.root / 'child-output'; output.mkdir()
        target = output / 'result.rs'
        for kind in ('symlink', 'hardlink', 'fifo'):
            if kind == 'symlink': target.symlink_to(outside)
            elif kind == 'hardlink': os.link(outside, target)
            else: os.mkfifo(target)
            with self.subTest(kind=kind), self.assertRaisesRegex(G.GenerationError, 'linked or nonregular'):
                G.collect_outputs(output, {'result.rs'})
            target.unlink()
        self.assertEqual(outside.read_bytes(), b'not generator output')

    def test_collector_refuses_directory_link_and_total_bytes(self):
        output = self.root / 'child-output'; output.mkdir()
        outside = self.root / 'outside-directory'; outside.mkdir(); (outside / 'result.rs').write_bytes(b'12345')
        (output / 'generated').symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(G.GenerationError, 'linked or nonregular'):
            G.collect_outputs(output, {'generated/result.rs'})
        (output / 'generated').unlink(); (output / 'result.rs').write_bytes(b'12345')
        with self.assertRaisesRegex(G.GenerationError, 'byte limit'):
            G.collect_outputs(output, {'result.rs'}, max_bytes=4)
        self.assertEqual(G.collect_outputs(output, {'result.rs'}, max_bytes=5), {'result.rs': b'12345'})


class DirectoryCustodyTests(unittest.TestCase):
    def test_replaced_or_linked_root_refuses_before_profile_construction(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp).resolve()
            root = base / 'output'; root.mkdir()
            roots = {root: G.directory_identity(root)}
            G.verify_directory_roots(roots)
            # Keep the original inode alive, so an allocator cannot recycle it.
            root.rename(base / 'original')
            root.mkdir()
            with self.assertRaisesRegex(G.GenerationError, 'directory was replaced'):
                G.verify_directory_roots(roots)
            root.rmdir(); root.symlink_to(base / 'original', target_is_directory=True)
            with self.assertRaisesRegex(G.GenerationError, 'parent-created directory'):
                G.verify_directory_roots(roots)

    @unittest.skipUnless(sys.platform == 'darwin' and Path('/usr/bin/sandbox-exec').is_file(), 'requires the actual macOS sandbox')
    def test_real_sandbox_denies_output_root_replacement(self):
        compiler = shutil.which('cc')
        if compiler is None:
            self.skipTest('native C compiler required for real sandbox syscall probe')
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp).resolve()
            source = base / 'probe.c'
            source.write_text('#include <unistd.h>\n#include <stdio.h>\nint main(int n,char**v){if(n!=3)return 2;int a=rmdir(v[1]);int b=symlink(v[2],v[1]);printf("%d %d\\n",a,b);return 0;}\n')
            executable = base / 'probe'
            build = REAL_RUN([compiler, str(source), '-o', str(executable)], capture_output=True, text=True)
            self.assertEqual(build.returncode, 0, build.stderr)
            output = base / 'output'; output.mkdir()
            victim = base / 'victim'; victim.mkdir()
            (victim / 'canary').write_bytes(b'outside original')
            roots = {output: G.directory_identity(output)}
            profile = base / 'profile.sb'
            profile.write_text(G.child_profile(executable, [], [output]))
            confined = REAL_RUN(['/usr/bin/sandbox-exec', '-f', str(profile), str(executable), str(output), str(victim)], stdin=subprocess.DEVNULL, close_fds=True, capture_output=True, text=True, env={}, timeout=10)
            self.assertEqual(confined.returncode, 0, confined.stderr)
            self.assertEqual(confined.stdout.strip(), '-1 -1')
            G.verify_directory_roots(roots)
            self.assertEqual((victim / 'canary').read_bytes(), b'outside original')
            control = REAL_RUN([str(executable), str(output), str(victim)], stdin=subprocess.DEVNULL, close_fds=True, capture_output=True, text=True, env={}, timeout=10)
            self.assertEqual(control.returncode, 0, control.stderr)
            self.assertEqual(control.stdout.strip(), '0 0')
            self.assertTrue(output.is_symlink())
            with self.assertRaises(G.GenerationError):
                G.verify_directory_roots(roots)
            self.assertEqual((victim / 'canary').read_bytes(), b'outside original')


if __name__ == '__main__':
    unittest.main()
